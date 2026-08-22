"""Artifact export and source-parity evidence for B2-R2."""

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

import p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_geometry as geometry
from p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_spec import MODEL_ROOT, NAMESPACE, SPEC


ASSEMBLED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembled.step"
EXPLODED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembly_order_exploded.step"
MODEL_ONLY_3MF = MODEL_ROOT / f"{NAMESPACE}_nine_printed_objects_model_only.3mf"
README = MODEL_ROOT / "README.md"


def required_artifact_paths() -> tuple[Path, ...]:
    return (ASSEMBLED_STEP, EXPLODED_STEP, MODEL_ONLY_3MF, README)


def _mesh_geometry(shape):
    vertices, triangles = shape.tessellate(SPEC.mesh_linear_deflection_mm, SPEC.mesh_angular_deflection_rad)
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, t)) for t in triangles],
        process=True,
        validate=True,
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
    if len(rows) != 9:
        raise RuntimeError(f"expected exactly nine printable objects, got {len(rows)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper(); model = wrapper.CreateModel(); objects = []
    for row in rows:
        obj = model.AddMeshObject()
        obj.SetName(str(row["label"]))
        obj.SetUUID(str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{row['label']}")))
        vertices, triangles = _mesh_geometry(row["shape"])
        obj.SetGeometry(vertices, triangles)
        model.AddBuildItem(obj, wrapper.GetIdentityTransform())
        objects.append({"name": row["label"], "vertices": len(vertices), "triangles": len(triangles)})
    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=path.parent) as temp:
        candidate = Path(temp) / path.name
        model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("3MF ZIP CRC failed")
            forbidden = [name for name in archive.namelist() if any(token in name.lower() for token in ("project_settings", "model_settings", "slice_info"))]
        if forbidden:
            raise RuntimeError(f"model-only 3MF contains slicer settings: {forbidden}")
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
        "object_count": len(parsed["objects"]),
        "build_item_count": len(parsed["build"]),
        "all_nonempty": all(row[1] and row[2] for row in parsed["objects"]),
        "all_manifold_and_oriented": all(row[3] for row in parsed["objects"]),
        "unique_names": len({row[0] for row in parsed["objects"]}) == len(parsed["objects"]),
    }


def _write_readme() -> None:
    README.write_text(
        "# B2-R2 corrected populated role stations\n\n"
        "CAD-only MVP evidence. Contains the assembled witness STEP, assembly-order exploded STEP, "
        "and a nine-object printed-only 3MF. Purchased motors, shafts, bearings, collars, shims, "
        "gears, and fasteners are witnesses in STEP only and are excluded from the 3MF. "
        "No rings, rollers, Hall parts, fins, LEDs, or electronics are included.\n"
    )


def export_all() -> tuple[Path, ...]:
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    export_step(geometry.assembled_shape(), ASSEMBLED_STEP)
    export_step(geometry.exploded_assembly_order_shape(), EXPLODED_STEP)
    write_model_only_3mf()
    _write_readme()
    return required_artifact_paths()


def _signature(shape):
    box = shape.bounding_box()
    return (
        len(shape.solids()),
        tuple(float(v) for v in (box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z)),
        float(sum(s.volume for s in shape.solids())),
        all(s.is_valid for s in shape.solids()),
    )


def source_export_parity_evidence() -> dict[str, object]:
    pairs = (
        (geometry.assembled_shape(), ASSEMBLED_STEP),
        (geometry.exploded_assembly_order_shape(), EXPLODED_STEP),
    )
    rows = []
    for source, path in pairs:
        source_sig = _signature(source)
        written_sig = _signature(import_step(path))
        rows.append({
            "path": str(path),
            "solid_count_equal": source_sig[0] == written_sig[0],
            "bounds_error_mm": max(abs(a-b) for a, b in zip(source_sig[1], written_sig[1])),
            "volume_error_mm3": abs(source_sig[2]-written_sig[2]),
            "written_valid": written_sig[3],
        })
    return {
        "rows": tuple(rows),
        "all_required_exist": all(path.is_file() and path.stat().st_size for path in required_artifact_paths()),
        "all_solid_counts_equal": all(row["solid_count_equal"] for row in rows),
        "all_written_valid": all(row["written_valid"] for row in rows),
        "maximum_bounds_error_mm": max(row["bounds_error_mm"] for row in rows),
        "maximum_volume_error_mm3": max(row["volume_error_mm3"] for row in rows),
    }


if __name__ == "__main__":
    export_all()
    print(json.dumps({"3mf": fresh_lib3mf_import_evidence(), "parity": source_export_parity_evidence()}, indent=2))
