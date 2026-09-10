"""BREP validity, collision, aperture-ray, and rear-cover tests for P0 v2."""

import pytest
from build123d import Align, Box, Location

from pill_click.p0_v2 import (
    P0V2,
    make_blind_rear_cover,
    make_bottom_shutter,
    make_housing,
    make_p0_v2_assembly,
    make_rail_coupon,
    make_shuttle,
    make_top_shutter,
)


def _box(
    size_x: float,
    size_y: float,
    size_z: float,
    center: tuple[float, float, float],
):
    return Box(
        size_x,
        size_y,
        size_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location(center))


def _intersection_volume(first, second) -> float:
    return (first & second).volume


def test_all_v2_parts_are_valid_single_solids() -> None:
    parts = [
        make_housing(),
        make_blind_rear_cover(),
        make_shuttle(),
        make_top_shutter(),
        make_bottom_shutter(),
    ]
    assert all(part.is_valid and part.volume > 0 for part in parts)
    assert all(len(part.solids()) == 1 for part in parts)


def test_v2_assemblies_have_only_the_five_frozen_parts() -> None:
    expected_fragments = {
        "fixed_housing",
        "blind_rear_cover",
        "shuttle",
        "top_shutter",
        "bottom_shutter",
    }
    for state in (P0V2.pressed_state, P0V2.released_state):
        assembly = make_p0_v2_assembly(state)
        labels = {child.label for child in assembly.children}
        assert assembly.is_valid
        assert len(labels) == 5
        assert all(any(fragment in label for label in labels) for fragment in expected_fragments)
        forbidden = ("spring", "magnet", "cam", "follower", "gate", "plunger")
        assert not any(token in label for token in forbidden for label in labels)


def test_dense_point_one_mm_sweep_is_collision_free() -> None:
    p = P0V2
    housing = make_housing(p)
    cover = make_blind_rear_cover(p).moved(
        Location((0.0, p.rear_cover_back_y + p.rear_cover_thickness / 2, 0.0))
    )
    shuttle = make_shuttle(p)
    top = make_top_shutter(p)
    bottom = make_bottom_shutter(p)
    assert _intersection_volume(housing, cover) < 1e-6

    states = [round(p.inward_state + index * 0.10, 2) for index in range(146)]
    states.append(p.maximum_pull_state)
    assert states[0] == pytest.approx(-1.0)
    assert states[-2] == pytest.approx(13.5)
    assert states[-1] == pytest.approx(13.55)
    assert len(states) == 147

    for state in states:
        location = Location((0.0, p.shuttle_center_y(state), 0.0))
        moving = [
            location * shuttle,
            location * top,
            location * bottom,
        ]
        for part in moving:
            assert _intersection_volume(housing, part) < 1e-6
            assert _intersection_volume(cover, part) < 1e-6
        for index, first in enumerate(moving):
            for second in moving[index + 1 :]:
                assert _intersection_volume(first, second) < 1e-6


def test_pressed_full_fixed_aperture_rays_are_open() -> None:
    p = P0V2
    assembly = make_p0_v2_assembly(p.pressed_state)
    probes = [
        _box(22.8, 9.8, 4.2, (0.0, p.fixed_fill_center_y, 18.0)),
        _box(21.8, 4.6, 4.2, (0.0, p.fixed_outlet_center_y, -18.0)),
    ]
    for probe in probes:
        assert sum(_intersection_volume(child, probe) for child in assembly.children) < 1e-6


def test_released_fixed_aperture_rays_hit_near_flush_shutters() -> None:
    p = P0V2
    center = p.shuttle_center_y(p.released_state)
    top = make_top_shutter(p).moved(Location((0.0, center, 0.0)))
    bottom = make_bottom_shutter(p).moved(Location((0.0, center, 0.0)))
    top_probe = _box(22.8, 9.8, 0.08, (0.0, p.fixed_fill_center_y, 19.85))
    bottom_probe = _box(21.8, 4.6, 0.08, (0.0, p.fixed_outlet_center_y, -19.85))
    assert _intersection_volume(top, top_probe) == pytest.approx(
        top_probe.volume, rel=1e-6
    )
    assert _intersection_volume(bottom, bottom_probe) == pytest.approx(
        bottom_probe.volume, rel=1e-6
    )


def test_released_translated_openings_are_under_opaque_housing() -> None:
    p = P0V2
    housing = make_housing(p)
    top_interval = p.moving_fill_interval(p.released_state)
    bottom_interval = p.moving_outlet_interval(p.released_state)
    top_probe = _box(
        p.moving_fill_width - 0.2,
        p.moving_fill_length - 0.2,
        0.04,
        (0.0, sum(top_interval) / 2, 19.975),
    )
    bottom_probe = _box(
        p.moving_outlet_width - 0.2,
        p.moving_outlet_length - 0.2,
        0.04,
        (0.0, sum(bottom_interval) / 2, -19.975),
    )
    assert _intersection_volume(housing, top_probe) == pytest.approx(
        top_probe.volume, rel=1e-6
    )
    assert _intersection_volume(housing, bottom_probe) == pytest.approx(
        bottom_probe.volume, rel=1e-6
    )


def test_rear_rays_hit_blind_cover_and_cover_has_no_tool_hole() -> None:
    p = P0V2
    cover = make_blind_rear_cover(p).moved(
        Location((0.0, p.rear_cover_back_y + p.rear_cover_thickness / 2, 0.0))
    )
    for x, z in ((0.0, 0.0), (-15.0, -14.0), (-15.0, 14.0), (15.0, -14.0), (15.0, 14.0)):
        probe = _box(0.2, 0.1, 0.2, (x, -19.9, z))
        assert _intersection_volume(cover, probe) == pytest.approx(
            probe.volume, rel=1e-6
        )


def test_nominal_and_loose_clearance_coupons_are_distinct_valid_artifacts() -> None:
    p = P0V2
    nominal = make_rail_coupon(p.groove_width_nominal)
    loose = make_rail_coupon(p.groove_width_loose)
    assert nominal.is_valid and loose.is_valid
    assert len(nominal.children) == 2
    assert len(loose.children) == 2
    assert nominal.label.endswith("2.7mm")
    assert loose.label.endswith("2.8mm")
    nominal_receiver = next(child for child in nominal.children if "receiver" in child.label)
    loose_receiver = next(child for child in loose.children if "receiver" in child.label)
    assert loose_receiver.volume < nominal_receiver.volume
