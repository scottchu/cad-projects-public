"""P4: captured 45-degree sliding carriage for the frozen P2 wire bend.

The two green side plates are now full-thickness guide cheeks.  The yellow
one-piece carriage lives *between* them with 0.30 mm side clearance.  Its
forming rod travels in paired diagonal 4.5 mm slots; a separate M3 pin in the
left/master cheek prevents the cross-cap from racking.  The P2 R6 / 90-degree
wire geometry and three steel Ø4 x 50 rods remain unchanged.

Axes: rods and guide pin run on X; Y points toward the ESC; Z points upward.
"""

from __future__ import annotations

from math import atan2, degrees, sqrt
from typing import Literal

from build123d import (
    Align,
    Box,
    BuildSketch,
    Cone,
    Compound,
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
P4_DEFAULTS = P2_DEFAULTS

# The carriage shoes are deliberately inside the fixed cheeks.  In this
# layout a face-to-face 0.30 mm gap is present at either side all along travel.
GUIDE_CLEARANCE = 0.30
CHEEK_THICKNESS = 4.0
RIGHT_CHEEK_X = (19.0, 23.0)
LEFT_CHEEK_X = (-23.0, -19.0)
RIGHT_SHOE_X = (14.7, 18.7)
BORE_CHAMFER = 0.4
BORE_MOUTH_DIAMETER = P4_DEFAULTS.rod_bore_diameter + 2.0 * BORE_CHAMFER
LEFT_SHOE_X = (-18.7, -14.7)

ROD_SLOT_WIDTH_MASTER = 4.5
ROD_SLOT_WIDTH_FOLLOWER = 4.8
ROD_SLOT_CLOSED = PointYZ(4.338299064, 34.338299064)
ROD_SLOT_OPEN = PointYZ(12.823580439, 42.823580439)
M3_PIN_DIAMETER = 3.0
M3_SLOT_WIDTH = 3.5
M3_PIN_CLOSED = PointYZ(14.0, 34.0)
M3_SLOT_CLOSED = PointYZ(13.646446609, 33.646446609)
M3_SLOT_OPEN = PointYZ(22.131727984, 42.131727984)
M3_PIN_LENGTH = 9.6
M3_PIN_CENTER_X = -19.35
OPEN_STOP_STROKE = 11.0
OPEN_COMPONENT = OPEN_STOP_STROKE / sqrt(2.0)


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


def _x_chamfered_bore(center_x: float, point: PointYZ, params: P2Parameters = P4_DEFAULTS) -> Shape:
    """Ø4.3 bore with 0.4 mm x 45 degree lead-ins on both cheek faces."""

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


def _extrude_yz_profile(sketch: Shape, center_x: float, thickness: float) -> Shape:
    return Pos(center_x, 0.0, 0.0) * extrude(sketch, thickness / 2.0, both=True)


def _capsule_yz(
    start: PointYZ,
    end: PointYZ,
    width: float,
    center_x: float,
    thickness: float,
) -> Shape:
    """A through-X rounded slot / guide strip, specified in YZ coordinates."""

    dy, dz = end.y - start.y, end.z - start.z
    length = sqrt(dy * dy + dz * dz)
    angle = degrees(atan2(dz, dy))
    midpoint = PointYZ((start.y + end.y) / 2.0, (start.z + end.z) / 2.0)
    spine = Pos(center_x, midpoint.y, midpoint.z) * Rot(angle, 0.0, 0.0) * Box(
        thickness,
        length,
        width,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return (
        spine
        + _x_cylinder(width, thickness, center_x, start.y, start.z)
        + _x_cylinder(width, thickness, center_x, end.y, end.z)
    )


def _rounded_fixed_L_profile() -> Shape:
    """Base fixed lower-left L. The guide strips are fused separately."""

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


def _yellow_shoe_profile() -> Shape:
    """P3 rounded L retained; its R3 relief keeps the loaded bend uncrushed."""

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


def _guide_cheeks(center_x: float) -> Shape:
    """Two overlapping guide rails: one carries the rod slot, one the M3 slot."""

    rod_rail = _capsule_yz(PointYZ(0.0, 29.5), PointYZ(15.0, 44.5), 6.0, center_x, CHEEK_THICKNESS)
    pin_rail = _capsule_yz(PointYZ(10.0, 30.5), PointYZ(25.0, 45.5), 5.8, center_x, CHEEK_THICKNESS)
    open_support = _capsule_yz(PointYZ(20.0, 40.0), PointYZ(24.0, 51.0), 4.0, center_x, CHEEK_THICKNESS)
    return rod_rail + pin_rail + open_support


def _inward_stop_lugs(side: Side) -> Shape:
    """Green lugs project into the 0.3 mm guide gap only at the closed stop.

    They provide the two exact Y=0 and Z=30 hard-stop planes without making
    the guide cheek rub the yellow shoe while it slides.
    """

    if side == "right":
        x0, x1 = 14.55, 19.0
    elif side == "left":
        x0, x1 = -19.0, -14.55
    else:
        raise ValueError("side must be left or right")
    vertical = Pos((x0 + x1) / 2.0, -1.5, 33.0) * Box(
        x1 - x0, 3.0, 6.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    # The R3 yellow relief occupies Y=0..3 at the corner.  This horizontal
    # lug therefore starts at Y=3 and overlaps the remaining flat bottom.
    horizontal = Pos((x0 + x1) / 2.0, 4.5, 28.5) * Box(
        x1 - x0, 3.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    return vertical + horizontal


def _open_stop_lug(side: Side) -> Shape:
    """Finite inward land that catches each shoe front at exact 11 mm open."""

    if side == "right":
        x0, x1 = 14.55, 19.0
    elif side == "left":
        x0, x1 = -19.0, -14.55
    else:
        raise ValueError("side must be left or right")
    face_y = 14.0 + OPEN_COMPONENT
    # Z=44..46 is inside the open shoe front but below the raised cap's
    # swept envelope and above the M3 pin's open-path envelope (max Z 43.278).
    return Pos((x0 + x1) / 2.0, face_y + 1.5, 45.0) * Box(
        x1 - x0, 3.0, 2.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )


def _slot_for_side(side: Side, center_x: float) -> Shape:
    width = ROD_SLOT_WIDTH_MASTER if side == "left" else ROD_SLOT_WIDTH_FOLLOWER
    rod_slot = _capsule_yz(
        ROD_SLOT_CLOSED,
        ROD_SLOT_OPEN,
        width,
        center_x,
        CHEEK_THICKNESS + 2.0,
    )
    if side == "left":
        pin_slot = _capsule_yz(
            M3_SLOT_CLOSED,
            M3_SLOT_OPEN,
            M3_SLOT_WIDTH,
            center_x,
            CHEEK_THICKNESS + 2.0,
        )
        return rod_slot + pin_slot
    return rod_slot


def build_fixed_plate(side: Side, params: P2Parameters = P4_DEFAULTS) -> Shape:
    """One green full-thickness cheek with slots and inward closing lugs."""

    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    center_x = 21.0 if side == "right" else -21.0
    base = _extrude_yz_profile(_rounded_fixed_L_profile(), center_x, CHEEK_THICKNESS)
    plate = base + _guide_cheeks(center_x) + _inward_stop_lugs(side) + _open_stop_lug(side)
    centers = rod_centers(params)
    for name in ("left", "bottom"):
        point = centers[name]
        plate -= _x_chamfered_bore(center_x, point, params)
    plate -= _slot_for_side(side, center_x)
    return _label(
        plate,
        f"{side}_green_full_thickness_slider_guide_cheek_two_fixed_bores_diagonal_slot"
        + ("_M3_master_slot" if side == "left" else "_follower_slot"),
        "#3F6B4F",
    )


def _raised_cap() -> Shape:
    # User-facing load cap: it is now above the guide rail and not part of
    # the contact/stop geometry.
    with BuildSketch(Plane.YZ) as profile:
        Polygon((10.0, 47.5), (18.0, 47.5), (18.0, 53.5), (10.0, 53.5))
        lower = [vertex for vertex in profile.vertices() if round(vertex.Y, 7) == 47.5]
        fillet(lower, radius=1.0)
    return _extrude_yz_profile(profile.sketch, 0.0, 46.0)


def build_pusher(params: P2Parameters = P4_DEFAULTS) -> Shape:
    """One printed yellow carriage: two 4 mm shoes plus broad raised push cap."""

    moving = rod_centers(params)["moving"]
    shoe_profile = _yellow_shoe_profile()
    shoes: list[Shape] = []
    for side, center_x in (("left", -16.7), ("right", 16.7)):
        shoe = _extrude_yz_profile(shoe_profile, center_x, CHEEK_THICKNESS)
        shoe -= _x_chamfered_bore(center_x, moving, params)
        if side == "left":
            shoe -= _x_cylinder(M3_PIN_DIAMETER, CHEEK_THICKNESS + 2.0, center_x, M3_PIN_CLOSED.y, M3_PIN_CLOSED.z)
        shoes.append(shoe)
    return _label(
        shoes[0] + shoes[1] + _raised_cap(),
        "yellow_one_piece_captured_sliding_carriage_0p3_side_clearance_raised_push_cap",
        "#E0A323",
    )


def moving_center(travel: float = 0.0, params: P2Parameters = P4_DEFAULTS) -> PointYZ:
    if not -1e-9 <= travel <= OPEN_STOP_STROKE + 1e-9:
        raise ValueError("travel must remain between the closed and 11 mm open stops")
    d = travel / sqrt(2.0)
    closed = rod_centers(params)["moving"]
    return PointYZ(closed.y + d, closed.z + d)


def pin_center(travel: float = 0.0) -> PointYZ:
    d = travel / sqrt(2.0)
    return PointYZ(M3_PIN_CLOSED.y + d, M3_PIN_CLOSED.z + d)


def build_moving_rod(travel: float = 0.0, params: P2Parameters = P4_DEFAULTS) -> Shape:
    point = moving_center(travel, params)
    return _label(
        build_reference_rod("moving_slider", point, params),
        "user_4x50_moving_rod_2mm_outer_projection",
        "#C9D0D4",
    )


def build_m3_guide_pin(travel: float = 0.0) -> Shape:
    point = pin_center(travel)
    return _label(
        _x_cylinder(M3_PIN_DIAMETER, M3_PIN_LENGTH, M3_PIN_CENTER_X, point.y, point.z),
        "reference_M3_master_antirack_guide_pin",
        "#202326",
    )


def build_rods(travel: float = 0.0, params: P2Parameters = P4_DEFAULTS) -> Compound:
    centers = rod_centers(params)
    return Compound(
        children=[
            build_reference_rod("left", centers["left"], params),
            build_reference_rod("bottom", centers["bottom"], params),
            build_moving_rod(travel, params),
        ],
        label="reference_exactly_three_user_4x50_rods_moving_rod_in_slots",
    )


def _fixed_children(params: P2Parameters) -> list[Shape]:
    return [
        build_fixed_plate("left", params),
        build_fixed_plate("right", params),
        build_esc(params),
        build_fc(params),
        build_wires(params),
        build_xt60(params),
    ]


def build_loaded(travel: float = 0.0, params: P2Parameters = P4_DEFAULTS) -> Compound:
    d = travel / sqrt(2.0)
    pusher = Pos(0.0, d, d) * build_pusher(params)
    pusher.label = f"yellow_carriage_diagonal_slider_travel_{travel:.3f}mm"
    return Compound(
        children=[
            build_fixed_plate("left", params),
            build_fixed_plate("right", params),
            pusher,
            build_rods(travel, params),
            build_m3_guide_pin(travel),
            build_esc(params),
            build_fc(params),
            build_wires(params),
            build_xt60(params),
        ],
        label=f"p4_captured_slider_loaded_{travel:.3f}mm_45deg_travel",
    )


def build_loaded_closed(params: P2Parameters = P4_DEFAULTS) -> Compound:
    return build_loaded(0.0, params)


def build_loaded_mid(params: P2Parameters = P4_DEFAULTS) -> Compound:
    return build_loaded(OPEN_STOP_STROKE / 2.0, params)


def build_loaded_open(params: P2Parameters = P4_DEFAULTS) -> Compound:
    return build_loaded(OPEN_STOP_STROKE, params)


def build_release(params: P2Parameters = P4_DEFAULTS) -> Compound:
    """Open geometry without the workpiece, exposing the wire loading path."""

    d = OPEN_COMPONENT
    pusher = Pos(0.0, d, d) * build_pusher(params)
    pusher.label = "yellow_carriage_release_open_workpiece_removed"
    return Compound(
        children=[
            build_fixed_plate("left", params),
            build_fixed_plate("right", params),
            pusher,
            build_rods(OPEN_STOP_STROKE, params),
            build_m3_guide_pin(OPEN_STOP_STROKE),
        ],
        label="p4_captured_slider_release_open_workpiece_removed",
    )


def build_release_open(params: P2Parameters = P4_DEFAULTS) -> Compound:
    """Explicit alias used by the release-open export and review contract."""

    return build_release(params)


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation is not None else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P2Parameters = P4_DEFAULTS) -> Compound:
    left = _on_bed(build_fixed_plate("left", params), 0.0, 0.0, Rot(0, 90, 0))
    left.label = "print_left_green_slider_guide_cheek"
    right = _on_bed(build_fixed_plate("right", params), 55.0, 0.0, Rot(0, 90, 0))
    right.label = "print_right_green_follower_slider_guide_cheek"
    left.label = "print_left_green_master_slider_guide_cheek"
    pusher = _on_bed(build_pusher(params), 115.0, 0.0, Rot(180, 0, 0))
    pusher.label = "print_yellow_one_piece_captured_sliding_carriage"
    return Compound(
        children=[left, right, pusher],
        label="p4_print_kit_exactly_three_printed_solids_no_rods_or_M3_pin",
    )


__all__ = [
    "CHEEK_THICKNESS",
    "GUIDE_CLEARANCE",
    "LEFT_CHEEK_X",
    "LEFT_SHOE_X",
    "M3_PIN_CLOSED",
    "M3_PIN_DIAMETER",
    "M3_SLOT_CLOSED",
    "M3_SLOT_OPEN",
    "M3_SLOT_WIDTH",
    "OPEN_COMPONENT",
    "OPEN_STOP_STROKE",
    "P4_DEFAULTS",
    "RIGHT_CHEEK_X",
    "RIGHT_SHOE_X",
    "ROD_SLOT_CLOSED",
    "ROD_SLOT_OPEN",
    "ROD_SLOT_WIDTH_FOLLOWER",
    "ROD_SLOT_WIDTH_MASTER",
    "build_fixed_plate",
    "build_loaded",
    "build_loaded_closed",
    "build_loaded_mid",
    "build_loaded_open",
    "build_m3_guide_pin",
    "build_moving_rod",
    "build_print_kit",
    "build_pusher",
    "build_release",
    "build_release_open",
    "build_rods",
    "contact_points",
    "moving_center",
    "pin_center",
    "rod_centers",
]
