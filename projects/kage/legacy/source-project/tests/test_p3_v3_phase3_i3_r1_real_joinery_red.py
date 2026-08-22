"""RED inventory for the localized I3-R1 real-joinery repair.

These tests are intentionally isolated from the rejected I3 checkpoint.  Each
test names one reviewer failure and must remain RED until the successor builds
and measures the real source/export solids.
"""

from __future__ import annotations

from hashlib import sha256
import importlib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "p3-v3-phase3-i3-r1-real-joinery-localized-repair-handoff.md"
HANDOFF_SHA256 = "7b20b2fff600623a1fceab4ec66717d6b5bcc3257d4d32653b26a72d35b704f4"
NS = "p3_v3_phase3_i3_r1_real_joinery"


def _load(suffix: str):
    name = f"{NS}_{suffix}"
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            pytest.fail(f"RED: successor module {name!r} is absent", pytrace=False)
        raise


def test_red_01_handoff_and_frozen_inputs_are_anchored():
    assert sha256(HANDOFF.read_bytes()).hexdigest() == HANDOFF_SHA256
    assert _load("spec").frozen_input_evidence()["all_frozen_hashes_match"] is True


def test_red_02_moving_joinery_is_boolean_material_not_overlay():
    rows = _load("geometry").moving_joinery_actual_brep_evidence()
    assert len(rows) == 6
    assert all(row["lap_added_volume_mm3"] > 0 for row in rows)
    assert all(row["cut_volume_mm3"] > 0 for row in rows)


def test_red_03_moving_hardware_has_no_unintended_material_intersection():
    e = _load("validation").moving_hardware_collision_evidence()
    assert e["placement_count"] == 30
    assert e["maximum_unintended_intersection_mm3"] <= 1e-7


def test_red_04_stationary_bridges_are_cut_and_hardware_clear():
    e = _load("validation").stationary_hardware_collision_evidence()
    assert e["bridge_count"] == 16
    assert e["positive_unintended_pair_count"] == 0
    assert e["maximum_unintended_intersection_mm3"] <= 1e-7


def test_red_05_front_ring_bridge_and_dowel_are_contract_dimensions():
    e = _load("geometry").front_ring_joinery_measurements()
    assert e["bridge_thickness_mm"] == pytest.approx(3.0)
    assert e["dowel_nominal_diameter_mm"] == pytest.approx(2.0)


def test_red_06_reconstruction_and_motion_are_measured_not_prefilled():
    e = _load("validation").actual_brep_acceptance_matrix()
    assert e["measurement_provenance"] == "actual_brep_operations"
    assert e["moving_reconstruction_xor_max_mm3"] <= 1e-7
    assert e["stationary_reconstruction_xor_max_mm3"] <= 1e-7
    assert e["motion_transform_count"] == 189_540
    motion = e["motion"]
    assert motion["state_evaluation_reference_count"] == 189_540
    assert motion["states_without_evaluated_signatures"] == 0
    assert motion["complete_pair_count"] == motion["expected_complete_pair_count"]
    assert motion["audit_state_count"] > 0
    assert motion["audit_unpruned_pair_count"] > 0
    assert motion["audit_missing_candidate_pair_count"] == 0
    assert motion["transformed_actual_brep_aabb_containment_violation_mm"] <= 1e-7
    assert motion["narrowphase_evaluated_signature_count"] == motion["unique_candidate_signature_count"]
    assert motion["maximum_unintended_intersection_mm3"] <= 1e-7


def test_red_07_plus30_print_transform_measures_real_aabbs_and_exact_brim():
    rows = _load("print_project").moving_plate_transform_evidence()
    assert len(rows) == 6
    assert all(row["rotation_degrees"] == pytest.approx(30.0) for row in rows)
    assert all(row["brim_mm_per_side"] == pytest.approx(3.5) for row in rows)
    assert all(max(row["raw_span_xy_mm"]) <= 244.864483 for row in rows)
    assert all(row["contained_in_usable_bed"] is True for row in rows)


def test_red_08_disassembled_3mf_contains_all_34_printable_bodies_only():
    e = _load("export").disassembled_3mf_import_evidence(write=False)
    assert e["printable_body_count"] == 34
    assert e["stationary_quadrant_count"] == 12
    assert e["moving_half_count"] == 6
    assert e["stationary_bridge_count"] == 16
    assert e["purchased_hardware_count"] == 0


def test_red_09_i3_12_v3_projection_is_canonical_and_stage_correct():
    e = _load("canonical").projection_evidence(write=False)
    assert e["schema"] == "kage.i3.12.3mf-parity-projection.v3"
    assert e["relationships_stage_correct"] is True
    assert e["rfc8785_jcs_verified"] is True
    assert e["c14n11_verified"] is True


def test_red_10_step_regeneration_is_fresh_atomic_and_imported():
    e = _load("export").fresh_atomic_regeneration_evidence(write=False)
    assert e["generated_in_new_temporary_directory"] is True
    assert e["atomic_publish"] is True
    assert e["fresh_process_import_count"] >= 2
    assert e["stale_artifact_reuse_count"] == 0


def test_red_11_each_geometry_parameter_has_a_measured_probe():
    e = _load("validation").parameter_ownership_probe_evidence()
    assert e["unowned_geometry_literals"] == []
    assert e["missing_adjustable_parameter_probes"] == []
    assert e["protected_geometry_probe_drift"] == []


def test_red_12_orca_project_has_six_real_plates_and_frozen_profiles():
    e = _load("print_project").orca_source_project_evidence(write=False)
    assert e["plate_count"] == 6
    assert e["build_object_count"] == 6
    assert e["filament_identifier"] == "GFG00"
    assert e["four_nozzle_mapping_verified"] is True
    assert e["moving_brim_mm"] == pytest.approx(3.5)
    assert e["skirt_loops"] == 0
    assert e["prime_tower_enabled"] is False


def test_red_13_freshness_digest_covers_every_authoritative_input():
    e = _load("export").freshness_input_evidence()
    assert e["missing_required_inputs"] == []
    assert e["signature_deletion_forces_regeneration"] is True


def test_red_14_imported_bounds_and_protected_parity_are_measured():
    e = _load("parity").fresh_process_source_import_evidence(write=False)
    assert e["protected_occurrence_count"] == 131
    assert e["protected_drift"] == []
    assert e["imported_global_bounds_mm"] == pytest.approx(
        [-150.0, -150.0, -32.5, 150.0, 150.0, 24.2514]
    )


def test_red_15_authorized_press_pairs_are_exact_actual_intersections():
    e = _load("validation").press_pair_actual_brep_evidence()
    assert e["pair_count"] == 22
    assert e["unexpected_positive_pair_count"] == 0
    assert e["maximum_volume_error_mm3"] <= 1e-7


def test_red_16_source_owned_successor_artifacts_are_isolated():
    e = _load("export").required_artifact_paths()
    assert e
    assert all(NS in str(path) for path in e)
