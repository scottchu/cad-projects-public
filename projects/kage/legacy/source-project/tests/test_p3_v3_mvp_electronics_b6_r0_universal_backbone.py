import json
import subprocess
import sys

import p3_v3_mvp_electronics_b6_r0_universal_backbone_export as export
import p3_v3_mvp_electronics_b6_r0_universal_backbone_validation as validation
from p3_v3_mvp_electronics_b6_r0_universal_backbone_spec import SPEC


EPS = 1e-6


def _fresh(function_name):
    script = (
        "import json;"
        "import p3_v3_mvp_electronics_b6_r0_universal_backbone_validation as v;"
        f"print(json.dumps(v.{function_name}(),default=list))"
    )
    result = subprocess.run([sys.executable, "-c", script], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def test_all_accepted_predecessors_are_byte_frozen():
    assert validation.immutable_predecessor_evidence()["all_unchanged"]


def test_exactly_one_valid_backbone_fits_print_bed_and_keeps_center_empty():
    evidence = validation.backbone_registry_evidence()
    assert evidence["printed_object_count"] == evidence["solid_count"] == 1
    assert evidence["valid_positive"]
    assert evidence["fits_260_square_with_brim"]
    assert evidence["flat_main_underside"]
    assert evidence["empty_optical_center_radius_mm"] == 68.0


def test_eight_r4_axes_and_shared_m3x8_stack():
    evidence = validation.seam_axis_and_hardware_evidence()
    assert evidence["axis_count"] == 8
    assert evidence["maximum_axis_delta_mm"] <= SPEC.axis_tolerance_mm
    assert evidence["m3x8_witness_count"] == evidence["washer_witness_count"] == 8
    assert evidence["engagement_mm"] + EPS >= SPEC.m3_engagement_min_mm
    assert evidence["tip_above_underside_mm"] + EPS >= SPEC.screw_tip_above_underside_min_mm
    assert evidence["maximum_backbone_hardware_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_universal_slots_side_load_nuts_and_replaceable_envelopes():
    evidence = validation.universal_interface_evidence()
    assert evidence["slot_count"] == evidence["side_load_nut_count"] == 14
    assert evidence["all_nuts_clear_printed_backbone"]
    assert evidence["minimum_board_gap_mm"] + EPS >= SPEC.board_gap_min_mm
    assert evidence["board_specific_hole_patterns"] == 0
    assert evidence["slot_size_mm"] == (3.4, 12.0)


def test_stationary_predecessors_and_three_ring_sweeps_clear():
    stationary = _fresh("stationary_predecessor_collision_evidence")
    assert stationary["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    rings = _fresh("ring_360_sweep_clearance_evidence")
    assert rings["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert rings["minimum_clearance_mm"] + EPS >= SPEC.ring_clearance_min_mm


def test_b2_sled_service_range_and_exact_pinions_clear():
    evidence = _fresh("motor_sled_and_b2r3_collision_evidence")
    assert evidence["pose_count"] == 15
    assert evidence["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_wiring_thermal_antenna_and_sequential_insertions():
    cable = validation.thermal_antenna_and_cable_evidence()
    assert cable["driver_to_led_heatsink_clearance_mm"] + EPS >= SPEC.led_driver_to_heatsink_min_mm
    assert cable["high_current_to_logic_trunk_clearance_mm"] + EPS >= SPEC.trunk_separation_min_mm
    assert cable["high_current_to_motor_branch_clearance_mm"] + EPS >= SPEC.trunk_separation_min_mm
    assert cable["antenna_backbone_intersection_mm3"] <= SPEC.brep_tolerance_mm3
    assert cable["open_channel_cross_section_mm"] == (6.0, 3.0)
    assert cable["general_bend_radius_mm"] >= 10.0
    assert cable["led_bend_radius_mm"] >= 15.0
    assert cable["led_service_loop_mm"] >= 80.0
    assert cable["motor_branch_loop_mm"] >= 25.0
    insertion = _fresh("sequential_insertion_evidence")
    assert insertion["pose_count"] == 21
    assert insertion["maximum_intersection_mm3"] <= SPEC.brep_tolerance_mm3


def test_exact_assembly_order_and_exported_artifacts_when_present():
    if export.EXPLODED_STEP.is_file():
        order = _fresh("assembly_order_evidence")
        assert all(order["required_steps_present"].values())
        assert order["strictly_ordered"] and order["b4_last"]
    if not all(path.is_file() for path in export.required_artifact_paths()):
        return
    three_mf = export.fresh_lib3mf_import_evidence()
    assert three_mf["object_count"] == three_mf["build_item_count"] == 1
    assert three_mf["all_nonempty"] and three_mf["all_manifold_and_oriented"] and three_mf["unique_names"]
    parity = export.source_export_parity_evidence()
    assert parity["all_solid_counts_equal"] and parity["all_written_valid_positive"]
    assert parity["maximum_bounds_error_mm"] <= EPS
    assert parity["maximum_volume_error_mm3"] <= 1e-3
