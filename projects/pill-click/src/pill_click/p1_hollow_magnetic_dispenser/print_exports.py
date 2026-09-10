"""Print poses and exact three-object P1 bundle."""

from build123d import Compound, Location
from .geometry import make_hollow_keyboard_container, make_magnetic_rear_cover, make_ported_outer_housing


def _located(shape, location, label):
    if shape.children:
        return Compound(children=[location * child for child in shape.children], label=label)
    placed = (location * shape).clean(); placed.label = label; return placed


def _on_bed(shape, rotation, label):
    oriented = _located(shape, Location((0, 0, 0), rotation), label)
    return _located(oriented, Location((0, 0, -oriented.bounding_box().min.Z)), label)


def print_outer_housing(): return _on_bed(make_ported_outer_housing(), (90, 0, 0), "outer_housing")
def print_hollow_keyboard_container(): return _on_bed(make_hollow_keyboard_container(), (-90, 0, 0), "integrated_inner")
def print_magnetic_rear_cover(): return _on_bed(make_magnetic_rear_cover(), (90, 0, 0), "rear_cover")


def make_print_bundle():
    children = []
    for shape, x, label in ((print_outer_housing(), -50, "housing"), (print_hollow_keyboard_container(), 0, "integrated_inner"), (print_magnetic_rear_cover(), 50, "rear_cover")):
        children.append(_located(shape, Location((x, 0, 0)), label))
    return Compound(children=children, label="p1_test_print_bundle_exactly_3_parts")


__all__ = ["make_print_bundle", "print_hollow_keyboard_container", "print_magnetic_rear_cover", "print_outer_housing"]
