"""P24 R1 manual three-slider clamp first-intent CAD.

P24 preserves the P20 R4 four-plate mechanism, stepped axle, keepers,
OD4 x 50 mm rods, XT60/workpiece context, and every inherited rod-center
path.  It removes all caps and adds one X-mirrored three-shoe cassette per
side.  The cassette holds an already hand-reached state; it never drives or
redirects a rod.

Coordinates: X is the rod axis.  FRONT is YZ, +Z is XT60 mating-head/up,
and +Y is wire-tail/outward.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import hypot
from typing import Literal

from build123d import Align, Box, Compound, Cylinder, Pos, Shape
from cadgen import srgb

from . import p20_r4_custom_profile_full_cad as p20


Side = Literal["left", "right"]
Role = Literal["blue", "orange", "green"]
State = Literal["RELEASED_OPEN", "CLAMPED_END"]
PointYZ = p20.PointYZ

SIDES: tuple[Side, ...] = ("left", "right")
ROLES: tuple[Role, ...] = ("blue", "orange", "green")
ROLE_TO_P20_NAME = {
    "blue": "bottom",
    "orange": "diagonal",
    "green": "upright",
}
STATE_COORDINATES: dict[State, tuple[float, float]] = {
    "RELEASED_OPEN": (0.0, 0.0),
    "CLAMPED_END": (1.0, 1.0),
}


@dataclass(frozen=True, slots=True)
class P24R1Parameters:
    rod_diameter: float = 4.00
    rod_length: float = 50.00
    outer_plate_running_gap: float = 0.30
    shoe_engagement: float = 3.70
    shoe_socket_id: float = 4.20
    blind_end_clearance: float = 0.30
    shoe_neck_diameter: float = 6.20
    shoe_flange_diameter: float = 8.20
    shoe_flange_thickness: float = 1.20
    shoe_stem_outboard_length: float = 9.00
    shoe_stem_flange_overlap: float = 0.10
    slot_width: float = 7.20
    relief_radial_clearance: float = 0.50
    frame_thickness: float = 3.00
    pressure_plate_thickness: float = 3.00
    pressure_travel: float = 0.60
    plate_capture_endplay: float = 0.30
    frame_outer_margin: float = 3.00
    screw_envelope_diameter: float = 6.00
    screw_clearance_diameter: float = 6.60
    screw_knob_diameter: float = 14.00
    screw_knob_thickness: float = 4.00
    screw_retainer_diameter: float = 10.00
    screw_retainer_thickness: float = 0.60
    screw_axis_y: float = -2.00
    screw_axis_z: float = -6.00
    axle_relief_diameter: float = 10.60
    relief_sample_count: int = 33

    @property
    def socket_depth(self) -> float:
        return self.shoe_engagement + self.blind_end_clearance

    @property
    def flange_over_slot_margin(self) -> float:
        return (self.shoe_flange_diameter - self.slot_width) / 2.0

    @property
    def slot_over_neck_clearance(self) -> float:
        return (self.slot_width - self.shoe_neck_diameter) / 2.0


P24_R1_DEFAULTS = P24R1Parameters()


@dataclass(frozen=True, slots=True)
class CassetteXLayout:
    frame_inboard_x: float
    frame_outboard_x: float
    frame_center_x: float
    socket_open_x: float
    socket_blind_x: float
    rod_end_x: float
    flange_front_x: float
    flange_back_x: float
    pressure_inner_x: float
    pressure_center_x: float
    pressure_outer_x: float


@dataclass(frozen=True, slots=True)
class ScrewXLayout:
    shaft_inboard_x: float
    shaft_outboard_x: float
    head_inboard_x: float
    head_outboard_x: float
    retainer_inboard_x: float
    retainer_outboard_x: float


def _unit_interval(value: float, name: str) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must stay in 0..1")
    return float(value)


def _check_side(side: Side) -> Side:
    if side not in SIDES:
        raise ValueError(f"unknown side {side!r}")
    return side


def inherited_rod_center(role: Role, mechanism_progress: float) -> PointYZ:
    """Pure inherited center authority; every caller delegates to P20."""

    mechanism_progress = _unit_interval(mechanism_progress, "mechanism_progress")
    try:
        name = ROLE_TO_P20_NAME[role]
    except KeyError as exc:
        raise ValueError(f"unknown rod role {role!r}") from exc
    return p20.world_rod_center(name, mechanism_progress)  # type: ignore[arg-type]


def shoe_center(
    role: Role,
    mechanism_progress: float,
    clamp_progress: float,
) -> PointYZ:
    """Shoe YZ follows only its rod path; clamp progress is deliberately inert."""

    _unit_interval(clamp_progress, "clamp_progress")
    return inherited_rod_center(role, mechanism_progress)


def slot_locus(
    role: Role,
    params: P24R1Parameters = P24_R1_DEFAULTS,
) -> tuple[PointYZ, ...]:
    """Complete inherited OPEN-to-END YZ locus used by frame and plate slots."""

    return tuple(
        inherited_rod_center(role, index / (params.relief_sample_count - 1))
        for index in range(params.relief_sample_count)
    )


def clamp_gap(
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
) -> float:
    return params.pressure_travel * (1.0 - _unit_interval(clamp_progress, "clamp_progress"))


def screw_backoff(
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
) -> float:
    """Screw travel equals plate travel plus the captive 0.30 mm endplay."""

    return (params.pressure_travel + params.plate_capture_endplay) * (
        1.0 - _unit_interval(clamp_progress, "clamp_progress")
    )


def inherited_outer_plate_face_abs_x(
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> float:
    return p20_params.right_outer_x + p20_params.outer_plate_thickness / 2.0


def cassette_x_layout(
    side: Side,
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> CassetteXLayout:
    """Pure X stack. Only pressure/screw placements depend on clamp progress."""

    sign = -1.0 if _check_side(side) == "left" else 1.0
    frame_inboard_abs = inherited_outer_plate_face_abs_x(p20_params) + params.outer_plate_running_gap
    frame_outboard_abs = frame_inboard_abs + params.frame_thickness
    flange_front_abs = frame_outboard_abs
    flange_back_abs = flange_front_abs + params.shoe_flange_thickness
    gap = clamp_gap(clamp_progress, params)
    pressure_inner_abs = flange_back_abs + gap
    pressure_outer_abs = pressure_inner_abs + params.pressure_plate_thickness

    def signed(value: float) -> float:
        return sign * value

    return CassetteXLayout(
        frame_inboard_x=signed(frame_inboard_abs),
        frame_outboard_x=signed(frame_outboard_abs),
        frame_center_x=signed((frame_inboard_abs + frame_outboard_abs) / 2.0),
        socket_open_x=signed(frame_inboard_abs),
        socket_blind_x=signed(frame_inboard_abs + params.socket_depth),
        rod_end_x=signed(params.rod_length / 2.0),
        flange_front_x=signed(flange_front_abs),
        flange_back_x=signed(flange_back_abs),
        pressure_inner_x=signed(pressure_inner_abs),
        pressure_center_x=signed((pressure_inner_abs + pressure_outer_abs) / 2.0),
        pressure_outer_x=signed(pressure_outer_abs),
    )


def screw_x_layout(
    side: Side,
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> ScrewXLayout:
    """Pure reaction/head/retainer stack for the conceptual threaded screw."""

    sign = -1.0 if _check_side(side) == "left" else 1.0
    clamped_plate = cassette_x_layout(side, 1.0, params, p20_params)
    current_plate = cassette_x_layout(side, clamp_progress, params, p20_params)
    backoff = screw_backoff(clamp_progress, params)
    head_inboard_abs = abs(clamped_plate.pressure_outer_x) + backoff
    head_outboard_abs = head_inboard_abs + params.screw_knob_thickness
    retainer_outboard_abs = (
        abs(clamped_plate.pressure_inner_x) - params.plate_capture_endplay + backoff
    )
    retainer_inboard_abs = retainer_outboard_abs - params.screw_retainer_thickness
    shaft_inboard_abs = abs(current_plate.frame_inboard_x) + backoff
    shaft_outboard_abs = head_inboard_abs + 0.50

    def signed(value: float) -> float:
        return sign * value

    return ScrewXLayout(
        shaft_inboard_x=signed(shaft_inboard_abs),
        shaft_outboard_x=signed(shaft_outboard_abs),
        head_inboard_x=signed(head_inboard_abs),
        head_outboard_x=signed(head_outboard_abs),
        retainer_inboard_x=signed(retainer_inboard_abs),
        retainer_outboard_x=signed(retainer_outboard_abs),
    )


def screw_contact_gaps(
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
) -> dict[str, float]:
    """Named axial gaps; one bearing face closes at each endpoint."""

    clamp_progress = _unit_interval(clamp_progress, "clamp_progress")
    return {
        "outboardHeadToPlateMm": params.plate_capture_endplay * (1.0 - clamp_progress),
        "inboardRetainerToPlateMm": params.plate_capture_endplay * clamp_progress,
        "frameThreadRadialClearanceMm": 0.0,
    }


def finger_protrusion(
    side: Side,
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> float:
    """Shoe finger stem length beyond the pressure plate's outboard face."""

    layout = cassette_x_layout(side, clamp_progress, params, p20_params)
    stem_outer_abs = (
        abs(layout.flange_back_x)
        - params.shoe_stem_flange_overlap
        + params.shoe_stem_outboard_length
    )
    return stem_outer_abs - abs(layout.pressure_outer_x)


def screw_axis_yz(params: P24R1Parameters = P24_R1_DEFAULTS) -> PointYZ:
    """Clearance-gated first-CAD screw axis, shared by both X-mirrored sides."""

    return PointYZ(params.screw_axis_y, params.screw_axis_z)


def slot_clearance_evidence(
    params: P24R1Parameters = P24_R1_DEFAULTS,
) -> dict[str, float]:
    axis = screw_axis_yz(params)
    minimum_axis_to_locus = min(
        hypot(axis.y - point.y, axis.z - point.z)
        for role in ROLES
        for point in slot_locus(role, params)
    )
    return {
        "slotOverNeckRadialClearanceMm": params.slot_over_neck_clearance,
        "flangeOverSlotCaptureMarginMm": params.flange_over_slot_margin,
        "minimumScrewAxisToPathCenterMm": minimum_axis_to_locus,
        "requiredScrewAxisToSlotCenterMm": (
            params.slot_width + params.screw_clearance_diameter
        ) / 2.0,
    }


def _outline_bounds(params: P24R1Parameters) -> tuple[float, float, float, float]:
    path_points = tuple(point for role in ROLES for point in slot_locus(role, params))
    radius = params.slot_width / 2.0
    y_min = min(point.y for point in path_points) - radius
    y_max = max(point.y for point in path_points) + radius
    z_min = min(point.z for point in path_points) - radius
    z_max = max(point.z for point in path_points) + radius
    feature_disks = (
        (p20.FIXED_AXLE_CENTER, params.axle_relief_diameter / 2.0),
        (screw_axis_yz(params), params.screw_clearance_diameter / 2.0),
    )
    y_min = min(y_min, *(center.y - r for center, r in feature_disks))
    y_max = max(y_max, *(center.y + r for center, r in feature_disks))
    z_min = min(z_min, *(center.z - r for center, r in feature_disks))
    z_max = max(z_max, *(center.z + r for center, r in feature_disks))
    margin = params.frame_outer_margin
    return y_min - margin, y_max + margin, z_min - margin, z_max + margin


def _colored(shape: Shape, label: str, color: str) -> Shape:
    shape.label = label
    shape.color = srgb(color)
    return shape


def _x_cylinder(diameter: float, length: float, x: float, center: PointYZ) -> Shape:
    return Pos(x, center.y, center.z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _path_relief(
    role: Role,
    x: float,
    thickness: float,
    params: P24R1Parameters,
) -> Shape:
    return Pos(x, 0.0, 0.0) * p20._capsule_cutter(
        slot_locus(role, params),
        params.slot_width,
        thickness + 2.0,
    )


def _plate_blank(x: float, thickness: float, params: P24R1Parameters) -> Shape:
    y_min, y_max, z_min, z_max = _outline_bounds(params)
    return Pos(x, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0) * Box(
        thickness,
        y_max - y_min,
        z_max - z_min,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def build_side_frame(
    side: Side,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> Shape:
    layout = cassette_x_layout(side, 1.0, params, p20_params)
    frame = _plate_blank(layout.frame_center_x, params.frame_thickness, params)
    cutters = [
        _path_relief(role, layout.frame_center_x, params.frame_thickness, params)
        for role in ROLES
    ]
    cutters.extend(
        (
            _x_cylinder(
                params.screw_envelope_diameter,
                params.frame_thickness + 2.0,
                layout.frame_center_x,
                screw_axis_yz(params),
            ),
            _x_cylinder(
                params.axle_relief_diameter,
                params.frame_thickness + 2.0,
                layout.frame_center_x,
                p20.FIXED_AXLE_CENTER,
            ),
        )
    )
    frame = frame - cutters
    color = "#58616B" if side == "left" else "#77828E"
    return _colored(
        frame,
        f"{side}_side_frame_T3_path_reliefs_M6_CONCEPTUAL_THREAD_REACTION_NOT_HELICAL",
        color,
    )


def build_pressure_plate(
    side: Side,
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> Shape:
    layout = cassette_x_layout(side, clamp_progress, params, p20_params)
    plate = _plate_blank(layout.pressure_center_x, params.pressure_plate_thickness, params)
    cutters = [
        _path_relief(role, layout.pressure_center_x, params.pressure_plate_thickness, params)
        for role in ROLES
    ]
    cutters.append(
        _x_cylinder(
            params.screw_clearance_diameter,
            params.pressure_plate_thickness + 2.0,
            layout.pressure_center_x,
            screw_axis_yz(params),
        )
    )
    plate = plate - cutters
    color = "#8E6CC8" if side == "left" else "#39A6A3"
    return _colored(
        plate,
        f"{side}_common_pressure_plate_T3_clamp_{clamp_progress:.2f}",
        color,
    )


def build_shoe(
    side: Side,
    role: Role,
    mechanism_progress: float,
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> Shape:
    center = shoe_center(role, mechanism_progress, clamp_progress)
    layout = cassette_x_layout(side, clamp_progress, params, p20_params)
    sign = -1.0 if side == "left" else 1.0
    body_inner_abs = abs(layout.socket_open_x)
    body_outer_abs = abs(layout.flange_back_x)
    body = _x_cylinder(
        params.shoe_neck_diameter,
        body_outer_abs - body_inner_abs,
        sign * (body_inner_abs + body_outer_abs) / 2.0,
        center,
    )
    flange = _x_cylinder(
        params.shoe_flange_diameter,
        params.shoe_flange_thickness,
        sign * (abs(layout.flange_front_x) + abs(layout.flange_back_x)) / 2.0,
        center,
    )
    stem_inner_abs = abs(layout.flange_back_x) - params.shoe_stem_flange_overlap
    stem_outer_abs = stem_inner_abs + params.shoe_stem_outboard_length
    stem = _x_cylinder(
        params.shoe_neck_diameter,
        stem_outer_abs - stem_inner_abs,
        sign * (stem_inner_abs + stem_outer_abs) / 2.0,
        center,
    )
    bore_start_abs = abs(layout.socket_open_x) - 0.01
    bore_end_abs = abs(layout.socket_blind_x)
    bore = _x_cylinder(
        params.shoe_socket_id,
        bore_end_abs - bore_start_abs,
        sign * (bore_start_abs + bore_end_abs) / 2.0,
        center,
    )
    shoe = body + flange + stem - bore
    colors = {
        ("left", "blue"): "#2278C9",
        ("right", "blue"): "#59AEF5",
        ("left", "orange"): "#D76824",
        ("right", "orange"): "#F5A15E",
        ("left", "green"): "#2D8D51",
        ("right", "green"): "#66C985",
    }
    return _colored(
        shoe,
        f"{side}_{role}_floating_shoe_socket_ID4p20_flange_D8p20",
        colors[(side, role)],
    )


def build_screw_components(
    side: Side,
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> tuple[Shape, Shape, Shape]:
    """Shaft, outboard head/knob, and inboard plate retraction retainer."""

    layout = screw_x_layout(side, clamp_progress, params, p20_params)
    sign = -1.0 if side == "left" else 1.0
    shaft = _x_cylinder(
        params.screw_envelope_diameter,
        abs(layout.shaft_outboard_x) - abs(layout.shaft_inboard_x),
        sign * (abs(layout.shaft_inboard_x) + abs(layout.shaft_outboard_x)) / 2.0,
        screw_axis_yz(params),
    )
    head = _x_cylinder(
        params.screw_knob_diameter,
        params.screw_knob_thickness,
        sign * (abs(layout.head_inboard_x) + abs(layout.head_outboard_x)) / 2.0,
        screw_axis_yz(params),
    )
    retainer = _x_cylinder(
        params.screw_retainer_diameter,
        params.screw_retainer_thickness,
        sign * (abs(layout.retainer_inboard_x) + abs(layout.retainer_outboard_x)) / 2.0,
        screw_axis_yz(params),
    )
    return shaft, head, retainer


def build_screw_envelope(
    side: Side,
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> Shape:
    shaft, head, retainer = build_screw_components(
        side, clamp_progress, params, p20_params
    )
    screw = shaft + head + retainer
    color = "#D8B24A" if side == "left" else "#D9DDE3"
    return _colored(
        screw,
        f"{side}_central_M6_CONCEPTUAL_THREAD_NOT_HELICAL_head_knob_captive_plate_retainer_clamp_{clamp_progress:.2f}",
        color,
    )


def module_parts(
    side: Side,
    mechanism_progress: float,
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> tuple[Shape, ...]:
    return (
        build_side_frame(side, params, p20_params),
        *(build_shoe(side, role, mechanism_progress, clamp_progress, params, p20_params) for role in ROLES),
        build_pressure_plate(side, clamp_progress, params, p20_params),
        build_screw_envelope(side, clamp_progress, params, p20_params),
    )


def build_side_cassette(
    side: Side,
    mechanism_progress: float,
    clamp_progress: float,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> Compound:
    return Compound(
        children=list(module_parts(side, mechanism_progress, clamp_progress, params, p20_params)),
        label=f"{side}_manual_three_slider_common_pressure_cassette",
    )


def _context_children(
    mechanism_progress: float,
    p20_params: p20.P20R4Parameters,
) -> list[Shape]:
    children: list[Shape] = [
        p20.build_center_axle(p20_params),
        p20.build_keeper("left", p20_params),
        p20.build_keeper("right", p20_params),
        p20.build_inner_plate("left", p20_params),
        p20.build_inner_plate("right", p20_params),
        p20.build_outer_plate("left", mechanism_progress, p20_params),
        p20.build_outer_plate("right", mechanism_progress, p20_params),
        p20.build_xt60_reference(p20_params),
        p20.build_workpiece_reference(),
    ]
    children.extend(
        p20.build_rod(name, mechanism_progress, p20_params) for name in p20.ROD_NAMES
    )
    return children


def build_preview(
    state: State,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> Compound:
    if state not in STATE_COORDINATES:
        raise ValueError(f"unknown P24 state {state!r}")
    if p20_params.rod_diameter != params.rod_diameter or p20_params.rod_length_target != params.rod_length:
        raise ValueError("P24 must preserve the inherited OD4 x 50 mm purchased rods")
    mechanism_progress, clamp_progress = STATE_COORDINATES[state]
    children = _context_children(mechanism_progress, p20_params)
    children.extend(
        build_side_cassette(side, mechanism_progress, clamp_progress, params, p20_params)
        for side in SIDES
    )
    return Compound(
        children=children,
        label=f"P24_R1_{state}_MANUAL_THREE_SLIDER_CLAMP_FIRST_INTENT_NOT_PRINT_AUTHORITY",
    )


def iter_leaf_shapes(shape: Shape):
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
        "shoeCount": sum("_floating_shoe_socket_ID4p20_" in label for label in labels),
        "frameCount": sum("_side_frame_T3_" in label for label in labels),
        "pressurePlateCount": sum("_common_pressure_plate_T3_" in label for label in labels),
        "screwEnvelopeCount": sum("_central_M6_CONCEPTUAL_THREAD_" in label for label in labels),
    }


def p24_pairwise_intersections(
    state: State,
    params: P24R1Parameters = P24_R1_DEFAULTS,
    p20_params: p20.P20R4Parameters = p20.P20_R4_DEFAULTS,
) -> tuple[tuple[str, str, float], ...]:
    mechanism_progress, clamp_progress = STATE_COORDINATES[state]
    parts = tuple(
        part
        for side in SIDES
        for part in module_parts(side, mechanism_progress, clamp_progress, params, p20_params)
    )
    return tuple(
        (first.label, second.label, p20.p19._intersection_volume(first, second))
        for first, second in combinations(parts, 2)
    )


def named_zero_penetration_contacts(state: State) -> tuple[tuple[str, str], ...]:
    contacts: list[tuple[str, str]] = []
    _, clamp_progress = STATE_COORDINATES[state]
    for side in SIDES:
        frame = f"{side}_side_frame_T3_path_reliefs_M6_CONCEPTUAL_THREAD_REACTION_NOT_HELICAL"
        pressure = f"{side}_common_pressure_plate_T3_clamp_{clamp_progress:.2f}"
        screw = f"{side}_central_M6_CONCEPTUAL_THREAD_NOT_HELICAL_head_knob_captive_plate_retainer_clamp_{clamp_progress:.2f}"
        contacts.extend(((frame, screw), (pressure, screw)))
        for role in ROLES:
            shoe = f"{side}_{role}_floating_shoe_socket_ID4p20_flange_D8p20"
            contacts.append((frame, shoe))
            if state == "CLAMPED_END":
                contacts.append((pressure, shoe))
    return tuple(contacts)


__all__ = [
    "CassetteXLayout",
    "ScrewXLayout",
    "P24R1Parameters",
    "P24_R1_DEFAULTS",
    "ROLE_TO_P20_NAME",
    "ROLES",
    "SIDES",
    "STATE_COORDINATES",
    "build_preview",
    "build_pressure_plate",
    "build_shoe",
    "build_side_frame",
    "build_screw_envelope",
    "build_screw_components",
    "cassette_x_layout",
    "clamp_gap",
    "finger_protrusion",
    "inherited_rod_center",
    "iter_leaf_shapes",
    "module_parts",
    "named_zero_penetration_contacts",
    "occurrence_census",
    "p24_pairwise_intersections",
    "screw_backoff",
    "screw_contact_gaps",
    "screw_x_layout",
    "shoe_center",
    "slot_clearance_evidence",
    "slot_locus",
]
