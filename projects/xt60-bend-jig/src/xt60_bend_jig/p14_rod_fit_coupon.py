"""Standalone P14 PETG rod-fit coupon.

This diagnostic part is deliberately independent of every XT60 bend-jig
mechanism.  It places nine labeled bores on a 3 x 3 grid so a printed PETG
sample can establish the first reliably insertable diameter above the known
too-tight 4.00 mm physical control.

Coordinate convention:
    XY is the printer bed, +Z is thickness, and the lower face is Z=0.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import hypot, sqrt
from pathlib import Path

from build123d import Align, Cone, Cylinder, Polygon, Pos, Text, extrude


@dataclass(frozen=True)
class P14RodFitCouponParameters:
    hole_diameters: tuple[float, ...] = (
        4.00,
        4.05,
        4.10,
        4.15,
        4.20,
        4.25,
        4.30,
        4.35,
        4.40,
    )
    plate_width: float = 40.0
    plate_depth: float = 42.0
    plate_thickness: float = 3.0
    clipped_corner_size: float = 4.0
    grid_pitch: float = 14.0
    label_offset_y: float = 4.65
    engraving_depth: float = 0.35
    diameter_font_size: float = 2.35
    entrance_chamfer: float = 0.28
    boolean_overshoot: float = 0.02
    minimum_cylindrical_land: float = 2.40
    minimum_ligament: float = 3.00
    minimum_edge_wall: float = 3.00
    minimum_label_outline_clearance: float = 1.00


DEFAULTS = P14RodFitCouponParameters()
PART_LABEL = "P14_PETG_rod_fit_coupon_3x3_4p00_to_4p40"


def hole_centres(
    p: P14RodFitCouponParameters = DEFAULTS,
) -> tuple[tuple[float, float], ...]:
    """Return row-major stations: left-to-right, then top-to-bottom."""

    pitch = p.grid_pitch
    return tuple(
        (column * pitch, -row * pitch)
        for row in (-1, 0, 1)
        for column in (-1, 0, 1)
    )


def label_centres(
    p: P14RodFitCouponParameters = DEFAULTS,
) -> tuple[tuple[float, float], ...]:
    """Place each unique diameter label directly below its paired bore."""

    return tuple((x, y - p.label_offset_y) for x, y in hole_centres(p))


def cylindrical_land(p: P14RodFitCouponParameters = DEFAULTS) -> float:
    return p.plate_thickness - 2.0 * p.entrance_chamfer


def entrance_diameters(
    p: P14RodFitCouponParameters = DEFAULTS,
) -> tuple[float, ...]:
    """Diameters on the outer top and bottom faces after the 45-degree chamfer."""

    return tuple(diameter + 2.0 * p.entrance_chamfer for diameter in p.hole_diameters)


def minimum_actual_ligament(p: P14RodFitCouponParameters = DEFAULTS) -> float:
    """Minimum planar material between chamfer entrance envelopes."""

    centres = hole_centres(p)
    radii = [diameter / 2.0 + p.entrance_chamfer for diameter in p.hole_diameters]
    return min(
        hypot(x1 - x0, y1 - y0) - radii[index0] - radii[index1]
        for index0, (x0, y0) in enumerate(centres)
        for index1, (x1, y1) in enumerate(centres[index0 + 1 :], index0 + 1)
    )


def minimum_actual_edge_wall(p: P14RodFitCouponParameters = DEFAULTS) -> float:
    """Minimum wall from a chamfer entrance envelope to the five-sided outline."""

    half_w = p.plate_width / 2.0
    half_d = p.plate_depth / 2.0
    clip_line_constant = -half_w - half_d + p.clipped_corner_size
    results: list[float] = []
    for (x, y), diameter in zip(hole_centres(p), p.hole_diameters, strict=True):
        radius = diameter / 2.0 + p.entrance_chamfer
        results.extend(
            (
                half_w - x - radius,
                half_w + x - radius,
                half_d - y - radius,
                half_d + y - radius,
            )
        )
        # The clipped upper-left edge lies on x - y = clip_line_constant.
        results.append((x - y - clip_line_constant) / sqrt(2.0) - radius)
    return min(results)


def minimum_label_to_outline_clearance(
    p: P14RodFitCouponParameters = DEFAULTS,
) -> float:
    """Conservative exact clearance from actual text bounds to the outline.

    The axis-aligned outline checks use each rendered glyph string's build123d
    bounding box.  The clipped upper-left edge uses the nearest bounding-box
    corner, which is conservative when that corner contains no glyph ink.
    """

    half_w = p.plate_width / 2.0
    half_d = p.plate_depth / 2.0
    clip_line_constant = -half_w - half_d + p.clipped_corner_size
    clearances: list[float] = []
    for (x, y), diameter in zip(label_centres(p), p.hole_diameters, strict=True):
        bounds = (Pos(x, y) * Text(f"{diameter:.2f}", font_size=p.diameter_font_size)).bounding_box()
        clearances.extend(
            (
                bounds.min.X + half_w,
                half_w - bounds.max.X,
                bounds.min.Y + half_d,
                half_d - bounds.max.Y,
                (bounds.min.X - bounds.max.Y - clip_line_constant) / sqrt(2.0),
            )
        )
    return min(clearances)


def parameter_manifest(
    p: P14RodFitCouponParameters = DEFAULTS,
) -> dict[str, object]:
    """Return the stable, serializable design and physical-test contract."""

    return {
        "schema": "P14RodFitCoupon/v1",
        "units": "mm",
        "coordinateConvention": "XY printer bed; lower face Z=0; +Z thickness",
        "parameters": asdict(p),
        "stationOrder": [f"{diameter:.2f}" for diameter in p.hole_diameters],
        "stationTraversal": "row-major: left-to-right, top-to-bottom; clipped corner is upper-left start datum",
        "interpretation": {
            "4.00": "physical too-tight press control",
            "4.05-4.40": "ascending candidates for PETG rod insertion",
        },
        "chamfer": {
            "bothEntrances": True,
            "axialDepthMm": p.entrance_chamfer,
            "radialDepthMm": p.entrance_chamfer,
            "includedSlopeDegrees": 45.0,
            "cylindricalLandMm": cylindrical_land(p),
        },
        "derived": {
            "minimumActualLigamentMm": minimum_actual_ligament(p),
            "minimumActualEdgeWallMm": minimum_actual_edge_wall(p),
            "minimumLabelToOutlineClearanceMm": minimum_label_to_outline_clearance(p),
        },
        "printOrientation": "flat on XY; bore axes +Z",
        "physicalValidationRequired": True,
    }


def parameter_manifest_sha256(
    p: P14RodFitCouponParameters = DEFAULTS,
) -> str:
    payload = json.dumps(parameter_manifest(p), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def _validate_parameters(p: P14RodFitCouponParameters) -> None:
    expected = tuple(round(4.00 + 0.05 * index, 2) for index in range(9))
    if p.hole_diameters != expected:
        raise ValueError("coupon stations must be exactly 4.00 through 4.40 by 0.05 mm")
    if p.plate_thickness != 3.0:
        raise ValueError("coupon thickness must be exactly 3.0 mm")
    if not 0.25 <= p.entrance_chamfer <= 0.30:
        raise ValueError("entrance chamfer must be between 0.25 and 0.30 mm")
    if cylindrical_land(p) < p.minimum_cylindrical_land:
        raise ValueError("cylindrical bore land is below the required minimum")
    if p.engraving_depth <= 0.0 or p.engraving_depth >= p.plate_thickness:
        raise ValueError("engraving depth must be positive and shallower than the plate")
    if p.clipped_corner_size <= 0.0:
        raise ValueError("the upper-left traversal datum must be present")
    if minimum_actual_ligament(p) < p.minimum_ligament:
        raise ValueError("bore ligament is below the PETG minimum")
    if minimum_actual_edge_wall(p) < p.minimum_edge_wall:
        raise ValueError("bore-to-outline edge wall is below the PETG minimum")
    if minimum_label_to_outline_clearance(p) < p.minimum_label_outline_clearance:
        raise ValueError("engraved label-to-outline clearance is below the minimum")


def _bore_cutter(diameter: float, x: float, y: float, p: P14RodFitCouponParameters):
    """Build one through-cutter with exact 45-degree entrance chamfers."""

    nominal_radius = diameter / 2.0
    over = p.boolean_overshoot
    cylinder = Pos(x, y, -over) * Cylinder(
        radius=nominal_radius,
        height=p.plate_thickness + 2.0 * over,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    bottom = Pos(x, y, -over) * Cone(
        bottom_radius=nominal_radius + p.entrance_chamfer + over,
        top_radius=nominal_radius,
        height=p.entrance_chamfer + over,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    top = Pos(x, y, p.plate_thickness - p.entrance_chamfer) * Cone(
        bottom_radius=nominal_radius,
        top_radius=nominal_radius + p.entrance_chamfer + over,
        height=p.entrance_chamfer + over,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    return cylinder.fuse(bottom, top)


def _engraved_text(text: str, x: float, y: float, p: P14RodFitCouponParameters):
    sketch = Pos(x, y) * Text(text, font_size=p.diameter_font_size)
    return Pos(0, 0, p.plate_thickness - p.engraving_depth) * extrude(
        sketch,
        amount=p.engraving_depth + 0.25,
    )


def build_coupon(p: P14RodFitCouponParameters = DEFAULTS):
    """Build the one-piece, flat-print P14 coupon as one closed solid."""

    _validate_parameters(p)
    half_w = p.plate_width / 2.0
    half_d = p.plate_depth / 2.0
    clip = p.clipped_corner_size
    outline = Polygon(
        (-half_w, -half_d),
        (half_w, -half_d),
        (half_w, half_d),
        (-half_w + clip, half_d),
        (-half_w, half_d - clip),
    )
    coupon = extrude(outline, amount=p.plate_thickness)

    bores = [
        _bore_cutter(diameter, x, y, p)
        for (x, y), diameter in zip(hole_centres(p), p.hole_diameters, strict=True)
    ]
    coupon = coupon - bores

    labels = [
        _engraved_text(f"{diameter:.2f}", x, y, p)
        for (x, y), diameter in zip(label_centres(p), p.hole_diameters, strict=True)
    ]
    coupon = coupon - labels
    coupon.label = PART_LABEL
    return coupon


def gen_step():
    return build_coupon(DEFAULTS)
