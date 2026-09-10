"""Static P0 v3 operational poses and rear-feed stack placements."""

from build123d import Compound, Location, Shape

from .geometry import (
    make_blind_rear_cover,
    make_bottom_shutter,
    make_housing,
    make_shuttle,
    make_top_shutter,
)
from .spec import P0V3, P0V3Spec


def _placed(shape: Shape, y: float, label: str) -> Shape:
    result = Location((0.0, y, 0.0)) * shape
    result.label = label
    return result


def placed_moving_parts(state: float, p: P0V3Spec = P0V3) -> list[Shape]:
    q = p.shutter_q(state)
    return [
        _placed(
            make_shuttle(p),
            p.shuttle_center_y(state),
            f"p0_v3_shuttle:s_{state:.2f}",
        ),
        _placed(
            make_top_shutter(p),
            p.latched_center_y + q,
            f"p0_v3_top_shutter:q_{q:.2f}",
        ),
        _placed(
            make_bottom_shutter(p),
            p.latched_center_y + q,
            f"p0_v3_bottom_shutter:q_{q:.2f}",
        ),
    ]


def make_rear_feed_stack(center_y: float, p: P0V3Spec = P0V3) -> Compound:
    if not p.feed_start_center_y <= center_y <= p.feed_end_center_y:
        raise ValueError("rear-feed center outside frozen sweep")
    children = [
        _placed(make_shuttle(p), center_y, f"p0_v3_feed_shuttle:c_{center_y:.2f}"),
        _placed(make_top_shutter(p), center_y, f"p0_v3_feed_top_shutter:c_{center_y:.2f}"),
        _placed(make_bottom_shutter(p), center_y, f"p0_v3_feed_bottom_shutter:c_{center_y:.2f}"),
    ]
    return Compound(children=children, label=f"p0_v3_rear_feed_stack:c_{center_y:.2f}")


def make_p0_v3_assembly(
    state: float = P0V3.released_state,
    p: P0V3Spec = P0V3,
) -> Compound:
    children = [make_housing(p), make_blind_rear_cover(p), *placed_moving_parts(state, p)]
    return Compound(
        children=children,
        label=f"pill_click_p0_v3_solid_shutters_s_{state:.2f}",
    )


__all__ = ["make_p0_v3_assembly", "make_rear_feed_stack", "placed_moving_parts"]
