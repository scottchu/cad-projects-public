"""P6 minimal two-plate / one-rod physical coupon.

This is not self-fixturing: one round rod leaves plate rotation free.  The
removable 38 mm gauge sets spacing only; a bench datum and two external clamps
set parallelism and angle.  Caps retain outward motion but cannot stop the
loose service plate moving inward after the gauge is removed.
"""

from __future__ import annotations

from dataclasses import dataclass

from build123d import Align, Box, Compound, Cone, Cylinder, Pos, Rot, Shape
from cadgen import srgb


@dataclass(frozen=True)
class P6Parameters:
    rod_diameter: float = 4.0
    rod_length: float = 50.0
    plate_size: float = 24.0
    plate_thickness: float = 3.0
    fixed_plate_bore: float = 3.90
    service_plate_bore: float = 4.05
    cap_outer_diameter: float = 8.0
    cap_length: float = 5.0
    cap_insertion_depth: float = 3.0
    cap_closed_end: float = 2.0
    fixed_cap_bore: float = 3.90
    service_cap_bore: float = 3.95
    cap_entry_chamfer: float = 0.35
    gap: float = 38.0
    gauge_width: float = 18.0
    gauge_height: float = 5.0


P6_DEFAULTS = P6Parameters()
THICKNESS_VARIANTS = (2.0, 2.5, 3.0, 3.5)
HOLE_FIT_DIAMETERS = (3.85, 3.90, 3.95, 4.00, 4.05, 4.10)
CAP_FIT_DIAMETERS = (3.85, 3.90, 3.95, 4.00)


def _label(shape: Shape, name: str, color: str) -> Shape:
    shape.label = name
    shape.color = srgb(color)
    return shape


def _z_bore(diameter: float, depth: float, z: float = -0.5) -> Shape:
    return Pos(0, 0, z) * Cylinder(
        diameter / 2, depth, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )


def build_plate(
    bore_diameter: float,
    thickness: float = 3.0,
    *,
    label: str = "square_plate",
    color: str = "#8A8F92",
    params: P6Parameters = P6_DEFAULTS,
) -> Shape:
    plate = Box(
        params.plate_size,
        params.plate_size,
        thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    plate -= _z_bore(bore_diameter, thickness + 1.0)
    return _label(plate, label, color)


def build_fixed_plate(params: P6Parameters = P6_DEFAULTS) -> Shape:
    return build_plate(
        params.fixed_plate_bore,
        params.plate_thickness,
        label="fixed_square_plate_24x24x3_bore_3p90_interference_candidate",
        color="#315B45",
        params=params,
    )


def build_service_plate(params: P6Parameters = P6_DEFAULTS) -> Shape:
    return build_plate(
        params.service_plate_bore,
        params.plate_thickness,
        label="service_square_plate_24x24x3_bore_4p05_clearance_candidate",
        color="#D39B19",
        params=params,
    )


def build_cap(
    bore_diameter: float,
    *,
    label: str = "blind_cap",
    color: str = "#8A8F92",
    params: P6Parameters = P6_DEFAULTS,
) -> Shape:
    """Round OD8 cap; local Z=0 is the open face and Z=3 the blind bottom."""

    cap = Cylinder(
        params.cap_outer_diameter / 2,
        params.cap_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    bore = _z_bore(bore_diameter, params.cap_insertion_depth + 0.01, -0.01)
    # Large radius at the open face, narrowing inward.
    entry = Pos(0, 0, -0.01) * Cone(
        bore_diameter / 2 + params.cap_entry_chamfer,
        bore_diameter / 2,
        params.cap_entry_chamfer,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    return _label(cap - bore - entry, label, color)


def build_fixed_cap(params: P6Parameters = P6_DEFAULTS) -> Shape:
    return build_cap(
        params.fixed_cap_bore,
        label="fixed_round_cap_OD8_L5_depth3_bore_3p90",
        color="#315B45",
        params=params,
    )


def build_service_cap(params: P6Parameters = P6_DEFAULTS) -> Shape:
    return build_cap(
        params.service_cap_bore,
        label="service_round_cap_OD8_L5_depth3_bore_3p95_removable_candidate",
        color="#D39B19",
        params=params,
    )


def build_reference_rod(params: P6Parameters = P6_DEFAULTS) -> Shape:
    rod = Cylinder(
        params.rod_diameter / 2,
        params.rod_length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return _label(rod, "purchased_steel_reference_rod_exact_4x50", "#B9C1C7")


def build_gap_gauge(params: P6Parameters = P6_DEFAULTS) -> Shape:
    """Broad spacer used below/off-axis from the rod, then removed sideways."""

    gauge = Box(
        params.gap,
        params.gauge_width,
        params.gauge_height,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return _label(
        gauge,
        "removable_38mm_gauge_use_below_rod_spacing_only_bench_and_two_clamps_set_parallelism",
        "#4F7AA3",
    )


def plate_centers(params: P6Parameters = P6_DEFAULTS) -> tuple[float, float]:
    return (
        -params.gap / 2 - params.plate_thickness / 2,
        params.gap / 2 + params.plate_thickness / 2,
    )


def _assembled_plate(plate: Shape, center_x: float) -> Shape:
    thickness = plate.bounding_box().size.Z
    return Pos(center_x - thickness / 2, 0, 0) * Rot(0, 90, 0) * plate


def _assembled_cap(cap: Shape, opening_x: float, side: str) -> Shape:
    if side == "left":
        return Pos(opening_x, 0, 0) * Rot(0, -90, 0) * cap
    if side == "right":
        return Pos(opening_x, 0, 0) * Rot(0, 90, 0) * cap
    raise ValueError("side must be left or right")


def build_default_assembly(params: P6Parameters = P6_DEFAULTS) -> Compound:
    left_x, right_x = plate_centers(params)
    fixed = _assembled_plate(build_fixed_plate(params), left_x)
    fixed.label = "fixed_square_plate_inner_minus19_outer_minus22"
    service = _assembled_plate(build_service_plate(params), right_x)
    service.label = "service_square_plate_inner_plus19_outer_plus22"
    left_cap = _assembled_cap(
        build_fixed_cap(params),
        -params.rod_length / 2 + params.cap_insertion_depth,
        "left",
    )
    left_cap.label = "fixed_cap_shoulder_at_x_minus22_socket_minus25_to_minus22"
    right_cap = _assembled_cap(
        build_service_cap(params),
        params.rod_length / 2 - params.cap_insertion_depth,
        "right",
    )
    right_cap.label = "service_cap_shoulder_at_x_plus22_socket_plus22_to_plus25"
    return Compound(
        children=[fixed, service, build_reference_rod(params), left_cap, right_cap],
        label="p6_two_plates_one_rod_two_caps_not_self_fixturing",
    )


def build_exploded(params: P6Parameters = P6_DEFAULTS) -> Compound:
    left_x, right_x = plate_centers(params)
    return Compound(
        children=[
            _assembled_plate(build_fixed_plate(params), left_x - 10),
            _assembled_plate(build_service_plate(params), right_x + 10),
            build_reference_rod(params),
            _assembled_cap(build_fixed_cap(params), -37, "left"),
            _assembled_cap(build_service_cap(params), 37, "right"),
        ],
        label="p6_exploded_same_five_parts",
    )


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P6Parameters = P6_DEFAULTS) -> Compound:
    fixed = _on_bed(build_fixed_plate(params), 0, 0)
    fixed.label = "print_fixed_plate_3mm_bore_3p90"
    service = _on_bed(build_service_plate(params), 30, 0)
    service.label = "print_service_plate_3mm_bore_4p05"
    fixed_cap = _on_bed(build_fixed_cap(params), 60, 0, Rot(180, 0, 0))
    fixed_cap.label = "print_fixed_round_cap_bore_3p90_closed_end_on_bed"
    service_cap = _on_bed(build_service_cap(params), 72, 0, Rot(180, 0, 0))
    service_cap.label = "print_service_round_cap_bore_3p95_closed_end_on_bed"
    gauge = _on_bed(build_gap_gauge(params), 0, 32)
    gauge.label = "print_broad_38mm_gap_gauge"
    return Compound(
        children=[fixed, service, fixed_cap, service_cap, gauge],
        label="p6_print_kit_two_plates_two_caps_one_gauge_no_rod",
    )


def build_hole_fit_ladder(params: P6Parameters = P6_DEFAULTS) -> Shape:
    ladder = Box(82, 16, params.plate_thickness, align=(Align.MIN, Align.CENTER, Align.MIN))
    for index, diameter in enumerate(HOLE_FIT_DIAMETERS):
        ladder -= Pos(11 + index * 12, 0, 0) * _z_bore(diameter, params.plate_thickness + 1)
    # Key notch identifies the 3.85 end.
    ladder -= Pos(0, 5, -0.5) * Box(
        4, 3, params.plate_thickness + 1, align=(Align.MIN, Align.MIN, Align.MIN)
    )
    return _label(
        ladder,
        "keyed_hole_ladder_3p85_3p90_3p95_4p00_4p05_4p10",
        "#8A8F92",
    )


def build_fit_ladder(params: P6Parameters = P6_DEFAULTS) -> Compound:
    parts: list[Shape] = []
    for index, thickness in enumerate(THICKNESS_VARIANTS):
        coupon = build_plate(
            params.service_plate_bore,
            thickness,
            label=f"thickness_coupon_{thickness:.1f}mm_bore_4p05",
            params=params,
        )
        coupon = _on_bed(coupon, index * 30, 0)
        coupon.label = f"thickness_coupon_{thickness:.1f}mm_bore_4p05"
        parts.append(coupon)
    ladder = _on_bed(build_hole_fit_ladder(params), 0, 32)
    ladder.label = "hole_ladder_vertical_bores_keyed_3p85_to_4p10"
    parts.append(ladder)
    for index, diameter in enumerate(CAP_FIT_DIAMETERS):
        cap = build_cap(diameter, label=f"cap_fit_bore_{diameter:.2f}".replace(".", "p"), params=params)
        cap = _on_bed(cap, 88 + index * 12, 32, Rot(180, 0, 0))
        cap.label = f"cap_fit_bore_{diameter:.2f}_vertical".replace(".", "p")
        parts.append(cap)
    return Compound(
        children=parts,
        label="p6_fit_ladder_all_plate_and_cap_bores_vertical_for_print_test",
    )


__all__ = [
    "CAP_FIT_DIAMETERS", "HOLE_FIT_DIAMETERS", "P6_DEFAULTS", "P6Parameters",
    "THICKNESS_VARIANTS", "build_cap", "build_default_assembly", "build_exploded",
    "build_fit_ladder", "build_fixed_cap", "build_fixed_plate", "build_gap_gauge",
    "build_hole_fit_ladder", "build_plate", "build_print_kit", "build_reference_rod",
    "build_service_cap", "build_service_plate", "plate_centers",
]
