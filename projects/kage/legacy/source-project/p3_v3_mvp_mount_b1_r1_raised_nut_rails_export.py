"""Artifact export and source-parity checks for the seven-object mount MVP."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile

from build123d import export_step, import_step
import lib3mf
import trimesh

import p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry as geometry
from p3_v3_mvp_mount_b1_r1_raised_nut_rails_spec import MODEL_ROOT, NAMESPACE, SPEC


ASSEMBLED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembled_test_rig.step"
EXPLODED_STEP = MODEL_ROOT / f"{NAMESPACE}_service_exploded.step"
MODEL_ONLY_3MF = MODEL_ROOT / f"{NAMESPACE}_seven_printed_objects_model_only.3mf"
README = MODEL_ROOT / "README.md"


def individual_step_paths() -> tuple[Path, ...]:
    names = ("quadrant_Q1", "quadrant_Q2", "quadrant_Q3", "quadrant_Q4", "reusable_motor_sled", "reusable_fixed_riser", "spine_riser")
    return tuple(MODEL_ROOT / f"{NAMESPACE}_{name}.step" for name in names)


def required_artifact_paths() -> tuple[Path, ...]:
    return (ASSEMBLED_STEP, EXPLODED_STEP, *individual_step_paths(), MODEL_ONLY_3MF, README)


def _mesh_geometry(shape):
    vertices, triangles = shape.tessellate(SPEC.mesh_linear_deflection_mm, SPEC.mesh_angular_deflection_rad)
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, t)) for t in triangles], process=True, validate=True,
    )
    if not mesh.is_watertight or not mesh.is_winding_consistent or not mesh.is_volume:
        raise RuntimeError("printable mesh is not a closed oriented volume")
    positions = []
    for vertex in mesh.vertices:
        p = lib3mf.Position(); p.Coordinates[:] = tuple(float(v) for v in vertex); positions.append(p)
    indices = []
    for a, b, c in mesh.faces:
        t = lib3mf.Triangle(); t.Indices[:] = (int(a), int(b), int(c)); indices.append(t)
    return positions, indices


def write_model_only_3mf(path: Path = MODEL_ONLY_3MF) -> dict[str, object]:
    rows = geometry.printable_occurrences()
    if len(rows) != 7:
        raise RuntimeError(f"expected exactly seven printable objects, got {len(rows)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper(); model = wrapper.CreateModel(); objects = []
    for row in rows:
        obj = model.AddMeshObject(); obj.SetName(str(row["label"])); obj.SetUUID(str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{row['label']}")))
        vertices, triangles = _mesh_geometry(row["shape"]); obj.SetGeometry(vertices, triangles)
        model.AddBuildItem(obj, wrapper.GetIdentityTransform())
        objects.append({"name": row["label"], "vertices": len(vertices), "triangles": len(triangles)})
    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=path.parent) as temp:
        candidate = Path(temp) / path.name; model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None: raise RuntimeError("3MF ZIP CRC failed")
            forbidden = [name for name in archive.namelist() if any(token in name.lower() for token in ("project_settings", "model_settings", "slice_info"))]
        if forbidden: raise RuntimeError(f"model-only 3MF contains slicer settings: {forbidden}")
        path.write_bytes(candidate.read_bytes())
    return {"path": str(path), "sha256": sha256(path.read_bytes()).hexdigest(), "object_count": len(objects), "objects": tuple(objects)}


def fresh_lib3mf_import_evidence(path: Path = MODEL_ONLY_3MF) -> dict[str, object]:
    script = r'''import json,lib3mf,sys
w=lib3mf.Wrapper();m=w.CreateModel();m.QueryReader("3mf").ReadFromFile(sys.argv[1]);o=[];it=m.GetMeshObjects()
while it.MoveNext():
 x=it.GetCurrentMeshObject();o.append((x.GetName(),x.GetVertexCount(),x.GetTriangleCount(),x.IsManifoldAndOriented()))
b=[];it=m.GetBuildItems()
while it.MoveNext():b.append(it.GetCurrent().GetObjectResource().GetName())
print(json.dumps({"objects":o,"build":b}))'''
    result = subprocess.run([sys.executable, "-c", script, str(path)], check=True, capture_output=True, text=True)
    parsed = json.loads(result.stdout)
    return {
        "object_count": len(parsed["objects"]), "build_item_count": len(parsed["build"]),
        "all_nonempty": all(row[1] and row[2] for row in parsed["objects"]),
        "all_manifold_and_oriented": all(row[3] for row in parsed["objects"]),
        "unique_names": len({row[0] for row in parsed["objects"]}) == len(parsed["objects"]),
    }


def export_all() -> tuple[Path, ...]:
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    export_step(geometry.assembled_test_rig_shape(), ASSEMBLED_STEP)
    export_step(geometry.service_exploded_shape(), EXPLODED_STEP)
    for row, path in zip(geometry.printable_occurrences(), individual_step_paths()): export_step(row["shape"], path)
    write_model_only_3mf()
    return required_artifact_paths()


def _signature(shape):
    box = shape.bounding_box()
    return (len(shape.solids()), tuple(float(v) for v in (box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z)), float(sum(s.volume for s in shape.solids())), all(s.is_valid for s in shape.solids()))


def source_export_parity_evidence() -> dict[str, object]:
    pairs = list(zip((row["shape"] for row in geometry.printable_occurrences()), individual_step_paths()))
    pairs += [(geometry.assembled_test_rig_shape(), ASSEMBLED_STEP), (geometry.service_exploded_shape(), EXPLODED_STEP)]
    rows = []
    for source, path in pairs:
        ss, ws = _signature(source), _signature(import_step(path))
        rows.append({"path": str(path), "solid_count_equal": ss[0] == ws[0], "bounds_error_mm": max(abs(a-b) for a,b in zip(ss[1],ws[1])), "volume_error_mm3": abs(ss[2]-ws[2]), "written_valid": ws[3]})
    return {
        "rows": tuple(rows), "all_required_exist": all(p.is_file() and p.stat().st_size for p in required_artifact_paths()),
        "all_solid_counts_equal": all(r["solid_count_equal"] for r in rows), "all_written_valid": all(r["written_valid"] for r in rows),
        "maximum_bounds_error_mm": max(r["bounds_error_mm"] for r in rows), "maximum_volume_error_mm3": max(r["volume_error_mm3"] for r in rows),
    }


if __name__ == "__main__":
    export_all(); print(json.dumps({"3mf": fresh_lib3mf_import_evidence(), "parity": source_export_parity_evidence()}, indent=2))
