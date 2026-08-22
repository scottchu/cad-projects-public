"""P5 minimal manually-squared slider for the frozen XT60 90-degree bend.

There are exactly three printed solids: two green L side plates and one yellow
U pusher.  The single moving Ø4 x 50 rod itself runs through an obround slot in
each green plate and a bore in each yellow arm.  The slot ends are the only
closed/open stops; no guide cheeks, anti-rack pin, secondary rail, or stop
lugs are used in this V1.
"""

from __future__ import annotations

from math import atan2, degrees, sqrt
from typing import Literal

from build123d import (
    Align,
    Box,
    BuildSketch,
    Compound,
    Cone,
    Cylinder,
    Plane,
    Polygon,
    Pos,
    Rot,
    Shape,
    extrude,
    fillet,
)
from cadgen import srgb

from xt60_bend_jig.p2_corner_clamp import (
    P2_DEFAULTS,
    P2Parameters,
    PointYZ,
    build_esc,
    build_fc,
    build_reference_rod,
    build_wires,
    build_xt60,
    contact_points,
    rod_centers,
)


Side = Literal["left", "right"]
P5_DEFAULTS = P2_DEFAULTS

CHEEK_THICKNESS = 4.0
GUIDE_CLEARANCE = 0.30
RIGHT_PLATE_X = (19.0, 23.0)
LEFT_PLATE_X = (-23.0, -19.0)
RIGHT_ARM_X = (14.7, 18.7)
LEFT_ARM_X = (-18.7, -14.7)
BORE_CHAMFER = 0.4
BORE_MOUTH_DIAMETER = P5_DEFAULTS.rod_bore_diameter + 2.0 * BORE_CHAMFER

MOVING_SLOT_WIDTH = 4.5  # Ø4 rod + 0.25 mm radial running clearance.
SLOT_RADIAL_CLEARANCE = (MOVING_SLOT_WIDTH - P5_DEFAULTS.rod_diameter) / 2.0
OPEN_STROKE = 11.0
OPEN_COMPONENT = OPEN_STROKE / sqrt(2.0)


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def _x_cylinder(diameter: float, length: float, x: float, y: float, z: float) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _extrude_yz_profile(sketch: Shape, center_x: float, thickness: float) -> Shape:
    return Pos(center_x, 0.0, 0.0) * extrude(sketch, thickness / 2.0, both=True)


def _x_chamfered_bore(center_x: float, point: PointYZ, params: P2Parameters = P5_DEFAULTS) -> Shape:
    half = CHEEK_THICKNESS / 2.0
    land = _x_cylinder(params.rod_bore_diameter, CHEEK_THICKNESS + 2.0, center_x, point.y, point.z)
    left = Pos(center_x - half + BORE_CHAMFER / 2.0, point.y, point.z) * Cone(
        BORE_MOUTH_DIAMETER / 2.0, params.rod_bore_diameter / 2.0, BORE_CHAMFER,
        rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    right = Pos(center_x + half - BORE_CHAMFER / 2.0, point.y, point.z) * Cone(
        BORE_MOUTH_DIAMETER / 2.0, params.rod_bore_diameter / 2.0, BORE_CHAMFER,
        rotation=(0, -90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return land + left + right


def _capsule_yz(start: PointYZ, end: PointYZ, width: float, center_x: float, thickness: float) -> Shape:
    """A true obround through-X slot or its enclosing single web."""

    dy, dz = end.y - start.y, end.z - start.z
    length = sqrt(dy * dy + dz * dz)
    angle = degrees(atan2(dz, dy))
    middle = PointYZ((start.y + end.y) / 2.0, (start.z + end.z) / 2.0)
    spine = Pos(center_x, middle.y, middle.z) * Rot(angle, 0.0, 0.0) * Box(
        thickness, length, width, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    return spine + _x_cylinder(width, thickness, center_x, start.y, start.z) + _x_cylinder(width, thickness, center_x, end.y, end.z)


def _fixed_L_profile() -> Shape:
    """The visible lower-left right angle; only free corners are rounded."""

    # Vertical arm reaches Y=18 so the full 45-degree moving-slot envelope
    # has 3.28 mm of outer material remaining. It is still one plain L.
    points = [(-12.0, 20.0), (25.0, 20.0), (25.0, 30.0), (18.0, 30.0), (18.0, 55.0), (-12.0, 55.0)]
    rounded = {(-12.0, 20.0), (25.0, 20.0), (25.0, 30.0), (18.0, 55.0), (-12.0, 55.0)}
    with BuildSketch(Plane.YZ) as profile:
        Polygon(*points)
        vertices = [v for v in profile.vertices() if (round(v.X, 7), round(v.Y, 7)) in rounded]
        fillet(vertices, radius=3.0)
    return profile.sketch


def _yellow_arm_profile() -> Shape:
    """R3 inside wire relief plus R2 root blend; no functional stop faces."""

    points = [(0.0, 30.0), (14.0, 30.0), (14.0, 50.0), (10.0, 50.0), (10.0, 40.0), (0.0, 40.0)]
    with BuildSketch(Plane.YZ) as profile:
        Polygon(*points)
        relief = [v for v in profile.vertices() if abs(v.X) <= 1e-9 and abs(v.Y - 30.0) <= 1e-9]
        fillet(relief, radius=3.0)
        root = [v for v in profile.vertices() if abs(v.X - 10.0) <= 1e-9 and abs(v.Y - 40.0) <= 1e-9]
        fillet(root, radius=2.0)
    return profile.sketch


def _cap() -> Shape:
    """Remote R1-bottomed hand-push crossbar, not a separate handle part."""

    with BuildSketch(Plane.YZ) as profile:
        Polygon((10.0, 47.5), (18.0, 47.5), (18.0, 53.5), (10.0, 53.5))
        lower = [v for v in profile.vertices() if round(v.Y, 7) == 47.5]
        fillet(lower, radius=1.0)
    return _extrude_yz_profile(profile.sketch, 0.0, 37.4)


def slot_endpoints(params: P2Parameters = P5_DEFAULTS) -> tuple[PointYZ, PointYZ]:
    """Cutter-circle centers; the rod contacts them at the exact 11 mm stops."""

    moving = rod_centers(params)["moving"]
    # The capsule's end-circle centers are *inside* the two rod center stops
    # by δ. The Ø4 rod then contacts the Ø4.5 slot at travel 0 / 11 exactly.
    low = PointYZ(
        moving.y + SLOT_RADIAL_CLEARANCE / sqrt(2.0),
        moving.z + SLOT_RADIAL_CLEARANCE / sqrt(2.0),
    )
    high = PointYZ(
        moving.y + OPEN_COMPONENT - SLOT_RADIAL_CLEARANCE / sqrt(2.0),
        moving.z + OPEN_COMPONENT - SLOT_RADIAL_CLEARANCE / sqrt(2.0),
    )
    return low, high


def moving_center(travel: float = 0.0, params: P2Parameters = P5_DEFAULTS) -> PointYZ:
    if not -1e-9 <= travel <= OPEN_STROKE + 1e-9:
        raise ValueError("travel is physically bounded by the 0 to 11 mm slot stops")
    point = rod_centers(params)["moving"]
    d = travel / sqrt(2.0)
    return PointYZ(point.y + d, point.z + d)


def build_fixed_plate(side: Side, params: P2Parameters = P5_DEFAULTS) -> Shape:
    """A plain green L with two fixed bores and one required moving slot."""

    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    x = -21.0 if side == "left" else 21.0
    plate = _extrude_yz_profile(_fixed_L_profile(), x, CHEEK_THICKNESS)
    for name in ("left", "bottom"):
        plate -= _x_chamfered_bore(x, rod_centers(params)[name], params)
    low, high = slot_endpoints(params)
    plate -= _capsule_yz(low, high, MOVING_SLOT_WIDTH, x, CHEEK_THICKNESS + 2.0)
    return _label(
        plate,
        f"{side}_plain_green_right_angle_plate_two_fixed_bores_one_45deg_obround_slot",
        "#3F6B4F",
    )


def build_pusher(params: P2Parameters = P5_DEFAULTS) -> Shape:
    """One yellow U: two arms, a crossbar, and only the moving-rod bores."""

    moving = rod_centers(params)["moving"]
    arms: list[Shape] = []
    for x in (-16.7, 16.7):
        arm = _extrude_yz_profile(_yellow_arm_profile(), x, CHEEK_THICKNESS)
        arms.append(arm - _x_chamfered_bore(x, moving, params))
    return _label(
        arms[0] + arms[1] + _cap(),
        "yellow_simple_U_pusher_manually_squared_no_antirack_hardware",
        "#E0A323",
    )


def build_moving_rod(travel: float = 0.0, params: P2Parameters = P5_DEFAULTS) -> Shape:
    return _label(
        build_reference_rod("moving_slot", moving_center(travel, params), params),
        "user_4x50_moving_rod_through_two_slots_and_two_U_arms_2mm_projection",
        "#C9D0D4",
    )


def build_rods(travel: float = 0.0, params: P2Parameters = P5_DEFAULTS) -> Compound:
    centers = rod_centers(params)
    return Compound(
        children=[
            build_reference_rod("left", centers["left"], params),
            build_reference_rod("bottom", centers["bottom"], params),
            build_moving_rod(travel, params),
        ],
        label="reference_exactly_three_user_4x50_rods",
    )


def build_loaded(travel: float = 0.0, params: P2Parameters = P5_DEFAULTS) -> Compound:
    d = travel / sqrt(2.0)
    pusher = Pos(0.0, d, d) * build_pusher(params)
    pusher.label = f"yellow_simple_U_pusher_manual_square_travel_{travel:.3f}mm"
    return Compound(
        children=[
            build_fixed_plate("left", params),
            build_fixed_plate("right", params),
            pusher,
            build_rods(travel, params),
            build_esc(params),
            build_fc(params),
            build_wires(params),
            build_xt60(params),
        ],
        label=f"p5_simple_slider_loaded_{travel:.3f}mm",
    )


def build_loaded_closed(params: P2Parameters = P5_DEFAULTS) -> Compound:
    return build_loaded(0.0, params)


def build_loaded_mid(params: P2Parameters = P5_DEFAULTS) -> Compound:
    return build_loaded(OPEN_STROKE / 2.0, params)


def build_loaded_open(params: P2Parameters = P5_DEFAULTS) -> Compound:
    return build_loaded(OPEN_STROKE, params)


def build_release_open(params: P2Parameters = P5_DEFAULTS) -> Compound:
    d = OPEN_COMPONENT
    pusher = Pos(0.0, d, d) * build_pusher(params)
    pusher.label = "yellow_simple_U_pusher_release_open_workpiece_removed"
    return Compound(
        children=[
            build_fixed_plate("left", params),
            build_fixed_plate("right", params),
            pusher,
            build_rods(OPEN_STROKE, params),
        ],
        label="p5_simple_slider_release_open_workpiece_removed",
    )


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation is not None else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P2Parameters = P5_DEFAULTS) -> Compound:
    left = _on_bed(build_fixed_plate("left", params), 0.0, 0.0, Rot(0, 90, 0))
    left.label = "print_left_plain_green_right_angle_slot_plate"
    right = _on_bed(build_fixed_plate("right", params), 55.0, 0.0, Rot(0, 90, 0))
    right.label = "print_right_plain_green_right_angle_slot_plate"
    pusher = _on_bed(build_pusher(params), 115.0, 0.0, Rot(180, 0, 0))
    pusher.label = "print_yellow_simple_U_pusher"
    return Compound(
        children=[left, right, pusher],
        label="p5_print_kit_exactly_three_printed_solids",
    )


__all__ = [
    "BORE_CHAMFER", "BORE_MOUTH_DIAMETER", "GUIDE_CLEARANCE", "MOVING_SLOT_WIDTH",
    "OPEN_COMPONENT", "OPEN_STROKE", "P5_DEFAULTS", "SLOT_RADIAL_CLEARANCE",
    "build_fixed_plate", "build_loaded", "build_loaded_closed", "build_loaded_mid",
    "build_loaded_open", "build_moving_rod", "build_print_kit", "build_pusher",
    "build_release_open", "build_rods", "contact_points", "moving_center", "rod_centers",
    "slot_endpoints",
]
