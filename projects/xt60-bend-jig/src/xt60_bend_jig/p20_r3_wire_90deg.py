"""P20 R3 wire-only correction on the committed P20 R2 assembly.

Every mechanism occurrence comes directly from P20 R2. The sole replacement
is the workpiece reference: P18's accepted vertical + R6 quarter-circle +
horizontal ``└`` topology is substituted for P19's inherited diagonal wire.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any

from build123d import Compound, Shape

from . import p18_r1_compact_counter_twist as p18
from . import p20_r2_fixed_rod_arc_rail as p20r2


P20_R2_HEAD = "9698cf30e9ddb3e576c08179bfdd067446514c67"
P20_R2_SOURCE_SHA256 = (
    "1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73"
)
P20_R2_FIXED_RAIL_STEP_SHA256 = (
    "07c398b9b01233150dc4ca0805e2a7e2980f60fff302e1442654e0c3fb3f8f2c"
)
P20_R2_FULL_MOTION_STEP_SHA256 = (
    "715851b434ab2e17a7f6c29be0b21924fb99ed6e28c20be8b276399a5d1d6bca"
)
P18_ACCEPTED_SOURCE_SHA256 = (
    "37a45b972afb534e695b6c334b72ec451f4d466aafedab12c22afd90b866440f"
)
WORKPIECE_OCCURRENCE_LABEL = "motion_full_fixed_workpiece_reference"


def _round(value: float) -> float:
    return round(float(value), 9)


def shape_signature(shape: Shape) -> tuple[Any, ...]:
    """Deterministic geometry signature for bounded occurrence regression."""
    bounds = shape.bounding_box()
    return (
        tuple(_round(value) for value in (bounds.min.X, bounds.min.Y, bounds.min.Z)),
        tuple(_round(value) for value in (bounds.max.X, bounds.max.Y, bounds.max.Z)),
        _round(shape.volume),
        len(shape.solids()),
        bool(shape.is_valid),
    )


def build_workpiece_reference_90deg(theta_deg: float = 0.0) -> Shape:
    """Delegate exactly to P18's accepted two-conductor 90-degree workpiece."""
    workpiece = p18.build_workpiece_reference(theta_deg, p18.P18_R1_DEFAULTS)
    workpiece.label = WORKPIECE_OCCURRENCE_LABEL
    return workpiece


def build_full_motion_open(
    p: p20r2.P20R2Parameters = p20r2.P20_R2_DEFAULTS,
) -> Compound:
    """Replace exactly one workpiece occurrence in the P20 R2 assembly."""
    base = p20r2.build_full_motion_open(p)
    children: list[Shape] = []
    replacement_count = 0
    for child in base.children:
        if child.label == WORKPIECE_OCCURRENCE_LABEL:
            children.append(build_workpiece_reference_90deg(0.0))
            replacement_count += 1
        else:
            children.append(child)
    if replacement_count != 1:
        raise RuntimeError(
            f"expected one P20 R2 workpiece occurrence, found {replacement_count}"
        )
    return Compound(
        children=children,
        label="P20_R3_full_motion_wire_only_90deg__P20_R2_MECHANISM_FROZEN",
    )


def wire_90deg_evidence() -> dict[str, object]:
    accepted = p18.workpiece_orientation_evidence(p18.P18_R1_DEFAULTS)
    return {
        "frontViewForm": accepted["frontViewForm"],
        "bendCenterYZ": accepted["bendCenterYZ"],
        "bendRadiusMm": accepted["bendRadiusMm"],
        "turnAngleDeg": 90.0,
        "turnAngleRad": 1.5707963267948966,
        "verticalLeg": {
            "yMm": -5.0,
            "fromZMm": 1.5,
            "toZMm": 20.5,
            "direction": "+Z toward XT60 / -Z away from XT60",
        },
        "horizontalTail": {
            "zMm": -4.5,
            "fromYMm": 1.0,
            "toYMm": 13.0,
            "direction": "+Y",
        },
        "verticalTangentYZ": accepted["arcTangenciesYZ"]["vertical"],
        "horizontalTangentYZ": accepted["arcTangenciesYZ"]["horizontal"],
        "tangentDot": 0.0,
        "usesP18AcceptedBuilder": True,
        "usesDiagonalLineParameters": False,
        "p18AcceptedSourceSha256": P18_ACCEPTED_SOURCE_SHA256,
    }


def non_workpiece_invariance_evidence(
    p: p20r2.P20R2Parameters = p20r2.P20_R2_DEFAULTS,
) -> dict[str, object]:
    baseline = p20r2.build_full_motion_open(p)
    candidate = build_full_motion_open(p)
    baseline_rows = {child.label: shape_signature(child) for child in baseline.children}
    candidate_rows = {child.label: shape_signature(child) for child in candidate.children}
    mismatches: dict[str, object] = {}
    for label, signature in baseline_rows.items():
        if label == WORKPIECE_OCCURRENCE_LABEL:
            continue
        if candidate_rows.get(label) != signature:
            mismatches[label] = {
                "p20R2": signature,
                "p20R3": candidate_rows.get(label),
            }
    return {
        "p20R2OccurrenceCount": len(baseline.children),
        "p20R3OccurrenceCount": len(candidate.children),
        "replacedOccurrenceLabels": (WORKPIECE_OCCURRENCE_LABEL,),
        "allNonWorkpieceLabelsAndGeometrySignaturesIdentical": not mismatches,
        "mismatches": mismatches,
        "workpieceChanged": (
            baseline_rows[WORKPIECE_OCCURRENCE_LABEL]
            != candidate_rows[WORKPIECE_OCCURRENCE_LABEL]
        ),
        "p20R2WorkpieceSignature": baseline_rows[WORKPIECE_OCCURRENCE_LABEL],
        "p20R3WorkpieceSignature": candidate_rows[WORKPIECE_OCCURRENCE_LABEL],
    }


def p20_r3_manifest() -> dict[str, object]:
    return {
        "candidateStatus": "P20 R3 wire-only 90-degree digital correction",
        "baselineHead": P20_R2_HEAD,
        "p20R2SourceSha256": P20_R2_SOURCE_SHA256,
        "p20R2FixedRailStepSha256": P20_R2_FIXED_RAIL_STEP_SHA256,
        "p20R2FullMotionStepSha256": P20_R2_FULL_MOTION_STEP_SHA256,
        "mechanismAuthority": "p20_r2_fixed_rod_arc_rail.build_full_motion_open",
        "onlyReplacement": WORKPIECE_OCCURRENCE_LABEL,
        "workpieceAuthority": "p18_r1_compact_counter_twist.build_workpiece_reference",
        "wire": wire_90deg_evidence(),
        "whiteRodOuterRailCount": 0,
        "physicalAcceptanceClaimed": False,
        "manufacturingAcceptanceClaimed": False,
        "nonGoals": (
            "mechanism or rail changes",
            "collision sweep",
            "mesh, slicing or printing",
        ),
    }


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


__all__ = [
    "build_full_motion_open",
    "build_workpiece_reference_90deg",
    "non_workpiece_invariance_evidence",
    "p20_r3_manifest",
    "shape_signature",
    "source_revision_sha256",
    "wire_90deg_evidence",
]
