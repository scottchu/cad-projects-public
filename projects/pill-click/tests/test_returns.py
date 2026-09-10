from __future__ import annotations

from dataclasses import replace

import pytest

from pill_click.parameters import DEFAULTS
from pill_click.returns import (
    MAGNET_GAP_VARIANTS,
    magnet_carrier_depth,
    magnet_return_placement,
    make_fixed_magnet_carrier,
    make_magnet_pocket_tool,
    make_magnet_gap_shim,
    make_magnet_return_pair,
    make_moving_magnet_carrier,
    make_serpentine_spring,
    make_spring_pair,
)


def _assert_one_positive_solid(shape: object) -> None:
    solids = list(shape.solids())
    assert len(solids) == 1
    assert solids[0].volume > 0
    assert solids[0].is_valid


@pytest.mark.parametrize("side", ["left", "right"])
def test_serpentine_springs_are_flat_valid_labeled_solids(side: str) -> None:
    spring = make_serpentine_spring(DEFAULTS, side)  # type: ignore[arg-type]
    _assert_one_positive_solid(spring)
    bounds = spring.bounding_box()
    assert bounds.min.Z == pytest.approx(0.0)
    assert bounds.max.Z == pytest.approx(DEFAULTS.spring_thickness)
    assert bounds.size.Y == pytest.approx(DEFAULTS.spring_depth)
    assert spring.label == f"spring_return:{side}"


def test_spring_pair_remains_two_separate_mirrored_parts() -> None:
    pair = make_spring_pair(DEFAULTS)
    solids = list(pair.solids())
    assert len(solids) == 2
    assert all(solid.volume > 0 and solid.is_valid for solid in solids)
    assert pair.label == "spring_return_pair"
    assert {child.label for child in pair.children} == {
        "spring_return:left",
        "spring_return:right",
    }


@pytest.mark.parametrize(
    "factory, label",
    [
        (make_fixed_magnet_carrier, "return_magnet_carrier:fixed"),
        (make_moving_magnet_carrier, "return_magnet_carrier:moving"),
    ],
)
def test_magnet_carriers_are_valid_and_keep_front_wall(factory, label: str) -> None:
    carrier = factory(DEFAULTS)
    _assert_one_positive_solid(carrier)
    assert carrier.label == label

    bounds = carrier.bounding_box()
    front_wall = bounds.max.Y - (
        bounds.min.Y + DEFAULTS.magnet_pocket_depth
    )
    assert front_wall >= 1.2


def test_magnet_pair_uses_travel_without_springs() -> None:
    placement = magnet_return_placement(DEFAULTS)
    assert placement.released_gap == pytest.approx(
        placement.pressed_gap + DEFAULTS.total_press_span
    )
    assert placement.carrier_depth == pytest.approx(magnet_carrier_depth(DEFAULTS))

    pair = make_magnet_return_pair(DEFAULTS)
    assert len(list(pair.solids())) == 2
    assert {child.label for child in pair.children} == {
        "return_magnet_carrier:fixed",
        "return_magnet_carrier:moving",
    }
    assert all("spring" not in child.label for child in pair.children)


def test_rear_loaded_pocket_tool_keeps_requested_diameter_and_depth() -> None:
    tool = make_magnet_pocket_tool(DEFAULTS)
    bounds = tool.bounding_box()
    assert bounds.size.X == pytest.approx(DEFAULTS.magnet_pocket_diameter)
    assert bounds.size.Z == pytest.approx(DEFAULTS.magnet_pocket_diameter)
    assert bounds.size.Y > DEFAULTS.magnet_pocket_depth  # rear-face overshoot
    assert bounds.size.Y == pytest.approx(DEFAULTS.magnet_pocket_depth + 0.4)


def test_measured_13_4_mm_travel_keeps_both_variants_geometrically_valid() -> None:
    measured = replace(DEFAULTS, ready_state=13.4)
    spring_pair = make_spring_pair(measured)
    magnet_pair = make_magnet_return_pair(measured)
    placement = magnet_return_placement(measured)

    assert len(list(spring_pair.solids())) == 2
    assert len(list(magnet_pair.solids())) == 2
    assert measured.spring_depth - measured.travel > 0
    assert placement.released_gap - placement.pressed_gap == pytest.approx(14.4)


@pytest.mark.parametrize("gap", MAGNET_GAP_VARIANTS)
def test_gap_shim_variants_are_positive_solids(gap: float) -> None:
    shim = make_magnet_gap_shim(gap)
    _assert_one_positive_solid(shim)
    assert shim.bounding_box().size.Y == pytest.approx(gap)
