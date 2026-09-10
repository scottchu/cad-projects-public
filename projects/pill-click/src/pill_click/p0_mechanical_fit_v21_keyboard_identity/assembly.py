"""Pressed and released placements for the V2.1 keyboard-identity assembly."""

from build123d import Compound, Location, Shape

from .geometry import (
    make_blind_two_side_latch_rear_cover,
    make_keyboard_identity_button,
    make_outer_housing,
)
from .spec import P0_MECHANICAL_FIT_V21, P0MechanicalFitV21Spec


def placed_keyboard_identity_button(
    state: float,
    p: P0MechanicalFitV21Spec = P0_MECHANICAL_FIT_V21,
) -> Shape:
    button = Location((0.0, p.inner_center_y(state), 0.0)) * make_keyboard_identity_button(p)
    button.label = f"keyboard_identity_button_state_{state:+.2f}"
    return button


def make_keyboard_identity_assembly(
    state: float,
    p: P0MechanicalFitV21Spec = P0_MECHANICAL_FIT_V21,
) -> Compound:
    if not p.inward_state <= state <= p.maximum_pull_state:
        raise ValueError(
            f"state {state:.3f} is outside captive travel "
            f"[{p.inward_state:.2f}, {p.maximum_pull_state:.2f}]"
        )
    return Compound(
        children=[
            make_outer_housing(p),
            placed_keyboard_identity_button(state, p),
            make_blind_two_side_latch_rear_cover(p),
        ],
        label=f"p0_mechanical_fit_v21_keyboard_identity_state_{state:+.2f}",
    )


def make_pressed_keyboard_identity_assembly(
    p: P0MechanicalFitV21Spec = P0_MECHANICAL_FIT_V21,
) -> Compound:
    return make_keyboard_identity_assembly(p.pressed_state, p)


def make_released_keyboard_identity_assembly(
    p: P0MechanicalFitV21Spec = P0_MECHANICAL_FIT_V21,
) -> Compound:
    return make_keyboard_identity_assembly(p.released_state, p)


__all__ = [
    "make_keyboard_identity_assembly",
    "make_pressed_keyboard_identity_assembly",
    "make_released_keyboard_identity_assembly",
    "placed_keyboard_identity_button",
]
