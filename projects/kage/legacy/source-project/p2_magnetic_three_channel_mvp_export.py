"""Secondary STL/3MF export for the standalone P2 magnetic mechanism."""

from __future__ import annotations

from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import trimesh

from p2_magnetic_three_channel_mvp_geometry import (
    make_front_cap_ring,
    make_hidden_driver,
    make_rear_base,
    make_separator,
    make_follower,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p2_magnetic_three_channel_mvp"
PRINT_ROOT = MODEL_ROOT / "print"


def mesh_data(shape):
    vertices, triangles = shape.tessellate(0.04, 0.10)
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )
    if not mesh.is_watertight or not mesh.is_volume:
        raise ValueError("print mesh must be watertight positive volume")
    return mesh


def variant_objects(thickness: float):
    tag = str(thickness).replace(".", "p")
    return [
        ("rear_base", make_rear_base()),
        ("hidden_driver_hour", make_hidden_driver("hour")),
        ("hidden_driver_minute", make_hidden_driver("minute")),
        ("hidden_driver_second", make_hidden_driver("second")),
        (f"separator_t{tag}", make_separator(thickness)),
        ("front_cap_ring_r0", make_front_cap_ring(0)),
        ("front_cap_ring_r1", make_front_cap_ring(1)),
        ("front_cap_ring_r2", make_front_cap_ring(2)),
        ("front_cap_ring_r3", make_front_cap_ring(3)),
        ("follower_hour_fin", make_follower("hour", thickness)),
        ("follower_minute_fin", make_follower("minute", thickness)),
        ("follower_second_fin", make_follower("second", thickness)),
    ]


def write_named_3mf(path: Path, objects):
    resources, items = [], []
    for object_id, (name, shape) in enumerate(objects, 1):
        mesh = mesh_data(shape)
        vertices = "".join(
            f'<vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>' for x, y, z in mesh.vertices
        )
        triangles = "".join(
            f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in mesh.faces
        )
        resources.append(
            f'<object id="{object_id}" type="model" name="{escape(name)}">'
            f"<mesh><vertices>{vertices}</vertices><triangles>{triangles}</triangles></mesh></object>"
        )
        items.append(f'<item objectid="{object_id}"/>')
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        '<metadata name="Title">KAGE P2 magnetic three-channel MVP</metadata>'
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


def generate_print_artifacts():
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    # Canonical per-part STL set uses t1.5 followers; variant-specific follower
    # STLs are added so every separator option remains directly printable.
    canonical = variant_objects(1.5)
    for name, shape in canonical:
        mesh_data(shape).export(PRINT_ROOT / f"{name}.stl", file_type="stl")
    for thickness in (1.0, 2.0):
        tag = str(thickness).replace(".", "p")
        for name in ("hour", "minute", "second"):
            mesh_data(make_follower(name, thickness)).export(
                PRINT_ROOT / f"follower_{name}_fin_t{tag}.stl", file_type="stl"
            )
    for thickness in (1.0, 1.5, 2.0):
        tag = str(thickness).replace(".", "p")
        write_named_3mf(
            PRINT_ROOT / f"p2_magnetic_three_channel_mvp_t{tag}.3mf",
            variant_objects(thickness),
        )


if __name__ == "__main__":
    generate_print_artifacts()
