"""Focused numeric gates for the isolated P3 V3 R1 transmission."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from p3_v3_transmission_r1_spec import (
    ACCEPTED_P3_V3_SHA256,
    P3_V3_TRANSMISSION_R1 as p,
)


ROOT = Path(__file__).resolve().parents[1]


def test_accepted_p3_v3_source_files_are_byte_for_byte_frozen():
    for relative, expected in ACCEPTED_P3_V3_SHA256.items():
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative


def test_coordinate_planes_and_frozen_role_layers_are_explicit():
    assert (p.clock_plane, p.viewer_axis) == ("XY", "+Z")
    assert (p.motor_axis, p.output_axis, p.axes_angle_degrees) == ("+X", "+Z", 90.0)
    assert p.roles == ("hour", "minute", "second")
    assert p.carrier_layers == ((2.8, 5.8), (6.2, 9.2), (9.6, 12.6))
    assert p.role_face_ranges == ((2.9, 5.7), (6.3, 9.1), (9.7, 12.5))
    for layer, face in zip(p.carrier_layers, p.role_face_ranges):
        assert face[0] - layer[0] == pytest.approx(p.pinion_face_margin)
        assert layer[1] - face[1] == pytest.approx(p.pinion_face_margin)
        assert face[1] - face[0] == pytest.approx(p.output_face_width)


def test_259t_ring_and_16t_output_pinion_pitch_equations():
    assert (p.ring_module, p.ring_teeth, p.ring_pitch_radius) == (1.0, 259, 129.5)
    assert p.ring_pitch_radius == pytest.approx(p.ring_module * p.ring_teeth / 2.0)
    assert (p.output_pinion_teeth, p.output_pinion_pitch_radius) == (16, 8.0)
    assert p.output_pinion_pitch_radius == pytest.approx(
        p.ring_module * p.output_pinion_teeth / 2.0
    )
    assert p.output_axis_radius == pytest.approx(
        p.ring_pitch_radius - p.output_pinion_pitch_radius
    )
    assert p.output_axis_radius == pytest.approx(121.5)
    assert 0.15 <= p.output_mesh_backlash <= 0.30


def test_ratio_step_resolution_and_seconds_speed_are_derived():
    assert p.gear_ratio == pytest.approx(16.1875)
    assert p.carrier_full_step_degrees == pytest.approx(0.1111969111969112)
    assert p.carrier_microstep_degrees == pytest.approx(0.00694980694980695)
    assert p.seconds_motor_rpm == pytest.approx(16.1875)
    assert p.seconds_microsteps_per_second == pytest.approx(863.3333333333334)


def test_equal_16t_miter_pair_obeys_pitch_cone_face_width_rule():
    assert (p.miter_module, p.miter_teeth, p.miter_ratio) == (1.0, 16, 1.0)
    assert p.miter_pitch_radius == pytest.approx(p.miter_module * p.miter_teeth / 2.0)
    assert p.miter_pitch_angle_degrees == pytest.approx(45.0)
    assert p.miter_cone_distance == pytest.approx(11.313708498984761)
    assert p.miter_face_width_limit == pytest.approx(3.7712361663282534)
    assert p.miter_face_width == pytest.approx(3.2)
    assert p.miter_face_width <= p.miter_face_width_limit
    assert p.miter_outer_back_face_offset == pytest.approx(p.miter_pitch_radius)
    assert p.miter_vertical_back_face_z == pytest.approx(
        p.miter_axis_intersection_z + p.miter_outer_back_face_offset
    )


def test_real_nema8_d_shaft_is_full_length_and_never_reaches_output_shaft():
    assert (p.motor_shaft_diameter, p.motor_shaft_across_flat) == (4.0, 3.5)
    assert p.motor_shaft_length == pytest.approx(7.0)
    assert p.nominal_motor_shaft_range == pytest.approx((111.25, 118.25))
    assert p.nominal_motor_shaft_range[1] - p.nominal_motor_shaft_range[0] == pytest.approx(7.0)
    assert p.motor_adjustment == pytest.approx(0.5)
    assert p.motor_adjustment_slot_travel == pytest.approx(2.0 * p.motor_adjustment)
    assert p.worst_case_motor_shaft_tip_radius == pytest.approx(119.0)
    assert p.worst_case_motor_to_output_shaft_clearance == pytest.approx(0.5)
    assert p.worst_case_motor_to_output_shaft_clearance >= 0.5


def test_mr84_bearing_planes_span_and_common_upper_datum():
    assert (p.bearing_code, p.bearing_id, p.bearing_od, p.bearing_width) == (
        "MR84",
        4.0,
        8.0,
        3.0,
    )
    assert p.lower_bearing_range == pytest.approx((-21.0, -18.0))
    assert p.upper_bearing_range == pytest.approx((-3.0, 0.0))
    lower_center = sum(p.lower_bearing_range) / 2.0
    upper_center = sum(p.upper_bearing_range) / 2.0
    assert upper_center - lower_center == pytest.approx(p.bearing_center_span)
    assert p.bearing_center_span == pytest.approx(18.0)
    assert p.bearing_center_span / p.output_shaft_diameter == pytest.approx(4.5)
    assert p.upper_common_datum_z == pytest.approx(p.upper_bearing_range[1])
    assert p.miter_to_upper_bearing_clearance == pytest.approx(0.10)


def test_output_d_shaft_length_endplay_and_role_spacers_are_explicit():
    assert (p.output_shaft_diameter, p.output_shaft_across_flat) == (4.0, 3.5)
    assert p.output_shaft_length == pytest.approx(40.0)
    assert p.output_shaft_z == pytest.approx((-25.0, 15.0))
    assert p.output_shaft_z[1] - p.output_shaft_z[0] == pytest.approx(p.output_shaft_length)
    assert p.lower_collar_engagement == pytest.approx(2.85)
    assert p.lower_collar_engagement >= 2.0
    assert p.shaft_above_second_pinion == pytest.approx(2.5)
    assert p.endplay_range == pytest.approx((0.05, 0.15))
    assert p.endplay_range[0] <= p.target_endplay <= p.endplay_range[1]
    assert p.role_spacer_lengths == pytest.approx((2.85, 6.25, 9.65))
    for role, face in enumerate(p.role_face_ranges):
        assert p.spacer_length(role) + p.spacer_axial_relief == pytest.approx(
            face[0] - p.upper_common_datum_z
        )


def test_d_bores_m2_tap_pilots_and_backlash_slider_are_explicit():
    assert p.miter_output_bore_across_flat == pytest.approx(3.60)
    assert p.output_pinion_bore_across_flat == pytest.approx(3.60)
    assert p.output_shaft_bore_across_flat == pytest.approx(3.60)
    assert p.m2_tap_pilot_diameter == pytest.approx(1.60)
    assert p.lower_collar_screw_z == pytest.approx(-22.50)
    assert p.lower_collar_z[0] < p.lower_collar_screw_z < p.lower_collar_z[1]
    assert p.slider_half_stroke == pytest.approx(0.08)
    assert p.slider_total_stroke == pytest.approx(0.16)
    assert p.slider_running_clearance == pytest.approx(0.30)
    assert p.bearing_outer_race_inner_radius == pytest.approx(3.10)
    assert p.upper_retainer_to_miter_clearance == pytest.approx(1.10)
    assert p.lower_bearing_retainer_pilot_engagement == pytest.approx(1.50)
    assert p.upper_bearing_retainer_pilot_engagement == pytest.approx(1.60)
    assert p.saddle_clamp_count == 4
    assert p.saddle_clamp_y == pytest.approx(14.50)
    assert p.spacer_outer_diameter == pytest.approx(5.80)


def test_non_driven_planes_retain_radial_clearance_from_internal_teeth():
    assert p.shaft_to_non_driven_tooth_clearance == pytest.approx(5.0)
    assert p.spacer_to_non_driven_tooth_clearance == pytest.approx(4.1)
    assert p.bearing_to_non_driven_tooth_clearance == pytest.approx(3.0)
    assert min(
        p.shaft_to_non_driven_tooth_clearance,
        p.spacer_to_non_driven_tooth_clearance,
        p.bearing_to_non_driven_tooth_clearance,
    ) >= 3.0


def test_topology_helper_rejects_smooth_cones_and_accepts_16t_threshold():
    assert not p.miter_topology_has_teeth(
        tip_vertices=2,
        tooth_side_faces=1,
        periodic_faces=1,
    )
    assert not p.miter_topology_has_teeth(
        tip_vertices=31,
        tooth_side_faces=32,
        periodic_faces=16,
    )
    assert p.miter_topology_has_teeth(
        tip_vertices=32,
        tooth_side_faces=32,
        periodic_faces=16,
    )
