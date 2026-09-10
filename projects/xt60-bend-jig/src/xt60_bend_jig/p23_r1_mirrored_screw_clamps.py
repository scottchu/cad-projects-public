"""P23 R1 mirrored side screw-clamp intent preview.

This is evidence-only CAD.  It preserves P20 R4's four plates, stepped axle,
keepers, exact rod paths, XT60 reference and 90-degree workpiece, but replaces
the six rod-end caps with two X-mirrored side modules.  Each module has a fixed
Green reaction socket, a guided Blue follower pocket, a guided Orange shoe and
one equal-pitch printed screw/knob context.

Coordinates: X is the purchased-rod axis; FRONT is YZ; +Z is the XT60 mating
head/up direction and +Y is the wire-tail/outward direction.
"""

from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from math import atan2, degrees, hypot
from typing import Literal

from build123d import Align, Box, Compound, Cylinder, Pos, Rot, Shape
from cadgen import srgb

from . import p20_r4_custom_profile_full_cad as p20


Side = Literal["left", "right"]
State = Literal["open", "clamped"]
PointYZ = p20.PointYZ

ROD_ROLE_TO_P20_NAME = {
    "blue": "bottom",
    "orange": "diagonal",
    "green": "upright",
}


@dataclass(frozen=True, slots=True)
class P23R1Parameters:
    """Named dimensions selected by the P23-DESIGN-01 contract."""

    rod_diameter: float = 4.00
    rod_length: float = 50.00
    yoke_inner_face_abs_x: float = 21.30
    yoke_thickness_x: float = 6.00
    outer_plate_running_gap: float = 0.30
    socket_id: float = 4.15
    socket_depth: float = 4.00
    socket_end_clearance: float = 0.30
    socket_outer_wall: float = 2.00
    green_capture_od: float = 9.00
    blue_follower_od: float = 8.15
    orange_shoe_length: float = 9.00
    orange_shoe_width: float = 6.00
    guide_sliding_clearance_each: float = 0.20
    guide_wall: float = 2.00
    yoke_wall: float = 2.40
    screw_major_diameter: float = 10.00
    screw_minor_diameter: float = 8.00
    screw_pitch: float = 2.00
    screw_nut_engagement: float = 10.00
    screw_usable_translation: float = 13.00
    screw_shaft_length: float = 31.00
    knob_diameter: float = 18.00
    knob_thickness: float = 6.00
    nut_block_size: float = 14.00
    nut_offset_behind_open: float = 15.00
    screw_axis_offset_from_orange: float = 8.00
    knob_nut_clearance: float = 1.00
    retention_lip_thickness_x: float = 1.20
    retention_flange_thickness_x: float = 3.20
    retention_tab_width: float = 3.00
    retention_tab_offset: float = 5.00
    retention_clearance_each: float = 0.20
    captive_head_diameter: float = 6.00
    captive_head_thickness: float = 2.00
    captive_neck_diameter: float = 3.00
    captive_neck_length: float = 3.00
    captive_radial_clearance: float = 0.25
    captive_axial_clearance: float = 0.25
    captive_housing_diameter: float = 10.00
    captive_housing_length: float = 6.00

    @property
    def yoke_outer_face_abs_x(self) -> float:
        return self.yoke_inner_face_abs_x + self.yoke_thickness_x

    @property
    def yoke_center_abs_x(self) -> float:
        return (self.yoke_inner_face_abs_x + self.yoke_outer_face_abs_x) / 2.0

    @property
    def blue_guide_inner_width(self) -> float:
        return self.blue_follower_od + 2.0 * self.guide_sliding_clearance_each

    @property
    def orange_guide_inner_width(self) -> float:
        return self.orange_shoe_width + 2.0 * self.guide_sliding_clearance_each

    @property
    def retention_cavity_thickness_x(self) -> float:
        return self.yoke_thickness_x - 2.0 * self.retention_lip_thickness_x

    @property
    def captive_head_cavity_diameter(self) -> float:
        return self.captive_head_diameter + 2.0 * self.captive_radial_clearance

    @property
    def captive_head_cavity_length(self) -> float:
        return self.captive_head_thickness + 2.0 * self.captive_axial_clearance

    @property
    def captive_neck_slot_diameter(self) -> float:
        return self.captive_neck_diameter + 2.0 * self.captive_radial_clearance


P23_R1_DEFAULTS = P23R1Parameters()
STATE_PROGRESS: dict[State, float] = {"open": 0.0, "clamped": 1.0}


def _check_side(side: Side) -> Side:
    if side not in ("left", "right"):
        raise ValueError(f"unknown side {side!r}")
    return side


def _check_progress(progress: float) -> float:
    if not 0.0 <= progress <= 1.0:
        raise ValueError("P23 progress must stay in 0..1")
    return float(progress)


def inherited_rod_center(role: Literal["blue", "orange", "green"], progress: float) -> PointYZ:
    """Delegate every rod center to the unchanged P20 R4 path authority."""

    progress = _check_progress(progress)
    try:
        name = ROD_ROLE_TO_P20_NAME[role]
    except KeyError as exc:
        raise ValueError(f"unknown rod role {role!r}") from exc
    return p20.world_rod_center(name, progress)  # type: ignore[arg-type]


def orange_travel_vector() -> PointYZ:
    """Exact OPEN-to-CLAMPED Orange translation vector in FRONT YZ."""

    start = inherited_rod_center("orange", 0.0)
    end = inherited_rod_center("orange", 1.0)
    return PointYZ(end.y - start.y, end.z - start.z)


def orange_travel_distance() -> float:
    vector = orange_travel_vector()
    return hypot(vector.y, vector.z)


def orange_travel_unit() -> PointYZ:
    distance = orange_travel_distance()
    vector = orange_travel_vector()
    return PointYZ(vector.y / distance, vector.z / distance)


def orange_shoe_center(progress: float) -> PointYZ:
    """Pure-math translating-shoe center; identical on both X sides."""

    progress = _check_progress(progress)
    start = inherited_rod_center("orange", 0.0)
    unit = orange_travel_unit()
    travel = orange_travel_distance() * progress
    return PointYZ(start.y + unit.y * travel, start.z + unit.z * travel)


def screw_turns(progress: float, params: P23R1Parameters = P23_R1_DEFAULTS) -> float:
    return orange_travel_distance() * _check_progress(progress) / params.screw_pitch


def side_yoke_center_x(side: Side, params: P23R1Parameters = P23_R1_DEFAULTS) -> float:
    """X-mirrored placement datum for the two side yokes."""

    return (-1.0 if _check_side(side) == "left" else 1.0) * params.yoke_center_abs_x


def side_inner_face_x(side: Side, params: P23R1Parameters = P23_R1_DEFAULTS) -> float:
    return (-1.0 if _check_side(side) == "left" else 1.0) * params.yoke_inner_face_abs_x


def blind_socket_center_x(side: Side, params: P23R1Parameters = P23_R1_DEFAULTS) -> float:
    """Center of a depth-controlled socket opened toward the mechanism."""

    inward_depth_sign = -1.0 if _check_side(side) == "left" else 1.0
    return side_inner_face_x(side, params) + inward_depth_sign * params.socket_depth / 2.0


def blind_socket_end_x(side: Side, params: P23R1Parameters = P23_R1_DEFAULTS) -> float:
    """Blind bottom plane; each rod end stops 0.30 mm before this plane."""

    inward_depth_sign = -1.0 if _check_side(side) == "left" else 1.0
    return side_inner_face_x(side, params) + inward_depth_sign * params.socket_depth


def capture_manifest(side: Side) -> tuple[str, str, str]:
    side = _check_side(side)
    return (
        f"{side}_green_fixed_capture",
        f"{side}_blue_follower_capture",
        f"{side}_orange_shoe_capture",
    )


def _colored(shape: Shape, label: str, color: str, alpha: float | None = None) -> Shape:
    shape.label = label
    shape.color = srgb(color) if alpha is None else srgb(color, alpha)
    return shape


def _x_cylinder(diameter: float, length: float, x: float, point: PointYZ) -> Shape:
    return Pos(x, point.y, point.z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _capsule_yz(start: PointYZ, end: PointYZ, width: float, center_x: float, thickness_x: float) -> Shape:
    """One constant-width obround extruded along X."""

    dy, dz = end.y - start.y, end.z - start.z
    length = hypot(dy, dz)
    angle = degrees(atan2(dz, dy))
    middle = PointYZ((start.y + end.y) / 2.0, (start.z + end.z) / 2.0)
    spine = Pos(center_x, middle.y, middle.z) * Rot(angle, 0.0, 0.0) * Box(
        thickness_x,
        length,
        width,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return (
        spine
        + _x_cylinder(width, thickness_x, center_x, start)
        + _x_cylinder(width, thickness_x, center_x, end)
    )


def _unit(vector: PointYZ) -> PointYZ:
    length = hypot(vector.y, vector.z)
    if length <= 1.0e-12:
        raise ValueError("direction must be non-zero")
    return PointYZ(vector.y / length, vector.z / length)


def _oriented_box_yz(
    center: PointYZ,
    along_length: float,
    across_width: float,
    center_x: float,
    thickness_x: float,
    direction: PointYZ,
) -> Shape:
    angle = degrees(atan2(direction.z, direction.y))
    return Pos(center_x, center.y, center.z) * Rot(angle, 0.0, 0.0) * Box(
        thickness_x,
        along_length,
        across_width,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _path_box_yz(
    start: PointYZ,
    end: PointYZ,
    moving_length: float,
    moving_width: float,
    center_x: float,
    thickness_x: float,
) -> Shape:
    vector = PointYZ(end.y - start.y, end.z - start.z)
    center = PointYZ((start.y + end.y) / 2.0, (start.z + end.z) / 2.0)
    return _oriented_box_yz(
        center,
        hypot(vector.y, vector.z) + moving_length,
        moving_width,
        center_x,
        thickness_x,
        _unit(vector),
    )


def _axis_angle_deg(direction: PointYZ) -> float:
    """Rotation about X taking local +Z onto one FRONT-YZ direction."""

    return degrees(atan2(-direction.y, direction.z))


def _axis_cylinder(diameter: float, length: float, center: PointYZ, direction: PointYZ, x: float) -> Shape:
    return Pos(x, center.y, center.z) * Rot(_axis_angle_deg(direction), 0.0, 0.0) * Cylinder(
        diameter / 2.0,
        length,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _axis_segment_cylinder(diameter: float, start: PointYZ, end: PointYZ, x: float) -> Shape:
    vector = PointYZ(end.y - start.y, end.z - start.z)
    center = PointYZ((start.y + end.y) / 2.0, (start.z + end.z) / 2.0)
    return _axis_cylinder(diameter, hypot(vector.y, vector.z), center, _unit(vector), x)


def _offset(point: PointYZ, direction: PointYZ, distance: float) -> PointYZ:
    return PointYZ(point.y + direction.y * distance, point.z + direction.z * distance)


def _left_perpendicular(direction: PointYZ) -> PointYZ:
    return PointYZ(-direction.z, direction.y)


def blue_retention_unit() -> PointYZ:
    blue = inherited_rod_center("blue", 1.0)
    orange = inherited_rod_center("orange", 1.0)
    return _unit(PointYZ(blue.y - orange.y, blue.z - orange.z))


def orange_retention_unit() -> PointYZ:
    blue = blue_retention_unit()
    return PointYZ(-blue.y, -blue.z)


def screw_axis_x(side: Side, params: P23R1Parameters = P23_R1_DEFAULTS) -> float:
    """Keep the Ø10 shaft outside the fixed yoke's X face by 0.30 mm."""

    sign = -1.0 if _check_side(side) == "left" else 1.0
    return sign * (
        params.yoke_outer_face_abs_x
        + params.screw_major_diameter / 2.0
        + params.outer_plate_running_gap
    )


def screw_interface_center(progress: float, params: P23R1Parameters = P23_R1_DEFAULTS) -> PointYZ:
    return _offset(
        orange_shoe_center(progress),
        _left_perpendicular(orange_travel_unit()),
        params.screw_axis_offset_from_orange,
    )


def screw_nut_center(params: P23R1Parameters = P23_R1_DEFAULTS) -> PointYZ:
    return _offset(screw_interface_center(0.0, params), orange_travel_unit(), -params.nut_offset_behind_open)


def nut_block_axial_half_extent(params: P23R1Parameters = P23_R1_DEFAULTS) -> float:
    """Projection of the square nut block's YZ half-extents on the drive axis."""

    drive = orange_travel_unit()
    return params.nut_block_size / 2.0 * (abs(drive.y) + abs(drive.z))


def knob_center(progress: float, params: P23R1Parameters = P23_R1_DEFAULTS) -> PointYZ:
    remaining = orange_travel_distance() * (1.0 - _check_progress(progress))
    return _offset(
        screw_nut_center(params),
        orange_travel_unit(),
        -(
            remaining
            + nut_block_axial_half_extent(params)
            + params.knob_thickness / 2.0
            + params.knob_nut_clearance
        ),
    )


def knob_nut_clearance(progress: float, params: P23R1Parameters = P23_R1_DEFAULTS) -> float:
    knob = knob_center(progress, params)
    nut = screw_nut_center(params)
    return (
        hypot(knob.y - nut.y, knob.z - nut.z)
        - nut_block_axial_half_extent(params)
        - params.knob_thickness / 2.0
    )


def _blind_socket_body(
    side: Side,
    center: PointYZ,
    outer_diameter: float,
    params: P23R1Parameters,
) -> Shape:
    body = _x_cylinder(outer_diameter, params.yoke_thickness_x, side_yoke_center_x(side, params), center)
    bore = _x_cylinder(params.socket_id, params.socket_depth + 0.02, blind_socket_center_x(side, params), center)
    return body - bore


def build_fixed_yoke(side: Side, params: P23R1Parameters = P23_R1_DEFAULTS) -> Shape:
    """One connected yoke with keyed guides and X-retaining face lips."""

    side = _check_side(side)
    x = side_yoke_center_x(side, params)
    blue_open = inherited_rod_center("blue", 0.0)
    blue_end = inherited_rod_center("blue", 1.0)
    orange_open = inherited_rod_center("orange", 0.0)
    orange_end = inherited_rod_center("orange", 1.0)
    green = inherited_rod_center("green", 0.0)
    drive = orange_travel_unit()

    green_outer = _x_cylinder(params.green_capture_od, params.yoke_thickness_x, x, green)
    blue_outer = _capsule_yz(
        blue_open, blue_end, params.blue_guide_inner_width + 2.0 * params.guide_wall,
        x, params.yoke_thickness_x,
    )
    blue_inner = _capsule_yz(
        blue_open, blue_end, params.blue_guide_inner_width,
        x, params.yoke_thickness_x + 2.0,
    )
    orange_outer = _path_box_yz(
        orange_open, orange_end,
        params.orange_shoe_length + 2.0 * params.guide_wall,
        params.orange_shoe_width + 2.0 * params.guide_wall,
        x, params.yoke_thickness_x,
    )
    orange_inner = _path_box_yz(
        orange_open, orange_end,
        params.orange_shoe_length + 2.0 * params.guide_sliding_clearance_each,
        params.orange_shoe_width + 2.0 * params.guide_sliding_clearance_each,
        x, params.yoke_thickness_x + 2.0,
    )

    screw_open = screw_interface_center(0.0, params)
    nut_center = screw_nut_center(params)
    screw_x = screw_axis_x(side, params)
    nut_block = Pos(screw_x, nut_center.y, nut_center.z) * Box(
        params.nut_block_size, params.nut_block_size, params.nut_block_size,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    screw_clearance = _axis_cylinder(
        params.screw_major_diameter + 0.40,
        2.0 * params.nut_block_size,
        nut_center, drive, screw_x,
    )

    retention_width = 2.0 * (
        params.retention_tab_offset + params.retention_tab_width / 2.0
        + params.retention_clearance_each
    )
    blue_retention_cavity = _capsule_yz(
        blue_open, blue_end, retention_width, x, params.retention_cavity_thickness_x,
    )
    orange_retention_cavity = _path_box_yz(
        orange_open, orange_end,
        params.orange_shoe_length + 2.0 * params.guide_sliding_clearance_each,
        retention_width, x, params.retention_cavity_thickness_x,
    )

    blue_mid = PointYZ((blue_open.y + blue_end.y) / 2.0, (blue_open.z + blue_end.z) / 2.0)
    orange_mid = PointYZ((orange_open.y + orange_end.y) / 2.0, (orange_open.z + orange_end.z) / 2.0)
    strut_blue = _capsule_yz(green, blue_mid, params.yoke_wall, x, params.yoke_thickness_x)
    strut_orange = _capsule_yz(green, orange_mid, params.yoke_wall, x, params.yoke_thickness_x)

    rail_perp = _left_perpendicular(drive)
    rail_offset = params.captive_housing_diameter / 2.0 + params.yoke_wall / 2.0 + 0.30
    rail_a = _capsule_yz(
        _offset(nut_center, rail_perp, rail_offset),
        _offset(screw_open, rail_perp, rail_offset),
        params.yoke_wall, x, params.yoke_thickness_x,
    )
    rail_b = _capsule_yz(
        _offset(nut_center, rail_perp, -rail_offset),
        _offset(screw_open, rail_perp, -rail_offset),
        params.yoke_wall, x, params.yoke_thickness_x,
    )

    yoke = (
        green_outer + blue_outer + orange_outer + nut_block
        + strut_blue + strut_orange + rail_a + rail_b
    )
    green_bore = _x_cylinder(
        params.socket_id, params.socket_depth + 0.02,
        blind_socket_center_x(side, params), green,
    )
    yoke = (
        yoke - blue_inner - orange_inner
        - blue_retention_cavity - orange_retention_cavity
        - green_bore - screw_clearance
    )
    return _colored(
        yoke,
        f"{side}_fixed_side_yoke_green_fixed_capture_blind_ID4p15_connected_x_retention_face_lips",
        "#68727D",
    )


def build_blue_follower(side: Side, progress: float, params: P23R1Parameters = P23_R1_DEFAULTS) -> Shape:
    center = inherited_rod_center("blue", progress)
    follower = _blind_socket_body(side, center, params.blue_follower_od, params)
    tab_center = _offset(center, blue_retention_unit(), params.retention_tab_offset)
    tab = _capsule_yz(
        center, tab_center, params.retention_tab_width,
        side_yoke_center_x(side, params), params.retention_flange_thickness_x,
    )
    follower = follower + tab
    follower = follower - _x_cylinder(
        params.socket_id, params.socket_depth + 0.02,
        blind_socket_center_x(side, params), center,
    )
    return _colored(
        follower,
        f"{side}_blue_follower_capture_blind_ID4p15_x_retention_flange",
        "#379BF6",
    )


def build_orange_shoe(side: Side, progress: float, params: P23R1Parameters = P23_R1_DEFAULTS) -> Shape:
    center = orange_shoe_center(progress)
    drive = orange_travel_unit()
    shoe = _oriented_box_yz(
        center, params.orange_shoe_length, params.orange_shoe_width,
        side_yoke_center_x(side, params), params.yoke_thickness_x, drive,
    )
    tab_center = _offset(center, orange_retention_unit(), params.retention_tab_offset)
    tab = _capsule_yz(
        center, tab_center, params.retention_tab_width,
        side_yoke_center_x(side, params), params.retention_flange_thickness_x,
    )
    interface = screw_interface_center(progress, params)
    screw_x = screw_axis_x(side, params)
    sign = -1.0 if side == "left" else 1.0
    bridge_start_x = sign * (params.yoke_outer_face_abs_x - 1.0)
    bridge_length_x = abs(screw_x - bridge_start_x)
    bridge_center_x = (screw_x + bridge_start_x) / 2.0
    outboard_bridge = Pos(bridge_center_x, center.y, center.z) * Box(
        bridge_length_x, params.yoke_wall, params.yoke_wall,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    thrust_arm = _capsule_yz(
        center, interface, params.yoke_wall, screw_x, params.yoke_wall,
    )
    captive_housing = _axis_cylinder(
        params.captive_housing_diameter, params.captive_housing_length,
        interface, drive, screw_x,
    )
    shoe = shoe + tab + outboard_bridge + thrust_arm + captive_housing
    shoe = shoe - _x_cylinder(
        params.socket_id, params.socket_depth + 0.02,
        blind_socket_center_x(side, params), center,
    )
    # Preserve the inherited non-Orange rod paths, including the tiny corner
    # clearance that a rectangular anti-rotation profile otherwise loses.
    for role in ("blue", "green"):
        shoe = shoe - _x_cylinder(
            params.rod_diameter + 2.0 * params.guide_sliding_clearance_each,
            params.yoke_thickness_x + 2.0,
            side_yoke_center_x(side, params),
            inherited_rod_center(role, progress),
        )
    head_cavity = _axis_cylinder(
        params.captive_head_cavity_diameter, params.captive_head_cavity_length,
        interface, drive, screw_x,
    )
    slot_start = _offset(
        interface, drive,
        -(params.captive_housing_length / 2.0 + params.captive_neck_length),
    )
    neck_slot = _axis_segment_cylinder(
        params.captive_neck_slot_diameter, slot_start, interface, screw_x,
    )
    shoe = shoe - head_cavity - neck_slot
    # Final fitted-interface trim removes only any rail/housing fringe left by
    # fused construction; the guide and bridge already carry declared 0.20 mm
    # running clearance.
    shoe = shoe - build_fixed_yoke(side, params)
    return _colored(
        shoe,
        f"{side}_orange_shoe_capture_blind_ID4p15_anti_rotation_keyed_x_retention_flange_captive_T_head_pocket",
        "#F18742",
    )


def build_screw_with_knob(
    side: Side,
    progress: float,
    params: P23R1Parameters = P23_R1_DEFAULTS,
) -> Shape:
    """One fused printed screw/knob context with a captive T-head nose."""

    progress = _check_progress(progress)
    x = screw_axis_x(side, params)
    drive = orange_travel_unit()
    head_center = screw_interface_center(progress, params)
    rear_knob_center = knob_center(progress, params)
    shaft_front = _offset(
        head_center, drive,
        -(params.captive_head_thickness / 2.0 + params.captive_neck_length - 0.40),
    )
    shaft_rear = _offset(
        rear_knob_center, drive, params.knob_thickness / 2.0 - 0.50,
    )
    neck_center = _offset(
        head_center, drive,
        -(params.captive_head_thickness / 2.0 + params.captive_neck_length / 2.0 - 0.20),
    )
    shaft = _axis_segment_cylinder(params.screw_major_diameter, shaft_rear, shaft_front, x)
    knob = _axis_cylinder(params.knob_diameter, params.knob_thickness, rear_knob_center, drive, x)
    neck = _axis_cylinder(params.captive_neck_diameter, params.captive_neck_length, neck_center, drive, x)
    head = _axis_cylinder(params.captive_head_diameter, params.captive_head_thickness, head_center, drive, x)
    screw = knob + shaft + neck + head
    return _colored(
        screw,
        f"{side}_printed_screw_with_knob_MAJOR_D10_P2_captive_T_head_turns_{screw_turns(progress, params):.5f}",
        "#D9DDE3",
    )


def module_parts(
    side: Side,
    progress: float,
    params: P23R1Parameters = P23_R1_DEFAULTS,
) -> tuple[Shape, Shape, Shape, Shape]:
    """Named module parts for topology and pairwise-collision inspection."""

    return (
        build_fixed_yoke(side, params),
        build_blue_follower(side, progress, params),
        build_orange_shoe(side, progress, params),
        build_screw_with_knob(side, progress, params),
    )


def build_side_module(
    side: Side,
    progress: float,
    params: P23R1Parameters = P23_R1_DEFAULTS,
) -> Compound:
    return Compound(
        children=list(module_parts(side, progress, params)),
        label=f"{side}_mirrored_screw_clamp_module",
    )


def _context_children(progress: float, p20_params: p20.P20R4Parameters) -> list[Shape]:
    children: list[Shape] = [
        p20.build_center_axle(p20_params),
        p20.build_keeper("left", p20_params),
        p20.build_keeper("right", p20_params),
        p20.build_inner_plate("left", p20_params),
        p20.build_inner_plate("right", p20_params),
        p20.build_outer_plate("left", progress, p20_params),
        p20.build_outer_plate("right", progress, p20_params),
        p20.build_xt60_reference(p20_params),
        p20.build_workpiece_reference(),
    ]
    children.extend(p20.build_rod(name, progress, p20_params) for name in p20.ROD_NAMES)
    return children


def build_preview(
    state: State,
    params: P23R1Parameters = P23_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> Compound:
    """Complete P23 OPEN or CLAMPED evidence-only assembly."""

    if state not in STATE_PROGRESS:
        raise ValueError(f"unknown state {state!r}")
    if p20_params.rod_length_target != params.rod_length or p20_params.rod_diameter != params.rod_diameter:
        raise ValueError("P23 must preserve the immutable P20 OD4 x 50 mm purchased rods")
    progress = STATE_PROGRESS[state]
    children = _context_children(progress, p20_params)
    children.extend(
        (build_side_module("left", progress, params), build_side_module("right", progress, params))
    )
    return Compound(
        children=children,
        label=f"P23_R1_{state.upper()}_MIRRORED_SCREW_CLAMPS_EVIDENCE_ONLY_NOT_PRINT_AUTHORITY",
    )


def iter_leaf_shapes(shape: Shape):
    """Yield labeled leaf occurrences for tests and compact evidence."""

    children = tuple(getattr(shape, "children", ()))
    if not children:
        yield shape
        return
    for child in children:
        yield from iter_leaf_shapes(child)


def occurrence_census(shape: Shape) -> dict[str, object]:
    labels = tuple(child.label for child in iter_leaf_shapes(shape))
    return {
        "labels": labels,
        "leafCount": len(labels),
        "rodCount": sum("_OD4_rod_L50.00" in label for label in labels),
        "capCount": sum("permanent_cap" in label for label in labels),
        "moduleCount": sum("printed_screw_with_knob" in label for label in labels),
        "captureCount": sum("capture_blind_ID4p15" in label for label in labels),
    }


__all__ = [
    "P23R1Parameters",
    "P23_R1_DEFAULTS",
    "ROD_ROLE_TO_P20_NAME",
    "STATE_PROGRESS",
    "blind_socket_center_x",
    "blind_socket_end_x",
    "build_blue_follower",
    "build_fixed_yoke",
    "build_orange_shoe",
    "build_preview",
    "build_screw_with_knob",
    "build_side_module",
    "capture_manifest",
    "inherited_rod_center",
    "iter_leaf_shapes",
    "knob_center",
    "knob_nut_clearance",
    "module_parts",
    "nut_block_axial_half_extent",
    "occurrence_census",
    "orange_shoe_center",
    "orange_travel_distance",
    "orange_travel_unit",
    "orange_travel_vector",
    "screw_turns",
    "screw_axis_x",
    "side_inner_face_x",
    "side_yoke_center_x",
]
