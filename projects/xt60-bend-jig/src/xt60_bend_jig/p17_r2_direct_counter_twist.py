"""P17 R2 direct-CAD counter-twist XT60 bend-jig candidate.

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
StateName = Literal["open", "mid", "contact", "locked"]
ArtifactName = Literal[
    "open",
    "mid",
    "contact",
    "locked",
    "exploded",
    "print_kit",
    "permanent_cap_coupon",
    "center_axle_coupon",
]

ROD_NAMES: tuple[RodName, ...] = ("upright", "bottom", "diagonal")
TRIANGLE_VERTEX_ORDER: tuple[RodName, ...] = ("bottom", "diagonal", "upright")
PHYSICAL_STAINLESS_STOCK_LENGTH_MM = 50.00
STATE_THETA: dict[StateName, float] = {
    "open": 0.0,
    "mid": 12.0,
    "contact": 23.4331751998,
    "locked": 24.0,
}
P17_R2_DESIGN_CONTRACT_PATH = (
    "docs/iterations/p17-r2-locked-rod-layout/DESIGN.md"
)
P17_R2_DESIGN_CONTRACT_SHA256 = (
    "0133dc4d45f38e91a20311d490b9b2fef2c8c0c6a07081c6b0c75fb19d620f95"
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


D13_COMMON_ROD_DELTA = PointYZ(16.1869657526, 10.2949747468)


I07_ACCEPTED_END_CENTERS: dict[RodName, PointYZ] = {
    "bottom": PointYZ(6.8, 24.9),
    "diagonal": PointYZ(14.2849242405, 16.4849242405),
    "upright": PointYZ(22.7, 9.0),
}


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
    locked: PointYZ

    @property
    def direction(self) -> PointYZ:
        length = self.open.distance_to(self.locked)
        return PointYZ(
            (self.locked.y - self.open.y) / length,
            (self.locked.z - self.open.z) / length,
        )

    @property
    def travel(self) -> float:
        return self.open.distance_to(self.locked)


@dataclass(frozen=True, slots=True)
class P17R2Parameters:
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
    inner_plate_diameter: float = 80.00
    left_outer_secondary_grip_diameter: float = 82.00
    right_outer_primary_grip_diameter: float = 85.00
    fixed_slot_width: float = 4.15
    outer_slot_width: float = 4.15
    slot_endpoint_margin: float = 1.40
    slot_sample_count: int = 33
    validation_sample_count: int = 65
    theta_lock_deg: float = 24.00
    min_web_mm: float = 2.20

    # D06 separates the unchanged outer-rotation datum C from the fixed purple
    # stepped-axle datum A.  Inner plate outlines and every frozen white-rod/
    # guide/cam construction remain authored about C; only the inner hex bores,
    # stepped axle and keepers move to A.
    outer_rotation_center_y: float = 3.00
    outer_rotation_center_z: float = 12.00
    fixed_axle_center_y: float = -29.00
    fixed_axle_center_z: float = 12.00
    fixed_axle_guide_sample_count: int = 33

    # Reference-only workpiece envelopes.
    xt60_body_y: float = 8.10
    xt60_body_z: float = 20.50
    xt60_body_center_y: float = -6.500
    xt60_body_center_z: float = 22.500
    wire_envelope_diameter: float = 4.30
    wire_preload: float = 0.25
    bend_center_y: float = -0.500
    bend_center_z: float = 3.500
    bend_radius: float = 6.00
    service_clearance_min: float = 0.75
    slot_fit_coupon_widths: tuple[float, ...] = (4.10, 4.15, 4.20, 4.25, 4.30)
    completed_pigtail_extract_end_y: float = 17.265

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
            raise ValueError("P17 R2 inner clear span must stay in 17.90..19.50 mm")
        if abs(self.rod_length_target - PHYSICAL_STAINLESS_STOCK_LENGTH_MM) > 1.0e-9:
            raise ValueError("P17 R2 must use all three uncut OD4 x 50.00 mm rods")
        if self.cap_socket_id < self.rod_diameter:
            raise ValueError("P17 R2 permanent cap default must not be an interference socket")
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
            raise ValueError("P17 D05 requires keeper OD10.00 / bore7.55 mm")
        if self.keeper_radial_wall_min < 1.20:
            raise ValueError("keeper radial wall must be at least 1.20 mm")
        if self.slot_sample_count < 5 or self.slot_sample_count % 2 == 0:
            raise ValueError("slot_sample_count must be odd and at least 5")
        if self.fixed_axle_guide_sample_count < 33 or self.fixed_axle_guide_sample_count % 2 == 0:
            raise ValueError("fixed axle guide requires an odd sample count of at least 33")
        if self.validation_sample_count < 65 or self.validation_sample_count % 2 == 0:
            raise ValueError("three-rod validation requires an odd sample count of at least 65")
        if self.fixed_slot_width != 4.15 or self.outer_slot_width != 4.15:
            raise ValueError("P17 three-rod contract requires 4.15 mm moving slots")
        if self.theta_lock_deg != 24.0:
            raise ValueError("P17 three-rod contract requires a 24 degree endpoint")


P17_R2_DEFAULTS = P17R2Parameters()

SERVICE_WAYPOINTS: tuple[ServicePose, ...] = (
    ServicePose(0.0, 0.0, 0.0),
    ServicePose(-4.0, 10.0, -15.0),
    ServicePose(-4.0, 50.0, -15.0),
)

I10_GUIDES: dict[RodName, GuidePath] = {
    "bottom": GuidePath(
        "bottom",
        PointYZ(-20.9852813742, 9.5000000000),
        PointYZ(-10.6500000000, 9.5000000000),
        PointYZ(-10.4000000000, 9.5000000000),
    ),
    "diagonal": GuidePath(
        "diagonal",
        PointYZ(5.5000000000, 9.5000000000),
        PointYZ(-1.8081475452, 2.1918524548),
        PointYZ(-1.9849242405, 2.0150757595),
    ),
    "upright": GuidePath(
        "upright",
        PointYZ(5.5000000000, -16.9852813742),
        PointYZ(5.5000000000, -6.6500000000),
        PointYZ(5.5000000000, -6.4000000000),
    ),
}


def _translate_guide(guide: GuidePath, delta: PointYZ) -> GuidePath:
    def moved(point: PointYZ) -> PointYZ:
        return PointYZ(point.y + delta.y, point.z + delta.z)

    return GuidePath(
        guide.name,
        moved(guide.open),
        moved(guide.contact),
        moved(guide.locked),
    )


GUIDES: dict[RodName, GuidePath] = {
    name: _translate_guide(guide, D13_COMMON_ROD_DELTA)
    for name, guide in I10_GUIDES.items()
}


def parameters_from_overrides(overrides: dict[str, object] | None = None) -> P17R2Parameters:
    overrides = overrides or {}
    unknown = set(overrides) - {field.name for field in fields(P17R2Parameters)}
    if unknown:
        raise ValueError(f"unknown P17 R2 parameter(s): {sorted(unknown)}")
    return replace(P17_R2_DEFAULTS, **overrides)


def parameters_from_env() -> P17R2Parameters:
    raw = os.environ.get("P17_R2_PARAMS_JSON", "").strip()
    overrides = json.loads(raw) if raw else {}
    return parameters_from_overrides(overrides)


def alpha_left(theta_deg: float) -> float:
    return -theta_deg


def alpha_right(theta_deg: float) -> float:
    return theta_deg


def rotation_for_side(side: SideName, theta_deg: float) -> float:
    return alpha_left(theta_deg) if side == "left" else alpha_right(theta_deg)


def _rotate_yz(point: PointYZ, angle_deg: float) -> PointYZ:
    a = radians(angle_deg)
    return PointYZ(
        point.y * cos(a) - point.z * sin(a),
        point.y * sin(a) + point.z * cos(a),
    )


def outer_rotation_center_yz(p: P17R2Parameters = P17_R2_DEFAULTS) -> PointYZ:
    """World YZ center C for both independently rotating outer plates."""
    return PointYZ(p.outer_rotation_center_y, p.outer_rotation_center_z)


def fixed_axle_center_yz(p: P17R2Parameters = P17_R2_DEFAULTS) -> PointYZ:
    """World YZ center A of the fixed purple stepped axle."""
    return PointYZ(p.fixed_axle_center_y, p.fixed_axle_center_z)


def pivot_yz(p: P17R2Parameters = P17_R2_DEFAULTS) -> PointYZ:
    """Compatibility name for the frozen outer-rotation center C."""
    return outer_rotation_center_yz(p)


def _relative_to_pivot(point: PointYZ, p: P17R2Parameters) -> PointYZ:
    pivot = outer_rotation_center_yz(p)
    return PointYZ(point.y - pivot.y, point.z - pivot.z)


def _world_from_pivot(local: PointYZ, p: P17R2Parameters) -> PointYZ:
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

    This is the single deterministic authority used for the D13 mating rails:
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


def rod_center(name: RodName, theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> PointYZ:
    guide = GUIDES[name]
    u = max(0.0, min(1.0, theta_deg / p.theta_lock_deg))
    return PointYZ(
        guide.open.y + (guide.locked.y - guide.open.y) * u,
        guide.open.z + (guide.locked.z - guide.open.z) * u,
    )


def outer_slot_local_center(side: SideName, name: RodName, theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> PointYZ:
    u = max(0.0, min(1.0, theta_deg / p.theta_lock_deg))
    return derive_mating_rail(
        lambda progress: rod_center(name, p.theta_lock_deg * progress, p),
        (u,),
        source_origin=PointYZ(0.0, 0.0),
        source_total_rotation_deg=0.0,
        target_origin=outer_rotation_center_yz(p),
        target_total_rotation_deg=rotation_for_side(side, p.theta_lock_deg),
    )[0]


def reconstruct_world_from_outer(side: SideName, name: RodName, theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> PointYZ:
    local = outer_slot_local_center(side, name, theta_deg, p)
    return _world_from_pivot(_rotate_yz(local, rotation_for_side(side, theta_deg)), p)


def outer_slot_locus(side: SideName, name: RodName, p: P17R2Parameters = P17_R2_DEFAULTS) -> tuple[PointYZ, ...]:
    progress = tuple(index / (p.slot_sample_count - 1) for index in range(p.slot_sample_count))
    return derive_mating_rail(
        lambda u: rod_center(name, p.theta_lock_deg * u, p),
        progress,
        source_origin=PointYZ(0.0, 0.0),
        source_total_rotation_deg=0.0,
        target_origin=outer_rotation_center_yz(p),
        target_total_rotation_deg=rotation_for_side(side, p.theta_lock_deg),
    )


def fixed_axle_guide_local_center(
    side: SideName,
    theta_deg: float,
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> PointYZ:
    """Part-local center of fixed axle A in an outer plate at ``theta_deg``."""
    center = outer_rotation_center_yz(p)
    axle = fixed_axle_center_yz(p)
    offset = PointYZ(axle.y - center.y, axle.z - center.z)
    return _rotate_yz(offset, -rotation_for_side(side, theta_deg))


def fixed_axle_guide_locus(
    side: SideName,
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> tuple[PointYZ, ...]:
    return tuple(
        fixed_axle_guide_local_center(
            side,
            p.theta_lock_deg * index / (p.fixed_axle_guide_sample_count - 1),
            p,
        )
        for index in range(p.fixed_axle_guide_sample_count)
    )


def reconstruct_fixed_axle_from_outer(
    side: SideName,
    theta_deg: float,
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> PointYZ:
    local = fixed_axle_guide_local_center(side, theta_deg, p)
    return _world_from_pivot(
        _rotate_yz(local, rotation_for_side(side, theta_deg)), p
    )


def fixed_guide_locus(name: RodName, p: P17R2Parameters = P17_R2_DEFAULTS) -> tuple[PointYZ, PointYZ]:
    guide = GUIDES[name]
    direction = guide.direction
    return (
        PointYZ(
            guide.open.y - direction.y * p.slot_endpoint_margin,
            guide.open.z - direction.z * p.slot_endpoint_margin,
        ),
        PointYZ(
            guide.locked.y + direction.y * p.slot_endpoint_margin,
            guide.locked.z + direction.z * p.slot_endpoint_margin,
        ),
    )


def fixed_guide_local_locus(name: RodName, p: P17R2Parameters = P17_R2_DEFAULTS) -> tuple[PointYZ, PointYZ]:
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
def _inner_plate_local(side: SideName, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
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
def _outer_plate_local(side: SideName, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
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


def build_inner_plate(side: SideName, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
    x = p.left_inner_x if side == "left" else p.right_inner_x
    pivot = outer_rotation_center_yz(p)
    return _label(
        Pos(x, pivot.y, pivot.z) * copy(_inner_plate_local(side, p)),
        _inner_plate_local(side, p).label,
        "#D89A19",
    )


def build_outer_plate(side: SideName, theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
    x = p.left_outer_x if side == "left" else p.right_outer_x
    color = "#377A3A" if side == "left" else "#2D6FA8"
    pivot = outer_rotation_center_yz(p)
    return _label(
        Pos(x, pivot.y, pivot.z) * Rot(rotation_for_side(side, theta_deg), 0.0, 0.0) * copy(_outer_plate_local(side, p)),
        _outer_plate_local(side, p).label,
        color,
    )


def build_center_axle(p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
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


def _keeper_local(p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
    # D05 print-ready retained lobe: OD10 / bore7.55 gives 1.225 mm radial wall.
    keeper = _x_cylinder(p.keeper_outer_diameter, p.outer_keeper_thickness, 0.0, 0.0, 0.0)
    bore = _x_cylinder(p.keeper_bore_diameter, p.outer_keeper_thickness + 1.0, 0.0, 0.0, 0.0)
    return keeper - bore


def build_keeper(side: SideName, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
    x = p.keeper_left_x if side == "left" else p.keeper_right_x
    pivot = fixed_axle_center_yz(p)
    keeper = Pos(x, pivot.y, pivot.z) * _keeper_local(p)
    return _label(
        keeper,
        f"{side}_permanent_press_fit_outer_keeper_on_real_seat_clearance_{p.keeper_axial_running_clearance:.2f}",
        "#111111",
    )


def build_rod(name: RodName, theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
    center = rod_center(name, theta_deg, p)
    return _label(
        _x_cylinder(p.rod_diameter, p.rod_length_target, 0.0, center.y, center.z),
        f"{name}_OD4_rod_L{p.rod_length_target:.2f}",
        "#B7B7B7",
    )


def _cap_local(
    p: P17R2Parameters = P17_R2_DEFAULTS,
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


def build_cap(side: SideName, name: RodName, theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
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


def build_xt60_reference(p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
    body = Pos(0.0, p.xt60_body_center_y, p.xt60_body_center_z) * Box(
        p.xt60_body_width_x,
        p.xt60_body_y,
        p.xt60_body_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return _label(body, "reference_only_XT60_body_envelope_not_load_path", "#C8E6FF")


def build_workpiece_reference(theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
    # Frozen I10 front view is a true head-up/tail-right "└": the short leg descends
    # from the XT60 head at Y=B_y-R, turns through the lower-left quadrant,
    # and leaves horizontally toward +Y. Both conductors differ only in X.
    wires: list[Shape] = []
    vertical_tangent_z = p.bend_center_z
    vertical_length = p.xt60_body_center_z - vertical_tangent_z
    horizontal_tangent_y = p.bend_center_y
    horizontal_length = 12.0
    for x in (-3.60, 3.60):
        incoming = _z_cylinder(
            p.wire_envelope_diameter,
            vertical_length,
            x,
            p.bend_center_y - p.bend_radius,
            vertical_tangent_z + vertical_length / 2.0,
        )
        full_bend = Pos(x, p.bend_center_y, p.bend_center_z) * Torus(
            p.bend_radius,
            p.wire_envelope_diameter / 2.0,
            rotation=(0.0, -90.0, 0.0),
        )
        quadrant_extent = p.bend_radius + p.wire_envelope_diameter / 2.0 + 0.10
        bend_clip = Pos(
            x,
            p.bend_center_y - quadrant_extent / 2.0,
            p.bend_center_z - quadrant_extent / 2.0,
        ) * Box(
            p.wire_envelope_diameter + 1.0,
            quadrant_extent,
            quadrant_extent,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        bend = full_bend & bend_clip
        outgoing = _y_cylinder(
            p.wire_envelope_diameter,
            horizontal_length,
            x,
            horizontal_tangent_y + horizontal_length / 2.0,
            p.bend_center_z - p.bend_radius,
        )
        wires.append(incoming + bend + outgoing)
    workpiece = wires[0] + wires[1]
    workpiece.label = f"reference_wire_envelopes_theta_{theta_deg:.1f}_not_load_path"
    workpiece.color = srgb("#F1C84B", 0.45)
    return workpiece


def completed_pigtail_removal_waypoints(
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> tuple[ServicePose, ...]:
    """D10-R1 service path rederived for the head-up/tail-right workpiece."""
    del p
    return SERVICE_WAYPOINTS


@lru_cache(maxsize=8)
def _completed_pigtail_seated(
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> Compound:
    """One cached final pigtail solid; service states are rigid transforms."""
    body = build_xt60_reference(p)
    body.label = "completed_pigtail_XT60_body"
    wires = build_workpiece_reference(0.0, p)
    wires.label = "completed_pigtail_two_separated_bent_wires"
    parts: list[Shape] = [body, wires]
    body_bottom_z = p.xt60_body_center_z - p.xt60_body_z / 2.0
    for x in (-3.60, 3.60):
        joint = _z_cylinder(
            6.00,
            4.00,
            x,
            p.xt60_body_center_y,
            body_bottom_z + 2.0,
        )
        joint.label = f"completed_pigtail_solder_joint_x_{x:+.2f}"
        parts.append(joint)
    return Compound(children=parts, label="completed_pigtail_seated_actual_envelope")


def _completed_pigtail_at(
    pose: ServicePose,
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> Shape:
    """Final actual body, two solder joints and two bent wires at one pose."""
    seated = copy(_completed_pigtail_seated(p))
    transformed = (
        Pos(0.0, pose.delta_y, pose.delta_z)
        * Pos(0.0, p.xt60_body_center_y, p.xt60_body_center_z)
        * Rot(pose.phi_deg, 0.0, 0.0)
        * Pos(0.0, -p.xt60_body_center_y, -p.xt60_body_center_z)
        * seated
    )
    return _label(
        transformed,
        (
            "completed_pigtail_actual_service_pose_"
            f"dy_{pose.delta_y:.3f}_dz_{pose.delta_z:.3f}_phi_{pose.phi_deg:.3f}"
        ),
        "#73A6FF",
    )


def completed_pigtail_removal_states(
    p: P17R2Parameters = P17_R2_DEFAULTS,
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> Compound:
    children = [shape for _, shape in completed_pigtail_removal_states(p)]
    return Compound(
        children=children,
        label="completed_pigtail_actual_D10_R1_rigid_body_removal_sweep",
    )


def build_service_envelopes(theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
    """D10 head-up/tail-right solder, heat-shrink, tool and removal space."""
    shapes: list[Shape] = []
    body_bottom_z = p.xt60_body_center_z - p.xt60_body_z / 2.0
    horizontal_start_y = p.bend_center_y
    for x in (-3.60, 3.60):
        solder = _z_cylinder(
            5.50, 4.00, x, p.xt60_body_center_y, body_bottom_z + 2.0
        )
        solder.label = f"reference_solder_joint_x_{x:+.2f}"
        solder.color = srgb("#E36B4A", 0.24)
        heat_shrink = _y_cylinder(
            6.00,
            12.00,
            x,
            horizontal_start_y + 6.0,
            p.bend_center_z - p.bend_radius,
        )
        heat_shrink.label = f"reference_heat_shrink_x_{x:+.2f}"
        heat_shrink.color = srgb("#555555", 0.16)
        outgoing = _y_cylinder(
            p.wire_envelope_diameter,
            30.00,
            x,
            horizontal_start_y + 15.0,
            p.bend_center_z - p.bend_radius,
        )
        outgoing.label = f"reference_outgoing_wire_x_{x:+.2f}"
        outgoing.color = srgb("#F1C84B", 0.18)
        tool = Pos(x, p.xt60_body_center_y, body_bottom_z + 2.0) * Box(
            8.00,
            8.00,
            10.00,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        tool.label = f"reference_soldering_tool_keepout_x_{x:+.2f}"
        tool.color = srgb("#9C6ADE", 0.08)
        shapes.extend((solder, heat_shrink, outgoing, tool))
    if abs(theta_deg) <= 1.0e-9:
        removal = build_completed_pigtail_removal_sweep(p)
        removal.color = srgb("#73A6FF", 0.06)
        shapes.append(removal)
    return Compound(children=shapes, label=f"reference_service_envelopes_theta_{theta_deg:.1f}")


def build_motion_state(state: StateName, p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
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
    return Compound(children=children, label=f"P17_R2_{state}_direct_counter_twist_center_axle")


def build_exploded(p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
    parts = [
        Pos(-4 * p.exploded_spacing_x, 0, 0) * build_outer_plate("left", 0.0, p),
        Pos(-3 * p.exploded_spacing_x, 0, 0) * build_keeper("left", p),
        Pos(-2 * p.exploded_spacing_x, 0, 0) * build_inner_plate("left", p),
        Pos(0, 0, 0) * build_center_axle(p),
        Pos(2 * p.exploded_spacing_x, 0, 0) * build_inner_plate("right", p),
        Pos(3 * p.exploded_spacing_x, 0, 0) * build_keeper("right", p),
        Pos(4 * p.exploded_spacing_x, 0, 0) * build_outer_plate("right", p.theta_lock_deg, p),
    ]
    for idx, name in enumerate(ROD_NAMES):
        parts.append(Pos(0, -44, idx * 9 - 9) * build_rod(name, 0.0, p))
        parts.append(Pos(-24, -58, idx * 9 - 9) * build_cap("left", name, 0.0, p))
        parts.append(Pos(24, -58, idx * 9 - 9) * build_cap("right", name, 0.0, p))
    return Compound(children=parts, label="P17_R2_exploded_all_production_parts")


def _lay_flat(shape: Shape) -> Shape:
    return Rot(0.0, -90.0, 0.0) * shape


def _center_on_bed(shape: Shape) -> Shape:
    bounds = shape.bounding_box()
    return Pos(
        -(bounds.min.X + bounds.max.X) / 2.0,
        -(bounds.min.Y + bounds.max.Y) / 2.0,
        -bounds.min.Z,
    ) * shape


def build_print_kit(p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
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
    return Compound(children=children, label="P17_R2_print_kit_printed_parts_only_no_rods")


def build_permanent_cap_coupon(p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
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
    base.label = "coupon_label_base_P17_R2_permanent_cap_ladder"
    children.append(base)
    children.append(Pos(0.0, 62.0, 0.0) * build_slot_fit_coupon(p))
    return Compound(children=children, label="P17_R2_permanent_cap_coupon_ID_ladder")


def build_slot_fit_coupon(p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
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
    return Compound(children=children, label="P17_R2_slot_fit_coupon_straight_and_curved_4p10_to_4p30")


def build_center_axle_coupon(p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
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
        label="P17_R2_center_axle_bearing_hex_keeper_retention_coupon_ladder",
    )


def build_artifact(name: ArtifactName, p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
    builders = {
        "open": lambda: build_motion_state("open", p),
        "mid": lambda: build_motion_state("mid", p),
        "contact": lambda: build_motion_state("contact", p),
        "locked": lambda: build_motion_state("locked", p),
        "exploded": lambda: build_exploded(p),
        "print_kit": lambda: build_print_kit(p),
        "permanent_cap_coupon": lambda: build_permanent_cap_coupon(p),
        "center_axle_coupon": lambda: build_center_axle_coupon(p),
    }
    if name not in builders:
        raise ValueError(f"unknown P17 R2 artifact {name!r}")
    artifact = builders[name]()
    return Compound(children=[artifact], label=f"P17_R2_ARTIFACT_{name}__{provenance_token(p)}")


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
    p: P17R2Parameters,
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
    p: P17R2Parameters,
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
    p: P17R2Parameters,
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    """D10 service proof: actual BREP plus dense full-component reconstruction."""
    production = _open_production_solids(p)
    production_compound = Compound(
        children=list(production.values()),
        label="D10_R1_all_final_open_production_solids",
    )
    brep_minimum = float("inf")
    brep_rows: dict[str, object] = {}
    maximum_intersection = 0.0
    for segment_index, sample_index, pose in _service_pose_samples(1001):
        pigtail = _completed_pigtail_at(pose, p)
        clearance = float(pigtail.distance(production_compound))
        intersection = (
            _intersection_volume(pigtail, production_compound)
            if clearance <= 1.0e-8
            else 0.0
        )
        brep_minimum = min(brep_minimum, clearance)
        maximum_intersection = max(maximum_intersection, intersection)
        key = f"segment_{segment_index}:sample_{sample_index:04d}"
        brep_rows[key] = {
            "clearanceMm": clearance,
            "intersectionMm3": intersection,
        }

    # The dense reconstruction evaluates every final obstacle family and every
    # final pigtail feature. X-separated plate/cap/keeper gaps are exact because
    # the path rotates only about X; rods/axle use exact YZ centerline envelopes.
    pigtail_half_x = max(
        p.xt60_body_width_x / 2.0,
        3.60 + 3.00,
        3.60 + p.wire_envelope_diameter / 2.0,
    )
    x_intervals = {
        "leftInnerPlate": (
            p.left_inner_x - p.inner_plate_thickness / 2.0,
            p.left_inner_x + p.inner_plate_thickness / 2.0,
        ),
        "rightInnerPlate": (
            p.right_inner_x - p.inner_plate_thickness / 2.0,
            p.right_inner_x + p.inner_plate_thickness / 2.0,
        ),
        "leftOuterPlate": (
            p.left_outer_x - p.outer_plate_thickness / 2.0,
            p.left_outer_x + p.outer_plate_thickness / 2.0,
        ),
        "rightOuterPlate": (
            p.right_outer_x - p.outer_plate_thickness / 2.0,
            p.right_outer_x + p.outer_plate_thickness / 2.0,
        ),
        "leftKeeper": (
            p.keeper_left_x - p.outer_keeper_thickness / 2.0,
            p.keeper_left_x + p.outer_keeper_thickness / 2.0,
        ),
        "rightKeeper": (
            p.keeper_right_x - p.outer_keeper_thickness / 2.0,
            p.keeper_right_x + p.outer_keeper_thickness / 2.0,
        ),
    }
    for name in ROD_NAMES:
        x_intervals[f"left{name.title()}Cap"] = (
            p.left_cap_inner_face_x - p.follower_head_length,
            p.left_cap_inner_face_x,
        )
        x_intervals[f"right{name.title()}Cap"] = (
            p.right_cap_inner_face_x,
            p.right_cap_inner_face_x + p.follower_head_length,
        )
    axial_gaps = {
        name: max(minimum - pigtail_half_x, -pigtail_half_x - maximum, 0.0)
        for name, (minimum, maximum) in x_intervals.items()
    }
    analytic_minima: dict[str, float] = dict(axial_gaps)
    feature_minima = {
        "xt60Body": float("inf"),
        "solderJoints": float("inf"),
        "twoBentWires": float("inf"),
    }
    for _segment_index, _sample_index, pose in _service_pose_samples(1001):
        for name in ROD_NAMES:
            local = _inverse_service_point(GUIDES[name].open, pose, p)
            feature_gaps = _pigtail_feature_clearances_to_x_member(
                local, p.rod_diameter / 2.0, p
            )
            analytic_minima[f"{name}Rod"] = min(
                analytic_minima.get(f"{name}Rod", float("inf")),
                *feature_gaps.values(),
            )
            for feature, gap in feature_gaps.items():
                feature_minima[feature] = min(feature_minima[feature], gap)
        axle_local = _inverse_service_point(fixed_axle_center_yz(p), pose, p)
        axle_gaps = _pigtail_feature_clearances_to_x_member(
            axle_local,
            p.center_axle_central_hex_af / sqrt(3.0),
            p,
        )
        analytic_minima["centerAxle"] = min(
            analytic_minima.get("centerAxle", float("inf")),
            *axle_gaps.values(),
        )
        for feature, gap in axle_gaps.items():
            feature_minima[feature] = min(feature_minima[feature], gap)
    analytic_minimum = min(analytic_minima.values())
    minimum = min(brep_minimum, analytic_minimum)
    segment_count = len(SERVICE_WAYPOINTS) - 1
    return {
        "pathId": "P17-D10-R1",
        "waypoints": tuple(
            (pose.delta_y, pose.delta_z, pose.phi_deg) for pose in SERVICE_WAYPOINTS
        ),
        "interpolation": "piecewise-linear in dy,dz,phi_deg",
        "brepSamplesPerSegment": 1001,
        "brepSampleCount": segment_count * 1001,
        "brepMinimumClearanceMm": brep_minimum,
        "brepMaximumIntersectionMm3": maximum_intersection,
        "brepRows": brep_rows,
        "analyticSamplesPerSegment": 1001,
        "analyticSampleCount": segment_count * 1001,
        "analyticMinimumClearanceMm": analytic_minimum,
        "analyticMinimumByProductionSolidMm": analytic_minima,
        "analyticMinimumByPigtailFeatureMm": feature_minima,
        "includedPigtailFeatures": ("XT60 body", "two solder joints", "two bent wires"),
        "includedProductionSolids": tuple(production),
        "minimumClearanceMm": minimum,
        "zeroIntersection": maximum_intersection <= 1.0e-7 and analytic_minimum >= 0.0,
        "passes": maximum_intersection <= 1.0e-7
        and minimum + 1.0e-9 >= p.service_clearance_min,
    }


def service_clearance_evidence(p: P17R2Parameters = P17_R2_DEFAULTS) -> dict[str, object]:
    """Actual-solid pivot service plus the revalidated D10 extraction gate."""
    fixed = {
        "center_axle": build_center_axle(p),
        "left_keeper": build_keeper("left", p),
        "right_keeper": build_keeper("right", p),
    }
    rows: dict[str, object] = {}
    minimum = float("inf")
    for index in range(9):
        theta = index * p.theta_lock_deg / 8.0
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
        "removalSequence": "full open -> revalidated D10 five-pose rigid-body removal path",
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
    p: P17R2Parameters,
) -> float:
    vertical_first = PointYZ(
        p.bend_center_y - p.bend_radius, p.bend_center_z
    )
    vertical_second = PointYZ(
        p.bend_center_y - p.bend_radius, p.xt60_body_center_z
    )
    horizontal_first = PointYZ(
        p.bend_center_y, p.bend_center_z - p.bend_radius
    )
    horizontal_second = PointYZ(
        p.bend_center_y + 12.0, p.bend_center_z - p.bend_radius
    )
    if name == "bottom":
        return _point_segment_distance_yz(center, vertical_first, vertical_second)
    if name == "upright":
        return _point_segment_distance_yz(center, horizontal_first, horizontal_second)
    angle = atan2(center.z - p.bend_center_z, center.y - p.bend_center_y)
    clamped_angle = max(-pi, min(-pi / 2.0, angle))
    arc_point = PointYZ(
        p.bend_center_y + p.bend_radius * cos(clamped_angle),
        p.bend_center_z + p.bend_radius * sin(clamped_angle),
    )
    return center.distance_to(arc_point)


def theta_contact_deg(p: P17R2Parameters = P17_R2_DEFAULTS) -> float:
    return p.theta_lock_deg * (
        GUIDES["upright"].travel - p.wire_preload
    ) / GUIDES["upright"].travel


def workpiece_orientation_evidence(
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    """Publish the frozen I10 front-view workpiece convention explicitly."""
    body_bottom_z = p.xt60_body_center_z - p.xt60_body_z / 2.0
    vertical_y = p.bend_center_y - p.bend_radius
    horizontal_z = p.bend_center_z - p.bend_radius
    return {
        "requirementIds": ("REQ-027",),
        "frontPlane": "world YZ",
        "screenRightAxis": "+Y",
        "screenUpAxis": "+Z",
        "frontViewForm": "└",
        "xt60BodyCenterYZ": (
            p.xt60_body_center_y,
            p.xt60_body_center_z,
        ),
        "xt60BodyBottomZMm": body_bottom_z,
        "bendCenterYZ": (p.bend_center_y, p.bend_center_z),
        "bendRadiusMm": p.bend_radius,
        "verticalLeg": {
            "yMm": vertical_y,
            "fromZMm": p.bend_center_z,
            "toZMm": p.xt60_body_center_z,
            "headDirection": "+Z",
        },
        "horizontalTail": {
            "zMm": horizontal_z,
            "fromYMm": p.bend_center_y,
            "toYMm": p.bend_center_y + 12.0,
            "tailDirection": "+Y",
        },
        "serviceExtractEndYMm": p.completed_pigtail_extract_end_y,
        "arcTangenciesYZ": {
            "vertical": (vertical_y, p.bend_center_z),
            "horizontal": (p.bend_center_y, horizontal_z),
        },
        "rodFeatureByIdentity": {
            "bottom": "upper-left vertical-leg former",
            "diagonal": "upper-right/middle bend-arc former",
            "upright": "lower-right horizontal-tail former",
        },
    }


def triangle_motion_evidence(
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    state_theta = {
        "open": 0.0,
        "contact": theta_contact_deg(p),
        "end": p.theta_lock_deg,
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
        "thetaEndDeg": p.theta_lock_deg,
        "commonStrokeMm": GUIDES["upright"].travel,
        "contactOffsetMm": expected_contact,
        "endOffsetMm": expected_end,
        "linearTravelLaw": "u=theta/theta_end",
        "endpointDerivativeMmPerDeg": GUIDES["upright"].travel / p.theta_lock_deg,
        "vertexOrder": TRIANGLE_VERTEX_ORDER,
        "rodVertexRole": ROD_VERTEX_ROLE,
        "openRightVerticalLegDeltaY": abs(
            GUIDES["diagonal"].open.y - GUIDES["upright"].open.y
        ),
        "acceptedEndDisplacementMmByRod": {
            name: GUIDES[name].locked.distance_to(I07_ACCEPTED_END_CENTERS[name])
            for name in ROD_NAMES
        },
        "maximumAcceptedEndDisplacementMm": max(
            GUIDES[name].locked.distance_to(I07_ACCEPTED_END_CENTERS[name])
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
    p: P17R2Parameters,
) -> PointYZ:
    step = 1.0e-4
    lower = max(0.0, theta_deg - step)
    upper = min(p.theta_lock_deg, theta_deg + step)
    first = outer_slot_local_center(side, name, lower, p)
    second = outer_slot_local_center(side, name, upper, p)
    return PointYZ(second.y - first.y, second.z - first.z)


def _crossing_sine(
    side: SideName,
    name: RodName,
    theta_deg: float,
    p: P17R2Parameters,
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
    p: P17R2Parameters,
) -> PointYZ:
    """D10-R1 exact dq/dtheta in millimetres per degree."""
    center = rod_center(name, theta_deg, p)
    relative = PointYZ(
        center.y - p.outer_rotation_center_y,
        center.z - p.outer_rotation_center_z,
    )
    travel_rate = GUIDES[name].travel / p.theta_lock_deg
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    """D10-R1 rail regularity, one-to-one branch and continuation proof."""
    sample_count = p.validation_sample_count
    sample_thetas = tuple(
        p.theta_lock_deg * index / (sample_count - 1)
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

    fixed_progress = GUIDES["upright"].travel / p.theta_lock_deg
    contact_travel = theta_contact_deg(p) / p.theta_lock_deg
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
                sign * radians(p.theta_lock_deg * travel),
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    sample_thetas = tuple(
        p.theta_lock_deg * index / (p.validation_sample_count - 1)
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    """Candidate-facing name for the frozen 3-rod triangle contract."""
    evidence = triangle_motion_evidence(p)
    evidence["sampleCount"] = p.validation_sample_count
    return evidence


def inverse_rail_reconstruction_evidence(
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    """All six inverse rod rails plus both fixed-axle rails."""
    evidence = rail_and_web_evidence(p)
    maximum_axle_residual = 0.0
    for side in ("left", "right"):
        for index in range(p.validation_sample_count):
            theta = p.theta_lock_deg * index / (p.validation_sample_count - 1)
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
def locked_layout_blocker_evidence(
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    """Detect, do not suppress, the frozen D13 product-interface blockers."""
    bottom_open = GUIDES["bottom"].open
    body_center = PointYZ(p.xt60_body_center_y, p.xt60_body_center_z)
    center_to_body = _point_rectangle_distance_yz(
        bottom_open,
        body_center,
        p.xt60_body_y / 2.0,
        p.xt60_body_z / 2.0,
    )
    signed_body_clearance = center_to_body - p.rod_diameter / 2.0
    vertical_wire_y = p.bend_center_y - p.bend_radius
    open_wire_centerline_separation = abs(bottom_open.y - vertical_wire_y)
    combined_wire_rod_radius = (
        p.rod_diameter + p.wire_envelope_diameter
    ) / 2.0
    open_wire_radial_overlap = (
        combined_wire_rod_radius - open_wire_centerline_separation
    )
    end_surface_gaps = {
        name: _wire_feature_offset(name, GUIDES[name].locked, p)
        - combined_wire_rod_radius
        for name in ROD_NAMES
    }
    infinite_straight_end_surface_gaps = {
        "bottom": abs(GUIDES["bottom"].locked.y - vertical_wire_y)
        - combined_wire_rod_radius,
        "upright": abs(
            GUIDES["upright"].locked.z
            - (p.bend_center_z - p.bend_radius)
        )
        - combined_wire_rod_radius,
    }
    open_rod = build_rod("bottom", 0.0, p)
    body = build_xt60_reference(p)
    wire = build_workpiece_reference(0.0, p)
    return {
        "candidate": "P17-D13 exact locked rod layout",
        "acceptanceClaimed": False,
        "knownInvalidProductInterface": True,
        "bottomOpenCenterYZ": bottom_open.as_tuple(),
        "xt60BodyCenterYZ": body_center.as_tuple(),
        "xt60BodyRectangleYZ": (
            p.xt60_body_center_y - p.xt60_body_y / 2.0,
            p.xt60_body_center_y + p.xt60_body_y / 2.0,
            p.xt60_body_center_z - p.xt60_body_z / 2.0,
            p.xt60_body_center_z + p.xt60_body_z / 2.0,
        ),
        "bottomOpenSignedBodyClearanceMm": signed_body_clearance,
        "bottomOpenBodyIntersectionMm3": _intersection_volume(open_rod, body),
        "verticalWireCenterlineY": vertical_wire_y,
        "bottomOpenWireCenterlineSeparationMm": open_wire_centerline_separation,
        "bottomOpenWireRadialOverlapMm": open_wire_radial_overlap,
        "bottomOpenWireIntersectionMm3": _intersection_volume(open_rod, wire),
        "endWireSurfaceGapMmByRod": end_surface_gaps,
        "endInfiniteStraightProxyGapMm": infinite_straight_end_surface_gaps,
        "lostEndContact": all(value > 0.0 for value in end_surface_gaps.values()),
        "physicalBoundary": (
            "review artifact only: known OPEN body/wire collision and lost END "
            "contact are intentionally materialized; no CAD, force, self-lock, "
            "fit, service, manufacturing or physical acceptance is claimed"
        ),
    }


@lru_cache(maxsize=None)
def actual_solid_motion_evidence(
    p: P17R2Parameters = P17_R2_DEFAULTS,
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
        theta = p.theta_lock_deg * index / (p.validation_sample_count - 1)
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
            build_rod(name, p.theta_lock_deg, p), wire
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
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
        theta = p.theta_lock_deg * index / (p.validation_sample_count - 1)
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
        ("end", p.theta_lock_deg, 1.0),
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    critical_thetas = (0.0, theta_contact_deg(p), p.theta_lock_deg)
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    evidence = _completed_pigtail_service_evidence(p)
    return {
        "pathId": evidence["pathId"],
        "sequence": "full open -> rederived three-pose rigid-body removal path",
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
        "analyticMinimumByProductionSolidMm": evidence[
            "analyticMinimumByProductionSolidMm"
        ],
        "analyticMinimumByPigtailFeatureMm": evidence[
            "analyticMinimumByPigtailFeatureMm"
        ],
        "includedPigtailFeatures": evidence["includedPigtailFeatures"],
        "includedProductionSolids": evidence["includedProductionSolids"],
        "minimumClearanceMm": evidence["minimumClearanceMm"],
        "zeroIntersection": evidence["zeroIntersection"],
        "passes": evidence["passes"],
        "finding": "D10-R1 full-component rigid-body removal sweep is clear",
    }


def fixed_occurrence_transform_evidence(
    p: P17R2Parameters = P17_R2_DEFAULTS,
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
    p: P17R2Parameters,
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
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
        index * p.theta_lock_deg / (p.fixed_axle_guide_sample_count - 1)
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
    p: P17R2Parameters,
) -> PointYZ:
    theta = p.theta_lock_deg * travel
    if contact == "fixed_axle":
        return fixed_axle_guide_local_center(side, theta, p)
    return outer_slot_local_center(side, contact, theta, p)  # type: ignore[arg-type]


def _combined_contact_residuals(
    side: SideName,
    travel: float,
    pose: tuple[float, float, float],
    p: P17R2Parameters,
) -> tuple[float, ...]:
    """Four nominal centerline normal residuals for one outer rigid pose.

    ``pose`` is ``(delta_y, delta_z, angle_radians)`` relative to C.  Slot
    tangent travel is eliminated locally, leaving one scalar path constraint
    per fixed contact.  This is a local mobility proof, not a force/fit claim.
    """
    center = outer_rotation_center_yz(p)
    world_contacts: tuple[tuple[str, PointYZ], ...] = (
        ("fixed_axle", fixed_axle_center_yz(p)),
        *((name, rod_center(name, p.theta_lock_deg * travel, p)) for name in ROD_NAMES),
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
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
    p: P17R2Parameters,
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> tuple[tuple[float, float, float], ...]:
    """Finite-difference Jacobian of :func:`outer_pose_constraint_residuals`."""
    return _combined_contact_jacobian(side, travel, pose, p)


def _solve_combined_contact_pose(
    side: SideName,
    travel: float,
    initial: tuple[float, float, float],
    p: P17R2Parameters,
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> dict[str, object]:
    rows: dict[str, object] = {}
    all_pass = True
    sample_count = p.validation_sample_count
    for side in ("left", "right"):
        sign = -1.0 if side == "left" else 1.0
        for index in range(sample_count):
            travel = index / (sample_count - 1)
            prescribed = (0.0, 0.0, sign * radians(p.theta_lock_deg * travel))
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
                "thetaDeg": p.theta_lock_deg * travel,
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
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
    contact_travel = theta_contact_deg(p) / p.theta_lock_deg
    for side in ("left", "right"):
        sign = -1.0 if side == "left" else 1.0
        for index, travel in enumerate((*base_travels, contact_travel)):
            pose = (0.0, 0.0, sign * radians(p.theta_lock_deg * travel))
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
                "thetaDeg": p.theta_lock_deg * travel,
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
    p: P17R2Parameters = P17_R2_DEFAULTS,
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
        label=f"P17_R2_fixed_axle_focus_theta_{theta_deg:.2f}__{provenance_token(p)}",
    )


def build_full_motion_open(
    p: P17R2Parameters = P17_R2_DEFAULTS,
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
        label=f"P17_R2_full_motion_open__{provenance_token(p)}",
    )


def p17_r2_manifest(p: P17R2Parameters = P17_R2_DEFAULTS) -> dict[str, object]:
    return {
        "candidateStatus": "exact D13 review materialization; known invalid product interface",
        "acceptanceClaimed": False,
        "contractPath": P17_R2_DESIGN_CONTRACT_PATH,
        "contractSha256": P17_R2_DESIGN_CONTRACT_SHA256,
        "fixedMember": "purple printed stepped center axle",
        "whiteRods": {
            "count": 3,
            "color": "white stainless",
            "roles": ROD_NAMES,
            "moving": True,
            "fixedReactionMember": False,
            "modeledTargetLengthMm": p.rod_length_target,
            "physicalStockLengthMm": PHYSICAL_STAINLESS_STOCK_LENGTH_MM,
            "stockUseDecision": "all three physical OD4 x 50.00 mm rods used uncut",
        },
        "parameters": asdict(p),
        "derived": {
            "inner_clear_span": p.inner_clear_span,
            "principal_stack_width": p.principal_stack_width,
            "rod_length_raw": p.rod_length_raw,
            "rod_length_target": p.rod_length_target,
            "center_axle_total_length": p.center_axle_total_length,
            "per_side_center_axle_length": p.per_side_center_axle_length,
            "left_inner_x": p.left_inner_x,
            "right_inner_x": p.right_inner_x,
            "left_outer_x": p.left_outer_x,
            "right_outer_x": p.right_outer_x,
            "right_primary_extra_lever_radius": p.right_primary_extra_lever_radius,
            "outer_bearing_bore_diameter": p.outer_bearing_bore_diameter,
            "inner_hex_bore_af": p.inner_hex_bore_af,
            "journal_outer_plate_overlap": p.journal_outer_plate_overlap,
            "journal_with_keeper_seat_length": p.journal_with_keeper_seat_length,
            "keeper_bore_diameter": p.keeper_bore_diameter,
            "keeper_outer_diameter": p.keeper_outer_diameter,
            "keeper_radial_wall_min": p.keeper_radial_wall_min,
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
                "locked": GUIDES[name].locked.as_tuple(),
                "travel": GUIDES[name].travel,
            }
            for name in ROD_NAMES
        },
        "lockedRodLayout": {
            "commonDeltaYZ": D13_COMMON_ROD_DELTA.as_tuple(),
            "workpieceMoved": False,
            "outerRailsDerivedBy": "derive_mating_rail(T_target^-1*T_source*p_source)",
            "knownBlockers": locked_layout_blocker_evidence(p),
        },
        "centerAxle": {
            "fixedMember": "purple printed stepped axle",
            "whiteRods": "all three OD4 rods remain moving forming rods",
            "onePiece": True,
            "worldInvariant": True,
            "outerRotationCenterYZ": outer_rotation_center_yz(p).as_tuple(),
            "fixedAxleCenterYZ": fixed_axle_center_yz(p).as_tuple(),
            "eccentricity": p.fixed_axle_eccentricity,
            "centralHexSpacerAf": p.center_axle_central_hex_af,
            "centralHexLength": p.inner_clear_span,
            "innerHexKeyAf": p.center_axle_inner_hex_af,
            "fixedInnerHexBoreAf": p.inner_hex_bore_af,
            "outerRoundJournalDiameter": p.outer_journal_diameter,
            "outerBearingBoreDiameter": p.outer_bearing_bore_diameter,
            "slideOverInvariant": p.outer_journal_diameter < p.inner_hex_bore_af,
            "keeperSeatLength": p.keeper_seat_length,
            "keeperBoreDiameter": p.keeper_bore_diameter,
            "keeperOuterDiameter": p.keeper_outer_diameter,
            "keeperRadialWallMin": p.keeper_radial_wall_min,
            "keeperCount": 2,
            "keeperStrategy": "separate permanent press-fit ring on modeled journal end seat; physical coupon required",
            "doesNotCoupleOuterRotation": True,
        },
        "caps": {
            "count": 6,
            "strategy": "permanent",
            "defaultSocketId": p.cap_socket_id,
            "slidingGuideId": p.cap_sliding_guide_id,
            "slidingGuideDepth": p.cap_sliding_guide_depth,
            "retentionDepth": p.cap_retention_depth,
            "engagementPerSide": p.cap_rod_engagement,
            "capLength": p.follower_head_length,
            "couponIds": p.cap_socket_ladder_ids,
            "couponDepths": p.cap_socket_ladder_depths,
        },
        "slotFitCoupon": {
            "rodDiameter": p.rod_diameter,
            "productionSlotWidth": p.fixed_slot_width,
            "widths": p.slot_fit_coupon_widths,
            "forms": ("straight", "curved"),
        },
        "endpoint": {
            "thetaDeg": p.theta_lock_deg,
            "meaning": "end-of-travel only",
            "retentionFeature": None,
            "selfLockClaimed": False,
            "compatibilityNames": ("locked", "theta_lock_deg", "GuidePath.locked"),
        },
        "service": {
            "pathId": "P17-D10-R1",
            "sequence": "full open -> frozen five-pose rigid-body removal path",
            "obsoleteInnerWindowRemoved": True,
            "removalWaypoints": tuple(
                (pose.delta_y, pose.delta_z, pose.phi_deg)
                for pose in completed_pigtail_removal_waypoints(p)
            ),
        },
        "workpieceOrientation": workpiece_orientation_evidence(p),
        "requirementTraceability": {
            "REQ-027": "workpieceOrientation front-view └ invariant",
            "REQ-028": "OPEN upper-left/upper-right/lower-right topology",
            "REQ-029": "END upper-left/middle/lower-right three-point wrap",
            "REQ-030": "locked compatibility word means endpoint only",
        },
        "pivotIntent": {
            "virtualKinematicDatumOnly": True,
            "behindXt60OnMinusY": False,
            "pivotZInsideBodyProjection": True,
            "fullAxleXShadowRequired": False,
            "reason": "four-plate axle spans beyond connector width; actual-solid service clearance is the gate",
        },
        "nonGoals": (
            "simulator",
            "shared_D_shaft",
            "removable_caps",
            "endpoint_lock",
            "yoke_bars",
        ),
    }


def manifest_sha256(p: P17R2Parameters = P17_R2_DEFAULTS) -> str:
    return sha256(json.dumps(p17_r2_manifest(p), sort_keys=True).encode("utf-8")).hexdigest()


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def provenance_token(p: P17R2Parameters = P17_R2_DEFAULTS) -> str:
    return f"manifest_{manifest_sha256(p)[:12]}__source_{source_revision_sha256()[:12]}"


def clear_geometry_caches() -> None:
    _inner_plate_local.cache_clear()
    _outer_plate_local.cache_clear()
    actual_solid_motion_evidence.cache_clear()
    two_sided_support_evidence.cache_clear()
    _completed_pigtail_seated.cache_clear()
    _completed_pigtail_service_evidence.cache_clear()
    locked_layout_blocker_evidence.cache_clear()


__all__ = [
    "P17R2Parameters",
    "P17_R2_DEFAULTS",
    "PHYSICAL_STAINLESS_STOCK_LENGTH_MM",
    "GUIDES",
    "D13_COMMON_ROD_DELTA",
    "ROD_NAMES",
    "STATE_THETA",
    "alpha_left",
    "alpha_right",
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
    "locked_layout_blocker_evidence",
    "rail_branch_regularity_evidence",
    "outer_pose_constraint_jacobian",
    "outer_pose_constraint_residuals",
    "outer_slot_local_center",
    "outer_slot_locus",
    "outer_rotation_center_yz",
    "parameters_from_env",
    "parameters_from_overrides",
    "p17_r2_manifest",
    "reconstruct_fixed_axle_from_outer",
    "reconstruct_world_from_outer",
    "rod_center",
    "rotation_for_side",
    "service_clearance_evidence",
    "theta_contact_deg",
    "triangle_motion_evidence",
    "triangle_motion_math_evidence",
    "transform_point_between_frames",
    "two_sided_support_evidence",
    "workpiece_orientation_evidence",
    "source_revision_sha256",
]
