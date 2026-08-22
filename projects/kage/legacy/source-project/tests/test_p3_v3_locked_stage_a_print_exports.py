"""Focused contracts for zero-delta locked Stage A print exports."""

from __future__ import annotations

import json

import pytest
from build123d import import_step

import p3_v3_locked_stage_a_print_exports as export


CORE_PACKS = ("base_joinery", "roller_tower", "motor_station")
ALL_PACKS = (*CORE_PACKS, "ring_seam_review_only")


def _bbox_gap(a, b) -> float | None:
    aa, bb = a.bounding_box(), b.bounding_box()
    gaps = (
        bb.min.X - aa.max.X, aa.min.X - bb.max.X,
        bb.min.Y - aa.max.Y, aa.min.Y - bb.max.Y,
        bb.min.Z - aa.max.Z, aa.min.Z - bb.max.Z,
    )
    positive = [value for value in gaps if value >= 0.0]
    return max(positive) if positive else None


def test_authority_and_selected_frozen_occurrences_have_exact_manifest_fingerprints():
    manifest, children = export.authority()
    assert export._sha(export.LOCKED_STEP) == export.LOCKED_STEP_SHA256
    for pack in ALL_PACKS:
        for index in export.PACKS[pack]["indices"]:
            shape = children[index]
            row = manifest["occurrences"][index]
            assert shape.label == row["label"]
            assert shape.is_valid and len(shape.solids()) == 1 and shape.volume > 0.0
            assert export.brep_fingerprint(shape)["brep_sha256"] == row["brep_fingerprint"]["brep_sha256"]


@pytest.mark.parametrize("pack", ALL_PACKS)
def test_named_step_objects_roundtrip_with_exact_frozen_geometry(pack):
    parity = json.loads(export.PARITY_JSON.read_text())["occurrences"]
    _, frozen_children = export.authority()
    step_path, _ = export.artifact_paths(pack)
    objects = tuple(import_step(step_path).children)
    indices = export.PACKS[pack]["indices"]
    assert len(objects) == len(indices)
    for obj, index in zip(objects, indices, strict=True):
        frozen = parity[index]
        facts = export.brep_fingerprint(obj)
        assert obj.label == frozen["label"]
        assert obj.is_valid and facts["topology"]["solids"] == 1
        assert facts["aabb_mm"] == pytest.approx(frozen["aabb_mm"], abs=1e-7)
        assert facts["volume_mm3"] == pytest.approx(frozen["volume_mm3"], abs=1e-6)
        assert facts["area_mm2"] == pytest.approx(frozen["area_mm2"], abs=1e-6)
        assert facts["topology"] == frozen["topology"]
        # Most occurrences retain the canonical parity digest through this
        # second STEP serialization.  OCC may perturb analytic center samples
        # on serializer round-trip; in that case prove zero solid difference.
        if facts["brep_sha256"] != frozen["brep_fingerprint"]["brep_sha256"]:
            source = frozen_children[index]
            left = source.cut(obj)
            right = obj.cut(source)
            assert sum(s.volume for s in left.solids()) <= 1e-7 if left else True
            assert sum(s.volume for s in right.solids()) <= 1e-7 if right else True


@pytest.mark.parametrize("pack", CORE_PACKS)
def test_translation_only_3mf_layout_is_named_in_volume_and_disjoint(pack):
    rows = export.layout_rows(pack)
    _, mf_path = export.artifact_paths(pack)
    mesh = export.read_3mf_objects(mf_path)
    assert [row["name"] for row in mesh] == [row["frozen_label"] for row in rows]
    assert all(row["vertices"] and row["triangles"] for row in mesh)
    for row in rows:
        x0, y0, z0, x1, y1, z1 = row["print_aabb_mm"]
        assert export.BED_MARGIN_MM - 1e-7 <= x0 < x1 <= export.BUILD_VOLUME_MM[0] - export.BED_MARGIN_MM + 1e-7
        assert export.BED_MARGIN_MM - 1e-7 <= y0 < y1 <= export.BUILD_VOLUME_MM[1] - export.BED_MARGIN_MM + 1e-7
        assert z0 == pytest.approx(0.0, abs=1e-7)
        assert z1 <= export.BUILD_VOLUME_MM[2] + 1e-7
        assert row["frozen_dimensions_mm"] == pytest.approx(export._dimensions(row["shape"]), abs=1e-7)
    for index, left in enumerate(rows):
        for right in rows[index + 1:]:
            lower_bound = _bbox_gap(left["shape"], right["shape"])
            distance = lower_bound if lower_bound is not None else left["shape"].distance_to(right["shape"])
            assert distance >= export.MIN_OBJECT_GAP_MM - 1e-6


def test_base_pair_is_the_minimum_adjacent_flat_seam_in_locked_assembly():
    rows = export.source_rows("base_joinery")
    q1, q2 = (row["shape"] for row in rows)
    a, b = q1.bounding_box(), q2.bounding_box()
    assert a.min.X == pytest.approx(b.max.X, abs=1e-7)
    assert (a.min.Z, a.max.Z) == pytest.approx((b.min.Z, b.max.Z), abs=1e-7)
    assert q1.distance_to(q2) == pytest.approx(0.0, abs=1e-7)
    hit = q1.intersect(q2)
    assert sum(s.volume for s in hit.solids()) <= 1e-7 if hit else True


def test_manifest_maps_every_object_and_warns_dowel_seam_review_only():
    path = export.MODEL_ROOT / "stage_a_print_export_manifest.json"
    manifest = json.loads(path.read_text())
    assert manifest["authority"]["locked_step_sha256"] == export.LOCKED_STEP_SHA256
    assert [pack["name"] for pack in manifest["packs"]] == list(ALL_PACKS)
    assert all(
        obj["frozen_generator_function"] and obj["frozen_label"] and obj["frozen_brep_sha256"]
        for pack in manifest["packs"] for obj in pack["objects"]
    )
    assert manifest["deferred_review_only_pack"] is None
    seam = manifest["packs"][-1]
    assert seam["status"] == "REVIEW_ONLY_DO_NOT_PRINT"
    assert "3 mm alignment dowel" in seam["warning"]
    assert "screw-only redesign" in seam["warning"]
