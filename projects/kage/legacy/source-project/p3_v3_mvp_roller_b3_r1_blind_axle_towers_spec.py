"""Frozen numeric contract for B3-R1 stationary C-bar roller towers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_roller_b3_r1_blind_axle_towers"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class PurchasedRollerHardware:
    bearing_name: str = "623ZZ"
    bearing_bore_mm: float = 3.0
    bearing_od_mm: float = 10.0
    bearing_width_mm: float = 4.0
    bearing_pocket_diameter_mm: float = 10.2
    bearing_pocket_depth_mm: float = 4.1
    axle_name: str = "M3x25_top_retained_blind_axle"
    axle_diameter_mm: float = 3.0
    axle_length_mm: float = 25.0
    axle_head_diameter_mm: float = 5.5
    axle_head_height_mm: float = 3.0
    top_nut_af_mm: float = 5.5
    top_nut_pocket_af_mm: float = 5.7
    top_nut_thickness_mm: float = 2.4
    top_nut_pocket_depth_mm: float = 2.6
    washer_id_mm: float = 3.2
    washer_od_mm: float = 7.0
    washer_thickness_mm: float = 0.5
    tower_mount_screw_diameter_mm: float = 3.0
    tower_mount_screw_length_mm: float = 8.0


@dataclass(frozen=True)
class RingGeometryAssumptions:
    role_names: tuple[str, ...] = ("hour", "minute", "second")
    role_centers_z_mm: tuple[float, ...] = (0.0, 6.7, 13.4)
    carrier_thickness_mm: float = 4.4
    complete_carrier_z_mm: tuple[tuple[float, float], ...] = ((-2.2, 2.2), (4.5, 8.9), (11.2, 15.6))
    smooth_guide_z_mm: tuple[tuple[float, float], ...] = ((-2.1, -0.1), (4.6, 6.6), (11.3, 13.3))
    tooth_face_z_mm: tuple[tuple[float, float], ...] = ((0.0, 2.1), (6.7, 8.8), (13.4, 15.5))
    race_radius_mm: float = 131.6
    tooth_tip_radius_mm: float = 129.0
    body_outer_radius_mm: float = 138.9
    fin_sweep_radius_mm: tuple[float, float] = (136.1, 143.7)


@dataclass(frozen=True)
class B3Spec:
    purchased: PurchasedRollerHardware = PurchasedRollerHardware()
    ring: RingGeometryAssumptions = RingGeometryAssumptions()

    tower_angles_deg: tuple[float, ...] = (60.0, 180.0, 300.0)
    axle_radius_mm: float = 118.0
    spine_landing_radius_mm: float = 100.0
    tower_max_radius_mm: float = 120.0

    roller_outer_diameter_mm: float = 30.0
    roller_total_height_mm: float = 6.2
    roller_groove_width_mm: float = 4.7
    roller_flange_thickness_mm: float = 0.75
    roller_guide_radius_mm: float = 13.45
    roller_tooth_relief_radius_mm: float = 10.6
    roller_axle_bore_diameter_mm: float = 3.4

    race_clearance_mm: float = 0.15
    tooth_clearance_mm: float = 0.4
    flange_overlap_mm: float = 1.4
    fin_clearance_mm: float = 3.1
    axial_clearance_total_mm: float = 0.3

    washer_z_mm: tuple[tuple[float, float], ...] = ((-3.6, -3.1), (3.1, 3.6), (9.8, 10.3), (16.5, 17.0))
    roller_z_mm: tuple[tuple[float, float], ...] = ((-3.1, 3.1), (3.6, 9.8), (10.3, 16.5))

    bottom_arm_z_mm: tuple[float, float] = (-5.0, -3.6)
    top_arm_z_mm: tuple[float, float] = (17.0, 20.4)
    arm_riser_clearance_mm: float = 0.2
    cbar_radial_mm: tuple[float, float] = (114.0, 120.0)
    cbar_tangential_mm: tuple[float, float] = (-11.2, 17.2)
    side_web_tangential_mm: tuple[float, float] = (15.2, 17.2)

    axle_under_head_z_mm: float = 20.4
    axle_tip_z_mm: float = -4.6
    axle_tip_riser_clearance_mm: float = 0.6
    blind_axle_pocket_diameter_mm: float = 3.2
    blind_axle_pocket_z_mm: tuple[float, float] = (-4.6, -3.6)
    blind_floor_mm: float = 0.4
    lower_mount_bore_diameter_mm: float = 3.3
    top_axle_bore_diameter_mm: float = 3.4
    top_nut_pocket_z_mm: tuple[float, float] = (17.6, 20.2)
    top_nut_min_engagement_mm: float = 2.4
    top_driver_diameter_mm: float = 6.5
    mount_axis_tangent_mm: tuple[float, float] = (-7.0, 7.0)

    hall_keepout_angles_deg: tuple[float, ...] = (90.0, 210.0, 330.0)
    hall_keepout_radial_mm: tuple[float, float] = (124.0, 146.0)
    hall_keepout_z_mm: tuple[float, float] = (-4.0, 18.0)
    hall_keepout_half_angle_deg: float = 6.0

    powered_q_mm: tuple[float, ...] = (-0.35, 0.0, 0.10)
    brep_tolerance_mm3: float = 1e-6
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15
    u1_usable_xy_mm: float = 260.0
    print_brim_mm: float = 5.0


SPEC = B3Spec()
