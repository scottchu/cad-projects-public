"""Focused BREP acceptance evidence for the B2-R2 populated drive stations."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import pi

from build123d import Compound, Location

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_validation as r4v
import p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry as b1
import p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_geometry as geometry
from p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_spec import SPEC


FROZEN_R4_TREE_HASH = "9cae6479cca23c38bdfff1bd28e4a7f30b422abede6f28fb6f1ccf4f86f28c3a"
FROZEN_B1_TREE_HASH = "675de24de9afa6afbcd7a6ba6c0079a1f60e72507a6e4cbe803f732d1c55e2df"


@lru_cache(maxsize=1)
def bracket_collision_evidence() -> dict[str, object]:
    rows = []
    for role in SPEC.station_roles:
        for q in SPEC.service_q_mm:
            body = geometry.motor_body_witness(0.0, q)
            plate = geometry.face_plate_shape(role, q_mm=q)
            features = (plate, *geometry.cheek_shapes(q), geometry.bottom_bridge_shape(q))
            rows.append({
                "role": role,
                "q_mm": q,
                "body_feature_intersections_mm3": tuple(
                    geometry.intersection_volume_mm3(body, feature) for feature in features
                ),
                "body_plate_distance_mm": body.distance_to(plate),
                "body_outer_radius_mm": float(body.bounding_box().max.X),
                "plate_inner_radius_mm": float(plate.bounding_box().min.X),
            })
    return {
        "rows": tuple(rows),
        "maximum_forbidden_intersection_mm3": max(max(row["body_feature_intersections_mm3"]) for row in rows),
        "maximum_face_plane_error_mm": max(abs(row["body_outer_radius_mm"]-row["plate_inner_radius_mm"]) for row in rows),
        "all_face_contact_distance_zero": all(row["body_plate_distance_mm"] <= 1e-7 for row in rows),
    }


@lru_cache(maxsize=1)
def pilot_and_m2_evidence() -> dict[str, object]:
    pilot_rows = []
    screw_rows = []
    expected_axes = tuple(
        (tangent, z)
        for tangent in SPEC.m2_face_axes_tangential_mm
        for z in SPEC.m2_face_axes_z_mm
    )
    for q in SPEC.service_q_mm:
        printed = geometry.printed_station_sled("hour", q)
        pilot = geometry.motor_pilot_witness(0.0, q)
        tower = geometry.tower_actual_solid("hour", q)
        pilot_rows.append({
            "q_mm": q,
            "pilot_printed_intersection_mm3": geometry.intersection_volume_mm3(pilot, printed),
            "pilot_tower_intersection_mm3": geometry.intersection_volume_mm3(pilot, tower),
            "pilot_tower_clearance_mm": pilot.distance_to(tower),
        })
        motor = geometry.motor_body_witness(0.0, q)
        plate = geometry.face_plate_shape("hour", q_mm=q)
        for axis, screw in zip(expected_axes, geometry.motor_m2_screw_witnesses(0.0, q)):
            engagement_volume = geometry.intersection_volume_mm3(screw, motor)
            screw_rows.append({
                "q_mm": q,
                "axis": axis,
                "engagement_mm": engagement_volume/(pi*(SPEC.purchased.motor_mount_screw_diameter_mm/2.0)**2),
                "screw_plate_intersection_mm3": geometry.intersection_volume_mm3(screw, plate),
            })
    return {
        "pilot_rows": tuple(pilot_rows),
        "opening_radial_clearance_per_side_mm": (SPEC.motor_face_opening_diameter_mm-SPEC.purchased.motor_pilot_diameter_mm)/2.0,
        "minimum_pilot_tower_clearance_mm": min(row["pilot_tower_clearance_mm"] for row in pilot_rows),
        "maximum_pilot_printed_intersection_mm3": max(row["pilot_printed_intersection_mm3"] for row in pilot_rows),
        "maximum_pilot_tower_intersection_mm3": max(row["pilot_tower_intersection_mm3"] for row in pilot_rows),
        "axes": expected_axes,
        "axis_pitch_tangential_mm": max(SPEC.m2_face_axes_tangential_mm)-min(SPEC.m2_face_axes_tangential_mm),
        "axis_pitch_z_mm": max(SPEC.m2_face_axes_z_mm)-min(SPEC.m2_face_axes_z_mm),
        "screw_rows": tuple(screw_rows),
        "minimum_engagement_mm": min(row["engagement_mm"] for row in screw_rows),
        "maximum_engagement_mm": max(row["engagement_mm"] for row in screw_rows),
        "maximum_screw_plate_intersection_mm3": max(row["screw_plate_intersection_mm3"] for row in screw_rows),
        "guaranteed_thread_depth_mm": SPEC.purchased.motor_mount_thread_depth_mm,
    }


@lru_cache(maxsize=1)
def driver_and_insertion_evidence() -> dict[str, object]:
    driver_rows = []
    insertion_rows = []
    bevel_rows = []
    for q in SPEC.service_q_mm:
        printed = geometry.printed_station_sled("hour", q)
        for tangent, z in geometry._motor_m2_axes():
            driver_rows.append({
                "q_mm": q,
                "axis": (tangent, z),
                "intersection_mm3": geometry.intersection_volume_mm3(
                    geometry.m2_driver_path(0.0, q, tangent, z), printed
                ),
            })
        face_end = SPEC.motor_face_radius_nominal_mm+q
        intersections = []
        for index in range(46):
            face = SPEC.bare_motor_face_insertion_start_radius_mm + (
                face_end-SPEC.bare_motor_face_insertion_start_radius_mm
            )*index/45.0
            intersections.append(
                geometry.intersection_volume_mm3(
                    geometry.bare_motor_at_face_witness(0.0, face), printed
                )
            )
        insertion_rows.append({"q_mm": q, "sample_count": len(intersections), "maximum_intersection_mm3": max(intersections)})
    for q in SPEC.powered_q_mm:
        printed = geometry.printed_station_sled("hour", q)
        mounted = Compound(children=[
            geometry.motor_body_witness(0.0, q),
            geometry.motor_pilot_witness(0.0, q),
            *geometry.motor_m2_screw_witnesses(0.0, q),
        ])
        printed_ivs = []
        mounted_ivs = []
        for index in range(12):
            rear = SPEC.bracket_outer_radius_nominal_mm+0.1+q + (
                SPEC.input_bevel_rear_radius_nominal_mm-(SPEC.bracket_outer_radius_nominal_mm+0.1)
            )*index/11.0
            dx = rear-(SPEC.input_bevel_rear_radius_nominal_mm+q)
            gear = geometry.input_bevel_witness(0.0, q).moved(Location((dx, 0.0, 0.0)))
            printed_ivs.append(geometry.intersection_volume_mm3(gear, printed))
            mounted_ivs.append(geometry.intersection_volume_mm3(gear, mounted))
        bevel_rows.append({
            "q_mm": q,
            "sample_count": len(printed_ivs),
            "maximum_printed_intersection_mm3": max(printed_ivs),
            "maximum_mounted_nonshaft_intersection_mm3": max(mounted_ivs),
        })
    return {
        "driver_rows": tuple(driver_rows),
        "maximum_driver_intersection_mm3": max(row["intersection_mm3"] for row in driver_rows),
        "insertion_rows": tuple(insertion_rows),
        "maximum_motor_insertion_intersection_mm3": max(row["maximum_intersection_mm3"] for row in insertion_rows),
        "bevel_rows": tuple(bevel_rows),
        "maximum_bevel_insertion_intersection_mm3": max(
            max(row["maximum_printed_intersection_mm3"], row["maximum_mounted_nonshaft_intersection_mm3"])
            for row in bevel_rows
        ),
    }


@lru_cache(maxsize=1)
def corrected_drive_evidence() -> dict[str, object]:
    bevel_rows = []
    for q, engagement in zip(SPEC.powered_q_mm, SPEC.powered_engagement_mm):
        input_bevel = geometry.input_bevel_witness(0.0, q)
        output_bevel = geometry.output_bevel_witness(0.0, q)
        bevel_rows.append({
            "q_mm": q,
            "intersection_mm3": geometry.intersection_volume_mm3(input_bevel, output_bevel),
            "backlash_mm": input_bevel.distance_to(output_bevel),
            "engagement_mm": engagement,
        })
    max_motor_shaft = geometry.motor_shaft_witness(0.0, 0.0, maximum=True)
    output_shaft = geometry.output_stack_witnesses("hour", 0.0, 0.0)[0]
    face_plate = geometry.face_plate_shape("hour")
    input_bevel = geometry.input_bevel_witness(0.0, 0.0)
    wire = geometry.wire_keepout_witness(0.0, min(SPEC.service_q_mm))
    return {
        "bevel_rows": tuple(bevel_rows),
        "maximum_bevel_intersection_mm3": max(row["intersection_mm3"] for row in bevel_rows),
        "minimum_backlash_mm": min(row["backlash_mm"] for row in bevel_rows),
        "maximum_backlash_mm": max(row["backlash_mm"] for row in bevel_rows),
        "engagements_mm": tuple(row["engagement_mm"] for row in bevel_rows),
        "maximum_shaft_clearance_mm": max_motor_shaft.distance_to(output_shaft),
        "wire_min_radius_mm": float(wire.bounding_box().min.X),
        "wire_center_margin_mm": float(wire.bounding_box().min.X)-SPEC.center_keepout_radius_mm,
        "face_plate_input_gear_radial_gap_mm": float(input_bevel.bounding_box().min.X)-float(face_plate.bounding_box().max.X),
    }


@lru_cache(maxsize=1)
def service_and_registry_evidence() -> dict[str, object]:
    base = Compound(children=[b1.named_quadrant(i) for i in range(1, 5)])
    service_rows = []
    purchased_rows = []
    for q in SPEC.service_q_mm:
        sled = geometry.printed_station_sled("hour", q)
        service_rows.append({
            "q_mm": q,
            "valid": sled.is_valid,
            "solid_count": len(sled.solids()),
            "base_intersection_mm3": geometry.intersection_volume_mm3(sled, base),
        })
        for part in geometry.station_purchased_witnesses("hour", 0.0, q):
            purchased_rows.append({"q_mm": q, "label": part.label, "printed_intersection_mm3": geometry.intersection_volume_mm3(part, sled)})
    registry = geometry.printable_occurrences()
    nonpinion = [part for part in geometry.station_purchased_witnesses("hour", 0.0, 0.0) if "16T_output_pinion" not in part.label]
    return {
        "service_rows": tuple(service_rows),
        "all_service_valid_one_solid": all(row["valid"] and row["solid_count"] == 1 for row in service_rows),
        "maximum_base_intersection_mm3": max(row["base_intersection_mm3"] for row in service_rows),
        "maximum_purchased_printed_intersection_mm3": max(row["printed_intersection_mm3"] for row in purchased_rows),
        "registry_count": len(registry),
        "registry_names": tuple(row["name"] for row in registry),
        "all_registry_one_solid_valid": all(len(row["shape"].solids()) == 1 and row["shape"].is_valid for row in registry),
        "maximum_nonpinion_radius_mm": max(float(part.bounding_box().max.X) for part in nonpinion),
    }


@lru_cache(maxsize=1)
def immutable_interface_evidence() -> dict[str, object]:
    r4_hash = r4v.namespace_tree_hash("p3_v3_mvp_base_q4_r4_functional_centered_step_lap")
    b1_hash = r4v.namespace_tree_hash("p3_v3_mvp_mount_b1_r1_raised_nut_rails")
    quadrants = tuple(b1.named_quadrant(i) for i in range(1, 5))
    base = Compound(children=list(quadrants))
    box = base.bounding_box()
    return {
        "r4_hash": r4_hash,
        "b1_hash": b1_hash,
        "r4_unchanged": r4_hash == FROZEN_R4_TREE_HASH,
        "b1_unchanged": b1_hash == FROZEN_B1_TREE_HASH,
        "base_underside_z_mm": tuple(float(q.bounding_box().min.Z) for q in quadrants),
        "output_axis_radius_mm": SPEC.shaft_radius_nominal_mm,
        "role_pinion_z_mm": SPEC.role_pinion_z_mm,
        "center_keepout_radius_mm": SPEC.center_keepout_radius_mm,
        "base_envelope_diameter_mm": max(float(box.size.X), float(box.size.Y)),
    }


def physical_validation_boundary() -> dict[str, object]:
    return {
        "cad_acceptance_only": True,
        "still_requires_print": (
            "motor insertion and four-screw access",
            "bearing and bevel fit",
            "backlash under load",
            "sled stiffness and repeated service travel",
        ),
        "later_layers_present": False,
    }
