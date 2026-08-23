"""Frozen dimensional contract for the KAGE P3 V0 motor outer ring.

XY is the clock plane, +Z faces the viewer, and -Z faces the wall.  This
module is intentionally isolated from the prior quartz and magnetic designs.
Purchased motor and Hall-module fits remain reference envelopes until the
actual components are measured.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sin, radians


@dataclass(frozen=True)
class P3V0MotorOuterRingSpec:
    bed_size: float = 256.0
    brim: float = 5.0
    center_clear_radius: float = 130.0

    carrier_radius: float = 135.0
    flange_radii: tuple[float, float] = (130.0, 140.0)
    flange_z: tuple[float, float] = (2.7, 5.7)
    spine_radii: tuple[float, float] = (132.0, 138.0)
    spine_z: tuple[float, float] = (5.7, 7.7)
    segment_extents: tuple[tuple[float, float], ...] = (
        (-60.0, 60.0),
        (60.0, 180.0),
        (180.0, 300.0),
    )
    seam_angles: tuple[float, float, float] = (60.0, 180.0, 300.0)

    fin_angle: float = 270.0
    fin_radial: float = 6.0
    fin_tangential: float = 1.2
    fin_height: float = 50.0

    key_tangential_length: float = 18.0
    key_end_radial: float = 5.0
    key_neck_radial: float = 3.0
    key_end_tangential: float = 5.0
    key_thickness: float = 1.0
    key_pocket_depth: float = 1.2
    key_xy_clearance_per_side: float = 0.15
    key_axial_clearance: float = 0.10
    key_installed_z: tuple[float, float] = (6.6, 7.6)

    hall_magnet_angle: float = 90.0
    hall_magnet_diameter: float = 3.0
    hall_magnet_thickness: float = 2.0
    hall_pocket_diameter: float = 3.15
    hall_pocket_depth: float = 2.15
    hall_rear_recess: float = 0.15

    frame_radii: tuple[float, float] = (141.0, 150.0)
    frame_z: tuple[float, float] = (0.0, 2.4)
    frame_quadrant_extents: tuple[tuple[float, float], ...] = (
        (-45.0, 45.0),
        (45.0, 135.0),
        (135.0, 225.0),
        (225.0, 315.0),
    )
    frame_seam_angles: tuple[float, float, float, float] = (45.0, 135.0, 225.0, 315.0)
    splice_arc_length: float = 24.0
    splice_radii: tuple[float, float] = (141.0, 150.0)
    splice_z: tuple[float, float] = (-2.0, 0.0)
    splice_hole_diameter: float = 3.4
    splice_hole_tangential_offsets: tuple[float, float] = (-7.0, 7.0)

    guide_angles: tuple[float, float, float, float] = (0.0, 90.0, 210.0, 330.0)
    guide_arc_length: float = 18.0
    guide_floor_radii: tuple[float, float] = (130.0, 141.2)
    guide_floor_z: tuple[float, float] = (0.0, 2.4)
    guide_outer_wall_radii: tuple[float, float] = (140.3, 141.2)
    guide_outer_wall_z: tuple[float, float] = (2.3, 7.2)
    guide_lip_radii: tuple[float, float] = (138.8, 141.2)
    guide_lip_top_z: float = 7.2
    guide_lip_outer_underside_z: float = 6.0

    motor_angle: float = 270.0
    motor_axis_radius_nominal: float = 146.0
    motor_axis_radius_start: float = 145.8
    motor_axis_radius_range: tuple[float, float] = (144.0, 148.0)
    motor_axis_radius_tuned_range: tuple[float, float] = (145.75, 145.85)
    motor_face_z: float = -4.5
    motor_keepout_xy: float = 20.6
    motor_keepout_length: float = 40.0
    motor_mount_pitch: float = 15.4
    motor_mount_clearance_diameter: float = 2.3
    motor_pilot_relief_diameter: float = 16.3
    motor_pilot_relief_depth: float = 1.6
    motor_shaft_diameter: float = 4.0
    motor_shaft_clearance_diameter: float = 4.2
    motor_shaft_length: float = 10.0
    motor_shaft_keepout_length: float = 11.0
    motor_slide_range: float = 4.0
    motor_slot_length: float = 5.0
    motor_slot_spacing_tangential: float = 18.0
    motor_frame_slot_length: float = 7.4
    motor_ear_radial: float = 12.0
    motor_ear_tangential: float = 7.0
    motor_ear_z: tuple[float, float] = (-4.7, 0.0)

    drive_hub_diameter: float = 10.0
    drive_tire_diameter: float = 12.0
    drive_contact_width: float = 2.6
    drive_z: tuple[float, float] = (2.9, 5.5)
    drive_shaft_bore_diameter: float = 4.10
    drive_pinch_hole_diameter: float = 2.2

    idler_angles: tuple[float, float] = (30.0, 150.0)
    idler_hub_diameter: float = 6.0
    idler_tire_diameter: float = 8.0
    idler_bore_diameter: float = 3.2
    idler_axis_radius_nominal: float = 144.0
    idler_axis_radius_range: tuple[float, float] = (143.5, 145.0)
    idler_axis_radius_tuned_range: tuple[float, float] = (143.75, 143.85)
    idler_axis_radius_start: float = 143.8
    idler_slot_length: float = 4.7
    idler_contact_width: float = 2.6
    idler_z: tuple[float, float] = (2.9, 5.5)

    hall_angle: float = 90.0
    hall_module_envelope: tuple[float, float, float] = (10.0, 15.0, 5.0)
    hall_face_gap_range: tuple[float, float] = (1.0, 8.0)
    hall_face_gap_nominal: float = 3.0
    hall_tangential_adjustment: float = 5.0
    hall_radial_adjustment: float = 2.0
    hall_mount_slot_diameter: float = 2.3
    hall_seat: tuple[float, float] = (16.0, 11.0)
    hall_seat_center_radius: float = 135.0
    hall_fastener_radius: float = 145.0
    hall_fastener_tangential_offsets: tuple[float, float] = (-13.0, 13.0)
    hall_seat_radii: tuple[float, float] = (130.0, 141.0)
    hall_seat_tangential: float = 17.0
    hall_bracket_z: tuple[float, float] = (-12.15, -10.15)
    hall_crossbar_radii: tuple[float, float] = (140.0, 149.5)
    hall_crossbar_tangential: float = 31.0
    hall_tower_radii: tuple[float, float] = (141.0, 149.5)
    hall_tower_tangential: float = 5.0
    hall_tower_z: tuple[float, float] = (-10.25, 0.0)
    hall_spacer_nominal_thickness: float = 5.0
    hall_spacer_range: tuple[float, float] = (0.0, 7.0)

    motor_full_step_degrees: float = 1.8
    microsteps: int = 16
    rated_holding_torque_nm: float = 0.04

    @property
    def carrier_od(self) -> float:
        return 2.0 * self.flange_radii[1]

    @property
    def carrier_segment_tangential_bbox(self) -> float:
        return 2.0 * self.flange_radii[1] * sin(radians(60.0))

    @property
    def carrier_segment_with_brim(self) -> float:
        return self.carrier_segment_tangential_bbox + 2.0 * self.brim

    @property
    def hall_front_wall(self) -> float:
        # The frozen 3.00 mm flange and 2.15 mm pocket imply 0.85 mm.
        return (self.flange_z[1] - self.flange_z[0]) - self.hall_pocket_depth

    @property
    def drive_ratio(self) -> float:
        return self.carrier_od / self.drive_tire_diameter

    @property
    def ring_full_step_degrees(self) -> float:
        return self.motor_full_step_degrees / self.drive_ratio

    @property
    def ring_microstep_degrees(self) -> float:
        return self.ring_full_step_degrees / self.microsteps

    @property
    def ring_microstep_arc_mm(self) -> float:
        return 2.0 * pi * self.carrier_radius * self.ring_microstep_degrees / 360.0

    @property
    def motor_rpm_at_seconds_speed(self) -> float:
        return self.drive_ratio

    @property
    def microsteps_per_second_at_seconds_speed(self) -> float:
        steps_per_motor_rev = 360.0 / self.motor_full_step_degrees * self.microsteps
        return steps_per_motor_rev * self.motor_rpm_at_seconds_speed / 60.0

    @property
    def nominal_compression(self) -> float:
        return self.flange_radii[1] + self.drive_tire_diameter / 2.0 - self.motor_axis_radius_start

    @property
    def nominal_idler_compression(self) -> float:
        return self.flange_radii[1] + self.idler_tire_diameter / 2.0 - self.idler_axis_radius_start


P3_V0 = P3V0MotorOuterRingSpec()


PRIOR_ISOLATION_SHA256 = {
    "p2r2_magnetic_three_channel_300mm_spec.py": "49c85b9c37f6b32eef6beff16daa23a6257a642f7559087ff28362e1033a2a5d",
    "p2r2_magnetic_three_channel_300mm_geometry.py": "2c6d2d16c24d3793eb27a13735162a1ddcd3c3f82c4fc4647e8d438c80281a35",
    "p2r2_magnetic_three_channel_300mm_export.py": "cd16346f3285b6aa764b8d8e4b13d1b3d68d3babb997c4ae32bfc479b606bec0",
    "p2r3_module_b_rail_coupon_spec.py": "55f61265b9fbfb8d1881daf974e16901f6d84928917902fde1e7dd0564e211b9",
    "p2r3_module_b_rail_coupon_geometry.py": "1a79eb5d534282d1a08edf342ee87a9810a976e1eeb4deacf34204f105551934",
    "p2r3_module_b_rail_coupon_export.py": "65dc63982f890c1050e532d54d7ac85cf6a1b5336b94ded05967c3a4af7b69ca",
    "models/p2r3_module_b_rail_coupon/print/p2r3_module_b_r135_three_part_coupon.3mf": "ca8df27c027c43f42d22000da2c631ed7dbd5ca28f2fee38101f57eb58a73bcd",
}


def validate_spec(p: P3V0MotorOuterRingSpec = P3_V0) -> None:
    assert p.center_clear_radius == p.flange_radii[0] == 130.0
    assert p.carrier_od == 280.0
    assert p.carrier_segment_tangential_bbox < 242.49
    assert p.carrier_segment_with_brim <= p.bed_size
    assert abs(p.hall_front_wall - 0.85) < 1e-9
    # Outer-sided guide: flange outer edge r140 has 0.30 mm radial clearance
    # to the wall at r140.30; the inward lip reaches r138.80 for 1.20 mm
    # positive capture while leaving the spine outer edge r138 0.80 mm clear.
    assert abs(p.guide_outer_wall_radii[0] - p.flange_radii[1] - 0.30) < 1e-9
    assert abs(p.flange_radii[1] - 138.80 - 1.20) < 1e-9
    assert abs(138.80 - p.spine_radii[1] - 0.80) < 1e-9
    assert p.drive_ratio == 280.0 / 12.0
    assert abs(p.ring_full_step_degrees - 0.07714285714285715) < 1e-12
    assert abs(p.ring_microstep_degrees - 0.004821428571428572) < 1e-12
    assert abs(p.ring_microstep_arc_mm - 0.01136022343485595) < 1e-12
    assert abs(p.motor_rpm_at_seconds_speed - 23.333333333333332) < 1e-12
    assert abs(p.microsteps_per_second_at_seconds_speed - 1244.4444444444443) < 1e-9
    assert abs(p.nominal_compression - 0.20) < 1e-9
    assert abs(p.nominal_idler_compression - 0.20) < 1e-9


validate_spec()
