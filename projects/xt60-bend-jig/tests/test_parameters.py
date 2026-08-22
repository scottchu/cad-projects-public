import pytest

from xt60_bend_jig.parameters import (
    DEFAULT_PARAMETERS,
    FIT_COUPON_SIZES,
    WIRE_DIAMETERS,
    PrototypeParameters,
)


def test_rod_stack_has_exact_span_and_end_protrusion() -> None:
    params = DEFAULT_PARAMETERS
    assert params.rod_diameter == 4.0
    assert params.rod_length == 50.0
    assert params.clear_span == 38.0
    assert params.side_plate_thickness == 4.0
    assert params.outer_span == 46.0
    assert params.rod_end_protrusion == 2.0


def test_wire_and_bend_envelopes_are_named() -> None:
    params = DEFAULT_PARAMETERS
    assert WIRE_DIAMETERS == {12: 4.3, 14: 3.5}
    assert params.wire_center_z == 10.0
    assert params.bend_start_y == 16.0
    assert params.bend_radius == 6.0
    assert params.vertical_leg_y == 22.0
    assert params.available_lead_length == 44.0


def test_three_reaction_positions_have_safe_pitch_and_web() -> None:
    params = DEFAULT_PARAMETERS
    assert params.lower_reaction_y_positions == (0.0, 6.5, 13.0)
    assert params.upper_reaction_z_positions == (22.0, 28.5, 35.0)
    for positions in (params.lower_reaction_y_positions, params.upper_reaction_z_positions):
        pitches = [right - left for left, right in zip(positions, positions[1:])]
        assert min(pitches) >= 6.5
        assert min(pitches) > params.rod_diameter


def test_motion_fasteners_and_clearances_are_explicit() -> None:
    params = DEFAULT_PARAMETERS
    assert params.moving_angle_degrees == 45.0
    assert params.moving_stroke == 11.0
    assert params.slot_width == 4.6
    assert params.m4_screw_diameter == 4.0
    assert params.m4_clearance_diameter == 4.5
    assert params.m4_nut_across_flats == 7.0
    assert params.m4_nut_thickness == 3.2
    assert params.m4_nut_trap_across_flats == pytest.approx(7.2)
    assert params.running_clearance_per_side == 0.25


def test_xt60_cradle_and_fit_coupon_allowances_are_exact() -> None:
    params = DEFAULT_PARAMETERS
    assert (params.xt60_width, params.xt60_depth, params.xt60_length) == (15.9, 8.1, 20.5)
    assert params.cradle_clearance_per_side == 0.4
    assert params.cradle_opening == pytest.approx((16.7, 8.9, 21.3))
    assert params.fit_coupon_sizes == FIT_COUPON_SIZES == (4.2, 4.3, 4.4, 4.5)


def test_invalid_acceptance_parameters_fail_early() -> None:
    with pytest.raises(ValueError, match="pitch"):
        PrototypeParameters(reaction_position_pitch=6.49)
    with pytest.raises(ValueError, match="frame clearance"):
        PrototypeParameters(reference_board_width=37.1)
    with pytest.raises(ValueError, match="PETG"):
        PrototypeParameters(designed_iron_to_petg_clearance=11.99)
    with pytest.raises(ValueError, match="rod length"):
        PrototypeParameters(rod_length=45.99)
    with pytest.raises(ValueError, match="moving angle"):
        PrototypeParameters(moving_angle_degrees=90.0)
