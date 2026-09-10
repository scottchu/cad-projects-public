"""Production print poses and the exactly-three-part V2 plate."""

from build123d import Compound, Location, Shape

from .coupon import make_c5_arm_cover_specimen, make_c5_housing_receiver_specimen
from .geometry import (
    make_blind_two_side_latch_rear_cover,
    make_outer_housing,
    make_solid_keyboard_button,
)


def _located(shape: Shape, location: Location, label: str) -> Shape:
    if shape.children:
        children = []
        for child in shape.children:
            placed = (location * child).clean()
            placed.label = child.label
            children.append(placed)
        return Compound(children=children, label=label)
    placed = (location * shape).clean()
    placed.label = label
    return placed


def _on_bed(shape: Shape, rotation: tuple[float, float, float], label: str) -> Shape:
    oriented = _located(shape, Location((0.0, 0.0, 0.0), rotation), label)
    return _located(
        oriented,
        Location((0.0, 0.0, -oriented.bounding_box().min.Z)),
        label,
    )


def print_outer_housing() -> Shape:
    return _on_bed(
        make_outer_housing(),
        (90.0, 0.0, 0.0),
        "p0_mechanical_fit_v2_outer_housing_print_rear_opening_on_bed",
    )


def print_solid_keyboard_button() -> Shape:
    return _on_bed(
        make_solid_keyboard_button(),
        (-90.0, 0.0, 0.0),
        "p0_mechanical_fit_v2_keyboard_button_print_key_face_on_bed",
    )


def print_blind_two_side_latch_rear_cover() -> Shape:
    return _on_bed(
        make_blind_two_side_latch_rear_cover(),
        (90.0, 0.0, 0.0),
        "p0_mechanical_fit_v2_two_side_latch_cover_print_blind_face_on_bed",
    )


def make_print_bundle() -> Compound:
    children = []
    for shape, location, label in (
        (print_outer_housing(), Location((-55.0, 0.0, 0.0)), "outer_housing"),
        (print_solid_keyboard_button(), Location((0.0, 0.0, 0.0)), "keyboard_button"),
        (
            print_blind_two_side_latch_rear_cover(),
            Location((55.0, 0.0, 0.0)),
            "rear_cover",
        ),
    ):
        children.append(_located(shape, location, label))
    return Compound(
        children=children,
        label="p0_mechanical_fit_v2_print_bundle_exactly_3_parts",
    )


def print_c5_arm_cover_specimen() -> Shape:
    return _on_bed(
        make_c5_arm_cover_specimen(),
        (90.0, 0.0, 0.0),
        "C5_V2_side_latch_arm_cover_specimen_print_cover_positive_Y_up",
    )


def print_c5_housing_receiver_specimen() -> Shape:
    return _on_bed(
        make_c5_housing_receiver_specimen(),
        (90.0, 0.0, 0.0),
        "C5_V2_side_latch_housing_receiver_specimen_print_housing_positive_Y_up",
    )


__all__ = [
    "make_print_bundle",
    "print_c5_arm_cover_specimen",
    "print_c5_housing_receiver_specimen",
    "print_blind_two_side_latch_rear_cover",
    "print_outer_housing",
    "print_solid_keyboard_button",
]
