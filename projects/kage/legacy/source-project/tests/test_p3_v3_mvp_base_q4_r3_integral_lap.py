"""Ten acceptance gates for the accepted Q4-R3 integral-lap handoff."""

from __future__ import annotations

import pytest

import p3_v3_mvp_base_q4_r3_integral_lap_export as export
import p3_v3_mvp_base_q4_r3_integral_lap_validation as validation
from p3_v3_mvp_base_q4_r3_integral_lap_spec import SPEC


def test_01_exactly_four_alternating_one_solid_quadrants():
    evidence = validation.part_registry_evidence()
    assert evidence["printable_count"] == 4
    assert evidence["roles"] == ("quadrant_A", "quadrant_B", "quadrant_A", "quadrant_B")
    assert evidence["all_one_solid_valid"] is True
    assert evidence["forbidden_occurrence_count"] == 0


def test_02_all_four_seams_have_frozen_half_lap_envelopes():
    evidence = validation.all_seam_engagement_evidence()
    assert evidence["seam_count"] == 4
    assert evidence["all_expected_ownership"] is True
    assert all(row["gross_radial_span_mm"] == pytest.approx(46.0) for row in evidence["rows"])
    assert all(row["gross_overlap_depth_mm"] == pytest.approx(10.0) for row in evidence["rows"])
    assert evidence["minimum_tongue_material_mm3"] > 540.0
    assert evidence["minimum_roof_material_mm3"] > 540.0
    assert evidence["maximum_seating_distance_mm"] <= SPEC.cad_linear_tolerance_mm


def test_03_final_quadrants_have_no_positive_volume_collision():
    evidence = validation.no_collision_evidence()
    assert len(evidence["rows"]) == 6
    assert evidence["maximum_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3


def test_04_q2_q4_straight_z_insertion():
    evidence = validation.straight_z_path_evidence()
    assert tuple(row["moving_quadrant"] for row in evidence["rows"]) == (2, 4)
    assert evidence["start_z_mm"] == pytest.approx(5.0)
    assert evidence["end_z_mm"] == pytest.approx(0.0)
    assert evidence["sample_step_mm"] <= 0.25
    assert all(len(row["offsets_mm"]) == 21 for row in evidence["rows"])
    assert evidence["maximum_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3


def test_05_eight_m3x6_interfaces_and_length_negatives():
    evidence = validation.hardware_evidence()
    assert evidence["interface_count"] == 8
    assert evidence["maximum_unintended_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["minimum_shaft_nut_intersection_mm3"] > 0.0
    assert evidence["m3x5_protrusion_mm"] == pytest.approx(0.1)
    assert evidence["m3x6_protrusion_mm"] == pytest.approx(1.1)
    assert evidence["m3x8_protrusion_mm"] == pytest.approx(3.1)
    assert evidence["m3x5_accepted"] is False
    assert evidence["m3x6_accepted"] is True
    assert evidence["m3x8_accepted"] is False


def test_06_actual_geometry_rejects_half_mm_misregistration():
    evidence = validation.registration_negative_evidence()
    assert evidence["nominal_pass"] is True
    assert evidence["all_negatives_rejected"] is True
    assert set(evidence["cases"]) == {"nominal", "radial_shift", "cross_seam_shift"}
    assert any(value > SPEC.brep_intersection_tolerance_mm3 for value in evidence["cases"]["radial_shift"]["shaft_intersections_mm3"])
    assert any(value > SPEC.brep_intersection_tolerance_mm3 for value in evidence["cases"]["cross_seam_shift"]["shaft_intersections_mm3"])


def test_07_polymer_front_is_flat_and_head_projection_is_separate():
    evidence = validation.flatness_evidence()
    assert all(value == pytest.approx(2.5, abs=0.02) for value in evidence["polymer_top_z_mm"])
    assert evidence["maximum_top_deviation_mm"] <= 0.02
    assert evidence["nominal_polymer_step_mm"] <= 0.02
    assert evidence["socket_head_projection_mm"] == pytest.approx(3.0)


def test_08_outline_and_r118_keepout():
    evidence = validation.keepout_and_outline_evidence()
    assert evidence["outer_diameter_mm"] == pytest.approx(300.0, abs=1e-7)
    assert evidence["inner_diameter_mm"] == pytest.approx(132.0, abs=1e-7)
    assert evidence["maximum_functional_vertex_radius_mm"] < 118.0
    assert evidence["maximum_keepout_void_mm3"] <= SPEC.brep_intersection_tolerance_mm3


def test_09_u1_bed_fit_and_supported_lap_orientations():
    evidence = validation.bed_fit_evidence()
    assert evidence["all_fit"] is True
    assert evidence["all_on_bed"] is True
    assert evidence["all_one_solid"] is True
    assert evidence["orientations"] == ("underside_down", "front_down", "underside_down", "front_down")
    assert all(max(row["span_with_brim_xy_mm"]) <= 260.0 for row in evidence["rows"])


def test_10_version_isolation_and_export_parity():
    isolation = validation.version_isolation_evidence()
    assert isolation["all_frozen_tree_hashes_match"] is True
    assert isolation["handoff_hash_matches"] is True
    mesh = export.fresh_lib3mf_import_evidence()
    assert mesh["object_count"] == mesh["build_item_count"] == 4
    assert mesh["all_nonempty"] is True
    assert mesh["all_manifold_and_oriented"] is True
    assert mesh["unique_names"] is True
    parity = export.source_export_parity_evidence()
    assert parity["all_required_exist"] is True
    assert parity["all_solid_counts_equal"] is True
    assert parity["all_written_valid"] is True
    assert parity["maximum_bounds_error_mm"] <= 1.0e-6
    assert parity["maximum_volume_error_mm3"] <= 1.0e-4
