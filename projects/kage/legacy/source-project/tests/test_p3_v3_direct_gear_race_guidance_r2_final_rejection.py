"""Direct regression gates for the final Revision-K R2 rejection.

This module deliberately specifies missing production APIs.  Every interface
API must return the actual host/tool/reference BREPs used by production; a
summary-only witness dictionary is insufficient.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from math import pi, radians
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from build123d import export_brep, import_step
import pytest

import p3_v3_direct_gear_race_guidance_r2_export as e
import p3_v3_direct_gear_race_guidance_r2_geometry as g
from p3_v3_direct_gear_race_guidance_r2_spec import P3_V3_DIRECT_GEAR_RACE_R2 as p


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_r2"
PRINT_ROOT = MODEL_ROOT / "production"
PLATE_MANIFEST = MODEL_ROOT / "production_94_manifest.json"
ORCA = Path("/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca")
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}


def _volume(shape) -> float:
    return sum(s.volume for s in shape.solids()) if shape else 0.0


def _iv(left, right) -> float:
    return _volume(left.intersect(right))


def _raw_brep_digest(shape) -> str:
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(suffix=".brep") as temporary:
        export_brep(shape, temporary.name)
        return sha256(Path(temporary.name).read_bytes()).hexdigest()


def _model_rows(path: Path):
    with ZipFile(path) as package:
        root = ET.fromstring(package.read("3D/3dmodel.model"))
    objects = {
        node.attrib["id"]: node.attrib.get("name", "")
        for node in root.findall(".//m:resources/m:object", NS)
    }
    return [objects[item.attrib["objectid"]] for item in root.findall(".//m:build/m:item", NS)]


def test_true_straight_bevel_has_720_sample_conjugate_coverage_and_bisected_backlash():
    assert hasattr(g, "straight_bevel_phase_evidence")
    for role in range(3):
        evidence = g.straight_bevel_phase_evidence(
            role, samples_per_tooth=720, bisection_iterations=24
        )
        assert evidence["samples_per_tooth"] == 720
        assert evidence["bisection_iterations"] >= 20
        assert evidence["tooth_pitch_deg"] == pytest.approx(360.0 / 16.0)
        assert len(evidence["conjugate_trace"]) == 720
        assert evidence["continuous_engagement"] is True
        assert evidence["minimum_concurrent_tooth_pairs"] >= 1
        assert 0.0 <= evidence["minimum_contact_gap_mm"]
        assert evidence["maximum_contact_gap_mm"] <= 0.25
        assert evidence["boundary_count"] == 2
        assert evidence["bisection_residual_deg"] <= 0.001
        assert 0.10 <= evidence["backlash_mm_at_pitch_line"] <= 0.25
        assert evidence["backlash_mm_at_pitch_line"] == pytest.approx(
            radians(evidence["lost_angle_deg"]) * 8.0, abs=0.002
        )
        for name in ("input_gear", "output_gear"):
            shape = evidence[name]
            assert shape.is_valid and _volume(shape) > 0
            assert len(shape.faces()) >= 48 and len(shape.edges()) >= 96
            box = shape.bounding_box()
            assert max(box.size.X, box.size.Y, box.size.Z) - min(
                box.size.X, box.size.Y, box.size.Z
            ) >= 2.0, f"{name} is not a tapered straight-bevel solid"


def test_carrier_caps_seams_and_stationary_keys_are_real_mating_topology():
    for role in range(3):
        for quadrant in range(4):
            interface = g.make_cap_interface_solids(role, quadrant)
            assert _volume(interface["raw_carrier"]) > _volume(interface["carrier"])
            assert _iv(interface["carrier"], interface["cap"]) <= 1e-7
            assert _iv(interface["pocket"], interface["cap"]) > 0
        for seam in range(4):
            interface = g.make_seam_interface_solids(role, seam)
            assert _volume(interface["raw_pair"]) > _volume(interface["cut_pair"])
            assert _iv(interface["cut_pair"], interface["plate"]) <= 1e-7
            assert interface["fastener_hole_count"] == 2
            assert all(_iv(interface["cut_pair"], tool) <= 1e-7 for tool in interface["fastener_tools"])
    for layer in ("rear", "front"):
        for seam in range(4):
            for lane in range(2):
                interface = g.make_stationary_key_interface_solids(layer, seam, lane)
                assert _volume(interface["raw_pair"]) > _volume(interface["cut_pair"])
                assert _iv(interface["cut_pair"], interface["key"]) <= 1e-7
                assert _iv(interface["pocket"], interface["key"]) > 0


@pytest.mark.parametrize("tower", range(2))
def test_i1_fixed_axle_faces_bores_endplay_and_tools_are_actual_solids(tower):
    assert hasattr(g, "fixed_axle_interface_solids")
    interface = g.fixed_axle_interface_solids(tower)
    for key in (
        "leaf", "raw_leaf", "lower_seat_tool", "upper_bridge", "raw_upper_bridge",
        "upper_bore_tool", "axle", "thrust_washer", "split_collar",
        "collar_tool_path", "withdrawal_tool_path",
    ):
        assert _volume(interface[key]) > 0, key
    assert _volume(interface["raw_leaf"]) - _volume(interface["leaf"]) > 20
    assert _iv(interface["leaf"], interface["lower_seat_tool"]) <= 1e-7
    assert _iv(interface["upper_bridge"], interface["upper_bore_tool"]) <= 1e-7
    assert interface["lower_seat_diameter_mm"] == pytest.approx(4.05, abs=0.01)
    assert interface["lower_seat_depth_mm"] == pytest.approx(3.00, abs=0.01)
    assert interface["blind_bottom_wall_mm"] >= 1.50
    assert interface["upper_bore_diameter_mm"] == pytest.approx(4.06, abs=0.01)
    assert 0.05 <= interface["face_derived_endplay_mm"] <= 0.15
    assert 0.80 <= interface["face_derived_axle_extension_mm"] <= 0.90
    assert _iv(interface["assembled_without_axle"], interface["collar_tool_path"]) <= 1e-7
    assert _iv(interface["assembled_without_axle"], interface["withdrawal_tool_path"]) <= 1e-7


@pytest.mark.parametrize("role", range(3))
def test_i2_cassette_pin_stack_flat_retention_and_tools_are_actual_solids(role):
    assert hasattr(g, "cassette_pin_interface_solids")
    interface = g.cassette_pin_interface_solids(role)
    for key in (
        "cassette", "raw_cassette", "pin_bore_tool", "pin", "pin_flat_tool",
        "roller", "retaining_washer", "m2_screw", "m3_set_screw",
        "m2_tool_path", "m3_tool_path",
    ):
        assert _volume(interface[key]) > 0, key
    assert len(interface["thrust_washers"]) == 2
    assert interface["pin_diameter_mm"] == pytest.approx(3.99, abs=0.01)
    assert interface["pin_length_mm"] == pytest.approx(7.70, abs=0.01)
    assert interface["blind_insertion_mm"] == pytest.approx(4.25, abs=0.01)
    assert interface["pin_bore_diameter_mm"] == pytest.approx(4.04, abs=0.01)
    assert interface["blind_bottom_wall_mm"] >= 1.50
    assert interface["roller_stack_mm"] == pytest.approx(3.30, abs=0.01)
    assert interface["axial_endplay_mm"] == pytest.approx(0.15, abs=0.01)
    assert interface["pin_flat_z_bounds_mm"] == pytest.approx((1.50, 3.50), abs=0.01)
    assert interface["pin_flat_depth_mm"] == pytest.approx(0.40, abs=0.01)
    assert interface["flat_normal_error_deg"] <= 2.0
    assert interface["washer_capture_overlap_mm"] >= 0.95
    assert interface["screw_head_bearing_overlap_mm"] >= 0.66
    host = interface["assembled_without_tools"]
    assert _iv(host, interface["m2_tool_path"]) <= 1e-7
    assert _iv(host, interface["m3_tool_path"]) <= 1e-7


@pytest.mark.parametrize("role", range(3))
def test_i3_spine_stop_adjuster_and_heat_tool_paths_are_actual_solids(role):
    assert hasattr(g, "spine_stop_interface_solids")
    interface = g.spine_stop_interface_solids(role)
    for key in (
        "spine", "cassette", "stop_plate", "adjuster_insert", "adjuster_bore_tool",
        "adjuster_screw_path_max_material", "heat_tool_path", "adjustment_tool_path",
        "stop_window_tool", "mounting_driver_paths",
    ):
        value = interface[key]
        if isinstance(value, (tuple, list)):
            assert value and all(_volume(shape) > 0 for shape in value)
        else:
            assert _volume(value) > 0, key
    assert interface["spine_envelope_mm"] == pytest.approx((24.0, 20.0, 21.7), abs=0.05)
    assert interface["adjuster_through_bore_diameter_mm"] == pytest.approx(3.50, abs=0.01)
    assert interface["adjuster_clear_bore_length_mm"] == pytest.approx(3.00, abs=0.01)
    assert interface["insert_radial_ligament_mm"] >= 1.20
    assert interface["max_bore_radial_ligament_mm"] >= 1.50
    assert interface["thread_engagement_min_mm"] >= 3.00
    assert interface["stop_pin_projection_mm"] == pytest.approx(4.00, abs=0.02)
    assert interface["stop_pin_backing_wall_mm"] >= 1.50
    assert interface["stop_window_transverse_clearance_per_side_mm"] >= 0.10
    assert interface["reversed_plate_interference_mm3"] > 0
    assert _iv(interface["bare_spine"], interface["heat_tool_path"]) <= 1e-7
    assert _iv(interface["assembled_without_adjuster"], interface["adjuster_screw_path_max_material"]) <= 1e-7


def test_service_states_remove_exactly_powered_keys_and_do_not_mutate_other_breps():
    nominal = {row["occurrence_name"]: row for row in g.production_occurrence_registry("assembled_nominal")}
    assert len(nominal) == 94
    powered_keys = {name for name in nominal if "powered_window_key" in name}
    assert len(powered_keys) == 3
    for state in ("service_min_UNSAFE_TO_POWER", "service_max_UNSAFE_TO_POWER"):
        service = {row["occurrence_name"]: row for row in g.production_occurrence_registry(state)}
        assert len(service) == 91
        assert set(nominal) - set(service) == powered_keys
        for name in sorted(service):
            assert service[name]["category"] == nominal[name]["category"]
            if service[name]["category"] not in {"motor_yoke", "output_pinion", "miter_gear"}:
                assert _raw_brep_digest(service[name]["shape"]) == _raw_brep_digest(nominal[name]["shape"])


def test_real_single_plate_u1_files_flatten_to_exactly_94_unique_occurrences():
    assert PLATE_MANIFEST.is_file()
    manifest = json.loads(PLATE_MANIFEST.read_text())
    plates = manifest["plates"]
    assert len(plates) >= 2
    flattened = []
    for plate in plates:
        path = MODEL_ROOT / plate["path"]
        assert path.parent == PRINT_ROOT and path.is_file()
        rows = _model_rows(path)
        assert rows == plate["occurrences"]
        assert plate["physicalPlateCount"] == 1
        assert plate["buildVolumeMm"] == [260, 260, 260]
        assert plate["minimumBedMarginMm"] >= 5.0
        assert plate["outOfBedCount"] == 0
        assert plate["overlapPairCount"] == 0
        flattened.extend(rows)
    assert len(flattened) == 94
    assert len(set(flattened)) == 94
    expected = {row["occurrence_name"] for row in g.production_occurrence_registry("assembled_nominal")}
    assert set(flattened) == expected


def test_each_physical_plate_loads_in_orca_with_zero_error_stderr():
    assert ORCA.is_file() and PLATE_MANIFEST.is_file()
    manifest = json.loads(PLATE_MANIFEST.read_text())
    for plate in manifest["plates"]:
        path = MODEL_ROOT / plate["path"]
        result = subprocess.run(
            [str(ORCA), "--info", str(path)], capture_output=True, text=True,
            timeout=180, check=False,
        )
        assert result.returncode == 0
        assert "manifold = yes" in result.stdout
        assert not re.search(r"(^|\n).*\b(error|failed|repair)\b", result.stderr, re.I)
        assert plate["orca"]["returnCode"] == 0
        assert plate["orca"]["stderrSha256"] == sha256(result.stderr.encode()).hexdigest()


def test_complete_purchased_hardware_registry_is_nonprinting_unique_and_solid():
    assert hasattr(g, "purchased_hardware_registry")
    rows = list(g.purchased_hardware_registry("assembled_nominal"))
    categories = Counter(row["category"] for row in rows)
    required = {
        "fixed_axle_reference", "cassette_pin_reference", "pom_roller_reference",
        "thrust_washer_reference", "cassette_m2_retainer_screw_reference",
        "cassette_retaining_washer_reference", "split_collar_reference",
        "compression_spring_reference", "heat_set_insert_reference",
        "adjuster_screw_reference", "motor_reference", "shaft_bearing_reference",
        "motor_mount_fastener_reference", "hall_magnet_reference",
    }
    assert required <= set(categories)
    assert categories["fixed_axle_reference"] == 2
    assert categories["cassette_pin_reference"] == 3
    assert categories["pom_roller_reference"] == 9
    assert categories["compression_spring_reference"] == 3
    assert categories["motor_reference"] == 3
    assert categories["shaft_bearing_reference"] == 6
    assert len({row["occurrence_name"] for row in rows}) == len(rows)
    assert all(row["printable"] is False and _volume(row["shape"]) > 0 for row in rows)


def test_coupon_and_ladders_have_exact_source_geometry_values_and_reference_flags():
    manifest = json.loads((MODEL_ROOT / "coupons" / "manifest.json").read_text())
    station = manifest["completeStation"]
    assert station["printingOccurrenceCount"] == 5
    expected_refs = {
        "guide_shoulder_screw": 6, "spring": 3, "adjuster_screw": 3,
        "adjuster_insert": 3, "adjuster_seat_washer": 3, "cassette_pin": 3,
        "pom_roller": 3, "thrust_washer": 6, "m2_retainer_screw": 3,
        "retaining_washer": 3, "pin_retention_screw": 3,
        "pin_retention_insert": 3, "stop_plate_mount_stack": 2,
        "spine_mount_stack": 2,
    }
    assert station["referenceCategoryCounts"] == expected_refs
    assert station["orientedBoundsMm"][0] <= 110.0
    assert station["orientedBoundsMm"][1] <= 85.0
    assert station["orientedBoundsMm"][2] <= 24.0
    assert manifest["stationLadder"]["families"] == {
        "cassette_pin_bore": [4.00, 4.04, 4.08],
        "guide_capsule_width": [3.35, 3.40, 3.45],
        "stop_window_width": [3.15, 3.20, 3.25],
        "spring_seat_diameter": [4.15, 4.20, 4.25],
        "adjuster_insert_pilot": [3.90, 4.00, 4.10],
        "stop_key_clearance_per_side": [0.15, 0.20, 0.25],
    }
    assert manifest["fixedLadder"]["keyedShimPairCount"] == 9
    assert manifest["fixedLadder"]["pairedBoreCells"] == [
        [4.02, 4.05], [4.05, 4.06], [4.08, 4.10]
    ]
    assert all(row["sourceBrepDigest"] for row in manifest["allObjects"])
    assert all(row["printing"] is False for row in manifest["allObjects"] if row["kind"] == "reference")


def test_manifests_flatten_counts_hash_every_artifact_and_match_written_steps():
    root_manifest = json.loads((MODEL_ROOT / "manifest.json").read_text())
    plate_manifest = json.loads(PLATE_MANIFEST.read_text())
    assert plate_manifest["flattenedOccurrenceCount"] == 94
    assert plate_manifest["flattenedUniqueOccurrenceCount"] == 94
    artifact_hashes = root_manifest["artifactSha256"]
    assert artifact_hashes
    for relative, digest in artifact_hashes.items():
        path = MODEL_ROOT / relative
        assert path.is_file()
        assert sha256(path.read_bytes()).hexdigest() == digest
    for state, parity in root_manifest["stateParity"].items():
        path = MODEL_ROOT / parity["path"]
        written = import_step(str(path))
        by_name = {child.label: child for child in written.children}
        rows = parity["occurrences"]
        assert set(by_name) == {row["name"] for row in rows}
        assert parity["writtenOccurrenceCount"] == len(by_name)
        for row in rows:
            assert row["brepDigest"] == _raw_brep_digest(by_name[row["name"]])

