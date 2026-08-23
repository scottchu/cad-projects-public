"""Direct regression gates for the independent R2 rejection.

These gates intentionally exercise production solids and written slicer
artifacts.  They are not report-only assertions.
"""

from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZipFile

import pytest

import p3_v3_direct_gear_race_guidance_r2_export as e
import p3_v3_direct_gear_race_guidance_r2_geometry as g
from p3_v3_direct_gear_race_guidance_r2_spec import (
    P3_V3_DIRECT_GEAR_RACE_R2 as p,
)


MODEL_ROOT = p.model_root


def _volume(shape):
    if shape is None:
        return 0.0
    return sum(solid.volume for solid in shape.solids())


def _intersection_volume(left, right):
    return _volume(left.intersect(right))


def _aabb(shape, placement):
    box = shape.bounding_box()
    return (
        box.min.X + placement["tx"],
        box.max.X + placement["tx"],
        box.min.Y + placement["ty"],
        box.max.Y + placement["ty"],
        box.min.Z + placement["tz"],
        box.max.Z + placement["tz"],
    )


def _aabb_overlap(left, right, clearance=0.01):
    return not (
        left[1] <= right[0] + clearance
        or right[1] <= left[0] + clearance
        or left[3] <= right[2] + clearance
        or right[3] <= left[2] + clearance
        or left[5] <= right[4] + clearance
        or right[5] <= left[4] + clearance
    )


def test_truthful_per_plate_3mf_contract_has_no_fake_multiplate_bundle_or_overlap():
    production = g.production_occurrence_registry("assembled_nominal")
    placements = e._pack_records(production)
    assert len(production) == 94
    assert not (MODEL_ROOT / "print" / "p3_v3_r2_production_94.3mf").exists()
    plate_files = sorted((MODEL_ROOT / "production").glob("plate_*.3mf"))
    assert plate_files
    assert len(plate_files) == len({row["plate"] for row in placements.values()})

    by_name = {row["occurrence_name"]: row for row in production}
    for plate in sorted({row["plate"] for row in placements.values()}):
        names = [name for name, place in placements.items() if place["plate"] == plate]
        boxes = [_aabb(by_name[name]["shape"], placements[name]) for name in names]
        for box in boxes:
            assert 0.0 <= box[0] < box[1] <= 270.0
            assert 0.0 <= box[2] < box[3] <= 270.0
            assert 0.0 <= box[4] < box[5] <= 270.0
        for index, left in enumerate(boxes):
            for right in boxes[index + 1 :]:
                assert not _aabb_overlap(left, right)

        with ZipFile(plate_files[plate - 1]) as package:
            settings = json.loads(package.read("Metadata/model_settings.json"))
            assert settings["plate_count"] == 1
            assert settings["truthful_format"] == "single-physical-plate-3mf"
            assert "Metadata/model_settings.config" not in package.namelist()


@pytest.mark.parametrize("role,quadrant", [(r, q) for r in range(3) for q in range(4)])
def test_hall_and_balance_caps_have_actual_mating_carrier_pockets(role, quadrant):
    interface = g.make_cap_interface_solids(role, quadrant)
    assert interface["kind"] == ("hall" if quadrant == 0 else "balance")
    assert _volume(interface["raw_carrier"]) - _volume(interface["carrier"]) > 4.0
    assert _intersection_volume(interface["carrier"], interface["cap"]) == pytest.approx(0.0)
    assert interface["radial_clearance_mm"] >= 0.06
    assert interface["bottom_clearance_mm"] >= 0.04


@pytest.mark.parametrize("layer", ["rear", "front"])
@pytest.mark.parametrize("seam", range(4))
@pytest.mark.parametrize("lane", range(2))
def test_stationary_registration_keys_have_quadrant_mating_cuts(layer, seam, lane):
    interface = g.make_stationary_key_interface_solids(layer, seam, lane)
    assert _volume(interface["raw_pair"]) - _volume(interface["cut_pair"]) > 2.0
    assert _intersection_volume(interface["cut_pair"], interface["key"]) == pytest.approx(0.0)
    assert interface["radial_clearance_mm"] >= 0.08
    assert interface["tangential_clearance_mm"] >= 0.08


@pytest.mark.parametrize("role", range(3))
def test_spine_cassette_stop_use_material_revision_k_interfaces(role):
    evidence = g.make_revision_k_production_interface_solids(role)
    for name in (
        "spine_guide_slot",
        "spine_insert_bore",
        "spine_retainer_bore",
        "cassette_guide_key",
        "cassette_retainer_bore",
        "stop_reversal_key",
        "stop_tool_access",
    ):
        assert evidence[name]["material_delta_mm3"] > 0.25, name
    assert evidence["cassette_spine_overlap_mm3"] == pytest.approx(0.0)
    assert evidence["cassette_to_spine_clearance_mm"] >= 0.10
    assert evidence["tool_access_is_open"] is True


@pytest.mark.parametrize("role", range(3))
@pytest.mark.parametrize("seam", range(4))
def test_seam_plates_have_matching_carrier_recess_and_fastener_interfaces(role, seam):
    interface = g.make_seam_interface_solids(role, seam)
    assert _volume(interface["raw_pair"]) - _volume(interface["cut_pair"]) > 8.0
    assert _intersection_volume(interface["cut_pair"], interface["plate"]) == pytest.approx(0.0)
    assert interface["recess_radial_clearance_mm"] >= 0.08
    assert interface["recess_tangential_clearance_mm"] >= 0.08
    assert interface["fastener_hole_count"] == 2
    assert interface["fastener_paths_open"] is True


def test_coupon_reference_contract_uses_purchased_hardware_not_arbitrary_printed_substitutes():
    contract = e.coupon_reference_contract()
    assert contract["reference_kind"] == "purchased-hardware"
    assert set(contract["hardware_categories"]) >= {
        "motor_shaft_reference",
        "output_shaft_reference",
        "shaft_bearing_reference",
        "shaft_retainer_reference",
        "motor_mount_fastener_reference",
    }
    assert contract["arbitrary_printed_reference_count"] == 0


def test_truthful_physical_plates_match_watertight_cube_orca_startup_control():
    manifest_path = MODEL_ROOT / "production_94_manifest.json"
    assert manifest_path.is_file()
    manifest = json.loads(manifest_path.read_text())
    control = e._orca_startup_diagnostic_control()
    assert control["returnCode"] == 0
    assert control["manifoldYesCount"] == 1
    assert control["onePartCount"] == 1
    assert control["errorPayloads"] in (
        [],
        [e.ORCA_EMPTY_EXCLUDE_STARTUP_DIAGNOSTIC],
    )
    for plate in manifest["plates"]:
        plate_path = MODEL_ROOT / plate["path"]
        facts = e._slicer_reload_facts(
            plate_path,
            expected_object_names=plate["occurrences"],
        )
        assert facts["returnCode"] == 0
        assert facts["manifoldYesCount"] == len(plate["occurrences"])
        assert facts["onePartCount"] == len(plate["occurrences"])
        assert facts["packagedObjectNames"] == plate["occurrences"]
        assert facts["packageContract"]["resourceObjectNames"] == plate["occurrences"]
        assert facts["packageContract"]["buildObjectIds"] == facts["packageContract"]["resourceObjectIds"]
        assert facts["errorPayloads"] == control["errorPayloads"]
        assert facts["startupDiagnosticMatchesCubeControl"] is True
