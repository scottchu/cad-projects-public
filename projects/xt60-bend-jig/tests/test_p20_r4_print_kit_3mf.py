from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from zipfile import ZipFile

import lib3mf
import pytest
from build123d import import_step

import xt60_bend_jig.p20_r4_blocked_test_print_3mf as p20
import xt60_bend_jig.p20_r4_custom_profile_full_cad as parent


ROOT = Path(__file__).parents[1]
CAD = ROOT / "cad/p20_r4_custom_profile_full_cad"
STEP = CAD / "p20_r4_print_kit.step"
THREEMF = CAD / "p20_r4_print_kit.3mf"
PROVENANCE = CAD / "p20-r4-3mf-provenance.json"


def _bounds(shape) -> tuple[float, float, float, float, float, float]:
    box = shape.bounding_box()
    return (
        float(box.min.X),
        float(box.min.Y),
        float(box.min.Z),
        float(box.max.X),
        float(box.max.Y),
        float(box.max.Z),
    )


def test_source_print_kit_is_exact_13_unchanged_separate_solids_on_bed() -> None:
    assert parent.source_revision_sha256() == p20.PARENT_SOURCE_SHA256
    parts = list(p20.build_print_parts())
    sources = [row[0] for row in p20.build_print_source_parts()]
    assert tuple(part.label for part in parts) == p20.PRINT_OBJECT_LABELS
    assert len(parts) == len(set(part.label for part in parts)) == 13
    assert all(len(part.solids()) == 1 and part.is_valid and part.volume > 0 for part in parts)
    for part, source in zip(parts, sources, strict=True):
        assert float(part.volume) == pytest.approx(float(source.volume), abs=1.0e-6)
        assert _bounds(part)[2] == pytest.approx(0.0, abs=1.0e-6)
    for first, second in combinations(parts, 2):
        a, b = _bounds(first), _bounds(second)
        overlap_x = min(a[3], b[3]) - max(a[0], b[0])
        overlap_y = min(a[4], b[4]) - max(a[1], b[1])
        assert not (overlap_x > 1.0e-7 and overlap_y > 1.0e-7)
    labels = " ".join(part.label.lower() for part in parts)
    assert "xt60" not in labels and "workpiece" not in labels and "_rod_" not in labels


def test_written_step_preserves_13_labels_and_source_volumes() -> None:
    written = import_step(STEP)
    assert tuple(child.label for child in written.children) == p20.PRINT_OBJECT_LABELS
    assert len(written.children) == 13
    for source, child in zip(p20.build_print_parts(), written.children, strict=True):
        assert child.is_valid and len(child.solids()) == 1 and child.volume > 0
        assert float(child.volume) == pytest.approx(float(source.volume), abs=1.0e-6)
        assert _bounds(child)[2] == pytest.approx(0.0, abs=1.0e-6)


def test_model_only_3mf_roundtrip_and_provenance() -> None:
    payload = json.loads(PROVENANCE.read_text())
    artifact = payload["artifact"]
    assert artifact["objectCount"] == artifact["meshObjectCount"] == artifact["buildItemCount"] == 13
    assert tuple(artifact["labels"]) == p20.PRINT_OBJECT_LABELS
    assert artifact["modelOnly"] and artifact["lib3mfRoundTripValid"]
    assert artifact["allMeshesManifoldAndOriented"] and artifact["allBuildTransformsIdentity"]
    assert artifact["layout"]["pairwiseBoundingBoxOverlapCount"] == 0
    assert artifact["layout"]["allMinimumZOnBed"]
    assert not payload["geometryChangedForThreeMF"]
    assert not payload["manufacturingAccepted"]
    assert not payload["printingInitiated"] and not payload["sliced"] and not payload["uploaded"]

    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    model.QueryReader("3mf").ReadFromFile(str(THREEMF))
    assert model.GetUnit() == lib3mf.ModelUnit.MilliMeter
    meshes = model.GetMeshObjects()
    labels = []
    while meshes.MoveNext():
        mesh = meshes.GetCurrentMeshObject()
        labels.append(mesh.GetName())
        assert mesh.GetVertexCount() > 0 and mesh.GetTriangleCount() > 0
        assert mesh.IsValid() and mesh.IsManifoldAndOriented()
    assert tuple(labels) == p20.PRINT_OBJECT_LABELS
    assert model.GetBuildItems().Count() == 13

    with ZipFile(THREEMF) as archive:
        names = archive.namelist()
    lowered = " ".join(names).lower()
    assert "gcode" not in lowered and "slice_info" not in lowered and "metadata/plate" not in lowered
