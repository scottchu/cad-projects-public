"""Deterministic BREP evidence for B3-R1 roller towers."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import hypot, pi

from build123d import Compound, Location

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_validation as r4v
import p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry as b1
import p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_geometry as b2
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as geometry
from p3_v3_mvp_roller_b3_r1_blind_axle_towers_spec import SPEC


P = SPEC.purchased
R = SPEC.ring
FROZEN_HASHES = {
    "p3_v3_mvp_base_q4_r4_functional_centered_step_lap": "9cae6479cca23c38bdfff1bd28e4a7f30b422abede6f28fb6f1ccf4f86f28c3a",
    "p3_v3_mvp_mount_b1_r1_raised_nut_rails": "675de24de9afa6afbcd7a6ba6c0079a1f60e72507a6e4cbe803f732d1c55e2df",
    "p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations": "ac47fc19eb54cd65dc5aedef57bcb8e87ae6048397752def8ec9a45b91a57705",
}


@lru_cache(maxsize=1)
def immutable_hash_evidence() -> dict[str, object]:
    actual = {name: r4v.namespace_tree_hash(name) for name in FROZEN_HASHES}
    return {"expected": FROZEN_HASHES, "actual": actual, "all_unchanged": actual == FROZEN_HASHES}


@lru_cache(maxsize=1)
def center_and_profile_evidence() -> dict[str, object]:
    rows = []
    for angle in SPEC.tower_angles_deg:
        for role, center, carrier, guide, tooth, roller_z in zip(
            R.role_names, R.role_centers_z_mm, R.complete_carrier_z_mm,
            R.smooth_guide_z_mm, R.tooth_face_z_mm, SPEC.roller_z_mm,
        ):
            roller = geometry.roller_shape(role, angle)
            rows.append({
                "angle_deg": angle, "role": role, "center_z_mm": center,
                "roller_z_mm": roller_z, "carrier_z_mm": carrier,
                "guide_z_mm": guide, "tooth_z_mm": tooth,
                "roller_axis_radius_mm": SPEC.axle_radius_mm,
                "solid_count": len(roller.solids()), "valid": roller.is_valid,
            })
    return {"rows": tuple(rows), "all_valid_one_solid": all(r["solid_count"] == 1 and r["valid"] for r in rows)}


@lru_cache(maxsize=1)
def retention_guidance_tooth_evidence() -> dict[str, object]:
    rows = []
    for angle in SPEC.tower_angles_deg:
        for role in R.role_names:
            roller = geometry.roller_shape(role, angle)
            ring = geometry.ring_witness(role)
            rows.append({
                "angle_deg": angle, "role": role,
                "roller_ring_intersection_mm3": geometry.intersection_volume_mm3(roller, ring),
            })
    return {
        "rows": tuple(rows),
        "maximum_roller_ring_intersection_mm3": max(r["roller_ring_intersection_mm3"] for r in rows),
        "race_clearance_mm": R.race_radius_mm-(SPEC.axle_radius_mm+SPEC.roller_guide_radius_mm),
        "tooth_clearance_mm": R.tooth_tip_radius_mm-(SPEC.axle_radius_mm+SPEC.roller_tooth_relief_radius_mm),
        "flange_overlap_mm": SPEC.axle_radius_mm+SPEC.roller_outer_diameter_mm/2.0-R.race_radius_mm,
        "lower_axial_clearance_mm": R.complete_carrier_z_mm[0][0]-(R.role_centers_z_mm[0]-SPEC.roller_groove_width_mm/2.0),
        "upper_axial_clearance_mm": (R.role_centers_z_mm[0]+SPEC.roller_groove_width_mm/2.0)-R.complete_carrier_z_mm[0][1],
        "axial_clearance_total_mm": SPEC.axial_clearance_total_mm,
    }


@lru_cache(maxsize=1)
def fin_and_hall_passage_evidence() -> dict[str, object]:
    stationary = geometry.printed_additions_shape()
    fin_rows = []
    for role in R.role_names:
        fin = geometry.fin_sweep_witness(role)
        fin_rows.append({"role": role, "intersection_mm3": geometry.intersection_volume_mm3(fin, stationary)})
    hall_rows = []
    for angle in SPEC.hall_keepout_angles_deg:
        keepout = geometry.hall_keepout_witness(angle)
        hall_rows.append({"angle_deg": angle, "intersection_mm3": geometry.intersection_volume_mm3(keepout, stationary)})
    return {
        "fin_rows": tuple(fin_rows),
        "maximum_fin_intersection_mm3": max(r["intersection_mm3"] for r in fin_rows),
        "fin_clearance_mm": R.fin_sweep_radius_mm[0]-(SPEC.axle_radius_mm+SPEC.roller_outer_diameter_mm/2.0),
        "hall_rows": tuple(hall_rows),
        "maximum_hall_intersection_mm3": max(r["intersection_mm3"] for r in hall_rows),
    }


@lru_cache(maxsize=1)
def washer_bearing_evidence() -> dict[str, object]:
    rows = []
    for angle in SPEC.tower_angles_deg:
        washers = Compound(children=[geometry.washer_witness(i, angle) for i in range(4)])
        rollers = Compound(children=[geometry.roller_shape(role, angle) for role in R.role_names])
        rows.append({
            "angle_deg": angle,
            "roller_washer_intersection_mm3": geometry.intersection_volume_mm3(rollers, washers),
            "bearing_roller_intersections_mm3": tuple(
                geometry.intersection_volume_mm3(geometry.bearing_witness(role, angle), geometry.roller_shape(role, angle))
                for role in R.role_names
            ),
        })
    return {
        "rows": tuple(rows),
        "maximum_roller_washer_intersection_mm3": max(r["roller_washer_intersection_mm3"] for r in rows),
        "maximum_bearing_roller_intersection_mm3": max(max(r["bearing_roller_intersections_mm3"]) for r in rows),
        "washer_stack_z_mm": SPEC.washer_z_mm,
        "roller_stack_z_mm": SPEC.roller_z_mm,
    }


@lru_cache(maxsize=1)
def radial_roller_insertion_evidence() -> dict[str, object]:
    rows = []
    for angle in SPEC.tower_angles_deg:
        stationary = Compound(children=[geometry.tower_shape(angle), *(geometry.ring_witness(role) for role in R.role_names)])
        for role in R.role_names:
            samples = []
            for index in range(39):
                radius = 80.0+(SPEC.axle_radius_mm-80.0)*index/38.0
                samples.append(geometry.intersection_volume_mm3(geometry.roller_shape(role, angle, radius), stationary))
            rows.append({"angle_deg": angle, "role": role, "sample_count": len(samples), "maximum_intersection_mm3": max(samples)})
    return {"rows": tuple(rows), "maximum_intersection_mm3": max(r["maximum_intersection_mm3"] for r in rows)}


@lru_cache(maxsize=1)
def corrected_axle_interface_evidence() -> dict[str, object]:
    rows = []
    for angle in SPEC.tower_angles_deg:
        riser = b1.spine_riser_shape() if angle == 300.0 else b1.fixed_riser_shape(angle)
        tower = geometry.tower_shape(angle)
        axle = geometry.axle_witness(angle)
        rows.append({
            "angle_deg": angle,
            "tower_riser_intersection_mm3": geometry.intersection_volume_mm3(tower, riser),
            "tower_riser_clearance_mm": tower.distance_to(riser),
            "axle_riser_intersection_mm3": geometry.intersection_volume_mm3(axle, riser),
            "axle_riser_clearance_mm": axle.distance_to(riser),
        })
    return {
        "rows": tuple(rows),
        "maximum_tower_riser_intersection_mm3": max(r["tower_riser_intersection_mm3"] for r in rows),
        "minimum_tower_riser_clearance_mm": min(r["tower_riser_clearance_mm"] for r in rows),
        "maximum_axle_riser_intersection_mm3": max(r["axle_riser_intersection_mm3"] for r in rows),
        "minimum_fixed_axle_riser_clearance_mm": min(r["axle_riser_clearance_mm"] for r in rows if r["angle_deg"] != 300.0),
        "axle_length_mm": SPEC.axle_under_head_z_mm-SPEC.axle_tip_z_mm,
        "blind_pocket_z_mm": SPEC.blind_axle_pocket_z_mm,
        "blind_pocket_depth_mm": SPEC.blind_axle_pocket_z_mm[1]-SPEC.blind_axle_pocket_z_mm[0],
        "blind_floor_mm": SPEC.blind_axle_pocket_z_mm[0]-SPEC.bottom_arm_z_mm[0],
        "no_bottom_nut": True,
    }


@lru_cache(maxsize=1)
def top_nut_access_evidence() -> dict[str, object]:
    rows = []
    shaft_area = pi*(P.axle_diameter_mm/2.0)**2
    for angle in SPEC.tower_angles_deg:
        tower = geometry.tower_shape(angle)
        nut = geometry.top_nut_witness(angle)
        axle = geometry.axle_witness(angle)
        driver = geometry.vertical_cylinder(
            angle, SPEC.axle_radius_mm, 0.0,
            SPEC.top_driver_diameter_mm,
            SPEC.axle_under_head_z_mm,
            30.0,
        )
        rows.append({
            "angle_deg": angle,
            "nut_tower_intersection_mm3": geometry.intersection_volume_mm3(nut, tower),
            "axle_tower_intersection_mm3": geometry.intersection_volume_mm3(axle, tower),
            "engagement_mm": geometry.intersection_volume_mm3(axle, nut)/shaft_area,
            "driver_tower_intersection_mm3": geometry.intersection_volume_mm3(driver, tower),
        })
    return {
        "rows": tuple(rows),
        "maximum_nut_tower_intersection_mm3": max(r["nut_tower_intersection_mm3"] for r in rows),
        "maximum_axle_tower_intersection_mm3": max(r["axle_tower_intersection_mm3"] for r in rows),
        "minimum_engagement_mm": min(r["engagement_mm"] for r in rows),
        "maximum_driver_tower_intersection_mm3": max(r["driver_tower_intersection_mm3"] for r in rows),
        "nut_pocket_z_mm": SPEC.top_nut_pocket_z_mm,
    }


@lru_cache(maxsize=1)
def axle_insertion_extraction_evidence() -> dict[str, object]:
    rows = []
    for angle in SPEC.tower_angles_deg:
        printed = Compound(children=[geometry.tower_shape(angle), *(geometry.roller_shape(role, angle) for role in R.role_names)])
        insertion = []
        for index in range(31):
            dz = 30.0*(30-index)/30.0
            insertion.append(geometry.intersection_volume_mm3(geometry.axle_witness(angle).moved(Location((0,0,dz))), printed))
        extraction = tuple(reversed(insertion))
        rows.append({
            "angle_deg": angle, "sample_count": len(insertion),
            "maximum_insertion_intersection_mm3": max(insertion),
            "maximum_extraction_intersection_mm3": max(extraction),
        })
    return {
        "rows": tuple(rows),
        "maximum_intersection_mm3": max(max(r["maximum_insertion_intersection_mm3"], r["maximum_extraction_intersection_mm3"]) for r in rows),
    }


@lru_cache(maxsize=1)
def b2_powered_mesh_evidence() -> dict[str, object]:
    additions = geometry.printed_additions_shape()
    rows = []
    for q in SPEC.powered_q_mm:
        base = b2.assembled_shape(q)
        rows.append({"q_mm": q, "intersection_mm3": geometry.intersection_volume_mm3(additions, base)})
    return {"rows": tuple(rows), "maximum_intersection_mm3": max(r["intersection_mm3"] for r in rows)}


@lru_cache(maxsize=1)
def envelope_and_print_evidence() -> dict[str, object]:
    tower_rows = []
    for angle in SPEC.tower_angles_deg:
        tower = geometry.tower_shape(angle)
        tower_rows.append({
            "angle_deg": angle,
            "maximum_radius_mm": max(hypot(v.X, v.Y) for v in tower.vertices()),
            "minimum_z_mm": float(tower.bounding_box().min.Z),
            "maximum_z_mm": float(tower.bounding_box().max.Z),
        })
    print_rows = []
    for row in geometry.printable_occurrences():
        box = row["shape"].bounding_box()
        print_rows.append({
            "name": row["name"], "minimum_z_mm": float(box.min.Z),
            "fits_u1": max(float(box.size.X), float(box.size.Y))+2*SPEC.print_brim_mm <= SPEC.u1_usable_xy_mm,
            "solid_count": len(row["shape"].solids()), "valid": row["shape"].is_valid,
        })
    return {
        "tower_rows": tuple(tower_rows),
        "maximum_tower_radius_mm": max(r["maximum_radius_mm"] for r in tower_rows),
        "print_rows": tuple(print_rows),
        "all_flat_on_bed": all(abs(r["minimum_z_mm"]) <= 1e-7 for r in print_rows),
        "all_fit_u1": all(r["fits_u1"] for r in print_rows),
        "all_one_solid_valid": all(r["solid_count"] == 1 and r["valid"] for r in print_rows),
        "print_object_count": len(print_rows),
    }


def physical_validation_boundary() -> dict[str, object]:
    return {
        "cad_acceptance_only": True,
        "still_requires_print": (
            "roller bearing press fit and free rotation",
            "blind axle retention and repeated extraction",
            "ring runout and seam passage",
            "loaded wear, noise, and torque",
        ),
        "later_layers_present": False,
    }


@lru_cache(maxsize=1)
def input_bevel_topology_repair_evidence() -> dict[str, object]:
    """Compare the inherited and topology-clean equivalent bevel witnesses."""
    from OCP.BOPAlgo import BOPAlgo_CheckStatus
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Check

    def self_intersecting(shape) -> bool:
        checker = BRepAlgoAPI_Check(shape.wrapped, True, True)
        checker.Perform()
        if checker.IsValid():
            return False
        return any(
            result.GetCheckStatus() == BOPAlgo_CheckStatus.BOPAlgo_SelfIntersect
            for result in checker.Result()
        )

    rows = []
    for angle in b2.SPEC.station_angles_deg:
        before = b2.input_bevel_witness(angle, 0.0)
        after = geometry.topology_clean_b2_input_bevel_witness(angle, 0.0)
        before_box = before.bounding_box()
        after_box = after.bounding_box()
        before_bounds = tuple(
            float(value)
            for value in (
                before_box.min.X, before_box.min.Y, before_box.min.Z,
                before_box.max.X, before_box.max.Y, before_box.max.Z,
            )
        )
        after_bounds = tuple(
            float(value)
            for value in (
                after_box.min.X, after_box.min.Y, after_box.min.Z,
                after_box.max.X, after_box.max.Y, after_box.max.Z,
            )
        )
        rows.append(
            {
                "angle_deg": angle,
                "before_volume_mm3": float(before.volume),
                "after_volume_mm3": float(after.volume),
                "volume_delta_mm3": abs(float(before.volume)-float(after.volume)),
                "maximum_bounds_delta_mm": max(
                    abs(left-right) for left, right in zip(before_bounds, after_bounds)
                ),
                "before_face_count": len(before.faces()),
                "after_face_count": len(after.faces()),
                "before_edge_count": len(before.edges()),
                "after_edge_count": len(after.edges()),
                "before_self_intersecting": self_intersecting(before),
                "after_self_intersecting": self_intersecting(after),
            }
        )
    return {
        "rows": tuple(rows),
        "maximum_volume_delta_mm3": max(row["volume_delta_mm3"] for row in rows),
        "maximum_bounds_delta_mm": max(row["maximum_bounds_delta_mm"] for row in rows),
        "all_face_edge_counts_preserved": all(
            row["before_face_count"] == row["after_face_count"]
            and row["before_edge_count"] == row["after_edge_count"]
            for row in rows
        ),
        "all_repaired_clean": all(not row["after_self_intersecting"] for row in rows),
    }
