"""Deterministic model-only 3MF export for the R1 roller retrofit kit."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile

import lib3mf
import trimesh

from p3_v3_mvp_free_roller_r1_retrofit_geometry import make_print_station_kit
from p3_v3_mvp_free_roller_r1_retrofit_spec import MODEL_ROOT, NAMESPACE, SPEC


STATION_KIT_3MF = MODEL_ROOT / "one_station_retrofit_kit_print_qty3.3mf"
MANIFEST = MODEL_ROOT / "print_manifest.json"


def _mesh(shape):
    vertices, triangles = shape.tessellate(
        SPEC.mesh_linear_deflection_mm,
        SPEC.mesh_angular_deflection_rad,
    )
    mesh = trimesh.Trimesh(
        vertices=[(float(vertex.X), float(vertex.Y), float(vertex.Z)) for vertex in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )
    if not mesh.is_watertight or not mesh.is_winding_consistent or not mesh.is_volume:
        raise RuntimeError(f"{shape.label} did not tessellate as a closed oriented volume")
    return mesh


def _add_mesh(wrapper, model, shape, ordinal: int):
    mesh_data = _mesh(shape)
    mesh = model.AddMeshObject()
    name = shape.label or f"{NAMESPACE}_object_{ordinal}"
    mesh.SetName(name)
    mesh.SetUUID(str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{name}:{ordinal}")))
    positions = []
    for vertex in mesh_data.vertices:
        position = lib3mf.Position()
        position.Coordinates[:] = tuple(float(value) for value in vertex)
        positions.append(position)
    indices = []
    for a, b, c in mesh_data.faces:
        triangle = lib3mf.Triangle()
        triangle.Indices[:] = (int(a), int(b), int(c))
        indices.append(triangle)
    mesh.SetGeometry(positions, indices)
    model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
    return mesh_data


def write_print_exports() -> dict[str, object]:
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    kit = make_print_station_kit()
    shapes = list(kit.children)
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    meshes = [_add_mesh(wrapper, model, shape, index) for index, shape in enumerate(shapes, 1)]
    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=MODEL_ROOT) as temporary:
        candidate = Path(temporary) / STATION_KIT_3MF.name
        model.QueryWriter("3mf").WriteToFile(str(candidate))
        with ZipFile(candidate) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("3MF failed ZIP CRC")
            forbidden = [
                name
                for name in archive.namelist()
                if any(token in name.lower() for token in ("project_settings", "model_settings", "slice_info"))
            ]
        if forbidden:
            raise RuntimeError(f"3MF embeds slicer state: {forbidden}")
        STATION_KIT_3MF.write_bytes(candidate.read_bytes())

    payload = {
        "namespace": NAMESPACE,
        "physical_gate": "CAD accepted only; countersink depth, nut fit, friction, wear and motion require physical checks",
        "existing_base_policy": {
            "replacement_base_exported": False,
            "base_reprint_required": False,
            "existing_part": "canonical Q3 r0 sector, quantity 3",
            "post_print_operation": "six rear ISO M3 90-degree countersinks, D6.0 x 1.45 mm target",
        },
        "lower_axle_socket": {
            "diameter_mm": SPEC.axle_clearance_diameter_mm,
            "z_mm": [SPEC.axle_z_mm[0], SPEC.lower_socket_top_z_mm],
            "depth_mm": SPEC.lower_socket_depth_mm,
            "post_outer_diameter_mm": SPEC.lower_post_od_mm,
            "post_top_z_mm": SPEC.lower_post_top_z_mm,
            "socket_overrun_above_post_mm": SPEC.lower_socket_top_clearance_mm,
            "finished_axle_diameter_mm": SPEC.axle_finished_diameter_mm,
        },
        "one_station_kit": {
            "path": str(STATION_KIT_3MF),
            "sha256": sha256(STATION_KIT_3MF.read_bytes()).hexdigest(),
            "bytes": STATION_KIT_3MF.stat().st_size,
            "object_count": len(shapes),
            "build_item_count": len(shapes),
            "print_quantity": 3,
            "bounds_mm": [
                [float(bounds[1][axis] - bounds[0][axis]) for axis in range(3)]
                for bounds in (mesh.bounds for mesh in meshes)
            ],
            "printer_process_profiles_embedded": False,
        },
        "effective_print_totals": {
            "station_frame": 3,
            "upper_bridge": 3,
            "flanged_spool": 9,
            "spacer": 6,
        },
        "purchased_hardware": {
            "station": "M3x10 90-degree flat-head screw x6; ordinary M3 nut x6",
            "bridge": "M3x6 screw x6; ordinary M3 nut x6",
        },
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    print(json.dumps(write_print_exports(), indent=2, sort_keys=True))
