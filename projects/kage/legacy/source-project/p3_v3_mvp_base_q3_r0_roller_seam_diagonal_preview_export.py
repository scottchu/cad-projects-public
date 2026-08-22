"""Model-only diagnostic 3MF for one identical Q3 sector, print quantity 3."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile

import lib3mf
import trimesh

from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import printable_sector_shape
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec import MODEL_ROOT, NAMESPACE, SPEC


MODEL_ONLY_3MF = MODEL_ROOT / "p3_v3_mvp_base_q3_identical_sector_print_qty3.3mf"
OBJECT_NAME = f"{NAMESPACE}_IDENTICAL_SECTOR_PRINT_QTY_3"


def _mesh_geometry(shape):
    vertices, triangles = shape.tessellate(
        SPEC.mesh_linear_deflection_mm,
        SPEC.mesh_angular_deflection_rad,
    )
    welded = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )
    if (
        not welded.is_watertight
        or not welded.is_winding_consistent
        or not welded.is_volume
        or len(welded.split(only_watertight=False)) != 1
    ):
        raise RuntimeError("Q3 diagnostic sector mesh is not one closed oriented shell")

    positions = []
    for vertex in welded.vertices:
        position = lib3mf.Position()
        position.Coordinates[:] = tuple(float(value) for value in vertex)
        positions.append(position)
    indices = []
    for a, b, c in welded.faces:
        triangle = lib3mf.Triangle()
        triangle.Indices[:] = (int(a), int(b), int(c))
        indices.append(triangle)
    return positions, indices, welded


def write_diagnostic_3mf(path: Path = MODEL_ONLY_3MF) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    mesh = model.AddMeshObject()
    mesh.SetName(OBJECT_NAME)
    mesh.SetUUID(str(uuid5(NAMESPACE_URL, OBJECT_NAME)))
    vertices, triangles, welded = _mesh_geometry(printable_sector_shape(1))
    mesh.SetGeometry(vertices, triangles)
    model.AddBuildItem(mesh, wrapper.GetIdentityTransform())

    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=path.parent) as temporary:
        candidate = Path(temporary) / path.name
        model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("Q3 diagnostic 3MF failed ZIP CRC")
            forbidden = sorted(
                name for name in archive.namelist()
                if any(token in name.lower() for token in ("project_settings", "model_settings", "slice_info"))
            )
        if forbidden:
            raise RuntimeError(f"Q3 diagnostic 3MF contains slicer profile members: {forbidden}")
        path.write_bytes(candidate.read_bytes())

    bounds = welded.bounds
    return {
        "path": str(path),
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "object_name": OBJECT_NAME,
        "object_count": 1,
        "build_item_count": 1,
        "print_quantity": 3,
        "vertices": len(vertices),
        "triangles": len(triangles),
        "manifold_and_oriented": True,
        "bounds_mm": [float(bounds[1][axis] - bounds[0][axis]) for axis in range(3)],
        "printer_process_profiles_embedded": False,
    }


if __name__ == "__main__":
    print(json.dumps(write_diagnostic_3mf(), indent=2, sort_keys=True))
