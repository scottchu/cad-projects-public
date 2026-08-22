"""Artifact export for the isolated KAGE P3 V3 visualization prototype."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import trimesh
from build123d import export_step

from p3_v3_stacked_three_motor_90deg_geometry import (
    PRIMARY_FACTORIES,
    make_gear_mesh_coupon,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v3_stacked_three_motor_90deg"
PRINT_ROOT = MODEL_ROOT / "print"


def _mesh(shape):
    vertices, triangles = shape.tessellate(0.05, 0.10)
    result = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )
    result.merge_vertices(digits_vertex=5)
    result.update_faces(result.unique_faces())
    result.remove_unreferenced_vertices()
    if not result.is_watertight or not result.is_volume or result.body_count != 1:
        raise ValueError("coupon object must be one watertight positive shell")
    return result


def write_coupon_3mf(path: Path) -> None:
    coupon = make_gear_mesh_coupon()
    named_meshes = []
    for child in coupon.children:
        mesh = _mesh(child)
        mesh.apply_translation(-mesh.bounds[0])
        named_meshes.append((child.label, mesh))

    resources, items = [], []
    cursor_x = 5.0
    for object_id, (name, mesh) in enumerate(named_meshes, 1):
        vertices = "".join(
            f'<vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>' for x, y, z in mesh.vertices
        )
        triangles = "".join(
            f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in mesh.faces
        )
        resources.append(
            f'<object id="{object_id}" type="model" name="{escape(name)}">'
            f'<mesh><vertices>{vertices}</vertices><triangles>{triangles}</triangles></mesh></object>'
        )
        items.append(
            f'<item objectid="{object_id}" transform="1 0 0 0 1 0 0 0 1 {cursor_x:.9g} 5 0"/>'
        )
        cursor_x += float(mesh.extents[0]) + 5.0
    if cursor_x > 251.0 or max(float(mesh.extents[1]) for _, mesh in named_meshes) + 10.0 > 256.0:
        raise ValueError("gear coupon exceeds 256 mm bed contract")

    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        '<metadata name="Title">KAGE P3 V3 provisional 259T to 12T mesh coupon</metadata>'
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


def generate_artifacts() -> None:
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    for name, factory in PRIMARY_FACTORIES:
        export_step(factory(), MODEL_ROOT / f"p3_v3_{name}.step")
    write_coupon_3mf(PRINT_ROOT / "p3_v3_m1_259T_12T_mesh_coupon.3mf")
    manifest = {
        "title": "KAGE P3 V3 stacked three-motor 90-degree drive",
        "status": "visualization prototype; purchased-part fit and gear performance unverified",
        "gear_coupon": "p3_v3_m1_259T_12T_mesh_coupon.3mf",
        "physical_gates": {
            "100_forward_reverse_cycles": "PENDING",
            "24_hour_seconds_speed_run": "PENDING",
            "printed_axial_runout_le_0p2_mm": "PENDING",
        },
        "warning": "The miter gears are envelope visualizations, not printable tooth geometry.",
    }
    (PRINT_ROOT / "p3_v3_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    generate_artifacts()
