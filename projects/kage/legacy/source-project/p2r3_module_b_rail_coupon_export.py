"""Secondary STL and named 3MF exports for P2R3 Module B."""

from __future__ import annotations

from html import escape
from math import radians
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import trimesh

from p2r3_module_b_rail_coupon_geometry import PRINTABLE_FACTORIES
from p2r3_module_b_rail_coupon_spec import P2R3_MODULE_B


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p2r3_module_b_rail_coupon"
PRINT_ROOT = MODEL_ROOT / "print"


def mesh_data(shape):
    vertices, triangles = shape.tessellate(0.04, 0.10)
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )
    mesh.merge_vertices(digits_vertex=5)
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    # Do not call fix_normals(multibody=True): it orients the blind-pocket
    # cavity as a second positive shell and fills the void in STL/3MF volume.
    # build123d's tessellation already carries the correct nested orientation.
    if not mesh.is_watertight or not mesh.is_volume:
        raise ValueError("each Module-B printable must be one watertight positive shell")
    volume_error = abs(float(mesh.volume) - float(shape.volume))
    if volume_error > max(0.10, abs(float(shape.volume)) * 5e-4):
        raise ValueError(
            f"mesh/source volume mismatch: mesh={mesh.volume:.6f}, BREP={shape.volume:.6f}"
        )
    return mesh


def print_mesh_data(name, shape):
    """Mesh in its validated support-free build orientation with Zmin=0."""
    mesh = mesh_data(shape).copy()
    if name == "removable_gate":
        mesh.apply_transform(
            trimesh.transformations.rotation_matrix(
                radians(P2R3_MODULE_B.gate_side_print_rotation_z_deg), (0.0, 0.0, 1.0)
            )
        )
        mesh.apply_transform(
            trimesh.transformations.rotation_matrix(
                radians(P2R3_MODULE_B.gate_side_print_rotation_x_deg), (1.0, 0.0, 0.0)
            )
        )
    minimum = mesh.bounds[0]
    mesh.apply_translation((-minimum[0], -minimum[1], -minimum[2]))
    return mesh


def _plate_layout(objects):
    placements = {
        "main_rail_coupon": (5.0, 5.0),
        "second_follower_fin": (92.0, 5.0),
        "removable_gate": (112.0, 5.0),
    }
    result = []
    for name, shape in objects:
        mesh = print_mesh_data(name, shape)
        x, y = placements[name]
        result.append((name, mesh, x, y))
    return result


def write_named_3mf(path: Path, objects):
    resources, items = [], []
    for object_id, (name, mesh, tx, ty) in enumerate(_plate_layout(objects), 1):
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
        transform = f'1 0 0 0 1 0 0 0 1 {tx:.9g} {ty:.9g} 0'
        items.append(f'<item objectid="{object_id}" transform="{transform}"/>')
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        '<metadata name="Title">KAGE P2R3 Module-B r135 rail coupon</metadata>'
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
    objects = [(name, factory()) for name, factory in PRINTABLE_FACTORIES]
    for name, shape in objects:
        print_mesh_data(name, shape).export(PRINT_ROOT / f"{name}.stl", file_type="stl")
    write_named_3mf(PRINT_ROOT / "p2r3_module_b_r135_three_part_coupon.3mf", objects)


if __name__ == "__main__":
    generate_print_artifacts()
