"""STEP/STL/3MF export helpers for the isolated KAGE P3 V0 prototype."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import trimesh
from build123d import export_step

from p3_v0_motor_outer_ring_geometry import (
    PRINTABLE_FACTORIES,
    make_assembled,
    make_axial_section,
    make_exploded,
    make_hall_module_reference,
    make_official_motor_reference,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v0_motor_outer_ring"
PRINT_ROOT = MODEL_ROOT / "print"


def mesh_data(shape):
    vertices, triangles = shape.tessellate(0.06, 0.12)
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )
    mesh.merge_vertices(digits_vertex=5)
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    if not mesh.is_watertight or not mesh.is_volume or mesh.body_count != 1:
        raise ValueError("each P3 printable must be one watertight positive shell")
    if abs(float(mesh.volume) - float(shape.volume)) > max(0.15, float(shape.volume) * 8e-4):
        raise ValueError("mesh/source volume mismatch")
    return mesh


def _normalized(mesh):
    result = mesh.copy()
    result.apply_translation(-result.bounds[0])
    return result


def _plate_layout(named_shapes):
    placed = []
    cursor_x = 5.0
    cursor_y = 5.0
    row_depth = 0.0
    for name, shape in named_shapes:
        mesh = _normalized(mesh_data(shape))
        width, depth = map(float, mesh.extents[:2])
        if cursor_x + width > 251.0:
            cursor_x = 5.0
            cursor_y += row_depth + 5.0
            row_depth = 0.0
        if cursor_y + depth > 251.0:
            raise ValueError(f"plate exceeds 256 mm bed including 5 mm brim: {name}")
        placed.append((name, mesh, cursor_x, cursor_y))
        cursor_x += width + 5.0
        row_depth = max(row_depth, depth)
    return placed


def write_named_3mf(path: Path, named_shapes):
    resources, items = [], []
    for object_id, (name, mesh, cursor_x, cursor_y) in enumerate(_plate_layout(named_shapes), 1):
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
        transform = f'1 0 0 0 1 0 0 0 1 {cursor_x:.9g} {cursor_y:.9g} 0'
        items.append(f'<item objectid="{object_id}" transform="{transform}"/>')

    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        '<metadata name="Title">KAGE P3 V0 motor outer-ring physical prototype</metadata>'
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


def generate_artifacts():
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    named_shapes = [(name, factory()) for name, factory in PRINTABLE_FACTORIES]
    by_name = dict(named_shapes)
    for name, shape in named_shapes:
        export_step(shape, MODEL_ROOT / f"p3_v0_{name}.step")
        _normalized(mesh_data(shape)).export(PRINT_ROOT / f"{name}.stl", file_type="stl")
    export_step(make_official_motor_reference(), MODEL_ROOT / "p3_v0_official_motor_reference.step")
    export_step(make_hall_module_reference(), MODEL_ROOT / "p3_v0_hall_module_reference.step")
    export_step(make_assembled(), MODEL_ROOT / "p3_v0_assembled.step")
    export_step(make_exploded(), MODEL_ROOT / "p3_v0_service_exploded.step")
    export_step(make_axial_section(), MODEL_ROOT / "p3_v0_axial_section.step")
    stale_combined = PRINT_ROOT / "p3_v0_motor_outer_ring_parts.3mf"
    if stale_combined.exists():
        stale_combined.unlink()
    for stale_single in PRINT_ROOT.glob("*_single_plate.3mf"):
        stale_single.unlink()

    plates = {
        "plate_01_carrier_a.3mf": [("carrier_segment_a", by_name["carrier_segment_a"])],
        "plate_02_carrier_b_hall.3mf": [("carrier_segment_b_hall", by_name["carrier_segment_b_hall"])],
        "plate_03_carrier_c_fin.3mf": [("carrier_segment_c_fin", by_name["carrier_segment_c_fin"])],
        "plate_04_frame_a.3mf": [("frame_quadrant_a", by_name["frame_quadrant_a"])],
        "plate_05_frame_b_hall.3mf": [("frame_quadrant_b_hall", by_name["frame_quadrant_b_hall"])],
        "plate_06_frame_c.3mf": [("frame_quadrant_c", by_name["frame_quadrant_c"])],
        "plate_07_frame_d_motor.3mf": [("frame_quadrant_d_motor", by_name["frame_quadrant_d_motor"])],
        "plate_08_small_petg_hardware.3mf": [
            *((f"carrier_joint_key_{i+1}", by_name["carrier_joint_key"]) for i in range(3)),
            *((f"frame_splice_plate_{i+1}", by_name["frame_splice_plate"]) for i in range(4)),
            ("motor_slide_cradle", by_name["motor_slide_cradle"]),
            ("drive_wheel", by_name["drive_wheel"]),
            *((f"idler_wheel_{i+1}", by_name["idler_wheel"]) for i in range(2)),
            ("hall_bracket", by_name["hall_bracket"]),
            ("hall_spacer_pad_5mm", by_name["hall_spacer_pad"]),
        ],
        "plate_09_tpu_tires.3mf": [
            ("drive_tire", by_name["drive_tire"]),
            *((f"idler_tire_{i+1}", by_name["idler_tire"]) for i in range(2)),
        ],
    }
    for filename, objects in plates.items():
        write_named_3mf(PRINT_ROOT / filename, objects)
    manifest = {
        "title": "KAGE P3 V0 motor outer-ring prototype",
        "bed_mm": [256, 256],
        "brim_mm": 5,
        "note": "Nine independent plates; assembly and exploded models are STEP review files only.",
        "plates": [
            {"file": filename, "material": "TPU" if "tpu" in filename else "PETG"}
            for filename in plates
        ],
    }
    (PRINT_ROOT / "p3_v0_print_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    generate_artifacts()
