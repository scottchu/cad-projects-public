from __future__ import annotations

from math import isclose

import pytest

from xt60_bend_jig.p17_compact_plate_optimizer import (
    CompactCandidate,
    DEFAULT_CANDIDATE,
    aligned_xt60_center,
    boundary_web_for_inner_diameter,
    derive_metrics,
    evaluate_candidate,
    fixed_inner_track,
    outer_rail_local,
    placed_guide_point,
    render_svg,
    select_candidate,
    side_angle,
    wire_route_front,
    world_from_outer_local,
)
from xt60_bend_jig.p17_r2_direct_counter_twist import ROD_NAMES


def _same_point(a, b, tolerance: float = 1e-9) -> bool:
    return isclose(a.y, b.y, abs_tol=tolerance) and isclose(a.z, b.z, abs_tol=tolerance)


def test_exact_candidate_and_fixed_orientation_contract() -> None:
    candidate = DEFAULT_CANDIDATE
    metrics = derive_metrics(candidate)
    assert evaluate_candidate(candidate).valid
    assert candidate.theta_deg == 45.0
    assert candidate.rotation_center.as_tuple() == (0.0, 0.0)
    assert candidate.rigid_shift.as_tuple() == (-14.6869657526, -12.2949747468)
    assert candidate.fixed_axle.as_tuple() == (-9.5, -9.5)
    assert isclose(metrics.raw_inner_diameter, 52.932202652842975, abs_tol=1e-12)
    assert isclose(metrics.raw_left_outer_diameter, 50.30769103922032, abs_tol=1e-12)
    assert isclose(metrics.raw_right_outer_diameter, 50.30769103922032, abs_tol=1e-12)
    assert metrics.inner_diameter == 52.933
    assert metrics.left_outer_diameter == 53.933
    assert metrics.right_outer_diameter == 54.933
    assert isclose(metrics.min_internal_web, 2.5977324813688853, abs_tol=1e-12)
    assert metrics.internal_limit.plate == "right_outer"
    assert (metrics.internal_limit.first_feature, metrics.internal_limit.second_feature) == (
        "upright",
        "fixed_axle",
    )
    assert _same_point(aligned_xt60_center(candidate), type(candidate.fixed_axle)(-5.0, 20.5))
    assert candidate.fixed_axle.y < aligned_xt60_center(candidate).y


def test_plate_sizes_are_derived_not_user_supplied_literals() -> None:
    with pytest.raises(TypeError):
        CompactCandidate(inner_diameter=52.933)  # type: ignore[call-arg]
    changed = CompactCandidate(required_web=2.30)
    assert derive_metrics(changed).inner_diameter == 53.133
    assert derive_metrics(changed).inner_diameter != derive_metrics(DEFAULT_CANDIDATE).inner_diameter


def test_derived_metrics_recompute_byte_for_byte_deterministically() -> None:
    first = derive_metrics(DEFAULT_CANDIDATE)
    derive_metrics.cache_clear()
    second = derive_metrics(DEFAULT_CANDIDATE)
    assert first == second


def test_true_limiting_bottom_track_marker_and_boundary_falsification() -> None:
    metrics = derive_metrics(DEFAULT_CANDIDATE)
    limit = metrics.boundary_limit
    assert (limit.plate, limit.feature) == ("fixed_inner", "bottom_start")
    assert _same_point(limit.center, type(limit.center)(-20.8852813742, 7.5))
    assert _same_point(
        limit.cutter_edge,
        type(limit.center)(-22.838179439690173, 8.201294621257519),
    )
    assert _same_point(
        limit.plate_edge,
        type(limit.center)(-24.909097180865416, 8.944970647475733),
    )
    assert isclose(limit.actual_web, 2.2003986735785106, abs_tol=1e-12)
    assert boundary_web_for_inner_diameter(metrics.inner_diameter) >= 2.20
    assert boundary_web_for_inner_diameter(metrics.inner_diameter - 0.001) < 2.20


def test_open_and_end_topology_are_the_frozen_p17_triangles() -> None:
    bottom_open = placed_guide_point("bottom", 0.0)
    diagonal_open = placed_guide_point("diagonal", 0.0)
    upright_open = placed_guide_point("upright", 0.0)
    assert isclose(bottom_open.z, diagonal_open.z, abs_tol=1e-9)
    assert isclose(diagonal_open.y, upright_open.y, abs_tol=1e-9)
    assert bottom_open.y < diagonal_open.y
    assert upright_open.z < diagonal_open.z

    bottom_end = placed_guide_point("bottom", 1.0)
    diagonal_end = placed_guide_point("diagonal", 1.0)
    upright_end = placed_guide_point("upright", 1.0)
    assert bottom_end.y < diagonal_end.y < upright_end.y
    assert bottom_end.z > diagonal_end.z > upright_end.z
    # The accepted END is the frozen upper-left -> middle -> lower-right
    # diagonal chain. It is intentionally not asserted to be mathematically
    # collinear; that would replace the current P17 guide endpoints.
    open_width = diagonal_open.y - bottom_open.y
    end_width = upright_end.y - bottom_end.y
    assert end_width < open_width


def test_fixed_inner_tracks_are_straight_and_contain_both_endpoints() -> None:
    for name in ROD_NAMES:
        start, end = fixed_inner_track(name)
        open_point = placed_guide_point(name, 0.0)
        end_point = placed_guide_point(name, 1.0)
        direction = (end.y - start.y, end.z - start.z)
        for point in (open_point, end_point):
            cross = (point.y - start.y) * direction[1] - (point.z - start.z) * direction[0]
            assert abs(cross) < 1e-8


def test_wire_route_is_exact_aligned_p17_front_projection() -> None:
    route = wire_route_front()
    assert _same_point(route[0], type(route[0])(-5.0, 20.5))
    assert _same_point(route[1], type(route[0])(-5.0, 1.5))
    assert _same_point(route[-2], type(route[0])(1.0, -4.5))
    assert _same_point(route[-1], type(route[0])(13.0, -4.5))


def test_all_six_outer_rails_reconstruct_the_same_three_rod_motion() -> None:
    candidate = DEFAULT_CANDIDATE
    samples = candidate.sample_count
    for side in ("left", "right"):
        assert side_angle(side, candidate.theta_deg) == (-45.0 if side == "left" else 45.0)
        for name in ROD_NAMES:
            rail = outer_rail_local(side, name, candidate)
            assert len(rail) == samples
            for index in (0, samples // 2, samples - 1):
                u = index / (samples - 1)
                reconstructed = world_from_outer_local(rail[index], side, u, candidate)
                assert _same_point(reconstructed, placed_guide_point(name, u, candidate), 1e-8)


def test_selection_is_deterministic_and_prefers_frozen_objective_order() -> None:
    candidate = DEFAULT_CANDIDATE
    lower_twist = type(candidate)(theta_deg=44.0)
    assert select_candidate((lower_twist, candidate)) == candidate
    assert select_candidate((candidate, lower_twist)) == candidate


def test_svg_is_byte_deterministic_and_contains_required_gate_labels() -> None:
    first = render_svg()
    second = render_svg()
    assert first == second
    for text in (
        "P17 R2",
        "OPEN",
        "END / LOCKED GEOMETRY",
        "+Z head/up",
        "+Y solder tail &amp; wires/right",
        "bottom",
        "diagonal",
        "upright",
        "left −45°",
        "right +45°",
        "A fixed axle",
        "bottom start cutter → plate: 2.2004 ≥ 2.20",
        "inverse-derived outer rails",
        "2 wires, coincident in FRONT",
    ):
        assert text in first
