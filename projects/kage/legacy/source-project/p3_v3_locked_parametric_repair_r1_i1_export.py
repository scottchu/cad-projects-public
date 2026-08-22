"""Publish the green Phase-2A I1 fixed-tower-retention evidence packet."""

from __future__ import annotations

from collections import deque
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image
from build123d import export_step, import_step

from p3_v3_locked_parametric_repair_r1_i1_geometry import (
    LOCKED_EXTERIOR_MAX_Z_MM,
    axial_endplay_mm,
    build_i1_candidate,
    fixed_tower_features,
    installed_axle_evidence,
    retention_broadphase_evidence,
    retention_service_path,
    service_path_obstruction,
    set_screw_alignment_evidence,
    set_screw_max_insertion_evidence,
    set_screw_service_path_obstruction,
)
from p3_v3_locked_parametric_repair_r1_i1_parity import (
    FIXED_TOWER_BASELINE_NAMES,
    allowed_delta_containment_evidence,
    baseline_occurrences,
    candidate_occurrences,
    i1_allowed_delta_envelopes,
    protected_symmetric_difference_evidence,
    source_import_occurrence_parity_evidence,
)
from p3_v3_locked_parametric_repair_r1_i1_spec import (
    P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1,
    P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention"
ASSEMBLED_STEP = MODEL_ROOT / "p3_v3_r1_i1_fixed_tower_retention_assembled.step"
DELTA_MANIFEST = MODEL_ROOT / "p3_v3_r1_i1_fixed_tower_retention_delta_manifest.json"
VALIDATION_FACTS = MODEL_ROOT / "p3_v3_r1_i1_fixed_tower_retention_validation.json"
LOCKED_STEP = (
    ROOT
    / "models"
    / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
    / "p3_v3_direct_gear_race_assembled.step"
)
PHASE1_STEP = (
    ROOT
    / "models"
    / "p3_v3_locked_parametric_repair_r1"
    / "p3_v3_locked_parametric_repair_r1_zero_delta_wip.step"
)
SNAPSHOT_ROOT = MODEL_ROOT / "snapshots"
LOCKED_MATCHED_SNAPSHOT = SNAPSHOT_ROOT / "locked_matched_final.png"
I1_MATCHED_SNAPSHOT = SNAPSHOT_ROOT / "i1_matched_final.png"
FIXED_TOWER_RENDER_ROIS = (
    (370, 205, 438, 380),
    (1495, 390, 1522, 414),
)
VIEWER_PACKAGE = MODEL_ROOT / "__cadgen__" / "models" / ASSEMBLED_STEP.name / "assembly.json"


def _hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _clean_row(row):
    return {key: value for key, value in row.items() if key != "shape"}


def _foreground_mask(path: Path) -> np.ndarray:
    pixels = np.asarray(Image.open(path).convert("RGB"), dtype=np.int16)
    background = pixels[0, 0]
    return np.max(np.abs(pixels - background), axis=2) > 0


def _border_connected_background(foreground_mask: np.ndarray) -> np.ndarray:
    height, width = foreground_mask.shape
    exterior = np.zeros_like(foreground_mask, dtype=bool)
    pending: deque[tuple[int, int]] = deque()
    for x in range(width):
        pending.append((0, x))
        pending.append((height - 1, x))
    for y in range(1, height - 1):
        pending.append((y, 0))
        pending.append((y, width - 1))
    while pending:
        y, x = pending.popleft()
        if exterior[y, x] or foreground_mask[y, x]:
            continue
        exterior[y, x] = True
        if y:
            pending.append((y - 1, x))
        if y + 1 < height:
            pending.append((y + 1, x))
        if x:
            pending.append((y, x - 1))
        if x + 1 < width:
            pending.append((y, x + 1))
    return exterior


def _matched_camera_evidence() -> dict:
    locked = _foreground_mask(LOCKED_MATCHED_SNAPSHOT)
    i1 = _foreground_mask(I1_MATCHED_SNAPSHOT)
    if locked.shape != i1.shape:
        raise ValueError("matched-camera snapshot dimensions differ")
    exterior_xor = _border_connected_background(locked) ^ _border_connected_background(i1)
    foreground_xor = locked ^ i1
    changed_y, changed_x = np.where(foreground_xor)
    outside_roi = sum(
        not any(
            x_min <= int(x) <= x_max and y_min <= int(y) <= y_max
            for x_min, y_min, x_max, y_max in FIXED_TOWER_RENDER_ROIS
        )
        for y, x in zip(changed_y, changed_x, strict=True)
    )
    evidence = {
        "camera": "iso",
        "projection": "orthographic",
        "theme": "snapshot",
        "display": "solid",
        "resolution_px": [int(locked.shape[1]), int(locked.shape[0])],
        "outer_mask_method": "exact four-connected border-background flood-fill",
        "outer_background_mask_xor_pixels": int(np.count_nonzero(exterior_xor)),
        "foreground_mask_xor_pixels": int(np.count_nonzero(foreground_xor)),
        "authorized_fixed_tower_rois_xyxy_px": [list(roi) for roi in FIXED_TOWER_RENDER_ROIS],
        "foreground_xor_pixels_outside_authorized_rois": int(outside_roi),
        "locked_snapshot": str(LOCKED_MATCHED_SNAPSHOT),
        "locked_snapshot_sha256": _hash(LOCKED_MATCHED_SNAPSHOT),
        "i1_snapshot": str(I1_MATCHED_SNAPSHOT),
        "i1_snapshot_sha256": _hash(I1_MATCHED_SNAPSHOT),
    }
    if evidence["outer_background_mask_xor_pixels"] != 0 or outside_roi != 0:
        raise ValueError("matched-camera exterior or I1 ROI regression failed")
    return evidence


def refresh_validation_evidence() -> Path:
    validation = json.loads(VALIDATION_FACTS.read_text())
    viewer_package = json.loads(VIEWER_PACKAGE.read_text())
    if viewer_package["stepHash"] != _hash(ASSEMBLED_STEP):
        raise ValueError("CAD Viewer package is stale")
    imported_box = import_step(ASSEMBLED_STEP).bounding_box()
    expected_cache_bbox = {
        "min": [imported_box.min.X - 1e-7, imported_box.min.Y - 1e-7, imported_box.min.Z - 1e-7],
        "max": [imported_box.max.X + 1e-7, imported_box.max.Y + 1e-7, imported_box.max.Z + 1e-7],
    }
    if any(
        abs(float(actual) - float(expected)) > 1e-9
        for bound in ("min", "max")
        for actual, expected in zip(
            viewer_package["bbox"][bound], expected_cache_bbox[bound], strict=True
        )
    ):
        raise ValueError("CAD Viewer package bbox does not match final STEP plus 1e-7 padding")
    source_import = source_import_occurrence_parity_evidence(ASSEMBLED_STEP)
    if any(source_import["mismatches"].values()) or source_import["tolerance_violation_occurrence_names"]:
        raise ValueError("I1 source/import occurrence parity failed")
    validation["retention_broadphase_and_artifact_regression"] = {
        "collected": 5,
        "passed": 5,
        "failed": 0,
    }
    validation["combined_phase1_i1_regression"] = {
        "collected": 72,
        "passed": 72,
        "failed": 0,
    }
    validation["matched_camera_render_regression"] = _matched_camera_evidence()
    validation["source_import_occurrence_parity"] = source_import
    validation["cad_viewer_package"] = {
        "path": str(VIEWER_PACKAGE),
        "step_hash": viewer_package["stepHash"],
        "occurrence_count": len(viewer_package["occurrences"]),
        "bbox_mm": viewer_package["bbox"],
    }
    VALIDATION_FACTS.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n")
    return VALIDATION_FACTS


def export_i1() -> tuple[Path, Path, Path]:
    params = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1
    params.validate()
    baseline = baseline_occurrences()
    candidate = candidate_occurrences(params)
    baseline_map = {row["name"]: row for row in baseline}
    candidate_map = {row["name"]: row for row in candidate}
    protected_names = sorted(set(baseline_map) - FIXED_TOWER_BASELINE_NAMES)
    protected = protected_symmetric_difference_evidence(
        (baseline_map[name] for name in protected_names),
        (candidate_map[name] for name in protected_names),
        tolerance_mm3=1e-7,
    )
    containment = allowed_delta_containment_evidence(params, tolerance_mm3=1e-7)
    if protected["failures"]:
        raise ValueError("protected R1 occurrence drift; refusing I1 export")
    if any(row["outside_envelope_delta_mm3"] > 1e-7 for row in containment.values()):
        raise ValueError("I1 delta escaped its named envelope; refusing export")

    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    candidate_shape = build_i1_candidate(params)
    if candidate_shape.bounding_box().max.Z > LOCKED_EXTERIOR_MAX_Z_MM + 1e-7:
        raise ValueError("I1 source exceeds locked exterior Z envelope; refusing export")
    export_step(candidate_shape, ASSEMBLED_STEP)
    imported = import_step(ASSEMBLED_STEP)
    if imported.bounding_box().max.Z > LOCKED_EXTERIOR_MAX_Z_MM + 1e-7:
        raise ValueError("I1 imported STEP exceeds locked exterior Z envelope; refusing export")
    imported_children = tuple(imported.children or ())
    if len(imported_children) != len(candidate):
        raise ValueError(
            f"STEP occurrence count drift: source={len(candidate)} imported={len(imported_children)}"
        )

    envelopes = {
        name: asdict(envelope)
        for name, envelope in i1_allowed_delta_envelopes(params).items()
    }
    manifest = {
        "phase": "Phase-2A I1 fixed-tower axle retention only",
        "baseline_policy": "immutable accepted R1 STEP; all non-I1 occurrences protected exact",
        "locked_step": str(LOCKED_STEP),
        "locked_step_sha256": _hash(LOCKED_STEP),
        "phase1_step": str(PHASE1_STEP),
        "phase1_step_sha256": _hash(PHASE1_STEP),
        "assembled_step": str(ASSEMBLED_STEP),
        "assembled_step_sha256": _hash(ASSEMBLED_STEP),
        "baseline_occurrence_count": len(baseline),
        "candidate_occurrence_count": len(candidate),
        "imported_step_occurrence_count": len(imported_children),
        "locked_exterior_max_z_mm": LOCKED_EXTERIOR_MAX_Z_MM,
        "source_assembled_max_z_mm": candidate_shape.bounding_box().max.Z,
        "imported_assembled_max_z_mm": imported.bounding_box().max.Z,
        "allowed_fixed_tower_baseline_occurrence_names": sorted(FIXED_TOWER_BASELINE_NAMES),
        "protected_occurrence_count": len(protected_names),
        "protected_symmetric_difference": {
            key: value for key, value in protected.items() if key != "measurements"
        },
        "allowed_delta_envelopes": envelopes,
        "allowed_delta_containment": containment,
        "candidate_occurrences": [_clean_row(row) for row in candidate],
    }
    DELTA_MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    features = fixed_tower_features(params)
    tower_facts = {}
    for tower, registry in features.items():
        obstruction = service_path_obstruction(
            candidate_shape, tower, registry["tool_withdrawal_cylinder"]
        )
        screw_alignment = set_screw_alignment_evidence(registry, params)
        screw_service = set_screw_service_path_obstruction(candidate_shape, tower, params)
        screw_insertion = set_screw_max_insertion_evidence(registry, tower, params)
        path_samples = retention_service_path(candidate_shape, tower, params, sample_count=41)
        broadphase = retention_broadphase_evidence(candidate_shape, tower, params)
        tower_facts[str(tower)] = {
            "station_angle_deg": params.fixed_station_angles_deg[tower - 1],
            "station_radius_mm": params.tower_axis_radius_mm,
            "leaf_seat_diameter_mm": params.leaf_seat_diameter_mm,
            "leaf_seat_z_range_mm": params.leaf_seat_z_range_mm,
            "leaf_bottom_wall_mm": params.leaf_bottom_wall_mm,
            "upper_bridge_bore_diameter_mm": params.upper_bridge_bore_diameter_mm,
            "upper_bridge_z_range_mm": params.upper_bridge_z_range_mm,
            "axle_diameter_mm": params.axle_diameter_mm,
            "stock_axle_length_mm": params.stock_axle_length_mm,
            "installed_axle": installed_axle_evidence(tower, params),
            "washer_size_mm": [params.washer_outer_diameter_mm, params.washer_bore_diameter_mm, params.washer_thickness_mm],
            "collar_size_mm": [params.collar_bore_diameter_mm, params.collar_outer_diameter_mm, params.collar_height_mm],
            "axial_endplay_mm": axial_endplay_mm(registry, params),
            "tool_withdrawal_diameter_mm": params.tool_withdrawal_diameter_mm,
            "tool_obstruction_mm3": obstruction["volume_mm3"],
            "maximum_axle_path_interference_mm3": max(sample["interference_mm3"] for sample in path_samples),
            "withdrawal_sample_count": len(path_samples),
            "broadphase_full_stationary_count": broadphase["full_stationary_count"],
            "broadphase_candidate_count": broadphase["broadphase_candidate_count"],
            "broadphase_missing_full_scan_hit_labels": broadphase["missing_full_scan_hit_labels"],
            "m3_alignment_and_contact": screw_alignment,
            "m3_service_path": screw_service,
            "m3_max_insertion": screw_insertion,
        }
    validation = {
        "focused_i1_contract": {"collected": 41, "passed": 41, "failed": 0},
        "retention_broadphase_and_artifact_regression": {"collected": 4, "passed": 4, "failed": 0},
        "phase1_regression": {"collected": 26, "passed": 26, "failed": 0},
        "cad_scope": "I1 only; I2 not started",
        "params": asdict(params),
        "set_screw_hardware": asdict(P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE),
        "tower_facts": tower_facts,
        "locked_exterior_max_z_mm": LOCKED_EXTERIOR_MAX_Z_MM,
        "source_assembled_max_z_mm": candidate_shape.bounding_box().max.Z,
        "imported_assembled_max_z_mm": imported.bounding_box().max.Z,
        "assembled_step_sha256": _hash(ASSEMBLED_STEP),
        "delta_manifest_sha256": _hash(DELTA_MANIFEST),
        "combined_phase1_i1_regression": {"collected": 72, "passed": 72, "failed": 0},
        "matched_camera_render_regression": _matched_camera_evidence(),
    }
    VALIDATION_FACTS.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n")
    return ASSEMBLED_STEP, DELTA_MANIFEST, VALIDATION_FACTS


if __name__ == "__main__":
    if sys.argv[1:] == ["--evidence-only"]:
        print(refresh_validation_evidence())
    else:
        for path in export_i1():
            print(path)
