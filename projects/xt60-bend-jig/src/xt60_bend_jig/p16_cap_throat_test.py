"""P16 PETG cap-throat fit test for a 0.4 mm nozzle.

P15 proved that its common 3.60 mm entry throat dominated all three cavity
sizes.  P16 therefore fixes the cavity at 4.20 mm and varies only the entry
throat.  Every specimen has the same cap, slit, handle, and label geometry.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path

from build123d import Align, Box, Compound, Cylinder, Pos


@dataclass(frozen=True)
class P16CapThroatParameters:
    throat_diameters: tuple[float, ...] = (4.05, 4.10, 4.15)
    cavity_diameter: float = 4.20
    cap_outer_diameter: float = 7.00
    cap_height: float = 3.80
    closed_base_thickness: float = 0.80
    throat_depth: float = 0.60
    slit_width: float = 0.60
    station_pitch: float = 17.00
    tag_length: float = 7.00
    tag_width: float = 5.00
    tag_thickness: float = 1.20
    tag_overlap: float = 0.20
    digit_width: float = 1.60
    digit_height: float = 2.80
    digit_stroke: float = 0.80
    digit_gap: float = 0.35
    engraving_depth: float = 0.40
    boolean_overshoot: float = 0.03
    minimum_radial_wall: float = 1.40


DEFAULTS = P16CapThroatParameters()
PART_LABEL = "P16_PETG_cap_throat_test_405_410_415"

_DIGIT_SEGMENTS = {
    "0": "abcedf",  # normalized below; all except middle g
    "1": "bc",
    "2": "abdeg",
    "3": "abcdg",
    "4": "bcfg",
    "5": "acdfg",
}


def _segments_for_digit(digit: str) -> set[str]:
    if digit == "0":
        return {"a", "b", "c", "d", "e", "f"}
    return set(_DIGIT_SEGMENTS[digit])


def station_x_positions(p: P16CapThroatParameters = DEFAULTS) -> tuple[float, ...]:
    half = p.station_pitch * (len(p.throat_diameters) - 1) / 2.0
    return tuple(index * p.station_pitch - half for index in range(len(p.throat_diameters)))


def cavity_depth(p: P16CapThroatParameters = DEFAULTS) -> float:
    return p.cap_height - p.closed_base_thickness - p.throat_depth


def minimum_radial_wall(p: P16CapThroatParameters = DEFAULTS) -> float:
    return (p.cap_outer_diameter - p.cavity_diameter) / 2.0


def parameter_manifest(p: P16CapThroatParameters = DEFAULTS) -> dict[str, object]:
    return {
        "schema": "P16CapThroatTest/v1",
        "units": "mm",
        "coordinateConvention": "XY printer bed; closed cap end Z=0; rod entry +Z",
        "parameters": asdict(p),
        "stationOrderLeftToRight": [f"{diameter:.2f}" for diameter in p.throat_diameters],
        "labels": [f"{round(diameter * 100):03d}" for diameter in p.throat_diameters],
        "p15PhysicalFinding": "all P15 caps were far too tight; common 3.60 mm throat dominated",
        "testIntent": "hold 4.20 mm cavity and 0.60 mm slit constant; isolate throat diameter",
        "nozzleContract": {
            "diameterMm": 0.40,
            "minimumLabelStrokeMm": p.digit_stroke,
            "engravingDepthMm": p.engraving_depth,
        },
        "derived": {
            "cavityDepthMm": cavity_depth(p),
            "minimumRadialWallMm": minimum_radial_wall(p),
        },
        "printOrientation": "three caps upright on closed ends; sockets face +Z",
        "physicalValidationRequired": True,
    }


def parameter_manifest_sha256(p: P16CapThroatParameters = DEFAULTS) -> str:
    payload = json.dumps(parameter_manifest(p), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def _validate_parameters(p: P16CapThroatParameters) -> None:
    if p.throat_diameters != (4.05, 4.10, 4.15):
        raise ValueError("P16 throat stations must be exactly 4.05, 4.10, and 4.15 mm")
    if p.cavity_diameter != 4.20:
        raise ValueError("P16 must isolate the throat with a fixed 4.20 mm cavity")
    if p.cap_outer_diameter != 7.00 or p.cap_height != 3.80:
        raise ValueError("cap envelope must remain 7.00 x 3.80 mm")
    if cavity_depth(p) <= 0.0:
        raise ValueError("cavity depth must be positive")
    if max(p.throat_diameters) >= p.cavity_diameter:
        raise ValueError("every test throat must remain smaller than the common cavity")
    if minimum_radial_wall(p) < p.minimum_radial_wall:
        raise ValueError("cap radial wall is below the PETG minimum")
    if p.digit_stroke < 2.0 * 0.40:
        raise ValueError("label strokes must be at least two 0.4 mm nozzle widths")
    if p.engraving_depth < 0.40:
        raise ValueError("engraving must span at least two 0.20 mm layers")
    if p.tag_thickness <= p.engraving_depth:
        raise ValueError("engraving must not cut through the handling tag")
    local_span = p.cap_outer_diameter / 2.0 + p.tag_length - p.tag_overlap
    if p.station_pitch <= local_span + p.cap_outer_diameter / 2.0:
        raise ValueError("labeled specimens must not overlap")


def _seven_segment_cutters(text: str, center_x: float, p: P16CapThroatParameters):
    """Return explicit 0.8 mm-stroke digit cutters reliable with a 0.4 nozzle."""

    digit_pitch = p.digit_width + p.digit_gap
    total_width = len(text) * p.digit_width + (len(text) - 1) * p.digit_gap
    first_x = center_x - total_width / 2.0 + p.digit_width / 2.0
    t = p.digit_stroke
    half_h = p.digit_height / 2.0
    vertical_length = (p.digit_height - 3.0 * t) / 2.0
    if vertical_length <= 0.0:
        raise ValueError("digit height is too small for the requested stroke")

    cutters = []
    for index, digit in enumerate(text):
        x = first_x + index * digit_pitch
        segment_specs = {
            "a": (x, half_h - t / 2.0, p.digit_width, t),
            "g": (x, 0.0, p.digit_width, t),
            "d": (x, -half_h + t / 2.0, p.digit_width, t),
            "f": (x - p.digit_width / 2.0 + t / 2.0, (half_h + t / 2.0) / 2.0, t, vertical_length),
            "b": (x + p.digit_width / 2.0 - t / 2.0, (half_h + t / 2.0) / 2.0, t, vertical_length),
            "e": (x - p.digit_width / 2.0 + t / 2.0, -(half_h + t / 2.0) / 2.0, t, vertical_length),
            "c": (x + p.digit_width / 2.0 - t / 2.0, -(half_h + t / 2.0) / 2.0, t, vertical_length),
        }
        for segment in _segments_for_digit(digit):
            sx, sy, width, depth = segment_specs[segment]
            cutters.append(
                Pos(sx, sy, p.tag_thickness - p.engraving_depth / 2.0)
                * Box(
                    width,
                    depth,
                    p.engraving_depth + p.boolean_overshoot,
                    align=(Align.CENTER, Align.CENTER, Align.CENTER),
                )
            )
    return cutters


def build_functional_cap_core(
    throat_diameter: float,
    p: P16CapThroatParameters = DEFAULTS,
):
    """Build the physically tested cap body without its handling tag/label."""

    _validate_parameters(p)
    if throat_diameter not in p.throat_diameters:
        raise ValueError("throat diameter is not a P16 test station")

    over = p.boolean_overshoot
    radius = p.cap_outer_diameter / 2.0
    body = Cylinder(radius, p.cap_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    cavity = Pos(0.0, 0.0, p.closed_base_thickness) * Cylinder(
        p.cavity_diameter / 2.0,
        cavity_depth(p) + over,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    throat_z = p.cap_height - p.throat_depth
    throat = Pos(0.0, 0.0, throat_z) * Cylinder(
        throat_diameter / 2.0,
        p.throat_depth + over,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    slit_x0 = min(p.throat_diameters) / 2.0 - over
    slit_length = radius - slit_x0 + 2.0 * over
    slit_height = p.cap_height - p.closed_base_thickness + over
    slit = Pos(
        slit_x0 + slit_length / 2.0,
        0.0,
        p.closed_base_thickness + slit_height / 2.0,
    ) * Box(
        slit_length,
        p.slit_width,
        slit_height,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    result = body - [cavity, throat, slit]
    result.label = f"P16_functional_cap_core_4p20_throat_{throat_diameter:.2f}"
    return result


def build_cap(throat_diameter: float, p: P16CapThroatParameters = DEFAULTS):
    core = build_functional_cap_core(throat_diameter, p)
    radius = p.cap_outer_diameter / 2.0
    tag_center_x = -radius - p.tag_length / 2.0 + p.tag_overlap
    tag = Pos(tag_center_x, 0.0, 0.0) * Box(
        p.tag_length,
        p.tag_width,
        p.tag_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    label = f"{round(throat_diameter * 100):03d}"
    result = core.fuse(tag) - _seven_segment_cutters(label, tag_center_x, p)
    result.label = f"P16_cap_fixed_cavity_4p20_throat_{throat_diameter:.2f}_label_{label}"
    return result


def build_caps(p: P16CapThroatParameters = DEFAULTS) -> tuple:
    _validate_parameters(p)
    return tuple(
        Pos(x, 0.0, 0.0) * build_cap(diameter, p)
        for x, diameter in zip(station_x_positions(p), p.throat_diameters, strict=True)
    )


def build_cap_throat_test(p: P16CapThroatParameters = DEFAULTS) -> Compound:
    return Compound(children=list(build_caps(p)), label=PART_LABEL)


def gen_step():
    return build_cap_throat_test(DEFAULTS)
