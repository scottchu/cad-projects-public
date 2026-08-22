from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest
import trimesh


ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/"models"/"v0_upright_fin_fixture"
PRINT=MODEL/"print"
NAMES=["fake_quartz_mask_body","hour_carrier_hand","minute_carrier_hand","second_carrier_hand"]


def strict_mesh(mesh: trimesh.Trimesh):
    mesh=mesh.copy()
    mesh.merge_vertices(digits_vertex=6)
    mesh.remove_unreferenced_vertices()
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.is_volume
    assert len(mesh.split(only_watertight=False)) == 1
    assert all(count == 2 for count in __import__("collections").Counter(tuple(sorted(edge)) for face in mesh.faces for edge in ((face[0],face[1]),(face[1],face[2]),(face[2],face[0]))).values())


def test_all_stls_are_one_manifold_shell_and_support_free():
    for name in NAMES:
        path=PRINT/f"{name}.stl"; assert path.exists() and path.stat().st_size>0
        mesh=trimesh.load_mesh(path,process=False); assert isinstance(mesh,trimesh.Trimesh)
        strict_mesh(mesh)
        assert mesh.bounds[0][2] == pytest.approx(0,abs=1e-5)


def test_four_object_3mf_is_literal_namespace_clean_and_manifold():
    path=PRINT/"v0_four_part_manual_optics.3mf"; assert path.exists()
    with ZipFile(path) as package:
        assert package.testzip() is None
        assert set(package.namelist()) == {"[Content_Types].xml","_rels/.rels","3D/3dmodel.model"}
        raw=package.read("3D/3dmodel.model")
    assert b"ns0:" not in raw
    root=ET.fromstring(raw); ns={"m":"http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    objects=root.findall("m:resources/m:object",ns); items=root.findall("m:build/m:item",ns)
    assert [obj.attrib["name"] for obj in objects] == NAMES
    assert len(objects)==len(items)==4
    for obj in objects:
        vertices=[tuple(float(v.attrib[k]) for k in ("x","y","z")) for v in obj.findall("m:mesh/m:vertices/m:vertex",ns)]
        faces=[tuple(int(v.attrib[k]) for k in ("v1","v2","v3")) for v in obj.findall("m:mesh/m:triangles/m:triangle",ns)]
        strict_mesh(trimesh.Trimesh(vertices=vertices,faces=faces,process=False))


def test_orca_loads_bundle_when_available(tmp_path):
    orca=Path("/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer")
    if not orca.exists(): pytest.skip("OrcaSlicer unavailable")
    result=subprocess.run([str(orca),"--datadir",str(tmp_path),"--info",str(PRINT/"v0_four_part_manual_optics.3mf")],capture_output=True,text=True,timeout=90)
    combined=(result.stdout+result.stderr).lower()
    assert result.returncode==0,combined
    assert "loading of a model file failed" not in combined and "run found error" not in combined


def test_manifest_hashes_structure_and_physical_caveat_are_live():
    path=PRINT/"v0_manifest.json"; manifest=json.loads(path.read_text())
    assert manifest["schema_version"]==1 and manifest["review_status"]=="pending_independent_review"
    assert manifest["implementation_may_self_approve"] is False
    assert manifest["printable_part_count"]==4 and manifest["printable_parts"]==NAMES
    assert manifest["three_mf"]["object_count"]==4
    assert manifest["physical_test_only"]==["force","friction","wear","runout","real shadow quality"]
    assert len(manifest["snapshots"]) >= 5
    records=[manifest["primary_step"]["assembled"],manifest["primary_step"]["exploded"],manifest["three_mf"]]
    for name in NAMES: records += [manifest["parts"][name]["step"],manifest["parts"][name]["stl"]]
    for record in records:
        artifact=ROOT/record["path"]
        assert artifact.exists() and sha256(artifact.read_bytes()).hexdigest()==record["sha256"]
    for record in manifest["snapshots"]:
        artifact=ROOT/record["path"]
        assert artifact.exists() and sha256(artifact.read_bytes()).hexdigest()==record["sha256"]
