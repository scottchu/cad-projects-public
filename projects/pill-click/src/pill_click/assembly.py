"""Labeled static assemblies for the two frozen v0 return variants."""

from build123d import Axis, Compound, Location, Shape

from .housing import make_back_cover, make_back_trap_plate, make_housing
from .latch import make_cam_carrier, make_compliant_follower
from .parameters import DEFAULTS, PillClickParameters
from .returns import (
    magnet_carrier_depth,
    make_fixed_magnet_carrier,
    make_moving_magnet_carrier,
    make_return_magnet_cap,
    make_spring_pair,
)
from .shuttle import make_shuttle, shuttle_location


def _place(shape: Shape, location: Location, label: str) -> Shape:
    placed = location * shape
    placed.label = label
    return placed


def _shared_children(
    state: float,
    params: PillClickParameters,
) -> list[Shape]:
    p = params
    cover_y = -p.housing_depth / 2 + p.back_cover_thickness / 2
    trap_y = -p.housing_depth / 2 - p.trap_plate_thickness / 2
    shuttle_pose = shuttle_location(state, p)

    housing = make_housing(p)
    cover = _place(make_back_cover(p), Location((0, cover_y, 0)), "rear_cover")
    trap = _place(
        make_back_trap_plate(p),
        Location((0, trap_y, 0)),
        "rear_magnet_trap_plate",
    )
    shuttle = _place(make_shuttle(p), shuttle_pose, "medicine_shuttle")

    # Shared external cam: replace the lower portion of the shuttle's left
    # side wall.  The groove opens toward -X, outside the medicine cavity.
    cam = make_cam_carrier(p).rotate(Axis.Y, -90)
    cam = _place(
        cam,
        shuttle_pose * Location((-p.shuttle_width / 2 + p.cam_plate_thickness, 0, 0)),
        "external_heart_cam",
    )

    # The fixed follower points +X from the outer housing side into the groove.
    follower = make_compliant_follower(p).rotate(Axis.Y, 90)
    follower_pin_reach = p.follower_beam_width + p.cam_groove_depth + 0.35
    follower_x = -p.shuttle_width / 2 - follower_pin_reach
    follower = _place(
        follower,
        Location((follower_x, p.latched_shuttle_center_y, 0)),
        "fixed_compliant_follower",
    )
    return [housing, cover, trap, shuttle, cam, follower]


def make_spring_assembly(
    params: PillClickParameters = DEFAULTS,
    *,
    state: float | None = None,
) -> Compound:
    """Return the spring-only ready assembly with exactly two printed springs."""

    p = params
    if state is None:
        state = p.ready_state
    children = _shared_children(state, p)
    shuttle_rear_y = p.latched_shuttle_center_y + state - p.shuttle_depth / 2
    springs = make_spring_pair(p)
    spring_center_y = shuttle_rear_y - p.spring_depth / 2
    spring_center_z = -0.28 * p.shuttle_height
    for child in springs.children:
        children.append(
            _place(
                child,
                Location((0, spring_center_y, spring_center_z)),
                child.label,
            )
        )
    return Compound(children=children, label="pill_click_spring_v0")


def make_magnet_assembly(
    params: PillClickParameters = DEFAULTS,
    *,
    state: float | None = None,
    minimum_gap: float | None = None,
) -> Compound:
    """Return the magnet-only assembly with one centered repelling pair."""

    p = params
    if state is None:
        state = p.ready_state
    if minimum_gap is None:
        minimum_gap = p.magnet_min_gap
    if minimum_gap not in (0.8, 1.2, 1.6):
        raise ValueError("minimum_gap must be 0.8, 1.2, or 1.6 mm")
    children = _shared_children(state, p)

    carrier_depth = magnet_carrier_depth(p)
    moving_center_y = (
        p.latched_shuttle_center_y
        + state
        - p.shuttle_depth / 2
        - carrier_depth / 2
    )
    moving_at_inward = (
        p.latched_shuttle_center_y
        + p.inward_stop_state
        - p.shuttle_depth / 2
        - carrier_depth / 2
    )
    fixed_center_y = moving_at_inward - carrier_depth - minimum_gap
    magnet_z = -0.28 * p.shuttle_height

    fixed = _place(
        make_fixed_magnet_carrier(p),
        Location((0, fixed_center_y, magnet_z)),
        "return_magnet_carrier:fixed",
    )
    moving = _place(
        make_moving_magnet_carrier(p),
        Location((0, moving_center_y, magnet_z)),
        "return_magnet_carrier:moving",
    )
    cap_offset = carrier_depth / 2 + p.trap_plate_thickness / 2
    fixed_cap = _place(
        make_return_magnet_cap(p, role="fixed"),
        Location((0, fixed_center_y - cap_offset, magnet_z)),
        "return_magnet_cap:fixed",
    )
    moving_cap = _place(
        make_return_magnet_cap(p, role="moving"),
        Location((0, moving_center_y - cap_offset, magnet_z)),
        "return_magnet_cap:moving",
    )
    children.extend([fixed, fixed_cap, moving, moving_cap])
    return Compound(
        children=children,
        label=f"pill_click_magnet_v0_gap_{minimum_gap:.1f}mm",
    )


__all__ = ["make_magnet_assembly", "make_spring_assembly"]
