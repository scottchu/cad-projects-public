"""Focused BREP and analytic acceptance evidence for the seven-object mount MVP."""

from __future__ import annotations

from copy import deepcopy
from math import cos, hypot, radians

from build123d import Align, Compound, Cylinder, Location

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_geometry as r4
import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_validation as r4v
import p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry as geometry
from p3_v3_mvp_mount_b1_r1_raised_nut_rails_spec import SPEC


FROZEN_R4_TREE_HASH = "9cae6479cca23c38bdfff1bd28e4a7f30b422abede6f28fb6f1ccf4f86f28c3a"


def isolation_and_locality_evidence() -> dict[str, object]:
    masks = tuple(geometry.modification_mask_shape().children)
    rows = []
    for index, (old, new) in enumerate(zip(r4.quadrant_shapes(), geometry.quadrant_shapes()), 1):
        old_out = deepcopy(old).cut(*(deepcopy(tool) for tool in masks))
        new_out = deepcopy(new).cut(*(deepcopy(tool) for tool in masks))
        rows.append({
            "quadrant": index,
            "old_minus_new_mm3": geometry.volume_mm3(deepcopy(old_out).cut(deepcopy(new_out))),
            "new_minus_old_mm3": geometry.volume_mm3(deepcopy(new_out).cut(deepcopy(old_out))),
        })
    actual = r4v.namespace_tree_hash("p3_v3_mvp_base_q4_r4_functional_centered_step_lap")
    return {
        "expected_r4_hash": FROZEN_R4_TREE_HASH,
        "actual_r4_hash": actual,
        "r4_unchanged": actual == FROZEN_R4_TREE_HASH,
        "rows": tuple(rows),
        "maximum_outside_mask_delta_mm3": max(max(row["old_minus_new_mm3"], row["new_minus_old_mm3"]) for row in rows),
    }


def registry_evidence() -> dict[str, object]:
    rows = geometry.printable_occurrences()
    return {
        "count": len(rows),
        "names": tuple(row["name"] for row in rows),
        "all_one_solid_valid": all(len(row["shape"].solids()) == 1 and row["shape"].is_valid for row in rows),
        "forbidden_drive_component_count": sum(
            any(token in row["name"] for token in ("motor_body", "gear", "bearing", "ring", "fin", "electronic"))
            for row in rows
        ),
    }


def mount_pattern_evidence() -> dict[str, object]:
    rows = tuple(
        (angle, radius, tangent)
        for angle in SPEC.motor_station_angles_deg
        for radius in SPEC.motor_axis_radii_mm
        for tangent in SPEC.motor_tangent_offsets_mm
    )
    printed = geometry.assembled_printed_shape()
    rejected_probes = tuple(
        geometry.vertical_cylinder(
            angle, SPEC.rejected_old_motor_axis_radius_mm, tangent,
            SPEC.m3_clearance_diameter_mm, SPEC.plate_bottom_z_mm, SPEC.plate_top_z_mm - SPEC.plate_bottom_z_mm,
        )
        for angle in SPEC.motor_station_angles_deg
        for tangent in SPEC.motor_tangent_offsets_mm
    )
    outer_driver_rows = tuple(
        geometry.intersection_volume_mm3(
            geometry.driver_path(angle, max(SPEC.motor_axis_radii_mm) + q, tangent),
            printed,
        )
        for angle in SPEC.motor_station_angles_deg
        for tangent in SPEC.motor_tangent_offsets_mm
        for q in (-SPEC.motor_service_travel_mm, 0.0, SPEC.motor_service_travel_mm)
    )
    return {
        "rows": rows,
        "count": len(rows),
        "radii": tuple(sorted({row[1] for row in rows})),
        "rejected_radius_mm": SPEC.rejected_old_motor_axis_radius_mm,
        "minimum_rejected_axis_solid_mm3": min(geometry.intersection_volume_mm3(probe, printed) for probe in rejected_probes),
        "maximum_r109_driver_obstruction_mm3": max(outer_driver_rows),
    }


def motor_nut_sweep_evidence() -> dict[str, object]:
    base = Compound(children=[geometry.named_quadrant(i) for i in range(1, 5)])
    corner_radius = SPEC.m3_nut_max_af_mm / (2.0 * cos(radians(30.0)))
    installed_rows = []
    sweep_rows = []
    for angle in SPEC.motor_station_angles_deg:
        for radius in SPEC.motor_axis_radii_mm:
            outward_open = radius == max(SPEC.motor_axis_radii_mm)
            c0 = radius - SPEC.motor_channel_working_length_mm / 2.0
            c1 = radius + SPEC.motor_channel_working_length_mm / 2.0
            start_radius = c1 + corner_radius + 0.1 if outward_open else c0 - corner_radius - 0.1
            for tangent in SPEC.motor_tangent_offsets_mm:
                for q in (-SPEC.motor_service_travel_mm, 0.0, SPEC.motor_service_travel_mm):
                    installed = geometry.m3_nut_shape(angle, radius + q, tangent, -30.0)
                    installed_rows.append({
                        "angle_deg": angle, "axis_radius_mm": radius, "tangent_mm": tangent, "q_mm": q,
                        "intersection_mm3": geometry.intersection_volume_mm3(installed, base),
                    })
                    end_radius = radius + q
                    samples = tuple(start_radius + (end_radius - start_radius) * i / 10.0 for i in range(11))
                    intersections = tuple(
                        geometry.intersection_volume_mm3(
                            geometry.m3_nut_shape(angle, sample_radius, tangent, -30.0), base
                        )
                        for sample_radius in samples
                    )
                    sweep_rows.append({
                        "angle_deg": angle, "axis_radius_mm": radius, "tangent_mm": tangent, "q_mm": q,
                        "sample_count": len(samples), "maximum_intersection_mm3": max(intersections),
                    })
    return {
        "installed_rows": tuple(installed_rows),
        "sweep_rows": tuple(sweep_rows),
        "maximum_installed_intersection_mm3": max(row["intersection_mm3"] for row in installed_rows),
        "maximum_rigid_sweep_intersection_mm3": max(row["maximum_intersection_mm3"] for row in sweep_rows),
        "nut_clock_deg": -30.0,
        "channel_width_mm": SPEC.nut_channel_width_mm,
        "nut_af_mm": SPEC.m3_nut_max_af_mm,
        "clearance_per_side_mm": (SPEC.nut_channel_width_mm - SPEC.m3_nut_max_af_mm) / 2.0,
        "mouth_throat_mm": SPEC.receiver_nib_throat_mm,
        "insertion_approach_length_mm": SPEC.nut_insertion_approach_length_mm,
    }


def lap_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    depth = 0.0001
    rows = []
    for name, angle, upper, lower in geometry.LAPS:
        upper_probe = r4.donor_plan_tool(angle, SPEC.lap_split_z_mm, depth)
        lower_probe = r4.donor_plan_tool(angle, SPEC.lap_split_z_mm - depth, depth)
        ua = geometry.intersection_volume_mm3(quadrants[upper - 1], upper_probe) / depth
        la = geometry.intersection_volume_mm3(quadrants[lower - 1], lower_probe) / depth
        rows.append({"name": name, "contact_area_mm2": min(ua, la)})
    return {"rows": tuple(rows), "minimum_contact_area_mm2": min(row["contact_area_mm2"] for row in rows)}


def rail_stack_evidence() -> dict[str, object]:
    return {
        "channel_z_mm": (SPEC.receiver_channel_bottom_z_mm, SPEC.receiver_channel_top_z_mm),
        "roof_top_z_mm": SPEC.receiver_roof_top_z_mm,
        "web_above_split_mm": SPEC.receiver_channel_bottom_z_mm - SPEC.lap_split_z_mm,
        "solid_below_channel_mm": SPEC.receiver_channel_bottom_z_mm - SPEC.plate_bottom_z_mm,
        "solid_below_tip_mm": SPEC.receiver_channel_bottom_z_mm - SPEC.receiver_tip_relief_depth_mm - SPEC.plate_bottom_z_mm,
        "motor_channel_length_mm": SPEC.motor_channel_working_length_mm,
        "motor_external_length_mm": SPEC.motor_rail_external_length_mm,
        "sidewall_mm": SPEC.receiver_sidewall_mm,
        "nut_channel_clearance_mm": SPEC.nut_channel_width_mm - SPEC.m3_nut_max_af_mm,
        "mouth_throat_mm": SPEC.receiver_nib_throat_mm,
        "screw_tip_z_mm": SPEC.screw_tip_z_mm,
        "screw_after_nut_mm": SPEC.screw_tip_after_nut_mm,
        "tip_channel_clearance_mm": SPEC.screw_tip_channel_clearance_mm,
        "top_only": True,
    }


def service_sweep_evidence() -> dict[str, object]:
    base = Compound(children=[geometry.named_quadrant(i) for i in range(1, 5)])
    rows = []
    for angle in SPEC.motor_station_angles_deg:
        for q in (-SPEC.motor_service_travel_mm, 0.0, SPEC.motor_service_travel_mm):
            sled = geometry.motor_sled_shape(q, angle)
            rows.append({
                "angle_deg": angle,
                "q_mm": q,
                "valid": sled.is_valid,
                "solids": len(sled.solids()),
                "seated_base_intersection_mm3": geometry.intersection_volume_mm3(sled, base),
                "lifted_removal_intersection_mm3": geometry.intersection_volume_mm3(
                    sled.moved(Location((0, 0, 20))), base
                ),
            })
    shoulder_rows = []
    for angle in SPEC.motor_station_angles_deg:
        for q in (-SPEC.motor_service_travel_mm, 0.0, SPEC.motor_service_travel_mm):
            shoulders = geometry.motor_sled_guide_shoulder_shapes(q, angle)
            rails = tuple(
                geometry._motor_rail_features(angle, radius, tangent)[0]
                for radius in SPEC.motor_axis_radii_mm
                for tangent in SPEC.motor_tangent_offsets_mm
            )
            for shoulder_index, shoulder in enumerate(shoulders):
                tangent = SPEC.motor_tangent_offsets_mm[1] if shoulder_index == 0 else SPEC.motor_tangent_offsets_mm[0]
                relevant = tuple(
                    geometry._motor_rail_features(angle, radius, tangent)[0]
                    for radius in SPEC.motor_axis_radii_mm
                )
                shoulder_rows.append({
                    "angle_deg": angle, "q_mm": q, "side": shoulder_index,
                    "clearance_mm": min(shoulder.distance_to(rail) for rail in relevant),
                })
    max_driver_radius = max(
        hypot(radius, tangent) + SPEC.driver_path_diameter_mm / 2.0
        for radius in (*SPEC.motor_axis_radii_mm, SPEC.fixed_center_radius_mm, SPEC.spine_center_radius_mm)
        for tangent in (
            *SPEC.motor_tangent_offsets_mm,
            *SPEC.fixed_axis_tangent_offsets_mm,
            *SPEC.spine_axis_tangent_offsets_mm,
        )
    )
    return {
        "rows": tuple(rows),
        "all_valid_one_solid": all(row["valid"] and row["solids"] == 1 for row in rows),
        "maximum_lifted_removal_intersection_mm3": max(row["lifted_removal_intersection_mm3"] for row in rows),
        "maximum_seated_base_intersection_mm3": max(row["seated_base_intersection_mm3"] for row in rows),
        "shoulder_rows": tuple(shoulder_rows),
        "minimum_actual_shoulder_clearance_mm": min(row["clearance_mm"] for row in shoulder_rows),
        "maximum_actual_shoulder_clearance_mm": max(row["clearance_mm"] for row in shoulder_rows),
        "guide_clearance_per_side_mm": SPEC.sled_guide_clearance_per_side_mm,
        "load_boss_radius_at_qmax_mm": SPEC.motor_output_witness_radius_mm + SPEC.motor_service_travel_mm + SPEC.sled_load_boss_diameter_mm / 2.0,
        "driver_envelope_max_radius_mm": max_driver_radius,
        "ring_witness_radius_mm": SPEC.ring_tooth_tip_radius_mm,
        "output_overhang_mm": SPEC.motor_output_overhang_from_outer_axis_mm,
    }


def riser_and_bed_evidence() -> dict[str, object]:
    parts = (geometry.fixed_riser_shape(), geometry.spine_riser_shape())
    seated = (geometry.fixed_riser_shape(60.0), geometry.spine_riser_shape())
    base = Compound(children=[geometry.named_quadrant(i) for i in range(1, 5)])
    rows = []
    for part in parts:
        box = part.bounding_box()
        rows.append({
            "label": part.label,
            "solid_count": len(part.solids()),
            "valid": part.is_valid,
            "top_z_mm": float(box.max.Z),
        })
    bed_rows = []
    for row in geometry.printable_occurrences():
        box = row["shape"].bounding_box()
        bed_rows.append({
            "name": row["name"],
            "min_z_mm": float(box.min.Z),
            "span_xy_mm": (float(box.size.X), float(box.size.Y)),
            "fits_u1": max(float(box.size.X), float(box.size.Y)) + 2 * SPEC.print_brim_mm <= SPEC.u1_usable_xy_mm,
        })
    tool_rows = []
    for role, part, angle, radius, tangents in (
        ("fixed", seated[0], 60.0, SPEC.fixed_center_radius_mm, SPEC.fixed_axis_tangent_offsets_mm),
        ("spine", seated[1], SPEC.spine_angle_deg, SPEC.spine_center_radius_mm, SPEC.spine_axis_tangent_offsets_mm),
    ):
        for tangent in tangents:
            tool_rows.append({
                "role": role, "tangent_mm": tangent,
                "screw_intersection_mm3": geometry.intersection_volume_mm3(
                    geometry.m3_screw_shape(angle, radius, tangent), part
                ),
                "driver_intersection_mm3": geometry.intersection_volume_mm3(
                    geometry.driver_path(angle, radius, tangent), part
                ),
            })
    return {
        "riser_rows": tuple(rows),
        "all_risers_fused_valid": all(row["solid_count"] == 1 and row["valid"] for row in rows),
        "maximum_seated_riser_distance_mm": max(part.distance_to(base) for part in seated),
        "interface_plane_z_mm": SPEC.mechanism_interface_z_mm,
        "rise_mm": SPEC.receiver_to_mechanism_interface_rise_mm,
        "bed_rows": tuple(bed_rows),
        "all_on_bed": all(abs(row["min_z_mm"]) <= 1e-7 for row in bed_rows),
        "all_fit_u1": all(row["fits_u1"] for row in bed_rows),
        "quadrant_bottom_z_mm": tuple(float(geometry.named_quadrant(i).bounding_box().min.Z) for i in range(1, 5)),
        "tool_rows": tuple(tool_rows),
        "maximum_screw_intersection_mm3": max(row["screw_intersection_mm3"] for row in tool_rows),
        "maximum_driver_intersection_mm3": max(row["driver_intersection_mm3"] for row in tool_rows),
    }


def physical_validation_boundary() -> dict[str, object]:
    return {
        "cad_acceptance_only": True,
        "still_requires_print": (
            "nut insertion and removal",
            "repeated adjustment cycles",
            "10 N clamp slip and yaw",
            "sled and riser stiffness",
        ),
        "drive_components_authorized": False,
    }
