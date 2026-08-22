"""Labeled source assemblies for the XT60 bend jig."""

from __future__ import annotations

from build123d import Compound, Pos, Rot, Shape

from .geometry import (
    build_cold_iron_keepout_reference,
    build_esc_reference,
    build_fc_reference,
    build_fit_coupon,
    build_knob,
    build_left_frame_with_drive_support,
    build_left_slider,
    build_m4_drive_reference,
    build_reaction_carrier,
    build_reference_rods,
    build_right_frame,
    build_right_slider,
    build_wires_reference,
    build_xt60_bridge,
    build_xt60_reference,
)

from .mechanism import solve_mechanism
from .parameters import DEFAULT_PARAMETERS, PrototypeParameters


def _rod_positions(
    params: PrototypeParameters | None,
    closure: float,
    wire_gauge: int,
    upper_index: int,
    lower_index: int,
) -> dict[str, tuple[float, float]]:
    """Adapt the mathematical solver's PointYZ values to geometry coordinates."""

    solution = solve_mechanism(
        params=params or DEFAULT_PARAMETERS,
        wire_gauge=wire_gauge,
        closure=closure,
        upper_index=upper_index,
        lower_index=lower_index,
    )
    return {
        name: (float(point.y), float(point.z))
        for name, point in solution.rod_centers.items()
    }


def _build_assembly(
    params: PrototypeParameters | None,
    closure: float,
    label: str,
    wire_gauge: int,
    upper_index: int,
    lower_index: int,
) -> Compound:
    params = params or DEFAULT_PARAMETERS
    solution = solve_mechanism(
        params=params,
        wire_gauge=wire_gauge,
        closure=closure,
        upper_index=upper_index,
        lower_index=lower_index,
    )
    closed_solution = solve_mechanism(
        params=params,
        wire_gauge=wire_gauge,
        closure=1.0,
        upper_index=upper_index,
        lower_index=lower_index,
    )
    if not closed_solution.usable:
        raise ValueError(
            f"selected reaction setting is not usable: {closed_solution.status}; "
            f"requires {closed_solution.minimum_required_lead_length:.3f} mm lead"
        )
    positions = _rod_positions(params, closure, wire_gauge, upper_index, lower_index)
    closed_positions = _rod_positions(params, 1.0, wire_gauge, upper_index, lower_index)
    moving_y, moving_z = positions["moving"]
    slider_dy = moving_y - closed_positions["moving"][0]
    slider_dz = moving_z - closed_positions["moving"][1]

    left_slider = Pos(0, slider_dy, slider_dz) * build_left_slider(params, wire_gauge)
    left_slider.label = "left_keyed_moving_slider"
    right_slider = Pos(0, slider_dy, slider_dz) * build_right_slider(params, wire_gauge)
    right_slider.label = "right_keyed_moving_slider"

    rods = build_reference_rods(positions["upper"], positions["lower"], positions["moving"])
    # Reference stack is below/behind the working rods, leaving the connector
    # and wire ends visible in both static states.
    esc = Pos(0, -24.0, 8.5) * build_esc_reference()
    esc.label = "reference_bottom_36x36_esc"
    fc = Pos(0, -24.0, 25.0) * build_fc_reference()
    fc.label = "reference_upper_flight_controller"
    endpoint = closed_solution.wire_endpoint
    connector = Pos(0, endpoint.y, endpoint.z) * build_xt60_reference(params)
    connector.label = "reference_xt60_body_15p9x8p1x20p5_with_5mm_solder_cups"
    wires = build_wires_reference(params, wire_gauge, upper_index, lower_index, 1.0)
    wires.label = "reference_simplified_90_degree_wires"
    bridge = Pos(0, endpoint.y, endpoint.z + 3.0) * build_xt60_bridge(params)
    bridge.label = "removable_xt60_bridge_cradle"

    carriers = [
        build_reaction_carrier(side, kind, params, wire_gauge, upper_index if kind == "upper" else lower_index)
        for side in ("left", "right")
        for kind in ("upper", "lower")
    ]
    drive_screw = build_m4_drive_reference(params, wire_gauge)
    knob_solution = solve_mechanism(params=params, wire_gauge=wire_gauge, closure=0.0)
    knob_point = knob_solution.moving_rod_center
    knob_distance = 25.0
    knob_y = knob_point.y + 6.0 + knob_solution.moving_outward_unit.y * knob_distance
    knob_z = knob_point.z + 6.0 + knob_solution.moving_outward_unit.z * knob_distance
    knob = Pos(
        -(params.outer_span / 2.0 + 5.5 + params.running_clearance_per_side),
        knob_y,
        knob_z,
    ) * (
        Rot(45, 0, 0) * build_knob(params)
    )
    knob.label = "m4_drive_knob"

    children = [
            build_left_frame_with_drive_support(params, wire_gauge),
            build_right_frame(params, wire_gauge),
            left_slider,
            right_slider,
            *carriers,
            knob,
            bridge,
            rods,
            drive_screw,
        ]
    if closure == 1.0:
        iron_keepout = build_cold_iron_keepout_reference()
        children.extend([esc, fc, connector, wires, iron_keepout])
    return Compound(children=children, label=label)


def build_closed_assembly(
    params: PrototypeParameters | None = None,
    wire_gauge: int = 12,
    upper_index: int = 1,
    lower_index: int = 1,
) -> Compound:
    """Static labeled compound at the mathematically closed position."""

    return _build_assembly(params, 1.0, "xt60_bend_jig_closed", wire_gauge, upper_index, lower_index)


def build_open_assembly(
    params: PrototypeParameters | None = None,
    wire_gauge: int = 12,
    upper_index: int = 1,
    lower_index: int = 1,
) -> Compound:
    """Static labeled compound with the forming rod and sliders retracted."""

    return _build_assembly(params, 0.0, "xt60_bend_jig_open", wire_gauge, upper_index, lower_index)


def _place_for_print(shape: Shape, x: float, y: float, label: str | None = None) -> Shape:
    bounds = shape.bounding_box()
    placed = Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * shape
    if label is not None:
        placed.label = label
    return placed


def build_print_kit(params: PrototypeParameters | None = None, wire_gauge: int = 12) -> Compound:
    """Non-overlapping printable parts only; no rods, electronics, wire or XT60."""

    raw_parts = [
        (build_left_frame_with_drive_support(params, wire_gauge), "left_ribbed_side_frame_with_diagonal_drive_support"),
        (build_right_frame(params, wire_gauge), "right_ribbed_side_frame"),
        (build_left_slider(params, wire_gauge), "left_keyed_moving_slider"),
        (build_right_slider(params, wire_gauge), "right_keyed_moving_slider"),
        (build_xt60_bridge(params), "removable_xt60_bridge_cradle"),
        (build_knob(params), "m4_drive_knob"),
        (build_fit_coupon(params), "rod_bore_and_slot_fit_coupon_4p2_to_4p5"),
    ]
    raw_parts.extend(
        (build_reaction_carrier(side, kind, params, wire_gauge, 1), f"{side}_{kind}_reaction_carrier")
        for side, kind in (("left", "upper"), ("right", "upper"), ("left", "lower"), ("right", "lower"))
    )
    printable = []
    cursor_x = 0.0
    for shape, label in raw_parts:
        printable.append(_place_for_print(shape, cursor_x, 0.0, label))
        cursor_x += shape.bounding_box().size.X + 10.0
    return Compound(children=printable, label="xt60_bend_jig_print_only_kit")


__all__ = ["build_closed_assembly", "build_open_assembly", "build_print_kit"]
