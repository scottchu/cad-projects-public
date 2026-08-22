"""P8 open three-rod cam bender.

The audited P7 follower math is preserved, while the opaque side walls and
scroll discs are replaced with open guide cheeks and skeletal cam spiders.
The lead is exactly vertical from 70 through the 80 degree end-stop dwell.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, degrees, hypot, pi, radians, sin
from typing import Literal

from build123d import (
    Align, Box, CenterArc, Compound, Cylinder, Line, Pos, Rot, Shape, Sphere,
    Vector, Wire, sweep,
)
from cadgen import srgb

from xt60_bend_jig.p2_corner_clamp import PointYZ
from xt60_bend_jig.p7_three_rod_scroll import (
    P7Parameters, _rotate_about_shaft, _slot_solid_x,
    _straight_slot_solid_x, _x_cylinder, _x_hex_prism,
    build_cap as _p7_build_cap, inverse_slot_point, rod_center, slot_path,
    smoothstep01, travel_at_angle,
)


RodName = Literal["upright", "bottom", "diagonal"]
Side = Literal["left", "right"]
ROD_NAMES: tuple[RodName, ...] = ("upright", "bottom", "diagonal")


@dataclass(frozen=True, slots=True)
class P8Parameters(P7Parameters):
    guide_rail_width: float = 9.4
    cam_rail_width: float = 8.8
    connector_rib_width: float = 3.6
    guide_boss_diameter: float = 14.0
    cam_hub_diameter: float = 24.0
    stop_pin_radius: float = 9.0
    stop_arc_width: float = 3.4
    lock_radius: float = 5.0
    crossmember_y: float = 12.0
    crossmember_z: float = 10.5
    crossmember_depth_y: float = 6.0
    crossmember_height: float = 4.0
    foot_y: float = 1.0
    foot_z: float = 8.5
    foot_depth_y: float = 28.0
    foot_height: float = 3.0
    wire_start_y: float = 28.0
    wire_start_z: float = 30.0
    straight_leg: float = 22.0
    pad_top_z: float = 27.85


P8_DEFAULTS = P8Parameters()


@dataclass(frozen=True, slots=True)
class WorkpieceState:
    shaft_angle_deg: float
    bend_angle_rad: float
    arc_end: PointYZ
    tangent: PointYZ
    tail_length: float
    endpoint: PointYZ


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def workpiece_state(angle_deg: float, params: P8Parameters = P8_DEFAULTS) -> WorkpieceState:
    if not 0.0 <= angle_deg <= params.end_angle:
        raise ValueError(f"angle must be within 0..{params.end_angle:g} degrees")
    alpha = pi / 2.0 * smoothstep01(angle_deg / params.rise_angle)
    arc_end = PointYZ(6.0 - params.bend_radius * sin(alpha), 36.0 - params.bend_radius * cos(alpha))
    tangent = PointYZ(-cos(alpha), sin(alpha))
    tail = params.available_lead - params.straight_leg - params.bend_radius * alpha
    endpoint = PointYZ(arc_end.y + tail * tangent.y, arc_end.z + tail * tangent.z)
    return WorkpieceState(angle_deg, alpha, arc_end, tangent, tail, endpoint)


def _guide_endpoints(name: RodName, params: P8Parameters) -> tuple[PointYZ, PointYZ]:
    return rod_center(name, 0.0, params), rod_center(name, params.end_angle, params)


def _rib(first: PointYZ, second: PointYZ, x: float, depth: float, width: float) -> Shape:
    return _straight_slot_solid_x(first, second, width, x, depth)


def lock_point(params: P8Parameters = P8_DEFAULTS) -> PointYZ:
    theta = radians(params.end_angle)
    return PointYZ(
        params.shaft_y + cos(theta) * -params.lock_radius,
        params.shaft_z + sin(theta) * -params.lock_radius,
    )


def stop_pin_point(params: P8Parameters = P8_DEFAULTS) -> PointYZ:
    return PointYZ(params.shaft_y + params.stop_pin_radius, params.shaft_z)


def build_guide_cheek(side: Side, params: P8Parameters = P8_DEFAULTS) -> Shape:
    """One narrow stationary cheek with an exterior-connected central window."""
    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.fixed_plate_center_x
    depth = params.fixed_plate_thickness
    base: Shape = _x_cylinder(params.guide_boss_diameter, depth, x, params.shaft_y, params.shaft_z)
    tools: list[Shape] = []
    for name in ROD_NAMES:
        first, second = _guide_endpoints(name, params)
        base = base + _straight_slot_solid_x(first, second, params.guide_rail_width, x, depth)
        tools.append(_straight_slot_solid_x(first, second, params.guide_slot_width, x, depth + 2.0))
    # Only short ties between nearest rail edges; there is no enclosing wall.
    for first, second in (
        (PointYZ(-3.0, 34.0), PointYZ(2.0, 36.0)),
        (PointYZ(5.0, 31.0), PointYZ(8.5, 27.5)),
        (PointYZ(-6.0, 27.5), PointYZ(7.0, 20.0)),
    ):
        base = base + _rib(first, second, x, depth, params.connector_rib_width)
    cheek = base - tools - _x_cylinder(params.shaft_bore_diameter, depth + 2.0, x, params.shaft_y, params.shaft_z)
    if side == "right":
        stop = stop_pin_point(params)
        stop_depth = params.scroll_plate_thickness + params.scroll_axial_clearance + 1.0
        stop_x = params.fixed_plate_outer_x - 0.5 + stop_depth / 2.0
        cheek = cheek + _x_cylinder(params.stop_pin_diameter, stop_depth, stop_x, stop.y, stop.z)
        lock = lock_point(params)
        cheek = cheek - _x_cylinder(params.end_lock_pin_diameter + 0.2, depth + 2.0, x, lock.y, lock.z)
    return _label(cheek, f"{side}_open_L_guide_cheek_three_narrow_rails", "#2E6845")


def build_fixed_frame(params: P8Parameters = P8_DEFAULTS) -> Shape:
    span = 2.0 * params.fixed_plate_outer_x + 0.4
    crossmember = Pos(0.0, params.crossmember_y, params.crossmember_z) * Box(
        span, params.crossmember_depth_y, params.crossmember_height,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    foot = Pos(0.0, params.foot_y, params.foot_z) * Box(
        span, params.foot_depth_y, params.foot_height,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    frame = build_guide_cheek("left", params) + build_guide_cheek("right", params) + crossmember + foot
    return _label(frame, "open_frame_two_L_cheeks_one_low_crossmember_one_flat_clamp_foot", "#315D43")


def _stop_arc_points(params: P8Parameters, steps: int = 40) -> tuple[PointYZ, ...]:
    return tuple(
        PointYZ(
            params.shaft_y + params.stop_pin_radius * cos(radians(-params.end_angle * i / steps)),
            params.shaft_z + params.stop_pin_radius * sin(radians(-params.end_angle * i / steps)),
        ) for i in range(steps + 1)
    )


def build_cam_spider(side: Side, params: P8Parameters = P8_DEFAULTS) -> Shape:
    """Predominantly-open cam with three inverse-slot rails and no outer ring."""
    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.scroll_plate_center_x
    depth = params.scroll_plate_thickness
    base: Shape = _x_cylinder(params.cam_hub_diameter, depth, x, params.shaft_y, params.shaft_z)
    slot_tools: list[Shape] = []
    for name in ROD_NAMES:
        path = slot_path(name, params)
        base = base + _slot_solid_x(path, params.cam_rail_width, x, depth)
        slot_tools.append(_slot_solid_x(path, params.scroll_slot_width, x, depth + 2.0))
        nearest = min(path, key=lambda q: hypot(q.y - params.shaft_y, q.z - params.shaft_z))
        base = base + _rib(params.shaft_center, nearest, x, depth, params.connector_rib_width)
    tools: list[Shape] = [
        *slot_tools,
        _x_hex_prism(params.scroll_hex_socket_across_corners, depth + 2.0, x, params.shaft_y, params.shaft_z),
        _slot_solid_x(_stop_arc_points(params), params.stop_arc_width, x, depth + 2.0),
        _x_cylinder(params.end_lock_pin_diameter + 0.2, depth + 2.0, x, params.shaft_y - params.lock_radius, params.shaft_z),
    ]
    return _label(base - tools, f"{side}_open_cam_spider_three_inverse_slot_rails_true_dwell", "#D69B16")


def build_rod(name: RodName, angle_deg: float, params: P8Parameters = P8_DEFAULTS) -> Shape:
    point = rod_center(name, angle_deg, params)
    return _label(_x_cylinder(params.rod_diameter, params.rod_length, 0.0, point.y, point.z),
                  f"purchased_304_stainless_{name}_rod_4x50", "#BEC7CC")


def build_rods(angle_deg: float, params: P8Parameters = P8_DEFAULTS) -> Compound:
    return Compound(children=[build_rod(name, angle_deg, params) for name in ROD_NAMES],
                    label=f"exactly_three_purchased_4x50_rods_at_{angle_deg:.1f}deg")


def build_cap(side: Side, point: PointYZ, params: P8Parameters = P8_DEFAULTS) -> Shape:
    cap = _p7_build_cap(side, point, params)
    cap.label = ("left_press_cap_3p90_trial_requires_print_validation" if side == "left" else
                 "right_removable_snap_keeper_4p10_3p60_trial_requires_print_validation")
    return cap


def build_caps(angle_deg: float, params: P8Parameters = P8_DEFAULTS) -> Compound:
    children: list[Shape] = []
    for name in ROD_NAMES:
        point = rod_center(name, angle_deg, params)
        children.extend((build_cap("left", point, params), build_cap("right", point, params)))
    return Compound(children=children, label="six_prototype_rod_retainers")


def build_shaft_and_dial(angle_deg: float, params: P8Parameters = P8_DEFAULTS) -> Shape:
    shaft = (
        _x_hex_prism(params.shaft_diameter, 1.8, -26.1, params.shaft_y, params.shaft_z)
        + _x_hex_prism(params.shaft_keeper_neck_across_corners, 3.4, -23.6, params.shaft_y, params.shaft_z)
        + _x_hex_prism(params.shaft_diameter, 53.0, 4.5, params.shaft_y, params.shaft_z)
    )
    shoulder = _x_cylinder(9.0, 2.0, 23.1, params.shaft_y, params.shaft_z)
    dial_x = 30.0
    dial = Pos(dial_x, params.shaft_y, params.shaft_z) * Cylinder(
        9.0, 5.0, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER))
    pointer = Pos(dial_x, params.shaft_y + 7.0, params.shaft_z) * Box(
        5.0, 5.0, 2.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    return _label(_rotate_about_shaft(shaft + shoulder + dial + pointer, angle_deg, params),
                  "shared_keyed_shaft_single_right_dial", "#202427")


def build_shaft_keeper(params: P8Parameters = P8_DEFAULTS) -> Shape:
    thickness = 3.0
    x = -(params.scroll_plate_outer_x + params.axial_float) - thickness / 2.0
    outer = _x_cylinder(10.0, thickness, x, params.shaft_y, params.shaft_z)
    pocket = _x_cylinder(params.shaft_keeper_pocket, thickness + 1.0, x, params.shaft_y, params.shaft_z)
    opening = Pos(x, params.shaft_y + 5.0, params.shaft_z) * Box(
        thickness + 1.0, 10.0, params.shaft_keeper_throat,
        align=(Align.CENTER, Align.CENTER, Align.CENTER))
    return _label(outer - pocket - opening,
                  "left_radial_shaft_keeper_true_axial_capture_on_reduced_neck", "#4B5357")


def build_end_lock_pin(params: P8Parameters = P8_DEFAULTS) -> Shape:
    point = lock_point(params)
    shaft = _x_cylinder(params.end_lock_pin_diameter, 9.0, 19.5, point.y, point.z)
    knob = _x_cylinder(6.0, 2.5, 25.25, point.y, point.z)
    return _label(shaft + knob, "removable_axial_lock_pin_exact_80deg_only", "#9B3434")


def build_wire_centerline(angle_deg: float, x: float, params: P8Parameters = P8_DEFAULTS) -> Wire:
    state = workpiece_state(angle_deg, params)
    start = Vector(x, params.wire_start_y, params.wire_start_z)
    endpoint = Vector(x, state.endpoint.y, state.endpoint.z)
    if state.bend_angle_rad <= 1e-12:
        return Wire([Line(start, endpoint).edge()])
    first = Line(start, Vector(x, 6.0, 30.0))
    arc = CenterArc(Vector(x, 6.0, 36.0), params.bend_radius, -90.0, -degrees(state.bend_angle_rad))
    last = Line(Vector(x, state.arc_end.y, state.arc_end.z), endpoint)
    return Wire([first.edge(), arc.edge(), last.edge()])


def build_wire(angle_deg: float, x: float, params: P8Parameters = P8_DEFAULTS) -> Shape:
    centerline = build_wire_centerline(angle_deg, x, params)
    return sweep(Wire.make_circle(params.wire_diameter / 2.0, centerline ^ 0.0), centerline)


def build_wires(angle_deg: float, params: P8Parameters = P8_DEFAULTS) -> Compound:
    children = [
        _label(build_wire(angle_deg, x, params),
               ("nonphysical_mid_deformation_reference_" if 0.0 < angle_deg < 70.0 else "physical_")
               + f"12AWG_lead_x{x:+g}_44mm_state_{angle_deg:g}", color)
        for x, color in ((-4.0, "#16191A"), (4.0, "#D83A2F"))
    ]
    return Compound(children=children, label=(
        "nonphysical_mid_deformation_reference_excluded_from_collision_claims"
        if 0.0 < angle_deg < 70.0 else f"two_physical_12AWG_leads_{angle_deg:g}deg"))


def build_esc_with_pads(params: P8Parameters = P8_DEFAULTS) -> Compound:
    esc = _label(Pos(0.0, 46.0, 25.75) * Box(
        36.0, 36.0, 3.5, align=(Align.CENTER, Align.CENTER, Align.CENTER)),
        "reference_bottom_ESC_below_FC", "#25292A")
    children: list[Shape] = [esc]
    for x, name in ((-4.0, "negative"), (4.0, "positive")):
        pad = Pos(x, 30.5, (27.5 + params.pad_top_z) / 2.0) * Box(
            5.0, 5.0, params.pad_top_z - 27.5, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        solder = Pos(x, params.wire_start_y, 28.2) * Sphere(2.2)
        children.extend((
            _label(pad, f"copper_{name}_pad_zero_gap_top_datum", "#D7982D"),
            _label(solder, f"solder_reference_{name}", "#BFC5C7"),
        ))
    return Compound(children=children, label="bottom_ESC_two_copper_pads_and_solder_references")


def build_fc_reference() -> Shape:
    return _label(Pos(0.0, 46.0, 32.0) * Box(
        36.0, 36.0, 2.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)),
        "reference_FC_above_bottom_ESC", "#3A4040")


def build_xt60(angle_deg: float, params: P8Parameters = P8_DEFAULTS) -> Shape:
    state = workpiece_state(angle_deg, params)
    length = 20.5
    body = Pos(0.0,
               state.endpoint.y + state.tangent.y * length / 2.0,
               state.endpoint.z + state.tangent.z * length / 2.0) * Rot(
        90.0 - degrees(state.bend_angle_rad), 0.0, 0.0) * Box(
            15.9, 8.1, length, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    return _label(body, f"reference_XT60_axis_follows_terminal_tangent_{angle_deg:g}deg", "#E6B51F")


def build_loaded(angle_deg: float, params: P8Parameters = P8_DEFAULTS) -> Compound:
    children: list[Shape] = [
        build_fixed_frame(params),
        _rotate_about_shaft(build_cam_spider("left", params), angle_deg, params),
        _rotate_about_shaft(build_cam_spider("right", params), angle_deg, params),
    ]
    children.extend(build_rods(angle_deg, params).children)
    children.extend(build_caps(angle_deg, params).children)
    children.extend((build_shaft_and_dial(angle_deg, params), build_shaft_keeper(params)))
    if abs(angle_deg - params.end_angle) <= 1e-9:
        children.append(build_end_lock_pin(params))
    children.extend((build_wires(angle_deg, params), build_esc_with_pads(params),
                     build_fc_reference(), build_xt60(angle_deg, params)))
    return Compound(children=children, label=f"p8_open_three_rod_cam_loaded_{angle_deg:g}deg")


def build_loaded_open(params: P8Parameters = P8_DEFAULTS) -> Compound:
    return build_loaded(0.0, params)


def build_loaded_mid(params: P8Parameters = P8_DEFAULTS) -> Compound:
    return build_loaded(35.0, params)


def build_loaded_closed(params: P8Parameters = P8_DEFAULTS) -> Compound:
    return build_loaded(params.end_angle, params)


def build_exploded(params: P8Parameters = P8_DEFAULTS) -> Compound:
    children: list[Shape] = [build_fixed_frame(params)]
    children.extend((
        Pos(-12.0, 0.0, 0.0) * build_cam_spider("left", params),
        Pos(12.0, 0.0, 0.0) * build_cam_spider("right", params),
    ))
    for index, name in enumerate(ROD_NAMES):
        dz = 18.0 + index * 8.0
        point = rod_center(name, 0.0, params)
        children.extend((
            Pos(0.0, 0.0, dz) * build_rod(name, 0.0, params),
            Pos(-12.0, 0.0, dz) * build_cap("left", point, params),
            Pos(12.0, 10.0 + index * 4.0, dz) * build_cap("right", point, params),
        ))
    children.extend((
        Pos(0.0, 0.0, -12.0) * build_shaft_and_dial(0.0, params),
        Pos(-10.0, 10.0, -12.0) * build_shaft_keeper(params),
        Pos(10.0, 10.0, -12.0) * build_end_lock_pin(params),
    ))
    return Compound(children=children, label="p8_exploded_open_cam_assembly_order")


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation is not None else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P8Parameters = P8_DEFAULTS) -> Compound:
    parts: list[Shape] = [
        _on_bed(build_fixed_frame(params), 0.0, 0.0),
        _on_bed(build_cam_spider("left", params), 76.0, 0.0, Rot(0.0, 90.0, 0.0)),
        _on_bed(build_cam_spider("right", params), 76.0, 70.0, Rot(0.0, 90.0, 0.0)),
        _on_bed(build_shaft_and_dial(0.0, params), 145.0, 0.0, Rot(0.0, 90.0, 0.0)),
        _on_bed(build_shaft_keeper(params), 175.0, 28.0, Rot(0.0, 90.0, 0.0)),
        _on_bed(build_end_lock_pin(params), 188.0, 28.0, Rot(0.0, 90.0, 0.0)),
    ]
    origin = PointYZ(0.0, 0.0)
    for index in range(3):
        parts.extend((
            _on_bed(build_cap("left", origin, params), 202.0 + index * 11.0, 0.0, Rot(0.0, 90.0, 0.0)),
            _on_bed(build_cap("right", origin, params), 202.0 + index * 11.0, 13.0, Rot(0.0, 90.0, 0.0)),
        ))
    for index, part in enumerate(parts):
        part.label = f"print_{index:02d}_{part.label}"
    return Compound(children=parts, label="p8_print_kit_twelve_printed_parts_no_rods_or_electronics")


def cam_projected_area_fraction(side: Side = "right", params: P8Parameters = P8_DEFAULTS) -> float:
    return build_cam_spider(side, params).volume / params.scroll_plate_thickness / (
        pi * (params.scroll_diameter / 2.0) ** 2)


__all__ = [
    "P8_DEFAULTS", "P8Parameters", "WorkpieceState", "build_cam_spider",
    "build_cap", "build_caps", "build_end_lock_pin", "build_esc_with_pads",
    "build_exploded", "build_fc_reference", "build_fixed_frame",
    "build_guide_cheek", "build_loaded", "build_loaded_closed",
    "build_loaded_mid", "build_loaded_open", "build_print_kit", "build_rod",
    "build_rods", "build_shaft_and_dial", "build_shaft_keeper", "build_wire",
    "build_wire_centerline", "build_wires", "build_xt60",
    "cam_projected_area_fraction", "inverse_slot_point", "lock_point",
    "rod_center", "slot_path", "stop_pin_point", "travel_at_angle",
    "workpiece_state",
]
