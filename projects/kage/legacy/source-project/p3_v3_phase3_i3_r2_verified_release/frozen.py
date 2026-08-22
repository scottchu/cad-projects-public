"""Read-only frozen-input and predecessor-fact audit for R2."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import lib3mf

from .artifact_consumer import ArtifactRejected, pin_current_release
from .registry import registry_comparison

from .spec import (
    FROZEN_HASHES,
    FROZEN_STEP_PATH,
    I3_12_PATH,
    I3_SPEC_PATH,
    R1_ARTIFACT_ROOT,
    R1_HANDOFF_PATH,
    R2_HANDOFF_PATH,
)


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def frozen_hash_evidence() -> dict[str, object]:
    paths = {
        "r2_handoff": R2_HANDOFF_PATH,
        "i3_spec": I3_SPEC_PATH,
        "i3_12": I3_12_PATH,
        "r1_handoff": R1_HANDOFF_PATH,
        "frozen_step": FROZEN_STEP_PATH,
    }
    actual = {name: file_sha256(path) for name, path in paths.items()}
    return {
        "paths": {name: str(path) for name, path in paths.items()},
        "expected": FROZEN_HASHES,
        "actual": actual,
        "all_match": actual == FROZEN_HASHES,
    }


def _lib3mf_counts(path: Path) -> dict[str, int]:
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    model.QueryReader("3mf").ReadFromFile(str(path))
    object_count = 0
    objects = model.GetObjects()
    while objects.MoveNext():
        object_count += 1
    build_item_count = 0
    build_items = model.GetBuildItems()
    while build_items.MoveNext():
        build_item_count += 1
    return {"objects": object_count, "build_items": build_item_count}


EXPECTED_ORCA_OBJECTS = (
    (1, "hour_I3_half_A_130T_beta15p230769", "fa6a01e8-5e16-50e5-a679-572d6f97eebb", 1, 1, 1001),
    (2, "hour_I3_half_B_130T_beta195p230769", "8647d48e-3be7-5bcc-96ce-f99edd27d2f1", 2, 2, 1002),
    (3, "minute_I3_half_A_130T_beta15p230769", "cd27fc98-3338-5c4a-930a-a5f3641c1250", 3, 3, 1003),
    (4, "minute_I3_half_B_130T_beta195p230769", "cf2d9c10-7eb8-51f4-9acb-70e15bda166e", 4, 4, 1004),
    (5, "second_I3_half_A_130T_beta15p230769", "e2b2957a-7f3c-57ac-a071-f4ad0ed15dd5", 5, 5, 1005),
    (6, "second_I3_half_B_130T_beta195p230769", "1d950c12-033f-5037-8c6d-7b006ed0746a", 6, 6, 1006),
)

EXPECTED_PROFILE_HASHES = {
    "filament": (
        "d7a7c0e5911779e70836bf53c29fd736c8702ff45ad46880690c2f092c5433df",
        "9887427bf889b4364b49b401aa69a1f874ff484e530a09a54be5e77a0bd5ad9b",
        "e46b5aac9d983eff69a18f6f2453fc2e5a28f1d581370195ef01c9d0d7032e57",
        "33f78fc9a87c83976a635d23c0303797bc9468c8a1c27ab2d1ef769ea66ac2d1",
        "24e4920907489bfdeb250ba749b005c97571d7a547416989af10df502896e99d",
    ),
    "machine": (
        "545e4456b78cc58e701ed257e4024b0ed9e2461cccc1046e6f901ce3c020ee0d",
        "ff0724000b1436fcc3d77ffa74bb623a9b322474fc20c8a8d5a26ee164077046",
        "b2ee2d2c31a26ddee7b0c8bd84c58934d9c01e84e1b8f7ae45e14acfd1f7b52a",
        "78dd750211347543368a8a0f136441ef7e23b3a4a09a9e33a370c91dbda273b9",
    ),
    "process": (
        "3342dbe3e995b66ab5700245c676f446a88d35f56498b074ab6fe14039d67763",
        "2df28dc2474b6aeb77d5416043b3a67e54ff7ea1cdf5a5daa9e97db7e5b034a6",
        "43fba9fe359864b265ffa8682cf404c2b935d12164ffe3d0048e5dcb0691db74",
        "66e9e51c4bd04cbbec49fa1a3a043bc3c6e329396c2b38a18db5a66b6e72b4e2",
    ),
}


def _metadata(node: ET.Element) -> dict[str, str]:
    return {
        str(child.attrib["key"]): str(child.attrib["value"])
        for child in node.findall("metadata")
    }


def _orca_archive_facts(path: Path) -> dict[str, object]:
    with ZipFile(path) as archive:
        plate_data = json.loads(archive.read("Metadata/plate_data.json"))
        model_data = json.loads(archive.read("Metadata/model_settings.json"))
        project = json.loads(archive.read("Metadata/project_settings.config"))
        xml_root = ET.fromstring(archive.read("Metadata/model_settings.config"))
    plate_rows = tuple(
        (
            int(row["plate_index"]), str(row["object_name"]), str(row["object_uuid"]),
            int(row["object_id"]), int(row["instance_id"]), int(row["identify_id"]),
        )
        for row in plate_data["plates"]
    )
    object_rows = tuple(
        (
            int(row["plate_index"]), str(row["object_name"]), str(row["object_uuid"]),
            int(row["object_id"]), int(row["instance_id"]), int(row["identify_id"]),
        )
        for row in model_data["objects"]
    )
    xml_objects = tuple(
        (
            int(node.attrib["id"]), _metadata(node)["name"], _metadata(node)["uuid"],
            int(_metadata(node)["extruder"]),
        )
        for node in xml_root.findall("object")
    )
    xml_plates = tuple(
        (
            int(_metadata(node)["plater_id"]), _metadata(node)["plater_name"],
            int(_metadata(node.find("model_instance"))["object_id"]),
            int(_metadata(node.find("model_instance"))["instance_id"]),
            int(_metadata(node.find("model_instance"))["identify_id"]),
        )
        for node in xml_root.findall("plate")
    )
    profile_hashes = {
        name: tuple(str(row["sha256"]) for row in project["profile_chains"][name])
        for name in ("filament", "machine", "process")
    }
    settings = {
        "object_extruders": tuple(int(row["extruder"]) for row in model_data["objects"]),
        "object_filament_slots": tuple(int(row["filament_slot"]) for row in model_data["objects"]),
        "object_physical_tools": tuple(str(row["physical_tool"]) for row in model_data["objects"]),
        "material": model_data["materials"],
        "bed_type": project["bed_type"],
        "curr_bed_type": project["curr_bed_type"],
        "brim_width": project["brim_width"],
        "skirt_loops": project["skirt_loops"],
        "enable_prime_tower": project["enable_prime_tower"],
        "filament_id": project["filament_id"],
        "filament_slot": project["filament_slot"],
        "physical_tool": project["physical_tool"],
        "machine_profile": project["machine_profile"],
        "process_profile": project["process_profile"],
        "nozzle_diameter": tuple(project["nozzle_diameter"]),
        "profile_hashes": profile_hashes,
    }
    return {
        "plate_rows": plate_rows,
        "object_rows": object_rows,
        "xml_objects": xml_objects,
        "xml_plates": xml_plates,
        "plate_settings": tuple(
            (str(row["brim_width"]), str(row["skirt_loops"]), str(row["enable_prime_tower"]))
            for row in plate_data["plates"]
        ),
        "settings": settings,
    }


def accepted_r1_fact_evidence() -> dict[str, object]:
    parity = json.loads((R1_ARTIFACT_ROOT / "step_parity_report.json").read_text())
    regeneration = json.loads(
        (R1_ARTIFACT_ROOT / "fresh_atomic_regeneration_report.json").read_text()
    )
    printable = _lib3mf_counts(R1_ARTIFACT_ROOT / "print_components.3mf")
    orca_path = R1_ARTIFACT_ROOT / "i3_8_six_moving_halves_source.3mf"
    orca = _lib3mf_counts(orca_path)
    archive = _orca_archive_facts(orca_path)
    registry = registry_comparison()
    measured = {
        "logical_occurrence_registry": parity["source_registry_count"],
        "protected_exact": parity["protected_occurrence_count"],
        "authorized_replacements": registry["predecessor_partition_counts"]["authorized_replacement"],
        "new_authorized": registry["predecessor_partition_counts"]["new_authorized"],
        "nominal_imported_step_occurrences": parity["nominal_imported_occurrence_count"],
        "exploded_imported_step_occurrences": parity["exploded_imported_occurrence_count"],
        "nominal_topology_failures": len(parity["nominal_topology_failures"]),
        "exploded_topology_failures": len(parity["exploded_topology_failures"]),
        "nominal_bounds_mm": parity["nominal_bounds_mm"],
        "exploded_bounds_mm": parity["exploded_bounds_mm"],
        "disassembled_objects": printable["objects"],
        "disassembled_build_items": printable["build_items"],
        "orca_objects": orca["objects"],
        "orca_build_items": orca["build_items"],
        "orca_plates": len(archive["plate_rows"]),
        "complete_step_runs": regeneration["complete_fresh_step_run_count"],
        "protected_drift": parity["protected_drift"],
    }
    expected = {
        "logical_occurrence_registry": 275,
        "protected_exact": 131,
        "authorized_replacements": 18,
        "new_authorized": 126,
        "nominal_imported_step_occurrences": 275,
        "exploded_imported_step_occurrences": 275,
        "nominal_topology_failures": 0,
        "exploded_topology_failures": 0,
        "nominal_bounds_mm": [-150, -150, -32.5, 150, 150, 24.2514],
        "exploded_bounds_mm": [-150, -150, -32.5, 150, 150, 78.8],
        "disassembled_objects": 34,
        "disassembled_build_items": 34,
        "orca_objects": 6,
        "orca_build_items": 6,
        "orca_plates": 6,
        "complete_step_runs": 1,
        "protected_drift": [],
    }
    expected_xml_objects = tuple((row[0], row[1], row[2], 1) for row in EXPECTED_ORCA_OBJECTS)
    expected_xml_plates = tuple((row[0], row[1], row[3], row[4], row[5]) for row in EXPECTED_ORCA_OBJECTS)
    mapping_checks = {
        "plate_json_exact": archive["plate_rows"] == EXPECTED_ORCA_OBJECTS,
        "object_json_exact": archive["object_rows"] == EXPECTED_ORCA_OBJECTS,
        "xml_objects_exact": archive["xml_objects"] == expected_xml_objects,
        "xml_plates_exact": archive["xml_plates"] == expected_xml_plates,
        "all_objects_extruder_1": archive["settings"]["object_extruders"] == (1,) * 6,
        "all_objects_filament_slot_1": archive["settings"]["object_filament_slots"] == (1,) * 6,
        "all_objects_tool_t0": archive["settings"]["object_physical_tools"] == ("T0",) * 6,
        "six_plate_process_settings": archive["plate_settings"] == (("3.5", "0", "0"),) * 6,
        "material_exact": archive["settings"]["material"] == [{"filament_identifier": "GFG00", "filament_slot": 1, "physical_tool": "T0"}],
        "u1_machine_exact": archive["settings"]["machine_profile"] == "Snapmaker U1 (0.4 nozzle)",
        "u1_four_nozzles": archive["settings"]["nozzle_diameter"] == ("0.4",) * 4,
        "bed_exact": (archive["settings"]["bed_type"], archive["settings"]["curr_bed_type"]) == ("Textured PEI Plate", "3"),
        "project_process_exact": (
            archive["settings"]["brim_width"], archive["settings"]["skirt_loops"],
            archive["settings"]["enable_prime_tower"], archive["settings"]["filament_id"],
            archive["settings"]["filament_slot"], archive["settings"]["physical_tool"],
            archive["settings"]["process_profile"],
        ) == ("3.5", "0", "0", "GFG00", 1, "T0", "0.20 Standard @Snapmaker U1 (0.4 nozzle)"),
        "profile_chains_exact": archive["settings"]["profile_hashes"] == EXPECTED_PROFILE_HASHES,
    }
    return {
        "measured": measured,
        "expected": expected,
        "archive": archive,
        "registry": registry,
        "mapping_checks": mapping_checks,
        "source_provenance": [
            "R1 step_parity_report.json",
            "R1 fresh_atomic_regeneration_report.json",
            "R1 lib3mf print_components.3mf",
            "R1 lib3mf i3_8_six_moving_halves_source.3mf",
            "R1 archive plate_data.json",
            "R1 archive model_settings.json",
            "R1 archive model_settings.config XML",
            "R1 archive project_settings.config",
            "R1 candidate_occurrences registry",
        ],
        "all_match": measured == expected and all(mapping_checks.values()) and registry["passed"],
    }


def artifact_rejection_evidence() -> dict[str, object]:
    """Exercise the production consumer against missing and stale releases."""

    cases = []
    with TemporaryDirectory(prefix="kage-r2-a-") as temporary:
        root = Path(temporary)
        (root / "assembled_nominal.step").write_bytes(b"forbidden root fallback")
        for name in ("missing_current_with_mutable_root", "stale_current"):
            if name == "stale_current":
                (root / "releases").mkdir(exist_ok=True)
                (root / "current").symlink_to("releases/" + "a" * 64)
            try:
                pin_current_release(root)
            except ArtifactRejected as exc:
                cases.append({"case": name, "rejection_code": exc.code})
            else:
                cases.append({"case": name, "rejection_code": None})
            if (root / "current").is_symlink():
                (root / "current").unlink()
    expected = [
        {"case": "missing_current_with_mutable_root", "rejection_code": "R2_ARTIFACT_CURRENT_MISSING"},
        {"case": "stale_current", "rejection_code": "R2_ARTIFACT_CURRENT_STALE"},
    ]
    return {
        "consumer": "artifact_consumer.pin_current_release",
        "readlink_count_per_attempt": 1,
        "cases": cases,
        "expected": expected,
        "passed": cases == expected,
    }
