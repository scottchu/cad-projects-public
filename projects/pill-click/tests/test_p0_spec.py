"""Executable math contract for the progressive P0 manual slider."""

import pytest

from pill_click.p0.spec import P0


def test_states_and_derived_center_are_frozen() -> None:
    p = P0
    assert p.inward_state == pytest.approx(-1.0)
    assert p.pressed_state == pytest.approx(0.0)
    assert p.released_state == pytest.approx(13.4)
    assert p.maximum_pull_state == pytest.approx(13.55)
    assert p.latched_center_y == pytest.approx(4.5)
    assert p.released_state - p.inward_state == pytest.approx(14.4)


def test_aperture_alignment_overlap_and_ready_closure_math() -> None:
    p = P0
    assert p.fill_overlap(p.pressed_state) == pytest.approx(p.fill_length)
    assert p.outlet_overlap(p.pressed_state) == pytest.approx(p.outlet_length)
    assert p.fill_overlap(p.released_state) == pytest.approx(0.0)
    assert p.outlet_overlap(p.released_state) == pytest.approx(0.0)

    ready_fill_local = p.fixed_interval_in_shuttle_frame(
        p.fixed_fill_interval(), p.released_state
    )
    ready_outlet_local = p.fixed_interval_in_shuttle_frame(
        p.fixed_outlet_interval(), p.released_state
    )
    assert ready_fill_local == pytest.approx((-24.4, -14.4))
    assert ready_outlet_local == pytest.approx((-8.8, -4.0))
    assert ready_fill_local[0] >= p.roof_closure_local_start_y
    assert ready_fill_local[1] <= p.roof_closure_local_end_y
    assert ready_outlet_local[0] >= p.floor_closure_local_start_y
    assert ready_outlet_local[1] <= p.floor_closure_local_end_y

    assert p.fill_overlap(p.inward_state) == pytest.approx(9.0)
    assert p.outlet_overlap(p.inward_state) == pytest.approx(3.8)


def test_rail_and_groove_clearance_math_is_frozen() -> None:
    p = P0
    assert p.rail_count == 4
    assert p.rail_radial_height == pytest.approx(1.2)
    assert p.rail_tangential_width == pytest.approx(2.2)
    assert p.groove_radial_depth == pytest.approx(0.65)
    assert p.groove_width == pytest.approx(2.7)
    assert p.groove_width_coupon_loose == pytest.approx(2.8)
    assert p.rail_tip_x - p.groove_bottom_x == pytest.approx(0.20)
    assert (p.groove_width - p.rail_tangential_width) / 2 == pytest.approx(
        0.25
    )
    assert p.bearing_boss_outer_x == pytest.approx(17.90)
    assert p.rail_tip_x == pytest.approx(17.45)
    assert p.rail_root_x == pytest.approx(18.65)
    assert p.housing_inner_half_x == pytest.approx(p.rail_root_x)


def test_land_intervals_and_engagement_margins() -> None:
    p = P0
    assert p.bearing_center_spacing == pytest.approx(7.2)
    assert p.bearing_end_to_end_span == pytest.approx(10.6)

    expected = {
        p.inward_state: ((-10.30, -6.90), (-3.10, 0.30)),
        p.pressed_state: ((-9.30, -5.90), (-2.10, 1.30)),
        p.released_state: ((4.10, 7.50), (11.30, 14.70)),
        p.maximum_pull_state: ((4.25, 7.65), (11.45, 14.85)),
    }
    for state, (rear_expected, front_expected) in expected.items():
        rear = p.land_interval(state, p.rear_land_local_y)
        front = p.land_interval(state, p.front_land_local_y)
        assert rear == pytest.approx(rear_expected)
        assert front == pytest.approx(front_expected)
        assert rear[0] >= p.rail_start_y
        assert front[1] <= p.rail_end_y

    ready_front = p.land_interval(p.released_state, p.front_land_local_y)
    max_front = p.land_interval(p.maximum_pull_state, p.front_land_local_y)
    assert p.rail_end_y - ready_front[1] == pytest.approx(0.65)
    assert p.rail_end_y - max_front[1] == pytest.approx(0.50)


def test_captive_tab_and_independent_stop_math() -> None:
    p = P0
    assert p.tab_side_clearance == pytest.approx(0.20)
    assert p.tab_shoulder_overlap == pytest.approx(1.00)
    assert p.tab_local_front_y == pytest.approx(-2.70)
    assert p.ready_endplay == pytest.approx(0.15)

    inward_key_rear = (
        p.shuttle_center_y(p.inward_state) + p.shuttle_front_y
    )
    assert inward_key_rear == pytest.approx(p.inward_stop_plane_y)


def test_rear_assembly_and_key_recess_have_nominal_clearance() -> None:
    p = P0
    assert (p.rear_channel_width - p.captive_tab_overall_width) / 2 == pytest.approx(
        0.20
    )
    assert (p.rear_channel_width - 2 * p.bearing_boss_outer_x) / 2 == pytest.approx(
        0.75
    )
    assert (p.key_recess_size - p.key_face_size) / 2 == pytest.approx(0.20)
    assert (p.interior_height - p.rear_insert_height) / 2 == pytest.approx(0.15)


def test_medicine_walls_are_two_mm_or_greater() -> None:
    p = P0
    assert p.shuttle_width / 2 - p.shuttle_inner_half_x == pytest.approx(2.0)
    assert p.shuttle_height / 2 - p.shuttle_inner_half_z == pytest.approx(2.0)
    assert p.shuttle_inner_rear_y - p.shuttle_rear_y == pytest.approx(2.0)
    assert p.shuttle_front_y - p.shuttle_inner_front_y == pytest.approx(2.0)


def test_out_of_range_states_are_rejected() -> None:
    with pytest.raises(ValueError):
        P0.shuttle_center_y(P0.inward_state - 0.01)
    with pytest.raises(ValueError):
        P0.shuttle_center_y(P0.maximum_pull_state + 0.01)
