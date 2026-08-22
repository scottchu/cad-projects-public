"""Frozen numeric contract for the P3 V3 R2 progressive print coupons.

Units are millimetres and degrees.  XY is the clock plane, +Z faces the
viewer, and both coupons use the parent mechanism's angle-zero (+X) station.
The coupons are intentionally separate from ``p3_v3_full_ring_r2``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sin, radians


@dataclass(frozen=True)
class P3V3R2PrintCouponSpec:
    # Frozen parent transmission.
    module: float = 1.0
    pressure_angle_degrees: float = 20.0
    ring_teeth: int = 260
    ring_pitch_radius: float = 130.0
    pinion_teeth: int = 16
    pinion_pitch_radius: float = 8.0
    output_axis_radius: float = 122.0
    ring_tooth_outer_radius: float = 132.5
    ring_root_radius: float = 132.5
    ring_body_outer_radius: float = 138.0
    ring_outer_radius: float = 140.0
    ring_thickness: float = 3.0
    tooth_phase_offset_degrees: float = 360.0 / (2.0 * 260.0)

    # Coupon A: seam/race and guide-clearance ladder.
    seam_arc_teeth_each: int = 12
    seam_overlap_tangential: float = 14.0
    seam_lap_inner_radius: float = 132.0
    seam_lap_outer_radius: float = 138.0
    seam_lap_layer: float = 1.5
    race_inner_radius: float = 138.0
    race_outer_radius: float = 140.0
    race_axial: float = 0.8
    seam_clamp_radius: float = 135.0
    seam_clamp_bore_diameter: float = 2.40
    seam_countersink_diameter: float = 4.20
    seam_countersink_depth: float = 1.20
    seam_nut_af: float = 4.15
    seam_nut_depth: float = 1.80
    alignment_pin_diameter: float = 2.0
    alignment_pin_length: float = 3.0
    alignment_bore_diameter: float = 2.10
    alignment_pin_tangential_offsets: tuple[float, float] = (-4.5, 4.5)
    guide_clearances: tuple[float, float, float] = (0.15, 0.25, 0.35)
    guide_shoe_radial_width: float = 4.0
    guide_shoe_tangential_length: float = 12.0
    guide_shoe_floor: float = 1.2

    # Separate stationary joiner coupon.
    joiner_step_size: tuple[float, float, float] = (6.0, 4.0, 1.2)
    joiner_clearance: float = 0.25
    joiner_body_size: tuple[float, float, float] = (18.0, 12.0, 3.0)
    joiner_m3_clearance: float = 3.40
    joiner_m3_nut_af: float = 5.50
    joiner_m3_nut_depth: float = 2.40

    # Coupon B: complete 24-tooth station arc and serviceable bearing stack.
    motor_arc_teeth: int = 24
    motor_arc_center_angle: float = 0.0
    motor_carrier_z0: float = 2.8
    motor_race_z0: float = 2.0
    pinion_face_range: tuple[float, float] = (3.6, 5.7)
    motor_face_radius: float = 111.75
    motor_face_size: float = 20.3
    motor_body_length: float = 39.3
    motor_shaft_diameter: float = 4.0
    motor_shaft_length: float = 7.0
    output_shaft_diameter: float = 4.0
    output_shaft_length: float = 40.0
    output_shaft_z: tuple[float, float] = (-25.0, 15.0)
    miter_teeth: int = 16
    miter_ratio: float = 1.0
    bearing_code: str = "MR84"
    bearing_id: float = 4.0
    bearing_od: float = 8.0
    bearing_width: float = 3.0
    bearing_center_span: float = 18.0
    bearing_pocket_diameter: float = 8.10
    bearing_pocket_depth: float = 3.10
    bearing_fixed_shoulder: float = 1.20
    bearing_cap_thickness: float = 1.60
    bearing_aperture_diameter: float = 6.40
    bearing_insert_boss_od: float = 6.0
    bearing_insert_bore: float = 3.20
    bearing_insert_depth: float = 3.0
    bearing_cap_screw_clearance: float = 2.40
    bearing_cap_fastener_spacing: float = 21.0
    fit_gauge_diameters: tuple[float, float] = (8.00, 8.20)
    fit_gauge_wall: float = 2.0
    fit_gauge_height: float = 3.10

    # Horizontal NEMA8 saddle and clamps.
    motor_adjustment: float = 0.50
    motor_slot_total_travel: float = 1.0
    motor_saddle_thickness: float = 3.0
    motor_saddle_x: tuple[float, float] = (72.0, 115.0)
    motor_saddle_half_width: float = 18.0
    motor_clamp_clearance: float = 3.40
    motor_clamp_nut_af: float = 5.50
    motor_clamp_nut_depth: float = 2.40
    motor_clamp_x: tuple[float, float] = (80.0, 103.0)
    motor_clamp_y: tuple[float, float] = (-14.5, 14.5)
    motor_clamp_strap_radial: float = 6.0
    motor_clamp_strap_tangential: float = 36.0
    motor_clamp_strap_thickness: float = 3.0
    motor_clamp_strap_z0: float = -1.85

    # Guide and optical-fin validation parts.
    guide_arm_min_thickness: float = 1.20
    operating_guide_clearance: float = 0.25
    fin_foot_radial: float = 6.0
    fin_foot_tangential: float = 14.0
    fin_foot_thickness: float = 2.0
    fin_foot_corner_radius: float = 1.0
    fin_hole_diameter: float = 2.40
    fin_hole_spacing: float = 8.0
    fin_insert_boss_od: float = 6.0
    fin_insert_bore: float = 3.20
    fin_insert_depth: float = 3.20
    fin_mount_radius: float = 135.0
    fin_blade_height: float = 15.0
    fin_blade_radial: float = 1.20
    fin_blade_tangential: float = 2.0

    @property
    def tooth_pitch_degrees(self) -> float:
        return 360.0 / self.ring_teeth

    @property
    def gear_ratio(self) -> float:
        return self.ring_teeth / self.pinion_teeth

    @property
    def center_distance(self) -> float:
        return self.ring_pitch_radius - self.pinion_pitch_radius

    @property
    def seam_half_angle_degrees(self) -> float:
        return self.seam_arc_teeth_each * self.tooth_pitch_degrees

    @property
    def motor_arc_angle_degrees(self) -> float:
        return self.motor_arc_teeth * self.tooth_pitch_degrees

    def motor_arc_chord(self, radius: float | None = None) -> float:
        r = self.ring_outer_radius if radius is None else radius
        return 2.0 * r * sin(radians(self.motor_arc_angle_degrees / 2.0))

    @property
    def seam_overlap_half(self) -> float:
        return self.seam_overlap_tangential / 2.0

    @property
    def bearing_ranges(self) -> tuple[tuple[float, float], tuple[float, float]]:
        return ((-21.0, -18.0), (-3.0, 0.0))

    @property
    def bearing_centers(self) -> tuple[float, float]:
        return tuple((a + b) / 2.0 for a, b in self.bearing_ranges)

    @property
    def ring_pitch_circumference(self) -> float:
        return 2.0 * pi * self.ring_pitch_radius


P3_V3_R2_PRINT_COUPON = P3V3R2PrintCouponSpec()
