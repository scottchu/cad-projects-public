"""V2 keyboard/inverted-rail mechanical-fit prototype."""

from .assembly import make_assembly, make_pressed_assembly, make_released_assembly, placed_inner
from .coupon import (
    make_c5_arm_cover_specimen,
    make_c5_coupon_assembly,
    make_c5_housing_receiver_specimen,
)
from .geometry import (
    make_blind_two_side_latch_rear_cover,
    make_deflected_side_latch_arm,
    make_outer_housing,
    make_rear_cover_core,
    make_side_latch_arm,
    make_side_latch_connector_pad,
    make_side_latch_hook,
    make_solid_keyboard_button,
)
from .print_exports import (
    make_print_bundle,
    print_c5_arm_cover_specimen,
    print_c5_housing_receiver_specimen,
    print_blind_two_side_latch_rear_cover,
    print_outer_housing,
    print_solid_keyboard_button,
)
from .spec import P0_MECHANICAL_FIT_V2, P0MechanicalFitV2Spec

__all__ = [
    "P0_MECHANICAL_FIT_V2",
    "P0MechanicalFitV2Spec",
    "make_assembly",
    "make_blind_two_side_latch_rear_cover",
    "make_c5_arm_cover_specimen",
    "make_c5_coupon_assembly",
    "make_c5_housing_receiver_specimen",
    "make_deflected_side_latch_arm",
    "make_outer_housing",
    "make_pressed_assembly",
    "make_print_bundle",
    "make_released_assembly",
    "make_rear_cover_core",
    "make_side_latch_arm",
    "make_side_latch_connector_pad",
    "make_side_latch_hook",
    "make_solid_keyboard_button",
    "placed_inner",
    "print_c5_arm_cover_specimen",
    "print_c5_housing_receiver_specimen",
    "print_blind_two_side_latch_rear_cover",
    "print_outer_housing",
    "print_solid_keyboard_button",
]
