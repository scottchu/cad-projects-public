"""P7 synchronized three-rod scroll prototype.

The purchased rods run on X.  Motion is solved in the YZ side view.  Each
rotating scroll slot is generated from the inverse kinematic relationship

    q(theta) = R(-theta) * (p(theta) - shaft_center)

rather than drawn by eye.  The follower centers move during 0..70 degrees and
remain fixed during the 70..80 degree constant-radius dwell.  The 80 degree
positive stop is therefore also the exact 90 degree workpiece pose.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, pi, radians, sin, sqrt
from typing import Literal

from build123d import Align, Box, Compound, Cylinder, Edge, Face, Plane, Pos, RegularPolygon, Rot, Shape, Side as OffsetSide, Wire, extrude
from cadgen import srgb

from xt60_bend_jig.p2_corner_clamp import (
    PointYZ,
    build_esc,
    build_fc,
    build_reference_rod as _p2_reference_rod,
    build_wires,
    build_xt60,
    rod_centers as _p2_closed_centers,
)


RodName = Literal["upright", "bottom", "diagonal"]
Side = Literal["left", "right"]


@dataclass(frozen=True, slots=True)
class P7Parameters:
    rod_diameter: float = 4.0
    rod_length: float = 50.0
    wire_diameter: float = 4.3
    bend_radius: float = 6.0
    available_lead: float = 44.0
    stroke: float = 11.0
    rise_angle: float = 70.0
    end_angle: float = 80.0
    guide_slot_width: float = 4.4
    scroll_slot_width: float = 4.4
    fixed_plate_thickness: float = 3.0
    scroll_plate_thickness: float = 2.5
    clear_span: float = 32.0
    scroll_axial_clearance: float = 0.30
    scroll_diameter: float = 64.0
    shaft_y: float = -7.5
    shaft_z: float = 32.5
    shaft_diameter: float = 6.0
    shaft_bore_diameter: float = 6.2
    scroll_hex_socket_across_corners: float = 6.15
    fixed_plate_y_min: float = -21.0
    fixed_plate_y_max: float = 24.0
    fixed_plate_z_min: float = 8.0
    fixed_plate_z_max: float = 73.0
    cap_body_diameter: float = 7.0
    cap_length: float = 4.0
    cap_socket_depth: float = 2.9
    left_cap_bore: float = 3.90
    right_cap_bore: float = 4.10
    right_keeper_snap_throat: float = 3.60
    axial_float: float = 0.30
    stop_tab_radial_min: float = 31.0
    stop_tab_radial_max: float = 36.0
    stop_tab_tangent_width: float = 3.0
    stop_pin_diameter: float = 3.0
    end_lock_pin_diameter: float = 3.0
    end_lock_radius: float = 8.5
    shaft_keeper_pocket: float = 5.4
    shaft_keeper_throat: float = 4.7
    shaft_keeper_neck_across_corners: float = 5.2
    shaft_keeper_neck_width: float = 3.2

    @property
    def fixed_plate_center_x(self) -> float:
        return self.clear_span / 2.0 + self.fixed_plate_thickness / 2.0

    @property
    def fixed_plate_outer_x(self) -> float:
        return self.clear_span / 2.0 + self.fixed_plate_thickness

    @property
    def scroll_plate_center_x(self) -> float:
        return self.fixed_plate_outer_x + self.scroll_axial_clearance + self.scroll_plate_thickness / 2.0

    @property
    def scroll_plate_outer_x(self) -> float:
        return self.fixed_plate_outer_x + self.scroll_axial_clearance + self.scroll_plate_thickness

    @property
    def rod_projection(self) -> float:
        return self.rod_length / 2.0 - self.scroll_plate_outer_x

    @property
    def cap_inner_x(self) -> float:
        return self.scroll_plate_outer_x + self.axial_float

    @property
    def shaft_center(self) -> PointYZ:
        return PointYZ(self.shaft_y, self.shaft_z)


P7_DEFAULTS = P7Parameters()


_CLOSED: dict[RodName, PointYZ] = {
    "upright": PointYZ(-4.15, 42.0),
    "bottom": PointYZ(12.0, 25.85),
    "diagonal": PointYZ(4.691852455, 34.691852455),
}
_CLOSE_DIR: dict[RodName, PointYZ] = {
    "upright": PointYZ(1.0, 0.0),
    "bottom": PointYZ(0.0, 1.0),
    "diagonal": PointYZ(-1.0 / sqrt(2.0), -1.0 / sqrt(2.0)),
}


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


def smoothstep01(value: float) -> float:
    value = min(1.0, max(0.0, value))
    return value * value * (3.0 - 2.0 * value)


def travel_at_angle(angle_deg: float, params: P7Parameters = P7_DEFAULTS) -> float:
    """Common closing travel; the final ten degrees are a true dwell."""

    if not 0.0 <= angle_deg <= params.end_angle:
        raise ValueError(f"angle must be within 0..{params.end_angle:g} degrees")
    return params.stroke * smoothstep01(angle_deg / params.rise_angle)


def rod_center(name: RodName, angle_deg: float, params: P7Parameters = P7_DEFAULTS) -> PointYZ:
    closed = _CLOSED[name]
    direction = _CLOSE_DIR[name]
    remaining = params.stroke - travel_at_angle(angle_deg, params)
    return PointYZ(closed.y - direction.y * remaining, closed.z - direction.z * remaining)


def inverse_slot_point(name: RodName, angle_deg: float, params: P7Parameters = P7_DEFAULTS) -> PointYZ:
    """Follower center in the unrotated scroll plate coordinate frame."""

    point = rod_center(name, angle_deg, params)
    dy = point.y - params.shaft_y
    dz = point.z - params.shaft_z
    theta = radians(angle_deg)
    return PointYZ(
        params.shaft_y + cos(theta) * dy + sin(theta) * dz,
        params.shaft_z - sin(theta) * dy + cos(theta) * dz,
    )


def slot_path(name: RodName, params: P7Parameters = P7_DEFAULTS, step_deg: float = 2.0) -> tuple[PointYZ, ...]:
    count = round(params.end_angle / step_deg)
    return tuple(inverse_slot_point(name, params.end_angle * index / count, params) for index in range(count + 1))


def _slot_solid_x(points: tuple[PointYZ, ...], width: float, x: float, depth: float) -> Shape:
    """One exact planar obround/spline slot extruded through an X plate."""

    vectors = [(0.0, point.y, point.z) for point in points]
    path = Wire([Edge.make_line(vectors[0], vectors[1])]) if len(vectors) == 2 else Wire.make_polygon(vectors)
    outline = path.offset_2d(width / 2.0, side=OffsetSide.BOTH, closed=True)
    tool = extrude(Face(outline), depth / 2.0, both=True)
    return Pos(x, 0.0, 0.0) * tool


def _straight_slot_solid_x(first: PointYZ, second: PointYZ, width: float, x: float, depth: float) -> Shape:
    """Straight YZ capsule whose through direction is unambiguously X."""

    dy, dz = second.y - first.y, second.z - first.z
    length = hypot(dy, dz)
    angle = 180.0 / pi * atan2(dz, dy)
    bar = Pos(x, (first.y + second.y) / 2.0, (first.z + second.z) / 2.0) * Rot(angle, 0.0, 0.0) * Box(
        depth, length, width, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    return bar + _x_cylinder(width, depth, x, first.y, first.z) + _x_cylinder(width, depth, x, second.y, second.z)


def _x_hex_prism(across_corners: float, length: float, x: float, y: float, z: float) -> Shape:
    face = RegularPolygon(across_corners / 2.0, 6, rotation=30.0)
    # RegularPolygon is on XY and extrudes on Z; reorient its axis to X.
    prism = Rot(0.0, 90.0, 0.0) * extrude(face, length / 2.0, both=True)
    return Pos(x, y, z) * prism


def _rotate_about_shaft(shape: Shape, angle_deg: float, params: P7Parameters) -> Shape:
    return Pos(0.0, params.shaft_y, params.shaft_z) * Rot(angle_deg, 0, 0) * Pos(
        0.0, -params.shaft_y, -params.shaft_z
    ) * shape


def build_fixed_frame(params: P7Parameters = P7_DEFAULTS) -> Shape:
    """One rigid printable frame: two guide plates, remote ties and clamp tab."""

    plate_y = (params.fixed_plate_y_min + params.fixed_plate_y_max) / 2.0
    plate_z = (params.fixed_plate_z_min + params.fixed_plate_z_max) / 2.0
    plate_dy = params.fixed_plate_y_max - params.fixed_plate_y_min
    plate_dz = params.fixed_plate_z_max - params.fixed_plate_z_min
    plates: list[Shape] = []
    for sign in (-1.0, 1.0):
        x = sign * params.fixed_plate_center_x
        plate = Pos(x, plate_y, plate_z) * Box(
            params.fixed_plate_thickness, plate_dy, plate_dz,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        guide_tools: list[Shape] = []
        for name in ("upright", "bottom", "diagonal"):
            guide_tools.append(
                _straight_slot_solid_x(
                    rod_center(name, 0.0, params), rod_center(name, params.end_angle, params),
                    params.guide_slot_width, x, params.fixed_plate_thickness + 2.0,
                )
            )
        shaft_bore = _x_cylinder(
            params.shaft_bore_diameter, params.fixed_plate_thickness + 2.0,
            x, params.shaft_y, params.shaft_z,
        )
        plates.append(plate - guide_tools - shaft_bore)

    # Both ties are outside the soldering/wire corridor.  They fuse the two
    # guide plates without occupying the 32 mm working span above Z=14.
    lower_tie = Pos(0.0, -18.0, 10.0) * Box(
        2.0 * params.fixed_plate_outer_x + 0.4, 6.0, 4.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    upper_tie = Pos(0.0, 21.0, 71.0) * Box(
        2.0 * params.fixed_plate_outer_x + 0.4, 6.0, 4.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    bench_tab = Pos(0.0, -28.5, 9.5) * Box(
        2.0 * params.fixed_plate_outer_x + 0.4, 17.0, 3.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    frame = plates[0] + plates[1] + lower_tie + upper_tie + bench_tab
    # The stop pins overlap the fixed guide plates by 1 mm, so they are a
    # retained part of the frame rather than loose tangent cylinders.
    for pin in build_stop_pins(params).children:
        frame = frame + pin
    # A remote arm routes around the outside of the scroll and returns behind
    # the dial.  Its Ø3 bore aligns with the dial only at the 80° final pose.
    lock = end_lock_point(params)
    bridge_z = 72.0
    bridge = Pos(23.0, lock.y, bridge_z) * Box(10.0, 6.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    arm = Pos(27.5, lock.y, (lock.z + bridge_z) / 2.0) * Box(
        3.0, 6.0, bridge_z - lock.z + 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    lock_bore = _x_cylinder(params.end_lock_pin_diameter + 0.2, 5.0, 27.5, lock.y, lock.z)
    frame = (frame + bridge + arm) - lock_bore
    return _label(
        frame,
        "fixed_two_guide_plate_frame_32mm_clear_span_with_remote_ties_and_flat_clamp_tab",
        "#315D43",
    )


def build_scroll_plate(side: Side, params: P7Parameters = P7_DEFAULTS) -> Shape:
    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.scroll_plate_center_x
    disc = Pos(x, params.shaft_y, params.shaft_z) * Cylinder(
        params.scroll_diameter / 2.0,
        params.scroll_plate_thickness,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    # A plain radial tab makes the final 80 degree stop inspectable.
    tab_mid = (params.stop_tab_radial_min + params.stop_tab_radial_max) / 2.0
    tab = Pos(x, params.shaft_y + tab_mid, params.shaft_z) * Box(
        params.scroll_plate_thickness,
        params.stop_tab_radial_max - params.stop_tab_radial_min,
        params.stop_tab_tangent_width,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    tools: list[Shape] = []
    for name in ("upright", "bottom", "diagonal"):
        tools.append(
            _slot_solid_x(
                slot_path(name, params), params.scroll_slot_width,
                x, params.scroll_plate_thickness + 2.0,
            )
        )
    shaft_bore = _x_hex_prism(
        params.scroll_hex_socket_across_corners,
        params.scroll_plate_thickness + 2.0,
        x,
        params.shaft_y,
        params.shaft_z,
    )
    return _label(
        (disc + tab) - tools - shaft_bore,
        f"{side}_mirrored_scroll_plate_three_inverse_kinematic_slots_true_70to80deg_dwell",
        "#D69B16",
    )


def build_stop_pins(params: P7Parameters = P7_DEFAULTS) -> Compound:
    """Two frame-anchored pins tangent to the advancing tab face at 80°."""

    theta = radians(params.end_angle)
    radial = (params.stop_tab_radial_min + params.stop_tab_radial_max) / 2.0
    tangent = params.stop_tab_tangent_width / 2.0 + params.stop_pin_diameter / 2.0
    local_y, local_z = radial, tangent
    world_y = params.shaft_y + cos(theta) * local_y - sin(theta) * local_z
    world_z = params.shaft_z + sin(theta) * local_y + cos(theta) * local_z
    pins: list[Shape] = []
    for sign in (-1.0, 1.0):
        # Span from the fixed outer face across the 0.4 mm running gap and the
        # scroll thickness so the contact is a real exterior stop.
        start = params.fixed_plate_outer_x - 1.0
        end = params.scroll_plate_outer_x + 0.5
        length = end - start
        x = sign * (start + length / 2.0)
        pins.append(
            _label(
                _x_cylinder(params.stop_pin_diameter, length, x, world_y, world_z),
                f"{('left' if sign < 0 else 'right')}_positive_80deg_stop_pin",
                "#26302B",
            )
        )
    return Compound(children=pins, label="paired_positive_80deg_end_stop_pins")


def build_rod(name: RodName, angle_deg: float, params: P7Parameters = P7_DEFAULTS) -> Shape:
    point = rod_center(name, angle_deg, params)
    return _label(
        _x_cylinder(params.rod_diameter, params.rod_length, 0.0, point.y, point.z),
        f"purchased_304_stainless_{name}_rod_4x50",
        "#BEC7CC",
    )


def build_rods(angle_deg: float, params: P7Parameters = P7_DEFAULTS) -> Compound:
    return Compound(
        children=[build_rod(name, angle_deg, params) for name in ("upright", "bottom", "diagonal")],
        label=f"exactly_three_purchased_4x50_rods_at_{angle_deg:.1f}deg",
    )


def build_shaft_and_dial(angle_deg: float, params: P7Parameters = P7_DEFAULTS) -> Shape:
    # A 3 mm long reduced hex neck positively captures the removable left
    # keeper between two full-size Ø6-across-corners shaft shoulders.
    shaft_left = _x_hex_prism(params.shaft_diameter, 1.8, -26.1, params.shaft_y, params.shaft_z)
    shaft_neck = _x_hex_prism(params.shaft_keeper_neck_across_corners, 3.4, -23.6, params.shaft_y, params.shaft_z)
    shaft_main = _x_hex_prism(params.shaft_diameter, 53.0, 4.5, params.shaft_y, params.shaft_z)
    shaft = shaft_left + shaft_neck + shaft_main
    # Fixed axial shoulder: 0.30 mm off the right scroll outer face.
    shoulder = _x_cylinder(10.0, 2.0, 23.1, params.shaft_y, params.shaft_z)
    dial_x = 33.0
    dial = Pos(dial_x, params.shaft_y, params.shaft_z) * Cylinder(
        11.0, 6.0, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    pointer = Pos(dial_x, params.shaft_y + 8.5, params.shaft_z) * Box(
        6.0, 6.0, 2.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    local_lock_bore = _x_cylinder(
        params.end_lock_pin_diameter + 0.2, 8.0, dial_x,
        params.shaft_y + params.end_lock_radius, params.shaft_z,
    )
    keyed = (shaft + shoulder + dial + pointer) - local_lock_bore
    return _label(
        _rotate_about_shaft(keyed, angle_deg, params),
        "shared_keyed_shaft_and_single_dial",
        "#202427",
    )


def build_cap(side: Side, point: PointYZ, params: P7Parameters = P7_DEFAULTS) -> Shape:
    """Left axial press cap or right radial snap-on C-keeper."""

    sign = -1.0 if side == "left" else 1.0
    inner = sign * params.cap_inner_x
    if side == "left":
        center_x = inner + sign * params.cap_length / 2.0
        body = _x_cylinder(params.cap_body_diameter, params.cap_length, center_x, point.y, point.z)
        socket_center = inner + sign * params.cap_socket_depth / 2.0
        socket = _x_cylinder(params.left_cap_bore, params.cap_socket_depth, socket_center, point.y, point.z)
        return _label(
            body - socket,
            "left_press_3p90_axial_cap_socket2p9_float0p30",
            "#C88714",
        )
    # Radially installed removable keeper: the Ø4.10 pocket is free running,
    # while the 3.60 mm throat snaps over the Ø4 rod and prevents axial loss.
    keeper_x = params.scroll_plate_outer_x + params.axial_float + params.cap_socket_depth / 2.0
    outer = _x_cylinder(params.cap_body_diameter, params.cap_socket_depth, keeper_x, point.y, point.z)
    pocket = _x_cylinder(params.right_cap_bore, params.cap_socket_depth + 1.0, keeper_x, point.y, point.z)
    radial_opening = Pos(keeper_x, point.y + params.cap_body_diameter / 2.0, point.z) * Box(
        params.cap_socket_depth + 1.0,
        params.cap_body_diameter,
        params.right_keeper_snap_throat,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return _label(
        outer - pocket - radial_opening,
        "right_radial_C_keeper_4p10_pocket_3p60_snap_throat_t2p9_float0p30",
        "#E0AE35",
    )


def build_caps(angle_deg: float, params: P7Parameters = P7_DEFAULTS) -> Compound:
    caps: list[Shape] = []
    for name in ("upright", "bottom", "diagonal"):
        point = rod_center(name, angle_deg, params)
        caps.extend((build_cap("left", point, params), build_cap("right", point, params)))
    return Compound(children=caps, label="six_simple_axial_caps_three_press_left_three_removable_right")


def build_shaft_keeper(params: P7Parameters = P7_DEFAULTS) -> Shape:
    """Radially removable left C-keeper gives the shared shaft axial capture."""

    thickness = 3.0
    inner_face = -(params.scroll_plate_outer_x + params.axial_float)
    x = inner_face - thickness / 2.0
    outer = _x_cylinder(10.0, thickness, x, params.shaft_y, params.shaft_z)
    pocket = _x_cylinder(params.shaft_keeper_pocket, thickness + 1.0, x, params.shaft_y, params.shaft_z)
    opening = Pos(x, params.shaft_y + 5.0, params.shaft_z) * Box(
        thickness + 1.0, 10.0, params.shaft_keeper_throat,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return _label(
        outer - pocket - opening,
        "left_radial_shaft_C_keeper_5p40_pocket_4p70_throat_on_5p20_neck_w3p20_t3_float0p30",
        "#4B5357",
    )


def end_lock_point(params: P7Parameters = P7_DEFAULTS) -> PointYZ:
    theta = radians(params.end_angle)
    return PointYZ(
        params.shaft_y + cos(theta) * params.end_lock_radius,
        params.shaft_z + sin(theta) * params.end_lock_radius,
    )


def build_end_lock_pin(params: P7Parameters = P7_DEFAULTS) -> Shape:
    point = end_lock_point(params)
    return _label(
        _x_cylinder(params.end_lock_pin_diameter, 12.0, 31.5, point.y, point.z),
        "removable_radial_end_lock_pin_d3_for_exact_80deg_pose",
        "#8E2F2F",
    )


def build_loaded(angle_deg: float, params: P7Parameters = P7_DEFAULTS) -> Compound:
    left = _rotate_about_shaft(build_scroll_plate("left", params), angle_deg, params)
    right = _rotate_about_shaft(build_scroll_plate("right", params), angle_deg, params)
    frame = build_fixed_frame(params)
    children: list[Shape] = [frame, left, right, *build_rods(angle_deg, params).children]
    children.extend(build_caps(angle_deg, params).children)
    children.extend((build_shaft_and_dial(angle_deg, params), build_shaft_keeper(params)))
    if abs(angle_deg - params.end_angle) <= 1e-9:
        children.append(build_end_lock_pin(params))
    children.extend((build_wires(), build_esc(), build_fc(), build_xt60()))
    return Compound(children=children, label=f"p7_three_rod_scroll_loaded_{angle_deg:.1f}deg")


def build_loaded_open(params: P7Parameters = P7_DEFAULTS) -> Compound:
    return build_loaded(0.0, params)


def build_loaded_mid(params: P7Parameters = P7_DEFAULTS) -> Compound:
    return build_loaded(40.0, params)


def build_loaded_closed(params: P7Parameters = P7_DEFAULTS) -> Compound:
    return build_loaded(params.end_angle, params)


def build_exploded(params: P7Parameters = P7_DEFAULTS) -> Compound:
    children: list[Shape] = [build_fixed_frame(params)]
    children.append(Pos(-12.0, 0.0, 0.0) * build_scroll_plate("left", params))
    children.append(Pos(12.0, 0.0, 0.0) * build_scroll_plate("right", params))
    for index, name in enumerate(("upright", "bottom", "diagonal")):
        children.append(Pos(0.0, 0.0, 18.0 + index * 7.0) * build_rod(name, 0.0, params))
        point = rod_center(name, 0.0, params)
        children.append(Pos(-12.0, 0.0, 18.0 + index * 7.0) * build_cap("left", point, params))
        # Radial (+Y) removal direction is explicit for each right C-keeper.
        children.append(Pos(12.0, 10.0 + index * 4.0, 18.0 + index * 7.0) * build_cap("right", point, params))
    children.append(Pos(0.0, 0.0, -12.0) * build_shaft_and_dial(0.0, params))
    children.append(Pos(-10.0, 10.0, -12.0) * build_shaft_keeper(params))
    children.append(Pos(10.0, 10.0, -12.0) * build_end_lock_pin(params))
    return Compound(children=children, label="p7_exploded_access_order_no_trapped_scrolls_or_rods")


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation is not None else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P7Parameters = P7_DEFAULTS) -> Compound:
    """Printed parts only; the three purchased rods and electronics are excluded."""

    parts: list[Shape] = [
        _on_bed(build_fixed_frame(params), 0.0, 0.0),
        _on_bed(build_scroll_plate("left", params), 72.0, 0.0, Rot(0, 90, 0)),
        _on_bed(build_scroll_plate("right", params), 72.0, 74.0, Rot(0, 90, 0)),
        _on_bed(build_shaft_and_dial(0.0, params), 142.0, 0.0, Rot(0, 90, 0)),
        _on_bed(build_shaft_keeper(params), 170.0, 30.0, Rot(0, 90, 0)),
        _on_bed(build_end_lock_pin(params), 185.0, 30.0, Rot(0, 90, 0)),
    ]
    for index in range(3):
        p = PointYZ(0.0, 0.0)
        parts.append(_on_bed(build_cap("left", p, params), 200.0 + index * 10.0, 0.0, Rot(0, 90, 0)))
        parts.append(_on_bed(build_cap("right", p, params), 200.0 + index * 10.0, 12.0, Rot(0, 90, 0)))
    for index, part in enumerate(parts):
        part.label = f"print_{index:02d}_{part.label}"
    return Compound(children=parts, label="p7_print_kit_frame_two_scrolls_one_shaft_dial_keeper_end_lock_six_rod_retainers")


def stop_pin_center(params: P7Parameters = P7_DEFAULTS) -> PointYZ:
    theta = radians(params.end_angle)
    radial = (params.stop_tab_radial_min + params.stop_tab_radial_max) / 2.0
    tangent = params.stop_tab_tangent_width / 2.0 + params.stop_pin_diameter / 2.0
    return PointYZ(
        params.shaft_y + cos(theta) * radial - sin(theta) * tangent,
        params.shaft_z + sin(theta) * radial + cos(theta) * tangent,
    )


__all__ = [
    "P7_DEFAULTS", "P7Parameters", "build_cap", "build_caps", "build_exploded",
    "build_end_lock_pin", "build_fixed_frame", "build_loaded", "build_loaded_closed", "build_loaded_mid",
    "build_loaded_open", "build_print_kit", "build_rod", "build_rods",
    "build_scroll_plate", "build_shaft_and_dial", "build_shaft_keeper", "build_stop_pins",
    "end_lock_point", "inverse_slot_point", "rod_center", "slot_path", "smoothstep01", "stop_pin_center",
    "travel_at_angle",
]
