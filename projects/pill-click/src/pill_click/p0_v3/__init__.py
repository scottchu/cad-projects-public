"""P0 v3 printable solid shutters, rear closeout, and faithful coupons."""

from .assembly import make_p0_v3_assembly, placed_moving_parts
from .coupons import (
    C1R1,
    C1R1B,
    C2_LEGACY,
    make_c4_snap_arm,
    make_c4_snap_coupon,
    make_c4_snap_receiver,
    make_c1r1_rail_coupon,
    make_c2_legacy_rail_coupon,
    make_rail_coupon,
    make_shutter_track_coupon,
)
from .geometry import (
    make_blind_rear_cover,
    make_bottom_shutter,
    make_housing,
    make_shuttle,
    make_top_shutter,
)
from .spec import P0V3, P0V3Spec

__all__ = [
    "C1R1",
    "C1R1B",
    "C2_LEGACY",
    "P0V3",
    "P0V3Spec",
    "make_blind_rear_cover",
    "make_bottom_shutter",
    "make_c4_snap_arm",
    "make_c4_snap_coupon",
    "make_c4_snap_receiver",
    "make_c1r1_rail_coupon",
    "make_c2_legacy_rail_coupon",
    "make_housing",
    "make_p0_v3_assembly",
    "make_rail_coupon",
    "make_shutter_track_coupon",
    "make_shuttle",
    "make_top_shutter",
    "placed_moving_parts",
]
