"""P6 hardware-fit coupon for the purchased Ø4 x 50 mm stainless rods.

This is deliberately a coupon, not another jig mechanism.  It establishes a
real printed press bore, service-slip bore, plate thickness ladder, hex-cap
socket ladder, and a removable 38 mm setup gauge before hardware is committed
to the main bend fixture.  X is the rod axis; the 24 mm plate faces lie in YZ.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, radians, sin
from typing import Literal

from build123d import Align, Box, BuildSketch, Compound, Cone, Cylinder, Plane, Polygon, Pos, Rot, Shape, extrude, fillet
from cadgen import srgb


Side = Literal["left", "right"]


@dataclass(frozen=True, slots=True)
class P6Parameters:
    rod_diameter: float = 4.0
    rod_length: float = 50.0
    plate_size: float = 24.0
    plate_corner_radius: float = 2.0
    nominal_plate_thickness: float = 3.0
    plate_thicknesses: tuple[float, ...] = (2.0, 2.5, 3.0, 3.5)
    press_hole_diameter: float = 3.90
    slip_hole_diameter: float = 4.20
    mouth_chamfer: float = 0.4
    inner_gap: float = 38.0
    cap_flat_to_flat: float = 8.0
    cap_length: float = 5.0
    cap_socket_depth: float = 3.0
    cap_bores: tuple[float, ...] = (3.90, 4.00, 4.10, 4.20)
    gauge_length: float = 38.0
    gauge_width: float = 8.0
    gauge_thickness: float = 3.0

    @property
    def plate_center_x(self) -> float:
        return self.inner_gap / 2.0 + self.nominal_plate_thickness / 2.0

    @property
    def cap_circumradius(self) -> float:
        return self.cap_flat_to_flat / (2.0 * cos(radians(30.0)))


P6_DEFAULTS = P6Parameters()


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def _x_cylinder(diameter: float, length: float, x: float, y: float = 0.0, z: float = 0.0) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0, length, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )


def _plate_profile(params: P6Parameters) -> Shape:
    half = params.plate_size / 2.0
    with BuildSketch(Plane.YZ) as profile:
        Polygon((-half, -half), (half, -half), (half, half), (-half, half))
        fillet(profile.vertices(), radius=params.plate_corner_radius)
    return profile.sketch


def _chamfered_hole(center_x: float, thickness: float, diameter: float, params: P6Parameters) -> Shape:
    """Through bore with symmetric 0.4 x 45 degree lead-ins."""

    c = params.mouth_chamfer
    mouth = diameter + 2.0 * c
    land = _x_cylinder(diameter, thickness + 2.0, center_x)
    left = Pos(center_x - thickness / 2.0 + c / 2.0, 0.0, 0.0) * Cone(
        mouth / 2.0, diameter / 2.0, c, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    right = Pos(center_x + thickness / 2.0 - c / 2.0, 0.0, 0.0) * Cone(
        mouth / 2.0, diameter / 2.0, c, rotation=(0, -90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    return land + left + right


def build_plate(side: Side, thickness: float = P6_DEFAULTS.nominal_plate_thickness, params: P6Parameters = P6_DEFAULTS) -> Shape:
    """One R2 24 mm test plate: left press fit, right service-slip fit."""

    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    if thickness not in params.plate_thicknesses:
        raise ValueError("thickness must be one of the frozen coupon ladder values")
    sign = -1.0 if side == "left" else 1.0
    # The cap/rod seating datum is the nominal t3 outer face at X=+/-22.
    # Thus every thickness samples a real assembled inner gap: 40/39/38/37.
    outer_face = params.inner_gap / 2.0 + params.nominal_plate_thickness
    x = sign * (outer_face - thickness / 2.0)
    hole = params.press_hole_diameter if side == "left" else params.slip_hole_diameter
    plate = Pos(x, 0.0, 0.0) * extrude(_plate_profile(params), thickness / 2.0, both=True)
    # One to four edge notches physically identify the thickness ladder
    # without adding another through-hole or fragile embossed text.
    count = params.plate_thicknesses.index(thickness) + 1
    notches: Shape | None = None
    for index in range(count):
        y = -7.0 + 4.0 * index
        notch = _x_cylinder(2.0, thickness + 2.0, x, y, params.plate_size / 2.0)
        notches = notch if notches is None else notches + notch
    assert notches is not None
    # One separate far-right edge notch permanently distinguishes the loose
    # service (Ø4.20) plate from the press (Ø3.90) twin at the same thickness.
    service_notch = _x_cylinder(2.0, thickness + 2.0, x, 9.0, params.plate_size / 2.0) if side == "right" else None
    return _label(
        plate - _chamfered_hole(x, thickness, hole, params) - notches - service_notch if service_notch is not None else plate - _chamfered_hole(x, thickness, hole, params) - notches,
        f"{side}_{'press_3p90' if side == 'left' else 'slip_4p20_service_notch'}_plate_t{thickness:.1f}_24mm_R2_{count}edge_notches",
        "#3F6B4F" if side == "left" else "#5D7F70",
    )


def build_reference_rod(params: P6Parameters = P6_DEFAULTS) -> Shape:
    return _label(_x_cylinder(params.rod_diameter, params.rod_length, 0.0), "reference_purchased_stainless_4x50_rod", "#C9D0D4")


def _hex_profile(params: P6Parameters) -> Shape:
    radius = params.cap_circumradius
    # Flats normal to Y give a true 8 mm across-flats dimension in Y.
    points = [(radius * cos(radians(30 + 60 * index)), radius * sin(radians(30 + 60 * index))) for index in range(6)]
    with BuildSketch(Plane.YZ) as profile:
        Polygon(*points)
    return profile.sketch


def build_cap(side: Side, bore: float, params: P6Parameters = P6_DEFAULTS) -> Shape:
    """One 8 mm AF cap; entry is inward, socket is blind at 3 mm depth."""

    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    if bore not in params.cap_bores:
        raise ValueError("bore must be one of the frozen cap ladder values")
    sign = -1.0 if side == "left" else 1.0
    # Nominal plates have outer faces at +/-22. Cap occupies +/-22..27.
    x = sign * (params.inner_gap / 2.0 + params.nominal_plate_thickness + params.cap_length / 2.0)
    body = Pos(x, 0.0, 0.0) * extrude(_hex_profile(params), params.cap_length / 2.0, both=True)
    entry_x = sign * (params.inner_gap / 2.0 + params.nominal_plate_thickness)
    socket_center = entry_x + sign * params.cap_socket_depth / 2.0
    socket = _x_cylinder(bore, params.cap_socket_depth, socket_center)
    entry_chamfer = Pos(entry_x + sign * params.mouth_chamfer / 2.0, 0.0, 0.0) * Cone(
        (bore + 2.0 * params.mouth_chamfer) / 2.0, bore / 2.0, params.mouth_chamfer,
        rotation=(0, -90 * sign, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    # Matching count of shallow outer-end dimples identifies cap bores.
    count = params.cap_bores.index(bore) + 1
    dimples: Shape | None = None
    # Closed outer end only: keep the count dimples well clear of the inward
    # entry chamfer and the 3 mm socket.
    outer_x = x + sign * (params.cap_length / 2.0 - 0.4)
    for index in range(count):
        dimple = _x_cylinder(0.9, 0.9, outer_x, -2.7 + index * 1.25, 0.0)
        dimples = dimple if dimples is None else dimples + dimple
    assert dimples is not None
    return _label(
        body - socket - entry_chamfer - dimples,
        f"{side}_hex8AF_cap_bore_{bore:.2f}_socket3_closedend2_{count}dimples",
        "#E0A323",
    )


def build_setup_gauge(params: P6Parameters = P6_DEFAULTS) -> Shape:
    """Optional removable 38 mm gap gauge, deliberately not part of the clamp."""

    gauge = Pos(0.0, 0.0, -10.5) * Box(
        params.gauge_length, params.gauge_width, params.gauge_thickness,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    # Modest edge rounding makes this a reusable setup tool rather than a sharp spacer.
    vertical_edges = [edge for edge in gauge.edges() if edge.length == params.gauge_length]
    return _label(fillet(vertical_edges, radius=1.0), "optional_removable_38mm_setup_gauge_not_permanent", "#8C9498")


def build_nominal_assembly(include_gauge: bool = True, params: P6Parameters = P6_DEFAULTS) -> Compound:
    """Assembly order: press left near a rod end/cap, slide right from the
    opposite end, then apply its service cap. Never drag a tight plate 50 mm.
    The optional gauge and external clamps only hold plate pitch/squareness.
    """
    left = build_plate("left", params.nominal_plate_thickness, params)
    right = build_plate("right", params.nominal_plate_thickness, params)
    fixed_cap = build_cap("left", 3.90, params)
    service_cap = build_cap("right", 4.10, params)
    children = [left, right, build_reference_rod(params), fixed_cap, service_cap]
    if include_gauge:
        children.append(build_setup_gauge(params))
    return Compound(children=children, label="p6_nominal_t3_press_left_slip_right_38mm_gap")


def build_exploded_assembly(params: P6Parameters = P6_DEFAULTS) -> Compound:
    left = Pos(-6.0, 0.0, 0.0) * build_plate("left", params.nominal_plate_thickness, params)
    right = Pos(6.0, 0.0, 0.0) * build_plate("right", params.nominal_plate_thickness, params)
    rod = Pos(0.0, 0.0, 12.0) * build_reference_rod(params)
    fixed_cap = Pos(-12.0, 0.0, 12.0) * build_cap("left", 3.90, params)
    service_cap = Pos(12.0, 0.0, 12.0) * build_cap("right", 4.10, params)
    gauge = Pos(0.0, 0.0, -12.0) * build_setup_gauge(params)
    return Compound(children=[left, right, rod, fixed_cap, service_cap, gauge], label="p6_exploded_hardware_fit_coupon_access_view")


def build_plate_ladder(params: P6Parameters = P6_DEFAULTS) -> Compound:
    children: list[Shape] = []
    for index, thickness in enumerate(params.plate_thicknesses):
        left = Pos(index * 32.0, -15.0, 0.0) * build_plate("left", thickness, params)
        right = Pos(index * 32.0, 15.0, 0.0) * build_plate("right", thickness, params)
        left.label = f"ladder_{left.label}"
        right.label = f"ladder_{right.label}"
        children.extend((left, right))
    return Compound(children=children, label="p6_plate_thickness_ladder_press_and_slip_pairs")


def build_cap_ladder(params: P6Parameters = P6_DEFAULTS) -> Compound:
    children: list[Shape] = []
    for index, bore in enumerate(params.cap_bores):
        cap = Pos(index * 12.0, 0.0, 0.0) * build_cap("right", bore, params)
        cap.label = f"ladder_{cap.label}"
        children.append(cap)
    return Compound(children=children, label="p6_hex_cap_socket_bore_ladder")


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation is not None else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P6Parameters = P6_DEFAULTS) -> Compound:
    """All test variants: 8 plates, 4 caps, and the optional removable gauge."""

    children: list[Shape] = []
    for index, thickness in enumerate(params.plate_thicknesses):
        left = _on_bed(build_plate("left", thickness, params), index * 30.0, 0.0, Rot(0, 90, 0))
        right = _on_bed(build_plate("right", thickness, params), index * 30.0, 32.0, Rot(0, 90, 0))
        left.label = f"print_{left.label}"
        right.label = f"print_{right.label}"
        children.extend((left, right))
    for index, bore in enumerate(params.cap_bores):
        cap = _on_bed(build_cap("right", bore, params), 130.0 + index * 12.0, 0.0, Rot(0, 90, 0))
        cap.label = f"print_{cap.label}"
        children.append(cap)
    gauge = _on_bed(build_setup_gauge(params), 130.0, 24.0)
    gauge.label = "print_optional_removable_38mm_setup_gauge"
    children.append(gauge)
    return Compound(children=children, label="p6_full_print_kit_8_plates_4_caps_1_gauge")


__all__ = [
    "P6_DEFAULTS", "P6Parameters", "build_cap", "build_cap_ladder", "build_exploded_assembly",
    "build_nominal_assembly", "build_plate", "build_plate_ladder", "build_print_kit", "build_reference_rod",
    "build_setup_gauge",
]
