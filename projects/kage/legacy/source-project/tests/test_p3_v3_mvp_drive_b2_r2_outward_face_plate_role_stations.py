"""Focused CAD acceptance for the B2-R2 three populated role stations."""

import pytest

import p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_export as export
import p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_validation as validation
from p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_spec import SPEC


def test_01_motor_body_clears_face_plate_cheeks_and_bridge_at_every_q():
    e = validation.bracket_collision_evidence()
    assert len(e["rows"]) == 15
    assert e["maximum_forbidden_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_02_motor_face_contact_is_only_at_r112_plus_q_plane():
    e = validation.bracket_collision_evidence()
    assert e["maximum_face_plane_error_mm"] <= 1e-7
    assert e["all_face_contact_distance_zero"] is True


def test_03_pilot_has_point_one_fit_and_four_point_four_tower_clearance():
    e = validation.pilot_and_m2_evidence()
    assert e["opening_radial_clearance_per_side_mm"] == pytest.approx(0.10)
    assert e["minimum_pilot_tower_clearance_mm"] >= 4.40-1e-7
    assert e["maximum_pilot_printed_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["maximum_pilot_tower_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_04_four_m2_holes_match_the_purchased_15p40_square():
    e = validation.pilot_and_m2_evidence()
    assert len(e["axes"]) == 4
    assert e["axis_pitch_tangential_mm"] == pytest.approx(15.40)
    assert e["axis_pitch_z_mm"] == pytest.approx(15.40)


def test_05_m2x4_engages_two_mm_without_exceeding_thread_depth():
    e = validation.pilot_and_m2_evidence()
    assert len(e["screw_rows"]) == 20
    assert e["minimum_engagement_mm"] == pytest.approx(2.00)
    assert e["maximum_engagement_mm"] == pytest.approx(2.00)
    assert e["maximum_engagement_mm"] <= e["guaranteed_thread_depth_mm"]
    assert e["maximum_screw_plate_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_06_four_d4p5_driver_sweeps_are_unobstructed_pre_ring():
    e = validation.driver_and_insertion_evidence()
    assert len(e["driver_rows"]) == 20
    assert e["maximum_driver_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_07_bare_motor_center_outward_insertion_is_collision_free():
    e = validation.driver_and_insertion_evidence()
    assert len(e["insertion_rows"]) == 5
    assert all(row["sample_count"] == 46 for row in e["insertion_rows"])
    assert e["maximum_motor_insertion_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_08_input_bevel_inserts_after_motor_mounting_through_window():
    e = validation.driver_and_insertion_evidence()
    assert len(e["bevel_rows"]) == 3
    assert all(row["sample_count"] == 12 for row in e["bevel_rows"])
    assert e["maximum_bevel_insertion_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_09_face_plate_to_input_gear_radial_gap_is_one_point_one_nine():
    e = validation.corrected_drive_evidence()
    assert e["face_plate_input_gear_radial_gap_mm"] == pytest.approx(1.19)


def test_10_frozen_interfaces_and_300_mm_envelope_are_unchanged():
    e = validation.immutable_interface_evidence()
    assert e["r4_unchanged"] is True
    assert e["b1_unchanged"] is True
    assert e["base_underside_z_mm"] == pytest.approx((-31.5,)*4)
    assert e["output_axis_radius_mm"] == pytest.approx(122.0)
    assert e["role_pinion_z_mm"] == ((0.0, 2.1), (6.7, 8.8), (13.4, 15.5))
    assert e["center_keepout_radius_mm"] == pytest.approx(66.0)
    assert e["base_envelope_diameter_mm"] == pytest.approx(300.0)


def test_11_prior_clean_b2_r1_clearance_and_service_gates_remain_true():
    drive = validation.corrected_drive_evidence()
    assert drive["maximum_bevel_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert 0.08 <= drive["minimum_backlash_mm"] <= drive["maximum_backlash_mm"] <= 0.20
    assert drive["engagements_mm"] == pytest.approx((0.16, 0.41, 0.66))
    assert drive["maximum_shaft_clearance_mm"] >= 0.75-1e-7
    assert drive["wire_min_radius_mm"] == pytest.approx(68.2)
    assert drive["wire_center_margin_mm"] >= 2.2-1e-7
    service = validation.service_and_registry_evidence()
    assert service["all_service_valid_one_solid"] is True
    assert service["maximum_base_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert service["maximum_purchased_printed_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert service["registry_count"] == 9
    assert service["all_registry_one_solid_valid"] is True
    assert service["maximum_nonpinion_radius_mm"] <= 128.5


def test_12_artifacts_are_model_only_and_source_export_equivalent():
    mesh = export.fresh_lib3mf_import_evidence()
    assert mesh["object_count"] == mesh["build_item_count"] == 9
    assert mesh["all_nonempty"] and mesh["all_manifold_and_oriented"] and mesh["unique_names"]
    parity = export.source_export_parity_evidence()
    assert parity["all_required_exist"] and parity["all_solid_counts_equal"] and parity["all_written_valid"]
    assert parity["maximum_bounds_error_mm"] <= 1e-6
    assert parity["maximum_volume_error_mm3"] <= 1e-4


def test_13_cad_only_boundary_and_no_later_layers():
    e = validation.physical_validation_boundary()
    assert e["cad_acceptance_only"] is True
    assert e["later_layers_present"] is False
    assert len(e["still_requires_print"]) == 4
