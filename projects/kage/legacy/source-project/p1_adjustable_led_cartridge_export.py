"""Secondary STL and multi-object 3MF exports for the P1 cartridge."""

from __future__ import annotations

from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import trimesh
from build123d import Location

from p1_adjustable_led_cartridge_geometry import PRINTABLE_FACTORIES


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p1_adjustable_led_cartridge"
PRINT_ROOT = MODEL_ROOT / "print"


def mesh_data(shape):
    vertices, triangles = shape.tessellate(0.05, 0.10)
    return trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )


def print_pose(index: int, shape):
    bbox = shape.bounding_box()
    return shape.moved(Location((index * 82.0, 0, -bbox.min.Z)))


def write_3mf(path: Path, objects: list[tuple[str, object]]) -> None:
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
            f"<mesh><vertices>{vertices}</vertices><triangles>{triangles}</triangles>"
            "</mesh></object>"
        )
        items.append(f'<item objectid="{object_id}"/>')
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        '<metadata name="Title">P1 adjustable LED cartridge printable parts</metadata>'
        f'<resources>{"".join(resources)}</resources><build>{"".join(items)}</build></model>'
    )
    types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        "</Relationships>"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", types)
        package.writestr("_rels/.rels", rels)
        package.writestr("3D/3dmodel.model", model)


def generate_print_artifacts() -> list[Path]:
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    objects = []
    for index, (name, factory) in enumerate(PRINTABLE_FACTORIES):
        posed = print_pose(index, factory())
        path = PRINT_ROOT / f"{name}.stl"
        mesh_data(posed).export(path, file_type="stl")
        outputs.append(path)
        objects.append((name, posed))
    bundle = PRINT_ROOT / "p1_adjustable_led_cartridge_printable_parts.3mf"
    write_3mf(bundle, objects)
    outputs.append(bundle)
    return outputs


if __name__ == "__main__":
    for output in generate_print_artifacts():
        print(output)
