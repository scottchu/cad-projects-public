"""Exactly seven focused gates from the accepted Q4-R2 screw-only handoff."""

from __future__ import annotations

from pathlib import Path
import re

from build123d import import_step
import pytest

import p3_v3_mvp_base_q4_r2_screw_only_export as export
import p3_v3_mvp_base_q4_r2_screw_only_geometry as geometry
import p3_v3_mvp_base_q4_r2_screw_only_validation as validation
from p3_v3_mvp_base_q4_r2_screw_only_spec import NAMESPACE, SPEC


ROOT = Path(__file__).resolve().parents[1]


def test_01_four_piece_bed_fit_and_solidity():
    evidence = validation.four_piece_bed_fit_and_solidity_evidence()
    assert evidence["quadrant_count"] == 4
    assert evidence["all_one_solid_valid_positive"] is True
    assert evidence["all_bed_contained_with_brim"] is True
    assert evidence["maximum_raw_span_mm"] == pytest.approx(212.061311893, abs=1e-6)
    assert evidence["maximum_brim_span_mm"] == pytest.approx(222.061311893, abs=1e-6)
    assert max(row["placed_z_floor_error_mm"] for row in evidence["rows"]) <= 1e-7


def test_02_exact_screw_only_registry():
    evidence = validation.screw_only_registry_evidence()
    assert evidence["printable_body_count"] == 8
    assert evidence["quadrant_count"] == 4
    assert evidence["clamp_count"] == 4
    assert evidence["integral_boss_count"] == 8
    assert evidence["screw_interface_count"] == 8
    assert evidence["nut_receiver_count"] == 8
    assert evidence["hardware_screw_count"] == 8
    assert evidence["hardware_nut_count"] == 8
    assert evidence["all_printables_one_solid"] is True
    assert all(evidence[key] == 0 for key in evidence if key.startswith("disallowed_"))
    source = "\n".join(
        (ROOT / name).read_text().lower()
        for name in (
            "p3_v3_mvp_base_q4_r2_screw_only_spec.py",
            "p3_v3_mvp_base_q4_r2_screw_only_geometry.py",
        )
    )
    assert "press_bore" not in source
    assert re.search(r"\b(?:dowel|pin)\b", source) is None


def test_03_m3x6_stack_containment_and_driver_access_with_length_negatives():
    evidence = validation.screw_stack_and_access_evidence()
    assert evidence["interface_count"] == 8
    assert all(row["screw_solid_count"] == 1 and row["nut_solid_count"] == 1 for row in evidence["rows"])
    assert evidence["maximum_unintended_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["minimum_shaft_nut_engagement_mm3"] > 0.0
    assert evidence["m3x6_full_nut_engagement_mm"] == pytest.approx(2.40)
    assert evidence["m3x6_tip_beyond_nut_mm"] == pytest.approx(0.80)
    assert evidence["m3x6_tip_beyond_nut_mm"] <= evidence["tip_relief_depth_mm"]
    assert evidence["bottom_skin_mm"] == pytest.approx(1.00)
    assert evidence["m3x5_engagement_mm"] == pytest.approx(2.20)
    assert evidence["m3x5_full_engagement_pass"] is False
    assert evidence["m3x8_tip_beyond_nut_mm"] == pytest.approx(2.80)
    assert evidence["m3x8_tip_contained_pass"] is False


def test_04_actual_solid_boss_receiver_fit_contact_and_openings():
    evidence = validation.boss_receiver_fit_evidence()
    assert evidence["maximum_boss_base_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["maximum_clamp_base_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["maximum_contact_distance_mm"] <= SPEC.cad_linear_tolerance_mm
    assert evidence["maximum_opening_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["round_actual_receiver_span_xy_mm"] == pytest.approx((4.15, 4.15), abs=1e-7)
    assert evidence["relieved_actual_receiver_span_xy_mm"] == pytest.approx((5.15, 4.15), abs=1e-7)
    assert evidence["round_actual_diametral_clearance_mm"] == pytest.approx(0.15, abs=1e-7)
    assert evidence["relieved_actual_radial_clearance_mm"] == pytest.approx(1.15, abs=1e-7)
    assert evidence["relieved_actual_tangential_clearance_mm"] == pytest.approx(0.15, abs=1e-7)
    assert evidence["boss_height_mm"] == pytest.approx(2.40, abs=1e-7)
    assert evidence["boss_front_recess_mm"] == pytest.approx(0.10, abs=1e-7)
    assert all(
        row["clamp_solid_count"] == 1 and row["adjacent_quadrant_solid_counts"] == (1, 1)
        for row in evidence["rows"]
    )


def test_05_same_registration_evaluator_rejects_translation_and_rotation():
    evidence = validation.seam_registration_sensitivity_evidence()
    assert evidence["nominal_pass"] is True
    assert evidence["cases"]["nominal"]["seam_gap_mm"] == pytest.approx(0.10, abs=1e-7)
    assert evidence["all_deliberate_negatives_rejected"] is True
    assert set(evidence["cases"]) == {
        "nominal",
        "left_translated",
        "right_translated",
        "left_rotated",
        "right_rotated",
    }


def test_06_all_clamps_insert_straight_up_and_old_attached_lowering_fails():
    evidence = validation.assembly_path_evidence()
    approved = evidence["approved_straight_up"]
    assert approved["sequence"] == "support_all_four_quadrants_insert_C1_C2_C3_then_C4_upward"
    assert len(approved["rows"]) == 4
    assert approved["path_clear"] is True
    rejected = evidence["rejected_attached_last_quadrant_lowering"]
    assert rejected["sequence"] == "lower_Q4_with_C4_attached"
    assert rejected["first_collision_z_offset_mm"] == pytest.approx(7.25)
    assert rejected["collision_sample_count"] > 0
    assert rejected["maximum_intersection_mm3"] > 1000.0
    assert rejected["path_clear"] is False


def test_07_reserved_zone_locked_isolation_step_validity_and_export_parity():
    isolation = validation.reserved_zone_and_locked_isolation_evidence()
    assert isolation["keepout_radius_range_mm"] == (118.0, 150.0)
    assert isolation["maximum_functional_vertex_radius_mm"] < SPEC.future_support_clear_radius_min_mm
    assert isolation["maximum_keepout_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert isolation["all_quadrant_brep_digests_equal"] is True
    assert isolation["frozen_input_evidence"]["all_frozen_hashes_match"] is True
    required = export.required_artifact_paths()
    assert all(NAMESPACE in str(path) for path in required[:-1])
    assert all(path.is_file() and path.stat().st_size > 0 for path in required)
    assembled = import_step(export.ASSEMBLED_STEP)
    exploded = import_step(export.EXPLODED_STEP)
    assert len(assembled.solids()) == 24
    assert len(exploded.solids()) == 24
    assert all(solid.is_valid and solid.volume > 0.0 for solid in assembled.solids() + exploded.solids())
    for path in export.individual_step_paths():
        shape = import_step(path)
        assert len(shape.solids()) == 1, path
        assert shape.is_valid and shape.volume > 0.0, path
        assert shape.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7), path
    mesh = export.fresh_lib3mf_import_evidence()
    assert mesh["object_count"] == mesh["build_item_count"] == 8
    assert mesh["all_nonempty"] is True
    assert mesh["all_manifold_and_oriented"] is True
    assert mesh["unique_names"] is True
    assert all(NAMESPACE in name for name in mesh["names"])
    parity = export.source_export_parity_evidence()
    assert parity["all_paths_exist"] is True
    assert parity["all_solid_counts_equal"] is True
    assert parity["all_written_valid"] is True
    assert parity["maximum_bounds_error_mm"] <= 1e-6
    assert parity["maximum_volume_error_mm3"] <= 1e-4
