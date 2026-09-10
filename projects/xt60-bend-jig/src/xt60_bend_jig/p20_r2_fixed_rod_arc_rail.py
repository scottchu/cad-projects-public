"""P20 R2 true fixed-rod arc-rail correction from the P19 product baseline.

This is deliberately an intermediate, non-product CAD candidate.  It removes
all six white-rod cuts from the two outer plates, so the three physical rods
are expected to intersect both solid outer plates.  The only new outer cuts
are the two side-specific 7.90 mm inverse-frame arc rails for the stationary
purple axle at A=(-15,-11), while both outer plates still rotate about C=(0,0).
"""

from __future__ import annotations

import json
import os
from copy import copy
from dataclasses import asdict, dataclass, fields
from functools import lru_cache
from hashlib import sha256
from math import hypot
from pathlib import Path
from typing import Literal

from build123d import Compound, Pos, Rot, Shape

from . import p19_r1_front_edge_short_tail as p19


SideName = Literal["left", "right"]
StateName = Literal["open", "mid", "end"]
PointYZ = p19.PointYZ
ROD_NAMES = p19.ROD_NAMES

P20_R2_CONTRACT_PATH = (
    "docs/iterations/p20-r2-fixed-rod-arc-rail/BRIEF.md"
)
P20_R2_CONTRACT_SHA256 = (
    "c56de0833258fbf932c8ea11f8d7e35c7ae2b7f8731c2486ebb53549cb1b726b"
)
P20_R2_IMPLEMENTATION_INPUT_SHA256 = (
    "acec208df5f1de3abcc9b245c51c6161f099363517f92616852c146677fcfb26"
)
OUTER_WHITE_ROD_CUT_COUNT = 0
INNER_WHITE_ROD_CUT_COUNT = 6
FIXED_AXLE_ARC_RAIL_COUNT = 2


@dataclass(frozen=True, slots=True)
class P20R2Parameters(p19.P19R1Parameters):
    """P19 parameter surface with exactly three authorized P20 R2 deltas."""

    def __post_init__(self) -> None:
        baseline = asdict(p19.P19_R1_DEFAULTS)
        candidate = asdict(self)
        expected = {
            "theta_end_deg": 45.0,
            "fixed_axle_center_y": -15.0,
            "fixed_axle_center_z": -11.0,
        }
        for name, baseline_value in baseline.items():
            wanted = expected.get(name, baseline_value)
            if candidate[name] != wanted:
                raise ValueError(
                    f"P20 R2 frozen parameter {name} must be {wanted!r}, "
                    f"not {candidate[name]!r}"
                )
        if self.fixed_axle_guide_sample_count != 33:
            raise ValueError("P20 R2 fixed axle arc requires exactly 33 samples")
        if abs(self.fixed_axle_guide_slot_width - 7.90) > 1.0e-12:
            raise ValueError("P20 R2 fixed axle arc cutter must be 7.90 mm")


_P20_VALUES = asdict(p19.P19_R1_DEFAULTS)
_P20_VALUES.update(
    theta_end_deg=45.0,
    fixed_axle_center_y=-15.0,
    fixed_axle_center_z=-11.0,
)
P20_R2_DEFAULTS = P20R2Parameters(**_P20_VALUES)
P20_R2_STATE_THETA: dict[StateName, float] = {
    "open": 0.0,
    "mid": 22.5,
    "end": 45.0,
}


def parameters_from_overrides(
    overrides: dict[str, object] | None = None,
) -> P20R2Parameters:
    overrides = overrides or {}
    unknown = set(overrides) - {field.name for field in fields(P20R2Parameters)}
    if unknown:
        raise ValueError(f"unknown P20 R2 parameter(s): {sorted(unknown)}")
    values = asdict(P20_R2_DEFAULTS)
    values.update(overrides)
    return P20R2Parameters(**values)


def parameters_from_env() -> P20R2Parameters:
    raw = os.environ.get("P20_R2_PARAMS_JSON", "").strip()
    return parameters_from_overrides(json.loads(raw) if raw else {})


def rotation_for_side(side: SideName, theta_deg: float) -> float:
    if side not in ("left", "right"):
        raise ValueError(f"unknown side {side!r}")
    return theta_deg if side == "left" else -theta_deg


def outer_rotation_center_yz(
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> PointYZ:
    return p19.outer_rotation_center_yz(p)


def fixed_axle_center_yz(
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> PointYZ:
    return p19.fixed_axle_center_yz(p)


def fixed_axle_local_center(
    side: SideName,
    u: float,
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> PointYZ:
    """One pure inverse-frame authority for both side-local axle loci."""
    if not 0.0 <= u <= 1.0:
        raise ValueError("P20 R2 rail progress must stay in 0..1")
    return p19.transform_point_between_frames(
        fixed_axle_center_yz(p),
        source_origin=PointYZ(0.0, 0.0),
        source_angle_deg=0.0,
        target_origin=outer_rotation_center_yz(p),
        target_angle_deg=rotation_for_side(side, p.theta_end_deg * u),
    )


def inverse_outer_local_to_world(
    side: SideName,
    point: PointYZ,
    u: float,
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> PointYZ:
    if not 0.0 <= u <= 1.0:
        raise ValueError("P20 R2 rail progress must stay in 0..1")
    return p19.transform_point_between_frames(
        point,
        source_origin=outer_rotation_center_yz(p),
        source_angle_deg=rotation_for_side(side, p.theta_end_deg * u),
        target_origin=PointYZ(0.0, 0.0),
        target_angle_deg=0.0,
    )


def reconstruct_fixed_axle_world(
    side: SideName,
    u: float,
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> PointYZ:
    return inverse_outer_local_to_world(
        side, fixed_axle_local_center(side, u, p), u, p
    )


def fixed_axle_rail_locus(
    side: SideName,
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> tuple[PointYZ, ...]:
    return tuple(
        fixed_axle_local_center(
            side, index / (p.fixed_axle_guide_sample_count - 1), p
        )
        for index in range(p.fixed_axle_guide_sample_count)
    )


@lru_cache(maxsize=None)
def _outer_plate_local(
    side: SideName,
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> Shape:
    diameter = (
        p.left_outer_secondary_grip_diameter
        if side == "left"
        else p.right_outer_primary_grip_diameter
    )
    color = "#377A3A" if side == "left" else "#2D6FA8"
    label = f"{side}_outer_fixed_axle_curved_rail_no_white_rod_outer_cuts"
    arc_cutter = p19._slot_capsule_cutter(
        fixed_axle_rail_locus(side, p),
        p.fixed_axle_guide_slot_width,
        p.outer_plate_thickness + 2.0,
    )
    part = p19._plate_blank(
        diameter,
        p.outer_plate_thickness,
        label,
        color,
        bore=arc_cutter,
    )
    part.label = label
    return part


def build_inner_plate(
    side: SideName,
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> Shape:
    return p19.build_inner_plate(side, p)


def build_outer_plate(
    side: SideName,
    theta_deg: float,
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> Shape:
    if not 0.0 <= theta_deg <= p.theta_end_deg:
        raise ValueError("P20 R2 outer angle must stay in 0..45 deg")
    x = p.left_outer_x if side == "left" else p.right_outer_x
    color = "#377A3A" if side == "left" else "#2D6FA8"
    center = outer_rotation_center_yz(p)
    local = _outer_plate_local(side, p)
    return p19._label(
        Pos(x, center.y, center.z)
        * Rot(rotation_for_side(side, theta_deg), 0.0, 0.0)
        * copy(local),
        local.label,
        color,
    )


def _occurrence(shape: Shape, label: str) -> Shape:
    shape.label = label
    return shape


def build_motion_state(
    state: StateName,
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> Compound:
    theta = P20_R2_STATE_THETA[state]
    children: list[Shape] = [
        _occurrence(p19.build_center_axle(p), "fixed_stepped_center_axle"),
        _occurrence(p19.build_keeper("left", p), "fixed_left_keeper"),
        _occurrence(p19.build_keeper("right", p), "fixed_right_keeper"),
        _occurrence(build_inner_plate("left", p), "fixed_left_inner_three_white_rod_rails"),
        _occurrence(build_inner_plate("right", p), "fixed_right_inner_three_white_rod_rails"),
        _occurrence(build_outer_plate("left", theta, p), "rotating_left_outer_fixed_axle_curved_rail"),
        _occurrence(build_outer_plate("right", theta, p), "rotating_right_outer_fixed_axle_curved_rail"),
        _occurrence(p19.build_xt60_reference(p), "fixed_xt60_reference"),
        _occurrence(p19.build_workpiece_reference(theta, p), "fixed_workpiece_reference"),
        _occurrence(p19.build_service_envelopes(theta, p), "reference_service_envelopes"),
    ]
    for name in ROD_NAMES:
        children.extend(
            (
                _occurrence(p19.build_rod(name, theta, p), f"{name}_OD4_rod_L50.00_expected_outer_collision"),
                _occurrence(p19.build_cap("left", name, theta, p), f"left_{name}_permanent_cap"),
                _occurrence(p19.build_cap("right", name, theta, p), f"right_{name}_permanent_cap"),
            )
        )
    return Compound(
        children=children,
        label=f"P20_R2_{state}_intermediate_non_product_arc_rail",
    )


def build_full_motion_open(
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> Compound:
    theta = 0.0
    children: list[Shape] = [
        _occurrence(p19.build_center_axle(p), "motion_full_fixed_stepped_center_axle"),
        _occurrence(p19.build_keeper("left", p), "motion_full_fixed_left_keeper"),
        _occurrence(p19.build_keeper("right", p), "motion_full_fixed_right_keeper"),
        _occurrence(build_inner_plate("left", p), "motion_full_fixed_left_inner"),
        _occurrence(build_inner_plate("right", p), "motion_full_fixed_right_inner"),
        _occurrence(build_outer_plate("left", theta, p), "motion_full_rotating_left_outer"),
        _occurrence(build_outer_plate("right", theta, p), "motion_full_rotating_right_outer"),
        _occurrence(p19.build_xt60_reference(p), "motion_full_fixed_xt60_reference"),
        _occurrence(p19.build_workpiece_reference(theta, p), "motion_full_fixed_workpiece_reference"),
    ]
    for name in ROD_NAMES:
        children.extend(
            (
                _occurrence(p19.build_rod(name, theta, p), f"motion_full_{name}_rod"),
                _occurrence(p19.build_cap("left", name, theta, p), f"motion_full_left_{name}_cap"),
                _occurrence(p19.build_cap("right", name, theta, p), f"motion_full_right_{name}_cap"),
            )
        )
    return Compound(
        children=children,
        label=f"P20_R2_full_motion_open__{provenance_token(p)}",
    )


def build_fixed_rail_review(
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> Compound:
    """Side-by-side plate-local review; colored witnesses sit inside both arcs."""
    children: list[Shape] = []
    for side, z_offset, color in (
        ("left", -34.0, "#B765D5"),
        ("right", 34.0, "#2FC9D1"),
    ):
        plate = Pos(0.0, 0.0, z_offset) * copy(_outer_plate_local(side, p))
        plate.label = f"review_{side}_outer_plate_full_7p90_arc_aperture"
        witness = Pos(0.0, 0.0, z_offset) * p19._slot_capsule_cutter(
            fixed_axle_rail_locus(side, p),
            1.0,
            p.outer_plate_thickness + 0.6,
        )
        witness = p19._label(
            witness,
            f"review_{side}_fixed_axle_arc_centerline_OPEN_to_END",
            color,
        )
        children.extend((plate, witness))
    return Compound(
        children=children,
        label="P20_R2_FOCUSED_BOTH_FIXED_AXLE_ARC_RAILS_NON_PRODUCT",
    )


def build_artifact(
    name: StateName | Literal["fixed_rail_review"],
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> Compound:
    if name == "fixed_rail_review":
        artifact = build_fixed_rail_review(p)
    elif name in P20_R2_STATE_THETA:
        artifact = build_motion_state(name, p)
    else:
        raise ValueError(f"unknown P20 R2 artifact {name!r}")
    return Compound(
        children=[artifact],
        label=f"P20_R2_ARTIFACT_{name}__{provenance_token(p)}",
    )


def topology_evidence(
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> dict[str, object]:
    radius = p.fixed_axle_eccentricity
    chord = fixed_axle_rail_locus("left", p)[0].distance_to(
        fixed_axle_rail_locus("left", p)[-1]
    )
    inner_exact = all(
        p19.fixed_guide_local_locus(name, p)
        == p19.fixed_guide_local_locus(name, p19.P19_R1_DEFAULTS)
        for name in ROD_NAMES
    )
    plates = {
        "left_inner": p19._inner_plate_local("left", p),
        "right_inner": p19._inner_plate_local("right", p),
        "left_outer": _outer_plate_local("left", p),
        "right_outer": _outer_plate_local("right", p),
    }
    return {
        "outerWhiteRodCutCount": OUTER_WHITE_ROD_CUT_COUNT,
        "innerWhiteRodCutCount": INNER_WHITE_ROD_CUT_COUNT,
        "fixedAxleArcRailCount": FIXED_AXLE_ARC_RAIL_COUNT,
        "fixedAxleArcRadiusMm": radius,
        "fixedAxleArcWidthMm": p.fixed_axle_guide_slot_width,
        "outerArcVsRoundEndpointChordMm": chord,
        "innerRailLociExactlyP19": inner_exact,
        "minimumOuterRimWebMm": min(
            p.left_outer_secondary_grip_diameter / 2.0
            - radius
            - p.fixed_axle_guide_slot_width / 2.0,
            p.right_outer_primary_grip_diameter / 2.0
            - radius
            - p.fixed_axle_guide_slot_width / 2.0,
        ),
        "allPlatesSingleValidSolids": all(
            len(shape.solids()) == 1 and shape.is_valid for shape in plates.values()
        ),
        "plateLabels": {name: shape.label for name, shape in plates.items()},
    }


@lru_cache(maxsize=None)
def fixed_axle_brep_evidence(
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> dict[str, object]:
    axle = p19.build_center_axle(p)
    intersections: dict[str, float] = {}
    clearances: dict[str, float] = {}
    solids: dict[str, bool] = {}
    for side in ("left", "right"):
        local = _outer_plate_local(side, p)
        solids[side] = len(local.solids()) == 1 and local.is_valid
        for index in range(p.fixed_axle_guide_sample_count):
            u = index / (p.fixed_axle_guide_sample_count - 1)
            outer = build_outer_plate(side, p.theta_end_deg * u, p)
            key = f"{side}:u_{u:.5f}"
            intersections[key] = p19._intersection_volume(axle, outer)
            clearances[key] = float(axle.distance(outer))
    maximum = max(intersections.values())
    minimum = min(clearances.values())
    return {
        "sampleCountPerSide": p.fixed_axle_guide_sample_count,
        "maximumAxleOuterPlateIntersectionMm3": maximum,
        "minimumAxleOuterPlateClearanceMm": minimum,
        "allOuterPlatesSingleValidSolids": all(solids.values()),
        "passes": maximum <= 1.0e-7 and minimum >= 0.148 and all(solids.values()),
        "intersectionRowsMm3": intersections,
        "clearanceRowsMm": clearances,
    }


@lru_cache(maxsize=None)
def collision_census_evidence(
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> dict[str, object]:
    expected_pairs = tuple(
        f"{name}_rod:{side}_outer"
        for name in ROD_NAMES
        for side in ("left", "right")
    )
    expected_rows: dict[str, list[float]] = {pair: [] for pair in expected_pairs}
    unexpected_rows: dict[str, float] = {}
    axle = p19.build_center_axle(p)
    keepers = {side: p19.build_keeper(side, p) for side in ("left", "right")}
    inners = {side: build_inner_plate(side, p) for side in ("left", "right")}
    body = p19.build_xt60_reference(p)

    def record(key: str, first: Shape, second: Shape) -> None:
        value = p19._intersection_volume(first, second)
        unexpected_rows[key] = max(unexpected_rows.get(key, 0.0), value)

    for index in range(p.fixed_axle_guide_sample_count):
        u = index / (p.fixed_axle_guide_sample_count - 1)
        theta = p.theta_end_deg * u
        outers = {side: build_outer_plate(side, theta, p) for side in ("left", "right")}
        rods = {name: p19.build_rod(name, theta, p) for name in ROD_NAMES}
        caps = {
            (side, name): p19.build_cap(side, name, theta, p)
            for side in ("left", "right")
            for name in ROD_NAMES
        }
        for name, rod in rods.items():
            for side, outer in outers.items():
                expected_rows[f"{name}_rod:{side}_outer"].append(
                    p19._intersection_volume(rod, outer)
                )
            record(f"{name}_rod:center_axle", rod, axle)
            record(f"{name}_rod:xt60", rod, body)
            for side in ("left", "right"):
                record(f"{name}_rod:{side}_inner", rod, inners[side])
                record(f"{name}_rod:{side}_keeper", rod, keepers[side])
        for side in ("left", "right"):
            record(f"center_axle:{side}_outer", axle, outers[side])
            record(f"{side}_keeper:{side}_outer", keepers[side], outers[side])
            record(f"{side}_inner:{side}_outer", inners[side], outers[side])
            record(f"{side}_outer:xt60", outers[side], body)
            for name in ROD_NAMES:
                cap = caps[(side, name)]
                record(f"{side}_{name}_cap:{side}_outer", cap, outers[side])
                record(f"{side}_{name}_cap:{side}_inner", cap, inners[side])
                record(f"{side}_{name}_cap:{side}_keeper", cap, keepers[side])

    tolerance = 1.0e-7
    unexpected = tuple(
        sorted(pair for pair, volume in unexpected_rows.items() if volume > tolerance)
    )
    all_expected = all(
        all(volume > tolerance for volume in rows)
        for rows in expected_rows.values()
    )
    return {
        "sampleCount": p.fixed_axle_guide_sample_count,
        "expectedCollisionPairs": expected_pairs,
        "expectedPairCount": len(expected_pairs),
        "allExpectedPairsCollideAtEveryState": all_expected,
        "minimumExpectedIntersectionMm3": min(
            volume for rows in expected_rows.values() for volume in rows
        ),
        "maximumUnexpectedIntersectionMm3": max(unexpected_rows.values()),
        "unexpectedCollisionPairs": unexpected,
        "passes": all_expected and not unexpected,
        "expectedIntersectionRowsMm3": expected_rows,
        "unexpectedMaximumRowsMm3": unexpected_rows,
    }


@lru_cache(maxsize=None)
def service_evidence(
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> dict[str, object]:
    production: dict[str, Shape] = {
        "center_axle": p19.build_center_axle(p),
        "left_keeper": p19.build_keeper("left", p),
        "right_keeper": p19.build_keeper("right", p),
        "left_inner": build_inner_plate("left", p),
        "right_inner": build_inner_plate("right", p),
        "left_outer": build_outer_plate("left", 0.0, p),
        "right_outer": build_outer_plate("right", 0.0, p),
        "xt60": p19.build_xt60_reference(p),
    }
    for name in ROD_NAMES:
        production[f"{name}_rod"] = p19.build_rod(name, 0.0, p)
        for side in ("left", "right"):
            production[f"{side}_{name}_cap"] = p19.build_cap(side, name, 0.0, p)
    service = p19.build_service_envelopes(0.0, p)
    tools = tuple(
        child
        for child in service.children
        if child.label.startswith("reference_soldering_tool_keepout")
    )
    intersections = {
        name: max(p19._intersection_volume(shape, tool) for tool in tools)
        for name, shape in production.items()
    }
    axle_clearances = [
        float(production["center_axle"].distance(target))
        for target in (p19.build_xt60_reference(p), *service.children)
    ]
    return {
        "state": "OPEN",
        "toolOccurrenceCount": len(tools),
        "maximumProductionToolIntersectionMm3": max(intersections.values()),
        "minimumAxleServiceClearanceMm": min(axle_clearances),
        "passes": (
            len(tools) == 2
            and max(intersections.values()) <= 1.0e-7
            and min(axle_clearances) > 0.0
        ),
        "productionToolIntersectionMm3ByObject": intersections,
        "physicalBoundary": "CAD service geometry only; no heat or ergonomic claim",
    }


def p20_r2_manifest(
    p: P20R2Parameters = P20_R2_DEFAULTS,
) -> dict[str, object]:
    return {
        "candidateStatus": "intermediate_non_product_fixed_rod_arc_rail",
        "physicalAcceptanceClaimed": False,
        "manufacturingAcceptanceClaimed": False,
        "productAcceptanceClaimed": False,
        "contractPath": P20_R2_CONTRACT_PATH,
        "contractSha256": P20_R2_CONTRACT_SHA256,
        "implementationInputManifestSha256": P20_R2_IMPLEMENTATION_INPUT_SHA256,
        "parameters": asdict(p),
        "outerRotationCenterYZ": outer_rotation_center_yz(p).as_tuple(),
        "fixedAxleCenterYZ": fixed_axle_center_yz(p).as_tuple(),
        "outerTravelDeg": {"left": 45.0, "right": -45.0, "relative": 90.0},
        "whiteRodOuterRailCount": OUTER_WHITE_ROD_CUT_COUNT,
        "whiteRodInnerRailCount": INNER_WHITE_ROD_CUT_COUNT,
        "fixedAxleArcRailCount": FIXED_AXLE_ARC_RAIL_COUNT,
        "knownRodOuterCollisionPairCount": 6,
        "knownCollisionBoundary": (
            "three OD4 rods intersect both solid outer plates; later rails are sequential"
        ),
        "nonGoals": (
            "white-rod outer rail sequencing",
            "mesh, 3MF, slicing or print",
            "force, torque, fit or physical acceptance",
        ),
    }


def manifest_sha256(p: P20R2Parameters = P20_R2_DEFAULTS) -> str:
    return sha256(
        json.dumps(p20_r2_manifest(p), sort_keys=True).encode("utf-8")
    ).hexdigest()


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def provenance_token(p: P20R2Parameters = P20_R2_DEFAULTS) -> str:
    return f"manifest_{manifest_sha256(p)[:12]}__source_{source_revision_sha256()[:12]}"


def clear_geometry_caches() -> None:
    _outer_plate_local.cache_clear()
    fixed_axle_brep_evidence.cache_clear()
    collision_census_evidence.cache_clear()
    service_evidence.cache_clear()
    p19.clear_geometry_caches()


__all__ = [
    "P20R2Parameters",
    "P20_R2_DEFAULTS",
    "P20_R2_STATE_THETA",
    "build_artifact",
    "build_fixed_rail_review",
    "build_full_motion_open",
    "build_motion_state",
    "build_outer_plate",
    "collision_census_evidence",
    "fixed_axle_brep_evidence",
    "fixed_axle_center_yz",
    "fixed_axle_local_center",
    "fixed_axle_rail_locus",
    "inverse_outer_local_to_world",
    "manifest_sha256",
    "outer_rotation_center_yz",
    "p20_r2_manifest",
    "parameters_from_env",
    "parameters_from_overrides",
    "provenance_token",
    "reconstruct_fixed_axle_world",
    "rotation_for_side",
    "service_evidence",
    "source_revision_sha256",
    "topology_evidence",
]
