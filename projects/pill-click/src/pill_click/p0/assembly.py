"""Labeled P0 static-pose assemblies."""

from build123d import Compound, Location, Shape

from .geometry import make_back_insert, make_housing, make_shuttle
from .spec import P0, P0Spec


def _place(shape: Shape, location: Location, label: str) -> Shape:
    placed = location * shape
    placed.label = label
    return placed


def placed_shuttle(state: float, p: P0Spec = P0) -> Shape:
    """Return the shuttle at a validated static state."""

    return _place(
        make_shuttle(p),
        Location((0.0, p.shuttle_center_y(state), 0.0)),
        f"p0_medicine_shuttle:s_{state:.2f}",
    )


def make_p0_assembly(
    state: float = P0.released_state,
    p: P0Spec = P0,
) -> Compound:
    """Return the manual-slider P0 assembly at ``state``."""

    housing = make_housing(p)
    insert = _place(
        make_back_insert(p),
        Location((0.0, p.rear_insert_center_y, 0.0)),
        "p0_rear_insert",
    )
    shuttle = placed_shuttle(state, p)
    return Compound(
        children=[housing, insert, shuttle],
        label=f"pill_click_p0_manual_slider_s_{state:.2f}",
    )


__all__ = ["make_p0_assembly", "placed_shuttle"]
