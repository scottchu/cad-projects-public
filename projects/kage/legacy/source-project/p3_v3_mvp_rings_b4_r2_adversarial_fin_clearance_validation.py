"""Actual-BREP adversarial fin-clearance evidence for B4-R2."""

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin

from build123d import Axis

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_validation as hashes
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_geometry as pinions
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_spec as pinion_spec
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_geometry as rings
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_spec as ring_spec
import p3_v3_mvp_rings_b4_r1_exact_involute_mesh_geometry as accepted_geometry
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as rollers
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_spec as roller_spec
from p3_v3_mvp_rings_b4_r2_adversarial_fin_clearance_spec import SPEC


R = ring_spec.SPEC.ring
P = pinion_spec.SPEC


def accepted_b4_r1_immutable_evidence():
    actual = hashes.namespace_tree_hash("p3_v3_mvp_rings_b4_r1_exact_involute_mesh")
    return {
        "expected": SPEC.accepted_b4_r1_tree_hash,
        "actual": actual,
        "unchanged": actual == SPEC.accepted_b4_r1_tree_hash,
    }


def _iv(left, right):
    common = deepcopy(left).intersect(deepcopy(right))
    return 0.0 if common is None else float(sum(solid.volume for solid in common.solids()))


@lru_cache(maxsize=1)
def nearest_fin_evidence():
    rows = []
    for role, role_name in enumerate(R.roles):
        roller_pose = SPEC.roller_fin_pose_deg[role]
        roller_target_pose = roller_spec.SPEC.tower_angles_deg[role]
        fin_at_roller = rings.fin_shape(role).rotate(Axis.Z, roller_pose)
        roller = rollers.roller_shape(role_name, roller_target_pose)
        rows.append(
            {
                "role": role_name,
                "target": "roller",
                "fin_pose_deg": roller_pose,
                "target_pose_deg": roller_target_pose,
                "pose_error_deg": abs(roller_pose - roller_target_pose),
                "iv_mm3": _iv(fin_at_roller, roller),
                "distance_mm": fin_at_roller.distance_to(roller),
            }
        )

        pinion_pose = SPEC.pinion_fin_pose_deg[role]
        pinion_target_pose = P.station_angles_deg[role]
        fin_at_pinion = rings.fin_shape(role).rotate(Axis.Z, pinion_pose)
        pinion = pinions.exact_output_pinion(role, 0.0, 0.0)
        rows.append(
            {
                "role": role_name,
                "target": "exact_pinion",
                "fin_pose_deg": pinion_pose,
                "target_pose_deg": pinion_target_pose,
                "pose_error_deg": abs(pinion_pose - pinion_target_pose),
                "iv_mm3": _iv(fin_at_pinion, pinion),
                "distance_mm": fin_at_pinion.distance_to(pinion),
            }
        )

    roller_rows = tuple(row for row in rows if row["target"] == "roller")
    pinion_rows = tuple(row for row in rows if row["target"] == "exact_pinion")
    return {
        "rows": tuple(rows),
        "roller_rows": roller_rows,
        "pinion_rows": pinion_rows,
        "maximum_iv_mm3": max(row["iv_mm3"] for row in rows),
        "maximum_pose_error_deg": max(row["pose_error_deg"] for row in rows),
        "minimum_roller_distance_mm": min(row["distance_mm"] for row in roller_rows),
        "maximum_roller_distance_mm": max(row["distance_mm"] for row in roller_rows),
        "minimum_exact_pinion_distance_mm": min(row["distance_mm"] for row in pinion_rows),
        "maximum_exact_pinion_distance_mm": max(row["distance_mm"] for row in pinion_rows),
    }


@lru_cache(maxsize=1)
def magnet_sensor_position_evidence():
    magnet_rows = []
    for role, (z0, z1) in enumerate(R.carrier_z_mm):
        angle = radians(ring_spec.SPEC.magnets.angle_deg)
        radius = ring_spec.SPEC.magnets.center_radius_mm
        magnet_rows.append(
            {
                "role": R.roles[role],
                "angle_deg": ring_spec.SPEC.magnets.angle_deg,
                "center_xyz_mm": (radius * cos(angle), radius * sin(angle), (z0 + z1) / 2),
            }
        )

    labels = tuple(str(child.label or "") for child in accepted_geometry.assembled_shape().children)
    sensor_labels = tuple(
        label
        for label in labels
        if (
            "sensor" in label.lower()
            or ("hall" in label.lower() and "keepout" not in label.lower())
        )
    )
    return {
        "rows": tuple(magnet_rows),
        "assembly_occurrence_count": len(labels),
        "sensor_occurrence_labels": sensor_labels,
        "sensor_occurrence_count": len(sensor_labels),
        "no_sensor_solids_added": len(sensor_labels) == 0,
    }


def physical_boundary():
    return {
        "cad_only": True,
        "b5_present": False,
        "geometry_changed_from_b4_r1": False,
        "still_requires_print": (
            "fin clearance under flex and runout",
            "roller motion under load",
            "exact pinion mesh under load",
            "magnet sensing",
        ),
    }
