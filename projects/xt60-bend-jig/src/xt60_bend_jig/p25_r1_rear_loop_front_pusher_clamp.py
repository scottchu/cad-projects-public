"""P25 R1 rear-yoke/front-pusher first-review CAD.

P25 preserves P20 R4 and its three purchased OD4 x 50 mm rods. Two mirrored
removable end modules hold only the manually reached END state. Per side,
one rear yoke supports Blue+Green, one hinged bar carries the only Orange
pad, one OD2 hinge pin envelope joins them, and one isolated spring envelope
reserves opening-bias space. The spring is not functionally proven.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import atan2, cos, degrees, hypot, radians, sin
from typing import Literal

from build123d import Align, Box, Compound, Cylinder, Pos, Rot, Shape
from cadgen import srgb

from . import p20_r4_custom_profile_full_cad as p20

Side = Literal["left", "right"]
Role = Literal["blue", "orange", "green"]
State = Literal["PRECLAMP_END", "LATCHED_END", "RELEASED_CLEAR"]
PointYZ = p20.PointYZ

SIDES: tuple[Side, ...] = ("left", "right")
ROLES: tuple[Role, ...] = ("blue", "orange", "green")
STATES: tuple[State, ...] = ("PRECLAMP_END", "LATCHED_END", "RELEASED_CLEAR")
ROLE_TO_P20_NAME = {"blue": "bottom", "orange": "diagonal", "green": "upright"}


@dataclass(frozen=True, slots=True)
class P25R1Parameters:
    rod_od: float = 4.00
    rod_length: float = 50.00
    plate_to_module_gap: float = 0.30
    module_axial_thickness: float = 3.20
    rod_tip_margin: float = 0.50
    rear_saddle_diameter: float = 4.35
    rear_saddle_wrap_angle: float = 120.0
    orange_pad_diameter: float = 4.30
    orange_pad_wrap_angle: float = 70.0
    yoke_min_wall: float = 3.00
    front_bar_min_wall: float = 3.00
    hinge_pin_diameter: float = 2.00
    hinge_running_clearance: float = 0.25
    released_open_angle: float = 60.0
    released_orange_clearance: float = 3.00
    latch_hook_engagement: float = 1.20
    latch_clearance: float = 0.25
    latch_release_travel: float = 1.50
    release_tab_length: float = 7.00
    spring_envelope_od: float = 6.00
    spring_wire_envelope: float = 0.50
    orange_pad_offset: float = 0.00
    front_bar_vertical_offset: float = 8.00
    rear_bridge_vertical_offset: float = -7.00
    end_extension: float = 5.50
    layer_gap: float = 0.20
    yoke_layer_thickness: float = 1.20
    spring_layer_thickness: float = 0.40
    front_layer_thickness: float = 1.20
    saddle_outer_diameter: float = 10.35
    hinge_lug_od: float = 6.50
    latch_receiver_od: float = 2.50
    latch_hook_outer_diameter: float = 6.00

    @property
    def rod_end_abs_x(self) -> float:
        return self.rod_length / 2.0

    @property
    def hinge_hole_diameter(self) -> float:
        return self.hinge_pin_diameter + 2.0 * self.hinge_running_clearance

    @property
    def layer_sum(self) -> float:
        return self.yoke_layer_thickness + 2.0 * self.layer_gap + self.spring_layer_thickness + self.front_layer_thickness


P25_R1_DEFAULTS = P25R1Parameters()


@dataclass(frozen=True, slots=True)
class AxialLayout:
    inboard_abs_x: float
    yoke_center_x: float
    spring_center_x: float
    front_center_x: float
    outboard_abs_x: float
    rod_end_abs_x: float


@dataclass(frozen=True, slots=True)
class ClampFrameYZ:
    blue: PointYZ
    orange: PointYZ
    green: PointYZ
    tangent: PointYZ
    hinge: PointYZ
    latch: PointYZ


def _unit(value: float, name: str) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must stay in 0..1")
    return float(value)


def _side_sign(side: Side) -> float:
    if side == "left":
        return -1.0
    if side == "right":
        return 1.0
    raise ValueError(f"unknown side {side!r}")


def inherited_rod_center(role: Role, mechanism_progress: float) -> PointYZ:
    """Single P25 placement authority, delegated exactly to P20."""
    try:
        name = ROLE_TO_P20_NAME[role]
    except KeyError as exc:
        raise ValueError(f"unknown rod role {role!r}") from exc
    return p20.world_rod_center(name, _unit(mechanism_progress, "mechanism_progress"))  # type: ignore[arg-type]


def clamp_state_rod_center(role: Role, clamp_state: float) -> PointYZ:
    """Clamp motion is inert with respect to all rod centres."""
    _unit(clamp_state, "clamp_state")
    return inherited_rod_center(role, 1.0)


def _add(a: PointYZ, b: PointYZ) -> PointYZ:
    return PointYZ(a.y + b.y, a.z + b.z)


def _scale(a: PointYZ, k: float) -> PointYZ:
    return PointYZ(a.y * k, a.z * k)


def _rotate_point(point: PointYZ, pivot: PointYZ, angle_deg: float) -> PointYZ:
    a = radians(angle_deg)
    dy, dz = point.y - pivot.y, point.z - pivot.z
    return PointYZ(pivot.y + dy * cos(a) - dz * sin(a), pivot.z + dy * sin(a) + dz * cos(a))


def clamp_frame(params: P25R1Parameters = P25_R1_DEFAULTS) -> ClampFrameYZ:
    blue = inherited_rod_center("blue", 1.0)
    orange = inherited_rod_center("orange", 1.0)
    green = inherited_rod_center("green", 1.0)
    dy, dz = green.y - blue.y, green.z - blue.z
    span = hypot(dy, dz)
    tangent = PointYZ(dy / span, dz / span)
    lift = PointYZ(0.0, params.front_bar_vertical_offset)
    hinge = _add(_add(blue, _scale(tangent, -params.end_extension)), lift)
    latch = _add(_add(green, _scale(tangent, params.end_extension)), lift)
    return ClampFrameYZ(blue, orange, green, tangent, hinge, latch)


def latch_exit_direction(params: P25R1Parameters = P25_R1_DEFAULTS) -> PointYZ:
    """Receiver motion in the bar frame at the start of positive-X opening.

    The fixed receiver appears to move opposite the bar's angular motion.
    For hinge-to-latch vector ``(dy, dz)``, that unit tangent is
    ``(dz, -dy) / length``.  The quick-hook mouth follows this direction so
    the rigid receiver can leave immediately instead of crossing the hook.
    """
    frame = clamp_frame(params)
    dy, dz = frame.latch.y - frame.hinge.y, frame.latch.z - frame.hinge.z
    length = hypot(dy, dz)
    return PointYZ(dz / length, -dy / length)


def state_angle(state: State, params: P25R1Parameters = P25_R1_DEFAULTS) -> float:
    if state == "LATCHED_END":
        return 0.0
    if state in ("PRECLAMP_END", "RELEASED_CLEAR"):
        return params.released_open_angle
    raise ValueError(f"unknown P25 state {state!r}")


def axial_layout(side: Side, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> AxialLayout:
    sign = _side_sign(side)
    outer_face = p20_params.right_outer_x + p20_params.outer_plate_thickness / 2.0
    inboard = outer_face + params.plate_to_module_gap
    outboard = inboard + params.module_axial_thickness
    if abs(params.layer_sum - params.module_axial_thickness) > 1.0e-9:
        raise ValueError("layer stack must equal module_axial_thickness")
    yoke_mid = inboard + params.yoke_layer_thickness / 2.0
    spring_mid = inboard + params.yoke_layer_thickness + params.layer_gap + params.spring_layer_thickness / 2.0
    front_mid = outboard - params.front_layer_thickness / 2.0
    return AxialLayout(inboard, sign * yoke_mid, sign * spring_mid, sign * front_mid, outboard, params.rod_end_abs_x)


def _color(shape: Shape, label: str, color: str, alpha: float = 1.0) -> Shape:
    shape.label = label
    shape.color = srgb(color, alpha)
    return shape


def _x_cylinder(diameter: float, length: float, x: float, p: PointYZ) -> Shape:
    return Pos(x, p.y, p.z) * Cylinder(diameter / 2.0, length, rotation=(0.0, 90.0, 0.0), align=(Align.CENTER, Align.CENTER, Align.CENTER))


def _bar(a: PointYZ, b: PointYZ, width: float, tx: float, x: float) -> Shape:
    dy, dz = b.y - a.y, b.z - a.z
    length = hypot(dy, dz)
    angle = degrees(atan2(dz, dy))
    mid = PointYZ((a.y + b.y) / 2.0, (a.z + b.z) / 2.0)
    blank = Box(tx, length, width, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    return Pos(x, mid.y, mid.z) * Rot(angle, 0.0, 0.0) * blank


def _rotate_shape(shape: Shape, pivot: PointYZ, angle_deg: float) -> Shape:
    if abs(angle_deg) < 1.0e-12:
        return shape
    return Pos(0.0, pivot.y, pivot.z) * Rot(angle_deg, 0.0, 0.0) * Pos(0.0, -pivot.y, -pivot.z) * shape


def _tangent_support(center: PointYZ, tx: float, x: float, params: P25R1Parameters) -> Shape:
    radial_gap = (params.rear_saddle_diameter - params.rod_od) / 2.0
    return Pos(x, center.y, center.z - params.rod_od / 2.0 - radial_gap / 2.0) * Box(tx, 1.20, radial_gap, align=(Align.CENTER, Align.CENTER, Align.CENTER))


def build_rear_yoke(side: Side, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> Shape:
    frame, layout = clamp_frame(params), axial_layout(side, params, p20_params)
    tx, x = params.yoke_layer_thickness, layout.yoke_center_x
    collars = []
    for center in (frame.blue, frame.green):
        outer = _x_cylinder(params.saddle_outer_diameter, tx, x, center)
        inner = _x_cylinder(params.rear_saddle_diameter, tx + 0.4, x, center)
        opening = Pos(x, center.y, center.z + params.saddle_outer_diameter / 4.0) * Box(tx + 0.4, params.saddle_outer_diameter * 0.72, params.saddle_outer_diameter, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        collars.append((outer - [inner, opening]) + _tangent_support(center, tx, x, params))
    shift = PointYZ(0.0, params.rear_bridge_vertical_offset)
    rb, rg = _add(frame.blue, shift), _add(frame.green, shift)
    bridge = _bar(rb, rg, params.yoke_min_wall, tx, x)
    blue_tangent = PointYZ(frame.blue.y, frame.blue.z - params.rod_od / 2.0)
    green_tangent = PointYZ(frame.green.y, frame.green.z - params.rod_od / 2.0)
    legs = _bar(blue_tangent, rb, params.yoke_min_wall, tx, x) + _bar(green_tangent, rg, params.yoke_min_wall, tx, x)
    hinge_lug = _x_cylinder(params.hinge_lug_od, tx, x, frame.hinge)
    hinge_hole = _x_cylinder(params.hinge_hole_diameter, tx + 0.4, x, frame.hinge)
    hinge_route = PointYZ(frame.hinge.y, rb.z)
    hinge_arm = _bar(rb, hinge_route, params.yoke_min_wall, tx, x) + _bar(
        hinge_route, frame.hinge, params.yoke_min_wall, tx, x
    )
    latch_lug = _x_cylinder(params.hinge_lug_od, tx, x, frame.latch)
    latch_route = PointYZ(frame.latch.y, rg.z)
    latch_arm = _bar(rg, latch_route, params.yoke_min_wall, tx, x) + _bar(
        latch_route, frame.latch, params.yoke_min_wall, tx, x
    )
    sign = _side_sign(side)
    receiver_x = sign * (layout.inboard_abs_x + params.module_axial_thickness / 2.0)
    receiver = _x_cylinder(params.latch_receiver_od, params.module_axial_thickness, receiver_x, frame.latch)
    yoke = collars[0] + collars[1] + bridge + legs + hinge_arm + hinge_lug + latch_arm + latch_lug + receiver
    yoke = yoke - hinge_hole
    return _color(yoke, f"rear_yoke_{side}_BLUE_GREEN_open_saddles_D4p35", "#5B6572")


def _locked_front_bar(side: Side, params: P25R1Parameters, p20_params: p20.P20R4Parameters) -> Shape:
    frame, layout = clamp_frame(params), axial_layout(side, params, p20_params)
    tx, x = params.front_layer_thickness, layout.front_center_x
    bar = _bar(frame.hinge, frame.latch, params.front_bar_min_wall, tx, x)
    hinge = _x_cylinder(params.hinge_lug_od, tx, x, frame.hinge)
    hinge_hole = _x_cylinder(params.hinge_hole_diameter, tx + 0.4, x, frame.hinge)
    hook = _x_cylinder(params.latch_hook_outer_diameter, tx, x, frame.latch)
    hook_hole = _x_cylinder(params.latch_receiver_od + 2.0 * params.latch_clearance, tx + 0.4, x, frame.latch)
    slot_end = _add(
        frame.latch,
        _scale(latch_exit_direction(params), params.latch_hook_outer_diameter),
    )
    hook_slot = _bar(frame.latch, slot_end, params.latch_receiver_od + 2.0 * params.latch_clearance, tx + 0.4, x)
    orange_top = frame.orange.z + params.rod_od / 2.0 + params.orange_pad_offset
    bar_axis_z = frame.orange.z + params.front_bar_vertical_offset
    bar_low = bar_axis_z - abs(frame.tangent.y) * params.front_bar_min_wall / 2.0
    pad_h = bar_low - orange_top + 0.05
    pad = Pos(x, frame.orange.y, (orange_top + bar_low + 0.05) / 2.0) * Box(tx, params.orange_pad_diameter, pad_h, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    release_tab_end = _add(frame.latch, PointYZ(0.0, params.release_tab_length))
    tab = _bar(frame.latch, release_tab_end, params.front_bar_min_wall, tx, x)
    result = bar + hinge + hook + pad + tab
    result = result - [hinge_hole, hook_hole, hook_slot]
    return _color(result, f"front_pusher_bar_{side}_ORANGE_only_quick_hook", "#E9A72C")


def build_front_pusher_bar(side: Side, state: State, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> Shape:
    frame = clamp_frame(params)
    result = _rotate_shape(_locked_front_bar(side, params, p20_params), frame.hinge, state_angle(state, params))
    result.label = f"front_pusher_bar_{side}_{state}_ORANGE_only"
    return result


def build_hinge_pin_envelope(side: Side, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> Shape:
    frame, layout = clamp_frame(params), axial_layout(side, params, p20_params)
    x = _side_sign(side) * (layout.inboard_abs_x + params.module_axial_thickness / 2.0)
    return _color(_x_cylinder(params.hinge_pin_diameter, params.module_axial_thickness, x, frame.hinge), f"hinge_pin_envelope_{side}_OD2p00", "#C7CDD3")


def build_opening_spring_envelope(side: Side, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> Shape:
    frame, layout = clamp_frame(params), axial_layout(side, params, p20_params)
    outer = _x_cylinder(params.spring_envelope_od, params.spring_layer_thickness, layout.spring_center_x, frame.hinge)
    inner = _x_cylinder(params.spring_envelope_od - 2.0 * params.spring_wire_envelope, params.spring_layer_thickness + 0.2, layout.spring_center_x, frame.hinge)
    return _color(outer - inner, f"opening_spring_envelope_{side}_UNVERIFIED", "#8ED0E5", 0.55)


def module_parts(side: Side, state: State, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> tuple[Shape, Shape, Shape, Shape]:
    return (build_rear_yoke(side, params, p20_params), build_front_pusher_bar(side, state, params, p20_params), build_hinge_pin_envelope(side, params, p20_params), build_opening_spring_envelope(side, params, p20_params))


def build_module(side: Side, state: State, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> Compound:
    return Compound(children=list(module_parts(side, state, params, p20_params)), label=f"P25_{side}_module_{state}")


def _context(p: p20.P20R4Parameters) -> list[Shape]:
    u = 1.0
    children: list[Shape] = [p20.build_center_axle(p), p20.build_keeper("left", p), p20.build_keeper("right", p), p20.build_inner_plate("left", p), p20.build_inner_plate("right", p), p20.build_outer_plate("left", u, p), p20.build_outer_plate("right", u, p), p20.build_xt60_reference(p), p20.build_workpiece_reference()]
    children.extend(p20.build_rod(name, u, p) for name in p20.ROD_NAMES)
    return children


def build_preview(state: State, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> Compound:
    if state not in STATES:
        raise ValueError(f"unknown P25 state {state!r}")
    if params.rod_od != p20_params.rod_diameter or params.rod_length != p20_params.rod_length_target:
        raise ValueError("P25 must preserve inherited OD4 x 50 mm rods")
    children = _context(p20_params)
    children.extend(build_module(side, state, params, p20_params) for side in SIDES)
    return Compound(children=children, label=f"P25_R1_{state}_FIRST_CAD_NOT_PRINT_AUTHORITY")


def build_exploded(params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> Compound:
    placed: list[Shape] = []
    for side_index, side in enumerate(SIDES):
        for index, part in enumerate(module_parts(side, "LATCHED_END", params, p20_params)):
            moved = Pos((index - 1.5) * 9.0, side_index * 42.0 - 21.0, 0.0) * part
            moved.label = part.label
            placed.append(moved)
    return Compound(children=placed, label="P25_R1_LEFT_RIGHT_MODULES_EXPLODED")


def iter_leaf_shapes(shape: Shape):
    children = tuple(getattr(shape, "children", ()))
    if not children:
        yield shape
    else:
        for child in children:
            yield from iter_leaf_shapes(child)


def occurrence_census(shape: Shape) -> dict[str, object]:
    labels = tuple(x.label for x in iter_leaf_shapes(shape))
    return {"labels": labels, "rodCount": sum("_OD4_rod_L50.00" in x for x in labels), "capCount": sum("permanent_cap" in x for x in labels), "rearYokeCount": sum(x.startswith("rear_yoke_") for x in labels), "frontBarCount": sum(x.startswith("front_pusher_bar_") for x in labels), "hingeEnvelopeCount": sum(x.startswith("hinge_pin_envelope_") for x in labels), "springEnvelopeCount": sum(x.startswith("opening_spring_envelope_") for x in labels)}


def p25_pairwise_intersections(state: State, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> tuple[tuple[str, str, float], ...]:
    parts = tuple(x for side in SIDES for x in module_parts(side, state, params, p20_params))
    return tuple((a.label, b.label, p20.p19._intersection_volume(a, b)) for a, b in combinations(parts, 2))


def rod_contact_table(side: Side, state: State, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> dict[str, dict[str, float]]:
    yoke = build_rear_yoke(side, params, p20_params)
    bar = build_front_pusher_bar(side, state, params, p20_params)
    rods = {role: p20.build_rod(name, 1.0, p20_params) for role, name in ROLE_TO_P20_NAME.items()}
    return {
        "rearYokeBlue": {"distance": float(yoke.distance(rods["blue"])), "intersection": p20.p19._intersection_volume(yoke, rods["blue"])},
        "rearYokeGreen": {"distance": float(yoke.distance(rods["green"])), "intersection": p20.p19._intersection_volume(yoke, rods["green"])},
        "frontBarOrange": {"distance": float(bar.distance(rods["orange"])), "intersection": p20.p19._intersection_volume(bar, rods["orange"])},
        "frontBarBlue": {"distance": float(bar.distance(rods["blue"])), "intersection": p20.p19._intersection_volume(bar, rods["blue"])},
        "frontBarGreen": {"distance": float(bar.distance(rods["green"])), "intersection": p20.p19._intersection_volume(bar, rods["green"])},
        "rearYokeOrange": {"distance": float(yoke.distance(rods["orange"])), "intersection": p20.p19._intersection_volume(yoke, rods["orange"])},
    }


def sweep_clearances(side: Side, params: P25R1Parameters = P25_R1_DEFAULTS, p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> dict[float, dict[str, float]]:
    frame = clamp_frame(params)
    locked = _locked_front_bar(side, params, p20_params)
    result: dict[float, dict[str, float]] = {}
    for angle in (0.0, 10.0, 30.0, params.released_open_angle):
        bar = _rotate_shape(locked, frame.hinge, angle)
        result[abs(angle)] = {role: float(bar.distance(p20.build_rod(name, 1.0, p20_params))) for role, name in ROLE_TO_P20_NAME.items()}
    return result


def latch_sweep_clearances(
    side: Side,
    params: P25R1Parameters = P25_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> dict[float, dict[str, float]]:
    """Actual-solid hook/receiver release evidence, dense near 0 degrees."""
    frame = clamp_frame(params)
    yoke = build_rear_yoke(side, params, p20_params)
    locked_bar = _locked_front_bar(side, params, p20_params)
    result: dict[float, dict[str, float]] = {}
    for angle in (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 30.0, 60.0):
        bar = _rotate_shape(locked_bar, frame.hinge, angle)
        result[angle] = {
            "distanceMm": float(bar.distance(yoke)),
            "intersectionMm3": p20.p19._intersection_volume(bar, yoke),
        }
    return result


def latch_release_gap(params: P25R1Parameters = P25_R1_DEFAULTS) -> float:
    frame = clamp_frame(params)
    released = _rotate_point(frame.latch, frame.hinge, params.released_open_angle)
    center_distance = hypot(released.y - frame.latch.y, released.z - frame.latch.z)
    return max(0.0, center_distance - (params.latch_hook_outer_diameter + params.latch_receiver_od) / 2.0)


def inherited_baseline_collision_mm3(p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS) -> float:
    return p20.p19._intersection_volume(p20.build_rod("bottom", 0.0, p20_params), p20.build_xt60_reference(p20_params))


__all__ = ["AxialLayout", "ClampFrameYZ", "P25R1Parameters", "P25_R1_DEFAULTS", "ROLE_TO_P20_NAME", "ROLES", "SIDES", "STATES", "axial_layout", "build_exploded", "build_front_pusher_bar", "build_hinge_pin_envelope", "build_module", "build_opening_spring_envelope", "build_preview", "build_rear_yoke", "clamp_frame", "clamp_state_rod_center", "inherited_baseline_collision_mm3", "inherited_rod_center", "iter_leaf_shapes", "latch_exit_direction", "latch_release_gap", "latch_sweep_clearances", "module_parts", "occurrence_census", "p25_pairwise_intersections", "rod_contact_table", "state_angle", "sweep_clearances"]
