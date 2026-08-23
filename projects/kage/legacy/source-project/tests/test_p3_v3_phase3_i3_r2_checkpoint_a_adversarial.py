"""Adversarial regressions for the independently rejected A false-greens."""

from __future__ import annotations

from inspect import signature

import pytest

from p3_v3_phase3_i3_r2_verified_release.frozen import artifact_rejection_evidence
from p3_v3_phase3_i3_r2_verified_release.gate_evaluator import checkpoint_a_evidence
from p3_v3_phase3_i3_r2_verified_release.geometry import (
    moving_half_shapes,
    seam_witnesses_from_shapes,
)
from p3_v3_phase3_i3_r2_verified_release.probes import analyze_parameter_consumption
from p3_v3_phase3_i3_r2_verified_release.spec import (
    DEFAULT_OWNERS,
    adjusted_owner_bundle,
)


@pytest.fixture(scope="module")
def evidence():
    return checkpoint_a_evidence()


def test_production_consumer_rejects_missing_and_stale_without_root_fallback() -> None:
    result = artifact_rejection_evidence()
    assert result["consumer"] == "artifact_consumer.pin_current_release"
    assert result["cases"] == result["expected"]
    assert {row["rejection_code"] for row in result["cases"]} == {
        "R2_ARTIFACT_CURRENT_MISSING",
        "R2_ARTIFACT_CURRENT_STALE",
    }


def test_r1_facts_are_remeasured_from_registry_archive_xml_json_and_lib3mf(evidence) -> None:
    r1 = evidence["r1_facts"]
    assert r1["all_match"]
    assert len(r1["source_provenance"]) == 9
    assert all(r1["mapping_checks"].values())
    assert r1["registry"]["predecessor_partition_counts"] == {
        "protected_exact": 131,
        "authorized_replacement": 18,
        "new_authorized": 126,
    }


def test_witness_crops_cannot_consume_adjusted_owners_after_shapes_are_frozen() -> None:
    assert tuple(signature(seam_witnesses_from_shapes).parameters) == ("shapes", "datums")
    frozen_all = moving_half_shapes(DEFAULT_OWNERS)
    frozen_hour = {key: value for key, value in frozen_all.items() if key[0] == "hour"}
    before = seam_witnesses_from_shapes(frozen_hour)
    changed = adjusted_owner_bundle(
        DEFAULT_OWNERS, "moving_joinery", "receive_xy_clearance_mm", 0.20
    )
    assert changed.moving_joinery.receive_xy_clearance_mm == 0.20
    after = seam_witnesses_from_shapes(frozen_hour)
    assert before == after


def test_butt_relief_is_measured_on_both_exterior_sides_of_all_six_seams(evidence) -> None:
    seams = evidence["geometry"]["seams"]
    assert len(seams) == 6
    for row in seams:
        assert row["half_a_butt_relief_mm"] == pytest.approx(0.025, abs=1e-7)
        assert row["half_b_butt_relief_mm"] == pytest.approx(0.025, abs=1e-7)
        assert row["butt_gap_mm"] == pytest.approx(0.050, abs=1e-7)


def test_protected_proof_compares_true_r1_rows_to_each_r2_successor(evidence) -> None:
    for probe in evidence["probes"].values():
        for comparison in (probe["baseline_registry"], probe["changed_registry"]):
            assert comparison["predecessor_source"].startswith("R1 baseline_rows")
            assert comparison["successor_source"].startswith("R2 protected_occurrence_rows")
            assert comparison["predecessor_count"] == comparison["successor_count"] == 131
            assert comparison["protected_drift"] == []


def test_full_275_successor_comparison_allows_exactly_six_geometry_changes(evidence) -> None:
    comparison = evidence["r1_facts"]["registry"]
    assert comparison["predecessor_count"] == comparison["successor_count"] == 275
    assert comparison["changed_ids"] == comparison["authorized_changed_ids"]
    assert len(comparison["changed_ids"]) == 6
    assert comparison["protected_drift"] == comparison["unauthorized_drift"] == []


def test_ast_rejects_adjustable_field_used_only_by_witness_code() -> None:
    fake = analyze_parameter_consumption(
        {
            "fake.py": (
                "def seam_witnesses(owners):\n"
                "    return owners.receive_xy_clearance_mm, owners.butt_face_relief_mm\n"
            )
        }
    )
    assert not fake["all_adjustable_fields_consumed"]
    assert not fake["production_consumers"]["receive_xy_clearance_mm"]
    assert fake["validation_consumers"]["receive_xy_clearance_mm"]


def test_ast_rejects_reviewer_same_named_no_geometry_spoof() -> None:
    spoof = analyze_parameter_consumption(
        {
            "spoof.py": (
                "def moving_seam_tools(owners):\n"
                "    return (owners.receive_xy_clearance_mm, owners.butt_face_relief_mm)\n"
                "def moving_half_shapes(owners):\n"
                "    return moving_seam_tools(owners)\n"
            )
        }
    )
    assert not spoof["all_adjustable_fields_consumed"]
    assert spoof["production_consumers"] == {
        "receive_xy_clearance_mm": [],
        "butt_face_relief_mm": [],
    }


def test_ast_rejects_renamed_wrapper_that_only_forwards_owner_values() -> None:
    spoof = analyze_parameter_consumption(
        {
            "wrapper.py": (
                "def renamed_reader(owners):\n"
                "    return {'c': owners.receive_xy_clearance_mm, "
                "'r': owners.butt_face_relief_mm}\n"
                "def renamed_wrapper(owners):\n"
                "    values = renamed_reader(owners)\n"
                "    return values\n"
            )
        }
    )
    assert not spoof["all_adjustable_fields_consumed"]


def test_ast_accepts_renamed_semantic_solid_to_boolean_dataflow() -> None:
    semantic = analyze_parameter_consumption(
        {
            "renamed.py": (
                "from build123d import Box\n"
                "def renamed_tools(owners):\n"
                "    cavity = Box(owners.receive_xy_clearance_mm, 2, 3)\n"
                "    relief = Box(owners.butt_face_relief_mm, 2, 3)\n"
                "    return {'cavity': cavity, 'relief': relief}\n"
                "def renamed_assembly(owners):\n"
                "    tools = renamed_tools(owners)\n"
                "    solid = Box(4, 5, 6)\n"
                "    solid = solid.cut(tools['cavity'])\n"
                "    solid = solid.cut(tools['relief'])\n"
                "    return solid\n"
            )
        }
    )
    assert semantic["all_adjustable_fields_consumed"]
    for rows in semantic["production_consumers"].values():
        assert rows[0]["consumer_function"] == "renamed_assembly"
        assert rows[0]["boolean_operation"] == "cut"


def test_locality_acceptance_uses_actual_delta_faces_and_owned_regions(evidence) -> None:
    for probe in evidence["probes"].values():
        assert probe["locality_acceptance_basis"] == (
            "actual_brep_symmetric_difference_faces_bounded_by_owned_tools"
        )
        changed = [row for row in probe["locality"] if row["delta_volume_mm3"] > 1e-9]
        assert {row["half_id"] for row in changed} == set(probe["expected_changed_halves"])
        assert all(row["delta_face_count"] > 0 and row["delta_aabb_mm"] for row in changed)
        assert all(row["owned_region_intersection_mm3"] > 1e-9 for row in changed)
        assert all(row["outside_owned_region_mm3"] <= 1e-7 for row in probe["locality"])
