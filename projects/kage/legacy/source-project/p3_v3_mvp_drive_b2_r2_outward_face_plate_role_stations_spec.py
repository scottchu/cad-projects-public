"""Frozen numeric contract for the isolated B2-R2 corrected drive stations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class PurchasedParts:
    """Single replaceable block for every purchased/catalog part dimension."""

    motor_frame_mm: float = 20.30
    motor_body_length_mm: float = 39.30
    motor_pilot_diameter_mm: float = 16.0
    motor_pilot_height_mm: float = 1.5
    motor_face_pitch_mm: float = 15.4
    motor_mount_thread: str = "M2x0.4"
    motor_mount_thread_depth_mm: float = 2.5
    motor_shaft_diameter_mm: float = 4.0
    motor_shaft_dflat_mm: float = 3.5
    motor_shaft_length_mm: float = 7.0
    motor_mount_screw_diameter_mm: float = 2.0
    motor_mount_screw_length_mm: float = 4.0

    spur_module_mm: float = 1.0
    spur_tooth_count: int = 16
    spur_pitch_radius_mm: float = 8.0
    spur_root_radius_mm: float = 6.75
    spur_tip_radius_mm: float = 9.0
    spur_face_mm: float = 2.1
    spur_bore_diameter_mm: float = 4.1
    spur_bore_dflat_mm: float = 3.6
    input_set_screw_diameter_mm: float = 3.0
    input_set_screw_length_mm: float = 3.0

    miter_ratio: float = 1.0
    miter_axis_offset_mm: float = 5.11
    miter_envelope_radius_mm: float = 5.0
    miter_face_mm: float = 3.0

    bearing_bore_mm: float = 4.0
    bearing_od_mm: float = 8.0
    bearing_width_mm: float = 3.0
    bearing_pocket_diameter_mm: float = 8.2
    bearing_pocket_depth_mm: float = 3.1
    shaft_min_diameter_mm: float = 3.99
    shaft_max_diameter_mm: float = 4.0
    collar_bore_mm: float = 4.0
    collar_od_mm: float = 8.0
    collar_width_mm: float = 4.0
    collar_set_screw_diameter_mm: float = 3.0
    shim_od_mm: float = 8.0
    shim_id_mm: float = 4.1
    shim_thickness_mm: float = 0.2

    seam_screw_length_mm: float = 6.0
    mount_screw_length_mm: float = 8.0
    m3_nut_af_mm: float = 5.5
    m3_nut_thickness_mm: float = 2.4


@dataclass(frozen=True)
class B2Spec:
    purchased: PurchasedParts = PurchasedParts()

    station_angles_deg: tuple[float, ...] = (0.0, 120.0, 240.0)
    station_roles: tuple[str, ...] = ("hour", "minute", "second")
    service_q_mm: tuple[float, ...] = (-2.5, -0.35, 0.0, 0.10, 2.5)
    powered_q_mm: tuple[float, ...] = (-0.35, 0.0, 0.10)

    # B2-R2 corrected radial interface. All values translate together by q.
    shaft_radius_nominal_mm: float = 122.0
    motor_face_radius_nominal_mm: float = 112.0
    motor_pilot_outer_face_radius_nominal_mm: float = 113.5
    motor_rear_radius_nominal_mm: float = 72.7
    input_bevel_center_radius_nominal_mm: float = 116.89
    input_bevel_rear_radius_nominal_mm: float = 115.19
    input_bevel_front_radius_nominal_mm: float = 118.59
    output_bevel_inward_tooth_radius_nominal_mm: float = 118.69
    output_shaft_inward_surface_radius_nominal_mm: float = 120.0
    motor_shaft_max_endpoint_radius_nominal_mm: float = 119.25
    tower_pocket_inward_radius_nominal_mm: float = 117.9
    bracket_plane_radius_nominal_mm: float = 112.0
    bracket_outer_radius_nominal_mm: float = 114.0

    motor_input_axis_z_mm: float = -10.0
    printed_max_z_mm: float = -5.2
    bracket_thickness_mm: float = 2.0
    face_plate_tangential_width_mm: float = 22.3
    face_plate_z_mm: tuple[float, float] = (-21.15, 1.15)
    motor_face_opening_diameter_mm: float = 16.2
    m2_clearance_diameter_mm: float = 2.3
    m2_face_axes_tangential_mm: tuple[float, ...] = (-7.7, 7.7)
    m2_face_axes_z_mm: tuple[float, ...] = (-17.7, -2.3)
    m2_screw_head_diameter_mm: float = 4.0
    m2_screw_head_height_mm: float = 2.0
    m2_driver_diameter_mm: float = 4.5
    m2_driver_outer_radius_mm: float = 150.0
    m2_screw_tip_radius_mm: float = 110.0
    m2_thread_engagement_mm: float = 2.0
    cheek_radial_mm: tuple[float, float] = (105.0, 114.0)
    cheek_tangential_abs_mm: tuple[float, float] = (11.15, 13.15)
    cheek_z_mm: tuple[float, float] = (-23.5, 1.5)
    bottom_bridge_radial_mm: tuple[float, float] = (105.0, 114.0)
    bottom_bridge_tangential_mm: tuple[float, float] = (-13.15, 13.15)
    bottom_bridge_z_mm: tuple[float, float] = (-23.5, -21.5)
    bare_motor_face_insertion_start_radius_mm: float = 67.0
    face_plate_input_gear_gap_mm: float = 1.19
    m3_tool_diameter_mm: float = 6.5

    wire_keepout_radial_mm: float = 2.0
    wire_keepout_tangential_mm: float = 14.0
    wire_keepout_axial_mm: float = 10.0
    center_keepout_radius_mm: float = 66.0
    minimum_wire_margin_mm: float = 2.2

    input_bevel_radial_length_mm: float = 3.4
    input_bevel_center_from_face_mm: float = 4.89
    nominal_tooth_clearance_mm: float = 0.10
    powered_engagement_mm: tuple[float, ...] = (0.16, 0.41, 0.66)
    powered_backlash_mm: tuple[float, ...] = (0.20, 0.14, 0.08)
    minimum_pilot_bearing_clearance_mm: float = 4.4
    minimum_shaft_clearance_mm: float = 0.75

    ring_tooth_count: int = 260
    ring_module_mm: float = 1.0
    ring_witness_inner_radius_mm: float = 129.0
    ring_witness_outer_radius_mm: float = 138.9
    expected_ratio: float = 16.25
    plate_outer_radius_mm: float = 150.0
    fin_keepout_radius_mm: float = 143.7
    roller_keepout_radius_mm: float = 118.0
    roller_keepout_angles_deg: tuple[float, ...] = (60.0, 180.0)
    spine_keepout_radius_mm: float = 100.0
    spine_keepout_angle_deg: float = 300.0

    lower_collar_z_mm: tuple[float, float] = (-19.0, -15.0)
    lower_bearing_z_mm: tuple[float, float] = (-14.8, -11.8)
    lower_shim_z_mm: tuple[float, float] = (-11.8, -11.6)
    miter_z_mm: tuple[float, float] = (-11.55, -8.55)
    upper_shim_z_mm: tuple[float, float] = (-8.5, -8.3)
    upper_bearing_z_mm: tuple[float, float] = (-8.3, -5.3)
    designed_endplay_mm: float = 0.10
    endplay_range_mm: tuple[float, float] = (0.05, 0.15)

    role_pinion_z_mm: tuple[tuple[float, float], ...] = ((0.0, 2.1), (6.7, 8.8), (13.4, 15.5))
    role_spacer_length_mm: tuple[float, ...] = (5.3, 12.0, 18.7)
    role_upper_collar_z_mm: tuple[tuple[float, float], ...] = ((2.2, 6.2), (8.9, 12.9), (15.6, 19.6))
    role_shaft_length_mm: tuple[float, ...] = (26.0, 33.0, 40.0)

    tower_outer_diameter_mm: float = 15.0
    tower_window_radial_mm: tuple[float, float] = (114.8, 120.0)
    tower_window_tangential_mm: float = 10.0
    tower_window_z_mm: tuple[float, float] = (-12.0, -8.0)
    cradle_wall_mm: float = 2.0
    cradle_clearance_mm: float = 0.35
    motor_pocket_floor_mm: float = 2.0
    fit_clearance_mm: float = 0.10
    brep_tolerance_mm3: float = 1e-6
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15
    u1_usable_xy_mm: float = 260.0
    print_brim_mm: float = 5.0


SPEC = B2Spec()
