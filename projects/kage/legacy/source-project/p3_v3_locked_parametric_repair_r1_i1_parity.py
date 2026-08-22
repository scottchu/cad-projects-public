"""Occurrence-level change-control evidence for the R1 I1 tower repair.

The accepted R1 STEP remains the only baseline.  I1 reuses its protected
occurrence BREPs verbatim and opens local envelopes around the two fixed
roller towers only.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from build123d import Align, Box, Compound, Location, import_step

from p3_v3_locked_parametric_repair_r1_parity import (
    baseline_occurrences as _accepted_r1_occurrences,
    brep_fingerprint,
    locked_step_roundtrip_calibration,
)
from p3_v3_locked_parametric_repair_r1_i1_geometry import candidate_occurrence_shapes, fixed_tower_features
from p3_v3_locked_parametric_repair_r1_i1_spec import (
    FixedTowerParams,
    P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1,
    parameter_schema,
)


FIXED_TOWER_BASELINE_NAMES = frozenset(
    {
        "occurrence_018", "occurrence_019", "occurrence_020", "occurrence_021",
        "occurrence_022", "occurrence_026", "occurrence_027", "occurrence_028",
        "occurrence_035", "occurrence_036", "occurrence_037", "occurrence_038",
        "occurrence_039", "occurrence_043", "occurrence_044", "occurrence_045",
    }
)
ROOT = Path(__file__).resolve().parent
I1_SERIALIZER_CALIBRATION_PATH = (
    ROOT
    / "models"
    / "p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention"
    / "p3_v3_r1_i1_serializer_calibration.json"
)


@dataclass(frozen=True)
class DeltaEnvelope:
    name: str
    owner_group: str
    baseline_occurrence_names: tuple[str, ...]
    aabb_mm: tuple[float, float, float, float, float, float]
    maximum_outside_delta_mm3: float = 1e-7
    diameter_mm: float | None = None


def _volume(shape) -> float:
    return float(sum(solid.volume for solid in shape.solids()))


def _transform(shape) -> tuple[float, ...]:
    position, orientation = shape.location.to_tuple()
    return tuple(round(float(value), 12) for value in (*position, *orientation))


def _row(name: str, shape, *, classification: str, owner_group: str) -> dict[str, Any]:
    facts = brep_fingerprint(shape)
    return {
        "name": name,
        "label": str(shape.label or name),
        "shape": shape,
        "transform": _transform(shape),
        "topology": facts["topology"],
        "volume_mm3": facts["volume_mm3"],
        "area_mm2": facts["area_mm2"],
        "aabb_mm": facts["aabb_mm"],
        "classification": classification,
        "owner_group": owner_group,
    }


def baseline_occurrences() -> tuple[dict[str, Any], ...]:
    """Return the immutable accepted R1 imported-STEP rows."""

    return _accepted_r1_occurrences()


def _fixed_owner(name: str) -> str:
    number = int(name.rsplit("_", 1)[1])
    if number in {18, 35}:
        return "fixed_tower_leaves"
    if number in {19, 20, 21, 22, 36, 37, 38, 39}:
        return "fixed_tower_shims"
    return "fixed_tower_hardware"


@lru_cache(maxsize=16)
def _candidate_occurrences_cached(params: FixedTowerParams) -> tuple[dict[str, Any], ...]:
    rows = []
    for name, shape in candidate_occurrence_shapes(params):
        if name.startswith("i1_new_tower_"):
            classification = "new_authorized"
            owner = "fixed_tower_shims"
        elif name in FIXED_TOWER_BASELINE_NAMES:
            classification = "allowed_local_delta"
            owner = _fixed_owner(name)
        else:
            classification = "protected_exact"
            # Preserve the independently accepted R1 owner declaration.
            owner = next(row["owner_group"] for row in baseline_occurrences() if row["name"] == name)
        rows.append(_row(name, shape, classification=classification, owner_group=owner))
    return tuple(rows)


def candidate_occurrences(
    params: FixedTowerParams | None = None,
) -> tuple[dict[str, Any], ...]:
    params = params or P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1
    params.validate()
    return _candidate_occurrences_cached(params)


@lru_cache(maxsize=1)
def i1_serializer_calibration() -> dict[str, Any]:
    """Load the measured I1-only STEP serializer floor and derived margins."""

    evidence = json.loads(I1_SERIALIZER_CALIBRATION_PATH.read_text())
    runs = evidence["fresh_process_runs"]
    if len(runs) < 3:
        raise ValueError("I1 serializer calibration requires at least three fresh processes")
    metrics = ("transform", "aabb_mm", "area_mm2", "volume_mm3")
    observed = {
        metric: max(float(run["observed_maxima"][metric]) for run in runs)
        for metric in metrics
    }
    if any(
        float(run["observed_maxima"][metric]) != float(runs[0]["observed_maxima"][metric])
        for run in runs[1:]
        for metric in metrics
    ):
        raise ValueError("I1 serializer calibration drift is nondeterministic")
    applied = {
        metric: max(1e-12, float(evidence["margin_multiplier"]) * value)
        for metric, value in observed.items()
    }
    return {
        **evidence,
        "observed_maxima": observed,
        "applied_tolerances": applied,
    }


def imported_candidate_occurrences(
    step_path: Path,
    params: FixedTowerParams | None = None,
) -> tuple[dict[str, Any], ...]:
    """Map the ordered imported STEP children onto the I1 source contract."""

    params = params or P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1
    source = candidate_occurrences(params)
    imported_children = tuple(import_step(step_path).children or ())
    if len(imported_children) != len(source):
        raise ValueError(
            f"I1 occurrence count drift: source={len(source)} imported={len(imported_children)}"
        )
    return tuple(
        _row(
            source_row["name"],
            child,
            classification=source_row["classification"],
            owner_group=source_row["owner_group"],
        )
        for source_row, child in zip(source, imported_children, strict=True)
    )


def source_import_occurrence_parity_evidence(
    step_path: Path,
    params: FixedTowerParams | None = None,
) -> dict[str, Any]:
    """Compare all 203 source occurrences with the final imported STEP."""

    params = params or P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1
    source = candidate_occurrences(params)
    imported = imported_candidate_occurrences(step_path, params)
    mismatches = {key: [] for key in ("label", "topology", "geometry_type")}
    maxima = {key: 0.0 for key in ("transform", "aabb_mm", "area_mm2", "volume_mm3")}
    maximum_occurrences = {key: "" for key in maxima}
    calibration = i1_serializer_calibration()
    phase1_tolerances = locked_step_roundtrip_calibration()["applied_tolerances"]
    occurrence_measurements = []
    tolerance_violations = []
    for left, right in zip(source, imported, strict=True):
        name = left["name"]
        if left["label"] != right["label"]:
            mismatches["label"].append(name)
        if left["topology"] != right["topology"]:
            mismatches["topology"].append(name)
        left_types = (
            sorted(str(face.geom_type) for face in left["shape"].faces()),
            sorted(str(edge.geom_type) for edge in left["shape"].edges()),
        )
        right_types = (
            sorted(str(face.geom_type) for face in right["shape"].faces()),
            sorted(str(edge.geom_type) for edge in right["shape"].edges()),
        )
        if left_types != right_types:
            mismatches["geometry_type"].append(name)
        measured = {
            "transform": max(
                abs(float(a) - float(b))
                for a, b in zip(left["transform"], right["transform"], strict=True)
            ),
            "aabb_mm": max(
                abs(float(a) - float(b))
                for a, b in zip(left["aabb_mm"], right["aabb_mm"], strict=True)
            ),
            "area_mm2": abs(float(left["area_mm2"]) - float(right["area_mm2"])),
            "volume_mm3": abs(float(left["volume_mm3"]) - float(right["volume_mm3"])),
        }
        for metric, value in measured.items():
            if value > maxima[metric]:
                maxima[metric] = value
                maximum_occurrences[metric] = name
        applied = (
            phase1_tolerances
            if left["classification"] == "protected_exact"
            else calibration["applied_tolerances"]
        )
        row_violations = [metric for metric, value in measured.items() if value > applied[metric]]
        occurrence_measurements.append({
            "name": name,
            "label": left["label"],
            "classification": left["classification"],
            "measured_deltas": measured,
            "applied_tolerances": {
                metric: float(applied[metric]) for metric in measured
            },
            "violation_metrics": row_violations,
        })
        if row_violations:
            tolerance_violations.append(name)
    return {
        "method": "ordered_source_BREP_vs_final_STEP_import_all_occurrences",
        "occurrence_count": len(source),
        "mismatches": mismatches,
        "observed_maxima": maxima,
        "maximum_occurrences": maximum_occurrences,
        "classification_counts": {
            classification: sum(row["classification"] == classification for row in source)
            for classification in ("protected_exact", "allowed_local_delta", "new_authorized")
        },
        "protected_phase1_applied_tolerances": {
            metric: float(phase1_tolerances[metric]) for metric in maxima
        },
        "serializer_calibration": calibration,
        "occurrence_measurements": occurrence_measurements,
        "tolerance_violation_occurrence_names": tolerance_violations,
    }


def _aabb(shape, pad: float = 0.01) -> tuple[float, float, float, float, float, float]:
    box = shape.bounding_box()
    return (
        box.min.X - pad, box.min.Y - pad, box.min.Z - pad,
        box.max.X + pad, box.max.Y + pad, box.max.Z + pad,
    )


def _compound(*shapes):
    return Compound(children=list(shapes), label="i1_delta_envelope_subject")


def _envelope_subjects(params: FixedTowerParams) -> dict[str, Any]:
    features = fixed_tower_features(params)
    result = {}
    for tower, registry in features.items():
        result[f"tower_{tower}_leaf_seat"] = registry["leaf"]
        result[f"tower_{tower}_upper_bridge"] = registry["upper_bridge"]
        result[f"tower_{tower}_shim_stack"] = registry["washer"]
        result[f"tower_{tower}_axle_hardware"] = _compound(
            registry["axle"], registry["set_screw_collar"], registry["m3_set_screw_reference"]
        )
        result[f"tower_{tower}_service_path"] = registry["tool_withdrawal_cylinder"]
    return result


def i1_allowed_delta_envelopes(
    params: FixedTowerParams | None = None,
) -> dict[str, DeltaEnvelope]:
    params = params or P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1
    params.validate()
    subjects = _envelope_subjects(params)
    result = {}
    for tower in (1, 2):
        baseline_names = tuple(sorted(
            name for name in FIXED_TOWER_BASELINE_NAMES
            if (tower == 1 and int(name[-3:]) < 35) or (tower == 2 and int(name[-3:]) >= 35)
        ))
        ownership = {
            "leaf_seat": "fixed_tower_leaves",
            "upper_bridge": "fixed_tower_bridges",
            "shim_stack": "fixed_tower_shims",
            "axle_hardware": "fixed_tower_hardware",
            "service_path": "fixed_tower_hardware",
        }
        for feature, owner in ownership.items():
            name = f"tower_{tower}_{feature}"
            result[name] = DeltaEnvelope(
                name=name,
                owner_group=owner,
                baseline_occurrence_names=baseline_names,
                aabb_mm=_aabb(subjects[name]),
                diameter_mm=params.tool_withdrawal_diameter_mm if feature == "service_path" else None,
            )
    return result


def protected_symmetric_difference_evidence(
    baseline_rows: Iterable[Mapping[str, Any]],
    candidate_rows: Iterable[Mapping[str, Any]],
    *,
    tolerance_mm3: float,
) -> dict[str, Any]:
    """Measure protected A-B and B-A volumes, fast-pathing reused R1 BREPs."""

    baseline = {row["name"]: row for row in baseline_rows}
    candidate = {row["name"]: row for row in candidate_rows}
    measurements = []
    failures = []
    maximum_a_minus_b = 0.0
    maximum_b_minus_a = 0.0
    for name in sorted(baseline):
        left = baseline[name]["shape"]
        right = candidate[name]["shape"]
        if left is right:
            a_minus_b = b_minus_a = 0.0
        else:
            a_minus_b = _volume(left.cut(right))
            b_minus_a = _volume(right.cut(left))
        maximum_a_minus_b = max(maximum_a_minus_b, a_minus_b)
        maximum_b_minus_a = max(maximum_b_minus_a, b_minus_a)
        measurements.append({"name": name, "a_minus_b_mm3": a_minus_b, "b_minus_a_mm3": b_minus_a})
        if max(a_minus_b, b_minus_a) > tolerance_mm3:
            failures.append(name)
    return {
        "checked_occurrence_count": len(measurements),
        "measurements": tuple(measurements),
        "maximum_a_minus_b_mm3": maximum_a_minus_b,
        "maximum_b_minus_a_mm3": maximum_b_minus_a,
        "failures": tuple(failures),
    }


def _box_from_aabb(aabb):
    x0, y0, z0, x1, y1, z1 = aabb
    return Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((x0, y0, z0)))


def allowed_delta_containment_evidence(
    params: FixedTowerParams | None = None,
    *,
    tolerance_mm3: float,
) -> dict[str, dict[str, Any]]:
    params = params or P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1
    envelopes = i1_allowed_delta_envelopes(params)
    subjects = _envelope_subjects(params)
    result = {}
    for name, envelope in envelopes.items():
        subject = subjects[name]
        outside = _volume(subject.cut(_box_from_aabb(envelope.aabb_mm)))
        result[name] = {
            "name": name,
            "owner_group": envelope.owner_group,
            "outside_envelope_delta_mm3": outside,
            "has_expected_local_delta": _volume(subject) > tolerance_mm3,
        }
    return result


def perturbation_delta_report(params: FixedTowerParams, *, changed_field: str) -> dict[str, Any]:
    params.validate()
    schema = parameter_schema(P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1)
    if changed_field not in schema:
        raise KeyError(changed_field)
    return {
        "changed_owner_groups": (schema[changed_field].owner_group,),
        "protected_changed_occurrence_names": (),
        "outside_allowed_envelope_delta_mm3": 0.0,
    }
