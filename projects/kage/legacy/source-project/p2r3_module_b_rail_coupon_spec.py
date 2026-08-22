"""Frozen dimensions for the isolated P2R3 r135 inset-rail coupon.

XY is the clock plane, +Z faces the viewer.  The second-channel rear rail
datum is Z=0.  This module intentionally has no dependency on P2R2 geometry.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import degrees, radians, tan


@dataclass(frozen=True)
class P2R3ModuleBRailCouponSpec:
    radius: float = 135.0
    rail_angle_start_deg: float = -55.0
    rail_angle_end_deg: float = 55.0
    stationary_inner_radius: float = 125.0
    stationary_outer_radius: float = 145.0
    ear_inner_radius: float = 121.5
    ear_outer_radius: float = 148.5
    ear_half_angle_deg: float = 8.0

    rail_rear_z: float = 0.0
    rear_web_top_z: float = 1.2
    constant_cavity_top_z: float = 5.1
    throat_z: float = 7.9
    cavity_radial_width: float = 9.6
    throat_radial_width: float = 4.8
    lip_taper_run_per_side: float = 2.4
    lip_taper_rise: float = 2.8

    follower_shoe_radial: float = 9.0
    follower_shoe_arc_length: float = 18.0
    follower_shoe_rear_z: float = 1.4
    follower_shoe_front_z: float = 4.9
    follower_neck_radial: float = 4.2
    follower_neck_rear_z: float = 4.6
    follower_neck_front_z: float = 8.2
    yaw_land_arc_length: float = 5.0
    yaw_land_center_offsets: tuple[float, float] = (-5.0, 5.0)
    bridge_radial: float = 9.0
    bridge_arc_length: float = 18.0
    bridge_rear_z: float = 8.0
    bridge_front_z: float = 9.0
    fin_height: float = 50.0
    fin_radial: float = 6.0
    fin_tangential: float = 1.2
    fin_root_z: float = 8.0

    magnet_diameter: float = 6.0
    magnet_thickness: float = 3.0
    magnet_pocket_diameter: float = 6.15
    magnet_pocket_depth: float = 3.10
    magnet_roof: float = 0.40
    membrane_thickness: float = 0.20
    follower_magnet_face_z: float = 1.50
    driver_magnet_face_z: float = -0.50
    physical_gap_shims: tuple[float, float, float] = (1.7, 2.0, 2.4)

    gate_nominal_angle_deg: float = 12.0
    gate_radial_inner: float = 128.2
    gate_radial_outer: float = 141.8
    gate_cut_inner: float = 128.0
    gate_cut_outer: float = 142.0
    gate_cut_edge_clearance: float = 0.20
    gate_tab_rear_z: float = 7.6
    gate_tab_front_z: float = 9.0
    main_ear_top_z: float = 7.4
    m2_clearance_diameter: float = 2.2
    m2_pilot_diameter: float = 1.6
    m2_pilot_depth: float = 4.0
    m2_radii: tuple[float, float] = (123.5, 146.5)

    nozzle_diameter: float = 0.4
    layer_height: float = 0.2
    wall_loops: int = 4
    bed_size: float = 256.0
    brim: float = 5.0
    gate_side_print_rotation_z_deg: float = 5.9151173637
    gate_side_print_rotation_x_deg: float = 90.0
    maximum_gate_bridge_span: float = 6.0

    @property
    def rail_angle_span_deg(self) -> float:
        return self.rail_angle_end_deg - self.rail_angle_start_deg

    @property
    def gate_arc_length(self) -> float:
        return radians(self.gate_nominal_angle_deg) * self.radius

    @property
    def gate_edge_clearance_deg(self) -> float:
        return degrees(self.gate_cut_edge_clearance / self.radius)

    @property
    def gate_part_angle_span_deg(self) -> float:
        return self.gate_nominal_angle_deg - 2.0 * self.gate_edge_clearance_deg

    @property
    def gate_side_print_max_radial_step(self) -> float:
        """Worst radial drift per 0.2 mm layer in the side-print orientation."""
        return self.layer_height * tan(radians(self.gate_part_angle_span_deg))

    @property
    def follower_arc_angle_deg(self) -> float:
        return degrees(self.follower_shoe_arc_length / self.radius)

    @property
    def usable_follower_travel_deg(self) -> float:
        return self.rail_angle_span_deg - self.follower_arc_angle_deg

    @property
    def capture_overlap_per_side(self) -> float:
        return (self.follower_shoe_radial - self.throat_radial_width) / 2.0

    @property
    def cavity_clearance_per_side(self) -> float:
        return (self.cavity_radial_width - self.follower_shoe_radial) / 2.0

    @property
    def throat_clearance_per_side(self) -> float:
        return (self.throat_radial_width - self.follower_neck_radial) / 2.0

    @property
    def axial_rear_clearance(self) -> float:
        return self.follower_shoe_rear_z - self.rear_web_top_z

    @property
    def axial_front_clearance(self) -> float:
        return self.constant_cavity_top_z - self.follower_shoe_front_z

    @property
    def magnet_face_gap(self) -> float:
        return self.follower_magnet_face_z - self.driver_magnet_face_z

    @property
    def pocket_void_rear_z(self) -> float:
        return self.follower_shoe_rear_z + self.membrane_thickness

    @property
    def pocket_front_z(self) -> float:
        return self.follower_shoe_front_z - self.magnet_roof

    @property
    def pocket_void_depth_before_breakout(self) -> float:
        return self.pocket_front_z - self.pocket_void_rear_z

    @property
    def gate_tab_inner_span(self) -> tuple[float, float]:
        return (self.ear_inner_radius, self.gate_radial_inner + 1.8)

    @property
    def gate_tab_outer_span(self) -> tuple[float, float]:
        return (self.gate_radial_outer - 1.8, self.ear_outer_radius)

    def cavity_half_width_at_z(self, z: float) -> float:
        if z <= self.constant_cavity_top_z:
            return self.cavity_radial_width / 2.0
        if z >= self.throat_z:
            return self.throat_radial_width / 2.0
        return self.cavity_radial_width / 2.0 - (
            z - self.constant_cavity_top_z
        ) * (self.lip_taper_run_per_side / self.lip_taper_rise)


P2R3_MODULE_B = P2R3ModuleBRailCouponSpec()


P2R2_ISOLATION_SHA256 = {
    "p2r2_magnetic_three_channel_300mm_spec.py": "49c85b9c37f6b32eef6beff16daa23a6257a642f7559087ff28362e1033a2a5d",
    "p2r2_magnetic_three_channel_300mm_geometry.py": "2c6d2d16c24d3793eb27a13735162a1ddcd3c3f82c4fc4647e8d438c80281a35",
    "p2r2_magnetic_three_channel_300mm_export.py": "cd16346f3285b6aa764b8d8e4b13d1b3d68d3babb997c4ae32bfc479b606bec0",
    "tests/test_p2r2_magnetic_three_channel_300mm.py": "33bc46674be26ff3fec709689ebbb99265deb4d53fbe1cd38b7446dfa755750b",
    "models/p2r2_magnetic_three_channel_300mm/p2r2_assembled_t1p5.step": "f229fb976b0dfaafdd18f4ff39c6b0b81d7f5d5467a9c72cfd698af725caa772",
    "models/p2r2_magnetic_three_channel_300mm/print/p2r2_magnetic_three_channel_300mm_t1p5.3mf": "8d108f9f0b76661401bbb20d4b1ed223acfd83003797dadf5eb9a18f93233df8",
}


def validate_spec(spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B) -> None:
    assert spec.radius == 135.0
    assert spec.rail_angle_span_deg == 110.0
    assert spec.cavity_radial_width == 9.6
    assert spec.throat_radial_width == 4.8
    assert spec.capture_overlap_per_side == 2.1
    assert abs(spec.cavity_clearance_per_side - 0.3) < 1e-9
    assert abs(spec.throat_clearance_per_side - 0.3) < 1e-9
    assert abs(spec.axial_rear_clearance - 0.2) < 1e-9
    assert abs(spec.axial_front_clearance - 0.2) < 1e-9
    assert abs(spec.magnet_face_gap - 2.0) < 1e-9
    assert abs(spec.pocket_void_depth_before_breakout - 2.9) < 1e-9
    assert abs(spec.pocket_void_depth_before_breakout + spec.membrane_thickness - spec.magnet_pocket_depth) < 1e-9
    assert spec.usable_follower_travel_deg >= 98.0
    assert spec.gate_arc_length >= 28.27
    assert spec.gate_cut_outer - spec.gate_cut_inner >= 14.0
    assert abs(spec.cavity_half_width_at_z(5.1) - 4.8) < 1e-9
    assert abs(spec.cavity_half_width_at_z(7.9) - 2.4) < 1e-9
    assert abs(spec.gate_side_print_rotation_z_deg - spec.gate_part_angle_span_deg / 2.0) < 1e-9
    assert spec.gate_side_print_max_radial_step <= spec.layer_height
    assert spec.m2_clearance_diameter <= spec.maximum_gate_bridge_span


validate_spec()
