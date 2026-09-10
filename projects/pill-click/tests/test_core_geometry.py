"""Frozen v0 housing, shuttle, stop, and transfer-sequence checks."""

import pytest

from pill_click.housing import make_back_cover, make_back_trap_plate, make_housing
from pill_click.parameters import DEFAULTS
from pill_click.shuttle import (
    fill_port_overlap,
    gate_is_closed,
    make_shuttle,
    outlet_overlap,
    shuttle_location,
)


def test_housing_is_valid_and_exactly_40_mm() -> None:
    housing = make_housing()
    size = housing.bounding_box().size

    assert housing.is_valid and housing.volume > 0
    assert size.X == pytest.approx(DEFAULTS.housing_size)
    assert size.Y == pytest.approx(DEFAULTS.housing_depth)
    assert size.Z == pytest.approx(DEFAULTS.housing_size)


def test_shuttle_and_rear_capture_parts_are_valid() -> None:
    parts = [make_shuttle(), make_back_cover(), make_back_trap_plate()]
    assert all(part.is_valid and part.volume > 0 for part in parts)
    assert all(len(part.solids()) == 1 for part in parts)


def test_fridge_magnet_pockets_and_barrier_are_frozen() -> None:
    p = DEFAULTS
    assert p.magnet_pocket_diameter == pytest.approx(6.1)
    assert p.magnet_pocket_depth == pytest.approx(2.1)
    assert p.back_cover_thickness - p.magnet_pocket_depth == pytest.approx(0.3)
    assert p.fridge_magnet_offset_x == pytest.approx(11.5)


def test_frozen_states_and_independent_hard_stops() -> None:
    p = DEFAULTS
    assert p.ready_state - p.inward_stop_state == pytest.approx(14.4)

    ready_center = shuttle_location(p.ready_state).position.Y
    tab_front = ready_center + p.tab_local_front_y
    assert tab_front == pytest.approx(p.ready_tab_front_y)
    assert p.shoulder_y - tab_front == pytest.approx(0.4)

    inward_center = shuttle_location(p.inward_stop_state).position.Y
    key_rear_face = inward_center + p.shuttle_depth / 2
    assert key_rear_face == pytest.approx(p.inward_stop_plane_y)

    with pytest.raises(ValueError):
        shuttle_location(p.ready_state + 0.01)
    with pytest.raises(ValueError):
        shuttle_location(p.inward_stop_state - 0.01)


def test_outlet_gate_deadband_and_latched_fill_sequence() -> None:
    p = DEFAULTS
    assert outlet_overlap(p.latched_state) == pytest.approx(p.outlet_depth)
    assert outlet_overlap(p.outlet_closed_state) == pytest.approx(0.0)
    assert gate_is_closed(p.outlet_closed_state)
    assert gate_is_closed(p.gate_open_state)
    assert not gate_is_closed(p.gate_open_state + 0.01)
    assert fill_port_overlap(p.latched_state) == pytest.approx(p.loading_port_depth)
    assert fill_port_overlap(p.ready_state) == pytest.approx(0.0)

    ready_rear = (
        p.latched_shuttle_center_y + p.ready_state - p.shuttle_depth / 2
    )
    housing_port_rear = p.loading_port_center_y - p.loading_port_depth / 2
    assert housing_port_rear - ready_rear >= 1.0
