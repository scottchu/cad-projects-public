"""Millimetre contract for the V2.2 layer-aware planar rear latch."""

from dataclasses import dataclass

from pill_click.p0_mechanical_fit_v21_keyboard_identity.spec import (
    P0MechanicalFitV21Spec,
)


Interval = tuple[float, float]


@dataclass(frozen=True)
class P0MechanicalFitV22Spec(P0MechanicalFitV21Spec):
    """V2.1 keyboard geometry with a 0.4 mm-nozzle-safe rear closure."""

    nozzle_diameter: float = 0.40
    nominal_layer_height: float = 0.20

    # Bring the key skirt almost to the 40 mm housing edge while preserving a
    # real front bezel.  The resulting 37.60 -> 29.00 mm loft gives the strong
    # mechanical-key taper requested in the physical review.
    front_bezel_chamfer: float = 0.20
    front_guide_size_xz: float = 38.00
    front_guide_corner_radius_xz: float = 5.20
    key_skirt_size_xz: float = 37.60
    key_skirt_corner_radius_xz: float = 5.00
    key_flare_local_y: float = 13.00

    # The accepted rails, front stops and 13.4 mm travel remain inherited.
    # The rear face is thicker so the compliant members have six nozzle-widths
    # of print depth when the cover is printed exterior-face-down.
    rear_faceplate_exterior_y: float = -21.10

    # Large finger paddles remain part of the faceplate, so all bending happens
    # within the XZ print plane rather than across layer lines.  Their 2.40 mm
    # side projection is six nozzle diameters and is intentionally easy to grip.
    planar_latch_paddle_x: Interval = (16.20, 22.40)
    planar_latch_paddle_z: Interval = (-5.00, 5.00)
    planar_latch_beam_x: Interval = (16.20, 17.40)
    planar_latch_upper_beam_z: Interval = (5.00, 18.50)
    planar_latch_lower_beam_z: Interval = (-18.50, -5.00)
    planar_latch_upper_outer_slot_z: Interval = (5.00, 20.20)
    planar_latch_lower_outer_slot_z: Interval = (-20.20, -5.00)
    planar_latch_inner_slot_x: Interval = (15.00, 16.20)
    planar_latch_inner_slot_z: Interval = (-18.50, 18.50)
    planar_latch_outer_slot_x: Interval = (17.40, 20.40)
    planar_latch_slot_corner_radius: float = 0.50
    planar_latch_pilot_relief_x: Interval = (14.90, 17.50)
    planar_latch_pilot_relief_z: Interval = (-18.60, 18.60)

    # A fixed nub projects into each 1.20 mm inner slot.  The paddle reaches it
    # after 0.80 mm, making the strain-limiting stop real geometry rather than a
    # documentation-only number.
    planar_latch_stop_projection_x: float = 0.40
    planar_latch_stop_z: Interval = (-1.60, 1.60)

    planar_latch_tower_x: Interval = (15.60, 18.00)
    planar_latch_tower_y: Interval = (-18.90, -15.90)
    planar_latch_tower_z: Interval = (-5.00, 5.00)
    planar_latch_hook_rear_base_y: float = -17.50
    planar_latch_hook_shoulder_y: float = -16.30
    planar_latch_hook_apex_front_y: float = -16.10
    planar_latch_hook_front_base_y: float = -15.90
    planar_latch_hook_shoulder_inner_x: float = 18.00
    planar_latch_hook_apex_x: float = 18.70

    planar_latch_broad_notch_x: Interval = (18.10, 20.20)
    planar_latch_broad_notch_y: Interval = (-18.90, -16.90)
    planar_latch_tower_passage_x: Interval = (15.20, 18.10)
    planar_latch_tower_passage_y: Interval = (-18.90, -15.50)
    planar_latch_receiver_pocket_x: Interval = (18.10, 18.80)
    planar_latch_receiver_pocket_y: Interval = (-16.50, -15.70)
    planar_latch_receiver_z: Interval = (-5.20, 5.20)

    planar_latch_release_travel_x: float = 0.70
    planar_latch_hard_stop_travel_x: float = 0.80

    @property
    def rear_faceplate_thickness_y(self) -> float:
        return self.rear_faceplate_interior_y - self.rear_faceplate_exterior_y

    @property
    def planar_latch_beam_thickness_x(self) -> float:
        return self.planar_latch_beam_x[1] - self.planar_latch_beam_x[0]

    @property
    def planar_latch_beam_effective_length_z(self) -> float:
        return self.planar_latch_upper_beam_z[1] - self.planar_latch_upper_beam_z[0]

    @property
    def planar_latch_inner_slot_width_x(self) -> float:
        return self.planar_latch_inner_slot_x[1] - self.planar_latch_inner_slot_x[0]

    @property
    def planar_latch_tower_thickness_x(self) -> float:
        return self.planar_latch_tower_x[1] - self.planar_latch_tower_x[0]

    @property
    def planar_latch_tower_width_z(self) -> float:
        return self.planar_latch_tower_z[1] - self.planar_latch_tower_z[0]

    @property
    def planar_latch_paddle_projection_x(self) -> float:
        return self.planar_latch_paddle_x[1] - self.half_housing

    @property
    def planar_latch_stop_surface_x(self) -> float:
        return self.planar_latch_inner_slot_x[0] + self.planar_latch_stop_projection_x

    @property
    def planar_latch_actual_stop_travel_x(self) -> float:
        return self.planar_latch_paddle_x[0] - self.planar_latch_stop_surface_x

    @property
    def planar_latch_hook_engagement_x(self) -> float:
        return self.planar_latch_hook_apex_x - self.planar_latch_receiver_pocket_x[0]

    @property
    def planar_latch_released_hook_clearance_x(self) -> float:
        return self.planar_latch_release_travel_x - self.planar_latch_hook_engagement_x

    @property
    def planar_latch_outer_skin_x(self) -> float:
        return self.half_housing - self.planar_latch_receiver_pocket_x[1]

    @property
    def planar_latch_axial_seating_clearance_y(self) -> float:
        return self.planar_latch_hook_shoulder_y - self.planar_latch_receiver_pocket_y[0]

    @property
    def planar_latch_retention_wall_y(self) -> float:
        return self.planar_latch_receiver_pocket_y[0] - self.planar_latch_broad_notch_y[1]

    def planar_latch_strain(self, travel: float) -> float:
        """Conservative fixed-guided beam surface-strain estimate."""
        return (
            3
            * self.planar_latch_beam_thickness_x
            * travel
            / self.planar_latch_beam_effective_length_z**2
        )


P0_MECHANICAL_FIT_V22 = P0MechanicalFitV22Spec()

__all__ = ["P0_MECHANICAL_FIT_V22", "P0MechanicalFitV22Spec"]
