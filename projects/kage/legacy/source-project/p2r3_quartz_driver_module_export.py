"""Named, print-oriented STL and 3MF artifacts for KAGE P2R3 Module A."""

from __future__ import annotations

from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import trimesh

from p2r3_quartz_driver_module_geometry import (
    compact_printable_objects,
    make_counterweight_cup,
    make_driver_arm,
    make_fit_coupon_ladder,
    make_full_radius_second_torque_wand,
    make_quartz_mount,
)
from p2r3_quartz_driver_module_spec import P2R3A


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p2r3_quartz_driver_module"
PRINT_ROOT = MODEL_ROOT / "print"


def mesh_data(shape):
    vertices, triangles = shape.tessellate(0.05, 0.10)
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )
    mesh.merge_vertices(digits_vertex=5)
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    trimesh.repair.fix_normals(mesh, multibody=True)
    if not mesh.is_watertight or not mesh.is_volume or mesh.body_count != 1:
        raise ValueError("each P2R3 print mesh must be one watertight positive-volume shell")
    return mesh


def _normalize(mesh):
    mesh = mesh.copy()
    minimum = mesh.bounds[0]
    mesh.apply_translation(-minimum)
    return mesh


def _shelf_pack(named_meshes, *, bed_width: float = 250.0, clearance: float = 6.0):
    """Deterministic 250 mm shelf pack used only for transfer-layout coordinates."""
    normalized = [(name, _normalize(mesh)) for name, mesh in named_meshes]
    normalized.sort(
        key=lambda item: (-(item[1].bounds[1][1] - item[1].bounds[0][1]), item[0])
    )
    cursor_x = cursor_y = row_height = 0.0
    packed = []
    for name, mesh in normalized:
        width = float(mesh.bounds[1][0] - mesh.bounds[0][0])
        depth = float(mesh.bounds[1][1] - mesh.bounds[0][1])
        if cursor_x and cursor_x + width > bed_width:
            cursor_x = 0.0
            cursor_y += row_height + clearance
            row_height = 0.0
        packed.append((name, mesh, cursor_x, cursor_y))
        cursor_x += width + clearance
        row_height = max(row_height, depth)
    if packed:
        total_depth = max(y + float(mesh.bounds[1][1]) for _, mesh, _, y in packed)
        if total_depth > 250.0:
            raise ValueError(f"P2R3 transfer plate exceeds 250 mm depth: {total_depth:.2f}")
    return packed


def write_named_3mf(path: Path, objects, title: str):
    packed = _shelf_pack([(name, mesh_data(shape)) for name, shape in objects])
    resources, items = [], []
    for object_id, (name, mesh, x_shift, y_shift) in enumerate(packed, 1):
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
        transform = f'1 0 0 0 1 0 0 0 1 {x_shift:.9g} {y_shift:.9g} 0'
        items.append(f'<item objectid="{object_id}" transform="{transform}"/>')
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        f'<metadata name="Title">{escape(title)}</metadata>'
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


def _stl_objects():
    objects = compact_printable_objects()
    objects.append(("second_driver_arm_r135_torque_wand", make_full_radius_second_torque_wand()))
    return objects


def generate_print_artifacts():
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    for name, shape in _stl_objects():
        mesh = _normalize(mesh_data(shape))
        mesh.export(PRINT_ROOT / f"{name}.stl", file_type="stl")

    compact = compact_printable_objects()
    write_named_3mf(
        PRINT_ROOT / "p2r3_module_a_compact_validation.3mf",
        compact,
        "KAGE P2R3 Module A compact quartz driver validation",
    )
    torque = [
        ("second_driver_arm_r135_torque_wand", make_full_radius_second_torque_wand()),
        ("counterweight_cup_second", make_counterweight_cup("second", arm_z0=0.0)),
        (
            "coupon_second_hub",
            make_fit_coupon_ladder(
                "second_hub", P2R3A.channel("second").hub_bore_candidates
            ),
        ),
    ]
    write_named_3mf(
        PRINT_ROOT / "p2r3_second_r135_torque_wand.3mf",
        torque,
        "KAGE P2R3 full-radius second-hand torque wand",
    )


if __name__ == "__main__":
    generate_print_artifacts()
