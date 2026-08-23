"""STEP-first geometry for the isolated 300 mm KAGE magnetic MVP."""

from __future__ import annotations

from math import radians

from build123d import Axis, Compound, Location

from p2r1_magnetic_three_channel_outboard_fins_geometry import (
    _annular_sector,
    _annulus,
    _box,
    _cylinder,
    _fuse_all,
    _polar_xy,
    make_follower as _make_follower,
    make_hidden_driver as _make_hidden_driver,
    pairwise_intersection_volume,
)
from p2r2_magnetic_three_channel_300mm_spec import MagneticThreeChannel300Spec, P2R2


def make_separator(thickness: float, spec: MagneticThreeChannel300Spec = P2R2):
    if thickness not in spec.separator_options:
        raise ValueError(f"unsupported separator thickness: {thickness}")
    z0 = spec.separator_rear_z
    plate = _annulus(spec.center_open_radius, spec.plate_outer_radius, thickness, z0)
    for radius, angle in spec.cap_fastener_sites[3]:
        x, y = _polar_xy(radius, angle)
        tool = _cylinder(spec.m3_clearance_diameter / 2, thickness + 0.4, z0 - 0.2)
        plate = plate.cut(tool.moved(Location((x, y, 0))))

    bosses = []
    for sites in spec.cap_fastener_sites[:3]:
        for radius, angle in sites:
            x, y = _polar_xy(radius, angle)
            boss = _cylinder(
                spec.separator_boss_diameter / 2,
                spec.separator_boss_height,
                z0 + thickness,
            ).moved(Location((x, y, 0)))
            pilot = _cylinder(
                spec.separator_pilot_diameter / 2,
                spec.separator_pilot_depth,
                z0 + thickness + spec.separator_boss_height - spec.separator_pilot_depth,
            ).moved(Location((x, y, 0)))
            bosses.append(boss.cut(pilot))
    result = _fuse_all([plate, *bosses])
    result.label = f"p2r2_separator_t{str(thickness).replace('.', 'p')}_with_12_integral_m2_bosses"
    return result


def make_front_cap_ring(index: int, spec: MagneticThreeChannel300Spec = P2R2):
    inner, outer = spec.cap_spans[index]
    cap = _annulus(inner, outer, spec.cap_thickness)
    for radius, angle in spec.cap_fastener_sites[index]:
        x, y = _polar_xy(radius, angle)
        if index < 3:
            through_d = spec.m2_clearance_diameter
            cbore_d = spec.m2_counterbore_diameter
            cbore_depth = spec.m2_counterbore_depth
        else:
            through_d = spec.m3_clearance_diameter
            cbore_d = through_d
            cbore_depth = 0.0
        through = _cylinder(through_d / 2, spec.cap_thickness + 0.4, -0.2).moved(
            Location((x, y, 0))
        )
        cap = cap.cut(through)
        if cbore_depth:
            cbore = _cylinder(
                cbore_d / 2,
                cbore_depth + 0.1,
                spec.cap_thickness - cbore_depth,
            ).moved(Location((x, y, 0)))
            cap = cap.cut(cbore)
    cap.label = f"p2r2_front_cap_ring_r{index}_{len(spec.cap_fastener_sites[index])}_fasteners"
    return cap


def make_follower(channel_name: str, separator_thickness: float, spec: MagneticThreeChannel300Spec = P2R2):
    result = _make_follower(channel_name, separator_thickness, spec)
    result.label = result.label.replace("p2r1_", "p2r2_")
    return result


def make_hidden_driver(channel_name: str, spec: MagneticThreeChannel300Spec = P2R2):
    result = _make_hidden_driver(channel_name, spec)
    result.label = result.label.replace("p2r1_", "p2r2_")
    return result


def placed_hidden_driver(channel_name: str, angle_deg: float, spec: MagneticThreeChannel300Spec = P2R2):
    return make_hidden_driver(channel_name, spec).rotate(Axis.Z, angle_deg)


def placed_follower(
    channel_name: str,
    separator_thickness: float,
    angle_deg: float,
    spec: MagneticThreeChannel300Spec = P2R2,
):
    return make_follower(channel_name, separator_thickness, spec).rotate(Axis.Z, angle_deg)


def make_rear_base(spec: MagneticThreeChannel300Spec = P2R2):
    """One manifold open-back cassette with 300 mm OD and six M3 spacers."""
    outer = _annulus(
        spec.base_outer_ring_span[0],
        spec.base_outer_ring_span[1],
        spec.rear_base_z[1] - spec.rear_base_z[0],
        spec.rear_base_z[0],
    )
    parts = [outer]

    # Three 6 mm backbones span r26..144 and overlap the outer ring by 6 mm.
    backbone_length = 144.0 - spec.center_open_radius
    backbone_center = (144.0 + spec.center_open_radius) / 2
    for angle in spec.backbone_angles:
        parts.append(
            _box(
                backbone_length,
                spec.backbone_width,
                spec.backbone_z[1] - spec.backbone_z[0],
                (backbone_center, 0, spec.backbone_z[0]),
            ).rotate(Axis.Z, angle)
        )

    # Three 18-degree wear pads per channel.  Their 0.4 mm Z overlap joins
    # them to the backbones; the second-channel pads also overlap the outer
    # base ring by 0.4 mm at r138..138.4.
    for channel in spec.channels:
        arc_length = radians(spec.pad_arc_degrees) * channel.radius
        for angle in spec.backbone_angles:
            parts.append(
                _annular_sector(
                    channel.radius + 0.20,
                    spec.pad_radial_width,
                    arc_length,
                    spec.pad_z[1] - 0.80,
                    0.80,
                    angle,
                    segments=36,
                )
            )

    spacer_z0, spacer_z1 = spec.stationary_spacer_z
    for radius, angle in spec.cap_fastener_sites[3]:
        x, y = _polar_xy(radius, angle)
        parts.append(
            _cylinder(
                spec.stationary_spacer_diameter / 2,
                spacer_z1 - (spacer_z0 - 0.40),
                spacer_z0 - 0.40,
            ).moved(Location((x, y, 0)))
        )

    result = _fuse_all(parts)
    result = result.solids()[0].fuse()
    through = _cylinder(
        spec.m3_clearance_diameter / 2,
        spacer_z1 - spec.rear_base_z[0] + 0.4,
        spec.rear_base_z[0] - 0.2,
    )
    for radius, angle in spec.cap_fastener_sites[3]:
        x, y = _polar_xy(radius, angle)
        result = result.cut(through.moved(Location((x, y, 0))))
    result.label = "p2r2_rear_base_300mm_open_back_9_wear_pads_6_integral_m3_spacers"
    return result


DEFAULT_ANGLES = {"hour": 25.0, "minute": 145.0, "second": 275.0}


def _placed_cap(index: int, thickness: float, spec: MagneticThreeChannel300Spec = P2R2):
    return make_front_cap_ring(index, spec).moved(
        Location((0, 0, spec.separator_rear_z + thickness + 4.0))
    )


def make_assembled(
    separator_thickness: float = 1.5,
    angles: dict[str, float] | None = None,
    spec: MagneticThreeChannel300Spec = P2R2,
):
    angles = DEFAULT_ANGLES if angles is None else angles
    children = [make_rear_base(spec)]
    children.extend(
        placed_hidden_driver(name, angles[name], spec) for name in ("second", "minute", "hour")
    )
    children.append(make_separator(separator_thickness, spec))
    children.extend(
        placed_follower(name, separator_thickness, angles[name], spec)
        for name in ("hour", "minute", "second")
    )
    children.extend(_placed_cap(index, separator_thickness, spec) for index in range(4))
    return Compound(
        children=children,
        label=f"p2r2_magnetic_three_channel_300mm_assembled_t{str(separator_thickness).replace('.', 'p')}",
    )


def make_service_exploded(spec: MagneticThreeChannel300Spec = P2R2):
    thickness = 1.5
    children = [make_rear_base(spec)]
    for index, name in enumerate(("second", "minute", "hour")):
        children.append(placed_hidden_driver(name, 0.0, spec).moved(Location((0, 0, -6.0 * index))))
    children.append(make_separator(thickness, spec).moved(Location((0, 0, 10.0))))
    for index, name in enumerate(("hour", "minute", "second")):
        children.append(make_follower(name, thickness, spec).moved(Location((0, 0, 20.0 + 8.0 * index))))
    for index in range(4):
        children.append(_placed_cap(index, thickness, spec).moved(Location((0, 0, 54.0 + 5.0 * index))))
    return Compound(children=children, label="p2r2_magnetic_three_channel_300mm_service_exploded_plus_z")


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

