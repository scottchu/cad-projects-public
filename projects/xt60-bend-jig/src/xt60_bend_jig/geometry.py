"""Build123d source geometry for the XT60 90 degree bend jig.

Coordinate convention
---------------------
The three 50 mm rods run on X.  Y is the horizontal direction in the bend
diagram and Z is up.  The two 4 mm side frames are centred at X = +/-21 mm,
which gives a 38 mm clear span and 46 mm outside span.  The rods consequently
project 2 mm beyond each outside face.

This module intentionally uses build123d directly.  It contains no export or
``cadgen`` calls; the model remains ordinary Python source that tests and later
STEP wrappers can consume.
"""

from __future__ import annotations

from math import atan2, degrees, sqrt
from typing import Any, Iterable, Literal

from build123d import (
    Align,
    Box,
    BuildLine,
    BuildSketch,
    CenterArc,
    Circle,
    Compound,
    Cylinder,
    Line,
    Plane,
    Pos,
    RegularPolygon,
    Rot,
    Shape,
    Wire,
    extrude,
    sweep,
)

from .mechanism import solve_mechanism
from .parameters import DEFAULT_PARAMETERS, PrototypeParameters


Side = Literal["left", "right"]

FRAME_THICKNESS = DEFAULT_PARAMETERS.side_plate_thickness
FRAME_CLEAR_SPAN = DEFAULT_PARAMETERS.clear_span
FRAME_OUTER_SPAN = DEFAULT_PARAMETERS.outer_span
FRAME_CENTER_X = (FRAME_OUTER_SPAN - FRAME_THICKNESS) / 2.0
ROD_DIAMETER = DEFAULT_PARAMETERS.rod_diameter
ROD_BORE_DIAMETER = 4.3
ADJUSTMENT_PITCH = DEFAULT_PARAMETERS.reaction_position_pitch
FORMING_SLOT_WIDTH = DEFAULT_PARAMETERS.slot_width
MOVING_CLAMP_PASSAGE_DIAMETER = 3.4
MOVING_INSERT_POCKET_DIAMETER = 4.6
MOVING_INSERT_POCKET_DEPTH = 5.0
MOVING_INSERT_BOSS_DIAMETER = 8.6
REACTION_INSERT_POCKET_DIAMETER = 4.6
REACTION_INSERT_POCKET_DEPTH = 3.5
REACTION_ROD_BOSS_DIAMETER = 9.0
REACTION_LOCK_BOSS_DIAMETER = 7.0
REACTION_LOCK_OFFSET = 7.0
SLIDER_COLLAR_DIAMETER = 10.0
XT60_ENVELOPE = (DEFAULT_PARAMETERS.xt60_width, DEFAULT_PARAMETERS.xt60_depth)
XT60_SIDE_CLEARANCE = DEFAULT_PARAMETERS.cradle_clearance_per_side
NUT_TRAP_AF = DEFAULT_PARAMETERS.m4_nut_trap_across_flats
FIT_SIZES = DEFAULT_PARAMETERS.fit_coupon_sizes
WIRE_BEND_RADIUS = DEFAULT_PARAMETERS.bend_radius
WIRE_HORIZONTAL_Z = DEFAULT_PARAMETERS.wire_center_z
WIRE_TANGENT_START_Y = DEFAULT_PARAMETERS.bend_start_y
WIRE_VERTICAL_TANGENT_Y = DEFAULT_PARAMETERS.vertical_leg_y


def _value(params: object | None, names: str | Iterable[str], default: float) -> float:
    """Read a numeric parameter while tolerating evolving, descriptive names."""

    if params is None:
        params = DEFAULT_PARAMETERS
    names = (names,) if isinstance(names, str) else tuple(names)
    for name in names:
        if params is not None and hasattr(params, name):
            return float(getattr(params, name))
    return float(default)


def _label(shape: Shape, name: str) -> Shape:
    shape.label = name
    return shape


def _x_cylinder(diameter: float, length: float, x: float, y: float, z: float) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _slot_x(
    width: float,
    overall_length: float,
    center: tuple[float, float, float],
    angle_degrees: float = 45.0,
    through_length: float = 7.0,
) -> Shape:
    """Rounded straight slot through X, with its long axis in the YZ plane."""

    x, y, z = center
    straight = overall_length - width
    half = straight / 2.0
    # Rotation about X sends local +Z toward -Y for a positive angle.
    offset_y = -half / sqrt(2.0) if angle_degrees == 45.0 else 0.0
    offset_z = half / sqrt(2.0) if angle_degrees == 45.0 else half
    middle = Pos(x, y, z) * Box(
        through_length,
        width,
        straight,
        rotation=(angle_degrees, 0, 0),
    )
    ends = (
        _x_cylinder(width, through_length, x, y + offset_y, z + offset_z)
        + _x_cylinder(width, through_length, x, y - offset_y, z - offset_z)
    )
    return middle + ends


def _obround_x(
    start: tuple[float, float],
    end: tuple[float, float],
    width: float,
    x: float,
    through_length: float,
) -> Shape:
    """Create an exact rounded track through X between two Y/Z centers."""

    sy, sz = start
    ey, ez = end
    dy, dz = ey - sy, ez - sz
    straight = sqrt(dy * dy + dz * dz)
    if straight <= 0:
        return _x_cylinder(width, through_length, x, sy, sz)
    angle = degrees(atan2(-dy, dz))
    middle = Pos(x, (sy + ey) / 2.0, (sz + ez) / 2.0) * Box(
        through_length, width, straight, rotation=(angle, 0, 0)
    )
    return middle + _x_cylinder(width, through_length, x, sy, sz) + _x_cylinder(width, through_length, x, ey, ez)


def build_side_frame(
    side: Side,
    params: PrototypeParameters | None = None,
    wire_gauge: int = 12,
) -> Shape:
    """Build one ribbed frame with reaction tracks and solver-derived moving slot."""

    if side not in ("left", "right"):
        raise ValueError("side must be 'left' or 'right'")
    thickness = _value(params, ("side_plate_thickness", "frame_thickness", "side_frame_thickness"), FRAME_THICKNESS)
    outer_span = _value(params, ("outer_span", "side_plate_outer_span", "frame_outer_span"), FRAME_OUTER_SPAN)
    bore = _value(params, ("rod_bore_diameter", "bore_diameter"), ROD_BORE_DIAMETER)
    params = params or DEFAULT_PARAMETERS
    pitch = max(6.5, params.reaction_position_pitch)
    slot_width = _value(params, ("forming_slot_width", "slider_slot_width"), FORMING_SLOT_WIDTH)
    x = (-1.0 if side == "left" else 1.0) * (outer_span - thickness) / 2.0

    # A long foot, rear tower and diagonal rib make a one-piece stable frame.
    # The upper/front quadrant is deliberately absent for soldering access.
    # Fourteen millimetres keeps material continuously above the lower and
    # diagonal slots; a thinner foot leaves printable islands between cuts.
    # The 18 mm-high foot leaves at least 2.4 mm of real PETG above every
    # lower insert pocket at both supported wire gauges.  The widened rear
    # tower similarly carries the upper pockets after their lock datums move
    # 7 mm away from the reaction track.
    foot = Pos(x, 10.5, 9.0) * Box(thickness, 71.0, 18.0)
    rear_tower = Pos(x, 16.0, 24.0) * Box(thickness, 20.0, 40.0)
    diagonal_rib = Pos(x, 0.0, 22.0) * Box(thickness, 6.0, 39.0, rotation=(45, 0, 0))
    body = foot + rear_tower + diagonal_rib

    solutions = [
        solve_mechanism(params=params, wire_gauge=wire_gauge, upper_index=i, lower_index=i)
        for i in range(params.reaction_position_count)
    ]
    upper_centers = [solution.upper_rod_center for solution in solutions]
    lower_centers = [solution.lower_rod_center for solution in solutions]
    upper_track = _obround_x(
        (upper_centers[0].y, upper_centers[0].z),
        (upper_centers[-1].y, upper_centers[-1].z),
        bore,
        x,
        thickness + 2.0,
    )
    lower_track = _obround_x(
        (lower_centers[0].y, lower_centers[0].z),
        (lower_centers[-1].y, lower_centers[-1].z),
        bore,
        x,
        thickness + 2.0,
    )
    closed = solve_mechanism(params=params, wire_gauge=wire_gauge, closure=1.0)
    opened = solve_mechanism(params=params, wire_gauge=wire_gauge, closure=0.0)
    forming_slot = _obround_x(
        (closed.moving_rod_center.y, closed.moving_rod_center.z),
        (opened.moving_rod_center.y, opened.moving_rod_center.z),
        slot_width,
        x,
        thickness + 2.0,
    )
    # M3 lock datums sit beside, rather than inside, the continuous tracks.
    upper_index_bores = [
        _x_cylinder(3.4, thickness + 2.0, x, point.y - REACTION_LOCK_OFFSET, point.z)
        for point in upper_centers
    ]
    lower_index_bores = [
        _x_cylinder(3.4, thickness + 2.0, x, point.y, point.z + REACTION_LOCK_OFFSET)
        for point in lower_centers
    ]
    # Each indexed M3 datum terminates in a heat-set insert seat in the side
    # frame, not in the removable carrier.  The cutter begins 0.1 mm outside
    # the outer face and advances exactly 3.5 mm into the 4 mm plate, leaving
    # a nominal 0.5 mm inner-face floor around the coaxial through passage.
    outward = -1.0 if side == "left" else 1.0
    outer_face_x = x + outward * thickness / 2.0
    pocket_center_x = outer_face_x - outward * 1.7
    index_lock_datums = [
        *((point.y - REACTION_LOCK_OFFSET, point.z) for point in upper_centers),
        *((point.y, point.z + REACTION_LOCK_OFFSET) for point in lower_centers),
    ]
    reaction_insert_pockets = [
        _x_cylinder(
            REACTION_INSERT_POCKET_DIAMETER,
            REACTION_INSERT_POCKET_DEPTH + 0.1,
            pocket_center_x,
            lock_y,
            lock_z,
        )
        for lock_y, lock_z in index_lock_datums
    ]
    bridge_solution = solve_mechanism(params=params, wire_gauge=wire_gauge, closure=1.0)
    bridge_mount_z = bridge_solution.wire_endpoint.z + 3.0
    bridge_mount_bores = [
        _x_cylinder(3.4, thickness + 2.0, x, bridge_solution.wire_endpoint.y, bridge_mount_z + z)
        for z in (3.0, 7.0, 11.0)
    ]
    body = body - [
        upper_track,
        lower_track,
        forming_slot,
        *upper_index_bores,
        *lower_index_bores,
        *reaction_insert_pockets,
        *bridge_mount_bores,
    ]
    return _label(body, f"{side}_ribbed_side_frame")


def build_left_frame(params: PrototypeParameters | None = None, wire_gauge: int = 12) -> Shape:
    return build_side_frame("left", params, wire_gauge)


def build_right_frame(params: PrototypeParameters | None = None, wire_gauge: int = 12) -> Shape:
    return build_side_frame("right", params, wire_gauge)


# Descriptive aliases used by some wrappers and review scripts.
build_left_side_frame = build_left_frame
build_right_side_frame = build_right_frame


def build_slider(side: Side, params: PrototypeParameters | None = None, wire_gauge: int = 12) -> Shape:
    """Build one keyed moving-rod slider, including the left drive hardware."""

    if side not in ("left", "right"):
        raise ValueError("side must be 'left' or 'right'")
    thickness = _value(params, ("frame_thickness", "side_frame_thickness"), FRAME_THICKNESS)
    outer_span = _value(params, ("outer_span", "side_plate_outer_span", "frame_outer_span"), FRAME_OUTER_SPAN)
    capture = _value(params, ("moving_rod_capture_diameter", "rod_bore_diameter"), ROD_BORE_DIAMETER)
    frame_face = outer_span / 2.0
    # The 2 mm external plate occupies X=23..25 (or -25..-23), remaining
    # wholly within the 50 mm rod span.
    plate_x = (-1.0 if side == "left" else 1.0) * (frame_face + 1.0)
    params = params or DEFAULT_PARAMETERS
    closed = solve_mechanism(params=params, wire_gauge=wire_gauge, closure=1.0)
    closed_y = closed.moving_closed_center.y
    closed_z = closed.moving_closed_center.z

    # A compact circular collar eliminates the large rotated plate that could
    # collide with reaction carriers at extreme matrix settings.
    collar = _x_cylinder(SLIDER_COLLAR_DIAMETER, 2.0, plate_x, closed_y, closed_z)
    # The 4 mm rod itself is the close-running key in the 4.6 mm slot.  A
    # printed sleeve cannot fit around a 4.3 mm capture bore while retaining
    # 0.25 mm clearance per side, so no plastic protrudes into the frame slot.
    # The local socket reaches just beyond both faces of the 2 mm slider plate.
    # It stops at the 50 mm rod end so an axial M3 retainer can bear on that end.
    rod_socket_length = 2.4
    body = collar - _x_cylinder(capture, rod_socket_length, plate_x, closed_y, closed_z)

    if side == "left":
        # Every drive feature is collinear with the solver's 45 degree YZ axis.
        drive_x = -(frame_face + 5.5 + params.running_clearance_per_side)
        drive_y, drive_z = closed_y + 6.0, closed_z + 6.0
        boss = Pos(drive_x, drive_y, drive_z) * Cylinder(5.5, 10.0, rotation=(45, 0, 0))
        outer_face = -frame_face - params.running_clearance_per_side
        # This transverse diagonal web joins the collar to the M4 boss while
        # keeping the reaction-carrier clearance envelope open.
        external_web = Pos((drive_x + outer_face) / 2.0, closed_y + 3.0, closed_z + 3.0) * Box(
            outer_face - drive_x + 0.4, 10.5, 5.0, rotation=(45, 0, 0)
        )
        body = body + [boss, external_web]
        m4_clearance = Pos(drive_x, drive_y, drive_z) * Cylinder(
            params.m4_clearance_diameter / 2.0, 50.0, rotation=(45, 0, 0)
        )
        hex_face = RegularPolygon(NUT_TRAP_AF / sqrt(3.0), 6)
        hex_prism = extrude(hex_face, 3.6)
        nut_trap = Pos(drive_x, drive_y - 2.5, drive_z + 2.5) * (Rot(45, 0, 0) * hex_prism)
        body = body - [m4_clearance, nut_trap]

    # Each slider gets a symmetric outward-facing axial rod-end retainer.  The
    # boss nominally begins at the X=+/-25 rod end and runs 7 mm outward; a
    # 0.1 mm root overlap makes the face union robust without entering the
    # side-frame envelope.  The Ø4.6 x 5 insert seat opens from the outer end,
    # and its Ø3.4 continuation reaches the local Ø4.3 rod socket.
    outward = -1.0 if side == "left" else 1.0
    rod_end_x = outward * (params.rod_length / 2.0)
    boss_length = 7.1
    boss_center_x = rod_end_x + outward * (boss_length / 2.0 - 0.1)
    retainer_boss = _x_cylinder(
        MOVING_INSERT_BOSS_DIAMETER,
        boss_length,
        boss_center_x,
        closed_y,
        closed_z,
    )
    body = body + retainer_boss

    pocket_center_x = outward * 29.5
    insert_pocket = _x_cylinder(
        MOVING_INSERT_POCKET_DIAMETER,
        MOVING_INSERT_POCKET_DEPTH + 0.2,
        pocket_center_x,
        closed_y,
        closed_z,
    )
    continuation = _x_cylinder(
        MOVING_CLAMP_PASSAGE_DIAMETER,
        2.2,
        outward * 26.0,
        closed_y,
        closed_z,
    )
    body = body - [insert_pocket, continuation]

    # Recut after every addition so neither drive web nor retainer boss can
    # refill the rod socket.
    body = body - _x_cylinder(capture, rod_socket_length, plate_x, closed_y, closed_z)

    return _label(body, f"{side}_keyed_moving_slider_with_axial_rod_end_retainer")


def build_left_slider(params: PrototypeParameters | None = None, wire_gauge: int = 12) -> Shape:
    return build_slider("left", params, wire_gauge)


def build_right_slider(params: PrototypeParameters | None = None, wire_gauge: int = 12) -> Shape:
    return build_slider("right", params, wire_gauge)


def build_reaction_carrier(
    side: Side,
    kind: Literal["upper", "lower"],
    params: PrototypeParameters | None = None,
    wire_gauge: int = 12,
    index: int = 1,
) -> Shape:
    """External M3-lockable rod carrier for one reaction-track end."""

    if side not in ("left", "right") or kind not in ("upper", "lower"):
        raise ValueError("carrier requires left/right and upper/lower")
    params = params or DEFAULT_PARAMETERS
    solution = solve_mechanism(
        params=params, wire_gauge=wire_gauge, upper_index=index, lower_index=index
    )
    point = solution.upper_rod_center if kind == "upper" else solution.lower_rod_center
    frame_face = params.outer_span / 2.0
    x = (-1.0 if side == "left" else 1.0) * (frame_face + 1.0)
    if kind == "upper":
        lock_y, lock_z = point.y - REACTION_LOCK_OFFSET, point.z
    else:
        lock_y, lock_z = point.y, point.z + REACTION_LOCK_OFFSET
    rod_boss = _x_cylinder(REACTION_ROD_BOSS_DIAMETER, 2.0, x, point.y, point.z)
    lock_boss = _x_cylinder(REACTION_LOCK_BOSS_DIAMETER, 2.0, x, lock_y, lock_z)
    connector = _obround_x(
        (point.y, point.z), (lock_y, lock_z), 5.0, x, 2.0
    )
    body = rod_boss + lock_boss + connector
    body = body - [
        _x_cylinder(ROD_BORE_DIAMETER, 4.0, x, point.y, point.z),
        _x_cylinder(3.4, 4.0, x, lock_y, lock_z),
    ]
    return _label(body, f"{side}_{kind}_reaction_carrier")


def build_left_drive_support(params: PrototypeParameters | None = None, wire_gauge: int = 12) -> Shape:
    """Fixed thrust/positive-stop block for the diagonal M4x40 drive."""

    params = params or DEFAULT_PARAMETERS
    opened = solve_mechanism(params=params, wire_gauge=wire_gauge, closure=0.0)
    p = opened.moving_rod_center
    x = -(params.outer_span / 2.0 + 5.5 + params.running_clearance_per_side)
    support_offset = 15.0
    drive_y = p.y + 6.0 + opened.moving_outward_unit.y * support_offset
    drive_z = p.z + 6.0 + opened.moving_outward_unit.z * support_offset
    body = Pos(x, drive_y, drive_z) * Cylinder(6.5, 8.0, rotation=(45, 0, 0))
    bore = Pos(x, drive_y, drive_z) * Cylinder(
        params.m4_clearance_diameter / 2.0, 50.0, rotation=(45, 0, 0)
    )
    return _label(body - bore, "left_m4x40_diagonal_thrust_support_positive_stop")


def build_left_frame_with_drive_support(
    params: PrototypeParameters | None = None, wire_gauge: int = 12
) -> Shape:
    """Monolithic fixed left body; the thrust support has positive overlap."""

    params = params or DEFAULT_PARAMETERS
    body = build_left_frame(params, wire_gauge) + build_left_drive_support(params, wire_gauge)
    opened = solve_mechanism(params=params, wire_gauge=wire_gauge, closure=0.0)
    p = opened.moving_rod_center
    drive_x = -(params.outer_span / 2.0 + 5.5 + params.running_clearance_per_side)
    support_offset = 15.0
    tunnel_y = p.y + 6.0 + opened.moving_outward_unit.y * support_offset
    tunnel_z = p.z + 6.0 + opened.moving_outward_unit.z * support_offset
    tunnel = Pos(drive_x, tunnel_y, tunnel_z) * Cylinder(
        params.m4_clearance_diameter / 2.0, 60.0, rotation=(45, 0, 0)
    )
    body = body - tunnel
    return _label(body, "left_ribbed_side_frame_with_diagonal_drive_support")


def build_m4_drive_reference(params: PrototypeParameters | None = None, wire_gauge: int = 12) -> Shape:
    """Reference-only M4x40 screw on the solver's diagonal drive axis."""

    params = params or DEFAULT_PARAMETERS
    closed = solve_mechanism(params=params, wire_gauge=wire_gauge, closure=1.0)
    opened = solve_mechanism(params=params, wire_gauge=wire_gauge, closure=0.0)
    start_y, start_z = closed.moving_closed_center.y + 6.0, closed.moving_closed_center.z + 6.0
    far_distance = params.moving_stroke + 25.0
    far_y = start_y + opened.moving_outward_unit.y * far_distance
    far_z = start_z + opened.moving_outward_unit.z * far_distance
    screw = Pos(
        -(params.outer_span / 2.0 + 5.5 + params.running_clearance_per_side),
        (start_y + far_y) / 2.0,
        (start_z + far_z) / 2.0,
    ) * Cylinder(
        params.m4_screw_diameter / 2.0, 40.0, rotation=(45, 0, 0)
    )
    return _label(screw, "reference_m4x40_diagonal_drive_screw")


def build_xt60_bridge(params: PrototypeParameters | None = None) -> Shape:
    """Removable upper collar with the solder-cup and wire region fully open."""

    params = params or DEFAULT_PARAMETERS
    connector_w = _value(params, ("xt60_width", "xt60_envelope_width"), XT60_ENVELOPE[0])
    connector_d = _value(params, ("xt60_depth", "xt60_envelope_depth"), XT60_ENVELOPE[1])
    clearance = _value(
        params,
        ("cradle_clearance_per_side", "xt60_side_clearance", "connector_side_clearance"),
        XT60_SIDE_CLEARANCE,
    )
    pocket_w = connector_w + 2.0 * clearance
    pocket_d = connector_d + 2.0 * clearance

    # The collar begins above the upper rod and surrounds only the connector's
    # upper half. Thin end tabs stop 0.25 mm from the inner frame faces.
    bridge_width = params.clear_span - 2.0 * params.running_clearance_per_side
    collar_z = 8.0
    cheek_x = bridge_width / 2.0 - 2.25
    outer = Pos(0, 0, collar_z) * Box(bridge_width, pocket_d + 4.0, 4.0)
    tabs = [Pos(x, 0, collar_z) * Box(4.5, pocket_d + 4.0, 12.0) for x in (-cheek_x, cheek_x)]
    pocket = Pos(0, 0, collar_z) * Box(pocket_w, pocket_d, 6.0)
    body = (outer + tabs) - pocket
    setting_holes = [
        _x_cylinder(3.4, 4.5, x, 0.0, z)
        for x in (-cheek_x, cheek_x)
        for z in (3.0, 7.0, 11.0)
    ]
    body = body - setting_holes
    return _label(body, "removable_xt60_bridge_cradle")


def build_cold_iron_keepout_reference() -> Shape:
    """Reference-only cold-iron approach envelope ending at the pad edge."""

    keepout = Pos(0, -18.0, 16.0) * Cylinder(6.0, 24.0, rotation=(90, 0, 0))
    return _label(keepout, "reference_cold_soldering_iron_keepout")


build_bridge = build_xt60_bridge
build_cradle = build_xt60_bridge


def build_knob(params: PrototypeParameters | None = None) -> Shape:
    """Printable drive knob with M4 clearance and eight positive grip ribs."""

    body = Cylinder(5.0, 8.0)
    for angle in range(0, 360, 45):
        body = body + (Pos(0, 0, 2.0) * Box(3.0, 12.0, 8.0, rotation=(0, 0, angle)))
    body = body - Cylinder(2.5, 30.0)
    return _label(body, "m4_drive_knob")


def build_end_cap(params: PrototypeParameters | None = None) -> Shape:
    """Press-on cap for one user-supplied 4 mm rod."""

    cap = Cylinder(4.0, 5.0)
    cap = cap + (Pos(0, 0, 3.0) * Cylinder(5.2, 2.0))
    cap = cap - (Pos(0, 0, -0.6) * Cylinder(2.0, 4.8))
    return _label(cap, "rod_end_cap")


def build_fit_coupon(params: PrototypeParameters | None = None) -> Shape:
    """One coupon containing 4.2, 4.3, 4.4 and 4.5 mm bores and slots."""

    body = Box(66.0, 34.0, 4.0)
    xs = (-24.0, -8.0, 8.0, 24.0)
    bores = [Pos(x, -9.0, 0.0) * Cylinder(d / 2.0, 6.0) for x, d in zip(xs, FIT_SIZES)]
    slots = [
        Pos(x, 9.0, 0.0) * Box(10.0 - d, d, 6.0)
        + Pos(x - (10.0 - d) / 2.0, 9.0, 0.0) * Cylinder(d / 2.0, 6.0)
        + Pos(x + (10.0 - d) / 2.0, 9.0, 0.0) * Cylinder(d / 2.0, 6.0)
        for x, d in zip(xs, FIT_SIZES)
    ]
    body = body - [*bores, *slots]
    return _label(body, "rod_bore_and_slot_fit_coupon_4p2_to_4p5")


def build_reference_rod(y: float = 0.0, z: float = 0.0, label: str = "reference_rod") -> Shape:
    rod = _x_cylinder(ROD_DIAMETER, 50.0, 0.0, y, z)
    return _label(rod, label)


def build_reference_rods(
    upper: tuple[float, float] = (18.0, 31.0),
    lower: tuple[float, float] = (-5.0, 3.5),
    moving: tuple[float, float] = (1.0, 20.0),
) -> Compound:
    rods = [
        build_reference_rod(*upper, "reference_upper_reaction_rod"),
        build_reference_rod(*lower, "reference_lower_reaction_rod"),
        build_reference_rod(*moving, "reference_moving_forming_rod"),
    ]
    return Compound(children=rods, label="reference_three_rod_set")


def build_esc_reference() -> Shape:
    return _label(Box(36.0, 36.0, 3.0), "reference_bottom_36x36_esc")


def build_fc_reference() -> Shape:
    return _label(Box(30.5, 30.5, 2.0), "reference_upper_flight_controller")


def build_xt60_reference(params: PrototypeParameters | None = None) -> Shape:
    params = params or DEFAULT_PARAMETERS
    # The insulating body begins above 5 mm solder cups.  The full requested
    # 15.9 x 8.1 x 20.5 body envelope is retained while the cups meet the wire
    # endpoints without colliding with the upper reaction rod.
    body = Pos(0, 0, 5.0) * Box(
        params.xt60_width,
        params.xt60_depth,
        params.xt60_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    cups = [Pos(x, 0, 2.5) * Cylinder(1.5, 5.0) for x in (-4.0, 4.0)]
    return _label(
        body + cups,
        "reference_xt60_body_15p9x8p1x20p5_with_5mm_solder_cups",
    )


def build_wire_centerline(
    x: float = 0.0,
    params: PrototypeParameters | None = None,
    wire_gauge: int = 12,
    upper_index: int = 1,
    lower_index: int = 1,
    closure: float = 1.0,
) -> Wire:
    """Exact R6 centerline: horizontal pad lead, quarter arc, vertical leg."""

    params = params or DEFAULT_PARAMETERS
    solution = solve_mechanism(
        params=params,
        wire_gauge=wire_gauge,
        closure=closure,
        upper_index=upper_index,
        lower_index=lower_index,
    )
    start = solution.wire_path[0]
    endpoint = solution.wire_path[-1]
    if closure == 0.0:
        with BuildLine(Plane.YZ) as path:
            Line((start.y, start.z), (endpoint.y, endpoint.z))
        return Pos(x, 0.0, 0.0) * Wire(path.line.edges())
    with BuildLine(Plane.YZ) as path:
        Line((start.y, start.z), (solution.bend_start.y, solution.bend_start.z))
        CenterArc(
            (solution.bend_center.y, solution.bend_center.z),
            params.bend_radius,
            -90.0,
            90.0,
        )
        Line(
            (solution.vertical_leg_start.y, solution.vertical_leg_start.z),
            (endpoint.y, endpoint.z),
        )
    return Pos(x, 0.0, 0.0) * Wire(path.line.edges())


def build_wire_reference(
    x: float,
    diameter: float | None = None,
    params: PrototypeParameters | None = None,
    wire_gauge: int = 12,
    upper_index: int = 1,
    lower_index: int = 1,
    closure: float = 1.0,
) -> Shape:
    """Solid 90 degree lead swept along the frozen, tangent R6 centerline."""

    params = params or DEFAULT_PARAMETERS
    solution = solve_mechanism(
        params=params,
        wire_gauge=wire_gauge,
        closure=closure,
        upper_index=upper_index,
        lower_index=lower_index,
    )
    diameter = diameter if diameter is not None else solution.wire_diameter
    centerline = build_wire_centerline(x, params, wire_gauge, upper_index, lower_index, closure)
    start = solution.wire_path[0]
    start_plane = Plane(origin=(x, start.y, start.z), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    with BuildSketch(start_plane) as profile:
        Circle(diameter / 2.0)
    wire = sweep(profile.sketch, centerline)
    return _label(wire, f"reference_90_degree_wire_{x:+.1f}")


def build_wires_reference(
    params: PrototypeParameters | None = None,
    wire_gauge: int = 12,
    upper_index: int = 1,
    lower_index: int = 1,
    closure: float = 1.0,
) -> Compound:
    return Compound(
        children=[
            build_wire_reference(-4.0, params=params, wire_gauge=wire_gauge, upper_index=upper_index, lower_index=lower_index, closure=closure),
            build_wire_reference(4.0, params=params, wire_gauge=wire_gauge, upper_index=upper_index, lower_index=lower_index, closure=closure),
        ],
        label="reference_simplified_90_degree_wires",
    )


__all__ = [
    "ADJUSTMENT_PITCH",
    "FIT_SIZES",
    "FORMING_SLOT_WIDTH",
    "FRAME_CLEAR_SPAN",
    "FRAME_OUTER_SPAN",
    "FRAME_THICKNESS",
    "NUT_TRAP_AF",
    "REACTION_INSERT_POCKET_DEPTH",
    "REACTION_INSERT_POCKET_DIAMETER",
    "REACTION_LOCK_BOSS_DIAMETER",
    "REACTION_LOCK_OFFSET",
    "REACTION_ROD_BOSS_DIAMETER",
    "ROD_BORE_DIAMETER",
    "ROD_DIAMETER",
    "SLIDER_COLLAR_DIAMETER",
    "XT60_ENVELOPE",
    "XT60_SIDE_CLEARANCE",
    "WIRE_BEND_RADIUS",
    "WIRE_HORIZONTAL_Z",
    "WIRE_TANGENT_START_Y",
    "WIRE_VERTICAL_TANGENT_Y",
    "build_bridge",
    "build_cold_iron_keepout_reference",
    "build_cradle",
    "build_end_cap",
    "build_esc_reference",
    "build_fc_reference",
    "build_fit_coupon",
    "build_knob",
    "build_left_frame",
    "build_left_drive_support",
    "build_left_frame_with_drive_support",
    "build_left_side_frame",
    "build_left_slider",
    "build_reference_rod",
    "build_reference_rods",
    "build_right_frame",
    "build_right_side_frame",
    "build_right_slider",
    "build_reaction_carrier",
    "build_m4_drive_reference",
    "build_side_frame",
    "build_slider",
    "build_wire_reference",
    "build_wire_centerline",
    "build_wires_reference",
    "build_xt60_bridge",
    "build_xt60_reference",
]
