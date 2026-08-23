"""Focused physical-failure evidence for the KAGE B0 base MVP.

Every function measures actual source BREP where that is meaningful.  The
fixture evaluator additionally accepts placement overrides so the same gate is
proved to reject deliberate shim and axis-offset fixtures.
"""

from __future__ import annotations

from copy import deepcopy
from math import hypot, pi

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Vector

import p3_v3_mvp_base_q4_r1_geometry as geometry
from p3_v3_mvp_base_q4_r1_spec import SPEC


def _bounds(shape) -> tuple[float, float, float, float, float, float]:
    box = shape.bounding_box()
    return (
        float(box.min.X),
        float(box.min.Y),
        float(box.min.Z),
        float(box.max.X),
        float(box.max.Y),
        float(box.max.Z),
    )


def _span_xy(shape) -> tuple[float, float]:
    bounds = _bounds(shape)
    return bounds[3] - bounds[0], bounds[4] - bounds[1]


def topology_and_bed_evidence() -> dict[str, object]:
    rows = []
    bed_center = SPEC.u1_bed_xy_mm / 2.0
    usable_min = SPEC.u1_edge_keepout_mm
    usable_max = SPEC.u1_bed_xy_mm - SPEC.u1_edge_keepout_mm
    for row in geometry.printable_occurrences():
        shape = row["shape"]
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
                "name": row["name"],
                "kind": row["kind"],
                "solid_count": len(shape.solids()),
                "is_valid": bool(shape.is_valid),
                "positive_volume": geometry.volume_mm3(shape) > 0.0,
                "raw_span_xy_mm": _span_xy(shape),
                "brim_span_xy_mm": (
                    brim_bounds[2] - brim_bounds[0],
                    brim_bounds[3] - brim_bounds[1],
                ),
                "centered_placement_bounds_xy_mm": brim_bounds,
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
        "rows": rows,
        "printable_body_count": len(rows),
        "quadrant_count": sum(row["kind"] == "quadrant" for row in rows),
        "bridge_count": sum(row["kind"] == "bridge" for row in rows),
        "all_one_solid_valid_positive": all(
            row["solid_count"] == 1 and row["is_valid"] and row["positive_volume"] for row in rows
        ),
        "all_bed_contained_with_brim": all(row["contained_in_usable_bed"] for row in rows),
        "maximum_raw_span_mm": max(max(row["raw_span_xy_mm"]) for row in rows),
        "maximum_brim_span_mm": max(max(row["brim_span_xy_mm"]) for row in rows),
    }


def assembled_datum_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    bridges = geometry.bridge_assembly_shapes()
    base = geometry.assembled_base_shape()
    center = Vector(0.0, 0.0, SPEC.base_thickness_mm / 2.0)
    return {
        "base_bounds_mm": _bounds(base),
        "full_assembly_bounds_mm": _bounds(geometry.assembled_shape()),
        "outer_diameter_x_mm": base.bounding_box().size.X,
        "outer_diameter_y_mm": base.bounding_box().size.Y,
        "inner_radius_from_center_mm": base.distance_to(center),
        "quadrant_z_bounds_mm": tuple((shape.bounding_box().min.Z, shape.bounding_box().max.Z) for shape in quadrants),
        "bridge_z_bounds_mm": tuple((shape.bounding_box().min.Z, shape.bounding_box().max.Z) for shape in bridges),
        "quadrant_front_coplanarity_range_mm": (
            max(shape.bounding_box().max.Z for shape in quadrants)
            - min(shape.bounding_box().max.Z for shape in quadrants)
        ),
        "bridge_seat_coplanarity_range_mm": (
            max(shape.bounding_box().max.Z for shape in bridges)
            - min(shape.bounding_box().max.Z for shape in bridges)
        ),
        "bridge_bottom_coplanarity_range_mm": (
            max(shape.bounding_box().min.Z for shape in bridges)
            - min(shape.bounding_box().min.Z for shape in bridges)
        ),
    }


def _compound_solids(shape, label: str):
    solids = geometry._solids(shape)
    if not solids:
        raise RuntimeError(f"{label} produced no BREP solids")
    return solids[0] if len(solids) == 1 else Compound(children=solids, label=label)


def _local_probe_box(
    angle_deg: float,
    radius_mm: float,
    radial_mm: float,
    tangential_mm: float,
    z0_mm: float,
    height_mm: float,
):
    x, y = geometry.local_point(angle_deg, radius_mm, 0.0)
    return Box(
        radial_mm,
        tangential_mm,
        height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).rotate(Axis.Z, angle_deg).moved(Location((x, y, z0_mm)))


def _actual_seam_gap_at_radius(left, right, angle_deg: float, radius_mm: float) -> float:
    probe = _local_probe_box(
        angle_deg,
        radius_mm,
        SPEC.seam_gap_probe_radial_mm,
        SPEC.seam_gap_probe_tangential_mm,
        0.0,
        SPEC.base_thickness_mm,
    )
    left_sample = _compound_solids(deepcopy(left).intersect(probe), "left_seam_face_sample")
    right_sample = _compound_solids(deepcopy(right).intersect(probe), "right_seam_face_sample")
    return left_sample.distance_to(right_sample)


def seam_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    rows = []
    for index in range(SPEC.quadrant_count):
        adjacent = (index + 1) % SPEC.quadrant_count
        seam_angle = SPEC.seam_angles_deg[adjacent]
        face_samples = tuple(
            {
                "radius_mm": radius,
                "measurement_status": "actual_brep_face_gap",
                "normal_gap_mm": _actual_seam_gap_at_radius(
                    quadrants[index], quadrants[adjacent], seam_angle, radius
                ),
            }
            for radius in SPEC.seam_face_sample_radii_mm
        )
        nonface_samples = tuple(
            {
                "radius_mm": radius,
                "measurement_status": "intentionally_non_face_dowel_void",
                "normal_gap_mm": None,
                "interface": (
                    "round_D4p15_split_slip"
                    if radius == SPEC.round_dowel_axis_radius_mm
                    else "radial_capsule_5p15_x_4p15_split_slip"
                ),
            }
            for radius in SPEC.seam_nonface_dowel_radii_mm
        )
        rows.append(
            {
                "pair": (index + 1, adjacent + 1),
                "seam_angle_deg": seam_angle,
                "minimum_brep_distance_mm": quadrants[index].distance_to(quadrants[adjacent]),
                "intersection_volume_mm3": geometry.intersection_volume_mm3(
                    quadrants[index], quadrants[adjacent]
                ),
                "face_samples": face_samples,
                "nonface_samples": nonface_samples,
            }
        )
    actual_face_gaps = tuple(
        sample["normal_gap_mm"]
        for row in rows
        for sample in row["face_samples"]
    )
    return {
        "rows": rows,
        "face_sample_radii_mm": SPEC.seam_face_sample_radii_mm,
        "nonface_dowel_radii_mm": SPEC.seam_nonface_dowel_radii_mm,
        "actual_face_measurement_count": len(actual_face_gaps),
        "intentionally_nonface_measurement_count": sum(
            len(row["nonface_samples"]) for row in rows
        ),
        "maximum_intersection_volume_mm3": max(row["intersection_volume_mm3"] for row in rows),
        "minimum_gap_mm": min(row["minimum_brep_distance_mm"] for row in rows),
        "maximum_gap_mm": max(row["minimum_brep_distance_mm"] for row in rows),
        "minimum_actual_face_gap_mm": min(actual_face_gaps),
        "maximum_actual_face_gap_mm": max(actual_face_gaps),
    }


def _rejected_two_lobed_relief_tool(angle_deg: float = 0.0):
    endpoints = [
        geometry.vertical_cylinder(
            angle_deg,
            SPEC.relief_dowel_axis_radius_mm + radial_offset,
            0.0,
            SPEC.relief_split_slot_tangential_mm,
            -SPEC.boolean_overshoot_mm,
            SPEC.base_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm,
        )
        for radial_offset in SPEC.relief_slot_center_offsets_mm
    ]
    return geometry.single_solid(
        endpoints[0].fuse(endpoints[1]),
        "rejected_two_lobed_D4p15_endpoint_union",
    )


def _slot_brep_measurements(tool, construction: str) -> dict[str, object]:
    local = deepcopy(tool).moved(
        Location((-SPEC.relief_dowel_axis_radius_mm, 0.0, 0.0))
    )
    width_rows = []
    for radial_offset in (
        SPEC.relief_slot_center_offsets_mm[0],
        0.0,
        SPEC.relief_slot_center_offsets_mm[1],
    ):
        probe = Box(
            SPEC.brep_slot_probe_radial_thickness_mm,
            SPEC.relief_split_slot_tangential_mm * 2.0,
            SPEC.base_thickness_mm + 4.0 * SPEC.boolean_overshoot_mm,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((radial_offset, 0.0, SPEC.base_thickness_mm / 2.0)))
        sample = _compound_solids(
            deepcopy(local).intersect(probe),
            f"{construction}_slot_section_{radial_offset}",
        )
        width_rows.append(
            {
                "radial_offset_mm": radial_offset,
                "actual_brep_tangential_width_mm": sample.bounding_box().size.Y,
            }
        )
    box = local.bounding_box()
    minimum_width = min(row["actual_brep_tangential_width_mm"] for row in width_rows)
    minimum_pin_clearance = (
        minimum_width - SPEC.dowel_nominal_diameter_mm
    ) / 2.0
    return {
        "construction": construction,
        "overall_actual_brep_radial_length_mm": box.size.X,
        "overall_actual_brep_tangential_width_mm": box.size.Y,
        "section_widths": tuple(width_rows),
        "minimum_actual_brep_tangential_width_mm": minimum_width,
        "minimum_d4_pin_side_clearance_mm": minimum_pin_clearance,
        "qualifies_constant_width_slot": (
            abs(box.size.X - SPEC.relief_split_slot_radial_mm)
            <= SPEC.cad_linear_tolerance_mm
            and all(
                abs(row["actual_brep_tangential_width_mm"] - SPEC.relief_split_slot_tangential_mm)
                <= SPEC.cad_linear_tolerance_mm
                for row in width_rows
            )
            and minimum_pin_clearance + SPEC.cad_linear_tolerance_mm
            >= SPEC.dowel_diametral_slip_mm / 2.0
        ),
    }


def relief_slot_brep_evidence() -> dict[str, object]:
    return {
        "production_true_capsule": _slot_brep_measurements(
            geometry.relieved_split_slip_tool(0.0),
            "rectangle_plus_semicircular_ends",
        ),
        "rejected_two_lobed_regression": _slot_brep_measurements(
            _rejected_two_lobed_relief_tool(0.0),
            "two_endpoint_cylinders_without_center_rectangle",
        ),
    }


def _outer_keepout_shell():
    height = SPEC.base_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm
    outer = Cylinder(
        SPEC.future_support_clear_radius_max_mm,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, -SPEC.boolean_overshoot_mm)))
    inner = Cylinder(
        SPEC.future_support_clear_radius_min_mm,
        height + 2.0 * SPEC.boolean_overshoot_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, -2.0 * SPEC.boolean_overshoot_mm)))
    return geometry.single_solid(outer.cut(inner), "B1_R118_R150_keepout_probe")


def future_support_keepout_evidence() -> dict[str, object]:
    shell = _outer_keepout_shell()
    removed = []
    for plain, joined in zip(geometry.plain_quadrant_shapes(), geometry.quadrant_shapes()):
        plain_volume = geometry.volume_mm3(deepcopy(plain).intersect(shell))
        joined_volume = geometry.volume_mm3(deepcopy(joined).intersect(shell))
        removed.append(max(0.0, plain_volume - joined_volume))
    bridge_radial_max = max(
        hypot(vertex.X, vertex.Y)
        for bridge in geometry.bridge_assembly_shapes()
        for vertex in bridge.vertices()
    )
    return {
        "keepout_radius_range_mm": (
            SPEC.future_support_clear_radius_min_mm,
            SPEC.future_support_clear_radius_max_mm,
        ),
        "removed_volume_per_quadrant_mm3": tuple(removed),
        "maximum_removed_volume_mm3": max(removed),
        "maximum_bridge_vertex_radius_mm": bridge_radial_max,
        "joinery_clearance_to_keepout_mm": SPEC.future_support_clear_radius_min_mm - bridge_radial_max,
    }


def bridge_contact_and_hardware_evidence() -> dict[str, object]:
    base = geometry.assembled_base_shape()
    assembly = geometry.assembled_shape()
    quadrants = geometry.quadrant_shapes()
    bridges = geometry.bridge_assembly_shapes()
    expected_press_intersection = (
        pi
        / 4.0
        * (
            SPEC.dowel_nominal_diameter_mm**2
            - SPEC.joiner_press_bore_diameter_mm**2
        )
        * SPEC.joiner_press_engagement_mm
    )
    seam_rows = []
    for seam_index, bridge in enumerate(bridges, start=1):
        left_index = (seam_index - 2) % SPEC.quadrant_count
        right_index = (seam_index - 1) % SPEC.quadrant_count
        contact_distances = (
            bridge.distance_to(quadrants[left_index]),
            bridge.distance_to(quadrants[right_index]),
        )
        dowel_rows = []
        for radius in SPEC.dowel_axis_radii_mm:
            pin = geometry.nominal_dowel_shape(seam_index, radius)
            dowel_rows.append(
                {
                    "radius_mm": radius,
                    "pin_base_intersection_mm3": geometry.intersection_volume_mm3(pin, base),
                    "pin_bridge_press_intersection_mm3": geometry.intersection_volume_mm3(pin, bridge),
                    "expected_press_intersection_mm3": expected_press_intersection,
                    "pin_to_base_clearance_mm": pin.distance_to(base),
                }
            )
        screw_rows = []
        for tangent in SPEC.screw_tangent_offsets_mm:
            screw = geometry.nominal_screw_shaft_shape(seam_index, tangent)
            nut = geometry.nominal_nut_shape(seam_index, tangent)
            driver = geometry.driver_access_shape(seam_index, tangent)
            screw_rows.append(
                {
                    "tangent_mm": tangent,
                    "screw_base_intersection_mm3": geometry.intersection_volume_mm3(screw, base),
                    "screw_bridge_intersection_mm3": geometry.intersection_volume_mm3(screw, bridge),
                    "nut_bridge_intersection_mm3": geometry.intersection_volume_mm3(nut, bridge),
                    "driver_assembly_intersection_mm3": geometry.intersection_volume_mm3(driver, assembly),
                }
            )
        seam_rows.append(
            {
                "seam_index": seam_index,
                "adjacent_quadrants": (left_index + 1, right_index + 1),
                "bridge_to_adjacent_quadrant_distances_mm": contact_distances,
                "bridge_base_positive_intersection_mm3": geometry.intersection_volume_mm3(bridge, base),
                "dowels": tuple(dowel_rows),
                "screws": tuple(screw_rows),
            }
        )
    return {
        "seams": tuple(seam_rows),
        "bridge_dimensions_mm": (
            SPEC.bridge_radial_mm,
            SPEC.bridge_tangential_mm,
            SPEC.bridge_thickness_mm,
        ),
        "bridge_solid_count": len(geometry.bridge_print_shape().solids()),
        "bridge_is_valid": bool(geometry.bridge_print_shape().is_valid),
        "screw_interface_count": SPEC.screw_count_total,
        "dowel_interface_count": SPEC.dowel_count_total,
        "nut_pocket_depth_mm": SPEC.nut_pocket_depth_mm,
        "nut_axial_slack_mm": SPEC.nut_axial_slack_mm,
        "screw_tip_beyond_base_and_nut_mm": SPEC.screw_tip_beyond_base_and_nut_mm,
        "screw_tip_relief_depth_mm": SPEC.screw_tip_relief_depth_mm,
        "bridge_bottom_skin_mm": SPEC.tip_relief_floor_from_bridge_bottom_mm,
        "press_engagement_mm": SPEC.joiner_press_engagement_mm,
        "base_slip_engagement_mm": SPEC.base_split_slip_engagement_mm,
        "dowel_diametral_slip_mm": SPEC.dowel_diametral_slip_mm,
        "relief_slot_brep": relief_slot_brep_evidence(),
        "minimum_round_pin_base_clearance_mm": min(
            dowel["pin_to_base_clearance_mm"]
            for seam in seam_rows
            for dowel in seam["dowels"]
            if dowel["radius_mm"] == SPEC.round_dowel_axis_radius_mm
        ),
        "minimum_relief_pin_base_clearance_mm": min(
            dowel["pin_to_base_clearance_mm"]
            for seam in seam_rows
            for dowel in seam["dowels"]
            if dowel["radius_mm"] == SPEC.relief_dowel_axis_radius_mm
        ),
        "nut_radial_wall_mm": SPEC.nut_radial_wall_mm,
        "nut_to_nearest_dowel_ligament_mm": SPEC.nut_to_nearest_dowel_ligament_mm,
        "tangential_end_wall_mm": SPEC.tangential_end_wall_mm,
        "maximum_void_intersection_mm3": max(
            value
            for seam in seam_rows
            for screw in seam["screws"]
            for value in (
                screw["screw_base_intersection_mm3"],
                screw["screw_bridge_intersection_mm3"],
                screw["nut_bridge_intersection_mm3"],
                screw["driver_assembly_intersection_mm3"],
            )
        ),
        "maximum_pin_base_intersection_mm3": max(
            dowel["pin_base_intersection_mm3"]
            for seam in seam_rows
            for dowel in seam["dowels"]
        ),
        "maximum_press_intersection_error_mm3": max(
            abs(
                dowel["pin_bridge_press_intersection_mm3"]
                - dowel["expected_press_intersection_mm3"]
            )
            for seam in seam_rows
            for dowel in seam["dowels"]
        ),
        "maximum_contact_distance_mm": max(
            distance
            for seam in seam_rows
            for distance in seam["bridge_to_adjacent_quadrant_distances_mm"]
        ),
    }


def evaluate_bridge_fixture(
    overrides: dict[int, tuple[float, float, float]] | None = None,
) -> dict[str, object]:
    """Evaluate radial, tangential, and Z overrides for any bridge occurrence."""

    overrides = overrides or {}
    quadrants = geometry.quadrant_shapes()
    rows = []
    for seam_index, bridge in enumerate(geometry.bridge_assembly_shapes(), start=1):
        radial_offset, tangent_offset, z_offset = overrides.get(seam_index, (0.0, 0.0, 0.0))
        angle = SPEC.seam_angles_deg[seam_index - 1]
        dx, dy = geometry.local_point(angle, radial_offset, tangent_offset)
        moved = deepcopy(bridge).moved(Location((dx, dy, z_offset)))
        box = moved.bounding_box()
        left_index = (seam_index - 2) % SPEC.quadrant_count
        right_index = (seam_index - 1) % SPEC.quadrant_count
        axis_error = hypot(radial_offset, tangent_offset)
        seat_plane_error = abs(box.max.Z)
        contact_distances = (
            moved.distance_to(quadrants[left_index]),
            moved.distance_to(quadrants[right_index]),
        )
        rows.append(
            {
                "seam_index": seam_index,
                "bridge_bottom_z_mm": box.min.Z,
                "bridge_top_z_mm": box.max.Z,
                "seat_plane_error_mm": seat_plane_error,
                "dowel_axis_error_mm": axis_error,
                "contact_distances_mm": contact_distances,
                "seat_contact_pass": (
                    seat_plane_error <= SPEC.coplanarity_tolerance_mm
                    and max(contact_distances) <= SPEC.cad_linear_tolerance_mm
                ),
                "dowel_axis_pass": axis_error <= SPEC.cad_linear_tolerance_mm,
            }
        )
    bottoms = [row["bridge_bottom_z_mm"] for row in rows]
    bottom_coplanarity = max(bottoms) - min(bottoms)
    return {
        "rows": tuple(rows),
        "bridge_bottom_coplanarity_mm": bottom_coplanarity,
        "maximum_seat_plane_error_mm": max(row["seat_plane_error_mm"] for row in rows),
        "maximum_dowel_axis_error_mm": max(row["dowel_axis_error_mm"] for row in rows),
        "z_coplanarity_pass": bottom_coplanarity <= SPEC.coplanarity_tolerance_mm,
        "all_seat_contacts_pass": all(row["seat_contact_pass"] for row in rows),
        "all_dowel_axes_pass": all(row["dowel_axis_pass"] for row in rows),
        "fixture_pass": (
            bottom_coplanarity <= SPEC.coplanarity_tolerance_mm
            and all(row["seat_contact_pass"] for row in rows)
            and all(row["dowel_axis_pass"] for row in rows)
        ),
    }


def production_fixture_evidence() -> dict[str, object]:
    return evaluate_bridge_fixture()


def deliberate_bad_fixture_evidence() -> dict[str, object]:
    return {
        "shim_seam_4": evaluate_bridge_fixture(
            {4: (0.0, 0.0, SPEC.bad_fixture_shim_mm)}
        ),
        "radial_axis_offset_seam_4": evaluate_bridge_fixture(
            {4: (SPEC.bad_fixture_radial_offset_mm, 0.0, 0.0)}
        ),
    }


def _vertical_path_offsets(start_mm: float, end_mm: float) -> tuple[float, ...]:
    """Return an inclusive monotonic path using the named assembly sample step."""

    direction = 1.0 if end_mm >= start_mm else -1.0
    step = SPEC.assembly_path_sample_step_mm * direction
    count = round(abs(end_mm - start_mm) / SPEC.assembly_path_sample_step_mm)
    offsets = tuple(start_mm + step * index for index in range(count + 1))
    if not offsets or abs(offsets[-1] - end_mm) > 1.0e-9:
        raise RuntimeError("assembly path endpoints must be divisible by the sample step")
    return offsets


def final_bridge_assembly_path_evidence() -> dict[str, object]:
    """Prove the approved final-bridge path and reject the old lowering path.

    S1-S3 form the open chain while all four quadrants are supported in their
    final XY locations. S4 and its two pressed pins then translate only upward
    from below. The bridge swept solid is a conservative continuous envelope
    of its exact 48 x 26 mm footprint; each pin swept solid is the exact D4
    cylinder over its full continuous Z travel. Actual moving BREPs are also
    checked at every named path sample.

    The rejected fixture lowers Q4 with S4 and both pins already attached. One
    positive actual-solid collision anywhere on that path is sufficient to
    prove the proposed assembly motion cannot be completed.
    """

    seam_index = SPEC.final_bridge_seam_index
    bridge = geometry.bridge_assembly_shape(seam_index)
    pins = tuple(
        geometry.nominal_dowel_shape(seam_index, radius)
        for radius in SPEC.dowel_axis_radii_mm
    )
    quadrants = geometry.quadrant_shapes()
    assembled_quadrants = Compound(
        children=[deepcopy(quadrant) for quadrant in quadrants],
        label="supported_four_quadrants",
    )

    approved_offsets = _vertical_path_offsets(
        SPEC.final_bridge_below_start_z_offset_mm,
        0.0,
    )
    approved_rows = []
    for z_offset in approved_offsets:
        moved_bridge = deepcopy(bridge).moved(Location((0.0, 0.0, z_offset)))
        moved_pins = tuple(
            deepcopy(pin).moved(Location((0.0, 0.0, z_offset)))
            for pin in pins
        )
        bridge_collision = geometry.intersection_volume_mm3(
            moved_bridge, assembled_quadrants
        )
        pin_collisions = tuple(
            geometry.intersection_volume_mm3(pin, assembled_quadrants)
            for pin in moved_pins
        )
        approved_rows.append(
            {
                "z_offset_mm": z_offset,
                "bridge_quadrant_intersection_mm3": bridge_collision,
                "pin_quadrant_intersections_mm3": pin_collisions,
                "total_intersection_mm3": bridge_collision + sum(pin_collisions),
            }
        )

    angle = SPEC.seam_angles_deg[seam_index - 1]
    center_x, center_y = geometry.local_point(
        angle, SPEC.bridge_center_radius_mm, 0.0
    )
    bridge_sweep_height = (
        SPEC.bridge_thickness_mm
        + abs(SPEC.final_bridge_below_start_z_offset_mm)
    )
    conservative_bridge_swept_solid = Box(
        SPEC.bridge_radial_mm,
        SPEC.bridge_tangential_mm,
        bridge_sweep_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).rotate(Axis.Z, angle).moved(
        Location((center_x, center_y, -bridge_sweep_height))
    )
    pin_sweep_z0 = (
        -SPEC.joiner_press_engagement_mm
        + SPEC.final_bridge_below_start_z_offset_mm
    )
    pin_sweep_height = (
        SPEC.dowel_length_mm
        + abs(SPEC.final_bridge_below_start_z_offset_mm)
    )
    exact_pin_swept_solids = tuple(
        geometry.vertical_cylinder(
            angle,
            radius,
            0.0,
            SPEC.dowel_nominal_diameter_mm,
            pin_sweep_z0,
            pin_sweep_height,
        )
        for radius in SPEC.dowel_axis_radii_mm
    )
    bridge_sweep_collision = geometry.intersection_volume_mm3(
        conservative_bridge_swept_solid, assembled_quadrants
    )
    pin_sweep_collisions = tuple(
        geometry.intersection_volume_mm3(pin_sweep, assembled_quadrants)
        for pin_sweep in exact_pin_swept_solids
    )

    fixed_quadrants = Compound(
        children=[deepcopy(quadrant) for quadrant in quadrants[:-1]],
        label="fixed_Q1_Q2_Q3",
    )
    rejected_offsets = _vertical_path_offsets(
        SPEC.rejected_last_quadrant_above_start_z_offset_mm,
        0.0,
    )
    rejected_rows = []
    for z_offset in rejected_offsets:
        moved_quadrant = deepcopy(quadrants[-1]).moved(
            Location((0.0, 0.0, z_offset))
        )
        moved_bridge = deepcopy(bridge).moved(Location((0.0, 0.0, z_offset)))
        moved_pins = tuple(
            deepcopy(pin).moved(Location((0.0, 0.0, z_offset)))
            for pin in pins
        )
        quadrant_collision = geometry.intersection_volume_mm3(
            moved_quadrant, fixed_quadrants
        )
        bridge_collision = geometry.intersection_volume_mm3(
            moved_bridge, fixed_quadrants
        )
        pin_collisions = tuple(
            geometry.intersection_volume_mm3(pin, fixed_quadrants)
            for pin in moved_pins
        )
        rejected_rows.append(
            {
                "z_offset_mm": z_offset,
                "last_quadrant_intersection_mm3": quadrant_collision,
                "attached_bridge_intersection_mm3": bridge_collision,
                "attached_pin_intersections_mm3": pin_collisions,
                "total_intersection_mm3": (
                    quadrant_collision + bridge_collision + sum(pin_collisions)
                ),
            }
        )

    colliding_rejected_rows = tuple(
        row
        for row in rejected_rows
        if row["total_intersection_mm3"] > SPEC.brep_intersection_tolerance_mm3
    )
    maximum_approved_sample_collision = max(
        row["total_intersection_mm3"] for row in approved_rows
    )
    maximum_rejected_bridge_collision = max(
        row["attached_bridge_intersection_mm3"] for row in rejected_rows
    )
    return {
        "approved_final_bridge_upward": {
            "sequence": "support_all_four_quadrants_preattach_S1_S2_S3_insert_S4_upward",
            "final_bridge_seam_index": seam_index,
            "preattached_bridge_indices": (1, 2, 3),
            "path_z_offsets_mm": approved_offsets,
            "sample_rows": tuple(approved_rows),
            "start_pin_top_clearance_below_quadrants_mm": (
                assembled_quadrants.bounding_box().min.Z
                - (
                    pins[0].bounding_box().max.Z
                    + SPEC.final_bridge_below_start_z_offset_mm
                )
            ),
            "maximum_sample_intersection_mm3": maximum_approved_sample_collision,
            "continuous_bridge_swept_solid_intersection_mm3": bridge_sweep_collision,
            "continuous_exact_pin_swept_solid_intersections_mm3": pin_sweep_collisions,
            "path_clear": (
                maximum_approved_sample_collision
                <= SPEC.brep_intersection_tolerance_mm3
                and bridge_sweep_collision <= SPEC.brep_intersection_tolerance_mm3
                and max(pin_sweep_collisions) <= SPEC.brep_intersection_tolerance_mm3
            ),
        },
        "rejected_last_quadrant_vertical_lowering": {
            "sequence": "lower_Q4_with_S4_and_both_pins_attached",
            "path_z_offsets_mm": rejected_offsets,
            "sample_rows": tuple(rejected_rows),
            "start_bridge_clearance_above_fixed_quadrants_mm": (
                bridge.bounding_box().min.Z
                + SPEC.rejected_last_quadrant_above_start_z_offset_mm
                - fixed_quadrants.bounding_box().max.Z
            ),
            "first_collision_z_offset_mm": (
                colliding_rejected_rows[0]["z_offset_mm"]
                if colliding_rejected_rows
                else None
            ),
            "collision_sample_count": len(colliding_rejected_rows),
            "maximum_attached_bridge_intersection_mm3": maximum_rejected_bridge_collision,
            "path_clear": not colliding_rejected_rows,
        },
    }
