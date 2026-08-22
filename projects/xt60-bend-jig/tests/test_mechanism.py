from itertools import combinations
from math import pi, sqrt

import pytest

from xt60_bend_jig.mechanism import PointYZ, solve_mechanism
from xt60_bend_jig.parameters import DEFAULT_PARAMETERS, WIRE_DIAMETERS


def test_closed_wire_path_is_an_exact_ninety_degree_bend() -> None:
    solution = solve_mechanism()
    assert solution.bend_angle_degrees == 90.0
    assert solution.bend_start == PointYZ(16.0, 10.0)
    assert solution.bend_center == PointYZ(16.0, 16.0)
    assert solution.vertical_leg_start == PointYZ(22.0, 16.0)
    assert solution.wire_path[0] == PointYZ(-6.0, 10.0)
    assert solution.wire_path[-2] == pytest.approx(PointYZ(22.0, 16.0))
    assert solution.wire_endpoint.y == pytest.approx(22.0)
    assert solution.wire_endpoint.z == pytest.approx(44.0 - 22.0 - 3.0 * pi + 16.0)
    assert solution.path_length == pytest.approx(44.0, abs=1e-12)


@pytest.mark.parametrize("wire_gauge", [12, 14])
@pytest.mark.parametrize("upper_index", range(3))
@pytest.mark.parametrize("lower_index", range(3))
def test_all_closed_rods_are_exactly_tangent_for_both_wire_gauges(
    wire_gauge: int, upper_index: int, lower_index: int
) -> None:
    solution = solve_mechanism(
        wire_gauge=wire_gauge,
        upper_index=upper_index,
        lower_index=lower_index,
        available_lead_length=60.0,
    )
    assert solution.wire_diameter == WIRE_DIAMETERS[wire_gauge]
    assert solution.upper_rod_center.distance_to(solution.upper_contact) == pytest.approx(
        solution.contact_radius, abs=1e-12
    )
    assert solution.lower_rod_center.distance_to(solution.lower_contact) == pytest.approx(
        solution.contact_radius, abs=1e-12
    )
    assert solution.moving_rod_center.distance_to(solution.moving_contact) == pytest.approx(
        solution.contact_radius, abs=1e-12
    )
    assert all(abs(gap) < 1e-12 for gap in solution.contact_gaps.values())


@pytest.mark.parametrize("wire_gauge", [12, 14])
def test_rods_do_not_overlap_at_any_reaction_position(wire_gauge: int) -> None:
    for upper_index in range(3):
        for lower_index in range(3):
            solution = solve_mechanism(
                wire_gauge=wire_gauge,
                upper_index=upper_index,
                lower_index=lower_index,
                available_lead_length=60.0,
            )
            for first, second in combinations(solution.rod_centers.values(), 2):
                assert first.distance_to(second) >= solution.parameters.rod_diameter


def test_closed_centers_are_derived_from_combined_contact_radius() -> None:
    solution = solve_mechanism(wire_gauge=12)
    radius = 2.0 + 4.3 / 2.0
    diagonal = 1.0 / sqrt(2.0)
    assert solution.lower_rod_center == PointYZ(6.5, 10.0 - radius)
    assert solution.upper_rod_center == PointYZ(22.0 - radius, 28.5)
    assert solution.moving_closed_center.y == pytest.approx(16.0 + (6.0 + radius) * diagonal)
    assert solution.moving_closed_center.z == pytest.approx(16.0 - (6.0 + radius) * diagonal)


def test_finite_path_conserves_available_length_across_closure() -> None:
    for lead_length in (32.0, 44.0, 60.0):
        for step in range(11):
            closure = step / 10.0
            solution = solve_mechanism(
                closure=closure,
                available_lead_length=lead_length,
            )
            assert solution.path_length == pytest.approx(lead_length, abs=1e-12)
            rendered_length = sum(
                first.distance_to(second)
                for first, second in zip(solution.wire_path, solution.wire_path[1:])
            )
            assert rendered_length == pytest.approx(lead_length, abs=0.002)


def test_default_length_marks_third_upper_position_unreachable() -> None:
    first = solve_mechanism(upper_index=0)
    second = solve_mechanism(upper_index=1)
    third = solve_mechanism(upper_index=2)
    assert first.upper_contact_reachable and first.usable
    assert second.upper_contact_reachable and second.usable
    assert not third.upper_contact_reachable
    assert not third.usable
    assert third.status == "upper-contact-unreachable"
    assert third.minimum_required_lead_length == pytest.approx(22.0 + 3.0 * pi + 19.0)
    assert third.contact_gaps["upper"] > 0.0
    assert third.upper_contact == third.wire_endpoint


def test_contact_gaps_are_measured_to_actual_finite_path() -> None:
    solution = solve_mechanism(upper_index=2)
    expected = solution.upper_rod_center.distance_to(solution.wire_endpoint) - solution.contact_radius
    assert solution.contact_gaps["upper"] == pytest.approx(expected, abs=1e-12)
    assert solution.contact_gaps["lower"] == pytest.approx(0.0, abs=1e-12)
    assert solution.contact_gaps["moving"] == pytest.approx(0.0, abs=1e-12)


def test_moving_rod_uses_outward_positive_y_negative_z_unit_vector() -> None:
    solution = solve_mechanism(closure=0.0)
    direction = solution.moving_outward_unit
    assert direction.y == pytest.approx(1.0 / sqrt(2.0))
    assert direction.z == pytest.approx(-1.0 / sqrt(2.0))
    assert direction.magnitude == pytest.approx(1.0)
    assert solution.moving_retraction == pytest.approx(11.0)


def test_moving_angle_parameter_controls_slot_and_screw_axis() -> None:
    from xt60_bend_jig.parameters import PrototypeParameters

    solution = solve_mechanism(params=PrototypeParameters(moving_angle_degrees=30.0))
    assert solution.moving_outward_unit.y == pytest.approx(sqrt(3.0) / 2.0)
    assert solution.moving_outward_unit.z == pytest.approx(-0.5)
    assert solution.screw_axis_direction == solution.moving_outward_unit
    assert solution.contact_gaps["moving"] == pytest.approx(0.0, abs=1e-12)


def test_closing_motion_is_monotonic_and_finishes_at_closed_center() -> None:
    solutions = [solve_mechanism(closure=index / 10.0) for index in range(11)]
    distances = [solution.moving_retraction for solution in solutions]
    assert distances == pytest.approx([11.0 - 1.1 * index for index in range(11)])
    assert all(right < left for left, right in zip(distances, distances[1:]))
    assert solutions[-1].moving_rod_center == solutions[-1].moving_closed_center


def test_parallel_end_guides_and_m4_axis_have_zero_ideal_skew() -> None:
    for closure in (0.0, 0.25, 0.5, 0.75, 1.0):
        solution = solve_mechanism(closure=closure)
        assert solution.left_moving_axis == solution.right_moving_axis
        assert solution.ideal_skew == 0.0
        assert solution.axis_collinearity_error == 0.0
        assert solution.screw_axis_direction == solution.moving_outward_unit


def test_clearance_contact_and_thermal_acceptance_margins() -> None:
    params = DEFAULT_PARAMETERS
    assert params.reference_board_width == 36.0
    assert params.nominal_frame_clearance == 1.0
    for lower_index in range(3):
        solution = solve_mechanism(lower_index=lower_index)
        assert solution.frame_clearance >= 0.5
        assert solution.pad_to_contact >= 6.0
        assert solution.iron_to_petg_clearance >= 12.0
    assert params.rod_end_protrusion == 2.0


@pytest.mark.parametrize("bad_gauge", [10, 16])
def test_unsupported_wire_gauges_are_rejected(bad_gauge: int) -> None:
    with pytest.raises(ValueError, match="unsupported"):
        solve_mechanism(wire_gauge=bad_gauge)


@pytest.mark.parametrize("closure", [-0.01, 1.01])
def test_closure_must_be_normalized(closure: float) -> None:
    with pytest.raises(ValueError, match="closure"):
        solve_mechanism(closure=closure)


def test_lead_too_short_for_requested_bend_is_rejected() -> None:
    with pytest.raises(ValueError, match="too short for the bend"):
        solve_mechanism(closure=1.0, available_lead_length=31.0)
