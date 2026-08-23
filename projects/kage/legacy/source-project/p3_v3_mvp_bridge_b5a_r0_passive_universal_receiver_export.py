"""Model-only 3MF export and STEP source/export parity for B5A."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile

from build123d import Compound, import_step
import lib3mf
import trimesh

import p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_geometry as geometry
from p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_spec import MODEL_ROOT, NAMESPACE, SPEC


ASSEMBLED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembled.step"
EXPLODED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembly_order_exploded.step"
MODEL_ONLY_3MF = MODEL_ROOT / f"{NAMESPACE}_four_printed_objects_model_only.3mf"
README = MODEL_ROOT / "README.md"


def required_artifact_paths() -> tuple[Path, ...]:
    return ASSEMBLED_STEP, EXPLODED_STEP, MODEL_ONLY_3MF, README


def _mesh(shape):
    vertices, triangles = shape.tessellate(
        SPEC.mesh_linear_deflection_mm,
        SPEC.mesh_angular_deflection_rad,
    )
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, triangle)) for triangle in triangles],
        process=True,
        validate=True,
    )
    if not mesh.is_watertight or not mesh.is_winding_consistent or not mesh.is_volume:
        raise RuntimeError("B5A printable mesh must be closed, oriented, and volumetric")
    positions = []
    for vertex in mesh.vertices:
        position = lib3mf.Position()
        position.Coordinates[:] = tuple(float(value) for value in vertex)
        positions.append(position)
    indices = []
    for a, b, c in mesh.faces:
        triangle = lib3mf.Triangle()
        triangle.Indices[:] = (int(a), int(b), int(c))
        indices.append(triangle)
    return positions, indices


def write_model_only_3mf(path: Path = MODEL_ONLY_3MF):
    rows = geometry.printable_occurrences()
    if len(rows) != 4:
        raise RuntimeError(f"expected exactly four B5A print objects, got {len(rows)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    object_rows = []
    for row in rows:
        obj = model.AddMeshObject()
        obj.SetName(str(row["label"]))
        obj.SetUUID(str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{row['label']}")))
        vertices, triangles = _mesh(row["shape"])
        obj.SetGeometry(vertices, triangles)
        model.AddBuildItem(obj, wrapper.GetIdentityTransform())
        object_rows.append((row["label"], len(vertices), len(triangles)))
    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=path.parent) as temporary:
        candidate = Path(temporary) / path.name
        model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("3MF ZIP CRC failure")
            forbidden = tuple(
                name for name in archive.namelist()
                if any(token in name.lower() for token in ("project_settings", "model_settings", "slice_info"))
            )
        if forbidden:
            raise RuntimeError(f"model-only 3MF contains slicer settings: {forbidden}")
        path.write_bytes(candidate.read_bytes())
    return {
        "path": str(path),
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "object_count": len(object_rows),
        "objects": tuple(object_rows),
    }


def fresh_lib3mf_import_evidence(path: Path = MODEL_ONLY_3MF):
    script = r'''import json,lib3mf,sys
w=lib3mf.Wrapper();m=w.CreateModel();m.QueryReader("3mf").ReadFromFile(sys.argv[1]);o=[];it=m.GetMeshObjects()
while it.MoveNext():
 x=it.GetCurrentMeshObject();o.append((x.GetName(),x.GetVertexCount(),x.GetTriangleCount(),x.IsManifoldAndOriented()))
b=[];it=m.GetBuildItems()
while it.MoveNext():b.append(it.GetCurrent().GetObjectResource().GetName())
print(json.dumps({"objects":o,"build":b}))'''
    result = subprocess.run(
        [sys.executable, "-c", script, str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    return {
        "object_count": len(data["objects"]),
        "build_item_count": len(data["build"]),
        "all_nonempty": all(row[1] and row[2] for row in data["objects"]),
        "all_manifold_and_oriented": all(row[3] for row in data["objects"]),
        "unique_names": len({row[0] for row in data["objects"]}) == len(data["objects"]),
    }


def _signature(shape):
    box = shape.bounding_box()
    return (
        len(shape.solids()),
        (box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z),
        sum(solid.volume for solid in shape.solids()),
        all(solid.is_valid and solid.volume > 0 for solid in shape.solids()),
    )


def _leaf_occurrences(shape):
    if not shape.children:
        yield shape
        return
    for child in shape.children:
        yield from _leaf_occurrences(child)


def _b5a_leaf_map(shape):
    rows = {}
    for leaf in _leaf_occurrences(shape):
        label = str(leaf.label or "")
        if NAMESPACE in label:
            rows[label] = _signature(leaf)
    return rows


def source_export_parity_evidence():
    rows = []
    for source_children, path in (
        (geometry.b5a_assembled_occurrences(), ASSEMBLED_STEP),
        (geometry.b5a_exploded_occurrences(), EXPLODED_STEP),
    ):
        source_map = _b5a_leaf_map(Compound(children=list(source_children)))
        written_map = _b5a_leaf_map(import_step(path))
        common = tuple(sorted(set(source_map) & set(written_map)))
        missing = tuple(sorted(set(source_map) - set(written_map)))
        unexpected = tuple(sorted(set(written_map) - set(source_map)))
        bounds_error = max(
            (max(abs(a - b) for a, b in zip(source_map[label][1], written_map[label][1])) for label in common),
            default=float("inf"),
        )
        volume_error = max(
            (abs(source_map[label][2] - written_map[label][2]) for label in common),
            default=float("inf"),
        )
        rows.append(
            {
                "path": str(path),
                "source_b5a_leaf_count": len(source_map),
                "written_b5a_leaf_count": len(written_map),
                "missing_labels": missing,
                "unexpected_labels": unexpected,
                "solid_counts_equal": all(source_map[label][0] == written_map[label][0] for label in common),
                "bounds_error_mm": bounds_error,
                "volume_error_mm3": volume_error,
                "written_valid_positive": all(written_map[label][3] for label in common),
            }
        )
    return {
        "rows": tuple(rows),
        "all_labels_equal": all(not row["missing_labels"] and not row["unexpected_labels"] for row in rows),
        "all_solid_counts_equal": all(row["solid_counts_equal"] for row in rows),
        "all_written_valid_positive": all(row["written_valid_positive"] for row in rows),
        "maximum_bounds_error_mm": max(row["bounds_error_mm"] for row in rows),
        "maximum_volume_error_mm3": max(row["volume_error_mm3"] for row in rows),
    }


def post_export_occurrence_validity_evidence():
    from OCP.BRepCheck import BRepCheck_Analyzer

    rows = []
    for path in (ASSEMBLED_STEP, EXPLODED_STEP):
        failures = []
        occurrences = tuple(_leaf_occurrences(import_step(path)))
        for index, occurrence in enumerate(occurrences, start=1):
            solids = tuple(occurrence.solids())
            reasons = []
            if not BRepCheck_Analyzer(occurrence.wrapped, True).IsValid():
                reasons.append("invalidTopology")
            if not solids:
                reasons.append("noSolid")
            if any(float(solid.volume) <= 0.0 for solid in solids):
                reasons.append("nonPositiveVolume")
            if reasons:
                failures.append({"occurrence": index, "label": str(occurrence.label or ""), "reasons": tuple(reasons)})
        rows.append({"path": str(path), "occurrence_count": len(occurrences), "failures": tuple(failures)})
    return {
        "rows": tuple(rows),
        "total_occurrence_count": sum(row["occurrence_count"] for row in rows),
        "failure_count": sum(len(row["failures"]) for row in rows),
        "all_valid_positive": all(not row["failures"] for row in rows),
    }


def write_readme():
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    README.write_text(
        "# B5A passive universal bridge/receiver MVP\n\n"
        "Exactly four printed objects: hour, minute, and second passive bridge/receivers, "
        "plus one DATUM ONLY / NO SENSOR alignment gauge. The assembled and exploded STEP "
        "files also contain accepted predecessor geometry and purchased M3x10, washer, and "
        "nut witnesses. No sensor, PCB, electronics body, or sensing claim is included. "
        "The 3MF is model-only and contains the four B5A printed objects only.\n"
    )
    return README


def export_secondary_artifacts():
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    result = write_model_only_3mf()
    write_readme()
    return result


if __name__ == "__main__":
    export_secondary_artifacts()
    print(json.dumps({"3mf": fresh_lib3mf_import_evidence()}, indent=2))
