"""Millimetre contract for the V2.3 keyboard silhouette and durable latch."""

from dataclasses import dataclass
from math import atan2, degrees, sqrt

from pill_click.p0_mechanical_fit_v22_planar_latch.spec import (
    P0MechanicalFitV22Spec,
)


Interval = tuple[float, float]


@dataclass(frozen=True)
class P0MechanicalFitV23Spec(P0MechanicalFitV22Spec):
    """Accepted V2 rails with a true keycap loft and thick retaining teeth."""

    # The functional shuttle stops behind the housing front.  From this seam
    # forward there is exactly one continuous, monotonically narrowing loft.
    # A 10.00 mm physical stroke retains the accepted released rail-stop
    # location.  The four extended rails touch rear-cover stop bosses at the
    # pressed state; their 0.80 mm lead remains behind the longer body.
    pressed_state: float = 3.40
    inward_state: float = 3.40
    released_state: float = 13.40
    maximum_pull_state: float = 13.55
    feed_start_center_y: float = -39.40
    feed_end_center_y: float = 7.90
    feed_step: float = 0.50
    inner_body_local_y: Interval = (-20.80, 1.50)
    male_rail_local_y: Interval = (-21.60, -3.20)
    spine_local_y: Interval = (-21.60, -12.80)
    key_local_y: Interval = (1.50, 20.50)
    key_skirt_size_xz: float = 34.20
    key_skirt_corner_radius_xz: float = 3.00
    key_face_size_xz: float = 27.50
    key_face_corner_radius_xz: float = 4.50
    key_face_edge_fillet_y: float = 0.90
    key_face_dish_radius_xz: float = 12.25
    # Zero disables the parametric spherical subtraction.  Nonzero values
    # continue to produce the earlier inset without changing the loft.
    key_face_dish_depth_y: float = 0.00

    front_guide_size_xz: float = 35.20
    front_guide_corner_radius_xz: float = 3.50
    front_bezel_chamfer: float = 1.00

    # Named Boolean-tool overshoots replace kernel-tolerance literals.
    housing_guide_boolean_overshoot_y: float = 0.20
    female_channel_boolean_overshoot_y: float = 0.01
    rear_cover_boolean_overshoot_y: float = 0.10

    # The locating pilot is 3.20 mm deep.  Its last 0.40 mm is a 45-degree
    # entry loft from the full guide-matched profile to a smaller tip.
    rear_pilot_front_y: float = -15.50
    rear_pilot_entry_chamfer_rear_y: float = -15.90
    rear_pilot_tip_size_xz: float = 33.40
    rear_pilot_tip_corner_radius_xz: float = 2.60

    # Four bosses share the accepted rail contact bands and create the inward
    # axial stop without changing the accepted front blind-stop plane.
    rear_stop_boss_contact_plane_y: float = -13.70
    rear_stop_boss_count: int = 4

    # Wider inner clearance slot and a 1.20 mm fixed stop provide a modeled
    # 1.20 mm squeeze limit.  The accepted in-plane beams and large paddles
    # remain unchanged.
    # Both compliant side strips are 2.00 mm wide (five nozzle widths) and sit
    # directly on the outside edges of the 40 mm cover.  Their isolation slots
    # are inboard, so the visible/finger-contact member is no longer trapped
    # between two slots.  The slots stop at Z +/-18.00 to retain printed anchor
    # bridges inside the rounded cover corners.
    # The fixed stop is a continuous full-height rail, not a small centre nub.
    # Its X=15.00 face and the paddle's X=16.20 inner face leave the modeled
    # 1.20 mm squeeze gap as actual open geometry.
    planar_latch_stop_rail_x: Interval = (13.80, 15.00)
    planar_latch_inner_slot_x: Interval = (15.00, 16.20)
    planar_latch_beam_x: Interval = (18.00, 20.00)
    planar_latch_outer_slot_x: Interval = (16.00, 18.00)
    planar_latch_inner_slot_z: Interval = (-18.00, 18.00)
    planar_latch_upper_beam_z: Interval = (5.00, 18.00)
    planar_latch_lower_beam_z: Interval = (-18.00, -5.00)
    planar_latch_upper_outer_slot_z: Interval = (5.00, 18.00)
    planar_latch_lower_outer_slot_z: Interval = (-18.00, -5.00)
    # Overlap the rounded branch cuts through the full inner slot.  Their
    # union is one continuous opening with rounded terminal corners and no
    # isolated ledges.
    planar_latch_slot_overlap_x: float = 1.00
    # Keep the forward locating pilot completely behind the fixed center plate,
    # leaving a straight, flat-sided clearance behind each outer flexure.
    planar_latch_pilot_relief_x: Interval = (13.80, 17.50)
    planar_latch_pilot_relief_z: Interval = (-18.10, 18.10)
    # The release surface ends at the 40 mm cover envelope.  The surrounding
    # outer slots isolate this central 10 mm-tall side pad so it remains
    # squeezeable without a tab protruding beyond the housing.
    planar_latch_paddle_x: Interval = (16.20, 20.00)
    planar_latch_stop_projection_x: float = 1.20
    planar_latch_release_travel_x: float = 0.90
    planar_latch_hard_stop_travel_x: float = 1.20

    # Durable retaining tower and tooth.  The tower begins at the same X=16.20
    # inner face as the paddle, so neither feature intrudes into the real
    # 1.20 mm squeeze gap.  Its 2.00 mm thickness is five nozzle widths.  The
    # tooth has a 1.20 mm axial plateau (six 0.20 mm layers), 0.80 mm radial
    # engagement, and is extruded through the full 10 mm tower height.
    planar_latch_tower_x: Interval = (16.20, 18.20)
    planar_latch_tower_y: Interval = (-20.30, -13.90)
    planar_latch_tower_z: Interval = (-5.00, 5.00)
    planar_latch_hook_rear_base_x: float = 17.20
    planar_latch_hook_rear_base_y: float = -17.50
    planar_latch_hook_shoulder_inner_x: float = 18.00
    planar_latch_hook_shoulder_y: float = -16.50
    planar_latch_hook_apex_x: float = 18.80
    planar_latch_hook_apex_front_y: float = -15.30
    planar_latch_hook_front_inner_x: float = 18.00
    planar_latch_hook_front_base_x: float = 17.20
    planar_latch_hook_front_base_y: float = -13.90

    planar_latch_broad_notch_x: Interval = (18.00, 20.20)
    planar_latch_broad_notch_y: Interval = (-18.90, -18.10)
    planar_latch_tower_passage_x: Interval = (15.20, 18.40)
    planar_latch_tower_passage_y: Interval = (-18.90, -13.50)
    planar_latch_receiver_pocket_x: Interval = (18.00, 18.80)
    planar_latch_receiver_pocket_y: Interval = (-16.60, -15.10)
    planar_latch_front_ramp_relief_x: Interval = (18.00, 18.80)
    planar_latch_front_ramp_relief_y: Interval = (-15.10, -13.50)
    planar_latch_receiver_z: Interval = (-5.40, 5.40)

    @property
    def key_loft_length_y(self) -> float:
        return self.key_local_y[1] - self.key_local_y[0]

    @property
    def inner_body_length_y(self) -> float:
        return self.inner_body_local_y[1] - self.inner_body_local_y[0]

    @property
    def inner_body_rear_to_rail_rear_gap_y(self) -> float:
        return self.inner_body_local_y[0] - self.male_rail_local_y[0]

    @property
    def working_travel_y(self) -> float:
        return self.released_state - self.pressed_state

    @property
    def pressed_face_world_y(self) -> float:
        return self.inner_center_y(self.pressed_state) + self.key_local_y[1]

    @property
    def released_face_world_y(self) -> float:
        return self.inner_center_y(self.released_state) + self.key_local_y[1]

    @property
    def rear_pilot_depth_y(self) -> float:
        return self.rear_pilot_front_y - self.rear_faceplate_interior_y

    @property
    def rear_pilot_straight_depth_y(self) -> float:
        return self.rear_pilot_entry_chamfer_rear_y - self.rear_faceplate_interior_y

    @property
    def rear_pilot_entry_chamfer_length_y(self) -> float:
        return self.rear_pilot_front_y - self.rear_pilot_entry_chamfer_rear_y

    @property
    def rear_pilot_entry_chamfer_radial_xz(self) -> float:
        return (self.rear_pilot_size_xz - self.rear_pilot_tip_size_xz) / 2

    @property
    def rear_pilot_entry_chamfer_angle_degrees(self) -> float:
        return degrees(
            atan2(
                self.rear_pilot_entry_chamfer_radial_xz,
                self.rear_pilot_entry_chamfer_length_y,
            )
        )

    @property
    def rear_stop_boss_x(self) -> Interval:
        return (self.main_guide_half, self.male_tip_x)

    @property
    def rear_stop_boss_y(self) -> Interval:
        return (self.rear_faceplate_interior_y, self.rear_stop_boss_contact_plane_y)

    @property
    def rear_stop_boss_width_x(self) -> float:
        return self.rear_stop_boss_x[1] - self.rear_stop_boss_x[0]

    @property
    def rear_stop_boss_length_y(self) -> float:
        return self.rear_stop_boss_y[1] - self.rear_stop_boss_y[0]

    @property
    def rear_stop_contact_area_total(self) -> float:
        return (
            self.rear_stop_boss_count
            * self.rear_stop_boss_width_x
            * self.male_rail_width_z
        )

    def inward_stop_gap_y(self, state: float) -> float:
        """Positive clearance, zero contact, negative stop interference."""
        return self.rail_world_y(state)[0] - self.rear_stop_boss_contact_plane_y

    @property
    def planar_latch_rounded_anchor_bridge_z(self) -> float:
        """Actual top-anchor depth at the inner edge of an outside beam."""
        corner_center = self.half_housing - self.housing_outer_corner_radius_xz
        radial_x = self.planar_latch_beam_x[0] - corner_center
        rounded_edge_z = corner_center + sqrt(
            self.housing_outer_corner_radius_xz**2 - radial_x**2
        )
        return rounded_edge_z - self.planar_latch_upper_outer_slot_z[1]

    def key_section_size_xz(self, local_y: float) -> float:
        """Linear two-section loft width at a local axial coordinate."""
        if not self.key_local_y[0] <= local_y <= self.key_local_y[1]:
            raise ValueError("key section lies outside the continuous loft")
        fraction = (local_y - self.key_local_y[0]) / self.key_loft_length_y
        return self.key_skirt_size_xz + fraction * (
            self.key_face_size_xz - self.key_skirt_size_xz
        )

    @property
    def key_seam_hidden_at_max_pull_y(self) -> float:
        seam_world_y = self.inner_center_y(self.maximum_pull_state) + self.key_local_y[0]
        return self.housing_front_y - seam_world_y

    @property
    def planar_latch_stop_surface_x(self) -> float:
        return self.planar_latch_stop_rail_x[1]

    @property
    def planar_latch_hook_axial_plateau_y(self) -> float:
        return self.planar_latch_hook_apex_front_y - self.planar_latch_hook_shoulder_y

    @property
    def planar_latch_hook_axial_length_y(self) -> float:
        return self.planar_latch_hook_front_base_y - self.planar_latch_hook_rear_base_y

    @property
    def planar_latch_axial_seating_clearance_y(self) -> float:
        return self.planar_latch_hook_shoulder_y - self.planar_latch_receiver_pocket_y[0]

    @property
    def planar_latch_axial_front_clearance_y(self) -> float:
        return self.planar_latch_receiver_pocket_y[1] - self.planar_latch_hook_apex_front_y

    @property
    def planar_latch_retention_wall_y(self) -> float:
        return self.planar_latch_receiver_pocket_y[0] - self.planar_latch_broad_notch_y[1]

    @property
    def planar_latch_tower_passage_clearance_x(self) -> float:
        return self.planar_latch_tower_passage_x[1] - self.planar_latch_tower_x[1]


P0_MECHANICAL_FIT_V23 = P0MechanicalFitV23Spec()

__all__ = ["P0_MECHANICAL_FIT_V23", "P0MechanicalFitV23Spec"]
