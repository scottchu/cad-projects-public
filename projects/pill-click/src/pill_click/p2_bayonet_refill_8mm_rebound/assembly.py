"""P2 four-part assembly placements."""

from build123d import Axis, Compound, Location

from .geometry import make_bayonet_cap, make_hollow_keyboard_container, make_magnetic_rear_cover, make_ported_outer_housing
from .spec import P2_BAYONET_REFILL_8MM_REBOUND


def placed_hollow_keyboard_container(state, p=P2_BAYONET_REFILL_8MM_REBOUND):
    shape = Location((0, p.inner_center_y(state), 0)) * make_hollow_keyboard_container(p)
    shape.label = f"p2_inner_state_{state:+.2f}"
    return shape


def placed_bayonet_cap(state, locked=True, exploded=0.0, p=P2_BAYONET_REFILL_8MM_REBOUND):
    cap = make_bayonet_cap(p)
    if locked:
        # Slot cutter sweeps +90 degrees in cap-local space.  The locked cap
        # therefore rotates -90 degrees around the fixed neck lugs.
        cap = cap.rotate(Axis.Y, -p.cap_rotation_degrees)
    y = p.inner_center_y(state) + p.key_local_y[1] + exploded
    cap = Location((0, y, 0)) * cap
    cap.label = "p2_cap_locked" if locked else "p2_cap_unlocked"
    return cap


def make_assembly(state, cap_locked=True, cap_exploded=0.0, p=P2_BAYONET_REFILL_8MM_REBOUND):
    if not p.inward_state <= state <= p.maximum_pull_state:
        raise ValueError("state is outside captive travel")
    return Compound(children=[
        make_ported_outer_housing(p),
        placed_hollow_keyboard_container(state, p),
        make_magnetic_rear_cover(p),
        placed_bayonet_cap(state, cap_locked, cap_exploded, p),
    ], label=f"p2_four_part_state_{state:+.2f}")


def make_pressed_assembly(p=P2_BAYONET_REFILL_8MM_REBOUND):
    return make_assembly(p.pressed_state, True, 0.0, p)


def make_released_assembly(p=P2_BAYONET_REFILL_8MM_REBOUND):
    return make_assembly(p.released_state, True, 0.0, p)


def make_cap_locked_assembly(p=P2_BAYONET_REFILL_8MM_REBOUND):
    return make_assembly(p.released_state, True, 0.0, p)


def make_cap_exploded_assembly(p=P2_BAYONET_REFILL_8MM_REBOUND):
    return make_assembly(p.released_state, False, 12.0, p)


__all__ = [name for name in globals() if name.startswith("make_") or name.startswith("placed_")]
