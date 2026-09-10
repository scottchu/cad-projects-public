"""Parametric millimetre contract for the three-part P1 dispenser."""

from dataclasses import dataclass
from math import pi, radians, tan
from pill_click.p0_mechanical_fit_v23_keyboard_durable_latch.spec import P0MechanicalFitV23Spec

Interval = tuple[float, float]


@dataclass(frozen=True)
class P1HollowMagneticDispenserSpec(P0MechanicalFitV23Spec):
    """V2.3 exterior with a one-piece hopper, integrated insets, and coaxial magnets."""
    nozzle_diameter: float = 0.40
    standard_shell_thickness: float = 1.20
    key_face_membrane_y: float = 0.80
    minimum_internal_radius: float = 1.20
    pressed_state: float = 3.40
    inward_state: float = 3.40
    released_state: float = 14.20
    # The named released pose is also the physical rail stop.  There is no
    # extra pull beyond the pose whose port is proven fully shuttered.
    maximum_pull_state: float = 14.20
    inner_body_local_y: Interval = (-20.80, 1.50)
    # Extend only the concealed rail front to the existing housing blind stop.
    # The earlier dispenser rail ended 4.35 mm before that stop, so the CAD
    # preview coordinate was not a physical limit.  At -3.85 the rail touches
    # the inherited blind wall exactly at `released_state`.
    male_rail_local_y: Interval = (-20.80, -3.85)
    spine_local_y: Interval = (-20.80, -12.80)
    # P1 uses one constant-size female rail groove.  The inherited V2.3
    # assembly flare made a second, larger rectangular inset at the rear
    # entrance even though the 0.20 mm rail clearance is already sufficient.
    female_mouth_extra_width_z: float = 0.0
    female_mouth_extra_depth_x: float = 0.0
    cavity_rear_y: float = -16.00
    cavity_seam_y: float = 1.50
    cavity_front_y: float = 19.70
    hopper_start_z: float = -3.00
    hopper_rear_throat_y: float = -9.50
    hopper_front_throat_y: float = 0.30
    hopper_throat_floor_z: float = -16.10
    hopper_blend_radius_xz: float = 1.20
    hopper_boolean_overlap_z: float = 0.10
    hopper_degenerate_section_height_z: float = 0.20
    # Maximum no-fin port that preserves the full 1.20 mm side walls while
    # allowing the normal inner body and housing floor to seal it at release.
    pill_port_width_x: float = 31.80
    # The moving inner opening is 9.30 mm long.  Its rear edge remains the
    # accepted production datum; the separate fixed housing aperture below is
    # shortened at only its forward edge to create the fail-closed seal.
    pill_port_length_y: float = 9.30
    pill_port_corner_radius_xy: float = 2.50
    inner_port_local_y: Interval = (-9.50, -0.20)
    # Fail-closed bias: retract only the forward edge of the fixed housing
    # aperture while its proven rear edge stays fixed.  The inner-container
    # aperture, travel, rails, and released stop remain accepted production
    # geometry.  This trades 2.50 mm of pressed overlap for a seal that
    # tolerates 3.00 mm of vertical sag without uncovering the aperture rear.
    outer_port_rearward_bias_y: float = 2.50
    inner_port_z: Interval = (-17.30, -14.30)
    outer_port_z: Interval = (-20.20, -16.90)
    reference_port_width_x: float = 22.00
    reference_port_length_y: float = 8.00
    released_seal_safety_inset: float = 0.40
    # A vertically held shuttle may fall this far below the mathematical rail
    # stop.  The port must remain fully shuttered throughout this envelope.
    released_vertical_sag_envelope_y: float = 3.00
    minimum_sagged_seal_separation_y: float = 1.00
    minimum_pressed_port_overlap_y: float = 6.80
    minimum_sagged_no_peek_margin_y: float = 0.17
    # Also cover a modest oblique look through the fixed opening.  This is a
    # source-level no-peek cone measured from the bottom-face normal in the
    # travel direction; rounded X edges can only improve the result.
    released_no_peek_half_angle_degrees: float = 8.00
    motion_sweep_sample_count: int = 55
    motion_sweep_max_step_y: float = 0.20
    # Tighten the accepted V2.3 locating pilot and tooth without introducing
    # a new stop or latch type.  The 2.00 mm flexure beams remain unchanged.
    rear_pilot_size_xz: float = 34.30
    rear_pilot_tip_size_xz: float = 33.50
    planar_latch_hook_apex_x: float = 18.90
    planar_latch_receiver_pocket_x: Interval = (18.00, 18.90)
    planar_latch_front_ramp_relief_x: Interval = (18.00, 18.90)
    magnet_nominal_diameter: float = 6.00
    magnet_nominal_depth_y: float = 2.00
    magnet_pocket_diameter: float = 6.10
    magnet_boolean_overshoot_y: float = 0.05
    # A same-face dental-pick bore overlaps the outside edge of every magnet
    # seat.  It reaches 0.50 mm beyond the seat floor so the pick can get
    # under the magnet, while remaining much too small to accept a magnet.
    magnet_pick_bore_diameter: float = 1.40
    magnet_pick_bore_overlap_x: float = 0.20
    magnet_pick_bore_extra_depth_y: float = 0.50
    return_magnet_centres_x: tuple[float, float] = (-8.50, 8.50)
    return_magnet_center_z: float = 0.00
    inner_magnet_pocket_y: Interval = (-20.80, -18.70)
    inner_magnet_protection_diameter: float = 9.00
    inner_magnet_medicine_barrier_y: float = 2.70
    cover_magnet_boss_diameter: float = 9.00
    # The visible M2 cylinder ends at the magnet-seat mouth.  Consequently the
    # complete front-open recess is exactly one 2.10 mm-deep seat; there is no
    # additional same-diameter installation tunnel in which a second magnet
    # can hide.
    cover_magnet_boss_y: Interval = (-18.80, -14.30)
    cover_m1_seat_y: Interval = (-21.10, -19.00)
    cover_m2_seat_y: Interval = (-16.40, -14.30)
    cover_magnet_web_y: Interval = (-19.00, -16.40)
    m1_forward_pole: str = "N"
    m2_rear_pole: str = "S"
    m2_forward_pole: str = "N"
    inner_rear_pole: str = "N"

    @property
    def working_travel_y(self): return self.released_state - self.pressed_state
    @property
    def cavity_rear_width_x(self): return self.inner_body_size_xz - 2 * self.standard_shell_thickness
    @property
    def cavity_seam_width_x(self): return self.cavity_rear_width_x
    @property
    def cavity_front_width_x(self): return self.key_section_size_xz(self.cavity_front_y) - 2 * self.standard_shell_thickness
    @property
    def cavity_rear_radius_xz(self): return max(self.minimum_internal_radius, self.inner_body_corner_radius_xz - self.standard_shell_thickness)
    @property
    def cavity_seam_radius_xz(self): return max(self.minimum_internal_radius, self.key_skirt_corner_radius_xz - self.standard_shell_thickness)
    @property
    def cavity_front_outer_radius_xz(self):
        f = (self.cavity_front_y - self.key_local_y[0]) / self.key_loft_length_y
        return self.key_skirt_corner_radius_xz + f * (self.key_face_corner_radius_xz - self.key_skirt_corner_radius_xz)
    @property
    def cavity_front_radius_xz(self): return max(self.minimum_internal_radius, self.cavity_front_outer_radius_xz - self.standard_shell_thickness)
    @property
    def cavity_rear_roof_z(self): return self.inner_body_size_xz / 2 - self.standard_shell_thickness
    @property
    def cavity_seam_roof_z(self): return self.cavity_rear_roof_z
    @property
    def cavity_front_roof_z(self): return self.key_section_size_xz(self.cavity_front_y) / 2 - self.standard_shell_thickness
    @property
    def chamber_boolean_floor_z(self): return self.hopper_start_z - self.hopper_boolean_overlap_z
    @property
    def hopper_boolean_top_z(self): return self.hopper_start_z + self.hopper_boolean_overlap_z
    @property
    def hopper_boolean_floor_z(self): return self.hopper_throat_floor_z - self.hopper_boolean_overlap_z
    @property
    def outer_port_center_world_y(self):
        aligned_center = self.inner_center_y(self.pressed_state) + sum(self.inner_port_local_y) / 2
        return aligned_center - self.outer_port_rearward_bias_y / 2
    @property
    def outer_port_length_y(self): return self.pill_port_length_y - self.outer_port_rearward_bias_y
    @property
    def outer_port_world_y(self):
        half = self.outer_port_length_y / 2
        return (self.outer_port_center_world_y - half, self.outer_port_center_world_y + half)
    def inner_port_world_y(self, state):
        center = self.inner_center_y(state)
        return (center + self.inner_port_local_y[0], center + self.inner_port_local_y[1])
    @staticmethod
    def interval_overlap_y(first: Interval, second: Interval):
        return max(0.0, min(first[1], second[1]) - max(first[0], second[0]))
    @property
    def pressed_port_overlap_y(self):
        return self.interval_overlap_y(self.inner_port_world_y(self.pressed_state), self.outer_port_world_y)
    def moving_port_tool_offset_y(self, state):
        return sum(self.inner_port_world_y(state)) / 2 - self.outer_port_center_world_y
    def port_separation_y(self, state): return round(self.inner_port_world_y(state)[0] - self.outer_port_world_y[1], 10)
    @property
    def released_port_separation_y(self): return self.port_separation_y(self.released_state)
    @property
    def released_return_shortfall_allowance_y(self):
        """Compatibility alias for the named vertical-sag envelope."""
        return self.released_vertical_sag_envelope_y
    @property
    def sagged_released_state(self): return self.maximum_pull_state - self.released_vertical_sag_envelope_y
    @property
    def sagged_port_separation_y(self): return self.port_separation_y(self.sagged_released_state)
    @property
    def released_operating_state(self): return self.sagged_released_state
    @property
    def released_operating_port_separation_y(self): return self.sagged_port_separation_y
    @property
    def released_view_depth_z(self): return self.inner_port_z[1] - self.outer_port_z[0]
    @property
    def sagged_no_peek_offset_y(self): return self.released_view_depth_z * tan(radians(self.released_no_peek_half_angle_degrees))
    @property
    def sagged_no_peek_margin_y(self): return self.sagged_port_separation_y - self.sagged_no_peek_offset_y
    @property
    def released_no_peek_offset_y(self): return self.sagged_no_peek_offset_y
    @property
    def released_no_peek_margin_y(self): return self.sagged_no_peek_margin_y
    @property
    def motion_sweep_step_y(self):
        return (self.maximum_pull_state - self.pressed_state) / (self.motion_sweep_sample_count - 1)
    @property
    def rear_pilot_clearance_per_side_xz(self):
        return (self.main_guide_size_xz - self.rear_pilot_size_xz) / 2
    @property
    def released_inner_port_front_cover_y(self): return self.housing_front_y - self.inner_port_world_y(self.released_state)[1]
    @property
    def released_inner_body_rear_world_y(self): return self.inner_center_y(self.released_state) + self.inner_body_local_y[0]
    @property
    def released_outer_port_rear_cover_y(self): return self.outer_port_world_y[0] - self.released_inner_body_rear_world_y
    @staticmethod
    def rounded_rectangle_area(width, length, radius): return width * length - (4 - pi) * radius**2
    @property
    def pill_port_area_xy(self): return self.rounded_rectangle_area(self.pill_port_width_x, self.pill_port_length_y, self.pill_port_corner_radius_xy)
    @property
    def reference_port_area_xy(self): return self.rounded_rectangle_area(self.reference_port_width_x, self.reference_port_length_y, self.pill_port_corner_radius_xy)
    @property
    def port_area_gain_ratio(self): return self.pill_port_area_xy / self.reference_port_area_xy
    @property
    def port_side_wall_thickness_x(self): return (self.inner_body_size_xz - self.pill_port_width_x) / 2
    @property
    def inner_magnet_seat_depth_y(self): return self.inner_magnet_pocket_y[1] - self.inner_magnet_pocket_y[0]
    @property
    def magnet_pick_bore_offset_x(self): return (self.magnet_pocket_diameter + self.magnet_pick_bore_diameter) / 2 - self.magnet_pick_bore_overlap_x
    @property
    def magnet_pick_bore_centres_x(self):
        return tuple(x - self.magnet_pick_bore_offset_x if x < 0 else x + self.magnet_pick_bore_offset_x for x in self.return_magnet_centres_x)
    @property
    def inner_magnet_pick_bore_y(self): return (self.inner_magnet_pocket_y[0], self.inner_magnet_pocket_y[1] + self.magnet_pick_bore_extra_depth_y)
    @property
    def cover_m1_pick_bore_y(self): return (self.cover_m1_seat_y[0], self.cover_m1_seat_y[1] + self.magnet_pick_bore_extra_depth_y)
    @property
    def cover_m2_pick_bore_y(self): return (self.cover_m2_seat_y[0] - self.magnet_pick_bore_extra_depth_y, self.cover_m2_seat_y[1])
    @property
    def magnet_pick_bore_depth_y(self): return self.magnet_nominal_depth_y + 0.10 + self.magnet_pick_bore_extra_depth_y
    @property
    def inner_pick_medicine_barrier_y(self): return self.cavity_rear_y - self.inner_magnet_pick_bore_y[1]
    @property
    def cover_pick_web_thickness_y(self): return self.cover_m2_pick_bore_y[0] - self.cover_m1_pick_bore_y[1]
    @property
    def magnet_pick_outer_boss_skin_x(self): return self.cover_magnet_boss_diameter / 2 - (self.magnet_pick_bore_offset_x + self.magnet_pick_bore_diameter / 2)
    @property
    def cover_m1_depth_y(self): return self.cover_m1_seat_y[1] - self.cover_m1_seat_y[0]
    @property
    def cover_m2_depth_y(self): return self.cover_m2_seat_y[1] - self.cover_m2_seat_y[0]
    @property
    def cover_magnet_web_thickness_y(self): return self.cover_magnet_web_y[1] - self.cover_magnet_web_y[0]
    @property
    def inner_magnet_count(self): return 2
    @property
    def rear_cover_magnet_count(self): return 4
    @property
    def m1_m2_attract(self): return self.m1_forward_pole != self.m2_rear_pole
    @property
    def m2_inner_repel(self): return self.m2_forward_pole == self.inner_rear_pole
    def magnet_face_separation_y(self, state): return self.inner_center_y(state) + self.inner_magnet_pocket_y[0] - self.cover_m2_seat_y[1]


P1_HOLLOW_MAGNETIC_DISPENSER = P1HollowMagneticDispenserSpec()
__all__ = ["P1_HOLLOW_MAGNETIC_DISPENSER", "P1HollowMagneticDispenserSpec"]
