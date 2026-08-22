"""Focused actual-solid CAD evidence for the Q4-R4 functional MVP base."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from math import hypot
from pathlib import Path

from build123d import Align, Compound, Cylinder, Location

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_geometry as geometry
from p3_v3_mvp_base_q4_r4_functional_centered_step_lap_spec import NAMESPACE, ROOT, SPEC


FROZEN_TREE_HASHES = {
    "p3_v3_mvp_base_q4_r1": "477f855bfda1f12533e080feee45028f1cc8e94d501ce6e270d4e097920f6e93",
    "p3_v3_mvp_base_q4_r2_screw_only": "b26a17f40e6767b878c44558bf7e7b41b3da9aa11f62b5b4d8b5315f70a802c2",
    "p3_v3_mvp_base_q4_r3_integral_lap": "8c9fde193bc35551c8d8eab45709da3a5187d5b35893180971218242738e5cd4",
}
AUTHORITY_HASHES = {
    "p3_v3_direct_gear_race_guidance_r2_spec.py": "0007955b05d68aa4b2b53926928dd142b0cd6c3412fc3a294703e7ab5d71679a",
    "p3_v3_direct_gear_race_guidance_r2_geometry.py": "4cac88b03c6872f032c9c7022b4192745b385b82da91b9cad323772482d5a13d",
    "docs/p3-v3-direct-gear-race-guidance-r2-frozen-handoff.md": "03cf057036166c9497cf37025616cdeb7bd2e582b1c5f7c464eec23ea80078cc",
}


def _tree_files(namespace: str) -> tuple[Path, ...]:
    files = [path for path in ROOT.glob(f"{namespace}*") if path.is_file()]
    files.extend(path for path in (ROOT / "tests").glob(f"test_{namespace}*") if path.is_file())
    model_root = ROOT / "models" / namespace
    if model_root.exists():
        files.extend(
            path for path in model_root.rglob("*")
            if path.is_file() and "__cadgen__" not in path.parts and "__pycache__" not in path.parts
        )
    return tuple(sorted(set(files), key=lambda path: path.as_posix()))


def namespace_tree_hash(namespace: str) -> str:
    digest = sha256()
    for path in _tree_files(namespace):
        relative = path.relative_to(ROOT).as_posix().encode()
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def version_isolation_evidence() -> dict[str, object]:
    actual_trees = {namespace: namespace_tree_hash(namespace) for namespace in FROZEN_TREE_HASHES}
    actual_authority = {
        relative: sha256((ROOT / relative).read_bytes()).hexdigest()
        for relative in AUTHORITY_HASHES
    }
    return {
        "expected_trees": FROZEN_TREE_HASHES,
        "actual_trees": actual_trees,
        "all_frozen_tree_hashes_match": actual_trees == FROZEN_TREE_HASHES,
        "expected_authority": AUTHORITY_HASHES,
        "actual_authority": actual_authority,
        "authority_hashes_match": actual_authority == AUTHORITY_HASHES,
    }


def part_registry_evidence() -> dict[str, object]:
    rows = geometry.printable_occurrences()
    forbidden = ("clamp", "bridge", "dowel", "carrier", "ring", "motor", "insert")
    labels = tuple(row["label"] for row in rows)
    return {
        "printable_count": len(rows),
        "labels": labels,
        "roles": tuple(row["kind"] for row in rows),
        "orientations": tuple(row["orientation"] for row in rows),
        "all_one_solid_valid": all(
            len(row["shape"].solids()) == 1 and row["shape"].is_valid and row["shape"].volume > 0.0
            for row in rows
        ),
        "forbidden_occurrence_count": sum(any(word in label.lower() for word in forbidden) for label in labels),
    }


def datum_flatness_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    probe_depth = 0.01
    rows = []
    for index, shape in enumerate(quadrants, 1):
        box = shape.bounding_box()
        contact_probe = Cylinder(
            SPEC.base_outer_radius_mm + 1.0,
            probe_depth,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((0.0, 0.0, SPEC.plate_bottom_z_mm)))
        rows.append({
            "quadrant": index,
            "min_z_mm": float(box.min.Z),
            "max_z_mm": float(box.max.Z),
            "bottom_contact_area_mm2": geometry.intersection_volume_mm3(shape, contact_probe) / probe_depth,
            "has_boss": index != 4,
        })
    return {
        "rows": tuple(rows),
        "plate_bottom_z_mm": SPEC.plate_bottom_z_mm,
        "nominal_polymer_top_z_mm": SPEC.plate_top_z_mm,
        "boss_top_z_mm": SPEC.screw_under_head_z_mm,
        "all_min_z_exact": all(abs(row["min_z_mm"] - SPEC.plate_bottom_z_mm) <= 1.0e-7 for row in rows),
        "minimum_bottom_contact_area_mm2": min(row["bottom_contact_area_mm2"] for row in rows),
        "bottom_coplanarity_mm": max(row["min_z_mm"] for row in rows) - min(row["min_z_mm"] for row in rows),
    }


def broad_lap_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    # Thin actual-solid slice approaches the split plane closely enough to
    # measure the AF6.4 chamfer mouth rather than averaging down its 0.30 lead.
    probe_depth = 0.0001
    rows = []
    for lap_index, (name, angle, upper, lower) in enumerate(geometry.LAPS):
        upper_probe = geometry.donor_plan_tool(angle, SPEC.lap_split_z_mm, probe_depth)
        lower_probe = geometry.donor_plan_tool(angle, SPEC.lap_split_z_mm - probe_depth, probe_depth)
        upper_area = geometry.intersection_volume_mm3(quadrants[upper - 1], upper_probe) / probe_depth
        lower_area = geometry.intersection_volume_mm3(quadrants[lower - 1], lower_probe) / probe_depth
        rows.append({
            "name": name,
            "upper": upper,
            "lower": lower,
            "upper_bearing_area_mm2": upper_area,
            "lower_bearing_area_mm2": lower_area,
            "mutual_contact_area_mm2": min(upper_area, lower_area),
            "gross_area_mm2": SPEC.lap_gross_area_mm2,
            "upper_thickness_mm": SPEC.plate_top_z_mm - SPEC.lap_split_z_mm,
            "lower_thickness_mm": SPEC.lap_split_z_mm - SPEC.plate_bottom_z_mm,
            "pair_intersection_mm3": geometry.intersection_volume_mm3(
                quadrants[upper - 1], quadrants[lower - 1]
            ),
        })
    pairwise = tuple(
        geometry.intersection_volume_mm3(quadrants[i], quadrants[j])
        for i in range(4) for j in range(i + 1, 4)
    )
    return {
        "rows": tuple(rows),
        "precedence": tuple((row["name"], row["upper"], row["lower"]) for row in rows),
        "minimum_upper_bearing_area_mm2": min(row["upper_bearing_area_mm2"] for row in rows),
        "minimum_mutual_contact_area_mm2": min(row["mutual_contact_area_mm2"] for row in rows),
        "maximum_pairwise_intersection_mm3": max(pairwise),
        "exterior_polymer_step_mm": 0.0,
    }


def hardware_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    printed = geometry.assembled_printed_shape()
    rows = []
    for lap_index, (name, _, upper, lower) in enumerate(geometry.LAPS):
        for radius in SPEC.seam_screw_axis_radii_mm:
            boss = geometry.bearing_boss_shape(lap_index, radius)
            hole = geometry.upper_clearance_tool(lap_index, radius)
            trap = geometry.nut_trap_tool(lap_index, radius)
            relief = geometry.tip_relief_tool(lap_index, radius)
            shaft = geometry.nominal_screw_shaft_shape(lap_index, radius)
            nut = geometry.nominal_nut_shape(lap_index, radius)
            rows.append({
                "seam": name,
                "radius_mm": radius,
                "boss_material_mm3": geometry.intersection_volume_mm3(boss, quadrants[upper - 1]),
                "upper_hole_residual_mm3": geometry.intersection_volume_mm3(hole, quadrants[upper - 1]),
                "trap_residual_mm3": geometry.intersection_volume_mm3(trap, quadrants[lower - 1]),
                "relief_residual_mm3": geometry.intersection_volume_mm3(relief, quadrants[lower - 1]),
                "shaft_printed_intersection_mm3": geometry.intersection_volume_mm3(shaft, printed),
                "nut_printed_intersection_mm3": geometry.intersection_volume_mm3(nut, printed),
                "driver_obstruction_mm3": geometry.intersection_volume_mm3(
                    geometry.driver_path_shape(lap_index, radius), printed
                ),
                "top_nut_insertion_obstruction_mm3": geometry.intersection_volume_mm3(
                    geometry.nut_insertion_path_shape(lap_index, radius), quadrants[lower - 1]
                ),
            })
    candidate_lengths = (6.0, 8.0, 10.0, 12.0)
    tips = {length: SPEC.screw_under_head_z_mm - length for length in candidate_lengths}
    return {
        "rows": tuple(rows),
        "interface_count": len(rows),
        "boss_count": len(rows),
        "hole_count": len(rows),
        "trap_count": len(rows),
        "trap_af_mm": SPEC.nut_trap_af_mm,
        "trap_depth_mm": SPEC.nut_trap_depth_mm,
        "tip_relief_bottom_z_mm": SPEC.tip_relief_bottom_z_mm,
        "underside_floor_mm": SPEC.tip_relief_bottom_z_mm - SPEC.plate_bottom_z_mm,
        "nut_thread_engagement_mm": SPEC.m3_nut_max_thickness_mm,
        "candidate_tip_z_mm": tips,
        "accepted_lengths_mm": tuple(
            length for length, tip in tips.items()
            if tip >= SPEC.tip_relief_bottom_z_mm and length <= SPEC.m3_screw_length_mm
        ),
        "maximum_void_residual_mm3": max(
            max(
                row["upper_hole_residual_mm3"],
                row["trap_residual_mm3"],
                row["relief_residual_mm3"],
                row["shaft_printed_intersection_mm3"],
                row["nut_printed_intersection_mm3"],
                row["driver_obstruction_mm3"],
                row["top_nut_insertion_obstruction_mm3"],
            )
            for row in rows
        ),
        "minimum_boss_material_mm3": min(row["boss_material_mm3"] for row in rows),
        "underside_tool_dependency": False,
    }


def top_down_assembly_sweep_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    order = (4, 3, 2, 1)
    offsets = tuple(
        SPEC.assembly_start_z_mm - index * SPEC.assembly_path_step_mm
        for index in range(int(SPEC.assembly_start_z_mm / SPEC.assembly_path_step_mm) + 1)
    )
    seated = []
    rows = []
    for moving_index in order:
        if seated:
            fixed = Compound(children=[deepcopy(quadrants[index - 1]) for index in seated])
            intersections = tuple(
                geometry.intersection_volume_mm3(
                    deepcopy(quadrants[moving_index - 1]).moved(Location((0.0, 0.0, offset))),
                    fixed,
                )
                for offset in offsets
            )
        else:
            intersections = tuple(0.0 for _ in offsets)
        rows.append({
            "moving_quadrant": moving_index,
            "fixed_quadrants": tuple(seated),
            "sample_count": len(offsets),
            "maximum_intersection_mm3": max(intersections),
        })
        seated.append(moving_index)
    return {
        "rows": tuple(rows),
        "order": order,
        "offsets_mm": offsets,
        "maximum_intersection_mm3": max(row["maximum_intersection_mm3"] for row in rows),
        "q1_closes_both_seams": tuple(
            name for name, _, upper, _ in geometry.LAPS if upper == 1
        ) == ("S12", "S41"),
    }


def mount_parity_evidence() -> dict[str, object]:
    printed = geometry.assembled_printed_shape()
    slot_tools = geometry.motor_slot_tools()
    spine_tools = geometry.spine_mount_tools()
    motor_rows = tuple(
        {
            "angle_deg": angle,
            "radius_mm": radius,
            "tangent_mm": tangent,
            "width_mm": SPEC.motor_slot_width_mm,
            "overall_length_mm": SPEC.motor_slot_overall_length_mm,
        }
        for angle in SPEC.motor_station_angles_deg
        for radius in SPEC.motor_slot_axis_radii_mm
        for tangent in SPEC.motor_slot_tangent_offsets_mm
    )
    spine_rows = tuple(
        {
            "angle_deg": SPEC.spine_angle_deg,
            "radius_mm": SPEC.spine_center_radius_mm,
            "tangent_mm": tangent,
            "diameter_mm": SPEC.spine_mount_path_diameter_mm,
        }
        for tangent in SPEC.spine_mount_tangent_offsets_mm
    )
    landing_rows = tuple(
        {
            "angle_deg": angle,
            "required_volume_mm3": geometry.volume_mm3(geometry.fixed_tower_landing_volume(angle)),
            "actual_material_mm3": geometry.intersection_volume_mm3(
                geometry.fixed_tower_landing_volume(angle), printed
            ),
        }
        for angle in SPEC.fixed_tower_angles_deg
    )
    old_tools = tuple(
        geometry.vertical_cylinder(
            SPEC.spine_angle_deg,
            SPEC.obsolete_tower_radius_mm,
            tangent,
            3.4,
            SPEC.plate_bottom_z_mm,
            SPEC.plate_nominal_thickness_mm,
        )
        for tangent in SPEC.obsolete_tower_tangent_offsets_mm
    )
    center_tool = Cylinder(
        SPEC.base_inner_radius_mm,
        SPEC.plate_nominal_thickness_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.plate_bottom_z_mm)))
    top_probe_depth = 0.01
    spine_top_bearing = geometry._local_box(
        SPEC.spine_angle_deg,
        SPEC.spine_center_radius_mm - SPEC.spine_foot_radial_mm / 2.0,
        SPEC.spine_center_radius_mm + SPEC.spine_foot_radial_mm / 2.0,
        -SPEC.spine_foot_tangential_mm / 2.0,
        SPEC.spine_foot_tangential_mm / 2.0,
        SPEC.plate_top_z_mm - top_probe_depth,
        top_probe_depth,
    )
    spine_top_bearing = spine_top_bearing.cut(
        *(deepcopy(tool) for tool in spine_tools)
    )
    required_spine_top_volume = geometry.volume_mm3(spine_top_bearing)
    return {
        "center_opening_diameter_mm": 2.0 * SPEC.base_inner_radius_mm,
        "center_opening_residual_mm3": geometry.intersection_volume_mm3(center_tool, printed),
        "motor_rows": motor_rows,
        "motor_slot_count": len(motor_rows),
        "maximum_motor_slot_residual_mm3": max(
            geometry.intersection_volume_mm3(tool, printed) for tool in slot_tools
        ),
        "spine_rows": spine_rows,
        "spine_path_count": len(spine_rows),
        "maximum_spine_path_residual_mm3": max(
            geometry.intersection_volume_mm3(tool, printed) for tool in spine_tools
        ),
        "fixed_tower_rows": landing_rows,
        "fixed_tower_count": len(landing_rows),
        "minimum_fixed_landing_coverage_ratio": min(
            row["actual_material_mm3"] / row["required_volume_mm3"] for row in landing_rows
        ),
        "spine_top_bearing_coverage_ratio": geometry.intersection_volume_mm3(
            spine_top_bearing, printed
        ) / required_spine_top_volume,
        "spine_top_bearing_z_mm": SPEC.plate_top_z_mm,
        "spine_removed_before_quadrant_separation": True,
        "obsolete_300_r119p5_paths_are_solid": all(
            geometry.intersection_volume_mm3(tool, printed) > 0.95 * geometry.volume_mm3(tool)
            for tool in old_tools
        ),
        "motor_service_travel_mm": SPEC.motor_service_travel_mm,
        "motor_powered_range_mm": (SPEC.motor_powered_q_min_mm, SPEC.motor_powered_q_max_mm),
        "output_axis_radius_mm": SPEC.motor_output_axis_radius_mm,
    }


def _max_vertex_radius(shape) -> float:
    return max(hypot(float(vertex.X), float(vertex.Y)) for vertex in shape.vertices())


def keepout_and_service_sweep_evidence() -> dict[str, object]:
    seam_envelope = geometry.seam_feature_envelope()
    q_samples = (-SPEC.motor_service_travel_mm, SPEC.motor_powered_q_min_mm, 0.0,
                 SPEC.motor_powered_q_max_mm, SPEC.motor_service_travel_mm)
    motor_rows = []
    for q_mm in q_samples:
        shapes = geometry.locked_motor_service_shapes(q_mm)
        motor_rows.append({
            "q_mm": q_mm,
            "maximum_intersection_mm3": max(
                geometry.intersection_volume_mm3(seam_envelope, shape) for shape in shapes
            ),
            "minimum_clearance_mm": min(seam_envelope.distance_to(shape) for shape in shapes),
        })
    locked_support_shapes = geometry.locked_tower_service_shapes()
    support_mount_paths = geometry.spine_mount_tools()
    fixed_landings = tuple(
        geometry.fixed_tower_landing_volume(angle) for angle in SPEC.fixed_tower_angles_deg
    )
    spine_landing = geometry.spine_landing_volume()
    hall_shapes = geometry.hall_keepout_shapes()
    ring_keepout = geometry.ring_motion_plan_keepout()
    return {
        "motor_rows": tuple(motor_rows),
        "maximum_motor_sweep_intersection_mm3": max(row["maximum_intersection_mm3"] for row in motor_rows),
        "minimum_motor_sweep_clearance_mm": min(row["minimum_clearance_mm"] for row in motor_rows),
        "maximum_locked_support_service_intersection_mm3": max(
            geometry.intersection_volume_mm3(seam_envelope, shape) for shape in locked_support_shapes
        ),
        "minimum_locked_support_service_clearance_mm": min(
            seam_envelope.distance_to(shape) for shape in locked_support_shapes
        ),
        "maximum_spine_mount_path_intersection_mm3": max(
            geometry.intersection_volume_mm3(seam_envelope, shape) for shape in support_mount_paths
        ),
        "minimum_spine_mount_path_clearance_mm": min(
            seam_envelope.distance_to(shape) for shape in support_mount_paths
        ),
        "maximum_fixed_landing_shared_polymer_mm3": max(
            geometry.intersection_volume_mm3(seam_envelope, shape) for shape in fixed_landings
        ),
        "spine_landing_shared_polymer_mm3": geometry.intersection_volume_mm3(
            seam_envelope, spine_landing
        ),
        "maximum_ring_intersection_mm3": geometry.intersection_volume_mm3(seam_envelope, ring_keepout),
        "ring_clearance_mm": seam_envelope.distance_to(ring_keepout),
        "maximum_hall_intersection_mm3": max(
            geometry.intersection_volume_mm3(seam_envelope, shape) for shape in hall_shapes
        ),
        "minimum_hall_clearance_mm": min(seam_envelope.distance_to(shape) for shape in hall_shapes),
        "maximum_seam_feature_radius_mm": max(
            _max_vertex_radius(geometry.receiver_plan_tool(
                angle, SPEC.plate_bottom_z_mm, SPEC.plate_nominal_thickness_mm
            ))
            for _, angle, _, _ in geometry.LAPS
        ),
        "receiver_worst_plan_corner_mm": hypot(SPEC.receiver_r_max_mm, SPEC.receiver_t_max_mm),
        "electronics_cut_count": 0,
    }


def u1_fit_evidence() -> dict[str, object]:
    rows = []
    for row in geometry.printable_occurrences():
        box = row["shape"].bounding_box()
        span = (float(box.size.X), float(box.size.Y), float(box.size.Z))
        rows.append({
            "name": row["name"],
            "span_mm": span,
            "span_with_brim_xy_mm": (
                span[0] + 2.0 * SPEC.quadrant_brim_mm,
                span[1] + 2.0 * SPEC.quadrant_brim_mm,
            ),
            "z_floor_error_mm": abs(float(box.min.Z)),
            "one_solid": len(row["shape"].solids()) == 1,
        })
    return {
        "rows": tuple(rows),
        "all_fit": all(max(row["span_with_brim_xy_mm"]) <= SPEC.u1_usable_xy_mm for row in rows),
        "all_on_bed": all(row["z_floor_error_mm"] <= 1.0e-7 for row in rows),
        "all_one_solid": all(row["one_solid"] for row in rows),
    }
