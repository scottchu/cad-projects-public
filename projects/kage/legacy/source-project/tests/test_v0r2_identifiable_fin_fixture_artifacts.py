from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest
import trimesh


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "v0r2_identifiable_fin_fixture"
PRINT = MODEL / "print"
NAMES = ["fake_standard_quartz_body", "hour_carrier_hand", "minute_carrier_hand", "second_carrier_hand"]


def strict_mesh(mesh: trimesh.Trimesh):
    mesh = mesh.copy()
    mesh.merge_vertices(digits_vertex=6)
    mesh.remove_unreferenced_vertices()
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.is_volume
    assert len(mesh.split(only_watertight=False)) == 1
    edge_counts = Counter(
        tuple(sorted(edge))
        for face in mesh.faces
        for edge in ((face[0], face[1]), (face[1], face[2]), (face[2], face[0]))
    )
    assert all(count == 2 for count in edge_counts.values())


def test_all_four_stls_are_single_manifold_bed_contact_shells():
    for name in NAMES:
        path = PRINT / f"{name}.stl"
        assert path.exists() and path.stat().st_size > 0
        mesh = trimesh.load_mesh(path, process=False)
        assert isinstance(mesh, trimesh.Trimesh)
        strict_mesh(mesh)
        assert mesh.bounds[0][2] == pytest.approx(0.0, abs=1e-5)


def test_four_object_3mf_is_namespace_clean_named_and_manifold():
    path = PRINT / "v0r2_four_part_identifiable_fin_test.3mf"
    assert path.exists()
    with ZipFile(path) as package:
        assert package.testzip() is None
        assert set(package.namelist()) == {"[Content_Types].xml", "_rels/.rels", "3D/3dmodel.model"}
        raw = package.read("3D/3dmodel.model")
    assert b"ns0:" not in raw
    root = ET.fromstring(raw)
    namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    objects = root.findall("m:resources/m:object", namespace)
    items = root.findall("m:build/m:item", namespace)
    assert [obj.attrib["name"] for obj in objects] == NAMES
    assert len(objects) == len(items) == 4
    for obj in objects:
        vertices = [
            tuple(float(vertex.attrib[key]) for key in ("x", "y", "z"))
            for vertex in obj.findall("m:mesh/m:vertices/m:vertex", namespace)
        ]
        faces = [
            tuple(int(face.attrib[key]) for key in ("v1", "v2", "v3"))
            for face in obj.findall("m:mesh/m:triangles/m:triangle", namespace)
        ]
        strict_mesh(trimesh.Trimesh(vertices=vertices, faces=faces, process=False))


def test_manifest_paths_hashes_counts_and_frozen_identity_spec_are_live():
    manifest = json.loads((PRINT / "v0r2_manifest.json").read_text())
    assert manifest["schema_version"] == 1
    assert manifest["review_status"] == "accepted_for_physical_test"
    assert manifest["independent_review"]["verdict"] == "ACCEPT"
    assert "collinear opaque shadows" in manifest["independent_review"]["caveat"]
    assert manifest["implementation_may_self_approve"] is False
    assert manifest["printable_part_count"] == 4 and manifest["printable_parts"] == NAMES
    assert manifest["three_mf"]["object_count"] == 4 and manifest["three_mf"]["object_names"] == NAMES
    assert manifest["frozen_spec"]["source_z"] == 40.0
    identity = manifest["frozen_spec"]["fin_identity"]
    assert identity["hour"]["physical_profile_mm"] == {"stem_width": 4.8, "crown_height": 0.8, "crown_width": 3.2}
    assert identity["minute"]["physical_profile_mm"] == {"stem_width": 3.2, "crown_height": 0.8, "crown_width": 1.6}
    assert identity["second"]["physical_profile_mm"] == {"stem_width": 1.6, "crown_height": 0.6, "crown_width": 0.4}
    records = [manifest["primary_step"]["assembled"], manifest["primary_step"]["exploded"], manifest["three_mf"]]
    for name in NAMES:
        records.extend((manifest["parts"][name]["step"], manifest["parts"][name]["stl"]))
    for record in records:
        artifact = ROOT / record["path"]
        assert artifact.exists()
        assert sha256(artifact.read_bytes()).hexdigest() == record["sha256"]
    for record in manifest["snapshots"]:
        artifact = ROOT / record["path"]
        assert artifact.exists()
        assert sha256(artifact.read_bytes()).hexdigest() == record["sha256"]
