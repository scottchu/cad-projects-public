"""CAD acceptance for the deliberately narrow seven-object mounting MVP."""

import pytest

import p3_v3_mvp_mount_b1_r1_raised_nut_rails_export as export
import p3_v3_mvp_mount_b1_r1_raised_nut_rails_validation as validation
from p3_v3_mvp_mount_b1_r1_raised_nut_rails_spec import SPEC


def test_01_r4_is_immutable_and_changes_are_localized():
    e = validation.isolation_and_locality_evidence()
    assert e["r4_unchanged"] is True
    assert e["maximum_outside_mask_delta_mm3"] <= SPEC.brep_tolerance_mm3


def test_02_exactly_seven_reusable_printed_objects_and_no_drive_parts():
    e = validation.registry_evidence()
    assert e["count"] == 7
    assert e["names"] == ("quadrant_Q1", "quadrant_Q2", "quadrant_Q3", "quadrant_Q4", "reusable_motor_sled", "reusable_fixed_riser", "spine_riser")
    assert e["all_one_solid_valid"] is True
    assert e["forbidden_drive_component_count"] == 0


def test_03_exact_motor_pattern_and_rejected_r126_is_solid():
    e = validation.mount_pattern_evidence()
    assert e["count"] == 12
    assert e["radii"] == (88.0, 109.0)
    assert e["rejected_radius_mm"] == pytest.approx(126.0)
    assert e["minimum_rejected_axis_solid_mm3"] > 1.0
    assert e["maximum_r109_driver_obstruction_mm3"] <= SPEC.brep_tolerance_mm3


def test_03b_every_motor_nut_and_rigid_mouth_sweep_is_collision_free():
    e = validation.motor_nut_sweep_evidence()
    assert len(e["installed_rows"]) == 36
    assert len(e["sweep_rows"]) == 36
    assert e["maximum_installed_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["maximum_rigid_sweep_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["nut_clock_deg"] == pytest.approx(-30.0)
    assert e["channel_width_mm"] == pytest.approx(5.8)
    assert e["nut_af_mm"] == pytest.approx(5.5)
    assert e["clearance_per_side_mm"] == pytest.approx(0.15)
    assert e["mouth_throat_mm"] >= 5.8
    assert e["insertion_approach_length_mm"] >= 7.0


def test_04_r4_lap_contact_remains_above_floor():
    assert validation.lap_evidence()["minimum_contact_area_mm2"] >= SPEC.minimum_lap_contact_area_mm2


def test_05_raised_receiver_stack_and_top_only_m3x8_math():
    e = validation.rail_stack_evidence()
    assert e["channel_z_mm"] == pytest.approx((-27.5, -24.5))
    assert e["roof_top_z_mm"] == pytest.approx(-22.3)
    assert e["web_above_split_mm"] == pytest.approx(1.0)
    assert e["solid_below_channel_mm"] == pytest.approx(4.0)
    assert e["solid_below_tip_mm"] == pytest.approx(3.75)
    assert e["motor_channel_length_mm"] >= 12.1
    assert e["motor_external_length_mm"] >= 14.1
    assert e["sidewall_mm"] >= 2.0
    assert e["nut_channel_clearance_mm"] == pytest.approx(0.3)
    assert e["mouth_throat_mm"] >= 5.8
    assert e["screw_tip_z_mm"] == pytest.approx(-27.3)
    assert e["screw_after_nut_mm"] == pytest.approx(0.4)
    assert e["tip_channel_clearance_mm"] == pytest.approx(0.2)
    assert e["top_only"] is True


def test_06_all_three_sled_station_sweeps_and_top_removal():
    e = validation.service_sweep_evidence()
    assert len(e["rows"]) == 9
    assert e["all_valid_one_solid"] is True
    assert e["maximum_lifted_removal_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["maximum_seated_base_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["guide_clearance_per_side_mm"] == pytest.approx(0.20)
    assert len(e["shoulder_rows"]) == 18
    assert e["minimum_actual_shoulder_clearance_mm"] >= 0.15
    assert e["maximum_actual_shoulder_clearance_mm"] <= 0.25


def test_07_output_witness_driver_and_ring_envelopes():
    e = validation.service_sweep_evidence()
    assert e["output_overhang_mm"] == pytest.approx(13.0)
    assert e["load_boss_radius_at_qmax_mm"] < e["ring_witness_radius_mm"]
    assert e["driver_envelope_max_radius_mm"] < e["ring_witness_radius_mm"]


def test_08_risers_are_fused_and_reach_interface_plane():
    e = validation.riser_and_bed_evidence()
    assert e["all_risers_fused_valid"] is True
    assert e["maximum_seated_riser_distance_mm"] <= 1e-7
    assert all(row["top_z_mm"] == pytest.approx(-5.2) for row in e["riser_rows"])
    assert e["interface_plane_z_mm"] == pytest.approx(-5.2)
    assert e["rise_mm"] == pytest.approx(17.1)
    assert len(e["tool_rows"]) == 4
    assert e["maximum_screw_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert e["maximum_driver_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_09_all_print_objects_are_on_bed_and_fit_u1():
    e = validation.riser_and_bed_evidence()
    assert e["all_on_bed"] is True
    assert e["all_fit_u1"] is True
    assert e["quadrant_bottom_z_mm"] == pytest.approx((-31.5,) * 4)


def test_10_exactly_seven_model_only_3mf_objects():
    e = export.fresh_lib3mf_import_evidence()
    assert e["object_count"] == e["build_item_count"] == 7
    assert e["all_nonempty"] is True
    assert e["all_manifold_and_oriented"] is True
    assert e["unique_names"] is True


def test_11_step_source_export_parity():
    e = export.source_export_parity_evidence()
    assert e["all_required_exist"] is True
    assert e["all_solid_counts_equal"] is True
    assert e["all_written_valid"] is True
    assert e["maximum_bounds_error_mm"] <= 1e-6
    assert e["maximum_volume_error_mm3"] <= 1e-4


def test_12_physical_proof_boundary_and_drive_stop():
    e = validation.physical_validation_boundary()
    assert e["cad_acceptance_only"] is True
    assert len(e["still_requires_print"]) == 4
    assert e["drive_components_authorized"] is False
