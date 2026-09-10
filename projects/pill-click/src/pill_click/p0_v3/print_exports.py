"""Print-pose transforms and plate layout derived from accepted P0 V3 solids.

This module must not remodel accepted geometry.  It only applies rigid-body
rotations/translations to the canonical constructors in :mod:`pill_click.p0_v3`.
"""

from collections.abc import Callable

from build123d import Compound, Location, Shape

from .coupons import (
    make_c1r1_rail_coupon,
    make_c2_legacy_rail_coupon,
    make_c4_snap_coupon,
    make_shutter_track_coupon,
)
from .geometry import (
    make_blind_rear_cover,
    make_bottom_shutter,
    make_housing,
    make_shuttle,
    make_top_shutter,
)


def _located(shape: Shape, location: Location, label: str) -> Shape:
    """Apply a location to leaves so XCAF assembly exporters preserve it."""

    if shape.children:
        children = []
        for child in shape.children:
            cleaned_child = (location * child).clean()
            cleaned_child.label = child.label
            children.append(cleaned_child)
        result = Compound(children=children, label=label)
    else:
        # ``clean`` removes coincident tessellation seams/splitters only.  It
        # has zero BREP symmetric difference and preserves volume/solids; this
        # makes the derived STL substantially friendlier to manifold checkers.
        result = (location * shape).clean()
        result.label = label
    return result


def _on_bed(shape: Shape, rotation: tuple[float, float, float], label: str) -> Shape:
    """Apply a rigid print rotation and translate the lowest point to Z=0."""

    rotation_location = Location((0.0, 0.0, 0.0), rotation)
    oriented = _located(shape, rotation_location, label)
    bed_location = Location((0.0, 0.0, -oriented.bounding_box().min.Z))
    return _located(oriented, bed_location, label)


def print_housing() -> Shape:
    # Front keyboard-key face on the bed; rear assembly opening points upward.
    return _on_bed(make_housing(), (-90.0, 0.0, 0.0), "P0_V3_housing_print_pose")


def print_inner_medicine_shuttle() -> Shape:
    # Key face on the bed; the medicine cavity grows upward without internal support.
    return _on_bed(
        make_shuttle(),
        (-90.0, 0.0, 0.0),
        "P0_V3_inner_medicine_shuttle_print_pose",
    )


def print_top_shutter() -> Shape:
    # Broad exterior web face on the bed.
    return _on_bed(make_top_shutter(), (180.0, 0.0, 0.0), "P0_V3_top_shutter_print_pose")


def print_bottom_shutter() -> Shape:
    # Broad exterior web face is already the lowest face.
    return _on_bed(make_bottom_shutter(), (0.0, 0.0, 0.0), "P0_V3_bottom_shutter_print_pose")


def print_rear_cover() -> Shape:
    # Full blind exterior face on the bed; pilot, stops, and snap arms point upward.
    return _on_bed(make_blind_rear_cover(), (90.0, 0.0, 0.0), "P0_V3_rear_cover_print_pose")


def _print_strengthened_rail_coupon(*, thick_lip: bool) -> Shape:
    coupon = make_c1r1_rail_coupon(thick_lip=thick_lip)
    rail, receiver = coupon.children
    # Orient each functional opening upward: negative-X rail tip upward and
    # positive-X receiver groove upward. The opposed rotations are required.
    rail = _on_bed(rail, (0.0, 90.0, 0.0), rail.label)
    receiver = _on_bed(receiver, (0.0, -90.0, 0.0), receiver.label)
    receiver = _located(receiver, Location((9.0, 0.0, 0.0)), receiver.label)
    label = (
        "P0_V3_C1R1B_nominal_L6p80_lip1p20_print_pair"
        if thick_lip
        else "P0_V3_C1R1_nominal_L6p80_lip0p80_print_pair"
    )
    return Compound(children=[rail, receiver], label=label)


def print_c1r1_nominal_lip0p80_coupon() -> Shape:
    return _print_strengthened_rail_coupon(thick_lip=False)


def print_c1r1b_nominal_lip1p20_coupon() -> Shape:
    return _print_strengthened_rail_coupon(thick_lip=True)


def print_c2_loose_rail_coupon() -> Shape:
    return _on_bed(
        make_c2_legacy_rail_coupon(),
        (0.0, 0.0, 0.0),
        "P0_V3_C2_loose_original_L3p40_print_pair",
    )


def print_c3_shutter_track_coupon() -> Shape:
    return _on_bed(make_shutter_track_coupon(), (0.0, 0.0, 0.0), "C3_shutter_track_coupon")


def print_c4_rear_snap_coupon() -> Shape:
    coupon = make_c4_snap_coupon()
    arm, receiver = coupon.children
    receiver = Location((8.0, 0.0, 0.0)) * receiver
    receiver.label = "C4_receiver_blind_pocket_outer_skin_1p20"
    # The accepted coupon is modeled in its mating pose.  Separate the two
    # unchanged solids on the print plate so a slicer cannot fuse their
    # zero-clearance contact faces.
    separated = Compound(children=[arm, receiver], label="C4_rear_snap_coupon_separated")
    return _on_bed(separated, (0.0, 0.0, 0.0), "C4_rear_snap_coupon")


PRINT_ITEM_FACTORIES: dict[str, Callable[[], Shape]] = {
    "housing": print_housing,
    "inner_medicine_shuttle": print_inner_medicine_shuttle,
    "top_shutter": print_top_shutter,
    "bottom_shutter": print_bottom_shutter,
    "rear_cover": print_rear_cover,
    "c1r1_nominal_L6p80_lip0p80_coupon": print_c1r1_nominal_lip0p80_coupon,
    "c1r1b_nominal_L6p80_lip1p20_coupon": print_c1r1b_nominal_lip1p20_coupon,
    "c2_loose_original_L3p40_coupon": print_c2_loose_rail_coupon,
    "c3_shutter_track_coupon": print_c3_shutter_track_coupon,
    "c4_rear_snap_coupon": print_c4_rear_snap_coupon,
}


# Centers on a 220 x 220 mm test plate.  Every item remains a separately named
# assembly occurrence in the STEP/3MF hierarchy; no sacrificial plate is added.
PRINT_PLATE_CENTERS: dict[str, tuple[float, float]] = {
    "housing": (-80.0, -75.0),
    "inner_medicine_shuttle": (-25.0, -75.0),
    "rear_cover": (30.0, -75.0),
    "c3_shutter_track_coupon": (80.0, -75.0),
    "top_shutter": (-80.0, -20.0),
    "bottom_shutter": (-40.0, -15.0),
    "c1r1_nominal_L6p80_lip0p80_coupon": (-8.0, -15.0),
    "c1r1b_nominal_L6p80_lip1p20_coupon": (11.0, -15.0),
    "c2_loose_original_L3p40_coupon": (28.0, -15.0),
    "c4_rear_snap_coupon": (46.0, -15.0),
}


def make_p0_v3_print_bundle() -> Compound:
    children = []
    for name, factory in PRINT_ITEM_FACTORIES.items():
        x, y = PRINT_PLATE_CENTERS[name]
        child = _located(factory(), Location((x, y, 0.0)), name)
        children.append(child)
    return Compound(children=children, label="P0_V3_C1R1_print_test_bundle_10_groups_15_solids")


__all__ = [
    "PRINT_ITEM_FACTORIES",
    "PRINT_PLATE_CENTERS",
    "make_p0_v3_print_bundle",
    "print_bottom_shutter",
    "print_c1r1_nominal_lip0p80_coupon",
    "print_c1r1b_nominal_lip1p20_coupon",
    "print_c2_loose_rail_coupon",
    "print_c3_shutter_track_coupon",
    "print_c4_rear_snap_coupon",
    "print_housing",
    "print_inner_medicine_shuttle",
    "print_rear_cover",
    "print_top_shutter",
]
