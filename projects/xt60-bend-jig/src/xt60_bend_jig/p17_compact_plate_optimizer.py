"""Deterministic 2D gate for the compact P17 R2 plate candidate.

This module deliberately does not build or modify any 3D solid.  It consumes
the authoritative current-P17 ``GUIDES``, applies one rigid placement to the
complete rod/workpiece set, and derives both outer-plate rails through the
same inverse-frame transform used by the P17 CAD source.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import lru_cache
from html import escape
from math import ceil, cos, hypot, pi, radians, sin
from pathlib import Path
from typing import Iterable, Literal, Sequence

from xt60_bend_jig.p17_r2_direct_counter_twist import (
    D13_COMMON_ROD_DELTA,
    GUIDES,
    P17_R2_DEFAULTS,
    ROD_NAMES,
    TRIANGLE_VERTEX_ORDER,
    PointYZ,
    RodName,
    SideName,
    transform_point_between_frames,
)


StateName = Literal["open", "end"]


@dataclass(frozen=True, slots=True)
class CompactCandidate:
    """Only independent optimizer inputs, all dimensions in millimetres."""

    theta_deg: float = 45.0
    rotation_center: PointYZ = PointYZ(0.0, 0.0)
    rigid_shift: PointYZ = PointYZ(-14.6869657526, -12.2949747468)
    fixed_axle: PointYZ = PointYZ(-9.5, -9.5)
    sample_count: int = 33
    required_web: float = 2.20
    left_hierarchy_increment: float = 1.0
    right_hierarchy_increment: float = 2.0
    maximum_plate_diameter: float = 55.0
    diameter_quantum: float = 0.001

    @property
    def inner_diameter(self) -> float:
        return derive_metrics(self).inner_diameter

    @property
    def left_outer_diameter(self) -> float:
        return derive_metrics(self).left_outer_diameter

    @property
    def right_outer_diameter(self) -> float:
        return derive_metrics(self).right_outer_diameter

    @property
    def min_internal_web(self) -> float:
        return derive_metrics(self).min_internal_web

    @property
    def boundary_web(self) -> float:
        """Compatibility name for the required boundary web input."""
        return self.required_web


DEFAULT_CANDIDATE = CompactCandidate()


@dataclass(frozen=True, slots=True)
class CandidateEvaluation:
    candidate: CompactCandidate
    valid: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BoundaryLimit:
    plate: str
    feature: str
    center: PointYZ
    cutter_edge: PointYZ
    plate_edge: PointYZ
    cutter_radius: float
    actual_web: float


@dataclass(frozen=True, slots=True)
class InternalWebLimit:
    plate: str
    first_feature: str
    second_feature: str
    centerline_distance: float
    first_radius: float
    second_radius: float

    @property
    def web(self) -> float:
        return self.centerline_distance - self.first_radius - self.second_radius


@dataclass(frozen=True, slots=True)
class DerivedMetrics:
    raw_inner_diameter: float
    raw_left_outer_diameter: float
    raw_right_outer_diameter: float
    inner_diameter: float
    left_outer_diameter: float
    right_outer_diameter: float
    min_internal_web: float
    internal_limit: InternalWebLimit
    boundary_limit: BoundaryLimit


def add(a: PointYZ, b: PointYZ) -> PointYZ:
    return PointYZ(a.y + b.y, a.z + b.z)


def subtract(a: PointYZ, b: PointYZ) -> PointYZ:
    return PointYZ(a.y - b.y, a.z - b.z)


def lerp(a: PointYZ, b: PointYZ, u: float) -> PointYZ:
    return PointYZ(a.y + (b.y - a.y) * u, a.z + (b.z - a.z) * u)


def rotate(point: PointYZ, angle_deg: float) -> PointYZ:
    angle = radians(angle_deg)
    return PointYZ(
        point.y * cos(angle) - point.z * sin(angle),
        point.y * sin(angle) + point.z * cos(angle),
    )


def side_angle(side: SideName, theta_deg: float) -> float:
    return -theta_deg if side == "left" else theta_deg


def placed_guide_point(
    name: RodName, u: float, candidate: CompactCandidate = DEFAULT_CANDIDATE
) -> PointYZ:
    """World rod centre along the exact current-P17 straight guide."""
    if not 0.0 <= u <= 1.0:
        raise ValueError("progress u must stay in 0..1")
    guide = GUIDES[name]
    return add(lerp(guide.open, guide.locked, u), candidate.rigid_shift)


def fixed_inner_track(
    name: RodName, candidate: CompactCandidate = DEFAULT_CANDIDATE
) -> tuple[PointYZ, PointYZ]:
    """The fixed-inner straight slot centreline, including P17 end margin."""
    guide = GUIDES[name]
    margin = P17_R2_DEFAULTS.slot_endpoint_margin
    direction = guide.direction
    start = PointYZ(
        guide.open.y - direction.y * margin,
        guide.open.z - direction.z * margin,
    )
    end = PointYZ(
        guide.locked.y + direction.y * margin,
        guide.locked.z + direction.z * margin,
    )
    return add(start, candidate.rigid_shift), add(end, candidate.rigid_shift)


def progress_samples(count: int) -> tuple[float, ...]:
    if count < 3:
        raise ValueError("sample count must be at least 3")
    return tuple(index / (count - 1) for index in range(count))


def outer_rail_local(
    side: SideName,
    name: RodName,
    candidate: CompactCandidate = DEFAULT_CANDIDATE,
) -> tuple[PointYZ, ...]:
    """Inverse-transform a fixed-world rod path into one outer plate frame."""
    samples = progress_samples(candidate.sample_count)
    return tuple(
        transform_point_between_frames(
            placed_guide_point(name, u, candidate),
            source_origin=PointYZ(0.0, 0.0),
            source_angle_deg=0.0,
            target_origin=candidate.rotation_center,
            target_angle_deg=side_angle(side, candidate.theta_deg) * u,
        )
        for u in samples
    )


def world_from_outer_local(
    local: PointYZ,
    side: SideName,
    state_u: float,
    candidate: CompactCandidate = DEFAULT_CANDIDATE,
) -> PointYZ:
    """Place a point authored in one outer plate into the fixed FRONT frame."""
    rotated = rotate(local, side_angle(side, candidate.theta_deg) * state_u)
    return add(candidate.rotation_center, rotated)


def outer_rail_world(
    side: SideName,
    name: RodName,
    state_u: float,
    candidate: CompactCandidate = DEFAULT_CANDIDATE,
) -> tuple[PointYZ, ...]:
    return tuple(
        world_from_outer_local(point, side, state_u, candidate)
        for point in outer_rail_local(side, name, candidate)
    )


def fixed_axle_rail_local(
    side: SideName, candidate: CompactCandidate = DEFAULT_CANDIDATE
) -> tuple[PointYZ, ...]:
    """Inverse-derived outer slot which keeps fixed axle A stationary."""
    offset = subtract(candidate.fixed_axle, candidate.rotation_center)
    return tuple(
        rotate(offset, -side_angle(side, candidate.theta_deg) * u)
        for u in progress_samples(candidate.sample_count)
    )


def fixed_axle_rail_world(
    side: SideName,
    state_u: float,
    candidate: CompactCandidate = DEFAULT_CANDIDATE,
) -> tuple[PointYZ, ...]:
    return tuple(
        world_from_outer_local(point, side, state_u, candidate)
        for point in fixed_axle_rail_local(side, candidate)
    )


def aligned_xt60_center(candidate: CompactCandidate = DEFAULT_CANDIDATE) -> PointYZ:
    """Apply the same D13 alignment and rigid shift as the rods."""
    source = PointYZ(
        P17_R2_DEFAULTS.xt60_body_center_y,
        P17_R2_DEFAULTS.xt60_body_center_z,
    )
    return add(add(source, D13_COMMON_ROD_DELTA), candidate.rigid_shift)


def wire_route_front(
    candidate: CompactCandidate = DEFAULT_CANDIDATE,
    arc_sample_count: int = 25,
) -> tuple[PointYZ, ...]:
    """Exact I10/D13+S wire route projected into FRONT YZ.

    The two physical wires are separated along X and therefore coincide in
    this projection.  The route is the fixed vertical leg, lower-left
    quarter-circle bend, and outward +Y horizontal tail from current P17.
    """
    if arc_sample_count < 3:
        raise ValueError("wire arc sample count must be at least 3")
    bend_source = PointYZ(
        P17_R2_DEFAULTS.bend_center_y,
        P17_R2_DEFAULTS.bend_center_z,
    )
    bend = add(add(bend_source, D13_COMMON_ROD_DELTA), candidate.rigid_shift)
    radius = P17_R2_DEFAULTS.bend_radius
    body = aligned_xt60_center(candidate)
    points: list[PointYZ] = [body, PointYZ(bend.y - radius, bend.z)]
    points.extend(
        PointYZ(
            bend.y + radius * cos(pi + (pi / 2.0) * index / (arc_sample_count - 1)),
            bend.z + radius * sin(pi + (pi / 2.0) * index / (arc_sample_count - 1)),
        )
        for index in range(1, arc_sample_count)
    )
    points.append(PointYZ(bend.y + 12.0, bend.z - radius))
    return tuple(points)


def _ceil_to_quantum(value: float, quantum: float) -> float:
    if quantum <= 0.0:
        raise ValueError("diameter quantum must be positive")
    return ceil(value / quantum - 1.0e-12) * quantum


def _point_segment_distance(point: PointYZ, start: PointYZ, end: PointYZ) -> float:
    dy, dz = end.y - start.y, end.z - start.z
    length_squared = dy * dy + dz * dz
    if length_squared <= 1.0e-24:
        return point.distance_to(start)
    u = ((point.y - start.y) * dy + (point.z - start.z) * dz) / length_squared
    u = max(0.0, min(1.0, u))
    closest = PointYZ(start.y + dy * u, start.z + dz * u)
    return point.distance_to(closest)


def _cross(a: PointYZ, b: PointYZ, c: PointYZ) -> float:
    return (b.y - a.y) * (c.z - a.z) - (b.z - a.z) * (c.y - a.y)


def _segments_intersect(a: PointYZ, b: PointYZ, c: PointYZ, d: PointYZ) -> bool:
    ab_c, ab_d = _cross(a, b, c), _cross(a, b, d)
    cd_a, cd_b = _cross(c, d, a), _cross(c, d, b)
    tolerance = 1.0e-12
    return (
        min(ab_c, ab_d) <= tolerance
        and max(ab_c, ab_d) >= -tolerance
        and min(cd_a, cd_b) <= tolerance
        and max(cd_a, cd_b) >= -tolerance
    )


def _segment_distance(a: PointYZ, b: PointYZ, c: PointYZ, d: PointYZ) -> float:
    if _segments_intersect(a, b, c, d):
        return 0.0
    return min(
        _point_segment_distance(a, c, d),
        _point_segment_distance(b, c, d),
        _point_segment_distance(c, a, b),
        _point_segment_distance(d, a, b),
    )


def _polyline_distance(first: Sequence[PointYZ], second: Sequence[PointYZ]) -> float:
    if not first or not second:
        raise ValueError("feature centerline cannot be empty")
    if len(first) == 1 and len(second) == 1:
        return first[0].distance_to(second[0])
    if len(first) == 1:
        return min(
            _point_segment_distance(first[0], start, end)
            for start, end in zip(second, second[1:])
        )
    if len(second) == 1:
        return min(
            _point_segment_distance(second[0], start, end)
            for start, end in zip(first, first[1:])
        )
    return min(
        _segment_distance(a, b, c, d)
        for a, b in zip(first, first[1:])
        for c, d in zip(second, second[1:])
    )


def _candidate_internal_limits(candidate: CompactCandidate) -> tuple[InternalWebLimit, ...]:
    rod_radius = P17_R2_DEFAULTS.fixed_slot_width / 2.0
    axle_inner_radius = P17_R2_DEFAULTS.fixed_inner_hex_bore_af / 2.0
    limits: list[InternalWebLimit] = []

    inner_features: list[tuple[str, tuple[PointYZ, ...], float]] = [
        (name, fixed_inner_track(name, candidate), rod_radius) for name in ROD_NAMES
    ]
    inner_features.append(("fixed_axle", (candidate.fixed_axle,), axle_inner_radius))
    for index, (first_name, first_line, first_radius) in enumerate(inner_features):
        for second_name, second_line, second_radius in inner_features[index + 1 :]:
            limits.append(
                InternalWebLimit(
                    "fixed_inner",
                    first_name,
                    second_name,
                    _polyline_distance(first_line, second_line),
                    first_radius,
                    second_radius,
                )
            )

    outer_rod_radius = P17_R2_DEFAULTS.outer_slot_width / 2.0
    axle_outer_radius = P17_R2_DEFAULTS.fixed_axle_guide_slot_width / 2.0
    for side in ("left", "right"):
        outer_features: list[tuple[str, tuple[PointYZ, ...], float]] = [
            (name, outer_rail_local(side, name, candidate), outer_rod_radius)
            for name in ROD_NAMES
        ]
        outer_features.append(
            ("fixed_axle", fixed_axle_rail_local(side, candidate), axle_outer_radius)
        )
        for index, (first_name, first_line, first_radius) in enumerate(outer_features):
            for second_name, second_line, second_radius in outer_features[index + 1 :]:
                limits.append(
                    InternalWebLimit(
                        f"{side}_outer",
                        first_name,
                        second_name,
                        _polyline_distance(first_line, second_line),
                        first_radius,
                        second_radius,
                    )
                )
    return tuple(limits)


@lru_cache(maxsize=64)
def derive_metrics(candidate: CompactCandidate = DEFAULT_CANDIDATE) -> DerivedMetrics:
    """Measure cutter envelopes/webs and derive every plate diameter."""
    rod_radius = P17_R2_DEFAULTS.fixed_slot_width / 2.0
    center = candidate.rotation_center
    fixed_limits: list[tuple[float, str, PointYZ, float]] = []
    for name in ROD_NAMES:
        for endpoint_name, point in zip(("start", "end"), fixed_inner_track(name, candidate)):
            radius = hypot(point.y - center.y, point.z - center.z)
            fixed_limits.append((radius + rod_radius, f"{name}_{endpoint_name}", point, rod_radius))
    axle_inner_radius = P17_R2_DEFAULTS.fixed_inner_hex_bore_af / 2.0
    axle_radial = hypot(
        candidate.fixed_axle.y - center.y,
        candidate.fixed_axle.z - center.z,
    )
    fixed_limits.append(
        (axle_radial + axle_inner_radius, "fixed_axle_bore", candidate.fixed_axle, axle_inner_radius)
    )
    limiting_edge_radius, limiting_name, limiting_center, limiting_cutter_radius = max(
        fixed_limits, key=lambda item: item[0]
    )
    raw_inner = 2.0 * (limiting_edge_radius + candidate.required_web)
    inner = _ceil_to_quantum(raw_inner, candidate.diameter_quantum)

    outer_raw: dict[SideName, float] = {}
    for side in ("left", "right"):
        feature_edge_radii = [
            hypot(point.y, point.z) + P17_R2_DEFAULTS.outer_slot_width / 2.0
            for name in ROD_NAMES
            for point in outer_rail_local(side, name, candidate)
        ]
        feature_edge_radii.extend(
            hypot(point.y, point.z)
            + P17_R2_DEFAULTS.fixed_axle_guide_slot_width / 2.0
            for point in fixed_axle_rail_local(side, candidate)
        )
        outer_raw[side] = 2.0 * (max(feature_edge_radii) + candidate.required_web)

    left = _ceil_to_quantum(
        max(outer_raw["left"], inner + candidate.left_hierarchy_increment),
        candidate.diameter_quantum,
    )
    right = _ceil_to_quantum(
        max(outer_raw["right"], inner + candidate.right_hierarchy_increment),
        candidate.diameter_quantum,
    )

    internal_limit = min(_candidate_internal_limits(candidate), key=lambda item: item.web)

    radial = subtract(limiting_center, center)
    radial_length = hypot(radial.y, radial.z)
    unit = PointYZ(radial.y / radial_length, radial.z / radial_length)
    cutter_edge = add(
        center,
        PointYZ(
            unit.y * (radial_length + limiting_cutter_radius),
            unit.z * (radial_length + limiting_cutter_radius),
        ),
    )
    plate_edge = add(
        center,
        PointYZ(unit.y * (inner / 2.0), unit.z * (inner / 2.0)),
    )
    boundary_limit = BoundaryLimit(
        "fixed_inner",
        limiting_name,
        limiting_center,
        cutter_edge,
        plate_edge,
        limiting_cutter_radius,
        cutter_edge.distance_to(plate_edge),
    )
    return DerivedMetrics(
        raw_inner,
        outer_raw["left"],
        outer_raw["right"],
        inner,
        left,
        right,
        internal_limit.web,
        internal_limit,
        boundary_limit,
    )


def evaluate_candidate(
    candidate: CompactCandidate = DEFAULT_CANDIDATE,
) -> CandidateEvaluation:
    """Apply the frozen P17 compact-gate constraints deterministically."""
    reasons: list[str] = []
    metrics = derive_metrics(candidate)
    if not 24.0 <= candidate.theta_deg <= 45.0:
        reasons.append("theta must stay in 24..45 deg")
    if candidate.sample_count != P17_R2_DEFAULTS.slot_sample_count:
        reasons.append("sample count must equal authoritative P17 cutter count")
    if candidate.required_web < 2.20:
        reasons.append("required web must be at least 2.20 mm")
    if candidate.left_hierarchy_increment < 1.0:
        reasons.append("left hierarchy increment must be at least 1.0 mm")
    if candidate.right_hierarchy_increment < 2.0:
        reasons.append("right hierarchy increment must be at least 2.0 mm")
    if not 50.0 <= metrics.inner_diameter <= candidate.maximum_plate_diameter:
        reasons.append("inner plate diameter must stay in 50..55 mm")
    if metrics.left_outer_diameter > candidate.maximum_plate_diameter:
        reasons.append("left outer plate exceeds maximum diameter")
    if metrics.right_outer_diameter > candidate.maximum_plate_diameter:
        reasons.append("right force outer plate exceeds maximum diameter")
    if metrics.left_outer_diameter + 1e-9 < metrics.inner_diameter + candidate.left_hierarchy_increment:
        reasons.append("left outer hierarchy is not satisfied")
    if metrics.right_outer_diameter + 1e-9 < metrics.inner_diameter + candidate.right_hierarchy_increment:
        reasons.append("right force outer hierarchy is not satisfied")
    if metrics.min_internal_web < candidate.required_web:
        reasons.append("internal web is below 2.20 mm")
    if metrics.boundary_limit.actual_web + 1e-12 < candidate.required_web:
        reasons.append("derived boundary web is below requirement")
    if candidate.fixed_axle.y >= aligned_xt60_center(candidate).y:
        reasons.append("fixed axle A is not left/behind XT60")
    return CandidateEvaluation(candidate, not reasons, tuple(reasons))


def select_candidate(candidates: Iterable[CompactCandidate]) -> CompactCandidate:
    """Select by the frozen objective: longest twist, then smallest plate."""
    valid = [item for item in candidates if evaluate_candidate(item).valid]
    if not valid:
        raise ValueError("no valid compact P17 candidate")
    return min(
        valid,
        key=lambda item: (
            -item.theta_deg,
            item.inner_diameter,
            item.right_outer_diameter,
            hypot(item.fixed_axle.y, item.fixed_axle.z),
        ),
    )


def boundary_web_for_inner_diameter(
    diameter: float, candidate: CompactCandidate = DEFAULT_CANDIDATE
) -> float:
    """Falsification helper: web left at the true limiting cutter edge."""
    metrics = derive_metrics(candidate)
    center = candidate.rotation_center
    cutter_edge_radius = hypot(
        metrics.boundary_limit.cutter_edge.y - center.y,
        metrics.boundary_limit.cutter_edge.z - center.z,
    )
    return diameter / 2.0 - cutter_edge_radius


def _svg_path(points: Sequence[PointYZ], panel_x: float, panel_y: float, scale: float) -> str:
    coords = [
        f"{panel_x + point.y * scale:.2f},{panel_y - point.z * scale:.2f}"
        for point in points
    ]
    return "M " + " L ".join(coords)


def _svg_circle(point: PointYZ, panel_x: float, panel_y: float, scale: float, **attrs: str) -> str:
    attributes = " ".join(f'{key.replace("_", "-")}="{escape(value)}"' for key, value in attrs.items())
    return (
        f'<circle cx="{panel_x + point.y * scale:.2f}" '
        f'cy="{panel_y - point.z * scale:.2f}" r="{2.0 * scale:.2f}" {attributes}/>'
    )


def render_svg(candidate: CompactCandidate = DEFAULT_CANDIDATE) -> str:
    """Render the deterministic fixed-FRONT OPEN/END P17 2D review gate."""
    evaluation = evaluate_candidate(candidate)
    if not evaluation.valid:
        raise ValueError("invalid candidate: " + "; ".join(evaluation.reasons))
    metrics = derive_metrics(candidate)

    width, height = 1500, 900
    panel_y, scale = 440.0, 8.0
    panels: tuple[tuple[StateName, float, float], ...] = (
        ("open", 0.0, 370.0),
        ("end", 1.0, 1090.0),
    )
    left_color, right_color = "#f59e0b", "#2563eb"
    rod_colors = {"bottom": "#111827", "diagonal": "#334155", "upright": "#0f172a"}
    lines: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<marker id="arrow-orange" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#f59e0b"/></marker>',
        '<marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#2563eb"/></marker>',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.small{font-size:14px;fill:#334155}.label{font-size:16px;font-weight:650;fill:#0f172a}.title{font-size:25px;font-weight:750;fill:#0f172a}.state{font-size:21px;font-weight:750;fill:#0f172a}</style>',
        "</defs>",
        '<rect width="1500" height="900" fill="#f8fafc"/>',
        '<text x="48" y="42" class="title">P17 R2 — compact plate optimizer 2D gate (not 3D)</text>',
        '<text x="48" y="68" class="small">Fixed FRONT: +Z head/up · +Y solder tail &amp; wires/right · exact current P17 rod identities</text>',
    ]

    xt60 = aligned_xt60_center(candidate)
    body_half_y = P17_R2_DEFAULTS.xt60_body_y / 2.0
    body_half_z = P17_R2_DEFAULTS.xt60_body_z / 2.0

    for state, u, panel_x in panels:
        state_name = "OPEN" if state == "open" else "END / LOCKED GEOMETRY"
        lines.append(f'<text x="{panel_x - 285:.0f}" y="108" class="state">{state_name}</text>')
        lines.append(
            f'<circle cx="{panel_x:.2f}" cy="{panel_y:.2f}" r="{candidate.right_outer_diameter / 2 * scale:.2f}" fill="#dbeafe" fill-opacity="0.24" stroke="{right_color}" stroke-width="3"/>'
        )
        lines.append(
            f'<circle cx="{panel_x:.2f}" cy="{panel_y:.2f}" r="{candidate.left_outer_diameter / 2 * scale:.2f}" fill="#fef3c7" fill-opacity="0.18" stroke="{left_color}" stroke-width="3"/>'
        )
        lines.append(
            f'<circle cx="{panel_x:.2f}" cy="{panel_y:.2f}" r="{candidate.inner_diameter / 2 * scale:.2f}" fill="#ffffff" fill-opacity="0.68" stroke="#64748b" stroke-width="2"/>'
        )

        # All three inner tracks remain straight and fixed in world coordinates.
        for name in ROD_NAMES:
            track = fixed_inner_track(name, candidate)
            lines.append(
                f'<path d="{_svg_path(track, panel_x, panel_y, scale)}" fill="none" stroke="#94a3b8" stroke-width="{P17_R2_DEFAULTS.fixed_slot_width * scale:.2f}" stroke-linecap="round" opacity="0.34"/>'
            )

        # Both side-local inverse rails, positioned at the state plate angle.
        for side, color in (("left", left_color), ("right", right_color)):
            for name in ROD_NAMES:
                rail = outer_rail_world(side, name, u, candidate)
                lines.append(
                    f'<path d="{_svg_path(rail, panel_x, panel_y, scale)}" fill="none" stroke="{color}" stroke-width="{P17_R2_DEFAULTS.outer_slot_width * scale:.2f}" stroke-linecap="round" stroke-linejoin="round" opacity="0.18"/>'
                )
                lines.append(
                    f'<path d="{_svg_path(rail, panel_x, panel_y, scale)}" fill="none" stroke="{color}" stroke-width="2.2" opacity="0.95"/>'
                )
            axle_rail = fixed_axle_rail_world(side, u, candidate)
            lines.append(
                f'<path d="{_svg_path(axle_rail, panel_x, panel_y, scale)}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="6 5" opacity="0.78"/>'
            )

        # Fixed XT60 body and wires; same aligned placement in both states.
        body_x = panel_x + (xt60.y - body_half_y) * scale
        body_y = panel_y - (xt60.z + body_half_z) * scale
        lines.append(
            f'<rect x="{body_x:.2f}" y="{body_y:.2f}" width="{2 * body_half_y * scale:.2f}" height="{2 * body_half_z * scale:.2f}" rx="5" fill="#facc15" stroke="#a16207" stroke-width="2" opacity="0.80"/>'
        )
        lines.append(
            f'<text x="{body_x - 5:.2f}" y="{body_y - 7:.2f}" class="small">XT60 head ↑</text>'
        )
        route = wire_route_front(candidate)
        lines.append(
            f'<path d="{_svg_path(route, panel_x, panel_y, scale)}" fill="none" stroke="#db2777" stroke-width="{P17_R2_DEFAULTS.wire_envelope_diameter * scale:.2f}" stroke-linecap="round" stroke-linejoin="round" opacity="0.28"/>'
        )
        lines.append(
            f'<path d="{_svg_path(route, panel_x, panel_y, scale)}" fill="none" stroke="#be185d" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        route_end = route[-1]
        lines.append(
            f'<text x="{panel_x + route_end.y * scale - 35:.2f}" y="{panel_y - route_end.z * scale + (25 if state == "open" else 74):.2f}" class="small">2 wires, coincident in FRONT → +Y</text>'
        )

        rod_points = {name: placed_guide_point(name, u, candidate) for name in ROD_NAMES}
        triangle = [rod_points[name] for name in TRIANGLE_VERTEX_ORDER]
        lines.append(
            f'<path d="{_svg_path(triangle, panel_x, panel_y, scale)}" fill="none" stroke="#111827" stroke-width="3.2" opacity="0.75"/>'
        )
        for name in ROD_NAMES:
            point = rod_points[name]
            lines.append(_svg_circle(point, panel_x, panel_y, scale, fill=rod_colors[name], stroke="#ffffff", stroke_width="2"))
            lines.append(
                f'<text x="{panel_x + point.y * scale + 18:.2f}" y="{panel_y - point.z * scale - 10:.2f}" class="small">{name}</text>'
            )

        # Fixed A and rotation datum C.
        lines.append(_svg_circle(candidate.fixed_axle, panel_x, panel_y, scale, fill="#7c3aed", stroke="#2e1065", stroke_width="4"))
        lines.append(
            f'<text x="{panel_x + candidate.fixed_axle.y * scale - 72:.2f}" y="{panel_y - candidate.fixed_axle.z * scale + 35:.2f}" class="label">A fixed axle</text>'
        )
        cx, cy = panel_x + candidate.rotation_center.y * scale, panel_y - candidate.rotation_center.z * scale
        lines.extend(
            [
                f'<line x1="{cx - 7:.2f}" y1="{cy:.2f}" x2="{cx + 7:.2f}" y2="{cy:.2f}" stroke="#0f766e" stroke-width="2"/>',
                f'<line x1="{cx:.2f}" y1="{cy - 7:.2f}" x2="{cx:.2f}" y2="{cy + 7:.2f}" stroke="#0f766e" stroke-width="2"/>',
                f'<text x="{cx + 9:.2f}" y="{cy - 8:.2f}" class="label">C</text>',
            ]
        )

        # Opposed 45-degree direction cues.
        arrow_y = panel_y + candidate.right_outer_diameter / 2 * scale + 34
        lines.append(
            f'<path d="M {panel_x - 125:.2f},{arrow_y:.2f} Q {panel_x - 40:.2f},{arrow_y + 55:.2f} {panel_x + 30:.2f},{arrow_y:.2f}" fill="none" stroke="{left_color}" stroke-width="3" marker-end="url(#arrow-orange)"/>'
        )
        lines.append(
            f'<path d="M {panel_x + 125:.2f},{arrow_y:.2f} Q {panel_x + 40:.2f},{arrow_y + 55:.2f} {panel_x - 30:.2f},{arrow_y:.2f}" fill="none" stroke="{right_color}" stroke-width="3" marker-end="url(#arrow-blue)"/>'
        )
        lines.append(f'<text x="{panel_x - 152:.2f}" y="{arrow_y + 67:.2f}" class="small">left −45°</text>')
        lines.append(f'<text x="{panel_x + 72:.2f}" y="{arrow_y + 67:.2f}" class="small">right +45°</text>')

        # Actual limiting extended bottom-track cutter edge to plate edge.
        gate_a = metrics.boundary_limit.cutter_edge
        gate_b = metrics.boundary_limit.plate_edge
        lines.append(f'<path d="{_svg_path((gate_a, gate_b), panel_x, panel_y, scale)}" stroke="#16a34a" stroke-width="5"/>')
        lines.append(
            f'<text x="{panel_x + gate_b.y * scale - 28:.2f}" y="{panel_y - gate_b.z * scale - 28:.2f}" class="small">bottom start cutter → plate: {metrics.boundary_limit.actual_web:.4f} ≥ {candidate.required_web:.2f}</text>'
        )

        lines.append(
            f'<text x="{panel_x - 285:.0f}" y="770" class="small">inner Ø{candidate.inner_diameter:.3f} · left outer Ø{candidate.left_outer_diameter:.3f} · right force outer Ø{candidate.right_outer_diameter:.3f}</text>'
        )

    lines.extend(
        [
            '<line x1="750" y1="90" x2="750" y2="790" stroke="#cbd5e1" stroke-width="2"/>',
            '<rect x="48" y="815" width="1404" height="58" rx="12" fill="#e2e8f0"/>',
            '<text x="70" y="842" class="label">✓ 3 × OD4 × 50 rods · ✓ OPEN right-angle triangle · ✓ END diagonal · ✓ identities unchanged · ✓ A left/behind XT60</text>',
            f'<text x="70" y="864" class="small">✓ straight fixed-inner tracks · ✓ inverse-derived outer rails · ✓ opposite twist · min internal web {metrics.min_internal_web:.3f} mm ({metrics.internal_limit.plate}: {metrics.internal_limit.first_feature}/{metrics.internal_limit.second_feature}) · CAD/print/physical acceptance NOT claimed</text>',
            '</svg>',
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_svg(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
