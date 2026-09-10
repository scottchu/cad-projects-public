"""Rear-installed captive medicine shuttle and frozen v0 state geometry."""

from build123d import Align, Axis, Box, Location, Part, chamfer

from .geometry import rounded_box
from .parameters import DEFAULTS, PillClickParameters


def _box(
    size_x: float,
    size_y: float,
    size_z: float,
    center: tuple[float, float, float],
) -> Part:
    return Box(
        size_x,
        size_y,
        size_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location(center))


def make_shuttle(params: PillClickParameters = DEFAULTS) -> Part:
    """Return the blank-key shuttle with sealed roof, floor gate, and stops."""

    p = params
    body = rounded_box(
        p.shuttle_width,
        p.shuttle_depth,
        p.shuttle_height,
        2.8,
    )

    # Closed cavity leaves a continuous 2 mm roof, floor, rear wall, and sides.
    cavity = _box(
        p.shuttle_width - 2 * p.shuttle_wall,
        p.shuttle_depth - 2 * p.shuttle_wall,
        p.shuttle_height - 2 * p.shuttle_wall,
        (0.0, 0.0, 0.0),
    )
    shuttle = body - cavity

    fill_local_y = p.loading_port_center_y - p.latched_shuttle_center_y
    fill = _box(
        p.loading_port_width,
        p.loading_port_depth,
        p.shuttle_wall + 1.0,
        (0.0, fill_local_y, p.shuttle_height / 2),
    )
    outlet = _box(
        p.outlet_width,
        p.outlet_depth,
        p.shuttle_wall + 1.0,
        (0.0, p.outlet_local_y, -p.shuttle_height / 2),
    )

    # The fixed gate blade moves from local Y=+1.0 to -13.4 over the full
    # physical stroke.  The oversize floor slot is backed by the solid housing
    # floor, so it is not an exterior spill opening.
    gate_path_min = -p.ready_state - p.gate_blade_depth / 2
    gate_path_max = -p.inward_stop_state + p.gate_blade_depth / 2
    gate_slot = _box(
        p.gate_blade_width + 0.4,
        gate_path_max - gate_path_min,
        p.shuttle_wall + 1.0,
        (0.0, 0.5 * (gate_path_min + gate_path_max), -p.shuttle_height / 2),
    )
    shuttle = shuttle - fill - outlet - gate_slot

    # Raised moving dam.  Together with the fixed blade it defines the
    # deliberately conservative 4.8..5.8 mm both-closed transfer deadband.
    dam_center_y = -(
        p.gate_open_state
        - 0.5 * (p.gate_blade_depth + p.gate_dam_depth)
    )
    floor_top = -p.shuttle_height / 2 + p.shuttle_wall
    dam_height = p.gate_blade_height - p.gate_vertical_overlap
    dam = _box(
        p.gate_dam_width,
        p.gate_dam_depth,
        dam_height,
        (0.0, dam_center_y, floor_top + dam_height / 2),
    )
    dam = chamfer(dam.edges().filter_by(Axis.X), p.gate_chamfer)
    shuttle = shuttle + dam

    # Two side tabs are rear-installed through the 37.3 mm channel.  Their
    # local front edge is derived so the ready pose lands at Y=15.4, leaving
    # 0.4 mm to the independent shoulder stop at Y=15.8.
    tab_center_y = p.tab_local_front_y - p.captive_tab_depth / 2
    tab_extension = 0.5 * (p.rear_tab_channel - p.shuttle_width)
    tab_center_x = p.shuttle_width / 2 + tab_extension / 2
    for sign in (-1.0, 1.0):
        tab = _box(
            tab_extension,
            p.captive_tab_depth,
            p.captive_tab_height,
            (sign * tab_center_x, tab_center_y, 0.0),
        )
        shuttle = shuttle + tab

    # Blank keycap; Orca Slicer owns all later lettering.  Its rear face meets
    # the housing counterbore plane at s=-1.0, independently of the cam.
    key_face = rounded_box(
        p.key_face_size,
        p.key_face_thickness,
        p.key_face_size,
        p.key_face_radius,
        center=(0.0, p.shuttle_depth / 2 + p.key_face_thickness / 2, 0.0),
    )
    shuttle = shuttle + key_face
    shuttle.label = "medicine_shuttle_blank_key"
    return shuttle


def shuttle_location(
    state: float,
    params: PillClickParameters = DEFAULTS,
) -> Location:
    """Return the assembly location for any frozen-v0 S state."""

    if not params.inward_stop_state <= state <= params.ready_state:
        raise ValueError("state exceeds independent hard stops")
    return Location((0.0, params.latched_shuttle_center_y + state, 0.0))


def latched_shuttle_location(params: PillClickParameters = DEFAULTS) -> Location:
    return shuttle_location(params.latched_state, params)


def ready_shuttle_location(params: PillClickParameters = DEFAULTS) -> Location:
    return shuttle_location(params.ready_state, params)


def outlet_overlap(state: float, params: PillClickParameters = DEFAULTS) -> float:
    """Return Y overlap between equal fixed and moving 4.8 mm outlets."""

    return max(0.0, params.outlet_depth - abs(state))


def gate_is_closed(state: float, params: PillClickParameters = DEFAULTS) -> bool:
    """Return the frozen transfer-gate state used for sequence validation."""

    return state <= params.gate_open_state


def fill_port_overlap(state: float, params: PillClickParameters = DEFAULTS) -> float:
    """Return overlap of the fixed and shuttle top-fill openings."""

    return max(0.0, params.loading_port_depth - abs(state))


__all__ = [
    "fill_port_overlap",
    "gate_is_closed",
    "latched_shuttle_location",
    "make_shuttle",
    "outlet_overlap",
    "ready_shuttle_location",
    "shuttle_location",
]
