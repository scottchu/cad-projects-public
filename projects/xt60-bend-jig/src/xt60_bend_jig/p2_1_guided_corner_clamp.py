"""P2.1 guided corner clamp built around the frozen P2 contact geometry.

The printed mechanism is deliberately small: one rigid green frame, one
yellow U pusher, one knob and two moving-rod keepers.  The moving rod and an
integral rectangular tongue run in parallel 45 degree slots, so the pusher
cannot rack.  A conventional M6 screw in a fixed nut bears on a broad thrust
pad.  It closes the jig positively; opening is deliberately manual after the
screw is backed out, avoiding an unassemblable hidden collar.

Axes remain P2: rods run on X, the ESC is toward +Y, and +Z is up.
"""

from __future__ import annotations

from collections import Counter
from math import sqrt
from pathlib import Path
from typing import Literal

from build123d import Align, Box, Compound, Cylinder, Pos, RegularPolygon, Rot, Shape, extrude
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
from xt60_bend_jig.p5_simple_slider import (
    _capsule_yz,
    _fixed_L_profile,
    _extrude_yz_profile,
    build_pusher as _build_p5_pusher,
)


Side = Literal["left", "right"]
P21_DEFAULTS = P2_DEFAULTS

PLATE_THICKNESS = 3.0
CLEAR_SPAN = 38.0
OUTER_SPAN = CLEAR_SPAN + 2.0 * PLATE_THICKNESS
PLATE_CENTER_X = (CLEAR_SPAN + PLATE_THICKNESS) / 2.0
ROD_PROJECTION = (P21_DEFAULTS.rod_length - OUTER_SPAN) / 2.0

LEFT_FIXED_BORE = 3.90
RIGHT_FIXED_BORE = 4.20
MOVING_SLOT_WIDTH = 4.50
MOVING_BORE = 4.20
OPEN_STROKE = 11.0
OPEN_COMPONENT = OPEN_STROKE / sqrt(2.0)

GUIDE_TONGUE_SIZE = 4.0
# The square tongue's 2.828 mm half-diagonal clears the R3.10 slot by 0.272.
GUIDE_SLOT_WIDTH = 6.30
GUIDE_CLEARANCE = GUIDE_SLOT_WIDTH / 2.0 - GUIDE_TONGUE_SIZE / sqrt(2.0)
GUIDE_CLOSED = PointYZ(14.0, 50.5)
GUIDE_OPEN = PointYZ(GUIDE_CLOSED.y + OPEN_COMPONENT, GUIDE_CLOSED.z + OPEN_COMPONENT)
GUIDE_THROAT_END = PointYZ(GUIDE_OPEN.y + 6.0 / sqrt(2.0), GUIDE_OPEN.z + 6.0 / sqrt(2.0))

M6_SHAFT_DIAMETER = 6.0
M6_CLEARANCE_DIAMETER = 6.6
M6_NUT_ACROSS_CORNERS = 12.0
M6_NUT_THICKNESS = 5.0
SCREW_AXIS_ANGLE_DEG = -45.0
DRIVE_CONTACT_CLOSED = PointYZ(11.3, 59.0)
NUT_AXIS_DISTANCE = 28.0
SCREW_LENGTH = 42.0
THRUST_TIP_DIAMETER = 8.0
THRUST_TIP_THICKNESS = 2.4
THRUST_PAD_DIAMETER = 12.0
THRUST_PAD_THICKNESS = 4.0
MOVING_ROD_KEEPER_GAP = 0.50
TONGUE_ROOT_DEPTH = 1.20
NUT_KEEPER_CLEARANCE = 0.30
KEEPER_SNAP_DEFLECTION = 0.30
KEEPER_SNAP_ARM_THICKNESS = 1.20
KEEPER_SNAP_ROOF_GAP = 0.20


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def _x_cylinder(diameter: float, length: float, x: float, point: PointYZ) -> Shape:
    return Pos(x, point.y, point.z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _axis_point(origin: PointYZ, distance: float) -> PointYZ:
    d = distance / sqrt(2.0)
    return PointYZ(origin.y + d, origin.z + d)


def _axis_cylinder(diameter: float, length: float, center: PointYZ, vertices: int | None = None) -> Shape:
    # build123d Cylinder is used for both the shaft and the conservative
    # across-corners nut/head envelopes; ``vertices`` remains an intent tag.
    return Pos(0.0, center.y, center.z) * Rot(SCREW_AXIS_ANGLE_DEG, 0.0, 0.0) * Cylinder(
        diameter / 2.0,
        length,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _axis_hex_prism(across_corners: float, length: float, center: PointYZ) -> Shape:
    hex_face = RegularPolygon(across_corners / 2.0, 6)
    prism = extrude(hex_face, length / 2.0, both=True)
    return Pos(0.0, center.y, center.z) * Rot(SCREW_AXIS_ANGLE_DEG, 0.0, 0.0) * prism


def _axis_side_load_slot(x_center: float, x_length: float, across_flats: float, length: float, center: PointYZ) -> Shape:
    return Pos(x_center, center.y, center.z) * Rot(SCREW_AXIS_ANGLE_DEG, 0.0, 0.0) * Box(
        x_length, across_flats, length, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )


def moving_center(travel: float = 0.0, params: P2Parameters = P21_DEFAULTS) -> PointYZ:
    if not -1e-9 <= travel <= OPEN_STROKE + 1e-9:
        raise ValueError("travel is bounded by the 0 to 11 mm slot stops")
    c = rod_centers(params)["moving"]
    d = travel / sqrt(2.0)
    return PointYZ(c.y + d, c.z + d)


def _moving_slot_endpoints(params: P2Parameters = P21_DEFAULTS) -> tuple[PointYZ, PointYZ]:
    radial = (MOVING_SLOT_WIDTH - params.rod_diameter) / 2.0
    closed = moving_center(0.0, params)
    open_ = moving_center(OPEN_STROKE, params)
    inset = radial / sqrt(2.0)
    return (
        PointYZ(closed.y + inset, closed.z + inset),
        PointYZ(open_.y - inset, open_.z - inset),
    )


def build_side_plate(side: Side, params: P2Parameters = P21_DEFAULTS) -> Shape:
    """A t3 green L with two fixed bores and two parallel guide slots."""

    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    x = -PLATE_CENTER_X if side == "left" else PLATE_CENTER_X
    plate = _extrude_yz_profile(_fixed_L_profile(), x, PLATE_THICKNESS)

    centers = rod_centers(params)
    fixed_bore = LEFT_FIXED_BORE if side == "left" else RIGHT_FIXED_BORE
    for name in ("left", "bottom"):
        plate -= _x_cylinder(fixed_bore, PLATE_THICKNESS + 2.0, x, centers[name])

    low, high = _moving_slot_endpoints(params)
    plate += _capsule_yz(low, high, 9.0, x, PLATE_THICKNESS)
    plate -= _capsule_yz(low, high, MOVING_SLOT_WIDTH, x, PLATE_THICKNESS + 2.0)

    plate += _capsule_yz(GUIDE_CLOSED, GUIDE_OPEN, 10.0, x, PLATE_THICKNESS)
    plate -= _capsule_yz(GUIDE_CLOSED, GUIDE_OPEN, GUIDE_SLOT_WIDTH, x, PLATE_THICKNESS + 2.0)
    # Open insertion throat: tongues enter here before the moving rod is fitted.
    plate -= _capsule_yz(GUIDE_OPEN, GUIDE_THROAT_END, GUIDE_SLOT_WIDTH, x, PLATE_THICKNESS + 2.0)
    return _label(
        plate,
        f"{side}_green_t3_L_press3p90_slip4p20_moving_and_antirack_slots",
        "#3F6B4F",
    )


def _build_screw_support() -> Shape:
    nut_center = _axis_point(DRIVE_CONTACT_CLOSED, NUT_AXIS_DISTANCE)
    bridge = Pos(0.0, -9.0, 54.0) * Box(
        OUTER_SPAN, 3.6, 3.6, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    lower_bridge = Pos(0.0, -9.0, 23.0) * Box(
        OUTER_SPAN, 6.0, 6.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    upper_bridge = Pos(0.0, nut_center.y, nut_center.z) * Box(
        OUTER_SPAN, 5.0, 5.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    support = Pos(0.0, nut_center.y, nut_center.z) * Box(
        14.0, 13.0, 13.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    nut_pocket = _axis_hex_prism(M6_NUT_ACROSS_CORNERS + 0.4, M6_NUT_THICKNESS + 0.4, nut_center)
    # The standard nut drops from +Z through an open service throat, then
    # settles into the diagonal hex pocket where its corners resist torque.
    nut_top_load = Pos(0.0, nut_center.y, nut_center.z + 4.0) * Box(
        M6_NUT_ACROSS_CORNERS + 0.8,
        M6_NUT_ACROSS_CORNERS + 0.8,
        19.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    through = _axis_cylinder(M6_CLEARANCE_DIAMETER, 44.0, nut_center)
    # Two narrow outer diagonal struts replace the former rear posts/cage.
    # They join the existing guide webs to the small nut bridge.
    struts = None
    strut_start = PointYZ(16.5, 53.0)
    strut_end = PointYZ(nut_center.y, nut_center.z)
    # Run outside the plate faces. Their inner strut faces are at +/-21.8,
    # leaving 0.30 mm from the tongue's +/-21.5 swept X envelope.
    for x in (-23.3, 23.3):
        strut = _capsule_yz(strut_start, strut_end, 4.0, x, PLATE_THICKNESS)
        struts = strut if struts is None else struts + strut
    assert struts is not None
    return (bridge + lower_bridge + upper_bridge + support + struts) - nut_pocket - nut_top_load - through


def _keeper_snap_hooks() -> Shape:
    """Two integral flex hooks positively retain the keyed keeper in +Z."""

    center = _axis_point(DRIVE_CONTACT_CLOSED, NUT_AXIS_DISTANCE)
    hooks: Shape | None = None
    for sign in (-1.0, 1.0):
        arm_x = sign * 7.4
        arm = Pos(arm_x, center.y, center.z + 5.0) * Box(
            KEEPER_SNAP_ARM_THICKNESS,
            8.6,
            10.4,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        # The hook overlaps the 6.6 mm keeper half-width by 0.30 mm. During
        # intentional installation/removal the two arms flex outward by that
        # amount; once seated, a 0.20 mm roof gap avoids preload.
        lip_x = sign * 6.55
        lip = Pos(lip_x, center.y, center.z + 9.7) * Box(
            0.5,
            8.6,
            1.0,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        hook = arm + lip
        hooks = hook if hooks is None else hooks + hook
    assert hooks is not None
    return hooks


def build_frame(params: P2Parameters = P21_DEFAULTS) -> Shape:
    frame = (
        build_side_plate("left", params)
        + build_side_plate("right", params)
        + _build_screw_support()
        + _keeper_snap_hooks()
    )
    return _label(
        frame,
        "one_piece_green_rigid_frame_t3_38mm_clear_span_flat_clamp_bridges",
        "#3F6B4F",
    )


def build_pusher(params: P2Parameters = P21_DEFAULTS) -> Shape:
    """The P5 U, with integral second guide tongues and a broad thrust pad."""

    pusher = _build_p5_pusher(params)
    moving = rod_centers(params)["moving"]
    # P5 uses 4.3 bores; close them locally and recut at 4.2 for this prototype.
    for x in (-16.7, 16.7):
        pusher += _x_cylinder(5.2, 4.0, x, moving)
        pusher -= _x_cylinder(MOVING_BORE, 6.0, x, moving)

    # Two integral square tongues enter the green parallel slots.
    for sign in (-1.0, 1.0):
        # 4.0 mm tongue from X=17.5..21.5 (mirrored) overlaps the 18.7 mm
        # yellow shoe face by exactly 1.2 mm: a real printable root.
        x = sign * 19.5
        pusher += Pos(x, GUIDE_CLOSED.y, GUIDE_CLOSED.z) * Box(
            4.0, GUIDE_TONGUE_SIZE, GUIDE_TONGUE_SIZE,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )

    # External thrust pad: its +axis face is the drive contact.  A short neck
    # joins it to the cap while leaving the central wire/iron corridor open.
    pad_center = _axis_point(DRIVE_CONTACT_CLOSED, -THRUST_PAD_THICKNESS / 2.0)
    pad = _axis_cylinder(THRUST_PAD_DIAMETER, THRUST_PAD_THICKNESS, pad_center)
    # Two side ribs join the pad without occupying the centered screw-tip
    # corridor. Their furthest +axis corner is exactly behind the pad face.
    ribs = None
    for x in (-5.25, 5.25):
        rib = Pos(x, 9.0, 54.0) * Box(1.5, 4.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        ribs = rib if ribs is None else ribs + rib
    assert ribs is not None
    pusher += pad + ribs
    return _label(
        pusher,
        "yellow_U_two_parallel_guides_M6_thrust_pad_manual_reopen",
        "#E0A323",
    )


def build_m6_nut() -> Shape:
    center = _axis_point(DRIVE_CONTACT_CLOSED, NUT_AXIS_DISTANCE)
    nut = _axis_hex_prism(M6_NUT_ACROSS_CORNERS, M6_NUT_THICKNESS, center)
    nut -= _axis_cylinder(M6_CLEARANCE_DIAMETER, M6_NUT_THICKNESS + 2.0, center)
    return _label(nut, "reference_standard_M6_hex_nut_fixed_in_green_pocket", "#666A6E")


def screw_contact_point(travel: float) -> PointYZ:
    return _axis_point(DRIVE_CONTACT_CLOSED, travel)


def build_screw(travel: float = 0.0) -> Compound:
    contact = screw_contact_point(travel)
    tip_center = _axis_point(contact, THRUST_TIP_THICKNESS / 2.0)
    shaft_center = _axis_point(tip_center, SCREW_LENGTH / 2.0)
    shaft = _label(
        _axis_cylinder(M6_SHAFT_DIAMETER, SCREW_LENGTH, shaft_center),
        f"reference_M6_screw_shaft_travel_{travel:.3f}",
        "#AEB5BA",
    )
    tip = _label(
        _axis_cylinder(THRUST_TIP_DIAMETER, THRUST_TIP_THICKNESS, tip_center),
        "reference_M6_broad_tip_bearing_on_yellow_pad",
        "#AEB5BA",
    )
    head_center = _axis_point(tip_center, SCREW_LENGTH + 2.0)
    head = _label(
        _axis_hex_prism(11.0, 4.0, head_center),
        "reference_M6_hex_head_captured_by_knob",
        "#AEB5BA",
    )
    return Compound(children=[shaft, tip, head], label="reference_M6_push_only_screw_manual_reopen")


def build_knob(travel: float = 0.0) -> Shape:
    tip_center = _axis_point(
        screw_contact_point(travel),
        THRUST_TIP_THICKNESS / 2.0,
    )
    head_center = _axis_point(tip_center, SCREW_LENGTH + 2.0)
    knob = _axis_cylinder(16.0, 8.0, head_center)
    knob -= _axis_hex_prism(11.4, 4.4, head_center)
    knob -= _axis_cylinder(M6_CLEARANCE_DIAMETER, 14.0, head_center)
    return _label(knob, f"printed_black_M6_knob_travel_{travel:.3f}", "#202326")


def build_nut_keeper() -> Shape:
    """Separate keyed keeper closes the M6 nut insertion throat.

    The underside skirt fits the top-load chute with 0.30 mm clearance per
    side and carries a shallow hex socket around the exposed nut corners.
    Thus the frame's lower pocket and the keeper share anti-rotation duty.
    """

    center = _axis_point(DRIVE_CONTACT_CLOSED, NUT_AXIS_DISTANCE)
    lid = Pos(0.0, center.y, center.z + 8.3) * Box(
        13.2, 8.6, 1.4, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    plug = Pos(0.0, center.y, center.z + 5.7) * Box(
        M6_NUT_ACROSS_CORNERS + 0.8 - 2.0 * NUT_KEEPER_CLEARANCE,
        M6_NUT_ACROSS_CORNERS + 0.8 - 2.0 * NUT_KEEPER_CLEARANCE,
        3.8,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    keeper = lid + plug
    keeper -= _axis_hex_prism(M6_NUT_ACROSS_CORNERS + 0.35, M6_NUT_THICKNESS + 1.0, center)
    keeper -= _axis_cylinder(M6_CLEARANCE_DIAMETER, 24.0, center)
    return _label(keeper, "printed_M6_nut_top_keeper_manual_service", "#202326")


def build_fixed_rod_caps(params: P2Parameters = P21_DEFAULTS) -> Compound:
    """Two right-end P6-candidate collars for the fixed reaction rods."""

    children: list[Shape] = []
    for name in ("left", "bottom"):
        point = rod_centers(params)[name]
        body_center_x = 25.3
        socket_center_x = 23.65
        cap = _x_cylinder(8.0, 6.0, body_center_x, point)
        cap -= _x_cylinder(4.10, 2.7, socket_center_x, point)
        children.append(_label(cap, f"P6_candidate_right_{name}_rod_cap_socket4p10_depth2p7", "#202326"))
    return Compound(children=children, label="two_P6_candidate_fixed_rod_service_caps")


def build_moving_rod_keepers(travel: float = 0.0, params: P2Parameters = P21_DEFAULTS) -> Compound:
    c = moving_center(travel, params)
    inner_x = OUTER_SPAN / 2.0 + MOVING_ROD_KEEPER_GAP
    children: list[Shape] = []
    for sign in (-1.0, 1.0):
        x = sign * (inner_x + 2.0)
        socket_x = sign * (inner_x + 1.4)
        keeper = _x_cylinder(8.0, 4.0, x, c) - _x_cylinder(4.10, 2.8, socket_x, c)
        children.append(_label(keeper, f"moving_rod_{'left' if sign < 0 else 'right'}_keeper_0p5mm_endplay", "#202326"))
    return Compound(children=children, label="two_removable_moving_rod_keepers")


def build_rods(travel: float = 0.0, params: P2Parameters = P21_DEFAULTS) -> Compound:
    c = rod_centers(params)
    return Compound(
        children=[
            build_reference_rod("left", c["left"], params),
            build_reference_rod("bottom", c["bottom"], params),
            build_reference_rod("moving", moving_center(travel, params), params),
        ],
        label="reference_exactly_three_user_4x50_rods",
    )


def build_loaded(travel: float = 0.0, params: P2Parameters = P21_DEFAULTS, references: bool = True) -> Compound:
    d = travel / sqrt(2.0)
    pusher = Pos(0.0, d, d) * build_pusher(params)
    pusher.label = f"yellow_guided_U_pusher_travel_{travel:.3f}mm"
    children: list[Shape] = [
        build_frame(params), pusher, build_rods(travel, params),
        build_moving_rod_keepers(travel, params), build_fixed_rod_caps(params), build_m6_nut(), build_nut_keeper(),
        build_screw(travel), build_knob(travel),
    ]
    if references:
        children.extend([build_esc(params), build_fc(params), build_wires(params), build_xt60(params)])
    return Compound(children=children, label=f"p2_1_guided_corner_clamp_travel_{travel:.3f}mm")


def build_loaded_closed(params: P2Parameters = P21_DEFAULTS) -> Compound:
    return build_loaded(0.0, params)


def build_loaded_mid(params: P2Parameters = P21_DEFAULTS) -> Compound:
    return build_loaded(OPEN_STROKE / 2.0, params)


def build_loaded_open(params: P2Parameters = P21_DEFAULTS) -> Compound:
    return build_loaded(OPEN_STROKE, params)


def build_release_open(params: P2Parameters = P21_DEFAULTS) -> Compound:
    return build_loaded(OPEN_STROKE, params, references=False)


def build_exploded(params: P2Parameters = P21_DEFAULTS) -> Compound:
    """Assembly-order view with all removable pieces pulled clear."""

    pusher = Pos(0.0, 60.0, 60.0) * build_pusher(params)
    centers = rod_centers(params)
    rods = Compound(children=[
        Pos(-80.0, 0.0, 0.0) * build_reference_rod("left_exploded_minus_X", centers["left"], params),
        Pos(80.0, 0.0, 0.0) * build_reference_rod("bottom_exploded_plus_X", centers["bottom"], params),
        Pos(-80.0, 0.0, 0.0) * build_reference_rod("moving_exploded_minus_X", moving_center(OPEN_STROKE, params), params),
    ], label="three_rods_exploded_along_X")
    raw_keepers = build_moving_rod_keepers(OPEN_STROKE, params).children
    keepers = Compound(children=[Pos(-115.0, 0.0, 0.0) * raw_keepers[0], Pos(115.0, 0.0, 0.0) * raw_keepers[1]], label="moving_keepers_exploded_along_X")
    raw_caps = build_fixed_rod_caps(params).children
    caps = Compound(children=[Pos(115.0, 0.0, 0.0) * cap for cap in raw_caps], label="fixed_caps_exploded_plus_X")
    nut = Pos(0.0, 0.0, 30.0) * build_m6_nut()
    keeper = Pos(0.0, 0.0, 42.0) * build_nut_keeper()
    screw = Pos(0.0, 100.0 / sqrt(2.0), 100.0 / sqrt(2.0)) * build_screw(OPEN_STROKE)
    knob = Pos(0.0, 140.0 / sqrt(2.0), 140.0 / sqrt(2.0)) * build_knob(OPEN_STROKE)
    return Compound(
        children=[build_frame(params), pusher, rods, keepers, caps, nut, keeper, screw, knob],
        label="p2_1_exploded_frame_slider_rods_X_caps_X_nut_Z_keeper_Z_screw_axis_knob",
    )


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation is not None else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P2Parameters = P21_DEFAULTS) -> Compound:
    """Eight printed solids; M6 screw/nut and all three rods are hardware."""

    frame = _on_bed(build_frame(params), 0.0, 0.0)
    frame.label = "print_one_piece_t3_guided_frame"
    pusher = _on_bed(build_pusher(params), 55.0, 0.0, Rot(180.0, 0.0, 0.0))
    pusher.label = "print_yellow_guided_pusher"
    knob = _on_bed(build_knob(), 105.0, 0.0, Rot(45.0, 0.0, 0.0))
    knob.label = "print_compact_hex_socket_knob"
    keeper = _on_bed(build_nut_keeper(), 125.0, 0.0)
    keeper.label = "print_keyed_nut_keeper"
    moving = build_moving_rod_keepers(params=params).children
    fixed = build_fixed_rod_caps(params).children
    small: list[Shape] = []
    for index, part in enumerate([*moving, *fixed]):
        placed = _on_bed(part, 105.0 + 15.0 * index, 24.0, Rot(0.0, 90.0, 0.0))
        placed.label = f"print_{part.label}"
        small.append(placed)
    return Compound(
        children=[frame, pusher, knob, keeper, *small],
        label="p2_1_print_kit_eight_printed_solids_hardware_excluded",
    )


def _welded_triangles(
    shape: Shape,
    *,
    linear_tolerance: float = 0.02,
    angular_tolerance: float = 0.05,
    weld_tolerance: float = 1e-6,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    """Tessellate one BREP and weld face-boundary duplicate vertices.

    OCC triangulates each face independently.  The ordinary mesh export keeps
    those coincident boundary vertices separate, which makes lib3mf correctly
    report every object as non-manifold.  Quantized welding restores the shared
    BREP edges without changing the source geometry or triangle winding.
    """

    raw_vertices, raw_triangles = shape.tessellate(linear_tolerance, angular_tolerance)
    vertex_by_key: dict[tuple[int, int, int], int] = {}
    vertices: list[tuple[float, float, float]] = []
    remap: list[int] = []
    for vertex in raw_vertices:
        point = (float(vertex.X), float(vertex.Y), float(vertex.Z))
        key = tuple(int(round(value / weld_tolerance)) for value in point)
        if key not in vertex_by_key:
            vertex_by_key[key] = len(vertices)
            vertices.append(tuple(value for value in point))
        remap.append(vertex_by_key[key])

    triangles: list[tuple[int, int, int]] = []
    for a, b, c in raw_triangles:
        triangle = (remap[a], remap[b], remap[c])
        if len(set(triangle)) == 3:
            triangles.append(triangle)

    undirected: Counter[tuple[int, int]] = Counter()
    directed: Counter[tuple[int, int]] = Counter()
    for a, b, c in triangles:
        for start, end in ((a, b), (b, c), (c, a)):
            undirected[tuple(sorted((start, end)))] += 1
            directed[(start, end)] += 1
    if any(count != 2 for count in undirected.values()):
        raise ValueError(f"{shape.label}: welded tessellation has an open/non-manifold edge")
    if any(
        directed[(a, b)] != 1 or directed[(b, a)] != 1
        for a, b in undirected
    ):
        raise ValueError(f"{shape.label}: welded tessellation has inconsistent orientation")
    return vertices, triangles


def export_print_kit_3mf(output: str | Path, params: P2Parameters = P21_DEFAULTS) -> Path:
    """Write and re-open an eight-mesh lib3mf-valid source-derived print kit."""

    import lib3mf

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    for part in build_print_kit(params).children:
        vertices, triangles = _welded_triangles(part)
        mesh = model.AddMeshObject()
        mesh.SetName(part.label)
        mesh.SetGeometry(
            [lib3mf.Position(vertex) for vertex in vertices],
            [lib3mf.Triangle(triangle) for triangle in triangles],
        )
        if not mesh.IsValid() or not mesh.IsManifoldAndOriented():
            raise ValueError(f"{part.label}: lib3mf rejected the welded source mesh")
        model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
    model.QueryWriter("3mf").WriteToFile(str(output_path))

    check_model = wrapper.CreateModel()
    check_model.QueryReader("3mf").ReadFromFile(str(output_path))
    meshes = check_model.GetMeshObjects()
    count = 0
    while meshes.MoveNext():
        mesh = meshes.GetCurrentMeshObject()
        if not mesh.IsValid() or not mesh.IsManifoldAndOriented():
            raise ValueError(f"{mesh.GetName()}: written 3MF failed round-trip validation")
        count += 1
    if count != 8:
        raise ValueError(f"written 3MF contains {count} meshes instead of 8")
    return output_path


__all__ = [
    "CLEAR_SPAN", "DRIVE_CONTACT_CLOSED", "GUIDE_CLEARANCE",
    "GUIDE_CLOSED", "GUIDE_OPEN", "GUIDE_THROAT_END", "LEFT_FIXED_BORE", "MOVING_ROD_KEEPER_GAP",
    "OPEN_STROKE", "OUTER_SPAN", "PLATE_THICKNESS", "RIGHT_FIXED_BORE",
    "KEEPER_SNAP_ARM_THICKNESS", "KEEPER_SNAP_DEFLECTION", "KEEPER_SNAP_ROOF_GAP",
    "ROD_PROJECTION", "TONGUE_ROOT_DEPTH", "build_exploded", "build_fixed_rod_caps", "build_frame", "build_knob", "build_loaded", "build_loaded_closed", "build_loaded_mid",
    "build_loaded_open", "build_m6_nut", "build_moving_rod_keepers", "build_nut_keeper", "build_print_kit", "build_pusher",
    "build_release_open", "build_rods", "build_screw", "build_side_plate",
    "contact_points", "export_print_kit_3mf", "moving_center", "rod_centers", "screw_contact_point",
]
