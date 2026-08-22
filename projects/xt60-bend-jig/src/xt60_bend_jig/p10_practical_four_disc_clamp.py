"""P10 practical four-disc clamp for a manually pre-bent XT60 pigtail.

P10 preserves P9's three-rod kinematics.  It adds a datum base, a removable
one-piece solder locator, exact cam hard stops, a removable wheel, positive
shaft retention, and phase-specific removal poses.  The L-shaped workpiece is
fixed at every cam angle; this model does not claim to bend a straight wire.
"""

from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from functools import lru_cache
from math import atan2, cos, degrees, hypot, pi, radians, sin, sqrt, tan
from typing import Literal

from build123d import (
    Align, Box, Compound, Cylinder, Face, Pos, Rot, Shape, Sphere, Vector, Wire,
    extrude,
)
from cadgen import srgb

from xt60_bend_jig.p2_corner_clamp import (
    PointYZ, build_wire_centerline, build_wires as _p2_build_wires,
    build_xt60 as _p2_build_xt60,
)
from xt60_bend_jig.p7_three_rod_scroll import (
    P7Parameters, _rotate_about_shaft, _straight_slot_solid_x, _x_cylinder,
    _x_hex_prism, inverse_slot_point, rod_center, slot_path, smoothstep01,
    travel_at_angle,
)
from xt60_bend_jig.p9_four_disc_three_rod import build_cam_slot_tool


RodName = Literal["upright", "bottom", "diagonal"]
Side = Literal["left", "right"]
EnvelopeState = Literal["as_printed", "seated_envelope"]
ROD_NAMES: tuple[RodName, ...] = ("upright", "bottom", "diagonal")


@dataclass(frozen=True, slots=True)
class P10Parameters(P7Parameters):
    scroll_diameter: float = 64.0
    shaft_y: float = -7.5
    shaft_z: float = 32.5
    fixed_plate_thickness: float = 3.0
    scroll_plate_thickness: float = 3.0
    scroll_axial_clearance: float = 0.30
    clear_span: float = 32.0
    guide_slot_width: float = 4.4
    scroll_slot_width: float = 4.4
    shaft_bore_diameter: float = 6.50
    scroll_hex_socket_across_corners: float = 6.25
    axial_float: float = 0.20
    base_x: float = 44.0
    base_y: float = 22.0
    base_z: float = 8.0
    locator_disengage_x: float = 46.0
    locator_park_x: float = 80.0
    pin_travel_x: float = 20.0
    keeper_travel_y: float = -6.0
    rod_withdraw_x: float = -55.0
    assembly_remove_y: float = -80.0
    wheel_radius: float = 16.0
    wheel_socket: float = 6.25
    wheel_notch: float = 6.30
    lock_radius: float = 15.50
    lock_local_angle: float = 200.0

    @property
    def stop_radial(self) -> float:
        return 34.0

    @property
    def stop_tangent(self) -> float:
        return 3.0

    @property
    def stop_arm_angle(self) -> float:
        return self.end_angle + degrees(atan2(self.stop_tangent, self.stop_radial))

    @property
    def stop_pin_radius(self) -> float:
        return hypot(self.stop_radial, self.stop_tangent)

    @property
    def stop_pin_y(self) -> float:
        angle = radians(self.end_angle)
        return self.shaft_y + cos(angle) * self.stop_radial - sin(angle) * self.stop_tangent

    @property
    def stop_pin_z(self) -> float:
        angle = radians(self.end_angle)
        return self.shaft_z + sin(angle) * self.stop_radial + cos(angle) * self.stop_tangent


P10_DEFAULTS = P10Parameters()


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def _box(center, size) -> Shape:
    return Pos(*center) * Box(*size, align=(Align.CENTER, Align.CENTER, Align.CENTER))


def _fuse(shapes: list[Shape]) -> Shape:
    result = shapes[0]
    for shape in shapes[1:]:
        result = result + shape
    return result


def _radial_bar_x(
    x: float, depth: float, r_min: float, r_max: float, tangent_width: float,
    angle_deg: float, params: P10Parameters,
) -> Shape:
    bar = Pos(x, params.shaft_y + (r_min + r_max) / 2.0, params.shaft_z) * Box(
        depth, r_max - r_min, tangent_width,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return _rotate_about_shaft(bar, angle_deg, params)


def lock_local_point(params: P10Parameters = P10_DEFAULTS) -> PointYZ:
    a = radians(params.lock_local_angle)
    return PointYZ(params.shaft_y + params.lock_radius * cos(a), params.shaft_z + params.lock_radius * sin(a))


def lock_world_point(params: P10Parameters = P10_DEFAULTS) -> PointYZ:
    q = lock_local_point(params)
    a = radians(params.end_angle)
    dy, dz = q.y - params.shaft_y, q.z - params.shaft_z
    return PointYZ(params.shaft_y + cos(a) * dy - sin(a) * dz,
                   params.shaft_z + sin(a) * dy + cos(a) * dz)


def _outboard_rib(side: Side, y_center: float, params: P10Parameters) -> Shape:
    sign = -1.0 if side == "left" else 1.0
    x_face = sign * 19.0
    proud = 0.35
    z0, z1 = -3.75, -1.25
    lead = proud / tan(radians(30.0))
    points = [
        Vector(x_face, y_center - 0.4, z0),
        Vector(x_face + sign * proud, y_center - 0.4, z0 + lead),
        Vector(x_face + sign * proud, y_center - 0.4, z1 - lead),
        Vector(x_face, y_center - 0.4, z1),
    ]
    return extrude(Face(Wire.make_polygon(points)), amount=0.8, dir=(0.0, 1.0, 0.0))


def _rear_rib(side: Side, local_x: float, params: P10Parameters) -> Shape:
    x_center = (-17.5 if side == "left" else 17.5) + local_x
    y_face, proud = -14.5, 0.40
    z0, z1 = -3.75, -1.25
    lead = proud / tan(radians(30.0))
    points = [
        Vector(x_center - 0.3, y_face, z0),
        Vector(x_center - 0.3, y_face - proud, z0 + lead),
        Vector(x_center - 0.3, y_face - proud, z1 - lead),
        Vector(x_center - 0.3, y_face, z1),
    ]
    return extrude(Face(Wire.make_polygon(points)), amount=0.6, dir=(1.0, 0.0, 0.0))


def build_base(params: P10Parameters = P10_DEFAULTS) -> Shape:
    body = _box((0.0, -7.5, -4.5), (44.0, 22.0, 8.0))
    mortises = [
        _box((-17.625, -7.65, -2.60), (3.25, 14.30, 4.20)),
        _box((17.625, -7.65, -2.60), (3.25, 14.30, 4.20)),
    ]
    t_main = _box((0.0, 1.60, -4.50), (46.0, 2.30, 3.30))
    t_neck = _box((0.0, 3.00, -3.40), (46.0, 1.50, 1.80))
    return _label(body - mortises - t_main - t_neck,
                  "shared_base_44x22x8_two_mortises_transverse_T_cavity", "#41484A")


def _fixed_disc_core(side: Side, params: P10Parameters) -> tuple[Shape, Shape, list[Shape]]:
    """Return the robust core, tongue/root, and shoulders before ribs/tools."""
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.fixed_plate_center_x
    depth = params.fixed_plate_thickness
    disc = _x_cylinder(params.scroll_diameter, depth, x, params.shaft_y, params.shaft_z)
    # Engaged tongue is Z=-4.5..-0.5; the extra 0.25 mm is the frozen
    # volumetric root, not additional mortise engagement.
    tongue_root = _box((x, -7.5, -2.375), (3.0, 14.0, 4.25))
    shoulders = [
        _box((x, -15.525, 0.85), (3.0, 2.55, 2.70)),
        _box((x, 0.375, 0.85), (3.0, 2.25, 2.70)),
    ]
    return _fuse([disc, tongue_root, *shoulders]), tongue_root, shoulders


@lru_cache(maxsize=4)
def _fixed_disc_prototype(side: Side, state: EnvelopeState, params: P10Parameters) -> Shape:
    if side not in ("left", "right") or state not in ("as_printed", "seated_envelope"):
        raise ValueError("invalid side or envelope state")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.fixed_plate_center_x
    depth = params.fixed_plate_thickness
    core, _, _ = _fixed_disc_core(side, params)
    arm = _radial_bar_x(x, depth, 30.5, 34.2, 3.0, params.stop_arm_angle, params)
    stop_x = sign * 20.4
    stop_pin = _x_cylinder(3.0, 4.8, stop_x, params.stop_pin_y, params.stop_pin_z)
    ribs = [
        _outboard_rib(side, -11.0, params), _outboard_rib(side, -4.0, params),
        _rear_rib(side, -0.75, params), _rear_rib(side, 0.75, params),
    ]
    raw = _fuse([core, arm, stop_pin, *ribs])
    tools: list[Shape] = []
    for name in ROD_NAMES:
        tools.append(_straight_slot_solid_x(
            rod_center(name, 0.0, params), rod_center(name, params.end_angle, params),
            params.guide_slot_width, x, depth + 2.0,
        ))
    tools.append(_x_cylinder(params.shaft_bore_diameter, depth + 2.0, x, params.shaft_y, params.shaft_z))
    if side == "right":
        lock = lock_world_point(params)
        tools.append(_x_cylinder(3.2, depth + 2.0, x, lock.y, lock.z))
    result = raw - tools
    if state == "seated_envelope":
        result = result - build_base(params)
    return result


def build_fixed_disc(
    side: Side, state: EnvelopeState = "as_printed", params: P10Parameters = P10_DEFAULTS,
) -> Shape:
    result = copy(_fixed_disc_prototype(side, state, params))
    return _label(result, f"{side}_fixed_disc_integral_stop_tongue_crush_ribs_{state}", "#39704C")


@lru_cache(maxsize=2)
def _cam_disc_prototype(side: Side, params: P10Parameters) -> Shape:
    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.scroll_plate_center_x
    depth = params.scroll_plate_thickness
    disc = _x_cylinder(params.scroll_diameter, depth, x, params.shaft_y, params.shaft_z)
    tab = _radial_bar_x(x, depth, 31.0, 36.0, 3.0, 0.0, params)
    raw = disc + tab
    if side == "left":
        # Functional keeper thrust face X=-22.50..-22.30; the final 0.05 mm
        # roots the boss into the cam ending at X=-22.25.
        raw = raw + _x_cylinder(10.0, 0.25, -22.375, params.shaft_y, params.shaft_z)
    tools: list[Shape] = [build_cam_slot_tool(name, side, params) for name in ROD_NAMES]
    tools.append(_x_hex_prism(params.scroll_hex_socket_across_corners, depth + 2.0, x, params.shaft_y, params.shaft_z))
    if side == "right":
        lock = lock_local_point(params)
        tools.append(_x_cylinder(3.2, depth + 2.0, x, lock.y, lock.z))
    return raw - tools


def build_cam_disc(side: Side, params: P10Parameters = P10_DEFAULTS) -> Shape:
    result = copy(_cam_disc_prototype(side, params))
    boss = "_thrust_boss_10OD_Xm22p50_to_m22p25" if side == "left" else ""
    return _label(result, f"{side}_cam_disc_three_inverse_slots_integral_80deg_stop_tab{boss}", "#D69B16")


def build_rod(name: RodName, angle_deg: float, x_shift: float = 0.0, params: P10Parameters = P10_DEFAULTS) -> Shape:
    point = rod_center(name, angle_deg, params)
    return _label(_x_cylinder(4.0, 50.0, x_shift, point.y, point.z),
                  f"purchased_304_stainless_{name}_rod_4x50", "#BCC5CA")


def build_rods(angle_deg: float, x_shift: float = 0.0, params: P10Parameters = P10_DEFAULTS) -> Compound:
    return Compound(children=[build_rod(name, angle_deg, x_shift, params) for name in ROD_NAMES],
                    label=f"exactly_three_rods_angle_{angle_deg:g}_xshift_{x_shift:g}")


def _locator_box_specs() -> list[tuple[str, tuple[float, float, float], tuple[float, float, float]]]:
    specs = [
        ("main_T_rail", (-0.25, 1.75, -4.65), (44.90, 2.00, 3.00)),
        ("T_neck_open_clearance", (-0.25, 3.00, -3.40), (44.90, 1.20, 1.50)),
        ("insertion_shoulder", (23.0, 2.0, -4.5), (2.0, 3.0, 4.0)),
    ]
    for x in (-8.5, 8.5):
        specs.extend((
            (f"runner_{x:+g}", (x, 14.1, -2.3), (2.5, 21.2, 3.0)),
            (f"lower_post_{x:+g}", (x, 25.675, 10.5), (2.5, 2.65, 28.6)),
            (f"upper_neck_{x:+g}", (x, 25.45, 26.275), (2.5, 1.0, 3.15)),
        ))
    specs.extend((
        ("upper_bridge", (0.0, 25.45, 26.65), (19.5, 1.0, 2.2)),
        ("left_wire_shelf", (-4.0, 25.45, 27.25), (4.6, 1.0, 1.2)),
        ("right_wire_shelf", (4.0, 25.45, 27.25), (4.6, 1.0, 1.2)),
        ("right_wire_fence", (6.65, 25.7, 29.025), (1.0, 1.0, 2.75)),
        ("right_ESC_edge_tab", (8.5, 26.9, 25.8), (2.5, 2.2, 3.0)),
        ("withdrawal_grip", (15.75, 25.675, 16.0), (12.5, 2.65, 6.0)),
    ))
    return specs


def _locator_wedge(as_printed: bool = True) -> Shape:
    rear_y = 0.40 if as_printed else 0.45
    points = [
        Vector(16.0, 0.75, -5.05), Vector(20.0, rear_y, -5.05),
        Vector(22.0, rear_y, -5.05), Vector(22.0, 0.75, -5.05),
    ]
    return extrude(Face(Wire.make_polygon(points)), amount=0.8, dir=(0.0, 0.0, 1.0))


def build_locator(
    state: EnvelopeState = "as_printed", x_shift: float = 0.0,
    params: P10Parameters = P10_DEFAULTS,
) -> Shape:
    if state not in ("as_printed", "seated_envelope"):
        raise ValueError("invalid locator envelope state")
    pieces = [_box(center, size) for _, center, size in _locator_box_specs()]
    pieces.append(_locator_wedge(as_printed=state == "as_printed"))
    locator = _fuse(pieces)
    if state == "seated_envelope":
        locator = locator - build_base(params)
    locator = Pos(x_shift, 0.0, 0.0) * locator
    return _label(locator, f"one_piece_open_locator_{state}_xshift_{x_shift:g}", "#3D7E9D")


def build_locator_swept_volume(
    distance: float = 80.0, params: P10Parameters = P10_DEFAULTS,
) -> Shape:
    """Exact union of the axis-aligned locator component translation sweeps."""
    swept: list[Shape] = []
    for _, center, size in _locator_box_specs():
        swept.append(_box((center[0] + distance / 2.0, center[1], center[2]),
                          (size[0] + abs(distance), size[1], size[2])))
    # Seated wedge envelope is monotone in X and sweeps inside the T cavity.
    swept.append(_box(((16.0 + 22.0 + distance) / 2.0, 0.60, -4.65),
                      (6.0 + abs(distance), 0.30, 0.8)))
    return _label(_fuse(swept), f"exact_locator_plusX_swept_volume_{distance:g}", "#74AFC8")


def build_shaft(angle_deg: float = 0.0, params: P10Parameters = P10_DEFAULTS) -> Shape:
    main = _x_hex_prism(6.0, 53.9, 4.65, params.shaft_y, params.shaft_z)  # -22.30..31.60
    neck = _x_cylinder(5.2, 3.5, -23.95, params.shaft_y, params.shaft_z)  # -25.70..-22.20
    shoulder = _x_hex_prism(6.0, 1.6, -26.40, params.shaft_y, params.shaft_z)  # -27.20..-25.60
    collar = _x_cylinder(9.0, 2.05, 23.475, params.shaft_y, params.shaft_z)  # 22.45..24.50
    result = _rotate_about_shaft(main + neck + shoulder + collar, angle_deg, params)
    return _label(result,
                  f"shared_keyed_shaft_right_collar_left_round_neck_terminal_shoulder_{angle_deg:g}deg", "#22282B")


def build_shaft_keeper(params: P10Parameters = P10_DEFAULTS) -> Shape:
    x = -24.0
    outer = _x_cylinder(10.0, 3.0, x, params.shaft_y, params.shaft_z)
    pocket = _x_cylinder(5.4, 4.0, x, params.shaft_y, params.shaft_z)
    opening = _box((x, params.shaft_y + 5.0, params.shaft_z), (4.0, 10.0, 4.7))
    return _label(outer - pocket - opening,
                  "removable_left_shaft_C_keeper_5p4_pocket_4p7_throat", "#51595C")


def _wheel_index_groove(params: P10Parameters) -> Shape:
    # Local +10 degree radial cut; after 80 degree shaft rotation it is world +90.
    groove = _radial_bar_x(31.8, 0.6, 10.5, 15.5, 0.8, 10.0, params)
    return groove


def build_wheel(
    angle_deg: float = 0.0, state: EnvelopeState = "as_printed",
    params: P10Parameters = P10_DEFAULTS,
) -> Shape:
    body = _x_cylinder(32.0, 6.0, 29.0, params.shaft_y, params.shaft_z)
    socket = _x_hex_prism(params.wheel_socket, 5.8, 28.9, params.shaft_y, params.shaft_z)
    notch = lock_local_point(params)
    notch_tool = _x_cylinder(params.wheel_notch, 8.0, 29.0, notch.y, notch.z)
    wheel = body - socket - notch_tool - _wheel_index_groove(params)
    # Two opposite shallow ribs project into the provisional socket.
    apothem = params.wheel_socket * cos(pi / 6.0) / 2.0
    ribs = [
        _box((28.0, params.shaft_y, params.shaft_z + sign * (apothem - 0.075)), (4.0, 0.8, 0.15))
        for sign in (-1.0, 1.0)
    ]
    wheel = wheel + ribs
    if state == "seated_envelope":
        wheel = wheel - build_shaft(0.0, params)
    wheel = _rotate_about_shaft(wheel, angle_deg, params)
    return _label(wheel, f"removable_thumbwheel_notched_indexed_socket_ribs_{state}_{angle_deg:g}deg", "#2A3032")


def build_lock_pin(parked: bool = False, params: P10Parameters = P10_DEFAULTS) -> Shape:
    point = lock_world_point(params)
    shift = params.pin_travel_x if parked else 0.0
    shaft = _x_cylinder(3.0, 18.0, 24.0 + shift, point.y, point.z)
    head = _x_cylinder(5.5, 2.0, 34.0 + shift, point.y, point.z)
    return _label(shaft + head,
                  f"lengthened_lock_pin_{'axial_parking' if parked else 'engaged'}_xshift_{shift:g}", "#A03737")


def build_left_cap(point: PointYZ, x_shift: float = 0.0, params: P10Parameters = P10_DEFAULTS) -> Shape:
    inner = -22.5 + x_shift
    body = _x_cylinder(7.0, 4.0, inner - 2.0, point.y, point.z)
    socket = _x_cylinder(3.90, 2.9, inner - 1.45, point.y, point.z)
    return _label(body - socket, "P10_left_cap_3p90_trial_engagement2p5_float0p20", "#C88714")


def build_right_keeper(
    point: PointYZ, y_shift: float = 0.0, params: P10Parameters = P10_DEFAULTS,
) -> Shape:
    x = 23.95
    outer = _x_cylinder(7.0, 2.9, x, point.y, point.z)
    pocket = _x_cylinder(4.10, 3.9, x, point.y, point.z)
    opening = _box((x, point.y + 3.5, point.z), (3.9, 7.0, 3.60))
    return _label(Pos(0.0, y_shift, 0.0) * (outer - pocket - opening),
                  f"P10_right_keeper_4p10_3p60_plusY_throat_float0p20_yshift_{y_shift:g}", "#E0AE35")


def build_retainers(
    angle_deg: float, right_y_shift: float = 0.0, left_x_shift: float = 0.0,
    params: P10Parameters = P10_DEFAULTS,
) -> Compound:
    parts: list[Shape] = []
    for name in ROD_NAMES:
        point = rod_center(name, angle_deg, params)
        parts.extend((build_left_cap(point, left_x_shift, params),
                      build_right_keeper(point, right_y_shift, params)))
    return Compound(children=parts, label="three_P10_left_caps_three_P10_right_keepers")


def build_electronics_reference() -> Compound:
    esc = _label(_box((0.0, 46.0, 25.75), (36.0, 36.0, 3.5)), "reference_bottom_ESC", "#25292B")
    fc = _label(_box((0.0, 46.0, 42.0), (30.5, 30.5, 2.0)), "reference_FC_above_ESC", "#4C5860")
    children: list[Shape] = [esc, fc]
    for x, name in ((-4.0, "negative"), (4.0, "positive")):
        pad = _box((x, 30.5, 27.675), (5.0, 5.0, 0.35))
        solder = Pos(x, 30.5, 28.0) * Sphere(1.6)
        children.extend((
            _label(pad, f"reference_{name}_copper_pad_center_Y30p5_top_Z27p85", "#D89A30"),
            _label(solder, f"reference_{name}_solder", "#C1C7C9"),
        ))
    return Compound(children=children, label="ESC_FC_pads_solder_reference")


def build_fixed_L_workpiece() -> Compound:
    wires = _p2_build_wires()
    wires.label = "same_fixed_prebent_L_insulated_pigtail_every_pose"
    xt60 = _p2_build_xt60()
    xt60.label = "reference_vertical_XT60_assumed_envelope"
    conductors: list[Shape] = []
    for x, color in ((-4.0, "#D3B274"), (4.0, "#D3B274")):
        conductor = Pos(x, 30.5, 30.0) * Cylinder(
            1.15, 5.0, rotation=(90.0, 0.0, 0.0),
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        conductors.append(_label(conductor, f"tinned_conductor_x{x:+g}_D2p3_Y28to33", color))
    return Compound(children=[wires, *conductors, xt60],
                    label="fixed_90deg_pigtail_two_5mm_stripped_conductors_XT60")


def contact_band(
    name: RodName, params: P10Parameters = P10_DEFAULTS,
) -> tuple[PointYZ, PointYZ]:
    """Return the frozen wire-contact center and path tangent in YZ."""

    if name not in ROD_NAMES:
        raise ValueError(f"unknown rod name: {name}")
    diagonal = 6.0 * (1.0 - 1.0 / sqrt(2.0))
    centers = {
        "upright": PointYZ(0.0, 42.0),
        "bottom": PointYZ(12.0, 30.0),
        "diagonal": PointYZ(diagonal, 30.0 + diagonal),
    }
    tangents = {
        "upright": PointYZ(0.0, 1.0),
        "bottom": PointYZ(-1.0, 0.0),
        "diagonal": PointYZ(-1.0 / sqrt(2.0), 1.0 / sqrt(2.0)),
    }
    return centers[name], tangents[name]


def build_solder_access_corridor(params: P10Parameters = P10_DEFAULTS) -> Shape:
    """Conservative locked-state iron-tip and hand corridor after locator removal.

    The tip tunnel covers both X=+/-4 mm solder legs from the pad edge toward
    +Y.  The overlapping hand box provides a larger grasp envelope beyond the
    ESC reference.  Electronics and the intended wire contact are deliberately
    not treated as obstacles; the structural jig is.
    """

    tip_tunnel = _box((0.0, 51.5, 30.5), (16.0, 47.0, 5.0))
    hand_envelope = _box((0.0, 78.0, 34.0), (30.0, 16.0, 18.0))
    return _label(tip_tunnel + hand_envelope,
                  "locked_locator_removed_solder_tip_and_hand_access_corridor", "#7FB7D8")


def build_solder_target_envelope(params: P10Parameters = P10_DEFAULTS) -> Compound:
    """Two frozen conductor bounding envelopes reached by the iron corridor."""

    children = [
        _label(_box((x, 30.5, 30.0), (2.3, 5.0, 2.3)),
               f"solder_target_conductor_envelope_x{x:+g}", "#D3B274")
        for x in (-4.0, 4.0)
    ]
    return Compound(children=children, label="two_frozen_solder_target_envelopes")


def build_principal_plates(
    angle_deg: float, state: EnvelopeState = "seated_envelope", y_shift: float = 0.0,
    params: P10Parameters = P10_DEFAULTS,
) -> Compound:
    parts: list[Shape] = [
        build_fixed_disc("left", state, params),
        _rotate_about_shaft(build_cam_disc("left", params), angle_deg, params),
        build_fixed_disc("right", state, params),
        _rotate_about_shaft(build_cam_disc("right", params), angle_deg, params),
    ]
    if y_shift:
        parts = [Pos(0.0, y_shift, 0.0) * part for part in parts]
    return Compound(children=parts, label=f"four_principal_plates_{state}_angle_{angle_deg:g}_yshift_{y_shift:g}")


def _assembly_children(
    angle_deg: float,
    locator_x: float,
    pin_parked: bool,
    rod_x: float = 0.0,
    keeper_y: float = 0.0,
    core_y: float = 0.0,
    params: P10Parameters = P10_DEFAULTS,
) -> list[Shape]:
    base = Pos(0.0, core_y, 0.0) * build_base(params)
    plates = list(build_principal_plates(angle_deg, "seated_envelope", core_y, params).children)
    shaft = Pos(0.0, core_y, 0.0) * build_shaft(angle_deg, params)
    keeper = Pos(0.0, core_y, 0.0) * build_shaft_keeper(params)
    wheel = Pos(0.0, core_y, 0.0) * build_wheel(angle_deg, "seated_envelope", params)
    rods = list(build_rods(angle_deg, rod_x, params).children)
    retainers = list(build_retainers(angle_deg, keeper_y, rod_x, params).children)
    return [base, *plates, *rods, *retainers, shaft, keeper, wheel,
            build_lock_pin(pin_parked, params), build_locator("seated_envelope", locator_x, params),
            build_electronics_reference(), build_fixed_L_workpiece()]


def build_loaded_open(params: P10Parameters = P10_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(0.0, 0.0, True, params=params),
                    label="p10_loaded_open_locator_supporting_fixed_prebent_pigtail")


def build_loaded_closed(params: P10Parameters = P10_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(80.0, 0.0, False, params=params),
                    label="p10_loaded_closed_80deg_stop_pin_engaged_locator_seated")


def build_locator_removed_closed(params: P10Parameters = P10_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(80.0, params.locator_park_x, False, params=params),
                    label="p10_closed_locator_removed_to_plus80_parking_pose")


def build_rods_withdrawn(params: P10Parameters = P10_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(
        0.0, params.locator_park_x, True,
        rod_x=params.rod_withdraw_x, keeper_y=params.keeper_travel_y, params=params),
        label="p10_reopened_right_keepers_removed_rods_left_caps_withdrawn_minus55")


def build_removal_clear(params: P10Parameters = P10_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(
        0.0, params.locator_park_x, True, rod_x=params.rod_withdraw_x,
        keeper_y=params.keeper_travel_y, core_y=params.assembly_remove_y, params=params),
        label="p10_final_base_four_plates_shaft_wheel_removed_minus80Y")


def build_lock_pin_swept_volume(params: P10Parameters = P10_DEFAULTS) -> Shape:
    point = lock_world_point(params)
    shaft_sweep = _x_cylinder(3.0, 38.0, 34.0, point.y, point.z)  # X15..53
    head_sweep = _x_cylinder(5.5, 22.0, 44.0, point.y, point.z)  # X33..55
    return _label(shaft_sweep + head_sweep, "exact_lock_pin_engaged_to_parked_plus20_sweep", "#C16969")


def build_keeper_swept_volume(
    name: RodName, angle_deg: float = 0.0, params: P10Parameters = P10_DEFAULTS,
) -> Shape:
    point = rod_center(name, angle_deg, params)
    end = PointYZ(point.y + params.keeper_travel_y, point.z)
    return _label(_straight_slot_solid_x(point, end, 7.0, 23.95, 2.9),
                  f"conservative_exact_outer_keeper_{name}_minus6Y_sweep", "#EDD06C")


def build_rod_cap_swept_volume(name: RodName, params: P10Parameters = P10_DEFAULTS) -> Shape:
    point = rod_center(name, 0.0, params)
    rod_sweep = _x_cylinder(4.0, 105.0, -27.5, point.y, point.z)
    cap_sweep = _x_cylinder(7.0, 59.0, -52.0, point.y, point.z)
    return _label(rod_sweep + cap_sweep, f"exact_{name}_rod_and_left_cap_minus55X_sweep", "#CBD3D6")


def _bbox_y_sweep(shape: Shape, distance: float) -> Shape:
    box = shape.bounding_box()
    return _box(((box.min.X + box.max.X) / 2.0,
                 (box.min.Y + box.max.Y + distance) / 2.0,
                 (box.min.Z + box.max.Z) / 2.0),
                (box.size.X, box.size.Y + abs(distance), box.size.Z))


def _final_core_proof_features(
    params: P10Parameters,
) -> list[tuple[str, Shape, Shape]]:
    """Return named outer primitives and valid conservative -Y sweeps.

    The fixed insertion feature is derived from the actual tongue and both
    shoulders.  Its Y bounds are therefore exactly [-16.8, 1.5], rather than a
    hand-entered approximation that could silently under-cover a shoulder.
    """

    dy = params.assembly_remove_y
    start = PointYZ(params.shaft_y, params.shaft_z)
    end = PointYZ(params.shaft_y + dy, params.shaft_z)
    base_outer = _box((0.0, -7.5, -4.5), (44.0, 22.0, 8.0))
    features: list[tuple[str, Shape, Shape]] = [
        ("base_outer", base_outer, _bbox_y_sweep(base_outer, dy)),
    ]
    for side in ("left", "right"):
        sign = -1.0 if side == "left" else 1.0
        fixed_x = sign * params.fixed_plate_center_x
        cam_x = sign * params.scroll_plate_center_x
        fixed_disc = _x_cylinder(
            params.scroll_diameter, params.fixed_plate_thickness,
            fixed_x, params.shaft_y, params.shaft_z,
        )
        fixed_arm = _radial_bar_x(
            fixed_x, params.fixed_plate_thickness,
            30.5, 34.2, 3.0, params.stop_arm_angle, params,
        )
        _, tongue, shoulders = _fixed_disc_core(side, params)
        # The seated fixed disc retains four small crush-rib remnants outside
        # the base.  They move with the final core and therefore belong in the
        # same declared insertion primitive as the tongue and shoulders.  Use
        # the actual rib builders and actual base subtraction so this proof
        # cannot silently drift from production geometry.
        seated_ribs = [
            rib - build_base(params)
            for rib in (
                _outboard_rib(side, -11.0, params),
                _outboard_rib(side, -4.0, params),
                _rear_rib(side, -0.75, params),
                _rear_rib(side, 0.75, params),
            )
        ]
        fixed_insert = _fuse([tongue, *shoulders, *seated_ribs])
        stop_pin = _x_cylinder(
            3.0, 4.8, sign * 20.4, params.stop_pin_y, params.stop_pin_z,
        )
        cam_disc = _x_cylinder(
            params.scroll_diameter, params.scroll_plate_thickness,
            cam_x, params.shaft_y, params.shaft_z,
        )
        cam_sweep = _straight_slot_solid_x(
            start, end, params.scroll_diameter, cam_x, params.scroll_plate_thickness,
        )
        if side == "left":
            boss_outer = _x_cylinder(10.0, 0.25, -22.375, params.shaft_y, params.shaft_z)
            cam_disc = cam_disc + boss_outer
            cam_sweep = cam_sweep + _straight_slot_solid_x(
                start, end, 10.0, -22.375, 0.25,
            )
        cam_tab = _radial_bar_x(
            cam_x, params.scroll_plate_thickness, 31.0, 36.0, 3.0, 0.0, params,
        )
        features.extend((
            (f"{side}_fixed_disc_outer", fixed_disc,
             _straight_slot_solid_x(start, end, params.scroll_diameter,
                                    fixed_x, params.fixed_plate_thickness)),
            (f"{side}_fixed_stop_arm_outer", fixed_arm, _bbox_y_sweep(fixed_arm, dy)),
            (f"{side}_fixed_tongue_shoulders_outer", fixed_insert,
             _bbox_y_sweep(fixed_insert, dy)),
            (f"{side}_fixed_stop_pin_outer", stop_pin,
             _straight_slot_solid_x(
                 PointYZ(params.stop_pin_y, params.stop_pin_z),
                 PointYZ(params.stop_pin_y + dy, params.stop_pin_z),
                 3.0, sign * 20.4, 4.8,
             )),
            (f"{side}_cam_disc_outer", cam_disc, cam_sweep),
            (f"{side}_cam_tab_outer", cam_tab, _bbox_y_sweep(cam_tab, dy)),
        ))
    shaft = build_shaft(0.0, params)
    keeper = build_shaft_keeper(params)
    wheel_outer = _x_cylinder(32.0, 6.0, 29.0, params.shaft_y, params.shaft_z)
    features.extend((
        ("shaft_complete", shaft, _bbox_y_sweep(shaft, dy)),
        ("shaft_keeper_complete", keeper, _bbox_y_sweep(keeper, dy)),
        ("wheel_outer", wheel_outer,
         _straight_slot_solid_x(start, end, 32.0, 29.0, 6.0)),
    ))
    return features


def build_final_core_moving_primitives(
    params: P10Parameters = P10_DEFAULTS,
) -> Compound:
    """The 16 named outer primitives covered by the final removal proof."""

    children: list[Shape] = []
    for name, primitive, _ in _final_core_proof_features(params):
        primitive.label = f"final_core_moving_primitive_{name}"
        primitive.color = srgb("#596164")
        children.append(primitive)
    return Compound(children=children, label="sixteen_final_core_moving_outer_primitives")


def build_final_core_swept_volume(params: P10Parameters = P10_DEFAULTS) -> Compound:
    """Valid continuous feature envelopes for the accepted -Y core removal.

    Each child is the exact translational sweep of a feature's outer primitive
    or a conservative superset of it.  Cuts are intentionally ignored.  A
    zero intersection with every child therefore proves zero intersection with
    the exact complete-part Minkowski sweep continuously, not only at samples.
    Splitting the fixed-disc stop pin from its plate avoids the false corner
    occupancy of a whole-part bounding-box sweep.
    """
    pieces = [sweep for _, _, sweep in _final_core_proof_features(params)]
    for index, piece in enumerate(pieces, 1):
        piece.label = f"continuous_minus80Y_feature_envelope_{index:02d}"
        piece.color = srgb("#7D8588")
    return Compound(children=pieces, label="continuous_conservative_complete_core_minus80Y_BREP_proof")


def build_fit_ladder(params: P10Parameters = P10_DEFAULTS) -> Shape:
    body = _box((3.0, 0.0, 0.0), (6.0, 32.0, 12.0))
    tools = [
        _x_hex_prism(socket, 8.0, 3.0, y, 0.0)
        for socket, y in zip((6.15, 6.25, 6.35), (-10.0, 0.0, 10.0))
    ]
    return _label(body - tools, "three_socket_fit_ladder_6p15_6p25_6p35_t6", "#717A7D")


def build_fit_plug(params: P10Parameters = P10_DEFAULTS) -> Shape:
    plug = _x_hex_prism(6.0, 8.0, 4.0, 0.0, 0.0)
    marks = [_x_hex_prism(6.40, 0.30, x, 0.0, 0.0) for x in (3.0, 5.6)]
    return _label(_fuse([plug, *marks]), "male_hex_fit_plug_6p00_marks_at_3p0_and_5p6", "#262D30")


def build_fit_coupon(params: P10Parameters = P10_DEFAULTS) -> Compound:
    ladder = build_fit_ladder(params)
    plug = Pos(0.0, 22.0, 0.0) * build_fit_plug(params)
    return Compound(children=[ladder, plug], label="p10_cam_wheel_hex_socket_fit_coupon_two_printed_solids")


def _on_bed(
    shape: Shape, x: float, y: float, y_rotation: float | None = None,
) -> Shape:
    placed = Rot(0.0, y_rotation, 0.0) * shape if y_rotation is not None else copy(shape)
    bounds = placed.bounding_box()
    return Pos(
        x - (bounds.min.X + bounds.max.X) / 2.0,
        y - (bounds.min.Y + bounds.max.Y) / 2.0,
        -bounds.min.Z,
    ) * placed


def build_exploded(params: P10Parameters = P10_DEFAULTS) -> Compound:
    angle = params.end_angle
    parts: list[Shape] = [
        Pos(-12.0, 0.0, 0.0) * build_fixed_disc("left", "as_printed", params),
        Pos(-6.0, 0.0, 0.0) * _rotate_about_shaft(build_cam_disc("left", params), angle, params),
        Pos(12.0, 0.0, 0.0) * build_fixed_disc("right", "as_printed", params),
        Pos(6.0, 0.0, 0.0) * _rotate_about_shaft(build_cam_disc("right", params), angle, params),
        Pos(0.0, -12.0, 0.0) * build_base(params),
        build_locator("as_printed", 80.0, params),
        build_shaft(angle, params), Pos(-10.0, 10.0, 0.0) * build_shaft_keeper(params),
        Pos(10.0, 0.0, 0.0) * build_wheel(angle, "as_printed", params),
        build_lock_pin(True, params),
        *build_rods(0.0, params.rod_withdraw_x, params).children,
        *build_retainers(0.0, -8.0, params.rod_withdraw_x, params).children,
        build_electronics_reference(), build_fixed_L_workpiece(),
    ]
    return Compound(children=parts, label="p10_exploded_workflow_as_printed_interference_features_visible")


def build_print_kit(params: P10Parameters = P10_DEFAULTS) -> Compound:
    raw_parts: list[tuple[Shape, float | None]] = [
        (build_fixed_disc("left", "as_printed", params), 90.0),
        (build_fixed_disc("right", "as_printed", params), -90.0),
        (build_cam_disc("left", params), 90.0), (build_cam_disc("right", params), -90.0),
        (build_base(params), None), (build_locator("as_printed", 0.0, params), None),
        (build_shaft(0.0, params), -90.0), (build_wheel(0.0, "as_printed", params), -90.0),
        (build_shaft_keeper(params), -90.0), (build_lock_pin(False, params), -90.0),
    ]
    for name in ROD_NAMES:
        point = rod_center(name, 0.0, params)
        raw_parts.append((build_left_cap(point, 0.0, params), -90.0))
    for name in ROD_NAMES:
        point = rod_center(name, 0.0, params)
        raw_parts.append((build_right_keeper(point, 0.0, params), -90.0))
    raw_parts.extend(((build_fit_ladder(params), -90.0), (build_fit_plug(params), -90.0)))
    positions = [
        (-135, -52), (-45, -52), (45, -52), (135, -52),
        (-130, 36), (-65, 36), (0, 36), (62, 36), (105, 36), (145, 36),
        (-105, 94), (-78, 94), (-51, 94), (-14, 94), (13, 94), (40, 94),
        (92, 98), (142, 98),
    ]
    children = [_on_bed(part, x, y, y_rotation)
                for (part, y_rotation), (x, y) in zip(raw_parts, positions)]
    for index, child in enumerate(children, 1):
        child.label = f"print_part_{index:02d}_{raw_parts[index - 1][0].label}"
    return Compound(children=children, label="p10_print_kit_exactly_18_printed_solids_excludes_rods_electronics")


__all__ = [
    "P10Parameters", "P10_DEFAULTS", "ROD_NAMES", "build_base", "build_fixed_disc",
    "build_cam_disc", "build_rod", "build_rods", "build_locator", "build_locator_swept_volume",
    "build_shaft", "build_shaft_keeper", "build_wheel", "build_lock_pin", "build_left_cap",
    "build_right_keeper", "build_retainers", "build_electronics_reference", "build_fixed_L_workpiece",
    "build_principal_plates", "build_loaded_open", "build_loaded_closed", "build_locator_removed_closed",
    "build_rods_withdrawn", "build_removal_clear", "build_exploded", "build_print_kit",
    "build_fit_ladder", "build_fit_plug", "build_fit_coupon", "build_lock_pin_swept_volume",
    "build_keeper_swept_volume", "build_rod_cap_swept_volume", "build_final_core_swept_volume",
    "build_final_core_moving_primitives", "build_solder_access_corridor",
    "build_solder_target_envelope", "contact_band",
    "lock_local_point", "lock_world_point", "travel_at_angle", "rod_center", "slot_path",
]
