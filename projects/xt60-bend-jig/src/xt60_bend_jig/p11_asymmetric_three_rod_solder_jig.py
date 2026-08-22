"""P11 compact asymmetric three-rod XT60 soldering-jig prototype.

P11 is intentionally independent of P10.  Rod axes are X and all mechanism
kinematics are derived in YZ about the shared shaft.  The workpiece reference
is an already routed 90-degree pigtail; only the rigid XT60 body-and-cup
vertical loading sweep is claimed.  Flexible-wire routing remains a physical
test because the complete rigid L-path crosses the open diagonal rod.
"""

from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from functools import lru_cache
from math import asin, atan2, cos, degrees, hypot, pi, radians, sin, sqrt
from typing import Literal

from build123d import (
    Align, Box, BuildLine, BuildSketch, CenterArc, Circle, Compound, Cone,
    Cylinder, Edge, Face, Line, Plane, Pos, RegularPolygon, Rot, Shape, Side as
    OffsetSide, Sphere, Vector, Wire, extrude, sweep,
)
from cadgen import srgb


RodName = Literal["upright", "bottom", "diagonal"]
Side = Literal["left", "right"]
ROD_NAMES: tuple[RodName, ...] = ("upright", "bottom", "diagonal")
FOLLOWER_ERROR_OFFSETS: tuple[tuple[float, float], ...] = (
    (-0.25, 0.0), (0.25, 0.0), (0.0, -0.25), (0.0, 0.25),
    (-0.25, -0.25), (-0.25, 0.25), (0.25, -0.25), (0.25, 0.25),
)


@dataclass(frozen=True, slots=True)
class PointYZ:
    y: float
    z: float

    def distance_to(self, other: "PointYZ") -> float:
        return hypot(self.y - other.y, self.z - other.z)


@dataclass(frozen=True, slots=True)
class P11Parameters:
    rod_diameter: float = 4.0
    rod_length: float = 50.0
    wire_diameter: float = 4.30
    wire_x: float = 4.0
    bend_radius: float = 6.0
    d1: float = 7.0
    horizontal_z: float = 30.0
    pad_y: float = 30.5
    cup_diameter: float = 3.0
    cup_height: float = 5.0
    xt60_x: float = 15.9
    xt60_y: float = 8.1
    xt60_z: float = 20.5
    plate_diameter: float = 56.0
    fixed_thickness: float = 2.8
    cam_thickness: float = 2.5
    axial_gap: float = 0.30
    clear_span: float = 26.0
    shaft_y: float = -5.0
    shaft_z: float = 29.0
    shaft_diameter: float = 6.0
    fixed_bore: float = 6.30
    cam_socket: float = 6.15
    datum_guide_width: float = 4.4
    datum_cam_lane: float = 4.8
    datum_locked_pocket: float = 4.4
    follower_guide_width: float = 4.9
    follower_cam_lane: float = 5.0
    construction_offset: float = 0.25
    end_angle: float = 35.0
    dwell_start: float = 32.0
    upright_stroke: float = 5.5
    bottom_stroke: float = 5.5
    diagonal_stroke: float = 11.0
    load_clearance: float = 3.0
    rod_withdraw_x: float = -55.0
    core_remove_y: float = -70.0
    keeper_remove_y: float = -10.0
    shaft_insert_x: float = 50.0
    shaft_neck_diameter: float = 5.2
    shaft_keeper_bore: float = 5.4
    rod_keeper_bore: float = 4.10
    rod_keeper_outer: float = 7.0
    rod_keeper_thickness: float = 2.9
    stop_radius: float = 20.0
    stop_world_angle: float = -120.0
    crush_rib_interference: float = 0.075

    def __post_init__(self) -> None:
        if not 5.0 <= self.bend_radius <= 7.0:
            raise ValueError("bend_radius must be within 5..7 mm")
        if not 6.0 <= self.d1 <= 8.0:
            raise ValueError("d1 must be within 6..8 mm")
        if (self.rod_diameter, self.rod_length) != (4.0, 50.0):
            raise ValueError("P11 uses exactly three purchased 4 x 50 mm rods")
        if self.plate_diameter > 56.0:
            raise ValueError("principal plate OD may not exceed 56 mm")
        if self.axial_body > 38.0:
            raise ValueError("four-plate axial body must not exceed 38 mm")

    @property
    def vertical_tangent_z(self) -> float:
        return self.horizontal_z + self.bend_radius

    @property
    def wire_entry_z(self) -> float:
        return self.vertical_tangent_z + self.d1

    @property
    def body_bottom_z(self) -> float:
        return self.wire_entry_z + self.cup_height

    @property
    def axial_body(self) -> float:
        return self.clear_span + 2.0 * (
            self.cam_thickness + self.axial_gap + self.fixed_thickness
        )

    @property
    def left_cam_x(self) -> float:
        return -(self.clear_span / 2.0 + self.fixed_thickness + self.axial_gap + self.cam_thickness / 2.0)

    @property
    def right_cam_x(self) -> float:
        return -self.left_cam_x

    @property
    def left_fixed_x(self) -> float:
        return -(self.clear_span / 2.0 + self.fixed_thickness / 2.0)

    @property
    def right_fixed_x(self) -> float:
        return -self.left_fixed_x

    @property
    def rod_projection(self) -> float:
        return self.rod_length / 2.0 - self.axial_body / 2.0

    @property
    def shaft_center(self) -> PointYZ:
        return PointYZ(self.shaft_y, self.shaft_z)


P11_DEFAULTS = P11Parameters()


_DIRECTION: dict[RodName, PointYZ] = {
    "upright": PointYZ(1.0, 0.0),
    "bottom": PointYZ(0.0, 1.0),
    "diagonal": PointYZ(-1.0 / sqrt(2.0), -1.0 / sqrt(2.0)),
}


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def _box(center: tuple[float, float, float], size: tuple[float, float, float]) -> Shape:
    return Pos(*center) * Box(*size, align=(Align.CENTER, Align.CENTER, Align.CENTER))


def _fuse(shapes: list[Shape]) -> Shape:
    result = shapes[0]
    for item in shapes[1:]:
        result = result + item
    return result


def _x_cylinder(diameter: float, length: float, x: float, y: float, z: float) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0, length, rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _x_hex(across_corners: float, length: float, x: float, y: float, z: float) -> Shape:
    face = RegularPolygon(across_corners / 2.0, 6, rotation=30.0)
    return Pos(x, y, z) * Rot(0.0, 90.0, 0.0) * extrude(face, length / 2.0, both=True)


def _rotate_about_shaft(shape: Shape, angle_deg: float, params: P11Parameters) -> Shape:
    return Pos(0.0, params.shaft_y, params.shaft_z) * Rot(angle_deg, 0.0, 0.0) * Pos(
        0.0, -params.shaft_y, -params.shaft_z
    ) * shape


def ease(value: float) -> float:
    s = max(0.0, min(1.0, value))
    return 3.0 * s * s - 2.0 * s * s * s


def travel_fraction(name: RodName, angle_deg: float) -> float:
    if not 0.0 <= angle_deg <= 35.0:
        raise ValueError("angle must be within 0..35 degrees")
    if name == "upright":
        return ease(angle_deg / 20.0)
    if name == "bottom":
        return ease((angle_deg - 5.0) / 22.0)
    if name == "diagonal":
        return ease(angle_deg / 32.0)
    raise ValueError(f"unknown rod name: {name}")


def role_stroke(name: RodName, params: P11Parameters = P11_DEFAULTS) -> float:
    return {
        "upright": params.upright_stroke,
        "bottom": params.bottom_stroke,
        "diagonal": params.diagonal_stroke,
    }[name]


def closed_rod_center(name: RodName, params: P11Parameters = P11_DEFAULTS) -> PointYZ:
    """Radius-derived contact center, reproducing every frozen R6 datum."""

    r = params.bend_radius
    rho = (params.wire_diameter + params.rod_diameter) / 2.0
    if name == "upright":
        return PointYZ(-rho, params.horizontal_z + 2.0 * r)
    if name == "bottom":
        return PointYZ(2.0 * r, params.horizontal_z - rho)
    if name == "diagonal":
        contact_y = r - r / sqrt(2.0)
        contact_z = params.horizontal_z + r - r / sqrt(2.0)
        return PointYZ(contact_y + rho / sqrt(2.0), contact_z + rho / sqrt(2.0))
    raise ValueError(f"unknown rod name: {name}")


def rod_center(name: RodName, angle_deg: float, params: P11Parameters = P11_DEFAULTS) -> PointYZ:
    closed = closed_rod_center(name, params)
    direction = _DIRECTION[name]
    remaining = role_stroke(name, params) * (1.0 - travel_fraction(name, angle_deg))
    return PointYZ(closed.y - direction.y * remaining, closed.z - direction.z * remaining)


def inverse_slot_point(name: RodName, angle_deg: float, params: P11Parameters = P11_DEFAULTS) -> PointYZ:
    point = rod_center(name, angle_deg, params)
    dy, dz = point.y - params.shaft_y, point.z - params.shaft_z
    a = radians(angle_deg)
    return PointYZ(
        params.shaft_y + cos(a) * dy + sin(a) * dz,
        params.shaft_z - sin(a) * dy + cos(a) * dz,
    )


def inverse_slot_path(
    name: RodName, params: P11Parameters = P11_DEFAULTS,
    start: float = 0.0, end: float | None = None, step: float = 0.5,
) -> tuple[PointYZ, ...]:
    final = params.end_angle if end is None else end
    count = max(1, round((final - start) / step))
    return tuple(
        inverse_slot_point(name, start + (final - start) * i / count, params)
        for i in range(count + 1)
    )


def _slot_solid_x(points: tuple[PointYZ, ...], width: float, x: float, depth: float) -> Shape:
    if len(points) < 2:
        raise ValueError("slot path requires at least two points")
    vectors = [(0.0, p.y, p.z) for p in points]
    # Use a faceted planar wire here: OCC exports its analytic line/arc offset
    # faces as a watertight STEP solid, whereas the equivalent high-order
    # spline offset can re-import as a shell in some STEP readers.
    path = Wire.make_polygon(vectors)
    try:
        outline = path.offset_2d(width / 2.0, side=OffsetSide.BOTH, closed=True)
        return Pos(x, 0.0, 0.0) * extrude(Face(outline), depth / 2.0, both=True)
    except ValueError:
        # Some valid inverse paths turn tightly enough for OCC's planar offset
        # builder to return null.  A union of exact adjacent capsules is the
        # same conservative swept follower envelope and is robust.
        return _fuse([
            _straight_slot_x(first, second, width, x, depth)
            for first, second in zip(points, points[1:])
        ])


def _straight_slot_x(first: PointYZ, second: PointYZ, width: float, x: float, depth: float) -> Shape:
    dy, dz = second.y - first.y, second.z - first.z
    length = hypot(dy, dz)
    angle = degrees(atan2(dz, dy))
    bar = Pos(x, (first.y + second.y) / 2.0, (first.z + second.z) / 2.0) * Rot(
        angle, 0.0, 0.0
    ) * Box(depth, length, width, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    return bar + _x_cylinder(width, depth, x, first.y, first.z) + _x_cylinder(
        width, depth, x, second.y, second.z
    )


def build_wire_centerline(x: float, params: P11Parameters = P11_DEFAULTS) -> Wire:
    r = params.bend_radius
    with BuildLine(Plane.YZ) as path:
        Line((params.pad_y, params.horizontal_z), (r, params.horizontal_z))
        CenterArc((r, params.horizontal_z + r), r, -90.0, -90.0)
        Line((0.0, params.vertical_tangent_z), (0.0, params.wire_entry_z))
    return Pos(x, 0.0, 0.0) * Wire(path.line.edges())


def build_wire(x: float, color: str, params: P11Parameters = P11_DEFAULTS) -> Shape:
    centerline = build_wire_centerline(x, params)
    start_plane = Plane(origin=(x, params.pad_y, params.horizontal_z), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    with BuildSketch(start_plane) as profile:
        Circle(params.wire_diameter / 2.0)
    return _label(sweep(profile.sketch, centerline), f"12AWG_R{params.bend_radius:g}_D1_{params.d1:g}_wire_x{x:+g}", color)


def build_wires(params: P11Parameters = P11_DEFAULTS) -> Compound:
    return Compound(children=[
        build_wire(-params.wire_x, "#D64536", params),
        build_wire(params.wire_x, "#17191C", params),
    ], label="two_exact_90deg_12AWG_reference_leads")


def build_xt60(params: P11Parameters = P11_DEFAULTS) -> Compound:
    cups = [
        _label(Pos(x, 0.0, params.wire_entry_z) * Cylinder(
            params.cup_diameter / 2.0, params.cup_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), f"assumed_XT60_cup_x{x:+g}_D3x5", "#C7A84A")
        for x in (-params.wire_x, params.wire_x)
    ]
    body = _label(_box(
        (0.0, 0.0, params.body_bottom_z + params.xt60_z / 2.0),
        (params.xt60_x, params.xt60_y, params.xt60_z),
    ), "assumed_XT60_body_15p9x8p1x20p5", "#E0A916")
    return Compound(children=[*cups, body], label="frozen_assumed_XT60_body_and_two_cups")


def build_workpiece(params: P11Parameters = P11_DEFAULTS) -> Compound:
    return Compound(children=[*build_wires(params).children, *build_xt60(params).children],
                    label="connected_90deg_reference_pigtail_flexible_loading_not_CAD_proven")


def build_loading_sweep(params: P11Parameters = P11_DEFAULTS, lift: float = 50.0) -> Compound:
    body = _box(
        (0.0, 0.0, params.body_bottom_z + params.xt60_z / 2.0 + lift / 2.0),
        (params.xt60_x, params.xt60_y, params.xt60_z + lift),
    )
    cups = [
        Pos(x, 0.0, params.wire_entry_z + (params.cup_height + lift) / 2.0) * Cylinder(
            params.cup_diameter / 2.0, params.cup_height + lift,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ) for x in (-params.wire_x, params.wire_x)
    ]
    return Compound(children=[_label(body, "vertical_XT60_body_swept_volume", "#E8C563"),
                              *[_label(c, "vertical_cup_swept_volume", "#D8C98F") for c in cups]],
                    label="CAD_proven_body_and_cups_vertical_loading_sweep_only")


def build_base(params: P11Parameters = P11_DEFAULTS) -> Shape:
    body = _box((0.0, -8.5, -2.5), (38.0, 19.0, 5.0))
    land = _box((0.0, -20.0, -2.5), (38.0, 8.0, 5.0))
    mortises = [
        _box((x, -8.0, -1.0), (params.fixed_thickness + 0.35, 12.4, 6.2))
        for x in (params.left_fixed_x, params.right_fixed_x)
    ]
    return _label((body + land) - mortises, "compact_base_with_38x8_flat_external_bench_clamp_land", "#3D4547")


def _fixed_tongue(side: Side, params: P11Parameters) -> Shape:
    x = params.left_fixed_x if side == "left" else params.right_fixed_x
    return _box((x, -8.0, 0.0), (params.fixed_thickness, 12.0, 8.0))


def _crush_ribs(side: Side, params: P11Parameters) -> Shape:
    """Four minimal raw ribs; the seated assembly uses their compressed envelope."""
    x = params.left_fixed_x if side == "left" else params.right_fixed_x
    mortise_width = params.fixed_thickness + 0.35
    rib_half_width = (mortise_width - params.fixed_thickness) / 2.0 + params.crush_rib_interference
    ribs = [
        _box((x + sx * params.fixed_thickness / 2.0, y, -1.5),
             (2.0 * rib_half_width, 1.5, 3.0))
        for sx in (-1.0, 1.0)
        for y in (-11.0, -5.0)
    ]
    return _fuse(ribs)


def _detent_leaf_tools(params: P11Parameters) -> list[Shape]:
    x = params.right_fixed_x
    d = params.fixed_thickness + 2.0
    return [
        _box((x, -8.0, 6.7), (d, 18.0, 0.8)),
        _box((x, -8.0, 9.3), (d, 18.0, 0.8)),
        _box((x, 1.3, 8.0), (d, 0.8, 3.4)),
    ]


def detent_nose_world(params: P11Parameters = P11_DEFAULTS) -> PointYZ:
    return PointYZ(0.0, 8.0)


def detent_pocket_local(angle_deg: float, params: P11Parameters = P11_DEFAULTS) -> PointYZ:
    p = detent_nose_world(params)
    dy, dz = p.y - params.shaft_y, p.z - params.shaft_z
    a = radians(angle_deg)
    return PointYZ(params.shaft_y + cos(a) * dy + sin(a) * dz,
                   params.shaft_z - sin(a) * dy + cos(a) * dz)


def stop_pin_world(params: P11Parameters = P11_DEFAULTS) -> PointYZ:
    # Lower-left quadrant stays clear of every R5/R6/R7 rod trajectory while
    # leaving enough circular-blank web for the stop channel.
    a = radians(params.stop_world_angle)
    return PointYZ(params.shaft_y + params.stop_radius * cos(a),
                   params.shaft_z + params.stop_radius * sin(a))


def stop_channel_extension_angle(params: P11Parameters = P11_DEFAULTS) -> float:
    # 0.10 radial clearance between a Ø2.0 pin and Ø2.2 channel is consumed
    # exactly at 35 degrees, making the following motion positive overlap.
    return degrees(2.0 * asin(0.10 / (2.0 * params.stop_radius)))


def stop_channel_path(params: P11Parameters = P11_DEFAULTS) -> tuple[PointYZ, ...]:
    pin = stop_pin_world(params)
    dy, dz = pin.y - params.shaft_y, pin.z - params.shaft_z
    extension = stop_channel_extension_angle(params)
    points: list[PointYZ] = []
    for i in range(73):
        # The path ends just before the 35-degree follower center.  At 35 the
        # Ø2 pin is internally tangent to the Ø2.2 end cap; further rotation
        # makes positive solid overlap with the channel wall.
        theta = -extension + params.end_angle * i / 72.0
        a = radians(theta)
        points.append(PointYZ(params.shaft_y + cos(a) * dy + sin(a) * dz,
                              params.shaft_z - sin(a) * dy + cos(a) * dz))
    return tuple(points)


def build_stop_pin(params: P11Parameters = P11_DEFAULTS) -> Shape:
    fixed_outer = params.right_fixed_x + params.fixed_thickness / 2.0
    cam_inner = params.right_cam_x - params.cam_thickness / 2.0
    p = stop_pin_world(params)
    return _label(_x_cylinder(2.0, params.axial_gap + 0.55,
                              (fixed_outer + cam_inner) / 2.0 + 0.05, p.y, p.z),
                  "integral_right_fixed_2mm_hard_stop_pin", "#2F6D4C")


@lru_cache(maxsize=64)
def _fixed_plate_prototype(
    side: Side, params: P11Parameters,
    slot_offset: tuple[float, float] = (0.0, 0.0), seated: bool = True,
) -> Shape:
    x = params.left_fixed_x if side == "left" else params.right_fixed_x
    depth = params.fixed_thickness
    disc = _x_cylinder(params.plate_diameter, depth, x, params.shaft_y, params.shaft_z)
    raw = disc + _fixed_tongue(side, params)
    if not seated:
        raw = raw + _crush_ribs(side, params)
    guide_width = params.datum_guide_width if side == "left" else params.follower_guide_width
    oy, oz = slot_offset if side == "right" else (0.0, 0.0)
    tools = [
        _straight_slot_x(
            PointYZ(rod_center(name, 0.0, params).y + oy, rod_center(name, 0.0, params).z + oz),
            PointYZ(rod_center(name, params.end_angle, params).y + oy,
                    rod_center(name, params.end_angle, params).z + oz),
                         guide_width, x, depth + 2.0)
        for name in ROD_NAMES
    ]
    tools.append(_x_cylinder(params.fixed_bore, depth + 2.0, x, params.shaft_y, params.shaft_z))
    if side == "right":
        tools.extend(_detent_leaf_tools(params))
    plate = raw - tools
    if side == "right":
        fixed_outer = params.right_fixed_x + depth / 2.0
        cam_inner = params.right_cam_x - params.cam_thickness / 2.0
        nose = _x_cylinder(2.0, 0.55, (fixed_outer + cam_inner) / 2.0 + 0.05,
                           detent_nose_world(params).y, detent_nose_world(params).z)
        pin = build_stop_pin(params)
        plate = plate + nose + pin
    return plate


def build_fixed_plate(
    side: Side, params: P11Parameters = P11_DEFAULTS,
    slot_offset: tuple[float, float] = (0.0, 0.0), seated: bool = True,
) -> Shape:
    color = "#2F6D4C" if side == "left" else "#4A8060"
    role = "datum" if side == "left" else "relieved_follower_integral_leaf_detent_and_stop_pin"
    fit = "seated_zero_overlap_crush_rib_envelope" if seated else "raw_integral_crush_ribs"
    offset = "" if side == "left" else f"_slot_offset_Y{slot_offset[0]:+g}_Z{slot_offset[1]:+g}"
    return _label(copy(_fixed_plate_prototype(side, params, slot_offset, seated)),
                  f"{side}_fixed_full_56mm_disc_{role}_{fit}{offset}", color)


def _offset_path(points: tuple[PointYZ, ...], offset: tuple[float, float]) -> tuple[PointYZ, ...]:
    oy, oz = offset
    return tuple(PointYZ(point.y + oy, point.z + oz) for point in points)


def _cam_slot_tools(
    name: RodName, side: Side, x: float, depth: float, params: P11Parameters,
    slot_offset: tuple[float, float] = (0.0, 0.0),
) -> list[Shape]:
    if side == "right":
        # Split at mid-stroke so each offset curve remains simple.  The overlap
        # is subtracted sequentially; no self-union seam is exported.
        return [
            _slot_solid_x(_offset_path(inverse_slot_path(name, params, 0.0, 18.0), slot_offset),
                          params.follower_cam_lane, x, depth + 2.0),
            _slot_solid_x(_offset_path(
                              inverse_slot_path(name, params, 17.5, params.end_angle), slot_offset),
                          params.follower_cam_lane, x, depth + 2.0),
        ]
    # The wide motion lane ends before the load-normal locked pocket.  The
    # narrower path overlaps it enough to remain connected while leaving the
    # exact 35-degree endpoint governed by Ø4.4 geometry.
    bands = (
        (0.0, 10.0, 4.8),
        (9.5, 12.0, 4.7),
        (11.5, 14.0, 4.6),
        (13.5, 16.0, 4.5),
        (15.5, params.dwell_start, params.datum_locked_pocket),
    )
    tools = [
        _slot_solid_x(
            inverse_slot_path(name, params, start, end, 0.25),
            width,
            x, depth + 2.0,
        )
        for start, end, width in bands
    ]
    q32 = inverse_slot_point(name, params.dwell_start, params)
    q35 = inverse_slot_point(name, params.end_angle, params)
    tools.extend((
        _straight_slot_x(q32, q35, 4.20, x, depth + 2.0),
        _x_cylinder(params.datum_locked_pocket, depth + 2.0, x, q35.y, q35.z),
    ))
    return tools


def _operating_tab_notches(x: float, depth: float, params: P11Parameters) -> list[Shape]:
    # Two edge cuts leave a broad finger at the bottom of the otherwise full
    # disc; no geometry extends beyond the 56 mm blank.
    return [
        _box((x, -11.5, 3.1), (depth + 2.0, 7.0, 3.0)),
        _box((x, 1.5, 3.1), (depth + 2.0, 7.0, 3.0)),
    ]


@lru_cache(maxsize=32)
def _cam_plate_prototype(
    side: Side, params: P11Parameters,
    slot_offset: tuple[float, float] = (0.0, 0.0),
) -> Shape:
    x = params.left_cam_x if side == "left" else params.right_cam_x
    depth = params.cam_thickness
    disc = _x_cylinder(params.plate_diameter, depth, x, params.shaft_y, params.shaft_z)
    tools: list[Shape] = []
    for name in ROD_NAMES:
        tools.extend(_cam_slot_tools(name, side, x, depth, params, slot_offset))
    tools.append(_x_hex(params.cam_socket, depth + 2.0, x, params.shaft_y, params.shaft_z))
    tools.extend(_operating_tab_notches(x, depth, params))
    if side == "right":
        # Two shallow face pockets receive the fixed leaf nose at 0 and 35.
        inner_face = params.right_cam_x - depth / 2.0
        for angle in (0.0, params.end_angle):
            p = detent_pocket_local(angle, params)
            tools.append(_x_cylinder(2.20, 0.45, inner_face + 0.15, p.y, p.z))
        tools.append(_slot_solid_x(stop_channel_path(params), 2.20, x, depth + 2.0))
    return disc - tools


def build_cam_plate(
    side: Side, params: P11Parameters = P11_DEFAULTS,
    slot_offset: tuple[float, float] = (0.0, 0.0),
) -> Shape:
    role = "datum_4p8_lane_4p4_locked_pocket" if side == "left" else "relieved_5p0_lane_two_state_detent_stop_channel"
    offset = "" if side == "left" else f"_slot_offset_Y{slot_offset[0]:+g}_Z{slot_offset[1]:+g}"
    return _label(copy(_cam_plate_prototype(side, params, slot_offset)),
                  f"{side}_cam_full_56mm_disc_{role}_integral_bottom_tab{offset}", "#D29A18")


def build_principal_plates(angle_deg: float, params: P11Parameters = P11_DEFAULTS, y_shift: float = 0.0) -> Compound:
    parts: list[Shape] = [
        build_fixed_plate("left", params),
        _rotate_about_shaft(build_cam_plate("left", params), angle_deg, params),
        _rotate_about_shaft(build_cam_plate("right", params), angle_deg, params),
        build_fixed_plate("right", params),
    ]
    if y_shift:
        parts = [Pos(0.0, y_shift, 0.0) * part for part in parts]
    return Compound(children=parts, label=f"exactly_four_principal_full_discs_angle_{angle_deg:g}")


def build_rod(name: RodName, angle_deg: float, params: P11Parameters = P11_DEFAULTS, x_shift: float = 0.0) -> Shape:
    p = rod_center(name, angle_deg, params)
    return _label(_x_cylinder(params.rod_diameter, params.rod_length, x_shift, p.y, p.z),
                  f"purchased_304_stainless_{name}_rod_4x50", "#BCC5CA")


def build_rods(angle_deg: float, params: P11Parameters = P11_DEFAULTS, x_shift: float = 0.0) -> Compound:
    return Compound(children=[build_rod(name, angle_deg, params, x_shift) for name in ROD_NAMES],
                    label=f"exactly_three_4x50_rods_angle_{angle_deg:g}")


def build_shaft(angle_deg: float = 0.0, params: P11Parameters = P11_DEFAULTS) -> Shape:
    key_length = params.axial_body + 2.0
    key = _x_hex(params.shaft_diameter, key_length, 0.0, params.shaft_y, params.shaft_z)
    left_neck = _x_cylinder(params.shaft_neck_diameter, 2.0,
                            -key_length / 2.0 - 1.0, params.shaft_y, params.shaft_z)
    right_head = _x_cylinder(9.0, 1.8, key_length / 2.0 + 0.9,
                             params.shaft_y, params.shaft_z)
    return _label(_rotate_about_shaft(key + left_neck + right_head, angle_deg, params),
                  f"right_inserted_6mm_keyed_shaft_integral_right_head_passable_left_neck_{angle_deg:g}deg",
                  "#252A2D")


def build_shaft_insertion_sweep(params: P11Parameters = P11_DEFAULTS) -> Compound:
    """Exact axial swept primitives from fully right of the plates to seated."""
    travel = params.shaft_insert_x
    key_length = params.axial_body + 2.0
    key = _x_hex(params.shaft_diameter, key_length + travel, travel / 2.0,
                 params.shaft_y, params.shaft_z)
    neck = _x_cylinder(params.shaft_neck_diameter, 2.0 + travel,
                       -key_length / 2.0 - 1.0 + travel / 2.0,
                       params.shaft_y, params.shaft_z)
    head = _x_cylinder(9.0, 1.8 + travel,
                       key_length / 2.0 + 0.9 + travel / 2.0,
                       params.shaft_y, params.shaft_z)
    return Compound(children=[
        _label(key, "continuous_keyed_body_right_to_seated_sweep", "#718087"),
        _label(neck, "continuous_passable_left_neck_right_to_seated_sweep", "#718087"),
        _label(head, "continuous_integral_right_head_trailing_sweep", "#718087"),
    ], label="complete_right_inserted_shaft_continuous_sweep")


def _c_keeper_boxes(
    x: float, point: PointYZ, axial_thickness: float, bore: float, outer: float,
    y_shift: float = 0.0, sweep_y: float | None = None,
) -> list[Shape]:
    arm = (outer - bore) / 2.0
    arm_y_min = point.y - outer / 2.0
    arm_y_max = point.y + outer / 2.0
    if sweep_y is not None:
        arm_y_min += min(0.0, sweep_y)
        arm_y_max += max(0.0, sweep_y)
    arm_y_min += y_shift
    arm_y_max += y_shift
    arm_length = arm_y_max - arm_y_min
    arm_center_y = (arm_y_min + arm_y_max) / 2.0
    z_offset = bore / 2.0 + arm / 2.0
    bridge_y_min = point.y - outer / 2.0 + y_shift + min(0.0, sweep_y or 0.0)
    bridge_y_max = point.y - outer / 2.0 + arm + y_shift + max(0.0, sweep_y or 0.0)
    return [
        _box((x, arm_center_y, point.z - z_offset),
             (axial_thickness, arm_length, arm)),
        _box((x, arm_center_y, point.z + z_offset),
             (axial_thickness, arm_length, arm)),
        _box((x, (bridge_y_min + bridge_y_max) / 2.0, point.z),
             (axial_thickness, bridge_y_max - bridge_y_min, outer)),
    ]


def build_shaft_keeper(
    params: P11Parameters = P11_DEFAULTS, y_shift: float = 0.0,
) -> Shape:
    key_length = params.axial_body + 2.0
    x = -key_length / 2.0 - 1.0
    parts = _c_keeper_boxes(x, params.shaft_center, 1.8,
                            params.shaft_keeper_bore, 9.0, y_shift)
    return _label(_fuse(parts), "separate_left_shaft_C_keeper_removable_minusY", "#76959D")


def build_shaft_keeper_escape_sweep(
    params: P11Parameters = P11_DEFAULTS,
    travel_y: float | None = None,
) -> Shape:
    """Continuous -Y sweep of the left shaft keeper.

    The short default travel proves that the C throat can disengage from the
    shaft.  The fallback core-removal proof passes ``core_remove_y`` so the
    declared sweep also contains the keeper's final rendered position.
    """
    key_length = params.axial_body + 2.0
    x = -key_length / 2.0 - 1.0
    travel = params.keeper_remove_y if travel_y is None else travel_y
    parts = _c_keeper_boxes(x, params.shaft_center, 1.8,
                            params.shaft_keeper_bore, 9.0,
                            sweep_y=travel)
    return _label(
        _fuse(parts),
        f"continuous_shaft_keeper_minusY_sweep_{abs(travel):g}mm",
        "#A6B8BE",
    )


def build_left_cap(point: PointYZ, params: P11Parameters = P11_DEFAULTS, x_shift: float = 0.0) -> Shape:
    inner = -params.axial_body / 2.0 - 0.2 + x_shift
    body = _x_cylinder(7.0, 3.7, inner - 1.85, point.y, point.z)
    socket = _x_cylinder(3.90, 3.0, inner - 1.5, point.y, point.z)
    return _label(body - socket, "left_rod_cap_3p90_tight_trial", "#C88714")


def build_right_keeper(point: PointYZ, params: P11Parameters = P11_DEFAULTS, y_shift: float = 0.0) -> Shape:
    x = params.axial_body / 2.0 + 1.45
    center_y = point.y + y_shift
    ring = _x_cylinder(
        params.rod_keeper_outer,
        params.rod_keeper_thickness,
        x,
        center_y,
        point.z,
    )
    bore = _x_cylinder(
        params.rod_keeper_bore,
        params.rod_keeper_thickness + 2.0,
        x,
        center_y,
        point.z,
    )
    # Open the annulus toward +Y.  The throat is exactly as wide as the
    # nominal bore, so the keeper can snap off sideways without requiring the
    # 50 mm rod to be withdrawn first.
    throat_length = params.rod_keeper_outer / 2.0 + 1.0
    throat = _box(
        (x, center_y + throat_length / 2.0, point.z),
        (
            params.rod_keeper_thickness + 2.0,
            throat_length,
            params.rod_keeper_bore,
        ),
    )
    return _label(
        ring - [bore, throat],
        "right_circular_C_keeper_4p10_plusY_open_remove_minusY",
        "#E0AE35",
    )


def build_right_keeper_escape_sweep(
    name: RodName, params: P11Parameters = P11_DEFAULTS,
) -> Shape:
    point = rod_center(name, 0.0, params)
    x = params.axial_body / 2.0 + 1.45
    parts = _c_keeper_boxes(x, point, 2.9, 4.10, 7.0,
                            sweep_y=params.keeper_remove_y)
    return _label(_fuse(parts), f"continuous_{name}_right_keeper_minusY_escape_sweep", "#EBCB7A")


def build_retainers(angle_deg: float, params: P11Parameters = P11_DEFAULTS,
                    right_y_shift: float = 0.0, left_x_shift: float = 0.0) -> Compound:
    parts: list[Shape] = []
    for name in ROD_NAMES:
        p = rod_center(name, angle_deg, params)
        parts.extend((build_left_cap(p, params, left_x_shift),
                      build_right_keeper(p, params, right_y_shift)))
    return Compound(children=parts, label="three_left_caps_and_three_removable_right_keepers")


def build_electronics_reference(params: P11Parameters = P11_DEFAULTS) -> Compound:
    esc = _box((0.0, 46.0, 25.75), (36.0, 36.0, 3.5))
    for x in (-params.wire_x, params.wire_x):
        esc = esc - Pos(x, params.pad_y, 25.75) * Cylinder(3.4, 5.0,
            align=(Align.CENTER, Align.CENTER, Align.CENTER))
    fc = _label(_box((0.0, 46.0, 42.0), (30.5, 30.5, 2.0)),
                "reference_upper_FC_P10_envelope", "#4C5860")
    parts: list[Shape] = [
        _label(esc, "reference_ESC_with_two_tool_access_keepouts", "#24292B"), fc,
    ]
    for x, name in ((-params.wire_x, "negative"), (params.wire_x, "positive")):
        parts.extend((
            _label(_box((x, params.pad_y, 27.675), (5.0, 5.0, 0.35)), f"intended_{name}_pad", "#D99C32"),
            _label(Pos(x, params.pad_y, 28.0) * Sphere(1.60), f"intended_{name}_solder", "#C8CED0"),
        ))
    return Compound(children=parts, label="ESC_and_two_intended_solder_targets")


def build_solder_tool_sweep(x: float, params: P11Parameters = P11_DEFAULTS) -> Shape:
    # The YZ projection is the frozen shallow 10-degree approach.  A symmetric
    # outward X cant (0.70 X per 1.0 Y) is required to clear the frozen upper
    # FC; a constant-X or centre-converging frustum intersects that reference.
    sign = -1.0 if x < 0.0 else 1.0
    direction = Vector(sign * 0.70, 1.0, sin(radians(10.0)) / cos(radians(10.0))).normalized()
    near = Cone(0.75, 2.75, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    far = Pos(0.0, 0.0, 8.0) * Cone(
        2.75, 11.0, 47.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    tool = near + far
    tool = Plane(origin=(x, params.pad_y, params.horizontal_z), z_dir=direction) * tool
    return _label(tool, f"55mm_shallow10deg_outwardX_solder_tool_sweep_x{x:+g}", "#77B8D8")


def build_solder_tool_sweeps(params: P11Parameters = P11_DEFAULTS) -> Compound:
    return Compound(children=[build_solder_tool_sweep(-params.wire_x, params),
                              build_solder_tool_sweep(params.wire_x, params)],
                    label="two_separate_55mm_solder_approach_sweeps")


def _assembly_children(
    angle_deg: float, params: P11Parameters, rod_x: float = 0.0,
    keeper_y: float = 0.0, core_y: float = 0.0,
) -> list[Shape]:
    base = Pos(0.0, core_y, 0.0) * build_base(params)
    plates = list(build_principal_plates(angle_deg, params, core_y).children)
    shaft = Pos(0.0, core_y, 0.0) * build_shaft(angle_deg, params)
    shaft_keeper = Pos(0.0, core_y, 0.0) * build_shaft_keeper(params)
    rods = list(build_rods(angle_deg, params, rod_x).children)
    retainers = list(build_retainers(angle_deg, params, keeper_y, rod_x).children)
    return [base, *plates, shaft, shaft_keeper, *rods, *retainers,
            build_electronics_reference(params), build_workpiece(params)]


def build_loaded_open(params: P11Parameters = P11_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(0.0, params),
                    label="p11_OPEN_body_cups_drop_clear_flexible_wire_route_unproven")


def build_loaded_closed(params: P11Parameters = P11_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(params.end_angle, params),
                    label="p11_LOCK_35deg_three_role_rods_exact_90deg_workpiece")


def build_solder_access(params: P11Parameters = P11_DEFAULTS) -> Compound:
    return Compound(children=[*_assembly_children(params.end_angle, params),
                              *build_solder_tool_sweeps(params).children],
                    label="p11_LOCK_two_separate_solder_tool_approaches")


def build_rods_withdrawn(params: P11Parameters = P11_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(0.0, params, params.rod_withdraw_x,
                                                 params.keeper_remove_y),
                    label="p11_OPEN_right_keepers_removed_rods_and_left_caps_withdrawn_minusX")


def build_removal_clear(params: P11Parameters = P11_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(0.0, params, params.rod_withdraw_x,
                                                 params.keeper_remove_y, params.core_remove_y),
                    label="p11_fallback_core_removed_minusY_after_rod_withdrawal")


def build_exploded(params: P11Parameters = P11_DEFAULTS) -> Compound:
    angle = params.end_angle
    parts: list[Shape] = [
        Pos(-12.0, 0.0, 0.0) * build_fixed_plate("left", params),
        Pos(-5.0, 0.0, 0.0) * _rotate_about_shaft(build_cam_plate("left", params), angle, params),
        Pos(5.0, 0.0, 0.0) * _rotate_about_shaft(build_cam_plate("right", params), angle, params),
        Pos(12.0, 0.0, 0.0) * build_fixed_plate("right", params),
        Pos(0.0, -25.0, 0.0) * build_base(params),
        Pos(0.0, 0.0, 12.0) * build_shaft(angle, params),
        Pos(-8.0, 0.0, 12.0) * build_shaft_keeper(params),
    ]
    for index, name in enumerate(ROD_NAMES):
        parts.append(Pos(0.0, 0.0, 12.0 + index * 5.0) * build_rod(name, angle, params))
    parts.extend(build_retainers(angle, params, 12.0, -10.0).children)
    return Compound(children=parts, label="p11_exploded_four_discs_three_rods_simple_hardware")


def _on_bed(shape: Shape, x: float, y: float, y_rotation: float = 90.0) -> Shape:
    placed = Rot(0.0, y_rotation, 0.0) * copy(shape)
    box = placed.bounding_box()
    return Pos(x - (box.min.X + box.max.X) / 2.0,
               y - (box.min.Y + box.max.Y) / 2.0, -box.min.Z) * placed


def build_print_kit(params: P11Parameters = P11_DEFAULTS) -> Compound:
    parts: list[Shape] = [
        _on_bed(build_fixed_plate("left", params, seated=False), -35.0, -32.0),
        _on_bed(build_cam_plate("left", params), 35.0, -32.0),
        _on_bed(build_cam_plate("right", params), -35.0, 32.0),
        _on_bed(build_fixed_plate("right", params, seated=False), 35.0, 32.0),
        _on_bed(build_base(params), 0.0, -77.0, 0.0),
        _on_bed(build_shaft(0.0, params), 0.0, 71.0, 0.0),
        # Keepers are constant-X C profiles.  Rotate X thickness into +Z so
        # the complete C face is on the bed instead of standing on an arm.
        _on_bed(build_shaft_keeper(params), -28.0, 71.0, -90.0),
    ]
    closed = rod_center("upright", params.end_angle, params)
    for i in range(3):
        # -90 degrees maps the cap's +X socket opening to +Z and puts its
        # closed circular end on the bed.  The same rotation lays each rod
        # keeper's complete C profile flat with its 2.9 mm thickness in Z.
        parts.append(_on_bed(build_left_cap(closed, params), -70.0, -15.0 + i * 15.0, -90.0))
        parts.append(_on_bed(build_right_keeper(closed, params), 70.0, -15.0 + i * 15.0, -90.0))
    return Compound(children=parts, label="p11_print_kit_small_retainers_flat_support_free")


def _coupon_block_with_bores(widths: tuple[float, ...], label: str, y: float) -> Shape:
    block = _box((0.0, y, 2.0), (30.0, 10.0, 4.0))
    for i, width in enumerate(widths):
        x = (i - (len(widths) - 1) / 2.0) * 8.0
        block = block - Pos(x, y, 2.0) * Cylinder(width / 2.0, 6.0,
            align=(Align.CENTER, Align.CENTER, Align.CENTER))
    return _label(block, label, "#758086")


def build_fit_coupon(params: P11Parameters = P11_DEFAULTS) -> Compound:
    datum = _coupon_block_with_bores((4.3, 4.4, 4.5), "datum_bores_4p3_4p4_4p5", -7.0)
    follower = _coupon_block_with_bores((4.8, 5.0), "follower_bores_4p8_5p0", 7.0)
    shaft = _coupon_block_with_bores((6.1, 6.2, 6.3), "shaft_bores_6p1_6p2_6p3", 21.0)
    return Compound(children=[datum, follower, shaft], label="p11_fit_coupon_print_before_mechanism")


def construction_height_delta(params: P11Parameters = P11_DEFAULTS) -> float:
    # Worst opposite construction errors across the complete guide span,
    # linearly interpolated over the 8 mm conductor spacing.
    guide_span = params.right_fixed_x - params.left_fixed_x
    return (2.0 * params.construction_offset) * (2.0 * params.wire_x) / guide_span


def stop_signed_clearance(angle_deg: float, params: P11Parameters = P11_DEFAULTS) -> float:
    """Analytic cam-channel end clearance: positive clear, 0 tangent, negative overlap."""
    endpoint = params.end_angle - stop_channel_extension_angle(params)
    chord = 2.0 * params.stop_radius * sin(radians(abs(endpoint - angle_deg)) / 2.0)
    return 0.10 - chord


def build_rod_withdraw_sweep(name: RodName, params: P11Parameters = P11_DEFAULTS) -> Shape:
    p = rod_center(name, 0.0, params)
    rod = _x_cylinder(params.rod_diameter, params.rod_length + abs(params.rod_withdraw_x),
                      params.rod_withdraw_x / 2.0, p.y, p.z)
    cap = _x_cylinder(7.0, 3.7 + abs(params.rod_withdraw_x),
                      -params.axial_body / 2.0 - 2.05 + params.rod_withdraw_x / 2.0, p.y, p.z)
    return _label(rod + cap, f"continuous_{name}_rod_and_left_cap_minusX_sweep", "#CAD2D5")


def build_intact_open_removal_failure_sweep(
    params: P11Parameters = P11_DEFAULTS,
) -> Shape:
    """Document the first rigid-body blocker before the fallback is invoked."""
    start = rod_center("diagonal", 0.0, params)
    end = PointYZ(start.y + params.core_remove_y, start.z)
    return _label(
        _straight_slot_x(start, end, params.rod_diameter, 0.0, params.rod_length),
        "FAILED_intact_OPEN_minusY_first_blocker_diagonal_rod_crosses_fixed_pigtail",
        "#C34A3D",
    )


def build_core_remove_sweep(params: P11Parameters = P11_DEFAULTS) -> Compound:
    # Sweep each rigid component's own bounding prism.  A single global core
    # bbox falsely fills the 26 mm central X corridor and therefore claims a
    # collision with a wire that lies between the separated side plates.
    core_parts = [build_base(params), *build_principal_plates(0.0, params).children]
    sweeps: list[Shape] = []
    for index, part in enumerate(core_parts):
        box = part.bounding_box()
        swept = _box(((box.min.X + box.max.X) / 2.0,
                      (box.min.Y + box.max.Y + params.core_remove_y) / 2.0,
                      (box.min.Z + box.max.Z) / 2.0),
                     (box.size.X, box.size.Y + abs(params.core_remove_y), box.size.Z))
        sweeps.append(_label(swept, f"component_{index}_continuous_minusY_prism", "#91A4AA"))
    start = PointYZ(params.shaft_y, params.shaft_z)
    end = PointYZ(params.shaft_y + params.core_remove_y, params.shaft_z)
    # The keyed shaft is contained by this exact Ø6 capsule sweep.  End head
    # and snap bboxes remain axially remote from the two X=+/-4 wires.
    key_length = params.axial_body + 2.0
    sweeps.append(_label(_straight_slot_x(
        start, end, params.shaft_diameter, 0.0, key_length,
    ), "keyed_shaft_continuous_minusY_capsule", "#91A4AA"))
    for index, (x, diameter, length) in enumerate((
        (-key_length / 2.0 - 1.0, params.shaft_neck_diameter, 2.0),
        (key_length / 2.0 + 0.9, 9.0, 1.8),
    )):
        sweeps.append(_label(_box(
            (x, (params.shaft_y * 2.0 + params.core_remove_y) / 2.0, params.shaft_z),
            (length, diameter + abs(params.core_remove_y), diameter),
        ), f"shaft_end_{index}_continuous_minusY_prism", "#91A4AA"))
    # The removal-clear artifact carries the already-disengaged keeper with
    # the core to core_remove_y.  Prove that complete path, not just the first
    # 10 mm throat-disengagement segment.
    sweeps.append(build_shaft_keeper_escape_sweep(params, params.core_remove_y))
    return Compound(children=sweeps, label="continuous_per_component_core_minusY_removal_sweeps")
