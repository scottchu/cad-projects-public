"""Focused B3-R0 plus B3-R1 correction acceptance tests."""

import pytest

import p3_v3_mvp_roller_b3_r1_blind_axle_towers_export as export
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_validation as validation
from p3_v3_mvp_roller_b3_r1_blind_axle_towers_spec import SPEC


def test_01_accepted_r4_b1_b2_r2_are_immutable():
    assert validation.immutable_hash_evidence()["all_unchanged"] is True


def test_02_three_towers_and_nine_role_centers_are_exact():
    e = validation.center_and_profile_evidence()
    assert len(e["rows"]) == 9 and e["all_valid_one_solid"]
    assert {r["angle_deg"] for r in e["rows"]} == {60.0, 180.0, 300.0}
    assert {r["center_z_mm"] for r in e["rows"]} == {0.0, 6.7, 13.4}
    assert all(r["roller_axis_radius_mm"] == pytest.approx(118.0) for r in e["rows"])


def test_03_flange_retention_and_axial_clearance_are_preserved():
    e = validation.retention_guidance_tooth_evidence()
    assert e["maximum_roller_ring_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["flange_overlap_mm"] == pytest.approx(1.4)
    assert e["lower_axial_clearance_mm"] == pytest.approx(0.15)
    assert e["upper_axial_clearance_mm"] == pytest.approx(0.15)
    assert e["axial_clearance_total_mm"] == pytest.approx(0.3)


def test_04_guide_radius_has_point_one_five_race_clearance():
    assert validation.retention_guidance_tooth_evidence()["race_clearance_mm"] == pytest.approx(0.15)


def test_05_tooth_relief_has_point_four_clearance():
    assert validation.retention_guidance_tooth_evidence()["tooth_clearance_mm"] == pytest.approx(0.4)


def test_06_full_360_fin_witness_and_hall_keepouts_pass_stationary_parts():
    e = validation.fin_and_hall_passage_evidence()
    assert e["maximum_fin_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["fin_clearance_mm"] == pytest.approx(3.1)
    assert e["maximum_hall_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_07_rollers_bearings_and_washers_have_zero_forbidden_iv():
    e = validation.washer_bearing_evidence()
    assert e["maximum_roller_washer_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["maximum_bearing_roller_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["washer_stack_z_mm"] == ((-3.6,-3.1),(3.1,3.6),(9.8,10.3),(16.5,17.0))


def test_08_all_nine_rollers_insert_radially_center_outward():
    e = validation.radial_roller_insertion_evidence()
    assert len(e["rows"]) == 9
    assert all(r["sample_count"] == 39 for r in e["rows"])
    assert e["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_09_axle_and_driver_sweeps_are_clear():
    assert validation.axle_insertion_extraction_evidence()["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert validation.top_nut_access_evidence()["maximum_driver_tower_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_10_b2_powered_mesh_states_clear_new_printed_parts():
    e = validation.b2_powered_mesh_evidence()
    assert tuple(r["q_mm"] for r in e["rows"]) == (-0.35,0.0,0.10)
    assert e["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_11_tower_envelope_and_all_print_bases_are_valid():
    e = validation.envelope_and_print_evidence()
    assert e["maximum_tower_radius_mm"] <= 120.0+1e-7
    assert e["all_flat_on_bed"] and e["all_fit_u1"] and e["all_one_solid_valid"]
    assert e["print_object_count"] == 22


def test_12_correction_actual_towers_clear_inherited_risers():
    e = validation.corrected_axle_interface_evidence()
    assert e["maximum_tower_riser_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["minimum_tower_riser_clearance_mm"] == pytest.approx(0.2)


def test_13_correction_actual_axles_clear_inherited_risers():
    e = validation.corrected_axle_interface_evidence()
    assert e["maximum_axle_riser_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["minimum_fixed_axle_riser_clearance_mm"] == pytest.approx(0.6)


def test_14_correction_m3x25_endpoints_are_exact():
    e = validation.corrected_axle_interface_evidence()
    assert e["axle_length_mm"] == pytest.approx(25.0)
    assert SPEC.axle_under_head_z_mm == pytest.approx(20.4)
    assert SPEC.axle_tip_z_mm == pytest.approx(-4.6)


def test_15_correction_blind_locator_depth_and_floor_are_exact():
    e = validation.corrected_axle_interface_evidence()
    assert e["blind_pocket_z_mm"] == (-4.6,-3.6)
    assert e["blind_pocket_depth_mm"] == pytest.approx(1.0)
    assert e["blind_floor_mm"] == pytest.approx(0.4)


def test_16_correction_top_nut_is_captured_without_tower_overlap():
    e = validation.top_nut_access_evidence()
    assert e["nut_pocket_z_mm"] == (17.6,20.2)
    assert e["maximum_nut_tower_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_17_correction_top_nut_engagement_is_at_least_two_point_four():
    assert validation.top_nut_access_evidence()["minimum_engagement_mm"] >= 2.4-1e-7


def test_18_correction_axle_clears_tower_and_has_top_driver_access():
    e = validation.top_nut_access_evidence()
    assert e["maximum_axle_tower_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["maximum_driver_tower_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_19_correction_axle_insertion_and_extraction_are_both_clear():
    e = validation.axle_insertion_extraction_evidence()
    assert len(e["rows"]) == 3
    assert all(r["sample_count"] == 31 for r in e["rows"])
    assert e["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_20_correction_uses_no_bottom_nut_and_no_predecessor_drilling():
    assert validation.corrected_axle_interface_evidence()["no_bottom_nut"] is True
    assert validation.immutable_hash_evidence()["all_unchanged"] is True


def test_21_artifacts_are_printed_only_and_source_export_equivalent():
    mesh = export.fresh_lib3mf_import_evidence()
    assert mesh["object_count"] == mesh["build_item_count"] == 22
    assert mesh["all_nonempty"] and mesh["all_manifold_and_oriented"] and mesh["unique_names"]
    parity = export.source_export_parity_evidence()
    assert parity["all_required_exist"] and parity["all_solid_counts_equal"] and parity["all_written_valid"]
    assert parity["maximum_bounds_error_mm"] <= 1e-6
    assert parity["maximum_volume_error_mm3"] <= 1e-4
    occurrence_validation = export.post_export_occurrence_validation_evidence()
    assert occurrence_validation["all_occurrences_valid"] is True
    assert all(
        row["failure_count"] == 0 and row["occurrence_count"] > 0
        for row in occurrence_validation["artifacts"]
    )


def test_22_cad_only_boundary_has_no_later_layers():
    e = validation.physical_validation_boundary()
    assert e["cad_acceptance_only"] and not e["later_layers_present"]
    assert len(e["still_requires_print"]) == 4


def test_23_b2_input_bevel_topology_repair_preserves_intended_solid():
    e = validation.input_bevel_topology_repair_evidence()
    assert e["maximum_bounds_delta_mm"] <= 1e-9
    assert e["maximum_volume_delta_mm3"] <= 1e-9
    assert e["all_face_edge_counts_preserved"] is True
    assert e["all_repaired_clean"] is True
