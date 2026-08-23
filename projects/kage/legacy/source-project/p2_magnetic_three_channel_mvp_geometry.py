"""STEP-first build123d geometry for the isolated KAGE P2 magnetic MVP."""

from __future__ import annotations

from math import cos, degrees, pi, radians, sin

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Compound,
    Cylinder,
    Location,
    Plane,
    Polygon,
    extrude,
)

from p2_magnetic_three_channel_mvp_spec import ChannelSpec, MagneticThreeChannelMvpSpec, P2


def _cylinder(radius: float, height: float, z0: float = 0.0):
    return Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, z0))
    )


def _annulus(inner_radius: float, outer_radius: float, height: float, z0: float = 0.0):
    return _cylinder(outer_radius, height, z0).cut(
        _cylinder(inner_radius, height + 0.4, z0 - 0.2)
    )


def _box(x: float, y: float, z: float, at=(0.0, 0.0, 0.0)):
    return Box(x, y, z, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location(at))


def _polar_xy(radius: float, angle_deg: float) -> tuple[float, float]:
    angle = radians(angle_deg)
    return radius * cos(angle), radius * sin(angle)


def _fuse_all(shapes):
    iterator = iter(shapes)
    result = next(iterator)
    for shape in iterator:
        result = result.fuse(shape)
    return result


def _annular_sector(
    radius: float,
    radial_width: float,
    arc_length: float,
    height: float,
    z0: float,
    angle_deg: float = 0.0,
    segments: int = 48,
):
    """Create a curved annular shoe centered at ``angle_deg``."""
    inner = radius - radial_width / 2
    outer = radius + radial_width / 2
    half_angle = degrees(arc_length / radius) / 2
    angles_outer = [angle_deg - half_angle + 2 * half_angle * i / segments for i in range(segments + 1)]
    angles_inner = list(reversed(angles_outer))
    points = [
        (outer * cos(radians(angle)), outer * sin(radians(angle))) for angle in angles_outer
    ]
    points.extend(
        (inner * cos(radians(angle)), inner * sin(radians(angle))) for angle in angles_inner
    )
    with BuildPart() as part:
        with BuildSketch(Plane.XY):
            Polygon(*points)
        extrude(amount=height)
    return part.part.moved(Location((0, 0, z0)))


def make_separator(
    thickness: float,
    spec: MagneticThreeChannelMvpSpec = P2,
):
    if thickness not in spec.separator_options:
        raise ValueError(f"unsupported separator thickness: {thickness}")
    z0 = spec.separator_rear_z
    plate = _annulus(spec.center_open_radius, spec.plate_outer_radius, thickness, z0)
    m3_tool = _cylinder(spec.m3_clearance_diameter / 2, thickness + 0.4, z0 - 0.2)
    for angle in spec.cap_fastener_angles[3]:
        x, y = _polar_xy(spec.stationary_hole_radius, angle)
        plate = plate.cut(m3_tool.moved(Location((x, y, 0))))
    bosses = []
    for radius, angles in zip(spec.cap_fastener_radii[:3], spec.cap_fastener_angles[:3]):
        for angle in angles:
            x, y = _polar_xy(radius, angle)
            boss = _cylinder(spec.separator_boss_diameter / 2, spec.separator_boss_height, z0 + thickness).moved(
                Location((x, y, 0))
            )
            pilot = _cylinder(
                spec.separator_pilot_diameter / 2,
                spec.separator_pilot_depth,
                z0 + thickness + spec.separator_boss_height - spec.separator_pilot_depth,
            ).moved(Location((x, y, 0)))
            bosses.append(boss.cut(pilot))
    result = _fuse_all([plate, *bosses])
    result.label = f"p2_separator_t{str(thickness).replace('.', 'p')}_with_9_integral_m2_bosses"
    return result


def make_front_cap_ring(
    index: int,
    spec: MagneticThreeChannelMvpSpec = P2,
):
    inner, outer = spec.cap_spans[index]
    cap = _annulus(inner, outer, spec.cap_thickness)
    radius = spec.cap_fastener_radii[index]
    angles = spec.cap_fastener_angles[index]
    if index < 3:
        through_diameter = spec.m2_clearance_diameter
        counterbore_diameter = spec.m2_counterbore_diameter
        counterbore_depth = spec.m2_counterbore_depth
    else:
        through_diameter = spec.m3_clearance_diameter
        # MVP R3 deliberately uses protruding external M3 heads/washers; the
        # 1.8 mm cap has no counterbore and makes no flush-head claim.
        counterbore_diameter = through_diameter
        counterbore_depth = 0.0
    for angle in angles:
        x, y = _polar_xy(radius, angle)
        through = _cylinder(through_diameter / 2, spec.cap_thickness + 0.4, -0.2).moved(
            Location((x, y, 0))
        )
        cap = cap.cut(through)
        if counterbore_depth:
            counterbore = _cylinder(
                counterbore_diameter / 2,
                counterbore_depth + 0.1,
                spec.cap_thickness - counterbore_depth,
            ).moved(Location((x, y, 0)))
            cap = cap.cut(counterbore)
    cap.label = f"p2_front_cap_ring_r{index}_{len(angles)}_fasteners"
    return cap


def _make_fin(channel: ChannelSpec, z0: float):
    radial = channel.fin_radial
    tangential = channel.fin_tangential
    height = channel.fin_height
    x0 = channel.radius - radial / 2
    if channel.fin_top == "rounded":
        stem = _box(radial, tangential, height - radial / 2, (channel.radius, 0, z0))
        crown = Cylinder(radial / 2, tangential, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(
            Axis.X, 90
        ).moved(Location((channel.radius, 0, z0 + height - radial / 2)))
        return stem.fuse(crown)
    if channel.fin_top == "chamfered":
        bevel_h = 3.0
        points = (
            (x0, z0),
            (x0 + radial, z0),
            (x0 + radial - bevel_h, z0 + height),
            (x0 + bevel_h, z0 + height),
        )
    else:
        points = (
            (x0, z0),
            (x0 + radial, z0),
            (channel.radius, z0 + height),
        )
    plane = Plane(origin=(0, -tangential / 2, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    with BuildPart() as part:
        with BuildSketch(plane):
            Polygon(*points)
        extrude(amount=tangential)
    return part.part


def make_follower(
    channel_name: str,
    separator_thickness: float,
    spec: MagneticThreeChannelMvpSpec = P2,
):
    """Visible captured follower at angle zero, in assembled world Z."""
    if separator_thickness not in spec.separator_options:
        raise ValueError(f"unsupported separator thickness: {separator_thickness}")
    channel = spec.by_name[channel_name]
    separator_front = spec.separator_rear_z + separator_thickness
    shoe_z = separator_front + 0.30
    shoe = _annular_sector(
        channel.radius,
        spec.shoe_radial,
        spec.shoe_arc_length,
        spec.shoe_thickness,
        shoe_z,
    )
    pocket = _cylinder(
        spec.magnet_pocket_diameter / 2,
        spec.magnet_pocket_depth,
        separator_front + 0.30,
    ).moved(Location((channel.radius, 0, 0)))
    shoe = shoe.cut(pocket)

    # Two separated lands at the arc ends resist yaw in the 4.8 mm slot.
    neck_height = 2.10
    land_arc = 5.0
    land_offset = degrees(5.0 / channel.radius)
    necks = [
        _annular_sector(
            channel.radius,
            spec.neck_radial,
            land_arc,
            neck_height,
            separator_front + 3.70,
            angle_deg=angle,
            segments=16,
        )
        for angle in (-land_offset, land_offset)
    ]
    bridge = _annular_sector(
        channel.radius,
        spec.shoe_radial,
        spec.shoe_arc_length,
        1.0,
        separator_front + 5.80,
    )
    fin = _make_fin(channel, separator_front + 5.80)
    result = _fuse_all([shoe, *necks, bridge, fin])
    result.label = f"p2_follower_{channel.name}_captured_shoe_two_yaw_lands_{channel.fin_top}_fin"
    return result


def make_hidden_driver(
    channel_name: str,
    spec: MagneticThreeChannelMvpSpec = P2,
):
    channel = spec.by_name[channel_name]
    z0, z1 = spec.driver_z
    # A 0.05 mm internal overlap removes tangent-only ring/boss and ring/paddle
    # seams from the printable mesh without changing any exterior fit datum.
    join_overlap = 0.05
    ring = _annulus(
        channel.radius - spec.driver_ring_radial_width / 2,
        channel.radius + spec.driver_ring_radial_width / 2,
        z1 - z0,
        z0,
    )
    boss = _cylinder(spec.magnet_boss_diameter / 2, spec.driver_boss_top_z - z0, z0).moved(
        Location((channel.radius - join_overlap, 0, 0))
    )
    pocket = _cylinder(
        spec.magnet_pocket_diameter / 2,
        spec.magnet_pocket_depth,
        spec.driver_boss_top_z - spec.magnet_pocket_depth,
    ).moved(
        Location((channel.radius - join_overlap, 0, 0))
    )
    boss = boss.cut(pocket)
    paddle_center_radius = channel.radius + spec.driver_ring_radial_width / 2 + spec.paddle_radial / 2
    paddle = _box(
        spec.paddle_radial,
        spec.paddle_tangential,
        z1 - z0,
        (paddle_center_radius - join_overlap, 0, z0),
    )
    result = _fuse_all([ring, boss, paddle])
    result.label = f"p2_hidden_driver_{channel.name}_ring_manual_{channel.name[0].upper()}_tab"
    return result


def placed_hidden_driver(
    channel_name: str,
    angle_deg: float,
    spec: MagneticThreeChannelMvpSpec = P2,
):
    return make_hidden_driver(channel_name, spec).rotate(Axis.Z, angle_deg)


def placed_follower(
    channel_name: str,
    separator_thickness: float,
    angle_deg: float,
    spec: MagneticThreeChannelMvpSpec = P2,
):
    return make_follower(channel_name, separator_thickness, spec).rotate(Axis.Z, angle_deg)


def make_rear_base(spec: MagneticThreeChannelMvpSpec = P2):
    """One skeletal open-back cassette with six base-integral M3 spacers."""
    outer = _annulus(*spec.base_outer_ring_span, spec.rear_base_z[1] - spec.rear_base_z[0], spec.rear_base_z[0])
    parts = [outer]
    for angle in spec.backbone_angles:
        backbone = _box(78, spec.backbone_width, 1.2, (65, 0, 0)).rotate(Axis.Z, angle)
        parts.append(backbone)
    pad_phases = ((0, 120, 240), (20, 140, 260), (40, 160, 280))
    for channel, angles in zip(spec.channels, pad_phases):
        arc_length = radians(spec.pad_arc_degrees) * channel.radius
        for angle in angles:
            parts.append(
                _annular_sector(channel.radius, spec.pad_radial_width, arc_length, 1.1, 1.2, angle, segments=24)
            )
            connector_length = 98 - (channel.radius + spec.pad_radial_width / 2) + 0.1
            connector_center = channel.radius + spec.pad_radial_width / 2 - 0.05 + connector_length / 2
            parts.append(
                _box(connector_length, spec.pad_connector_width, 1.2, (connector_center, 0, 0)).rotate(Axis.Z, angle)
            )
    spacer_z0, spacer_z1 = spec.stationary_spacer_z
    for angle in spec.cap_fastener_angles[3]:
        x, y = _polar_xy(spec.stationary_hole_radius, angle)
        parts.append(
            _cylinder(
                spec.stationary_spacer_diameter / 2,
                spacer_z1 - spacer_z0,
                spacer_z0,
            ).moved(Location((x, y, 0)))
        )
    result = _fuse_all(parts)
    # One continuous M3 clearance path passes through each spacer and the base
    # ring.  The extra 0.2 mm at both ends avoids coincident boolean faces.
    through_tool = _cylinder(
        spec.m3_clearance_diameter / 2,
        spacer_z1 - spec.rear_base_z[0] + 0.4,
        spec.rear_base_z[0] - 0.2,
    )
    for angle in spec.cap_fastener_angles[3]:
        x, y = _polar_xy(spec.stationary_hole_radius, angle)
        result = result.cut(through_tool.moved(Location((x, y, 0))))
    result.label = "p2_rear_base_open_back_9_wear_pads_6_integral_m3_spacer_columns"
    return result


DEFAULT_ANGLES = {"hour": 25.0, "minute": 145.0, "second": 275.0}


def _placed_cap(index: int, thickness: float, spec: MagneticThreeChannelMvpSpec):
    return make_front_cap_ring(index, spec).moved(
        Location((0, 0, spec.separator_rear_z + thickness + 4.0))
    )


def make_assembled(
    separator_thickness: float = 1.5,
    angles: dict[str, float] | None = None,
    spec: MagneticThreeChannelMvpSpec = P2,
):
    angles = DEFAULT_ANGLES if angles is None else angles
    children = [make_rear_base(spec)]
    for channel_name in ("second", "minute", "hour"):
        children.append(placed_hidden_driver(channel_name, angles[channel_name], spec))
    children.append(make_separator(separator_thickness, spec))
    for channel_name in ("hour", "minute", "second"):
        children.append(placed_follower(channel_name, separator_thickness, angles[channel_name], spec))
    children.extend(_placed_cap(index, separator_thickness, spec) for index in range(4))
    assembly = Compound(
        children=children,
        label=f"p2_magnetic_three_channel_mvp_assembled_t{str(separator_thickness).replace('.', 'p')}",
    )
    return assembly


def make_service_exploded(spec: MagneticThreeChannelMvpSpec = P2):
    t = 1.5
    children = [make_rear_base(spec)]
    for index, channel_name in enumerate(("second", "minute", "hour")):
        children.append(placed_hidden_driver(channel_name, 0, spec).moved(Location((0, 0, -6.0 * index))))
    children.append(make_separator(t, spec).moved(Location((0, 0, 10))))
    for index, channel_name in enumerate(("hour", "minute", "second")):
        children.append(make_follower(channel_name, t, spec).moved(Location((0, 0, 20 + 8 * index))))
    for index in range(4):
        children.append(_placed_cap(index, t, spec).moved(Location((0, 0, 54 + 5 * index))))
    return Compound(children=children, label="p2_magnetic_three_channel_mvp_service_exploded_plus_z")


PRINTABLE_FACTORIES = (
    ("rear_base", make_rear_base),
    ("hidden_driver_hour", lambda: make_hidden_driver("hour")),
    ("hidden_driver_minute", lambda: make_hidden_driver("minute")),
    ("hidden_driver_second", lambda: make_hidden_driver("second")),
    ("separator_t1p0", lambda: make_separator(1.0)),
    ("separator_t1p5", lambda: make_separator(1.5)),
    ("separator_t2p0", lambda: make_separator(2.0)),
    ("front_cap_ring_r0", lambda: make_front_cap_ring(0)),
    ("front_cap_ring_r1", lambda: make_front_cap_ring(1)),
    ("front_cap_ring_r2", lambda: make_front_cap_ring(2)),
    ("front_cap_ring_r3", lambda: make_front_cap_ring(3)),
    ("follower_hour_fin_t1p5", lambda: make_follower("hour", 1.5)),
    ("follower_minute_fin_t1p5", lambda: make_follower("minute", 1.5)),
    ("follower_second_fin_t1p5", lambda: make_follower("second", 1.5)),
)


def make_magnet_reference(
    radius: float,
    z0: float,
    label: str,
    spec: MagneticThreeChannelMvpSpec = P2,
):
    magnet = _cylinder(spec.magnet_diameter / 2, spec.magnet_thickness, z0).moved(
        Location((radius, 0, 0))
    )
    magnet.label = label
    return magnet


def pairwise_intersection_volume(a, b) -> float:
    """Robust sum of pairwise solid intersections; never intersect compounds."""
    total = 0.0
    for solid_a in a.solids():
            for solid_b in b.solids():
                overlap = solid_a.intersect(solid_b)
                if overlap is None:
                    continue
                total += sum(max(0.0, solid.volume) for solid in overlap.solids())
    return total
