"""Deterministic D4 face-only colour separation in source-image coordinates."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image


CLASSES = ("black", "gray", "white", "deep-blue", "glass-mix")
PALETTE = {
    "black": "#08090b",
    "gray": "#9b9b9d",
    "white": "#ffffff",
    "deep-blue": "#075fbc",
    "glass-mix": "#b8d9ec",
}


def flood_background(candidate: np.ndarray) -> np.ndarray:
    """Return only candidate pixels connected to the canvas edge (4-neighbour)."""
    height, width = candidate.shape
    out = np.zeros_like(candidate, dtype=bool)
    stack = [(x, y) for x in range(width) for y in (0, height - 1) if candidate[y, x]]
    stack += [(x, y) for y in range(height) for x in (0, width - 1) if candidate[y, x]]
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= width or y >= height or out[y, x] or not candidate[y, x]:
            continue
        out[y, x] = True
        stack.extend(((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
    return out


def classify_rgb(rgb: np.ndarray) -> tuple[dict[str, np.ndarray], np.ndarray]:
    """Quantize D4 RGB pixels, with named source-coordinate repair regions.

    The tire regions retain dark-gray tread blocks distinct from black grooves.
    The bumper/skid regions consolidate neutral anti-alias shading only; the
    license plate and lights remain outside those repair regions.
    """
    red, green, blue = (rgb[:, :, channel] for channel in range(3))
    near_white = np.minimum(np.minimum(red, green), blue) >= 242
    background = flood_background(near_white)
    foreground = ~background

    value = np.maximum(np.maximum(red, green), blue)
    black = foreground & (value < 76)
    deep_blue = foreground & ~black & (blue > green + 35) & (blue > red + 100) & (red < 110)
    glass = foreground & ~black & ~deep_blue & (blue > red + 15) & (green > red + 12) & (blue >= green)
    white = foreground & ~black & ~deep_blue & ~glass & (np.minimum(np.minimum(red, green), blue) >= 190) & ((np.maximum(np.maximum(red, green), blue) - np.minimum(np.minimum(red, green), blue)) <= 48)
    gray = foreground & ~(black | deep_blue | glass | white)

    # D4 pixel-coordinate ROIs, derived from its visible wheel and lower-body
    # regions. They do not alter the canvas, contours, lettering, or lamps.
    tire_roi = np.zeros_like(foreground)
    tire_roi[860:1110, 45:305] = True
    tire_roi[795:1120, 805:1115] = True
    tire_roi[690:1010, 1080:1235] = True
    tire_gray = foreground & tire_roi & (value >= 34) & (value < 76) & ((np.maximum(np.maximum(red, green), blue) - np.minimum(np.minimum(red, green), blue)) <= 28)
    black &= ~tire_gray
    gray |= tire_gray

    lower_body_roi = np.zeros_like(foreground)
    lower_body_roi[795:1010, 175:320] = True
    lower_body_roi[795:1010, 625:1010] = True
    lower_body_roi[945:1045, 265:805] = True
    neutral = (np.maximum(np.maximum(red, green), blue) - np.minimum(np.minimum(red, green), blue)) <= 28
    body_gray = foreground & lower_body_roi & neutral & (value >= 46) & (value < 186)
    body_white = foreground & lower_body_roi & neutral & (value >= 186)
    # The plate remains an intentionally bright white distinct from bumper
    # shading, so its source-derived rectangle is excluded from consolidation.
    plate_roi = np.zeros_like(foreground)
    plate_roi[840:950, 325:625] = True
    body_gray &= ~plate_roi
    body_white &= ~plate_roi
    black &= ~(body_gray | body_white)
    white &= ~body_gray
    gray &= ~body_white
    gray |= body_gray
    white |= body_white
    masks = {"black": black, "gray": gray, "white": white, "deep-blue": deep_blue, "glass-mix": glass}
    return masks, background


def classify(image_path: Path) -> tuple[dict[str, np.ndarray], np.ndarray]:
    """Load D4 then delegate to the deterministic RGB classifier."""
    rgb = np.asarray(Image.open(image_path).convert("RGB"), dtype=np.int16)
    return classify_rgb(rgb)


def contours(mask: np.ndarray) -> list[list[tuple[int, int]]]:
    """Trace grid-aligned closed boundaries; preserve every pixel-scale component."""
    height, width = mask.shape
    edges: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for y, x in np.argwhere(mask):
        if y == 0 or not mask[y - 1, x]:
            edges[(x, y)].append((x + 1, y))
        if x == width - 1 or not mask[y, x + 1]:
            edges[(x + 1, y)].append((x + 1, y + 1))
        if y == height - 1 or not mask[y + 1, x]:
            edges[(x + 1, y + 1)].append((x, y + 1))
        if x == 0 or not mask[y, x - 1]:
            edges[(x, y + 1)].append((x, y))

    paths: list[list[tuple[int, int]]] = []
    while edges:
        start = next(iter(edges))
        point = start
        path = [start]
        incoming: tuple[int, int] | None = None
        while True:
            candidates = edges[point]
            if incoming is None:
                end = candidates[-1]
            else:
                # A right-hand turn preserves the clockwise boundary of a
                # component at a diagonal-only contact instead of crossing
                # into the component that merely shares that grid vertex.
                direction = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}[incoming]
                preference = ((direction + 1) % 4, direction, (direction + 3) % 4, (direction + 2) % 4)
                by_direction = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}
                candidates_by_direction = {by_direction[(end[0] - point[0], end[1] - point[1])]: end for end in candidates}
                end = next(candidates_by_direction[value] for value in preference if value in candidates_by_direction)
            candidates.remove(end)
            if not edges[point]:
                del edges[point]
            incoming = (end[0] - point[0], end[1] - point[1])
            point = end
            path.append(point)
            if point == start:
                break
        paths.extend(simplify_collinear(loop) for loop in split_self_touching(path))
    return paths


def split_self_touching(path: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    """Decompose a closed grid walk at every repeated vertex.

    Pixel components can touch diagonally while also connecting elsewhere. A
    right-hand walk then legitimately revisits a grid vertex, which is valid
    under even-odd fill but not import-safe as one self-touching SVG subpath.
    Splitting retains every directed boundary segment as simple closed loops.
    """
    pending = [path]
    simple: list[list[tuple[int, int]]] = []
    while pending:
        current = pending.pop()
        seen: dict[tuple[int, int], int] = {}
        split_at: tuple[int, int] | None = None
        for index, point in enumerate(current[:-1]):
            if point in seen:
                split_at = (seen[point], index)
                break
            seen[point] = index
        if split_at is None:
            simple.append(current)
            continue
        first, second = split_at
        loop = current[first:second + 1]
        remainder = current[:first + 1] + current[second + 1:]
        pending.extend((loop, remainder))
    return simple


def simplify_collinear(path: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Remove only redundant straight grid vertices; never smooth or discard contours."""
    if len(path) <= 4:
        return path
    core = path[:-1]
    kept: list[tuple[int, int]] = []
    for index, current in enumerate(core):
        previous = core[index - 1]
        following = core[(index + 1) % len(core)]
        if (previous[0] == current[0] == following[0]) or (previous[1] == current[1] == following[1]):
            continue
        kept.append(current)
    return kept + [kept[0]]


def svg_path(paths: list[list[tuple[int, int]]]) -> str:
    return " ".join("M " + " L ".join(f"{x} {y}" for x, y in path) + " Z" for path in paths)


def generate(input_path: Path, output_path: Path, report_path: Path) -> dict[str, object]:
    masks, background = classify(input_path)
    height, width = background.shape
    groups = []
    counts: dict[str, int] = {}
    contour_counts: dict[str, int] = {}
    for name in CLASSES:
        paths = contours(masks[name])
        counts[name] = int(masks[name].sum())
        contour_counts[name] = len(paths)
        groups.append(f'  <g id="{name}" data-visible-class="{name}" fill="{PALETTE[name]}" fill-rule="evenodd"><path d="{svg_path(paths)}"/></g>')
    source_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join((
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" data-source-sha256="{source_hash}" data-units="source-image-units">',
        '  <title>D4 five-class face separation</title>',
        *groups,
        '</svg>',
        '',
    )), encoding="utf-8")
    report = {
        "source": str(input_path), "source_sha256": source_hash, "width": width, "height": height,
        "units": "source-image-units", "class_pixel_counts": counts,
        "class_contours": contour_counts, "background_pixels": int(background.sum()),
        "method": "exclusive RGB rules; edge-connected near-white background removed; shared pixel-grid boundaries; collinear-only path reduction",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    generate(args.input, args.output, args.report)


if __name__ == "__main__":
    main()
