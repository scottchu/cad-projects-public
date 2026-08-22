"""STEP-first build123d geometry for the P2R3 Module-B r135 coupon."""

from __future__ import annotations

from math import ceil, cos, degrees, radians, sin

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Compound,
    Cylinder,
    Face,
    Location,
    Plane,
    Polygon,
    Vector,
    Wire,
    extrude,
    loft,
)

from p2r3_module_b_rail_coupon_spec import P2R3ModuleBRailCouponSpec, P2R3_MODULE_B


def _polar(radius: float, angle_deg: float) -> tuple[float, float]:
    a = radians(angle_deg)
    return radius * cos(a), radius * sin(a)


def _cylinder(radius: float, height: float, z0: float = 0.0):
    return Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0))
    )


def _sector_face(
    inner_radius: float,
    outer_radius: float,
    angle_start_deg: float,
    angle_end_deg: float,
    z: float,
):
    segments = max(12, ceil(abs(angle_end_deg - angle_start_deg) * 2.0))
    angles = [
        angle_start_deg + (angle_end_deg - angle_start_deg) * i / segments
        for i in range(segments + 1)
    ]
    points = [Vector(*_polar(outer_radius, angle), z) for angle in angles]
    points.extend(Vector(*_polar(inner_radius, angle), z) for angle in reversed(angles))
    return Face(Wire.make_polygon(points, close=True))


def _sector(
    inner_radius: float,
    outer_radius: float,
    angle_start_deg: float,
    angle_end_deg: float,
    height: float,
    z0: float = 0.0,
):
    face = _sector_face(inner_radius, outer_radius, angle_start_deg, angle_end_deg, 0.0)
    return extrude(face, amount=height).moved(Location((0.0, 0.0, z0)))


def _centered_sector(
    radius: float,
    radial_width: float,
    arc_length: float,
    height: float,
    z0: float,
    angle_deg: float = 0.0,
):
    half_angle = degrees(arc_length / radius) / 2.0
    return _sector(
        radius - radial_width / 2.0,
        radius + radial_width / 2.0,
        angle_deg - half_angle,
        angle_deg + half_angle,
        height,
        z0,
    )


def _fuse_all(shapes):
    iterator = iter(shapes)
    result = next(iterator)
    for shape in iterator:
        result = result.fuse(shape)
    return result


def _cavity_tool(
    angle_start_deg: float,
    angle_end_deg: float,
    spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B,
):
    overshoot = 0.15
    start = angle_start_deg - overshoot
    end = angle_end_deg + overshoot
    constant = _sector(
        spec.radius - spec.cavity_radial_width / 2.0,
        spec.radius + spec.cavity_radial_width / 2.0,
        start,
        end,
        spec.constant_cavity_top_z - spec.rear_web_top_z,
        spec.rear_web_top_z,
    )
    lower = _sector_face(
        spec.radius - spec.cavity_radial_width / 2.0,
        spec.radius + spec.cavity_radial_width / 2.0,
        start,
        end,
        spec.constant_cavity_top_z - 0.02,
    )
    upper = _sector_face(
        spec.radius - spec.throat_radial_width / 2.0,
        spec.radius + spec.throat_radial_width / 2.0,
        start,
        end,
        spec.throat_z + 0.20,
    )
    transition = loft([lower, upper], ruled=True)
    return constant.fuse(transition)


def _rail_segment(
    inner_radius: float,
    outer_radius: float,
    angle_start_deg: float,
    angle_end_deg: float,
    spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B,
):
    body = _sector(
        inner_radius,
        outer_radius,
        angle_start_deg,
        angle_end_deg,
        spec.throat_z,
        spec.rail_rear_z,
    )
    return body.cut(_cavity_tool(angle_start_deg, angle_end_deg, spec))


def make_main_rail_coupon(spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B):
    """One-piece 110-degree rail with a central loading window and pilot ears."""
    rail = _rail_segment(
        spec.stationary_inner_radius,
        spec.stationary_outer_radius,
        spec.rail_angle_start_deg,
        spec.rail_angle_end_deg,
        spec,
    )

    # 0.02 mm radial and 0.02 degree kernel overshoot prevents faceted boolean
    # residue while retaining the frozen nominal r128..142 / 12-degree window.
    gate_cut = _sector(
        spec.gate_cut_inner - 0.02,
        spec.gate_cut_outer + 0.02,
        -spec.gate_nominal_angle_deg / 2.0 - 0.02,
        spec.gate_nominal_angle_deg / 2.0 + 0.02,
        spec.throat_z + 0.4,
        -0.2,
    )
    rail = rail.cut(gate_cut)

    # Bands outside the r128..142 loading window keep both rail halves one
    # printable solid.  Their top is lowered by one 0.2 mm layer so the gate
    # tabs seat without positive-volume overlap.
    inner_ear = _sector(
        spec.ear_inner_radius,
        spec.gate_cut_inner,
        -spec.ear_half_angle_deg,
        spec.ear_half_angle_deg,
        spec.main_ear_top_z,
        0.0,
    )
    outer_ear = _sector(
        spec.gate_cut_outer,
        spec.ear_outer_radius,
        -spec.ear_half_angle_deg,
        spec.ear_half_angle_deg,
        spec.main_ear_top_z,
        0.0,
    )
    rail = _fuse_all([rail, inner_ear, outer_ear])

    # Lower the two gate-tab seats to Z7.4.  The tabs begin at Z7.6, leaving
    # the frozen 0.2 mm assembled seam without changing the groove profile.
    half_part_angle = spec.gate_part_angle_span_deg / 2.0
    seat_tools = []
    for inner, outer in (spec.gate_tab_inner_span, spec.gate_tab_outer_span):
        seat_tools.append(
            _sector(
                inner - 0.10,
                outer + 0.10,
                -half_part_angle - 0.10,
                half_part_angle + 0.10,
                spec.throat_z - spec.main_ear_top_z + 0.4,
                spec.main_ear_top_z,
            )
        )
    rail = rail.cut(_fuse_all(seat_tools))

    pilot_z0 = spec.main_ear_top_z - spec.m2_pilot_depth
    for radius in spec.m2_radii:
        x, y = _polar(radius, 0.0)
        pilot = _cylinder(
            spec.m2_pilot_diameter / 2.0,
            spec.m2_pilot_depth + 0.2,
            pilot_z0,
        ).moved(Location((x, y, 0.0)))
        rail = rail.cut(pilot)

    rail.label = "p2r3_module_b_main_r135_110deg_integral_c_slot"
    return rail


def make_removable_gate(spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B):
    """12-degree exact-profile gate with two external M2 mounting ears."""
    half_part_angle = spec.gate_part_angle_span_deg / 2.0
    gate = _rail_segment(
        spec.gate_radial_inner,
        spec.gate_radial_outer,
        -half_part_angle,
        half_part_angle,
        spec,
    )

    inner_start, inner_end = spec.gate_tab_inner_span
    outer_start, outer_end = spec.gate_tab_outer_span
    tab_height = spec.gate_tab_front_z - spec.gate_tab_rear_z
    inner_tab = _sector(
        inner_start,
        inner_end,
        -half_part_angle,
        half_part_angle,
        tab_height,
        spec.gate_tab_rear_z,
    )
    outer_tab = _sector(
        outer_start,
        outer_end,
        -half_part_angle,
        half_part_angle,
        tab_height,
        spec.gate_tab_rear_z,
    )
    gate = _fuse_all([gate, inner_tab, outer_tab])

    for radius in spec.m2_radii:
        x, y = _polar(radius, 0.0)
        clearance = _cylinder(
            spec.m2_clearance_diameter / 2.0,
            tab_height + 0.4,
            spec.gate_tab_rear_z - 0.2,
        ).moved(Location((x, y, 0.0)))
        gate = gate.cut(clearance)

    gate.label = "p2r3_module_b_removable_12deg_exact_profile_m2_gate"
    return gate


def _make_pointed_fin(spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B):
    x0 = spec.radius - spec.fin_radial / 2.0
    points = (
        (x0, spec.fin_root_z),
        (x0 + spec.fin_radial, spec.fin_root_z),
        (spec.radius, spec.fin_root_z + spec.fin_height),
    )
    plane = Plane(
        origin=(0.0, -spec.fin_tangential / 2.0, 0.0),
        x_dir=(1.0, 0.0, 0.0),
        z_dir=(0.0, -1.0, 0.0),
    )
    with BuildPart() as part:
        with BuildSketch(plane):
            Polygon(*points)
        extrude(amount=spec.fin_tangential)
    return part.part


def make_second_follower_fin(spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B):
    """P2R2-sized second follower with breakout membrane and pointed fin."""
    shoe = _centered_sector(
        spec.radius,
        spec.follower_shoe_radial,
        spec.follower_shoe_arc_length,
        spec.follower_shoe_front_z - spec.follower_shoe_rear_z,
        spec.follower_shoe_rear_z,
    )
    necks = []
    for offset in spec.yaw_land_center_offsets:
        necks.append(
            _centered_sector(
                spec.radius,
                spec.follower_neck_radial,
                spec.yaw_land_arc_length,
                spec.follower_neck_front_z - spec.follower_neck_rear_z,
                spec.follower_neck_rear_z,
                degrees(offset / spec.radius),
            )
        )
    bridge = _centered_sector(
        spec.radius,
        spec.bridge_radial,
        spec.bridge_arc_length,
        spec.bridge_front_z - spec.bridge_rear_z,
        spec.bridge_rear_z,
    )
    follower = _fuse_all([shoe, *necks, bridge, _make_pointed_fin(spec)])

    # The 0.2 mm disk at the rear mouth remains printable.  Punching it out
    # restores the full 3.10 mm installation depth; the modeled void is 2.90.
    x, y = _polar(spec.radius, 0.0)
    pocket = _cylinder(
        spec.magnet_pocket_diameter / 2.0,
        spec.pocket_void_depth_before_breakout,
        spec.pocket_void_rear_z,
    ).moved(Location((x, y, 0.0)))
    follower = follower.cut(pocket)
    follower.label = "p2r3_module_b_second_follower_breakout_membrane_pointed_fin"
    return follower


def placed_follower(
    angle_deg: float,
    z_offset: float = 0.0,
    spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B,
):
    return make_second_follower_fin(spec).rotate(Axis.Z, angle_deg).moved(
        Location((0.0, 0.0, z_offset))
    )


def make_installed_coupon(
    follower_angle_deg: float = 25.0,
    spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B,
):
    main = make_main_rail_coupon(spec)
    gate = make_removable_gate(spec)
    follower = placed_follower(follower_angle_deg, 0.0, spec)
    return Compound(
        children=[main, gate, follower],
        label="p2r3_module_b_r135_installed_three_part_coupon",
    )


def make_exploded_coupon(spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B):
    main = make_main_rail_coupon(spec)
    gate = make_removable_gate(spec).moved(Location((0.0, 0.0, 22.0)))
    follower = placed_follower(0.0, 35.0, spec)
    return Compound(
        children=[main, gate, follower],
        label="p2r3_module_b_r135_service_exploded_plus_z",
    )


def make_radial_z_section(spec: P2R3ModuleBRailCouponSpec = P2R3_MODULE_B):
    """True radial-Z cut through the gate, follower shoe, and blind pocket."""
    slab = Box(
        70.0,
        0.60,
        65.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((spec.radius, 0.0, 0.0)))
    section_solids = []
    for name, shape in (
        ("main", make_main_rail_coupon(spec)),
        ("gate", make_removable_gate(spec)),
        ("follower", placed_follower(0.0, 0.0, spec)),
    ):
        intersections = shape.intersect(slab)
        for index, solid in enumerate(intersections.solids(), 1):
            solid.label = f"p2r3_module_b_radial_z_{name}_{index}"
            section_solids.append(solid)
    return Compound(
        children=section_solids,
        label="p2r3_module_b_true_radial_z_c_slot_and_pocket_section",
    )


def pairwise_intersection_volume(left, right) -> float:
    intersection = left.intersect(right)
    if intersection is None:
        return 0.0
    return sum(abs(solid.volume) for solid in intersection.solids())


PRINTABLE_FACTORIES = (
    ("main_rail_coupon", make_main_rail_coupon),
    ("second_follower_fin", make_second_follower_fin),
    ("removable_gate", make_removable_gate),
)
