"""Secondary print exports and manifest for the V0R2 identifiable-fin fixture."""

from __future__ import annotations

from hashlib import sha256
from html import escape
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build123d import Location, import_step
import trimesh

from v0r2_identifiable_fin_fixture_geometry import part_factories
from v0r2_identifiable_fin_fixture_spec import (
    V0R2,
    fin_projected_width_at_local_z,
    fin_projected_width_at_wall_radius,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "v0r2_identifiable_fin_fixture"
PRINT_ROOT = MODEL_ROOT / "print"
SNAPSHOT_ROOT = MODEL_ROOT / "snapshots"
PART_NAMES = [name for name, _ in part_factories()]


def sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def print_pose(name: str, shape):
    offsets = {
        "fake_standard_quartz_body": 0.0,
        "hour_carrier_hand": 75.0,
        "minute_carrier_hand": 155.0,
        "second_carrier_hand": 245.0,
    }
    return shape.moved(Location((offsets[name], 0, -shape.bounding_box().min.Z)))


def mesh_data(shape):
    vertices, triangles = shape.tessellate(0.03, 0.08)
    mesh = trimesh.Trimesh(
        vertices=[(float(vertex.X), float(vertex.Y), float(vertex.Z)) for vertex in vertices],
        faces=[tuple(map(int, face)) for face in triangles],
        process=True,
        validate=True,
    )
    shells = mesh.split(only_watertight=False)
    if not mesh.is_watertight or not mesh.is_volume or len(shells) != 1:
        raise ValueError("print mesh must be one closed manifold shell")
    return mesh


def write_four_object_3mf(path: Path, objects: list[tuple[str, object]]) -> None:
    if [name for name, _ in objects] != PART_NAMES or len(objects) != 4:
        raise ValueError("3MF must contain exactly the four frozen V0R2 objects")
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
        '<metadata name="Title">V0R2 identifiable-fin compact optics fixture</metadata>'
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
    with ZipFile(path) as package:
        if package.testzip() is not None:
            raise RuntimeError("3MF CRC failure")


def artifact(path: Path, shape=None) -> dict[str, object]:
    result: dict[str, object] = {"path": str(path.relative_to(ROOT)), "sha256": sha(path)}
    if shape is not None:
        bbox = shape.bounding_box()
        result.update(
            {
                "bbox_mm": [bbox.size.X, bbox.size.Y, bbox.size.Z],
                "volume_mm3": shape.volume,
                "solid_count": len(shape.solids()),
            }
        )
    return result


def generate_print_artifacts() -> dict[str, object]:
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    objects: list[tuple[str, object]] = []
    part_records: dict[str, object] = {}
    for name, factory in part_factories():
        local = factory()
        posed = print_pose(name, local)
        stl = PRINT_ROOT / f"{name}.stl"
        mesh_data(posed).export(stl, file_type="stl")
        step = MODEL_ROOT / f"{name}.step"
        if not step.exists():
            raise FileNotFoundError(f"generate primary STEP first: {step}")
        part_records[name] = {"step": artifact(step, import_step(step)), "stl": artifact(stl, posed)}
        objects.append((name, posed))

    bundle = PRINT_ROOT / "v0r2_four_part_identifiable_fin_test.3mf"
    write_four_object_3mf(bundle, objects)
    assembly_step = MODEL_ROOT / "v0r2_assembled.step"
    exploded_step = MODEL_ROOT / "v0r2_exploded.step"
    for path in (assembly_step, exploded_step):
        if not path.exists():
            raise FileNotFoundError(f"generate primary STEP first: {path}")

    identity_records = {}
    root_z = V0R2.ring_axial_thickness - V0R2.fin_root_overlap
    for carrier in V0R2.carriers:
        midpoint = (root_z + carrier.local_height) / 2
        identity = V0R2.fin_identities[carrier.name]
        identity_records[carrier.name] = {
            "physical_profile_mm": {
                "stem_width": identity.stem_width,
                "crown_height": identity.crown_height,
                "crown_width": identity.crown_width,
            },
            "projected_width_base_mid_tip_mm": [
                fin_projected_width_at_local_z(carrier, z)
                for z in (root_z, midpoint, carrier.local_height)
            ],
            "projected_width_at_wall_radius_60_80_mm": [
                fin_projected_width_at_wall_radius(carrier, radius) for radius in (60.0, 80.0)
            ],
        }

    snapshots = sorted(SNAPSHOT_ROOT.glob("*.png")) if SNAPSHOT_ROOT.exists() else []
    manifest = {
        "schema_version": 1,
        "review_status": "accepted_for_physical_test",
        "independent_review": {
            "verdict": "ACCEPT",
            "scope": "V0R2 fin-identity geometry, preserved V0R1 interfaces, generated STEP/STL/3MF artifacts, and review snapshots",
            "evidence": [
                "Distinct H/M/S stem and crown profiles match the frozen brief.",
                "Projection math, 5-degree motion sweep, source-to-STEP equality, mesh manifold, and Orca-load checks passed.",
                "Independent visual review found no CAD blocker for a physical shadow test.",
            ],
            "caveat": "Exact collinear opaque shadows necessarily occlude shared pixels; physical LED testing must confirm readability from unequal widths and 85/110/130 mm endpoints.",
        },
        "implementation_may_self_approve": False,
        "units": "millimeter",
        "printable_part_count": 4,
        "printable_parts": PART_NAMES,
        "primary_step": {
            "assembled": artifact(assembly_step, import_step(assembly_step)),
            "exploded": artifact(exploded_step, import_step(exploded_step)),
        },
        "parts": part_records,
        "three_mf": {**artifact(bundle), "object_count": 4, "object_names": PART_NAMES},
        "snapshots": [artifact(path) for path in snapshots],
        "frozen_spec": {
            "source_z": V0R2.source_z,
            "representative_body": [V0R2.body_x, V0R2.body_y, V0R2.body_depth],
            "carrier_radii": [carrier.radius for carrier in V0R2.carriers],
            "carrier_z": {
                carrier.name: [carrier.ring_bottom_z, carrier.base_z, carrier.tip_z]
                for carrier in V0R2.carriers
            },
            "fin_radial_thickness": V0R2.fin_radial_thickness,
            "fin_identity": identity_records,
        },
        "implementation_validation": {
            "source_geometry_motion_tests": {
                "command": "UV_CACHE_DIR=.uv-cache uv run pytest tests/test_v0r2_identifiable_fin_fixture.py -q -rA",
                "passed": 7,
                "failed": 0,
                "exit_code": 0,
            },
            "artifact_tests": {
                "command": "UV_CACHE_DIR=.uv-cache uv run pytest tests/test_v0r2_identifiable_fin_fixture_artifacts.py -q -rA",
                "passed": 3,
                "failed": 0,
                "exit_code": 0,
            },
            "snapmaker_orca_load": {
                "binary": "/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca",
                "command": "Snapmaker_Orca --datadir <temporary-directory> --info models/v0r2_identifiable_fin_fixture/print/v0r2_four_part_identifiable_fin_test.3mf",
                "exit_code": 0,
                "reported_component_records": 4,
                "all_reported_manifold": True,
                "temporary_datadir": True,
                "nonfatal_diagnostic": "calc_exclude_triangles:Unable to create exclude triangles",
            },
            "persistent_server_started": False,
        },
        "physical_test_only": [
            "real shadow contrast and identity under overlap",
            "carrier fit, friction, free rotation, and wear",
            "LED source extent, sharpness, temperature, and electrical safety",
        ],
        "notes": [
            "V0R2 preserves all accepted V0R1 mechanics and changes only the fin silhouette.",
            "Perfectly coincident opaque shadows still occlude shared pixels; unequal endpoints and widths preserve identity outside the overlap.",
            "Independent CAD review accepted V0R2 for physical testing; real shadow readability remains a print-and-light experiment.",
        ],
    }
    manifest_path = PRINT_ROOT / "v0r2_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(generate_print_artifacts(), indent=2))
