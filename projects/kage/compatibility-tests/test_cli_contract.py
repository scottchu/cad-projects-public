import json
from pathlib import Path
import subprocess
import sys

import pytest

from optical_spec import (
    REFERENCE_FINAL_INPUTS,
    body_stack_packaging,
    calculate_scenario,
    central_occlusion_check,
    clock_angles,
    flared_pod_clearance,
    halo_response,
    penumbra_width,
    projected_hand,
    projected_direct_shaft_disc,
    projected_mask,
    projected_ring_carrier,
    projected_offset,
    projection_distances,
    stage_presets,
)


def cli(*args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    executable = Path(sys.executable).parent / "kage-clock"
    assert executable.is_file(), "uv must install the kage-clock console script"
    result = subprocess.run([str(executable), *args], capture_output=True, text=True)
    assert result.returncode == expect, result.stderr
    return result


def test_pure_projection_functions_recompute_non_default_relationships():
    assert projection_distances(42, 60) == {
        "source_hand_mm": 42.0,
        "hand_wall_mm": 60.0,
        "source_wall_mm": 102.0,
        "magnification": pytest.approx(102 / 42),
    }
    minute = projected_hand(70, 2.4, 42, 60)
    assert minute["projected_length_mm"] == pytest.approx(170)
    assert minute["projected_width_mm"] == pytest.approx(5.828571)
    assert penumbra_width(0.8, 42, 60) == pytest.approx(1.142857)
    assert projected_offset(10, -5, 42, 60) == {
        "projected_x_mm": pytest.approx(-14.285714),
        "projected_y_mm": pytest.approx(7.142857),
    }


def test_pure_functions_reject_invalid_inputs():
    with pytest.raises(ValueError):
        projection_distances(0, 60)
    with pytest.raises(ValueError):
        projection_distances(42, -1)
    with pytest.raises(ValueError):
        penumbra_width(-0.1, 42, 60)
    with pytest.raises(ValueError):
        halo_response(195, 45, 101, 74)
    with pytest.raises(ValueError):
        clock_angles(24, 0, 0)
    with pytest.raises(ValueError, match="wall_z < mask_z < source_z"):
        projected_mask(physical_radius_mm=55, mask_z_mm=40, source_z_mm=104.8, wall_z_mm=50)


def test_central_occlusion_uses_angular_extent_for_every_measured_component():
    result = central_occlusion_check(
        occluder_radius_mm=20,
        occluder_source_distance_mm=40,
        hardware={
            "nut": (5, 45),
            "movement-corner": (18, 50),
        },
    )
    assert result["occluder_angular_extent"] == pytest.approx(0.5)
    assert result["components"]["nut"]["hidden"] is True
    assert result["components"]["movement-corner"]["hidden"] is True
    assert result["all_hardware_hidden"] is True
    failed = central_occlusion_check(
        occluder_radius_mm=10,
        occluder_source_distance_mm=40,
        hardware={"stand": (15, 40)},
    )
    assert failed["all_hardware_hidden"] is False
    assert failed["central_obstruction_failures"] == ["stand"]


def test_ring_carrier_projects_radial_interval_and_visible_span():
    carrier = projected_ring_carrier(
        name="hour",
        carrier_inner_radius_mm=18,
        carrier_outer_radius_mm=24,
        blocker_radial_start_mm=24,
        blocker_radial_end_mm=60,
        blocker_width_mm=9,
        blocker_shape="leaf-kite",
        axial_plane_offset_mm=0,
        source_hand_mm=42,
        hand_wall_mm=60,
        effective_occluder_radius_mm=130,
        optical_angle_degrees=365,
    )
    assert carrier["movement_type"] == "annular-ring-carrier"
    assert carrier["projected_radial_start_mm"] == pytest.approx(58.285714)
    assert carrier["projected_radial_end_mm"] == pytest.approx(145.714286)
    assert carrier["visible_projected_span_mm"] == pytest.approx(15.714286)
    assert carrier["optical_angle_degrees"] == pytest.approx(5)
    assert "not-drive" in carrier["angle_semantics"]


def test_ring_carrier_axial_offset_changes_optics_without_modeling_drive():
    carrier = projected_ring_carrier(
        name="minute",
        carrier_inner_radius_mm=11,
        carrier_outer_radius_mm=17,
        blocker_radial_start_mm=17,
        blocker_radial_end_mm=70,
        blocker_width_mm=2.4,
        blocker_shape="blade",
        axial_plane_offset_mm=2,
        source_hand_mm=42,
        hand_wall_mm=60,
        effective_occluder_radius_mm=130,
        exposed_drive_radius_mm=17.5,
        clear_center_radius_mm=10,
    )
    assert carrier["effective_source_hand_mm"] == 44
    assert carrier["effective_hand_wall_mm"] == 58
    assert carrier["magnification"] == pytest.approx(102 / 44)
    with pytest.raises(ValueError):
        projected_ring_carrier(
            name="bad",
            carrier_inner_radius_mm=18,
            carrier_outer_radius_mm=24,
            blocker_radial_start_mm=25,
            blocker_radial_end_mm=60,
            blocker_width_mm=9,
            blocker_shape="blade",
            axial_plane_offset_mm=0,
            source_hand_mm=42,
            hand_wall_mm=60,
            effective_occluder_radius_mm=130,
        )


def test_reference_stepped_body_packaging_derives_exact_stack():
    body = body_stack_packaging(source_hand_mm=42, **REFERENCE_FINAL_INPUTS["body"])
    assert body["overall_depth_mm"] == 70
    assert body["total_front_to_wall_mm"] == 115
    assert body["hand_plane_from_front_mm"] == pytest.approx(52.2)
    assert body["aperture_plane_from_front_mm"] == pytest.approx(10.2)
    assert body["available_optical_run_mm"] == 42
    assert body["optical_packaging_allowance_mm"] == 0
    assert body["movement_packaging_allowance_mm"] == pytest.approx(2.8)
    assert body["hand_wall_mm"] == pytest.approx(62.8)
    assert body["radial_shoulder_mm"] == 55
    assert body["rear_opening_diameter_mm"] == 120
    assert body["rear_opening_radial_wall_mm"] == 15
    assert body["movement_lateral_clearance_mm"] == pytest.approx(10.5)
    assert body["source_plane_behind_front_occluder_mm"] == pytest.approx(-1.8)
    assert body["fits_axially"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("rear_pod_diameter_mm", 280),
        ("rear_opening_diameter_mm", 150),
        ("pod_front_overlap_mm", 12),
        ("movement_envelope_width_mm", 0),
    ],
)
def test_body_packaging_rejects_impossible_geometry(field, value):
    inputs = dict(REFERENCE_FINAL_INPUTS["body"])
    inputs[field] = value
    with pytest.raises(ValueError):
        body_stack_packaging(source_hand_mm=42, **inputs)


def test_reference_scenario_recomputes_optics_halo_and_warnings():
    scenario = calculate_scenario("reference-final")
    optics = scenario["optics"]
    assert scenario["schema_version"] == 1
    assert "inference" in scenario["provenance"]
    assert optics["source_wall_mm"] == pytest.approx(104.8)
    assert optics["magnification"] == pytest.approx(104.8 / 42)
    assert optics["hands"]["hour"]["projected_length_mm"] == pytest.approx(144.220183)
    assert optics["hands"]["minute"]["projected_length_mm"] == pytest.approx(174.666667)
    assert optics["hands"]["second"]["projected_length_mm"] == pytest.approx(220.49505)
    assert optics["penumbra_mm"] == pytest.approx(1.19619)
    assert optics["projected_sweep_diameter_mm"] == pytest.approx(440.990099)
    assert scenario["halo"]["diameter_mm"] == pytest.approx(411.096)
    assert "shadow_exceeds_halo" in scenario["warnings"]
    assert "optical_stack_has_little_tuning_allowance" in scenario["warnings"]
    assert scenario["movement_type"] == "quartz-driven-orbital-hands"
    assert scenario["movement"]["drive_geometry_modeled"] is False
    assert "no printed gearing" in scenario["movement"]["drive_mechanism"]
    assert scenario["movement"]["hollow_center"] is False
    assert scenario["movement"]["room_to_wall_stack"] == [
        "viewer-cosmetic-shell-and-metal-heatsink",
        "point-led-and-thin-flared-aperture",
        "second-minute-hour-direct-shaft-blocker-discs",
        "fixed-physical-mask-and-quartz-face",
        "stock-quartz-case",
        "wall-standoff",
        "wall",
    ]
    assert scenario["movement"]["fixed_mask_is_separate_from_cosmetic_shell"] is True
    assert scenario["movement"]["movement_hardware_reference"] == {
        "shipped_variant_overall_mm": 34.0,
        "shipped_threaded_bushing_mm": 7.7,
        "published_cad_overall_mm": 29.7,
        "provisional_variant_dependent": True,
        "movement_envelope_adjustable": True,
        "mounting_thickness_adjustable": True,
    }
    assert "measure_selected_quartz_shaft_bores_and_axial_heights" in scenario["warnings"]


def test_authoritative_fixed_mask_and_direct_disc_stack_math():
    mask = projected_mask(
        physical_radius_mm=55.5714285714,
        mask_z_mm=60,
        source_z_mm=104.8,
        wall_z_mm=0,
    )
    assert mask["projected_radius_mm"] == pytest.approx(130, abs=0.003)
    assert mask["physical_diameter_mm"] == pytest.approx(111.142857)
    expected = {
        "hour": (61.2, 60, 9, "leaf-kite", 43.6, 61.2, 2.403670, 1.122936, 144.220183, 14.222735, 17.024972),
        "minute": (62.8, 70, 2.4, "blade", 42.0, 62.8, 2.495238, 1.196190, 174.666667, 44.669218, 12.721259),
        "second": (64.4, 85, .8, "needle", 40.4, 64.4, 2.594059, 1.275248, 220.495050, 90.497601, 8.076657),
    }
    for name, (z, tip, width, shape, length, wall, mag, penumbra, projected_tip, visible, margin) in expected.items():
        disc = projected_direct_shaft_disc(
            name=name,
            plane_z_mm=z,
            source_z_mm=104.8,
            wall_z_mm=0,
            carrier_outer_radius_mm=47,
            blocker_radial_start_mm=47,
            blocker_radial_end_mm=tip,
            blocker_width_mm=width,
            blocker_shape=shape,
            projected_mask_radius_mm=mask["projected_radius_mm"],
            effective_aperture_mm=.8,
            required_hide_margin_mm=5,
        )
        assert (disc["source_blocker_mm"], disc["blocker_wall_mm"]) == pytest.approx((length, wall))
        assert disc["magnification"] == pytest.approx(mag, abs=1e-6)
        assert disc["penumbra_mm"] == pytest.approx(penumbra, abs=1e-6)
        assert disc["projected_tip_mm"] == pytest.approx(projected_tip, abs=1e-6)
        assert disc["visible_length_mm"] == pytest.approx(visible, abs=.003)
        assert disc["carrier_hide_margin_mm"] == pytest.approx(margin, abs=.003)
        assert disc["carrier_hidden"] is True
    assert projected_direct_shaft_disc(
        name="second", plane_z_mm=64.4, source_z_mm=104.8, wall_z_mm=0,
        carrier_outer_radius_mm=47, blocker_radial_start_mm=47,
        blocker_radial_end_mm=85, blocker_width_mm=.8, blocker_shape="needle",
        projected_mask_radius_mm=mask["projected_radius_mm"],
    )["required_full_field_angle_degrees"] == pytest.approx(129.157068)


def test_flared_pod_envelope_rejects_continuous_150mm_pod():
    clearance = flared_pod_clearance(
        blocker_tip_radius_mm=85,
        blocker_z_mm=64.4,
        source_z_mm=104.8,
        pod_clear_radius_mm=60,
        pod_rear_z_mm=45,
    )
    assert clearance["required_clear_radius_at_pod_rear_mm"] == pytest.approx(125.816832)
    assert clearance["minimum_room_side_pod_end_z_mm"] == pytest.approx(76.282353)
    assert clearance["continuous_pod_clears_cone"] is False
    assert clearance["pod_must_end_before_cone_expands"] is True


def test_orbital_study_has_per_plane_optics_without_selecting_final_drive():
    scenario = calculate_scenario("reference-orbital-study")
    assert scenario["movement_type"] == "annular-orbital-hollow-center"
    assert scenario["movement"]["scenario_role"] == "comparison-only optical hypothesis"
    assert "comparison study" in scenario["provenance"]
    assert scenario["movement"]["carriers"]["hour"]["axial_plane_offset_mm"] == pytest.approx(1.6)
    assert scenario["movement"]["carriers"]["minute"]["axial_plane_offset_mm"] == 0
    assert scenario["movement"]["carriers"]["second"]["axial_plane_offset_mm"] == pytest.approx(-1.6)
    assert scenario["movement"]["carriers"]["hour"]["effective_source_hand_mm"] == pytest.approx(43.6)
    assert scenario["movement"]["carriers"]["minute"]["effective_source_hand_mm"] == pytest.approx(42.0)
    assert scenario["movement"]["carriers"]["second"]["effective_source_hand_mm"] == pytest.approx(40.4)
    assert scenario["movement"]["carriers"]["hour"]["visible_projected_span_mm"] == pytest.approx(14.222735, abs=.003)
    assert scenario["movement"]["carriers"]["minute"]["visible_projected_span_mm"] == pytest.approx(44.669218, abs=.003)
    assert scenario["movement"]["carriers"]["second"]["visible_projected_span_mm"] == pytest.approx(90.497601, abs=.003)
    assert scenario["movement"]["ring_stack"]["worst_carrier_hide_margin_mm"] == pytest.approx(1.59151, abs=.003)
    assert all(not failed for failed in scenario["movement"]["failure_flags"].values())
    assert scenario["movement"]["ring_stack"] == {
        "clear_center_diameter_mm": 36.0,
        "carrier_inner_radius_mm": 38.0,
        "carrier_outer_radius_mm": 48.0,
        "maximum_exposed_drive_radius_mm": 49.5,
        "carrier_thickness_mm": 1.2,
        "axial_gap_mm": 0.4,
        "axial_pitch_mm": 1.6,
        "three_ring_stack_depth_mm": 4.4,
        "worst_carrier_hide_margin_mm": pytest.approx(1.59151, abs=.003),
    }
    hour = scenario["movement"]["carriers"]["hour"]
    minute = scenario["movement"]["carriers"]["minute"]
    second = scenario["movement"]["carriers"]["second"]
    for carrier in (hour, minute, second):
        assert carrier["carrier_inner_radius_mm"] == 38
        assert carrier["carrier_outer_radius_mm"] == 48
        assert carrier["carrier_thickness_mm"] == 1.2
        assert carrier["axial_gap_mm"] == 0.4
        assert carrier["exposed_drive_radius_mm"] == 49.5
        assert carrier["clear_center_radius_mm"] == 18
        assert set(carrier["failure_flags"]) == {
            "donut_shadow", "collision", "vignetting", "glare",
            "pivot_drift", "central_obstruction",
        }
    assert hour["penumbra_mm"] == pytest.approx(0.8 * 61.2 / 43.6)
    assert minute["penumbra_mm"] == pytest.approx(0.8 * 62.8 / 42)
    assert second["penumbra_mm"] == pytest.approx(0.8 * 64.4 / 40.4)
    assert hour["projected_tip_mm"] == pytest.approx(144.220183)
    assert minute["projected_tip_mm"] == pytest.approx(174.666667)
    assert second["projected_tip_mm"] == pytest.approx(220.49505)
    assert (hour["optical_angle_degrees"], minute["optical_angle_degrees"], second["optical_angle_degrees"]) == pytest.approx((305.2916667, 63.5, 210))
    assert "independent" in scenario["movement"]["angle_semantics"]


def test_named_stage_presets_include_wired_led_and_reference_final():
    presets = stage_presets()
    assert set(presets) == {"wired-led-breadboard", "generic-quartz", "reference-final", "reference-orbital-study"}
    assert presets["wired-led-breadboard"]["source_hand_mm"] == 40
    assert presets["wired-led-breadboard"]["hand_lengths_mm"] == {"hour": 45, "minute": 70}
    assert presets["wired-led-breadboard"]["movement"]["movement_type"] == "manual-concentric-ring-jig"
    assert presets["generic-quartz"]["movement"]["movement_type"] == "standard-center-shaft-quartz"
    assert presets["reference-final"]["body"]["rear_pod_diameter_mm"] == 150
    assert presets["reference-final"]["body"]["rear_opening_diameter_mm"] == 120


def test_cli_list_and_scenario_json_schema():
    listing = json.loads(cli("list", "--json").stdout)
    assert listing["schema_version"] == 1
    assert {item["name"] for item in listing["scenarios"]} == {"wired-led-breadboard", "generic-quartz", "reference-final", "reference-orbital-study"}

    payload = json.loads(cli("scenario", "reference-final", "--json").stdout)
    assert set(payload) == {"schema_version", "scenario", "description", "provenance", "movement_type", "movement", "body", "optics", "halo", "warnings"}
    assert payload["schema_version"] == 1
    assert payload["scenario"] == "reference-final"
    assert payload["body"]["derived"]["overall_depth_mm"] == 70
    assert payload["optics"]["source_wall_mm"] == pytest.approx(104.8)

    p0 = json.loads(cli("scenario", "wired-led-breadboard", "--json").stdout)
    assert p0["schema_version"] == 1
    assert set(p0["optics"]["hands"]) == {"hour", "minute"}
    assert p0["optics"]["hands"]["hour"]["shape"] == "blade"
    assert p0["halo"]["enabled"] is False
    assert p0["movement_type"] == "manual-concentric-ring-jig"

    generic = json.loads(cli("scenario", "generic-quartz", "--json").stdout)
    assert generic["movement_type"] == "standard-center-shaft-quartz"
    assert generic["movement"]["carriers"] == {}
    assert generic["halo"]["enabled"] is False


def test_cli_projection_and_body_are_callable_in_text_and_json():
    text = cli("projection", "--source-hand", "42", "--hand-wall", "60", "--aperture", "0.8").stdout
    assert "2.4286x" in text and "1.14 mm" in text
    projection = json.loads(cli("projection", "--source-hand", "42", "--hand-wall", "60", "--json").stdout)
    assert projection["schema_version"] == 1
    assert projection["calculation"] == "projection"
    body = json.loads(cli("body", "--json").stdout)
    assert body["schema_version"] == 1
    assert body["calculation"] == "body"
    assert body["derived"]["overall_depth_mm"] == 70
    assert body["derived"]["fits_axially"] is True


def test_cli_ring_carrier_exposes_optics_without_claiming_drive_geometry():
    args = (
        "ring-carrier", "--name", "hour", "--inner-radius", "38", "--outer-radius", "48",
        "--blocker-start", "48", "--blocker-end", "60", "--blocker-width", "9",
        "--shape", "leaf-kite", "--source-hand", "42", "--hand-wall", "60",
        "--occluder-radius", "130", "--optical-angle", "305.2917", "--axial-offset", "1.6",
    )
    payload = json.loads(cli(*args, "--json").stdout)
    assert payload["schema_version"] == 1
    assert payload["calculation"] == "ring-carrier"
    assert payload["drive_mechanism"] == "not modeled"
    assert payload["carrier"]["visible_projected_span_mm"] == pytest.approx(10.366972)
    assert payload["carrier"]["carrier_hide_margin_mm"] == pytest.approx(14.197248)
    assert payload["carrier"]["all_clear"] is True
    text = cli(*args).stdout
    assert "not drive geometry" in text
    assert "Drive mechanism      not modeled" in text


def test_cli_central_occlusion_reports_hidden_and_exposed_hardware():
    hidden = json.loads(cli(
        "occlusion", "--occluder-radius", "20", "--occluder-distance", "40",
        "--hardware", "nut:5:45", "--hardware", "body-corner:18:50", "--json",
    ).stdout)
    assert hidden["schema_version"] == 1
    assert hidden["calculation"] == "central-occlusion"
    assert hidden["result"]["all_hardware_hidden"] is True
    exposed = cli(
        "occlusion", "--occluder-radius", "10", "--occluder-distance", "40",
        "--hardware", "stand:15:40",
    ).stdout
    assert "All hardware hidden NO" in exposed
    assert "EXPOSED" in exposed


def test_cli_fixed_mask_and_direct_disc_match_reference_scenario():
    mask = json.loads(cli("mask", "--json").stdout)
    assert mask["calculation"] == "fixed-mask"
    assert mask["result"]["projected_radius_mm"] == pytest.approx(130, abs=.003)
    assert "cosmetic shell does not" in mask["note"]

    disc = json.loads(cli(
        "direct-disc", "--name", "second", "--plane-z", "64.4",
        "--blocker-end", "85", "--blocker-width", ".8", "--shape", "needle",
        "--json",
    ).stdout)
    assert disc["calculation"] == "direct-shaft-disc"
    assert disc["disc"]["movement_type"] == "quartz-direct-shaft-orbital-disc"
    assert disc["disc"]["magnification"] == pytest.approx(104.8 / 40.4)
    assert disc["disc"]["required_full_field_angle_degrees"] == pytest.approx(129.157068)
    assert disc["disc"]["carrier_hidden"] is True

    invalid = cli(
        "direct-disc", "--name", "second", "--plane-z", "105",
        "--blocker-end", "85", "--blocker-width", ".8", "--shape", "needle",
        expect=2,
    )
    assert "between wall and source" in invalid.stderr

    invalid_mask = cli(
        "mask", "--source-z", "104.8", "--mask-z", "40", "--wall-z", "50",
        expect=2,
    )
    assert "wall_z < mask_z < source_z" in invalid_mask.stderr


def test_cli_invalid_geometry_returns_usage_error():
    result = cli("projection", "--source-hand", "0", "--hand-wall", "60", expect=2)
    assert "must be positive" in result.stderr


def test_wired_led_breadboard_human_output_states_that_halo_is_disabled():
    text = cli("scenario", "wired-led-breadboard").stdout
    assert "Halo                disabled for this stage" in text
