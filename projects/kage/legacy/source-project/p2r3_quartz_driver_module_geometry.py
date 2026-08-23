"""STEP-first implementation geometry for KAGE P2R3 Module A.

Only the printed quartz driver side is implemented here.  The future magnetic
follower / inset-rail cassette is intentionally absent and belongs to Module B.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from build123d import Align, Axis, Box, CenterOf, Compound, Cylinder, Location

from p2r3_quartz_driver_module_spec import DriverChannel, P2R3A, QuartzDriverModuleSpec


def _box_x(length: float, width: float, height: float, z0: float):
    return Box(
        length,
        width,
        height,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, z0)))


def _centered_box(length: float, width: float, height: float, z0: float):
    return Box(
        length,
        width,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, z0)))


def _cylinder(radius: float, height: float, z0: float):
    return Cylinder(
        radius,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, z0)))


def _fuse_all(parts):
    parts = list(parts)
    if not parts:
        raise ValueError("cannot fuse an empty part list")
    result = parts[0]
    for part in parts[1:]:
        result = result.fuse(part)
    if not result.is_valid or not result.solids() or result.volume <= 0:
        raise ValueError("P2R3 fuse produced invalid/non-positive geometry")
    return result


def make_quartz_mount(spec: QuartzDriverModuleSpec = P2R3A):
    """Printed panel retained by the quartz movement's threaded shaft and nut."""
    plate = _cylinder(spec.mount_outer_diameter / 2, spec.mount_thickness, spec.mount_rear_z)
    bore = _cylinder(
        spec.mount_nominal_bore / 2,
        spec.mount_thickness + 0.4,
        spec.mount_rear_z - 0.2,
    )
    plate = plate.cut(bore)
    plate.label = "p2r3a_printed_quartz_mount_70mm_nominal_8p2_bore"
    return plate


def make_provisional_quartz_case_reference(spec: QuartzDriverModuleSpec = P2R3A):
    """Nonprintable envelope only; source movement has not been measured."""
    q = spec.quartz
    body = _centered_box(q.case_width_x, q.case_height_y, q.case_depth_z, q.case_rear_z)
    body.label = "PROVISIONAL_NONPRINTABLE_MH011_HR1688_CASE_REFERENCE_56x56x16p2"
    return body


def make_provisional_shaft_reference(name: str, spec: QuartzDriverModuleSpec = P2R3A):
    """Nested coaxial shaft envelope.  It intentionally overlaps its siblings."""
    channel = spec.channel(name)
    height = channel.shaft_attach_z - spec.quartz.case_front_z
    shaft = _cylinder(channel.shaft_nominal_od / 2, height, spec.quartz.case_front_z)
    shaft.label = (
        f"PROVISIONAL_NONPRINTABLE_{name.upper()}_SHAFT_REFERENCE_"
        f"OD{str(channel.shaft_nominal_od).replace('.', 'p')}"
    )
    return shaft


def make_counterweight_cup(
    name: str,
    *,
    arm_z0: float | None = None,
    spec: QuartzDriverModuleSpec = P2R3A,
):
    """Captured C-channel ballast cup with 6 mm of radial adjustment.

    The channel has 0.40 mm Y and 0.20 mm Z clearance per side.  A deliberately
    narrower snap mouth lets the cup install from -Z; two integral arm stops
    bound its radial travel.  Two wide, shallow ballast wells sit beside the
    central arm tunnel, keeping the complete cup in its channel-specific Z
    corridor while providing 0.228 cm3 usable fill volume.
    """
    channel = spec.channel(name)
    nominal_tail_z0 = channel.arm_z[0] + channel.counterweight_tail_z_offset
    tail_z0 = nominal_tail_z0 if arm_z0 is None else arm_z0
    cup_z_offset = channel.counterweight_cup_z[0] - nominal_tail_z0
    z0 = tail_z0 + cup_z_offset
    body_top = z0 + spec.counterweight_cup_height_z
    tunnel_height = spec.arm_thickness + spec.counterweight_tail_clearance_z
    tunnel_z0 = tail_z0 - spec.counterweight_tail_clearance_z_per_side
    snap_z0 = z0 - 0.05
    snap_height = tunnel_z0 - snap_z0 + 0.10
    cavity_z0 = body_top - spec.counterweight_ballast_well_depth_z
    body = _centered_box(
        spec.counterweight_cup_length_x,
        spec.counterweight_cup_width_y,
        spec.counterweight_cup_height_z,
        z0,
    )
    tunnel = _centered_box(
        spec.counterweight_cup_length_x + 0.6,
        spec.arm_width + spec.counterweight_tail_clearance_y,
        tunnel_height,
        tunnel_z0,
    )
    snap_mouth = _centered_box(
        spec.counterweight_cup_length_x + 0.6,
        spec.counterweight_snap_opening_y,
        snap_height,
        snap_z0,
    )
    wells = [
        _centered_box(
            spec.counterweight_ballast_well_length_x,
            spec.counterweight_ballast_well_width_y,
            spec.counterweight_ballast_well_depth_z + 0.10,
            cavity_z0,
        ).moved(Location((0, sign * spec.counterweight_ballast_well_center_y, 0)))
        for sign in (-1, 1)
    ]
    cup = body.cut(tunnel).cut(snap_mouth)
    for well in wells:
        cup = cup.cut(well)
    cup.label = (
        f"p2r3a_{name}_captured_snap_counterweight_cup_"
        f"travel{spec.counterweight_adjustment_travel_x:g}"
    )
    return cup


def _driver_radius(channel: DriverChannel, radius_kind: str) -> float:
    if radius_kind == "validation":
        return channel.validation_radius
    if radius_kind == "production":
        return channel.production_radius
    raise ValueError("radius_kind must be 'validation' or 'production'")


def make_driver_arm(
    name: str,
    *,
    radius_kind: str = "validation",
    hub_bore: float | None = None,
    spec: QuartzDriverModuleSpec = P2R3A,
):
    """Printed driver arm with a full-depth magnet seat and opposite cup rail."""
    channel = spec.channel(name)
    radius = _driver_radius(channel, radius_kind)
    bore = channel.shaft_nominal_od if hub_bore is None else hub_bore
    arm_z0, arm_z1 = channel.arm_z
    counter_radius = (
        channel.counterweight_validation_radius
        if radius_kind == "validation"
        else channel.counterweight_production_radius
    )

    forward = _box_x(radius, spec.arm_width, spec.arm_thickness, arm_z0)
    half_travel = spec.counterweight_adjustment_travel_x / 2
    half_cup = spec.counterweight_cup_length_x / 2
    outer_stop_center_x = -(
        counter_radius
        + half_travel
        + half_cup
        + spec.counterweight_stop_gap_x
        + spec.counterweight_stop_length_x / 2
    )
    inner_stop_center_x = -(
        counter_radius
        - half_travel
        - half_cup
        - spec.counterweight_stop_gap_x
        - spec.counterweight_stop_length_x / 2
    )
    tail_length = abs(outer_stop_center_x) + spec.counterweight_stop_length_x / 2
    tail_z0 = arm_z0 + channel.counterweight_tail_z_offset
    tail = _box_x(tail_length, spec.arm_width, spec.arm_thickness, tail_z0).rotate(
        Axis.Z, 180.0
    )
    outer_stop = _centered_box(
        spec.counterweight_stop_length_x,
        spec.counterweight_stop_width_y,
        spec.arm_thickness,
        tail_z0,
    ).moved(Location((outer_stop_center_x, 0, 0)))
    inner_stop = _centered_box(
        spec.counterweight_stop_length_x,
        spec.counterweight_stop_width_y,
        spec.arm_thickness,
        tail_z0,
    ).moved(Location((inner_stop_center_x, 0, 0)))
    hub = _cylinder(spec.hub_outer_diameter / 2, spec.arm_thickness, arm_z0)

    boss_z0 = arm_z1 - spec.magnet_boss_height
    magnet_boss = _cylinder(
        spec.magnet_boss_outer_diameter / 2,
        spec.magnet_boss_height,
        boss_z0,
    ).moved(Location((radius, 0, 0)))
    body = _fuse_all((forward, tail, inner_stop, outer_stop, hub, magnet_boss))

    hub_tool = _cylinder(bore / 2, spec.arm_thickness + 0.4, arm_z0 - 0.2)
    pocket = _cylinder(
        spec.magnet_pocket_diameter / 2,
        spec.magnet_pocket_depth + 0.2,
        arm_z1 - spec.magnet_pocket_depth,
    ).moved(Location((radius, 0, 0)))
    arm = body.cut(hub_tool).cut(pocket)
    arm.label = (
        f"p2r3a_{name}_{radius_kind}_driver_arm_r{radius:g}_"
        f"w{spec.arm_width:g}_t{spec.arm_thickness:g}_hub{bore:g}_magnet6x3"
    )
    return arm


def placed_driver_arm(
    name: str,
    angle_deg: float,
    *,
    radius_kind: str = "validation",
    spec: QuartzDriverModuleSpec = P2R3A,
):
    return make_driver_arm(name, radius_kind=radius_kind, spec=spec).rotate(Axis.Z, angle_deg)


def placed_counterweight_cup(
    name: str,
    angle_deg: float,
    *,
    radius_kind: str = "validation",
    axial_float_z: float = 0.0,
    spec: QuartzDriverModuleSpec = P2R3A,
):
    if abs(axial_float_z) > spec.counterweight_axial_float_z + 1e-9:
        raise ValueError(
            f"axial_float_z must remain within +/-{spec.counterweight_axial_float_z:g} mm"
        )
    channel = spec.channel(name)
    radius = (
        channel.counterweight_validation_radius
        if radius_kind == "validation"
        else channel.counterweight_production_radius
    )
    return (
        make_counterweight_cup(name, spec=spec)
        .moved(Location((-radius, 0, axial_float_z)))
        .rotate(Axis.Z, angle_deg)
    )


def make_compact_reference_assembly(spec: QuartzDriverModuleSpec = P2R3A):
    """True aligned-angle compact pose used by solid collision tests."""
    children = [
        make_quartz_mount(spec),
        make_provisional_quartz_case_reference(spec),
    ]
    for name in ("hour", "minute", "second"):
        children.append(make_provisional_shaft_reference(name, spec))
    for channel, angle in zip(spec.channels, spec.compact_angles_deg):
        children.append(placed_driver_arm(channel.name, angle, spec=spec))
        children.append(placed_counterweight_cup(channel.name, angle, spec=spec))
    return Compound(children=children, label="p2r3a_compact_quartz_driver_reference_assembly")


def clock_angles_deg(hour: int, minute: int, second: int) -> tuple[float, float, float]:
    """Continuous-sweep clockwise-equivalent angles used for collision poses."""
    return (
        30.0 * (hour % 12) + 0.5 * minute + second / 120.0,
        6.0 * minute + 0.1 * second,
        6.0 * second,
    )


def make_clock_state_reference_assembly(
    hour: int,
    minute: int,
    second: int,
    *,
    spec: QuartzDriverModuleSpec = P2R3A,
):
    """Compact reference at one real clock state, including provisional movement."""
    children = [make_quartz_mount(spec), make_provisional_quartz_case_reference(spec)]
    for name in ("hour", "minute", "second"):
        children.append(make_provisional_shaft_reference(name, spec))
    for channel, angle in zip(spec.channels, clock_angles_deg(hour, minute, second)):
        children.append(placed_driver_arm(channel.name, angle, spec=spec))
        children.append(placed_counterweight_cup(channel.name, angle, spec=spec))
    return Compound(
        children=children,
        label=f"p2r3a_dynamic_regression_state_{hour:02d}{minute:02d}{second:02d}",
    )


def make_full_radius_second_torque_wand(spec: QuartzDriverModuleSpec = P2R3A):
    arm = make_driver_arm("second", radius_kind="production", spec=spec)
    arm.label = "p2r3a_second_full_radius_r135_torque_wand"
    return arm


def make_full_radius_second_torque_wand_reference(spec: QuartzDriverModuleSpec = P2R3A):
    return Compound(
        children=[
            make_full_radius_second_torque_wand(spec),
            placed_counterweight_cup("second", 0.0, radius_kind="production", spec=spec),
        ],
        label="p2r3a_second_r135_torque_wand_with_adjustable_counterweight_cup",
    )


def make_fit_coupon_ladder(
    name: str,
    bores: tuple[float, float, float, float],
    spec: QuartzDriverModuleSpec = P2R3A,
):
    """Connected four-step ladder; each pad has a different bore and thickness."""
    if len(bores) != 4:
        raise ValueError("coupon ladder requires four bores")
    total_length = spec.coupon_pad_length + 3 * spec.coupon_pitch
    x0 = -total_length / 2 + spec.coupon_pad_length / 2
    parts = [
        _centered_box(
            total_length,
            spec.coupon_web_width,
            spec.coupon_web_thickness,
            0.0,
        )
    ]
    centers = []
    for index, (bore, thickness) in enumerate(zip(bores, spec.coupon_thickness_steps)):
        x = x0 + index * spec.coupon_pitch
        pad = _centered_box(
            spec.coupon_pad_length,
            spec.coupon_pad_width,
            thickness,
            0.0,
        ).moved(Location((x, 0, 0)))
        parts.append(pad)
        centers.append((x, bore, thickness))
    ladder = _fuse_all(parts)
    for x, bore, thickness in centers:
        tool = _cylinder(bore / 2, thickness + 0.4, -0.2).moved(Location((x, 0, 0)))
        ladder = ladder.cut(tool)
    ladder.label = f"p2r3a_{name}_fit_coupon_ladder_4_bores_4_thicknesses"
    return ladder


def make_all_fit_coupons(spec: QuartzDriverModuleSpec = P2R3A):
    ladders = [
        make_fit_coupon_ladder("movement_mount", spec.mount_bore_candidates, spec),
        make_fit_coupon_ladder("hour_hub", spec.channel("hour").hub_bore_candidates, spec),
        make_fit_coupon_ladder("minute_hub", spec.channel("minute").hub_bore_candidates, spec),
        make_fit_coupon_ladder("second_hub", spec.channel("second").hub_bore_candidates, spec),
    ]
    placed = [ladder.moved(Location((0, -27.0 + 18.0 * index, 0))) for index, ladder in enumerate(ladders)]
    return Compound(children=placed, label="p2r3a_all_hub_and_mount_fit_coupon_ladders")


def pairwise_intersection_volume(left, right) -> float:
    total = 0.0
    for left_solid in left.solids():
        for right_solid in right.solids():
            common = left_solid.intersect(right_solid)
            if common is not None:
                total += sum(abs(solid.volume) for solid in common.solids())
    return total


def compact_dynamic_envelope_diameter(spec: QuartzDriverModuleSpec = P2R3A) -> float:
    """Diameter swept by every compact printed arm and its nominal cup."""
    maximum_radius = 0.0
    for channel in spec.channels:
        for shape in (
            make_driver_arm(channel.name, spec=spec),
            placed_counterweight_cup(channel.name, 0.0, spec=spec),
        ):
            for vertex in shape.vertices():
                maximum_radius = max(maximum_radius, hypot(vertex.X, vertex.Y))
    return 2.0 * maximum_radius


@dataclass(frozen=True)
class BalanceSolution:
    name: str
    arm_mass_g: float
    arm_centroid_x_mm: float
    cup_mass_g: float
    cup_centroid_x_mm: float
    ideal_filler_mass_g: float
    quantized_filler_mass_g: float
    residual_gf_cm: float


def _petg_mass_g(shape, spec: QuartzDriverModuleSpec) -> float:
    return shape.volume * spec.petg_density_g_per_cm3 / 1000.0


def production_balance_solution(
    name: str,
    *,
    spec: QuartzDriverModuleSpec = P2R3A,
) -> BalanceSolution:
    """Balance from live production BREP mass properties, not magnet-only math."""
    channel = spec.channel(name)
    arm = make_driver_arm(name, radius_kind="production", spec=spec)
    cup = placed_counterweight_cup(name, 0.0, radius_kind="production", spec=spec)
    arm_mass = _petg_mass_g(arm, spec)
    cup_mass = _petg_mass_g(cup, spec)
    arm_x = arm.center(CenterOf.MASS).X
    cup_x = cup.center(CenterOf.MASS).X
    fixed_moment = (
        arm_mass * arm_x / 10.0
        + cup_mass * cup_x / 10.0
        + spec.magnet_mass_g * channel.production_radius / 10.0
    )
    filler_radius_cm = channel.counterweight_production_radius / 10.0
    ideal = fixed_moment / filler_radius_cm
    resolution = 0.01 if name == "second" else 0.10
    quantized = round(ideal / resolution) * resolution
    residual = fixed_moment - quantized * filler_radius_cm
    return BalanceSolution(
        name=name,
        arm_mass_g=arm_mass,
        arm_centroid_x_mm=arm_x,
        cup_mass_g=cup_mass,
        cup_centroid_x_mm=cup_x,
        ideal_filler_mass_g=ideal,
        quantized_filler_mass_g=quantized,
        residual_gf_cm=residual,
    )


def compact_printable_objects(spec: QuartzDriverModuleSpec = P2R3A):
    objects = [("quartz_mount", make_quartz_mount(spec))]
    for name in ("hour", "minute", "second"):
        objects.append((f"driver_arm_{name}_compact", make_driver_arm(name, spec=spec)))
        objects.append((f"counterweight_cup_{name}", make_counterweight_cup(name, arm_z0=0.0, spec=spec)))
    objects.extend(
        (
            ("coupon_movement_mount", make_fit_coupon_ladder("movement_mount", spec.mount_bore_candidates, spec)),
            ("coupon_hour_hub", make_fit_coupon_ladder("hour_hub", spec.channel("hour").hub_bore_candidates, spec)),
            ("coupon_minute_hub", make_fit_coupon_ladder("minute_hub", spec.channel("minute").hub_bore_candidates, spec)),
            ("coupon_second_hub", make_fit_coupon_ladder("second_hub", spec.channel("second").hub_bore_candidates, spec)),
        )
    )
    return objects
