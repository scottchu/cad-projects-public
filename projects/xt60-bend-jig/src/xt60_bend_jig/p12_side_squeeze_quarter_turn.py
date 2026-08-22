"""P12 compact side-cheek, single-cam XT60 forming-jig prototype.

P12 intentionally leaves P11 untouched.  It reuses P11's accepted workpiece
envelope and three role-specific rod motion laws, but replaces the four full
discs and bottom base with two fixed skeleton cheeks, one right-side skeleton
cam and one rear/top spine with a narrow clamp tongue.
"""

from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from functools import lru_cache
from math import cos, radians, sin

from build123d import Align, Box, Compound, Cylinder, Pos, Rot, Shape, Vector

from . import p11_asymmetric_three_rod_solder_jig as p11


RodName = p11.RodName
PointYZ = p11.PointYZ
ROD_NAMES = p11.ROD_NAMES


@dataclass(frozen=True, slots=True)
class P12Parameters:
    motion: p11.P11Parameters = p11.P11_DEFAULTS
    clear_span: float = 26.0
    cheek_thickness: float = 4.0
    cam_thickness: float = 3.0
    cam_gap: float = 0.30
    cheek_web: float = 3.0
    cam_web: float = 3.0
    connector_web: float = 6.0
    hub_outer: float = 22.0
    fixed_bore: float = 6.30
    cam_socket: float = 6.15
    spine_y: float = -6.15
    spine_z: float = 50.0
    spine_depth_y: float = 4.0
    spine_height_z: float = 8.0
    spine_tongue_length: float = 3.0
    spine_tongue_y: float = 3.8
    spine_tongue_z: float = 5.2
    spine_fit_clearance: float = 0.20
    clamp_tongue_width_x: float = 18.0
    clamp_tongue_length_y: float = 24.0
    clamp_tongue_thickness_z: float = 4.0
    lever_width: float = 8.0
    lever_end_y: float = -25.0
    lever_end_z: float = 17.0
    detent_radius: float = 8.0
    detent_nose_diameter: float = 2.0
    detent_pocket_diameter: float = 2.4
    stop_pin_diameter: float = 2.0
    stop_lane_width: float = 2.2
    rod_cap_outer: float = 7.0
    rod_cap_socket: float = 3.90
    rod_cap_thickness: float = 3.7
    rod_keeper_outer: float = 7.0
    rod_keeper_bore: float = 4.10
    rod_keeper_thickness: float = 2.9
    shaft_keeper_outer: float = 9.0
    shaft_keeper_bore: float = 5.40
    shaft_keeper_thickness: float = 1.8

    def __post_init__(self) -> None:
        if (self.motion.rod_diameter, self.motion.rod_length) != (4.0, 50.0):
            raise ValueError("P12 requires exactly three purchased 4 x 50 mm rods")
        if self.principal_width_x >= self.motion.rod_length:
            raise ValueError("P12 frame and cam must remain inside the 50 mm rod ends")
        if self.spine_fit_clearance <= 0.0:
            raise ValueError("spine tongue fit requires positive printable clearance")

    @property
    def shaft_center(self) -> PointYZ:
        return self.motion.shaft_center

    @property
    def left_cheek_x(self) -> float:
        return -(self.clear_span + self.cheek_thickness) / 2.0

    @property
    def right_cheek_x(self) -> float:
        return -self.left_cheek_x

    @property
    def cam_x(self) -> float:
        return (
            self.clear_span / 2.0
            + self.cheek_thickness
            + self.cam_gap
            + self.cam_thickness / 2.0
        )

    @property
    def left_outer_x(self) -> float:
        return self.left_cheek_x - self.cheek_thickness / 2.0

    @property
    def right_outer_x(self) -> float:
        return self.right_cheek_x + self.cheek_thickness / 2.0

    @property
    def cam_inner_x(self) -> float:
        return self.cam_x - self.cam_thickness / 2.0

    @property
    def cam_outer_x(self) -> float:
        return self.cam_x + self.cam_thickness / 2.0

    @property
    def principal_width_x(self) -> float:
        return self.cam_outer_x - self.left_outer_x


P12_DEFAULTS = P12Parameters()


def _label(shape: Shape, name: str, color: str) -> Shape:
    return p11._label(shape, name, color)


def _box(center: tuple[float, float, float], size: tuple[float, float, float]) -> Shape:
    return Pos(*center) * Box(*size, align=(Align.CENTER, Align.CENTER, Align.CENTER))


def _mid(first: PointYZ, second: PointYZ) -> PointYZ:
    return PointYZ((first.y + second.y) / 2.0, (first.z + second.z) / 2.0)


def _detent_nose_world(params: P12Parameters) -> PointYZ:
    return PointYZ(params.motion.shaft_y, params.motion.shaft_z - params.detent_radius)


def _detent_pocket_local(angle_deg: float, params: P12Parameters) -> PointYZ:
    point = _detent_nose_world(params)
    dy = point.y - params.motion.shaft_y
    dz = point.z - params.motion.shaft_z
    angle = radians(angle_deg)
    return PointYZ(
        params.motion.shaft_y + cos(angle) * dy + sin(angle) * dz,
        params.motion.shaft_z - sin(angle) * dy + cos(angle) * dz,
    )


def _spine_pocket_center(side: str, params: P12Parameters) -> tuple[float, float, float]:
    sign = -1.0 if side == "left" else 1.0
    inner_face = sign * params.clear_span / 2.0
    return (
        inner_face + sign * params.spine_tongue_length / 2.0,
        params.spine_y,
        params.spine_z,
    )


def _guide_outer_width(side: str, params: P12Parameters) -> float:
    guide = (
        params.motion.datum_guide_width
        if side == "left"
        else params.motion.follower_guide_width
    )
    return guide + 2.0 * params.cheek_web


@lru_cache(maxsize=8)
def _cheek_prototype(side: str, params: P12Parameters) -> Shape:
    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    x = params.left_cheek_x if side == "left" else params.right_cheek_x
    depth = params.cheek_thickness
    shaft = params.shaft_center
    guide_width = (
        params.motion.datum_guide_width
        if side == "left"
        else params.motion.follower_guide_width
    )

    rails: list[Shape] = []
    connectors: list[Shape] = []
    guide_tools: list[Shape] = []
    for name in ROD_NAMES:
        opened = p11.rod_center(name, 0.0, params.motion)
        closed = p11.rod_center(name, params.motion.end_angle, params.motion)
        rails.append(
            p11._straight_slot_x(
                opened, closed, _guide_outer_width(side, params), x, depth
            )
        )
        connectors.append(
            p11._straight_slot_x(
                shaft, _mid(opened, closed), params.connector_web, x, depth
            )
        )
        guide_tools.append(
            p11._straight_slot_x(opened, closed, guide_width, x, depth + 2.0)
        )

    anchor = _box((x, params.spine_y, params.spine_z), (depth, 11.0, 11.0))
    anchor_connector = p11._straight_slot_x(
        shaft,
        PointYZ(params.spine_y, params.spine_z),
        params.connector_web,
        x,
        depth,
    )
    hub = p11._x_cylinder(
        params.hub_outer, depth, x, params.motion.shaft_y, params.motion.shaft_z
    )
    raw = p11._fuse([hub, anchor, anchor_connector, *rails, *connectors])

    pocket_x, pocket_y, pocket_z = _spine_pocket_center(side, params)
    pocket = _box(
        (pocket_x, pocket_y, pocket_z),
        (
            params.spine_tongue_length + params.spine_fit_clearance,
            params.spine_tongue_y + params.spine_fit_clearance,
            params.spine_tongue_z + params.spine_fit_clearance,
        ),
    )
    bore = p11._x_cylinder(
        params.fixed_bore,
        depth + 2.0,
        x,
        params.motion.shaft_y,
        params.motion.shaft_z,
    )
    cheek = raw - [*guide_tools, bore, pocket]

    if side == "right":
        interaction_x = (params.right_outer_x + params.cam_inner_x) / 2.0
        interaction_depth = params.cam_gap + 0.55
        nose = _detent_nose_world(params)
        stop = p11.stop_pin_world(params.motion)
        detent = p11._x_cylinder(
            params.detent_nose_diameter,
            interaction_depth,
            interaction_x,
            nose.y,
            nose.z,
        )
        stop_pin = p11._x_cylinder(
            params.stop_pin_diameter,
            interaction_depth,
            interaction_x,
            stop.y,
            stop.z,
        )
        cheek = cheek + detent + stop_pin

    role = "datum_4p4" if side == "left" else "follower_4p9_detent_stop"
    return _label(cheek, f"{side}_skeleton_cheek_{role}", "#2F7653")


def build_cheek(side: str, params: P12Parameters = P12_DEFAULTS) -> Shape:
    return copy(_cheek_prototype(side, params))


@lru_cache(maxsize=8)
def _cam_prototype(params: P12Parameters) -> Shape:
    x = params.cam_x
    depth = params.cam_thickness
    shaft = params.shaft_center
    parts: list[Shape] = [
        p11._x_cylinder(
            params.hub_outer,
            depth,
            x,
            params.motion.shaft_y,
            params.motion.shaft_z,
        )
    ]
    tools: list[Shape] = []

    for name in ROD_NAMES:
        path = p11.inverse_slot_path(name, params.motion, step=0.5)
        parts.append(
            p11._slot_solid_x(
                path,
                params.motion.follower_cam_lane + 2.0 * params.cam_web,
                x,
                depth,
            )
        )
        parts.append(
            p11._straight_slot_x(
                shaft,
                path[len(path) // 2],
                params.connector_web,
                x,
                depth,
            )
        )
        # Use the accepted datum-side taper and 4.4 mm locked pocket on the
        # one driving cam; the opposite cheek remains a relieved follower.
        tools.extend(p11._cam_slot_tools(name, "left", x, depth, params.motion))

    stop_path = p11.stop_channel_path(params.motion)
    parts.append(
        p11._slot_solid_x(
            stop_path,
            params.stop_lane_width + 2.0 * params.cam_web,
            x,
            depth,
        )
    )
    parts.append(
        p11._straight_slot_x(
            shaft,
            stop_path[len(stop_path) // 2],
            params.connector_web,
            x,
            depth,
        )
    )

    lever_end = PointYZ(params.lever_end_y, params.lever_end_z)
    parts.append(
        p11._straight_slot_x(
            shaft, lever_end, params.lever_width, x, depth
        )
    )
    parts.append(
        p11._x_cylinder(
            params.lever_width + 2.0,
            depth,
            x,
            lever_end.y,
            lever_end.z,
        )
    )

    tools.append(
        p11._x_hex(
            params.cam_socket,
            depth + 2.0,
            x,
            params.motion.shaft_y,
            params.motion.shaft_z,
        )
    )
    tools.append(
        p11._slot_solid_x(
            stop_path, params.stop_lane_width, x, depth + 2.0
        )
    )
    for angle in (0.0, params.motion.end_angle):
        pocket = _detent_pocket_local(angle, params)
        tools.append(
            p11._x_cylinder(
                params.detent_pocket_diameter,
                depth + 2.0,
                x,
                pocket.y,
                pocket.z,
            )
        )

    cam = p11._fuse(parts) - tools
    return _label(
        cam,
        "right_skeleton_cam_three_role_slots_35deg_lever",
        "#D49B18",
    )


def build_cam(params: P12Parameters = P12_DEFAULTS) -> Shape:
    return copy(_cam_prototype(params))


def build_spine(params: P12Parameters = P12_DEFAULTS) -> Shape:
    main = _box(
        (0.0, params.spine_y, params.spine_z),
        (params.clear_span, params.spine_depth_y, params.spine_height_z),
    )
    tongues: list[Shape] = []
    for side in ("left", "right"):
        x, y, z = _spine_pocket_center(side, params)
        tongues.append(
            _box(
                (x, y, z),
                (
                    params.spine_tongue_length,
                    params.spine_tongue_y,
                    params.spine_tongue_z,
                ),
            )
        )
    rear_face = params.spine_y - params.spine_depth_y / 2.0
    clamp = _box(
        (
            0.0,
            rear_face - params.clamp_tongue_length_y / 2.0,
            params.spine_z - params.spine_height_z / 2.0
            + params.clamp_tongue_thickness_z / 2.0,
        ),
        (
            params.clamp_tongue_width_x,
            params.clamp_tongue_length_y,
            params.clamp_tongue_thickness_z,
        ),
    )
    return _label(
        p11._fuse([main, *tongues, clamp]),
        "rear_top_spine_xt60_backstop_and_narrow_clamp_tongue_no_bottom_plate",
        "#405D4A",
    )


def build_shaft(params: P12Parameters = P12_DEFAULTS) -> Shape:
    key_start = params.left_outer_x
    key_end = params.cam_outer_x
    key_length = key_end - key_start
    key_center = (key_start + key_end) / 2.0
    key = p11._x_hex(
        6.0,
        key_length,
        key_center,
        params.motion.shaft_y,
        params.motion.shaft_z,
    )
    head = p11._x_cylinder(
        10.0,
        2.0,
        key_start - 1.0,
        params.motion.shaft_y,
        params.motion.shaft_z,
    )
    neck = p11._x_cylinder(
        5.2,
        3.0,
        key_end + 1.5,
        params.motion.shaft_y,
        params.motion.shaft_z,
    )
    return _label(key + head + neck, "left_inserted_keyed_shaft_right_keeper_neck", "#172A35")


def _circular_c_clip(
    point: PointYZ,
    x: float,
    bore: float,
    outer: float,
    thickness: float,
    label: str,
    color: str,
) -> Shape:
    ring = p11._x_cylinder(outer, thickness, x, point.y, point.z)
    hole = p11._x_cylinder(bore, thickness + 2.0, x, point.y, point.z)
    throat_length = outer / 2.0 + 1.0
    throat = _box(
        (x, point.y + throat_length / 2.0, point.z),
        (thickness + 2.0, throat_length, bore),
    )
    return _label(ring - [hole, throat], label, color)


def build_shaft_keeper(params: P12Parameters = P12_DEFAULTS) -> Shape:
    point = params.shaft_center
    x = params.cam_outer_x + 2.2
    return _circular_c_clip(
        point,
        x,
        params.shaft_keeper_bore,
        params.shaft_keeper_outer,
        params.shaft_keeper_thickness,
        "right_circular_shaft_C_keeper_5p40",
        "#7799A2",
    )


def build_left_rod_cap(point: PointYZ, params: P12Parameters = P12_DEFAULTS) -> Shape:
    inner = params.left_outer_x - 0.2
    center_x = inner - params.rod_cap_thickness / 2.0
    body = p11._x_cylinder(
        params.rod_cap_outer,
        params.rod_cap_thickness,
        center_x,
        point.y,
        point.z,
    )
    socket = p11._x_cylinder(
        params.rod_cap_socket,
        3.0,
        inner - 1.5,
        point.y,
        point.z,
    )
    return _label(body - socket, "left_round_rod_cap_3p90", "#C88714")


def build_right_rod_keeper(point: PointYZ, params: P12Parameters = P12_DEFAULTS) -> Shape:
    return _circular_c_clip(
        point,
        params.cam_outer_x + params.rod_keeper_thickness / 2.0,
        params.rod_keeper_bore,
        params.rod_keeper_outer,
        params.rod_keeper_thickness,
        "right_round_rod_C_keeper_4p10",
        "#E0AE35",
    )


def build_retainers(angle_deg: float, params: P12Parameters = P12_DEFAULTS) -> Compound:
    parts: list[Shape] = []
    for name in ROD_NAMES:
        point = p11.rod_center(name, angle_deg, params.motion)
        parts.extend((build_left_rod_cap(point, params), build_right_rod_keeper(point, params)))
    return Compound(children=parts, label="three_round_caps_and_three_round_C_keepers")


def build_frame(angle_deg: float, params: P12Parameters = P12_DEFAULTS) -> Compound:
    cam = p11._rotate_about_shaft(build_cam(params), angle_deg, params.motion)
    shaft = p11._rotate_about_shaft(build_shaft(params), angle_deg, params.motion)
    return Compound(
        children=[
            build_spine(params),
            build_cheek("left", params),
            build_cheek("right", params),
            cam,
            shaft,
            build_shaft_keeper(params),
        ],
        label="p12_two_cheeks_one_skeleton_cam_one_rear_spine_no_bottom_plate",
    )


def _assembly_children(angle_deg: float, params: P12Parameters) -> list[Shape]:
    return [
        *build_frame(angle_deg, params).children,
        *p11.build_rods(angle_deg, params.motion).children,
        *build_retainers(angle_deg, params).children,
        *p11.build_workpiece(params.motion).children,
        *p11.build_electronics_reference(params.motion).children,
    ]


def build_loaded_open(params: P12Parameters = P12_DEFAULTS) -> Compound:
    return Compound(children=_assembly_children(0.0, params), label="p12_OPEN_side_squeeze_jig")


def build_loaded_closed(params: P12Parameters = P12_DEFAULTS) -> Compound:
    return Compound(
        children=_assembly_children(params.motion.end_angle, params),
        label="p12_LOCK_side_squeeze_quarter_turn_jig",
    )


def build_solder_access(params: P12Parameters = P12_DEFAULTS) -> Compound:
    return Compound(
        children=[
            *_assembly_children(params.motion.end_angle, params),
            *p11.build_solder_tool_sweeps(params.motion).children,
        ],
        label="p12_LOCK_open_front_two_solder_tool_approaches",
    )


def build_exploded(params: P12Parameters = P12_DEFAULTS) -> Compound:
    angle = params.motion.end_angle
    parts: list[Shape] = [
        Pos(-12.0, 0.0, 0.0) * build_cheek("left", params),
        Pos(12.0, 0.0, 0.0) * build_cheek("right", params),
        Pos(22.0, 0.0, 0.0)
        * p11._rotate_about_shaft(build_cam(params), angle, params.motion),
        Pos(0.0, -18.0, 8.0) * build_spine(params),
        Pos(0.0, 0.0, 14.0)
        * p11._rotate_about_shaft(build_shaft(params), angle, params.motion),
        Pos(8.0, 0.0, 14.0) * build_shaft_keeper(params),
    ]
    for index, name in enumerate(ROD_NAMES):
        point = p11.rod_center(name, angle, params.motion)
        parts.extend(
            (
                Pos(0.0, 0.0, 18.0 + index * 5.0)
                * p11.build_rod(name, angle, params.motion),
                Pos(-10.0, 0.0, 18.0 + index * 5.0)
                * build_left_rod_cap(point, params),
                Pos(10.0, 0.0, 18.0 + index * 5.0)
                * build_right_rod_keeper(point, params),
            )
        )
    return Compound(children=parts, label="p12_exploded_compact_side_squeeze_parts")


def _on_bed(shape: Shape, x: float, y: float, y_rotation: float = -90.0) -> Shape:
    placed = Rot(0.0, y_rotation, 0.0) * copy(shape)
    box = placed.bounding_box()
    return Pos(
        x - (box.min.X + box.max.X) / 2.0,
        y - (box.min.Y + box.max.Y) / 2.0,
        -box.min.Z,
    ) * placed


def build_print_kit(params: P12Parameters = P12_DEFAULTS) -> Compound:
    closed = p11.rod_center("upright", params.motion.end_angle, params.motion)
    parts: list[Shape] = [
        _on_bed(build_cheek("left", params), -42.0, -32.0),
        _on_bed(build_cheek("right", params), 0.0, -32.0),
        _on_bed(build_cam(params), 43.0, -30.0),
        _on_bed(build_spine(params), -28.0, 42.0, 0.0),
        _on_bed(build_shaft(params), 32.0, 53.0, 0.0),
        _on_bed(build_shaft_keeper(params), 70.0, 35.0),
    ]
    for index in range(3):
        parts.append(_on_bed(build_left_rod_cap(closed, params), 66.0, -15.0 + index * 14.0))
        parts.append(_on_bed(build_right_rod_keeper(closed, params), -70.0, -15.0 + index * 14.0))
    return Compound(children=parts, label="p12_print_kit_no_bottom_plate_support_free_layout")


def printed_core_parts(angle_deg: float, params: P12Parameters = P12_DEFAULTS) -> tuple[Shape, ...]:
    """Printed structural parts only, excluding retainers and purchased rods."""

    return tuple(build_frame(angle_deg, params).children[:4])


def stop_signed_clearance(angle_deg: float, params: P12Parameters = P12_DEFAULTS) -> float:
    """Radial path clearance for the fixed Ø2 pin in the 2.2 mm channel."""

    fixed = p11.stop_pin_world(params.motion)
    dy = fixed.y - params.motion.shaft_y
    dz = fixed.z - params.motion.shaft_z
    a = radians(angle_deg)
    local = PointYZ(
        params.motion.shaft_y + cos(a) * dy + sin(a) * dz,
        params.motion.shaft_z - sin(a) * dy + cos(a) * dz,
    )
    path = p11.stop_channel_path(params.motion)
    distance = min(local.distance_to(point) for point in path)
    return (params.stop_lane_width - params.stop_pin_diameter) / 2.0 - distance

