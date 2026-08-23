import json
import subprocess
import sys

import p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_export as export
import p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_validation as validation
from p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_spec import SPEC


EPS = 1e-6


def _fresh(function_name):
    script = (
        "import json;"
        "import p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_validation as v;"
        f"print(json.dumps(v.{function_name}(),default=list))"
    )
    result = subprocess.run([sys.executable, "-c", script], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def test_predecessors_are_byte_frozen():
    assert validation.immutable_predecessor_evidence()["all_unchanged"]


def test_exactly_four_valid_printed_solids_and_no_sensor_geometry():
    evidence = validation.printable_registry_evidence()
    assert evidence["printed_object_count"] == 4
    assert evidence["all_one_solid_valid"]
    assert evidence["all_on_print_datum"]
    assert evidence["gauge_label_present"]
    assert evidence["prohibited_geometry_labels"] == ()


def test_shared_b3_axes_and_revised_capture_locator():
    axes = validation.mount_axis_and_ear_evidence()
    assert axes["maximum_axis_delta_mm"] <= SPEC.axis_tolerance_mm
    assert abs(axes["ear_thickness_mm"] - 0.20) <= EPS
    assert axes["tower_z_change_mm"] == 0.0
    rollers = validation.ear_to_stationary_roller_evidence()
    assert rollers["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert rollers["minimum_distance_mm"] + EPS >= SPEC.stationary_roller_clearance_mm


def test_stationary_q_states_and_exact_pinions_clear():
    assert _fresh("stationary_q_evidence")["all_unexpected_clear"]
    pinions = _fresh("exact_pinion_q_evidence")
    assert pinions["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_target_lower_ring_and_fin_clearances():
    evidence = _fresh("ring_clearance_evidence")
    assert evidence["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert evidence["minimum_target_distance_mm"] + EPS >= SPEC.target_ring_clearance_min_mm
    assert evidence["minimum_lower_distance_mm"] + EPS >= SPEC.lower_ring_clearance_min_mm
    assert evidence["minimum_fin_distance_mm"] + EPS >= SPEC.fin_clearance_min_mm


def test_representative_seam_and_magnet_poses_clear():
    evidence = _fresh("representative_moving_feature_evidence")
    assert evidence["pose_count"] == 18
    assert evidence["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_slot_endpoints_nominal_and_passive_datum():
    evidence = validation.insertion_and_active_datum_evidence()
    assert evidence["all_slot_positions_within_travel"]
    assert evidence["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert abs(evidence["centered_insertion_clearance_each_side_mm"] - 0.10) <= EPS
    assert evidence["centered_retained_overlap_total_mm"] + EPS >= 0.20
    assert evidence["full_channel_side_float_one_lip_retention_mm"] + EPS >= 0.20


def test_receiver_hardware_stack_and_driver_clear():
    evidence = validation.hardware_stack_evidence()
    assert evidence["maximum_unintended_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert evidence["tip_projection_mm"] <= evidence["tip_well_depth_mm"]
    assert evidence["blind_floor_clearance_mm"] + EPS >= 0.20


def test_u1_and_physical_boundary():
    assert validation.u1_printability_evidence()["all_fit_u1"]
    boundary = validation.physical_boundary()
    assert boundary["printed_object_count"] == 4
    assert boundary["sensor_or_electronics_geometry_present"] is False
    assert boundary["sensing_claim"] is False


def test_exported_artifacts_when_present():
    if not all(path.is_file() for path in export.required_artifact_paths()):
        return
    three_mf = export.fresh_lib3mf_import_evidence()
    assert three_mf["object_count"] == three_mf["build_item_count"] == 4
    assert three_mf["all_nonempty"] and three_mf["all_manifold_and_oriented"] and three_mf["unique_names"]
    parity = export.source_export_parity_evidence()
    assert parity["all_labels_equal"]
    assert parity["all_solid_counts_equal"]
    assert parity["all_written_valid_positive"]
    assert parity["maximum_bounds_error_mm"] <= EPS
    assert parity["maximum_volume_error_mm3"] <= 1e-3
