"""Secondary print exports and manifest for the V0 upright-fin fixture."""

from __future__ import annotations

from hashlib import sha256
from html import escape
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from build123d import Location, import_step
import trimesh

from v0_upright_fin_fixture_geometry import part_factories
from v0_upright_fin_fixture_spec import V0, projected_radius, required_half_angle


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "v0_upright_fin_fixture"
PRINT_ROOT = MODEL_ROOT / "print"
SNAPSHOT_ROOT = MODEL_ROOT / "snapshots"
PART_NAMES = [name for name, _ in part_factories()]


def sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def print_pose(name: str, shape):
    offsets = {"fake_quartz_mask_body": 0.0, "hour_carrier_hand": 100.0,
               "minute_carrier_hand": 180.0, "second_carrier_hand": 275.0}
    return shape.moved(Location((offsets[name], 0, -shape.bounding_box().min.Z)))


def mesh_data(shape):
    vertices, triangles = shape.tessellate(0.03, 0.08)
    mesh = trimesh.Trimesh(
        vertices=[(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        faces=[tuple(map(int, face)) for face in triangles], process=True, validate=True,
    )
    if not mesh.is_watertight or not mesh.is_volume or len(mesh.split(only_watertight=False)) != 1:
        raise ValueError("print mesh must be one closed manifold shell")
    return mesh


def write_four_object_3mf(path: Path, objects: list[tuple[str, object]]) -> None:
    resources, items = [], []
    for object_id, (name, shape) in enumerate(objects, 1):
        mesh = mesh_data(shape)
        vertices = "".join(f'<vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>' for x, y, z in mesh.vertices)
        triangles = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in mesh.faces)
        resources.append(f'<object id="{object_id}" type="model" name="{escape(name)}"><mesh><vertices>{vertices}</vertices><triangles>{triangles}</triangles></mesh></object>')
        items.append(f'<item objectid="{object_id}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?>'
             '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             '<metadata name="Title">V0 four-part upright-fin manual optics fixture</metadata>'
             f'<resources>{"".join(resources)}</resources><build>{"".join(items)}</build></model>')
    types = ('<?xml version="1.0" encoding="UTF-8"?>'
             '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
             '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
             '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
            '</Relationships>')
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", types)
        package.writestr("_rels/.rels", rels)
        package.writestr("3D/3dmodel.model", model)
    with ZipFile(path) as package:
        if package.testzip() is not None:
            raise RuntimeError("3MF CRC failure")


def _artifact(path: Path, shape=None) -> dict[str, object]:
    result: dict[str, object] = {"path": str(path.relative_to(ROOT)), "sha256": sha(path)}
    if shape is not None:
        bbox = shape.bounding_box()
        result.update({"bbox_mm": [bbox.size.X, bbox.size.Y, bbox.size.Z],
                       "volume_mm3": shape.volume, "solid_count": len(shape.solids())})
    return result


def generate_print_artifacts() -> dict[str, object]:
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    objects, part_records = [], {}
    for name, factory in part_factories():
        local = factory()
        posed = print_pose(name, local)
        stl = PRINT_ROOT / f"{name}.stl"
        # Export the same welded, validated exterior mesh used by the 3MF so
        # the STL does not retain OCC face-local duplicate seams.
        mesh_data(posed).export(stl, file_type="stl")
        step = MODEL_ROOT / f"{name}.step"
        if not step.exists():
            raise FileNotFoundError(f"generate primary STEP first: {step}")
        part_records[name] = {"step": _artifact(step, import_step(step)), "stl": _artifact(stl, posed)}
        objects.append((name, posed))
    bundle = PRINT_ROOT / "v0_four_part_manual_optics.3mf"
    write_four_object_3mf(bundle, objects)
    assembly_step = MODEL_ROOT / "v0_assembled.step"
    exploded_step = MODEL_ROOT / "v0_exploded.step"
    snapshots = sorted(SNAPSHOT_ROOT.glob("*.png")) if SNAPSHOT_ROOT.exists() else []
    manifest = {
        "schema_version": 1,
        "review_status": "pending_independent_review",
        "implementation_may_self_approve": False,
        "units": "millimeter",
        "printable_part_count": 4,
        "printable_parts": PART_NAMES,
        "primary_step": {"assembled": _artifact(assembly_step, import_step(assembly_step)),
                         "exploded": _artifact(exploded_step, import_step(exploded_step))},
        "parts": part_records,
        "three_mf": {**_artifact(bundle), "object_count": 4},
        "snapshots": [_artifact(path) for path in snapshots],
        "frozen_spec": {
            "source_z": V0.source_z, "body": [V0.body_diameter, V0.body_diameter, V0.body_height],
            "arbor_height": V0.arbor_height, "carrier_radii": [c.radius for c in V0.carriers],
            "ring_section": [V0.ring_radial_width, V0.ring_axial_thickness],
            "fin_section": [V0.fin_radial_thickness, V0.fin_tangential_width],
            "carrier_z": {c.name: [c.ring_bottom_z, c.base_z, c.tip_z] for c in V0.carriers},
            "shadow_targets": {c.name: [48.0, c.target_tip_radius] for c in V0.carriers},
            "required_led_half_angle_degrees": required_half_angle(V0.source_z, 130.0),
        },
        "physical_test_only": ["force", "friction", "wear", "runout", "real shadow quality"],
        "notes": ["Manual optics proof only; not compatible with a real quartz movement.",
                  "Implementation is pending independent geometry and physical review."],
    }
    manifest_path = PRINT_ROOT / "v0_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(generate_print_artifacts(), indent=2))
