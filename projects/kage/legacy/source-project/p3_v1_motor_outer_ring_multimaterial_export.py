"""Aligned multi-volume 3MF export for KAGE P3 V1 wheels."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import trimesh

from p3_v1_motor_outer_ring_multimaterial_geometry import (
    make_drive_material_pair,
    make_idler_material_pair,
)
from p3_v1_motor_outer_ring_multimaterial_spec import P3_V1


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v1_motor_outer_ring_multimaterial"
PRINT_ROOT = MODEL_ROOT / "print"


def _mesh(shape):
    vertices, triangles = shape.tessellate(0.025, 0.05)
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )
    mesh.merge_vertices(digits_vertex=6)
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    if not mesh.is_watertight or not mesh.is_volume or mesh.body_count != 1:
        raise ValueError("each P3 V1 material body must be one watertight positive mesh")
    return mesh


def write_multivolume_3mf(path: Path, role: str, material_pair) -> dict:
    spec = P3_V1
    names = (f"{role}_PETG_hub", f"{role}_TPU_tread")
    meshes = [_mesh(shape) for shape in material_pair]
    combined_min = [min(float(mesh.bounds[0][axis]) for mesh in meshes) for axis in range(3)]
    combined_max = [max(float(mesh.bounds[1][axis]) for mesh in meshes) for axis in range(3)]
    transform_xyz = (
        spec.three_mf_brim - combined_min[0],
        spec.three_mf_brim - combined_min[1],
        -combined_min[2],
    )
    if combined_max[0] + transform_xyz[0] > spec.three_mf_bed_size - spec.three_mf_brim:
        raise ValueError("P3 V1 3MF exceeds X bed contract")
    if combined_max[1] + transform_xyz[1] > spec.three_mf_bed_size - spec.three_mf_brim:
        raise ValueError("P3 V1 3MF exceeds Y bed contract")

    resources = [
        '<basematerials id="1">'
        f'<base name="{escape(spec.petg_material_name)}" displaycolor="{spec.petg_display_color}FF"/>'
        f'<base name="{escape(spec.tpu_material_name)}" displaycolor="{spec.tpu_display_color}FF"/>'
        '</basematerials>'
    ]
    items = []
    transform = (
        f'1 0 0 0 1 0 0 0 1 '
        f'{transform_xyz[0]:.9g} {transform_xyz[1]:.9g} {transform_xyz[2]:.9g}'
    )
    for index, (name, mesh) in enumerate(zip(names, meshes), 0):
        object_id = index + 2
        vertices = "".join(
            f'<vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>'
            for x, y, z in mesh.vertices
        )
        triangles = "".join(
            f'<triangle v1="{a}" v2="{b}" v3="{c}"/>'
            for a, b, c in mesh.faces
        )
        resources.append(
            f'<object id="{object_id}" type="model" name="{escape(name)}" pid="1" pindex="{index}">'
            f'<mesh><vertices>{vertices}</vertices><triangles>{triangles}</triangles></mesh></object>'
        )
        items.append(f'<item objectid="{object_id}" transform="{transform}"/>')

    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        f'<metadata name="Title">KAGE P3 V1 {escape(role)} aligned PETG TPU wheel</metadata>'
        '<metadata name="MaterialAssignment">Explicit core basematerials: PETG pindex 0; TPU pindex 1</metadata>'
        f'<resources>{"".join(resources)}</resources><build>{"".join(items)}</build></model>'
    )
    types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        '</Types>'
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        '</Relationships>'
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", types)
        package.writestr("_rels/.rels", rels)
        package.writestr("3D/3dmodel.model", model)
    with ZipFile(path) as package:
        if package.testzip() is not None:
            raise RuntimeError("3MF CRC failure")
    return {
        "file": path.name,
        "role": role,
        "objects": list(names),
        "materials": [spec.petg_material_name, spec.tpu_material_name],
        "material_assignments_embedded": True,
        "shared_transform": list(transform_xyz),
    }


def generate_artifacts() -> None:
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    entries = [
        write_multivolume_3mf(
            PRINT_ROOT / "p3_v1_drive_wheel_PETG_TPU.3mf",
            "drive",
            make_drive_material_pair(),
        ),
        write_multivolume_3mf(
            PRINT_ROOT / "p3_v1_idler_wheel_PETG_TPU.3mf",
            "idler",
            make_idler_material_pair(),
        ),
    ]
    manifest = {
        "title": "KAGE P3 V1 aligned six-lobe multi-material wheels",
        "unit": "millimeter",
        "bed_mm": [P3_V1.three_mf_bed_size, P3_V1.three_mf_bed_size],
        "brim_mm": P3_V1.three_mf_brim,
        "packages": entries,
        "note": "Each 3MF has two aligned volumes and explicit core basematerial assignments. Confirm filament/tool mapping in the slicer before printing.",
    }
    (PRINT_ROOT / "p3_v1_multimaterial_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    generate_artifacts()
