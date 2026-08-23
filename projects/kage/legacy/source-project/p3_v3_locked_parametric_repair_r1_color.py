"""Project-local copy of the non-geometric sRGB color helper."""

from __future__ import annotations

from build123d import Color


def _linear(channel: float) -> float:
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def srgb(value: str, alpha: float = 1.0) -> Color:
    text = value.strip().lstrip("#")
    if len(text) == 3:
        text = "".join(character * 2 for character in text)
    if len(text) != 6:
        raise ValueError(f"expected #rgb or #rrggbb, got {value!r}")
    red, green, blue = (int(text[index:index + 2], 16) for index in (0, 2, 4))
    return Color(_linear(red / 255.0), _linear(green / 255.0), _linear(blue / 255.0), alpha)

