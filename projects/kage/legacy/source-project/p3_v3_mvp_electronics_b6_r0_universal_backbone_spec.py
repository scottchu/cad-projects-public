"""Frozen numeric contract for the B6-R0 universal electronics backbone MVP.

Only the R4 chassis datums and the NEMA 8 mechanical reference are confirmed.
All electronics envelopes remain replaceable variables until a purchased board
and its exact STEP are selected.  Units are millimetres/degrees.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_electronics_b6_r0_universal_backbone"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class UniversalElectronicsBackboneSpec:
    # Confirmed inherited R4 datum; never edit the R4 source from B6.
    r4_outer_diameter_mm: float = 300.0
    r4_plate_thickness_mm: float = 6.0
    r4_plate_top_z_mm: float = -25.5
    r4_plate_underside_z_mm: float = -31.5
    r4_seam_angles_deg: tuple[float, ...] = (45.0, 135.0, 225.0, 315.0)
    r4_seam_axis_radii_mm: tuple[float, ...] = (82.0, 104.0)
    motor_station_angles_deg: tuple[float, ...] = (0.0, 120.0, 240.0)
    lowest_ring_bottom_z_mm: float = -2.2

    # Confirmed motor and optical references; no purchased motor is selected.
    nema8_env_xyz: tuple[float, float, float] = (20.3, 20.3, 39.3)
    nema8_shaft_diameter_mm: float = 4.0
    nema8_shaft_protrusion_mm: float = 7.0
    led_mcpcb_diameter_mm: float = 20.0
    led_heatsink_reference_diameter_mm: float = 40.0

    # Replaceable provisional board envelopes. Keep these names stable.
    esp_env_xyz: tuple[float, float, float] = (50.0, 40.0, 15.0)
    tmc_env_xyz: tuple[float, float, float] = (22.0, 18.0, 15.0)
    pd_trigger_env_xyz: tuple[float, float, float] = (30.0, 20.0, 10.0)
    logic_buck_env_xyz: tuple[float, float, float] = (45.0, 25.0, 15.0)
    led_cc_driver_env_xyz: tuple[float, float, float] = (45.0, 25.0, 15.0)
    installed_height_max: float = 15.0
    envelope_clearance_mm: float = 1.0
    board_gap_min_mm: float = 5.0

    # One-piece PETG printed backbone plan.
    inner_web_radii_mm: tuple[float, float] = (68.0, 80.0)
    control_lobe_angle_deg: float = 60.0
    control_lobe_radii_mm: tuple[float, float] = (68.0, 108.0)
    control_lobe_tangent_mm: tuple[float, float] = (-25.0, 25.0)
    power_lobe_angle_deg: float = 180.0
    power_lobe_radii_mm: tuple[float, float] = (68.0, 96.0)
    power_lobe_tangent_mm: tuple[float, float] = (-47.5, 47.5)
    motion_lobe_angle_deg: float = 300.0
    motion_lobe_radii_mm: tuple[float, float] = (68.0, 89.5)
    motion_lobe_tangent_mm: tuple[float, float] = (-32.0, 32.0)
    pd_input_lobe_angle_deg: float = 270.0
    pd_input_lobe_radii_mm: tuple[float, float] = (68.0, 90.0)
    pd_input_lobe_tangent_mm: tuple[float, float] = (-15.0, 15.0)
    cable_arm_angle_deg: float = 270.0
    cable_arm_radii_mm: tuple[float, float] = (90.0, 143.0)
    cable_arm_tangent_mm: tuple[float, float] = (-7.0, 7.0)

    web_thickness_mm: float = 1.5
    pad_thickness_mm: float = 4.0
    landing_pip_height_mm: float = 0.5
    landing_pip_diameter_mm: float = 3.0
    mount_arm_tangent_width_mm: float = 8.0
    mount_pad_diameter_mm: float = 10.0
    printed_underside_z_mm: float = -25.0
    print_brim_mm: float = 5.0
    print_footprint_limit_xy_mm: float = 260.0

    # Shared R4 seam fastener replacement stack.
    m3_clearance_diameter_mm: float = 3.4
    seam_screw_length_mm: float = 8.0
    seam_screw_diameter_mm: float = 3.0
    seam_screw_head_diameter_mm: float = 5.5
    seam_screw_head_height_mm: float = 3.0
    seam_washer_thickness_mm: float = 0.5
    seam_washer_od_mm: float = 7.0
    seam_counterbore_diameter_mm: float = 7.4
    seam_counterbore_floor_z_mm: float = -23.5
    seam_screw_under_head_z_mm: float = -23.0
    existing_r4_nut_top_z_mm: float = -28.6
    existing_r4_nut_bottom_z_mm: float = -31.0
    m3_engagement_min_mm: float = 2.4
    screw_tip_above_underside_min_mm: float = 0.3

    # Universal, intentionally non-board-specific mounting interfaces.
    board_slot_width_mm: float = 3.4
    board_slot_overall_length_mm: float = 12.0
    board_slot_pad_radial_mm: float = 16.0
    board_slot_pad_tangent_mm: float = 8.0
    side_load_nut_channel_af_mm: float = 5.8
    side_load_nut_channel_depth_mm: float = 2.6
    ordinary_m3_nut_af_mm: float = 5.5
    ordinary_m3_nut_thickness_mm: float = 2.4
    nut_channel_bottom_floor_mm: float = 0.4

    # Open wiring, service, RF, and thermal reservations.
    open_channel_width_mm: float = 6.0
    open_channel_height_mm: float = 3.0
    open_channel_rail_width_mm: float = 1.5
    trunk_separation_min_mm: float = 6.0
    general_bend_radius_min_mm: float = 10.0
    led_bend_radius_min_mm: float = 15.0
    led_service_loop_mm: float = 80.0
    motor_branch_loop_mm: float = 25.0
    esp_antenna_keepout_mm: float = 10.0
    led_driver_to_heatsink_min_mm: float = 30.0
    ring_clearance_min_mm: float = 3.0

    # Representative collision/validation controls.
    motor_sled_q_samples_mm: tuple[float, ...] = (-2.5, -0.35, 0.0, 0.1, 2.5)
    axis_tolerance_mm: float = 0.05
    brep_tolerance_mm3: float = 1.0e-6
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15

    @property
    def printed_top_z_mm(self) -> float:
        return self.printed_underside_z_mm + self.web_thickness_mm

    @property
    def pad_top_z_mm(self) -> float:
        return self.printed_underside_z_mm + self.pad_thickness_mm

    @property
    def seam_screw_tip_z_mm(self) -> float:
        return self.seam_screw_under_head_z_mm - self.seam_screw_length_mm

    @property
    def seam_engagement_mm(self) -> float:
        return self.existing_r4_nut_top_z_mm - self.seam_screw_tip_z_mm

    @property
    def seam_tip_above_underside_mm(self) -> float:
        return self.seam_screw_tip_z_mm - self.r4_plate_underside_z_mm


SPEC = UniversalElectronicsBackboneSpec()
