"""Focused B0 gates: real solids, real interfaces, paths, and bad fixtures."""

from __future__ import annotations

from pathlib import Path
import re

from build123d import import_step
import pytest

import p3_v3_mvp_base_q4_r1_export as export
import p3_v3_mvp_base_q4_r1_geometry as geometry
import p3_v3_mvp_base_q4_r1_validation as validation
from p3_v3_mvp_base_q4_r1_spec import MODEL_ROOT, NAMESPACE, SPEC, frozen_input_evidence


ROOT = Path(__file__).resolve().parents[1]


def test_01_frozen_handoffs_and_reconciled_scope_are_exact():
    assert frozen_input_evidence()["all_frozen_hashes_match"] is True
    assert SPEC.base_outer_radius_mm == 150.0
    assert SPEC.base_inner_radius_mm == 66.0
    assert SPEC.base_thickness_mm == 2.5
    assert SPEC.seam_base_angle_deg == 45.0
    assert SPEC.seam_gap_nominal_mm == pytest.approx(0.10)
    assert SPEC.bridge_count_total == 4
    assert (SPEC.bridge_radial_min_mm, SPEC.bridge_radial_max_mm) == (69.0, 117.0)
    assert SPEC.bridge_center_radius_mm == SPEC.screw_axis_radius_mm == 93.0
    assert SPEC.screw_tangent_offsets_mm == (-7.0, 7.0)
    assert SPEC.dowel_axis_radii_mm == (78.0, 108.0)
    assert SPEC.legacy_mount_voids_enabled is False


def test_02_each_printed_body_is_one_solid_and_fits_u1_with_five_mm_brim():
    evidence = validation.topology_and_bed_evidence()
    assert evidence["printable_body_count"] == 8
    assert evidence["quadrant_count"] == 4
    assert evidence["bridge_count"] == 4
    assert evidence["all_one_solid_valid_positive"] is True
    assert evidence["all_bed_contained_with_brim"] is True
    assert evidence["maximum_raw_span_mm"] == pytest.approx(212.061311893, abs=1e-6)
    assert evidence["maximum_brim_span_mm"] == pytest.approx(222.061311893, abs=1e-6)
    assert max(row["placed_z_floor_error_mm"] for row in evidence["rows"]) <= 1e-7


def test_03_assembled_od_id_z_and_all_functional_planes_are_coplanar():
    evidence = validation.assembled_datum_evidence()
    assert evidence["base_bounds_mm"] == pytest.approx((-150.0, -150.0, 0.0, 150.0, 150.0, 2.5), abs=1e-7)
    assert evidence["full_assembly_bounds_mm"] == pytest.approx((-150.0, -150.0, -5.0, 150.0, 150.0, 2.5), abs=1e-7)
    assert evidence["outer_diameter_x_mm"] == pytest.approx(300.0)
    assert evidence["outer_diameter_y_mm"] == pytest.approx(300.0)
    assert evidence["inner_radius_from_center_mm"] == pytest.approx(66.0)
    assert evidence["quadrant_front_coplanarity_range_mm"] <= SPEC.coplanarity_tolerance_mm
    assert evidence["bridge_seat_coplanarity_range_mm"] <= SPEC.coplanarity_tolerance_mm
    assert evidence["bridge_bottom_coplanarity_range_mm"] <= SPEC.coplanarity_tolerance_mm


def test_04_all_four_seams_have_real_point_one_gap_and_zero_overlap():
    evidence = validation.seam_evidence()
    assert len(evidence["rows"]) == 4
    assert evidence["maximum_intersection_volume_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["minimum_gap_mm"] == pytest.approx(SPEC.seam_gap_nominal_mm, abs=1e-7)
    assert evidence["maximum_gap_mm"] == pytest.approx(SPEC.seam_gap_nominal_mm, abs=1e-7)
    assert evidence["actual_face_measurement_count"] == 24
    assert evidence["intentionally_nonface_measurement_count"] == 8
    assert evidence["minimum_actual_face_gap_mm"] == pytest.approx(SPEC.seam_gap_nominal_mm, abs=1e-7)
    assert evidence["maximum_actual_face_gap_mm"] == pytest.approx(SPEC.seam_gap_nominal_mm, abs=1e-7)
    assert all(
        sample["measurement_status"] == "actual_brep_face_gap"
        and sample["normal_gap_mm"] == pytest.approx(SPEC.seam_gap_nominal_mm, abs=1e-7)
        for row in evidence["rows"]
        for sample in row["face_samples"]
    )
    assert all(
        sample["measurement_status"] == "intentionally_non_face_dowel_void"
        and sample["normal_gap_mm"] is None
        for row in evidence["rows"]
        for sample in row["nonface_samples"]
    )


def test_05_bridge_footprints_and_all_joinery_leave_r118_to_r150_untouched():
    evidence = validation.future_support_keepout_evidence()
    assert evidence["keepout_radius_range_mm"] == (118.0, 150.0)
    assert evidence["maximum_removed_volume_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["maximum_bridge_vertex_radius_mm"] < SPEC.future_support_clear_radius_min_mm
    assert evidence["joinery_clearance_to_keepout_mm"] > 0.0


def test_06_real_bridge_contacts_hardware_voids_engagement_and_driver_access_pass():
    evidence = validation.bridge_contact_and_hardware_evidence()
    assert evidence["bridge_dimensions_mm"] == pytest.approx((48.0, 26.0, 5.0))
    assert evidence["bridge_solid_count"] == 1
    assert evidence["bridge_is_valid"] is True
    assert evidence["screw_interface_count"] == 8
    assert evidence["dowel_interface_count"] == 8
    assert evidence["maximum_contact_distance_mm"] <= 1e-7
    assert evidence["maximum_void_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["maximum_pin_base_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["maximum_press_intersection_error_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert evidence["nut_pocket_depth_mm"] == pytest.approx(2.70)
    assert evidence["nut_axial_slack_mm"] == pytest.approx(0.30)
    assert evidence["press_engagement_mm"] == pytest.approx(3.50)
    assert evidence["base_slip_engagement_mm"] == pytest.approx(2.50)
    assert evidence["dowel_diametral_slip_mm"] == pytest.approx(0.15)
    assert evidence["minimum_round_pin_base_clearance_mm"] == pytest.approx(0.075, abs=1e-7)
    assert evidence["minimum_relief_pin_base_clearance_mm"] == pytest.approx(0.075, abs=1e-7)
    slot = evidence["relief_slot_brep"]["production_true_capsule"]
    assert slot["overall_actual_brep_radial_length_mm"] == pytest.approx(5.15, abs=1e-7)
    assert slot["overall_actual_brep_tangential_width_mm"] == pytest.approx(4.15, abs=1e-7)
    assert slot["minimum_actual_brep_tangential_width_mm"] == pytest.approx(4.15, abs=1e-7)
    assert slot["minimum_d4_pin_side_clearance_mm"] == pytest.approx(0.075, abs=1e-7)
    assert slot["qualifies_constant_width_slot"] is True
    rejected = evidence["relief_slot_brep"]["rejected_two_lobed_regression"]
    assert rejected["minimum_actual_brep_tangential_width_mm"] < 4.03
    assert rejected["minimum_d4_pin_side_clearance_mm"] < 0.015
    assert rejected["qualifies_constant_width_slot"] is False
    assert evidence["screw_tip_beyond_base_and_nut_mm"] == pytest.approx(1.10)
    assert evidence["screw_tip_relief_depth_mm"] >= evidence["screw_tip_beyond_base_and_nut_mm"]
    assert evidence["bridge_bottom_skin_mm"] == pytest.approx(1.00)
    assert evidence["nut_radial_wall_mm"] > 20.0
    assert evidence["nut_to_nearest_dowel_ligament_mm"] > 9.0
    assert evidence["tangential_end_wall_mm"] > 2.6


def test_07_same_fixture_gate_passes_nominal_and_rejects_two_deliberate_negatives():
    production = validation.production_fixture_evidence()
    bad = validation.deliberate_bad_fixture_evidence()
    assert production["fixture_pass"] is True
    shim = bad["shim_seam_4"]
    assert shim["fixture_pass"] is False
    assert shim["z_coplanarity_pass"] is False
    assert shim["all_seat_contacts_pass"] is False
    assert shim["bridge_bottom_coplanarity_mm"] == pytest.approx(0.50)
    radial = bad["radial_axis_offset_seam_4"]
    assert radial["fixture_pass"] is False
    assert radial["all_dowel_axes_pass"] is False
    assert radial["maximum_dowel_axis_error_mm"] == pytest.approx(0.50)


def test_07b_final_bridge_inserts_upward_but_attached_last_quadrant_lowering_fails():
    evidence = validation.final_bridge_assembly_path_evidence()
    approved = evidence["approved_final_bridge_upward"]
    assert approved["sequence"] == "support_all_four_quadrants_preattach_S1_S2_S3_insert_S4_upward"
    assert approved["final_bridge_seam_index"] == 4
    assert approved["preattached_bridge_indices"] == (1, 2, 3)
    assert approved["path_z_offsets_mm"][0] == pytest.approx(-3.0)
    assert approved["path_z_offsets_mm"][-1] == pytest.approx(0.0)
    assert approved["start_pin_top_clearance_below_quadrants_mm"] == pytest.approx(0.50)
    assert approved["maximum_sample_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert approved["continuous_bridge_swept_solid_intersection_mm3"] <= SPEC.brep_intersection_tolerance_mm3
    assert max(approved["continuous_exact_pin_swept_solid_intersections_mm3"]) <= SPEC.brep_intersection_tolerance_mm3
    assert approved["path_clear"] is True

    rejected = evidence["rejected_last_quadrant_vertical_lowering"]
    assert rejected["sequence"] == "lower_Q4_with_S4_and_both_pins_attached"
    assert rejected["path_z_offsets_mm"][0] == pytest.approx(8.0)
    assert rejected["path_z_offsets_mm"][-1] == pytest.approx(0.0)
    assert rejected["start_bridge_clearance_above_fixed_quadrants_mm"] == pytest.approx(0.50)
    assert rejected["first_collision_z_offset_mm"] == pytest.approx(7.25)
    assert rejected["collision_sample_count"] > 0
    assert rejected["maximum_attached_bridge_intersection_mm3"] > 1000.0
    assert rejected["path_clear"] is False


def test_08_successor_registry_is_exactly_eight_printed_bodies_and_no_forbidden_systems():
    rows = geometry.printable_occurrences()
    assert len(rows) == SPEC.printable_body_count == 8
    assert len({row["label"] for row in rows}) == 8
    assert {row["kind"] for row in rows} == {"quadrant", "bridge"}
    source = (ROOT / "p3_v3_mvp_base_q4_r1_geometry.py").read_text().lower()
    forbidden = ("motor", "pinion", "roller", "electronics", "led", "legacy_mount")
    assert not any(re.search(rf"\b{re.escape(token)}\b", source) for token in forbidden)
    assert all(NAMESPACE in str(path) for path in export.required_artifact_paths())


def test_09_every_step_artifact_imports_with_expected_solid_count_and_bounds():
    required = export.required_artifact_paths()
    assert all(path.is_file() and path.stat().st_size > 0 for path in required)
    assembled = import_step(export.ASSEMBLED_STEP)
    exploded = import_step(export.EXPLODED_STEP)
    assert len(assembled.solids()) == 8
    assert len(exploded.solids()) == 8
    size = assembled.bounding_box().size
    assert (size.X, size.Y, size.Z) == pytest.approx((300.0, 300.0, 7.5), abs=1e-6)
    for path in export.individual_step_paths():
        imported = import_step(path)
        assert len(imported.solids()) == 1, path
        assert imported.is_valid, path
        assert imported.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7), path


def test_10_model_only_3mf_is_eight_named_manifold_objects_and_no_slicer_profiles():
    path = export.MODEL_ONLY_3MF
    assert path.is_file() and path.stat().st_size > 0
    evidence = export.fresh_lib3mf_import_evidence(path)
    assert evidence["object_count"] == 8
    assert evidence["build_item_count"] == 8
    assert evidence["all_nonempty"] is True
    assert evidence["all_manifold_and_oriented"] is True
    assert evidence["unique_names"] is True
    assert all(NAMESPACE in name for name in evidence["names"])


def test_11_available_orca_cli_loads_the_model_only_3mf():
    evidence = export.orca_load_evidence()
    assert evidence["available"] is True
    assert evidence["loaded"] is True, evidence


def test_12_readme_preserves_mvp_boundary_and_physical_only_release_gates():
    text = " ".join(export.README.read_text().lower().split())
    for phrase in (
        "four-to-one",
        "visible/front face at z=0",
        "5 mm brim",
        "three complete cycles",
        "vertically under self weight",
        "free-standing front deviation",
        "r118..150",
        "cad does not prove",
        "no ring",
        "no slicer profile",
        "support all four quadrants",
        "only bridges s1, s2, and s3",
        "insert bridge s4 upward from below",
        "do not lower a last quadrant",
    ):
        assert phrase in text
    assert "loosely attach each bridge" not in text
    assert "lower the adjacent quadrant" not in text
