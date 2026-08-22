"""Deterministic model-only 3MF exports for the passive roller MVP."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile

import lib3mf
import trimesh

from p3_v3_mvp_free_roller_r0_three_station_geometry import (
    make_derivative_sector_bed_print,
    make_print_station_kit,
)
from p3_v3_mvp_free_roller_r0_three_station_spec import MODEL_ROOT, NAMESPACE, SPEC


BASE_3MF = MODEL_ROOT / "derivative_q3_sector_print_qty3.3mf"
STATION_KIT_3MF = MODEL_ROOT / "one_station_print_kit_print_qty3.3mf"
MANIFEST = MODEL_ROOT / "print_manifest.json"


def _mesh(shape):
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
    if not welded.is_watertight or not welded.is_winding_consistent or not welded.is_volume:
        raise RuntimeError(f"{shape.label} did not tessellate as a closed oriented volume")
    return welded


def _add_mesh(wrapper, model, shape, ordinal: int):
    welded = _mesh(shape)
    mesh = model.AddMeshObject()
    name = shape.label or f"{NAMESPACE}_object_{ordinal}"
    mesh.SetName(name)
    mesh.SetUUID(str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{name}:{ordinal}")))
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
    mesh.SetGeometry(positions, indices)
    model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
    return welded


def _write(path: Path, shapes: list, print_quantity: int) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    meshes = [_add_mesh(wrapper, model, shape, index) for index, shape in enumerate(shapes, 1)]
    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=path.parent) as temporary:
        candidate = Path(temporary) / path.name
        model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None:
                raise RuntimeError(f"{path.name} failed ZIP CRC")
            forbidden = [
                name for name in archive.namelist()
                if any(token in name.lower() for token in ("project_settings", "model_settings", "slice_info"))
            ]
        if forbidden:
            raise RuntimeError(f"{path.name} embeds slicer state: {forbidden}")
        path.write_bytes(candidate.read_bytes())
    bounds = [mesh.bounds for mesh in meshes]
    return {
        "path": str(path),
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "object_count": len(shapes),
        "build_item_count": len(shapes),
        "print_quantity": print_quantity,
        "bounds_mm": [
            [float(box[1][axis] - box[0][axis]) for axis in range(3)]
            for box in bounds
        ],
        "printer_process_profiles_embedded": False,
    }


def write_print_exports() -> dict[str, object]:
    base = _write(BASE_3MF, [make_derivative_sector_bed_print()], 3)
    kit = make_print_station_kit()
    station = _write(STATION_KIT_3MF, list(kit.children), 3)
    payload = {
        "namespace": NAMESPACE,
        "physical_gate": "CAD accepted only; friction, wear and motion require the printed prototype",
        "canonical_base_policy": {
            "artifact_object_count": 1,
            "artifact_build_item_count": 1,
            "copies_per_clock": 3,
            "copies_share_one_canonical_file": True,
            "three_copies_fit_one_u1_bed": False,
        },
        "base": base,
        "one_station_kit": station,
        "effective_totals": {
            "derivative_sector": 3,
            "station_frame": 3,
            "upper_bridge": 3,
            "flanged_spool": 9,
            "spacer": 6,
        },
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    print(json.dumps(write_print_exports(), indent=2, sort_keys=True))
