"""V2.2 keyboard pill-click with layer-aware planar rear latches."""

from .assembly import (
    make_planar_latch_assembly,
    make_pressed_planar_latch_assembly,
    make_released_planar_latch_assembly,
    placed_keyboard_identity_button,
)
from .geometry import (
    make_keyboard_identity_button,
    make_keyboard_identity_keycap,
    make_outer_housing,
    make_deflected_planar_latch_lock,
    make_planar_latch_hook,
    make_planar_latch_lock,
    make_planar_latch_rear_cover,
    make_planar_latch_stop,
)
from .spec import P0_MECHANICAL_FIT_V22, P0MechanicalFitV22Spec

__all__ = [
    "P0_MECHANICAL_FIT_V22",
    "P0MechanicalFitV22Spec",
    "make_keyboard_identity_button",
    "make_keyboard_identity_keycap",
    "make_outer_housing",
    "make_deflected_planar_latch_lock",
    "make_planar_latch_assembly",
    "make_planar_latch_hook",
    "make_planar_latch_lock",
    "make_planar_latch_rear_cover",
    "make_planar_latch_stop",
    "make_pressed_planar_latch_assembly",
    "make_released_planar_latch_assembly",
    "placed_keyboard_identity_button",
]
