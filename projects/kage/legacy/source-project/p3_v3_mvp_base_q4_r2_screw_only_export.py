"""Artifact paths, model-only 3MF, and source/export parity for Q4-R2."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile

from build123d import import_step
import lib3mf
import trimesh

from p3_v3_mvp_base_q4_r2_screw_only_geometry import assembled_shape, printable_occurrences, service_exploded_shape
from p3_v3_mvp_base_q4_r2_screw_only_spec import MODEL_ROOT, NAMESPACE, SPEC


ASSEMBLED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembled.step"
EXPLODED_STEP = MODEL_ROOT / f"{NAMESPACE}_service_exploded.step"
MODEL_ONLY_3MF = MODEL_ROOT / f"{NAMESPACE}_printable_parts_model_only.3mf"
README = MODEL_ROOT / "README.md"


def individual_step_paths() -> tuple[Path, ...]:
    quadrants = tuple(
        MODEL_ROOT / f"{NAMESPACE}_quadrant_Q{index}_front_down.step"
        for index in range(1, SPEC.quadrant_count + 1)
    )
    clamps = tuple(
        MODEL_ROOT / f"{NAMESPACE}_clamp_C{index}_bottom_down.step"
        for index in range(1, SPEC.clamp_count_total + 1)
    )
    return quadrants + clamps


def required_artifact_paths() -> tuple[Path, ...]:
    return (ASSEMBLED_STEP, EXPLODED_STEP, *individual_step_paths(), MODEL_ONLY_3MF, README)


def _mesh_geometry(shape):
    vertices, triangles = shape.tessellate(SPEC.mesh_linear_deflection_mm, SPEC.mesh_angular_deflection_rad)
    welded = trimesh.Trimesh(
        vertices=[(float(vertex.X), float(vertex.Y), float(vertex.Z)) for vertex in vertices],
        faces=[tuple(map(int, triangle)) for triangle in triangles],
        process=True,
        validate=True,
    )
    if not welded.is_watertight or not welded.is_winding_consistent or not welded.is_volume:
        raise RuntimeError("printable Q4-R2 mesh is not one closed oriented shell")
    positions = []
    for vertex in welded.vertices:
        position = lib3mf.Position()
        position.Coordinates[:] = (float(vertex[0]), float(vertex[1]), float(vertex[2]))
        positions.append(position)
    indices = []
    for a, b, c in welded.faces:
        triangle = lib3mf.Triangle()
        triangle.Indices[:] = (int(a), int(b), int(c))
        indices.append(triangle)
    if not positions or not indices:
        raise RuntimeError("printable Q4-R2 body tessellated empty")
    return positions, indices


def write_model_only_3mf(path: Path = MODEL_ONLY_3MF) -> dict[str, object]:
    rows = printable_occurrences()
    if len(rows) != SPEC.printable_body_count:
        raise RuntimeError(f"expected {SPEC.printable_body_count} printable bodies, got {len(rows)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    objects = []
    for row in rows:
        mesh = model.AddMeshObject()
        mesh.SetName(str(row["label"]))
        mesh.SetUUID(str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{row['label']}")))
        vertices, triangles = _mesh_geometry(row["shape"])
        mesh.SetGeometry(vertices, triangles)
        model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
        objects.append(
            {"name": row["label"], "kind": row["kind"], "vertices": len(vertices), "triangles": len(triangles)}
        )
    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=path.parent) as temporary:
        candidate = Path(temporary) / path.name
        model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("model-only Q4-R2 3MF failed ZIP CRC")
            forbidden = sorted(
                name
                for name in archive.namelist()
                if "project_settings" in name.lower()
                or "model_settings" in name.lower()
                or "slice_info" in name.lower()
            )
        if forbidden:
            raise RuntimeError(f"model-only Q4-R2 3MF contains slicer profile members: {forbidden}")
        path.write_bytes(candidate.read_bytes())
    return {
        "path": str(path),
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "objects": tuple(objects),
        "object_count": len(objects),
        "build_item_count": len(objects),
        "printer_process_profiles_embedded": False,
    }


def fresh_lib3mf_import_evidence(path: Path = MODEL_ONLY_3MF) -> dict[str, object]:
    script = r'''
import json, lib3mf, sys
w=lib3mf.Wrapper(); m=w.CreateModel(); m.QueryReader("3mf").ReadFromFile(sys.argv[1])
objects=[]; it=m.GetMeshObjects()
while it.MoveNext():
    o=it.GetCurrentMeshObject()
    objects.append({"name":o.GetName(),"vertices":o.GetVertexCount(),"triangles":o.GetTriangleCount(),"manifold":o.IsManifoldAndOriented()})
build=[]; bit=m.GetBuildItems()
while bit.MoveNext(): build.append(bit.GetCurrent().GetObjectResource().GetName())
print(json.dumps({"objects":objects,"build":build},sort_keys=True))
'''
    completed = subprocess.run([sys.executable, "-c", script, str(path)], check=True, capture_output=True, text=True)
    parsed = json.loads(completed.stdout)
    return {
        "object_count": len(parsed["objects"]),
        "build_item_count": len(parsed["build"]),
        "all_nonempty": all(row["vertices"] > 0 and row["triangles"] > 0 for row in parsed["objects"]),
        "all_manifold_and_oriented": all(row["manifold"] for row in parsed["objects"]),
        "unique_names": len({row["name"] for row in parsed["objects"]}) == len(parsed["objects"]),
        "names": tuple(row["name"] for row in parsed["objects"]),
    }


def _shape_signature(shape) -> dict[str, object]:
    box = shape.bounding_box()
    return {
        "solid_count": len(shape.solids()),
        "bounds_mm": (
            float(box.min.X),
            float(box.min.Y),
            float(box.min.Z),
            float(box.max.X),
            float(box.max.Y),
            float(box.max.Z),
        ),
        "volume_mm3": float(sum(solid.volume for solid in shape.solids())),
        "all_valid": all(bool(solid.is_valid) and solid.volume > 0.0 for solid in shape.solids()),
    }


def source_export_parity_evidence() -> dict[str, object]:
    source_individual = tuple(row["shape"] for row in printable_occurrences())
    rows = []
    for source, path in zip(source_individual, individual_step_paths()):
        written = import_step(path)
        source_signature = _shape_signature(source)
        written_signature = _shape_signature(written)
        rows.append(
            {
                "path": str(path),
                "source": source_signature,
                "written": written_signature,
                "solid_count_equal": source_signature["solid_count"] == written_signature["solid_count"],
                "bounds_error_mm": max(
                    abs(left - right)
                    for left, right in zip(source_signature["bounds_mm"], written_signature["bounds_mm"])
                ),
                "volume_error_mm3": abs(source_signature["volume_mm3"] - written_signature["volume_mm3"]),
            }
        )
    assembly_rows = []
    for source, path in ((assembled_shape(), ASSEMBLED_STEP), (service_exploded_shape(), EXPLODED_STEP)):
        written = import_step(path)
        source_signature = _shape_signature(source)
        written_signature = _shape_signature(written)
        assembly_rows.append(
            {
                "path": str(path),
                "source": source_signature,
                "written": written_signature,
                "solid_count_equal": source_signature["solid_count"] == written_signature["solid_count"],
                "bounds_error_mm": max(
                    abs(left - right)
                    for left, right in zip(source_signature["bounds_mm"], written_signature["bounds_mm"])
                ),
                "volume_error_mm3": abs(source_signature["volume_mm3"] - written_signature["volume_mm3"]),
            }
        )
    all_rows = rows + assembly_rows
    return {
        "individual_rows": tuple(rows),
        "assembly_rows": tuple(assembly_rows),
        "all_paths_exist": all(path.is_file() and path.stat().st_size > 0 for path in required_artifact_paths()),
        "all_solid_counts_equal": all(row["solid_count_equal"] for row in all_rows),
        "maximum_bounds_error_mm": max(row["bounds_error_mm"] for row in all_rows),
        "maximum_volume_error_mm3": max(row["volume_error_mm3"] for row in all_rows),
        "all_written_valid": all(row["written"]["all_valid"] for row in all_rows),
    }


if __name__ == "__main__":
    evidence = write_model_only_3mf()
    evidence["fresh_import"] = fresh_lib3mf_import_evidence()
    print(json.dumps(evidence, indent=2, sort_keys=True))
