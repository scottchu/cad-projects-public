"""Focused actual-solid and contract validation for B6-R1."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import hypot

from build123d import Align, Box, Compound, Cylinder, Location

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_geometry as r4
import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_validation as hashes
import p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry as b1
import p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_geometry as b2
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_geometry as b2r3
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as b3
import p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_geometry as b5a
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_spec as ring_spec
import p3_v3_mvp_electronics_b6_r1_coplanar_broad_underside_geometry as geometry
from p3_v3_mvp_electronics_b6_r1_coplanar_broad_underside_spec import SPEC


FROZEN_HASHES = {
    "p3_v3_mvp_base_q4_r4_functional_centered_step_lap": "9cae6479cca23c38bdfff1bd28e4a7f30b422abede6f28fb6f1ccf4f86f28c3a",
    "p3_v3_mvp_mount_b1_r1_raised_nut_rails": "675de24de9afa6afbcd7a6ba6c0079a1f60e72507a6e4cbe803f732d1c55e2df",
    "p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion": "bf0bbf3d320c395c9530a39a2de9ccd41c21abc876f40507c70cbc40c6cccb72",
    "p3_v3_mvp_roller_b3_r1_blind_axle_towers": "9b384da3c608c69e205b5221a8495098fc775a7cc8e20772c1032790db846a71",
    "p3_v3_mvp_rings_b4_r2_adversarial_fin_clearance": "7b2087184ca58ca128f76b8d35465ed0e5e1e7c8c97536d3ee2897705361f02c",
    "p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver": "b69715b9a867667c79a3f19587820758a95fd8c37878d027d7f4a9644617704d",
}


@lru_cache(maxsize=1)
def immutable_predecessor_evidence():
    actual = {name: hashes.namespace_tree_hash(name) for name in FROZEN_HASHES}
    return {"expected": FROZEN_HASHES, "actual": actual, "all_unchanged": actual == FROZEN_HASHES}


@lru_cache(maxsize=1)
def backbone_registry_evidence():
    shape = geometry.backbone_shape()
    box = shape.bounding_box()
    return {
        "printed_object_count": 1,
        "solid_count": len(shape.solids()),
        "valid_positive": shape.is_valid and geometry.volume_mm3(shape) > 0.0,
        "volume_mm3": geometry.volume_mm3(shape),
        "bbox_xyz_mm": (float(box.size.X), float(box.size.Y), float(box.size.Z)),
        "bbox_with_brim_xy_mm": (
            float(box.size.X) + 2.0 * SPEC.print_brim_mm,
            float(box.size.Y) + 2.0 * SPEC.print_brim_mm,
        ),
        "fits_260_square_with_brim": max(box.size.X, box.size.Y) + 2.0 * SPEC.print_brim_mm <= SPEC.print_footprint_limit_xy_mm + 1e-9,
        "global_min_z_mm": float(box.min.Z),
        "intended_underside_z_mm": SPEC.printed_underside_z_mm,
        "functional_web_top_z_mm": SPEC.printed_top_z_mm,
        "functional_pad_top_z_mm": SPEC.pad_top_z_mm,
        "empty_optical_center_radius_mm": SPEC.inner_web_radii_mm[0],
    }


@lru_cache(maxsize=1)
def broad_underside_support_evidence():
    """Measure the true global underside and its near-bed connected footprint.

    A thin actual-solid intersection is deliberately used here: the rejected
    R0 four-pip geometry produces four tiny solids, while R1 must produce one
    broad connected support solid at the global minimum Z.
    """
    shape = geometry.backbone_shape()
    box = shape.bounding_box()
    z0 = float(box.min.Z)
    face_tol_mm = 1.0e-7
    underside_faces = tuple(
        face
        for face in shape.faces()
        if abs(float(face.bounding_box().max.Z) - float(face.bounding_box().min.Z)) <= face_tol_mm
        and abs(float(face.bounding_box().min.Z) - z0) <= face_tol_mm
    )
    underside_area_mm2 = sum(float(face.area) for face in underside_faces)

    margin_mm = 2.0
    probe_h = SPEC.support_layer_probe_thickness_mm
    support_probe = Box(
        float(box.size.X) + 2.0 * margin_mm,
        float(box.size.Y) + 2.0 * margin_mm,
        probe_h,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((float(box.min.X) - margin_mm, float(box.min.Y) - margin_mm, z0)))
    support_layer = deepcopy(shape).intersect(support_probe)
    support_solids = tuple(support_layer.solids())
    support_area_estimate_mm2 = geometry.volume_mm3(support_layer) / probe_h

    below_gap_mm = 1.0e-4
    below_probe_h = 2.0
    below_probe = Box(
        float(box.size.X) + 2.0 * margin_mm,
        float(box.size.Y) + 2.0 * margin_mm,
        below_probe_h - below_gap_mm,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(
        Location(
            (
                float(box.min.X) - margin_mm,
                float(box.min.Y) - margin_mm,
                SPEC.printed_underside_z_mm - below_probe_h,
            )
        )
    )
    below_plane_volume_mm3 = geometry.intersection_volume_mm3(shape, below_probe)

    return {
        "global_min_z_mm": z0,
        "intended_underside_z_mm": SPEC.printed_underside_z_mm,
        "global_min_matches_intended_plane": abs(z0 - SPEC.printed_underside_z_mm) <= face_tol_mm,
        "global_min_planar_face_count": len(underside_faces),
        "global_min_planar_area_mm2": underside_area_mm2,
        "global_min_is_broad": underside_area_mm2 >= SPEC.minimum_broad_underside_area_mm2,
        "material_below_intended_plane_mm3": below_plane_volume_mm3,
        "no_material_below_intended_plane": below_plane_volume_mm3 <= SPEC.brep_tolerance_mm3,
        "support_probe_thickness_mm": probe_h,
        "support_footprint_solid_count": len(support_solids),
        "support_footprint_connected": len(support_solids) == 1,
        "support_footprint_area_estimate_mm2": support_area_estimate_mm2,
        "support_footprint_is_broad": support_area_estimate_mm2 >= SPEC.minimum_connected_support_area_mm2,
    }


def seam_axis_and_hardware_evidence():
    rows = []
    for axis in geometry.seam_axes():
        b6_xy = geometry.polar(float(axis["angle_deg"]), float(axis["radius_mm"]), 0.0)
        r4_xy = r4.local_point(float(axis["angle_deg"]), float(axis["radius_mm"]), 0.0)
        rows.append(
            {
                **axis,
                "axis_delta_mm": hypot(b6_xy[0] - r4_xy[0], b6_xy[1] - r4_xy[1]),
            }
        )
    backbone = geometry.backbone_shape()
    hardware = geometry.seam_hardware_witnesses()
    return {
        "rows": tuple(rows),
        "axis_count": len(rows),
        "maximum_axis_delta_mm": max(row["axis_delta_mm"] for row in rows),
        "m3x8_witness_count": len(hardware) // 2,
        "washer_witness_count": len(hardware) // 2,
        "engagement_mm": SPEC.seam_engagement_mm,
        "tip_above_underside_mm": SPEC.seam_tip_above_underside_mm,
        "maximum_backbone_hardware_intersection_mm3": max(
            geometry.intersection_volume_mm3(backbone, item) for item in hardware
        ),
    }


def universal_interface_evidence():
    nuts = geometry.side_load_nut_witnesses()
    backbone = geometry.backbone_shape()
    component_rows = geometry.component_layout()
    power = [row for row in component_rows if row["name"] in ("logic_buck", "led_cc_driver")]
    motion = [row for row in component_rows if str(row["name"]).startswith("tmc2209_")]

    def tangent_gap(left, right):
        return abs(float(right["tangent_mm"]) - float(left["tangent_mm"])) - (
            float(left["tangent_size_mm"]) + float(right["tangent_size_mm"])
        ) / 2.0

    board_gaps = (
        tangent_gap(power[0], power[1]),
        tangent_gap(motion[0], motion[1]),
        tangent_gap(motion[1], motion[2]),
    )
    return {
        "slot_count": len(geometry.board_slot_layout()),
        "side_load_nut_count": len(nuts),
        "all_nuts_clear_printed_backbone": max(
            geometry.intersection_volume_mm3(backbone, nut) for nut in nuts
        ) <= SPEC.brep_tolerance_mm3,
        "minimum_board_gap_mm": min(board_gaps),
        "board_specific_hole_patterns": 0,
        "ordinary_m3_nut_af_mm": SPEC.ordinary_m3_nut_af_mm,
        "channel_af_mm": SPEC.side_load_nut_channel_af_mm,
        "slot_size_mm": (SPEC.board_slot_width_mm, SPEC.board_slot_overall_length_mm),
    }


def _protected_b6_children():
    return (geometry.backbone_shape(), *geometry.component_envelope_witnesses())


def _max_intersection(left_children, right_children):
    return max(
        geometry.intersection_volume_mm3(left, right)
        for left in left_children
        for right in right_children
    )


def _min_distance(left_children, right_children):
    return min(float(left.distance_to(right)) for left in left_children for right in right_children)


@lru_cache(maxsize=1)
def stationary_predecessor_collision_evidence():
    protected = _protected_b6_children()
    r4_shapes = tuple(r4.named_quadrant(i) for i in range(1, 5))
    b1_shapes = (b1.fixed_riser_shape(60.0), b1.fixed_riser_shape(180.0), b1.spine_riser_shape())
    b3_shapes = tuple(b3.printed_additions_shape().children)
    b5_shapes = tuple(b5a.bridge_receiver_shape(index) for index in range(3))
    groups = (
        ("R4", r4_shapes, True),
        ("B1", b1_shapes, False),
        ("B3-R1", b3_shapes, False),
        ("B5A", b5_shapes, False),
    )
    rows = []
    for name, shapes, contact_allowed in groups:
        rows.append(
            {
                "stage": name,
                "shape_count": len(shapes),
                "maximum_intersection_mm3": _max_intersection(protected, shapes),
                "minimum_distance_mm": _min_distance(protected, shapes),
                "contact_allowed": contact_allowed,
            }
        )
    return {
        "rows": tuple(rows),
        "maximum_intersection_mm3": max(row["maximum_intersection_mm3"] for row in rows),
    }


@lru_cache(maxsize=1)
def motor_sled_and_b2r3_collision_evidence():
    protected = _protected_b6_children()
    rows = []
    for role_index, (role, angle) in enumerate(zip(b2.SPEC.station_roles, b2.SPEC.station_angles_deg)):
        for q_mm in SPEC.motor_sled_q_samples_mm:
            shapes = (
                b2.printed_station_sled(role, q_mm, angle),
                b2.motor_body_witness(angle, q_mm),
                b2r3.exact_output_pinion(role_index, q_mm, 0.0),
            )
            rows.append(
                {
                    "role": role,
                    "q_mm": q_mm,
                    "maximum_intersection_mm3": _max_intersection(protected, shapes),
                    "minimum_distance_mm": _min_distance(protected, shapes),
                }
            )
    return {
        "rows": tuple(rows),
        "pose_count": len(rows),
        "maximum_intersection_mm3": max(row["maximum_intersection_mm3"] for row in rows),
        "minimum_distance_mm": min(row["minimum_distance_mm"] for row in rows),
    }


def ring_360_sweep_clearance_evidence():
    protected = _protected_b6_children()
    rows = []
    for role_index, role in enumerate(ring_spec.SPEC.ring.roles):
        z0 = ring_spec.SPEC.ring.carrier_z_mm[role_index][0]
        z1 = ring_spec.SPEC.fin.blade_z_mm[role_index][1]
        swept = Cylinder(
            ring_spec.SPEC.fin.blade_radii_mm[1],
            z1 - z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((0.0, 0.0, z0)))
        rows.append(
            {
                "role": role,
                "sweep_deg": 360.0,
                "minimum_clearance_mm": min(float(shape.distance_to(swept)) for shape in protected),
                "maximum_intersection_mm3": max(
                    geometry.intersection_volume_mm3(shape, swept) for shape in protected
                ),
            }
        )
    return {
        "rows": tuple(rows),
        "minimum_clearance_mm": min(row["minimum_clearance_mm"] for row in rows),
        "maximum_intersection_mm3": max(row["maximum_intersection_mm3"] for row in rows),
    }


def thermal_antenna_and_cable_evidence():
    envelopes = {shape.label: shape for shape in geometry.component_envelope_witnesses()}
    driver = next(shape for label, shape in envelopes.items() if "led_cc_driver" in label)
    antenna, heatsink = geometry.keepout_witnesses()
    high_current, logic, motor = geometry.wiring_witnesses()
    return {
        "driver_to_led_heatsink_clearance_mm": float(driver.distance_to(heatsink)),
        "esp_antenna_keepout_mm": SPEC.esp_antenna_keepout_mm,
        "antenna_backbone_intersection_mm3": geometry.intersection_volume_mm3(antenna, geometry.backbone_shape()),
        "high_current_to_logic_trunk_clearance_mm": float(high_current.distance_to(logic)),
        "high_current_to_motor_branch_clearance_mm": float(high_current.distance_to(motor)),
        "open_channel_cross_section_mm": (SPEC.open_channel_width_mm, SPEC.open_channel_height_mm),
        "general_bend_radius_mm": SPEC.general_bend_radius_min_mm,
        "led_bend_radius_mm": SPEC.led_bend_radius_min_mm,
        "led_service_loop_mm": SPEC.led_service_loop_mm,
        "motor_branch_loop_mm": SPEC.motor_branch_loop_mm,
        "installed_envelope_top_z_mm": max(shape.bounding_box().max.Z for shape in envelopes.values()),
    }


@lru_cache(maxsize=1)
def sequential_insertion_evidence():
    base = tuple(r4.named_quadrant(i) for i in range(1, 5))
    rows = []
    for dz in (20.0, 10.0, 5.0, 1.0, 0.0):
        moving = deepcopy(geometry.backbone_shape()).moved(Location((0.0, 0.0, dz)))
        rows.append(
            {
                "stage": "B6_down_to_R4",
                "dz_mm": dz,
                "maximum_intersection_mm3": max(
                    geometry.intersection_volume_mm3(moving, target) for target in base
                ),
            }
        )
    protected = _protected_b6_children()
    later_parts = (
        ("B1_fixed_A60", b1.fixed_riser_shape(60.0)),
        ("B2_hour_sled", b2.printed_station_sled("hour", 0.0, 0.0)),
        ("B3_tower_A60", b3.tower_shape(60.0)),
        ("B5A_H_bridge", b5a.bridge_receiver_shape(0)),
    )
    for name, part in later_parts:
        for dz in (20.0, 10.0, 5.0, 0.0):
            moving = deepcopy(part).moved(Location((0.0, 0.0, dz)))
            rows.append(
                {
                    "stage": name,
                    "dz_mm": dz,
                    "maximum_intersection_mm3": max(
                        geometry.intersection_volume_mm3(moving, target) for target in protected
                    ),
                }
            )
    return {
        "rows": tuple(rows),
        "pose_count": len(rows),
        "maximum_intersection_mm3": max(row["maximum_intersection_mm3"] for row in rows),
    }


def assembly_order_evidence():
    labels = tuple(str(child.label or "") for child in geometry.exploded_shape().children)
    required = tuple(f"step_{index:02d}_" for index in range(1, 12))
    present = {token: any(token in label for label in labels) for token in required}
    first_indices = tuple(min(i for i, label in enumerate(labels) if token in label) for token in required)
    return {
        "occurrence_count": len(labels),
        "required_steps_present": present,
        "first_indices": first_indices,
        "strictly_ordered": all(a < b for a, b in zip(first_indices, first_indices[1:])),
        "b4_last": all("step_11_B4_LAST" in label for label in labels[first_indices[-1]:]),
    }
