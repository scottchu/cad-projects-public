"""Frozen numeric contract for the B1-R1 raised captive-nut rail MVP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_mount_b1_r1_raised_nut_rails"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class RaisedNutRailSpec:
    # Immutable R4 datum copied by reference, not by editing the R4 source.
    plate_bottom_z_mm: float = -31.5
    plate_top_z_mm: float = -25.5
    lap_split_z_mm: float = -28.5
    base_outer_radius_mm: float = 150.0
    base_inner_radius_mm: float = 66.0

    # Raised blind nut receiver section.
    receiver_channel_bottom_z_mm: float = -27.5
    receiver_channel_top_z_mm: float = -24.5
    receiver_channel_height_mm: float = 3.0
    receiver_roof_top_z_mm: float = -22.3
    receiver_roof_thickness_mm: float = 2.2
    receiver_web_above_split_mm: float = 1.0
    receiver_solid_below_channel_mm: float = 4.0
    receiver_tip_relief_depth_mm: float = 0.25
    receiver_solid_below_tip_mm: float = 3.75

    # Common top-down M3 stack.
    mounting_foot_thickness_mm: float = 3.0
    m3_screw_diameter_mm: float = 3.0
    m3_clearance_diameter_mm: float = 3.4
    m3_screw_length_mm: float = 8.0
    m3_socket_head_diameter_mm: float = 5.5
    m3_socket_head_height_mm: float = 3.0
    m3_nut_max_af_mm: float = 5.5
    m3_nut_max_thickness_mm: float = 2.4
    nut_channel_width_mm: float = 5.8
    nut_insertion_approach_length_mm: float = 7.0
    nut_channel_vertical_clearance_mm: float = 0.6
    screw_tip_after_nut_mm: float = 0.4
    screw_tip_channel_clearance_mm: float = 0.2
    driver_path_diameter_mm: float = 6.5
    driver_path_height_mm: float = 45.0

    # Motor receiver rails and reusable sled.
    motor_station_angles_deg: tuple[float, ...] = (0.0, 120.0, 240.0)
    motor_axis_radii_mm: tuple[float, ...] = (88.0, 109.0)
    rejected_old_motor_axis_radius_mm: float = 126.0
    motor_tangent_offsets_mm: tuple[float, ...] = (-12.0, 12.0)
    motor_service_travel_mm: float = 2.5
    motor_top_slot_width_mm: float = 3.6
    motor_top_slot_overall_length_mm: float = 8.6
    motor_channel_working_length_mm: float = 12.1
    motor_rail_external_length_mm: float = 14.1
    motor_rail_external_width_mm: float = 9.8
    receiver_sidewall_mm: float = 2.0
    # Rigid AF5.5 nuts must pass without a snap-fit deformation assumption.
    receiver_nib_intrusion_per_side_mm: float = 0.0
    receiver_nib_radial_length_mm: float = 0.8
    receiver_nib_throat_mm: float = 5.8
    ring_tooth_tip_radius_mm: float = 129.0
    motor_output_witness_radius_mm: float = 122.0
    motor_output_overhang_from_outer_axis_mm: float = 13.0

    sled_radial_min_mm: float = 81.5
    sled_radial_max_mm: float = 115.5
    sled_tangent_half_width_mm: float = 17.0
    sled_guide_clearance_per_side_mm: float = 0.20
    sled_guide_shoulder_thickness_mm: float = 1.2
    sled_guide_shoulder_depth_mm: float = 1.0
    # D8 stays inside the R129 witness even at q=+2.5 mm.
    sled_load_boss_diameter_mm: float = 8.0
    sled_load_boss_height_mm: float = 8.0
    sled_rib_radial_min_mm: float = 110.0
    sled_rib_radial_max_mm: float = 127.0
    sled_rib_tangential_mm: float = 8.0
    sled_rib_height_mm: float = 3.0
    physical_clamp_test_load_n: float = 10.0

    # Reusable fixed riser and installed spine riser.
    fixed_angles_deg: tuple[float, ...] = (60.0, 180.0)
    fixed_center_radius_mm: float = 118.0
    fixed_axis_tangent_offsets_mm: tuple[float, ...] = (-7.0, 7.0)
    fixed_rail_radial_width_mm: float = 9.8
    fixed_channel_tangential_length_mm: float = 20.4
    fixed_rail_tangential_length_mm: float = 22.4
    fixed_foot_radial_width_mm: float = 12.0
    fixed_foot_tangential_length_mm: float = 22.4
    fixed_stem_radial_width_mm: float = 8.0
    fixed_stem_tangential_width_mm: float = 16.0

    spine_angle_deg: float = 300.0
    spine_center_radius_mm: float = 100.0
    spine_axis_tangent_offsets_mm: tuple[float, ...] = (-7.0, 7.0)
    spine_foot_radial_width_mm: float = 20.0
    spine_foot_tangential_length_mm: float = 24.0
    spine_stem_radial_width_mm: float = 8.0
    spine_stem_tangential_width_mm: float = 20.0
    mechanism_interface_z_mm: float = -5.2
    receiver_to_mechanism_interface_rise_mm: float = 17.1

    # Export and numerical validation controls.
    brep_tolerance_mm3: float = 1.0e-6
    minimum_lap_contact_area_mm2: float = 1095.0
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15
    u1_bed_xy_mm: float = 270.0
    u1_edge_keepout_mm: float = 5.0
    print_brim_mm: float = 5.0
    exploded_radial_mm: float = 30.0
    exploded_component_z_mm: float = 28.0

    @property
    def rail_height_above_plate_mm(self) -> float:
        return self.receiver_roof_top_z_mm - self.plate_top_z_mm

    @property
    def screw_under_head_z_mm(self) -> float:
        return self.receiver_roof_top_z_mm + self.mounting_foot_thickness_mm

    @property
    def screw_tip_z_mm(self) -> float:
        return self.screw_under_head_z_mm - self.m3_screw_length_mm

    @property
    def u1_usable_xy_mm(self) -> float:
        return self.u1_bed_xy_mm - 2.0 * self.u1_edge_keepout_mm


SPEC = RaisedNutRailSpec()
