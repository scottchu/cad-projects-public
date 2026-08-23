"""Revision K RED contracts for the isolated direct-gear-race R2 model.

These tests intentionally precede the R2 implementation.  They must collect
without an R2 module, then fail with an explicit missing-module/artifact
message.  The locked non-R2 sources and exports are rollback inputs and are
never imported as an implementation fallback here.
"""

from __future__ import annotations

from collections import Counter
import importlib
import inspect
import itertools
import json
from math import isfinite
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_r2"
SPEC_MODULE = "p3_v3_direct_gear_race_guidance_r2_spec"
GEOMETRY_MODULE = "p3_v3_direct_gear_race_guidance_r2_geometry"
EXPORT_MODULE = "p3_v3_direct_gear_race_guidance_r2_export"

ROLES = ("hour", "minute", "second")
ROLE_KEYS = ("H", "M", "S")
RADIAL_SIGN_KEYS = (
    "H60", "H180", "H300",
    "M60", "M180", "M300",
    "S60", "S180", "S300",
)
AXIAL_SIGN_KEYS = ROLE_KEYS
SETUP_VALUES_MM = (-1.00, -0.75, -0.50, -0.25, 0.00, 0.25, 0.50, 0.75, 1.00)

EXPECTED_PRODUCTION_COUNTS = {
    "moving_carrier_quadrant": 12,
    "moving_recessed_seam_plate": 12,
    "rear_stationary_quadrant": 4,
    "front_stationary_quadrant": 4,
    "stationary_joint_registration_key": 16,
    "motor_yoke": 3,
    "output_pinion": 3,
    "miter_gear": 6,
    "motor_powered_window_key": 3,
    "fixed_tower_leaf": 2,
    "fixed_tower_upper_bridge": 2,
    "selected_fixed_tower_shim": 4,
    "tower_300_structural_spine": 1,
    "tower_300_role_slider_cassette": 3,
    "tower_300_three_window_stop_plate": 1,
    "role_spacer": 6,
    "hall_pocket_cap": 3,
    "balance_pocket_cap": 9,
}

FORBIDDEN_PRODUCTION_TERMS = (
    "eccentric",
    "printed_pom_roller",
    "roller_spool",
    "generic_compliant_carriage",
    "compliant_upper_bridge",
    "fixed_eccentric_tower_bar",
    "common_300_axle",
    "single_spring",
    "coupon",
    "fit_ladder",
)


def _load_module(name: str):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            pytest.fail(
                f"RED: isolated R2 module {name!r} does not exist yet; "
                "do not satisfy this with a rollback-module alias",
                pytrace=False,
            )
        raise


def _field(value, name: str):
    if isinstance(value, dict):
        assert name in value, f"missing report field {name!r}"
        return value[name]
    assert hasattr(value, name), f"missing report attribute {name!r}"
    return getattr(value, name)


def _spec():
    module = _load_module(SPEC_MODULE)
    assert hasattr(module, "P3_V3_DIRECT_GEAR_RACE_R2")
    value = module.P3_V3_DIRECT_GEAR_RACE_R2
    assert "_r2_spec.py" in Path(module.__file__).name
    return value


def _geometry():
    module = _load_module(GEOMETRY_MODULE)
    assert "_r2_geometry.py" in Path(module.__file__).name
    return module


def _assert_bounds(bounds, expected, *, tolerance=1e-6):
    assert len(bounds) == len(expected)
    assert tuple(bounds) == pytest.approx(tuple(expected), abs=tolerance)


def test_authoritative_r2_namespace_and_revision_k_spec():
    p = _spec()

    expected = {
        "clock_outer_diameter": 300.00,
        "ring_teeth": 260,
        "pinion_teeth": 16,
        "gear_module": 1.00,
        "gear_ratio": 16.25,
        "carrier_race_radius": 131.60,
        "tooth_tip_radius": 129.00,
        "tooth_root_radius": 132.50,
        "ring_body_outer_radius": 138.90,
        "stationary_outer_radius": 150.00,
        "shells_per_critical_pose": 4096,
        "motion_samples_per_revolution": 1040,
        "role_local_q_acceptance_abs_max_mm": 0.76,
        "role_local_powered_stop_abs_mm": 1.00,
        "role_local_service_stop_abs_mm": 1.25,
        "role_local_powered_margin_min_mm": 0.24,
        "fixed_axle_diameter_mm": 3.99,
        "fixed_axle_length_mm": 30.00,
        "cassette_pin_diameter_mm": 3.99,
        "cassette_pin_length_mm": 7.70,
        "production_printed_occurrence_count": 94,
    }
    for name, wanted in expected.items():
        assert getattr(p, name) == pytest.approx(wanted), name

    assert tuple(p.fixed_setup_values_mm) == pytest.approx(SETUP_VALUES_MM)
    assert p.rollback_model_root != MODEL_ROOT
    assert Path(p.model_root).name == MODEL_ROOT.name


def test_authoritative_pose_api_solves_role_local_state_and_rejects_free_ring_centres():
    g = _geometry()
    signature = inspect.signature(g.make_r2_pose)
    required = {
        "ring_angles_deg",
        "motor_q_mm",
        "fixed_setup_mm",
        "roller_axial_float_mm",
        "race_profile_error_functions",
        "race_axial_warp_functions",
        "operating_mode",
    }
    assert required <= set(signature.parameters)
    assert "ring_radial_offsets_xy_mm" not in signature.parameters
    assert "common_q_300_mm" not in signature.parameters

    zero = lambda _angle: 0.0
    pose = g.make_r2_pose(
        ring_angles_deg=(0.0, 0.0, 0.0),
        motor_q_mm=(0.0, 0.0, 0.0),
        fixed_setup_mm=(0.0, 0.0),
        roller_axial_float_mm=(0.0, 0.0, 0.0),
        race_profile_error_functions=(zero, zero, zero),
        race_axial_warp_functions=(zero, zero, zero),
        operating_mode="powered",
    )
    q = _field(pose, "role_local_q_mm")
    assert set(q) == set(ROLE_KEYS)
    assert all(isfinite(q[role]) and abs(q[role]) <= 0.76 for role in ROLE_KEYS)
    centres = _field(pose, "solved_ring_centres_xy_mm")
    assert set(centres) == set(ROLE_KEYS)
    assert len(_field(pose, "occurrences")) >= 94

    with pytest.raises(ValueError):
        g.make_r2_pose(
            ring_angles_deg=(0.0, 0.0, 0.0),
            motor_q_mm=(0.11, 0.0, 0.0),
            fixed_setup_mm=(0.0, 0.0),
            roller_axial_float_mm=(0.0, 0.0, 0.0),
            race_profile_error_functions=(zero, zero, zero),
            race_axial_warp_functions=(zero, zero, zero),
            operating_mode="powered",
        )
    unsafe = g.make_r2_pose(
        ring_angles_deg=(0.0, 0.0, 0.0),
        motor_q_mm=(2.50, 0.0, 0.0),
        fixed_setup_mm=(0.0, 0.0),
        roller_axial_float_mm=(0.0, 0.0, 0.0),
        race_profile_error_functions=(zero, zero, zero),
        race_axial_warp_functions=(zero, zero, zero),
        operating_mode="service_unpowered",
    )
    assert "UNSAFE_TO_POWER" in _field(unsafe, "label")


def test_role_local_compliant_solves_all_4096_shells_at_every_critical_pose():
    g = _geometry()
    shells = list(g.iter_revision_k_tolerance_shells())
    assert len(shells) == 4096

    radial_vectors = set()
    axial_vectors = set()
    combined = set()
    for shell in shells:
        radial = _field(shell, "radial_signs")
        axial = _field(shell, "axial_signs")
        assert tuple(radial) == RADIAL_SIGN_KEYS
        assert tuple(axial) == AXIAL_SIGN_KEYS
        radial_tuple = tuple(radial[key] for key in RADIAL_SIGN_KEYS)
        axial_tuple = tuple(axial[key] for key in AXIAL_SIGN_KEYS)
        assert set(radial_tuple) <= {-1, 1}
        assert set(axial_tuple) <= {-1, 1}
        radial_vectors.add(radial_tuple)
        axial_vectors.add(axial_tuple)
        combined.add(radial_tuple + axial_tuple)
    assert (len(radial_vectors), len(axial_vectors), len(combined)) == (512, 8, 4096)

    critical = g.critical_pose_inputs()
    assert {
        "assembled_nominal",
        "powered_min",
        "powered_max",
        "service_min_UNSAFE_TO_POWER",
        "service_max_UNSAFE_TO_POWER",
    } <= set(critical)

    for pose_name in critical:
        report = g.solve_role_local_shells(pose_name, shells)
        assert _field(report, "evaluated_shell_count") == 4096
        assert not _field(report, "failing_shells")
        worst = _field(report, "worst_passing_shell")
        q = _field(worst, "role_local_q_mm")
        force = _field(worst, "role_force_n")
        assert set(q) == set(ROLE_KEYS)
        assert set(force) == set(ROLE_KEYS)
        assert all(abs(q[key]) <= 0.76 for key in ROLE_KEYS)
        assert all(1.00 - abs(q[key]) >= 0.24 for key in ROLE_KEYS)
        assert all(0.185 <= force[key] <= 0.678 for key in ROLE_KEYS)
        assert 0.555 <= sum(force.values()) <= 2.034
        assert max(abs(value) for value in _field(worst, "contact_residuals_mm").values()) <= 0.05
        assert min(_field(worst, "flange_overlaps_mm").values()) >= 1.05


def test_discrete_fixed_setup_gate_rejects_continuous_only_intersections():
    g = _geometry()
    assert g.select_discrete_fixed_setup((0.10, 0.20), SETUP_VALUES_MM) is None
    assert g.select_discrete_fixed_setup((-1.00, -1.00), SETUP_VALUES_MM) == pytest.approx(-1.00)
    assert g.select_discrete_fixed_setup((1.00, 1.00), SETUP_VALUES_MM) == pytest.approx(1.00)

    accepted = g.validate_fixed_setup_intersection(
        measured_intervals={60: (-0.30, 0.20), 180: (0.60, 0.90)},
        setup_values_mm=SETUP_VALUES_MM,
    )
    selected = _field(accepted, "selected_setup_mm")
    assert selected[60] in (-0.25, 0.00)
    assert selected[180] == pytest.approx(0.75)
    assert max(abs(v) for v in _field(accepted, "role_residuals_mm").values()) <= 0.25


def test_fixed_axle_seat_retention_and_datum_actual_brep():
    g = _geometry()
    for station_angle, shim_index, pose_name in itertools.product(
        (60, 180), range(-4, 5), g.critical_pose_inputs()
    ):
        report = g.fixed_axle_seat_retention_and_datum_report(
            station_angle_deg=station_angle,
            shim_index=shim_index,
            pose_name=pose_name,
        )
        assert _field(report, "used_actual_brep") is True
        assert _field(report, "axle_diameter_mm") == pytest.approx(3.99)
        assert _field(report, "axle_length_mm") == pytest.approx(30.00)
        assert _field(report, "blind_seat_diameter_mm") == pytest.approx(4.05)
        assert _field(report, "blind_seat_depth_mm") == pytest.approx(3.00)
        _assert_bounds(_field(report, "blind_seat_z_mm"), (-5.20, -2.20))
        assert _field(report, "upper_bore_diameter_mm") == pytest.approx(4.06)
        _assert_bounds(_field(report, "upper_bridge_z_mm"), (16.70, 19.70))
        assert _field(report, "thrust_washer_mm") == pytest.approx((8.00, 0.15))
        assert 19.90 <= _field(report, "collar_lower_z_mm") <= 20.00
        assert _field(report, "collar_thickness_mm") == pytest.approx(4.00)
        assert _field(report, "axle_top_z_mm") == pytest.approx(24.80)
        assert 0.05 <= _field(report, "axial_endplay_mm") <= 0.15
        assert 0.80 <= _field(report, "axle_extension_mm") <= 0.90
        assert _field(report, "positive_volume_interference_mm3") <= 1e-7
        assert _field(report, "retained") is True
        assert _field(report, "service_tool_path_clear") is True


def test_cassette_pin_fit_stop_and_retention_actual_brep():
    g = _geometry()
    for role in ROLES:
        report = g.cassette_pin_fit_stop_and_retention_report(role)
        assert _field(report, "used_actual_brep") is True
        assert _field(report, "pin_mm") == pytest.approx((3.99, 7.70))
        assert _field(report, "blind_bore_mm") == pytest.approx((4.04, 4.25))
        assert _field(report, "diametral_clearance_mm") == pytest.approx(0.05)
        assert _field(report, "bottom_wall_mm") >= 1.50
        assert _field(report, "pin_contacts_blind_shoulder") is True
        assert _field(report, "exposed_stack_height_mm") == pytest.approx(3.45)
        assert _field(report, "axial_endplay_mm") == pytest.approx(0.15)
        assert _field(report, "retaining_washer_mm") == pytest.approx((6.00, 0.50, 2.20))
        assert _field(report, "m2_internal_thread_depth_mm") == pytest.approx(4.00)
        assert _field(report, "m2_screw_length_mm") == pytest.approx(4.00)
        assert _field(report, "m2_nominal_engagement_mm") == pytest.approx(3.50)
        _assert_bounds(_field(report, "pin_flat_z_mm"), (1.50, 3.50))
        assert _field(report, "pin_flat_depth_mm") == pytest.approx(0.40)
        assert _field(report, "pin_flat_clocking_error_deg") <= 2.00
        assert _field(report, "pin_flat_normal") == "-u"
        assert _field(report, "service_path_non_destructive") is True


def test_spine_stop_plate_and_adjuster_tool_paths_are_actual_solid_gates():
    g = _geometry()
    spine = g.spine_stop_plate_complete_interfaces_report()
    assert _field(spine, "used_actual_brep") is True
    _assert_bounds(_field(spine, "spine_functional_envelope_mm"), (24.00, 20.00, 21.70))
    _assert_bounds(_field(spine, "spine_z_mm"), (-5.20, 16.50))
    assert _field(spine, "mount_foot_mm") == pytest.approx((24.00, 20.00, 3.00))
    assert _field(spine, "main_back_web_radial_mm") == pytest.approx(4.00)
    assert _field(spine, "minimum_receiver_wall_mm") >= 1.50
    assert _field(spine, "mount_fastener_count") == 2
    assert _field(spine, "mount_fastener_tangent_locations_mm") == pytest.approx((-7.00, 7.00))
    assert _field(spine, "stop_plate_mm") == pytest.approx((3.00, 18.00, 20.00))
    assert _field(spine, "powered_stop_contacts_mm") == pytest.approx((-1.00, 1.00))
    assert _field(spine, "service_stop_contacts_mm") == pytest.approx((-1.25, 1.25))
    assert _field(spine, "powered_beyond_stop_interference_mm3") > 0.0
    assert _field(spine, "service_beyond_stop_interference_mm3") > 0.0
    assert _field(spine, "reversed_plate_interference_mm3") > 0.0
    assert _field(spine, "all_driver_cylinders_clear") is True

    for role, position in itertools.product(ROLES, (0.00, 1.00, 2.00)):
        adjuster = g.adjuster_tool_path_report(role, position)
        assert _field(adjuster, "used_actual_brep") is True
        assert _field(adjuster, "insert_od_length_mm") == pytest.approx((4.20, 4.00))
        assert _field(adjuster, "boss_od_mm") >= 6.60
        assert _field(adjuster, "finished_through_bore_diameter_mm") == pytest.approx(3.50, abs=0.10)
        assert _field(adjuster, "insert_engagement_mm") >= 3.00
        assert _field(adjuster, "insert_radial_ligament_mm") >= 1.20
        assert _field(adjuster, "through_bore_radial_ligament_mm") >= 1.50
        assert _field(adjuster, "d3p6_screw_path_intersection_mm3") <= 1e-7
        assert _field(adjuster, "d4x20_adjustment_tool_path_clear") is True
        assert _field(adjuster, "d7x25_heat_tool_path_clear_at_step_2") is True


def test_single_adjuster_insert_installation_stage_and_authoritative_state_machine():
    g = _geometry()
    states = list(g.authoritative_assembly_state_machine())
    assert [state["step"] for state in states] == list(range(1, 15))
    assert all(state.get("active_architecture") == "revision_k_role_local" for state in states)
    assert not any(state.get("common_q_300_active") for state in states)
    assert not any(state.get("eccentric_active") for state in states)

    events = [
        event
        for state in states
        for event in state.get("events", ())
        if event.get("kind") == "heat_install_adjuster_insert"
    ]
    assert Counter(event["role"] for event in events) == Counter({role: 1 for role in ROLE_KEYS})
    assert {event["step"] for event in events} == {2}
    assert all(event["host"] == "bare_300_spine" for event in events)
    assert all(event["d7x25_heat_tool_path_clear"] for event in events)


def test_authoritative_production_manifest_94_and_forbidden_objects():
    g = _geometry()
    manifest = list(g.production_occurrence_manifest())
    assert len(manifest) == 94
    assert len({row["occurrence_name"] for row in manifest}) == 94
    assert Counter(row["category"] for row in manifest) == Counter(EXPECTED_PRODUCTION_COUNTS)
    labels = " ".join(row["occurrence_name"].lower() for row in manifest)
    for forbidden in FORBIDDEN_PRODUCTION_TERMS:
        assert forbidden not in labels
    assert all(row["printable"] is True for row in manifest)
    assert all(row["source_module"].startswith("p3_v3_direct_gear_race_guidance_r2") for row in manifest)


def test_complete_station_coupon_and_all_fit_ladders_are_source_derived():
    g = _geometry()
    coupon = g.complete_station_coupon_report()
    assert _field(coupon, "canonical_crop_equal") is True
    assert _field(coupon, "printed_occurrence_count") == 5
    assert Counter(_field(coupon, "printed_categories")) == Counter({
        "tower_300_structural_spine": 1,
        "tower_300_role_slider_cassette": 3,
        "tower_300_three_window_stop_plate": 1,
    })
    bounds = _field(coupon, "oriented_printed_bounds_mm")
    assert all(actual <= maximum for actual, maximum in zip(bounds, (110.00, 85.00, 24.00)))
    assert _field(coupon, "references_are_non_printing") is True
    assert _field(coupon, "minimum_xy_bed_margin_mm") >= 5.00

    station_ladder = g.complete_station_fit_ladder_report()
    assert _field(station_ladder, "cell_count") == 18
    assert _field(station_ladder, "family_count") == 6
    assert all(count == 3 for count in _field(station_ladder, "cells_per_family").values())
    assert _field(station_ladder, "source_derived") is True

    fixed = g.fixed_tower_coupon_and_ladder_report()
    assert _field(fixed, "shim_pair_assembly_count") == 9
    assert _field(fixed, "blind_seat_bridge_bore_cell_count") == 3
    assert _field(fixed, "shim_indices") == list(range(-4, 5))
    assert all(pair["inboard_mm"] + pair["outboard_mm"] == pytest.approx(3.00) for pair in _field(fixed, "shim_pairs"))
    assert all(0.50 <= value <= 2.50 for pair in _field(fixed, "shim_pairs") for value in (pair["inboard_mm"], pair["outboard_mm"]))
    assert _field(fixed, "source_derived") is True


def test_full_1040_sample_actual_brep_motion_mesh_and_parity_api():
    g = _geometry()
    report = g.validate_full_motion_brep_and_parity()
    assert _field(report, "used_actual_brep") is True
    assert _field(report, "samples_per_revolution") == 1040
    assert _field(report, "ring_roles") == list(ROLES)
    assert _field(report, "q_values_mm") == pytest.approx([-0.35, 0.00, 0.10])
    assert _field(report, "other_role_phase_pair_count") == 9
    assert _field(report, "dynamic_role_poses_per_q") == 28080
    assert _field(report, "static_phase_cartesian_count") == 27
    assert _field(report, "actual_brep_candidate_pairs_checked") > 0
    assert _field(report, "unintended_positive_volume_intersection_count") == 0
    assert _field(report, "invalid_shape_count") == 0
    assert _field(report, "minimum_contact_ratio") >= 1.20
    assert 0.10 <= _field(report, "minimum_tangential_backlash_mm")
    assert _field(report, "maximum_tangential_backlash_mm") <= 0.25
    assert _field(report, "minimum_working_depth_mm") >= 1.60
    assert _field(report, "source_export_occurrence_parity") is True
    assert _field(report, "source_export_brep_digest_parity") is True
    assert _field(report, "maximum_export_bounds_delta_mm") <= 0.02
    assert _field(report, "maximum_export_relative_volume_error") <= 1e-5


def test_required_r2_artifacts_exist_under_only_the_new_model_root():
    expected = (
        "p3_v3_r2_assembled.step",
        "p3_v3_r2_service_exploded.step",
        "p3_v3_r2_powered_min.step",
        "p3_v3_r2_powered_max.step",
        "p3_v3_r2_service_min_UNSAFE_TO_POWER.step",
        "p3_v3_r2_service_max_UNSAFE_TO_POWER.step",
        "print/p3_v3_r2_production_94.3mf",
        "coupons/p3_v3_r2_complete_station_coupon.3mf",
        "coupons/p3_v3_r2_complete_station_fit_ladder.3mf",
        "coupons/p3_v3_r2_fixed_tower_coupon.3mf",
        "coupons/p3_v3_r2_fixed_tower_fit_ladder.3mf",
        "manifest.json",
    )
    missing = [relative for relative in expected if not (MODEL_ROOT / relative).is_file()]
    assert not missing, f"RED: R2 artifacts have not been emitted: {missing}"

    manifest = json.loads((MODEL_ROOT / "manifest.json").read_text())
    assert manifest["namespace"] == "p3_v3_direct_gear_race_guidance_r2"
    assert manifest["revision"] == "K"
    assert manifest["productionPrintedOccurrences"] == 94
    assert manifest["shellsPerCriticalPose"] == 4096
    assert manifest["motionSamplesPerRevolution"] == 1040
    assert manifest["sourceModules"] == [SPEC_MODULE, GEOMETRY_MODULE, EXPORT_MODULE]
    assert all("locked_pre_radial_visibility" not in path for path in manifest["artifacts"])
