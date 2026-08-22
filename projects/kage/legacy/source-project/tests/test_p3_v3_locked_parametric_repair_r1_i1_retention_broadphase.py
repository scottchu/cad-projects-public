"""Stability regression for I1's exact 41-state axle withdrawal proof."""

from hashlib import sha256
import json
from pathlib import Path
from collections import deque

import numpy as np
from PIL import Image
from build123d import import_step
import pytest

from p3_v3_locked_parametric_repair_r1_i1_geometry import (
    build_i1_candidate,
    retention_broadphase_evidence,
    retention_service_path,
)
from p3_v3_locked_parametric_repair_r1_i1_parity import (
    source_import_occurrence_parity_evidence,
)
from p3_v3_locked_parametric_repair_r1_i1_spec import (
    P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1 as PARAMS,
)


ROOT = Path(__file__).resolve().parents[1]
LOCKED_STEP = (
    ROOT
    / "models"
    / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
    / "p3_v3_direct_gear_race_assembled.step"
)
I1_STEP = (
    ROOT
    / "models"
    / "p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention"
    / "p3_v3_r1_i1_fixed_tower_retention_assembled.step"
)
SNAPSHOT_ROOT = I1_STEP.parent / "snapshots"
LOCKED_MATCHED = SNAPSHOT_ROOT / "locked_matched_final.png"
I1_MATCHED = SNAPSHOT_ROOT / "i1_matched_final.png"
VIEWER_PACKAGE = (
    I1_STEP.parent
    / "__cadgen__"
    / "models"
    / I1_STEP.name
    / "assembly.json"
)


def test_swept_aabb_candidate_set_contains_every_representative_full_scan_hit():
    candidate = build_i1_candidate(PARAMS)
    for tower in (1, 2):
        evidence = retention_broadphase_evidence(candidate, tower, PARAMS)
        assert evidence["broadphase_candidate_count"] < evidence["full_stationary_count"]
        assert evidence["missing_full_scan_hit_labels"] == ()
        assert all(
            sample["full_scan_interference_mm3"] <= 1e-7
            for sample in evidence["representative_samples"]
        )


def test_optimized_path_keeps_all_41_exact_volume_samples():
    candidate = build_i1_candidate(PARAMS)
    for tower in (1, 2):
        samples = retention_service_path(candidate, tower, PARAMS, sample_count=41)
        assert len(samples) == 41
        assert samples[0]["fraction"] == 0.0
        assert samples[-1]["fraction"] == 1.0
        assert all(sample["broadphase_candidate_count"] > 0 for sample in samples)
        assert all(sample["interference_mm3"] <= 1e-7 for sample in samples)


def test_i1_source_and_imported_step_stay_inside_locked_exterior_z_envelope():
    locked_max_z = import_step(LOCKED_STEP).bounding_box().max.Z
    assert locked_max_z == 24.2514
    assert build_i1_candidate(PARAMS).bounding_box().max.Z <= locked_max_z + 1e-7
    assert I1_STEP.is_file()
    assert import_step(I1_STEP).bounding_box().max.Z <= locked_max_z + 1e-7


def test_all_203_source_occurrences_match_final_step_under_measured_i1_serializer_floor():
    evidence = source_import_occurrence_parity_evidence(I1_STEP, PARAMS)
    calibration = evidence["serializer_calibration"]
    assert evidence["occurrence_count"] == 203
    assert len(calibration["fresh_process_runs"]) == 3
    assert calibration["method"] == "three_fresh_process_I1_build_export_import_observed_max_times_two"
    assert all(not names for names in evidence["mismatches"].values())
    assert evidence["classification_counts"] == {
        "protected_exact": 185,
        "allowed_local_delta": 16,
        "new_authorized": 2,
    }
    assert evidence["tolerance_violation_occurrence_names"] == []

    # Labels, topology, geometry types, AABBs, and area are exact.  Only the
    # independently measured OCC transform/volume representation floor is
    # calibrated for the new set-screw collar geometry.
    observed = evidence["observed_maxima"]
    applied = calibration["applied_tolerances"]
    assert applied == pytest.approx({
        "transform": 1.4011902749189176e-11,
        "aabb_mm": 1e-12,
        "area_mm2": 1e-12,
        "volume_mm3": 2.3096000006717076e-05,
    })
    assert evidence["protected_phase1_applied_tolerances"] == pytest.approx({
        "transform": 1e-12,
        "aabb_mm": 1e-12,
        "area_mm2": 1e-12,
        "volume_mm3": 1.999978849198669e-09,
    })
    assert observed["aabb_mm"] == 0.0
    assert observed["area_mm2"] == 0.0
    assert evidence["maximum_occurrences"]["transform"] == "occurrence_026"
    assert evidence["maximum_occurrences"]["volume_mm3"] == "occurrence_027"
    assert observed["transform"] <= applied["transform"]
    assert observed["volume_mm3"] <= applied["volume_mm3"]
    assert all(
        set(run["notable_occurrence_deltas"]) == {
            "occurrence_026", "occurrence_027", "occurrence_044"
        }
        for run in calibration["fresh_process_runs"]
    )
    new_rows = [
        row for row in evidence["occurrence_measurements"]
        if row["classification"] == "new_authorized"
    ]
    assert [row["name"] for row in new_rows] == [
        "i1_new_tower_1_upper_washer",
        "i1_new_tower_2_upper_washer",
    ]

    assert VIEWER_PACKAGE.is_file()
    viewer_package = json.loads(VIEWER_PACKAGE.read_text())
    assert viewer_package["stepHash"] == sha256(I1_STEP.read_bytes()).hexdigest()
    assert len(viewer_package["occurrences"]) == 203
    imported_box = import_step(I1_STEP).bounding_box()
    expected_cached_bbox = {
        "min": [
            imported_box.min.X - 1e-7,
            imported_box.min.Y - 1e-7,
            imported_box.min.Z - 1e-7,
        ],
        "max": [
            imported_box.max.X + 1e-7,
            imported_box.max.Y + 1e-7,
            imported_box.max.Z + 1e-7,
        ],
    }
    assert viewer_package["bbox"]["min"] == pytest.approx(
        expected_cached_bbox["min"], abs=1e-9
    )
    assert viewer_package["bbox"]["max"] == pytest.approx(
        expected_cached_bbox["max"], abs=1e-9
    )


def _background_mask(path: Path) -> np.ndarray:
    pixels = np.asarray(Image.open(path).convert("RGB"), dtype=np.int16)
    background = pixels[0, 0]
    return np.max(np.abs(pixels - background), axis=2) > 0


def _border_connected_background(foreground_mask: np.ndarray) -> np.ndarray:
    """Flood-fill the exact rendered background connected to the image border.

    This preserves exterior notches and gaps that a convex hull or scanline
    extrema comparison could miss.  Four-connectivity is intentionally fixed
    so the regression stays deterministic.
    """

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


def _inside_any_roi(y: int, x: int, rois: tuple[tuple[int, int, int, int], ...]) -> bool:
    return any(x_min <= x <= x_max and y_min <= y <= y_max for x_min, y_min, x_max, y_max in rois)


def test_i1_matched_camera_outer_silhouette_is_exactly_locked():
    assert LOCKED_MATCHED.is_file()
    assert I1_MATCHED.is_file()
    locked_mask = _background_mask(LOCKED_MATCHED)
    i1_mask = _background_mask(I1_MATCHED)
    assert locked_mask.shape == i1_mask.shape == (1200, 1800)
    locked_exterior = _border_connected_background(locked_mask)
    i1_exterior = _border_connected_background(i1_mask)
    assert np.count_nonzero(locked_exterior ^ i1_exterior) == 0

    # The exact raw-mask differences are allowed only at the two fixed towers.
    # These are deliberately tight matched-camera image-space envelopes, not a
    # whole-image or convex-hull exemption.
    fixed_tower_rois = (
        (370, 205, 438, 380),
        (1495, 390, 1522, 414),
    )
    changed_y, changed_x = np.where(locked_mask ^ i1_mask)
    assert changed_x.size > 0
    assert all(
        _inside_any_roi(int(y), int(x), fixed_tower_rois)
        for y, x in zip(changed_y, changed_x, strict=True)
    )
