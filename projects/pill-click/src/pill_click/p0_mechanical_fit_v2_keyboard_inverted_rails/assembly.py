"""Static pressed/released placements for the V2 three-part prototype."""

from build123d import Compound, Location, Shape

from .geometry import (
    make_blind_two_side_latch_rear_cover,
    make_outer_housing,
    make_solid_keyboard_button,
)
from .spec import P0_MECHANICAL_FIT_V2, P0MechanicalFitV2Spec


def placed_inner(
    state: float,
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Shape:
    inner = Location((0.0, p.inner_center_y(state), 0.0)) * make_solid_keyboard_button(p)
    inner.label = f"solid_keyboard_button_state_{state:+.2f}"
    return inner


def make_assembly(
    state: float,
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Compound:
    if not p.inward_state <= state <= p.maximum_pull_state:
        raise ValueError(
            f"state {state:.3f} is outside captive travel "
            f"[{p.inward_state:.2f}, {p.maximum_pull_state:.2f}]"
        )
    return Compound(
        children=[
            make_outer_housing(p),
            placed_inner(state, p),
            make_blind_two_side_latch_rear_cover(p),
        ],
        label=f"p0_mechanical_fit_v2_exactly_three_parts_state_{state:+.2f}",
    )


def make_pressed_assembly(
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Compound:
    return make_assembly(p.pressed_state, p)


def make_released_assembly(
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Compound:
    return make_assembly(p.released_state, p)


__all__ = ["make_assembly", "make_pressed_assembly", "make_released_assembly", "placed_inner"]
