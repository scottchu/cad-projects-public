"""P17 R2 direct-CAD counter-twist XT60 bend-jig candidate.

Coordinates: X is the rod/plate-stack axis. The mechanism lives in YZ. The
fixed inner guide plates are grounded by one stepped center axle. Left and
right outer plates are separate hand-operated occurrences rotating equal
magnitude and opposite sign about X on round journals.

This module is CAD/source evidence only. Cap retention, lock force, heat
response, wear, vibration, wire holding, and final physical acceptance remain
physical gates.
"""

from __future__ import annotations

import json
import os
from copy import copy
from dataclasses import asdict, dataclass, fields, replace
from functools import lru_cache
from hashlib import sha256
from math import atan2, cos, degrees, hypot, radians, sin, sqrt
from pathlib import Path
from typing import Literal

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
    extrude,
)
from cadgen import srgb


RodName = Literal["upright", "bottom", "diagonal"]
SideName = Literal["left", "right"]
StateName = Literal["open", "mid", "locked"]
ArtifactName = Literal[
    "open",
    "mid",
    "locked",
    "exploded",
    "print_kit",
    "permanent_cap_coupon",
    "center_axle_coupon",
    "lock_closeup",
]

ROD_NAMES: tuple[RodName, ...] = ("upright", "bottom", "diagonal")
STATE_THETA: dict[StateName, float] = {"open": 0.0, "mid": 16.0, "locked": 32.0}
P17_R2_DESIGN_CONTRACT_PATH = (
    "docs/iterations/p17-r2-fixed-reaction-rod-motion/DESIGN.md"
)
P17_R2_DESIGN_CONTRACT_SHA256 = (
    "f7462b5916a5fb7972df8b9fa47d03eea56a5bb1b4725f9ded452bfdbb2b21e1"
)


@dataclass(frozen=True, slots=True)
class PointYZ:
    y: float
    z: float

    def as_tuple(self) -> tuple[float, float]:
        return (self.y, self.z)

    def distance_to(self, other: "PointYZ") -> float:
        return hypot(self.y - other.y, self.z - other.z)


@dataclass(frozen=True, slots=True)
class GuidePath:
    name: RodName
    open: PointYZ
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
    cap_rod_engagement: float = 4.00

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
    follower_head_length: float = 4.40
    cap_closed_end_wall: float = 0.35
    cap_socket_id: float = 4.04
    cap_socket_ladder_ids: tuple[float, ...] = (3.96, 4.00, 4.04, 4.08, 4.12)
    cap_socket_ladder_depths: tuple[float, ...] = (3.50, 4.00, 4.50)

    # Plates, slots, lock, and print allowances.
    inner_plate_diameter: float = 54.00
    left_outer_secondary_grip_diameter: float = 60.00
    right_outer_primary_grip_diameter: float = 63.00
    lock_nose_orbit_radius: float = 30.00
    lock_nose_radius: float = 2.00
    lock_nose_axial_thickness: float = 1.60
    lock_contact_clearance: float = 0.02
    lock_over_center_capture: float = 0.40
    lock_receiver_stop_depth: float = 2.00
    lock_receiver_normal_width: float = 4.00
    lock_receiver_release_shift: float = 5.00
    lock_receiver_closing_deflection: float = 4.50
    lock_receiver_bridge_radius: float = 37.00
    lock_receiver_bridge_diameter: float = 3.20
    lock_flexure_width: float = 1.60
    lock_lead_in_length: float = 4.00
    lock_thumb_tab_length: float = 6.00
    fixed_slot_width: float = 4.20
    outer_slot_width: float = 4.20
    slot_endpoint_margin: float = 1.40
    slot_sample_count: int = 33
    theta_lock_deg: float = 32.00
    hard_stop_dwell_deg: float = 3.00
    min_web_mm: float = 2.20

    # D06 separates the unchanged outer-rotation datum C from the fixed purple
    # stepped-axle datum A.  Inner plate outlines and every frozen white-rod/
    # lock construction remain authored about C; only the inner hex bores,
    # stepped axle and keepers move to A.
    outer_rotation_center_y: float = -10.60
    outer_rotation_center_z: float = 17.00
    fixed_axle_center_y: float = -29.00
    fixed_axle_center_z: float = 17.00
    fixed_axle_guide_sample_count: int = 33

    # Reference-only workpiece envelopes.
    xt60_body_y: float = 8.10
    xt60_body_z: float = 20.50
    xt60_body_center_y: float = 0.00
    xt60_body_center_z: float = 21.00
    wire_envelope_diameter: float = 4.30
    service_clearance_min: float = 0.75
    slot_fit_coupon_widths: tuple[float, ...] = (4.10, 4.15, 4.20, 4.25, 4.30)
    completed_pigtail_window_start_y: float = 4.50
    completed_pigtail_window_center_z: float = 22.50
    completed_pigtail_window_width_z: float = 8.00
    completed_pigtail_extract_end_y: float = 34.00

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
        if self.rod_length_target >= 45.0:
            raise ValueError("P17 R2 rod length must not inherit the rejected 50 mm rod")
        if self.cap_socket_id < self.rod_diameter:
            raise ValueError("P17 R2 permanent cap default must not be an interference socket")
        if (self.follower_head_diameter - self.cap_socket_id) / 2.0 < 1.20:
            raise ValueError("permanent follower cap radial wall must be at least 1.20 mm")
        if self.cap_rod_engagement + self.cap_closed_end_wall > self.follower_head_length + 1.0e-9:
            raise ValueError("cap engagement must leave a closed-end wall")
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
        if self.lock_nose_orbit_radius + self.lock_nose_radius > self.right_outer_primary_grip_diameter / 2.0 + self.min_web_mm:
            raise ValueError("integral lock nose must retain a printable root on the right outer")
        if not 0.30 <= self.lock_over_center_capture <= 0.60:
            raise ValueError("P17 D04 lock capture must stay in the named 0.30..0.60 mm range")
        if self.lock_receiver_release_shift <= 2.0 * self.lock_nose_radius:
            raise ValueError("modeled thumb release must move the retaining shoulder clear of the lock nose")
        if self.slot_sample_count < 5 or self.slot_sample_count % 2 == 0:
            raise ValueError("slot_sample_count must be odd and at least 5")
        if self.fixed_axle_guide_sample_count < 33 or self.fixed_axle_guide_sample_count % 2 == 0:
            raise ValueError("fixed axle guide requires an odd sample count of at least 33")
        if self.fixed_slot_width != 4.20 or self.outer_slot_width != 4.20:
            raise ValueError("P17 D04 requires 4.20 mm low-wobble production slots")
        if self.pivot_y >= -self.xt60_body_y / 2.0:
            raise ValueError("P17 D04 pivot must remain behind the XT60 on -Y")
        if abs(self.fixed_axle_eccentricity - 18.40) > 1.0e-9:
            raise ValueError("P17 D07 fixed axle eccentricity must remain 18.40 mm")
        if self.completed_pigtail_window_width_z < 8.00:
            raise ValueError("completed-pigtail window must retain the D05 8.00 mm minimum width")


P17_R2_DEFAULTS = P17R2Parameters()

GUIDES: dict[RodName, GuidePath] = {
    # Collision-checked world-space guide centers derived around the offset
    # pivot.  The provisional D04 table was rejected during implementation
    # because it put rods through the actual XT60 body envelope.  These paths
    # preserve the three supported rod roles with positive body/axle clearance.
    "upright": GuidePath("upright", PointYZ(-12.0, 3.0), PointYZ(-18.0, 13.0)),
    "bottom": GuidePath("bottom", PointYZ(-5.0, -12.0), PointYZ(8.0, -12.0)),
    "diagonal": GuidePath("diagonal", PointYZ(11.5, 9.0), PointYZ(3.0, 1.0)),
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


def rod_center(name: RodName, theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> PointYZ:
    guide = GUIDES[name]
    u = max(0.0, min(1.0, theta_deg / p.theta_lock_deg))
    smooth = u * u * (3.0 - 2.0 * u)
    return PointYZ(
        guide.open.y + (guide.locked.y - guide.open.y) * smooth,
        guide.open.z + (guide.locked.z - guide.open.z) * smooth,
    )


def outer_slot_local_center(side: SideName, name: RodName, theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> PointYZ:
    world = rod_center(name, theta_deg, p)
    return _rotate_yz(_relative_to_pivot(world, p), -rotation_for_side(side, theta_deg))


def reconstruct_world_from_outer(side: SideName, name: RodName, theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> PointYZ:
    local = outer_slot_local_center(side, name, theta_deg, p)
    return _world_from_pivot(_rotate_yz(local, rotation_for_side(side, theta_deg)), p)


def outer_slot_locus(side: SideName, name: RodName, p: P17R2Parameters = P17_R2_DEFAULTS) -> tuple[PointYZ, ...]:
    return tuple(
        outer_slot_local_center(side, name, p.theta_lock_deg * index / (p.slot_sample_count - 1), p)
        for index in range(p.slot_sample_count)
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


def _segment_box_yz(
    first: PointYZ,
    second: PointYZ,
    *,
    x: float,
    thickness_x: float,
    width: float,
) -> Shape:
    """A rectangular member whose long axis follows one YZ segment."""
    dy = second.y - first.y
    dz = second.z - first.z
    length = hypot(dy, dz)
    if length <= 1.0e-9:
        raise ValueError("YZ segment must have positive length")
    angle = degrees(atan2(dz, dy))
    return (
        Pos(x, (first.y + second.y) / 2.0, (first.z + second.z) / 2.0)
        * Rot(angle, 0.0, 0.0)
        * Box(
            thickness_x,
            length,
            width,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
    )


def _lock_unit_vectors(p: P17R2Parameters) -> tuple[PointYZ, PointYZ]:
    angle = radians(p.theta_lock_deg)
    normal = PointYZ(cos(angle), sin(angle))
    tangent = PointYZ(-sin(angle), cos(angle))
    return normal, tangent


def _lock_center_at_lock(p: P17R2Parameters) -> PointYZ:
    normal, _ = _lock_unit_vectors(p)
    return PointYZ(
        normal.y * p.lock_nose_orbit_radius,
        normal.z * p.lock_nose_orbit_radius,
    )


def _lock_nose_local(p: P17R2Parameters) -> Shape:
    """Integral round nose on the right outer, authored in outer-local YZ."""
    x = p.outer_plate_thickness / 2.0 + p.lock_nose_axial_thickness / 2.0 - 0.20
    nose = _x_cylinder(
        2.0 * p.lock_nose_radius,
        p.lock_nose_axial_thickness,
        x,
        p.lock_nose_orbit_radius,
        0.0,
    )
    return _label(nose, "right_outer_integral_lock_nose_over_center", "#2D6FA8")


def _lock_receiver_components_local(
    p: P17R2Parameters,
    *,
    condition: Literal["seated", "closing_unreleased", "released"] = "seated",
) -> dict[str, Shape]:
    """One grounded receiver solid with a connected compliant latch arm.

    ``closing_unreleased`` is the same occurrence with nose-driven ramp
    deflection; ``released`` is the same flexure deflected by the thumb tab.
    Neither condition translates the receiver datum or substitutes a second
    part.  The seated shape is the snapped-back locked/back-drive condition.
    """
    normal, tangent = _lock_unit_vectors(p)
    center = _lock_center_at_lock(p)
    outer_offset_x = p.right_outer_x - p.right_inner_x
    nose_x = outer_offset_x + p.outer_plate_thickness / 2.0 + p.lock_nose_axial_thickness / 2.0 - 0.20
    receiver_x = (
        outer_offset_x
        + p.outer_plate_thickness / 2.0
        + 0.20
        + p.lock_nose_axial_thickness / 2.0
    )

    def along(origin: PointYZ, direction: PointYZ, distance: float) -> PointYZ:
        return PointYZ(origin.y + direction.y * distance, origin.z + direction.z * distance)

    # A single radial load path overlaps the fixed disk from r=24 mm and
    # crosses axially outside the rotating disk.  Both stop and flexure remain
    # connected to this grounded bridge in every modeled condition.
    ground_inner = PointYZ(normal.y * 24.0, normal.z * 24.0)
    bridge_center = PointYZ(
        normal.y * p.lock_receiver_bridge_radius,
        normal.z * p.lock_receiver_bridge_radius,
    )
    ground_arm = _segment_box_yz(
        ground_inner,
        bridge_center,
        x=0.0,
        thickness_x=p.inner_plate_thickness,
        width=p.lock_receiver_bridge_diameter,
    )
    axial_bridge = _x_cylinder(
        p.lock_receiver_bridge_diameter,
        receiver_x + p.lock_nose_axial_thickness / 2.0,
        (receiver_x + p.lock_nose_axial_thickness / 2.0) / 2.0,
        bridge_center.y,
        bridge_center.z,
    )
    hard_face = along(
        center,
        tangent,
        p.lock_nose_radius + p.lock_contact_clearance,
    )
    hard_center = along(hard_face, tangent, p.lock_receiver_stop_depth / 2.0)
    hard_stop = _segment_box_yz(
        along(hard_center, normal, -p.lock_receiver_normal_width / 2.0),
        along(hard_center, normal, p.lock_receiver_normal_width / 2.0),
        x=receiver_x,
        thickness_x=p.lock_nose_axial_thickness,
        width=p.lock_receiver_stop_depth,
    )

    catch_face = along(
        center,
        tangent,
        -(p.lock_nose_radius + p.lock_over_center_capture),
    )
    catch_center = along(catch_face, tangent, -p.lock_receiver_stop_depth / 2.0)
    deflection = 0.0
    if condition == "closing_unreleased":
        deflection = p.lock_receiver_closing_deflection
    elif condition == "released":
        deflection = p.lock_receiver_release_shift
    catch_center = along(catch_center, normal, deflection)

    retaining_catch = _segment_box_yz(
        along(catch_center, normal, -p.lock_receiver_normal_width / 2.0),
        along(catch_center, normal, p.lock_receiver_normal_width / 2.0),
        x=receiver_x,
        thickness_x=p.lock_nose_axial_thickness,
        width=p.lock_receiver_stop_depth,
    )

    # Sloped lead-in is part of the compliant arm.  During normal closing the
    # nose moves this ramp outward; after the nose passes the zero-penetration
    # throat, the undercut/catch snaps back to the seated location.
    ramp_outer = along(
        along(catch_center, tangent, -p.lock_lead_in_length),
        normal,
        p.lock_receiver_normal_width / 2.0,
    )
    lead_in_ramp = _segment_box_yz(
        along(catch_center, normal, p.lock_receiver_normal_width / 2.0),
        ramp_outer,
        x=receiver_x,
        thickness_x=p.lock_nose_axial_thickness,
        width=p.lock_flexure_width,
    )

    flexure_root = bridge_center
    flexure_beam = _segment_box_yz(
        flexure_root,
        along(catch_center, normal, p.lock_receiver_normal_width / 2.0),
        x=receiver_x,
        thickness_x=p.lock_nose_axial_thickness,
        width=p.lock_flexure_width,
    )
    stop_rib = _segment_box_yz(
        bridge_center,
        along(hard_center, normal, p.lock_receiver_normal_width / 2.0),
        x=receiver_x,
        thickness_x=p.lock_nose_axial_thickness,
        width=p.lock_receiver_bridge_diameter,
    )
    thumb_tab = _segment_box_yz(
        along(catch_center, normal, p.lock_receiver_normal_width / 2.0),
        along(catch_center, normal, p.lock_receiver_normal_width / 2.0 + p.lock_thumb_tab_length),
        x=receiver_x,
        thickness_x=p.lock_nose_axial_thickness,
        width=p.lock_receiver_bridge_diameter,
    )
    return {
        "ground_arm": ground_arm,
        "axial_bridge": axial_bridge,
        "hard_stop": hard_stop + stop_rib,
        "flexure_beam": flexure_beam,
        "lead_in_ramp": lead_in_ramp,
        "retaining_shoulder": retaining_catch,
        "thumb_release_tab": thumb_tab,
    }


def _lock_receiver_local(
    p: P17R2Parameters,
    *,
    condition: Literal["seated", "closing_unreleased", "released"] = "seated",
) -> Shape:
    components = list(_lock_receiver_components_local(p, condition=condition).values())
    receiver = components[0] + components[1:]
    return _label(
        receiver,
        f"right_inner_same_solid_one_way_receiver_ramp_throat_hard_stop_undercut_{condition}",
        "#D89A19",
    )


def _completed_pigtail_window_cutter_local(p: P17R2Parameters) -> Shape:
    """Rounded fixed-inner production window authored from world dimensions."""
    front_edge_y = p.pivot_y + p.inner_plate_diameter / 2.0
    half_width = p.completed_pigtail_window_width_z / 2.0
    start_center = PointYZ(
        p.completed_pigtail_window_start_y - p.pivot_y + half_width,
        p.completed_pigtail_window_center_z - p.pivot_z,
    )
    end_center = PointYZ(
        front_edge_y - p.pivot_y + half_width,
        p.completed_pigtail_window_center_z - p.pivot_z,
    )
    return _slot_capsule_cutter(
        (start_center, end_center),
        p.completed_pigtail_window_width_z,
        p.inner_plate_thickness + 2.0,
    )


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
    part = part - _completed_pigtail_window_cutter_local(p)
    if side == "right":
        part = part + _lock_receiver_local(p)
        part.label = "right_inner_fixed_guide_hex_keyed_with_completed_pigtail_window_and_receiver"
    else:
        part.label = "left_inner_fixed_guide_hex_keyed_with_completed_pigtail_window"
    return part


@lru_cache(maxsize=None)
def _outer_plate_local(side: SideName, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
    diameter = (
        p.left_outer_secondary_grip_diameter
        if side == "left"
        else p.right_outer_primary_grip_diameter
    )
    label = "left_outer_secondary_cam_mirrored_fixed_axle_guide" if side == "left" else "right_outer_primary_actuator_larger_integrated_lock_nose_mirrored_fixed_axle_guide"
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
    if side == "right":
        part = part + _lock_nose_local(p)
    else:
        grip = Pos(0.0, -28.0, 0.0) * Box(4.0, 4.0, 11.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        part = part + grip
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


def build_lock_nose(theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> Shape:
    """Standalone actual-solid lock nose in its assembled world transform."""
    pivot = outer_rotation_center_yz(p)
    return _label(
        Pos(p.right_outer_x, pivot.y, pivot.z)
        * Rot(alpha_right(theta_deg), 0.0, 0.0)
        * copy(_lock_nose_local(p)),
        f"right_outer_lock_nose_theta_{theta_deg:.2f}",
        "#2D6FA8",
    )


def build_lock_receiver(
    p: P17R2Parameters = P17_R2_DEFAULTS,
    *,
    condition: Literal["seated", "closing_unreleased", "released"] = "seated",
) -> Shape:
    """Standalone occurrence of the same grounded receiver/flexure solid."""
    pivot = outer_rotation_center_yz(p)
    return _label(
        Pos(p.right_inner_x, pivot.y, pivot.z) * _lock_receiver_local(p, condition=condition),
        f"right_inner_same_receiver_{condition}",
        "#D89A19",
    )


def build_lock_receiver_component(
    name: Literal["hard_stop", "retaining_shoulder", "lead_in_ramp", "flexure_beam", "thumb_release_tab"],
    p: P17R2Parameters = P17_R2_DEFAULTS,
    *,
    condition: Literal["seated", "closing_unreleased", "released"] = "seated",
) -> Shape:
    pivot = outer_rotation_center_yz(p)
    component = _lock_receiver_components_local(p, condition=condition)[name]
    return _label(
        Pos(p.right_inner_x, pivot.y, pivot.z) * component,
        f"right_inner_{name}_{condition}",
        "#D89A19",
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
    engagement_depth = p.cap_rod_engagement if engagement_depth is None else engagement_depth
    head_length = max(p.follower_head_length, engagement_depth + p.cap_closed_end_wall)
    head = Cylinder(
        p.follower_head_diameter / 2.0,
        head_length,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    socket_center_x = socket_open_side * (head_length / 2.0 - engagement_depth / 2.0)
    socket = _x_cylinder(socket_id, engagement_depth + 0.20, socket_center_x, 0.0, 0.0)
    cap = head - socket
    return _label(cap, "permanent_follower_cap_blind_socket_ID4p04_depth4p00", "#1D1D1F")


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
    # Two insulated conductors leave the connector on +Y.  They are reference
    # envelopes only; the forming rods may intentionally contact them.
    wires = [
        _y_cylinder(p.wire_envelope_diameter, 24.0, x, 16.0, p.xt60_body_center_z)
        for x in (-3.60, 3.60)
    ]
    workpiece = wires[0] + wires[1]
    workpiece.label = f"reference_wire_envelopes_theta_{theta_deg:.1f}_not_load_path"
    workpiece.color = srgb("#F1C84B", 0.45)
    return workpiece


def completed_pigtail_removal_waypoints(
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> tuple[PointYZ, ...]:
    """Persisted D05 release/open/lift/+Y extraction dogleg centerline."""
    return (
        PointYZ(p.xt60_body_center_y, p.xt60_body_center_z),
        PointYZ(p.xt60_body_center_y, p.completed_pigtail_window_center_z),
        PointYZ(8.0, p.completed_pigtail_window_center_z),
        PointYZ(20.0, p.completed_pigtail_window_center_z),
        PointYZ(p.completed_pigtail_extract_end_y, p.completed_pigtail_window_center_z),
    )


def _completed_pigtail_at(
    center: PointYZ,
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> Shape:
    """Produced connector, joints, heat shrink, wires, and finger clearance."""
    body = Pos(0.0, center.y, center.z) * Box(
        p.xt60_body_width_x,
        p.xt60_body_y,
        p.xt60_body_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    parts: list[Shape] = [body]
    for x in (-3.60, 3.60):
        parts.extend(
            (
                _y_cylinder(5.50, 4.00, x, center.y + 5.05, center.z),
                _y_cylinder(6.00, 10.00, x, center.y + 12.05, center.z),
                _y_cylinder(p.wire_envelope_diameter, 24.00, x, center.y + 29.05, center.z),
            )
        )
    finger = Pos(0.0, center.y + 2.0, center.z) * Box(
        8.0,
        6.0,
        8.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    parts.append(finger)
    result = parts[0] + parts[1:]
    return _label(
        result,
        f"completed_pigtail_actual_service_occurrence_y_{center.y:.2f}_z_{center.z:.2f}",
        "#73A6FF",
    )


def completed_pigtail_removal_states(
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> tuple[tuple[str, Shape], ...]:
    """Dense actual-solid samples for the released-open dogleg sweep."""
    waypoints = completed_pigtail_removal_waypoints(p)
    rows: list[tuple[str, Shape]] = []
    sample_index = 0
    for segment_index, (first, second) in enumerate(zip(waypoints, waypoints[1:])):
        travel = first.distance_to(second)
        divisions = max(1, int(travel / 1.0 + 0.999999))
        for index in range(divisions + 1):
            if segment_index and index == 0:
                continue
            u = index / divisions
            center = PointYZ(
                first.y + (second.y - first.y) * u,
                first.z + (second.z - first.z) * u,
            )
            rows.append((f"dogleg_{sample_index:02d}", _completed_pigtail_at(center, p)))
            sample_index += 1
    return tuple(rows)


def build_completed_pigtail_removal_sweep(
    p: P17R2Parameters = P17_R2_DEFAULTS,
) -> Compound:
    children = [shape for _, shape in completed_pigtail_removal_states(p)]
    return Compound(
        children=children,
        label="completed_pigtail_actual_released_open_lift_then_plusY_removal_sweep",
    )


def build_service_envelopes(theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
    """Actual solids for the +Y solder, heat-shrink, tool and removal space."""
    shapes: list[Shape] = []
    for x in (-3.60, 3.60):
        solder = _y_cylinder(5.50, 4.00, x, 6.05, p.xt60_body_center_z)
        solder.label = f"reference_solder_joint_x_{x:+.2f}"
        solder.color = srgb("#E36B4A", 0.24)
        heat_shrink = _y_cylinder(6.00, 12.00, x, 12.05, p.xt60_body_center_z)
        heat_shrink.label = f"reference_heat_shrink_x_{x:+.2f}"
        heat_shrink.color = srgb("#555555", 0.16)
        outgoing = _y_cylinder(p.wire_envelope_diameter, 30.00, x, 19.05, p.xt60_body_center_z)
        outgoing.label = f"reference_outgoing_wire_x_{x:+.2f}"
        outgoing.color = srgb("#F1C84B", 0.18)
        tool = Pos(x, 9.00, p.xt60_body_center_z) * Box(
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


def build_lock_closeup(p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
    return Compound(
        children=[
            build_inner_plate("right", p),
            build_outer_plate("right", p.theta_lock_deg, p),
        ],
        label="P17_R2_lock_closeup_same_right_inner_receiver_and_right_outer_nose",
    )


def build_artifact(name: ArtifactName, p: P17R2Parameters = P17_R2_DEFAULTS) -> Compound:
    builders = {
        "open": lambda: build_motion_state("open", p),
        "mid": lambda: build_motion_state("mid", p),
        "locked": lambda: build_motion_state("locked", p),
        "exploded": lambda: build_exploded(p),
        "print_kit": lambda: build_print_kit(p),
        "permanent_cap_coupon": lambda: build_permanent_cap_coupon(p),
        "center_axle_coupon": lambda: build_center_axle_coupon(p),
        "lock_closeup": lambda: build_lock_closeup(p),
    }
    if name not in builders:
        raise ValueError(f"unknown P17 R2 artifact {name!r}")
    artifact = builders[name]()
    return Compound(children=[artifact], label=f"P17_R2_ARTIFACT_{name}__{provenance_token(p)}")


def lock_contact_gap_y(theta_deg: float, p: P17R2Parameters = P17_R2_DEFAULTS) -> float:
    """Signed closing-direction nose-to-hard-stop clearance in millimetres."""
    _, tangent = _lock_unit_vectors(p)
    center = _rotate_yz(PointYZ(p.lock_nose_orbit_radius, 0.0), alpha_right(theta_deg))
    locked_center = _lock_center_at_lock(p)
    hard_face = PointYZ(
        locked_center.y + tangent.y * (p.lock_nose_radius + p.lock_contact_clearance),
        locked_center.z + tangent.z * (p.lock_nose_radius + p.lock_contact_clearance),
    )
    center_to_face = PointYZ(hard_face.y - center.y, hard_face.z - center.z)
    return center_to_face.y * tangent.y + center_to_face.z * tangent.z - p.lock_nose_radius


def _intersection_volume(first: Shape, second: Shape) -> float:
    common = first.intersect(second)
    if common is None:
        return 0.0
    if hasattr(common, "volume"):
        return float(common.volume)
    return sum(float(item.volume) for item in common)


def service_clearance_evidence(p: P17R2Parameters = P17_R2_DEFAULTS) -> dict[str, object]:
    """Actual-solid pivot service and released-open extraction evidence."""
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
    production_open = {
        "center_axle": build_center_axle(p),
        "left_keeper": build_keeper("left", p),
        "right_keeper": build_keeper("right", p),
        "left_inner_with_window": build_inner_plate("left", p),
        "right_inner_with_window": build_inner_plate("right", p),
        "left_outer_open": build_outer_plate("left", 0.0, p),
        "right_outer_open": build_outer_plate("right", 0.0, p),
    }
    for name in ROD_NAMES:
        production_open[f"{name}_rod_open"] = build_rod(name, 0.0, p)
        production_open[f"left_{name}_cap_open"] = build_cap("left", name, 0.0, p)
        production_open[f"right_{name}_cap_open"] = build_cap("right", name, 0.0, p)
    removal_minimum = float("inf")
    removal_rows: dict[str, object] = {}
    for state_name, pigtail in completed_pigtail_removal_states(p):
        for production_name, solid in production_open.items():
            value = float(pigtail.distance(solid))
            intersection = _intersection_volume(pigtail, solid) if value <= 1.0e-8 else 0.0
            removal_minimum = min(removal_minimum, value)
            removal_rows[f"{state_name}:{production_name}"] = {
                "minimumClearanceMm": value,
                "zeroIntersection": intersection <= 1.0e-7,
                "intersectionMm3": intersection,
            }
    minimum = min(minimum, removal_minimum)
    return {
        "minimumRequiredMm": p.service_clearance_min,
        "minimumActualMm": minimum,
        "passes": minimum + 1.0e-9 >= p.service_clearance_min,
        "pivotServiceRows": rows,
        "removalSequence": "release -> full open -> lift to window centerline -> +Y extraction",
        "removalWaypointsYZ": [point.as_tuple() for point in completed_pigtail_removal_waypoints(p)],
        "removalMinimumActualMm": removal_minimum,
        "removalZeroIntersection": all(row["zeroIntersection"] for row in removal_rows.values()),
        "removalRows": removal_rows,
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
    inner_neighbors.append(_completed_pigtail_window_cutter_local(p))
    inner_neighbors.extend(_lock_receiver_components_local(p).values())
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
        if side == "left":
            outer_neighbors.append(
                Pos(0.0, -28.0, 0.0)
                * Box(4.0, 4.0, 11.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
            )
        else:
            outer_neighbors.append(_lock_nose_local(p))
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
    sample_count = p.fixed_axle_guide_sample_count
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
    ]
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
        "contractPath": P17_R2_DESIGN_CONTRACT_PATH,
        "contractSha256": P17_R2_DESIGN_CONTRACT_SHA256,
        "fixedMember": "purple printed stepped center axle",
        "whiteRods": {
            "count": 3,
            "color": "white stainless",
            "roles": ROD_NAMES,
            "moving": True,
            "fixedReactionMember": False,
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
                "right_lock_contact_gap_y": lock_contact_gap_y(theta, p),
            }
            for state, theta in STATE_THETA.items()
        },
        "guides": {
            name: {
                "open": GUIDES[name].open.as_tuple(),
                "locked": GUIDES[name].locked.as_tuple(),
                "travel": GUIDES[name].travel,
            }
            for name in ROD_NAMES
        },
        "centerAxle": {
            "fixedMember": "purple printed stepped axle",
            "whiteRods": "all three OD4 rods remain moving forming/locking rods",
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
            "couponIds": p.cap_socket_ladder_ids,
            "couponDepths": p.cap_socket_ladder_depths,
        },
        "slotFitCoupon": {
            "rodDiameter": p.rod_diameter,
            "productionSlotWidth": p.fixed_slot_width,
            "widths": p.slot_fit_coupon_widths,
            "forms": ("straight", "curved"),
        },
        "lock": {
            "geometry": "integral right-outer nose plus same-solid right-inner ramp/throat/hard-stop/undercut receiver",
            "overCenterCapture": p.lock_over_center_capture,
            "contactClearance": p.lock_contact_clearance,
            "releaseShift": p.lock_receiver_release_shift,
            "releaseFeature": "connected flexure and thumb tab; no alternate receiver occurrence",
        },
        "service": {
            "sequence": "release -> full open -> lift -> +Y completed-pigtail extraction",
            "completedPigtailWindowStartY": p.completed_pigtail_window_start_y,
            "completedPigtailWindowCenterZ": p.completed_pigtail_window_center_z,
            "completedPigtailWindowWidthZ": p.completed_pigtail_window_width_z,
            "removalWaypointsYZ": tuple(point.as_tuple() for point in completed_pigtail_removal_waypoints(p)),
        },
        "pivotIntent": {
            "behindXt60OnMinusY": True,
            "pivotZInsideBodyProjection": True,
            "fullAxleXShadowRequired": False,
            "reason": "four-plate axle spans beyond connector width; actual-solid service clearance is the gate",
        },
        "nonGoals": (
            "simulator",
            "animation_sidecar",
            "shared_D_shaft",
            "removable_caps",
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


def lock_backdrive_evidence(p: P17R2Parameters = P17_R2_DEFAULTS) -> dict[str, object]:
    theta = p.theta_lock_deg
    result: dict[str, object] = {
        "thetaDeg": theta,
        "side": "right",
        "rightLockContactGapY": lock_contact_gap_y(theta, p),
        "rodChecks": {},
    }
    hard_stop = build_lock_receiver_component("hard_stop", p)
    shoulder = build_lock_receiver_component("retaining_shoulder", p)
    released_shoulder = build_lock_receiver_component(
        "retaining_shoulder", p, condition="released"
    )
    closing_rows: dict[str, object] = {}
    for closing_theta in (0.0, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 30.0, 31.0, 31.5, 31.8):
        nose = build_lock_nose(closing_theta, p)
        receiver = build_lock_receiver(p, condition="closing_unreleased")
        catch = build_lock_receiver_component(
            "retaining_shoulder", p, condition="closing_unreleased"
        )
        closing_rows[f"theta_{closing_theta:.1f}"] = {
            "receiverIntersectionMm3": _intersection_volume(nose, receiver),
            "catchClearanceMm": float(nose.distance(catch)),
            "condition": "same_receiver_nose_driven_flexure_unreleased",
        }
    released_rows: dict[str, object] = {}
    for opening_theta in (32.0, 31.5, 31.0, 30.0):
        nose = build_lock_nose(opening_theta, p)
        receiver = build_lock_receiver(p, condition="released")
        released_rows[f"theta_{opening_theta:.1f}"] = {
            "receiverIntersectionMm3": _intersection_volume(nose, receiver),
            "catchClearanceMm": float(nose.distance(released_shoulder)),
            "condition": "same_receiver_thumb_tab_deflected",
        }
    overclose_receiver = build_lock_receiver(p, condition="seated")
    overclose_nose = build_lock_nose(theta + 1.0, p)
    overclose_total = _intersection_volume(overclose_nose, overclose_receiver)
    overclose_hard = _intersection_volume(overclose_nose, hard_stop)
    result["solidLockChecks"] = {
        "lockedHardStopIntersectionMm3": _intersection_volume(build_lock_nose(theta, p), hard_stop),
        "overclosedHardStopIntersectionMm3": _intersection_volume(build_lock_nose(theta + 1.0, p), hard_stop),
        "lockedShoulderIntersectionMm3": _intersection_volume(build_lock_nose(theta, p), shoulder),
        "opening1degShoulderIntersectionMm3": _intersection_volume(build_lock_nose(theta - 1.0, p), shoulder),
        "opening2degShoulderIntersectionMm3": _intersection_volume(build_lock_nose(theta - 2.0, p), shoulder),
        "releasedOpening2degShoulderIntersectionMm3": _intersection_volume(build_lock_nose(theta - 2.0, p), released_shoulder),
        "overclosedReceiverIntersectionMm3": overclose_total,
        "overclosedNonHardStopIntersectionMm3": max(0.0, overclose_total - overclose_hard),
        "overCenterCaptureMm": p.lock_over_center_capture,
    }
    result["normalClosingSweep"] = closing_rows
    result["releasedOpeningSweep"] = released_rows
    result["sameReceiverOccurrence"] = {
        "worldDatumXYZ": (p.right_inner_x, p.pivot_y, p.pivot_z),
        "connectedSolidCountSeated": len(build_lock_receiver(p, condition="seated").solids()),
        "connectedSolidCountClosing": len(build_lock_receiver(p, condition="closing_unreleased").solids()),
        "connectedSolidCountReleased": len(build_lock_receiver(p, condition="released").solids()),
        "releaseFeature": "connected radial flexure, lead-in ramp, undercut catch, and thumb tab",
    }
    total_torque = 0.0
    for name in ROD_NAMES:
        before = reconstruct_world_from_outer("right", name, theta - p.hard_stop_dwell_deg, p)
        at_lock = reconstruct_world_from_outer("right", name, theta, p)
        tangent = PointYZ(at_lock.y - before.y, at_lock.z - before.z)
        length = hypot(tangent.y, tangent.z)
        tangent_u = PointYZ(tangent.y / length, tangent.z / length)
        normal = PointYZ(-tangent_u.z, tangent_u.y)
        reaction = PointYZ(0.0, -1.0)
        center = at_lock
        torque = center.y * reaction.z - center.z * reaction.y
        normal_dot_reaction = normal.y * reaction.y + normal.z * reaction.z
        total_torque += torque
        result["rodChecks"][name] = {
            "worldCenter": center.as_tuple(),
            "slotTangent": tangent_u.as_tuple(),
            "slotNormal": normal.as_tuple(),
            "nominalReaction": reaction.as_tuple(),
            "normalDotReaction": normal_dot_reaction,
            "torqueAboutHub": torque,
        }
    result["summedTorqueAboutRightHub"] = total_torque
    result["claimBoundary"] = "CAD receiver-pocket/contact proof only; physical self-lock not claimed"
    return result


__all__ = [
    "P17R2Parameters",
    "P17_R2_DEFAULTS",
    "GUIDES",
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
    "build_lock_nose",
    "build_lock_receiver",
    "build_lock_receiver_component",
    "build_motion_state",
    "build_service_envelopes",
    "build_slot_fit_coupon",
    "clear_geometry_caches",
    "completed_pigtail_removal_states",
    "completed_pigtail_removal_waypoints",
    "combined_contact_closure_evidence",
    "fixed_axle_actual_solid_evidence",
    "fixed_axle_center_yz",
    "fixed_axle_guide_local_center",
    "fixed_axle_guide_locus",
    "fixed_occurrence_transform_evidence",
    "fixed_guide_locus",
    "lock_backdrive_evidence",
    "lock_contact_gap_y",
    "manifest_sha256",
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
    "source_revision_sha256",
]
