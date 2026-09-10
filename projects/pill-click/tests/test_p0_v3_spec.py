"""Named-variable and derived-equation contract for accepted P0 v3."""

import pytest

from pill_click.p0_v3 import P0V3


def test_state_and_lost_motion_contract() -> None:
    p = P0V3
    assert p.latched_center_y == pytest.approx(4.50)
    assert p.shutter_q(-1.00) == pytest.approx(0.00)
    assert p.shutter_q(0.00) == pytest.approx(0.00)
    assert p.shutter_q(13.40) == pytest.approx(13.40)
    assert p.shutter_q(13.55) == pytest.approx(13.55)
    assert p.relative_lost_motion(-1.00) == pytest.approx(-1.00)
    assert p.relative_lost_motion(0.00) == pytest.approx(0.00)


def test_printable_shutter_track_section_equations() -> None:
    p = P0V3
    assert p.shutter_web_thickness == pytest.approx(0.80)
    assert p.shutter_flange_thickness == pytest.approx(0.80)
    assert p.opaque_shroud_thickness == pytest.approx(0.80)
    assert p.shutter_exterior_recess == pytest.approx(0.20)
    assert p.track_lateral_clearance == pytest.approx(0.20)
    assert p.track_lateral_clearance_per_side == pytest.approx(0.20)
    assert (p.track_web_width - p.shutter_web_width) / 2 == pytest.approx(0.20)
    assert p.track_vertical_clearance == pytest.approx(0.20)
    assert p.track_floor_clearance == pytest.approx(0.20)
    assert p.track_capture_overlap == pytest.approx(1.00)
    assert p.track_capture_overlap_per_side == pytest.approx(1.00)


def test_solid_shutter_and_aperture_intervals() -> None:
    p = P0V3
    assert p.fixed_fill_interval() == pytest.approx((-4.50, 5.50))
    assert p.top_shutter_interval_q(0.00) == pytest.approx((-18.40, -5.10))
    assert p.top_shutter_interval_q(13.40) == pytest.approx((-5.00, 8.30))
    assert p.top_shutter_interval_q(13.55) == pytest.approx((-4.85, 8.45))
    assert p.moving_fill_interval(0.00) == pytest.approx((-4.50, 5.50))
    assert p.moving_fill_interval(13.40) == pytest.approx((8.90, 18.90))
    assert p.fixed_fill_interval()[0] - p.top_shutter_interval_q(0.0)[1] == pytest.approx(0.60)
    assert p.fixed_fill_interval()[0] - p.top_shutter_interval_q(13.4)[0] == pytest.approx(0.50)
    assert p.top_opaque_shroud_rear_y - p.top_shutter_interval_q(13.55)[1] == pytest.approx(0.25)

    assert p.fixed_outlet_interval() == pytest.approx((0.80, 5.60))
    assert p.bottom_shutter_interval_q(0.00) == pytest.approx((-18.40, 0.20))
    assert p.bottom_shutter_interval_q(13.40) == pytest.approx((-5.00, 13.60))
    assert p.bottom_shutter_interval_q(13.55) == pytest.approx((-4.85, 13.75))
    assert p.moving_outlet_interval(0.00) == pytest.approx((0.80, 5.60))
    assert p.moving_outlet_interval(13.40) == pytest.approx((14.20, 19.00))
    assert p.fixed_outlet_interval()[0] - p.bottom_shutter_interval_q(0.0)[1] == pytest.approx(0.60)
    assert p.bottom_opaque_shroud_rear_y - p.bottom_shutter_interval_q(13.55)[1] == pytest.approx(0.25)


def test_release_backlash_retains_required_margins() -> None:
    p = P0V3
    for q in (13.30, 13.40, 13.50):
        assert p.fixed_fill_interval()[0] - p.top_shutter_interval_q(q)[0] >= 0.40 - 1e-9
        assert p.top_opaque_shroud_rear_y - p.top_shutter_interval_q(q)[1] >= 0.30 - 1e-9
        assert p.bottom_opaque_shroud_rear_y - p.bottom_shutter_interval_q(q)[1] >= 0.30 - 1e-9


def test_coupling_socket_and_envelopes() -> None:
    p = P0V3
    assert p.coupling_socket_length_y == pytest.approx(
        p.coupling_lug_length_y + p.coupling_lost_motion + 2 * p.coupling_end_clearance
    )
    assert p.coupling_rearward_shift_y == pytest.approx(-9.00)
    assert p.top_lug_local_y == pytest.approx((-20.60, -19.40))
    assert p.top_socket_local_y == pytest.approx((-20.70, -18.30))
    assert p.bottom_lug_local_y == pytest.approx((-14.60, -13.40))
    assert p.bottom_socket_local_y == pytest.approx((-14.70, -12.30))
    assert p.top_complete_coupling_local_y == pytest.approx((-21.30, -10.60))
    assert p.bottom_complete_coupling_local_y == pytest.approx((-15.30, -4.60))
    assert p.top_coupling_channel_front_y == pytest.approx(7.65)
    assert p.bottom_coupling_channel_front_y == pytest.approx(13.65)
    assert p.top_coupling_aperture_y_clearance == pytest.approx(1.60)
    assert p.bottom_coupling_aperture_y_clearance == pytest.approx(0.90)
    assert min(
        p.top_coupling_aperture_y_clearance,
        p.bottom_coupling_aperture_y_clearance,
    ) >= 0.60
    assert p.coupling_socket_width_x - p.coupling_lug_width_x == pytest.approx(0.40)
    assert p.coupling_channel_width / 2 == pytest.approx(2.70)
    assert p.estimated_detent_strain == pytest.approx(0.009375)
    assert p.estimated_detent_strain < 0.03


def test_rear_feed_guide_and_captivity_math() -> None:
    p = P0V3
    assert p.rear_channel_wall == pytest.approx(1.35)
    assert p.key_main_clearance == pytest.approx(0.20)
    assert (p.rear_channel_width - p.key_face_size) / 2 == pytest.approx(1.05)
    assert (p.rear_channel_height - p.key_face_size) / 2 == pytest.approx(0.30)
    assert p.tab_rear_channel_clearance == pytest.approx(0.20)
    assert p.tab_stop_pad_overlap == pytest.approx(1.00)
    assert p.released_endplay == pytest.approx(0.15)
    assert p.shuttle_center_y(p.maximum_pull_state) + p.tab_local_front_y == pytest.approx(p.front_shoulder_y)
    assert p.feed_sample_count == 390
    assert len(p.feed_states()) == 390
    assert p.feed_states()[0] == pytest.approx(-34.40)
    assert p.feed_states()[-1] == pytest.approx(4.50)


def test_c1r1_strengthened_land_and_backing_rib_math() -> None:
    p = P0V3
    assert p.land_length == pytest.approx(6.80)
    assert p.bearing_boss_width == pytest.approx(4.30)
    assert p.groove_width_nominal == pytest.approx(2.70)
    assert p.normal_lip_per_side == pytest.approx(0.80)
    assert p.mouth_lip_per_side == pytest.approx(0.60)
    assert p.rear_land_local_y == pytest.approx(-13.80)
    assert p.front_land_local_y == pytest.approx(-6.60)
    assert p.longitudinal_land_gap == pytest.approx(0.40)
    assert p.rear_land_backing_radial_thickness == pytest.approx(0.80)
    assert p.rear_land_backing_body_overlap_y == pytest.approx(0.20)
    assert p.rear_land_backing_local_y == pytest.approx((-17.20, -12.80))

    expected = {
        -1.00: ((-13.70, -6.90), (-6.50, 0.30)),
        0.00: ((-12.70, -5.90), (-5.50, 1.30)),
        13.40: ((0.70, 7.50), (7.90, 14.70)),
        13.55: ((0.85, 7.65), (8.05, 14.85)),
    }
    for state, (rear, front) in expected.items():
        assert p.land_interval(state, p.rear_land_local_y) == pytest.approx(rear)
        assert p.land_interval(state, p.front_land_local_y) == pytest.approx(front)
        assert front[0] - rear[1] == pytest.approx(0.40)
    assert p.rail_end_y - expected[13.55][1][1] == pytest.approx(0.50)
    assert expected[-1.00][0][0] - p.rail_start_y == pytest.approx(5.00)


def test_faceplate_pilot_stops_and_snap_math() -> None:
    p = P0V3
    assert p.rear_faceplate_interior_y - p.rear_faceplate_exterior_y == pytest.approx(1.30)
    assert -18.40 - p.rear_faceplate_interior_y == pytest.approx(0.30)
    assert p.rear_cover_pilot_x_clearance == pytest.approx(0.20)
    assert p.rear_cover_pilot_z_clearance == pytest.approx(0.25)
    assert p.rear_snap_center_x == pytest.approx(16.20)
    assert p.rear_snap_top_hook_apex_z - p.rear_snap_top_beam_outer_z == pytest.approx(0.55)
    assert p.rear_snap_pocket_outer_z - p.rear_snap_top_hook_apex_z == pytest.approx(0.10)
    assert 20.0 - p.rear_snap_pocket_outer_z == pytest.approx(1.20)
    assert p.nominal_snap_strain == pytest.approx(0.0176, abs=1e-4)
    assert p.worst_snap_strain == pytest.approx(0.0208, abs=1e-4)
    assert p.worst_snap_strain < 0.03
    assert -9.50 - p.rear_snap_pocket_front_y == pytest.approx(0.35)


def test_out_of_range_motion_is_rejected() -> None:
    with pytest.raises(ValueError):
        P0V3.shutter_q(-1.01)
    with pytest.raises(ValueError):
        P0V3.shuttle_center_y(13.56)
