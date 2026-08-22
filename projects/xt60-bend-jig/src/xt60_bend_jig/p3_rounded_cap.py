"""P3 rounded push-cap refinement of the preserved P2 mechanism.

Only the printed side-profile language and synchronized crossbridge are
refined here.  The P2 wire path, rods, contacts, stop datums, and 45-degree
travel remain the mechanical source of truth.

Axes: rods run on X, Y points right toward the ESC, and Z points up.
"""

from __future__ import annotations

from typing import Literal

from build123d import (
    Align,
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
    build_rods,
    build_wires,
    build_xt60,
    contact_points,
    rod_centers,
)


Side = Literal["left", "right"]
P3_DEFAULTS = P2_DEFAULTS
BORE_CHAMFER = 0.4
BORE_MOUTH_DIAMETER = P3_DEFAULTS.rod_bore_diameter + 2.0 * BORE_CHAMFER


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def _extrude_yz_profile(sketch: Shape, center_x: float, thickness: float) -> Shape:
    return Pos(center_x, 0.0, 0.0) * extrude(sketch, thickness / 2.0, both=True)


def _rounded_green_profile() -> Shape:
    """Rounded free outline with the functional (Y=0,Z=30) corner sharp."""

    points = [(-12.0, 20.0), (25.0, 20.0), (25.0, 30.0), (0.0, 30.0), (0.0, 55.0), (-12.0, 55.0)]
    rounded = {(-12.0, 20.0), (25.0, 20.0), (25.0, 30.0), (0.0, 55.0), (-12.0, 55.0)}
    with BuildSketch(Plane.YZ) as profile:
        Polygon(*points)
        vertices = [
            vertex
            for vertex in profile.vertices()
            if (round(vertex.X, 7), round(vertex.Y, 7)) in rounded
        ]
        fillet(vertices, radius=3.0)
    return profile.sketch


def _rounded_yellow_tab_profile() -> Shape:
    """Compact L with an exact R3 mating relief and R2 free root blend."""

    points = [(0.0, 30.0), (14.0, 30.0), (14.0, 50.0), (10.0, 50.0), (10.0, 40.0), (0.0, 40.0)]
    with BuildSketch(Plane.YZ) as profile:
        Polygon(*points)
        mating = [
            vertex
            for vertex in profile.vertices()
            if abs(vertex.X) <= 1e-9 and abs(vertex.Y - 30.0) <= 1e-9
        ]
        fillet(mating, radius=3.0)
        elbow = [
            vertex
            for vertex in profile.vertices()
            if abs(vertex.X - 10.0) <= 1e-9 and abs(vertex.Y - 40.0) <= 1e-9
        ]
        fillet(elbow, radius=2.0)
    return profile.sketch


def _rounded_cap_profile() -> Shape:
    """46 mm cap cross-section with R1 lower free corners and a flat top."""

    points = [(10.0, 44.0), (18.0, 44.0), (18.0, 50.0), (10.0, 50.0)]
    with BuildSketch(Plane.YZ) as profile:
        Polygon(*points)
        lower = [
            vertex
            for vertex in profile.vertices()
            if round(vertex.Y, 7) == 44.0
        ]
        fillet(lower, radius=1.0)
    return profile.sketch


def _x_cylinder(diameter: float, length: float, x: float, y: float, z: float) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _x_chamfered_bore(
    center_x: float,
    center: PointYZ,
    params: P2Parameters = P3_DEFAULTS,
) -> Shape:
    """Ø4.3 through bore plus constructive 0.4 x 45-degree mouth cones."""

    half = params.plate_thickness / 2.0
    chamfer = BORE_CHAMFER
    land = _x_cylinder(
        params.rod_bore_diameter,
        params.plate_thickness + 2.0,
        center_x,
        center.y,
        center.z,
    )
    left = Pos(center_x - half + chamfer / 2.0, center.y, center.z) * Cone(
        BORE_MOUTH_DIAMETER / 2.0,
        params.rod_bore_diameter / 2.0,
        chamfer,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    right = Pos(center_x + half - chamfer / 2.0, center.y, center.z) * Cone(
        BORE_MOUTH_DIAMETER / 2.0,
        params.rod_bore_diameter / 2.0,
        chamfer,
        rotation=(0, -90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return land + left + right


def build_fixed_plate(side: Side, params: P2Parameters = P3_DEFAULTS) -> Shape:
    """Rounded fixed L; both stop planes remain sharp and datum-driven."""

    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.plate_center_x
    plate = _extrude_yz_profile(_rounded_green_profile(), x, params.plate_thickness)
    centers = rod_centers(params)
    bores = _x_chamfered_bore(x, centers["left"], params) + _x_chamfered_bore(
        x, centers["bottom"], params
    )
    return _label(
        plate - bores,
        f"{side}_rounded_fixed_L_sharp_Y0_Z30_stops_two_chamfered_4p3_bores",
        "#3F6B4F",
    )


def build_push_cap(params: P2Parameters = P3_DEFAULTS) -> Shape:
    """Remote 46 x 8 x 6 synchronized load-spreading crossbridge."""

    return _label(
        _extrude_yz_profile(_rounded_cap_profile(), 0.0, params.outer_span),
        "synchronized_push_cap_crossbridge_not_a_handle",
        "#E0A323",
    )


def build_pusher(params: P2Parameters = P3_DEFAULTS) -> Shape:
    """Two rounded tabs synchronized by a broad remote push cap.

    The yellow span is a synchronized push cap/crossbridge, not a handle.  It
    remains remote from the wires; only the 4 mm steel forming rod contacts
    them.
    """

    moving = rod_centers(params)["moving"]
    tab_profile = _rounded_yellow_tab_profile()
    tabs: list[Shape] = []
    for sign in (-1.0, 1.0):
        x = sign * params.plate_center_x
        tab = _extrude_yz_profile(tab_profile, x, params.plate_thickness)
        tab -= _x_chamfered_bore(x, moving, params)
        tabs.append(tab)

    cap = build_push_cap(params)
    return _label(
        cap + tabs,
        "synchronized_push_cap_crossbridge_not_a_handle_one_piece_pusher",
        "#E0A323",
    )


def build_loaded_closed(params: P2Parameters = P3_DEFAULTS) -> Compound:
    return Compound(
        children=[
            build_fixed_plate("left", params),
            build_fixed_plate("right", params),
            build_pusher(params),
            build_rods(params=params),
            build_esc(params),
            build_fc(params),
            build_wires(params),
            build_xt60(params),
        ],
        label="p3_rounded_cap_closed_frozen_P2_mechanics_no_actuation",
    )


def build_loaded_open(params: P2Parameters = P3_DEFAULTS) -> Compound:
    d = params.withdrawal_component
    pusher = Pos(0.0, d, d) * build_pusher(params)
    pusher.label = "synchronized_push_cap_open_11mm_45deg_no_actuation"
    return Compound(
        children=[
            build_fixed_plate("left", params),
            build_fixed_plate("right", params),
            pusher,
            build_rods(params.moving_open, params),
            build_esc(params),
            build_fc(params),
            build_wires(params),
            build_xt60(params),
        ],
        label="p3_rounded_cap_open_frozen_P2_mechanics_no_actuation",
    )


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation is not None else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P2Parameters = P3_DEFAULTS) -> Compound:
    left = _on_bed(build_fixed_plate("left", params), 0.0, 0.0, Rot(0, 90, 0))
    left.label = "print_left_rounded_fixed_L"
    right = _on_bed(build_fixed_plate("right", params), 50.0, 0.0, Rot(0, 90, 0))
    right.label = "print_right_rounded_fixed_L"
    pusher = _on_bed(build_pusher(params), 100.0, 0.0, Rot(180, 0, 0))
    pusher.label = "print_synchronized_push_cap_not_handle"
    return Compound(
        children=[left, right, pusher],
        label="p3_rounded_cap_print_kit_exactly_three_solids",
    )


__all__ = [
    "BORE_CHAMFER",
    "BORE_MOUTH_DIAMETER",
    "P3_DEFAULTS",
    "build_fixed_plate",
    "build_loaded_closed",
    "build_loaded_open",
    "build_print_kit",
    "build_push_cap",
    "build_pusher",
    "contact_points",
    "rod_centers",
]
