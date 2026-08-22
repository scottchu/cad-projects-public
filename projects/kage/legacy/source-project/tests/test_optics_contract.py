from datetime import datetime
from math import isclose, pi

import pytest

from optical_spec import (
    HaloConfig,
    OpticalConfig,
    WiredLedBreadboard,
    clock_angles,
    resolve_time,
    warning_codes,
)


def test_p0_wired_led_defaults_and_adjustment_ranges():
    p0 = WiredLedBreadboard()
    assert p0.source_hand_mm == 40
    assert p0.hand_wall_mm == 60
    assert p0.minute_hand_mm == 70
    assert p0.source_hand_range_mm == (25, 80)
    assert p0.hand_wall_range_mm == (30, 120)
    assert p0.printed_aperture_trials_mm == (1.0, 1.5, 2.0)
    assert p0.led_current_ma == 350


def test_pinhole_distance_magnification_and_projection():
    p = OpticalConfig()
    assert p.source_wall_mm == p.source_hand_mm + p.hand_wall_mm == 100
    assert p.magnification == 2.5
    assert p.project_length(p.minute_hand_mm) == 175
    assert p.project_width(p.minute_width_mm) == 6


@pytest.mark.parametrize(
    ("source_hand", "hand_wall", "expected_m"),
    [(20, 60, 4.0), (40, 60, 2.5), (80, 60, 1.75), (40, 30, 1.75), (40, 120, 4.0)],
)
def test_non_default_projection_relationships_reject_a_constant_magnification(source_hand, hand_wall, expected_m):
    p = OpticalConfig(source_hand_mm=source_hand, hand_wall_mm=hand_wall)
    assert p.source_wall_mm == source_hand + hand_wall
    assert p.magnification == expected_m
    assert p.project_length(37) == 37 * expected_m


def test_projection_monotonicity_with_source_and_wall_distances():
    assert OpticalConfig(source_hand_mm=25).magnification > OpticalConfig(source_hand_mm=80).magnification
    assert OpticalConfig(hand_wall_mm=120).magnification > OpticalConfig(hand_wall_mm=30).magnification
    with pytest.raises(ValueError):
        OpticalConfig(source_hand_mm=0)


def test_penumbra_approximation_for_wired_led_breadboard():
    p = OpticalConfig(aperture_mm=1.0)
    assert p.penumbra_mm == 1.5
    assert OpticalConfig(aperture_mm=2.0).penumbra_mm == 3.0


@pytest.mark.parametrize(
    ("aperture", "source_hand", "hand_wall", "expected"),
    [(0.6, 40, 60, 0.9), (1.0, 25, 60, 2.4), (1.0, 80, 60, 0.75), (1.5, 40, 120, 4.5)],
)
def test_non_default_penumbra_relationship_rejects_distance_ignoring_shortcut(aperture, source_hand, hand_wall, expected):
    assert OpticalConfig(aperture_mm=aperture, source_hand_mm=source_hand, hand_wall_mm=hand_wall).penumbra_mm == expected


def test_penumbra_monotonicity_in_all_three_inputs():
    base = OpticalConfig().penumbra_mm
    assert OpticalConfig(aperture_mm=2).penumbra_mm > base
    assert OpticalConfig(source_hand_mm=80).penumbra_mm < base
    assert OpticalConfig(hand_wall_mm=120).penumbra_mm > base


def test_point_source_offset_translates_opposite_and_scales_by_m_minus_one():
    p = OpticalConfig(led_offset_x_mm=8, led_offset_y_mm=-4)
    assert p.projected_pivot_mm == (-12, 6)
    assert OpticalConfig(source_hand_mm=80, led_offset_x_mm=8).projected_pivot_mm[0] == -6


def test_halo_is_independent_of_point_projection_inputs():
    halo = HaloConfig()
    changed_point = OpticalConfig(source_hand_mm=75, aperture_mm=4.0, led_offset_x_mm=20)
    assert HaloConfig().radius_mm == halo.radius_mm
    assert changed_point.magnification != OpticalConfig().magnification


def test_halo_relationship_rejects_constant_radius_mutation():
    baseline = HaloConfig()
    farther = HaloConfig(wall_gap_mm=90)
    more_diffuse = HaloConfig(spread_percent=90)
    assert farther.radius_mm > baseline.radius_mm
    assert more_diffuse.radius_mm > baseline.radius_mm
    # Point-source changes cannot leak into halo calculations.
    assert HaloConfig().radius_mm == HaloConfig().radius_mm


def test_default_10_10_35_angles_include_subordinate_hand_motion():
    hour, minute, second = clock_angles(10, 10, 35)
    assert isclose(second, 35 * pi / 30)
    assert isclose(minute, (10 + 35 / 60) * pi / 30)
    assert isclose(hour, (10 + (10 + 35 / 60) / 60) * pi / 6)


def test_manual_time_is_deterministic_and_real_tick_vs_sweep_differs():
    sample = datetime(2026, 8, 10, 9, 8, 7, 500_000)
    assert resolve_time(use_real_time=False, manual=(10, 10, 35), now=sample) == (10, 10, 35.0)
    assert resolve_time(use_real_time=True, now=sample, sweep=False) == (9, 8, 7.0)
    assert resolve_time(use_real_time=True, now=sample, sweep=True) == (9, 8, 7.5)


def test_warning_thresholds_are_executable():
    optical = OpticalConfig(source_hand_mm=40)
    codes = warning_codes(optical, HaloConfig(base_radius_mm=150))
    assert "shadow_exceeds_halo" in codes
    assert "source_path_exceeds_shell" in codes
    assert "led_too_close" in warning_codes(OpticalConfig(source_hand_mm=8), HaloConfig())
    assert "aperture_reduces_brightness" in warning_codes(OpticalConfig(aperture_mm=0.4), HaloConfig())
    assert "source_path_exceeds_shell" not in warning_codes(optical, HaloConfig(), stage="p0")
    assert "led_too_close" in warning_codes(OpticalConfig(source_hand_mm=8), HaloConfig(), stage="p0")
    assert "verify_led_thermal_clearance_from_pla" in warning_codes(optical, HaloConfig(), stage="p0")
    assert "verify_led_thermal_clearance_from_pla" in warning_codes(optical, HaloConfig(), stage="p1")
    assert "source_path_exceeds_shell" not in warning_codes(
        OpticalConfig(source_hand_mm=17), HaloConfig(), body_depth_mm=35, movement_depth_mm=15, shell_mm=2
    )
    assert "source_path_exceeds_shell" in warning_codes(
        OpticalConfig(source_hand_mm=19), HaloConfig(), body_depth_mm=35, movement_depth_mm=15, shell_mm=2
    )
