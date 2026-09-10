"""Faithful physical C1-C4 interface coupons for P0 v3."""

from dataclasses import dataclass

from build123d import (
    BuildSketch,
    Compound,
    Location,
    Plane,
    Polygon,
    Rectangle,
    extrude,
    loft,
)

from .geometry import (
    _box,
    _box_bounds,
    _box_between_y,
    _make_snap_root_prism,
)
from .spec import P0V3, P0V3Spec


@dataclass(frozen=True)
class RailCouponVariant:
    """Versioned rail-coupon geometry; IDs are physical-test identities."""

    coupon_id: str
    rail_length: float
    land_length: float
    bearing_boss_width: float
    groove_width: float
    groove_bottom_x: float

    @property
    def mouth_bottom_x(self) -> float:
        return self.groove_bottom_x - P0V3.groove_mouth_extra_depth


C1R1 = RailCouponVariant(
    coupon_id="P0_V3_C1R1_nominal_L6p80_lip0p80",
    rail_length=22.4,
    land_length=6.8,
    bearing_boss_width=4.3,
    groove_width=2.7,
    groove_bottom_x=-1.4,
)
C1R1B = RailCouponVariant(
    coupon_id="P0_V3_C1R1B_nominal_L6p80_lip1p20",
    rail_length=22.4,
    land_length=6.8,
    bearing_boss_width=5.1,
    groove_width=2.7,
    groove_bottom_x=-1.4,
)
C2_LEGACY = RailCouponVariant(
    coupon_id="P0_V3_C2_loose_original_L3p40",
    rail_length=19.0,
    land_length=3.4,
    bearing_boss_width=3.5,
    groove_width=2.8,
    groove_bottom_x=-1.5,
)


def _coupon_rail(p: P0V3Spec, variant: RailCouponVariant) -> object:
    carrier = _box_bounds((0.0, 2.0), (0.0, variant.rail_length), (-3.5, 3.5))
    profile = Polygon(
        (0.0, 0.0),
        (-p.rail_radial_height, p.rail_rear_lead_in),
        (-p.rail_radial_height, variant.rail_length),
        (0.0, variant.rail_length),
    )
    rail = extrude(profile, 2.2)
    bbox = rail.bounding_box()
    rail = rail.moved(Location((0.0, 0.0, -sum((bbox.min.Z, bbox.max.Z)) / 2)))
    result = carrier + rail
    result.label = f"{variant.coupon_id}__fixed_rail_carrier_lead_in_0p70"
    return result


def _coupon_rail_receiver(*, variant: RailCouponVariant, p: P0V3Spec) -> object:
    half_length = variant.land_length / 2
    half_boss = variant.bearing_boss_width / 2
    # The contacting boss is exact. Handling wings remain behind X=-1.55 and
    # outside its Z envelope, so they cannot alter the rail interface.
    receiver = _box_bounds(
        (-3.4, -0.75),
        (-half_length, half_length),
        (-half_boss, half_boss),
    )
    receiver = receiver + _box_bounds(
        (-3.4, -1.55),
        (-half_length, half_length),
        (half_boss, 3.5),
    )
    receiver = receiver + _box_bounds(
        (-3.4, -1.55),
        (-half_length, half_length),
        (-3.5, -half_boss),
    )
    receiver = receiver - _box_bounds(
        (variant.groove_bottom_x, -0.65),
        (-half_length - 0.01, half_length + 0.01),
        (-variant.groove_width / 2, variant.groove_width / 2),
    )
    receiver = receiver - _box_bounds(
        (variant.mouth_bottom_x, -0.65),
        (half_length - p.groove_mouth_length, half_length + 0.01),
        (
            -(variant.groove_width + p.groove_mouth_extra_width) / 2,
            (variant.groove_width + p.groove_mouth_extra_width) / 2,
        ),
    )
    receiver.label = f"{variant.coupon_id}__receiver_positive_Y_mouth"
    return receiver


def _make_rail_coupon(variant: RailCouponVariant, p: P0V3Spec) -> Compound:
    rail = _coupon_rail(p, variant)
    receiver = _coupon_rail_receiver(variant=variant, p=p)
    return Compound(children=[rail, receiver], label=variant.coupon_id)


def make_c1r1_rail_coupon(
    *,
    thick_lip: bool = False,
    p: P0V3Spec = P0V3,
) -> Compound:
    """Strengthened nominal coupon; ``thick_lip`` selects C1R1B."""

    return _make_rail_coupon(C1R1B if thick_lip else C1R1, p)


def make_c2_legacy_rail_coupon(p: P0V3Spec = P0V3) -> Compound:
    """Preserved original C2 loose-clearance diagnostic coupon."""

    return _make_rail_coupon(C2_LEGACY, p)


def make_rail_coupon(
    loose: bool = False,
    p: P0V3Spec = P0V3,
    *,
    thick_lip: bool = False,
) -> Compound:
    """Compatibility dispatcher for the strengthened nominal or legacy C2."""

    if loose:
        if thick_lip:
            raise ValueError("C1R1B is nominal-only; C2 remains unchanged")
        return make_c2_legacy_rail_coupon(p)
    return make_c1r1_rail_coupon(thick_lip=thick_lip, p=p)


def _c3_track_receiver(p: P0V3Spec) -> object:
    receiver = _box_bounds((-15.9, 15.9), (0.0, 32.0), (-2.0, 2.0))
    receiver = receiver - _box_bounds((-13.9, 13.9), (-0.01, 32.01), (0.0, 1.2))
    receiver = receiver - _box_bounds((-12.7, 12.7), (-0.01, 32.01), (1.2, 2.01))
    # Fixed negative-Y mouth: +0.40 total width and +0.20 height.
    receiver = receiver - _box_bounds((-14.1, 14.1), (-0.01, 0.8), (-0.2, 1.4))
    receiver = receiver - _box_bounds((-12.9, 12.9), (-0.01, 0.8), (1.0, 2.01))
    receiver.label = "C3_captured_track_receiver_negative_Y_mouth"
    return receiver


def _c3_slider(p: P0V3Spec) -> object:
    web = _box_bounds((-12.5, 12.5), (-6.0, 6.0), (1.0, 1.8))
    full = _box_bounds((-13.7, 13.7), (-6.0, 5.2), (0.2, 1.0))
    full_section = Rectangle(27.4, 0.8).moved(
        Location((0.0, 5.2, 0.6), (90.0, 0.0, 0.0))
    )
    tip_section = Rectangle(25.0, 0.4).moved(
        Location((0.0, 6.0, 0.8), (90.0, 0.0, 0.0))
    )
    slider = web + full + loft([full_section, tip_section])
    slider.label = "C3_solid_shutter_slider_positive_Y_lead"
    return slider


def make_shutter_track_coupon(p: P0V3Spec = P0V3) -> Compound:
    return Compound(
        children=[_c3_track_receiver(p), _c3_slider(p)],
        label="p0_v3_C3_captured_shutter_track",
    )


def make_c4_snap_arm(p: P0V3Spec = P0V3) -> object:
    arm = _make_c4_snap_arm_rootless(p) + _make_snap_root_prism(p)
    arm = arm.clean()
    arm.label = "C4_reversible_snap_arm_V3p1_exact_R0p80"
    return arm


def _make_c4_snap_arm_rootless(p: P0V3Spec = P0V3) -> object:
    """V3.1 accounting baseline: grip, straight beam, and hook only."""

    grip = _box_bounds((-2.0, 1.2), (-3.0, 0.0), (-6.0, 6.0))
    beam = _box_bounds((0.0, 1.2), (0.0, 8.85), (-1.8, 1.8))
    with BuildSketch(Plane.XY) as hook_profile:
        Polygon((1.2, 7.75), (1.75, 8.30), (1.2, 8.85))
    hook = extrude(hook_profile.sketch, 3.6).moved(Location((0.0, 0.0, -1.8)))
    arm = (grip + beam + hook).clean()
    arm.label = "C4_reversible_snap_arm_V3p1_rootless_baseline"
    return arm


def make_c4_snap_receiver(p: P0V3Spec = P0V3) -> object:
    receiver = _box_bounds((1.2, 3.05), (0.0, 10.5), (-6.0, 6.0))
    receiver = receiver - _box_bounds((1.19, 1.85), (7.75, 8.85), (-2.0, 2.0))
    receiver.label = "C4_receiver_blind_pocket_outer_skin_1p20"
    return receiver


def make_c4_snap_coupon(p: P0V3Spec = P0V3) -> Compound:
    return Compound(
        children=[make_c4_snap_arm(p), make_c4_snap_receiver(p)],
        label="p0_v3_C4_one_arm_reversible_snap",
    )


__all__ = [
    "C1R1",
    "C1R1B",
    "C2_LEGACY",
    "RailCouponVariant",
    "make_c4_snap_arm",
    "make_c4_snap_coupon",
    "make_c4_snap_receiver",
    "make_c1r1_rail_coupon",
    "make_c2_legacy_rail_coupon",
    "make_rail_coupon",
    "make_shutter_track_coupon",
]
