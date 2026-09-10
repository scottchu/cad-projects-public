"""Exact two-specimen C5 side-latch coupon derived from V2 production geometry."""

from build123d import Compound

from .geometry import (
    _box_bounds,
    make_blind_two_side_latch_rear_cover,
    make_outer_housing,
)
from .spec import P0_MECHANICAL_FIT_V2, P0MechanicalFitV2Spec


def make_c5_arm_cover_specimen(
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
):
    crop = _box_bounds(
        (14.0, 20.1),
        (p.rear_faceplate_exterior_y - 0.1, p.side_latch_beam_y[1] + 0.1),
        (-6.0, 6.0),
    )
    specimen = (make_blind_two_side_latch_rear_cover(p) & crop).clean()
    specimen.label = "C5_V2_side_latch_arm_cover_specimen"
    return specimen


def make_c5_housing_receiver_specimen(
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
):
    crop = _box_bounds(
        (16.5, 20.1),
        (p.housing_rear_y - 0.1, p.side_latch_forward_beam_passage_y[1] + 0.1),
        (-6.0, 6.0),
    )
    specimen = (make_outer_housing(p) & crop).clean()
    specimen.label = "C5_V2_side_latch_housing_receiver_specimen"
    return specimen


def make_c5_coupon_assembly(
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Compound:
    return Compound(
        children=[
            make_c5_arm_cover_specimen(p),
            make_c5_housing_receiver_specimen(p),
        ],
        label="C5_V2_one_side_latch_pad_notch_coupon_two_part_assembly",
    )


__all__ = [
    "make_c5_arm_cover_specimen",
    "make_c5_coupon_assembly",
    "make_c5_housing_receiver_specimen",
]
