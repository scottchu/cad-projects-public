"""Non-manufactured P1 review geometry."""

from build123d import Align, Box
from .geometry import make_hollow_keyboard_container
from .spec import P1_HOLLOW_MAGNETIC_DISPENSER


def make_hopper_cutaway(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    envelope = Box(50, 100, 100, align=(Align.MIN, Align.CENTER, Align.CENTER))
    result = (make_hollow_keyboard_container(p) & envelope).clean()
    result.label = "p1_integrated_inner_positive_x_cutaway"
    return result


__all__ = ["make_hopper_cutaway"]
