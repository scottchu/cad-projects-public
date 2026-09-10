"""Executable dimensional contract for P0 v2 captured shutters."""

import pytest

from pill_click.p0_v2 import P0V2


def test_frozen_state_coordinates() -> None:
    p = P0V2
    assert p.latched_center_y == pytest.approx(4.5)
    assert p.pressed_state == pytest.approx(0.0)
    assert p.released_state == pytest.approx(13.4)
    assert p.inward_state == pytest.approx(-1.0)
    assert p.maximum_pull_state == pytest.approx(13.55)


def test_pressed_apertures_are_fully_aligned() -> None:
    p = P0V2
    assert p.fixed_fill_interval() == pytest.approx((-4.5, 5.5))
    assert p.moving_fill_interval(0.0) == pytest.approx((-4.7, 5.7))
    assert p.fill_overlap(0.0) == pytest.approx(p.fixed_fill_length)
    assert p.fixed_outlet_interval() == pytest.approx((1.1, 5.9))
    assert p.moving_outlet_interval(0.0) == pytest.approx((0.9, 6.1))
    assert p.outlet_overlap(0.0) == pytest.approx(p.fixed_outlet_length)


def test_released_openings_hide_and_fixed_openings_are_backed() -> None:
    p = P0V2
    assert p.moving_fill_interval(13.4) == pytest.approx((8.7, 19.1))
    assert 20.0 - p.moving_fill_interval(13.4)[1] == pytest.approx(
        p.top_hidden_front_margin
    )
    assert p.moving_outlet_interval(13.4) == pytest.approx((14.3, 19.5))
    assert (
        p.bottom_opaque_front_boundary_y
        - p.moving_outlet_interval(13.4)[1]
    ) == pytest.approx(p.bottom_hidden_front_margin)

    assert p.top_shutter_interval(13.4) == pytest.approx((-5.0, 20.0))
    assert (
        p.fixed_fill_interval()[0] - p.top_shutter_interval(13.4)[0]
    ) == pytest.approx(p.top_fixed_backing_margin)
    assert p.bottom_shutter_interval(13.4) == pytest.approx((0.5, 20.0))
    assert (
        p.fixed_outlet_interval()[0] - p.bottom_shutter_interval(13.4)[0]
    ) == pytest.approx(p.bottom_fixed_backing_margin)


def test_pressed_shutter_envelopes_stay_inside_housing() -> None:
    p = P0V2
    assert p.top_shutter_interval(0.0) == pytest.approx((-18.4, 6.6))
    assert p.bottom_shutter_interval(0.0) == pytest.approx((-12.9, 6.6))
    for bounds in (p.top_shutter_interval(0.0), p.bottom_shutter_interval(0.0)):
        assert bounds[0] >= -20.0
        assert bounds[1] <= 20.0


def test_captured_shutter_section_math() -> None:
    p = P0V2
    assert p.shutter_web_thickness == pytest.approx(0.8)
    assert (p.shutter_flange_width - p.shutter_web_width) / 2 == pytest.approx(
        1.0
    )
    assert p.shutter_flange_thickness == pytest.approx(0.4)
    assert p.shutter_lateral_clearance == pytest.approx(0.2)
    assert p.shutter_vertical_clearance == pytest.approx(0.15)
    assert p.shutter_track_floor_clearance == pytest.approx(0.2)
    assert p.derived_lip_overlap == pytest.approx(0.8)
    assert p.derived_lip_overlap == pytest.approx(
        p.shutter_lip_capture_overlap
    )
    assert p.shutter_exterior_step == pytest.approx(0.1)
    assert 20.0 - p.top_shutter_exterior_z == pytest.approx(0.1)
    assert p.bottom_shutter_exterior_z - (-20.0) == pytest.approx(0.1)
    assert max(
        p.shutter_lateral_clearance,
        p.rear_cover_side_clearance,
        p.rear_cover_vertical_clearance,
    ) <= 0.25


def test_rail_land_and_entry_math_is_preserved() -> None:
    p = P0V2
    assert p.rail_count == 4
    assert p.rail_radial_height == pytest.approx(1.2)
    assert p.rail_tangential_width == pytest.approx(2.2)
    assert p.groove_radial_depth == pytest.approx(0.65)
    assert p.groove_width_nominal == pytest.approx(2.7)
    assert p.groove_width_loose == pytest.approx(2.8)
    assert p.rail_tip_x - p.groove_bottom_x == pytest.approx(0.2)
    assert (
        p.groove_width_nominal - p.rail_tangential_width
    ) / 2 == pytest.approx(0.25)
    assert p.rail_rear_lead_in == pytest.approx(0.7)
    assert p.groove_mouth_length == pytest.approx(0.6)
    assert p.bearing_center_spacing == pytest.approx(7.2)
    assert p.bearing_end_to_end_span == pytest.approx(10.6)

    expected = {
        -1.0: ((-10.30, -6.90), (-3.10, 0.30)),
        0.0: ((-9.30, -5.90), (-2.10, 1.30)),
        13.4: ((4.10, 7.50), (11.30, 14.70)),
        13.55: ((4.25, 7.65), (11.45, 14.85)),
    }
    for state, (rear_expected, front_expected) in expected.items():
        assert p.land_interval(state, p.rear_land_local_y) == pytest.approx(
            rear_expected
        )
        assert p.land_interval(state, p.front_land_local_y) == pytest.approx(
            front_expected
        )


def test_rear_channel_cover_and_snap_retention_math() -> None:
    p = P0V2
    assert p.rear_channel_width == pytest.approx(37.3)
    assert p.rear_channel_height == pytest.approx(35.8)
    assert p.key_face_size == pytest.approx(35.2)
    assert (p.rear_channel_width - p.key_face_size) / 2 == pytest.approx(1.05)
    assert (p.rear_channel_height - p.key_face_size) / 2 == pytest.approx(0.3)
    assert p.rear_cover_width == pytest.approx(37.0)
    assert p.rear_cover_height == pytest.approx(35.4)
    assert p.rear_cover_thickness == pytest.approx(2.4)
    assert p.rear_cover_side_clearance == pytest.approx(0.15)
    assert p.rear_cover_vertical_clearance == pytest.approx(0.2)
    assert p.rear_hook_count == 4
    assert p.rear_hook_tip_span == pytest.approx(38.9)
    assert p.derived_hook_overlap == pytest.approx(0.8)
    assert p.derived_hook_overlap == pytest.approx(
        p.rear_hook_extraction_overlap
    )
    assert p.rear_hook_chamfer == pytest.approx(0.7)
    assert p.rear_hook_cantilever_thickness == pytest.approx(1.2)
    assert p.rear_cover_back_y == pytest.approx(-20.0)


def test_out_of_range_states_are_rejected() -> None:
    with pytest.raises(ValueError):
        P0V2.shuttle_center_y(-1.01)
    with pytest.raises(ValueError):
        P0V2.shuttle_center_y(13.56)
