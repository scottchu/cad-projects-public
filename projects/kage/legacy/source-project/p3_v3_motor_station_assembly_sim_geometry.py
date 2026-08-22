"""STEP-first staged geometry for the KAGE P3 V3 motor station assembly."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    Compound,
    Cylinder,
    Location,
    import_step,
)
from cadgen import srgb

from p3_v3_full_ring_r2_geometry import (
    _full_role_ring,
    make_output_pinion,
)
from p3_v3_motor_station_assembly_sim_spec import (
    P3V3MotorStationAssemblySimSpec,
    P3_V3_MOTOR_STATION_ASSEMBLY_SIM,
)
from p3_v3_transmission_r1_geometry import (
    _d_prism_z,
    _one_sided_radial_passage,
    make_bearing as r1_make_bearing,
    make_miter_pair as r1_make_miter_pair,
    make_motor_body as r1_make_motor_body,
    make_motor_shaft as r1_make_motor_shaft,
    make_output_shaft as r1_make_output_shaft,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v3_motor_station_assembly_sim"
PURCHASED_ROOT = MODEL_ROOT / "purchased"


def _label(shape, label: str, color: str):
    shape.label = label
    shape.color = srgb(color)
    return shape


def _translated_r1(part, role: int, spec: P3V3MotorStationAssemblySimSpec):
    return deepcopy(part).moved(
        Location((spec.station_translation_x, 0.0, spec.role_shift_z(role)))
    )


def _annulus_at_axis(
    x: float,
    inner_radius: float,
    outer_radius: float,
    z0: float,
    z1: float,
):
    outer = Cylinder(
        outer_radius,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, 0.0, z0)))
    inner = Cylinder(
        inner_radius,
        z1 - z0 + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, 0.0, z0 - 0.2)))
    return outer.cut(inner)


def _clearance_cloud(shape, clearance: float):
    """Conservative six-direction BREP clearance without mesh substitution."""

    cloud = deepcopy(shape)
    for delta in (
        (clearance, 0.0, 0.0),
        (-clearance, 0.0, 0.0),
        (0.0, clearance, 0.0),
        (0.0, -clearance, 0.0),
        (0.0, 0.0, clearance),
        (0.0, 0.0, -clearance),
    ):
        cloud = cloud.fuse(deepcopy(shape).moved(Location(delta)))
    return cloud


def make_motor_body(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    body = _translated_r1(r1_make_motor_body(), role, spec)
    body.label = f"stage_motor_{spec.parent.roles[role]}_NEMA8_REFERENCE"
    return body


def make_motor_shaft(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    shaft = _translated_r1(r1_make_motor_shaft(), role, spec)
    shaft.label = f"stage_motor_{spec.parent.roles[role]}_4x7_D_shaft_REFERENCE"
    return shaft


@lru_cache(maxsize=3)
def _make_miter_pair_cached(role: int, spec: P3V3MotorStationAssemblySimSpec):
    horizontal, vertical = r1_make_miter_pair()
    horizontal = _translated_r1(horizontal, role, spec)
    vertical = _translated_r1(vertical, role, spec)
    # The vertical gear keeps R1's +Y-facing D-bore and radial M2 clamp.  Add a
    # real radial clamp to the horizontal motor bevel as positive axial
    # retention on the NEMA8 D-shaft; its D-bore remains the torque path.
    center_z = spec.miter_intersection_z(role)
    motor_flat_z = center_z + spec.motor_shaft_across_flat / 2.0
    horizontal_grub = Cylinder(
        spec.shaft_set_screw_tap_pilot_diameter / 2.0,
        spec.miter_hub_diameter / 2.0 - spec.motor_shaft_across_flat / 2.0 + 0.3,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((118.0, 0.0, motor_flat_z - 0.05)))
    horizontal = horizontal.cut(horizontal_grub)
    horizontal.label = f"stage_{spec.parent.roles[role]}_horizontal_miter_D_bore_M2_axial_lock"
    vertical.label = f"stage_{spec.parent.roles[role]}_vertical_miter_common_D_bore_M2_set_screw"
    return horizontal, vertical


def make_miter_pair(
    role: int,
    spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM,
):
    """Return unparented copies so assembly stages cannot steal each other's gears."""

    horizontal, vertical = _make_miter_pair_cached(role, spec)
    return deepcopy(horizontal), deepcopy(vertical)


def make_output_shaft(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    shaft = _translated_r1(r1_make_output_shaft(), role, spec)
    return _label(shaft, f"stage_{spec.parent.roles[role]}_purchased_4x40_D_shaft_3p5AF_REFERENCE", "#B9C0C5")


def make_bearing(role: int, which: str, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    bearing = _translated_r1(r1_make_bearing(which), role, spec)
    bearing.label = f"stage_{spec.parent.roles[role]}_MR84ZZ_{which}_REFERENCE"
    return bearing


def make_bearing_radial_cap(
    role: int,
    which: str,
    spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM,
):
    """Removable +X gate that positively blocks MR84 radial escape."""

    if which not in ("lower", "upper"):
        raise ValueError(which)
    z0, z1 = spec.lower_bearing_z(role) if which == "lower" else spec.upper_bearing_z(role)
    x0 = 128.25 + spec.bearing_cap_radial_clearance_x
    cap = Box(
        spec.bearing_cap_thickness_x,
        27.0,
        z1 - z0,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((x0, 0.0, z0)))
    for y in spec.bearing_cap_screw_y:
        hole = Cylinder(
            spec.motor_clearance_hole_diameter / 2.0,
            spec.bearing_cap_thickness_x + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).rotate(Axis.Y, 90.0).moved(Location((x0 - 0.2, y, (z0 + z1) / 2.0)))
        cap = cap.cut(hole)
    return _label(cap, f"{which}_MR84_removable_radial_gate_2x_M2x4", "#AEB5B9")


def make_bearing_cap_screws(
    role: int,
    which: str,
    spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM,
):
    z0, z1 = spec.lower_bearing_z(role) if which == "lower" else spec.upper_bearing_z(role)
    x = 128.25 + spec.bearing_cap_radial_clearance_x + spec.bearing_cap_thickness_x
    screw_ref = _purchased_screw("iso4762_socket_head_cap_screw_m2x4.step")
    screws = []
    for index, y in enumerate(spec.bearing_cap_screw_y):
        screw = deepcopy(screw_ref).rotate(Axis.Y, 90.0).moved(Location((x, y, (z0 + z1) / 2.0)))
        screw.label = f"ISO4762_M2x4_{which}_bearing_gate_screw_{index+1}_REFERENCE"
        screw.color = srgb("#B9C0C5")
        screws.append(screw)
    return tuple(screws)


def make_role_pinion(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    # R2 places each pinion at its global station angle.  Rotate it back so the
    # staged assembly remains on the readable +X station datum.
    pinion = deepcopy(make_output_pinion(role)).rotate(
        Axis.Z, -spec.parent.motor_station_angles[role]
    )
    face_z0, face_z1 = spec.parent.pinion_face_ranges[role]
    # Fill the inherited bore only after all tooth/station rotations are final,
    # then cut one common +Y-facing D-bore.  This decouples tooth phase from
    # shaft-flat phase for all H/M/S stations.
    refill = Cylinder(
        3.6,
        face_z1 - face_z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((spec.output_axis_x, 0.0, face_z0)))
    common_d_bore = _d_prism_z(
        spec.output_axis_x,
        face_z0 - 0.2,
        face_z1 + 0.2,
        spec.shaft_bore_clearance_diameter,
        spec.shaft_bore_across_flat,
    )
    set_screw = _one_sided_radial_passage(
        spec.output_axis_x,
        (face_z0 + face_z1) / 2.0,
        spec.parent.output_shaft_diameter / 2.0,
        spec.parent.pinion_outer_radius + 0.30,
        spec.shaft_set_screw_tap_pilot_diameter,
    )
    pinion = pinion.fuse(refill).cut(common_d_bore).cut(set_screw)
    pinion.label = f"stage_{spec.parent.roles[role]}_exact_R2_output_pinion_common_D_bore_M2_set_screw"
    return pinion


def make_ring_mesh_coupon(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    # Rotate the complete ring by the same normalization applied to the global
    # role pinion.  The 260T ring is not invariant under an arbitrary 120/240
    # degree turn; keeping both transforms coupled preserves the exact phase.
    ring = deepcopy(_full_role_ring(role)).rotate(
        Axis.Z, -spec.parent.motor_station_angles[role]
    )
    # Keep a 56 mm tangential coupon centered on +X.  It contains the exact
    # active 260T R2 tooth form while keeping review STEP files compact.
    crop = Box(24.0, 56.0, 40.0, align=(Align.MIN, Align.CENTER, Align.CENTER)).moved(
        Location((128.0, 0.0, sum(spec.parent.pinion_face_ranges[role]) / 2.0))
    )
    pieces = ring.intersect(crop)
    if not pieces:
        raise ValueError("ring mesh coupon crop produced no solid")
    coupon = max(pieces, key=lambda s: s.volume)
    coupon.label = f"stage_{spec.parent.roles[role]}_exact_R2_ring_mesh_coupon"
    coupon.color = srgb(spec.parent.role_colors[role])
    return coupon


def _motor_driver_tools(role: int, spec: P3V3MotorStationAssemblySimSpec):
    center_z = spec.miter_intersection_z(role)
    half = spec.motor_mount_pitch / 2.0
    tools = []
    for index, (y, z) in enumerate(
        (pair for y in (-half, half) for z in (center_z - half, center_z + half) for pair in [(y, z)])
    ):
        tool = Cylinder(
            spec.motor_driver_clearance_diameter / 2.0,
            20.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).rotate(Axis.Y, 90.0).moved(
            Location((spec.motor_face_plate_x[1] + spec.motor_screw_head_height, y, z))
        )
        tools.append(_label(tool, f"M2_motor_driver_access_{index+1}_KEEP_CLEAR", "#75C9D1"))
    return tuple(tools)


def _shaft_driver_tool(
    role: int,
    kind: str,
    spec: P3V3MotorStationAssemblySimSpec,
):
    if kind == "lower_collar":
        z = spec.lower_collar_z(role)[0] + 0.80
        start_y = spec.collar_outer_diameter / 2.0
    elif kind == "vertical_miter":
        # Existing vertical miter hub top and height are inherited from R1.
        z = -4.10 + spec.role_shift_z(role)
        start_y = spec.parent.miter_face_width + 6.0
    elif kind == "output_pinion":
        z = sum(spec.parent.pinion_face_ranges[role]) / 2.0
        start_y = spec.parent.pinion_outer_radius
    elif kind == "top_collar":
        z = spec.top_collar_screw_z(role)
        start_y = spec.collar_outer_diameter / 2.0
    else:
        raise ValueError(kind)
    tool = Cylinder(
        spec.set_screw_tool_clearance_diameter / 2.0,
        22.0 - start_y,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).rotate(Axis.X, -90.0).moved(Location((spec.output_axis_x, start_y, z)))
    return _label(tool, f"M2_{kind}_driver_access_KEEP_CLEAR", "#75C9D1")


def _horizontal_bevel_driver_tool(
    role: int,
    spec: P3V3MotorStationAssemblySimSpec,
):
    center_z = spec.miter_intersection_z(role)
    start_z = center_z + spec.miter_hub_diameter / 2.0
    tool = Cylinder(
        spec.set_screw_tool_clearance_diameter / 2.0,
        15.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((118.0, 0.0, start_z)))
    return _label(tool, "M2_horizontal_motor_bevel_driver_access_KEEP_CLEAR", "#75C9D1")


def _bearing_cap_driver_tools(
    role: int,
    spec: P3V3MotorStationAssemblySimSpec,
):
    refs = []
    x0 = 128.25 + spec.bearing_cap_radial_clearance_x + spec.bearing_cap_thickness_x + spec.motor_screw_head_height
    for which in ("lower", "upper"):
        z0, z1 = spec.lower_bearing_z(role) if which == "lower" else spec.upper_bearing_z(role)
        for index, y in enumerate(spec.bearing_cap_screw_y):
            tool = Cylinder(
                spec.motor_driver_clearance_diameter / 2.0,
                14.0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).rotate(Axis.Y, 90.0).moved(Location((x0, y, (z0 + z1) / 2.0)))
            refs.append(_label(tool, f"M2_{which}_bearing_gate_driver_{index+1}_KEEP_CLEAR", "#75C9D1"))
    return tuple(refs)


def make_motor_face_flange(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    center_z = spec.miter_intersection_z(role)
    x0, x1 = spec.motor_face_plate_x
    plate = Box(
        x1 - x0,
        23.0,
        23.0,
        align=(Align.MIN, Align.CENTER, Align.CENTER),
    ).moved(Location((x0, 0.0, center_z)))
    center_passage = Cylinder(
        spec.motor_center_passage_diameter / 2.0,
        x1 - x0 + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).moved(Location(((x0 + x1) / 2.0, 0.0, center_z)))
    plate = plate.cut(center_passage)
    half = spec.motor_mount_pitch / 2.0
    for y in (-half, half):
        for z in (center_z - half, center_z + half):
            hole = Cylinder(
                spec.motor_clearance_hole_diameter / 2.0,
                x1 - x0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).rotate(Axis.Y, 90.0).moved(Location(((x0 + x1) / 2.0, y, z)))
            plate = plate.cut(hole)
    return _label(plate, "gearbox_motor_face_flange_1p5mm_with_4x_M2_clearance", "#778187")


def make_gearbox_frame(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    lower = spec.lower_bearing_z(role)
    upper = spec.upper_bearing_z(role)
    # Side posts run continuously into the mounting feet.  Earlier exploratory
    # geometry left a vertical gap here, which made the bearing yoke a floating
    # disjoint solid even though it looked aligned in one view.
    z0 = spec.gearbox_foot_z[0]
    z1 = upper[1] + 1.5
    frame = make_motor_face_flange(role, spec)

    # Two open side posts stay outside the complete 18 mm miter envelope.
    for y in (-spec.frame_side_y, spec.frame_side_y):
        post = Box(
            16.5,
            spec.frame_wall,
            z1 - z0,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((111.75, y, z0)))
        frame = frame.fuse(post)

    # Three-quarter C cradles support each MR84 outer race from the output side
    # and both tangential sides.  A full annular pocket is impossible at the
    # lower bearing because the orthogonal bevel gear legitimately occupies
    # the inner quadrant.  The open side is the bearing insertion path.
    for bearing_range in (lower, upper):
        bz0, bz1 = bearing_range
        cradle = Box(
            8.50,
            23.0,
            bz1 - bz0,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((119.75, 0.0, bz0)))
        pocket = Cylinder(
            spec.bearing_pocket_diameter / 2.0,
            bz1 - bz0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.output_axis_x, 0.0, bz0 - 0.2)))
        frame = frame.fuse(cradle.cut(pocket))
        if bearing_range == lower:
            lip_z0, lip_z1 = bz0 - 0.8, bz0
        else:
            lip_z0, lip_z1 = bz1, bz1 + 0.8
        lip = Box(
            8.50,
            23.0,
            lip_z1 - lip_z0,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((119.75, 0.0, lip_z0)))
        lip_opening = Cylinder(
            spec.bearing_lip_opening / 2.0,
            lip_z1 - lip_z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.output_axis_x, 0.0, lip_z0 - 0.2)))
        frame = frame.fuse(lip.cut(lip_opening))

    # Two longitudinal feet, four M3 clearance holes.  Their screw axes are
    # inboard of the moving ring and reachable from +Z.
    foot_x0 = 78.0
    # Extend beneath the side posts so the yoke, feet, and motor flange are one
    # load path rather than merely aligned disjoint solids.
    foot_x1 = 114.5
    for y in spec.chassis_mount_y:
        foot = Box(
            foot_x1 - foot_x0,
            7.0,
            spec.gearbox_foot_thickness,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((foot_x0, y, spec.gearbox_foot_z[0])))
        frame = frame.fuse(foot)
    rear_cross_tie = Box(
        7.0,
        36.0,
        spec.gearbox_foot_thickness,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((foot_x0, 0.0, spec.gearbox_foot_z[0])))
    frame = frame.fuse(rear_cross_tie)
    for x in spec.chassis_mount_x:
        for y in spec.chassis_mount_y:
            hole = Cylinder(
                spec.chassis_screw_clearance_diameter / 2.0,
                spec.gearbox_foot_thickness + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, spec.gearbox_foot_z[0] - 0.2)))
            frame = frame.cut(hole)

    # Blind M2 pilots in the side posts accept the two removable radial-gate
    # screws for each MR84.  The driver remains entirely on the open +X side.
    for bearing_range in (lower, upper):
        center_z = sum(bearing_range) / 2.0
        for y in spec.bearing_cap_screw_y:
            pilot = Cylinder(
                spec.shaft_set_screw_tap_pilot_diameter / 2.0,
                spec.bearing_cap_screw_engagement + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).rotate(Axis.Y, 90.0).moved(
                Location((128.25 - spec.bearing_cap_screw_engagement - 0.05, y, center_z))
            )
            frame = frame.cut(pilot)

    # Explicit service windows.  Each window is cut from the same BREP cylinder
    # used by the access tests.  Motor windows remove only the shallow inner
    # edge of the two side posts; shaft-clamp windows cross only the +Y post,
    # leaving the -Y post and rear cross-tie as uninterrupted load paths.
    for tool in _motor_driver_tools(role, spec):
        frame = frame.cut(tool)
    for kind in ("lower_collar", "vertical_miter"):
        frame = frame.cut(_shaft_driver_tool(role, kind, spec))
    frame = frame.cut(_horizontal_bevel_driver_tool(role, spec))
    # Role H sits 4.3 mm below S; without this explicit body envelope its
    # motor corner clips the shared foot.  Cut the real role-specific motor
    # body plus 0.20 mm clearance while preserving the remote cross-tie.
    frame = frame.cut(_clearance_cloud(make_motor_body(role, spec), 0.20))

    # The rectangular cradle-minus-round-pocket operation can leave a small
    # isolated crescent on the open (+X) side of the bearing.  It is not part
    # of the load path (the two tangential saddles are fused into the posts),
    # and retaining it would create an unprintable floating second solid.
    # Deliberately keep only the connected yoke/feet/flange solid.
    connected = frame.solids()
    if len(connected) > 1:
        frame = max(connected, key=lambda solid: solid.volume)

    frame.label = f"gearbox_open_yoke_{spec.parent.roles[role]}_one_piece"
    frame.color = srgb("#778187")
    return frame


def make_chassis_patch(spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    z0, z1 = spec.chassis_patch_z
    patch = Box(54.0, 42.0, z1 - z0, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
        Location((68.0, 0.0, z0))
    )
    # Integral bosses extend far enough to carry a 5.5 mm insert below the
    # yoke feet.  The pilot is blind from below and open from +Z.
    for x in spec.chassis_mount_x:
        for y in spec.chassis_mount_y:
            boss = Cylinder(
                4.0,
                spec.chassis_insert_length,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
            ).moved(Location((x, y, z1)))
            pilot = Cylinder(
                spec.chassis_insert_pilot_diameter / 2.0,
                spec.chassis_insert_length + 0.2,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
            ).moved(Location((x, y, z1 + 0.1)))
            patch = patch.fuse(boss).cut(pilot)
    # Shared service scallop for the low hour-channel lower-collar hex key.
    # Minute/second axes are already above the chassis top, but cutting all
    # three source tools keeps the common part definition explicit.
    for role in range(3):
        patch = patch.cut(_shaft_driver_tool(role, "lower_collar", spec))
    return _label(patch, "fixed_chassis_patch_with_4x_M3_heat_set_insert_pockets", "#59666F")


def make_heat_set_insert_references(spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    refs = []
    z1 = spec.chassis_patch_z[1]
    for index, (x, y) in enumerate(
        (pair for x in spec.chassis_mount_x for y in spec.chassis_mount_y for pair in [(x, y)])
    ):
        outer = Cylinder(
            spec.chassis_insert_outer_diameter / 2.0,
            spec.chassis_insert_length,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((x, y, z1)))
        bore = Cylinder(
            1.5,
            spec.chassis_insert_length + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((x, y, z1 + 0.2)))
        refs.append(_label(outer.cut(bore), f"purchased_M3_heat_set_insert_{index+1}_REFERENCE", "#D9A441"))
    return tuple(refs)


@lru_cache(maxsize=2)
def _purchased_screw(name: str):
    return import_step(PURCHASED_ROOT / name)


def make_motor_screws(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    screw_ref = _purchased_screw("iso4762_socket_head_cap_screw_m2x4.step")
    center_z = spec.miter_intersection_z(role)
    half = spec.motor_mount_pitch / 2.0
    screws = []
    for index, (y, z) in enumerate(
        (pair for y in (-half, half) for z in (center_z - half, center_z + half) for pair in [(y, z)])
    ):
        screw = deepcopy(screw_ref).rotate(Axis.Y, 90.0).moved(
            Location((spec.motor_face_plate_x[1], y, z))
        )
        screw.label = f"ISO4762_M2x4_motor_screw_{index+1}"
        screw.color = srgb("#B9C0C5")
        screws.append(screw)
    return tuple(screws)


def make_chassis_screws(spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    screw_ref = _purchased_screw("iso4762_socket_head_cap_screw_m3x8.step")
    screws = []
    for index, (x, y) in enumerate(
        (pair for x in spec.chassis_mount_x for y in spec.chassis_mount_y for pair in [(x, y)])
    ):
        screw = deepcopy(screw_ref).moved(Location((x, y, spec.gearbox_foot_z[1])))
        screw.label = f"ISO4762_M3x8_chassis_screw_{index+1}"
        screw.color = srgb("#B9C0C5")
        screws.append(screw)
    return tuple(screws)


def make_role_spacer(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    z0, z1 = spec.spacer_z(role)
    spacer = _annulus_at_axis(
        spec.output_axis_x,
        spec.spacer_bore_diameter / 2.0,
        spec.spacer_outer_diameter / 2.0,
        z0,
        z1,
    )
    return _label(spacer, f"{spec.parent.roles[role]}_role_spacer_L{z1-z0:.2f}", spec.parent.role_colors[role])


def make_clamp_collar(role: int, which: str, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    z0, z1 = spec.lower_collar_z(role) if which == "lower" else spec.top_collar_z(role)
    collar = _annulus_at_axis(
        spec.output_axis_x,
        spec.shaft_bore_clearance_diameter / 2.0,
        spec.collar_outer_diameter / 2.0,
        z0,
        z1,
    )
    # Split and clamp screw are represented as service clearances.  The part is
    # a purchased metal collar; printed-thread performance is not assumed.
    split = Box(2.4, 0.8, z1 - z0 + 0.4, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
        Location((spec.output_axis_x + 1.6, 0.0, z0 - 0.2))
    )
    screw_z = z0 + 0.80 if which == "lower" else spec.top_collar_screw_z(role)
    screw = _one_sided_radial_passage(
        spec.output_axis_x,
        screw_z,
        spec.parent.output_shaft_diameter / 2.0,
        spec.collar_outer_diameter / 2.0,
        spec.shaft_set_screw_tap_pilot_diameter,
    )
    collar = collar.cut(split).cut(screw)
    return _label(collar, f"purchased_4mm_split_clamp_collar_{which}_REFERENCE", "#6B7074")


def make_grub_screw_references(
    role: int,
    spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM,
):
    refs = []
    # Horizontal motor bevel: screw approaches from +Z and lands on the
    # supplied motor shaft's +Z D-flat.
    center_z = spec.miter_intersection_z(role)
    z0 = center_z + spec.motor_shaft_across_flat / 2.0
    z1 = center_z + spec.miter_hub_diameter / 2.0 + 0.15
    horizontal = Cylinder(1.0, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((118.0, 0.0, z0))
    )
    refs.append(_label(horizontal, "purchased_M2x3_horizontal_bevel_grub_screw_REFERENCE", "#6B7074"))

    # Vertical bevel and output pinion both approach the common +Y D-flat.
    for kind, z, outer in (
        ("vertical_bevel", -4.10 + spec.role_shift_z(role), spec.miter_outer_radius + 0.2),
        ("output_pinion", sum(spec.parent.pinion_face_ranges[role]) / 2.0, spec.parent.pinion_outer_radius + 0.2),
    ):
        y0 = spec.output_shaft_flat_y
        screw = Cylinder(1.0, outer - y0, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
            Axis.X, -90.0
        ).moved(Location((spec.output_axis_x, y0, z)))
        refs.append(_label(screw, f"purchased_M2x3_{kind}_grub_screw_REFERENCE", "#6B7074"))
    return tuple(refs)


def make_final_station_parts(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    horizontal, vertical = make_miter_pair(role, spec)
    parts = [
        make_chassis_patch(spec),
        *make_heat_set_insert_references(spec),
        make_gearbox_frame(role, spec),
        *make_chassis_screws(spec),
        make_motor_body(role, spec),
        make_motor_shaft(role, spec),
        *make_motor_screws(role, spec),
        make_bearing(role, "lower", spec),
        make_bearing_radial_cap(role, "lower", spec),
        *make_bearing_cap_screws(role, "lower", spec),
        make_bearing(role, "upper", spec),
        make_bearing_radial_cap(role, "upper", spec),
        *make_bearing_cap_screws(role, "upper", spec),
        make_output_shaft(role, spec),
        horizontal,
        vertical,
        *make_grub_screw_references(role, spec),
        make_clamp_collar(role, "lower", spec),
        make_role_spacer(role, spec),
        make_role_pinion(role, spec),
        make_clamp_collar(role, "top", spec),
        make_ring_mesh_coupon(role, spec),
    ]
    return tuple(parts)


def make_final_station(role: int, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    return Compound(children=list(make_final_station_parts(role, spec)), label=f"STATIC_STAGE4_CUTAWAY_{spec.parent.roles[role]}_final_height_locked")


def _moved_parts(parts, delta):
    return [deepcopy(part).moved(Location(delta)) for part in parts]


def make_stage_1_motor_mount(role: int = 2, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    frame = make_gearbox_frame(role, spec)
    horizontal, _ = make_miter_pair(role, spec)
    motor_group = [make_motor_body(role, spec), make_motor_shaft(role, spec)]
    motor_group.extend(make_motor_screws(role, spec))
    motor_group.extend([horizontal, make_grub_screw_references(role, spec)[0]])
    parts = [frame, *_moved_parts(motor_group, (spec.motor_explode_x, 0.0, 0.0))]
    return Compound(children=parts, label="STATIC_STAGE1_mount_NEMA8_and_horizontal_bevel_before_output_stack")


def make_stage_2_gearbox_mount(role: int = 2, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    horizontal, _ = make_miter_pair(role, spec)
    motor = [
        make_motor_body(role, spec),
        make_motor_shaft(role, spec),
        *make_motor_screws(role, spec),
        horizontal,
        make_grub_screw_references(role, spec)[0],
    ]
    yoke = [make_gearbox_frame(role, spec), *make_chassis_screws(spec)]
    fixed = [make_chassis_patch(spec), *make_heat_set_insert_references(spec)]
    return Compound(
        children=[*fixed, *_moved_parts([*motor, *yoke], (0.0, 0.0, spec.frame_explode_z))],
        label="STATIC_STAGE2_mount_open_yoke_with_4x_M3x8",
    )


def make_stage_3_shaft_stack(role: int = 2, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    horizontal, vertical = make_miter_pair(role, spec)
    base = [
        make_chassis_patch(spec),
        *make_heat_set_insert_references(spec),
        make_gearbox_frame(role, spec),
        *make_chassis_screws(spec),
        make_motor_body(role, spec),
        make_motor_shaft(role, spec),
        *make_motor_screws(role, spec),
        horizontal,
        make_grub_screw_references(role, spec)[0],
    ]
    ordered = [
        make_clamp_collar(role, "lower", spec),
        make_bearing(role, "lower", spec),
        vertical,
        make_bearing(role, "upper", spec),
        make_output_shaft(role, spec),
        make_role_spacer(role, spec),
        make_role_pinion(role, spec),
        make_clamp_collar(role, "top", spec),
    ]
    exploded = []
    for index, part in enumerate(ordered):
        exploded.extend(_moved_parts([part], (0.0, 0.0, (index + 1) * spec.stack_explode_z)))
    gates = []
    for which in ("lower", "upper"):
        gates.extend(
            _moved_parts(
                [make_bearing_radial_cap(role, which, spec), *make_bearing_cap_screws(role, which, spec)],
                (spec.service_explode_x, 0.0, 0.0),
            )
        )
    return Compound(
        children=[*base, *exploded, *gates],
        label="STATIC_STAGE3_build_output_stack_then_install_MR84_gates_before_ring",
    )


def make_stage_4_height_lock(role: int = 2, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    return make_final_station(role, spec)


def make_stage_5_reverse_service(role: int = 2, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    """Static honest reverse-service view.

    The role ring comes off first, followed by both MR84 gates and the complete
    vertical output stack.  Only then are the four motor screws reachable.
    """

    installed = []
    removed_ring = []
    removed_gates = []
    removed_stack = []
    for part in make_final_station_parts(role, spec):
        label = part.label.lower()
        if "ring_mesh_coupon" in label:
            removed_ring.extend(_moved_parts([part], (0.0, 70.0, 0.0)))
        elif "bearing_gate" in label or "radial_gate" in label:
            removed_gates.extend(_moved_parts([part], (spec.service_explode_x, 0.0, 0.0)))
        elif any(
            token in label
            for token in (
                "purchased_4x40_d_shaft",
                "mr84zz_",
                "vertical_miter",
                "vertical_bevel_grub",
                "lower_reference",
                "role_spacer",
                "output_pinion",
                "top_reference",
            )
        ):
            removed_stack.extend(_moved_parts([part], (0.0, 0.0, 32.0)))
        else:
            installed.append(part)
    motor_axes = list(_motor_driver_tools(role, spec))
    return Compound(
        children=[*installed, *removed_ring, *removed_gates, *removed_stack, *motor_axes],
        label="STATIC_STAGE5_REVERSE_SERVICE_ring_then_gates_then_output_stack_then_motor_M2",
    )


def make_gate_install_stage_parts(
    role: int,
    spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM,
):
    """Installed solids present while the MR84 gates are fitted.

    The role ring is deliberately absent because it is installed only after
    the gate screws are torqued.
    """

    return tuple(
        part
        for part in make_final_station_parts(role, spec)
        if "ring_mesh_coupon" not in part.label.lower()
    )


def make_motor_service_stage_parts(
    role: int,
    spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM,
):
    """Stationary solids remaining when the motor screws are serviced."""

    removed_tokens = (
        "ring_mesh_coupon",
        "bearing_gate",
        "radial_gate",
        "purchased_4x40_d_shaft",
        "mr84zz_",
        "vertical_miter",
        "vertical_bevel_grub",
        "lower_reference",
        "role_spacer",
        "output_pinion",
        "top_reference",
    )
    return tuple(
        part
        for part in make_final_station_parts(role, spec)
        if not any(token in part.label.lower() for token in removed_tokens)
    )


def make_three_role_axial_comparison(spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    stations = []
    for role in range(3):
        parts = list(make_final_station_parts(role, spec))
        stations.extend(_moved_parts(parts, (0.0, (role - 1) * 75.0, 0.0)))
    return Compound(children=stations, label="H_M_S_exact_output_height_comparison")


def make_tool_access_references(role: int = 2, spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM):
    refs = list(_motor_driver_tools(role, spec))
    for index, (x, y) in enumerate(
        (pair for x in spec.chassis_mount_x for y in spec.chassis_mount_y for pair in [(x, y)])
    ):
        tool = Cylinder(4.0, 25.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x, y, spec.gearbox_foot_z[1] + spec.chassis_screw_head_diameter / 2.0))
        )
        refs.append(_label(tool, f"M3_driver_access_{index+1}_KEEP_CLEAR", "#75C9D1"))
    refs.extend(
        _shaft_driver_tool(role, kind, spec)
        for kind in ("lower_collar", "vertical_miter", "output_pinion", "top_collar")
    )
    refs.append(_horizontal_bevel_driver_tool(role, spec))
    refs.extend(_bearing_cap_driver_tools(role, spec))
    return tuple(refs)


def make_shaft_insertion_swept_volume(
    role: int,
    spec: P3V3MotorStationAssemblySimSpec = P3_V3_MOTOR_STATION_ASSEMBLY_SIM,
):
    z0, z1 = spec.shaft_z(role)
    swept = _d_prism_z(
        spec.output_axis_x,
        z0,
        z1 + 45.0,
        spec.parent.output_shaft_diameter,
        spec.shaft_across_flat,
    )
    return _label(swept, f"{spec.parent.roles[role]}_shaft_insertion_swept_volume", "#75C9D1")
