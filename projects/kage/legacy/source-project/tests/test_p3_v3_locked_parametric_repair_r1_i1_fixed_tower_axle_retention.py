"""RED contract for I1 fixed-tower axle retention on the accepted R1 clock.

This test module intentionally precedes the production I1 namespace.  It may
only authorize local changes to the two fixed roller towers at 60 and 180
degrees.  The accepted 201-occurrence R1 STEP remains the independent baseline;
ring teeth/bodies/fins, motors, chassis, frame, adjustable tower, and every
other occurrence are protected exact.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, is_dataclass, replace
from hashlib import sha256
import importlib
from pathlib import Path
from typing import Any, Mapping

import pytest


ROOT = Path(__file__).resolve().parents[1]
LOCKED_STEP = (
    ROOT
    / "models"
    / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
    / "p3_v3_direct_gear_race_assembled.step"
)
LOCKED_STEP_SHA256 = "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7"

SPEC_MODULE = "p3_v3_locked_parametric_repair_r1_i1_spec"
GEOMETRY_MODULE = "p3_v3_locked_parametric_repair_r1_i1_geometry"
PARITY_MODULE = "p3_v3_locked_parametric_repair_r1_i1_parity"

FIXED_TOWER_ANGLES_DEG = (60.0, 180.0)
FIXED_TOWER_BASELINE_NAMES = frozenset(
    (
        "occurrence_018", "occurrence_019", "occurrence_020",
        "occurrence_021", "occurrence_022", "occurrence_026",
        "occurrence_027", "occurrence_028", "occurrence_035",
        "occurrence_036", "occurrence_037", "occurrence_038",
        "occurrence_039", "occurrence_043", "occurrence_044",
        "occurrence_045",
    )
)
PROTECTED_RING_ROLLER_NAMES = frozenset(
    (
        "occurrence_023", "occurrence_024", "occurrence_025",
        "occurrence_040", "occurrence_041", "occurrence_042",
        "occurrence_057", "occurrence_058", "occurrence_059",
    )
)

EXPECTED_DEFAULTS = {
    "fixed_station_angles_deg": FIXED_TOWER_ANGLES_DEG,
    "tower_axis_radius_mm": 125.5,
    "leaf_seat_diameter_mm": 4.05,
    "leaf_seat_z_range_mm": (-5.20, -2.20),
    "minimum_leaf_bottom_wall_mm": 1.50,
    "upper_bridge_bore_diameter_mm": 4.06,
    "upper_bridge_z_range_mm": (16.70, 19.70),
    "axle_diameter_mm": 3.99,
    "axle_length_mm": 30.0,
    "axle_bottom_z_mm": -5.20,
    "washer_outer_diameter_mm": 8.0,
    "washer_bore_diameter_mm": 4.0,
    "washer_thickness_mm": 0.15,
    "collar_bore_diameter_mm": 4.0,
    "collar_outer_diameter_mm": 8.0,
    "collar_height_mm": 4.0,
    "collar_bottom_z_mm": 19.95,
    "collar_fastener_nominal_mm": 3.0,
    "nominal_endplay_mm": 0.10,
    "minimum_endplay_mm": 0.05,
    "maximum_endplay_mm": 0.15,
    "tool_withdrawal_diameter_mm": 6.50,
}

EXPECTED_SCHEMA_FIELDS = frozenset(EXPECTED_DEFAULTS)
REQUIRED_ROW_FIELDS = {
    "name", "label", "shape", "transform", "topology", "volume_mm3",
    "area_mm2", "aabb_mm", "classification", "owner_group",
}
ALLOWED_I1_OWNER_GROUPS = {
    "fixed_tower_leaves",
    "fixed_tower_bridges",
    "fixed_tower_shims",
    "fixed_tower_hardware",
}
EXPECTED_ENVELOPE_NAMES = {
    f"tower_{tower}_{feature}"
    for tower in (1, 2)
    for feature in ("leaf_seat", "upper_bridge", "shim_stack", "axle_hardware", "service_path")
}


def _load(name: str):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            pytest.fail(
                f"RED: I1 production module {name!r} does not exist yet",
                pytrace=False,
            )
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


def _params():
    module = _spec_module()
    assert hasattr(module, "P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1")
    return module.P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1


def _volume(shape) -> float:
    return float(sum(solid.volume for solid in shape.solids()))


def _row_map(rows):
    result = {}
    for row in rows:
        assert REQUIRED_ROW_FIELDS <= set(row), row
        assert row["name"] not in result
        result[row["name"]] = row
    return result


def _meta(value: Any, name: str) -> Any:
    return value[name] if isinstance(value, Mapping) else getattr(value, name)


def test_i1_is_anchored_to_the_immutable_accepted_r1_step():
    assert LOCKED_STEP.is_file()
    assert sha256(LOCKED_STEP.read_bytes()).hexdigest() == LOCKED_STEP_SHA256


def test_i1_namespace_is_isolated_and_cannot_alias_rejected_or_locked_source_modules():
    forbidden = ("direct_gear_race_guidance_r2", "/rollback/", "import *")
    for module in (_spec_module(), _geometry_module(), _parity_module()):
        source = Path(module.__file__).read_text()
        assert not any(token in source for token in forbidden)


def test_fixed_tower_params_are_frozen_complete_and_exact():
    module = _spec_module()
    assert hasattr(module, "FixedTowerParams")
    params = _params()
    assert type(params).__name__ == "FixedTowerParams"
    assert is_dataclass(params)
    assert getattr(params, "__dataclass_params__").frozen is True
    assert {field.name for field in fields(params)} == EXPECTED_SCHEMA_FIELDS
    for name, expected in EXPECTED_DEFAULTS.items():
        actual = getattr(params, name)
        if isinstance(expected, tuple):
            assert actual == pytest.approx(expected)
        else:
            assert actual == pytest.approx(expected)
    with pytest.raises(FrozenInstanceError):
        params.axle_diameter_mm = 4.0


def test_fixed_tower_parameter_schema_declares_ownership_ranges_and_probe_values():
    module = _spec_module()
    params = _params()
    schema = module.parameter_schema(params)
    assert set(schema) == EXPECTED_SCHEMA_FIELDS
    for field_name, contract in schema.items():
        assert _meta(contract, "path") == field_name
        assert _meta(contract, "units") in {"mm", "deg", "count"}
        assert _meta(contract, "owner_group") in ALLOWED_I1_OWNER_GROUPS
        assert _meta(contract, "minimum") is not None
        assert _meta(contract, "maximum") is not None
        assert _meta(contract, "minimum") <= _meta(contract, "maximum")
        assert _meta(contract, "probe_value") is not None


def test_iso4026_m3x2_set_screw_hardware_catalog_is_frozen_and_buildable_by_contract():
    module = _spec_module()
    hardware = module.P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE
    assert is_dataclass(hardware)
    assert getattr(hardware, "__dataclass_params__").frozen is True
    assert hardware.catalog_designation == "M3x2 ISO 4026 flat-point set screw; collar tapped M3x0.5"
    assert hardware.nominal_screw_diameter_mm == pytest.approx(3.0)
    assert hardware.tap_pilot_diameter_mm == pytest.approx(2.5)
    assert hardware.nominal_screw_length_mm == pytest.approx(2.0)
    assert hardware.hex_socket_across_flats_mm == pytest.approx(1.5)
    assert hardware.minimum_thread_engagement_mm >= 1.5
    assert hardware.nominal_outer_face_recess_mm == pytest.approx(0.005)
    assert hardware.adjustment_allowance_mm == pytest.approx(0.20)
    assert hardware.rigid_overtravel_probe_mm == pytest.approx(0.05)
    assert hardware.required_post_print_operation == "Tap D2.50 pilot M3x0.5 after printing"
    assert "not a finished M3 thread" in hardware.assembly_risk
    hardware.validate()


def test_derived_retention_math_has_required_clearances_support_and_endplay():
    p = _params()
    assert p.leaf_seat_depth_mm == pytest.approx(3.0)
    assert p.leaf_seat_radial_clearance_mm == pytest.approx((4.05 - 3.99) / 2.0)
    assert p.upper_bridge_radial_clearance_mm == pytest.approx((4.06 - 3.99) / 2.0)
    assert p.axle_top_z_mm == pytest.approx(24.80)
    assert p.stock_axle_length_mm == pytest.approx(30.0)
    assert p.installed_axle_span_mm == pytest.approx(29.4514)
    assert p.axle_trim_allowance_mm == pytest.approx(0.5486)
    assert p.collar_top_z_mm == pytest.approx(23.95)
    assert p.support_plane_z_mm == pytest.approx((-2.20, 16.70))
    assert p.retained_stack_top_z_mm + p.nominal_endplay_mm == pytest.approx(p.collar_bottom_z_mm)
    assert p.minimum_endplay_mm <= p.nominal_endplay_mm <= p.maximum_endplay_mm
    assert p.leaf_bottom_wall_mm >= p.minimum_leaf_bottom_wall_mm
    p.validate()


@pytest.mark.parametrize(
    "field_name,bad_value,phrase",
    (
        ("fixed_station_angles_deg", (60.0, 181.0), "stations"),
        ("leaf_seat_diameter_mm", 3.98, "seat"),
        ("leaf_seat_z_range_mm", (-5.20, -2.30), "seat depth"),
        ("minimum_leaf_bottom_wall_mm", 1.49, "bottom wall"),
        ("upper_bridge_bore_diameter_mm", 3.98, "bridge"),
        ("upper_bridge_z_range_mm", (16.70, 19.60), "bridge span"),
        ("axle_diameter_mm", 4.06, "axle"),
        ("axle_length_mm", 29.0, "axle length"),
        ("washer_thickness_mm", 0.0, "washer"),
        ("collar_bore_diameter_mm", 3.98, "collar bore"),
        ("collar_outer_diameter_mm", 6.49, "tool"),
        ("collar_height_mm", 3.0, "collar height"),
        ("collar_fastener_nominal_mm", 2.0, "M3"),
        ("nominal_endplay_mm", 0.16, "endplay"),
        ("tool_withdrawal_diameter_mm", 6.49, "tool"),
    ),
)
def test_invalid_fixed_tower_dimensions_fail_closed(field_name, bad_value, phrase):
    candidate = replace(_params(), **{field_name: bad_value})
    with pytest.raises(ValueError, match=phrase):
        candidate.validate()


def test_fixed_tower_feature_registry_has_two_towers_and_required_named_solids():
    features = _geometry_module().fixed_tower_features(_params())
    assert set(features) == {1, 2}
    expected = {
        "leaf", "upper_bridge", "axle", "washer", "set_screw_collar",
        "m3_set_screw_reference", "tool_withdrawal_cylinder",
    }
    for tower, registry in features.items():
        assert set(registry) == expected, tower
        assert all(registry[name].is_valid for name in expected)
        assert all(len(registry[name].solids()) == 1 for name in expected)


def test_both_fixed_tower_axes_remain_at_locked_60_and_180_degree_stations():
    geometry = _geometry_module()
    p = _params()
    features = geometry.fixed_tower_features(p)
    for tower, expected_angle in zip((1, 2), FIXED_TOWER_ANGLES_DEG, strict=True):
        center = features[tower]["axle"].center()
        assert geometry.polar_angle_deg(center.X, center.Y) == pytest.approx(expected_angle)
        assert (center.X**2 + center.Y**2) ** 0.5 == pytest.approx(p.tower_axis_radius_mm)


def test_leaf_seat_is_blind_d4p05_by_3_with_minimum_1p50_bottom_wall():
    geometry = _geometry_module()
    p = _params()
    for registry in geometry.fixed_tower_features(p).values():
        evidence = geometry.blind_seat_evidence(registry["leaf"], p)
        assert evidence["diameter_mm"] == pytest.approx(4.05)
        assert evidence["z_range_mm"] == pytest.approx((-5.20, -2.20))
        assert evidence["depth_mm"] == pytest.approx(3.0)
        assert evidence["bottom_wall_mm"] >= 1.50
        assert evidence["breaks_bottom"] is False


def test_upper_bridge_has_d4p06_bore_across_exact_z_span():
    geometry = _geometry_module()
    p = _params()
    for registry in geometry.fixed_tower_features(p).values():
        evidence = geometry.bridge_bore_evidence(registry["upper_bridge"], p)
        assert evidence["diameter_mm"] == pytest.approx(4.06)
        assert evidence["z_range_mm"] == pytest.approx((16.70, 19.70))
        assert evidence["is_through"] is True


def test_axle_washer_and_intact_m3_set_screw_collar_have_exact_bounding_dimensions():
    p = _params()
    for registry in _geometry_module().fixed_tower_features(p).values():
        axle_box = registry["axle"].bounding_box()
        washer_box = registry["washer"].bounding_box()
        collar_box = registry["set_screw_collar"].bounding_box()
        assert sorted((axle_box.size.X, axle_box.size.Y)) == pytest.approx((3.99, 3.99))
        assert axle_box.size.Z == pytest.approx(30.0)
        assert sorted((washer_box.size.X, washer_box.size.Y)) == pytest.approx((8.0, 8.0))
        assert washer_box.size.Z == pytest.approx(0.15)
        assert sorted((collar_box.size.X, collar_box.size.Y)) == pytest.approx((8.0, 8.0))
        assert collar_box.size.Z == pytest.approx(4.0)
        assert collar_box.min.Z == pytest.approx(19.95)
        assert "intact_D4_D8x4_M3_set_screw" in registry["set_screw_collar"].label


def test_installed_axle_truthfully_reports_stock_span_trim_and_locked_top():
    geometry = _geometry_module()
    p = _params()
    for tower in (1, 2):
        evidence = geometry.installed_axle_evidence(tower, p)
        assert evidence["stock_axle_length_mm"] == pytest.approx(30.0)
        assert evidence["installed_length_mm"] == pytest.approx(29.4514)
        assert evidence["installed_axle_span_mm"] == pytest.approx(29.4514)
        assert evidence["trim_allowance_mm"] == pytest.approx(0.5486)
        assert evidence["bottom_z_mm"] == pytest.approx(-5.20)
        assert evidence["top_z_mm"] == pytest.approx(24.2514)


def test_iso4026_set_screw_tapped_wall_contact_adjustment_and_service_are_actual_solid_clear():
    geometry = _geometry_module()
    p = _params()
    candidate = geometry.build_i1_candidate(p)
    for tower, registry in geometry.fixed_tower_features(p).items():
        alignment = geometry.set_screw_alignment_evidence(registry, p)
        assert alignment["axis_angle_deg"] == pytest.approx(p.fixed_station_angles_deg[tower - 1])
        assert alignment["nominal_diameter_mm"] == pytest.approx(3.0)
        assert alignment["tap_pilot_diameter_mm"] == pytest.approx(2.5)
        assert alignment["nominal_screw_length_mm"] == pytest.approx(2.0)
        assert alignment["hex_socket_across_flats_mm"] == pytest.approx(1.5)
        assert alignment["minimum_thread_engagement_mm"] >= 1.5
        assert alignment["actual_thread_engagement_mm"] == pytest.approx(2.0)
        assert alignment["intact_tapped_wall_volume_mm3"] > 1e-6
        assert alignment["nominal_outer_face_recess_mm"] == pytest.approx(0.005)
        assert alignment["adjustment_allowance_mm"] == pytest.approx(0.20)
        assert alignment["nominal_tip_to_axle_gap_mm"] == pytest.approx(0.0)
        assert alignment["collar_axle_radial_clearance_mm"] == pytest.approx(0.005)
        assert alignment["axle_screw_interference_mm3"] <= 1e-7
        assert alignment["collar_axle_interference_mm3"] <= 1e-7
        assert alignment["screw_max_z_mm"] < 24.2514

        service = geometry.set_screw_service_path_obstruction(candidate, tower, p)
        assert service["screw_withdrawal_volume_mm3"] <= 1e-7
        assert service["screw_withdrawal_labels"] == ()
        assert service["tap_access_volume_mm3"] <= 1e-7
        assert service["tap_access_labels"] == ()
        assert service["hex_driver_access_volume_mm3"] <= 1e-7
        assert service["hex_driver_access_labels"] == ()

        insertion = geometry.set_screw_max_insertion_evidence(registry, tower, p)
        assert insertion["maximum_rigid_insertion_mm"] == pytest.approx(0.0)
        assert insertion["nominal_axle_overlap_mm3"] <= 1e-7
        assert insertion["overtravel_probe_mm"] == pytest.approx(0.05)
        assert insertion["overtravel_axle_overlap_mm3"] > 1e-6
        assert insertion["preload_modelled"] is False


def test_axle_is_bottomed_and_supported_at_two_separated_planes():
    geometry = _geometry_module()
    p = _params()
    for registry in geometry.fixed_tower_features(p).values():
        evidence = geometry.axle_support_evidence(registry, p)
        assert evidence["axle_bottomed"] is True
        assert evidence["support_plane_z_mm"] == pytest.approx((-2.20, 16.70))
        assert evidence["support_plane_count"] == 2
        assert evidence["support_span_mm"] == pytest.approx(18.90)
        assert evidence["axle_solid_interference_mm3"] <= 1e-7


def test_axial_stack_endplay_is_between_0p05_and_0p15_at_both_towers():
    geometry = _geometry_module()
    p = _params()
    for registry in geometry.fixed_tower_features(p).values():
        endplay = geometry.axial_endplay_mm(registry, p)
        assert endplay == pytest.approx(0.10)
        assert 0.05 <= endplay <= 0.15


def test_d6p50_tool_and_axle_withdrawal_cylinder_is_unobstructed():
    geometry = _geometry_module()
    p = _params()
    candidate = geometry.build_i1_candidate(p)
    for tower, registry in geometry.fixed_tower_features(p).items():
        tool = registry["tool_withdrawal_cylinder"]
        assert sorted((tool.bounding_box().size.X, tool.bounding_box().size.Y)) == pytest.approx((6.50, 6.50))
        obstruction = geometry.service_path_obstruction(candidate, tower, tool)
        assert obstruction["volume_mm3"] <= 1e-7
        assert obstruction["labels"] == ()


def test_retention_hardware_has_a_clear_straight_insertion_and_removal_path():
    geometry = _geometry_module()
    p = _params()
    candidate = geometry.build_i1_candidate(p)
    for tower in (1, 2):
        samples = geometry.retention_service_path(candidate, tower, p, sample_count=41)
        assert len(samples) == 41
        assert samples[0]["state"] == "installed"
        assert samples[-1]["state"] == "withdrawn"
        assert all(sample["interference_mm3"] <= 1e-7 for sample in samples)


def test_allowed_delta_envelopes_are_named_local_and_owned_only_by_i1():
    envelopes = _parity_module().i1_allowed_delta_envelopes(_params())
    assert set(envelopes) == EXPECTED_ENVELOPE_NAMES
    for name, envelope in envelopes.items():
        assert _meta(envelope, "owner_group") in ALLOWED_I1_OWNER_GROUPS
        assert set(_meta(envelope, "baseline_occurrence_names")) <= FIXED_TOWER_BASELINE_NAMES
        assert len(_meta(envelope, "aabb_mm")) == 6
        assert _meta(envelope, "maximum_outside_delta_mm3") == pytest.approx(1e-7)
        if name.endswith("service_path"):
            assert _meta(envelope, "diameter_mm") == pytest.approx(6.50)


def test_only_fixed_tower_i1_occurrences_may_change_or_be_added():
    parity = _parity_module()
    baseline = _row_map(parity.baseline_occurrences())
    candidate = _row_map(parity.candidate_occurrences(_params()))
    assert len(baseline) == 201
    assert set(baseline) - FIXED_TOWER_BASELINE_NAMES <= set(candidate)
    for name, row in candidate.items():
        if name in baseline and name not in FIXED_TOWER_BASELINE_NAMES:
            assert row["classification"] == "protected_exact"
        elif name not in baseline:
            assert row["classification"] == "new_authorized"
            assert row["owner_group"] in ALLOWED_I1_OWNER_GROUPS


def test_ring_teeth_bodies_fins_motor_stations_chassis_frame_and_tower3_are_exact():
    parity = _parity_module()
    baseline = _row_map(parity.baseline_occurrences())
    candidate = _row_map(parity.candidate_occurrences(_params()))
    protected_names = set(baseline) - FIXED_TOWER_BASELINE_NAMES
    assert PROTECTED_RING_ROLLER_NAMES <= protected_names
    evidence = parity.protected_symmetric_difference_evidence(
        (baseline[name] for name in sorted(protected_names)),
        (candidate[name] for name in sorted(protected_names)),
        tolerance_mm3=1e-7,
    )
    assert evidence["checked_occurrence_count"] == len(protected_names)
    assert evidence["maximum_a_minus_b_mm3"] <= 1e-7
    assert evidence["maximum_b_minus_a_mm3"] <= 1e-7
    assert evidence["failures"] == ()


def test_fixed_yoke_deltas_are_contained_inside_named_leaf_and_bridge_envelopes():
    parity = _parity_module()
    evidence = parity.allowed_delta_containment_evidence(_params(), tolerance_mm3=1e-7)
    assert set(evidence) == EXPECTED_ENVELOPE_NAMES
    assert all(item["outside_envelope_delta_mm3"] <= 1e-7 for item in evidence.values())
    assert all(item["has_expected_local_delta"] for item in evidence.values() if not item["name"].endswith("service_path"))


@pytest.mark.parametrize(
    "field_name,probe_value,expected_owner",
    (
        ("leaf_seat_diameter_mm", 4.07, "fixed_tower_leaves"),
        ("upper_bridge_bore_diameter_mm", 4.08, "fixed_tower_bridges"),
        ("washer_thickness_mm", 0.12, "fixed_tower_shims"),
        ("collar_bottom_z_mm", 19.90, "fixed_tower_hardware"),
        ("tool_withdrawal_diameter_mm", 6.70, "fixed_tower_hardware"),
    ),
)
def test_parameter_perturbations_change_only_the_declared_owner_envelope(
    field_name, probe_value, expected_owner
):
    module = _spec_module()
    parity = _parity_module()
    params = replace(_params(), **{field_name: probe_value})
    params.validate()
    schema = module.parameter_schema(_params())
    assert _meta(schema[field_name], "owner_group") == expected_owner
    report = parity.perturbation_delta_report(params, changed_field=field_name)
    assert set(report["changed_owner_groups"]) == {expected_owner}
    assert report["protected_changed_occurrence_names"] == ()
    assert report["outside_allowed_envelope_delta_mm3"] <= 1e-7
