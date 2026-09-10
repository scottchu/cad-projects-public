"""Parametric millimetre contract for the four-part P1 dispenser."""

from dataclasses import dataclass
from math import pi

from pill_click.p0_mechanical_fit_v23_keyboard_durable_latch.spec import P0MechanicalFitV23Spec

Interval = tuple[float, float]


@dataclass(frozen=True)
class P1HollowMagneticDispenserSpec(P0MechanicalFitV23Spec):
    """V2.3 exterior with an open-rear hopper, bonded cap, and coaxial magnets."""

    nozzle_diameter: float = 0.40
    standard_shell_thickness: float = 1.20
    key_face_membrane_y: float = 0.80
    minimum_internal_radius: float = 1.20
    pressed_state: float = 3.40
    inward_state: float = 3.40
    released_state: float = 18.40
    maximum_pull_state: float = 18.55
    inner_body_local_y: Interval = (-20.80, 1.50)
    male_rail_local_y: Interval = (-20.80, -8.20)
    spine_local_y: Interval = (-20.80, -12.80)
    open_body_shell_rear_y: float = -15.80
    inner_rear_cap_panel_y: Interval = (-20.80, -19.60)
    cap_tongue_depth_y: float = 1.20
    cap_tongue_width_xz: float = 1.20
    cap_tongue_clearance_xz: float = 0.20
    cap_cartridge_front_y: float = -16.00
    cap_cartridge_overlap_y: float = 0.20
    cap_panel_size_xz: float = 34.20
    cap_panel_corner_radius_xz: float = 3.00
    cavity_rear_y: float = -15.70
    cavity_seam_y: float = 1.50
    cavity_front_y: float = 19.70
    hopper_start_z: float = -3.00
    hopper_rear_throat_y: float = -6.00
    hopper_front_throat_y: float = 6.00
    hopper_throat_floor_z: float = -16.10
    hopper_blend_radius_xz: float = 1.20
    hopper_boolean_overlap_z: float = 0.10
    hopper_degenerate_section_height_z: float = 0.20
    pill_port_width_x: float = 30.00
    pill_port_length_y: float = 12.00
    pill_port_corner_radius_xy: float = 2.50
    inner_port_local_y: Interval = (-6.00, 6.00)
    inner_port_z: Interval = (-17.30, -14.30)
    outer_port_z: Interval = (-20.20, -16.90)
    reference_port_width_x: float = 22.00
    reference_port_length_y: float = 8.00
    released_shutter_safety_inset: float = 0.40
    magnet_nominal_diameter: float = 6.00
    magnet_nominal_depth_y: float = 2.00
    magnet_pocket_diameter: float = 6.10
    magnet_boolean_overshoot_y: float = 0.05
    return_magnet_centres_x: tuple[float, float] = (-8.50, 8.50)
    return_magnet_center_z: float = 0.00
    inner_magnet_pocket_y: Interval = (-20.80, -18.70)
    inner_magnet_protection_diameter: float = 9.00
    inner_magnet_medicine_barrier_y: float = 2.70
    cover_magnet_boss_diameter: float = 9.00
    cover_magnet_boss_y: Interval = (-18.80, -12.90)
    cover_m1_seat_y: Interval = (-21.10, -19.00)
    cover_m2_seat_y: Interval = (-16.40, -14.30)
    cover_m2_front_access_y: Interval = (-14.30, -12.80)
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
    def outer_port_center_world_y(self): return self.inner_center_y(self.pressed_state) + sum(self.inner_port_local_y) / 2
    @property
    def outer_port_world_y(self):
        half = self.pill_port_length_y / 2
        return (self.outer_port_center_world_y - half, self.outer_port_center_world_y + half)
    def inner_port_world_y(self, state):
        center = self.inner_center_y(state)
        return (center + self.inner_port_local_y[0], center + self.inner_port_local_y[1])
    @property
    def released_port_separation_y(self): return self.inner_port_world_y(self.released_state)[0] - self.outer_port_world_y[1]
    @staticmethod
    def rounded_rectangle_area(width, length, radius): return width * length - (4 - pi) * radius**2
    @property
    def pill_port_area_xy(self): return self.rounded_rectangle_area(self.pill_port_width_x, self.pill_port_length_y, self.pill_port_corner_radius_xy)
    @property
    def reference_port_area_xy(self): return self.rounded_rectangle_area(self.reference_port_width_x, self.reference_port_length_y, self.pill_port_corner_radius_xy)
    @property
    def port_area_gain_ratio(self): return self.pill_port_area_xy / self.reference_port_area_xy
    @property
    def inner_magnet_seat_depth_y(self): return self.inner_magnet_pocket_y[1] - self.inner_magnet_pocket_y[0]
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
    def broad_stop_gap_y(self, state): return self.inner_center_y(state) + self.inner_rear_cap_panel_y[0] - self.cover_magnet_boss_y[1]
    def magnet_face_separation_y(self, state): return self.inner_center_y(state) + self.inner_magnet_pocket_y[0] - self.cover_m2_seat_y[1]


P1_HOLLOW_MAGNETIC_DISPENSER = P1HollowMagneticDispenserSpec()
__all__ = ["P1_HOLLOW_MAGNETIC_DISPENSER", "P1HollowMagneticDispenserSpec"]
