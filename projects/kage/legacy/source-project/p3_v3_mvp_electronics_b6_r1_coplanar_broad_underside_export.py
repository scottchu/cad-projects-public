"""Secondary 3MF export and source/export parity for B6-R1."""

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

import p3_v3_mvp_electronics_b6_r1_coplanar_broad_underside_geometry as geometry
from p3_v3_mvp_electronics_b6_r1_coplanar_broad_underside_spec import MODEL_ROOT, NAMESPACE, SPEC


ASSEMBLED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembled.step"
EXPLODED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembly_order_exploded.step"
MODEL_ONLY_3MF = MODEL_ROOT / f"{NAMESPACE}_one_backbone_model_only.3mf"
README = MODEL_ROOT / "README.md"
STEP_PARTS_REPORT = MODEL_ROOT / "STEP_PARTS_SEARCH.md"


def required_artifact_paths() -> tuple[Path, ...]:
    return ASSEMBLED_STEP, EXPLODED_STEP, MODEL_ONLY_3MF, README, STEP_PARTS_REPORT


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
        raise RuntimeError("B6 printable mesh must be closed, oriented, and volumetric")
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
    path.parent.mkdir(parents=True, exist_ok=True)
    shape = geometry.printable_shape()
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    obj = model.AddMeshObject()
    obj.SetName(str(shape.label))
    obj.SetUUID(str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{shape.label}")))
    vertices, triangles = _mesh(shape)
    obj.SetGeometry(vertices, triangles)
    model.AddBuildItem(obj, wrapper.GetIdentityTransform())
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
        "object_count": 1,
        "vertex_count": len(vertices),
        "triangle_count": len(triangles),
    }


def fresh_lib3mf_import_evidence(path: Path = MODEL_ONLY_3MF):
    script = r'''import json,lib3mf,sys
w=lib3mf.Wrapper();m=w.CreateModel();m.QueryReader("3mf").ReadFromFile(sys.argv[1]);o=[];it=m.GetMeshObjects()
while it.MoveNext():
 x=it.GetCurrentMeshObject();o.append((x.GetName(),x.GetVertexCount(),x.GetTriangleCount(),x.IsManifoldAndOriented()))
b=[];it=m.GetBuildItems()
while it.MoveNext():b.append(it.GetCurrent().GetObjectResource().GetName())
print(json.dumps({"objects":o,"build":b}))'''
    result = subprocess.run([sys.executable, "-c", script, str(path)], check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return {
        "object_count": len(data["objects"]),
        "build_item_count": len(data["build"]),
        "all_nonempty": all(row[1] and row[2] for row in data["objects"]),
        "all_manifold_and_oriented": all(row[3] for row in data["objects"]),
        "unique_names": len({row[0] for row in data["objects"]}) == len(data["objects"]),
    }


def _leaves(shape):
    if not shape.children:
        yield shape
        return
    for child in shape.children:
        yield from _leaves(child)


def _signature(shape):
    box = shape.bounding_box()
    return (
        len(shape.solids()),
        (box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z),
        sum(solid.volume for solid in shape.solids()),
        all(solid.is_valid and solid.volume > 0.0 for solid in shape.solids()),
    )


def _find_backbone(shape):
    candidates = [
        leaf for leaf in _leaves(shape)
        if "one_solid_PETG_backbone" in str(leaf.label or "") or "step_02_B6_backbone" in str(leaf.label or "")
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"expected one B6 backbone occurrence, got {len(candidates)}")
    return candidates[0]


def source_export_parity_evidence():
    source = _signature(geometry.backbone_shape())
    rows = []
    for path, exploded_dz in ((ASSEMBLED_STEP, 0.0), (EXPLODED_STEP, -45.0)):
        written = _signature(_find_backbone(import_step(path)))
        expected_bounds = tuple(
            value + (exploded_dz if index in (2, 5) else 0.0)
            for index, value in enumerate(source[1])
        )
        rows.append(
            {
                "path": str(path),
                "solid_count_equal": source[0] == written[0],
                "bounds_error_mm": max(abs(a - b) for a, b in zip(expected_bounds, written[1])),
                "volume_error_mm3": abs(source[2] - written[2]),
                "written_valid_positive": written[3],
            }
        )
    return {
        "rows": tuple(rows),
        "all_solid_counts_equal": all(row["solid_count_equal"] for row in rows),
        "all_written_valid_positive": all(row["written_valid_positive"] for row in rows),
        "maximum_bounds_error_mm": max(row["bounds_error_mm"] for row in rows),
        "maximum_volume_error_mm3": max(row["volume_error_mm3"] for row in rows),
    }


def write_readme():
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    README.write_text(
        "# B6-R1 coplanar broad-underside electronics backbone MVP\n\n"
        "One removable PETG printed solid mounted on the eight existing R4 seam axes. "
        "R1 removes the rejected four isolated landing pips and extends the complete "
        "connected footprint to a broad coplanar global underside at Z=-25.5 mm while "
        "preserving the R0 functional web and pad top elevations. "
        "The assembled and exploded STEP files contain non-print board, hardware, cable, "
        "antenna, and thermal witnesses. Electronics envelopes are replaceable and no "
        "board-specific hole pattern is claimed. The 3MF is model-only and contains exactly "
        "the single B6 backbone. B4 moving rings remain the last assembly step.\n"
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
