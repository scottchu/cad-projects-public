"""Artifact export and source-parity evidence for B3-R1."""

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

import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as geometry
from p3_v3_mvp_roller_b3_r1_blind_axle_towers_spec import MODEL_ROOT, NAMESPACE, SPEC


ASSEMBLED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembled.step"
EXPLODED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembly_order_exploded.step"
MODEL_ONLY_3MF = MODEL_ROOT / f"{NAMESPACE}_twenty_two_printed_objects_model_only.3mf"
README = MODEL_ROOT / "README.md"


def required_artifact_paths() -> tuple[Path, ...]:
    return (ASSEMBLED_STEP, EXPLODED_STEP, MODEL_ONLY_3MF, README)


def _mesh_geometry(shape):
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
        raise RuntimeError("printable mesh is not a closed oriented volume")
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


def write_model_only_3mf(path: Path = MODEL_ONLY_3MF) -> dict[str, object]:
    rows = geometry.printable_occurrences()
    if len(rows) != 22:
        raise RuntimeError(f"expected exactly twenty-two printable objects, got {len(rows)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    objects = []
    for row in rows:
        obj = model.AddMeshObject()
        obj.SetName(str(row["label"]))
        obj.SetUUID(str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{row['label']}")))
        vertices, triangles = _mesh_geometry(row["shape"])
        obj.SetGeometry(vertices, triangles)
        model.AddBuildItem(obj, wrapper.GetIdentityTransform())
        objects.append(
            {
                "name": row["label"],
                "vertices": len(vertices),
                "triangles": len(triangles),
            }
        )
    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=path.parent) as temp:
        candidate = Path(temp) / path.name
        model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("3MF ZIP CRC failed")
            forbidden = [
                name
                for name in archive.namelist()
                if any(
                    token in name.lower()
                    for token in ("project_settings", "model_settings", "slice_info")
                )
            ]
        if forbidden:
            raise RuntimeError(f"model-only 3MF contains slicer settings: {forbidden}")
        path.write_bytes(candidate.read_bytes())
    return {
        "path": str(path),
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "object_count": len(objects),
        "objects": tuple(objects),
    }


def fresh_lib3mf_import_evidence(path: Path = MODEL_ONLY_3MF) -> dict[str, object]:
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
    parsed = json.loads(result.stdout)
    return {
        "object_count": len(parsed["objects"]),
        "build_item_count": len(parsed["build"]),
        "all_nonempty": all(row[1] and row[2] for row in parsed["objects"]),
        "all_manifold_and_oriented": all(row[3] for row in parsed["objects"]),
        "unique_names": len({row[0] for row in parsed["objects"]})
        == len(parsed["objects"]),
    }


def _write_readme() -> None:
    README.write_text(
        "# B3-R1 blind-axle roller towers\n\n"
        "CAD-only MVP evidence for the corrected M3x25 top-retained blind axle. "
        "Contains an assembled witness STEP, an assembly-order exploded STEP, and "
        "a twenty-two-object printed-only 3MF. The 3MF contains only inherited base "
        "and drive prints, the second reusable fixed riser, three C-bar towers, and "
        "nine rollers. Purchased bearings, washers, axles, nuts, and mounting screws "
        "are STEP witnesses only. Ring geometry is an explicit non-print STEP witness "
        "and is excluded from the 3MF. Hall parts, fins, LEDs, motors, and electronics "
        "are not printed deliverables and are not present as assembly components.\n"
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
        tuple(
            float(value)
            for value in (
                box.min.X,
                box.min.Y,
                box.min.Z,
                box.max.X,
                box.max.Y,
                box.max.Z,
            )
        ),
        float(sum(solid.volume for solid in shape.solids())),
        all(solid.is_valid for solid in shape.solids()),
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
        rows.append(
            {
                "path": str(path),
                "solid_count_equal": source_sig[0] == written_sig[0],
                "bounds_error_mm": max(
                    abs(a - b) for a, b in zip(source_sig[1], written_sig[1])
                ),
                "volume_error_mm3": abs(source_sig[2] - written_sig[2]),
                "written_valid": written_sig[3],
            }
        )
    return {
        "rows": tuple(rows),
        "all_required_exist": all(
            path.is_file() and path.stat().st_size for path in required_artifact_paths()
        ),
        "all_solid_counts_equal": all(row["solid_count_equal"] for row in rows),
        "all_written_valid": all(row["written_valid"] for row in rows),
        "maximum_bounds_error_mm": max(row["bounds_error_mm"] for row in rows),
        "maximum_volume_error_mm3": max(row["volume_error_mm3"] for row in rows),
    }


def _leaf_occurrences(shape):
    children = tuple(shape.children)
    if not children:
        yield shape
        return
    for child in children:
        yield from _leaf_occurrences(child)


def _is_self_intersecting(shape) -> bool:
    from OCP.BOPAlgo import BOPAlgo_CheckStatus
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Check

    checker = BRepAlgoAPI_Check(shape.wrapped, True, True)
    checker.Perform()
    if checker.IsValid():
        return False
    return any(
        result.GetCheckStatus() == BOPAlgo_CheckStatus.BOPAlgo_SelfIntersect
        for result in checker.Result()
    )


def post_export_occurrence_validation_evidence() -> dict[str, object]:
    """Apply the strong topology checker to every imported STEP occurrence."""
    from OCP.BRepCheck import BRepCheck_Analyzer

    artifact_rows = []
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
            if _is_self_intersecting(occurrence):
                reasons.append("selfIntersecting")
            if reasons:
                failures.append(
                    {
                        "occurrence": index,
                        "label": occurrence.label,
                        "reasons": tuple(reasons),
                        "solid_count": len(solids),
                        "volumes_mm3": tuple(float(solid.volume) for solid in solids),
                    }
                )
        artifact_rows.append(
            {
                "path": str(path),
                "occurrence_count": len(occurrences),
                "failure_count": len(failures),
                "failures": tuple(failures),
            }
        )
    return {
        "artifacts": tuple(artifact_rows),
        "all_occurrences_valid": all(
            row["failure_count"] == 0 for row in artifact_rows
        ),
    }


if __name__ == "__main__":
    export_all()
    print(
        json.dumps(
            {
                "3mf": fresh_lib3mf_import_evidence(),
                "parity": source_export_parity_evidence(),
                "occurrence_validation": post_export_occurrence_validation_evidence(),
            },
            indent=2,
        )
    )
