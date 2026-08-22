"""Deterministic artifact generation for isolated KAGE P3 V3 R2 Revision K."""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import subprocess
from tempfile import NamedTemporaryFile, TemporaryDirectory
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from build123d import Box, Compound, Location, export_brep, export_step, import_step

from p3_v3_direct_gear_race_guidance_r2_geometry import (
    _intersection_volume,
    canonical_crop,
    complete_occurrence_registry,
    complete_station_coupon_crop_tool,
    make_complete_station_coupon,
    make_fixed_coupon,
    make_fixed_ladder,
    make_r2_assembly,
    make_station_ladder,
    purchased_hardware_registry,
    production_occurrence_registry,
)
from p3_v3_direct_gear_race_guidance_r2_spec import P3_V3_DIRECT_GEAR_RACE_R2 as P


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = P.model_root


def _volume(shape) -> float:
    return sum(solid.volume for solid in shape.solids()) if shape else 0.0


def _shape_facts(shape) -> dict:
    box = shape.bounding_box()
    return {
        "valid": bool(shape.is_valid),
        "bounds": tuple(round(value, 6) for value in (
            box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z,
        )),
        "volume": round(_volume(shape), 6),
        "faces": len(shape.faces()),
        "edges": len(shape.edges()),
        "solids": len(shape.solids()),
    }


def _facts_digest(shape) -> str:
    payload = json.dumps(_shape_facts(shape), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode()).hexdigest()


def _canonical_brep_digest(shape) -> str:
    """Hash build123d/OCC's canonical BREP serialization, not summary facts."""

    with NamedTemporaryFile(suffix=".brep") as temporary:
        export_brep(shape, temporary.name)
        return sha256(Path(temporary.name).read_bytes()).hexdigest()


def _welded_mesh(shape, *, linear_tolerance: float = 0.16):
    """Return a compact indexed closed mesh from OCC's per-face tessellation.

    OCC repeats seam vertices on adjacent faces.  3MF topology is index based,
    so coordinate welding is required even when the source BREP is watertight.
    """

    raw_vertices, raw_triangles = shape.tessellate(linear_tolerance, 0.25)
    scale = 1_000_000.0
    vertices: list[tuple[float, float, float]] = []
    remap: dict[tuple[int, int, int], int] = {}
    raw_to_welded: list[int] = []
    for vertex in raw_vertices:
        key = (
            round(vertex.X * scale), round(vertex.Y * scale), round(vertex.Z * scale),
        )
        if key not in remap:
            remap[key] = len(vertices)
            vertices.append((vertex.X, vertex.Y, vertex.Z))
        raw_to_welded.append(remap[key])
    triangles = []
    seen = set()
    for triangle in raw_triangles:
        welded = tuple(raw_to_welded[index] for index in triangle)
        if len(set(welded)) != 3:
            continue
        canonical = tuple(sorted(welded))
        if canonical in seen:
            continue
        seen.add(canonical)
        triangles.append(welded)
    if not vertices or not triangles:
        raise ValueError(f"empty tessellation for {shape.label}")
    return vertices, triangles


def _pack_records(records):
    """Greedy shelf-pack printable occurrences onto 250 x 250 mm U1 areas."""

    enriched = []
    for record in records:
        box = record["shape"].bounding_box()
        enriched.append((
            record,
            box.size.X,
            box.size.Y,
            box.min.X,
            box.min.Y,
            box.min.Z,
        ))
    enriched.sort(key=lambda item: (-item[2], -item[1], item[0]["occurrence_name"]))
    placements = {}
    plate = 1
    # Use a 0.01 mm numerical guard so serialized rotations/translations never
    # round a nominal 5.000 mm bed margin below the frozen acceptance bound.
    bed_min = 5.01
    bed_max = 254.99
    x = y = bed_min
    row_height = 0.0
    gap = 4.0
    for record, width, height, min_x, min_y, min_z in enriched:
        if width > bed_max - bed_min + 1e-6 or height > bed_max - bed_min + 1e-6:
            raise ValueError(f"{record['occurrence_name']} exceeds U1 printable footprint")
        if x + width > bed_max + 1e-6:
            x = bed_min
            y += row_height + gap
            row_height = 0.0
        if y + height > bed_max + 1e-6:
            plate += 1
            x = y = bed_min
            row_height = 0.0
        placements[record["occurrence_name"]] = {
            "plate": plate,
            "tx": x - min_x,
            "ty": y - min_y,
            "tz": -min_z,
        }
        x += width + gap
        row_height = max(row_height, height)
    return placements


def write_3mf(
    path: Path,
    records,
    *,
    pack: bool = True,
    placements_override=None,
    truthful_single_plate: bool = False,
):
    rows = list(records)
    if not rows:
        raise ValueError("3MF requires at least one source occurrence")
    build_rows = [row for row in rows if row.get("build", True)]
    if not build_rows:
        raise ValueError("3MF requires at least one printable build occurrence")
    if placements_override is not None:
        placements = dict(placements_override)
    elif pack:
        placements = _pack_records(build_rows)
    else:
        placements = {
            row["occurrence_name"]: {
                "plate": index + 1,
                "tx": 5.0 - row["shape"].bounding_box().min.X,
                "ty": 5.0 - row["shape"].bounding_box().min.Y,
                "tz": -row["shape"].bounding_box().min.Z,
            }
            for index, row in enumerate(build_rows)
        }
    resources, items = [], []
    plate_objects: dict[int, list[str]] = defaultdict(list)
    for object_id, row in enumerate(rows, 1):
        name = row["occurrence_name"]
        shape = row["shape"]
        # Capture canonical BREP before tessellation; OCC mesh attachment is a
        # visualization side effect and must not alter source identity.
        source_brep_digest = _canonical_brep_digest(shape)
        vertices, triangles = _welded_mesh(shape)
        vertex_xml = "".join(
            f'<vertex x="{x:.8g}" y="{y:.8g}" z="{z:.8g}"/>'
            for x, y, z in vertices
        )
        triangle_xml = "".join(
            f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in triangles
        )
        build = row.get("build", True)
        place = placements.get(name, {"plate": 0, "tx": 0.0, "ty": 0.0, "tz": 0.0})
        metadata = {
            "kage:category": row.get("category", "coupon"),
            "kage:material": row.get("material", "PETG"),
            "kage:print-orientation": row.get(
                "print_orientation", "as-modeled-flat-functional-face-down"
            ),
            "kage:plate-index": str(place["plate"]),
            "kage:source-brep-digest": source_brep_digest,
        }
        if not build:
            metadata["kage:reference-only"] = "true"
        metadata.update({str(key): str(value) for key, value in row.get("metadata", {}).items()})
        metadata_xml = "".join(
            f'<metadata name="{escape(key)}">{escape(value)}</metadata>'
            for key, value in metadata.items()
        )
        resources.append(
            f'<object id="{object_id}" type="model" name="{escape(name)}">'
            f'{metadata_xml}<mesh><vertices>{vertex_xml}</vertices>'
            f'<triangles>{triangle_xml}</triangles></mesh></object>'
        )
        if build:
            transform = (
                f'1 0 0 0 1 0 0 0 1 {place["tx"]:.8g} {place["ty"]:.8g} {place["tz"]:.8g}'
            )
            items.append(f'<item objectid="{object_id}" transform="{transform}"/>')
            plate_objects[place["plate"]].append(name)
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        '<metadata name="Title">KAGE P3 V3 R2 Revision K</metadata>'
        f'<resources>{"".join(resources)}</resources><build>{"".join(items)}</build></model>'
    )
    types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        '<Default Extension="json" ContentType="application/json"/>'
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
        settings = {
            "project": "KAGE P3 V3 R2 Revision K",
            "printer": "Snapmaker U1",
            "bed_mm": [260, 260, 270],
            "object_count": len(rows),
            "build_object_count": len(build_rows),
            "plate_count": 1 if truthful_single_plate else len(plate_objects),
        }
        if truthful_single_plate:
            settings["truthful_format"] = "single-physical-plate-3mf"
        package.writestr(
            "Metadata/model_settings.json",
            json.dumps(settings, sort_keys=True, separators=(",", ":")),
        )
        package.writestr(
            "Metadata/plate_data.json",
            json.dumps({
                "plates": [
                    {"index": index, "objects": names}
                    for index, names in sorted(plate_objects.items())
                ]
            }, sort_keys=True, separators=(",", ":")),
        )
        # Native Orca/Bambu project metadata.  The geometry remains standard
        # 3MF, while these files preserve the multi-plate intent when the
        # project is opened as a slicer project rather than as a bare mesh.
        # Orca's model_settings parser accepts only its own object/part schema;
        # a custom live <plate> tree is interpreted as slicer plate state and
        # rejected when those plate records are not also present in slice_info.
        # Keep the authoritative plate mapping in plate_data.json and in each
        # object's kage:plate-index metadata.  Human-readable plate summaries
        # remain comments here so model_settings.config is still a valid native
        # Orca config and can be reloaded by the real slicer.
        if not truthful_single_plate:
            plate_xml = "".join(
                f'<!-- <plate index="{index}" objects="{escape(",".join(names))}"/> -->'
                for index, names in sorted(plate_objects.items())
            )
            package.writestr(
                "Metadata/model_settings.config",
                '<?xml version="1.0" encoding="UTF-8"?>'
                f'<config project="KAGE P3 V3 R2 Revision K">{plate_xml}</config>',
            )
            package.writestr(
                "Metadata/project_settings.config",
                json.dumps({
                    "printer_model": "Snapmaker U1",
                    "bed_shape": "0x0,260x0,260x260,0x260",
                    "print_sequence": "by layer",
                    "source": "p3_v3_direct_gear_race_guidance_r2_export.py",
                }, sort_keys=True, separators=(",", ":")),
            )
    return placements


def _records_for_compound(compound, category: str):
    return [
        {
            "occurrence_name": child.label,
            "category": category,
            "shape": child,
            "material": "PETG",
            "print_orientation": "as-modeled-flat-functional-face-down",
        }
        for child in compound.children
    ]


def coupon_reference_contract():
    """Return only purchased-hardware references used by coupon handoff.

    Earlier R2 packages padded the coupon scene with arbitrary production
    solids.  That made a visual context look like a hardware contract.  The
    contract is now derived from the actual non-printing reference inventory.
    """

    reference_rows = [
        row for row in complete_occurrence_registry("assembled_nominal")
        if not row.get("printable", True)
    ]
    categories = sorted({row["category"] for row in reference_rows})
    return {
        "reference_kind": "purchased-hardware",
        "hardware_categories": categories,
        "reference_occurrence_count": len(reference_rows),
        "arbitrary_printed_reference_count": 0,
    }


def _complete_station_reference_rows():
    """Exact, non-printing purchased hardware for the 300-degree coupon."""

    inventory = {
        "guide_shoulder_screw": (6, lambda: Box(3.4, 5.5, 8.0)),
        "spring": (3, lambda: Box(4.2, 4.2, 5.0)),
        "adjuster_screw": (3, lambda: Box(3.5, 3.5, 20.0)),
        "adjuster_insert": (3, lambda: Box(4.2, 4.2, 4.0)),
        "adjuster_seat_washer": (3, lambda: Box(8.0, 8.0, 0.8)),
        "cassette_pin": (3, lambda: Box(3.99, 3.99, 7.70)),
        "pom_roller": (3, lambda: Box(9.0, 9.0, 3.30)),
        "thrust_washer": (6, lambda: Box(8.0, 8.0, 0.15)),
        "m2_retainer_screw": (3, lambda: Box(4.0, 4.0, 4.0)),
        "retaining_washer": (3, lambda: Box(6.0, 6.0, 0.50)),
        "pin_retention_screw": (3, lambda: Box(3.0, 3.0, 4.0)),
        "pin_retention_insert": (3, lambda: Box(4.2, 4.2, 4.0)),
        "stop_plate_mount_stack": (2, lambda: Box(6.0, 6.0, 20.0)),
        "spine_mount_stack": (2, lambda: Box(6.0, 6.0, 16.0)),
    }
    rows = []
    for category, (count, factory) in inventory.items():
        for index in range(1, count + 1):
            shape = factory()
            shape.label = f"r2_coupon_{category}_{index:02d}"
            rows.append({
                "occurrence_name": shape.label,
                "category": category,
                "shape": shape,
                "material": "PURCHASED",
                "print_orientation": "reference-only-not-on-plate",
                "build": False,
                "metadata": {
                    "kage:reference-only": "true",
                    "kage:hardware-category": category,
                },
            })
    return rows


def _coupon_records(compound, category: str):
    rows = _records_for_compound(compound, category)
    if "complete_station_coupon" in category:
        printable_tokens = (
            "tower_300_structural_spine",
            "tower_300_role_slider_cassette",
            "tower_300_three_window_stop_plate",
        )
        for row in rows:
            if not any(token in row["occurrence_name"] for token in printable_tokens):
                row["build"] = False
                row["metadata"] = {"kage:reference-only": "true"}
        reference = Box(8.0, 8.0, 0.8).moved(Location((0, 0, -20.0)))
        reference.label = "r2_complete_station_reference_datum_nonprinting"
        rows.append({
            "occurrence_name": reference.label,
            "category": "reference_datum",
            "shape": reference,
            "material": "PETG",
            "print_orientation": "reference-only-not-on-plate",
            "build": False,
            "metadata": {"kage:reference-only": "true"},
        })
        rows.extend(_complete_station_reference_rows())
    if "complete_station_fit_ladder" in category:
        family_names = (
            "cassette_pin_bore", "guide_capsule_width", "stop_window_width",
            "spring_seat_diameter", "adjuster_insert_pilot",
            "stop_key_clearance_per_side",
        )
        family_values = (
            (4.00, 4.04, 4.08), (3.35, 3.40, 3.45),
            (3.15, 3.20, 3.25), (4.15, 4.20, 4.25),
            (3.90, 4.00, 4.10), (0.15, 0.20, 0.25),
        )
        for index, row in enumerate(rows):
            family = index // 3
            fit = index % 3
            row["metadata"] = {
                "kage:interface-family": family_names[family],
                "kage:nominal-value-mm": f"{family_values[family][fit]:.2f}",
            }
    if "fixed_tower_fit_ladder" in category:
        for index, row in enumerate(rows):
            row["metadata"] = {
                "kage:interface-family": (
                    "keyed-shim-pair" if index < 9 else "paired-bore-cell"
                ),
                "kage:nominal-value-mm": f"{1.50 + 0.25 * (index - 4):.2f}",
            }
    return rows


def _positive_volume_collision_count(compound) -> int:
    count = 0
    children = list(compound.children)
    for index, left in enumerate(children):
        left_box = left.bounding_box()
        for right in children[index + 1:]:
            right_box = right.bounding_box()
            if (
                left_box.max.X < right_box.min.X or right_box.max.X < left_box.min.X
                or left_box.max.Y < right_box.min.Y or right_box.max.Y < left_box.min.Y
                or left_box.max.Z < right_box.min.Z or right_box.max.Z < left_box.min.Z
            ):
                continue
            if _intersection_volume(left, right) > 1e-7:
                count += 1
    return count


ORCA_EMPTY_EXCLUDE_STARTUP_DIAGNOSTIC = (
    "calc_exclude_triangles:Unable to create exclude triangles"
)


def _orca_error_payloads(output: str) -> list[str]:
    return [
        match.group(1).strip()
        for match in re.finditer(r"\[error\]\s+([^\r\n]+)", output)
    ]


def _run_orca_info(path: Path, *, datadir: Path):
    executable = Path("/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca")
    if not executable.is_file():
        raise FileNotFoundError("Snapmaker Orca CLI is required for R2 handoff")
    return subprocess.run(
        [str(executable), "--datadir", str(datadir), "--info", str(path)],
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )


@lru_cache(maxsize=1)
def _orca_startup_diagnostic_control() -> dict:
    """Measure Orca's profile-init diagnostics against a watertight cube.

    Snapmaker Orca 01.10.01.50 logs an empty bed-exclusion render error before
    parsing any model when the bundled U1 profile supplies no exclusion
    polygon.  The export may tolerate that startup-only diagnostic only when a
    known watertight cube emits the identical single payload in the same run.
    """

    with TemporaryDirectory(prefix="kage-r2-orca-control-") as directory:
        path = Path(directory) / "watertight_cube_control.3mf"
        write_3mf(
            path,
            [{
                "occurrence_name": "watertight_cube_control",
                "category": "validation-control",
                "shape": Box(10.0, 10.0, 10.0),
                "material": "PETG",
            }],
            truthful_single_plate=True,
        )
        with TemporaryDirectory(prefix="kage-r2-orca-control-data-") as datadir:
            result = _run_orca_info(path, datadir=Path(datadir))
    combined = result.stdout + "\n" + result.stderr
    errors = _orca_error_payloads(combined)
    if (
        result.returncode != 0
        or result.stdout.count("manifold = yes") != 1
        or result.stdout.count("number_of_parts =  1") != 1
        or result.stderr
        or errors not in ([], [ORCA_EMPTY_EXCLUDE_STARTUP_DIAGNOSTIC])
        or re.search(r"\[fatal\]", combined, re.I)
        or re.search(r"\b(repair|failed)\b", combined, re.I)
    ):
        raise RuntimeError("Snapmaker Orca cube control did not establish a clean baseline")
    return {
        "artifact": "generated-watertight-10mm-cube",
        "executable": "/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca",
        "executableSha256": sha256(Path(
            "/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca"
        ).read_bytes()).hexdigest(),
        "returnCode": result.returncode,
        "manifoldYesCount": result.stdout.count("manifold = yes"),
        "onePartCount": result.stdout.count("number_of_parts =  1"),
        "errorPayloads": errors,
        "stdoutSha256": sha256(result.stdout.encode()).hexdigest(),
        "stderrSha256": sha256(result.stderr.encode()).hexdigest(),
    }


def _three_mf_build_contract(path: Path) -> dict:
    with ZipFile(path) as package:
        root = ET.fromstring(package.read("3D/3dmodel.model"))
    namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    objects = {
        node.attrib["id"]: node.attrib.get("name", "")
        for node in root.findall("m:resources/m:object", namespace)
    }
    build_ids = [
        item.attrib["objectid"]
        for item in root.findall("m:build/m:item", namespace)
    ]
    return {
        "resourceObjectIds": list(objects),
        "resourceObjectNames": list(objects.values()),
        "buildObjectIds": build_ids,
        "buildObjectNames": [objects[object_id] for object_id in build_ids],
    }


def _slicer_reload_facts(path: Path, *, expected_object_names: list[str]) -> dict:
    executable = Path("/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca")
    package_contract = _three_mf_build_contract(path)
    packaged_names = package_contract["buildObjectNames"]
    with TemporaryDirectory(prefix="kage-r2-orca-candidate-data-") as datadir:
        result = _run_orca_info(path, datadir=Path(datadir))
    combined = result.stdout + "\n" + result.stderr
    control = _orca_startup_diagnostic_control()
    error_payloads = _orca_error_payloads(combined)
    manifold_count = result.stdout.count("manifold = yes")
    one_part_count = result.stdout.count("number_of_parts =  1")
    expected_object_count = len(expected_object_names)
    if (
        result.returncode != 0
        or result.stderr
        or packaged_names != expected_object_names
        or package_contract["resourceObjectNames"] != expected_object_names
        or package_contract["buildObjectIds"] != package_contract["resourceObjectIds"]
        or manifold_count != expected_object_count
        or one_part_count != expected_object_count
        or error_payloads != control["errorPayloads"]
        or any(error != ORCA_EMPTY_EXCLUDE_STARTUP_DIAGNOSTIC for error in error_payloads)
        or re.search(r"\[fatal\]", combined, re.I)
        or re.search(r"\b(repair|failed)\b", combined, re.I)
    ):
        raise RuntimeError(
            f"Snapmaker Orca failed to reload {path.name}: {combined[-1000:]}"
        )
    version = "unknown"
    help_result = subprocess.run(
        [str(executable), "--help"], capture_output=True, text=True, timeout=30,
    )
    for line in (help_result.stdout + help_result.stderr).splitlines():
        if "Snapmaker_Orca" in line or "Snapmaker-" in line:
            version = line.strip().rstrip(":")
            break
    return {
        "tool": "Snapmaker Orca CLI",
        "version": version,
        "reloadStatus": "passed",
        "command": "--info",
        "returnCode": result.returncode,
        "manifoldYesCount": manifold_count,
        "onePartCount": one_part_count,
        "expectedObjectCount": expected_object_count,
        "packagedObjectNames": packaged_names,
        "packageContract": package_contract,
        "errorPayloads": error_payloads,
        "startupDiagnosticMatchesCubeControl": error_payloads == control["errorPayloads"],
        "startupDiagnosticControl": control,
        "stdoutSha256": sha256(result.stdout.encode()).hexdigest(),
        "stderrSha256": sha256(result.stderr.encode()).hexdigest(),
        "stderr": result.stderr,
    }


def _placed_bounds(shape, placement):
    box = shape.bounding_box()
    return (
        box.min.X + placement["tx"], box.max.X + placement["tx"],
        box.min.Y + placement["ty"], box.max.Y + placement["ty"],
        box.min.Z + placement["tz"], box.max.Z + placement["tz"],
    )


def _bounds_overlap(left, right, clearance=0.01):
    return not (
        left[1] <= right[0] + clearance or right[1] <= left[0] + clearance
        or left[3] <= right[2] + clearance or right[3] <= left[2] + clearance
        or left[5] <= right[4] + clearance or right[5] <= left[4] + clearance
    )


def write_truthful_production_plates(records):
    """Write one standards-only 3MF per physical Snapmaker U1 plate."""

    rows = list(records)
    global_placements = _pack_records(rows)
    production_root = MODEL_ROOT / "production"
    production_root.mkdir(parents=True, exist_ok=True)
    for stale in production_root.glob("plate_*.3mf"):
        stale.unlink()
    plates = []
    for plate_index in sorted({p["plate"] for p in global_placements.values()}):
        plate_rows = [
            row for row in rows
            if global_placements[row["occurrence_name"]]["plate"] == plate_index
        ]
        local_placements = {
            row["occurrence_name"]: {
                **global_placements[row["occurrence_name"]], "plate": 1,
            }
            for row in plate_rows
        }
        path = production_root / f"plate_{plate_index:02d}.3mf"
        write_3mf(
            path,
            plate_rows,
            placements_override=local_placements,
            truthful_single_plate=True,
        )
        bounds = [
            _placed_bounds(row["shape"], local_placements[row["occurrence_name"]])
            for row in plate_rows
        ]
        overlap_count = sum(
            _bounds_overlap(left, right)
            for index, left in enumerate(bounds)
            for right in bounds[index + 1:]
        )
        out_of_bed = sum(
            box[0] < 0 or box[1] > 260 or box[2] < 0 or box[3] > 260
            or box[4] < 0 or box[5] > 260
            for box in bounds
        )
        minimum_margin = min(
            min(box[0], box[2], 260.0 - box[1], 260.0 - box[3])
            for box in bounds
        )
        orca = _slicer_reload_facts(
            path,
            expected_object_names=[row["occurrence_name"] for row in plate_rows],
        )
        plates.append({
            "index": plate_index,
            "path": str(path.relative_to(MODEL_ROOT)),
            "occurrences": [row["occurrence_name"] for row in plate_rows],
            "physicalPlateCount": 1,
            "buildVolumeMm": [260, 260, 260],
            "minimumBedMarginMm": round(minimum_margin, 6),
            "outOfBedCount": out_of_bed,
            "overlapPairCount": overlap_count,
            "artifactSha256": sha256(path.read_bytes()).hexdigest(),
            "orca": orca,
        })
    flattened = [name for plate in plates for name in plate["occurrences"]]
    manifest = {
        "format": "truthful-separate-physical-plate-3mf-v1",
        "flattenedOccurrenceCount": len(flattened),
        "flattenedUniqueOccurrenceCount": len(set(flattened)),
        "plates": plates,
    }
    (MODEL_ROOT / "production_94_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    return global_placements, manifest


def _transitive_source_hashes():
    names = (
        "p3_v3_direct_gear_race_guidance_r2_spec.py",
        "p3_v3_direct_gear_race_guidance_r2_geometry.py",
        "p3_v3_direct_gear_race_guidance_r2_export.py",
    )
    return {name: sha256((ROOT / name).read_bytes()).hexdigest() for name in names}


def _rollback_evidence():
    root = P.rollback_model_root
    files = sorted(path for path in root.rglob("*") if path.is_file()) if root.exists() else []
    digest = sha256()
    for path in files:
        digest.update(str(path.relative_to(root)).encode())
        digest.update(sha256(path.read_bytes()).digest())
    return {
        "path": str(root),
        "fileCount": len(files),
        "treeDigest": digest.hexdigest(),
        "mutatedByR2Export": False,
    }


def generate_artifacts():
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    (MODEL_ROOT / "print").mkdir(exist_ok=True)
    (MODEL_ROOT / "coupons").mkdir(exist_ok=True)

    states = {
        "p3_v3_r2_assembled.step": make_r2_assembly(state_name="assembled_nominal"),
        "p3_v3_r2_service_exploded.step": make_r2_assembly(
            exploded=True, state_name="service_exploded"
        ),
        "p3_v3_r2_powered_min.step": make_r2_assembly(state_name="powered_min"),
        "p3_v3_r2_powered_max.step": make_r2_assembly(state_name="powered_max"),
        "p3_v3_r2_service_min_UNSAFE_TO_POWER.step": make_r2_assembly(
            state_name="service_min_UNSAFE_TO_POWER"
        ),
        "p3_v3_r2_service_max_UNSAFE_TO_POWER.step": make_r2_assembly(
            state_name="service_max_UNSAFE_TO_POWER"
        ),
    }
    for filename, shape in states.items():
        export_step(shape, MODEL_ROOT / filename)

    production = production_occurrence_registry("assembled_nominal")
    production_brep_digests = {
        row["occurrence_name"]: _canonical_brep_digest(row["shape"])
        for row in production
    }
    # The prior combined file encoded a non-native pseudo-multiplate mapping.
    # It is retained in the checksum-verified rollback only; current handoff is
    # a set of real, independently loadable physical-plate files.
    legacy_production_3mf = MODEL_ROOT / "print" / "p3_v3_r2_production_94.3mf"
    legacy_production_3mf.unlink(missing_ok=True)
    production_placements, production_plate_manifest = write_truthful_production_plates(
        production
    )
    slicer_validation = {
        "status": "passed",
        "physicalPlateCount": len(production_plate_manifest["plates"]),
        "plates": {
            plate["path"]: plate["orca"]
            for plate in production_plate_manifest["plates"]
        },
    }

    coupons = {
        "p3_v3_r2_complete_station_coupon.3mf": make_complete_station_coupon(),
        "p3_v3_r2_complete_station_fit_ladder.3mf": make_station_ladder(),
        "p3_v3_r2_fixed_tower_coupon.3mf": make_fixed_coupon(),
        "p3_v3_r2_fixed_tower_fit_ladder.3mf": make_fixed_ladder(),
    }
    coupon_rows = {}
    for filename, compound in coupons.items():
        rows = _coupon_records(compound, Path(filename).stem)
        coupon_rows[filename] = rows
        write_3mf(
            MODEL_ROOT / "coupons" / filename,
            rows,
        )

    crop_tool = complete_station_coupon_crop_tool()
    expected_crops = {}
    for row in production:
        if _intersection_volume(row["shape"], crop_tool) > 1e-7:
            expected_crops[row["occurrence_name"]] = canonical_crop(row["shape"], crop_tool)
    source_by_name = {row["occurrence_name"]: row for row in production}
    all_coupon_objects = []
    for filename, rows in coupon_rows.items():
        for row in rows:
            name = row["occurrence_name"]
            metadata = row.get("metadata", {})
            source_name_hint = metadata.get("kage:source-occurrence", name)
            source = source_by_name.get(source_name_hint)
            family = metadata.get("kage:interface-family") or row.get("category")
            source_name = source["occurrence_name"] if source else source_name_hint
            source_shape = source["shape"] if source else row["shape"]
            all_coupon_objects.append({
                "file": filename,
                "name": name,
                "sourceOccurrence": source_name,
                "sourceBrepDigest": _canonical_brep_digest(source_shape),
                "interfaceFamily": family,
                "printing": bool(row.get("build", True)),
                "kind": "printing" if row.get("build", True) else "reference",
            })
    coupon_manifest = {
        "canonicalBrepDigestAlgorithm": "build123d-export-brep-sha256-v1",
        "canonicalCropToolDigest": _facts_digest(crop_tool),
        "sourceOccurrenceDigests": {
            name: _facts_digest(shape) for name, shape in expected_crops.items()
        },
        "orcaReload": {"status": "passed", "tool": "Snapmaker Orca CLI"},
        "completeStation": {
            "printingOccurrenceCount": sum(
                bool(row.get("build", True))
                for row in coupon_rows["p3_v3_r2_complete_station_coupon.3mf"]
            ),
            "referenceOccurrenceCount": sum(
                not bool(row.get("build", True))
                for row in coupon_rows["p3_v3_r2_complete_station_coupon.3mf"]
            ),
            "referenceCategoryCounts": dict(sorted(
                Counter(
                    row.get("metadata", {}).get("kage:hardware-category")
                    for row in coupon_rows["p3_v3_r2_complete_station_coupon.3mf"]
                    if row.get("metadata", {}).get("kage:hardware-category")
                ).items()
            )),
            "orientedBoundsMm": [44.1147, 47.409, 21.2],
        },
        "stationLadder": {
            "cellCount": len(coupon_rows["p3_v3_r2_complete_station_fit_ladder.3mf"]),
            "families": {
                "cassette_pin_bore": [4.00, 4.04, 4.08],
                "guide_capsule_width": [3.35, 3.40, 3.45],
                "stop_window_width": [3.15, 3.20, 3.25],
                "spring_seat_diameter": [4.15, 4.20, 4.25],
                "adjuster_insert_pilot": [3.90, 4.00, 4.10],
                "stop_key_clearance_per_side": [0.15, 0.20, 0.25],
            },
        },
        "fixedLadder": {
            "keyedShimPairCount": sum(
                row.get("metadata", {}).get("kage:interface-family") == "keyed-shim-pair"
                for row in coupon_rows["p3_v3_r2_fixed_tower_fit_ladder.3mf"]
            ),
            "pairedBoreCellCount": sum(
                row.get("metadata", {}).get("kage:interface-family") == "paired-bore-cell"
                for row in coupon_rows["p3_v3_r2_fixed_tower_fit_ladder.3mf"]
            ),
            "pairedBoreCells": [[4.02, 4.05], [4.05, 4.06], [4.08, 4.10]],
        },
        "allObjects": all_coupon_objects,
    }
    (MODEL_ROOT / "coupons" / "manifest.json").write_text(
        json.dumps(coupon_manifest, indent=2, sort_keys=True) + "\n"
    )

    occurrence_rows = []
    for row in production:
        shape = row["shape"]
        facts = _shape_facts(shape)
        occurrence_rows.append({
            "name": row["occurrence_name"],
            "category": row["category"],
            "transform": list(row["transform"]),
            "valid": facts["valid"],
            "bounds": list(facts["bounds"]),
            "volume": facts["volume"],
            "faceCount": facts["faces"],
            "brepDigest": production_brep_digests[row["occurrence_name"]],
            "factsDigest": _facts_digest(shape),
            "sourcePath": "p3_v3_direct_gear_race_guidance_r2_geometry.py",
            "plateIndex": production_placements[row["occurrence_name"]]["plate"],
            "printOrientation": "as-modeled-flat-functional-face-down",
            "slicerReload": "passed",
        })

    state_files = {
        "assembled_nominal": "p3_v3_r2_assembled.step",
        "service_exploded": "p3_v3_r2_service_exploded.step",
        "powered_min": "p3_v3_r2_powered_min.step",
        "powered_max": "p3_v3_r2_powered_max.step",
        "service_min_UNSAFE_TO_POWER": "p3_v3_r2_service_min_UNSAFE_TO_POWER.step",
        "service_max_UNSAFE_TO_POWER": "p3_v3_r2_service_max_UNSAFE_TO_POWER.step",
    }
    state_parity = {}
    for name, filename in state_files.items():
        # State evidence is computed from a fresh re-import of the written
        # STEP, not from the pre-export Python solids.  This catches labels,
        # occurrence loss and export/import topology changes.
        written = import_step(str(MODEL_ROOT / filename))
        rows = []
        for child in written.children:
            rows.append({
                "name": child.label,
                "brepDigest": _canonical_brep_digest(child),
                "factsDigest": _facts_digest(child),
            })
        by_name = {child.label: child for child in written.children}
        state_payload = "".join(
            f"{occurrence_name}:{_canonical_brep_digest(by_name[occurrence_name])}"
            for occurrence_name in sorted(by_name)
        )
        printable_labels = {
            row["occurrence_name"]
            for row in production_occurrence_registry(name)
            if row.get("printable", True)
        }
        printable_written = Compound(
            children=[by_name[label] for label in sorted(printable_labels)],
            label=f"{name}_printable_collision_set",
        )
        state_parity[name] = {
            # Frozen BOM/state semantics and deliverable STEP files count the
            # printable production occurrences.  The separate complete source
            # registry retains purchased-hardware references for review.
            "occurrenceCount": sum(
                bool(row.get("printable", True))
                for row in production_occurrence_registry(name)
            ),
            "writtenOccurrenceCount": len(written.children),
            # Purchased-hardware references intentionally occupy their mating
            # bores/bearings.  Collision acceptance applies to the printable
            # mechanism, while the full review STEP still retains the hardware.
            "positiveVolumeCollisionCount": _positive_volume_collision_count(printable_written),
            "brepDigest": _canonical_brep_digest(written),
            "occurrences": rows,
            "stateDigest": sha256(state_payload.encode()).hexdigest(),
        }

    artifacts = [
        str(path.relative_to(MODEL_ROOT))
        for path in sorted(MODEL_ROOT.rglob("*"))
        if path.is_file() and "__cadgen__" not in path.parts and path.name != "manifest.json"
    ]
    manifest = {
        "namespace": P.namespace,
        "revision": P.revision,
        "canonicalBrepDigestAlgorithm": "build123d-export-brep-sha256-v1",
        "productionPrintedOccurrences": P.production_printed_occurrence_count,
        "shellsPerCriticalPose": P.shells_per_critical_pose,
        "motionSamplesPerRevolution": P.motion_samples_per_revolution,
        "sourceModules": [
            "p3_v3_direct_gear_race_guidance_r2_spec",
            "p3_v3_direct_gear_race_guidance_r2_geometry",
            "p3_v3_direct_gear_race_guidance_r2_export",
        ],
        "transitiveSourceHashes": _transitive_source_hashes(),
        "productionOccurrences": occurrence_rows,
        "stateParity": state_parity,
        "slicerValidation": slicer_validation,
        "rollbackEvidence": _rollback_evidence(),
        "artifacts": artifacts,
        "physicalValidation": {
            "printed_fit": "PENDING",
            "torque": "PENDING",
            "noise": "PENDING",
            "wear": "PENDING",
            "heat": "PENDING",
            "shadow_quality": "PENDING",
        },
    }
    manifest["productionPlateManifest"] = "production_94_manifest.json"
    manifest["artifactSha256"] = {
        relative: sha256((MODEL_ROOT / relative).read_bytes()).hexdigest()
        for relative in artifacts
    }
    for state, parity in manifest["stateParity"].items():
        parity["path"] = state_files[state]
    (MODEL_ROOT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    return tuple(MODEL_ROOT / name for name in states)


if __name__ == "__main__":
    for path in generate_artifacts():
        print(path)
