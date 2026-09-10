"""Print poses and three-object plate layout for mechanical-fit V2.3."""

from build123d import Compound, Location, Shape

from .geometry import (
    make_keyboard_button,
    make_outer_housing,
    make_planar_latch_rear_cover,
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
    """Place the housing rear opening on the bed."""
    return _on_bed(
        make_outer_housing(),
        (90.0, 0.0, 0.0),
        "p0_mechanical_fit_v23_outer_housing_rear_opening_on_bed",
    )


def print_keyboard_button() -> Shape:
    """Place the flat, edge-filleted keyboard face on the bed."""
    return _on_bed(
        make_keyboard_button(),
        (-90.0, 0.0, 0.0),
        "p0_mechanical_fit_v23_keyboard_button_key_face_on_bed",
    )


def print_planar_latch_rear_cover() -> Shape:
    """Place the rear cover exterior face on the bed."""
    return _on_bed(
        make_planar_latch_rear_cover(),
        (90.0, 0.0, 0.0),
        "p0_mechanical_fit_v23_rear_cover_exterior_face_on_bed",
    )


def make_print_bundle() -> Compound:
    """Return three named, independently selectable, non-overlapping objects."""
    children = []
    for shape, location, label in (
        (print_outer_housing(), Location((-55.0, 0.0, 0.0)), "outer_housing"),
        (print_keyboard_button(), Location((0.0, 0.0, 0.0)), "keyboard_button"),
        (
            print_planar_latch_rear_cover(),
            Location((55.0, 0.0, 0.0)),
            "rear_cover",
        ),
    ):
        children.append(_located(shape, location, label))
    return Compound(
        children=children,
        label="p0_mechanical_fit_v23_test_print_bundle_exactly_3_parts",
    )


__all__ = [
    "make_print_bundle",
    "print_keyboard_button",
    "print_outer_housing",
    "print_planar_latch_rear_cover",
]
