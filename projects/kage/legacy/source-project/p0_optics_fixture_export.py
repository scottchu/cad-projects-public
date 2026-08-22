"""Secondary mesh/3MF export and manifest generation for P0 optics fixture."""

from __future__ import annotations

from hashlib import sha256
from html import escape
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build123d import Location, export_stl
import trimesh

from p0_optics_fixture_geometry import part_factories
from p0_optics_fixture_spec import P0, projected_contract


PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_ROOT = PROJECT_ROOT / "models" / "p0_optics_fixture"
PRINT_ROOT = MODEL_ROOT / "print"


def _print_shape(name: str, shape, index: int):
    z_shift = -shape.bounding_box().min.Z
    x_shift = 0.0 if name == "pedestal_mask" else 75.0 + (index - 1) * 95.0
    return shape.moved(Location((x_shift, 0, z_shift)))


def _mesh_data(shape):
    vertices, triangles = shape.tessellate(0.03, 0.08)
    # OCC tessellation repeats vertices per face.  STL readers commonly weld
    # those vertices, but strict 3MF readers interpret them as disconnected
    # triangle shells.  Process once here so the actual 3MF topology is
    # manifold instead of relying on slicer repair.
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[(int(a), int(b), int(c)) for a, b, c in triangles],
        process=True,
        validate=True,
    )
    if not mesh.is_watertight or not mesh.is_volume:
        raise ValueError("3MF source mesh is not a closed manifold volume")
    return mesh.vertices.tolist(), mesh.faces.tolist()


def _write_four_object_3mf(path: Path, objects: list[tuple[str, object]]) -> None:
    resources = []
    build_items = []
    for object_id, (name, shape) in enumerate(objects, start=1):
        vertices, triangles = _mesh_data(shape)
        vertex_xml = "".join(f'<vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>' for x, y, z in vertices)
        triangle_xml = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in triangles)
        resources.append(
            f'<object id="{object_id}" type="model" name="{escape(name)}"><mesh><vertices>{vertex_xml}</vertices><triangles>{triangle_xml}</triangles></mesh></object>'
        )
        build_items.append(f'<item objectid="{object_id}"/>')
    model_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        '<metadata name="Title">P0 four-part shadow clock optics fixture</metadata>'
        f'<resources>{"".join(resources)}</resources><build>{"".join(build_items)}</build></model>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        '</Types>'
    )
    relationships = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        '</Relationships>'
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", content_types)
        package.writestr("_rels/.rels", relationships)
        package.writestr("3D/3dmodel.model", model_xml)
        if package.testzip() is not None:
            raise RuntimeError("3MF CRC validation failed")


def generate_print_artifacts() -> dict[str, object]:
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    objects: list[tuple[str, object]] = []
    artifacts: dict[str, dict[str, object]] = {}
    for index, (name, factory) in enumerate(part_factories()):
        local_shape = factory()
        shape = _print_shape(name, local_shape, index)
        stl_path = PRINT_ROOT / f"p0_{name}.stl"
        export_stl(shape, stl_path, tolerance=0.03, angular_tolerance=0.08)
        bbox = shape.bounding_box()
        artifacts[name] = {
            "path": str(stl_path.relative_to(PROJECT_ROOT)),
            "sha256": sha256(stl_path.read_bytes()).hexdigest(),
            "solid_count": len(shape.solids()),
            "bbox_mm": [bbox.size.X, bbox.size.Y, bbox.size.Z],
            "volume_mm3": shape.volume,
        }
        objects.append((name, shape))

    threemf_path = PRINT_ROOT / "p0_four_part_test_bundle.3mf"
    _write_four_object_3mf(threemf_path, objects)
    manifest = {
        "schema_version": 1,
        "status": "pending_independent_review",
        "units": "millimeter",
        "printable_part_count": 4,
        "printable_parts": [name for name, _ in objects],
        "three_mf": {
            "path": str(threemf_path.relative_to(PROJECT_ROOT)),
            "sha256": sha256(threemf_path.read_bytes()).hexdigest(),
            "object_count": 4,
        },
        "spec": {
            "wall_z_mm": P0.wall_z_mm,
            "mask_z_mm": P0.mask_z_mm,
            "hand_planes_z_mm": [hand.plane_z_mm for hand in P0.hands],
            "source_z_mm": P0.source_z_mm,
            "body_rear_diameter_mm": P0.body_rear_diameter_mm,
            "body_mask_diameter_mm": P0.body_mask_diameter_mm,
            "body_depth_mm": P0.body_depth_mm,
            "hand_thickness_mm": P0.hand_thickness_mm,
            "slicer_infill_percent": P0.body_slicer_infill_percent,
        },
        "projection": projected_contract(),
        "stl": artifacts,
        "notes": [
            "CAD body is intentionally solid; apply low infill in the slicer.",
            "Hub pad force and long-term fit are physical-test gates, not CAD claims.",
            "Verify hand release and LED heat shielding before optical testing.",
        ],
    }
    manifest_path = PRINT_ROOT / "p0_print_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    print(json.dumps(generate_print_artifacts(), indent=2))
