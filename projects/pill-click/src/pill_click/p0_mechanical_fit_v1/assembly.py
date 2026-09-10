"""Static source placements for the manual mechanical-fit slider."""

from build123d import Compound, Location, Shape

from .geometry import make_outer_housing, make_snap_rear_cover, make_solid_inner_button
from .spec import P0_MECHANICAL_FIT_V1, P0MechanicalFitV1Spec


def _placed(shape: Shape, y: float, label: str) -> Shape:
    placed = Location((0.0, y, 0.0)) * shape
    placed.label = label
    return placed


def make_assembly(
    state: float,
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Compound:
    if not p.inward_state <= state <= p.maximum_pull_state:
        raise ValueError(
            f"state {state:.3f} is outside captive travel "
            f"[{p.inward_state:.2f}, {p.maximum_pull_state:.2f}]"
        )
    inner = _placed(
        make_solid_inner_button(p),
        p.inner_center_y(state),
        f"solid_inner_button_state_{state:+.2f}",
    )
    return Compound(
        children=[make_outer_housing(p), inner, make_snap_rear_cover(p)],
        label=f"p0_mechanical_fit_v1_three_part_assembly_state_{state:+.2f}",
    )


def make_pressed_assembly(
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Compound:
    return make_assembly(p.pressed_state, p)


def make_released_assembly(
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Compound:
    return make_assembly(p.released_state, p)


__all__ = ["make_assembly", "make_pressed_assembly", "make_released_assembly"]
