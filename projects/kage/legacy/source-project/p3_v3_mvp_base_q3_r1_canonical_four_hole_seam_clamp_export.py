"""Quantity-explicit 3MF handoff for unchanged Q3 sectors and new clamps."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile

import lib3mf
import trimesh

from p3_v3_mvp_base_q3_r1_canonical_four_hole_seam_clamp_geometry import (
    canonical_printable_sector_shape,
    printable_clamp_shape,
)
from p3_v3_mvp_base_q3_r1_canonical_four_hole_seam_clamp_spec import MODEL_ROOT, NAMESPACE, SPEC


SECTOR_3MF = MODEL_ROOT / f"{NAMESPACE}_canonical_sector_print_qty3.3mf"
CLAMP_3MF = MODEL_ROOT / f"{NAMESPACE}_canonical_clamp_print_qty3.3mf"
MANIFEST = MODEL_ROOT / f"{NAMESPACE}_manifest.json"


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
        raise RuntimeError("3MF source is not one closed oriented shell")

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


def _write_one_object_quantity(path: Path, shape, object_name: str, print_quantity: int) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    mesh = model.AddMeshObject()
    mesh.SetName(object_name)
    mesh.SetPartNumber(f"PRINT_QTY_{print_quantity}")
    mesh.SetUUID(str(uuid5(NAMESPACE_URL, object_name)))
    vertices, triangles, welded = _mesh_geometry(shape)
    mesh.SetGeometry(vertices, triangles)
    model.AddBuildItem(mesh, wrapper.GetIdentityTransform())

    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=path.parent) as temporary:
        candidate = Path(temporary) / path.name
        model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None:
                raise RuntimeError(f"{path.name} failed ZIP CRC")
            forbidden = sorted(
                name for name in archive.namelist()
                if any(token in name.lower() for token in ("project_settings", "model_settings", "slice_info"))
            )
        if forbidden:
            raise RuntimeError(f"{path.name} contains slicer profile members: {forbidden}")
        path.write_bytes(candidate.read_bytes())

    bounds = welded.bounds
    return {
        "path": str(path),
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "object_name": object_name,
        "object_count": 1,
        "build_item_count": 1,
        "print_quantity": print_quantity,
        "vertices": len(vertices),
        "triangles": len(triangles),
        "manifold_and_oriented": True,
        "bounds_mm": [float(bounds[1][axis] - bounds[0][axis]) for axis in range(3)],
        "printer_process_profiles_embedded": False,
    }


def write_print_handoff() -> dict[str, object]:
    sector = _write_one_object_quantity(
        SECTOR_3MF,
        canonical_printable_sector_shape(),
        f"{NAMESPACE}_CANONICAL_SECTOR_PRINT_QTY_3",
        SPEC.sector_print_quantity,
    )
    clamp = _write_one_object_quantity(
        CLAMP_3MF,
        printable_clamp_shape(),
        f"{NAMESPACE}_CANONICAL_CLAMP_PRINT_QTY_3",
        SPEC.clamp_print_quantity,
    )
    payload = {
        "namespace": NAMESPACE,
        "status": "CAD_VALIDATED_PHYSICAL_STRENGTH_UNPROVEN",
        "sector": sector,
        "clamp": clamp,
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    print(json.dumps(write_print_handoff(), indent=2, sort_keys=True))
