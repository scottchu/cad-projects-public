"""STEP-first geometry for the P3 V3 R2 progressive print coupons.

The functional models stay at the parent clock coordinates.  Export code lays
individual printable parts onto the build plate without changing these source
datums.  Purchased hardware and motor/gear references are assembly-only.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin, sqrt

import py_gearworks as pgw
from build123d import (
    Align,
    Axis,
    Box,
    Compound,
    Cone,
    Cylinder,
    Face,
    Location,
    Vector,
    Wire,
    extrude,
)
from cadgen import srgb

from p3_v3_full_ring_r2_geometry import make_output_pinion
from p3_v3_r2_print_coupon_spec import (
    P3V3R2PrintCouponSpec,
    P3_V3_R2_PRINT_COUPON,
)
from p3_v3_transmission_r1_geometry import (
    make_bearing as r1_make_bearing,
    make_miter_pair as r1_make_miter_pair,
    make_motor_body as r1_make_motor_body,
    make_motor_shaft as r1_make_motor_shaft,
    make_output_shaft as r1_make_output_shaft,
)


def _annulus(inner: float, outer: float, height: float, z0: float):
    outside = Cylinder(outer, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0))
    )
    inside = Cylinder(inner, height + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0 - 0.2))
    )
    return outside.cut(inside)


def _sector_prism(radius: float, angle0: float, angle1: float, z0: float, z1: float):
    """Convex fan prism used only as a stable cutter for short ring arcs."""

    samples = max(8, int(abs(angle1 - angle0)) + 1)
    points = [Vector(0.0, 0.0, 0.0)]
    for index in range(samples + 1):
        angle = radians(angle0 + (angle1 - angle0) * index / samples)
        points.append(Vector(radius * cos(angle), radius * sin(angle), 0.0))
    face = Face(Wire.make_polygon(points, close=True))
    return extrude(face, amount=z1 - z0).moved(Location((0.0, 0.0, z0)))


def _hex_prism(af: float, height: float, z0: float, x: float, y: float):
    radius = af / sqrt(3.0)
    points = [
        Vector(x + radius * cos(radians(30.0 + i * 60.0)), y + radius * sin(radians(30.0 + i * 60.0)), 0.0)
        for i in range(6)
    ]
    return extrude(Face(Wire.make_polygon(points, close=True)), amount=height).moved(
        Location((0.0, 0.0, z0))
    )


def _intersection_volume(left, right) -> float:
    common = left.intersect(right)
    return sum(solid.volume for solid in common.solids()) if common else 0.0


def _ring_gear_teeth(height: float, z0: float, spec: P3V3R2PrintCouponSpec):
    wrapper = pgw.SpurRingGear(
        number_of_teeth=spec.ring_teeth,
        module=spec.module,
        height=height,
        center=[0.0, 0.0, z0],
        pressure_angle=radians(spec.pressure_angle_degrees),
        backlash=0.10,
    )
    return wrapper.build_part().solid().rotate(Axis.Z, spec.tooth_phase_offset_degrees)


@lru_cache(maxsize=1)
def _seam_ring_master():
    p = P3_V3_R2_PRINT_COUPON
    teeth = _ring_gear_teeth(p.ring_thickness, 0.0, p)
    body = _annulus(p.ring_root_radius, p.ring_body_outer_radius, p.ring_thickness, 0.0)
    race = _annulus(p.race_inner_radius, p.race_outer_radius, p.race_axial, 0.0)
    return teeth.fuse(body).fuse(race)


def _seam_cutters(spec: P3V3R2PrintCouponSpec):
    bore = Cylinder(
        spec.seam_clamp_bore_diameter / 2.0,
        spec.ring_thickness + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((spec.seam_clamp_radius, 0.0, -0.2)))
    countersink = Cone(
        spec.seam_clamp_bore_diameter / 2.0,
        spec.seam_countersink_diameter / 2.0,
        spec.seam_countersink_depth,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((spec.seam_clamp_radius, 0.0, spec.ring_thickness - spec.seam_countersink_depth)))
    nut = _hex_prism(
        spec.seam_nut_af,
        spec.seam_nut_depth + 0.01,
        -0.005,
        spec.seam_clamp_radius,
        0.0,
    )
    pins = [
        Cylinder(
            spec.alignment_bore_diameter / 2.0,
            spec.ring_thickness + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.seam_clamp_radius, y, -0.2)))
        for y in spec.alignment_pin_tangential_offsets
    ]
    return (bore, countersink, nut, *pins)


def make_seam_arc_half(side: str, spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    """One real 12-tooth arc end with its complementary flush half-lap."""

    if side not in {"lower", "upper"}:
        raise ValueError("seam side must be lower or upper")
    sign = -1.0 if side == "lower" else 1.0
    angle0, angle1 = ((-spec.seam_half_angle_degrees, 0.0) if sign < 0 else (0.0, spec.seam_half_angle_degrees))
    sector = _sector_prism(spec.ring_outer_radius + 1.0, angle0, angle1, -0.2, spec.ring_thickness + 0.4)
    fragments = _seam_ring_master().intersect(sector)
    arc = max(fragments, key=lambda shape: shape.volume)

    lap_band = _annulus(
        spec.seam_lap_inner_radius,
        spec.seam_lap_outer_radius,
        spec.ring_thickness,
        0.0,
    )
    native_box = Box(
        10.0,
        spec.seam_overlap_half,
        spec.seam_lap_layer + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(
        Location(
            (
                (spec.seam_lap_inner_radius + spec.seam_lap_outer_radius) / 2.0,
                sign * spec.seam_overlap_half / 2.0,
                spec.seam_lap_layer if side == "lower" else -0.2,
            )
        )
    )
    # Remove the complementary layer on the native side, then cross the seam
    # with the retained half.  Teeth (R < 132) and race (R >= 138) are never cut.
    native_relief_pieces = lap_band.intersect(native_box)
    native_relief = max(native_relief_pieces, key=lambda shape: shape.volume)
    arc = arc.cut(native_relief)
    tongue_z = 0.0 if side == "lower" else spec.seam_lap_layer
    tongue_box = Box(
        10.0,
        spec.seam_overlap_half,
        spec.seam_lap_layer,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(
        Location(
            (
                (spec.seam_lap_inner_radius + spec.seam_lap_outer_radius) / 2.0,
                -sign * spec.seam_overlap_half / 2.0,
                tongue_z,
            )
        )
    )
    tongue = max(tongue_box.intersect(lap_band), key=lambda shape: shape.volume)
    arc = arc.fuse(tongue)
    for cutter in _seam_cutters(spec):
        arc = arc.cut(cutter)
    arc.label = f"p3_v3_r2_seam_{side}_real_12T_arc_half"
    arc.color = srgb("#3F8F87" if side == "lower" else "#E38B48")
    return arc


def make_seam_hardware_references(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    core = Cylinder(
        1.0,
        spec.ring_thickness - spec.seam_countersink_depth,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((spec.seam_clamp_radius, 0.0, 0.0)))
    head = Cone(
        1.0,
        spec.seam_countersink_diameter / 2.0 - 0.05,
        spec.seam_countersink_depth,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((spec.seam_clamp_radius, 0.0, spec.ring_thickness - spec.seam_countersink_depth)))
    screw = core.fuse(head)
    screw.label = "p3_v3_r2_seam_M2_flush_screw_REFERENCE"
    screw.color = srgb("#6B7074")
    nut = _hex_prism(4.0, spec.seam_nut_depth, 0.0, spec.seam_clamp_radius, 0.0)
    nut.label = "p3_v3_r2_seam_M2_AF4_nut_REFERENCE"
    nut.color = srgb("#778187")
    pins = []
    for index, y in enumerate(spec.alignment_pin_tangential_offsets):
        pin = Cylinder(
            spec.alignment_pin_diameter / 2.0,
            spec.alignment_pin_length,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.seam_clamp_radius, y, 0.0)))
        pin.label = f"p3_v3_r2_seam_D2x3_alignment_pin_{index + 1}_REFERENCE"
        pin.color = srgb("#778187")
        pins.append(pin)
    return (screw, nut, *pins)


def make_guide_shoe_variant(clearance: float, index: int = 0, spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    if clearance not in spec.guide_clearances:
        raise ValueError("guide clearance is not one of the frozen variants")
    length = spec.guide_shoe_tangential_length
    outer_width = spec.guide_shoe_radial_width + 2.0 * spec.guide_shoe_floor
    height = spec.race_axial + 2.0 * clearance + 2.0 * spec.guide_shoe_floor
    shoe = Box(
        outer_width,
        length,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((139.0, 28.0 + index * 18.0, -clearance - spec.guide_shoe_floor)))
    cavity = Box(
        (spec.race_outer_radius - spec.race_inner_radius) + 2.0 * clearance,
        length + 0.4,
        spec.race_axial + 2.0 * clearance,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((139.0, 28.0 + index * 18.0, -clearance)))
    shoe = shoe.cut(cavity)
    shoe.label = f"p3_v3_r2_guide_shoe_clearance_{clearance:.2f}mm"
    shoe.color = srgb(("#4E7D72", "#D39B55", "#9A6F99")[index])
    return shoe


def make_guide_race_gauge(clearance: float, index: int = 0, spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    gauge = Box(
        spec.race_outer_radius - spec.race_inner_radius,
        spec.guide_shoe_tangential_length - 0.4,
        spec.race_axial,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((139.0, 28.0 + index * 18.0, 0.0)))
    gauge.label = f"p3_v3_r2_race_gauge_for_{clearance:.2f}mm_shoe_REFERENCE"
    gauge.color = srgb("#C7C9C8")
    return gauge


def make_stationary_joiner_parts(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    bx, by, bz = spec.joiner_body_size
    sx, sy, sz = spec.joiner_step_size
    male = Box(bx / 2.0, by, bz, align=(Align.MAX, Align.CENTER, Align.MIN))
    tongue = Box(sx, sy, sz, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((0.0, 0.0, bz - sz)))
    male = male.fuse(tongue)
    female = Box(bx / 2.0, by, bz, align=(Align.MIN, Align.CENTER, Align.MIN))
    pocket = Box(
        sx + 2.0 * spec.joiner_clearance,
        sy + 2.0 * spec.joiner_clearance,
        sz + spec.joiner_clearance,
        align=(Align.MIN, Align.CENTER, Align.MAX),
    ).moved(Location((-spec.joiner_clearance, 0.0, bz + 0.01)))
    female = female.cut(pocket)
    for part_name, part in (("male", male), ("female", female)):
        bore = Cylinder(
            spec.joiner_m3_clearance / 2.0,
            bz + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((2.0, 0.0, -0.2)))
        part = part.cut(bore)
        if part_name == "male":
            part = part.cut(_hex_prism(spec.joiner_m3_nut_af, spec.joiner_m3_nut_depth, 0.0, 2.0, 0.0))
            male = part
        else:
            female = part
    male.label = "p3_v3_r2_stationary_joiner_male_6x4x1p2_step"
    female.label = "p3_v3_r2_stationary_joiner_female_clearance_0p25"
    male.color = female.color = srgb("#69737A")
    return male, female


def make_seam_coupon_assembly(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    children = [make_seam_arc_half("lower", spec), make_seam_arc_half("upper", spec)]
    children.extend(make_seam_hardware_references(spec))
    for index, clearance in enumerate(spec.guide_clearances):
        children.append(make_guide_shoe_variant(clearance, index, spec))
        children.append(make_guide_race_gauge(clearance, index, spec))
    male, female = make_stationary_joiner_parts(spec)
    children.extend((male.moved(Location((105.0, 58.0, 0.0))), female.moved(Location((105.0, 58.0, 0.0)))))
    return Compound(children=children, label="p3_v3_r2_A_seam_race_progressive_coupon")


def seam_printable_parts(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    male, female = make_stationary_joiner_parts(spec)
    return (
        make_seam_arc_half("lower", spec),
        make_seam_arc_half("upper", spec),
        *(make_guide_shoe_variant(c, i, spec) for i, c in enumerate(spec.guide_clearances)),
        male,
        female,
    )


@lru_cache(maxsize=1)
def _motor_arc_master():
    p = P3_V3_R2_PRINT_COUPON
    teeth = _ring_gear_teeth(p.pinion_face_range[1] - p.pinion_face_range[0], p.pinion_face_range[0], p)
    body = _annulus(131.6, 138.9, p.ring_thickness, p.motor_carrier_z0)
    race = _annulus(p.race_inner_radius, p.race_outer_radius, p.race_axial, p.motor_race_z0)
    return teeth.fuse(body).fuse(race)


def make_motor_arc(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    half = spec.motor_arc_angle_degrees / 2.0
    crop = _sector_prism(spec.ring_outer_radius + 1.0, -half, half, 1.6, 6.2)
    pieces = _motor_arc_master().intersect(crop)
    arc = max(pieces, key=lambda shape: shape.volume)
    # Two underside heat-set bosses match the removable fin foot.
    for y in (-spec.fin_hole_spacing / 2.0, spec.fin_hole_spacing / 2.0):
        boss = Cylinder(
            spec.fin_insert_boss_od / 2.0,
            spec.fin_insert_depth,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.fin_mount_radius, y, spec.motor_carrier_z0 - spec.fin_insert_depth)))
        bore = Cylinder(
            spec.fin_insert_bore / 2.0,
            spec.fin_insert_depth + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.fin_mount_radius, y, spec.motor_carrier_z0 - spec.fin_insert_depth - 0.2)))
        arc = arc.fuse(boss).cut(bore)
    arc.label = "p3_v3_r2_B_real_M1_260T_24T_motor_station_arc"
    arc.color = srgb("#3F8F87")
    return arc


def make_motor_mesh_pair_at_phase(
    ring_angle_degrees: float,
    spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON,
):
    """Canonical full ring and coupled station pinion for phase sampling."""

    ring = deepcopy(_motor_arc_master()).rotate(Axis.Z, ring_angle_degrees)
    pinion = make_output_pinion(0)
    pinion = pinion.rotate(
        Axis((spec.output_axis_radius, 0.0, 0.0), (0.0, 0.0, 1.0)),
        ring_angle_degrees * spec.gear_ratio,
    )
    return ring, pinion


def _shift_r1(part, spec: P3V3R2PrintCouponSpec):
    shifted = part.moved(Location((0.5, 0.0, 0.0)))
    shifted.label = part.label.replace("p3_v3_r1", "p3_v3_r2_coupon_B")
    return shifted


def make_motor_station_references(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    refs = [
        _shift_r1(r1_make_motor_body(), spec),
        _shift_r1(r1_make_motor_shaft(), spec),
        _shift_r1(r1_make_output_shaft(), spec),
        _shift_r1(r1_make_bearing("lower"), spec),
        _shift_r1(r1_make_bearing("upper"), spec),
    ]
    return tuple(refs)


def make_printable_drive_gears(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    """The actual printed 16:16 miter pair and M1 16T output pinion."""

    horizontal, vertical = r1_make_miter_pair()
    horizontal = _shift_r1(horizontal, spec)
    vertical = _shift_r1(vertical, spec)
    pinion = make_output_pinion(0)
    horizontal.label = "p3_v3_r2_B_PRINT_M1_16T_horizontal_miter"
    vertical.label = "p3_v3_r2_B_PRINT_M1_16T_vertical_miter"
    pinion.label = "p3_v3_r2_B_PRINT_M1_16T_output_pinion_D4p1"
    return horizontal, vertical, pinion


def make_bearing_housing(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    x = spec.output_axis_radius
    lower_z0 = spec.bearing_ranges[0][0] - spec.bearing_fixed_shoulder
    upper_z0 = spec.bearing_ranges[1][0] - spec.bearing_fixed_shoulder
    cup_od = 14.0
    housing = None
    for which, z0, bearing_range in (("lower", lower_z0, spec.bearing_ranges[0]), ("upper", spec.bearing_ranges[1][0] - 0.1, spec.bearing_ranges[1])):
        cup_height = spec.bearing_fixed_shoulder + spec.bearing_width if which == "lower" else spec.bearing_pocket_depth
        cup = Cylinder(cup_od / 2.0, cup_height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, 0.0, z0)))
        aperture = Cylinder(spec.bearing_aperture_diameter / 2.0, spec.bearing_fixed_shoulder + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, 0.0, z0 - 0.2)))
        pocket = Cylinder(spec.bearing_pocket_diameter / 2.0, spec.bearing_pocket_depth + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, 0.0, bearing_range[0] - 0.1)))
        cup = cup.cut(pocket)
        if which == "lower":
            cup = cup.cut(aperture)
        housing = cup if housing is None else housing.fuse(cup)
    # Twin 1.2 mm guide arms and pylon columns leave the miter envelope open.
    for sign in (-1.0, 1.0):
        y = sign * 10.5
        pylon = Box(12.0, spec.guide_arm_min_thickness, 22.2, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, lower_z0)))
        housing = housing.fuse(pylon)
        for z in (-22.0, -1.2):
            arm = Box(12.0, 5.0, spec.guide_arm_min_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, sign * 9.0, z)))
            housing = housing.fuse(arm)
        boss = Cylinder(spec.bearing_insert_boss_od / 2.0, 3.1, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, -3.1)))
        insert = Cylinder(spec.bearing_insert_bore / 2.0, spec.bearing_insert_depth + 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, -3.05)))
        housing = housing.fuse(boss).cut(insert)
    # A 3 mm mounting foot meets, but does not overlap, the motor saddle.
    foot = Box(14.0, 24.0, spec.motor_saddle_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, 0.0, -25.2)))
    housing = housing.fuse(foot)
    shaft_corridor = Cylinder(spec.bearing_aperture_diameter / 2.0, 27.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, 0.0, -25.4)))
    housing = housing.cut(shaft_corridor)
    horizontal, _ = r1_make_miter_pair()
    housing = housing.cut(_shift_r1(horizontal, spec))
    housing.label = "p3_v3_r2_B_two_MR84_18mm_span_bearing_housing"
    housing.color = srgb("#69737A")
    return housing


def make_bearing_cap(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    x = spec.output_axis_radius
    cap = _annulus(
        spec.bearing_aperture_diameter / 2.0,
        7.0,
        spec.bearing_cap_thickness,
        0.0,
    ).moved(Location((x, 0.0, 0.0)))
    for sign in (-1.0, 1.0):
        y = sign * 10.5
        ear = Box(10.0, 7.0, spec.bearing_cap_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, sign * 7.5, 0.0)))
        cap = cap.fuse(ear)
        hole = Cylinder(spec.bearing_cap_screw_clearance / 2.0, spec.bearing_cap_thickness + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, -0.2)))
        cap = cap.cut(hole)
    cap.label = "p3_v3_r2_B_MR84_removable_cap_D6p4_aperture"
    cap.color = srgb("#AEB5B9")
    return cap


def _slot_cutter(x: float, y: float, z0: float, diameter: float, travel: float, height: float):
    left = Cylinder(diameter / 2.0, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x - travel / 2.0, y, z0)))
    right = Cylinder(diameter / 2.0, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x + travel / 2.0, y, z0)))
    bridge = Box(travel, diameter, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, z0)))
    return left.fuse(right).fuse(bridge)


def make_motor_saddle(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    x0, x1 = spec.motor_saddle_x
    z0 = -22.15 - spec.motor_saddle_thickness
    saddle = Box(x1 - x0, 2.0 * spec.motor_saddle_half_width, spec.motor_saddle_thickness, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((x0, 0.0, z0)))
    for x in spec.motor_clamp_x:
        for y in spec.motor_clamp_y:
            slot = _slot_cutter(x, y, z0 - 0.2, spec.motor_clamp_clearance, spec.motor_slot_total_travel, spec.motor_saddle_thickness + 0.4)
            saddle = saddle.cut(slot)
            # Captive nut pocket follows the same +/-0.5 radial travel.
            for dx in (-spec.motor_adjustment, spec.motor_adjustment):
                saddle = saddle.cut(_hex_prism(spec.motor_clamp_nut_af, spec.motor_clamp_nut_depth, z0, x + dx, y))
    saddle.label = "p3_v3_r2_B_NEMA8_3mm_saddle_four_M3_slotted_clamps"
    saddle.color = srgb("#59646B")
    return saddle


def make_motor_clamp_straps(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    """Two printable bars that clamp the horizontal NEMA8 body to the saddle."""

    straps = []
    for index, x in enumerate(spec.motor_clamp_x):
        strap = Box(
            spec.motor_clamp_strap_radial,
            spec.motor_clamp_strap_tangential,
            spec.motor_clamp_strap_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, 0.0, spec.motor_clamp_strap_z0)))
        for y in spec.motor_clamp_y:
            strap = strap.cut(
                Cylinder(
                    spec.motor_clamp_clearance / 2.0,
                    spec.motor_clamp_strap_thickness + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                ).moved(Location((x, y, spec.motor_clamp_strap_z0 - 0.2)))
            )
        strap.label = f"p3_v3_r2_B_NEMA8_M3_clamp_strap_{index + 1}"
        strap.color = srgb("#87939A")
        straps.append(strap)
    return tuple(straps)


def make_fit_gauge(diameter: float, index: int, spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    if diameter not in spec.fit_gauge_diameters:
        raise ValueError("fit gauge diameter is not frozen")
    gauge = _annulus(diameter / 2.0, diameter / 2.0 + spec.fit_gauge_wall, spec.fit_gauge_height, 0.0)
    gauge = gauge.moved(Location((90.0 + 14.0 * index, -35.0, 0.0)))
    gauge.label = f"p3_v3_r2_B_MR84_fit_gauge_D{diameter:.2f}"
    gauge.color = srgb("#D39B55")
    return gauge


def make_operating_guide_shoe(material: str, angle: float, spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    if material not in {"PETG", "TPU95A"}:
        raise ValueError("shoe material must be PETG or TPU95A")
    c = spec.operating_guide_clearance
    # Open inner side avoids the carrier body; floor and outer wall establish
    # the requested axial and radial clearances to the 2 x 0.8 race.
    floor = Box(3.45, 10.0, spec.guide_arm_min_thickness, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((137.75, 0.0, 0.55)))
    outer_wall = Box(0.95, 10.0, 2.65, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((140.0 + c, 0.0, 0.55)))
    arm = Box(8.0, spec.guide_arm_min_thickness, 2.65, align=(Align.MAX, Align.CENTER, Align.MIN)).moved(Location((137.85, 0.0, -2.0)))
    shoe = floor.fuse(outer_wall).fuse(arm).rotate(Axis.Z, angle)
    shoe.label = f"p3_v3_r2_B_{material}_guide_shoe_0p25_clearance"
    shoe.color = srgb("#4E7D72" if material == "PETG" else "#8F63A8")
    return shoe


def _rounded_foot(spec: P3V3R2PrintCouponSpec):
    # Constructive rounded rectangle avoids topology-sensitive post fillets.
    r = spec.fin_foot_corner_radius
    radial = spec.fin_foot_radial
    tangent = spec.fin_foot_tangential
    center_x = spec.fin_mount_radius
    core_x = Box(radial - 2.0 * r, tangent, spec.fin_foot_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((center_x, 0.0, 5.8)))
    core_y = Box(radial, tangent - 2.0 * r, spec.fin_foot_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((center_x, 0.0, 5.8)))
    foot = core_x.fuse(core_y)
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            corner = Cylinder(r, spec.fin_foot_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((center_x + sx * (radial / 2.0 - r), sy * (tangent / 2.0 - r), 5.8)))
            foot = foot.fuse(corner)
    return foot


def make_fin(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    foot = _rounded_foot(spec)
    for y in (-spec.fin_hole_spacing / 2.0, spec.fin_hole_spacing / 2.0):
        foot = foot.cut(Cylinder(spec.fin_hole_diameter / 2.0, spec.fin_foot_thickness + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((spec.fin_mount_radius, y, 5.6))))
    blade = Box(spec.fin_blade_radial, spec.fin_blade_tangential, spec.fin_blade_height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((spec.fin_mount_radius, 0.0, 7.8)))
    fin = foot.fuse(blade)
    fin.label = "p3_v3_r2_B_fin_6x14x2_R1_15mm_blade"
    fin.color = srgb("#D95D78")
    return fin


def motor_printable_parts(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    return (
        make_motor_arc(spec),
        make_bearing_housing(spec),
        make_bearing_cap(spec),
        make_motor_saddle(spec),
        *make_motor_clamp_straps(spec),
        *make_printable_drive_gears(spec),
        make_fit_gauge(spec.fit_gauge_diameters[0], 0, spec),
        make_fit_gauge(spec.fit_gauge_diameters[1], 1, spec),
        make_operating_guide_shoe("PETG", -12.0, spec),
        make_operating_guide_shoe("TPU95A", 12.0, spec),
        make_fin(spec),
    )


def make_motor_station_coupon_assembly(spec: P3V3R2PrintCouponSpec = P3_V3_R2_PRINT_COUPON):
    return Compound(
        children=[*motor_printable_parts(spec), *make_motor_station_references(spec)],
        label="p3_v3_r2_B_24T_horizontal_NEMA8_motor_station_coupon",
    )


PRIMARY_FACTORIES = (
    ("seam_race_coupon", make_seam_coupon_assembly),
    ("motor_station_coupon", make_motor_station_coupon_assembly),
)


PRINTABLE_GROUPS = (
    ("A_seam_race", seam_printable_parts),
    ("B_motor_station", motor_printable_parts),
)
