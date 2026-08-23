"""Focused CAD acceptance for the Q4-R4 functional centered step-lap base."""

from __future__ import annotations

import pytest

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_export as export
import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_validation as validation
from p3_v3_mvp_base_q4_r4_functional_centered_step_lap_spec import SPEC


def test_01_version_isolation_and_revision_k_authority():
    evidence = validation.version_isolation_evidence()
    assert evidence["all_frozen_tree_hashes_match"] is True
    assert evidence["authority_hashes_match"] is True


def test_02_exactly_four_valid_printable_quadrants():
    evidence = validation.part_registry_evidence()
    assert evidence["printable_count"] == 4
    assert evidence["roles"] == ("two_upper", "upper_lower", "upper_lower", "two_lower")
    assert evidence["orientations"] == ("underside_down",) * 4
    assert evidence["all_one_solid_valid"] is True
    assert evidence["forbidden_occurrence_count"] == 0


def test_03_locked_circle_datum_and_flat_coplanar_underside():
    evidence = validation.datum_flatness_evidence()
    assert evidence["plate_bottom_z_mm"] == pytest.approx(-31.5)
    assert evidence["nominal_polymer_top_z_mm"] == pytest.approx(-25.5)
    assert evidence["boss_top_z_mm"] == pytest.approx(-25.0)
    assert evidence["all_min_z_exact"] is True
    assert evidence["bottom_coplanarity_mm"] <= 1.0e-7
    assert evidence["minimum_bottom_contact_area_mm2"] > 10000.0


def test_04_actual_broad_complementary_laps_and_net_contact():
    evidence = validation.broad_lap_evidence()
    assert evidence["precedence"] == (
        ("S12", 1, 2), ("S23", 2, 3), ("S34", 3, 4), ("S41", 1, 4)
    )
    assert all(row["gross_area_mm2"] == pytest.approx(1196.0) for row in evidence["rows"])
    assert all(row["upper_thickness_mm"] == pytest.approx(3.0) for row in evidence["rows"])
    assert all(row["lower_thickness_mm"] == pytest.approx(3.0) for row in evidence["rows"])
    assert evidence["minimum_mutual_contact_area_mm2"] >= SPEC.actual_mutual_split_plane_contact_area_min_mm2
    assert tuple(row["mutual_contact_area_mm2"] for row in evidence["rows"]) == pytest.approx(
        (1098.3701, 1098.3701, 1125.0552, 1125.0552), abs=0.02
    )
    assert evidence["maximum_pairwise_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["exterior_polymer_step_mm"] == pytest.approx(0.0)


def test_05_top_only_m3x6_captive_nut_stack_and_length_negatives():
    evidence = validation.hardware_evidence()
    assert evidence["interface_count"] == evidence["boss_count"] == evidence["hole_count"] == evidence["trap_count"] == 8
    assert evidence["trap_af_mm"] == pytest.approx(5.8)
    assert evidence["trap_depth_mm"] == pytest.approx(2.5)
    assert evidence["tip_relief_bottom_z_mm"] == pytest.approx(-31.2)
    assert evidence["underside_floor_mm"] >= 0.30
    assert evidence["nut_thread_engagement_mm"] == pytest.approx(2.4)
    assert evidence["accepted_lengths_mm"] == (6.0,)
    assert evidence["maximum_void_residual_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["minimum_boss_material_mm3"] > 20.0
    assert evidence["underside_tool_dependency"] is False


def test_06_q4_q3_q2_q1_straight_z_top_down_assembly():
    evidence = validation.top_down_assembly_sweep_evidence()
    assert evidence["order"] == (4, 3, 2, 1)
    assert evidence["offsets_mm"][0] == pytest.approx(8.0)
    assert evidence["offsets_mm"][-1] == pytest.approx(0.0)
    assert evidence["maximum_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["q1_closes_both_seams"] is True


def test_07_actual_mount_parity_and_obsolete_tower_rejection():
    evidence = validation.mount_parity_evidence()
    assert evidence["center_opening_diameter_mm"] == pytest.approx(132.0)
    assert evidence["center_opening_residual_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["motor_slot_count"] == 12
    assert evidence["maximum_motor_slot_residual_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["spine_path_count"] == 2
    assert evidence["maximum_spine_path_residual_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["fixed_tower_count"] == 2
    assert evidence["minimum_fixed_landing_coverage_ratio"] >= 0.999999
    assert evidence["spine_top_bearing_coverage_ratio"] >= 0.999999
    assert evidence["spine_top_bearing_z_mm"] == pytest.approx(-25.5)
    assert evidence["spine_removed_before_quadrant_separation"] is True
    assert evidence["obsolete_300_r119p5_paths_are_solid"] is True
    assert evidence["motor_service_travel_mm"] == pytest.approx(2.5)
    assert evidence["motor_powered_range_mm"] == pytest.approx((-0.35, 0.10))
    assert evidence["output_axis_radius_mm"] == pytest.approx(122.0)


def test_08_actual_service_sweeps_paths_and_keepouts_clear_seams():
    evidence = validation.keepout_and_service_sweep_evidence()
    assert evidence["maximum_motor_sweep_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["minimum_motor_sweep_clearance_mm"] > 9.0
    assert evidence["maximum_locked_support_service_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["maximum_spine_mount_path_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["maximum_fixed_landing_shared_polymer_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    # The resolved S34/spine-foot overlap is shared structural plate polymer,
    # not a hardware/tool collision; the D3.2 paths remain clear above.
    assert evidence["spine_landing_shared_polymer_mm3"] == pytest.approx(23.5526, abs=0.02)
    assert evidence["maximum_ring_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["maximum_hall_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["maximum_seam_feature_radius_mm"] < 118.0
    assert evidence["receiver_worst_plan_corner_mm"] == pytest.approx(116.9473, abs=0.001)
    assert evidence["electronics_cut_count"] == 0


def test_09_u1_actual_oriented_part_fit():
    evidence = validation.u1_fit_evidence()
    assert evidence["all_fit"] is True
    assert evidence["all_on_bed"] is True
    assert evidence["all_one_solid"] is True
    assert all(max(row["span_with_brim_xy_mm"]) <= 260.0 for row in evidence["rows"])


def test_10_exactly_four_model_only_3mf_objects():
    evidence = export.fresh_lib3mf_import_evidence()
    assert evidence["object_count"] == evidence["build_item_count"] == 4
    assert evidence["all_nonempty"] is True
    assert evidence["all_manifold_and_oriented"] is True
    assert evidence["unique_names"] is True


def test_11_source_to_step_export_parity():
    evidence = export.source_export_parity_evidence()
    assert evidence["all_required_exist"] is True
    assert evidence["all_solid_counts_equal"] is True
    assert evidence["all_written_valid"] is True
    assert evidence["maximum_bounds_error_mm"] <= 1.0e-6
    assert evidence["maximum_volume_error_mm3"] <= 1.0e-4
