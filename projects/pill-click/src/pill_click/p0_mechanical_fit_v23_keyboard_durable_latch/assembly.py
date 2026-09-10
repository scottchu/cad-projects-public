"""Pressed and released V2.3 keyboard/durable-latch assembly placements."""

from build123d import Compound, Location, Shape

from .geometry import make_keyboard_button, make_outer_housing, make_planar_latch_rear_cover
from .spec import P0_MECHANICAL_FIT_V23, P0MechanicalFitV23Spec


def placed_keyboard_button(
    state: float,
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Shape:
    button = Location((0.0, p.inner_center_y(state), 0.0)) * make_keyboard_button(p)
    button.label = f"v23_keyboard_button_state_{state:+.2f}"
    return button


def make_assembly(
    state: float,
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Compound:
    if not p.inward_state <= state <= p.maximum_pull_state:
        raise ValueError(
            f"state {state:.3f} is outside captive travel "
            f"[{p.inward_state:.2f}, {p.maximum_pull_state:.2f}]"
        )
    return Compound(
        children=[
            make_outer_housing(p),
            placed_keyboard_button(state, p),
            make_planar_latch_rear_cover(p),
        ],
        label=f"p0_mechanical_fit_v23_keyboard_durable_latch_state_{state:+.2f}",
    )


def make_pressed_assembly(
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Compound:
    return make_assembly(p.pressed_state, p)


def make_released_assembly(
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Compound:
    return make_assembly(p.released_state, p)


__all__ = [
    "make_assembly",
    "make_pressed_assembly",
    "make_released_assembly",
    "placed_keyboard_button",
]
