"""Model-only 3MF export and artifact paths for the KAGE B0 base MVP."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile

import lib3mf
import trimesh

from p3_v3_mvp_base_q4_r1_geometry import printable_occurrences
from p3_v3_mvp_base_q4_r1_spec import MODEL_ROOT, NAMESPACE, SPEC


ASSEMBLED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembled.step"
EXPLODED_STEP = MODEL_ROOT / f"{NAMESPACE}_service_exploded.step"
MODEL_ONLY_3MF = MODEL_ROOT / f"{NAMESPACE}_printable_parts_model_only.3mf"
README = MODEL_ROOT / "README.md"
# The generic OrcaSlicer binary on this host opens a GUI and does not return
# from ``--info``.  Snapmaker Orca is the installed U1 tooling and provides a
# deterministic headless parser for the same 3MF core format.
ORCA = Path("/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca")


def individual_step_paths() -> tuple[Path, ...]:
    quadrants = tuple(
        MODEL_ROOT / f"{NAMESPACE}_quadrant_Q{index}_front_down.step"
        for index in range(1, SPEC.quadrant_count + 1)
    )
    bridges = tuple(
        MODEL_ROOT / f"{NAMESPACE}_bridge_S{index}_bottom_down.step"
        for index in range(1, SPEC.bridge_count_total + 1)
    )
    return quadrants + bridges


def required_artifact_paths() -> tuple[Path, ...]:
    return (ASSEMBLED_STEP, EXPLODED_STEP, *individual_step_paths(), MODEL_ONLY_3MF, README)


def _mesh_geometry(shape):
    vertices, triangles = shape.tessellate(
        SPEC.mesh_linear_deflection_mm,
        SPEC.mesh_angular_deflection_rad,
    )
    # OCC tessellation is face-local and therefore duplicates vertices along
    # BREP face seams. Weld and validate those seams before writing 3MF; raw
    # tessellation otherwise looks closed but fails slicer manifold checks.
    welded = trimesh.Trimesh(
        vertices=[(float(vertex.X), float(vertex.Y), float(vertex.Z)) for vertex in vertices],
        faces=[tuple(map(int, triangle)) for triangle in triangles],
        process=True,
        validate=True,
    )
    if (
        not welded.is_watertight
        or not welded.is_winding_consistent
        or not welded.is_volume
        or len(welded.split(only_watertight=False)) != 1
    ):
        raise RuntimeError("printable B0 mesh is not one closed oriented shell")
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
        raise RuntimeError("printable B0 body tessellated empty")
    return positions, indices


def write_model_only_3mf(path: Path = MODEL_ONLY_3MF) -> dict[str, object]:
    """Write eight named mesh objects with no printer/process profile payload."""

    rows = printable_occurrences()
    if len(rows) != SPEC.printable_body_count:
        raise RuntimeError(f"expected {SPEC.printable_body_count} printable bodies, got {len(rows)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    object_rows = []
    for row in rows:
        mesh = model.AddMeshObject()
        mesh.SetName(str(row["label"]))
        mesh.SetUUID(str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{row['label']}")))
        vertices, triangles = _mesh_geometry(row["shape"])
        mesh.SetGeometry(vertices, triangles)
        model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
        object_rows.append(
            {
                "name": row["label"],
                "kind": row["kind"],
                "vertices": len(vertices),
                "triangles": len(triangles),
            }
        )
    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=path.parent) as temporary:
        candidate = Path(temporary) / path.name
        model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("model-only B0 3MF failed ZIP CRC")
            names = set(archive.namelist())
            forbidden_profile_members = sorted(
                name
                for name in names
                if "project_settings" in name.lower()
                or "model_settings" in name.lower()
                or "slice_info" in name.lower()
            )
        if forbidden_profile_members:
            raise RuntimeError(f"model-only 3MF contains slicer profile members: {forbidden_profile_members}")
        path.write_bytes(candidate.read_bytes())
    return {
        "path": str(path),
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "objects": object_rows,
        "object_count": len(object_rows),
        "build_item_count": len(object_rows),
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
    completed = subprocess.run(
        [sys.executable, "-c", script, str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    parsed = json.loads(completed.stdout)
    return {
        "object_count": len(parsed["objects"]),
        "build_item_count": len(parsed["build"]),
        "all_nonempty": all(row["vertices"] > 0 and row["triangles"] > 0 for row in parsed["objects"]),
        "all_manifold_and_oriented": all(row["manifold"] for row in parsed["objects"]),
        "unique_names": len({row["name"] for row in parsed["objects"]}) == len(parsed["objects"]),
        "names": tuple(row["name"] for row in parsed["objects"]),
    }


def orca_load_evidence(path: Path = MODEL_ONLY_3MF, timeout_seconds: int = 90) -> dict[str, object]:
    if not ORCA.is_file():
        return {"available": False, "loaded": False, "path": str(ORCA)}
    completed = subprocess.run(
        [str(ORCA), "--info", str(path)],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    combined = (completed.stdout + completed.stderr).lower()
    return {
        "available": True,
        "loaded": (
            completed.returncode == 0
            and "loading of a model file failed" not in combined
            and "run found error" not in combined
            and combined.count("manifold = yes") == SPEC.printable_body_count
        ),
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-1000:],
        "stderr_tail": completed.stderr[-1000:],
        "path": str(ORCA),
    }


if __name__ == "__main__":
    evidence = write_model_only_3mf()
    evidence["fresh_import"] = fresh_lib3mf_import_evidence()
    evidence["orca"] = orca_load_evidence()
    print(json.dumps(evidence, indent=2, sort_keys=True))
