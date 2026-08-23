"""Frozen numeric contract for the Q4-R4 functional MVP chassis.

The plate grows rearward from the locked clock mounting datum.  All values are
millimetres/degrees and all future component placeholders remain named, non-
cutting interface reservations until purchased parts are selected.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_base_q4_r4_functional_centered_step_lap"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class FunctionalCenteredStepLapSpec:
    # Base envelope and locked world datum.
    base_outer_radius_mm: float = 150.0
    base_inner_radius_mm: float = 66.0
    plate_top_z_mm: float = -25.5
    plate_bottom_z_mm: float = -31.5
    plate_nominal_thickness_mm: float = 6.0
    quadrant_count: int = 4
    seam_angles_deg: tuple[float, ...] = (45.0, 135.0, 225.0, 315.0)
    seam_relief_per_face_mm: float = 0.05

    # Centered complementary 3 + 3 mm step-lap.
    lap_r_min_mm: float = 70.0
    lap_r_max_mm: float = 116.0
    donor_t_min_mm: float = -13.0
    donor_t_max_mm: float = 13.0
    receiver_r_min_mm: float = 69.8
    receiver_r_max_mm: float = 116.2
    receiver_t_min_mm: float = -13.2
    receiver_t_max_mm: float = 13.2
    lap_split_z_mm: float = -28.5
    lower_land_thickness_mm: float = 3.0
    upper_lap_thickness_mm: float = 3.0
    plan_clearance_per_edge_mm: float = 0.2
    # The resolved acceptance metric is true mutual split-plane contact after
    # both AF5.8 traps and their 0.30 entry leads, not upper-donor area alone.
    # Mandatory R88 motor slots cross S12/S23, so all mount voids are counted.
    # Expected net: S12/S23 ~1098.37; S34/S41 ~1125.06.
    actual_mutual_split_plane_contact_area_min_mm2: float = 1095.0
    free_edge_chamfer_mm: float = 0.3

    # Seam stack: top boss, upper clearance, captive ordinary metal nut.
    screws_per_seam: int = 2
    seam_screw_axis_radii_mm: tuple[float, float] = (82.0, 104.0)
    seam_screw_axis_tangent_mm: float = 0.0
    upper_clearance_hole_diameter_mm: float = 3.4
    bearing_boss_diameter_mm: float = 8.0
    bearing_boss_height_mm: float = 0.5
    screw_under_head_z_mm: float = -25.0
    m3_screw_nominal_diameter_mm: float = 3.0
    m3_screw_length_mm: float = 6.0
    m3_socket_head_max_diameter_mm: float = 5.5
    m3_socket_head_height_mm: float = 3.0
    driver_hex_mm: float = 2.5
    driver_path_diameter_mm: float = 8.0
    driver_path_length_mm: float = 25.0
    m3_nut_max_af_mm: float = 5.5
    m3_nut_max_thickness_mm: float = 2.4
    nut_trap_af_mm: float = 5.8
    nut_trap_depth_mm: float = 2.5
    nut_trap_entry_chamfer_mm: float = 0.3
    nut_axial_slack_mm: float = 0.1
    tip_relief_diameter_mm: float = 3.4
    tip_relief_depth_mm: float = 0.2
    nut_trap_bottom_z_mm: float = -31.0
    tip_relief_bottom_z_mm: float = -31.2
    minimum_underside_floor_mm: float = 0.3

    # Authoritative Revision-K plate interfaces.
    motor_station_angles_deg: tuple[float, float, float] = (0.0, 120.0, 240.0)
    motor_slot_axis_radii_mm: tuple[float, float] = (88.0, 126.0)
    motor_slot_tangent_offsets_mm: tuple[float, float] = (-12.0, 12.0)
    motor_slot_width_mm: float = 3.6
    motor_slot_overall_length_mm: float = 8.6
    motor_service_travel_mm: float = 2.5
    motor_powered_q_min_mm: float = -0.35
    motor_powered_q_max_mm: float = 0.10
    motor_output_axis_radius_mm: float = 122.0
    motor_clamp_washer_outer_diameter_mm: float = 7.0
    motor_driver_path_diameter_mm: float = 6.5

    fixed_tower_angles_deg: tuple[float, float] = (60.0, 180.0)
    fixed_tower_center_radius_mm: float = 118.0
    fixed_tower_landing_radial_mm: float = 12.0
    fixed_tower_landing_tangential_mm: float = 18.0
    spine_angle_deg: float = 300.0
    spine_center_radius_mm: float = 100.0
    spine_foot_radial_mm: float = 20.0
    spine_foot_tangential_mm: float = 24.0
    spine_mount_tangent_offsets_mm: tuple[float, float] = (-7.0, 7.0)
    spine_mount_path_diameter_mm: float = 3.2
    obsolete_tower_radius_mm: float = 119.5
    obsolete_tower_tangent_offsets_mm: tuple[float, float] = (-4.5, 4.5)

    miter_ratio: float = 1.0
    miter_axis_offset_mm: float = 5.11
    tooth_tip_radius_mm: float = 129.0
    carrier_race_radius_mm: float = 131.6
    tooth_root_radius_mm: float = 132.5
    ring_body_outer_radius_mm: float = 138.9
    fin_outer_radius_mm: float = 143.7
    stationary_outer_radius_mm: float = 150.0

    hall_magnet_count: int = 3
    hall_magnet_radius_mm: float = 136.0
    hall_magnet_pocket_diameter_mm: float = 4.1
    hall_magnet_pocket_depth_mm: float = 2.1
    hall_module_angle_deg: float = 90.0
    hall_module_envelope_mm: tuple[float, float, float] = (12.0, 8.0, 4.0)
    hall_wire_bend_zone_mm: float = 3.0
    hall_connector_service_shell_mm: float = 1.0
    hall_mechanical_clearance_mm: float = 0.5

    # Purchased-part interface variables; these do not create base cutouts.
    motor_body_width_mm: float = 20.3
    motor_body_height_mm: float = 20.3
    motor_body_length_mm: float = 39.3
    motor_shaft_diameter_mm: float = 3.99
    motor_shaft_protrusion_mm: float = 7.0
    motor_face_mount_pitch_mm: float = 15.4
    motor_face_hole_diameter_mm: float = 2.2
    motor_face_radial_datum_mm: float = 111.75
    electronics_envelope_mm: tuple[float, float, float] = (50.0, 40.0, 15.0)
    electronics_mount_pitch_mm: tuple[float, float] = (42.0, 32.0)
    electronics_hole_d_mm: float = 3.4
    cable_channel_d_mm: float = 6.0
    cable_min_bend_r_mm: float = 10.0

    # Validation/export controls.
    boolean_overshoot_mm: float = 0.5
    brep_intersection_tolerance_mm3: float = 1.0e-7
    cad_linear_tolerance_mm: float = 0.02
    assembly_start_z_mm: float = 8.0
    assembly_path_step_mm: float = 0.5
    u1_bed_xy_mm: float = 270.0
    u1_edge_keepout_mm: float = 5.0
    quadrant_brim_mm: float = 5.0
    exploded_quadrant_radial_mm: float = 28.0
    exploded_hardware_z_mm: float = 18.0
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15

    @property
    def base_thickness_mm(self) -> float:
        return self.plate_nominal_thickness_mm

    @property
    def seam_gap_nominal_mm(self) -> float:
        return 2.0 * self.seam_relief_per_face_mm

    @property
    def lap_gross_area_mm2(self) -> float:
        return (self.lap_r_max_mm - self.lap_r_min_mm) * (
            self.donor_t_max_mm - self.donor_t_min_mm
        )

    @property
    def screw_count_total(self) -> int:
        return len(self.seam_angles_deg) * self.screws_per_seam

    @property
    def motor_slot_count_total(self) -> int:
        return (
            len(self.motor_station_angles_deg)
            * len(self.motor_slot_axis_radii_mm)
            * len(self.motor_slot_tangent_offsets_mm)
        )

    @property
    def u1_usable_xy_mm(self) -> float:
        return self.u1_bed_xy_mm - 2.0 * self.u1_edge_keepout_mm


SPEC = FunctionalCenteredStepLapSpec()
