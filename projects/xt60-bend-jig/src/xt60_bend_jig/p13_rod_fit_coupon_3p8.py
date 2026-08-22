"""Standalone PETG fit coupon for the measured P13 forming rods.

This module intentionally does not import or modify the production P13 model.
It is a source-derived diagnostic part for a rod measured at 3.80 mm.  Seven
closely spaced bores bracket the likely PETG press-to-slide transition without
wasting material on a full-size plate.

Coordinate convention:
    XY is the printer bed, +Z is thickness, and the lower face is Z=0.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path

from build123d import Align, Cylinder, Polygon, Pos, Text, extrude


@dataclass(frozen=True)
class P13RodFitCouponParameters:
    measured_rod_diameter: float = 3.80
    hole_diameters: tuple[float, ...] = (
        3.70,
        3.75,
        3.80,
        3.85,
        3.90,
        3.95,
        4.00,
    )
    plate_width: float = 40.0
    plate_depth: float = 28.0
    plate_thickness: float = 3.0
    clipped_corner_size: float = 4.0
    horizontal_pitch: float = 9.50
    row_offset_y: float = 5.50
    label_offset_y: float = 5.55
    engraving_depth: float = 0.35
    diameter_font_size: float = 2.20
    minimum_ligament: float = 3.00
    minimum_edge_wall: float = 3.00


DEFAULTS = P13RodFitCouponParameters()
PART_LABEL = "P13_rod_3p80_compact_fit_coupon_7_bores_3p70_to_4p00"


def parameter_manifest(
    p: P13RodFitCouponParameters = DEFAULTS,
) -> dict[str, object]:
    """Return a stable, serializable parameter contract for provenance."""

    return {
        "schema": "P13RodFitCoupon3p8/v2",
        "units": "mm",
        "coordinateConvention": "XY printer bed; lower face Z=0; +Z thickness",
        "parameters": asdict(p),
        "interpretation": {
            "3.70": "aggressive interference / expected failure bound",
            "3.80": "nominal press-fit candidate",
            "3.90": "nominal snug/removable candidate",
            "4.00": "nominal sliding candidate",
        },
        "stationOrder": [f"{diameter:.2f}" for diameter in p.hole_diameters],
        "printOrientation": "flat on XY; bore axes +Z, matching flat-printed caps",
        "physicalValidationRequired": True,
    }


def parameter_manifest_sha256(
    p: P13RodFitCouponParameters = DEFAULTS,
) -> str:
    payload = json.dumps(parameter_manifest(p), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def _validate_parameters(p: P13RodFitCouponParameters) -> None:
    if len(p.hole_diameters) != 7:
        raise ValueError("coupon must have exactly seven diameter stations")
    if tuple(sorted(set(p.hole_diameters))) != p.hole_diameters:
        raise ValueError("hole diameters must be strictly ordered")
    if p.plate_thickness <= 0 or p.engraving_depth <= 0:
        raise ValueError("plate thickness and engraving depth must be positive")
    if p.engraving_depth >= p.plate_thickness:
        raise ValueError("engraving must not cut through the coupon")
    if p.clipped_corner_size <= 0:
        raise ValueError("the asymmetric clipped datum must be present")
    if p.horizontal_pitch - max(p.hole_diameters) < p.minimum_ligament:
        raise ValueError("same-row bore ligament is below the PETG minimum")

    centres = hole_centres(p)
    max_radius = max(p.hole_diameters) / 2.0
    half_w = p.plate_width / 2.0
    half_d = p.plate_depth / 2.0
    if min(half_w - abs(x) - max_radius for x, _ in centres) < p.minimum_edge_wall:
        raise ValueError("bore-to-side edge wall is below the PETG minimum")
    if min(half_d - abs(y) - max_radius for _, y in centres) < p.minimum_edge_wall:
        raise ValueError("bore-to-end edge wall is below the PETG minimum")
    row_gap = 2.0 * p.row_offset_y - max(p.hole_diameters)
    if row_gap < p.minimum_ligament:
        raise ValueError("between-row bore ligament is below the PETG minimum")


def hole_centres(
    p: P13RodFitCouponParameters = DEFAULTS,
) -> tuple[tuple[float, float], ...]:
    pitch = p.horizontal_pitch
    y = p.row_offset_y
    # Ordered left-to-right across the upper row, then left-to-right across the
    # lower row.  This makes the engraved numeric order unambiguous.
    return (
        (-1.5 * pitch, y),
        (-0.5 * pitch, y),
        (0.5 * pitch, y),
        (1.5 * pitch, y),
        (-pitch, -y),
        (0.0, -y),
        (pitch, -y),
    )


def label_centres(
    p: P13RodFitCouponParameters = DEFAULTS,
) -> tuple[tuple[float, float], ...]:
    """Return diameter-label centres paired one-to-one with ``hole_centres``."""

    return tuple(
        (x, y + (p.label_offset_y if y > 0.0 else -p.label_offset_y))
        for x, y in hole_centres(p)
    )


def _engraved_text(text: str, font_size: float, x: float, y: float, p):
    """Return an overshooting engraving cutter for reliable top-face subtraction."""

    sketch = Pos(x, y) * Text(text, font_size=font_size)
    return Pos(0, 0, p.plate_thickness - p.engraving_depth) * extrude(
        sketch,
        amount=p.engraving_depth + 0.25,
    )


def build_coupon(p: P13RodFitCouponParameters = DEFAULTS):
    """Build the one-piece, flat-print coupon as one closed positive solid."""

    _validate_parameters(p)
    half_w = p.plate_width / 2.0
    half_d = p.plate_depth / 2.0
    clip = p.clipped_corner_size

    # The clipped upper-left corner is an unmistakable physical datum.
    outline = Polygon(
        (-half_w, -half_d),
        (half_w, -half_d),
        (half_w, half_d),
        (-half_w + clip, half_d),
        (-half_w, half_d - clip),
    )
    coupon = extrude(outline, amount=p.plate_thickness)

    for (x, y), diameter in zip(hole_centres(p), p.hole_diameters, strict=True):
        cutter = Pos(x, y, -0.5) * Cylinder(
            radius=diameter / 2.0,
            height=p.plate_thickness + 1.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        coupon = coupon - cutter

    for (x, y), diameter in zip(
        label_centres(p), p.hole_diameters, strict=True
    ):
        coupon = coupon - _engraved_text(
            f"{diameter:.2f}", p.diameter_font_size, x, y, p
        )

    coupon.label = PART_LABEL
    return coupon


def gen_step():
    return build_coupon(DEFAULTS)
