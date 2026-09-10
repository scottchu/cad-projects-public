"""P20 R1 axle-only evidence scaffold; intentionally not a product candidate.

Coordinates remain P19's: X is the plate-stack/rod axis and FRONT is world
YZ, with +Z mating-head/up and +Y short-tail/tool-approach/outward-right.

This bounded scaffold preserves the P19 rods, inner tracks, stack, workpiece,
service geometry, axle profile, keepers and cap geometry.  Its only geometry
delta is the frozen P20 contract: move the axle datum to A=(-15,-11), rotate
each outer plate physically about A through -45/+45 degrees, replace the P19
eccentric axle arc with one centered round journal, and remove all six outer
rod rails without adding substitute rod apertures.  The resulting six OPEN
rod/outer-plate collisions are deliberate evidence and are never suppressed.
"""

from __future__ import annotations

import json
import os
from copy import copy
from dataclasses import asdict, dataclass, fields, replace
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import cos, pi, radians, sin
from pathlib import Path
from typing import Literal

from build123d import Align, Compound, Cylinder, Pos, Rot, Shape
from cadgen import srgb

import xt60_bend_jig.p19_r1_front_edge_short_tail as p19


PointYZ = p19.PointYZ
MotionState = p19.MotionState
RodName = p19.RodName
SideName = p19.SideName
ROD_NAMES = p19.ROD_NAMES
GUIDES = p19.GUIDES

StateName = Literal["open", "mid", "end"]
SCAFFOLD_STATUS = "evidence-only intentionally-colliding non-candidate scaffold"
P20_SCAFFOLD_CONTRACT_PATH = (
    "docs/iterations/p20-r1-fixed-rod-reset/SCAFFOLD_BRIEF.md"
)
P20_SCAFFOLD_CONTRACT_SHA256 = (
    "02b6dbcd0487b6a2eef294e14cd07bdb9f37bf68776a0ab6f581d4f11232653e"
)


class CollisionEvaluationError(RuntimeError):
    """Fail-closed signal: a BREP common could not determine collision truth."""


@dataclass(frozen=True, slots=True)
class P20R1Parameters(p19.P19R1Parameters):
    """P19 geometry with only the frozen P20 scaffold parameter deltas."""

    theta_end_deg: float = 45.00
    fixed_axle_center_y: float = -15.00
    fixed_axle_center_z: float = -11.00

    def __post_init__(self) -> None:
        # Preserve the P19 physical stock and fit/stack constraints, while
        # intentionally replacing only P19's 5-degree and axle-datum guards.
        baseline = p19.P19_R1_DEFAULTS
        mutable = {"theta_end_deg", "fixed_axle_center_y", "fixed_axle_center_z"}
        for field in fields(p19.P19R1Parameters):
            if field.name not in mutable and getattr(self, field.name) != getattr(baseline, field.name):
                raise ValueError(f"P20 scaffold must preserve P19 parameter {field.name}")
        if self.theta_end_deg != 45.0:
            raise ValueError("P20 scaffold requires exactly 45 degrees per side")
        if (self.fixed_axle_center_y, self.fixed_axle_center_z) != (-15.0, -11.0):
            raise ValueError("P20 scaffold requires axle datum A=(-15,-11)")
        if self.rod_length_target != p19.PHYSICAL_STAINLESS_STOCK_LENGTH_MM:
            raise ValueError("P20 scaffold must preserve uncut OD4 x 50 mm rods")
        if self.outer_bearing_bore_diameter <= self.outer_journal_diameter:
            raise ValueError("centered outer journal must retain diametral clearance")


P20_R1_SCAFFOLD_DEFAULTS = P20R1Parameters()
STATE_U: dict[StateName, float] = {"open": 0.0, "mid": 0.5, "end": 1.0}


def parameters_from_overrides(
    overrides: dict[str, object] | None = None,
) -> P20R1Parameters:
    overrides = overrides or {}
    unknown = set(overrides) - {field.name for field in fields(P20R1Parameters)}
    if unknown:
        raise ValueError(f"unknown P20 R1 scaffold parameter(s): {sorted(unknown)}")
    return replace(P20_R1_SCAFFOLD_DEFAULTS, **overrides)


def parameters_from_env() -> P20R1Parameters:
    raw = os.environ.get("P20_R1_SCAFFOLD_PARAMS_JSON", "").strip()
    overrides = json.loads(raw) if raw else {}
    return parameters_from_overrides(overrides)


def fixed_axle_center_yz(
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> PointYZ:
    return PointYZ(p.fixed_axle_center_y, p.fixed_axle_center_z)


def outer_rotation_center_yz(
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> PointYZ:
    """P19 disk center C at OPEN; it is not the P20 physical pivot."""
    return PointYZ(p.outer_rotation_center_y, p.outer_rotation_center_z)


def _rotate_yz(point: PointYZ, angle_deg: float) -> PointYZ:
    angle = radians(angle_deg)
    return PointYZ(
        point.y * cos(angle) - point.z * sin(angle),
        point.y * sin(angle) + point.z * cos(angle),
    )


def rotation_for_side(
    side: SideName,
    u: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> float:
    if not 0.0 <= u <= 1.0:
        raise ValueError("P20 scaffold motion progress must stay in 0..1")
    return (-1.0 if side == "left" else 1.0) * p.theta_end_deg * u


def centered_outer_local_to_world(
    point: PointYZ,
    side: SideName,
    u: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> PointYZ:
    """Pure centered-frame authority: T_s(q,u)=A+R(alpha_s(u))*q."""
    axle = fixed_axle_center_yz(p)
    offset = _rotate_yz(point, rotation_for_side(side, u, p))
    return PointYZ(axle.y + offset.y, axle.z + offset.z)


def world_to_centered_outer_local(
    point: PointYZ,
    side: SideName,
    u: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> PointYZ:
    """Exact inverse of :func:`centered_outer_local_to_world`."""
    axle = fixed_axle_center_yz(p)
    return _rotate_yz(
        PointYZ(point.y - axle.y, point.z - axle.z),
        -rotation_for_side(side, u, p),
    )


def fixed_axle_guide_local_center(
    side: SideName,
    u: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> PointYZ:
    """The fixed axle is the same local origin for both sides at every state."""
    # Validate the side/state through the one shared motion function.
    rotation_for_side(side, u, p)
    return PointYZ(0.0, 0.0)


def motion_state(
    u: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> MotionState:
    """P19 rod world paths with the P20 -45/+45 outer-plate rotations."""
    if not 0.0 <= u <= 1.0:
        raise ValueError("P20 scaffold motion progress must stay in 0..1")
    baseline_state = p19.motion_state(u, p19.P19_R1_DEFAULTS)
    theta = p.theta_end_deg * u
    return MotionState(
        u=u,
        theta_deg=theta,
        alpha_left_deg=-theta,
        alpha_right_deg=theta,
        rods=baseline_state.rods,
    )


def rod_center(
    name: RodName,
    theta_deg: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> PointYZ:
    u = max(0.0, min(1.0, theta_deg / p.theta_end_deg))
    return motion_state(u, p).rod(name)


def _label(shape: Shape, label: str, color: str | None = None) -> Shape:
    shape.label = label
    if color is not None:
        shape.color = srgb(color)
    return shape


@lru_cache(maxsize=None)
def _outer_plate_local(
    side: SideName,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Shape:
    """Disk centered at C-A, with exactly one round bore at local q_A=(0,0)."""
    diameter = (
        p.left_outer_secondary_grip_diameter
        if side == "left"
        else p.right_outer_primary_grip_diameter
    )
    center = outer_rotation_center_yz(p)
    axle = fixed_axle_center_yz(p)
    disk_center_local = PointYZ(center.y - axle.y, center.z - axle.z)
    disk = Pos(0.0, disk_center_local.y, disk_center_local.z) * Cylinder(
        diameter / 2.0,
        p.outer_plate_thickness,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    journal = Cylinder(
        p.outer_bearing_bore_diameter / 2.0,
        p.outer_plate_thickness + 2.0,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    # Deliberately no outer rod cutter of any kind in this scaffold.
    color = "#377A3A" if side == "left" else "#2D6FA8"
    return _label(
        disk - journal,
        f"P20_scaffold_{side}_outer_zero_outer_rod_rails_centered_round_axle_journal_non_candidate",
        color,
    )


def build_outer_plate(
    side: SideName,
    theta_deg: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Shape:
    x = p.left_outer_x if side == "left" else p.right_outer_x
    axle = fixed_axle_center_yz(p)
    u = max(0.0, min(1.0, theta_deg / p.theta_end_deg))
    color = "#377A3A" if side == "left" else "#2D6FA8"
    return _label(
        Pos(x, axle.y, axle.z)
        * Rot(rotation_for_side(side, u, p), 0.0, 0.0)
        * copy(_outer_plate_local(side, p)),
        _outer_plate_local(side, p).label,
        color,
    )


def build_inner_plate(
    side: SideName,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Shape:
    return _label(
        p19.build_inner_plate(side, p),
        f"P20_scaffold_{side}_inner_fixed_three_straight_closed_tracks_axle_A_non_candidate",
        "#D89A19",
    )


def build_center_axle(
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Shape:
    return _label(
        p19.build_center_axle(p),
        "P20_scaffold_fixed_stepped_center_axle_at_A_non_candidate",
        "#5B4B8A",
    )


def build_keeper(
    side: SideName,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Shape:
    return _label(
        p19.build_keeper(side, p),
        f"P20_scaffold_fixed_{side}_keeper_at_A_non_candidate",
        "#111111",
    )


def build_rod(
    name: RodName,
    theta_deg: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Shape:
    center = rod_center(name, theta_deg, p)
    return _label(
        p19._x_cylinder(p.rod_diameter, p.rod_length_target, 0.0, center.y, center.z),
        f"P20_scaffold_{name}_OD4_rod_L{p.rod_length_target:.2f}_P19_world_path_non_candidate",
        "#B7B7B7",
    )


def build_cap(
    side: SideName,
    name: RodName,
    theta_deg: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Shape:
    cap = p19.build_cap(side, name, theta_deg, p)
    return _label(
        cap,
        f"P20_scaffold_{side}_{name}_permanent_follower_cap_P19_geometry_non_candidate",
        "#1D1D1F",
    )


def build_xt60_reference(
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Shape:
    return _label(
        p19.build_xt60_reference(p),
        "reference_P20_scaffold_XT60_body_P19_geometry_non_candidate",
        "#C8E6FF",
    )


def build_workpiece_reference(
    theta_deg: float,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Shape:
    return _label(
        p19.build_workpiece_reference(theta_deg, p),
        "reference_P20_scaffold_short_tail_wires_P19_geometry_non_candidate",
        "#F1C84B",
    )


def intersection_volume(first: Shape, second: Shape) -> float:
    try:
        common = first & second
        return 0.0 if common is None else float(common.volume)
    except Exception as exc:
        raise CollisionEvaluationError(
            "BREP common failed; collision state is unknown"
        ) from exc


def _state_shapes(
    u: float,
    p: P20R1Parameters,
) -> dict[str, Shape]:
    theta = p.theta_end_deg * u
    shapes: dict[str, Shape] = {
        "left_outer_plate": build_outer_plate("left", theta, p),
        "right_outer_plate": build_outer_plate("right", theta, p),
        "left_inner_plate": build_inner_plate("left", p),
        "right_inner_plate": build_inner_plate("right", p),
        "center_axle": build_center_axle(p),
        "left_keeper": build_keeper("left", p),
        "right_keeper": build_keeper("right", p),
        "xt60_reference": build_xt60_reference(p),
        "wire_reference": build_workpiece_reference(theta, p),
    }
    for name in ROD_NAMES:
        shapes[f"{name}_rod"] = build_rod(name, theta, p)
        for side in ("left", "right"):
            shapes[f"{side}_{name}_cap"] = build_cap(side, name, theta, p)
    return shapes


@lru_cache(maxsize=None)
def scaffold_collision_evidence(
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> dict[str, object]:
    """Measure the six expected OPEN collisions and reject every new pair.

    P19's intended rod/wire contact after first contact and the keeper's
    designed retention interference are separately reported as preserved
    baseline contacts; neither is a new P20 scaffold collision.
    """
    expected_pairs = tuple(
        f"{name}_rod::{side}_outer_plate"
        for name in ROD_NAMES
        for side in ("left", "right")
    )
    open_shapes = _state_shapes(0.0, p)
    open_expected = {
        pair: intersection_volume(open_shapes[pair.split("::")[0]], open_shapes[pair.split("::")[1]])
        for pair in expected_pairs
    }

    unexpected: dict[str, float] = {}
    rows: dict[str, object] = {}
    preserved_contacts: dict[str, float] = {}
    for state_name, u in STATE_U.items():
        shapes = _state_shapes(u, p)
        theta = p.theta_end_deg * u
        state_expected = {
            pair: intersection_volume(shapes[pair.split("::")[0]], shapes[pair.split("::")[1]])
            for pair in expected_pairs
        }
        state_unexpected: dict[str, float] = {}
        for (first_name, first), (second_name, second) in combinations(shapes.items(), 2):
            volume = intersection_volume(first, second)
            if volume <= 1.0e-7:
                continue
            unordered = frozenset((first_name, second_name))
            is_expected = any(
                unordered == frozenset((f"{name}_rod", f"{side}_outer_plate"))
                for name in ROD_NAMES
                for side in ("left", "right")
            )
            is_preserved_baseline_contact = (
                unordered in (
                    frozenset(("center_axle", "left_keeper")),
                    frozenset(("center_axle", "right_keeper")),
                    frozenset(("xt60_reference", "wire_reference")),
                )
                or any(
                    unordered == frozenset((f"{name}_rod", "wire_reference"))
                    for name in ROD_NAMES
                )
            )
            pair = f"{state_name}:{first_name}::{second_name}"
            if is_expected:
                continue
            if is_preserved_baseline_contact:
                preserved_contacts[pair] = volume
                continue
            state_unexpected[pair] = volume
            unexpected[pair] = volume

        service_intersections: dict[str, float] = {}
        service = p19.build_service_envelopes(theta, p)
        for service_index, service_shape in enumerate(service.children):
            for production_name in (
                "left_outer_plate",
                "right_outer_plate",
                "left_inner_plate",
                "right_inner_plate",
                "center_axle",
                "left_keeper",
                "right_keeper",
            ):
                volume = intersection_volume(shapes[production_name], service_shape)
                if volume > 1.0e-7:
                    pair = f"{state_name}:{production_name}::service_{service_index}_{service_shape.label}"
                    service_intersections[pair] = volume
                    unexpected[pair] = volume
        rows[state_name] = {
            "u": u,
            "thetaDeg": theta,
            "expectedRodOuterCollisionMm3ByPair": state_expected,
            "unexpectedCollisionMm3ByPair": state_unexpected,
            "unexpectedServiceEnvelopeCollisionMm3ByPair": service_intersections,
        }
    return {
        "status": SCAFFOLD_STATUS,
        "expectedPairCount": len(expected_pairs),
        "expectedPairs": expected_pairs,
        "openExpectedCollisionMm3ByPair": open_expected,
        "openExpectedCollisionTotalMm3": sum(open_expected.values()),
        "preservedP19ReferenceContactMm3ByPair": preserved_contacts,
        "unexpectedCollisionPairs": tuple(unexpected),
        "unexpectedCollisionMm3ByPair": unexpected,
        "passesExceptExpectedSixOpenRodOuterCollisions": (
            len(open_expected) == 6
            and all(value > 1.0e-7 for value in open_expected.values())
            and not unexpected
        ),
        "states": rows,
        "claimBoundary": (
            "evidence-only scaffold; six OPEN rod/solid-outer-plate collisions "
            "are intentional and no mechanism, product, print, or physical acceptance is claimed"
        ),
    }


def _occurrence(shape: Shape, label: str) -> Shape:
    shape.label = label
    return shape


def build_motion_state(
    state: StateName,
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Compound:
    u = STATE_U[state]
    theta = p.theta_end_deg * u
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
        p19.build_service_envelopes(theta, p),
    ]
    for name in ROD_NAMES:
        children.extend(
            (
                build_rod(name, theta, p),
                build_cap("left", name, theta, p),
                build_cap("right", name, theta, p),
            )
        )
    return Compound(
        children=children,
        label=(
            f"P20_R1_{state}_evidence_only_intentionally_colliding_"
            f"non_candidate_scaffold__{provenance_token(p)}"
        ),
    )


def build_full_motion_open(
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> Compound:
    children: list[Shape] = [
        _occurrence(build_center_axle(p), "motion_full_fixed_stepped_center_axle__P20_scaffold"),
        _occurrence(build_keeper("left", p), "motion_full_fixed_left_keeper__P20_scaffold"),
        _occurrence(build_keeper("right", p), "motion_full_fixed_right_keeper__P20_scaffold"),
        _occurrence(build_inner_plate("left", p), "motion_full_fixed_left_inner__P20_scaffold"),
        _occurrence(build_inner_plate("right", p), "motion_full_fixed_right_inner__P20_scaffold"),
        _occurrence(build_outer_plate("left", 0.0, p), "motion_full_rotating_left_outer__P20_scaffold"),
        _occurrence(build_outer_plate("right", 0.0, p), "motion_full_rotating_right_outer__P20_scaffold"),
        _occurrence(build_xt60_reference(p), "motion_full_fixed_xt60_reference__P20_scaffold"),
        _occurrence(build_workpiece_reference(0.0, p), "motion_full_fixed_workpiece_reference__P20_scaffold"),
    ]
    for name in ROD_NAMES:
        children.extend(
            (
                _occurrence(build_rod(name, 0.0, p), f"motion_full_{name}_rod__P20_scaffold"),
                _occurrence(build_cap("left", name, 0.0, p), f"motion_full_left_{name}_cap__P20_scaffold"),
                _occurrence(build_cap("right", name, 0.0, p), f"motion_full_right_{name}_cap__P20_scaffold"),
            )
        )
    return Compound(
        children=children,
        label=f"P20_R1_full_motion_evidence_only_non_candidate_scaffold__{provenance_token(p)}",
    )


def p20_scaffold_manifest(
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> dict[str, object]:
    return {
        "candidateStatus": SCAFFOLD_STATUS,
        "physicalAcceptanceClaimed": False,
        "productAcceptanceClaimed": False,
        "contractPath": P20_SCAFFOLD_CONTRACT_PATH,
        "contractSha256": P20_SCAFFOLD_CONTRACT_SHA256,
        "productBaseline": "P19 R1 b69b6ad12af611644987f026eef4940db9c7bb34",
        "parameters": asdict(p),
        "motion": {
            "sharedProgress": "u in [0,1]",
            "leftRotation": "-45u deg about A",
            "rightRotation": "+45u deg about A",
            "relativeTravelDeg": 90.0,
            "centeredFrame": "T_s(q,u)=A+R(alpha_s(u))*q",
            "fixedAxleLocalPoint": (0.0, 0.0),
        },
        "topology": {
            "outerRodRailCount": 0,
            "substituteOuterRodApertureCount": 0,
            "innerRodTrackCountPerSide": 3,
            "whiteRodCount": 3,
            "capCount": 6,
            "staticOccurrenceCount": 19,
            "staticServiceEnvelopeOccurrenceCount": 1,
            "fullMotionOccurrenceCount": 18,
        },
        "collisionEvidence": scaffold_collision_evidence(p),
    }


def manifest_sha256(
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> str:
    return sha256(
        json.dumps(p20_scaffold_manifest(p), sort_keys=True).encode("utf-8")
    ).hexdigest()


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def provenance_token(
    p: P20R1Parameters = P20_R1_SCAFFOLD_DEFAULTS,
) -> str:
    return f"manifest_{manifest_sha256(p)[:12]}__source_{source_revision_sha256()[:12]}"


def clear_geometry_caches() -> None:
    _outer_plate_local.cache_clear()
    scaffold_collision_evidence.cache_clear()
    p19.clear_geometry_caches()


__all__ = [
    "CollisionEvaluationError",
    "GUIDES",
    "MotionState",
    "P20R1Parameters",
    "P20_R1_SCAFFOLD_DEFAULTS",
    "PointYZ",
    "ROD_NAMES",
    "SCAFFOLD_STATUS",
    "build_center_axle",
    "build_full_motion_open",
    "build_inner_plate",
    "build_motion_state",
    "build_outer_plate",
    "build_rod",
    "centered_outer_local_to_world",
    "clear_geometry_caches",
    "fixed_axle_center_yz",
    "fixed_axle_guide_local_center",
    "intersection_volume",
    "manifest_sha256",
    "motion_state",
    "p20_scaffold_manifest",
    "parameters_from_env",
    "parameters_from_overrides",
    "provenance_token",
    "scaffold_collision_evidence",
    "source_revision_sha256",
    "world_to_centered_outer_local",
]
