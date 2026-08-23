"""Compact B4-R2 evidence-only regression suite."""

import pytest

import p3_v3_mvp_rings_b4_r2_adversarial_fin_clearance_export as export
import p3_v3_mvp_rings_b4_r2_adversarial_fin_clearance_validation as validation
from p3_v3_mvp_rings_b4_r2_adversarial_fin_clearance_spec import SPEC


def test_01_accepted_b4_r1_is_immutable():
    assert validation.accepted_b4_r1_immutable_evidence()["unchanged"]


def test_02_artifacts_are_byte_identical_to_b4_r1():
    evidence = export.artifact_identity_evidence()
    assert len(evidence["rows"]) == 3
    assert evidence["all_byte_identical"]


def test_03_adversarial_fin_poses_use_actual_breps():
    evidence = validation.nearest_fin_evidence()
    assert len(evidence["rows"]) == 6
    assert evidence["maximum_pose_error_deg"] == pytest.approx(0.0)
    assert evidence["maximum_iv_mm3"] == 0.0
    assert evidence["minimum_roller_distance_mm"] >= SPEC.roller_distance_mm[0]
    assert evidence["maximum_roller_distance_mm"] <= SPEC.roller_distance_mm[1]
    assert evidence["minimum_exact_pinion_distance_mm"] >= SPEC.exact_pinion_distance_min_mm
    assert {row["target"] for row in evidence["rows"]} == {"roller", "exact_pinion"}


def test_04_sensor_absence_is_measured_from_assembly():
    evidence = validation.magnet_sensor_position_evidence()
    assert len(evidence["rows"]) == 3
    assert evidence["assembly_occurrence_count"] > 0
    assert evidence["sensor_occurrence_count"] == 0
    assert not evidence["sensor_occurrence_labels"]
    assert evidence["no_sensor_solids_added"]


def test_05_evidence_only_boundary_and_no_b5():
    boundary = validation.physical_boundary()
    assert boundary["cad_only"]
    assert not boundary["b5_present"]
    assert not boundary["geometry_changed_from_b4_r1"]
