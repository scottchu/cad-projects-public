"""Contract tests for the V2.1 keyboard-identity silhouette derivative."""

import pytest
from build123d import Vector

from pill_click.p0_mechanical_fit_v2_keyboard_inverted_rails import (
    P0_MECHANICAL_FIT_V2,
)
from pill_click.p0_mechanical_fit_v21_keyboard_identity import (
    P0_MECHANICAL_FIT_V21,
    make_keyboard_identity_button,
    make_pressed_keyboard_identity_assembly,
    make_released_keyboard_identity_assembly,
    placed_keyboard_identity_button,
)
from pill_click.p0_mechanical_fit_v21_keyboard_identity.geometry import (
    make_blind_two_side_latch_rear_cover,
    make_outer_housing,
)


p = P0_MECHANICAL_FIT_V21


def _bbox(shape):
    box = shape.bounding_box()
    return (box.min.X, box.max.X, box.min.Y, box.max.Y, box.min.Z, box.max.Z)


def _intersection_volume(first, second) -> float:
    intersection = first & second
    return 0.0 if intersection is None else intersection.volume


def test_keyboard_identity_dimensions_and_travel_are_explicit() -> None:
    assert p.keycap_height == pytest.approx(8.0)
    assert p.key_skirt_size_xz == pytest.approx(34.2)
    assert p.key_face_size_xz == pytest.approx(29.0)
    assert p.key_face_dish_depth_y == pytest.approx(0.55)
    assert p.released_state - p.pressed_state == pytest.approx(13.4)
    assert p.pressed_key_proud_y == pytest.approx(5.0)
    assert p.released_key_proud_y == pytest.approx(18.4)


def test_physically_accepted_v2_rails_stops_and_travel_are_frozen() -> None:
    v2 = P0_MECHANICAL_FIT_V2
    assert p.male_rail_centres_z == v2.male_rail_centres_z
    assert p.male_rail_width_z == v2.male_rail_width_z
    assert p.male_rail_external_height_x == v2.male_rail_external_height_x
    assert p.male_rail_local_y == v2.male_rail_local_y
    assert p.female_channel_blind_front_y == v2.female_channel_blind_front_y
    assert p.blind_stop_wall_axial_thickness == v2.blind_stop_wall_axial_thickness
    assert p.released_state == v2.released_state
    assert p.maximum_pull_state == v2.maximum_pull_state


def test_rear_side_clamp_is_deliberately_tighter_than_v2() -> None:
    v2 = P0_MECHANICAL_FIT_V2
    assert p.side_latch_beam_thickness_x == pytest.approx(1.10)
    assert p.side_latch_beam_thickness_x > v2.side_latch_beam_thickness_x
    assert p.side_latch_hook_apex_x - p.side_latch_pocket_x[0] == pytest.approx(0.60)
    assert (
        p.side_latch_hook_apex_x - p.side_latch_pocket_x[0]
        > v2.side_latch_hook_apex_x - v2.side_latch_pocket_x[0]
    )
    assert p.predicted_hook_release_travel == pytest.approx(0.66)
    assert p.predicted_hook_release_travel >= p.side_latch_required_hook_release_x
    assert p.predicted_hook_stop_travel == pytest.approx(0.75625)
    assert p.side_latch_outer_skin_x == pytest.approx(1.20)


def test_tall_dished_inner_is_one_valid_solid_with_v2_rails() -> None:
    inner = make_keyboard_identity_button()
    assert inner.is_valid and len(inner.solids()) == 1 and inner.volume > 0
    # The rail tips define X; the 34.2 mm body defines Z.
    assert _bbox(inner) == pytest.approx(
        (-18.3, 18.3, -17.2, 20.5, -17.1, 17.1), abs=0.005
    )
    # The centre is recessed, while the face rim remains printable solid geometry.
    assert not inner.is_inside(Vector(0.0, 20.49, 0.0), tolerance=1e-7)
    assert inner.is_inside(Vector(0.0, 19.94, 0.0), tolerance=1e-7)
    assert inner.is_inside(Vector(13.5, 20.40, 0.0), tolerance=1e-7)


def test_pressed_and_released_assemblies_preserve_three_parts_and_exact_stroke() -> None:
    pressed = make_pressed_keyboard_identity_assembly()
    released = make_released_keyboard_identity_assembly()
    assert len(pressed.children) == len(pressed.solids()) == 3
    assert len(released.children) == len(released.solids()) == 3
    assert _bbox(pressed) == pytest.approx((-20, 20, -20, 25.0, -20, 20))
    assert _bbox(released) == pytest.approx((-20, 20, -20, 38.4, -20, 20))
    assert released.bounding_box().max.Y - pressed.bounding_box().max.Y == pytest.approx(13.4)


@pytest.mark.parametrize(
    "state",
    (p.inward_state, p.pressed_state, 6.0, p.released_state, p.maximum_pull_state),
)
def test_keyboard_identity_inner_is_collision_free_at_key_travel_states(state: float) -> None:
    moving = placed_keyboard_identity_button(state)
    assert _intersection_volume(make_outer_housing(), moving) < 1e-6
    assert _intersection_volume(make_blind_two_side_latch_rear_cover(), moving) < 1e-6
