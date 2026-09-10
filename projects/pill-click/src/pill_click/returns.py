"""Independent return-force parts for the Pill Click prototype.

Coordinate convention
---------------------
X is module width, Y is the rear-to-front actuation axis, and Z is up.  A
press moves the shuttle in negative Y.

The spring parts are returned in their flat printing orientation.  Their
local origin is the centre of the spring footprint and their print-bed face
is at ``Z == 0``.  ``make_spring_pair`` places the two handed springs at their
nominal module X positions without changing that orientation.

Magnet carriers use the magnet axis as their local Y axis.  Their local
origin is the carrier centre and the rear-load opening faces negative Y.  The
pair helper returns the released pose: the fixed carrier is behind the moving
carrier and pressing moves only the moving carrier in negative Y.

The spring and magnet factories are deliberately separate.  No factory in
this module combines printed springs with return magnets.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, degrees, hypot
from typing import Literal

from build123d import Axis, Box, Compound, Cylinder, Location, Shape, Solid

from .parameters import DEFAULTS, PillClickParameters


SpringSide = Literal["left", "right"]
MAGNET_GAP_VARIANTS: tuple[float, ...] = (0.8, 1.2, 1.6)


@dataclass(frozen=True)
class MagnetReturnPlacement:
    """Nominal carrier placement data for a centred repelling magnet pair.

    ``released_gap`` is the plastic-to-plastic clearance between the fixed
    and moving carriers.  At the fully pressed pose it becomes
    ``pressed_gap``.  Both magnets are installed with equal poles facing one
    another; polarity is an assembly instruction rather than printed
    geometry.
    """

    carrier_depth: float
    released_gap: float
    pressed_gap: float
    fixed_center_y: float
    moving_center_y: float


def _fuse(parts: list[Solid], label: str) -> Solid:
    """Fuse overlapping solids and require one closed positive-volume body."""

    if not parts:
        raise ValueError("at least one solid is required")
    result: Shape = parts[0]
    for part in parts[1:]:
        result = result.fuse(part)
    solids = list(result.solids())
    if len(solids) != 1:
        raise ValueError(f"{label} did not fuse into one solid")
    solid = solids[0]
    solid.label = label
    return solid


def _validate_spring_parameters(params: PillClickParameters) -> None:
    if params.spring_thickness <= 0:
        raise ValueError("spring_thickness must be positive")
    if params.spring_width <= params.spring_thickness:
        raise ValueError("spring_width must exceed spring_thickness")
    if params.spring_depth <= 4 * params.spring_thickness:
        raise ValueError("spring_depth is too short for its beam thickness")
    if params.spring_turns < 1:
        raise ValueError("spring_turns must be at least one")


def make_serpentine_spring(
    params: PillClickParameters = DEFAULTS,
    side: SpringSide = "left",
) -> Solid:
    """Build one replaceable, flat-printing serpentine return spring.

    ``spring_width`` controls the centreline's lateral peak-to-peak excursion;
    ``spring_depth`` controls the full Y footprint, and ``spring_thickness``
    is both the in-plane beam thickness and the printed Z thickness.  Broad
    end feet make the part easy to capture in simple slots.  ``side`` mirrors
    the meander while keeping the same local datum and bounding envelope.

    The output is a single labeled, closed, positive-volume solid.
    """

    _validate_spring_parameters(params)
    if side not in ("left", "right"):
        raise ValueError("side must be 'left' or 'right'")

    beam = params.spring_thickness
    height = params.spring_thickness
    depth = params.spring_depth
    turns = params.spring_turns
    handedness = -1.0 if side == "left" else 1.0

    # A compact foot leaves most of the requested depth available for flex.
    foot_depth = max(2.2, 1.4 * beam)
    flex_depth = depth - 2.0 * foot_depth
    half_excursion = params.spring_width / 2.0
    foot_width = params.spring_width + 2.0 * beam

    segment_count = 2 * turns + 1
    nodes: list[tuple[float, float]] = [(0.0, -flex_depth / 2.0)]
    for index in range(1, segment_count):
        fraction = index / segment_count
        x = handedness * half_excursion * (1.0 if index % 2 else -1.0)
        y = -flex_depth / 2.0 + fraction * flex_depth
        nodes.append((x, y))
    nodes.append((0.0, flex_depth / 2.0))

    z_center = height / 2.0
    parts: list[Solid] = []

    # Rounded node pads remove sharp internal corners and robustly join each
    # diagonal beam.  The cylinders are vertical and share the print-bed face.
    for x, y in nodes:
        parts.append(
            Location((x, y, z_center))
            * Cylinder(beam / 2.0, height)
        )

    for (x0, y0), (x1, y1) in zip(nodes, nodes[1:]):
        dx = x1 - x0
        dy = y1 - y0
        length = hypot(dx, dy)
        angle = degrees(atan2(dy, dx))
        segment = Box(length, beam, height)
        segment = segment.rotate(Axis.Z, angle)
        segment = Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, z_center)) * segment
        parts.append(segment)

    # Replaceable mounting feet.  Their inner edges overlap the endpoint pads,
    # producing one monolithic printable part without coincident-only joins.
    foot_y = depth / 2.0 - foot_depth / 2.0
    parts.extend(
        [
            Location((0.0, -foot_y, z_center))
            * Box(foot_width, foot_depth, height),
            Location((0.0, foot_y, z_center))
            * Box(foot_width, foot_depth, height),
        ]
    )

    return _fuse(parts, f"spring_return:{side}")


def spring_pair_offset_x(params: PillClickParameters = DEFAULTS) -> float:
    """Return the nominal X offset of either spring from module centre."""

    _validate_spring_parameters(params)
    half_foot = (params.spring_width + 2.0 * params.spring_thickness) / 2.0
    available_half_width = params.shuttle_width / 2.0
    offset = params.shuttle_width / 4.0
    if offset + half_foot > available_half_width:
        offset = available_half_width - half_foot
    if offset <= half_foot:
        raise ValueError("shuttle_width is too small for two separate springs")
    return offset


def make_spring_pair(params: PillClickParameters = DEFAULTS) -> Compound:
    """Return two mirrored spring parts at nominal module X positions.

    The labeled children remain separate replaceable parts.  This compound is
    for the spring variant only and contains no magnet carrier geometry.
    """

    offset = spring_pair_offset_x(params)
    left = Location((-offset, 0.0, 0.0)) * make_serpentine_spring(params, "left")
    right = Location((offset, 0.0, 0.0)) * make_serpentine_spring(params, "right")
    left.label = "spring_return:left"
    right.label = "spring_return:right"
    return Compound(children=[left, right], label="spring_return_pair")


def _validate_magnet_parameters(params: PillClickParameters) -> None:
    if params.magnet_diameter <= 0 or params.magnet_thickness <= 0:
        raise ValueError("magnet dimensions must be positive")
    if params.magnet_pocket_diameter <= params.magnet_diameter:
        raise ValueError("magnet pocket diameter must exceed magnet diameter")
    if params.magnet_pocket_depth <= params.magnet_thickness:
        raise ValueError("magnet pocket depth must exceed magnet thickness")
    if params.travel <= 0:
        raise ValueError("travel must be positive")


def magnet_carrier_depth(params: PillClickParameters = DEFAULTS) -> float:
    """Return carrier depth including a solid front medicine barrier."""

    _validate_magnet_parameters(params)
    barrier = max(1.2, params.wall / 2.0)
    return params.magnet_pocket_depth + barrier


def make_magnet_pocket_tool(params: PillClickParameters = DEFAULTS) -> Solid:
    """Return a positive cylinder tool for a rear-loaded magnet pocket.

    The local rear carrier face is at ``Y == -carrier_depth / 2``.  This tool
    overshoots only that rear face and terminates at the nominal pocket depth,
    preserving the calculated solid front wall after subtraction.
    """

    _validate_magnet_parameters(params)
    carrier_depth = magnet_carrier_depth(params)
    rear_y = -carrier_depth / 2.0
    overshoot = 0.4
    tool_depth = params.magnet_pocket_depth + overshoot
    tool_center_y = rear_y + (params.magnet_pocket_depth - overshoot) / 2.0
    tool = Cylinder(
        params.magnet_pocket_diameter / 2.0,
        tool_depth,
        rotation=(90.0, 0.0, 0.0),
    )
    tool = Location((0.0, tool_center_y, 0.0)) * tool
    tool.label = "return_magnet_pocket_tool"
    return tool


def _make_magnet_carrier(
    params: PillClickParameters,
    *,
    label: str,
    flange: bool,
) -> Solid:
    _validate_magnet_parameters(params)
    depth = magnet_carrier_depth(params)
    radial_wall = max(2.0, params.wall * 0.85)
    body_size = params.magnet_pocket_diameter + 2.0 * radial_wall
    body = Box(body_size, depth, body_size)

    if flange:
        # Side ears provide a broad fixed-housing interface while keeping the
        # rear pocket opening unobstructed.
        flange_width = body_size + 2.0 * params.wall
        flange_depth = min(1.6, depth)
        rear_y = -depth / 2.0
        flange_body = Box(flange_width, flange_depth, body_size)
        flange_body = Location((0.0, rear_y + flange_depth / 2.0, 0.0)) * flange_body
        body = body.fuse(flange_body)

    pocket = make_magnet_pocket_tool(params)
    carrier = body.cut(pocket)
    solids = list(carrier.solids())
    if len(solids) != 1:
        raise ValueError(f"{label} did not produce one carrier solid")
    result = solids[0]
    result.label = label
    return result


def make_fixed_magnet_carrier(params: PillClickParameters = DEFAULTS) -> Solid:
    """Build the rear-housing carrier for the fixed return magnet.

    The rear-loaded 6.1 x 2.1 mm default pocket faces negative Y.  A solid
    front wall separates the magnet from the moving mechanism.
    """

    return _make_magnet_carrier(
        params,
        label="return_magnet_carrier:fixed",
        flange=True,
    )


def make_moving_magnet_carrier(params: PillClickParameters = DEFAULTS) -> Solid:
    """Build the shuttle-side carrier for the moving return magnet.

    The pocket also loads from negative Y, leaving a continuous solid wall on
    the medicine-facing positive-Y side.  It is intended to be fused or
    mechanically captured behind the medicine shuttle by the assembly source.
    """

    return _make_magnet_carrier(
        params,
        label="return_magnet_carrier:moving",
        flange=False,
    )


def make_return_magnet_cap(
    params: PillClickParameters = DEFAULTS,
    *,
    role: Literal["fixed", "moving"],
) -> Solid:
    """Return a solid rear cap that mechanically traps one return magnet."""

    if role not in ("fixed", "moving"):
        raise ValueError("role must be fixed or moving")
    radial_wall = max(2.0, params.wall * 0.85)
    body_size = params.magnet_pocket_diameter + 2.0 * radial_wall
    cap = Box(body_size, params.trap_plate_thickness, body_size)
    cap.label = f"return_magnet_cap:{role}"
    return cap


def magnet_return_placement(
    params: PillClickParameters = DEFAULTS,
    *,
    pressed_gap: float | None = None,
) -> MagnetReturnPlacement:
    """Return ready-pose coordinates from the inward hard-stop minimum gap."""

    _validate_magnet_parameters(params)
    if pressed_gap is None:
        pressed_gap = params.magnet_min_gap
    if pressed_gap <= 0:
        raise ValueError("pressed_gap must be positive")
    depth = magnet_carrier_depth(params)
    released_gap = pressed_gap + params.total_press_span
    return MagnetReturnPlacement(
        carrier_depth=depth,
        released_gap=released_gap,
        pressed_gap=pressed_gap,
        fixed_center_y=-(released_gap / 2.0 + depth / 2.0),
        moving_center_y=released_gap / 2.0 + depth / 2.0,
    )


def make_magnet_return_pair(
    params: PillClickParameters = DEFAULTS,
    *,
    pressed_gap: float | None = None,
) -> Compound:
    """Return the centred opposing magnet carriers in the released pose.

    The labeled children are carrier solids with one centred rear-loaded
    pocket each.  Install one 6 x 2 mm magnet per pocket with equal poles
    facing across the gap.  This compound is for the magnet variant only and
    contains no printed spring geometry.

    A 6 x 2 mm pair has strongly distance-dependent repulsion.  In particular,
    a 13.4 mm travel makes the released pole separation much larger than the
    pressed separation, so this layout is a fit prototype rather than a claim
    that the pair can supply adequate return force over the full stroke.
    """

    placement = magnet_return_placement(params, pressed_gap=pressed_gap)
    fixed = Location((0.0, placement.fixed_center_y, 0.0)) * make_fixed_magnet_carrier(params)
    moving = Location((0.0, placement.moving_center_y, 0.0)) * make_moving_magnet_carrier(params)
    fixed.label = "return_magnet_carrier:fixed"
    moving.label = "return_magnet_carrier:moving"
    return Compound(children=[fixed, moving], label="return_magnet_pair")


def make_magnet_gap_shim(
    gap: float,
    params: PillClickParameters = DEFAULTS,
) -> Solid:
    """Return a labeled rear datum shim for a 0.8/1.2/1.6 mm minimum gap."""

    if gap not in MAGNET_GAP_VARIANTS:
        raise ValueError("gap must be one of 0.8, 1.2, or 1.6 mm")
    carrier_size = params.magnet_pocket_diameter + 2 * max(2.0, params.wall * 0.85)
    shim = Box(carrier_size, gap, carrier_size)
    shim.label = f"return_magnet_gap_shim:{gap:.1f}mm"
    return shim


__all__ = [
    "MagnetReturnPlacement",
    "MAGNET_GAP_VARIANTS",
    "SpringSide",
    "magnet_carrier_depth",
    "magnet_return_placement",
    "make_fixed_magnet_carrier",
    "make_magnet_pocket_tool",
    "make_magnet_gap_shim",
    "make_magnet_return_pair",
    "make_moving_magnet_carrier",
    "make_return_magnet_cap",
    "make_serpentine_spring",
    "make_spring_pair",
    "spring_pair_offset_x",
]
