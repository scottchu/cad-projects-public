"""Frozen millimetre contract for the V2.1 keyboard-identity derivative."""

from dataclasses import dataclass

from pill_click.p0_mechanical_fit_v2_keyboard_inverted_rails.spec import (
    P0MechanicalFitV2Spec,
)


@dataclass(frozen=True)
class P0MechanicalFitV21Spec(P0MechanicalFitV2Spec):
    # Physical V2 feedback: rails and front stops are accepted. Only the rear
    # side-squeeze latch is tightened for positive retention.
    side_latch_beam_thickness_x: float = 1.10
    side_latch_hook_shoulder_inner_x: float = 18.10
    side_latch_hook_apex_x: float = 18.70
    side_latch_direct_insertion_travel_x: float = 0.65
    side_latch_required_hook_release_x: float = 0.65
    side_latch_pad_release_travel_x: float = 0.48
    side_latch_pad_squeeze_stop_x: float = 0.55
    side_latch_pocket_depth_x: float = 0.70
    side_latch_outer_skin_x: float = 1.20
    side_latch_pocket_x: tuple[float, float] = (18.10, 18.80)

    key_face_size_xz: float = 29.0
    key_face_corner_radius_xz: float = 5.5
    key_face_edge_fillet_y: float = 1.0
    key_local_y: tuple[float, float] = (12.5, 20.5)
    key_face_dish_radius_xz: float = 14.0
    key_face_dish_depth_y: float = 0.55

    @property
    def keycap_height(self) -> float:
        return self.key_local_y[1] - self.key_local_y[0]

    @property
    def key_face_dish_sphere_radius(self) -> float:
        radius = self.key_face_dish_radius_xz
        depth = self.key_face_dish_depth_y
        return (radius**2 + depth**2) / (2 * depth)

    @property
    def pressed_key_proud_y(self) -> float:
        return self.inner_center_y(self.pressed_state) + self.key_local_y[1] - self.housing_front_y

    @property
    def released_key_proud_y(self) -> float:
        return self.inner_center_y(self.released_state) + self.key_local_y[1] - self.housing_front_y


P0_MECHANICAL_FIT_V21 = P0MechanicalFitV21Spec()

__all__ = ["P0_MECHANICAL_FIT_V21", "P0MechanicalFitV21Spec"]
