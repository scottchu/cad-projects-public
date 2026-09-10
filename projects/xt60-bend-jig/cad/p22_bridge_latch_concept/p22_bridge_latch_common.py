"""P22 evidence-only bridge latch concept for user intent review.

Coordinate frame: X is rod/axial direction; FRONT is the YZ plane.
This intentionally simplifies the inherited rail cuts. It tests only the
relationship: Blue and Green react, Orange is depressed, and a positive hook
retains a rigid bridge against immediate back-drive.
"""

from __future__ import annotations

from math import atan2, degrees, hypot

from build123d import Box, Compound, Cylinder, Pos, Rot
from cadgen import srgb


ROD_LENGTH = 50.0
ROD_DIAMETER = 4.0
PLATE_THICKNESS = 3.2
INNER_SPAN = 28.4
OUTER_GAP = 0.4
PLATE_RADIUS = 22.5

BLUE = (2.228077655, 5.248301944)
ORANGE_LOCKED = (8.478077655, -0.501698056)
ORANGE_RELEASED = (6.0, 5.0)
GREEN = (14.728077655, -6.251698056)


def _colored(shape, label: str, color: str, alpha: float = 1.0):
    shape.label = label
    shape.color = srgb(color, alpha)
    return shape


def _x_cylinder(diameter: float, length: float, x: float, y: float, z: float):
    return Pos(x - length / 2.0, y, z) * Rot(0, 90, 0) * Cylinder(diameter / 2.0, length)


def _plate(x: float, label: str, color: str):
    return _colored(_x_cylinder(PLATE_RADIUS * 2.0, PLATE_THICKNESS, x, 6.0, 0.0), label, color, 0.28)


def _bridge_bar(x: float):
    dy = GREEN[0] - BLUE[0]
    dz = GREEN[1] - BLUE[1]
    length = hypot(dy, dz) + 16.0
    angle = degrees(atan2(dz, dy))
    mid_y = (BLUE[0] + GREEN[0]) / 2.0
    mid_z = (BLUE[1] + GREEN[1]) / 2.0
    bar = Box(4.0, length, 7.0)
    return _colored(Pos(x, mid_y, mid_z) * Rot(angle, 0, 0) * bar, "rigid_blue_green_bridge", "#69727D")


def _reaction_pad(x: float, yz: tuple[float, float], label: str, color: str):
    return _colored(_x_cylinder(7.0, 5.0, x, yz[0], yz[1]), label, color)


def _positive_hook(x: float, engaged: bool):
    # A visible J-hook beside Green. It rotates away in RELEASED state.
    y, z = GREEN
    stem = Box(4.0, 5.0, 18.0)
    toe = Box(4.0, 10.0, 5.0)
    hook = Compound(children=[
        Pos(x, y + 8.0, z - 4.0) * stem,
        Pos(x, y + 4.5, z - 10.5) * toe,
    ])
    if not engaged:
        hook = Pos(0, y, z) * Rot(55, 0, 0) * Pos(0, -y, -z) * hook
    return _colored(hook, "positive_release_hook", "#D74F4F")


def build_concept(*, locked: bool):
    inner_x = INNER_SPAN / 2.0 + PLATE_THICKNESS / 2.0
    outer_x = inner_x + PLATE_THICKNESS + OUTER_GAP
    parts = [
        _plate(-inner_x, "fixed_left_inner", "#20242A"),
        _plate(inner_x, "fixed_right_inner", "#20242A"),
        _plate(-outer_x, "left_outer", "#343A42"),
        _plate(outer_x, "right_outer", "#343A42"),
    ]

    orange = ORANGE_LOCKED if locked else ORANGE_RELEASED
    for name, yz, color in (
        ("blue_reaction_rod_OD4_L50", BLUE, "#379BF6"),
        ("orange_driven_rod_OD4_L50", orange, "#F18742"),
        ("green_reaction_rod_OD4_L50", GREEN, "#4DBE73"),
    ):
        parts.append(_colored(_x_cylinder(ROD_DIAMETER, ROD_LENGTH, 0.0, yz[0], yz[1]), name, color))

    bridge_x = 29.0 if locked else 37.0
    parts.extend([
        _bridge_bar(bridge_x),
        _reaction_pad(27.0 if locked else 35.0, BLUE, "blue_bridge_seat", "#379BF6"),
        _reaction_pad(27.0 if locked else 35.0, GREEN, "green_bridge_seat", "#4DBE73"),
        _reaction_pad(27.0 if locked else 35.0, orange, "orange_press_pad", "#F18742"),
        _positive_hook(31.0 if locked else 39.0, locked),
    ])

    root = Compound(children=parts)
    root.label = "p22_bridge_latch_LOCKED" if locked else "p22_bridge_latch_RELEASED"
    return root
