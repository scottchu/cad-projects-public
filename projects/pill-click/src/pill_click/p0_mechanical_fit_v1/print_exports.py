"""Rigid print poses and three-part plate layout for mechanical-fit v1."""

from build123d import Compound, Location, Shape

from .geometry import make_outer_housing, make_snap_rear_cover, make_solid_inner_button


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
        (0.0, -90.0, 0.0),
        "p0_mechanical_fit_v1_outer_housing_print_X_negative_face_on_bed",
    )


def print_solid_inner_button() -> Shape:
    return _on_bed(
        make_solid_inner_button(),
        (-90.0, 0.0, 0.0),
        "p0_mechanical_fit_v1_solid_inner_button_print_key_face_on_bed",
    )


def print_snap_rear_cover() -> Shape:
    return _on_bed(
        make_snap_rear_cover(),
        (90.0, 0.0, 0.0),
        "p0_mechanical_fit_v1_snap_rear_cover_print_blind_face_on_bed",
    )


def make_print_bundle() -> Compound:
    children = []
    for shape, location, label in (
        (print_outer_housing(), Location((-55.0, 0.0, 0.0)), "outer_housing"),
        (print_solid_inner_button(), Location((0.0, 0.0, 0.0)), "solid_inner_button"),
        (print_snap_rear_cover(), Location((55.0, 0.0, 0.0)), "snap_rear_cover"),
    ):
        children.append(_located(shape, location, label))
    return Compound(
        children=children,
        label="p0_mechanical_fit_v1_print_bundle_exactly_3_parts_no_openings",
    )


__all__ = [
    "make_print_bundle",
    "print_solid_inner_button",
    "print_outer_housing",
    "print_snap_rear_cover",
]
