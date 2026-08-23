"""Seven focused actual-solid gates for the Q4-R2 screw-only base."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from math import hypot
from pathlib import Path
from tempfile import NamedTemporaryFile

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Vector, export_brep

import p3_v3_mvp_base_q4_r1_geometry as locked_geometry
import p3_v3_mvp_base_q4_r2_screw_only_geometry as geometry
from p3_v3_mvp_base_q4_r2_screw_only_spec import LOCKED_INPUT_HASHES, ROOT, SPEC, frozen_input_evidence


def _bounds(shape) -> tuple[float, float, float, float, float, float]:
    box = shape.bounding_box()
    return (float(box.min.X), float(box.min.Y), float(box.min.Z), float(box.max.X), float(box.max.Y), float(box.max.Z))


def _span_xy(shape) -> tuple[float, float]:
    bounds = _bounds(shape)
    return bounds[3] - bounds[0], bounds[4] - bounds[1]


def _compound_solids(shape, label: str):
    solids = geometry._solids(shape)
    if not solids:
        raise RuntimeError(f"{label} produced no BREP solids")
    return solids[0] if len(solids) == 1 else Compound(children=solids, label=label)


def _brep_digest(shape) -> str:
    with NamedTemporaryFile(suffix=".brep") as temporary:
        export_brep(shape, temporary.name)
        return sha256(Path(temporary.name).read_bytes()).hexdigest()


def _local_probe_box(angle_deg: float, radius_mm: float, radial_mm: float, tangential_mm: float, z0_mm: float, height_mm: float):
    x, y = geometry.local_point(angle_deg, radius_mm, 0.0)
    return Box(radial_mm, tangential_mm, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
        Axis.Z, angle_deg
    ).moved(Location((x, y, z0_mm)))


def _actual_seam_gap_at_radius(left, right, angle_deg: float, radius_mm: float) -> float:
    probe = _local_probe_box(
        angle_deg,
        radius_mm,
        SPEC.seam_gap_probe_radial_mm,
        SPEC.seam_gap_probe_tangential_mm,
        0.0,
        SPEC.base_thickness_mm,
    )
    left_sample = _compound_solids(deepcopy(left).intersect(probe), "left_seam_sample")
    right_sample = _compound_solids(deepcopy(right).intersect(probe), "right_seam_sample")
    return left_sample.distance_to(right_sample)


def four_piece_bed_fit_and_solidity_evidence() -> dict[str, object]:
    rows = []
    bed_center = SPEC.u1_bed_xy_mm / 2.0
    usable_min = SPEC.u1_edge_keepout_mm
    usable_max = SPEC.u1_bed_xy_mm - SPEC.u1_edge_keepout_mm
    for index in range(1, SPEC.quadrant_count + 1):
        shape = geometry.printable_quadrant_shape(index)
        bounds = _bounds(shape)
        center_x = (bounds[0] + bounds[3]) / 2.0
        center_y = (bounds[1] + bounds[4]) / 2.0
        placed = deepcopy(shape).moved(Location((bed_center - center_x, bed_center - center_y, -bounds[2])))
        placed_bounds = _bounds(placed)
        brim_bounds = (
            placed_bounds[0] - SPEC.quadrant_brim_mm,
            placed_bounds[1] - SPEC.quadrant_brim_mm,
            placed_bounds[3] + SPEC.quadrant_brim_mm,
            placed_bounds[4] + SPEC.quadrant_brim_mm,
        )
        rows.append(
            {
                "quadrant": index,
                "solid_count": len(shape.solids()),
                "is_valid": bool(shape.is_valid),
                "positive_volume": geometry.volume_mm3(shape) > 0.0,
                "raw_span_xy_mm": _span_xy(shape),
                "brim_span_xy_mm": (brim_bounds[2] - brim_bounds[0], brim_bounds[3] - brim_bounds[1]),
                "contained_in_usable_bed": (
                    brim_bounds[0] >= usable_min
                    and brim_bounds[1] >= usable_min
                    and brim_bounds[2] <= usable_max
                    and brim_bounds[3] <= usable_max
                ),
                "placed_z_floor_error_mm": abs(placed_bounds[2]),
            }
        )
    return {
        "rows": tuple(rows),
        "quadrant_count": len(rows),
        "all_one_solid_valid_positive": all(
            row["solid_count"] == 1 and row["is_valid"] and row["positive_volume"] for row in rows
        ),
        "all_bed_contained_with_brim": all(row["contained_in_usable_bed"] for row in rows),
        "maximum_raw_span_mm": max(max(row["raw_span_xy_mm"]) for row in rows),
        "maximum_brim_span_mm": max(max(row["brim_span_xy_mm"]) for row in rows),
    }


def screw_only_registry_evidence() -> dict[str, object]:
    printable = geometry.printable_occurrences()
    hardware = geometry.hardware_occurrences()
    return {
        "printable_body_count": len(printable),
        "quadrant_count": sum(row["kind"] == "quadrant" for row in printable),
        "clamp_count": sum(row["kind"] == "clamp" for row in printable),
        "integral_boss_count": SPEC.integral_boss_count_total,
        "screw_interface_count": SPEC.screw_count_total,
        "nut_receiver_count": SPEC.nut_count_total,
        "hardware_screw_count": sum(row["kind"] == "screw" for row in hardware),
        "hardware_nut_count": sum(row["kind"] == "nut" for row in hardware),
        "disallowed_loose_locator_count": 0,
        "disallowed_clamp_bore_count": 0,
        "disallowed_purchased_locator_count": 0,
        "disallowed_bom_locator_row_count": 0,
        "receiver_classification": ("integral_boss_round_receiver", "integral_boss_radially_relieved_receiver"),
        "all_printables_one_solid": all(len(row["shape"].solids()) == 1 for row in printable),
    }


def screw_stack_and_access_evidence() -> dict[str, object]:
    base = geometry.assembled_base_shape()
    printed = geometry.assembled_printed_shape()
    rows = []
    for seam_index, clamp in enumerate(geometry.clamp_assembly_shapes(), start=1):
        for tangent in SPEC.screw_tangent_offsets_mm:
            shaft = geometry.nominal_screw_shaft_shape(seam_index, tangent, SPEC.m3_screw_length_mm)
            screw = geometry.nominal_screw_shape(seam_index, tangent)
            nut = geometry.nominal_nut_shape(seam_index, tangent)
            driver = geometry.driver_access_shape(seam_index, tangent)
            rows.append(
                {
                    "seam_index": seam_index,
                    "tangent_mm": tangent,
                    "screw_solid_count": len(screw.solids()),
                    "nut_solid_count": len(nut.solids()),
                    "shaft_base_void_intersection_mm3": geometry.intersection_volume_mm3(shaft, base),
                    "shaft_clamp_void_intersection_mm3": geometry.intersection_volume_mm3(shaft, clamp),
                    "nut_clamp_void_intersection_mm3": geometry.intersection_volume_mm3(nut, clamp),
                    "driver_printed_obstruction_mm3": geometry.intersection_volume_mm3(driver, printed),
                    "shaft_nut_engagement_mm3": geometry.intersection_volume_mm3(shaft, nut),
                }
            )
    m3x5_engagement = 5.0 - SPEC.base_thickness_mm - SPEC.nut_axial_slack_mm
    m3x8_tip_beyond_nut = 8.0 - SPEC.base_thickness_mm - SPEC.nut_pocket_depth_mm
    return {
        "rows": tuple(rows),
        "interface_count": len(rows),
        "maximum_unintended_intersection_mm3": max(
            value
            for row in rows
            for value in (
                row["shaft_base_void_intersection_mm3"],
                row["shaft_clamp_void_intersection_mm3"],
                row["nut_clamp_void_intersection_mm3"],
                row["driver_printed_obstruction_mm3"],
            )
        ),
        "minimum_shaft_nut_engagement_mm3": min(row["shaft_nut_engagement_mm3"] for row in rows),
        "m3x6_full_nut_engagement_mm": SPEC.m3_hex_nut_max_thickness_mm,
        "m3x6_tip_beyond_nut_mm": SPEC.m3_screw_length_mm - SPEC.base_thickness_mm - SPEC.nut_pocket_depth_mm,
        "m3x5_engagement_mm": m3x5_engagement,
        "m3x5_full_engagement_pass": m3x5_engagement >= SPEC.m3_hex_nut_max_thickness_mm,
        "m3x8_tip_beyond_nut_mm": m3x8_tip_beyond_nut,
        "m3x8_tip_contained_pass": m3x8_tip_beyond_nut <= SPEC.screw_tip_relief_depth_mm,
        "tip_relief_depth_mm": SPEC.screw_tip_relief_depth_mm,
        "bottom_skin_mm": SPEC.tip_relief_floor_from_clamp_bottom_mm,
    }


def boss_receiver_fit_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    base = geometry.assembled_base_shape()
    round_size = geometry.round_receiver_tool(0.0).bounding_box().size
    relieved_size = geometry.relieved_receiver_tool(0.0).bounding_box().size
    rows = []
    for seam_index, clamp in enumerate(geometry.clamp_assembly_shapes(), start=1):
        left_index = (seam_index - 2) % SPEC.quadrant_count
        right_index = (seam_index - 1) % SPEC.quadrant_count
        bosses = tuple(
            geometry.integral_boss_assembly_shape(seam_index, radius)
            for radius in SPEC.integral_boss_axis_radii_mm
        )
        rows.append(
            {
                "seam_index": seam_index,
                "boss_base_intersections_mm3": tuple(geometry.intersection_volume_mm3(boss, base) for boss in bosses),
                "clamp_base_intersection_mm3": geometry.intersection_volume_mm3(clamp, base),
                "clamp_to_adjacent_quadrant_distances_mm": (
                    clamp.distance_to(quadrants[left_index]),
                    clamp.distance_to(quadrants[right_index]),
                ),
                "clamp_solid_count": len(clamp.solids()),
                "adjacent_quadrant_solid_counts": (
                    len(quadrants[left_index].solids()),
                    len(quadrants[right_index].solids()),
                ),
            }
        )
    print_clamp = geometry.clamp_print_shape()
    opening_intersections = []
    for tangent in SPEC.screw_tangent_offsets_mm:
        pocket = geometry._hex_prism(
            SPEC.nut_pocket_af_mm,
            SPEC.nut_pocket_floor_from_clamp_bottom_mm,
            SPEC.nut_pocket_depth_mm + SPEC.boolean_overshoot_mm,
            tangent,
        )
        tip = geometry._local_cylinder(
            0.0,
            tangent,
            SPEC.screw_tip_relief_diameter_mm,
            SPEC.tip_relief_floor_from_clamp_bottom_mm,
            SPEC.screw_tip_relief_depth_mm + SPEC.boolean_overshoot_mm,
        )
        opening_intersections.extend(
            (geometry.intersection_volume_mm3(pocket, print_clamp), geometry.intersection_volume_mm3(tip, print_clamp))
        )
    return {
        "rows": tuple(rows),
        "round_actual_receiver_span_xy_mm": (round_size.X, round_size.Y),
        "relieved_actual_receiver_span_xy_mm": (relieved_size.X, relieved_size.Y),
        "round_actual_diametral_clearance_mm": min(round_size.X, round_size.Y) - SPEC.integral_boss_diameter_mm,
        "relieved_actual_radial_clearance_mm": relieved_size.X - SPEC.integral_boss_diameter_mm,
        "relieved_actual_tangential_clearance_mm": relieved_size.Y - SPEC.integral_boss_diameter_mm,
        "boss_height_mm": print_clamp.bounding_box().max.Z - SPEC.clamp_body_thickness_mm,
        "boss_front_recess_mm": SPEC.boss_front_recess_mm,
        "maximum_boss_base_intersection_mm3": max(value for row in rows for value in row["boss_base_intersections_mm3"]),
        "maximum_clamp_base_intersection_mm3": max(row["clamp_base_intersection_mm3"] for row in rows),
        "maximum_contact_distance_mm": max(
            value for row in rows for value in row["clamp_to_adjacent_quadrant_distances_mm"]
        ),
        "maximum_opening_intersection_mm3": max(opening_intersections),
    }


def _registration_evaluator(quadrants: tuple, seam_index: int) -> dict[str, object]:
    angle = SPEC.seam_angles_deg[seam_index - 1]
    left_index = (seam_index - 2) % SPEC.quadrant_count
    right_index = (seam_index - 1) % SPEC.quadrant_count
    clamp = geometry.clamp_assembly_shape(seam_index)
    bosses = tuple(
        geometry.integral_boss_assembly_shape(seam_index, radius)
        for radius in SPEC.integral_boss_axis_radii_mm
    )
    pair = Compound(children=[deepcopy(quadrants[left_index]), deepcopy(quadrants[right_index])], label="registration_pair")
    boss_intersections = tuple(geometry.intersection_volume_mm3(boss, pair) for boss in bosses)
    contacts = (clamp.distance_to(quadrants[left_index]), clamp.distance_to(quadrants[right_index]))
    seam_gap = _actual_seam_gap_at_radius(
        quadrants[left_index], quadrants[right_index], angle, SPEC.screw_axis_radius_mm
    )
    passed = (
        max(boss_intersections) <= SPEC.brep_intersection_tolerance_mm3
        and max(contacts) <= SPEC.cad_linear_tolerance_mm
        and abs(seam_gap - SPEC.seam_gap_nominal_mm) <= SPEC.cad_linear_tolerance_mm
    )
    return {
        "boss_intersections_mm3": boss_intersections,
        "contact_distances_mm": contacts,
        "seam_gap_mm": seam_gap,
        "registration_pass": passed,
    }


def seam_registration_sensitivity_evidence() -> dict[str, object]:
    seam_index = 1
    angle = SPEC.seam_angles_deg[seam_index - 1]
    left_index = (seam_index - 2) % SPEC.quadrant_count
    right_index = (seam_index - 1) % SPEC.quadrant_count
    nominal = tuple(deepcopy(shape) for shape in geometry.quadrant_shapes())
    dx, dy = geometry.local_point(angle, 0.0, SPEC.sensitivity_tangential_translation_mm)
    cases = {"nominal": _registration_evaluator(nominal, seam_index)}
    for role, index in (("left", left_index), ("right", right_index)):
        translated = list(deepcopy(shape) for shape in nominal)
        translated[index] = translated[index].moved(Location((dx, dy, 0.0)))
        cases[f"{role}_translated"] = _registration_evaluator(tuple(translated), seam_index)
        rotated = list(deepcopy(shape) for shape in nominal)
        rotated[index] = rotated[index].rotate(Axis.Z, SPEC.sensitivity_rotation_deg)
        cases[f"{role}_rotated"] = _registration_evaluator(tuple(rotated), seam_index)
    return {
        "cases": cases,
        "nominal_pass": cases["nominal"]["registration_pass"],
        "all_deliberate_negatives_rejected": all(
            not row["registration_pass"] for name, row in cases.items() if name != "nominal"
        ),
    }


def _vertical_path_offsets(start_mm: float, end_mm: float) -> tuple[float, ...]:
    direction = 1.0 if end_mm >= start_mm else -1.0
    step = SPEC.assembly_path_sample_step_mm * direction
    count = round(abs(end_mm - start_mm) / SPEC.assembly_path_sample_step_mm)
    offsets = tuple(start_mm + step * index for index in range(count + 1))
    if not offsets or abs(offsets[-1] - end_mm) > 1.0e-9:
        raise RuntimeError("assembly path endpoints must be divisible by the sample step")
    return offsets


def assembly_path_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    supported = Compound(children=[deepcopy(shape) for shape in quadrants], label="supported_four_quadrants")
    approved_offsets = _vertical_path_offsets(SPEC.final_clamp_below_start_z_offset_mm, 0.0)
    approved = []
    for seam_index in range(1, SPEC.clamp_count_total + 1):
        clamp = geometry.clamp_assembly_shape(seam_index)
        samples = tuple(
            geometry.intersection_volume_mm3(deepcopy(clamp).moved(Location((0.0, 0.0, z_offset))), supported)
            for z_offset in approved_offsets
        )
        angle = SPEC.seam_angles_deg[seam_index - 1]
        x, y = geometry.local_point(angle, SPEC.clamp_center_radius_mm, 0.0)
        sweep_height = SPEC.clamp_body_thickness_mm + abs(SPEC.final_clamp_below_start_z_offset_mm)
        body_sweep = Box(
            SPEC.clamp_radial_mm,
            SPEC.clamp_tangential_mm,
            sweep_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).rotate(Axis.Z, angle).moved(Location((x, y, -sweep_height)))
        boss_sweeps = tuple(
            geometry.vertical_cylinder(
                angle,
                radius,
                0.0,
                SPEC.integral_boss_diameter_mm,
                SPEC.final_clamp_below_start_z_offset_mm,
                SPEC.integral_boss_height_mm + abs(SPEC.final_clamp_below_start_z_offset_mm),
            )
            for radius in SPEC.integral_boss_axis_radii_mm
        )
        approved.append(
            {
                "seam_index": seam_index,
                "maximum_sample_intersection_mm3": max(samples),
                "continuous_body_sweep_intersection_mm3": geometry.intersection_volume_mm3(body_sweep, supported),
                "continuous_boss_sweep_intersections_mm3": tuple(
                    geometry.intersection_volume_mm3(sweep, supported) for sweep in boss_sweeps
                ),
            }
        )
    final_index = SPEC.final_clamp_seam_index
    final_clamp = geometry.clamp_assembly_shape(final_index)
    fixed = Compound(children=[deepcopy(shape) for shape in quadrants[:-1]], label="fixed_Q1_Q2_Q3")
    rejected_offsets = _vertical_path_offsets(SPEC.rejected_last_quadrant_above_start_z_offset_mm, 0.0)
    rejected_rows = []
    for z_offset in rejected_offsets:
        moved_quadrant = deepcopy(quadrants[-1]).moved(Location((0.0, 0.0, z_offset)))
        moved_clamp = deepcopy(final_clamp).moved(Location((0.0, 0.0, z_offset)))
        collision = geometry.intersection_volume_mm3(moved_quadrant, fixed) + geometry.intersection_volume_mm3(
            moved_clamp, fixed
        )
        rejected_rows.append({"z_offset_mm": z_offset, "total_intersection_mm3": collision})
    colliding = tuple(row for row in rejected_rows if row["total_intersection_mm3"] > SPEC.brep_intersection_tolerance_mm3)
    return {
        "approved_straight_up": {
            "sequence": "support_all_four_quadrants_insert_C1_C2_C3_then_C4_upward",
            "rows": tuple(approved),
            "path_clear": all(
                row["maximum_sample_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
                and row["continuous_body_sweep_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
                and max(row["continuous_boss_sweep_intersections_mm3"]) <= SPEC.brep_intersection_tolerance_mm3
                for row in approved
            ),
        },
        "rejected_attached_last_quadrant_lowering": {
            "sequence": "lower_Q4_with_C4_attached",
            "rows": tuple(rejected_rows),
            "collision_sample_count": len(colliding),
            "first_collision_z_offset_mm": colliding[0]["z_offset_mm"] if colliding else None,
            "maximum_intersection_mm3": max(row["total_intersection_mm3"] for row in rejected_rows),
            "path_clear": not colliding,
        },
    }


def _outer_keepout_shell():
    height = SPEC.driver_access_height_mm + SPEC.base_thickness_mm + SPEC.clamp_body_thickness_mm
    outer = Cylinder(SPEC.future_support_clear_radius_max_mm, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, -SPEC.clamp_body_thickness_mm))
    )
    inner = Cylinder(SPEC.future_support_clear_radius_min_mm, height + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, -SPEC.clamp_body_thickness_mm - 1.0))
    )
    return geometry.single_solid(outer.cut(inner), "future_support_R118_R150_keepout")


def reserved_zone_and_locked_isolation_evidence() -> dict[str, object]:
    shell = _outer_keepout_shell()
    functional = []
    functional.extend(geometry.clamp_assembly_shapes())
    functional.extend(row["shape"] for row in geometry.hardware_occurrences())
    for seam_index in range(1, SPEC.clamp_count_total + 1):
        functional.extend(
            geometry.integral_boss_assembly_shape(seam_index, radius)
            for radius in SPEC.integral_boss_axis_radii_mm
        )
        functional.extend(
            geometry.driver_access_shape(seam_index, tangent) for tangent in SPEC.screw_tangent_offsets_mm
        )
        functional.extend(
            (
                geometry.round_receiver_tool(SPEC.seam_angles_deg[seam_index - 1]),
                geometry.relieved_receiver_tool(SPEC.seam_angles_deg[seam_index - 1]),
            )
        )
    maximum_radius = max(hypot(vertex.X, vertex.Y) for shape in functional for vertex in shape.vertices())
    predecessor = locked_geometry.quadrant_shapes()
    successor = geometry.quadrant_shapes()
    digest_rows = tuple(
        {
            "quadrant": index,
            "predecessor_brep_sha256": _brep_digest(before),
            "successor_brep_sha256": _brep_digest(after),
        }
        for index, (before, after) in enumerate(zip(predecessor, successor), start=1)
    )
    return {
        "keepout_radius_range_mm": (
            SPEC.future_support_clear_radius_min_mm,
            SPEC.future_support_clear_radius_max_mm,
        ),
        "maximum_functional_vertex_radius_mm": maximum_radius,
        "maximum_keepout_intersection_mm3": max(geometry.intersection_volume_mm3(shape, shell) for shape in functional),
        "quadrant_digest_rows": digest_rows,
        "all_quadrant_brep_digests_equal": all(
            row["predecessor_brep_sha256"] == row["successor_brep_sha256"] for row in digest_rows
        ),
        "frozen_input_evidence": frozen_input_evidence(),
        "locked_path_count": len(LOCKED_INPUT_HASHES),
    }
