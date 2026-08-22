"""Geometry and isolation contracts for the KAGE P3 V2 comparison models."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest
from OCP.BRepCheck import BRepCheck_Analyzer

from p3_v2_three_ring_comparison_geometry import make_concentric_three_ring, make_stacked_three_ring
from p3_v2_three_ring_comparison_spec import P3_V1_ISOLATION_SHA256, P3_V2 as p


ROOT = Path(__file__).resolve().parents[1]


def _children(shape):
    return list(shape.children)


def _assert_valid_positive_solid(shape):
    assert BRepCheck_Analyzer(shape.wrapped).IsValid()
    assert shape.is_valid
    assert shape.volume > 0.0
    assert len(shape.solids()) == 1


def test_p3_v1_checkpoint_is_untouched():
    for relative, expected in P3_V1_ISOLATION_SHA256.items():
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_frozen_stack_and_concentric_math():
    assert p.frame_outer_radius * 2.0 == pytest.approx(300.0)
    assert p.stacked_z_starts == pytest.approx((2.7, 4.8, 6.9))
    assert p.stacked_axial_gap == pytest.approx(0.30)
    assert p.stacked_total_height == pytest.approx(6.0)
    assert p.stacked_fin_lane_gap == pytest.approx(0.60)
    assert p.concentric_radial_gap == pytest.approx(4.0)
    assert p.concentric_center_clear_diameter == pytest.approx(229.0)


def test_stacked_assembly_has_frame_and_three_valid_moving_bodies():
    children = _children(make_stacked_three_ring())
    assert len(children) == 4
    for child in children:
        _assert_valid_positive_solid(child)
    moving = children[1:]
    for lower, upper in zip(moving, moving[1:]):
        assert upper.bounding_box().min.Z - lower.bounding_box().min.Z == pytest.approx(p.stacked_pitch)
        assert sum(piece.volume for piece in (lower.intersect(upper) or [])) == pytest.approx(0.0, abs=1e-8)


def test_stacked_fins_have_collision_free_radial_lanes_at_full_overlap():
    half = p.fin_radial_width / 2.0
    intervals = [(radius - half, radius + half) for radius in p.stacked_fin_radii]
    assert intervals[1][0] - intervals[0][1] == pytest.approx(0.6)
    assert intervals[2][0] - intervals[1][1] == pytest.approx(0.6)
    ring_interval = (
        p.stacked_carrier_radius - p.carrier_radial_width / 2.0,
        p.stacked_carrier_radius + p.carrier_radial_width / 2.0,
    )
    for start, end in intervals:
        assert end <= ring_interval[0] - 0.3 + 1e-9


def test_concentric_assembly_has_three_disjoint_valid_carriers():
    children = _children(make_concentric_three_ring())
    assert len(children) == 4
    for child in children:
        _assert_valid_positive_solid(child)
    moving = children[1:]
    for inner, outer in zip(moving, moving[1:]):
        assert sum(piece.volume for piece in (inner.intersect(outer) or [])) == pytest.approx(0.0, abs=1e-8)


@pytest.mark.parametrize("factory", [make_stacked_three_ring, make_concentric_three_ring])
def test_assembly_bounds_remain_inside_300mm_frame(factory):
    assembly = factory()
    bounds = assembly.bounding_box()
    assert bounds.size.X == pytest.approx(300.0)
    assert bounds.size.Y == pytest.approx(300.0)
    assert max(abs(bounds.min.X), abs(bounds.max.X), abs(bounds.min.Y), abs(bounds.max.Y)) <= 150.0 + 1e-9
