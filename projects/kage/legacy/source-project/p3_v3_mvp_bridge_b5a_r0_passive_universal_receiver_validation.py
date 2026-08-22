"""Focused actual-solid validation for the B5A passive bridge/receiver MVP."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import hypot

from build123d import Compound, Cylinder, Align, Location

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_validation as hashes
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_geometry as pinions
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_geometry as rings
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_spec as ring_spec
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as b3
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_spec as b3_spec
import p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_geometry as geometry
from p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_spec import SPEC


FROZEN_HASHES = {
    "p3_v3_mvp_base_q4_r4_functional_centered_step_lap": "9cae6479cca23c38bdfff1bd28e4a7f30b422abede6f28fb6f1ccf4f86f28c3a",
    "p3_v3_mvp_mount_b1_r1_raised_nut_rails": "675de24de9afa6afbcd7a6ba6c0079a1f60e72507a6e4cbe803f732d1c55e2df",
    "p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations": "ac47fc19eb54cd65dc5aedef57bcb8e87ae6048397752def8ec9a45b91a57705",
    "p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion": "bf0bbf3d320c395c9530a39a2de9ccd41c21abc876f40507c70cbc40c6cccb72",
    "p3_v3_mvp_roller_b3_r1_blind_axle_towers": "9b384da3c608c69e205b5221a8495098fc775a7cc8e20772c1032790db846a71",
    "p3_v3_mvp_rings_b4_r0_segmented_fins_magnets": "c8bdf02cd21e5af35e90ebe6dec49025097687ee4752ac7c4c2acdb852bf0da2",
    "p3_v3_mvp_rings_b4_r1_exact_involute_mesh": "fdc8f459730747bff59b036f1e8614afea717d720d07d0e5012f06c536cc5f03",
    "p3_v3_mvp_rings_b4_r2_adversarial_fin_clearance": "7b2087184ca58ca128f76b8d35465ed0e5e1e7c8c97536d3ee2897705361f02c",
}


def _bbox_overlap(left, right) -> bool:
    a, b = left.bounding_box(), right.bounding_box()
    return not (
        a.max.X < b.min.X or b.max.X < a.min.X
        or a.max.Y < b.min.Y or b.max.Y < a.min.Y
        or a.max.Z < b.min.Z or b.max.Z < a.min.Z
    )


def _distance_and_intersection(left, right) -> tuple[float, float]:
    """Use the actual-BREP distance first; boolean only when contact is possible."""
    distance = float(left.distance_to(right))
    intersection = (
        geometry.intersection_volume_mm3(left, right)
        if distance <= SPEC.brep_tolerance_mm3
        else 0.0
    )
    return distance, intersection


@lru_cache(maxsize=1)
def immutable_predecessor_evidence():
    actual = {name: hashes.namespace_tree_hash(name) for name in FROZEN_HASHES}
    return {"expected": FROZEN_HASHES, "actual": actual, "all_unchanged": actual == FROZEN_HASHES}


@lru_cache(maxsize=1)
def printable_registry_evidence():
    rows = []
    for item in geometry.printable_occurrences():
        shape = item["shape"]
        box = shape.bounding_box()
        rows.append(
            {
                "name": item["name"],
                "label": item["label"],
                "solids": len(shape.solids()),
                "valid": shape.is_valid,
                "volume_mm3": geometry.volume_mm3(shape),
                "bbox_xyz_mm": (float(box.size.X), float(box.size.Y), float(box.size.Z)),
                "minimum_z_mm": float(box.min.Z),
            }
        )
    labels = tuple(row["label"] for row in rows)
    prohibited = tuple(
        label for label in labels
        if any(token in label.lower() for token in ("electronics", "pcb", "hall_sensor"))
    )
    return {
        "rows": tuple(rows),
        "printed_object_count": len(rows),
        "all_one_solid_valid": all(row["solids"] == 1 and row["valid"] and row["volume_mm3"] > 0 for row in rows),
        "all_on_print_datum": all(abs(row["minimum_z_mm"]) <= 1e-8 for row in rows),
        "gauge_label_present": any(SPEC.gauge_label in label for label in labels),
        "prohibited_geometry_labels": prohibited,
    }


def mount_axis_and_ear_evidence():
    rows = []
    for role in SPEC.roles:
        for tangent in SPEC.mount_axis_tangent_mm:
            b5_xy = geometry.polar(role.mount_radius_mm, role.anchor_angle_deg, tangent)
            b3_radius = b3.landing_radius(role.anchor_angle_deg)
            b3_xy = b3.local_point(role.anchor_angle_deg, b3_radius, tangent)
            rows.append(
                {
                    "role": role.name,
                    "tangent_mm": tangent,
                    "b5_xy_mm": b5_xy,
                    "b3_xy_mm": b3_xy,
                    "axis_delta_mm": hypot(b5_xy[0] - b3_xy[0], b5_xy[1] - b3_xy[1]),
                }
            )
    ear_thickness = SPEC.capture_ear_z_mm[1] - SPEC.capture_ear_z_mm[0]
    return {
        "rows": tuple(rows),
        "maximum_axis_delta_mm": max(row["axis_delta_mm"] for row in rows),
        "ear_z_mm": SPEC.capture_ear_z_mm,
        "ear_thickness_mm": ear_thickness,
        "ear_outer_diameter_mm": SPEC.capture_ear_outer_diameter_mm,
        "ear_bore_diameter_mm": SPEC.capture_ear_bore_diameter_mm,
        "tower_z_change_mm": SPEC.tower_geometry_z_change_mm,
        "inherited_fastener": SPEC.inherited_mount_screw,
    }


def ear_to_stationary_roller_evidence():
    rows = []
    for role in SPEC.roles[:2]:
        pads = []
        for tangent in SPEC.mount_axis_tangent_mm:
            outer = geometry.vertical_cylinder(
                role.anchor_angle_deg, role.mount_radius_mm, tangent,
                SPEC.capture_ear_outer_diameter_mm,
                SPEC.capture_ear_z_mm[0],
                SPEC.capture_ear_z_mm[1] - SPEC.capture_ear_z_mm[0],
            )
            bore = geometry.vertical_cylinder(
                role.anchor_angle_deg, role.mount_radius_mm, tangent,
                SPEC.capture_ear_bore_diameter_mm,
                SPEC.capture_ear_z_mm[0] - 0.05,
                SPEC.capture_ear_z_mm[1] - SPEC.capture_ear_z_mm[0] + 0.10,
            )
            pads.append(outer.cut(bore))
        ears = Compound(children=pads)
        roller = b3.roller_shape("hour", role.anchor_angle_deg)
        rows.append(
            {
                "role": role.name,
                "intersection_mm3": geometry.intersection_volume_mm3(ears, roller),
                "distance_mm": ears.distance_to(roller),
            }
        )
    return {
        "rows": tuple(rows),
        "maximum_intersection_mm3": max(row["intersection_mm3"] for row in rows),
        "minimum_distance_mm": min(row["distance_mm"] for row in rows),
        "contract_maximum_possible_mm": b3_spec.SPEC.roller_z_mm[0][0] - SPEC.capture_ear_z_mm[1],
    }


@lru_cache(maxsize=1)
def stationary_q_evidence():
    rows = []
    for q_mm in SPEC.q_mm:
        inherited = b3.assembled_shape(q_mm)
        for role_index, role in enumerate(SPEC.roles):
            bridge = geometry.bridge_receiver_shape(role_index)
            own_tower_token = f"printed_C_bar_A{role.anchor_angle_deg:03.0f}"
            collisions = []
            for child in inherited.children:
                label = str(child.label or "")
                if "nonprint_ring_witness" in label or own_tower_token in label:
                    continue
                if not _bbox_overlap(bridge, child):
                    continue
                iv = geometry.intersection_volume_mm3(bridge, child)
                if iv > SPEC.brep_tolerance_mm3:
                    collisions.append((label, iv))
            own_tower = b3.tower_shape(role.anchor_angle_deg)
            rows.append(
                {
                    "q_mm": q_mm,
                    "role": role.name,
                    "unexpected_collisions": tuple(collisions),
                    "own_tower_intersection_mm3": geometry.intersection_volume_mm3(bridge, own_tower),
                    "own_tower_distance_mm": bridge.distance_to(own_tower),
                }
            )
    return {
        "rows": tuple(rows),
        "all_unexpected_clear": all(not row["unexpected_collisions"] for row in rows),
        "q_states": SPEC.q_mm,
    }


@lru_cache(maxsize=1)
def exact_pinion_q_evidence():
    additions = Compound(children=[geometry.bridge_receiver_shape(index) for index in range(3)])
    rows = []
    for q_mm in SPEC.q_mm:
        for role_index, role in enumerate(SPEC.roles):
            pinion = pinions.exact_output_pinion(role_index, q_mm, 0.0)
            distance, intersection = _distance_and_intersection(additions, pinion)
            rows.append(
                {
                    "q_mm": q_mm,
                    "role": role.name,
                    "intersection_mm3": intersection,
                    "distance_mm": distance,
                }
            )
    return {
        "rows": tuple(rows),
        "maximum_intersection_mm3": max(row["intersection_mm3"] for row in rows),
        "minimum_distance_mm": min(row["distance_mm"] for row in rows),
    }


@lru_cache(maxsize=1)
def ring_clearance_evidence():
    def conservative_ring_envelope(role_index: int):
        z0, z1 = ring_spec.SPEC.ring.carrier_z_mm[role_index]
        tooth_z0, tooth_z1 = ring_spec.SPEC.ring.tooth_z_mm[role_index]
        body = rings.annulus(
            ring_spec.SPEC.ring.race_radius_mm,
            ring_spec.SPEC.ring.body_outer_radius_mm,
            z0,
            z1 - z0,
        )
        teeth = rings.annulus(
            ring_spec.SPEC.ring.tip_radius_mm,
            ring_spec.SPEC.ring.race_radius_mm,
            tooth_z0,
            tooth_z1 - tooth_z0,
        )
        return body.fuse(teeth)

    rows = []
    fin_rows = []
    for receiver_index, receiver_role in enumerate(SPEC.roles):
        bridge = geometry.bridge_receiver_shape(receiver_index)
        target = conservative_ring_envelope(receiver_index)
        distance, intersection = _distance_and_intersection(bridge, target)
        rows.append(
            {
                "receiver_role": receiver_role.name,
                "moving_role": receiver_role.name,
                "kind": "target_ring",
                "intersection_mm3": intersection,
                "distance_mm": distance,
            }
        )
        for lower_index in range(receiver_index):
            lower = conservative_ring_envelope(lower_index)
            distance, intersection = _distance_and_intersection(bridge, lower)
            rows.append(
                {
                    "receiver_role": receiver_role.name,
                    "moving_role": SPEC.roles[lower_index].name,
                    "kind": "lower_ring",
                    "intersection_mm3": intersection,
                    "distance_mm": distance,
                }
            )
        for moving_index, moving_role in enumerate(SPEC.roles):
            fin = rings.fin_shape(moving_index).rotate(
                geometry.Axis.Z,
                receiver_role.receiver_angle_deg - ring_spec.SPEC.fin.datum_angle_deg,
            )
            distance, intersection = _distance_and_intersection(bridge, fin)
            fin_rows.append(
                {
                    "receiver_role": receiver_role.name,
                    "moving_role": moving_role.name,
                    "intersection_mm3": intersection,
                    "distance_mm": distance,
                }
            )
    target_rows = tuple(row for row in rows if row["kind"] == "target_ring")
    lower_rows = tuple(row for row in rows if row["kind"] == "lower_ring")
    return {
        "ring_rows": tuple(rows),
        "fin_rows": tuple(fin_rows),
        "minimum_target_distance_mm": min(row["distance_mm"] for row in target_rows),
        "minimum_lower_distance_mm": min(row["distance_mm"] for row in lower_rows),
        "minimum_fin_distance_mm": min(row["distance_mm"] for row in fin_rows),
        "maximum_intersection_mm3": max(row["intersection_mm3"] for row in (*rows, *fin_rows)),
    }


@lru_cache(maxsize=1)
def representative_moving_feature_evidence():
    """Compact actual-solid feature poses, not a brute 360 x 3 sweep."""
    additions = Compound(children=[geometry.bridge_receiver_shape(index) for index in range(3)])
    seam_rows = []
    magnet_rows = []
    for moving_index, moving_role in enumerate(SPEC.roles):
        for receiver_index, receiver_role in enumerate(SPEC.roles):
            seam_index = receiver_index
            seam_angle = ring_spec.SPEC.ring.seam_angles_deg[seam_index]
            z0, z1 = ring_spec.SPEC.ring.carrier_z_mm[moving_index]
            segment = rings._lap_roi(seam_angle, z0, z1).fuse(
                rings._boss_half(seam_angle, True, z0, z1),
                rings._boss_half(seam_angle, False, z0, z1),
            ).rotate(
                geometry.Axis.Z, receiver_role.receiver_angle_deg - seam_angle
            )
            distance, intersection = _distance_and_intersection(additions, segment)
            seam_rows.append(
                {
                    "moving_role": moving_role.name,
                    "seam_index": seam_index + 1,
                    "aligned_receiver": receiver_role.name,
                    "distance_mm": distance,
                    "intersection_mm3": intersection,
                }
            )
            magnet = rings.magnet_witness(moving_index).rotate(
                geometry.Axis.Z,
                receiver_role.receiver_angle_deg - ring_spec.SPEC.magnets.angle_deg,
            )
            distance, intersection = _distance_and_intersection(additions, magnet)
            magnet_rows.append(
                {
                    "moving_role": moving_role.name,
                    "aligned_receiver": receiver_role.name,
                    "distance_mm": distance,
                    "intersection_mm3": intersection,
                }
            )
    return {
        "seam_rows": tuple(seam_rows),
        "magnet_rows": tuple(magnet_rows),
        "pose_count": len(seam_rows) + len(magnet_rows),
        "maximum_intersection_mm3": max(
            row["intersection_mm3"] for row in (*seam_rows, *magnet_rows)
        ),
        "minimum_distance_mm": min(row["distance_mm"] for row in (*seam_rows, *magnet_rows)),
    }


def insertion_and_active_datum_evidence():
    states = (*SPEC.active_radius_range_mm, SPEC.active_radius_nominal_mm)
    rows = []
    usable_half_travel = (SPEC.tongue_slot_radial_length_mm - SPEC.receiver_clearance_diameter_mm) / 2.0
    for role_index, role in enumerate(SPEC.roles):
        receiver = geometry.bridge_receiver_shape(role_index)
        for active_radius in states:
            gauge = geometry.gauge_at_role(role_index, active_radius)
            slot_center_radius = active_radius - SPEC.active_offset_from_slot_center_mm
            rows.append(
                {
                    "role": role.name,
                    "active_radius_mm": active_radius,
                    "slot_center_radius_mm": slot_center_radius,
                    "clamp_offset_in_slot_mm": SPEC.clamp_axis_radius_mm - slot_center_radius,
                    "intersection_mm3": geometry.intersection_volume_mm3(receiver, gauge),
                    "distance_mm": receiver.distance_to(gauge),
                }
            )
    return {
        "rows": tuple(rows),
        "usable_half_travel_mm": usable_half_travel,
        "active_radius_range_mm": SPEC.active_radius_range_mm,
        "active_radius_nominal_mm": SPEC.active_radius_nominal_mm,
        "all_slot_positions_within_travel": all(abs(row["clamp_offset_in_slot_mm"]) <= usable_half_travel + 1e-9 for row in rows),
        "maximum_intersection_mm3": max(row["intersection_mm3"] for row in rows),
        "channel_width_mm": SPEC.channel_width_mm,
        "throat_width_mm": SPEC.channel_width_mm - SPEC.capture_lip_total_mm,
        "gauge_width_mm": SPEC.gauge_tangential_width_mm,
        "centered_insertion_clearance_each_side_mm": (
            SPEC.channel_width_mm - SPEC.capture_lip_total_mm - SPEC.gauge_tangential_width_mm
        ) / 2.0,
        "centered_retained_overlap_total_mm": SPEC.capture_lip_total_mm - (
            SPEC.channel_width_mm - SPEC.capture_lip_total_mm - SPEC.gauge_tangential_width_mm
        ),
        "full_channel_side_float_one_lip_retention_mm": SPEC.capture_lip_total_mm / 2.0,
    }


def hardware_stack_evidence():
    stack = (
        SPEC.washer_thickness_mm
        + SPEC.future_tongue_max_thickness_mm
        + SPEC.floor_thickness_mm
        + SPEC.captured_nut_thickness_mm
    )
    tip_projection = SPEC.receiver_screw_length_mm - stack
    rows = []
    for role_index, role in enumerate(SPEC.roles):
        receiver = geometry.bridge_receiver_shape(role_index)
        screw, washer, nut = geometry.receiver_hardware_witnesses(role_index)
        x, y = geometry.polar(SPEC.clamp_axis_radius_mm, role.receiver_angle_deg)
        driver = Cylinder(
            SPEC.inherited_driver_diameter_mm / 2.0,
            SPEC.driver_access_height_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, role.receiver_top_z_mm + SPEC.washer_thickness_mm)))
        rows.append(
            {
                "role": role.name,
                "screw_receiver_intersection_mm3": geometry.intersection_volume_mm3(screw, receiver),
                "washer_receiver_intersection_mm3": geometry.intersection_volume_mm3(washer, receiver),
                "nut_receiver_intersection_mm3": geometry.intersection_volume_mm3(nut, receiver),
                "driver_receiver_intersection_mm3": geometry.intersection_volume_mm3(driver, receiver),
            }
        )
    return {
        "rows": tuple(rows),
        "stack_mm": stack,
        "screw_length_mm": SPEC.receiver_screw_length_mm,
        "tip_projection_mm": tip_projection,
        "tip_well_depth_mm": SPEC.blind_tip_well_depth_mm,
        "blind_floor_clearance_mm": SPEC.blind_floor_clearance_min_mm,
        "maximum_unintended_intersection_mm3": max(
            max(value for key, value in row.items() if key.endswith("intersection_mm3"))
            for row in rows
        ),
    }


def u1_printability_evidence():
    rows = []
    for item in geometry.printable_occurrences():
        box = item["shape"].bounding_box()
        required_xy = (float(box.size.X) + 2 * SPEC.print_brim_mm, float(box.size.Y) + 2 * SPEC.print_brim_mm)
        rows.append({"name": item["name"], "required_xy_with_brim_mm": required_xy, "fits_u1": max(required_xy) <= SPEC.u1_usable_xy_mm})
    return {"rows": tuple(rows), "all_fit_u1": all(row["fits_u1"] for row in rows)}


def physical_boundary():
    return {
        "cad_only": True,
        "printed_object_count": 4,
        "sensor_or_electronics_geometry_present": False,
        "sensing_claim": False,
        "gauge_is_datum_only": True,
        "still_requires_print": (
            "PETG capture-ear stiffness and roller running clearance",
            "M3 nut capture and driver access",
            "center-service insertion and removal",
            "future tongue fit",
            "sensor selection and sensing calibration",
        ),
    }
