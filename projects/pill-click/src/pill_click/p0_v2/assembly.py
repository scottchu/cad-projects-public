"""Static-pose assemblies for P0 v2."""

from build123d import Compound, Location, Shape

from .geometry import (
    make_blind_rear_cover,
    make_bottom_shutter,
    make_housing,
    make_shuttle,
    make_top_shutter,
)
from .spec import P0V2, P0V2Spec


def _place(shape: Shape, location: Location, label: str) -> Shape:
    placed = location * shape
    placed.label = label
    return placed


def placed_moving_parts(state: float, p: P0V2Spec = P0V2) -> list[Shape]:
    y = p.shuttle_center_y(state)
    location = Location((0.0, y, 0.0))
    return [
        _place(make_shuttle(p), location, f"p0_v2_shuttle:s_{state:.2f}"),
        _place(make_top_shutter(p), location, f"p0_v2_top_shutter:s_{state:.2f}"),
        _place(
            make_bottom_shutter(p),
            location,
            f"p0_v2_bottom_shutter:s_{state:.2f}",
        ),
    ]


def make_p0_v2_assembly(
    state: float = P0V2.released_state,
    p: P0V2Spec = P0V2,
) -> Compound:
    cover_center_y = p.rear_cover_back_y + p.rear_cover_thickness / 2
    cover = _place(
        make_blind_rear_cover(p),
        Location((0.0, cover_center_y, 0.0)),
        "p0_v2_blind_rear_cover",
    )
    children = [make_housing(p), cover, *placed_moving_parts(state, p)]
    return Compound(
        children=children,
        label=f"pill_click_p0_v2_captured_shutters_s_{state:.2f}",
    )


__all__ = ["make_p0_v2_assembly", "placed_moving_parts"]
