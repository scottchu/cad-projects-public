"""Pressed and released three-part P1 assembly placements."""

from build123d import Compound, Location
from .geometry import make_hollow_keyboard_container, make_magnetic_rear_cover, make_ported_outer_housing
from .spec import P1_HOLLOW_MAGNETIC_DISPENSER, P1HollowMagneticDispenserSpec


def placed_hollow_keyboard_container(state, p=P1_HOLLOW_MAGNETIC_DISPENSER):
    shape = Location((0, p.inner_center_y(state), 0)) * make_hollow_keyboard_container(p)
    shape.label = f"p1_integrated_inner_state_{state:+.2f}"
    return shape


def make_assembly(state, p=P1_HOLLOW_MAGNETIC_DISPENSER):
    if not p.inward_state <= state <= p.maximum_pull_state:
        raise ValueError("state is outside captive travel")
    return Compound(children=[make_ported_outer_housing(p), placed_hollow_keyboard_container(state, p), make_magnetic_rear_cover(p)], label=f"p1_three_part_state_{state:+.2f}")


def make_pressed_assembly(p=P1_HOLLOW_MAGNETIC_DISPENSER): return make_assembly(p.pressed_state, p)
def make_released_assembly(p=P1_HOLLOW_MAGNETIC_DISPENSER): return make_assembly(p.released_state, p)


__all__ = ["make_assembly", "make_pressed_assembly", "make_released_assembly", "placed_hollow_keyboard_container"]
