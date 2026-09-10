"""Printable push-push latch geometry for the Pill Click shuttle.

The moving shuttle carries a shallow asymmetric heart-cam track.  With the
shuttle moving toward ``-Y``, a fixed follower moves toward ``+Y`` relative to
the track: the first press takes the short entry lobe, release seats the pin in
the heart notch, and the next press sends it over the longer return lobe.  A
thin cantilever lets the pin move in X as those branches diverge.

This is deliberately an independently authored, first-print mechanism rather
than a claim of production-ready kinematics.  FDM corner rounding, layer-line
friction, follower preload, and the actual return force can all change branch
selection.  Print the latch coupon and physically cycle it before integrating
it into the medicine shuttle; tune the groove width or beam thickness rather
than scaling the whole model.
"""

from __future__ import annotations

from math import atan2, degrees, hypot

from build123d import Align, Axis, Box, Cylinder, Vector

from .parameters import DEFAULTS, PillClickParameters


def _cam_points(params: PillClickParameters) -> tuple[tuple[float, float], ...]:
    """Return a state-referenced heart loop from ready through overtravel."""

    half_branch = params.cam_branch_spacing / 2
    ready = -params.ready_state
    crest = -params.inward_stop_state
    return (
        (0.0, ready),
        (-0.57 * half_branch, ready + 0.27 * params.total_press_span),
        (-half_branch, ready + 0.65 * params.total_press_span),
        (-0.34 * half_branch, crest),
        (0.0, -params.latched_state),
        (0.34 * half_branch, crest),
        (half_branch, ready + 0.65 * params.total_press_span),
        (0.76 * half_branch, ready + 0.25 * params.total_press_span),
        (0.0, ready),
    )


def _groove_segment(
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    width: float,
    z_min: float,
    height: float,
):
    """Create a closed rectangular sweep segment for a recessed track."""

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = hypot(dx, dy)
    angle = degrees(atan2(dy, dx))
    midpoint = Vector(
        0.5 * (start[0] + end[0]),
        0.5 * (start[1] + end[1]),
        z_min,
    )
    segment = Box(
        length,
        width,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    return segment.rotate(Axis.Z, angle).translate(midpoint)


def make_cam_carrier(params: PillClickParameters = DEFAULTS):
    """Return the shuttle-mounted carrier with a recessed heart-cam groove.

    The carrier is centered in X/Y with its mounting face at Z=0.  The groove
    opens on +Z, is blind, and leaves at least one millimetre of floor beneath
    the follower.  The result is one closed positive-volume solid.
    """

    points = _cam_points(params)
    path_min_y = min(y for _, y in points)
    path_max_y = max(y for _, y in points)
    edge_margin = params.cam_groove_width
    carrier_width = (
        params.cam_branch_spacing
        + params.cam_groove_width
        + 2 * edge_margin
    )
    carrier_depth = path_max_y - path_min_y + params.cam_groove_width + 2.0
    carrier_center_y = 0.5 * (path_min_y + path_max_y)
    plate_thickness = params.cam_plate_thickness
    groove_depth = min(params.cam_groove_depth, plate_thickness - 1.0)
    if groove_depth <= 0:
        raise ValueError("cam_plate_thickness must leave a positive groove floor")
    if params.cam_groove_width <= params.follower_pin_diameter:
        raise ValueError("cam groove must be wider than the follower pin")

    carrier = Box(
        carrier_width,
        carrier_depth,
        plate_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).translate(Vector(0, carrier_center_y, 0))

    # Overshoot the top face slightly so every cutter opens the groove cleanly.
    cutter_overshoot = 0.2
    cutter_z = plate_thickness - groove_depth
    cutter_height = groove_depth + cutter_overshoot
    for start, end in zip(points, points[1:]):
        carrier = carrier - _groove_segment(
            start,
            end,
            width=params.cam_groove_width,
            z_min=cutter_z,
            height=cutter_height,
        )

    # Circular junctions remove sharp internal corners that would trap a round
    # pin after normal FDM corner swelling.
    junction_radius = 0.5 * params.cam_groove_width
    for x, y in points[:-1]:
        junction = Cylinder(
            junction_radius,
            cutter_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).translate(Vector(x, y, cutter_z))
        carrier = carrier - junction

    carrier.label = "push_push_cam_carrier"
    return carrier


def make_compliant_follower(params: PillClickParameters = DEFAULTS):
    """Return a fixed cantilever follower with an integral vertical pin.

    The anchor sits at negative Y, the beam extends toward +Y, and its thin X
    section provides the lateral compliance needed to follow both cam lobes.
    The pin enters the carrier from +Z.  The part is a single connected solid.
    """

    beam_thickness = params.follower_beam_thickness
    follower_height = params.follower_beam_width
    pin_radius = 0.5 * params.follower_pin_diameter
    beam_length = params.total_press_span + 2.0 * params.cam_groove_width
    anchor_depth = max(2.5, 1.6 * beam_thickness)
    anchor_width = max(2.6 * params.follower_beam_width, 4.0 * beam_thickness)
    tip_pad_diameter = max(1.8 * params.follower_pin_diameter, 2.2 * beam_thickness)
    pin_engagement = params.cam_groove_depth + 0.35

    if beam_thickness <= 0 or follower_height <= 0:
        raise ValueError("follower beam dimensions must be positive")

    anchor_center_y = -0.5 * (beam_length + anchor_depth)
    anchor = Box(
        anchor_width,
        anchor_depth,
        follower_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).translate(Vector(0, anchor_center_y, 0))

    beam = Box(
        beam_thickness,
        beam_length,
        follower_height,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    ).translate(Vector(0, -beam_length, 0))

    tip_pad = Cylinder(
        0.5 * tip_pad_diameter,
        follower_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    pin = Cylinder(
        pin_radius,
        pin_engagement,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).translate(Vector(0, 0, follower_height))

    follower = anchor + beam + tip_pad + pin
    follower.label = "compliant_cam_follower"
    return follower


__all__ = ["make_cam_carrier", "make_compliant_follower"]
