"""P19 R1 direct-CAD counter-twist XT60 bend-jig candidate.

Coordinates: X is the rod/plate-stack axis. The mechanism lives in YZ. The
fixed inner guide plates are grounded by one stepped center axle. Left and
right outer plates are separate hand-operated occurrences rotating equal
magnitude and opposite sign about X on round journals.

This module is CAD/source evidence only. Cap retention, endpoint retention,
heat response, wear, vibration, wire holding, and final physical acceptance
remain physical gates.
"""

from __future__ import annotations

import json
import os
from copy import copy
from dataclasses import asdict, dataclass, fields, replace
from functools import lru_cache
from hashlib import sha256
from math import atan, atan2, cos, degrees, hypot, pi, radians, sin, sqrt
from pathlib import Path
from typing import Callable, Iterable, Literal, Sequence

from build123d import (
    Align,
    Box,
    BuildPart,
    BuildSketch,
    Compound,
    Cylinder,
    Plane,
    Pos,
    RegularPolygon,
    Rot,
    Shape,
    Torus,
    Vector,
    extrude,
)
from cadgen import srgb


RodName = Literal["upright", "bottom", "diagonal"]
SideName = Literal["left", "right"]
StateName = Literal["open", "mid", "contact", "end"]
ArtifactName = Literal[
    "open",
    "mid",
    "contact",
    "end",
    "exploded",
    "print_kit",
    "permanent_cap_coupon",
    "center_axle_coupon",
]

ROD_NAMES: tuple[RodName, ...] = ("upright", "bottom", "diagonal")
TRIANGLE_VERTEX_ORDER: tuple[RodName, ...] = ("bottom", "diagonal", "upright")
PHYSICAL_STAINLESS_STOCK_LENGTH_MM = 50.00
P19_R1_DESIGN_CONTRACT_PATH = (
    "docs/iterations/p19-r1-front-edge-short-tail/"
    "REOPTIMIZED_4MM_OPEN_UPRIGHT_DESIGN.md"
)
P19_R1_DESIGN_CONTRACT_SHA256 = (
    "36e346c45f6b241e834da8d2dcc9009823bbf85809044021b42e8a33e1f393d4"
)

ROD_VERTEX_ROLE: dict[RodName, str] = {
    "bottom": "upper_left_to_upper_left",
    "diagonal": "upper_right_to_middle",
    "upright": "lower_right_to_lower_right",
}


@dataclass(frozen=True, slots=True)
class PointYZ:
    y: float
    z: float

    def as_tuple(self) -> tuple[float, float]:
        return (self.y, self.z)

    def distance_to(self, other: "PointYZ") -> float:
        return hypot(self.y - other.y, self.z - other.z)


P19_OPEN_UPRIGHT_DOWNWARD_MM = 4.172814225900
P19_END_COMMON_DELTA = PointYZ(1.552212035894, -0.977677650052)
P19_RAIL_CENTER_TRAVEL_MIN_MM = 4.0
P19_OPEN_WIRE_CLEARANCE_MIN_MM = 0.75
P19_TOOL_KEEP_OUTSIDE_RIM_MM = 0.75
P19_CONDITION_MAX = 15.0


@dataclass(frozen=True, slots=True)
class ServicePose:
    delta_y: float
    delta_z: float
    phi_deg: float


@dataclass(frozen=True, slots=True)
class GuidePath:
    name: RodName
    open: PointYZ
    contact: PointYZ
    end: PointYZ

    @property
    def direction(self) -> PointYZ:
        length = self.open.distance_to(self.end)
        return PointYZ(
            (self.end.y - self.open.y) / length,
            (self.end.z - self.open.z) / length,
        )

    @property
    def travel(self) -> float:
        return self.open.distance_to(self.end)


@dataclass(frozen=True, slots=True)
class MotionState:
    """One shared normalized physical state for both outer plates."""

    u: float
    theta_deg: float
    alpha_left_deg: float
    alpha_right_deg: float
    rods: tuple[tuple[RodName, PointYZ], ...]

    def rod(self, name: RodName) -> PointYZ:
        return dict(self.rods)[name]


@dataclass(frozen=True, slots=True)
class P19R1Parameters:
    # XT60 and axial stack.
    xt60_body_width_x: float = 15.90
    xt60_side_clearance_each: float = 1.25
    inner_plate_thickness: float = 3.20
    outer_plate_thickness: float = 3.20
    inner_outer_running_gap: float = 0.40
    cap_to_outer_running_gap: float = 0.30
    cap_rod_engagement: float = 8.70

    # Stepped center axle.
    center_axle_central_hex_af: float = 10.00
    center_axle_inner_hex_af: float = 8.00
    fixed_inner_hex_bore_af: float = 8.15
    outer_journal_diameter: float = 7.60
    outer_journal_clearance_diametral: float = 0.30
    keeper_seat_length: float = 1.20
    outer_keeper_thickness: float = 1.20
    keeper_axial_running_clearance: float = 0.25
    keeper_retention_interference_diametral: float = 0.05
    keeper_outer_diameter: float = 10.00
    keeper_coupon_bore_diameters: tuple[float, ...] = (7.50, 7.55, 7.60)

    # Rod/cap/follower geometry.
    rod_diameter: float = 4.00
    follower_head_diameter: float = 6.60
    follower_head_length: float = 9.05
    cap_closed_end_wall: float = 0.35
    cap_sliding_guide_id: float = 4.15
    cap_sliding_guide_depth: float = 4.70
    cap_socket_id: float = 4.04
    cap_retention_depth: float = 4.00
    cap_socket_ladder_ids: tuple[float, ...] = (3.96, 4.00, 4.04, 4.08, 4.12)
    cap_socket_ladder_depths: tuple[float, ...] = (3.50, 4.00, 4.50)

    # Plates, slots, endpoint travel, and print allowances.
    inner_plate_diameter: float = 54.400
    left_outer_secondary_grip_diameter: float = 54.700
    right_outer_primary_grip_diameter: float = 55.000
    fixed_slot_width: float = 4.15
    outer_slot_width: float = 4.15
    slot_endpoint_margin: float = 0.00
    slot_sample_count: int = 65
    validation_sample_count: int = 65
    theta_end_deg: float = 5.00
    min_web_mm: float = 2.20

    # D06 separates the unchanged outer-rotation datum C from the fixed purple
    # stepped-axle datum A.  Inner plate outlines and every frozen white-rod/
    # guide/cam construction remain authored about C; only the inner hex bores,
    # stepped axle and keepers move to A.
    outer_rotation_center_y: float = 0.00
    outer_rotation_center_z: float = 0.00
    fixed_axle_center_y: float = -13.00
    fixed_axle_center_z: float = -9.00
    fixed_axle_guide_sample_count: int = 33

    # Reference-only workpiece envelopes.
    xt60_body_y: float = 8.10
    xt60_body_z: float = 20.50
    xt60_body_center_y: float = -5.000
    xt60_body_center_z: float = 20.500
    wire_envelope_diameter: float = 4.30
    wire_preload: float = 0.25
    wire_line_point_y: float = 12.192732506095444
    wire_line_point_z: float = 10.892453295819136
    wire_line_direction_y: float = 0.7359310117618296
    wire_line_direction_z: float = -0.6770565308208832
    wire_model_start_y: float = -7.00
    wire_model_end_y: float = 36.25
    solder_tool_min_y: float = 28.25
    solder_tool_size_yz: float = 8.00
    solder_tool_depth_x: float = 10.00
    service_clearance_min: float = 0.75
    slot_fit_coupon_widths: tuple[float, ...] = (4.10, 4.15, 4.20, 4.25, 4.30)
    completed_pigtail_extract_end_y: float = 18.765

    # Layouts.
    exploded_spacing_x: float = 18.00

    @property
    def inner_clear_span(self) -> float:
        return self.xt60_body_width_x + 2.0 * self.xt60_side_clearance_each

    @property
    def principal_stack_width(self) -> float:
        return (
            self.inner_clear_span
            + 2.0 * self.inner_plate_thickness
            + 2.0 * self.outer_plate_thickness
            + 2.0 * self.inner_outer_running_gap
        )

    @property
    def rod_length_raw(self) -> float:
        return (
            self.principal_stack_width
            + 2.0 * self.cap_to_outer_running_gap
            + 2.0 * self.cap_rod_engagement
        )

    @property
    def rod_length_target(self) -> float:
        return round(self.rod_length_raw, 2)

    @property
    def center_axle_total_length(self) -> float:
        return self.inner_clear_span + 2.0 * self.per_side_center_axle_length

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
    def left_inner_x(self) -> float:
        return -(self.inner_clear_span / 2.0 + self.inner_plate_thickness / 2.0)

    @property
    def right_inner_x(self) -> float:
        return self.inner_clear_span / 2.0 + self.inner_plate_thickness / 2.0

    @property
    def left_outer_x(self) -> float:
        return (
            self.left_inner_x
            - self.inner_plate_thickness / 2.0
            - self.inner_outer_running_gap
            - self.outer_plate_thickness / 2.0
        )

    @property
    def right_outer_x(self) -> float:
        return (
            self.right_inner_x
            + self.inner_plate_thickness / 2.0
            + self.inner_outer_running_gap
            + self.outer_plate_thickness / 2.0
        )

    @property
    def left_cap_inner_face_x(self) -> float:
        return self.left_outer_x - self.outer_plate_thickness / 2.0 - self.cap_to_outer_running_gap

    @property
    def right_cap_inner_face_x(self) -> float:
        return self.right_outer_x + self.outer_plate_thickness / 2.0 + self.cap_to_outer_running_gap

    @property
    def right_primary_extra_lever_radius(self) -> float:
        return (
            self.right_outer_primary_grip_diameter
            - self.left_outer_secondary_grip_diameter
        ) / 2.0

    @property
    def outer_bearing_bore_diameter(self) -> float:
        return self.outer_journal_diameter + self.outer_journal_clearance_diametral

    @property
    def fixed_axle_guide_slot_width(self) -> float:
        return self.outer_journal_diameter + self.outer_journal_clearance_diametral

    @property
    def fixed_axle_eccentricity(self) -> float:
        return hypot(
            self.fixed_axle_center_y - self.outer_rotation_center_y,
            self.fixed_axle_center_z - self.outer_rotation_center_z,
        )

    @property
    def pivot_y(self) -> float:
        """Compatibility alias for the frozen outer-rotation center C."""
        return self.outer_rotation_center_y

    @property
    def pivot_z(self) -> float:
        """Compatibility alias for the frozen outer-rotation center C."""
        return self.outer_rotation_center_z

    @property
    def slot_center_slop_nominal(self) -> float:
        return (self.fixed_slot_width - self.rod_diameter) / 2.0

    @property
    def inner_hex_bore_af(self) -> float:
        return self.fixed_inner_hex_bore_af

    @property
    def inner_hex_bore_circumradius(self) -> float:
        """Exact regular-hex corner radius; never substitute AF/2."""
        return self.fixed_inner_hex_bore_af / sqrt(3.0)

    @property
    def inner_hex_bore_web(self) -> float:
        return (self.inner_plate_diameter / 2.0) - (self.inner_hex_bore_af / 2.0)

    @property
    def outer_bearing_wall(self) -> float:
        return (self.left_outer_secondary_grip_diameter / 2.0) - (self.outer_bearing_bore_diameter / 2.0)

    @property
    def journal_outer_plate_overlap(self) -> float:
        return self.outer_plate_thickness

    @property
    def journal_with_keeper_seat_length(self) -> float:
        return (
            self.inner_outer_running_gap
            + self.outer_plate_thickness
            + self.keeper_axial_running_clearance
            + self.keeper_seat_length
        )

    @property
    def keeper_bore_diameter(self) -> float:
        return self.outer_journal_diameter - self.keeper_retention_interference_diametral

    @property
    def keeper_radial_wall_min(self) -> float:
        return (self.keeper_outer_diameter - self.keeper_bore_diameter) / 2.0

    @property
    def keeper_left_x(self) -> float:
        return -self.center_axle_total_length / 2.0 + self.outer_keeper_thickness / 2.0

    @property
    def keeper_right_x(self) -> float:
        return self.center_axle_total_length / 2.0 - self.outer_keeper_thickness / 2.0

    def __post_init__(self) -> None:
        if not 17.90 <= self.inner_clear_span <= 19.50:
            raise ValueError("P19 R1 inner clear span must stay in 17.90..19.50 mm")
        if abs(self.rod_length_target - PHYSICAL_STAINLESS_STOCK_LENGTH_MM) > 1.0e-9:
            raise ValueError("P19 R1 must use all three uncut OD4 x 50.00 mm rods")
        if self.cap_socket_id < self.rod_diameter:
            raise ValueError("P19 R1 permanent cap default must not be an interference socket")
        if (self.follower_head_diameter - self.cap_socket_id) / 2.0 < 1.20:
            raise ValueError("permanent follower cap radial wall must be at least 1.20 mm")
        if self.cap_rod_engagement + self.cap_closed_end_wall > self.follower_head_length + 1.0e-9:
            raise ValueError("cap engagement must leave a closed-end wall")
        if abs(self.cap_sliding_guide_depth + self.cap_retention_depth - self.cap_rod_engagement) > 1.0e-9:
            raise ValueError("stepped cap guide and retention depths must equal rod engagement")
        if self.cap_sliding_guide_id != self.fixed_slot_width:
            raise ValueError("cap proximal guide ID must match the moving-slot fit")
        if self.right_primary_extra_lever_radius <= 0.0:
            raise ValueError("right primary actuator must have larger grip leverage")
        if self.fixed_axle_guide_slot_width <= self.outer_journal_diameter:
            raise ValueError("outer axle guide must clear round journal")
        if self.outer_journal_diameter >= self.inner_hex_bore_af:
            raise ValueError("round journal must slide through the fixed-inner hex bore")
        if self.center_axle_inner_hex_af >= self.inner_hex_bore_af:
            raise ValueError("inner hex key needs named AF clearance in the fixed-inner bore")
        if self.inner_hex_bore_web < self.min_web_mm:
            raise ValueError("inner hex bore web is below PETG minimum")
        if self.outer_bearing_wall < self.min_web_mm:
            raise ValueError("outer bearing wall is below PETG minimum")
        if self.journal_outer_plate_overlap < 2.40:
            raise ValueError("journal must support most of the outer plate thickness")
        if self.keeper_bore_diameter >= self.outer_journal_diameter:
            raise ValueError("keeper must have modeled permanent retention/interference on the seat")
        if abs(self.keeper_outer_diameter - 10.00) > 1.0e-9 or abs(self.keeper_bore_diameter - 7.55) > 1.0e-9:
            raise ValueError("P19 R1 requires keeper OD10.00 / bore7.55 mm")
        if self.keeper_radial_wall_min < 1.20:
            raise ValueError("keeper radial wall must be at least 1.20 mm")
        if self.slot_sample_count < 5 or self.slot_sample_count % 2 == 0:
            raise ValueError("slot_sample_count must be odd and at least 5")
        if self.fixed_axle_guide_sample_count < 33 or self.fixed_axle_guide_sample_count % 2 == 0:
            raise ValueError("fixed axle guide requires an odd sample count of at least 33")
        if self.validation_sample_count < 65 or self.validation_sample_count % 2 == 0:
            raise ValueError("three-rod validation requires an odd sample count of at least 65")
        if self.fixed_slot_width != 4.15 or self.outer_slot_width != 4.15:
            raise ValueError("P19 R1 three-rod contract requires 4.15 mm moving slots")
        if self.theta_end_deg != 5.0:
            raise ValueError("P19 R1 cycle-4 contract requires a 5 degree endpoint")


P19_R1_DEFAULTS = P19R1Parameters()

SERVICE_WAYPOINTS: tuple[ServicePose, ...] = (
    ServicePose(0.0, 0.0, 0.0),
    ServicePose(-8.0, 10.0, -5.0),
    ServicePose(-16.0, 26.0, -10.0),
    ServicePose(-16.0, 50.0, -10.0),
)

GUIDES: dict[RodName, GuidePath] = {
    "bottom": GuidePath(
        "bottom",
        PointYZ(5.000000000000, 10.000000000000),
        PointYZ(8.852590965276, 8.326267979887),
        PointYZ(9.552212035894, 8.022322349948),
    ),
    "diagonal": GuidePath(
        "diagonal",
        PointYZ(20.400000000000, 10.000000000000),
        PointYZ(20.008143071241, 9.341391109371),
        PointYZ(15.802212035894, 2.272322349948),
    ),
    "upright": GuidePath(
        "upright",
        PointYZ(20.400000000000, -9.172814225900),
        PointYZ(21.974422349877, -3.745816893946),
        PointYZ(22.052212035894, -3.477677650052),
    ),
}

FIRST_CONTACT_PROGRESS: dict[RodName, float] = {
    "bottom": 0.8463118446369933,
    "diagonal": 0.08522727272723803,
    "upright": 0.9529178553801358,
}
STATE_THETA: dict[StateName, float] = {
    "open": 0.0,
    "mid": P19_R1_DEFAULTS.theta_end_deg / 2.0,
    "contact": P19_R1_DEFAULTS.theta_end_deg
    * min(FIRST_CONTACT_PROGRESS.values()),
    "end": P19_R1_DEFAULTS.theta_end_deg,
}


def parameters_from_overrides(overrides: dict[str, object] | None = None) -> P19R1Parameters:
    overrides = overrides or {}
    unknown = set(overrides) - {field.name for field in fields(P19R1Parameters)}
    if unknown:
        raise ValueError(f"unknown P19 R1 parameter(s): {sorted(unknown)}")
    return replace(P19_R1_DEFAULTS, **overrides)


def parameters_from_env() -> P19R1Parameters:
    raw = os.environ.get("P19_R1_PARAMS_JSON", "").strip()
    overrides = json.loads(raw) if raw else {}
    return parameters_from_overrides(overrides)


def alpha_left(theta_deg: float) -> float:
    return -theta_deg


def alpha_right(theta_deg: float) -> float:
    return theta_deg


def rotation_for_side(side: SideName, theta_deg: float) -> float:
    return alpha_left(theta_deg) if side == "left" else alpha_right(theta_deg)


def motion_state(
    u: float,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> MotionState:
    """Return the one physical P19 state shared by both plate sides.

    The function is pure math.  Every rod position, outer rail, static STEP
    state and Viewer transform delegates to this same normalized ``u`` law.
    """
    if not 0.0 <= u <= 1.0:
        raise ValueError("P19 motion progress must stay in 0..1")
    theta = p.theta_end_deg * u
    rods = tuple(
        (
            name,
            PointYZ(
                GUIDES[name].open.y
                + (GUIDES[name].end.y - GUIDES[name].open.y) * u,
                GUIDES[name].open.z
                + (GUIDES[name].end.z - GUIDES[name].open.z) * u,
            ),
        )
        for name in ROD_NAMES
    )
    return MotionState(
        u=u,
        theta_deg=theta,
        alpha_left_deg=alpha_left(theta),
        alpha_right_deg=alpha_right(theta),
        rods=rods,
    )


def _rotate_yz(point: PointYZ, angle_deg: float) -> PointYZ:
    a = radians(angle_deg)
    return PointYZ(
        point.y * cos(a) - point.z * sin(a),
        point.y * sin(a) + point.z * cos(a),
    )


def outer_rotation_center_yz(p: P19R1Parameters = P19_R1_DEFAULTS) -> PointYZ:
    """World YZ center C for both independently rotating outer plates."""
    return PointYZ(p.outer_rotation_center_y, p.outer_rotation_center_z)


def fixed_axle_center_yz(p: P19R1Parameters = P19_R1_DEFAULTS) -> PointYZ:
    """World YZ center A of the fixed purple stepped axle."""
    return PointYZ(p.fixed_axle_center_y, p.fixed_axle_center_z)


def pivot_yz(p: P19R1Parameters = P19_R1_DEFAULTS) -> PointYZ:
    """Compatibility name for the frozen outer-rotation center C."""
    return outer_rotation_center_yz(p)


def _relative_to_pivot(point: PointYZ, p: P19R1Parameters) -> PointYZ:
    pivot = outer_rotation_center_yz(p)
    return PointYZ(point.y - pivot.y, point.z - pivot.z)


def _world_from_pivot(local: PointYZ, p: P19R1Parameters) -> PointYZ:
    pivot = outer_rotation_center_yz(p)
    return PointYZ(local.y + pivot.y, local.z + pivot.z)


def transform_point_between_frames(
    point: PointYZ,
    *,
    source_origin: PointYZ,
    source_angle_deg: float,
    target_origin: PointYZ,
    target_angle_deg: float,
) -> PointYZ:
    """Map one source-local YZ point into a target-local rotating frame.

    This is the single deterministic authority used for every P19 mating rail:
    ``p_target = T_target^-1 * T_source * p_source``.  It is pure math and
    deliberately contains no BREP or cutter operations.
    """
    source_world_offset = _rotate_yz(point, source_angle_deg)
    world = PointYZ(
        source_origin.y + source_world_offset.y,
        source_origin.z + source_world_offset.z,
    )
    target_world_offset = PointYZ(
        world.y - target_origin.y,
        world.z - target_origin.z,
    )
    return _rotate_yz(target_world_offset, -target_angle_deg)


def derive_mating_rail(
    source_path: Sequence[PointYZ] | Callable[[float], PointYZ],
    progress_values: Iterable[float],
    *,
    source_origin: PointYZ,
    source_total_rotation_deg: float,
    target_origin: PointYZ,
    target_total_rotation_deg: float,
) -> tuple[PointYZ, ...]:
    """Derive a sampled rail in another frame from one parameterized path.

    ``progress_values`` are normalized ``u`` samples.  A sequence source must
    have exactly one point per sample; a callable is evaluated at each sample.
    CW/CCW is expressed only by the sign of each total rotation.
    """
    progress = tuple(float(value) for value in progress_values)
    if any(value < 0.0 or value > 1.0 for value in progress):
        raise ValueError("rail progress values must stay in 0..1")
    if callable(source_path):
        points = tuple(source_path(value) for value in progress)
    else:
        points = tuple(source_path)
        if len(points) != len(progress):
            raise ValueError("source path and progress samples must have equal length")
    return tuple(
        transform_point_between_frames(
            point,
            source_origin=source_origin,
            source_angle_deg=source_total_rotation_deg * u,
            target_origin=target_origin,
            target_angle_deg=target_total_rotation_deg * u,
        )
        for point, u in zip(points, progress)
    )


def rod_center(name: RodName, theta_deg: float, p: P19R1Parameters = P19_R1_DEFAULTS) -> PointYZ:
    u = max(0.0, min(1.0, theta_deg / p.theta_end_deg))
    return motion_state(u, p).rod(name)


def outer_slot_local_center(side: SideName, name: RodName, theta_deg: float, p: P19R1Parameters = P19_R1_DEFAULTS) -> PointYZ:
    u = max(0.0, min(1.0, theta_deg / p.theta_end_deg))
    return derive_mating_rail(
        lambda progress: rod_center(name, p.theta_end_deg * progress, p),
        (u,),
        source_origin=PointYZ(0.0, 0.0),
        source_total_rotation_deg=0.0,
        target_origin=outer_rotation_center_yz(p),
        target_total_rotation_deg=rotation_for_side(side, p.theta_end_deg),
    )[0]


def reconstruct_world_from_outer(side: SideName, name: RodName, theta_deg: float, p: P19R1Parameters = P19_R1_DEFAULTS) -> PointYZ:
    local = outer_slot_local_center(side, name, theta_deg, p)
    return _world_from_pivot(_rotate_yz(local, rotation_for_side(side, theta_deg)), p)


def outer_slot_locus(side: SideName, name: RodName, p: P19R1Parameters = P19_R1_DEFAULTS) -> tuple[PointYZ, ...]:
    progress = tuple(index / (p.slot_sample_count - 1) for index in range(p.slot_sample_count))
    return derive_mating_rail(
        lambda u: rod_center(name, p.theta_end_deg * u, p),
        progress,
        source_origin=PointYZ(0.0, 0.0),
        source_total_rotation_deg=0.0,
        target_origin=outer_rotation_center_yz(p),
        target_total_rotation_deg=rotation_for_side(side, p.theta_end_deg),
    )


def outer_rail_speed(
    side: SideName,
    name: RodName,
    u: float,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> float:
    """Exact centreline speed ``|dq/du|`` for one inverse-derived rail."""
    state = motion_state(u, p)
    point = state.rod(name)
    guide = GUIDES[name]
    velocity = PointYZ(
        guide.end.y - guide.open.y,
        guide.end.z - guide.open.z,
    )
    alpha_prime = radians(
        -p.theta_end_deg if side == "left" else p.theta_end_deg
    )
    # q=R(-alpha)p; rotation preserves the norm of v-alpha' Jp.
    world_tangent = PointYZ(
        velocity.y + alpha_prime * point.z,
        velocity.z - alpha_prime * point.y,
    )
    return hypot(world_tangent.y, world_tangent.z)


def _adaptive_simpson(
    function: Callable[[float], float],
    first: float,
    last: float,
    *,
    tolerance: float = 1.0e-12,
    max_depth: int = 24,
) -> float:
    middle = (first + last) / 2.0
    fa, fm, fb = function(first), function(middle), function(last)
    whole = (last - first) * (fa + 4.0 * fm + fb) / 6.0

    def recurse(
        a: float,
        b: float,
        f_a: float,
        f_m: float,
        f_b: float,
        estimate: float,
        tol: float,
        depth: int,
    ) -> float:
        m = (a + b) / 2.0
        lm, rm = (a + m) / 2.0, (m + b) / 2.0
        f_lm, f_rm = function(lm), function(rm)
        left = (m - a) * (f_a + 4.0 * f_lm + f_m) / 6.0
        right = (b - m) * (f_m + 4.0 * f_rm + f_b) / 6.0
        delta = left + right - estimate
        if depth <= 0 or abs(delta) <= 15.0 * tol:
            return left + right + delta / 15.0
        return recurse(a, m, f_a, f_lm, f_m, left, tol / 2.0, depth - 1) + recurse(
            m, b, f_m, f_rm, f_b, right, tol / 2.0, depth - 1
        )

    return recurse(first, last, fa, fm, fb, whole, tolerance, max_depth)


def outer_rail_center_travel(
    side: SideName,
    name: RodName,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> float:
    return _adaptive_simpson(lambda u: outer_rail_speed(side, name, u, p), 0.0, 1.0)


def fixed_axle_guide_local_center(
    side: SideName,
    theta_deg: float,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> PointYZ:
    """Part-local center of fixed axle A in an outer plate at ``theta_deg``."""
    center = outer_rotation_center_yz(p)
    axle = fixed_axle_center_yz(p)
    offset = PointYZ(axle.y - center.y, axle.z - center.z)
    return _rotate_yz(offset, -rotation_for_side(side, theta_deg))


def fixed_axle_guide_locus(
    side: SideName,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> tuple[PointYZ, ...]:
    return tuple(
        fixed_axle_guide_local_center(
            side,
            p.theta_end_deg * index / (p.fixed_axle_guide_sample_count - 1),
            p,
        )
        for index in range(p.fixed_axle_guide_sample_count)
    )


def reconstruct_fixed_axle_from_outer(
    side: SideName,
    theta_deg: float,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> PointYZ:
    local = fixed_axle_guide_local_center(side, theta_deg, p)
    return _world_from_pivot(
        _rotate_yz(local, rotation_for_side(side, theta_deg)), p
    )


def fixed_guide_locus(name: RodName, p: P19R1Parameters = P19_R1_DEFAULTS) -> tuple[PointYZ, PointYZ]:
    guide = GUIDES[name]
    direction = guide.direction
    return (
        PointYZ(
            guide.open.y - direction.y * p.slot_endpoint_margin,
            guide.open.z - direction.z * p.slot_endpoint_margin,
        ),
        PointYZ(
            guide.end.y + direction.y * p.slot_endpoint_margin,
            guide.end.z + direction.z * p.slot_endpoint_margin,
        ),
    )


def fixed_guide_local_locus(name: RodName, p: P19R1Parameters = P19_R1_DEFAULTS) -> tuple[PointYZ, PointYZ]:
    return tuple(_relative_to_pivot(point, p) for point in fixed_guide_locus(name, p))  # type: ignore[return-value]


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def _x_cylinder(diameter: float, length: float, x: float, y: float, z: float) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _y_cylinder(diameter: float, length: float, x: float, y: float, z: float) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(90.0, 0.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _z_cylinder(diameter: float, length: float, x: float, y: float, z: float) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _yz_line_cylinder(
    diameter: float,
    first: PointYZ,
    second: PointYZ,
    x: float,
) -> Shape:
    """Centered cylinder along one arbitrary FRONT-YZ line segment."""
    dy = second.y - first.y
    dz = second.z - first.z
    length = hypot(dy, dz)
    if length <= 1.0e-9:
        raise ValueError("YZ line cylinder needs two distinct endpoints")
    angle = degrees(atan2(dz, dy))
    return (
        Pos(x, (first.y + second.y) / 2.0, (first.z + second.z) / 2.0)
        * Rot(angle, 0.0, 0.0)
        * Cylinder(
            diameter / 2.0,
            length,
            rotation=(90.0, 0.0, 0.0),
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
    )


def wire_line_z_at_y(
    y: float,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> float:
    if abs(p.wire_line_direction_y) <= 1.0e-12:
        raise ValueError("P19 short-tail wire line may not be vertical in Y")
    u = (y - p.wire_line_point_y) / p.wire_line_direction_y
    return p.wire_line_point_z + u * p.wire_line_direction_z


def _x_hex_prism(across_flats: float, length: float, x: float, y: float = 0.0, z: float = 0.0) -> Shape:
    # RegularPolygon(..., major_radius=False) uses the supplied apothem. For a
    # hexagon, apothem equals across-flats / 2.
    with BuildPart() as part:
        with BuildSketch(Plane.YZ):
            RegularPolygon(
                across_flats / 2.0,
                6,
                major_radius=False,
                align=(Align.CENTER, Align.CENTER),
            )
        extrude(amount=length / 2.0, both=True)
    return Pos(x, y, z) * part.part


def _slot_capsule_cutter(points: tuple[PointYZ, ...], width: float, length_x: float) -> Shape:
    cutters: list[Shape] = []
    for point in points:
        cutters.append(_x_cylinder(width, length_x, 0.0, point.y, point.z))
    for first, second in zip(points, points[1:]):
        dy = second.y - first.y
        dz = second.z - first.z
        length = hypot(dy, dz)
        if length <= 1.0e-9:
            continue
        angle = degrees(atan2(dz, dy))
        bridge = Pos(0.0, (first.y + second.y) / 2.0, (first.z + second.z) / 2.0) * Rot(angle, 0.0, 0.0) * Box(
            length_x,
            length,
            width,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        cutters.append(bridge)
    result = cutters[0]
    for cutter in cutters[1:]:
        result = result + cutter
    return result


def _plate_blank(
    diameter: float,
    thickness: float,
    label: str,
    color: str,
    *,
    bore: Shape,
) -> Shape:
    disk = Cylinder(
        diameter / 2.0,
        thickness,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    part = disk - bore
    return _label(part, label, color)


@lru_cache(maxsize=None)
def _inner_plate_local(side: SideName, p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    center = outer_rotation_center_yz(p)
    axle = fixed_axle_center_yz(p)
    hex_bore = _x_hex_prism(
        p.inner_hex_bore_af,
        p.inner_plate_thickness + 2.0,
        0.0,
        axle.y - center.y,
        axle.z - center.z,
    )
    part = _plate_blank(
        p.inner_plate_diameter,
        p.inner_plate_thickness,
        f"{side}_inner_fixed_guide_hex_keyed_to_center_axle",
        "#D89A19",
        bore=hex_bore,
    )
    for name in ROD_NAMES:
        part = part - _slot_capsule_cutter(fixed_guide_local_locus(name, p), p.fixed_slot_width, p.inner_plate_thickness + 2.0)
    part.label = f"{side}_inner_fixed_guide_hex_keyed_three_straight_closed_tracks"
    return part


@lru_cache(maxsize=None)
def _outer_plate_local(side: SideName, p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    diameter = (
        p.left_outer_secondary_grip_diameter
        if side == "left"
        else p.right_outer_primary_grip_diameter
    )
    label = "left_outer_secondary_cam_mirrored_fixed_axle_guide" if side == "left" else "right_outer_primary_actuator_larger_mirrored_fixed_axle_guide"
    color = "#377A3A" if side == "left" else "#2D6FA8"
    axle_guide = _slot_capsule_cutter(
        fixed_axle_guide_locus(side, p),
        p.fixed_axle_guide_slot_width,
        p.outer_plate_thickness + 2.0,
    )
    part = _plate_blank(
        diameter,
        p.outer_plate_thickness,
        label,
        color,
        bore=axle_guide,
    )
    for name in ROD_NAMES:
        part = part - _slot_capsule_cutter(outer_slot_locus(side, name, p), p.outer_slot_width, p.outer_plate_thickness + 2.0)
    part.label = label
    return part


def build_inner_plate(side: SideName, p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    x = p.left_inner_x if side == "left" else p.right_inner_x
    pivot = outer_rotation_center_yz(p)
    return _label(
        Pos(x, pivot.y, pivot.z) * copy(_inner_plate_local(side, p)),
        _inner_plate_local(side, p).label,
        "#D89A19",
    )


def build_outer_plate(side: SideName, theta_deg: float, p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    x = p.left_outer_x if side == "left" else p.right_outer_x
    color = "#377A3A" if side == "left" else "#2D6FA8"
    pivot = outer_rotation_center_yz(p)
    return _label(
        Pos(x, pivot.y, pivot.z) * Rot(rotation_for_side(side, theta_deg), 0.0, 0.0) * copy(_outer_plate_local(side, p)),
        _outer_plate_local(side, p).label,
        color,
    )


def build_center_axle(p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    pivot = fixed_axle_center_yz(p)
    central = _x_hex_prism(p.center_axle_central_hex_af, p.inner_clear_span, 0.0, pivot.y, pivot.z)
    left_key = _x_hex_prism(
        p.center_axle_inner_hex_af,
        p.inner_plate_thickness,
        -(p.inner_clear_span / 2.0 + p.inner_plate_thickness / 2.0), pivot.y, pivot.z,
    )
    right_key = _x_hex_prism(
        p.center_axle_inner_hex_af,
        p.inner_plate_thickness,
        p.inner_clear_span / 2.0 + p.inner_plate_thickness / 2.0, pivot.y, pivot.z,
    )
    journal_len = p.journal_with_keeper_seat_length
    left_journal = _x_cylinder(
        p.outer_journal_diameter,
        journal_len,
        -(p.inner_clear_span / 2.0 + p.inner_plate_thickness + journal_len / 2.0),
        pivot.y,
        pivot.z,
    )
    right_journal = _x_cylinder(
        p.outer_journal_diameter,
        journal_len,
        p.inner_clear_span / 2.0 + p.inner_plate_thickness + journal_len / 2.0,
        pivot.y,
        pivot.z,
    )
    axle = central + left_key + right_key + left_journal + right_journal
    return _label(
        axle,
        "stepped_center_axle_one_piece_hex_spacer_hex_keys_round_journals_no_outer_coupling",
        "#5B4B8A",
    )


def _keeper_local(p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    # D05 print-ready retained lobe: OD10 / bore7.55 gives 1.225 mm radial wall.
    keeper = _x_cylinder(p.keeper_outer_diameter, p.outer_keeper_thickness, 0.0, 0.0, 0.0)
    bore = _x_cylinder(p.keeper_bore_diameter, p.outer_keeper_thickness + 1.0, 0.0, 0.0, 0.0)
    return keeper - bore


def build_keeper(side: SideName, p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    x = p.keeper_left_x if side == "left" else p.keeper_right_x
    pivot = fixed_axle_center_yz(p)
    keeper = Pos(x, pivot.y, pivot.z) * _keeper_local(p)
    return _label(
        keeper,
        f"{side}_permanent_press_fit_outer_keeper_on_real_seat_clearance_{p.keeper_axial_running_clearance:.2f}",
        "#111111",
    )


def build_rod(name: RodName, theta_deg: float, p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    center = rod_center(name, theta_deg, p)
    return _label(
        _x_cylinder(p.rod_diameter, p.rod_length_target, 0.0, center.y, center.z),
        f"{name}_OD4_rod_L{p.rod_length_target:.2f}",
        "#B7B7B7",
    )


def _cap_local(
    p: P19R1Parameters = P19_R1_DEFAULTS,
    *,
    socket_id: float | None = None,
    engagement_depth: float | None = None,
    socket_open_side: Literal[-1, 1] = 1,
) -> Shape:
    socket_id = p.cap_socket_id if socket_id is None else socket_id
    retention_depth = (
        p.cap_retention_depth if engagement_depth is None else engagement_depth
    )
    total_engagement = p.cap_sliding_guide_depth + retention_depth
    head_length = max(
        p.follower_head_length, total_engagement + p.cap_closed_end_wall
    )
    head = Cylinder(
        p.follower_head_diameter / 2.0,
        head_length,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    guide_depth = p.cap_sliding_guide_depth
    # Overshoot only the open face. The blind end remains exactly controlled by
    # ``cap_closed_end_wall`` rather than being accidentally thinned by a
    # symmetric cutter overshoot.
    guide_center_x = socket_open_side * (
        head_length / 2.0 + 0.05 - guide_depth / 2.0
    )
    guide = _x_cylinder(
        p.cap_sliding_guide_id,
        guide_depth + 0.10,
        guide_center_x,
        0.0,
        0.0,
    )
    cutters: list[Shape] = [guide]
    if retention_depth > 1.0e-9:
        retention_center_x = socket_open_side * (
            head_length / 2.0 - guide_depth - retention_depth / 2.0
        )
        cutters.append(
            _x_cylinder(
                socket_id,
                retention_depth,
                retention_center_x,
                0.0,
                0.0,
            )
        )
    cap = head - cutters
    return _label(
        cap,
        "permanent_follower_cap_stepped_blind_socket_ID4p15x4p70_ID4p04x4p00",
        "#1D1D1F",
    )


def build_cap(side: SideName, name: RodName, theta_deg: float, p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    center = rod_center(name, theta_deg, p)
    if side == "left":
        x = p.left_cap_inner_face_x - p.follower_head_length / 2.0
        socket_open_side: Literal[-1, 1] = 1
    else:
        x = p.right_cap_inner_face_x + p.follower_head_length / 2.0
        socket_open_side = -1
    cap = Pos(x, center.y, center.z) * copy(_cap_local(p, socket_open_side=socket_open_side))
    cap.label = f"{side}_{name}_permanent_follower_cap"
    return cap


def build_xt60_reference(p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    body = Pos(0.0, p.xt60_body_center_y, p.xt60_body_center_z) * Box(
        p.xt60_body_width_x,
        p.xt60_body_y,
        p.xt60_body_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return _label(body, "reference_only_XT60_body_envelope_not_load_path", "#C8E6FF")


def build_workpiece_reference(theta_deg: float, p: P19R1Parameters = P19_R1_DEFAULTS) -> Shape:
    """Two short-tail wire envelopes on the accepted END-derived diagonal."""
    wires: list[Shape] = []
    first = PointYZ(p.wire_model_start_y, wire_line_z_at_y(p.wire_model_start_y, p))
    second = PointYZ(p.wire_model_end_y, wire_line_z_at_y(p.wire_model_end_y, p))
    for x in (-3.60, 3.60):
        wires.append(_yz_line_cylinder(p.wire_envelope_diameter, first, second, x))
    workpiece = wires[0] + wires[1]
    workpiece.label = (
        f"reference_short_ESC_tail_wire_envelopes_theta_{theta_deg:.3f}_not_load_path"
    )
    workpiece.color = srgb("#F1C84B", 0.45)
    return workpiece


def completed_pigtail_removal_waypoints(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> tuple[ServicePose, ...]:
    """D10-R1 service path rederived for the head-up/tail-right workpiece."""
    del p
    return SERVICE_WAYPOINTS


@lru_cache(maxsize=8)
def _completed_pigtail_seated(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> Compound:
    """One cached final pigtail solid; service states are rigid transforms."""
    body = build_xt60_reference(p)
    body.label = "completed_pigtail_XT60_body"
    wires = build_workpiece_reference(0.0, p)
    wires.label = "completed_pigtail_two_separated_bent_wires"
    parts: list[Shape] = [body, wires]
    joint_center_y = p.solder_tool_min_y + 3.00
    joint_direction_span_y = 4.0 * p.wire_line_direction_y
    joint_direction_span_z = 4.0 * p.wire_line_direction_z
    joint_center = PointYZ(joint_center_y, wire_line_z_at_y(joint_center_y, p))
    for x in (-3.60, 3.60):
        joint = _yz_line_cylinder(
            6.00,
            PointYZ(
                joint_center.y - joint_direction_span_y / 2.0,
                joint_center.z - joint_direction_span_z / 2.0,
            ),
            PointYZ(
                joint_center.y + joint_direction_span_y / 2.0,
                joint_center.z + joint_direction_span_z / 2.0,
            ),
            x,
        )
        joint.label = f"completed_pigtail_solder_joint_x_{x:+.2f}"
        parts.append(joint)
    return Compound(children=parts, label="completed_pigtail_seated_actual_envelope")


def _completed_pigtail_at(
    pose: ServicePose,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> Shape:
    """Final actual body, two solder joints and two bent wires at one pose."""
    features = _completed_pigtail_features_at(pose, p)
    return _label(
        Compound(children=list(features.values())),
        (
            "completed_pigtail_actual_service_pose_"
            f"dy_{pose.delta_y:.3f}_dz_{pose.delta_z:.3f}_phi_{pose.phi_deg:.3f}"
        ),
        "#73A6FF",
    )


def _completed_pigtail_features_at(
    pose: ServicePose,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, Shape]:
    """Return separately transformed finite solids for pairwise evidence."""
    seated = _completed_pigtail_seated(p)
    transform = (
        Pos(0.0, pose.delta_y, pose.delta_z)
        * Pos(0.0, p.xt60_body_center_y, p.xt60_body_center_z)
        * Rot(pose.phi_deg, 0.0, 0.0)
        * Pos(0.0, -p.xt60_body_center_y, -p.xt60_body_center_z)
    )
    features: dict[str, Shape] = {
        "xt60Body": transform * seated.children[0],
        "solderJointMinus": transform * seated.children[2],
        "solderJointPlus": transform * seated.children[3],
    }
    for index, wire in enumerate(seated.children[1].solids()):
        features[f"bentWire{index}"] = transform * wire
    for name, shape in features.items():
        shape.label = f"completed_pigtail_{name}"
    return features


def completed_pigtail_removal_states(
    p: P19R1Parameters = P19_R1_DEFAULTS,
    *,
    samples_per_segment: int = 81,
) -> tuple[tuple[str, Shape], ...]:
    """Actual-solid samples of the revalidated D10 pose interpolation."""
    if samples_per_segment < 2:
        raise ValueError("service path needs at least two samples per segment")
    waypoints = completed_pigtail_removal_waypoints(p)
    rows: list[tuple[str, Shape]] = []
    sample_index = 0
    for segment_index, (first, second) in enumerate(zip(waypoints, waypoints[1:])):
        divisions = samples_per_segment - 1
        for index in range(samples_per_segment):
            if segment_index and index == 0:
                continue
            u = index / divisions
            pose = ServicePose(
                first.delta_y + (second.delta_y - first.delta_y) * u,
                first.delta_z + (second.delta_z - first.delta_z) * u,
                first.phi_deg + (second.phi_deg - first.phi_deg) * u,
            )
            rows.append(
                (
                    f"segment_{segment_index}_sample_{index:04d}_global_{sample_index:04d}",
                    _completed_pigtail_at(pose, p),
                )
            )
            sample_index += 1
    return tuple(rows)


def build_completed_pigtail_removal_sweep(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> Compound:
    children = [shape for _, shape in completed_pigtail_removal_states(p)]
    return Compound(
        children=children,
        label="completed_pigtail_actual_D10_R1_rigid_body_removal_sweep",
    )


def build_service_envelopes(theta_deg: float, p: P19R1Parameters = P19_R1_DEFAULTS) -> Compound:
    """Short-tail solder, tool and outgoing-wire service references."""
    shapes: list[Shape] = []
    tool_center_y = p.solder_tool_min_y + p.solder_tool_size_yz / 2.0
    tool_center_z = wire_line_z_at_y(tool_center_y, p)
    joint_center_y = p.solder_tool_min_y + 3.0
    joint_center = PointYZ(joint_center_y, wire_line_z_at_y(joint_center_y, p))
    for x in (-3.60, 3.60):
        solder = _yz_line_cylinder(
            5.50,
            PointYZ(
                joint_center.y - 2.0 * p.wire_line_direction_y,
                joint_center.z - 2.0 * p.wire_line_direction_z,
            ),
            PointYZ(
                joint_center.y + 2.0 * p.wire_line_direction_y,
                joint_center.z + 2.0 * p.wire_line_direction_z,
            ),
            x,
        )
        solder.label = f"reference_solder_joint_x_{x:+.2f}"
        solder.color = srgb("#E36B4A", 0.24)
        tool = Pos(x, tool_center_y, tool_center_z) * Box(
            p.solder_tool_depth_x,
            p.solder_tool_size_yz,
            p.solder_tool_size_yz,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        tool.label = f"reference_soldering_tool_keepout_x_{x:+.2f}"
        tool.color = srgb("#9C6ADE", 0.08)
        shapes.extend((solder, tool))
    return Compound(children=shapes, label=f"reference_service_envelopes_theta_{theta_deg:.1f}")


def build_motion_state(state: StateName, p: P19R1Parameters = P19_R1_DEFAULTS) -> Compound:
    theta = STATE_THETA[state]
    children: list[Shape] = [
        build_center_axle(p),
        build_keeper("left", p),
        build_keeper("right", p),
        build_inner_plate("left", p),
        build_inner_plate("right", p),
        build_outer_plate("left", theta, p),
        build_outer_plate("right", theta, p),
        build_xt60_reference(p),
        build_workpiece_reference(theta, p),
        build_service_envelopes(theta, p),
    ]
    for name in ROD_NAMES:
        children.append(build_rod(name, theta, p))
        children.append(build_cap("left", name, theta, p))
        children.append(build_cap("right", name, theta, p))
    return Compound(children=children, label=f"P19_R1_{state}_direct_counter_twist_center_axle")


def build_exploded(p: P19R1Parameters = P19_R1_DEFAULTS) -> Compound:
    parts = [
        Pos(-4 * p.exploded_spacing_x, 0, 0) * build_outer_plate("left", 0.0, p),
        Pos(-3 * p.exploded_spacing_x, 0, 0) * build_keeper("left", p),
        Pos(-2 * p.exploded_spacing_x, 0, 0) * build_inner_plate("left", p),
        Pos(0, 0, 0) * build_center_axle(p),
        Pos(2 * p.exploded_spacing_x, 0, 0) * build_inner_plate("right", p),
        Pos(3 * p.exploded_spacing_x, 0, 0) * build_keeper("right", p),
        Pos(4 * p.exploded_spacing_x, 0, 0) * build_outer_plate("right", p.theta_end_deg, p),
    ]
    for idx, name in enumerate(ROD_NAMES):
        parts.append(Pos(0, -44, idx * 9 - 9) * build_rod(name, 0.0, p))
        parts.append(Pos(-24, -58, idx * 9 - 9) * build_cap("left", name, 0.0, p))
        parts.append(Pos(24, -58, idx * 9 - 9) * build_cap("right", name, 0.0, p))
    return Compound(children=parts, label="P19_R1_exploded_all_production_parts")


def _lay_flat(shape: Shape) -> Shape:
    return Rot(0.0, -90.0, 0.0) * shape


def _center_on_bed(shape: Shape) -> Shape:
    bounds = shape.bounding_box()
    return Pos(
        -(bounds.min.X + bounds.max.X) / 2.0,
        -(bounds.min.Y + bounds.max.Y) / 2.0,
        -bounds.min.Z,
    ) * shape


def build_print_kit(p: P19R1Parameters = P19_R1_DEFAULTS) -> Compound:
    children: list[Shape] = []
    kit_parts = [
        _lay_flat(copy(_inner_plate_local("left", p))),
        _lay_flat(copy(_inner_plate_local("right", p))),
        _lay_flat(copy(_outer_plate_local("left", p))),
        _lay_flat(copy(_outer_plate_local("right", p))),
        build_center_axle(p),
        _lay_flat(_label(_keeper_local(p), f"left_permanent_press_fit_outer_keeper_on_real_seat_clearance_{p.keeper_axial_running_clearance:.2f}", "#111111")),
        _lay_flat(_label(_keeper_local(p), f"right_permanent_press_fit_outer_keeper_on_real_seat_clearance_{p.keeper_axial_running_clearance:.2f}", "#111111")),
    ]
    positions = [(-78, 42), (-22, 42), (42, 42), (108, 42), (-56, -28), (10, -28), (26, -28)]
    for shape, (x, y) in zip(kit_parts, positions):
        placed = Pos(x, y, 0) * _center_on_bed(shape)
        label = f"print_{shape.label}"
        color = "#D89A19"
        if "left_outer" in label:
            color = "#377A3A"
        elif "right_outer" in label:
            color = "#2D6FA8"
        elif "stepped_center_axle" in label:
            color = "#5B4B8A"
        elif "keeper" in label:
            color = "#111111"
        children.append(_label(placed, label, color))
    for idx, name in enumerate(ROD_NAMES):
        for side_index, side in enumerate(("left", "right")):
            cap = Pos(-34 + idx * 14 + side_index * 82, -78, 0) * _center_on_bed(
                _lay_flat(copy(_cap_local(p, socket_open_side=1)))
            )
            cap.label = f"print_{side}_{name}_permanent_cap"
            children.append(cap)
    return Compound(children=children, label="P19_R1_print_kit_printed_parts_only_no_rods")


def build_permanent_cap_coupon(p: P19R1Parameters = P19_R1_DEFAULTS) -> Compound:
    children: list[Shape] = []
    for row, depth in enumerate(p.cap_socket_ladder_depths):
        for col, diameter in enumerate(p.cap_socket_ladder_ids):
            cap = Pos((col - 2) * 12.0, (row - 1) * 14.0, 0.0) * _cap_local(
                p,
                socket_id=diameter,
                engagement_depth=depth,
            )
            cap.label = f"coupon_permanent_cap_ID{diameter:.2f}_depth{depth:.2f}".replace(".", "p")
            children.append(cap)
    base = Pos(0.0, 0.0, -3.0) * Box(62.0, 40.0, 1.2, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    base.label = "coupon_label_base_P19_R1_permanent_cap_ladder"
    children.append(base)
    children.append(Pos(0.0, 62.0, 0.0) * build_slot_fit_coupon(p))
    return Compound(children=children, label="P19_R1_permanent_cap_coupon_ID_ladder")


def build_slot_fit_coupon(p: P19R1Parameters = P19_R1_DEFAULTS) -> Compound:
    """Straight and representative curved PETG slot ladders for OD4 rods."""
    children: list[Shape] = []
    straight = (PointYZ(-7.0, 0.0), PointYZ(7.0, 0.0))
    curved = (
        PointYZ(-7.0, 0.0),
        PointYZ(-3.5, 0.8),
        PointYZ(0.0, 2.0),
        PointYZ(3.5, 0.8),
        PointYZ(7.0, 0.0),
    )
    for index, width in enumerate(p.slot_fit_coupon_widths):
        for form_index, (form, locus) in enumerate((('straight', straight), ('curved', curved))):
            blank = Box(
                p.inner_plate_thickness,
                20.0,
                10.0,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            )
            coupon = blank - _slot_capsule_cutter(locus, width, p.inner_plate_thickness + 2.0)
            coupon = Pos((index - 2) * 24.0, (form_index - 0.5) * 14.0, 0.0) * _center_on_bed(_lay_flat(coupon))
            coupon.label = f"slot_fit_{form}_OD4_width_{width:.2f}".replace('.', 'p')
            children.append(coupon)
    return Compound(children=children, label="P19_R1_slot_fit_coupon_straight_and_curved_4p10_to_4p30")


def build_center_axle_coupon(p: P19R1Parameters = P19_R1_DEFAULTS) -> Compound:
    axle = Pos(-18, 0, 0) * build_center_axle(p)
    outer_ring = _x_cylinder(p.outer_bearing_bore_diameter, p.outer_plate_thickness, 18, 0, 0) - _x_cylinder(
        p.outer_journal_diameter, p.outer_plate_thickness + 1.0, 18, 0, 0
    )
    outer_ring = _label(outer_ring, "coupon_outer_round_bearing_bore_clearance_0p30", "#2D6FA8")
    hex_ring = _x_hex_prism(p.inner_hex_bore_af, p.inner_plate_thickness, 42) - _x_hex_prism(
        p.center_axle_inner_hex_af, p.inner_plate_thickness + 1.0, 42
    )
    hex_ring = _label(hex_ring, "coupon_inner_hex_key_fit_clearance_0p15", "#D89A19")
    children: list[Shape] = [axle, outer_ring, hex_ring]
    for index, bore_diameter in enumerate(p.keeper_coupon_bore_diameters):
        y = -28.0 + index * 14.0
        ring = _x_cylinder(p.keeper_outer_diameter, p.outer_keeper_thickness, 62, y, 0) - _x_cylinder(
            bore_diameter,
            p.outer_keeper_thickness + 1.0,
            62,
            y,
            0,
        )
        ring = _label(
            ring,
            f"coupon_keeper_OD10p00_bore_{bore_diameter:.2f}".replace(".", "p"),
            "#111111",
        )
        seat = _label(
            _x_cylinder(p.outer_journal_diameter, 5.0, 70, y, 0),
            f"coupon_keeper_seat_OD{p.outer_journal_diameter:.2f}".replace(".", "p"),
            "#5B4B8A",
        )
        children.extend((ring, seat))
    return Compound(
        children=children,
        label="P19_R1_center_axle_bearing_hex_keeper_retention_coupon_ladder",
    )


def build_artifact(name: ArtifactName, p: P19R1Parameters = P19_R1_DEFAULTS) -> Compound:
    builders = {
        "open": lambda: build_motion_state("open", p),
        "mid": lambda: build_motion_state("mid", p),
        "contact": lambda: build_motion_state("contact", p),
        "end": lambda: build_motion_state("end", p),
        "exploded": lambda: build_exploded(p),
        "print_kit": lambda: build_print_kit(p),
        "permanent_cap_coupon": lambda: build_permanent_cap_coupon(p),
        "center_axle_coupon": lambda: build_center_axle_coupon(p),
    }
    if name not in builders:
        raise ValueError(f"unknown P19 R1 artifact {name!r}")
    artifact = builders[name]()
    return Compound(children=[artifact], label=f"P19_R1_ARTIFACT_{name}__{provenance_token(p)}")


def _intersection_volume(first: Shape, second: Shape) -> float:
    common = first.intersect(second)
    if common is None:
        return 0.0
    if hasattr(common, "volume"):
        return float(common.volume)
    return sum(float(item.volume) for item in common)


def _service_pose_samples(samples_per_segment: int) -> tuple[tuple[int, int, ServicePose], ...]:
    if samples_per_segment < 2:
        raise ValueError("service path needs at least two samples per segment")
    rows: list[tuple[int, int, ServicePose]] = []
    for segment_index, (first, second) in enumerate(
        zip(SERVICE_WAYPOINTS, SERVICE_WAYPOINTS[1:])
    ):
        divisions = samples_per_segment - 1
        for sample_index in range(samples_per_segment):
            u = sample_index / divisions
            rows.append(
                (
                    segment_index,
                    sample_index,
                    ServicePose(
                        first.delta_y + (second.delta_y - first.delta_y) * u,
                        first.delta_z + (second.delta_z - first.delta_z) * u,
                        first.phi_deg + (second.phi_deg - first.phi_deg) * u,
                    ),
                )
            )
    return tuple(rows)


def _inverse_service_point(
    point: PointYZ,
    pose: ServicePose,
    p: P19R1Parameters,
) -> PointYZ:
    """Map one stationary world-YZ point into the seated pigtail frame."""
    dy = point.y - pose.delta_y - p.xt60_body_center_y
    dz = point.z - pose.delta_z - p.xt60_body_center_z
    angle = radians(-pose.phi_deg)
    return PointYZ(
        p.xt60_body_center_y + dy * cos(angle) - dz * sin(angle),
        p.xt60_body_center_z + dy * sin(angle) + dz * cos(angle),
    )


def _point_rectangle_distance_yz(
    point: PointYZ,
    center: PointYZ,
    half_y: float,
    half_z: float,
) -> float:
    return hypot(
        max(abs(point.y - center.y) - half_y, 0.0),
        max(abs(point.z - center.z) - half_z, 0.0),
    )


def _pigtail_feature_clearances_to_x_member(
    local_center: PointYZ,
    member_radius: float,
    p: P19R1Parameters,
) -> dict[str, float]:
    """Exact YZ feature-envelope gaps where the member overlaps in X."""
    body = (
        _point_rectangle_distance_yz(
            local_center,
            PointYZ(p.xt60_body_center_y, p.xt60_body_center_z),
            p.xt60_body_y / 2.0,
            p.xt60_body_z / 2.0,
        )
        - member_radius
    )
    body_bottom_z = p.xt60_body_center_z - p.xt60_body_z / 2.0
    joint_first = PointYZ(p.xt60_body_center_y, body_bottom_z)
    joint_second = PointYZ(p.xt60_body_center_y, body_bottom_z + 4.0)
    joints = (
        _point_segment_distance_yz(local_center, joint_first, joint_second)
        - 3.0
        - member_radius
    )
    wires = (
        min(_wire_feature_offset(name, local_center, p) for name in ROD_NAMES)
        - p.wire_envelope_diameter / 2.0
        - member_radius
    )
    return {"xt60Body": body, "solderJoints": joints, "twoBentWires": wires}


def _open_production_solids(
    p: P19R1Parameters,
) -> dict[str, Shape]:
    solids: dict[str, Shape] = {
        "centerAxle": build_center_axle(p),
        "leftKeeper": build_keeper("left", p),
        "rightKeeper": build_keeper("right", p),
        "leftInnerPlate": build_inner_plate("left", p),
        "rightInnerPlate": build_inner_plate("right", p),
        "leftOuterPlate": build_outer_plate("left", 0.0, p),
        "rightOuterPlate": build_outer_plate("right", 0.0, p),
    }
    for name in ROD_NAMES:
        solids[f"{name}Rod"] = build_rod(name, 0.0, p)
        solids[f"left{name.title()}Cap"] = build_cap("left", name, 0.0, p)
        solids[f"right{name.title()}Cap"] = build_cap("right", name, 0.0, p)
    return solids


@lru_cache(maxsize=8)
def _completed_pigtail_service_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """Pairwise finite-solid and dense analytic rigid-removal proof."""
    production = _open_production_solids(p)
    x_members: dict[str, tuple[PointYZ, float]] = {
        **{
            f"{name}Rod": (GUIDES[name].open, p.rod_diameter / 2.0)
            for name in ROD_NAMES
        },
        "centerAxle": (
            fixed_axle_center_yz(p),
            p.center_axle_central_hex_af / sqrt(3.0),
        ),
    }
    wire_first = PointYZ(
        p.wire_model_start_y,
        wire_line_z_at_y(p.wire_model_start_y, p),
    )
    wire_second = PointYZ(
        p.wire_model_end_y,
        wire_line_z_at_y(p.wire_model_end_y, p),
    )
    joint_center_y = p.solder_tool_min_y + 3.0
    joint_center = PointYZ(
        joint_center_y,
        wire_line_z_at_y(joint_center_y, p),
    )
    joint_first = PointYZ(
        joint_center.y - 2.0 * p.wire_line_direction_y,
        joint_center.z - 2.0 * p.wire_line_direction_z,
    )
    joint_second = PointYZ(
        joint_center.y + 2.0 * p.wire_line_direction_y,
        joint_center.z + 2.0 * p.wire_line_direction_z,
    )

    analytic_pair_minima: dict[str, dict[str, object]] = {}
    analytic_rows: dict[str, object] = {}
    analytic_minimum = float("inf")
    analytic_limiting: dict[str, object] | None = None
    analytic_samples_per_segment = 1001
    for segment_index, sample_index, pose in _service_pose_samples(
        analytic_samples_per_segment
    ):
        pose_key = f"segment_{segment_index}:sample_{sample_index:04d}"
        pose_minimum = float("inf")
        pose_limiting_pair = ""
        for production_name, (center, radius) in x_members.items():
            local = _inverse_service_point(center, pose, p)
            clearances = {
                "xt60Body": (
                    _point_rectangle_distance_yz(
                        local,
                        PointYZ(p.xt60_body_center_y, p.xt60_body_center_z),
                        p.xt60_body_y / 2.0,
                        p.xt60_body_z / 2.0,
                    )
                    - radius
                ),
                "bentWire0": (
                    _point_segment_distance_yz(local, wire_first, wire_second)
                    - p.wire_envelope_diameter / 2.0
                    - radius
                ),
                "bentWire1": (
                    _point_segment_distance_yz(local, wire_first, wire_second)
                    - p.wire_envelope_diameter / 2.0
                    - radius
                ),
                "solderJointMinus": (
                    _point_segment_distance_yz(local, joint_first, joint_second)
                    - 3.0
                    - radius
                ),
                "solderJointPlus": (
                    _point_segment_distance_yz(local, joint_first, joint_second)
                    - 3.0
                    - radius
                ),
            }
            for feature_name, clearance in clearances.items():
                pair_name = f"{feature_name}::{production_name}"
                previous = analytic_pair_minima.get(pair_name)
                if previous is None or clearance < previous["clearanceMm"]:
                    analytic_pair_minima[pair_name] = {
                        "clearanceMm": clearance,
                        "pose": (pose.delta_y, pose.delta_z, pose.phi_deg),
                        "segmentIndex": segment_index,
                        "sampleIndex": sample_index,
                    }
                if clearance < pose_minimum:
                    pose_minimum = clearance
                    pose_limiting_pair = pair_name
                if clearance < analytic_minimum:
                    analytic_minimum = clearance
                    analytic_limiting = {
                        "pigtailFeature": feature_name,
                        "productionSolid": production_name,
                        "pose": (pose.delta_y, pose.delta_z, pose.phi_deg),
                        "segmentIndex": segment_index,
                        "sampleIndex": sample_index,
                        "clearanceMm": clearance,
                    }
        analytic_rows[pose_key] = {
            "clearanceMm": pose_minimum,
            "limitingPair": pose_limiting_pair,
        }

    # Every remaining production obstacle is separated in X from every
    # pigtail feature.  The exact bounding-box X gap is a conservative lower
    # bound on full 3D solid distance and is invariant under the YZ motion.
    seated_features = _completed_pigtail_features_at(ServicePose(0.0, 0.0, 0.0), p)
    for feature_name, feature in seated_features.items():
        feature_box = feature.bounding_box()
        for production_name, obstacle in production.items():
            if production_name in x_members:
                continue
            obstacle_box = obstacle.bounding_box()
            x_gap = max(
                obstacle_box.min.X - feature_box.max.X,
                feature_box.min.X - obstacle_box.max.X,
                0.0,
            )
            pair_name = f"{feature_name}::{production_name}"
            analytic_pair_minima[pair_name] = {
                "clearanceMm": x_gap,
                "pose": "all",
                "proof": "exact invariant bounding-box X separation lower bound",
            }
            if x_gap < analytic_minimum:
                analytic_minimum = x_gap
                analytic_limiting = {
                    "pigtailFeature": feature_name,
                    "productionSolid": production_name,
                    "pose": "all",
                    "clearanceMm": x_gap,
                }

    brep_samples_per_segment = 41
    brep_minimum = float("inf")
    brep_rows: dict[str, object] = {}
    brep_pair_minima: dict[str, dict[str, object]] = {}
    maximum_intersection = 0.0
    maximum_intersection_pair: dict[str, object] | None = None
    brep_limiting: dict[str, object] | None = None
    for segment_index, sample_index, pose in _service_pose_samples(
        brep_samples_per_segment
    ):
        features = _completed_pigtail_features_at(pose, p)
        pose_minimum = float("inf")
        pose_limiting_pair = ""
        pose_limiting_intersection = 0.0
        for feature_name, feature in features.items():
            feature_box = feature.bounding_box()
            for production_name, obstacle in production.items():
                obstacle_box = obstacle.bounding_box()
                x_gap = max(
                    obstacle_box.min.X - feature_box.max.X,
                    feature_box.min.X - obstacle_box.max.X,
                    0.0,
                )
                if x_gap + 1.0e-12 >= p.service_clearance_min:
                    clearance = x_gap
                    intersection = 0.0
                    distance_kind = "exact invariant X-separation lower bound"
                else:
                    clearance = float(feature.distance(obstacle))
                    intersection = (
                        _intersection_volume(feature, obstacle)
                        if clearance <= 1.0e-8
                        else 0.0
                    )
                    distance_kind = "actual BREP pair distance"
                pair_name = f"{feature_name}::{production_name}"
                previous = brep_pair_minima.get(pair_name)
                if previous is None or clearance < previous["clearanceMm"]:
                    brep_pair_minima[pair_name] = {
                        "clearanceMm": clearance,
                        "intersectionMm3": intersection,
                        "distanceKind": distance_kind,
                        "pose": (pose.delta_y, pose.delta_z, pose.phi_deg),
                        "segmentIndex": segment_index,
                        "sampleIndex": sample_index,
                    }
                if clearance < pose_minimum:
                    pose_minimum = clearance
                    pose_limiting_pair = pair_name
                    pose_limiting_intersection = intersection
                if clearance < brep_minimum:
                    brep_minimum = clearance
                    brep_limiting = {
                        "pigtailFeature": feature_name,
                        "productionSolid": production_name,
                        "pose": (pose.delta_y, pose.delta_z, pose.phi_deg),
                        "segmentIndex": segment_index,
                        "sampleIndex": sample_index,
                        "clearanceMm": clearance,
                        "intersectionMm3": intersection,
                        "distanceKind": distance_kind,
                    }
                if intersection > maximum_intersection:
                    maximum_intersection = intersection
                    maximum_intersection_pair = {
                        "pigtailFeature": feature_name,
                        "productionSolid": production_name,
                        "pose": (pose.delta_y, pose.delta_z, pose.phi_deg),
                        "segmentIndex": segment_index,
                        "sampleIndex": sample_index,
                        "clearanceMm": clearance,
                        "intersectionMm3": intersection,
                    }
        key = f"segment_{segment_index}:sample_{sample_index:04d}"
        brep_rows[key] = {
            "clearanceMm": pose_minimum,
            "limitingPair": pose_limiting_pair,
            "intersectionMm3": pose_limiting_intersection,
        }
    minimum = min(brep_minimum, analytic_minimum)
    segment_count = len(SERVICE_WAYPOINTS) - 1
    return {
        "pathId": "P19-R1-rigid-removal",
        "waypoints": tuple(
            (pose.delta_y, pose.delta_z, pose.phi_deg) for pose in SERVICE_WAYPOINTS
        ),
        "interpolation": "piecewise-linear in dy,dz,phi_deg",
        "searchBounds": {
            "deltaYmm": (-30.0, 30.0),
            "deltaZmm": (-20.0, 50.0),
            "phiDeg": (-90.0, 90.0),
            "gridStep": (2.0, 2.0, 5.0),
            "edgeSubsamples": 5,
            "objective": "minimum-cost practical upward withdrawal",
        },
        "brepSamplesPerSegment": brep_samples_per_segment,
        "brepSampleCount": segment_count * brep_samples_per_segment,
        "brepMinimumClearanceMm": brep_minimum,
        "brepMaximumIntersectionMm3": maximum_intersection,
        "brepLimitingPair": brep_limiting,
        "brepMaximumIntersectionPair": maximum_intersection_pair,
        "brepMinimumByPair": brep_pair_minima,
        "brepRows": brep_rows,
        "analyticSamplesPerSegment": analytic_samples_per_segment,
        "analyticSampleCount": segment_count * analytic_samples_per_segment,
        "analyticMinimumClearanceMm": analytic_minimum,
        "analyticLimitingPair": analytic_limiting,
        "analyticMinimumByPair": analytic_pair_minima,
        "analyticRows": analytic_rows,
        "includedPigtailFeatures": ("XT60 body", "two solder joints", "two bent wires"),
        "includedProductionSolids": tuple(production),
        "minimumClearanceMm": minimum,
        "zeroIntersection": maximum_intersection <= 1.0e-7,
        "passes": maximum_intersection <= 1.0e-7
        and minimum + 1.0e-9 >= p.service_clearance_min,
    }


def service_clearance_evidence(p: P19R1Parameters = P19_R1_DEFAULTS) -> dict[str, object]:
    """Actual-solid pivot service plus the repaired pairwise extraction gate."""
    fixed = {
        "center_axle": build_center_axle(p),
        "left_keeper": build_keeper("left", p),
        "right_keeper": build_keeper("right", p),
    }
    rows: dict[str, object] = {}
    minimum = float("inf")
    for index in range(9):
        theta = index * p.theta_end_deg / 8.0
        state = f"sample_{index:02d}_theta_{theta:.2f}"
        targets = [build_xt60_reference(p), *build_service_envelopes(theta, p).children]
        for fixed_name, solid in fixed.items():
            clearances = [float(solid.distance(target)) for target in targets]
            value = min(clearances)
            minimum = min(minimum, value)
            rows[f"{state}:{fixed_name}"] = {
                "minimumClearanceMm": value,
                "zeroIntersection": all(_intersection_volume(solid, target) <= 1.0e-7 for target in targets),
            }
    removal = _completed_pigtail_service_evidence(p)
    minimum = min(minimum, float(removal["minimumClearanceMm"]))
    return {
        "minimumRequiredMm": p.service_clearance_min,
        "minimumActualMm": minimum,
        "passes": minimum + 1.0e-9 >= p.service_clearance_min,
        "pivotServiceRows": rows,
        "removalSequence": "full open -> repaired four-pose rigid-body removal path",
        "removalWaypoints": removal["waypoints"],
        "removalMinimumActualMm": removal["minimumClearanceMm"],
        "removalZeroIntersection": removal["zeroIntersection"],
        "removalRows": removal["brepRows"],
        "removalEvidence": removal,
        "rows": rows,
    }


def _point_segment_distance_yz(point: PointYZ, first: PointYZ, second: PointYZ) -> float:
    dy = second.y - first.y
    dz = second.z - first.z
    denominator = dy * dy + dz * dz
    if denominator <= 1.0e-18:
        return point.distance_to(first)
    u = max(
        0.0,
        min(
            1.0,
            ((point.y - first.y) * dy + (point.z - first.z) * dz)
            / denominator,
        ),
    )
    nearest = PointYZ(first.y + u * dy, first.z + u * dz)
    return point.distance_to(nearest)


def _segment_distance_yz(
    first_a: PointYZ,
    first_b: PointYZ,
    second_a: PointYZ,
    second_b: PointYZ,
) -> float:
    return min(
        _point_segment_distance_yz(first_a, second_a, second_b),
        _point_segment_distance_yz(first_b, second_a, second_b),
        _point_segment_distance_yz(second_a, first_a, first_b),
        _point_segment_distance_yz(second_b, first_a, first_b),
    )


def _polyline_distance_yz(
    first: tuple[PointYZ, ...], second: tuple[PointYZ, ...]
) -> float:
    return min(
        _segment_distance_yz(a0, a1, b0, b1)
        for a0, a1 in zip(first, first[1:])
        for b0, b1 in zip(second, second[1:])
    )


def _triangle_area(points: tuple[PointYZ, PointYZ, PointYZ]) -> float:
    first, second, third = points
    return abs(
        first.y * (second.z - third.z)
        + second.y * (third.z - first.z)
        + third.y * (first.z - second.z)
    ) / 2.0


def _wire_feature_offset(
    name: RodName,
    center: PointYZ,
    p: P19R1Parameters,
) -> float:
    del name
    return abs(wire_signed_center_distance(center, p))


def wire_normal_yz(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> PointYZ:
    return PointYZ(-p.wire_line_direction_z, p.wire_line_direction_y)


def wire_signed_center_distance(
    center: PointYZ,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> float:
    normal = wire_normal_yz(p)
    return (
        (center.y - p.wire_line_point_y) * normal.y
        + (center.z - p.wire_line_point_z) * normal.z
    )


def wire_surface_clearance(
    center: PointYZ,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> float:
    combined_radius = (p.rod_diameter + p.wire_envelope_diameter) / 2.0
    return abs(wire_signed_center_distance(center, p)) - combined_radius


def first_contact_progress(
    name: RodName,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> float:
    first = wire_signed_center_distance(GUIDES[name].open, p)
    last = wire_signed_center_distance(GUIDES[name].end, p)
    combined_radius = (p.rod_diameter + p.wire_envelope_diameter) / 2.0
    target = combined_radius if first > 0.0 else -combined_radius
    return (target - first) / (last - first)


def theta_contact_deg(p: P19R1Parameters = P19_R1_DEFAULTS) -> float:
    return p.theta_end_deg * min(first_contact_progress(name, p) for name in ROD_NAMES)


def workpiece_orientation_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """Publish the accepted head-up, short-tail-right P19 frame."""
    return {
        "requirementIds": ("REQ-031", "P19-cycle-4"),
        "frontPlane": "world YZ",
        "screenRightAxis": "+Y",
        "screenUpAxis": "+Z",
        "frontViewForm": "XT60 head +Z; short ESC tail/tool +Y",
        "xt60BodyCenterYZ": (
            p.xt60_body_center_y,
            p.xt60_body_center_z,
        ),
        "matingHeadDirection": "+Z",
        "shortTail": {
            "linePointYZ": (p.wire_line_point_y, p.wire_line_point_z),
            "lineDirectionYZ": (
                p.wire_line_direction_y,
                p.wire_line_direction_z,
            ),
            "tailDirection": "+Y/right",
            "modelYRange": (p.wire_model_start_y, p.wire_model_end_y),
        },
        "solderToolKeepout": {
            "minimumY": p.solder_tool_min_y,
            "sizeYZ": p.solder_tool_size_yz,
            "minimumOutsideLargestRimMm": P19_TOOL_KEEP_OUTSIDE_RIM_MM,
        },
        "rodFeatureByIdentity": {
            "bottom": "OPEN upper-left / END upper-left",
            "diagonal": "OPEN upper-right / END middle",
            "upright": "OPEN lower-right / END lower-right",
        },
    }


def triangle_motion_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    state_theta = {
        "open": 0.0,
        "contact": theta_contact_deg(p),
        "end": p.theta_end_deg,
    }
    triangles: dict[str, object] = {}
    for state, theta in state_theta.items():
        points = tuple(
            rod_center(name, theta, p) for name in TRIANGLE_VERTEX_ORDER
        )
        triangles[state] = {
            "centersYZ": {
                name: rod_center(name, theta, p).as_tuple() for name in ROD_NAMES
            },
            "areaMm2": _triangle_area(points),  # type: ignore[arg-type]
            "sideLengthsMm": (
                points[0].distance_to(points[1]),
                points[1].distance_to(points[2]),
                points[2].distance_to(points[0]),
            ),
            "wireFeatureOffsetsMm": {
                name: _wire_feature_offset(name, rod_center(name, theta, p), p)
                for name in ROD_NAMES
            },
        }
    expected_contact = p.rod_diameter / 2.0 + p.wire_envelope_diameter / 2.0
    expected_end = expected_contact - p.wire_preload
    return {
        "requirementIds": ("REQ-028", "REQ-029", "REQ-030"),
        "triangles": triangles,
        "thetaContactDeg": theta_contact_deg(p),
        "thetaEndDeg": p.theta_end_deg,
        "commonStrokeMm": GUIDES["upright"].travel,
        "contactOffsetMm": expected_contact,
        "endOffsetMm": expected_end,
        "linearTravelLaw": "u=theta/theta_end",
        "endpointDerivativeMmPerDeg": GUIDES["upright"].travel / p.theta_end_deg,
        "vertexOrder": TRIANGLE_VERTEX_ORDER,
        "rodVertexRole": ROD_VERTEX_ROLE,
        "openRightVerticalLegDeltaY": abs(
            GUIDES["diagonal"].open.y - GUIDES["upright"].open.y
        ),
        "acceptedEndDisplacementMmByRod": {
            name: motion_state(1.0, p).rod(name).distance_to(GUIDES[name].end)
            for name in ROD_NAMES
        },
        "maximumAcceptedEndDisplacementMm": max(
            motion_state(1.0, p).rod(name).distance_to(GUIDES[name].end)
            for name in ROD_NAMES
        ),
        "rodLengthMm": p.rod_length_target,
        "capEngagementMmPerSide": p.cap_rod_engagement,
        "capLengthMm": p.follower_head_length,
        "nominalDiametralGuidePlayMm": p.fixed_slot_width - p.rod_diameter,
        "nominalAngularWobbleDeg": degrees(
            atan((p.fixed_slot_width - p.rod_diameter) / 21.60)
        ),
        "physicalBoundary": (
            "wire preload is a geometric displacement proxy; force, insulation "
            "response, springback, cap retention and printed fit remain physical"
        ),
    }


def _curve_tangent(
    side: SideName,
    name: RodName,
    theta_deg: float,
    p: P19R1Parameters,
) -> PointYZ:
    step = 1.0e-4
    lower = max(0.0, theta_deg - step)
    upper = min(p.theta_end_deg, theta_deg + step)
    first = outer_slot_local_center(side, name, lower, p)
    second = outer_slot_local_center(side, name, upper, p)
    return PointYZ(second.y - first.y, second.z - first.z)


def _crossing_sine(
    side: SideName,
    name: RodName,
    theta_deg: float,
    p: P19R1Parameters,
) -> float:
    fixed_tangent_local = _rotate_yz(
        GUIDES[name].direction,
        -rotation_for_side(side, theta_deg),
    )
    outer_tangent = _curve_tangent(side, name, theta_deg, p)
    denominator = hypot(fixed_tangent_local.y, fixed_tangent_local.z) * hypot(
        outer_tangent.y, outer_tangent.z
    )
    return abs(
        fixed_tangent_local.y * outer_tangent.z
        - fixed_tangent_local.z * outer_tangent.y
    ) / denominator


def _analytic_outer_rail_derivative(
    side: SideName,
    name: RodName,
    theta_deg: float,
    p: P19R1Parameters,
) -> PointYZ:
    """D10-R1 exact dq/dtheta in millimetres per degree."""
    center = rod_center(name, theta_deg, p)
    relative = PointYZ(
        center.y - p.outer_rotation_center_y,
        center.z - p.outer_rotation_center_z,
    )
    travel_rate = GUIDES[name].travel / p.theta_end_deg
    dr = PointYZ(
        GUIDES[name].direction.y * travel_rate,
        GUIDES[name].direction.z * travel_rate,
    )
    alpha_prime = (-1.0 if side == "left" else 1.0) * pi / 180.0
    j_relative = PointYZ(-relative.z, relative.y)
    pre_rotation = PointYZ(
        dr.y - alpha_prime * j_relative.y,
        dr.z - alpha_prime * j_relative.z,
    )
    return _rotate_yz(
        pre_rotation,
        -rotation_for_side(side, theta_deg),
    )


def rail_branch_regularity_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """D10-R1 rail regularity, one-to-one branch and continuation proof."""
    sample_count = p.validation_sample_count
    sample_thetas = tuple(
        p.theta_end_deg * index / (sample_count - 1)
        for index in range(sample_count)
    )
    rows: dict[str, object] = {}
    minimum_derivative = float("inf")
    minimum_nonadjacent_gap = float("inf")
    for side in ("left", "right"):
        for name in ROD_NAMES:
            derivatives = tuple(
                hypot(
                    _analytic_outer_rail_derivative(side, name, theta, p).y,
                    _analytic_outer_rail_derivative(side, name, theta, p).z,
                )
                for theta in sample_thetas
            )
            locus = tuple(
                outer_slot_local_center(side, name, theta, p)
                for theta in sample_thetas
            )
            branch_gap = min(
                _segment_distance_yz(
                    locus[first],
                    locus[first + 1],
                    locus[second],
                    locus[second + 1],
                )
                for first in range(len(locus) - 1)
                for second in range(first + 2, len(locus) - 1)
            )
            row_min_derivative = min(derivatives)
            minimum_derivative = min(minimum_derivative, row_min_derivative)
            minimum_nonadjacent_gap = min(
                minimum_nonadjacent_gap, branch_gap
            )
            rows[f"{side}:{name}"] = {
                "minimumAnalyticDerivativeMmPerDeg": row_min_derivative,
                "endpointDerivativeMmPerDeg": (
                    derivatives[0],
                    derivatives[-1],
                ),
                "minimumNonAdjacentBranchGapMm": branch_gap,
                "oneToOneNoSelfIntersection": branch_gap > 1.0e-8,
            }

    fixed_progress = GUIDES["upright"].travel / p.theta_end_deg
    contact_travel = theta_contact_deg(p) / p.theta_end_deg
    continuation_travels = tuple(
        sorted(
            {
                *(index / (sample_count - 1) for index in range(sample_count)),
                contact_travel,
            }
        )
    )
    continuation_rows: dict[str, object] = {}
    maximum_continuation_residual = 0.0
    maximum_continuation_pose_error = 0.0
    for side in ("left", "right"):
        sign = -1.0 if side == "left" else 1.0
        previous = (0.0, 0.0, 0.0)
        for index, travel in enumerate(continuation_travels):
            prescribed = (
                0.0,
                0.0,
                sign * radians(p.theta_end_deg * travel),
            )
            solved, residual = _solve_combined_contact_pose(
                side, travel, previous, p
            )
            pose_error = max(
                abs(solved[value] - prescribed[value]) for value in range(3)
            )
            maximum_continuation_residual = max(
                maximum_continuation_residual, residual
            )
            maximum_continuation_pose_error = max(
                maximum_continuation_pose_error, pose_error
            )
            continuation_rows[f"{side}:sample_{index:02d}"] = {
                "travel": travel,
                "solvedPose": solved,
                "prescribedPose": prescribed,
                "residualNormMm": residual,
                "poseError": pose_error,
                "continuedFromPreviousSample": True,
                "branchJump": False,
            }
            previous = solved
    passes = (
        minimum_derivative > 1.0e-8
        and fixed_progress > 0.0
        and minimum_nonadjacent_gap > 1.0e-8
        and maximum_continuation_residual <= 1.0e-6
        and maximum_continuation_pose_error <= 1.0e-6
    )
    return {
        "passes": passes,
        "sampleCount": sample_count,
        "includesExactOpenContactEnd": True,
        "minimumAnalyticRailDerivativeMmPerDeg": minimum_derivative,
        "fixedTrackProgressMmPerDeg": fixed_progress,
        "fixedTrackProgressStrictlyMonotonic": fixed_progress > 0.0,
        "minimumNonAdjacentBranchGapMm": minimum_nonadjacent_gap,
        "allRailsOneToOneNoSelfIntersection": minimum_nonadjacent_gap > 1.0e-8,
        "maximumContinuationResidualMm": maximum_continuation_residual,
        "maximumContinuationPoseError": maximum_continuation_pose_error,
        "continuationHasNoBranchJump": (
            maximum_continuation_residual <= 1.0e-6
            and maximum_continuation_pose_error <= 1.0e-6
        ),
        "rows": rows,
        "continuationRows": continuation_rows,
    }


def rail_and_web_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    sample_thetas = tuple(
        p.theta_end_deg * index / (p.validation_sample_count - 1)
        for index in range(p.validation_sample_count)
    )
    maximum_reconstruction = 0.0
    minimum_crossing_sine = float("inf")
    rows: dict[str, object] = {}
    for side in ("left", "right"):
        for name in ROD_NAMES:
            residuals: list[float] = []
            crossing: list[float] = []
            for theta in sample_thetas:
                residual = reconstruct_world_from_outer(
                    side, name, theta, p
                ).distance_to(rod_center(name, theta, p))
                sine = _crossing_sine(side, name, theta, p)
                residuals.append(residual)
                crossing.append(sine)
            maximum_reconstruction = max(maximum_reconstruction, max(residuals))
            minimum_crossing_sine = min(minimum_crossing_sine, min(crossing))
            rows[f"{side}:{name}"] = {
                "maximumReconstructionResidualMm": max(residuals),
                "minimumCrossingSine": min(crossing),
            }

    inner_radius = p.inner_plate_diameter / 2.0
    inner_loci = {name: fixed_guide_local_locus(name, p) for name in ROD_NAMES}
    inner_boundary_webs = [
        inner_radius
        - max(hypot(point.y, point.z) for point in locus)
        - p.fixed_slot_width / 2.0
        for locus in inner_loci.values()
    ]
    inner_pair_webs = [
        _segment_distance_yz(*inner_loci[first], *inner_loci[second])
        - p.fixed_slot_width
        for index, first in enumerate(ROD_NAMES)
        for second in ROD_NAMES[index + 1 :]
    ]
    axle_local = _relative_to_pivot(fixed_axle_center_yz(p), p)
    inner_hex_radius = p.inner_hex_bore_af / sqrt(3.0)
    inner_axle_webs = [
        _point_segment_distance_yz(axle_local, *locus)
        - inner_hex_radius
        - p.fixed_slot_width / 2.0
        for locus in inner_loci.values()
    ]

    outer_webs: dict[str, float] = {}
    outer_rod_cutter_gaps: dict[str, float] = {}
    for side, diameter in (
        ("left", p.left_outer_secondary_grip_diameter),
        ("right", p.right_outer_primary_grip_diameter),
    ):
        rod_loci = {name: outer_slot_locus(side, name, p) for name in ROD_NAMES}
        axle_locus = fixed_axle_guide_locus(side, p)
        boundary = [
            diameter / 2.0
            - max(hypot(point.y, point.z) for point in locus)
            - p.outer_slot_width / 2.0
            for locus in rod_loci.values()
        ]
        pair = [
            _polyline_distance_yz(rod_loci[first], rod_loci[second])
            - p.outer_slot_width
            for index, first in enumerate(ROD_NAMES)
            for second in ROD_NAMES[index + 1 :]
        ]
        axle = [
            _polyline_distance_yz(axle_locus, locus)
            - (p.fixed_axle_guide_slot_width + p.outer_slot_width) / 2.0
            for locus in rod_loci.values()
        ]
        outer_rod_cutter_gaps[side] = min(pair)
        outer_webs[side] = min(boundary + pair + axle)

    minimum_web = min(
        inner_boundary_webs
        + inner_pair_webs
        + inner_axle_webs
        + list(outer_webs.values())
    )
    return {
        "sampleCount": p.validation_sample_count,
        "maximumRailReconstructionResidualMm": maximum_reconstruction,
        "minimumCrossingSine": minimum_crossing_sine,
        "minimumRequiredWebMm": p.min_web_mm,
        "minimumWebMm": minimum_web,
        "minimumInnerWebMm": min(
            inner_boundary_webs + inner_pair_webs + inner_axle_webs
        ),
        "minimumOuterWebMm": outer_webs,
        "minimumOuterRodCutterGapMm": outer_rod_cutter_gaps,
        "minimumFixedExtendedRodCutterGapMm": min(inner_pair_webs),
        "allFixedEndpointMarginsMm": {
            name: p.slot_endpoint_margin for name in ROD_NAMES
        },
        "platesAreSingleValidSolids": {
            "left_inner": len(build_inner_plate("left", p).solids()) == 1
            and build_inner_plate("left", p).is_valid,
            "right_inner": len(build_inner_plate("right", p).solids()) == 1
            and build_inner_plate("right", p).is_valid,
            "left_outer": len(build_outer_plate("left", 0.0, p).solids()) == 1
            and build_outer_plate("left", 0.0, p).is_valid,
            "right_outer": len(build_outer_plate("right", 0.0, p).solids()) == 1
            and build_outer_plate("right", 0.0, p).is_valid,
        },
        "rows": rows,
    }


def triangle_motion_math_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """Candidate-facing name for the frozen 3-rod triangle contract."""
    evidence = triangle_motion_evidence(p)
    evidence["sampleCount"] = p.validation_sample_count
    return evidence


def inverse_rail_reconstruction_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """All six inverse rod rails plus both fixed-axle rails."""
    evidence = rail_and_web_evidence(p)
    maximum_axle_residual = 0.0
    for side in ("left", "right"):
        for index in range(p.validation_sample_count):
            theta = p.theta_end_deg * index / (p.validation_sample_count - 1)
            maximum_axle_residual = max(
                maximum_axle_residual,
                reconstruct_fixed_axle_from_outer(side, theta, p).distance_to(
                    fixed_axle_center_yz(p)
                ),
            )
        maximum_axle_residual = max(
            maximum_axle_residual,
            reconstruct_fixed_axle_from_outer(side, theta_contact_deg(p), p).distance_to(
                fixed_axle_center_yz(p)
            ),
        )
    regularity = rail_branch_regularity_evidence(p)
    return {
        **evidence,
        "rodRailCount": 6,
        "fixedAxleRailCount": 2,
        "maximumAxleReconstructionResidualMm": maximum_axle_residual,
        "includesExactContact": True,
        "regularity": regularity,
        "passes": (
            evidence["maximumRailReconstructionResidualMm"] <= 0.05
            and evidence["minimumWebMm"] + 1.0e-9 >= p.min_web_mm
            and regularity["passes"]
        ),
    }


@lru_cache(maxsize=None)
def interface_alignment_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """Check all OPEN clearances, END preload and outside-rim tool access."""
    body_center = PointYZ(p.xt60_body_center_y, p.xt60_body_center_z)
    body = build_xt60_reference(p)
    wire = build_workpiece_reference(0.0, p)
    open_wire_clearances = {
        name: wire_surface_clearance(GUIDES[name].open, p) for name in ROD_NAMES
    }
    first_contacts = {
        name: first_contact_progress(name, p) for name in ROD_NAMES
    }
    end_surface_gaps = {
        name: wire_surface_clearance(GUIDES[name].end, p) for name in ROD_NAMES
    }
    body_clearances = {
        name: float(build_rod(name, 0.0, p).distance(body)) for name in ROD_NAMES
    }
    wire_intersections = {
        name: _intersection_volume(build_rod(name, 0.0, p), wire)
        for name in ROD_NAMES
    }
    tool_rim_clearance = (
        p.solder_tool_min_y - p.right_outer_primary_grip_diameter / 2.0
    )
    short_tail_centerline = p.solder_tool_min_y - GUIDES["upright"].end.y + 1.35947953
    return {
        "candidate": "P19-R1 cycle-4 front-edge short-tail interface",
        "cadInterfaceAcceptanceClaimed": True,
        "xt60BodyCenterYZ": body_center.as_tuple(),
        "openWireSurfaceClearanceMmByRod": open_wire_clearances,
        "firstContactProgressByRod": first_contacts,
        "openBodyClearanceMmByRod": body_clearances,
        "openWireIntersectionMm3ByRod": wire_intersections,
        "endWireSurfaceGapMmByRod": end_surface_gaps,
        "allThreeEndContactsAtPreload": all(
            abs(value + p.wire_preload) <= 1.0e-8
            for value in end_surface_gaps.values()
        ),
        "toolKeepoutMinimumYMm": p.solder_tool_min_y,
        "toolKeepoutOutsideLargestRimMm": tool_rim_clearance,
        "shortTailCenterlineMm": short_tail_centerline,
        "passes": (
            min(open_wire_clearances.values()) + 1.0e-9
            >= P19_OPEN_WIRE_CLEARANCE_MIN_MM
            and min(first_contacts.values()) > 0.0
            and min(body_clearances.values()) >= p.service_clearance_min
            and max(wire_intersections.values()) <= 1.0e-7
            and all(
                abs(value + p.wire_preload) <= 1.0e-8
                for value in end_surface_gaps.values()
            )
            and tool_rim_clearance + 1.0e-9 >= P19_TOOL_KEEP_OUTSIDE_RIM_MM
        ),
        "physicalBoundary": (
            "CAD verifies OPEN clearance and END geometric preload only; force, "
            "self-lock, fit, heat, wear and physical acceptance remain unproven"
        ),
    }


@lru_cache(maxsize=None)
def short_tail_service_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """Actual-BREP OPEN solder-tool and short-tail service-path gate.

    The translucent wire and solder references may overlap the tool keepout;
    production solids may not.  This gate deliberately stays at OPEN because
    soldering is the service operation the P19 front-edge layout is designed
    to expose.
    """
    production: dict[str, Shape] = {
        "center_axle": build_center_axle(p),
        "left_keeper": build_keeper("left", p),
        "right_keeper": build_keeper("right", p),
        "left_inner": build_inner_plate("left", p),
        "right_inner": build_inner_plate("right", p),
        "left_outer": build_outer_plate("left", 0.0, p),
        "right_outer": build_outer_plate("right", 0.0, p),
        "xt60": build_xt60_reference(p),
    }
    for name in ROD_NAMES:
        production[f"{name}_rod"] = build_rod(name, 0.0, p)
        production[f"left_{name}_cap"] = build_cap("left", name, 0.0, p)
        production[f"right_{name}_cap"] = build_cap("right", name, 0.0, p)

    service = build_service_envelopes(0.0, p)
    tools = tuple(
        child for child in service.children
        if child.label.startswith("reference_soldering_tool_keepout")
    )
    wire = build_workpiece_reference(0.0, p)
    production_tool_intersections = {
        name: max(_intersection_volume(shape, tool) for tool in tools)
        for name, shape in production.items()
    }
    production_tool_distances = {
        name: min(float(shape.distance(tool)) for tool in tools)
        for name, shape in production.items()
    }
    rod_wire_intersections = {
        name: _intersection_volume(build_rod(name, 0.0, p), wire)
        for name in ROD_NAMES
    }
    return {
        "state": "OPEN",
        "toolOccurrenceCount": len(tools),
        "toolKeepoutMinimumYMm": p.solder_tool_min_y,
        "toolKeepoutOutsideLargestRimMm": (
            p.solder_tool_min_y - p.right_outer_primary_grip_diameter / 2.0
        ),
        "maximumProductionToolIntersectionMm3": max(
            production_tool_intersections.values()
        ),
        "minimumProductionToolClearanceMm": min(
            production_tool_distances.values()
        ),
        "productionToolIntersectionMm3ByObject": production_tool_intersections,
        "productionToolClearanceMmByObject": production_tool_distances,
        "openRodWireIntersectionMm3ByRod": rod_wire_intersections,
        "passes": (
            len(tools) == 2
            and max(production_tool_intersections.values()) <= 1.0e-7
            and max(rod_wire_intersections.values()) <= 1.0e-7
            and p.solder_tool_min_y
            - p.right_outer_primary_grip_diameter / 2.0
            + 1.0e-9
            >= P19_TOOL_KEEP_OUTSIDE_RIM_MM
        ),
        "physicalBoundary": (
            "CAD verifies OPEN geometric access only; iron approach, operator "
            "ergonomics, heat transfer and the assembled ESC tail remain physical"
        ),
    }


@lru_cache(maxsize=None)
def actual_solid_motion_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """65-state actual BREP collision sweep with explicit wire allow-list."""
    body = build_xt60_reference(p)
    wire = build_workpiece_reference(0.0, p)
    axle = build_center_axle(p)
    keepers = {side: build_keeper(side, p) for side in ("left", "right")}
    inner_local = {
        side: copy(_inner_plate_local(side, p)) for side in ("left", "right")
    }
    outer_local = {
        side: copy(_outer_plate_local(side, p)) for side in ("left", "right")
    }
    rows: dict[str, object] = {}
    minimum_xt60_clearance = float("inf")
    maximum_unintended_intersection = 0.0
    maximum_precontact_wire_intersection = 0.0
    minimum_contact_wire_clearance = float("inf")
    end_wire_intersections: dict[str, float] = {}
    all_plate_guides_clear = True
    all_fixed_hardware_clear = True
    contact_theta = theta_contact_deg(p)
    for index in range(p.validation_sample_count):
        theta = p.theta_end_deg * index / (p.validation_sample_count - 1)
        for name in ROD_NAMES:
            rod = build_rod(name, theta, p)
            body_intersection = _intersection_volume(rod, body)
            body_clearance = float(rod.distance(body))
            minimum_xt60_clearance = min(minimum_xt60_clearance, body_clearance)
            maximum_unintended_intersection = max(
                maximum_unintended_intersection, body_intersection
            )
            fixed_hardware_intersections = [
                _intersection_volume(rod, axle),
                *(
                    _intersection_volume(rod, keeper)
                    for keeper in keepers.values()
                ),
            ]
            all_fixed_hardware_clear &= max(fixed_hardware_intersections) <= 1.0e-7
            maximum_unintended_intersection = max(
                maximum_unintended_intersection,
                *fixed_hardware_intersections,
            )

            fixed_center = _relative_to_pivot(rod_center(name, theta, p), p)
            fixed_probe = _x_cylinder(
                p.rod_diameter,
                p.inner_plate_thickness + 0.10,
                0.0,
                fixed_center.y,
                fixed_center.z,
            )
            plate_intersections: dict[str, float] = {}
            for side in ("left", "right"):
                plate_intersections[f"{side}_inner"] = _intersection_volume(
                    fixed_probe, inner_local[side]
                )
                outer_center = outer_slot_local_center(side, name, theta, p)
                outer_probe = _x_cylinder(
                    p.rod_diameter,
                    p.outer_plate_thickness + 0.10,
                    0.0,
                    outer_center.y,
                    outer_center.z,
                )
                plate_intersections[f"{side}_outer"] = _intersection_volume(
                    outer_probe, outer_local[side]
                )
            all_plate_guides_clear &= max(plate_intersections.values()) <= 1.0e-7
            maximum_unintended_intersection = max(
                maximum_unintended_intersection,
                *plate_intersections.values(),
            )

            wire_intersection = _intersection_volume(rod, wire)
            wire_clearance = float(rod.distance(wire))
            if theta < contact_theta - 1.0e-6:
                maximum_precontact_wire_intersection = max(
                    maximum_precontact_wire_intersection, wire_intersection
                )
            rows[f"sample_{index:02d}:{name}"] = {
                "thetaDeg": theta,
                "xt60ClearanceMm": body_clearance,
                "xt60IntersectionMm3": body_intersection,
                "wireClearanceMm": wire_clearance,
                "wireIntersectionMm3": wire_intersection,
                "wireContactAllowListed": theta + 1.0e-6 >= contact_theta,
                "plateGuideIntersectionsMm3": plate_intersections,
                "fixedHardwareIntersectionsMm3": fixed_hardware_intersections,
            }

    for name in ROD_NAMES:
        contact_rod = build_rod(name, contact_theta, p)
        minimum_contact_wire_clearance = min(
            minimum_contact_wire_clearance, float(contact_rod.distance(wire))
        )
        end_wire_intersections[name] = _intersection_volume(
            build_rod(name, p.theta_end_deg, p), wire
        )
    return {
        "sampleCount": p.validation_sample_count,
        "includesExactContact": True,
        "minimumXt60ClearanceMm": minimum_xt60_clearance,
        "maximumUnintendedIntersectionMm3": maximum_unintended_intersection,
        "maximumPrecontactWireIntersectionMm3": maximum_precontact_wire_intersection,
        "minimumExactContactWireClearanceMm": minimum_contact_wire_clearance,
        "endWireIntersectionMm3ByRod": end_wire_intersections,
        "wireAllowList": (
            "zero before first contact; tangency at exact contact; named 0.25 mm "
            "geometric displacement proxy from contact through END"
        ),
        "allPlateGuidesClear": all_plate_guides_clear,
        "allFixedHardwareClear": all_fixed_hardware_clear,
        "passes": (
            minimum_xt60_clearance + 1.0e-9 >= p.service_clearance_min
            and maximum_unintended_intersection <= 1.0e-7
            and maximum_precontact_wire_intersection <= 1.0e-7
            and minimum_contact_wire_clearance <= 1.0e-6
            and all(value > 0.0 for value in end_wire_intersections.values())
            and all_plate_guides_clear
            and all_fixed_hardware_clear
        ),
        "rows": rows,
    }


@lru_cache(maxsize=None)
def two_sided_support_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """Actual two-sided material plus D10-R2 continuous normal-strip proof."""
    plates = {
        "left_inner": copy(_inner_plate_local("left", p)),
        "right_inner": copy(_inner_plate_local("right", p)),
        "left_outer": copy(_outer_plate_local("left", p)),
        "right_outer": copy(_outer_plate_local("right", p)),
    }
    probe_diameter = 0.20
    support_offset = p.fixed_slot_width / 2.0 + 0.30
    rows: dict[str, object] = {}
    outer_strip_rows: dict[str, object] = {}
    minimum_probe_volume = float("inf")
    support_strip_depth = 0.30
    support_strip_sample_count = 61
    support_strip_boundary_epsilon = 1.0e-4
    expected_probe_volume = pi * (probe_diameter / 2.0) ** 2 * p.outer_plate_thickness
    minimum_outer_endpoint_probe_ratio = float("inf")

    def outer_strip_row(
        plate: Shape,
        center: PointYZ,
        normal: PointYZ,
    ) -> dict[str, object]:
        offsets = tuple(
            p.outer_slot_width / 2.0
            + support_strip_boundary_epsilon
            + (support_strip_depth - support_strip_boundary_epsilon)
            * index
            / (support_strip_sample_count - 1)
            for index in range(support_strip_sample_count)
        )
        inside = tuple(
            plate.is_inside(
                Vector(
                    0.0,
                    center.y + offset * normal.y,
                    center.z + offset * normal.z,
                ),
                tolerance=1.0e-7,
            )
            for offset in offsets
        )
        first_material_index = next(
            (index for index, value in enumerate(inside) if value),
            None,
        )
        continuous = (
            first_material_index is not None
            and all(inside[first_material_index:])
        )
        return {
            "offsetsFromCenterMm": offsets,
            "pointInsideMaterial": inside,
            "firstMaterialIndex": first_material_index,
            "estimatedSweptBoundaryRecessionMm": (
                None
                if first_material_index is None
                else offsets[first_material_index] - p.outer_slot_width / 2.0
            ),
            "continuousFromSweptBoundaryThroughPlus0p30": continuous,
        }
    for index in range(p.validation_sample_count):
        theta = p.theta_end_deg * index / (p.validation_sample_count - 1)
        for name in ROD_NAMES:
            fixed_center = _relative_to_pivot(rod_center(name, theta, p), p)
            fixed_tangent = GUIDES[name].direction
            fixed_normal = PointYZ(-fixed_tangent.z, fixed_tangent.y)
            for side in ("left", "right"):
                volumes: list[float] = []
                for sign in (-1.0, 1.0):
                    point = PointYZ(
                        fixed_center.y + sign * support_offset * fixed_normal.y,
                        fixed_center.z + sign * support_offset * fixed_normal.z,
                    )
                    probe = _x_cylinder(
                        probe_diameter,
                        p.inner_plate_thickness,
                        0.0,
                        point.y,
                        point.z,
                    )
                    volumes.append(
                        _intersection_volume(probe, plates[f"{side}_inner"])
                    )
                minimum_probe_volume = min(minimum_probe_volume, *volumes)
                rows[f"sample_{index:02d}:{side}_inner:{name}"] = volumes

                outer_center = outer_slot_local_center(side, name, theta, p)
                outer_tangent = _curve_tangent(side, name, theta, p)
                tangent_length = hypot(outer_tangent.y, outer_tangent.z)
                outer_normal = PointYZ(
                    -outer_tangent.z / tangent_length,
                    outer_tangent.y / tangent_length,
                )
                volumes = []
                for sign in (-1.0, 1.0):
                    point = PointYZ(
                        outer_center.y + sign * support_offset * outer_normal.y,
                        outer_center.z + sign * support_offset * outer_normal.z,
                    )
                    probe = _x_cylinder(
                        probe_diameter,
                        p.outer_plate_thickness,
                        0.0,
                        point.y,
                        point.z,
                    )
                    volume = _intersection_volume(
                        probe, plates[f"{side}_outer"]
                    )
                    volumes.append(volume)
                    minimum_outer_endpoint_probe_ratio = min(
                        minimum_outer_endpoint_probe_ratio,
                        volume / expected_probe_volume,
                    )
                minimum_probe_volume = min(minimum_probe_volume, *volumes)
                rows[f"sample_{index:02d}:{side}_outer:{name}"] = volumes

                strip_rows: list[dict[str, object]] = []
                for sign in (-1.0, 1.0):
                    signed_normal = PointYZ(
                        sign * outer_normal.y,
                        sign * outer_normal.z,
                    )
                    strip_rows.append(
                        outer_strip_row(
                            plates[f"{side}_outer"],
                            outer_center,
                            signed_normal,
                        )
                    )
                outer_strip_rows[
                    f"sample_{index:02d}:{side}_outer:{name}"
                ] = strip_rows

    contact_theta = theta_contact_deg(p)
    for side in ("left", "right"):
        for name in ROD_NAMES:
            outer_center = outer_slot_local_center(side, name, contact_theta, p)
            outer_tangent = _curve_tangent(side, name, contact_theta, p)
            tangent_length = hypot(outer_tangent.y, outer_tangent.z)
            outer_normal = PointYZ(
                -outer_tangent.z / tangent_length,
                outer_tangent.y / tangent_length,
            )
            contact_rows: list[dict[str, object]] = []
            for sign in (-1.0, 1.0):
                signed_normal = PointYZ(
                    sign * outer_normal.y,
                    sign * outer_normal.z,
                )
                contact_rows.append(
                    outer_strip_row(
                        plates[f"{side}_outer"],
                        outer_center,
                        signed_normal,
                    )
                )
            outer_strip_rows[f"contact_exact:{side}_outer:{name}"] = contact_rows

    closed_end_rows: dict[str, float] = {}
    for state, theta, outward_sign in (
        ("open", 0.0, -1.0),
        ("end", p.theta_end_deg, 1.0),
    ):
        for name in ROD_NAMES:
            fixed_tangent = GUIDES[name].direction
            fixed_center = _relative_to_pivot(rod_center(name, theta, p), p)
            fixed_distance = (
                p.slot_endpoint_margin + p.fixed_slot_width / 2.0 + 0.30
            )
            fixed_point = PointYZ(
                fixed_center.y + outward_sign * fixed_distance * fixed_tangent.y,
                fixed_center.z + outward_sign * fixed_distance * fixed_tangent.z,
            )
            for side in ("left", "right"):
                probe = _x_cylinder(
                    probe_diameter,
                    p.inner_plate_thickness,
                    0.0,
                    fixed_point.y,
                    fixed_point.z,
                )
                value = _intersection_volume(probe, plates[f"{side}_inner"])
                closed_end_rows[f"{state}:{side}_inner:{name}"] = value
                minimum_probe_volume = min(minimum_probe_volume, value)

                outer_center = outer_slot_local_center(side, name, theta, p)
                tangent = _curve_tangent(side, name, theta, p)
                tangent_length = hypot(tangent.y, tangent.z)
                unit_tangent = PointYZ(
                    tangent.y / tangent_length, tangent.z / tangent_length
                )
                outer_distance = p.outer_slot_width / 2.0 + 0.30
                outer_point = PointYZ(
                    outer_center.y + outward_sign * outer_distance * unit_tangent.y,
                    outer_center.z + outward_sign * outer_distance * unit_tangent.z,
                )
                probe = _x_cylinder(
                    probe_diameter,
                    p.outer_plate_thickness,
                    0.0,
                    outer_point.y,
                    outer_point.z,
                )
                value = _intersection_volume(probe, plates[f"{side}_outer"])
                closed_end_rows[f"{state}:{side}_outer:{name}"] = value
                minimum_probe_volume = min(minimum_probe_volume, value)
    return {
        "sampleCount": p.validation_sample_count,
        "plateCount": 4,
        "rodCount": 3,
        "probeDiameterMm": probe_diameter,
        "includesExactContact": True,
        "outerSupportStripDepthMm": support_strip_depth,
        "outerSupportStripSampleCountPerSide": support_strip_sample_count,
        "outerSupportStripBoundaryEpsilonMm": support_strip_boundary_epsilon,
        "outerEndpointProbeExpectedVolumeMm3": expected_probe_volume,
        "minimumOuterEndpointProbeMaterialRatio": minimum_outer_endpoint_probe_ratio,
        "allOuterEndpointProbesFull": minimum_outer_endpoint_probe_ratio >= 0.999,
        "allOuterSupportStripsContinuous": all(
            row["continuousFromSweptBoundaryThroughPlus0p30"]
            for pair in outer_strip_rows.values()
            for row in pair
        ),
        "maximumEstimatedSweptBoundaryRecessionMm": max(
            row["estimatedSweptBoundaryRecessionMm"]
            for pair in outer_strip_rows.values()
            for row in pair
            if row["estimatedSweptBoundaryRecessionMm"] is not None
        ),
        "minimumMaterialProbeVolumeMm3": minimum_probe_volume,
        "allNormalSidesSupported": all(
            all(value > 1.0e-4 for value in volumes) for volumes in rows.values()
        ),
        "allSlotEndsClosed": all(
            value > 1.0e-4 for value in closed_end_rows.values()
        ),
        "passes": (
            minimum_probe_volume > 1.0e-4
            and minimum_outer_endpoint_probe_ratio >= 0.999
            and all(
                row["continuousFromSweptBoundaryThroughPlus0p30"]
                for pair in outer_strip_rows.values()
                for row in pair
            )
        ),
        "normalSupportRows": rows,
        "outerSupportStripRows": outer_strip_rows,
        "closedEndRows": closed_end_rows,
    }


def cap_stack_closure_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    critical_thetas = (0.0, theta_contact_deg(p), p.theta_end_deg)
    collisions: dict[str, float] = {}
    rod_cap_engagements: dict[str, float] = {}
    for theta in critical_thetas:
        plates = {
            "left_inner": build_inner_plate("left", p),
            "right_inner": build_inner_plate("right", p),
            "left_outer": build_outer_plate("left", theta, p),
            "right_outer": build_outer_plate("right", theta, p),
        }
        for name in ROD_NAMES:
            rod = build_rod(name, theta, p)
            for side in ("left", "right"):
                cap = build_cap(side, name, theta, p)
                key = f"theta_{theta:.9f}:{side}:{name}"
                rod_cap_engagements[key] = _intersection_volume(rod, cap)
                for plate_name, plate in plates.items():
                    collisions[f"{key}:{plate_name}"] = _intersection_volume(
                        cap, plate
                    )
                collisions[f"{key}:{side}_keeper"] = _intersection_volume(
                    cap, build_keeper(side, p)
                )
    return {
        "rodLengthMm": p.rod_length_target,
        "principalStackWidthMm": p.principal_stack_width,
        "capToOuterGapMmPerSide": p.cap_to_outer_running_gap,
        "derivedEngagementMmPerSide": (
            p.rod_length_target
            - p.principal_stack_width
            - 2.0 * p.cap_to_outer_running_gap
        )
        / 2.0,
        "capLengthMm": p.follower_head_length,
        "closedEndWallMm": p.cap_closed_end_wall,
        "proximalGuide": {
            "idMm": p.cap_sliding_guide_id,
            "depthMm": p.cap_sliding_guide_depth,
        },
        "distalRetention": {
            "idMm": p.cap_socket_id,
            "depthMm": p.cap_retention_depth,
            "physicalCouponRequired": True,
        },
        "capCount": 6,
        "maximumCapPlateOrKeeperIntersectionMm3": max(collisions.values()),
        "maximumNominalRodCapMaterialIntersectionMm3": max(
            rod_cap_engagements.values()
        ),
        "distalNominalRadialClearanceMm": (
            p.cap_socket_id - p.rod_diameter
        )
        / 2.0,
        "passes": max(collisions.values()) <= 1.0e-7
        and abs(
            (
                p.rod_length_target
                - p.principal_stack_width
                - 2.0 * p.cap_to_outer_running_gap
            )
            / 2.0
            - p.cap_rod_engagement
        )
        <= 1.0e-9
        and p.cap_sliding_guide_depth + p.cap_retention_depth
        == p.cap_rod_engagement
        and p.follower_head_length
        >= p.cap_rod_engagement + p.cap_closed_end_wall,
        "collisionRows": collisions,
        "rodCapIntersectionRows": rod_cap_engagements,
    }


def central_span_service_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    evidence = _completed_pigtail_service_evidence(p)
    return {
        "pathId": evidence["pathId"],
        "sequence": "full open -> repaired four-pose rigid-body removal path",
        "innerClearSpanMm": p.inner_clear_span,
        "xt60BodyWidthMm": p.xt60_body_width_x,
        "sideClearanceMmEach": p.xt60_side_clearance_each,
        "waypoints": evidence["waypoints"],
        "brepSamplesPerSegment": evidence["brepSamplesPerSegment"],
        "brepSampleCount": evidence["brepSampleCount"],
        "brepMinimumClearanceMm": evidence["brepMinimumClearanceMm"],
        "brepMaximumIntersectionMm3": evidence["brepMaximumIntersectionMm3"],
        "analyticSamplesPerSegment": evidence["analyticSamplesPerSegment"],
        "analyticSampleCount": evidence["analyticSampleCount"],
        "analyticMinimumClearanceMm": evidence["analyticMinimumClearanceMm"],
        "analyticLimitingPair": evidence["analyticLimitingPair"],
        "analyticMinimumByPair": evidence["analyticMinimumByPair"],
        "brepLimitingPair": evidence["brepLimitingPair"],
        "brepMaximumIntersectionPair": evidence["brepMaximumIntersectionPair"],
        "brepMinimumByPair": evidence["brepMinimumByPair"],
        "includedPigtailFeatures": evidence["includedPigtailFeatures"],
        "includedProductionSolids": evidence["includedProductionSolids"],
        "minimumClearanceMm": evidence["minimumClearanceMm"],
        "zeroIntersection": evidence["zeroIntersection"],
        "passes": evidence["passes"],
        "finding": "P19-R1 pairwise finite-solid rigid-body removal sweep is clear",
    }


def legacy_validator_collision_regression_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    """Reproduce the blocked validator's 47.2594024 mm3 false-pass case.

    The historical aggregate check hid the individual wire/rod intersection at
    this pose.  This fixture is evidence only: it uses the rejected wire datum
    and rejected service pose while all candidate product geometry stays frozen.
    """
    legacy = replace(
        p,
        wire_line_point_y=12.286052150181444,
        wire_line_point_z=11.146304978289136,
    )
    pose = ServicePose(-4.0, 26.84, -15.0)
    features = _completed_pigtail_features_at(pose, legacy)
    diagonal = build_rod("diagonal", 0.0, p)
    rows: dict[str, dict[str, float]] = {}
    for feature_name in ("bentWire0", "bentWire1"):
        feature = features[feature_name]
        rows[feature_name] = {
            "distanceMm": float(feature.distance(diagonal)),
            "intersectionMm3": _intersection_volume(feature, diagonal),
        }
    maximum = max(row["intersectionMm3"] for row in rows.values())
    return {
        "historicalPose": (pose.delta_y, pose.delta_z, pose.phi_deg),
        "historicalWireLinePoint": (
            legacy.wire_line_point_y,
            legacy.wire_line_point_z,
        ),
        "productionSolid": "diagonalRod",
        "rows": rows,
        "maximumIntersectionMm3": maximum,
        "regressionDetected": maximum > 47.259,
    }


def fixed_occurrence_transform_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    center = outer_rotation_center_yz(p)
    axle = fixed_axle_center_yz(p)
    fixed_frames = {
        "stepped_center_axle": (0.0, axle.y, axle.z, 0.0),
        "left_inner_fixed_guide": (p.left_inner_x, center.y, center.z, 0.0),
        "right_inner_fixed_guide": (p.right_inner_x, center.y, center.z, 0.0),
        "left_keeper": (p.keeper_left_x, axle.y, axle.z, 0.0),
        "right_keeper": (p.keeper_right_x, axle.y, axle.z, 0.0),
    }
    states = {
        state: {
            "fixedFramesXYZAngleDeg": fixed_frames,
            "leftOuterAngleDeg": alpha_left(theta),
            "rightOuterAngleDeg": alpha_right(theta),
            "outerRotationCenterYZ": center.as_tuple(),
        }
        for state, theta in STATE_THETA.items()
    }
    return {
        "fixedOccurrenceNames": tuple(fixed_frames),
        "states": states,
        "allFixedWorldInvariant": all(
            row["fixedFramesXYZAngleDeg"] == fixed_frames for row in states.values()
        ),
    }


def _fixed_axle_feature_gap_evidence(
    p: P19R1Parameters,
) -> tuple[float, bool]:
    center = outer_rotation_center_yz(p)
    axle = fixed_axle_center_yz(p)
    offset = PointYZ(axle.y - center.y, axle.z - center.z)
    inner_hex = _x_hex_prism(
        p.inner_hex_bore_af,
        p.inner_plate_thickness + 2.0,
        0.0,
        offset.y,
        offset.z,
    )
    inner_neighbors: list[Shape] = [
        _slot_capsule_cutter(
            fixed_guide_local_locus(name, p),
            p.fixed_slot_width,
            p.inner_plate_thickness + 2.0,
        )
        for name in ROD_NAMES
    ]
    distances = [float(inner_hex.distance(neighbor)) for neighbor in inner_neighbors]
    intersections = [
        _intersection_volume(inner_hex, neighbor) for neighbor in inner_neighbors
    ]
    for side in ("left", "right"):
        axle_guide = _slot_capsule_cutter(
            fixed_axle_guide_locus(side, p),
            p.fixed_axle_guide_slot_width,
            p.outer_plate_thickness + 2.0,
        )
        outer_neighbors: list[Shape] = [
            _slot_capsule_cutter(
                outer_slot_locus(side, name, p),
                p.outer_slot_width,
                p.outer_plate_thickness + 2.0,
            )
            for name in ROD_NAMES
        ]
        distances.extend(
            float(axle_guide.distance(neighbor)) for neighbor in outer_neighbors
        )
        intersections.extend(
            _intersection_volume(axle_guide, neighbor)
            for neighbor in outer_neighbors
        )
    return min(distances), max(intersections) <= 1.0e-7


def fixed_axle_actual_solid_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    center = outer_rotation_center_yz(p)
    axle_center = fixed_axle_center_yz(p)
    offset = PointYZ(axle_center.y - center.y, axle_center.z - center.z)
    inner_hex_radius = p.inner_hex_bore_af / sqrt(3.0)
    inner_boundary_web = (
        p.inner_plate_diameter / 2.0
        - (p.fixed_axle_eccentricity + inner_hex_radius)
    )
    left_boundary_web = (
        p.left_outer_secondary_grip_diameter / 2.0
        - (p.fixed_axle_eccentricity + p.fixed_axle_guide_slot_width / 2.0)
    )
    right_boundary_web = (
        p.right_outer_primary_grip_diameter / 2.0
        - (p.fixed_axle_eccentricity + p.fixed_axle_guide_slot_width / 2.0)
    )
    analytic_webs = [inner_boundary_web, left_boundary_web, right_boundary_web]
    for name in ROD_NAMES:
        first, second = fixed_guide_local_locus(name, p)
        analytic_webs.append(
            _point_segment_distance_yz(offset, first, second)
            - (inner_hex_radius + p.fixed_slot_width / 2.0)
        )
    for side in ("left", "right"):
        axle_locus = fixed_axle_guide_locus(side, p)
        for name in ROD_NAMES:
            analytic_webs.append(
                _polyline_distance_yz(axle_locus, outer_slot_locus(side, name, p))
                - (p.fixed_axle_guide_slot_width + p.outer_slot_width) / 2.0
            )

    exact_gap, exact_cutters_clear = _fixed_axle_feature_gap_evidence(p)
    axle = build_center_axle(p)
    body = build_xt60_reference(p)
    samples = tuple(
        index * p.theta_end_deg / (p.fixed_axle_guide_sample_count - 1)
        for index in range(p.fixed_axle_guide_sample_count)
    )
    all_axle_outer_clear = True
    all_keeper_outer_clear = True
    all_axle_rod_clear = True
    all_keeper_cap_clear = True
    all_service_clear = True
    minimum_service_clearance = float("inf")
    center_filled = True
    for theta in samples:
        for side in ("left", "right"):
            outer = build_outer_plate(side, theta, p)
            keeper = build_keeper(side, p)
            all_axle_outer_clear &= _intersection_volume(axle, outer) <= 1.0e-7
            all_keeper_outer_clear &= _intersection_volume(keeper, outer) <= 1.0e-7
            probe = _x_cylinder(
                1.0,
                p.outer_plate_thickness,
                p.left_outer_x if side == "left" else p.right_outer_x,
                center.y,
                center.z,
            )
            center_filled &= _intersection_volume(probe, outer) > 0.10
        for name in ROD_NAMES:
            rod = build_rod(name, theta, p)
            all_axle_rod_clear &= _intersection_volume(axle, rod) <= 1.0e-7
            for side in ("left", "right"):
                all_keeper_cap_clear &= (
                    _intersection_volume(
                        build_keeper(side, p), build_cap(side, name, theta, p)
                    )
                    <= 1.0e-7
                )
        service_targets = [body, *build_service_envelopes(theta, p).children]
        for fixed in (axle, build_keeper("left", p), build_keeper("right", p)):
            for target in service_targets:
                distance = float(fixed.distance(target))
                minimum_service_clearance = min(minimum_service_clearance, distance)
                all_service_clear &= (
                    _intersection_volume(fixed, target) <= 1.0e-7
                )
    minimum_analytic_web = min(analytic_webs)
    return {
        "minimumRequiredWebMm": p.min_web_mm,
        "minimumAnalyticWebMm": minimum_analytic_web,
        "minimumActualOuterGuideWebMm": min(analytic_webs[6:]),
        "minimumActualInnerHexWebMm": inner_boundary_web,
        "leftOuterBoundaryWebMm": left_boundary_web,
        "rightOuterBoundaryWebMm": right_boundary_web,
        "minimumExactFrozenFeatureGapMm": exact_gap,
        "allFrozenFeatureCuttersClear": exact_cutters_clear,
        "minimumAxleGuideRadialClearanceMm": (
            p.fixed_axle_guide_slot_width - p.outer_journal_diameter
        )
        / 2.0,
        "minimumKeeperRadialCaptureMm": (
            p.keeper_outer_diameter - p.fixed_axle_guide_slot_width
        )
        / 2.0,
        "minimumXt60AndServiceClearanceMm": minimum_service_clearance,
        "sampleCount": len(samples),
        "allAxleOuterPlateIntersectionsZero": all_axle_outer_clear,
        "allKeeperOuterPlateIntersectionsZero": all_keeper_outer_clear,
        "allAxleGuideProbeIntersectionsZero": all_axle_outer_clear,
        "allAxleWhiteRodIntersectionsZero": all_axle_rod_clear,
        "allKeeperCapIntersectionsZero": all_keeper_cap_clear,
        "allXt60AndServiceIntersectionsZero": all_service_clear,
        "centerAtCHasNoDecorativeHole": center_filled,
    }


def _determinant_3x3(matrix: list[list[float]]) -> float:
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def _symmetric_eigenvalues_3x3(matrix: list[list[float]]) -> tuple[float, float, float]:
    """Jacobi eigenvalues for a real symmetric 3x3 matrix."""
    work = [row[:] for row in matrix]
    for _ in range(40):
        pairs = ((0, 1), (0, 2), (1, 2))
        p_index, q_index = max(pairs, key=lambda pair: abs(work[pair[0]][pair[1]]))
        off = work[p_index][q_index]
        if abs(off) <= 1.0e-15:
            break
        angle = 0.5 * atan2(
            2.0 * off,
            work[q_index][q_index] - work[p_index][p_index],
        )
        c_value = cos(angle)
        s_value = sin(angle)
        for index in range(3):
            if index in (p_index, q_index):
                continue
            p_value = work[index][p_index]
            q_value = work[index][q_index]
            work[index][p_index] = work[p_index][index] = (
                c_value * p_value - s_value * q_value
            )
            work[index][q_index] = work[q_index][index] = (
                s_value * p_value + c_value * q_value
            )
        pp = work[p_index][p_index]
        qq = work[q_index][q_index]
        work[p_index][p_index] = (
            c_value * c_value * pp
            - 2.0 * s_value * c_value * off
            + s_value * s_value * qq
        )
        work[q_index][q_index] = (
            s_value * s_value * pp
            + 2.0 * s_value * c_value * off
            + c_value * c_value * qq
        )
        work[p_index][q_index] = work[q_index][p_index] = 0.0
    return tuple(sorted((work[0][0], work[1][1], work[2][2])))  # type: ignore[return-value]


def _normalized_singular_values(
    jacobian: tuple[tuple[float, float, float], ...],
    characteristic_radius_mm: float,
) -> tuple[float, float, float]:
    # Pose coordinates are normalized as (dy/1mm, dz/1mm,
    # dangle*characteristic_radius/1mm), then every scalar constraint row is
    # normalized to unit length. This makes the conditioning dimensionless.
    normalized_rows: list[tuple[float, float, float]] = []
    for row in jacobian:
        scaled = (row[0], row[1], row[2] / characteristic_radius_mm)
        norm = sqrt(sum(value * value for value in scaled))
        normalized_rows.append(tuple(value / norm for value in scaled))
    gram = [
        [
            sum(row[first] * row[second] for row in normalized_rows)
            for second in range(3)
        ]
        for first in range(3)
    ]
    eigenvalues = _symmetric_eigenvalues_3x3(gram)
    return tuple(sqrt(max(0.0, value)) for value in eigenvalues)  # type: ignore[return-value]


def _singular_values(
    jacobian: tuple[tuple[float, float, float], ...],
) -> tuple[float, float, float]:
    gram = [
        [
            sum(row[first] * row[second] for row in jacobian)
            for second in range(3)
        ]
        for first in range(3)
    ]
    eigenvalues = _symmetric_eigenvalues_3x3(gram)
    return tuple(sqrt(max(0.0, value)) for value in eigenvalues)  # type: ignore[return-value]


def _solve_3x3(matrix: list[list[float]], vector: list[float]) -> list[float]:
    augmented = [list(matrix[row]) + [vector[row]] for row in range(3)]
    for column in range(3):
        pivot = max(range(column, 3), key=lambda row: abs(augmented[row][column]))
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        if abs(divisor) <= 1.0e-14:
            raise ValueError("combined contact normal equations are singular")
        for index in range(column, 4):
            augmented[column][index] /= divisor
        for row in range(3):
            if row == column:
                continue
            factor = augmented[row][column]
            for index in range(column, 4):
                augmented[row][index] -= factor * augmented[column][index]
    return [augmented[row][3] for row in range(3)]


def _contact_curve_local(
    side: SideName,
    contact: str,
    travel: float,
    p: P19R1Parameters,
) -> PointYZ:
    theta = p.theta_end_deg * travel
    if contact == "fixed_axle":
        return fixed_axle_guide_local_center(side, theta, p)
    return outer_slot_local_center(side, contact, theta, p)  # type: ignore[arg-type]


def _combined_contact_residuals(
    side: SideName,
    travel: float,
    pose: tuple[float, float, float],
    p: P19R1Parameters,
) -> tuple[float, ...]:
    """Four nominal centerline normal residuals for one outer rigid pose.

    ``pose`` is ``(delta_y, delta_z, angle_radians)`` relative to C.  Slot
    tangent travel is eliminated locally, leaving one scalar path constraint
    per fixed contact.  This is a local mobility proof, not a force/fit claim.
    """
    center = outer_rotation_center_yz(p)
    world_contacts: tuple[tuple[str, PointYZ], ...] = (
        ("fixed_axle", fixed_axle_center_yz(p)),
        *((name, rod_center(name, p.theta_end_deg * travel, p)) for name in ROD_NAMES),
    )
    delta_y, delta_z, angle_radians = pose
    result: list[float] = []
    epsilon = 1.0e-5
    lower = max(0.0, travel - epsilon)
    upper = min(1.0, travel + epsilon)
    for contact, world in world_contacts:
        before = _contact_curve_local(side, contact, lower, p)
        after = _contact_curve_local(side, contact, upper, p)
        tangent = PointYZ(after.y - before.y, after.z - before.z)
        tangent_length = hypot(tangent.y, tangent.z)
        normal = PointYZ(-tangent.z / tangent_length, tangent.y / tangent_length)
        local = _rotate_yz(
            PointYZ(
                world.y - center.y - delta_y,
                world.z - center.z - delta_z,
            ),
            -degrees(angle_radians),
        )
        target = _contact_curve_local(side, contact, travel, p)
        result.append(
            normal.y * (local.y - target.y) + normal.z * (local.z - target.z)
        )
    return tuple(result)


def outer_pose_constraint_residuals(
    side: SideName,
    travel: float,
    pose: tuple[float, float, float],
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> tuple[float, float, float, float]:
    """Public four-contact residual vector for independent finite differences.

    Row order is ``fixed_axle, upright, bottom, diagonal``. ``pose`` is
    ``(delta_y_mm, delta_z_mm, alpha_rad)`` relative to rotation datum C.
    Each scalar is signed local normal distance to its derived outer rail.
    """
    return _combined_contact_residuals(side, travel, pose, p)  # type: ignore[return-value]


def _combined_contact_jacobian(
    side: SideName,
    travel: float,
    pose: tuple[float, float, float],
    p: P19R1Parameters,
) -> tuple[tuple[float, float, float], ...]:
    base = _combined_contact_residuals(side, travel, pose, p)
    step = 1.0e-6
    columns: list[tuple[float, ...]] = []
    for column in range(3):
        perturbed = list(pose)
        perturbed[column] += step
        values = _combined_contact_residuals(
            side, travel, tuple(perturbed), p  # type: ignore[arg-type]
        )
        columns.append(tuple((values[row] - base[row]) / step for row in range(4)))
    return tuple(
        (columns[0][row], columns[1][row], columns[2][row])
        for row in range(4)
    )


def outer_pose_constraint_jacobian(
    side: SideName,
    travel: float,
    pose: tuple[float, float, float],
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> tuple[tuple[float, float, float], ...]:
    """Finite-difference Jacobian of :func:`outer_pose_constraint_residuals`."""
    return _combined_contact_jacobian(side, travel, pose, p)


def _solve_combined_contact_pose(
    side: SideName,
    travel: float,
    initial: tuple[float, float, float],
    p: P19R1Parameters,
) -> tuple[tuple[float, float, float], float]:
    pose = list(initial)
    for _ in range(60):
        residual = _combined_contact_residuals(
            side, travel, tuple(pose), p  # type: ignore[arg-type]
        )
        jacobian = _combined_contact_jacobian(
            side, travel, tuple(pose), p  # type: ignore[arg-type]
        )
        normal_matrix = [
            [
                sum(jacobian[row][a] * jacobian[row][b] for row in range(4))
                + (1.0e-12 if a == b else 0.0)
                for b in range(3)
            ]
            for a in range(3)
        ]
        right_hand = [
            -sum(jacobian[row][column] * residual[row] for row in range(4))
            for column in range(3)
        ]
        correction = _solve_3x3(normal_matrix, right_hand)
        pose = [pose[index] + correction[index] for index in range(3)]
        if max(abs(value) for value in correction) <= 1.0e-12:
            break
    final_residual = _combined_contact_residuals(
        side, travel, tuple(pose), p  # type: ignore[arg-type]
    )
    return (
        tuple(pose),  # type: ignore[return-value]
        sqrt(sum(value * value for value in final_residual)),
    )


def combined_contact_closure_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    rows: dict[str, object] = {}
    all_pass = True
    sample_count = p.validation_sample_count
    for side in ("left", "right"):
        sign = -1.0 if side == "left" else 1.0
        for index in range(sample_count):
            travel = index / (sample_count - 1)
            prescribed = (0.0, 0.0, sign * radians(p.theta_end_deg * travel))
            residual = _combined_contact_residuals(side, travel, prescribed, p)
            jacobian = _combined_contact_jacobian(side, travel, prescribed, p)
            row_sets = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
            maximum_minor = max(
                abs(_determinant_3x3([list(jacobian[row]) for row in rows3]))
                for rows3 in row_sets
            )
            solve_rows: list[dict[str, object]] = []
            for delta in (
                (0.40, -0.30, radians(2.0)),
                (-0.50, 0.40, radians(-2.5)),
            ):
                initial = tuple(prescribed[i] + delta[i] for i in range(3))
                solved, solved_residual = _solve_combined_contact_pose(
                    side, travel, initial, p
                )
                pose_error = max(abs(solved[i] - prescribed[i]) for i in range(3))
                solve_rows.append(
                    {
                        "pose": solved,
                        "poseError": pose_error,
                        "residualNormMm": solved_residual,
                    }
                )
            maximum_pose_error = max(row["poseError"] for row in solve_rows)
            converged = all(
                row["poseError"] <= 1.0e-6
                and row["residualNormMm"] <= 1.0e-6
                for row in solve_rows
            )
            row_pass = (
                sqrt(sum(value * value for value in residual)) <= 1.0e-6
                and maximum_minor > 1.0e-6
                and converged
            )
            all_pass &= row_pass
            rows[f"{side}:sample_{index:02d}"] = {
                "travel": travel,
                "thetaDeg": p.theta_end_deg * travel,
                "contactResidualNormMm": sqrt(
                    sum(value * value for value in residual)
                ),
                "mobilityJacobianRank": 3 if maximum_minor > 1.0e-6 else 2,
                "maximumRank3Minor": maximum_minor,
                "perturbedSolves": solve_rows,
                "allPerturbedSolvesConvergedToPrescribedPose": converged,
                "maximumPerturbedPoseError": maximum_pose_error,
                "passes": row_pass,
            }
    return {
        "passes": all_pass,
        "sampleCountPerSide": sample_count,
        "rows": rows,
        "claimBoundary": (
            "nominal centerline local-mobility closure only; slot clearance, "
            "force, friction, self-lock and physical fit are not proven"
        ),
    }


def conditioning_evidence(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> dict[str, object]:
    rows: dict[str, object] = {}
    minimum_ratio = float("inf")
    maximum_condition = 0.0
    minimum_rank = 3
    characteristic_radius = max(
        fixed_axle_center_yz(p).distance_to(outer_rotation_center_yz(p)),
        *(
            rod_center(name, 0.0, p).distance_to(outer_rotation_center_yz(p))
            for name in ROD_NAMES
        ),
    )
    base_travels = tuple(
        index / (p.validation_sample_count - 1)
        for index in range(p.validation_sample_count)
    )
    contact_travel = theta_contact_deg(p) / p.theta_end_deg
    for side in ("left", "right"):
        sign = -1.0 if side == "left" else 1.0
        for index, travel in enumerate((*base_travels, contact_travel)):
            pose = (0.0, 0.0, sign * radians(p.theta_end_deg * travel))
            jacobian = _combined_contact_jacobian(side, travel, pose, p)
            raw_singular_values = _singular_values(jacobian)
            singular_values = _normalized_singular_values(
                jacobian, characteristic_radius
            )
            largest = singular_values[-1]
            smallest = singular_values[0]
            ratio = smallest / largest
            rank = sum(value > largest * 1.0e-9 for value in singular_values)
            condition = largest / smallest
            minimum_ratio = min(minimum_ratio, ratio)
            maximum_condition = max(maximum_condition, condition)
            minimum_rank = min(minimum_rank, rank)
            row_name = (
                f"{side}:contact_exact"
                if index == p.validation_sample_count
                else f"{side}:sample_{index:02d}"
            )
            rows[row_name] = {
                "travel": travel,
                "thetaDeg": p.theta_end_deg * travel,
                "residualVectorMm": outer_pose_constraint_residuals(
                    side, travel, pose, p
                ),
                "rawJacobian": jacobian,
                "rawSingularValues": raw_singular_values,
                "normalizedSingularValues": singular_values,
                "sigmaMinOverSigmaMax": ratio,
                "conditionNumber": condition,
                "rank": rank,
            }
    return {
        "sampleCountPerSide": p.validation_sample_count,
        "includesExactContactPerSide": True,
        "residualRowOrder": ("fixed_axle", "upright", "bottom", "diagonal"),
        "poseCoordinateOrder": ("delta_y_mm", "delta_z_mm", "alpha_rad"),
        "translationScaleMm": 1.0,
        "rotationScaleRadiusMm": characteristic_radius,
        "rowNormalization": "unit Euclidean norm after pose-coordinate scaling",
        "minimumRank": minimum_rank,
        "minimumSigmaMinOverSigmaMax": minimum_ratio,
        "maximumConditionNumber": maximum_condition,
        "passes": minimum_rank == 3 and minimum_ratio >= 1.0e-3,
        "rows": rows,
    }


def _motion_occurrence(shape: Shape, label: str) -> Shape:
    shape.label = label
    return shape


def build_fixed_axle_focus_state(
    theta_deg: float = 0.0,
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> Compound:
    children = [
        _motion_occurrence(build_center_axle(p), "motion_fixed_stepped_center_axle"),
        _motion_occurrence(build_keeper("left", p), "motion_fixed_left_keeper"),
        _motion_occurrence(build_keeper("right", p), "motion_fixed_right_keeper"),
        _motion_occurrence(build_inner_plate("left", p), "motion_fixed_left_inner"),
        _motion_occurrence(build_inner_plate("right", p), "motion_fixed_right_inner"),
        _motion_occurrence(build_outer_plate("left", theta_deg, p), "motion_rotating_left_outer"),
        _motion_occurrence(build_outer_plate("right", theta_deg, p), "motion_rotating_right_outer"),
        _motion_occurrence(build_xt60_reference(p), "motion_fixed_xt60_reference"),
        _motion_occurrence(build_workpiece_reference(theta_deg, p), "motion_fixed_workpiece_reference"),
    ]
    for name in ROD_NAMES:
        children.extend(
            (
                _motion_occurrence(build_rod(name, theta_deg, p), f"motion_{name}_rod"),
                _motion_occurrence(build_cap("left", name, theta_deg, p), f"motion_left_{name}_cap"),
                _motion_occurrence(build_cap("right", name, theta_deg, p), f"motion_right_{name}_cap"),
            )
        )
    return Compound(
        children=children,
        label=f"P19_R1_fixed_axle_focus_theta_{theta_deg:.2f}__{provenance_token(p)}",
    )


def build_full_motion_open(
    p: P19R1Parameters = P19_R1_DEFAULTS,
) -> Compound:
    children: list[Shape] = [
        _motion_occurrence(build_center_axle(p), "motion_full_fixed_stepped_center_axle"),
        _motion_occurrence(build_keeper("left", p), "motion_full_fixed_left_keeper"),
        _motion_occurrence(build_keeper("right", p), "motion_full_fixed_right_keeper"),
        _motion_occurrence(build_inner_plate("left", p), "motion_full_fixed_left_inner"),
        _motion_occurrence(build_inner_plate("right", p), "motion_full_fixed_right_inner"),
        _motion_occurrence(build_outer_plate("left", 0.0, p), "motion_full_rotating_left_outer"),
        _motion_occurrence(build_outer_plate("right", 0.0, p), "motion_full_rotating_right_outer"),
        _motion_occurrence(build_xt60_reference(p), "motion_full_fixed_xt60_reference"),
        _motion_occurrence(build_workpiece_reference(0.0, p), "motion_full_fixed_workpiece_reference"),
    ]
    for name in ROD_NAMES:
        children.extend(
            (
                _motion_occurrence(build_rod(name, 0.0, p), f"motion_full_{name}_rod"),
                _motion_occurrence(build_cap("left", name, 0.0, p), f"motion_full_left_{name}_cap"),
                _motion_occurrence(build_cap("right", name, 0.0, p), f"motion_full_right_{name}_cap"),
            )
        )
    return Compound(
        children=children,
        label=f"P19_R1_full_motion_open__{provenance_token(p)}",
    )


def p19_r1_manifest(p: P19R1Parameters = P19_R1_DEFAULTS) -> dict[str, object]:
    return {
        "candidateStatus": "P19 R1 cycle-4 front-edge short-tail CAD candidate",
        "physicalAcceptanceClaimed": False,
        "contractPath": P19_R1_DESIGN_CONTRACT_PATH,
        "contractSha256": P19_R1_DESIGN_CONTRACT_SHA256,
        "parameters": asdict(p),
        "derived": {
            "innerClearSpanMm": p.inner_clear_span,
            "principalStackWidthMm": p.principal_stack_width,
            "rodLengthMm": p.rod_length_target,
            "centerAxleTotalLengthMm": p.center_axle_total_length,
            "innerHexCircumradiusMm": p.inner_hex_bore_circumradius,
        },
        "states": {
            state: {
                "theta_deg": theta,
                "alpha_left_deg": alpha_left(theta),
                "alpha_right_deg": alpha_right(theta),
            }
            for state, theta in STATE_THETA.items()
        },
        "guides": {
            name: {
                "open": GUIDES[name].open.as_tuple(),
                "contact": GUIDES[name].contact.as_tuple(),
                "end": GUIDES[name].end.as_tuple(),
                "travel": GUIDES[name].travel,
                "firstContactProgress": first_contact_progress(name, p),
            }
            for name in ROD_NAMES
        },
        "synchronizedMotion": {
            "sharedProgress": "u in [0,1]",
            "leftRotation": "-theta*u",
            "rightRotation": "+theta*u",
            "worldRodAuthority": "motion_state(u)",
            "outerRailsDerivedBy": "q_s_i(u)=R(-alpha_s(u))*(p_i(u)-C)",
            "manualRailExtension": False,
            "outerRailCenterTravelMm": {
                f"{side}:{name}": outer_rail_center_travel(side, name, p)
                for side in ("left", "right")
                for name in ROD_NAMES
            },
        },
        "centerAxle": {
            "fixedMember": "purple printed stepped axle",
            "onePiece": True,
            "worldInvariant": True,
            "outerRotationCenterYZ": outer_rotation_center_yz(p).as_tuple(),
            "fixedAxleCenterYZ": fixed_axle_center_yz(p).as_tuple(),
            "keeperCount": 2,
            "doesNotCoupleOuterRotation": True,
        },
        "whiteRods": {
            "count": 3,
            "roles": ROD_NAMES,
            "moving": True,
            "diameterMm": p.rod_diameter,
            "lengthMm": p.rod_length_target,
        },
        "caps": {
            "count": 6,
            "strategy": "permanent",
        },
        "endpoint": {
            "thetaDeg": p.theta_end_deg,
            "meaning": "end-of-travel only",
            "selfLockClaimed": False,
        },
        "workpieceOrientation": workpiece_orientation_evidence(p),
        "interfaceEvidence": interface_alignment_evidence(p),
        "nonGoals": (
            "manual rail extension",
            "new linkage or grip",
            "endpoint lock or self-lock claim",
            "physical force or fit claim",
        ),
    }


def manifest_sha256(p: P19R1Parameters = P19_R1_DEFAULTS) -> str:
    return sha256(json.dumps(p19_r1_manifest(p), sort_keys=True).encode("utf-8")).hexdigest()


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def provenance_token(p: P19R1Parameters = P19_R1_DEFAULTS) -> str:
    return f"manifest_{manifest_sha256(p)[:12]}__source_{source_revision_sha256()[:12]}"


def clear_geometry_caches() -> None:
    _inner_plate_local.cache_clear()
    _outer_plate_local.cache_clear()
    actual_solid_motion_evidence.cache_clear()
    two_sided_support_evidence.cache_clear()
    _completed_pigtail_seated.cache_clear()
    _completed_pigtail_service_evidence.cache_clear()
    interface_alignment_evidence.cache_clear()
    short_tail_service_evidence.cache_clear()


__all__ = [
    "P19R1Parameters",
    "P19_R1_DEFAULTS",
    "PHYSICAL_STAINLESS_STOCK_LENGTH_MM",
    "GUIDES",
    "ROD_NAMES",
    "STATE_THETA",
    "MotionState",
    "motion_state",
    "alpha_left",
    "alpha_right",
    "outer_rail_center_travel",
    "wire_surface_clearance",
    "first_contact_progress",
    "build_artifact",
    "build_center_axle",
    "build_center_axle_coupon",
    "build_fixed_axle_focus_state",
    "build_full_motion_open",
    "build_completed_pigtail_removal_sweep",
    "build_motion_state",
    "build_service_envelopes",
    "build_slot_fit_coupon",
    "clear_geometry_caches",
    "completed_pigtail_removal_states",
    "completed_pigtail_removal_waypoints",
    "combined_contact_closure_evidence",
    "conditioning_evidence",
    "derive_mating_rail",
    "central_span_service_evidence",
    "fixed_axle_actual_solid_evidence",
    "fixed_axle_center_yz",
    "fixed_axle_guide_local_center",
    "fixed_axle_guide_locus",
    "fixed_occurrence_transform_evidence",
    "fixed_guide_locus",
    "manifest_sha256",
    "actual_solid_motion_evidence",
    "cap_stack_closure_evidence",
    "inverse_rail_reconstruction_evidence",
    "interface_alignment_evidence",
    "legacy_validator_collision_regression_evidence",
    "rail_branch_regularity_evidence",
    "outer_pose_constraint_jacobian",
    "outer_pose_constraint_residuals",
    "outer_slot_local_center",
    "outer_slot_locus",
    "outer_rotation_center_yz",
    "parameters_from_env",
    "parameters_from_overrides",
    "p19_r1_manifest",
    "reconstruct_fixed_axle_from_outer",
    "reconstruct_world_from_outer",
    "rod_center",
    "rotation_for_side",
    "service_clearance_evidence",
    "short_tail_service_evidence",
    "theta_contact_deg",
    "triangle_motion_evidence",
    "triangle_motion_math_evidence",
    "transform_point_between_frames",
    "two_sided_support_evidence",
    "workpiece_orientation_evidence",
    "source_revision_sha256",
]
