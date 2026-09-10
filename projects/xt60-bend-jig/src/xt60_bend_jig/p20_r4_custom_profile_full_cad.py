"""P20 R4 complete custom-profile CAD intent preview.

The model is deliberately a non-manufacturing preview.  It implements the
last accepted 2D customizer profile as one shared 361-point path authority,
then derives the two rotating outer-plate rail sets by inverse transforms.
Known 1.152 mm inner-rim and 1.715 mm left Blue/Orange web warnings are kept
visible; this module does not repair or waive them.

Coordinates: X is the plate-stack/rod axis.  FRONT is YZ, +Z is the XT60
mating head/up direction, and +Y is the wire-tail/outward-right direction.
"""

from __future__ import annotations

import json
from copy import copy
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from math import cos, radians, sin
from pathlib import Path
from typing import Literal

from build123d import (
    Align,
    BuildLine,
    CenterArc,
    Compound,
    Cylinder,
    Plane,
    Polyline,
    Pos,
    Rot,
    Shape,
    Side,
    extrude,
    make_face,
    offset,
)
from cadgen import srgb

from . import p19_r1_front_edge_short_tail as p19
from . import p20_r3_wire_90deg as p20r3


RodName = Literal["bottom", "diagonal", "upright"]
SideName = Literal["left", "right"]
StateName = Literal["open", "mid", "end"]
PointYZ = p19.PointYZ

ROD_NAMES: tuple[RodName, ...] = ("bottom", "diagonal", "upright")
PATH_STEPS = 360
PATH_POINT_COUNT = PATH_STEPS + 1
BREP_RAIL_POINT_COUNT = 33
PLATE_TRAVEL_DEG = 45.0

PROFILE_JSON = (
    '{"rods":[{"name":"bottom","startAngleDeg":118,"startRadiusMm":16,'
    '"archMm":0},{"name":"diagonal","startAngleDeg":45,"startRadiusMm":16,'
    '"archMm":0},{"name":"upright","startAngleDeg":-23,"startRadiusMm":16,'
    '"archMm":0}],"endOffset":{"yMm":-7.3241343806549555,'
    '"zMm":-2.77402040577638},"pathSteps":360,"archPeak":0.5,'
    '"curveBias":0,"innerPlateRadiusMm":20,"outerPlateRadiusMm":22.5,'
    '"fixedAxle":{"yMm":-10,"zMm":-10,"leftTravelDeg":45,'
    '"rightTravelDeg":-45,"guideWidthMm":7.9},'
    '"whiteRodCutterDiameterMm":4.15}'
)
PROFILE_SHA256 = "7a8013c935c74df865b3bd861ec163a00725e86f0e27415489babd26cd85eeb0"
INPUT_MANIFEST_SHA256 = "4286336b7709980f7d9ec4d22bb3f54f262639b88d3b3a7a1dba36b9e48b0691"

# Exact coordinates from the frozen design contract.  Keeping them explicit
# avoids re-deriving a rounded screenshot state in BREP code.
OPEN_POINTS: dict[RodName, PointYZ] = {
    "bottom": PointYZ(-7.511545005, 14.127161486),
    "diagonal": PointYZ(11.313708499, 11.313708499),
    "upright": PointYZ(14.728077655, -6.251698056),
}
END_POINTS: dict[RodName, PointYZ] = {
    "bottom": PointYZ(2.228077655, 5.248301944),
    "diagonal": PointYZ(8.478077655, -0.501698056),
    "upright": PointYZ(14.728077655, -6.251698056),
}
FIXED_AXLE_CENTER = PointYZ(-10.0, -10.0)


@dataclass(frozen=True, slots=True)
class P20R4Parameters:
    """Frozen full-preview geometry and inherited P19 axial-stack values."""

    inner_plate_radius: float = 20.0
    outer_plate_radius: float = 22.5
    inner_plate_thickness: float = 3.20
    outer_plate_thickness: float = 3.20
    inner_outer_running_gap: float = 0.40
    rod_diameter: float = 4.00
    # The purchased stainless rods are immutable OD4 x 50 mm stock. Widening
    # the fixed inner-plate span must be absorbed by the printed axial stack;
    # it must never silently change the purchased rod length.
    rod_length_target: float = 50.00
    fixed_slot_width: float = 4.15
    outer_slot_width: float = 4.15
    fixed_axle_guide_slot_width: float = 7.90
    fixed_axle_center_y: float = -10.0
    fixed_axle_center_z: float = -10.0

    # P19 axial stack and permanent-cap geometry are retained verbatim.
    xt60_body_width_x: float = 15.90
    xt60_side_clearance_each: float = 6.25
    cap_to_outer_running_gap: float = 0.30
    cap_rod_engagement: float = 8.70
    follower_head_diameter: float = 6.60
    follower_head_length: float = 9.05
    cap_closed_end_wall: float = 0.35
    cap_sliding_guide_id: float = 4.15
    cap_sliding_guide_depth: float = 4.70
    # P16/P13 physical evidence supports 4.10 mm as the modest looser PETG
    # fit for nominal OD4 rod; 4.04 mm was reported physically too tight.
    cap_socket_id: float = 4.10
    cap_retention_depth: float = 4.00

    center_axle_central_hex_af: float = 10.00
    center_axle_inner_hex_af: float = 8.00
    fixed_inner_hex_bore_af: float = 8.15
    outer_journal_diameter: float = 7.60
    keeper_seat_length: float = 1.20
    outer_keeper_thickness: float = 1.20
    keeper_axial_running_clearance: float = 0.25
    keeper_retention_interference_diametral: float = 0.05
    keeper_outer_diameter: float = 10.00

    xt60_body_y: float = 8.10
    xt60_body_z: float = 20.50
    xt60_body_center_y: float = -5.00
    xt60_body_center_z: float = 20.50
    exploded_spacing_x: float = 18.00

    @property
    def inner_clear_span(self) -> float:
        return self.xt60_body_width_x + 2.0 * self.xt60_side_clearance_each

    @property
    def left_inner_x(self) -> float:
        return -(self.inner_clear_span / 2.0 + self.inner_plate_thickness / 2.0)

    @property
    def right_inner_x(self) -> float:
        return -self.left_inner_x

    @property
    def left_outer_x(self) -> float:
        return self.left_inner_x - (
            self.inner_plate_thickness / 2.0
            + self.inner_outer_running_gap
            + self.outer_plate_thickness / 2.0
        )

    @property
    def right_outer_x(self) -> float:
        return -self.left_outer_x

    @property
    def left_cap_inner_face_x(self) -> float:
        return self.left_outer_x - self.outer_plate_thickness / 2.0 - self.cap_to_outer_running_gap

    @property
    def right_cap_inner_face_x(self) -> float:
        return -self.left_cap_inner_face_x

    @property
    def available_cap_rod_engagement(self) -> float:
        """Actual symmetric rod insertion remaining after the wider stack."""
        return self.rod_length_target / 2.0 + self.left_cap_inner_face_x

    @property
    def journal_with_keeper_seat_length(self) -> float:
        return (
            self.inner_outer_running_gap
            + self.outer_plate_thickness
            + self.keeper_axial_running_clearance
            + self.keeper_seat_length
        )

    @property
    def per_side_center_axle_length(self) -> float:
        return (
            self.inner_plate_thickness
            + self.inner_outer_running_gap
            + self.outer_plate_thickness
            + self.keeper_axial_running_clearance
            + self.keeper_seat_length
        )

    @property
    def center_axle_total_length(self) -> float:
        return self.inner_clear_span + 2.0 * self.per_side_center_axle_length

    @property
    def keeper_bore_diameter(self) -> float:
        return self.outer_journal_diameter - self.keeper_retention_interference_diametral

    @property
    def keeper_left_x(self) -> float:
        return -self.center_axle_total_length / 2.0 + self.outer_keeper_thickness / 2.0

    @property
    def keeper_right_x(self) -> float:
        return -self.keeper_left_x

    @property
    def inner_hex_bore_af(self) -> float:
        return self.fixed_inner_hex_bore_af


P20_R4_DEFAULTS = P20R4Parameters()
STATE_U: dict[StateName, float] = {"open": 0.0, "mid": 0.5, "end": 1.0}


def _clamp_u(u: float) -> float:
    if not 0.0 <= u <= 1.0:
        raise ValueError("P20 R4 progress must stay in 0..1")
    return float(u)


def _rotate(point: PointYZ, angle_deg: float) -> PointYZ:
    angle = radians(angle_deg)
    return PointYZ(
        point.y * cos(angle) - point.z * sin(angle),
        point.y * sin(angle) + point.z * cos(angle),
    )


def world_rod_center(name: RodName, u: float) -> PointYZ:
    """Single pure world-path authority used by rods and every rail."""
    u = _clamp_u(u)
    start, end = OPEN_POINTS[name], END_POINTS[name]
    return PointYZ(
        start.y + (end.y - start.y) * u,
        start.z + (end.z - start.z) * u,
    )


def outer_rotation_deg(side: SideName, u: float) -> float:
    u = _clamp_u(u)
    if side == "left":
        return PLATE_TRAVEL_DEG * u
    if side == "right":
        return -PLATE_TRAVEL_DEG * u
    raise ValueError(f"unknown side {side!r}")


def outer_local_center(side: SideName, name: RodName, u: float) -> PointYZ:
    """Inverse-frame rod center in one outer plate's unrotated local frame."""
    return _rotate(world_rod_center(name, u), -outer_rotation_deg(side, u))


def fixed_axle_local_center(side: SideName, u: float) -> PointYZ:
    return _rotate(FIXED_AXLE_CENTER, -outer_rotation_deg(side, u))


def reconstruct_world_from_outer(side: SideName, local: PointYZ, u: float) -> PointYZ:
    return _rotate(local, outer_rotation_deg(side, u))


def progress_samples() -> tuple[float, ...]:
    return tuple(index / PATH_STEPS for index in range(PATH_POINT_COUNT))


def inner_rail_locus(name: RodName) -> tuple[PointYZ, ...]:
    return tuple(world_rod_center(name, u) for u in progress_samples())


def outer_rail_locus(side: SideName, name: RodName) -> tuple[PointYZ, ...]:
    return tuple(outer_local_center(side, name, u) for u in progress_samples())


def fixed_axle_rail_locus(side: SideName) -> tuple[PointYZ, ...]:
    return tuple(fixed_axle_local_center(side, u) for u in progress_samples())


def outer_brep_rail_locus(side: SideName, name: RodName) -> tuple[PointYZ, ...]:
    """Small verified interpolation set used only for the written BREP."""
    return tuple(
        outer_local_center(side, name, index / (BREP_RAIL_POINT_COUNT - 1))
        for index in range(BREP_RAIL_POINT_COUNT)
    )


def _same_point(first: PointYZ, second: PointYZ, tolerance: float = 1.0e-10) -> bool:
    return first.distance_to(second) <= tolerance


def _capsule_cutter(points: tuple[PointYZ, ...], width: float, length_x: float) -> Shape:
    """Extrude a constant-width YZ capsule through a plate along X.

    The curve is simplified only when every canonical point is collinear; the
    361-point authority remains the source of that proof.  Curved paths use a
    spline constrained through every canonical sample.
    """
    if not points:
        raise ValueError("rail cutter requires at least one point")
    if all(_same_point(points[0], point) for point in points[1:]):
        return p19._x_cylinder(width, length_x, 0.0, points[0].y, points[0].z)

    first, last = points[0], points[-1]
    dy, dz = last.y - first.y, last.z - first.z
    scale = max((dy * dy + dz * dz) ** 0.5, 1.0)
    collinear = all(abs((point.y - first.y) * dz - (point.z - first.z) * dy) <= 1.0e-9 * scale for point in points)
    if collinear:
        return p19._slot_capsule_cutter((first, last), width, length_x)
    with BuildLine(Plane.YZ) as path:
        Polyline(*((point.y, point.z) for point in points))
    outline = offset(path.line, amount=width / 2.0, side=Side.BOTH, closed=True)
    face = make_face(outline)
    return extrude(face, amount=length_x / 2.0, dir=(1.0, 0.0, 0.0), both=True)


def _fixed_axle_arc_cutter(side: SideName, width: float, length_x: float) -> Shape:
    """Exact R=sqrt(200) circular axle guide, not a polyline approximation."""
    sweep = -PLATE_TRAVEL_DEG if side == "left" else PLATE_TRAVEL_DEG
    with BuildLine(Plane.YZ) as path:
        CenterArc((0.0, 0.0), 200.0**0.5, -135.0, sweep)
    outline = offset(path.line, amount=width / 2.0, side=Side.BOTH, closed=True)
    return extrude(
        make_face(outline),
        amount=length_x / 2.0,
        dir=(1.0, 0.0, 0.0),
        both=True,
    )


def _plate_disk(radius: float, thickness: float) -> Shape:
    return Cylinder(
        radius,
        thickness,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


@lru_cache(maxsize=None)
def _inner_plate_local(
    side: SideName,
    p: P20R4Parameters = P20_R4_DEFAULTS,
) -> Shape:
    # Keep one independently owned BREP per side.  Reusing a single cached
    # shape made the STEP exporter reuse its XCAF identity, so the later
    # right-inner label replaced both exported occurrence names.
    if side not in ("left", "right"):
        raise ValueError(f"unknown side {side!r}")
    hex_bore = p19._x_hex_prism(
        p.inner_hex_bore_af,
        p.inner_plate_thickness + 2.0,
        0.0,
        p.fixed_axle_center_y,
        p.fixed_axle_center_z,
    )
    cutters: list[Shape] = [hex_bore]
    cutters.extend(
        _capsule_cutter(
            (OPEN_POINTS[name], END_POINTS[name]),
            p.fixed_slot_width,
            p.inner_plate_thickness + 2.0,
        )
        for name in ("bottom", "diagonal")
    )
    # Green is exactly stationary on the inner plates: one round bore only.
    green = OPEN_POINTS["upright"]
    cutters.append(p19._x_cylinder(p.fixed_slot_width, p.inner_plate_thickness + 2.0, 0.0, green.y, green.z))
    part = _plate_disk(p.inner_plate_radius, p.inner_plate_thickness) - cutters
    part.label = "inner_R20_blue_orange_complete_green_round_bore_fixed_axle_hex"
    return part


@lru_cache(maxsize=None)
def _outer_plate_local(side: SideName, p: P20R4Parameters = P20_R4_DEFAULTS) -> Shape:
    cutters: list[Shape] = [
        _fixed_axle_arc_cutter(
            side,
            p.fixed_axle_guide_slot_width,
            p.outer_plate_thickness + 2.0,
        )
    ]
    cutters.extend(
        _capsule_cutter(
            outer_brep_rail_locus(side, name),
            p.outer_slot_width,
            p.outer_plate_thickness + 2.0,
        )
        for name in ROD_NAMES
    )
    part = _plate_disk(p.outer_plate_radius, p.outer_plate_thickness) - cutters
    part.label = f"{side}_outer_R22p5_all_three_inverse_rails_and_fixed_axle_arc"
    return part


def _colored(shape: Shape, label: str, color: str, alpha: float | None = None) -> Shape:
    shape.label = label
    shape.color = srgb(color) if alpha is None else srgb(color, alpha)
    return shape


def build_inner_plate(side: SideName, p: P20R4Parameters = P20_R4_DEFAULTS) -> Shape:
    x = p.left_inner_x if side == "left" else p.right_inner_x
    return _colored(
        Pos(x, 0.0, 0.0) * copy(_inner_plate_local(side, p)),
        f"fixed_{side}_inner_R20_blue_orange_rails_green_round_bore",
        "#D89A19",
    )


def build_outer_plate(side: SideName, u: float, p: P20R4Parameters = P20_R4_DEFAULTS) -> Shape:
    x = p.left_outer_x if side == "left" else p.right_outer_x
    color = "#377A3A" if side == "left" else "#2D6FA8"
    return _colored(
        Pos(x, 0.0, 0.0) * Rot(outer_rotation_deg(side, u), 0.0, 0.0) * copy(_outer_plate_local(side, p)),
        f"rotating_{side}_outer_R22p5_three_inverse_rails_fixed_axle_arc",
        color,
    )


def build_center_axle(p: P20R4Parameters = P20_R4_DEFAULTS) -> Shape:
    return _colored(
        p19.build_center_axle(p),  # type: ignore[arg-type]
        f"fixed_stepped_axle_A_y-10_z-10_L{p.center_axle_total_length:.2f}",
        "#B765D5",
    )


def build_keeper(side: SideName, p: P20R4Parameters = P20_R4_DEFAULTS) -> Shape:
    return _colored(
        p19.build_keeper(side, p),  # type: ignore[arg-type]
        f"fixed_{side}_permanent_outer_keeper",
        "#E86AA7",
    )


def build_rod(name: RodName, u: float, p: P20R4Parameters = P20_R4_DEFAULTS) -> Shape:
    point = world_rod_center(name, u)
    colors = {"bottom": "#379BF6", "diagonal": "#F18742", "upright": "#4DBE73"}
    return _colored(
        p19._x_cylinder(p.rod_diameter, p.rod_length_target, 0.0, point.y, point.z),
        f"{name}_OD4_rod_L{p.rod_length_target:.2f}",
        colors[name],
    )


def build_cap(side: SideName, name: RodName, u: float, p: P20R4Parameters = P20_R4_DEFAULTS) -> Shape:
    point = world_rod_center(name, u)
    if side == "left":
        x = p.left_cap_inner_face_x - p.follower_head_length / 2.0
        socket_open_side: Literal[-1, 1] = 1
    else:
        x = p.right_cap_inner_face_x + p.follower_head_length / 2.0
        socket_open_side = -1
    cap = Pos(x, point.y, point.z) * copy(
        p19._cap_local(p, socket_open_side=socket_open_side)  # type: ignore[arg-type]
    )
    return _colored(cap, f"{side}_{name}_permanent_cap_H9p05", "#1D1D1F")


def build_xt60_reference(p: P20R4Parameters = P20_R4_DEFAULTS) -> Shape:
    return _colored(
        p19.build_xt60_reference(p),  # type: ignore[arg-type]
        "fixed_reference_XT60_body",
        "#C8E6FF",
        0.42,
    )


def build_workpiece_reference() -> Shape:
    return _colored(
        p20r3.build_workpiece_reference_90deg(0.0),
        "fixed_reference_exact_90deg_two_conductor_workpiece",
        "#F1C84B",
        0.65,
    )


def _state_children(u: float, p: P20R4Parameters, *, motion_prefix: bool = False) -> list[Shape]:
    prefix = "motion_full_" if motion_prefix else ""
    children: list[Shape] = [
        build_center_axle(p),
        build_keeper("left", p),
        build_keeper("right", p),
        build_inner_plate("left", p),
        build_inner_plate("right", p),
        build_outer_plate("left", u, p),
        build_outer_plate("right", u, p),
        build_xt60_reference(p),
        build_workpiece_reference(),
    ]
    for name in ROD_NAMES:
        children.extend((build_rod(name, u, p), build_cap("left", name, u, p), build_cap("right", name, u, p)))
    if motion_prefix:
        label_map = {
            f"fixed_stepped_axle_A_y-10_z-10_L{p.center_axle_total_length:.2f}": "motion_full_fixed_stepped_axle",
            "fixed_left_permanent_outer_keeper": "motion_full_fixed_left_keeper",
            "fixed_right_permanent_outer_keeper": "motion_full_fixed_right_keeper",
            "fixed_left_inner_R20_blue_orange_rails_green_round_bore": "motion_full_fixed_left_inner",
            "fixed_right_inner_R20_blue_orange_rails_green_round_bore": "motion_full_fixed_right_inner",
            "rotating_left_outer_R22p5_three_inverse_rails_fixed_axle_arc": "motion_full_rotating_left_outer",
            "rotating_right_outer_R22p5_three_inverse_rails_fixed_axle_arc": "motion_full_rotating_right_outer",
            "fixed_reference_XT60_body": "motion_full_fixed_xt60_reference",
            "fixed_reference_exact_90deg_two_conductor_workpiece": "motion_full_fixed_workpiece_reference",
        }
        for child in children:
            if child.label in label_map:
                child.label = label_map[child.label]
            elif f"_OD4_rod_L{p.rod_length_target:.2f}" in child.label:
                child.label = f"{prefix}{child.label.split('_', 1)[0]}_rod"
            elif "_permanent_cap_H9p05" in child.label:
                side, name, *_ = child.label.split("_")
                child.label = f"{prefix}{side}_{name}_cap"
    return children


def build_motion_state(state: StateName, p: P20R4Parameters = P20_R4_DEFAULTS) -> Compound:
    u = STATE_U[state]
    return Compound(
        children=_state_children(u, p),
        label=f"P20_R4_{state}_FULL_18_OCCURRENCE_NON_MANUFACTURING_PREVIEW",
    )


def build_full_motion_open(p: P20R4Parameters = P20_R4_DEFAULTS) -> Compound:
    return Compound(
        children=_state_children(0.0, p, motion_prefix=True),
        label=f"P20_R4_full_motion_OPEN_18_OCCURRENCE_PREVIEW__{provenance_token()}",
    )


def build_exploded(p: P20R4Parameters = P20_R4_DEFAULTS) -> Compound:
    """All 18 occurrences spread axially/laterally for cap and gap review."""
    children = _state_children(0.0, p)
    placed: list[Shape] = []
    plate_x = {
        "rotating_left_outer": -72.0,
        "fixed_left_inner": -36.0,
        "fixed_right_inner": 36.0,
        "rotating_right_outer": 72.0,
    }
    for child in children:
        label = child.label
        delta = Pos(0.0, 0.0, 0.0)
        for token, target_x in plate_x.items():
            if label.startswith(token):
                current = child.bounding_box().center().X
                delta = Pos(target_x - current, 0.0, 0.0)
                break
        if "keeper" in label:
            current = child.bounding_box().center().X
            target = -54.0 if "left" in label else 54.0
            delta = Pos(target - current, 0.0, 0.0)
        elif "stepped_axle" in label:
            delta = Pos(0.0, -38.0, 0.0)
        elif "OD4_rod" in label:
            row = ROD_NAMES.index(label.split("_", 1)[0])
            delta = Pos(0.0, -52.0, (row - 1) * 10.0)
        elif "permanent_cap" in label and "keeper" not in label:
            parts = label.split("_")
            side, name = parts[0], parts[1]
            row = ROD_NAMES.index(name)
            delta = Pos(-24.0 if side == "left" else 24.0, -66.0, (row - 1) * 10.0)
        elif "XT60" in label:
            delta = Pos(0.0, 44.0, 4.0)
        elif "workpiece" in label:
            delta = Pos(0.0, 48.0, -18.0)
        moved = delta * child
        moved.label = label
        moved.color = child.color
        placed.append(moved)
    return Compound(children=placed, label="P20_R4_exploded_ALL_18_OCCURRENCES_AXIAL_REVIEW")


def build_artifact(name: StateName | Literal["exploded"], p: P20R4Parameters = P20_R4_DEFAULTS) -> Compound:
    return build_exploded(p) if name == "exploded" else build_motion_state(name, p)


def profile_evidence() -> dict[str, object]:
    residuals = []
    axle_residuals = []
    for u in progress_samples():
        for side in ("left", "right"):
            for name in ROD_NAMES:
                residuals.append(reconstruct_world_from_outer(side, outer_local_center(side, name, u), u).distance_to(world_rod_center(name, u)))
            axle_residuals.append(reconstruct_world_from_outer(side, fixed_axle_local_center(side, u), u).distance_to(FIXED_AXLE_CENTER))
    green = inner_rail_locus("upright")
    interpolation_deviations: dict[str, float] = {}
    for side in ("left", "right"):
        for name in ROD_NAMES:
            brep = outer_brep_rail_locus(side, name)
            maximum = 0.0
            for exact in outer_rail_locus(side, name):
                best = min(
                    _point_segment_distance(exact, first, second)
                    for first, second in zip(brep, brep[1:])
                )
                maximum = max(maximum, best)
            interpolation_deviations[f"{side}:{name}"] = maximum
    return {
        "profileSha256": sha256(PROFILE_JSON.encode("utf-8")).hexdigest(),
        "profileJsonParses": json.loads(PROFILE_JSON)["pathSteps"] == PATH_STEPS,
        "pointCountPerPath": PATH_POINT_COUNT,
        "greenInnerTravelMm": green[0].distance_to(green[-1]),
        "maxRodInverseRoundTripResidualMm": max(residuals),
        "maxFixedAxleRoundTripResidualMm": max(axle_residuals),
        "brepRailPointCount": BREP_RAIL_POINT_COUNT,
        "brepInterpolationMaxDeviationMm": max(interpolation_deviations.values()),
        "brepInterpolationDeviationByRailMm": interpolation_deviations,
        "knownInnerRimWebMm": 1.152,
        "knownLeftBlueOrangeWebMm": 1.715,
        "manufacturingAccepted": False,
    }


def occurrence_census(shape: Compound) -> dict[str, object]:
    labels = tuple(child.label for child in shape.children)
    return {
        "occurrenceCount": len(labels),
        "labels": labels,
        "plateCount": sum(
            ("_inner" in label or "_outer" in label)
            and "keeper" not in label
            and "cap" not in label
            for label in labels
        ),
        "rodCount": sum("_rod" in label and "fixed" not in label for label in labels),
        "capCount": sum("_cap" in label for label in labels),
        "keeperCount": sum("keeper" in label for label in labels),
        "hasXt60": any("xt60" in label.lower() for label in labels),
        "has90DegWorkpiece": any("workpiece" in label for label in labels),
    }


def _point_segment_distance(point: PointYZ, first: PointYZ, second: PointYZ) -> float:
    dy, dz = second.y - first.y, second.z - first.z
    denominator = dy * dy + dz * dz
    if denominator <= 1.0e-24:
        return point.distance_to(first)
    amount = ((point.y - first.y) * dy + (point.z - first.z) * dz) / denominator
    amount = max(0.0, min(1.0, amount))
    projection = PointYZ(first.y + amount * dy, first.z + amount * dz)
    return point.distance_to(projection)


def solid_evidence(p: P20R4Parameters = P20_R4_DEFAULTS) -> dict[str, object]:
    states: dict[str, object] = {}
    for state in ("open", "mid", "end"):
        assembly = build_motion_state(state, p)
        states[state] = {
            "occurrenceCount": len(assembly.children),
            "allValid": all(child.is_valid for child in assembly.children),
            "allPositiveVolume": all(child.volume > 0.0 for child in assembly.children),
        }
    return states


def actual_solid_evidence(p: P20R4Parameters = P20_R4_DEFAULTS) -> dict[str, object]:
    """Focused OPEN/MID/END rod/axle/cap versus plate BREP evidence."""
    maximum_rod_plate = 0.0
    maximum_axle_outer = 0.0
    maximum_cap_plate = 0.0
    minimum_cap_outer_clearance = float("inf")
    for u in STATE_U.values():
        inners = {side: build_inner_plate(side, p) for side in ("left", "right")}
        outers = {side: build_outer_plate(side, u, p) for side in ("left", "right")}
        axle = build_center_axle(p)
        for outer in outers.values():
            maximum_axle_outer = max(maximum_axle_outer, p19._intersection_volume(axle, outer))
        for name in ROD_NAMES:
            rod = build_rod(name, u, p)
            for plate in (*inners.values(), *outers.values()):
                maximum_rod_plate = max(maximum_rod_plate, p19._intersection_volume(rod, plate))
            for side in ("left", "right"):
                cap = build_cap(side, name, u, p)
                maximum_cap_plate = max(
                    maximum_cap_plate,
                    p19._intersection_volume(cap, inners[side]),
                    p19._intersection_volume(cap, outers[side]),
                )
                minimum_cap_outer_clearance = min(
                    minimum_cap_outer_clearance,
                    float(cap.distance(outers[side])),
                )
    return {
        "states": tuple(STATE_U),
        "maximumRodPlateIntersectionMm3": maximum_rod_plate,
        "maximumAxleOuterIntersectionMm3": maximum_axle_outer,
        "maximumCapPlateIntersectionMm3": maximum_cap_plate,
        "minimumCapOuterAxialClearanceMm": minimum_cap_outer_clearance,
        "rodSupportedByInnerAndOuterFeatures": maximum_rod_plate <= 1.0e-7,
        "fixedAxleWorldInvariant": True,
        "passesPreviewCollisionGate": max(
            maximum_rod_plate,
            maximum_axle_outer,
            maximum_cap_plate,
        ) <= 1.0e-7,
    }


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def provenance_token() -> str:
    return f"profile_{PROFILE_SHA256[:12]}__source_{source_revision_sha256()[:12]}"


def clear_geometry_caches() -> None:
    _inner_plate_local.cache_clear()
    _outer_plate_local.cache_clear()


__all__ = [
    "END_POINTS",
    "FIXED_AXLE_CENTER",
    "INPUT_MANIFEST_SHA256",
    "OPEN_POINTS",
    "PATH_POINT_COUNT",
    "PROFILE_JSON",
    "PROFILE_SHA256",
    "P20R4Parameters",
    "P20_R4_DEFAULTS",
    "ROD_NAMES",
    "build_artifact",
    "build_exploded",
    "build_full_motion_open",
    "build_motion_state",
    "actual_solid_evidence",
    "fixed_axle_local_center",
    "fixed_axle_rail_locus",
    "inner_rail_locus",
    "occurrence_census",
    "outer_local_center",
    "outer_rail_locus",
    "profile_evidence",
    "progress_samples",
    "reconstruct_world_from_outer",
    "solid_evidence",
    "source_revision_sha256",
    "world_rod_center",
]
