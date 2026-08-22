"""Deterministic STEP/STL/3MF exporter for the P3 V3 R2 print coupons."""

from __future__ import annotations

from hashlib import sha256
from html import escape
import json
from math import radians
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

import trimesh
from build123d import Axis, Location, export_step, export_stl, import_step

from p3_v3_r2_print_coupon_geometry import (
    PRIMARY_FACTORIES,
    PRINTABLE_GROUPS,
)
from p3_v3_r2_print_coupon_spec import P3_V3_R2_PRINT_COUPON as p


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v3_r2_print_coupons"
PRINT_ROOT = MODEL_ROOT / "print"
STL_ROOT = PRINT_ROOT / "stl"


def _safe_name(label: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in label).strip("_")


def _shape_facts(shape) -> dict[str, object]:
    box = shape.bounding_box()
    return {
        "label": shape.label,
        "solids": len(shape.solids()),
        "volumeMm3": round(float(shape.volume), 6),
        "boundsMm": {
            "min": [round(float(v), 6) for v in tuple(box.min)],
            "max": [round(float(v), 6) for v in tuple(box.max)],
        },
    }


def _print_orientation(label: str) -> tuple[tuple[float, float, float], str]:
    """Return an intentional XYZ Euler orientation for every printable role."""

    if "24T_motor_station_arc" in label:
        return (180.0, 0.0, 0.0), "carrier top annulus on bed; bosses, race, and teeth face upward"
    if "horizontal_miter" in label:
        return (0.0, -90.0, 0.0), "gear axis vertical with broad back face on bed"
    if "vertical_miter" in label or "output_pinion" in label:
        return (0.0, 0.0, 0.0), "gear axis vertical with hub/back face on bed"
    if "fin_6x14x2" in label:
        return (0.0, 0.0, 0.0), "rounded 6x14 foot on bed; blade prints vertically"
    if "bearing_housing" in label:
        return (0.0, 0.0, 0.0), "broad mounting foot on bed"
    if "removable_cap" in label or "saddle" in label or "clamp_strap" in label:
        return (0.0, 0.0, 0.0), "broad planar face on bed"
    if "fit_gauge" in label:
        return (0.0, 0.0, 0.0), "annular gauge face on bed"
    if "guide_shoe" in label:
        return (0.0, 0.0, 0.0), "flat guide base on bed"
    if "seam_lower" in label or "seam_upper" in label:
        return (0.0, 0.0, 0.0), "broad carrier/lap face on bed"
    if "stationary_joiner" in label:
        return (0.0, 0.0, 0.0), "stationary joiner body face on bed"
    raise ValueError(f"no explicit print orientation for {label}")


def _oriented(shape):
    angles, _ = _print_orientation(shape.label)
    result = shape.moved(Location())
    for axis, angle in zip((Axis.X, Axis.Y, Axis.Z), angles):
        if angle:
            result = result.rotate(axis, angle)
    result.label = shape.label
    return result


def _at_print_origin(shape):
    clone = _oriented(shape)
    box = clone.bounding_box()
    return clone.moved(Location((-box.min.X, -box.min.Y, -box.min.Z)))


def _mesh(shape) -> trimesh.Trimesh:
    vertices, triangles = shape.tessellate(0.04, 0.08)
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
        raise ValueError(f"{shape.label} must mesh as one watertight positive body")
    return mesh


def _orientation_matrix(angles: tuple[float, float, float]):
    return trimesh.transformations.euler_matrix(*(radians(value) for value in angles), axes="sxyz")


def _matrix_to_3mf(matrix) -> str:
    values = (
        matrix[0, 0], matrix[1, 0], matrix[2, 0],
        matrix[0, 1], matrix[1, 1], matrix[2, 1],
        matrix[0, 2], matrix[1, 2], matrix[2, 2],
        matrix[0, 3], matrix[1, 3], matrix[2, 3],
    )
    return " ".join(f"{float(value):.9g}" for value in values)


def _pack_meshes(named_meshes, bed_x: float = 250.0, gap: float = 5.0):
    """Shelf-pack raw meshes with explicit per-object rotation transforms."""

    placements = []
    cursor_x = gap
    cursor_y = gap
    row_depth = 0.0
    for name, mesh, angles, intent in named_meshes:
        rotation = _orientation_matrix(angles)
        oriented = mesh.copy()
        oriented.apply_transform(rotation)
        width, depth = float(oriented.extents[0]), float(oriented.extents[1])
        if cursor_x + width + gap > bed_x:
            cursor_x = gap
            cursor_y += row_depth + gap
            row_depth = 0.0
        translation = trimesh.transformations.translation_matrix(
            (
                cursor_x - float(oriented.bounds[0][0]),
                cursor_y - float(oriented.bounds[0][1]),
                -float(oriented.bounds[0][2]),
            )
        )
        transform = translation @ rotation
        placed = mesh.copy()
        placed.apply_transform(transform)
        if abs(float(placed.bounds[0][2])) > 1e-6:
            raise ValueError(f"{name} does not sit at Z=0 after print transform")
        placements.append((name, mesh, transform, placed.bounds.copy(), angles, intent))
        cursor_x += width + gap
        row_depth = max(row_depth, depth)
    return placements, (bed_x, cursor_y + row_depth + gap)


def write_printable_3mf(path: Path, printable_parts) -> dict[str, object]:
    named_meshes = []
    for part in printable_parts:
        angles, intent = _print_orientation(part.label)
        named_meshes.append((part.label, _mesh(part), angles, intent))
    placements, plate_size = _pack_meshes(named_meshes)
    if plate_size[1] > 250.0:
        raise ValueError(f"printable coupon 3MF exceeds 250 mm Y plate: {plate_size[1]:.2f}")
    resources, items = [], []
    placement_facts = []
    for object_id, (name, mesh, transform, bounds, angles, intent) in enumerate(placements, 1):
        vertices = "".join(
            f'<vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>'
            for x, y, z in mesh.vertices
        )
        triangles = "".join(
            f'<triangle v1="{a}" v2="{b}" v3="{c}"/>'
            for a, b, c in mesh.faces
        )
        resources.append(
            f'<object id="{object_id}" type="model" name="{escape(name)}">'
            f"<mesh><vertices>{vertices}</vertices><triangles>{triangles}</triangles></mesh></object>"
        )
        items.append(
            f'<item objectid="{object_id}" transform="{_matrix_to_3mf(transform)}"/>'
        )
        placement_facts.append(
            {
                "objectId": object_id,
                "label": name,
                "orientationEulerDegreesXYZ": list(angles),
                "orientationIntent": intent,
                "transform3mf": _matrix_to_3mf(transform),
                "boundsMm": {
                    "min": [round(float(value), 6) for value in bounds[0]],
                    "max": [round(float(value), 6) for value in bounds[1]],
                },
            }
        )
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        '<metadata name="Title">KAGE P3 V3 R2 progressive print coupons</metadata>'
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
        for member in package.namelist():
            if member.endswith((".xml", ".rels", ".model")) or member == "[Content_Types].xml":
                ET.fromstring(package.read(member))
        root = ET.fromstring(package.read("3D/3dmodel.model"))
        ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
        objects = root.findall(".//m:object", ns)
        items_found = root.findall(".//m:item", ns)
        if len(objects) != len(placements) or len(items_found) != len(placements):
            raise RuntimeError("3MF object/build item count mismatch")
        for obj in objects:
            triangles_node = obj.find("m:mesh/m:triangles", ns)
            if triangles_node is None or not triangles_node.findall("m:triangle", ns):
                raise RuntimeError(f"3MF object {obj.attrib.get('id')} has no triangles")
    return {
        "objects": len(placements),
        "items": len(placements),
        "plateSizeMm": [round(v, 3) for v in plate_size],
        "placements": placement_facts,
        "xmlValidation": "ElementTree parsed all XML members; every mesh has nonempty triangles",
    }


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "p3_v3_r2_print_coupon_spec.py",
        ROOT / "p3_v3_r2_print_coupon_geometry.py",
        ROOT / "p3_v3_r2_print_coupon_export.py",
    )
    return {path.name: sha256(path.read_bytes()).hexdigest() for path in paths}


def _file_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(MODEL_ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path.read_bytes()).hexdigest(),
    }


def generate_artifacts(output_root: Path = MODEL_ROOT) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    print_root = output_root / "print"
    stl_root = print_root / "stl"
    stl_root.mkdir(parents=True, exist_ok=True)

    assembly_records = []
    for name, factory in PRIMARY_FACTORIES:
        source_shape = factory()
        step_path = output_root / f"p3_v3_r2_{name}.step"
        export_step(source_shape, step_path)
        imported = import_step(step_path)
        source_box = source_shape.bounding_box()
        imported_box = imported.bounding_box()
        extent_delta = [
            abs(float(a) - float(b))
            for a, b in zip(tuple(source_box.size), tuple(imported_box.size))
        ]
        if max(extent_delta) > 1e-5 or len(imported.solids()) != len(source_shape.solids()):
            raise RuntimeError(f"STEP source/export parity failed for {name}: {extent_delta}")
        assembly_records.append(
            {
                "name": name,
                "sourceFacts": _shape_facts(source_shape),
                "importedSolids": len(imported.solids()),
                "extentDeltaMm": [round(v, 9) for v in extent_delta],
                "file": _file_record(step_path),
            }
        )

    printable_parts = []
    stl_records = []
    labels = set()
    for group_name, factory in PRINTABLE_GROUPS:
        for part in factory():
            if part.label in labels:
                raise ValueError(f"duplicate printable label: {part.label}")
            labels.add(part.label)
            printable_parts.append(part)
            print_shape = _at_print_origin(part)
            orientation_angles, orientation_intent = _print_orientation(part.label)
            stl_path = stl_root / f"{_safe_name(part.label)}.stl"
            export_stl(print_shape, stl_path, tolerance=0.04, angular_tolerance=0.08)
            mesh = trimesh.load_mesh(stl_path, process=True)
            if not mesh.is_watertight or not mesh.is_volume or mesh.body_count != 1:
                raise RuntimeError(f"STL validation failed for {part.label}")
            stl_records.append(
                {
                    "group": group_name,
                    "sourceFacts": _shape_facts(part),
                    "printFacts": _shape_facts(print_shape),
                    "orientationEulerDegreesXYZ": list(orientation_angles),
                    "orientationIntent": orientation_intent,
                    "meshBodies": int(mesh.body_count),
                    "file": _file_record(stl_path),
                }
            )

    bundle_path = print_root / "p3_v3_r2_printable_coupons.3mf"
    bundle_facts = write_printable_3mf(bundle_path, printable_parts)
    manifest = {
        "title": "KAGE P3 V3 R2 progressive print coupons",
        "status": "CAD acceptance only; dimensional fit, wear, load, noise, and print-process behavior are unverified",
        "coordinateSystem": "XY clock plane; +Z viewer; angle-zero station on +X",
        "frozenTransmission": {
            "module": p.module,
            "pressureAngleDegrees": p.pressure_angle_degrees,
            "ringTeeth": p.ring_teeth,
            "ringPitchRadiusMm": p.ring_pitch_radius,
            "pinionTeeth": p.pinion_teeth,
            "pinionPitchRadiusMm": p.pinion_pitch_radius,
            "centerDistanceMm": p.center_distance,
            "motorArcAngleDegrees": p.motor_arc_angle_degrees,
            "motorArcOuterChordMm": p.motor_arc_chord(),
            "bearingCenterSpanMm": p.bearing_center_span,
        },
        "declaredContacts": [
            "output shaft D-flat to output-pinion D-bore",
            "motor shaft D-flat to horizontal-miter D-bore",
            "output shaft D-flat to vertical-miter D-bore",
            "bearing outer races to housing/cap shoulders",
            "motor body underside to saddle top",
            "motor body top to both printable M3 clamp straps",
            "seam lap split plane and stationary joiner mating faces",
        ],
        "assemblyNote": (
            "Coupon B is a complete horizontal NEMA8 retention and transmission fit assembly. "
            "The two M1 16T miter gears, M1 16T output pinion, saddle, two clamp straps, "
            "bearing housing/cap, guide shoes, fin, fit gauges, and 24T ring arc are printed. "
            "The motor, both shafts, two MR84 bearings, screws, nuts, heat-set inserts, pins, "
            "washers, and shaft collar are purchased and are excluded from the printable-only 3MF."
        ),
        "purchasedBom": [
            {"item": "NEMA8 horizontal stepper motor", "quantity": 1, "specification": "20.3 mm square face x 39.3 mm body; integrated 4 x 7 mm D-shaft, 3.5 mm across-flat"},
            {"item": "output D-shaft", "quantity": 1, "specification": "4.00 mm diameter x 40.0 mm long, 3.5 mm across-flat"},
            {"item": "MR84ZZ bearing", "quantity": 2, "specification": "4 x 8 x 3 mm"},
            {"item": "M2 heat-set insert", "quantity": 4, "specification": "3.2 mm OD x 3.0 mm long; two bearing-cap and two fin-foot bosses"},
            {"item": "M2 socket-head screw", "quantity": 2, "specification": "M2 x 6 mm for removable bearing cap"},
            {"item": "M2 socket-head screw", "quantity": 2, "specification": "M2 x 8 mm for removable fin foot"},
            {"item": "M2 cup-point grub screw", "quantity": 3, "specification": "M2 x 3 mm for two miter hubs and output-pinion hub"},
            {"item": "M3 socket-head screw", "quantity": 4, "specification": "M3 x 30 mm for two motor clamp straps"},
            {"item": "M3 hex nut", "quantity": 4, "specification": "AF 5.5 mm captive in saddle slots"},
            {"item": "M3 washer", "quantity": 4, "specification": "3.2 mm ID x 7 mm OD under clamp-strap screw heads"},
            {"item": "split shaft collar", "quantity": 1, "specification": "4.0 mm bore x 8 mm OD x 5 mm wide with M2 clamp screw"},
            {"item": "M2 countersunk screw", "quantity": 1, "specification": "M2 x 5 mm for seam half-lap"},
            {"item": "M2 hex nut", "quantity": 1, "specification": "AF 4.0 mm for seam half-lap"},
            {"item": "alignment pin", "quantity": 2, "specification": "2.0 mm diameter x 3.0 mm hardened dowel"},
        ],
        "sourceHashes": _source_hashes(),
        "assemblies": assembly_records,
        "individualPrintableStl": stl_records,
        "printableOnly3mf": {**bundle_facts, "file": _file_record(bundle_path)},
        "physicalGates": {
            "seamClampTorqueAndSlip": "PENDING",
            "alignmentPinInsertionAndRemoval": "PENDING",
            "guideClearanceSelection": "PENDING",
            "MR84PocketAndCapFit": "PENDING",
            "NEMA8AdjustmentAndMiterMesh": "PENDING",
            "finStiffnessAndShadowQuality": "PENDING",
        },
    }
    manifest_path = output_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


if __name__ == "__main__":
    generate_artifacts()
