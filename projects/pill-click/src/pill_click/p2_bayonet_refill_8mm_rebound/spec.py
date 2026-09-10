"""Parametric contract for the P2 bayonet-refill / 8 mm rebound experiment."""

from dataclasses import dataclass
from math import atan, degrees, pi

from pill_click.p1_hollow_magnetic_dispenser.spec import P1HollowMagneticDispenserSpec


@dataclass(frozen=True)
class P2BayonetRefill8mmReboundSpec(P1HollowMagneticDispenserSpec):
    """P1 production motion with an isolated refill cap and larger return magnets."""

    # M1 remains the accepted 6 mm fridge attachment.  M2 and its opposed
    # inner seats are the only seats enlarged for this experiment.
    fridge_magnet_pocket_diameter: float = 6.10
    rebound_magnet_pocket_diameter: float = 8.10
    inner_magnet_pocket_diameter: float = 8.10
    fridge_pick_bore_offset_x: float = 3.55
    rebound_pick_bore_offset_x: float = 4.55
    inner_pick_bore_offset_x: float = 4.55
    cover_magnet_boss_diameter: float = 11.00
    inner_magnet_protection_diameter: float = 11.00

    # Refill interface; +Y is the front/key-face direction.
    refill_clear_bore_diameter: float = 16.00
    refill_neck_outer_diameter: float = 20.00
    refill_neck_projection_y: float = 4.00
    refill_neck_body_overlap_y: float = 0.25
    refill_neck_lug_radial_projection: float = 1.20
    refill_neck_lug_body_overlap: float = 0.30
    refill_neck_lug_axial_thickness_y: float = 1.60
    refill_neck_lug_arc_degrees: float = 30.00

    cap_outer_diameter: float = 26.00
    cap_internal_running_diameter: float = 20.60
    cap_top_thickness_y: float = 2.00
    cap_internal_depth_y: float = 5.85
    cap_radial_clearance_per_side: float = 0.30
    cap_axial_clearance_y: float = 0.25
    cap_rotation_degrees: float = 90.00
    cap_ramp_rise_y: float = 1.20
    cap_lead_in_chamfer: float = 0.60
    cap_rotation_stop_thickness: float = 1.20
    cap_minimum_wall_after_slots: float = 1.50
    cap_slot_sampling_degrees: float = 7.50

    @property
    def refill_neck_base_y(self):
        return self.key_local_y[1] - self.refill_neck_body_overlap_y

    @property
    def refill_neck_front_y(self):
        return self.key_local_y[1] + self.refill_neck_projection_y

    @property
    def refill_bore_y(self):
        return (self.cavity_front_y - 0.10, self.refill_neck_front_y + 0.10)

    @property
    def refill_lug_y(self):
        return (
            self.refill_neck_front_y - self.refill_neck_lug_axial_thickness_y,
            self.refill_neck_front_y,
        )

    @property
    def cap_total_depth_y(self):
        return self.cap_internal_depth_y + self.cap_top_thickness_y

    @property
    def cap_shell_radial_thickness(self):
        return (self.cap_outer_diameter - self.cap_internal_running_diameter) / 2

    @property
    def neck_lug_outer_radius(self):
        return self.refill_neck_outer_diameter / 2 + self.refill_neck_lug_radial_projection

    @property
    def neck_lug_arc_length(self):
        return self.neck_lug_outer_radius * pi * self.refill_neck_lug_arc_degrees / 180

    @property
    def cap_slot_axial_height_y(self):
        return self.refill_neck_lug_axial_thickness_y + self.cap_axial_clearance_y

    @property
    def cap_locked_axial_overlap_y(self):
        return self.refill_neck_lug_axial_thickness_y - self.cap_axial_clearance_y

    @property
    def cap_ramp_angle_degrees(self):
        arc = self.neck_lug_outer_radius * pi * self.cap_rotation_degrees / 180
        return degrees(atan(self.cap_ramp_rise_y / arc))

    def _pick_centres(self, offset):
        return tuple(x - offset if x < 0 else x + offset for x in self.return_magnet_centres_x)

    @property
    def fridge_pick_bore_centres_x(self):
        return self._pick_centres(self.fridge_pick_bore_offset_x)

    @property
    def rebound_pick_bore_centres_x(self):
        return self._pick_centres(self.rebound_pick_bore_offset_x)

    @property
    def inner_pick_bore_centres_x(self):
        return self._pick_centres(self.inner_pick_bore_offset_x)


P2_BAYONET_REFILL_8MM_REBOUND = P2BayonetRefill8mmReboundSpec()

__all__ = ["P2_BAYONET_REFILL_8MM_REBOUND", "P2BayonetRefill8mmReboundSpec"]
