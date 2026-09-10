"""Print poses and exact four-mesh P2 bundle."""

from build123d import Compound, Location

from .geometry import make_bayonet_cap, make_hollow_keyboard_container, make_magnetic_rear_cover, make_ported_outer_housing


def _located(shape, location, label):
    placed = (location * shape).clean()
    placed.label = label
    return placed


def _on_bed(shape, rotation, label):
    oriented = _located(shape, Location((0, 0, 0), rotation), label)
    return _located(oriented, Location((0, 0, -oriented.bounding_box().min.Z)), label)


def print_outer_housing(): return _on_bed(make_ported_outer_housing(), (90, 0, 0), "outer_housing")
def print_hollow_keyboard_container(): return _on_bed(make_hollow_keyboard_container(), (-90, 0, 0), "integrated_inner")
def print_magnetic_rear_cover(): return _on_bed(make_magnetic_rear_cover(), (90, 0, 0), "rear_cover")
def print_bayonet_cap(): return _on_bed(make_bayonet_cap(), (-90, 0, 0), "bayonet_cap")


def make_print_bundle():
    children = []
    for shape, x, label in (
        (print_outer_housing(), -75, "outer_housing"),
        (print_hollow_keyboard_container(), -25, "integrated_inner"),
        (print_magnetic_rear_cover(), 25, "rear_cover"),
        (print_bayonet_cap(), 65, "bayonet_cap"),
    ):
        children.append(_located(shape, Location((x, 0, 0)), label))
    return Compound(children=children, label="p2_four_part_test_bundle_exactly_4_meshes")


__all__ = [name for name in globals() if name.startswith("make_") or name.startswith("print_")]
