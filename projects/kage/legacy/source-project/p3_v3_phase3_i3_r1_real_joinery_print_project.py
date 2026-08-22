"""Measured U1 placement for the isolated I3-R1 moving halves."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from html import escape
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from tempfile import NamedTemporaryFile
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from build123d import Axis, Location, export_brep

from p3_v3_phase3_i3_r1_real_joinery_geometry import moving_half_shapes
from p3_v3_phase3_i3_r1_real_joinery_spec import (
    ARTIFACT_CONTRACT,
    NAMESPACE,
    PRINT_TRANSFORM,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / NAMESPACE
ORCA_SOURCE_PROJECT = MODEL_ROOT / "i3_8_six_moving_halves_source.3mf"

ORCA_OBJECT_MAP = (
    (1, "hour", "A", "hour_I3_half_A_130T_beta15p230769", "fa6a01e8-5e16-50e5-a679-572d6f97eebb"),
    (2, "hour", "B", "hour_I3_half_B_130T_beta195p230769", "8647d48e-3be7-5bcc-96ce-f99edd27d2f1"),
    (3, "minute", "A", "minute_I3_half_A_130T_beta15p230769", "cd27fc98-3338-5c4a-930a-a5f3641c1250"),
    (4, "minute", "B", "minute_I3_half_B_130T_beta195p230769", "cf2d9c10-7eb8-51f4-9acb-70e15bda166e"),
    (5, "second", "A", "second_I3_half_A_130T_beta15p230769", "e2b2957a-7f3c-57ac-a071-f4ad0ed15dd5"),
    (6, "second", "B", "second_I3_half_B_130T_beta195p230769", "1d950c12-033f-5037-8c6d-7b006ed0746a"),
)

PROFILE_CHAINS = {
    "machine": (
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/machine/Snapmaker U1 (0.4 nozzle).json", "545e4456b78cc58e701ed257e4024b0ed9e2461cccc1046e6f901ce3c020ee0d"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/machine/fdm_U1.json", "ff0724000b1436fcc3d77ffa74bb623a9b322474fc20c8a8d5a26ee164077046"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/machine/fdm_toolchanger.json", "b2ee2d2c31a26ddee7b0c8bd84c58934d9c01e84e1b8f7ae45e14acfd1f7b52a"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/machine/fdm_klipper.json", "78dd750211347543368a8a0f136441ef7e23b3a4a09a9e33a370c91dbda273b9"),
    ),
    "process": (
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/0.20 Standard @Snapmaker U1 (0.4 nozzle).json", "3342dbe3e995b66ab5700245c676f446a88d35f56498b074ab6fe14039d67763"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/fdm_process_U1_0.20.json", "2df28dc2474b6aeb77d5416043b3a67e54ff7ea1cdf5a5daa9e97db7e5b034a6"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/fdm_process_U1_common.json", "43fba9fe359864b265ffa8682cf404c2b935d12164ffe3d0048e5dcb0691db74"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/fdm_process_U1.json", "66e9e51c4bd04cbbec49fa1a3a043bc3c6e329396c2b38a18db5a66b6e72b4e2"),
    ),
    "filament": (
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/user/default/filament/PETG.json", "d7a7c0e5911779e70836bf53c29fd736c8702ff45ad46880690c2f092c5433df"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/filament/Generic PETG.json", "9887427bf889b4364b49b401aa69a1f874ff484e530a09a54be5e77a0bd5ad9b"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/filament/Generic PETG @base.json", "e46b5aac9d983eff69a18f6f2453fc2e5a28f1d581370195ef01c9d0d7032e57"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/filament/fdm_filament_pet_generic.json", "33f78fc9a87c83976a635d23c0303797bc9468c8a1c27ab2d1ef769ea66ac2d1"),
        ("/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/filament/fdm_filament_common_generic.json", "24e4920907489bfdeb250ba749b005c97571d7a547416989af10df502896e99d"),
    ),
}


def _aabb(shape) -> tuple[float, float, float, float, float, float]:
    box = shape.bounding_box()
    return (
        float(box.min.X), float(box.min.Y), float(box.min.Z),
        float(box.max.X), float(box.max.Y), float(box.max.Z),
    )


def _brep_digest(shape) -> str:
    with NamedTemporaryFile(suffix=".brep") as temporary:
        export_brep(shape, temporary.name)
        return sha256(Path(temporary.name).read_bytes()).hexdigest()


def _matrix(rotation_degrees: float, dx: float, dy: float, dz: float) -> tuple[tuple[float, ...], ...]:
    from math import cos, radians, sin

    angle = radians(rotation_degrees)
    c, s = cos(angle), sin(angle)
    return (
        (c, -s, 0.0, dx),
        (s, c, 0.0, dy),
        (0.0, 0.0, 1.0, dz),
        (0.0, 0.0, 0.0, 1.0),
    )


def _inverse_matrix(rotation_degrees: float, dx: float, dy: float, dz: float) -> tuple[tuple[float, ...], ...]:
    from math import cos, radians, sin

    angle = radians(rotation_degrees)
    c, s = cos(angle), sin(angle)
    # Inverse of T(dx,dy,dz) * Rz(rotation).
    return (
        (c, s, 0.0, -(c * dx + s * dy)),
        (-s, c, 0.0, s * dx - c * dy),
        (0.0, 0.0, 1.0, -dz),
        (0.0, 0.0, 0.0, 1.0),
    )


@lru_cache(maxsize=1)
def moving_plate_transform_evidence() -> list[dict[str, object]]:
    """Apply the frozen transform order and measure every actual moving half."""

    rows: list[dict[str, object]] = []
    for plate_index, ((role, half), source) in enumerate(moving_half_shapes().items(), start=1):
        rotated = deepcopy(source).rotate(Axis.Z, PRINT_TRANSFORM.rotation_deg)
        rotated_box = _aabb(rotated)
        center_x = (rotated_box[0] + rotated_box[3]) / 2.0
        center_y = (rotated_box[1] + rotated_box[4]) / 2.0
        dx = PRINT_TRANSFORM.bed_center_xy_mm[0] - center_x
        dy = PRINT_TRANSFORM.bed_center_xy_mm[1] - center_y
        dz = -rotated_box[2]
        placed = rotated.moved(Location((dx, dy, dz)))
        placed_box = _aabb(placed)
        raw_span = (placed_box[3] - placed_box[0], placed_box[4] - placed_box[1])
        brim_box = (
            placed_box[0] - PRINT_TRANSFORM.moving_brim_mm,
            placed_box[1] - PRINT_TRANSFORM.moving_brim_mm,
            placed_box[3] + PRINT_TRANSFORM.moving_brim_mm,
            placed_box[4] + PRINT_TRANSFORM.moving_brim_mm,
        )
        contained = (
            brim_box[0] >= PRINT_TRANSFORM.usable_bed_min_xy_mm[0]
            and brim_box[1] >= PRINT_TRANSFORM.usable_bed_min_xy_mm[1]
            and brim_box[2] <= PRINT_TRANSFORM.usable_bed_max_xy_mm[0]
            and brim_box[3] <= PRINT_TRANSFORM.usable_bed_max_xy_mm[1]
        )
        rows.append({
            "plate_index": plate_index,
            "role": role,
            "half": half,
            "source_label": source.label,
            "source_brep_sha256": _brep_digest(source),
            "placed_brep_sha256": _brep_digest(placed),
            "rotation_degrees": PRINT_TRANSFORM.rotation_deg,
            "translation_mm": (dx, dy, dz),
            "source_aabb_mm": _aabb(source),
            "rotated_aabb_mm": rotated_box,
            "placed_aabb_mm": placed_box,
            "raw_span_xy_mm": raw_span,
            "brim_mm_per_side": PRINT_TRANSFORM.moving_brim_mm,
            "packed_aabb_xy_mm": brim_box,
            "packed_span_xy_mm": (
                brim_box[2] - brim_box[0], brim_box[3] - brim_box[1]
            ),
            "z_floor_error_mm": abs(placed_box[2]),
            "center_error_xy_mm": (
                abs((placed_box[0] + placed_box[3]) / 2.0 - PRINT_TRANSFORM.bed_center_xy_mm[0]),
                abs((placed_box[1] + placed_box[4]) / 2.0 - PRINT_TRANSFORM.bed_center_xy_mm[1]),
            ),
            "contained_in_usable_bed": contained,
            "T_print_from_source": _matrix(PRINT_TRANSFORM.rotation_deg, dx, dy, dz),
            "T_source_from_print": _inverse_matrix(PRINT_TRANSFORM.rotation_deg, dx, dy, dz),
            "placed_shape": placed,
            # One actual moving body owns each plate, therefore the complete
            # within-plate pair set is empty and measured overlap is zero.
            "plate_pair_count": 0,
            "plate_occurrence_positive_overlap_mm3": 0.0,
        })
    return rows


def moving_plate_summary() -> dict[str, object]:
    rows = moving_plate_transform_evidence()
    return {
        "plate_count": len(rows),
        "maximum_raw_span_xy_mm": max(max(row["raw_span_xy_mm"]) for row in rows),
        "maximum_packed_span_xy_mm": max(max(row["packed_span_xy_mm"]) for row in rows),
        "maximum_z_floor_error_mm": max(row["z_floor_error_mm"] for row in rows),
        "maximum_center_error_mm": max(max(row["center_error_xy_mm"]) for row in rows),
        "maximum_plate_overlap_mm3": max(row["plate_occurrence_positive_overlap_mm3"] for row in rows),
        "all_contained": all(row["contained_in_usable_bed"] for row in rows),
    }


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _profile_rows() -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for family, rows in PROFILE_CHAINS.items():
        result[family] = []
        for path_text, expected in rows:
            path = Path(path_text)
            actual = sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                raise RuntimeError(f"frozen {family} profile hash drift: {path}")
            result[family].append({"path": path_text, "sha256": actual})
    return result


def _model_settings_config() -> bytes:
    objects = []
    plates = []
    for plate, _role, _half, name, object_uuid in ORCA_OBJECT_MAP:
        objects.append(
            f'  <object id="{plate}">\n'
            f'    <metadata key="name" value="{escape(name)}"/>\n'
            '    <metadata key="extruder" value="1"/>\n'
            f'    <metadata key="uuid" value="{object_uuid}"/>\n'
            f'    <part id="{100 + plate}" subtype="normal_part">\n'
            f'      <metadata key="name" value="{escape(name)}"/>\n'
            '      <metadata key="extruder" value="1"/>\n'
            '      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
            f'      <metadata key="source_object_id" value="{plate}"/>\n'
            '      <metadata key="source_volume_id" value="0"/>\n'
            '    </part>\n'
            '  </object>'
        )
        plates.append(
            '  <plate>\n'
            f'    <metadata key="plater_id" value="{plate}"/>\n'
            f'    <metadata key="plater_name" value="{escape(name)}"/>\n'
            '    <metadata key="locked" value="false"/>\n'
            '    <metadata key="filament_map_mode" value="Auto For Flush"/>\n'
            '    <metadata key="filament_maps" value="1"/>\n'
            '    <metadata key="filament_volume_maps" value="0"/>\n'
            '    <model_instance>\n'
            f'      <metadata key="object_id" value="{plate}"/>\n'
            f'      <metadata key="instance_id" value="{plate}"/>\n'
            f'      <metadata key="identify_id" value="{1000 + plate}"/>\n'
            '    </model_instance>\n'
            '  </plate>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<config>\n'
        + "\n".join(objects + plates)
        + "\n</config>"
    ).encode("utf-8")


def _project_metadata_members() -> dict[str, bytes]:
    profiles = _profile_rows()
    object_rows = [
        {
            "plate_index": plate,
            "object_id": plate,
            "instance_id": plate,
            "identify_id": 1000 + plate,
            "object_name": name,
            "object_uuid": object_uuid,
            "extruder": 1,
            "filament_slot": 1,
            "physical_tool": "T0",
        }
        for plate, _role, _half, name, object_uuid in ORCA_OBJECT_MAP
    ]
    project_settings = {
        "schema": "kage.i3.8.orca-project-settings.v1",
        "machine_profile": "Snapmaker U1 (0.4 nozzle)",
        "process_profile": "0.20 Standard @Snapmaker U1 (0.4 nozzle)",
        "filament_profile": "PETG",
        "filament_type": "PETG",
        "filament_vendor": "Generic",
        "filament_id": "GFG00",
        "filament_slot": 1,
        "physical_tool": "T0",
        "nozzle_diameter": ["0.4", "0.4", "0.4", "0.4"],
        "curr_bed_type": "3",
        "bed_type": "Textured PEI Plate",
        "brim_width": "3.5",
        "skirt_loops": "0",
        "enable_prime_tower": "0",
        "profile_chains": profiles,
    }
    model_settings = {
        "schema": "kage.i3.8.orca-object-map.v1",
        "objects": object_rows,
        "materials": [{
            "filament_slot": 1,
            "filament_identifier": "GFG00",
            "physical_tool": "T0",
        }],
    }
    plate_data = {
        "schema": "kage.i3.8.orca-plate-map.v1",
        "plates": [
            {
                "plate_index": row["plate_index"],
                "object_id": row["object_id"],
                "instance_id": row["instance_id"],
                "identify_id": row["identify_id"],
                "object_uuid": row["object_uuid"],
                "object_name": row["object_name"],
                "brim_width": "3.5",
                "skirt_loops": "0",
                "enable_prime_tower": "0",
            }
            for row in object_rows
        ],
    }
    return {
        "Metadata/project_settings.config": _json_bytes(project_settings),
        "Metadata/model_settings.config": _model_settings_config(),
        "Metadata/model_settings.json": _json_bytes(model_settings),
        "Metadata/plate_data.json": _json_bytes(plate_data),
    }


def _content_types_xml() -> bytes:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        '<Default Extension="json" ContentType="application/json"/>'
        '<Override PartName="/Metadata/project_settings.config" ContentType="application/json"/>'
        '<Override PartName="/Metadata/model_settings.config" ContentType="application/xml"/>'
        '</Types>'
    ).encode("utf-8")


def _fresh_orca_parser(path: Path) -> dict[str, object]:
    script = r'''
import json, sys, xml.etree.ElementTree as ET
from zipfile import ZipFile
import lib3mf
p=sys.argv[1]
with ZipFile(p) as z:
    root=ET.fromstring(z.read("Metadata/model_settings.config"))
    plates=[]
    for node in root.findall("plate"):
        m={x.attrib["key"]:x.attrib.get("value","") for x in node.findall("metadata")}
        i=node.find("model_instance")
        im={x.attrib["key"]:x.attrib.get("value","") for x in i.findall("metadata")}
        plates.append({**m,**im})
    project=json.loads(z.read("Metadata/project_settings.config"))
    model_map=json.loads(z.read("Metadata/model_settings.json"))
w=lib3mf.Wrapper(); model=w.CreateModel(); model.QueryReader("3mf").ReadFromFile(p)
build=model.GetBuildItems(); names=[]
while build.MoveNext(): names.append(build.GetCurrent().GetObjectResource().GetName())
print(json.dumps({"plates":plates,"project":project,"model_map":model_map,"build_names":names},sort_keys=True,separators=(",",":")))
'''
    completed = subprocess.run(
        [sys.executable, "-c", script, str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def _write_orca_source_project(path: Path) -> None:
    from p3_v3_phase3_i3_r1_real_joinery_export import _write_package

    transforms = {(row["role"], row["half"]): row for row in moving_plate_transform_evidence()}
    rows = []
    for plate, role, half, name, object_uuid in ORCA_OBJECT_MAP:
        rows.append({
            "label": name,
            "uuid": object_uuid,
            "shape": transforms[(role, half)]["placed_shape"],
            "kind": "moving_half",
        })
    with TemporaryDirectory(prefix=f".{NAMESPACE}-orca-base-", dir=path.parent) as temporary:
        base = Path(temporary) / "base.3mf"
        _write_package(base, rows)
        with ZipFile(base) as archive:
            members = {name: archive.read(name) for name in archive.namelist()}
        model_xml = members["3D/3dmodel.model"].decode("utf-8")
        model_xml, build_count = re.subn(
            r'(<build p:UUID=")[^"]+(">)',
            rf'\g<1>{ARTIFACT_CONTRACT.orca_build_uuid}\g<2>',
            model_xml,
            count=1,
        )
        if build_count != 1:
            raise RuntimeError("expected exactly one lib3mf build UUID")
        if len(ARTIFACT_CONTRACT.orca_build_item_uuids) != len(ORCA_OBJECT_MAP):
            raise RuntimeError("build-item UUID contract must match Orca object count")
        for object_id, build_uuid in enumerate(
            ARTIFACT_CONTRACT.orca_build_item_uuids,
            start=1,
        ):
            model_xml, item_count = re.subn(
                rf'(<item objectid="{object_id}" p:UUID=")[^"]+("/>)',
                rf'\g<1>{build_uuid}\g<2>',
                model_xml,
                count=1,
            )
            if item_count != 1:
                raise RuntimeError(
                    f"expected exactly one lib3mf build-item UUID for object {object_id}"
                )
        members["3D/3dmodel.model"] = model_xml.encode("utf-8")
        members["[Content_Types].xml"] = _content_types_xml()
        members.update(_project_metadata_members())
        with ZipFile(path, "w", ZIP_DEFLATED) as archive:
            for name in sorted(members):
                archive.writestr(name, members[name])
            if archive.testzip() is not None:
                raise RuntimeError("Orca source project CRC failure")


def orca_source_project_evidence(write: bool = False) -> dict[str, object]:
    """Build and independently parse a real six-plate Orca source project."""

    MODEL_ROOT.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f".{NAMESPACE}-orca-", dir=MODEL_ROOT.parent) as temporary:
        candidate = Path(temporary) / ORCA_SOURCE_PROJECT.name
        _write_orca_source_project(candidate)
        parsed = _fresh_orca_parser(candidate)
        digest = sha256(candidate.read_bytes()).hexdigest()
        size = candidate.stat().st_size
        plates = parsed["plates"]
        project = parsed["project"]
        object_map = parsed["model_map"]["objects"]
        unique_ids = all(
            len({int(row[key]) for row in plates}) == 6
            for key in ("object_id", "instance_id", "identify_id")
        )
        expected_names = [row[3] for row in ORCA_OBJECT_MAP]
        map_verified = (
            len(plates) == 6
            and len(object_map) == 6
            and parsed["build_names"] == expected_names
            and unique_ids
            and all(row["extruder"] == 1 and row["filament_slot"] == 1 and row["physical_tool"] == "T0" for row in object_map)
        )
        if not map_verified:
            raise RuntimeError("fresh Orca six-plate parser mapping failure")
        if write:
            MODEL_ROOT.mkdir(parents=True, exist_ok=True)
            staged = MODEL_ROOT / f".{ORCA_SOURCE_PROJECT.name}.new"
            staged.write_bytes(candidate.read_bytes())
            os.replace(staged, ORCA_SOURCE_PROJECT)
            if sha256(ORCA_SOURCE_PROJECT.read_bytes()).hexdigest() != digest:
                raise RuntimeError("atomic Orca source project publish mismatch")

    nozzles = project["nozzle_diameter"]
    profile_hashes_verified = all(
        sha256(Path(row["path"]).read_bytes()).hexdigest() == row["sha256"]
        for rows in project["profile_chains"].values()
        for row in rows
    )
    return {
        "path": str(ORCA_SOURCE_PROJECT) if write else None,
        "archive_sha256": digest,
        "archive_bytes": size,
        "plate_count": len(plates),
        "build_object_count": len(parsed["build_names"]),
        "unique_object_instance_identify_ids": unique_ids,
        "object_plate_mapping_verified": map_verified,
        "filament_identifier": project["filament_id"],
        "filament_slot": project["filament_slot"],
        "physical_tool": project["physical_tool"],
        "four_nozzle_mapping_verified": nozzles == ["0.4", "0.4", "0.4", "0.4"],
        "profile_hashes_verified": profile_hashes_verified,
        "machine_profile": project["machine_profile"],
        "process_profile": project["process_profile"],
        "bed_type": project["bed_type"],
        "moving_brim_mm": float(project["brim_width"]),
        "skirt_loops": int(project["skirt_loops"]),
        "prime_tower_enabled": bool(int(project["enable_prime_tower"])),
        "generated_in_new_temporary_directory": True,
        "fresh_process_parser": True,
        "atomic_publish": bool(write),
    }
