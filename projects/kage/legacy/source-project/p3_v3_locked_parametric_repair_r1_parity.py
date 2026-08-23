"""Occurrence-level parity evidence for the KAGE locked parametric copy."""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import tempfile
from typing import Any, Iterable, Mapping

from p3_v3_locked_parametric_repair_r1_geometry import (
    LOCKED_ROOT,
    ROOT,
    build_candidate,
    flatten_occurrences,
)
from build123d import export_step, import_step
from p3_v3_locked_parametric_repair_r1_spec import (
    P3V3LockedParametricRepairR1,
    P3_V3_LOCKED_PARAMETRIC_REPAIR_R1,
)


LOCKED_BASELINE = {
    "root": LOCKED_ROOT,
    "generator": LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step.py",
    "step": LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step",
}

# Candidate parity is intentionally evaluated only after the same STEP
# serialization boundary as the immutable baseline.  This is not an export
# artifact path; the directory is process-local and deleted automatically.
_PARITY_TMP = tempfile.TemporaryDirectory(prefix="kage_p3_v3_r1_parity_")
_PARITY_TMP_ROOT = Path(_PARITY_TMP.name)


def hash_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _transform(shape) -> tuple[float, ...]:
    position, orientation = shape.location.to_tuple()
    return tuple(round(float(value), 12) for value in (*position, *orientation))


def _aabb(shape) -> tuple[float, ...]:
    box = shape.bounding_box()
    return tuple(round(float(value), 9) for value in (
        box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z,
    ))


def _topology(shape) -> dict[str, int]:
    return {
        "solids": len(shape.solids()),
        "shells": len(shape.shells()),
        "faces": len(shape.faces()),
        "edges": len(shape.edges()),
        "vertices": len(shape.vertices()),
    }


_FINGERPRINT_CACHE: dict[int, dict[str, Any]] = {}


def brep_fingerprint(shape) -> dict[str, Any]:
    """Hash canonical BREP geometry facts plus independent mass facts.

    OCC's ASCII writer preserves internal entity numbering, which can differ
    after an otherwise exact deterministic rebuild.  Canonical sorted vertex,
    edge, and face facts reject real topology/geometry drift without treating
    harmless OCC numbering as a model change.
    """

    key = id(shape)
    cached = _FINGERPRINT_CACHE.get(key)
    if cached is not None:
        return dict(cached)
    topology = _topology(shape)
    vertex_points = sorted(
        tuple(round(float(axis), 9) for axis in (vertex.X, vertex.Y, vertex.Z))
        for vertex in shape.vertices()
    )
    edge_facts = sorted(
        (
            str(edge.geom_type),
            round(float(edge.length), 9),
            tuple(round(float(axis), 9) for axis in edge.center()),
        )
        for edge in shape.edges()
    )
    face_facts = sorted(
        (
            str(face.geom_type),
            round(float(face.area), 9),
            tuple(round(float(axis), 9) for axis in face.center()),
        )
        for face in shape.faces()
    )
    canonical = json.dumps(
        {
            "topology": topology,
            "vertices": vertex_points,
            "edges": edge_facts,
            "faces": face_facts,
            "aabb": _aabb(shape),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    result = {
        "brep_sha256": sha256(canonical).hexdigest(),
        "topology": topology,
        "volume_mm3": round(float(sum(s.volume for s in shape.solids())), 9),
        "area_mm2": round(float(sum(f.area for f in shape.faces())), 9),
        "aabb_mm": _aabb(shape),
    }
    _FINGERPRINT_CACHE[key] = result
    return dict(result)


def _owner_group(label: str) -> str:
    if "_RIGID_q" in label or "_RADIAL_SLOT_q" in label:
        return "motor_stations"
    if "quadrant_Q" in label or "splice" in label or "fin" in label:
        return "role_rings"
    if "tower" in label or "roller" in label:
        return "fixed_towers"
    if "chassis" in label or "frame" in label or "front_ring" in label:
        return "global_envelope"
    if "clamp" in label or "REFERENCE" in label:
        return "hardware"
    return "stationary_joints"


def _rows(shape, *, adjustments: tuple[float, float, float]) -> tuple[dict[str, Any], ...]:
    changed = any(abs(value) > 1e-12 for value in adjustments)
    rows = []
    for index, occurrence in enumerate(flatten_occurrences(shape)):
        label = str(occurrence.label or f"unlabeled_{index:03d}")
        owner = _owner_group(label)
        facts = brep_fingerprint(occurrence)
        classification = "allowed_local_delta" if changed and owner == "motor_stations" else "protected_exact"
        rows.append({
            "name": f"occurrence_{index:03d}",
            "label": label,
            "transform": _transform(occurrence),
            "shape": occurrence,
            "topology": facts["topology"],
            "volume_mm3": facts["volume_mm3"],
            "area_mm2": facts["area_mm2"],
            "aabb_mm": facts["aabb_mm"],
            "classification": classification,
            "owner_group": owner,
        })
    return tuple(rows)


def _raw_representation_delta(
    base_rows: Iterable[Mapping[str, Any]],
    candidate_rows: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Quantify serializer representation drift without hiding geometry drift."""

    base = {row["name"]: row for row in base_rows}
    candidate = {row["name"]: row for row in candidate_rows}
    common = sorted(set(base) & set(candidate))
    topology_mismatches = []
    geometry_type_mismatches = []
    label_mismatches = []
    max_transform = max_aabb = max_area = max_volume = 0.0
    for name in common:
        left, right = base[name], candidate[name]
        if left["label"] != right["label"]:
            label_mismatches.append(name)
        if left["topology"] != right["topology"]:
            topology_mismatches.append(name)
        left_face_types = sorted(str(face.geom_type) for face in left["shape"].faces())
        right_face_types = sorted(str(face.geom_type) for face in right["shape"].faces())
        left_edge_types = sorted(str(edge.geom_type) for edge in left["shape"].edges())
        right_edge_types = sorted(str(edge.geom_type) for edge in right["shape"].edges())
        if left_face_types != right_face_types or left_edge_types != right_edge_types:
            geometry_type_mismatches.append(name)
        max_transform = max(
            max_transform,
            *(abs(float(a) - float(b)) for a, b in zip(left["transform"], right["transform"])),
        )
        max_aabb = max(
            max_aabb,
            *(abs(float(a) - float(b)) for a, b in zip(left["aabb_mm"], right["aabb_mm"])),
        )
        max_area = max(max_area, abs(float(left["area_mm2"]) - float(right["area_mm2"])))
        max_volume = max(max_volume, abs(float(left["volume_mm3"]) - float(right["volume_mm3"])))
    return {
        "common_occurrence_count": len(common),
        "added_occurrence_names": sorted(set(candidate) - set(base)),
        "removed_occurrence_names": sorted(set(base) - set(candidate)),
        "label_mismatch_occurrence_names": label_mismatches,
        "topology_mismatch_occurrence_names": topology_mismatches,
        "geometry_type_mismatch_occurrence_names": geometry_type_mismatches,
        "maximum_transform_delta": max_transform,
        "maximum_aabb_delta_mm": max_aabb,
        "maximum_area_delta_mm2": max_area,
        "maximum_volume_delta_mm3": max_volume,
    }


@lru_cache(maxsize=1)
def baseline_occurrences() -> tuple[dict[str, Any], ...]:
    # Independent evidence path: baseline geometry comes from the immutable
    # locked STEP artifact, never from the candidate or copied generator.
    return _rows(import_step(LOCKED_BASELINE["step"]), adjustments=(0.0, 0.0, 0.0))


@lru_cache(maxsize=1)
def locked_step_roundtrip_calibration() -> dict[str, Any]:
    """Measure the serializer's own numeric floor from the immutable STEP.

    Applied comparison tolerances are exactly twice the observed locked STEP
    round-trip maxima (plus a 1e-12 numeric guard when the observed value is
    zero).  They are evidence, not a replacement for exact topology/type and
    imported-vs-imported fingerprint parity.
    """

    roundtrip_step = _PARITY_TMP_ROOT / "locked_step_roundtrip.step"
    source_rows = baseline_occurrences()
    from build123d import Compound

    export_step(
        Compound(children=[row["shape"] for row in source_rows], label="locked_roundtrip"),
        roundtrip_step,
    )
    roundtrip_rows = _rows(import_step(roundtrip_step), adjustments=(0.0, 0.0, 0.0))
    observed = _raw_representation_delta(source_rows, roundtrip_rows)
    applied = {
        "transform": max(1e-12, 2.0 * observed["maximum_transform_delta"]),
        "aabb_mm": max(1e-12, 2.0 * observed["maximum_aabb_delta_mm"]),
        "area_mm2": max(1e-12, 2.0 * observed["maximum_area_delta_mm2"]),
        "volume_mm3": max(1e-12, 2.0 * observed["maximum_volume_delta_mm3"]),
        "protected_symmetric_difference_mm3": 1e-7,
    }
    return {
        "method": "immutable_locked_step_export_reimport_observed_max_times_two",
        "source_path": str(LOCKED_BASELINE["step"]),
        "roundtrip_path": str(roundtrip_step),
        "observed": observed,
        "applied_tolerances": applied,
    }


@lru_cache(maxsize=8)
def _candidate_evidence_for_adjustments(
    adjustments: tuple[float, float, float],
) -> tuple[tuple[dict[str, Any], ...], tuple[dict[str, Any], ...], Path]:
    if adjustments == (0.0, 0.0, 0.0):
        # Build independently from the candidate adapter, while preserving a
        # cached result for the repeated parity tests.
        shape = build_candidate(P3_V3_LOCKED_PARAMETRIC_REPAIR_R1)["shape"]
    else:
        from dataclasses import replace

        params = replace(
            P3_V3_LOCKED_PARAMETRIC_REPAIR_R1,
            service_states=replace(
                P3_V3_LOCKED_PARAMETRIC_REPAIR_R1.service_states,
                motor_adjustments_mm=adjustments,
            ),
        )
        shape = build_candidate(params)["shape"]

    # Compare imported STEP with imported STEP.  Comparing an in-memory OCC
    # rebuild directly with a STEP import produced harmless 1e-9 mm2/mm3 mass
    # representation drift and was therefore asymmetric evidence.
    token = "_".join(f"{value:+.6f}".replace("+", "p").replace("-", "m") for value in adjustments)
    candidate_step = _PARITY_TMP_ROOT / f"candidate_{token}.step"
    export_step(shape, candidate_step)
    source_rows = _rows(shape, adjustments=adjustments)
    imported_rows = _rows(import_step(candidate_step), adjustments=adjustments)
    return source_rows, imported_rows, candidate_step


def _candidate_for_adjustments(adjustments: tuple[float, float, float]) -> tuple[dict[str, Any], ...]:
    return _candidate_evidence_for_adjustments(adjustments)[1]


def candidate_occurrences(
    params: P3V3LockedParametricRepairR1 | None = None,
) -> tuple[dict[str, Any], ...]:
    params = params or P3_V3_LOCKED_PARAMETRIC_REPAIR_R1
    params.validate()
    return _candidate_for_adjustments(tuple(params.service_states.motor_adjustments_mm))


def protected_feature_masks() -> dict[str, Any]:
    p = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1
    return {
        "ring_teeth": p.gear_train.ring_teeth,
        "pinion_teeth": p.gear_train.pinion_teeth,
        "module_mm": p.gear_train.module_mm,
        "carrier_race_radius_mm": p.gear_train.carrier_race_radius_mm,
        "tooth_tip_radius_mm": p.gear_train.tooth_tip_radius_mm,
        "tooth_root_radius_mm": p.gear_train.tooth_root_radius_mm,
        "ring_body_outer_radius_mm": p.gear_train.ring_body_outer_radius_mm,
        "carrier_layers_mm": p.role_rings.carrier_layers_mm,
        "fin_radial_ranges_mm": p.role_rings.fin_radial_ranges_mm,
        "fin_start_z_mm": p.role_rings.fin_start_z_mm,
        "fin_tip_z_mm": p.role_rings.fin_tip_z_mm,
        "fin_angles_deg": p.role_rings.fin_angles_deg,
        "motor_station_angles_deg": p.motor_stations.station_angles_deg,
        "output_axis_radius_mm": p.gear_train.output_axis_radius_mm,
        "motor_yoke_occurrence_count": 3,
        "nema8_occurrence_count": 3,
        "rear_chassis_quadrant_count": 4,
        "outer_frame_post_count": 6,
        "overall_aabb_mm": (-150.0, -150.0, -32.5, 150.0, 150.0, 24.2514),
    }


def _signature(row: Mapping[str, Any]) -> tuple[Any, ...]:
    facts = brep_fingerprint(row["shape"])
    return (
        row["label"], tuple(row["transform"]), facts["brep_sha256"],
        facts["topology"], facts["volume_mm3"], facts["area_mm2"], tuple(facts["aabb_mm"]),
    )


def diff_occurrence_sets(
    base: Mapping[str, Mapping[str, Any]],
    candidate: Mapping[str, Mapping[str, Any]],
) -> dict[str, list[str]]:
    base_names, candidate_names = set(base), set(candidate)
    common = base_names & candidate_names
    return {
        "changed_occurrence_names": sorted(name for name in common if _signature(base[name]) != _signature(candidate[name])),
        "added_occurrence_names": sorted(candidate_names - base_names),
        "removed_occurrence_names": sorted(base_names - candidate_names),
    }


def _shape_volume(shape) -> float:
    return float(sum(solid.volume for solid in shape.solids()))


@lru_cache(maxsize=8)
def protected_symmetric_difference_evidence(
    adjustments: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> dict[str, Any]:
    """Measure A-B and B-A volume for every protected occurrence.

    This is an actual OCC boolean gate, not an inference from matching mass or
    hashes.  Candidate shapes have already crossed the STEP export/import
    boundary, so both sides of the measurement are imported STEP BREPs.
    """

    baseline = {row["name"]: row for row in baseline_occurrences()}
    candidate_rows = _candidate_for_adjustments(adjustments)
    candidate = {row["name"]: row for row in candidate_rows}
    tolerance = float(
        locked_step_roundtrip_calibration()["applied_tolerances"]
        ["protected_symmetric_difference_mm3"]
    )
    measurements = []
    violations = []
    maximum = 0.0
    for name in sorted(set(baseline) & set(candidate)):
        row = candidate[name]
        if row["classification"] != "protected_exact":
            continue
        left = baseline[name]["shape"]
        right = row["shape"]
        a_minus_b = _shape_volume(left.cut(right))
        b_minus_a = _shape_volume(right.cut(left))
        measured = max(a_minus_b, b_minus_a)
        maximum = max(maximum, measured)
        result = {
            "name": name,
            "a_minus_b_mm3": a_minus_b,
            "b_minus_a_mm3": b_minus_a,
            "maximum_mm3": measured,
            "passes": measured <= tolerance,
        }
        measurements.append(result)
        if not result["passes"]:
            violations.append(name)
    return {
        "method": "OCC_boolean_cut_imported_locked_STEP_vs_imported_candidate_STEP",
        "tolerance_mm3": tolerance,
        "protected_occurrence_count": len(measurements),
        "maximum_symmetric_difference_mm3": maximum,
        "violation_occurrence_names": violations,
        "occurrences": measurements,
    }


def validate_parity_manifest(rows: Iterable[Mapping[str, Any]]) -> None:
    known = {row["name"] for row in baseline_occurrences()}
    allowed = {"protected_exact", "allowed_local_delta", "new_authorized"}
    for row in rows:
        name = str(row["name"])
        if name not in known:
            raise ValueError(f"unknown occurrence {name!r} is unauthorized")
        if row.get("classification") not in allowed:
            raise ValueError(f"occurrence {name!r} has unknown classification")


def parity_manifest(params: P3V3LockedParametricRepairR1 | None = None) -> dict[str, Any]:
    params = params or P3_V3_LOCKED_PARAMETRIC_REPAIR_R1
    rows = list(candidate_occurrences(params))
    validate_parity_manifest(rows)
    base = {row["name"]: row for row in baseline_occurrences()}
    candidate = {row["name"]: row for row in rows}
    diff = diff_occurrence_sets(base, candidate)
    protected_drift = sorted(
        name for name in diff["changed_occurrence_names"]
        if candidate[name]["classification"] == "protected_exact"
    )
    calibration = locked_step_roundtrip_calibration()
    adjustments = tuple(params.service_states.motor_adjustments_mm)
    source_rows, _, candidate_step = _candidate_evidence_for_adjustments(adjustments)
    source_vs_imported = _raw_representation_delta(source_rows, rows)
    symmetric_difference = protected_symmetric_difference_evidence(adjustments)
    if symmetric_difference["violation_occurrence_names"]:
        raise ValueError(
            "protected symmetric-difference gate failed for "
            + ", ".join(symmetric_difference["violation_occurrence_names"])
        )
    return {
        "namespace": "p3_v3_locked_parametric_repair_r1",
        "locked_generator_sha256": hash_file(LOCKED_BASELINE["generator"]),
        "locked_step_sha256": hash_file(LOCKED_BASELINE["step"]),
        "baseline_evidence": "immutable_locked_step_import",
        "candidate_evidence": "new_namespace_generator_exported_and_reimported_step",
        "comparison_method": "imported_locked_step_vs_imported_candidate_step",
        "candidate_temporary_step_evidence_path": str(candidate_step),
        "numeric_tolerance_calibration": calibration,
        "locked_source_vs_imported_step_evidence": calibration["observed"],
        "candidate_source_vs_imported_step_evidence": source_vs_imported,
        "protected_symmetric_difference_evidence": symmetric_difference,
        "occurrences": rows,
        "unknown_occurrence_names": diff["added_occurrence_names"],
        "unclassified_occurrence_names": [row["name"] for row in rows if not row.get("classification")],
        "protected_drift_occurrence_names": protected_drift,
    }
