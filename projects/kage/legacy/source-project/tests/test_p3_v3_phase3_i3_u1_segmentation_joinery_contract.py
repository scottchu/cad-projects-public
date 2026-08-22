"""RED contract for KAGE Phase-3 I3 U1 segmentation and joinery.

The accepted I3.1 document is the sole design input.  These tests intentionally
precede the production namespace and must fail closed until the implementation
exists.  Rejected Revision-K/R2 geometry is evidence only and must never become
an implementation dependency.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, is_dataclass, replace
from hashlib import sha256
import importlib
import inspect
from math import pi, radians
from pathlib import Path
from typing import Any, Mapping

import pytest


ROOT = Path(__file__).resolve().parents[1]
ACCEPTED_SPEC = ROOT / "docs" / "p3-v3-phase3-i3-u1-segmentation-joinery-accepted-spec.md"
ACCEPTED_SPEC_SHA256 = "abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77"
FROZEN_STEP = (
    ROOT
    / "models"
    / "p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention"
    / "p3_v3_r1_i1_fixed_tower_retention_assembled.step"
)
FROZEN_STEP_SHA256 = "8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724"
MODEL_ROOT = ROOT / "models" / "p3_v3_phase3_i3_u1_segmentation_joinery"

SPEC_MODULE = "p3_v3_phase3_i3_u1_segmentation_joinery_spec"
GEOMETRY_MODULE = "p3_v3_phase3_i3_u1_segmentation_joinery_geometry"
PARITY_MODULE = "p3_v3_phase3_i3_u1_segmentation_joinery_parity"
EXPORT_MODULE = "p3_v3_phase3_i3_u1_segmentation_joinery_export"

EXPECTED_DEFAULTS = {
    "u1_nominal_xy_mm": 270.0,
    "u1_edge_keepout_mm": 5.0,
    "u1_usable_xy_mm": 260.0,
    "fallback_raw_bed_xy_mm": 260.0,
    "fallback_usable_xy_mm": 250.0,
    "moving_half_raw_xy_max_mm": 244.864483,
    "moving_brim_nominal_mm": 3.5,
    "moving_brim_fallback_max_mm": 3.5,
    "ring_teeth": 260,
    "moving_segment_count_per_role": 2,
    "moving_segment_teeth": 130,
    "stationary_segment_count_per_family": 4,
    "moving_seam_base_deg": 15.230769230769,
    "stationary_seam_base_deg": 37.5,
    "moving_join_radii_mm": (133.5, 140.0),
    "moving_join_tangent_length_mm": 16.0,
    "moving_lower_lap_mm": 2.0,
    "moving_upper_lap_mm": 1.0,
    "lap_xy_clearance_mm": 0.10,
    "lap_z_clearance_mm": 0.08,
    "seam_face_relief_mm": 0.025,
    "seam_gap_target_mm": 0.05,
    "seam_gap_range_mm": (0.03, 0.10),
    "seam_step_target_mm": 0.10,
    "seam_step_hard_max_mm": 0.15,
    "tooth_phase_tangent_max_mm": 0.10,
    "race_tir_target_mm": 0.15,
    "race_tir_hard_max_mm": 0.20,
    "race_pitch_concentricity_max_mm": 0.10,
}

ROLES = ("hour", "minute", "second")
STATIONARY_FAMILIES = ("rear_chassis", "stationary_frame", "outer_front_ring")
EXPECTED_HARDWARE_TOTALS = {"bridges": 16, "screws": 44, "nuts": 44, "dowels": 22}
EXPECTED_ARTIFACTS = {
    "assembled_nominal.step",
    "service_exploded.step",
    "print_components.3mf",
    "source_import_parity_manifest.json",
    "purchased_hardware_bom.json",
    "assembly_state_manifest.json",
    "plate_manifest.json",
}


def _load(name: str):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            pytest.fail(f"RED: isolated I3 production module {name!r} does not exist", pytrace=False)
        raise


def _spec_module():
    module = _load(SPEC_MODULE)
    assert Path(module.__file__).resolve().parent == ROOT
    return module


def _geometry_module():
    module = _load(GEOMETRY_MODULE)
    assert Path(module.__file__).resolve().parent == ROOT
    return module


def _parity_module():
    module = _load(PARITY_MODULE)
    assert Path(module.__file__).resolve().parent == ROOT
    return module


def _export_module():
    module = _load(EXPORT_MODULE)
    assert Path(module.__file__).resolve().parent == ROOT
    return module


def _params():
    return _spec_module().P3_V3_PHASE3_I3_U1_SEGMENTATION_JOINERY


def _meta(value: Any, key: str) -> Any:
    return value[key] if isinstance(value, Mapping) else getattr(value, key)


def _volume(shape) -> float:
    return float(sum(solid.volume for solid in shape.solids()))


def test_i3_is_anchored_to_exact_accepted_spec_and_frozen_phase2a_step():
    assert sha256(ACCEPTED_SPEC.read_bytes()).hexdigest() == ACCEPTED_SPEC_SHA256
    assert sha256(FROZEN_STEP.read_bytes()).hexdigest() == FROZEN_STEP_SHA256
    assert MODEL_ROOT != FROZEN_STEP.parent


def test_isolated_namespace_forbids_rejected_r2_and_hand_edited_exports():
    forbidden = (
        "p3_v3_direct_gear_race_guidance_r2_geometry",
        "p3_v3_full_ring_r2_geometry",
        "/rollback/",
        "import *",
        "export_step(",
    )
    for module in (_spec_module(), _geometry_module(), _parity_module()):
        source = inspect.getsource(module)
        assert not any(token in source for token in forbidden)


def test_i3_parameter_group_is_frozen_complete_exact_and_named():
    p = _params()
    assert is_dataclass(p) and getattr(p, "__dataclass_params__").frozen
    assert {field.name for field in fields(p)} == set(EXPECTED_DEFAULTS)
    for name, expected in EXPECTED_DEFAULTS.items():
        actual = getattr(p, name)
        assert actual == pytest.approx(expected)
    with pytest.raises(FrozenInstanceError):
        p.ring_teeth = 261
    assert _spec_module().OWNER_GROUP == "phase3_i3_u1_segmentation_joinery"


def test_i3_parameter_schema_has_one_owned_contract_per_normative_variable():
    schema = _spec_module().parameter_schema(_params())
    assert set(schema) == set(EXPECTED_DEFAULTS)
    for name, contract in schema.items():
        assert _meta(contract, "path") == name
        assert _meta(contract, "owner_group") == "phase3_i3_u1_segmentation_joinery"
        assert _meta(contract, "units") in {"mm", "deg", "count"}
        assert _meta(contract, "probe_value") is not None


def test_tooth_lattice_and_hybrid_segment_equations_are_exact():
    p = _params()
    assert p.tooth_pitch_deg == pytest.approx(360.0 / 260.0)
    assert p.tooth_pitch_arc_mm == pytest.approx(2.0 * pi * 130.0 / 260.0)
    assert p.moving_seam_base_deg == pytest.approx(11.0 * p.tooth_pitch_deg)
    assert p.moving_seam_angles_deg == pytest.approx((15.230769230769, 195.230769230769))
    assert p.moving_segment_teeth * p.moving_segment_count_per_role == p.ring_teeth
    assert p.stationary_seam_angles_deg == pytest.approx((37.5, 127.5, 217.5, 307.5))


def test_bed_and_brim_equations_match_both_u1_profiles():
    p = _params()
    assert p.u1_nominal_xy_mm - 2 * p.u1_edge_keepout_mm == pytest.approx(p.u1_usable_xy_mm)
    assert p.fallback_raw_bed_xy_mm - 2 * p.u1_edge_keepout_mm == pytest.approx(p.fallback_usable_xy_mm)
    assert p.moving_half_raw_xy_max_mm + 2 * p.moving_brim_nominal_mm == pytest.approx(251.864483)
    assert p.moving_half_raw_xy_max_mm + 2 * p.moving_brim_fallback_max_mm == pytest.approx(251.864483)
    assert p.moving_nominal_packed_xy_mm < p.u1_usable_xy_mm
    assert p.moving_fallback_packed_xy_mm > p.fallback_usable_xy_mm


def test_moving_joint_ligament_and_stack_equations_are_exact():
    p = _params()
    assert p.moving_nut_radial_wall_mm == pytest.approx(1.15)
    assert p.moving_nut_to_dowel_ligament_mm == pytest.approx(1.35)
    assert p.moving_tangential_end_wall_mm == pytest.approx(0.90)
    assert p.moving_tooth_root_setback_mm == pytest.approx(1.00)
    assert p.moving_m2_screw_stack_mm == pytest.approx(3.00)
    assert p.moving_screw_head_adjacent_clearance_mm == pytest.approx(1.27)
    assert p.moving_screw_head_adjacent_clearance_mm >= 1.25


def test_stationary_joint_stack_and_ligament_equations_are_exact():
    p = _spec_module().P3_V3_PHASE3_I3_HARDWARE
    assert p.chassis_m3_stack_mm == pytest.approx(5.0)
    assert p.frame_m2_stack_mm == pytest.approx(4.0)
    assert p.front_ring_m2_stack_mm == pytest.approx(3.0)
    assert p.frame_inner_radial_ligament_mm == pytest.approx(1.2)
    assert p.frame_front_hour_fin_clearance_mm == pytest.approx(0.60)


@pytest.mark.parametrize(
    "field_name,bad_value,phrase",
    (
        ("moving_segment_count_per_role", 3, "integer tooth allocation"),
        ("stationary_segment_count_per_family", 2, "stationary semicircles"),
        ("moving_join_radii_mm", (133.49, 140.0), "R133.50"),
        ("moving_join_radii_mm", (133.5, 140.01), "R140.00"),
        ("moving_brim_nominal_mm", 8.0, "nominal U1 bed"),
        ("seam_gap_range_mm", (0.02, 0.10), "seam gap"),
        ("race_tir_hard_max_mm", 0.21, "race TIR"),
    ),
)
def test_normative_refusal_parameters_fail_closed(field_name, bad_value, phrase):
    candidate = replace(_params(), **{field_name: bad_value})
    with pytest.raises(ValueError, match=phrase):
        candidate.validate()


def test_candidate_registry_has_exact_hybrid_segment_counts_and_no_old_seams():
    rows = _geometry_module().candidate_occurrences()
    labels = [row["label"] for row in rows]
    for role in ROLES:
        role_halves = [label for label in labels if f"direct_race_{role}_M1_260T_I3_half_" in label]
        assert len(role_halves) == 2
        assert any("I3_half_A_130T_beta15p230769" in label for label in role_halves)
        assert any("I3_half_B_130T_beta195p230769" in label for label in role_halves)
        assert not any(f"p3_v3_r2_{role}_seam_" in label for label in labels)
    for family in STATIONARY_FAMILIES:
        assert len([label for label in labels if f"{family}_I3_beta37p5_quadrant_Q" in label]) == 4


def test_exact_label_allowlist_and_protected_occurrence_ranges_are_enforced():
    evidence = _parity_module().label_allowlist_evidence()
    assert evidence["unexpected_added_labels"] == []
    assert evidence["missing_required_labels"] == []
    assert evidence["surviving_old_seam_labels"] == []
    assert evidence["protected_label_drift"] == []
    assert evidence["protected_occurrence_count"] == 131


def test_segments_come_from_frozen_world_breps_and_reconstruct_outside_seam_rois():
    evidence = _parity_module().segment_reconstruction_evidence()
    assert evidence["moving_family_count"] == 3
    assert evidence["stationary_family_count"] == 3
    assert all(row["xor_outside_seam_mm3"] <= 1e-7 for row in evidence["families"])
    assert all(row["source_method"] == "frozen_world_brep_intersection" for row in evidence["families"])


def test_moving_halves_have_130_teeth_each_and_joinery_stays_outside_functional_surfaces():
    evidence = _geometry_module().moving_half_actual_solid_evidence()
    assert len(evidence) == 6
    for row in evidence:
        assert row["tooth_count"] == 130
        assert row["join_radius_min_mm"] >= 133.50
        assert row["join_radius_max_mm"] <= 140.00
        assert row["race_intersection_mm3"] <= 1e-7
        assert row["active_tooth_flank_intersection_mm3"] <= 1e-7


def test_each_moving_seam_has_integral_laps_two_real_screws_two_nuts_and_one_dowel():
    evidence = _geometry_module().moving_joinery_evidence()
    assert len(evidence) == 6
    for row in evidence:
        assert row["lower_lap_thickness_mm"] == pytest.approx(2.0)
        assert row["upper_lap_thickness_mm"] == pytest.approx(1.0)
        assert row["xy_clearance_mm"] == pytest.approx(0.10)
        assert row["z_clearance_mm"] == pytest.approx(0.08)
        assert row["seam_face_relief_mm"] == pytest.approx(0.025)
        assert row["screw_count"] == 2 and row["nut_count"] == 2 and row["dowel_count"] == 1
        assert row["nut_pocket_mm"] == pytest.approx((4.2, 4.2, 1.7))
        assert row["lower_press_bore_diameter_mm"] == pytest.approx(2.95)
        assert row["upper_slip_bore_diameter_mm"] == pytest.approx(3.10)


def test_all_moving_driver_nut_and_dowel_loading_paths_are_actual_solid_clear():
    evidence = _geometry_module().moving_loading_path_evidence()
    assert evidence["driver_path_count"] == 12
    assert evidence["nut_loading_path_count"] == 12
    assert evidence["dowel_path_count"] == 6
    assert evidence["maximum_preassembly_intersection_mm3"] <= 1e-7
    assert evidence["all_nuts_captured_after_closure"] is True
    assert evidence["maximum_slip_diametral_clearance_mm"] <= 0.12


def test_stationary_joinery_has_exact_bridges_hardware_and_loading_paths():
    evidence = _geometry_module().stationary_joinery_evidence()
    assert evidence["rear_chassis"] == {"bridges": 8, "screws": 16, "nuts": 16, "dowels": 8}
    assert evidence["stationary_frame"] == {"bridges": 4, "screws": 8, "nuts": 8, "dowels": 4}
    assert evidence["outer_front_ring"] == {"bridges": 4, "screws": 8, "nuts": 8, "dowels": 4}
    assert evidence["totals"] == EXPECTED_HARDWARE_TOTALS
    assert evidence["maximum_preassembly_tool_intersection_mm3"] <= 1e-7
    assert evidence["all_nuts_captured_after_closure"] is True
    assert evidence["minimum_hour_fin_radial_clearance_mm"] >= 0.60


def test_hardware_registry_and_bom_have_exact_nonduplicated_totals():
    registry = _geometry_module().hardware_registry()
    assert len({row["label"] for row in registry}) == len(registry)
    totals = {key: sum(row["kind"] == key[:-1] for row in registry) for key in ("bridges", "screws", "nuts", "dowels")}
    assert totals == EXPECTED_HARDWARE_TOTALS
    assert all(row["classification"] in {"printed", "purchased"} for row in registry)


def test_tooth_phase_race_sampling_and_full_motion_sweep_pass_actual_solids():
    phase = _geometry_module().tooth_phase_and_race_evidence()
    assert phase["assembled_ring_teeth"] == {role: 260 for role in ROLES}
    assert phase["maximum_tangential_phase_error_mm"] <= 0.10
    assert phase["sample_count_per_ring"] >= 1040
    assert phase["maximum_cad_race_tir_mm"] <= 0.02
    motion = _geometry_module().full_motion_sweep_evidence()
    assert motion["roles"] == 3 and motion["seams"] == 6
    assert motion["tooth_positions"] == 260
    assert motion["seam_offset_count"] == 3
    assert motion["motor_q_count"] == 3
    assert motion["tower_q_count"] == 3
    assert motion["tested_pinion_count"] == 3 and motion["tested_roller_count"] == 9
    assert motion["maximum_unintended_intersection_mm3"] <= 1e-7


def test_source_export_parity_and_locked_silhouette_are_exact_outside_i3_rois():
    evidence = _parity_module().source_import_and_silhouette_evidence()
    assert evidence["global_bounds_mm"] == pytest.approx((-150, -150, -32.5, 150, 150, 24.2514))
    assert evidence["protected_label_drift"] == []
    assert evidence["protected_topology_drift"] == []
    assert evidence["protected_transform_drift"] == []
    assert evidence["protected_brep_digest_drift"] == []
    assert evidence["four_connected_outer_contour_xor_pixels"] == 0
    assert evidence["eight_connected_outer_contour_xor_pixels"] == 0
    assert evidence["changes_outside_named_i3_rois_pixels"] == 0


def test_plate_registry_contains_one_moving_half_per_plate_and_full_envelopes_fit():
    manifest = _export_module().build_plate_manifest(write=False)
    moving_rows = [row for row in manifest["plates"] if row["family"] == "moving_half"]
    assert len(moving_rows) == 6
    assert all(row["occurrence_count"] == 1 for row in moving_rows)
    assert all(row["contained_in_usable_bed"] for row in manifest["plates"])
    assert all(row["positive_overlap_mm3"] <= 1e-7 for row in manifest["plates"])
    for occurrence in manifest["occurrences"]:
        required = {
            "source_label", "source_brep_sha256", "material", "printer", "slicer_profile",
            "nozzle_mm", "layer_height_mm", "bed_profile_mm", "edge_keepout_mm", "brim_mm",
            "support_skirt_purge_envelope_mm", "raw_bbox_mm", "packed_bbox_mm", "plate_id",
            "source_to_print_transform", "restore_to_assembly_transform",
        }
        assert required <= set(occurrence)


def test_print_3mf_contains_only_disassembled_printable_components():
    evidence = _export_module().print_components_3mf_evidence()
    assert evidence["assembled_clock_occurrence_count"] == 0
    assert evidence["purchased_hardware_occurrence_count"] == 0
    assert evidence["moving_half_count"] == 6
    assert evidence["source_brep_hash_mismatches"] == []
    assert evidence["reload_ok"] is True


def test_required_source_owned_artifacts_and_state_manifests_exist():
    _export_module().export_i3(write=False)
    assert EXPECTED_ARTIFACTS <= {path.name for path in MODEL_ROOT.iterdir() if path.is_file()}
    states = _export_module().assembly_state_manifest(write=False)
    assert set(states) >= {
        "source_printed_segments",
        "purchased_hardware",
        "preassembled_role_rings",
        "nominal_installed_assembly",
        "service_exploded_assembly",
    }


def test_refusal_api_rejects_every_named_forbidden_condition():
    refusal = _spec_module().refusal_validator
    cases = {
        "three_moving_segments": {"moving_segment_count_per_role": 3},
        "stationary_semicircles": {"stationary_segment_count_per_family": 2},
        "off_lattice_seam": {"moving_seam_base_deg": 15.0},
        "join_inside_r133p5": {"moving_join_radii_mm": (133.4, 140.0)},
        "join_outside_r140": {"moving_join_radii_mm": (133.5, 140.1)},
        "threaded_insert": {"receiver_type": "heat_set_insert"},
        "loose_1mm_splice": {"moving_join_style": "loose_1mm_splice"},
        "oversize_nut": {"din562_m2_height_mm": 1.61},
        "stationary_join_inside_r144p5": {"stationary_join_min_radius_mm": 144.4},
        "old_cardinal_seam": {"surviving_old_seam_count": 1},
        "in_stack_seam_assembly": {"in_stack_ring_assembly": True},
        "hall_geometry": {"hall_geometry_count": 1},
        "hand_edited_export": {"source_owned_export": False},
    }
    for name, overrides in cases.items():
        with pytest.raises(ValueError, match=name):
            refusal(overrides)
