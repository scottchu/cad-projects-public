"""RED contract for accepted KAGE Phase-3 I3.2 through I3.12 amendments.

This file intentionally precedes the isolated production namespace.  It pins
every immutable design document and the Phase-2A source artifact, then demands
the finite registry, actual-solid, package, semantic-3MF, and phase-separation
evidence closed by I3.12.  Final slicing/G-code remains an explicit external
PENDING gate and is not a CAD-suite failure.
"""

from __future__ import annotations

from hashlib import sha256
import importlib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MODEL_ROOT = ROOT / "models" / "p3_v3_phase3_i3_u1_segmentation_joinery"
FROZEN_STEP = (
    ROOT
    / "models"
    / "p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention"
    / "p3_v3_r1_i1_fixed_tower_retention_assembled.step"
)

SPEC_MODULE = "p3_v3_phase3_i3_u1_segmentation_joinery_spec"
GEOMETRY_MODULE = "p3_v3_phase3_i3_u1_segmentation_joinery_geometry"
PARITY_MODULE = "p3_v3_phase3_i3_u1_segmentation_joinery_parity"
EXPORT_MODULE = "p3_v3_phase3_i3_u1_segmentation_joinery_export"

FROZEN_STEP_SHA256 = "8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724"
AMENDMENT_HASHES = {
    "i3_1": (
        "p3-v3-phase3-i3-u1-segmentation-joinery-accepted-spec.md",
        "abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77",
    ),
    "i3_2": (
        "p3-v3-phase3-i3-2-design-amendment.md",
        "9998612e8b9d5f6865b714dcd47199cf33afde787840350f261256c404d3bdc3",
    ),
    "i3_3": (
        "p3-v3-phase3-i3-3-design-amendment.md",
        "4d29f72ba299ffe35ebbfa92349323681f4a3f6c76ac3a11a74a41462bc62691",
    ),
    "i3_4": (
        "p3-v3-phase3-i3-4-design-amendment.md",
        "c6fb12ceab347b258b4f3be65b61d32f178bbf3075cf68869d5d87e9d47636e1",
    ),
    "i3_5": (
        "p3-v3-phase3-i3-5-design-amendment.md",
        "08ab0d28e84036a3bcf17e74e9d3ab18d22c376f8a9f71f4cd1fd6494ede35d6",
    ),
    "i3_6": (
        "p3-v3-phase3-i3-6-design-amendment.md",
        "326f9dbd21fa04885447c8080390a70187176f90020f0ebfee212255bc4154f9",
    ),
    "i3_7": (
        "p3-v3-phase3-i3-7-design-amendment.md",
        "7dc3657a2cea56bf5061d7be06303f7b265df48b1c55098dfe9864d57248fe48",
    ),
    "i3_8": (
        "p3-v3-phase3-i3-8-design-amendment.md",
        "3ca35b53d725c54b3e1299dd3a757a09baba7562dd7e984f1fbd7128be22cf4c",
    ),
    "i3_9": (
        "p3-v3-phase3-i3-9-design-amendment.md",
        "88e3ca6ede27fd37d3fd22039362698994914ff1deceed82178fb170fe88408e",
    ),
    "i3_10": (
        "p3-v3-phase3-i3-10-design-amendment.md",
        "e398947925734687a060324adcf91d2c12584739f70dfe48c76a9cd2834d9e0b",
    ),
    "i3_11": (
        "p3-v3-phase3-i3-11-design-amendment.md",
        "da99646a7c7bf0f4f7487ee7898c504771dc62b467e66b934fc679a25a6598fd",
    ),
    "i3_12": (
        "p3-v3-phase3-i3-12-design-amendment.md",
        "e482b6f14e03d23080d5011b424efcaf0be280ea39ee9df5a93559ca0659a713",
    ),
}

EXPECTED_UUIDS = (
    "fa6a01e8-5e16-50e5-a679-572d6f97eebb",
    "8647d48e-3be7-5bcc-96ce-f99edd27d2f1",
    "cd27fc98-3338-5c4a-930a-a5f3641c1250",
    "cf2d9c10-7eb8-51f4-9acb-70e15bda166e",
    "e2b2957a-7f3c-57ac-a071-f4ad0ed15dd5",
    "1d950c12-033f-5037-8c6d-7b006ed0746a",
)


def _load(name: str):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            pytest.fail(f"RED: isolated I3 production module {name!r} does not exist", pytrace=False)
        raise


def test_all_i3_documents_and_phase2a_step_are_immutable_hash_anchors():
    assert sha256(FROZEN_STEP.read_bytes()).hexdigest() == FROZEN_STEP_SHA256
    for _, (name, expected) in AMENDMENT_HASHES.items():
        assert sha256((DOCS / name).read_bytes()).hexdigest() == expected


def test_i3_12_contract_summary_closes_registry_printables_and_motion_product():
    summary = _load(SPEC_MODULE).accepted_contract_summary()
    assert summary["amendment_hashes"] == {key: value[1] for key, value in AMENDMENT_HASHES.items()}
    assert summary["frozen_step_sha256"] == FROZEN_STEP_SHA256
    assert summary["registry_classification_counts"] == {
        "protected_exact": 131,
        "authorized_replacement": 18,
        "new_authorized": 126,
    }
    assert summary["registry_count"] == 275
    assert summary["printable_body_count"] == 34
    assert summary["moving_half_count"] == 6
    assert summary["moving_half_teeth"] == 130
    assert summary["cartesian_motion_state_count"] == 189_540
    assert summary["press_iv_pair_count"] == 22


def test_exact_six_plate_object_uuid_and_tool_map_is_frozen():
    rows = _load(SPEC_MODULE).source_3mf_object_map()
    assert len(rows) == 6
    assert tuple(row["object_uuid"] for row in rows) == EXPECTED_UUIDS
    assert [row["plate_index"] for row in rows] == [1, 2, 3, 4, 5, 6]
    assert all(row["teeth"] == 130 for row in rows)
    assert all(row["extruder"] == 1 for row in rows)
    assert all(row["filament_slot"] == 1 for row in rows)
    assert all(row["physical_tool"] == "T0" for row in rows)


def test_actual_solid_evidence_covers_complete_i3_cartesian_state_space():
    evidence = _load(GEOMETRY_MODULE).actual_solid_acceptance_evidence()
    assert evidence["registry_count"] == 275
    assert evidence["printable_body_count"] == 34
    assert evidence["moving_half_count"] == 6
    assert evidence["moving_half_tooth_counts"] == [130] * 6
    assert evidence["cartesian_motion_state_count"] == 189_540
    assert evidence["actual_solid_collision_checks"] is True
    assert evidence["maximum_unintended_intersection_mm3"] <= 1e-7
    assert evidence["driver_and_loading_paths_clear"] is True
    assert evidence["joinery_and_hardware_complete"] is True


def test_candidate_and_reference_packages_and_bit_exact_masks_are_closed():
    evidence = _load(PARITY_MODULE).raster_and_package_evidence()
    assert evidence["reference_occurrence_count"] == 203
    assert evidence["candidate_occurrence_count"] == 275
    assert evidence["candidate_classification_counts"] == [131, 18, 126]
    assert evidence["reference_package_complete"] is True
    assert evidence["candidate_package_complete"] is True
    assert evidence["authorized_id_count"] == 144
    assert evidence["four_connected_exterior_xor"] == 0
    assert evidence["eight_connected_exterior_xor"] == 0
    assert evidence["foreground_xor_outside_mask"] == 0
    assert evidence["outer_contour_xor"] == 0


def test_source_owned_3mf_has_exact_semantics_and_detached_traceability():
    evidence = _load(EXPORT_MODULE).source_3mf_semantic_evidence(write=False)
    assert evidence["member_grammar_ok"] is True
    assert evidence["unknown_members"] == []
    assert evidence["plate_count"] == 6
    assert evidence["object_count"] == 6
    assert evidence["printable_body_count"] == 34
    assert evidence["object_uuids"] == list(EXPECTED_UUIDS)
    assert evidence["extruder_map"] == [1] * 6
    assert evidence["filament_slot_map"] == [1] * 6
    assert evidence["physical_tool_map"] == ["T0"] * 6
    assert evidence["parity_projection_equal"] is True
    assert evidence["traceability_detached"] is True


def test_cad_acceptance_is_green_while_print_release_remains_explicit_pending():
    manifest = _load(EXPORT_MODULE).cad_acceptance_manifest(write=False)
    assert manifest["cad_phase"]["status"] == "PASS"
    assert manifest["cad_phase"]["step_and_source_3mf_complete"] is True
    assert manifest["backend_status"] == "DEFERRED_EXTERNAL_BACKEND_UNAVAILABLE"
    assert manifest["print_release"]["status"] in {"RED", "PENDING", "RED/PENDING"}
    assert manifest["print_release"]["gcode_count"] == 0
    assert manifest["physical_acceptance"]["status"] == "PENDING"


def test_required_i3_12_artifact_set_is_source_owned_and_version_isolated():
    paths = _load(EXPORT_MODULE).required_artifact_paths()
    required = {
        "assembled_nominal.step",
        "service_exploded.step",
        "print_components.3mf",
        "source_import_parity_manifest.json",
        "purchased_hardware_bom.json",
        "assembly_state_manifest.json",
        "plate_manifest.json",
        "i3_printable_body_manifest.json",
        "i3_10_3mf_traceability.json",
        "i3_10_3mf_parity_projection.json",
        "i3_8_validation_manifest.json",
    }
    assert required <= {Path(path).name for path in paths}
    assert all(Path(path).is_relative_to(MODEL_ROOT) for path in paths)

