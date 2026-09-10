"""Three-part, opening-free P0 mechanical-fit prototype."""

from .assembly import make_assembly, make_pressed_assembly, make_released_assembly
from .geometry import make_outer_housing, make_snap_rear_cover, make_solid_inner_button
from .print_exports import (
    make_print_bundle,
    print_solid_inner_button,
    print_outer_housing,
    print_snap_rear_cover,
)
from .spec import P0_MECHANICAL_FIT_V1, P0MechanicalFitV1Spec

__all__ = [
    "P0_MECHANICAL_FIT_V1",
    "P0MechanicalFitV1Spec",
    "make_assembly",
    "make_solid_inner_button",
    "make_outer_housing",
    "make_pressed_assembly",
    "make_print_bundle",
    "make_released_assembly",
    "make_snap_rear_cover",
    "print_solid_inner_button",
    "print_outer_housing",
    "print_snap_rear_cover",
]
