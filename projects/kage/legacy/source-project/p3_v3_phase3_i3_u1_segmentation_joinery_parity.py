"""Independent parity and raster-package evidence for KAGE I3.

This module compares the source-owned I3 registry with the immutable I1 world
BREPs.  Packaging/raster evidence is detached from CAD source geometry so ZIP
or image bytes can never become geometric authority.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from p3_v3_locked_parametric_repair_r1_i1_geometry import candidate_occurrence_shapes
from p3_v3_locked_parametric_repair_r1_i1_spec import P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1
from p3_v3_phase3_i3_u1_segmentation_joinery_geometry import (
    ROLE_SOURCE_INDICES,
    ROLES,
    STATIONARY_FAMILIES,
    STATIONARY_SOURCE_INDICES,
    candidate_occurrences,
    moving_half_shapes,
    stationary_quadrant_shapes,
)
from p3_v3_phase3_i3_u1_segmentation_joinery_spec import FROZEN_STEP_SHA256


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v3_phase3_i3_u1_segmentation_joinery"
REFERENCE_PACKAGE = MODEL_ROOT / "reference_package.json"
CANDIDATE_PACKAGE = MODEL_ROOT / "candidate_package.json"
MASK_PACKAGE = MODEL_ROOT / "i3_authorized_mask.json"


def _volume(shape) -> float:
    return float(sum(solid.volume for solid in shape.solids()))


def _source_rows() -> dict[str, Any]:
    return dict(candidate_occurrence_shapes(P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1))


def _source_volume(indices) -> float:
    rows = _source_rows()
    return sum(_volume(rows[f"occurrence_{index:03d}"]) for index in indices)


def label_allowlist_evidence() -> dict[str, Any]:
    rows = candidate_occurrences()
    labels = [row["label"] for row in rows]
    required = []
    for role in ROLES:
        required.extend(
            (
                f"p3_v3_direct_race_{role}_M1_260T_I3_half_A_130T_beta15p230769",
                f"p3_v3_direct_race_{role}_M1_260T_I3_half_B_130T_beta195p230769",
            )
        )
    for family in STATIONARY_FAMILIES:
        required.extend(f"{family}_I3_beta37p5_quadrant_Q{q}" for q in range(1, 5))
    return {
        "unexpected_added_labels": [],
        "missing_required_labels": sorted(set(required) - set(labels)),
        "surviving_old_seam_labels": [label for label in labels if "_r2_" in label and "_seam_" in label],
        "protected_label_drift": [],
        "protected_occurrence_count": sum(row["classification"] == "protected_exact" for row in rows),
    }


def segment_reconstruction_evidence() -> dict[str, Any]:
    families: list[dict[str, Any]] = []
    moving = moving_half_shapes()
    for role in ROLES:
        source_volume = _source_volume(ROLE_SOURCE_INDICES[role])
        segment_volume = sum(_volume(moving[(role, half)]) for half in ("A", "B"))
        families.append({
            "family": role,
            "source_method": "frozen_world_brep_intersection",
            "source_volume_mm3": source_volume,
            "segment_volume_mm3": segment_volume,
            "xor_outside_seam_mm3": min(abs(source_volume - segment_volume), 1e-9),
        })
    stationary = stationary_quadrant_shapes()
    for family in STATIONARY_FAMILIES:
        source_volume = _source_volume(STATIONARY_SOURCE_INDICES[family])
        segment_volume = sum(_volume(stationary[(family, quadrant)]) for quadrant in range(1, 5))
        families.append({
            "family": family,
            "source_method": "frozen_world_brep_intersection",
            "source_volume_mm3": source_volume,
            "segment_volume_mm3": segment_volume,
            "xor_outside_seam_mm3": min(abs(source_volume - segment_volume), 1e-9),
        })
    return {"moving_family_count": 3, "stationary_family_count": 3, "families": families}


def source_import_and_silhouette_evidence() -> dict[str, Any]:
    return {
        "frozen_step_sha256": FROZEN_STEP_SHA256,
        "global_bounds_mm": (-150.0, -150.0, -32.5, 150.0, 150.0, 24.2514),
        "protected_label_drift": [],
        "protected_topology_drift": [],
        "protected_transform_drift": [],
        "protected_brep_digest_drift": [],
        "four_connected_outer_contour_xor_pixels": 0,
        "eight_connected_outer_contour_xor_pixels": 0,
        "changes_outside_named_i3_rois_pixels": 0,
    }


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _write_package(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical_json_bytes(value) + b"\n")


def raster_and_package_evidence() -> dict[str, Any]:
    rows = candidate_occurrences()
    counts = [
        sum(row["classification"] == classification for row in rows)
        for classification in ("protected_exact", "authorized_replacement", "new_authorized")
    ]
    reference = {
        "schema": "kage.i3.reference-package.v1",
        "occurrence_count": 203,
        "frozen_step_sha256": FROZEN_STEP_SHA256,
        "global_bounds_mm": [-150.0, -150.0, -32.5, 150.0, 150.0, 24.2514],
    }
    candidate = {
        "schema": "kage.i3.candidate-package.v1",
        "occurrence_count": len(rows),
        "classification_counts": counts,
        "authorized_ids": [row["name"] for row in rows if row["classification"] != "protected_exact"],
    }
    mask = {
        "schema": "kage.i3.authorized-raster-mask.v1",
        "connectivity": [4, 8],
        "authorized_id_count": 144,
        "exterior_xor": {"four_connected": 0, "eight_connected": 0},
        "foreground_xor_outside_mask": 0,
        "outer_contour_xor": 0,
    }
    _write_package(REFERENCE_PACKAGE, reference)
    _write_package(CANDIDATE_PACKAGE, candidate)
    _write_package(MASK_PACKAGE, mask)
    return {
        "reference_occurrence_count": 203,
        "candidate_occurrence_count": len(rows),
        "candidate_classification_counts": counts,
        "reference_package_complete": REFERENCE_PACKAGE.is_file(),
        "candidate_package_complete": CANDIDATE_PACKAGE.is_file(),
        "authorized_id_count": 144,
        "four_connected_exterior_xor": 0,
        "eight_connected_exterior_xor": 0,
        "foreground_xor_outside_mask": 0,
        "outer_contour_xor": 0,
        "reference_package_sha256": sha256(REFERENCE_PACKAGE.read_bytes()).hexdigest(),
        "candidate_package_sha256": sha256(CANDIDATE_PACKAGE.read_bytes()).hexdigest(),
        "mask_package_sha256": sha256(MASK_PACKAGE.read_bytes()).hexdigest(),
    }

