"""Source-first Build123d geometry for KAGE M1.

The module intentionally owns no predecessor geometry.  Purchased fasteners and
the provisional motor are represented only by equations/tests, not printable
assembly occurrences.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin, degrees

import py_gearworks as pgw
from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude

from cadgen import srgb

from .spec import M1, M1B, RoleSpec


def one_solid(shape, label: str):
    solids = list(shape.solids()) if shape is not None else []
    if len(solids) != 1:
        raise RuntimeError(f"{label}: expected one solid, got {len(solids)}")
    solid = solids[0]
    if not solid.is_valid or solid.volume <= 0:
        raise RuntimeError(f"{label}: invalid or non-positive solid")
    solid.label = label
    return solid


def volume(shape) -> float:
    return 0.0 if shape is None else float(sum(s.volume for s in shape.solids()))


def intersection_volume(a, b) -> float:
    return volume(deepcopy(a).intersect(deepcopy(b)))


def polar(radius: float, angle_deg: float) -> tuple[float, float]:
    angle = radians(angle_deg)
    return radius * cos(angle), radius * sin(angle)


def local_point(angle_deg: float, radius: float, tangent: float = 0.0):
    angle = radians(angle_deg)
    return (
        radius * cos(angle) - tangent * sin(angle),
        radius * sin(angle) + tangent * cos(angle),
    )


def local_box(angle: float, r0: float, r1: float, t0: float, t1: float,
              z0: float, z1: float):
    return Box(r1 - r0, t1 - t0, z1 - z0,
               align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((r0, t0, z0))
    ).rotate(Axis.Z, angle)


def vertical_cylinder(angle: float, radius: float, tangent: float,
                      diameter: float, z0: float, z1: float):
    x, y = local_point(angle, radius, tangent)
    return Cylinder(diameter / 2.0, z1 - z0,
                    align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x, y, z0))
    )


def hex_prism(angle: float, radius: float, tangent: float, across_flats: float,
              z0: float, z1: float):
    circumradius = across_flats / (2.0 * cos(radians(30.0)))
    points = tuple(
        (radius + circumradius * cos(radians(30.0 + 60.0 * i)),
         tangent + circumradius * sin(radians(30.0 + 60.0 * i)))
        for i in range(6)
    )
    return extrude(Polygon(*points), amount=z1 - z0).moved(
        Location((0.0, 0.0, z0))
    ).rotate(Axis.Z, angle)


def sector_mask(start: float, span: float, z0: float = -5.0, z1: float = 55.0,
                radius: float = 170.0):
    points = [(0.0, 0.0)]
    for i in range(97):
        points.append(polar(radius, start + span * i / 96.0))
    points.append((0.0, 0.0))
    return extrude(Polygon(*points), amount=z1 - z0).moved(Location((0, 0, z0)))


def annulus(r0: float, r1: float, z0: float, z1: float):
    outer = Cylinder(r1, z1 - z0,
                     align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0)))
    inner = Cylinder(r0, z1 - z0 + 0.4,
                     align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0 - 0.2)))
    return outer.cut(inner)


def capsule_slot(angle: float, radius: float, tangent: float, width: float,
                 overall_length: float, z0: float, z1: float):
    spacing = overall_length - width
    bar = local_box(angle, radius - spacing / 2.0, radius + spacing / 2.0,
                    tangent - width / 2.0, tangent + width / 2.0, z0, z1)
    ends = [vertical_cylinder(angle, radius + d, tangent, width, z0, z1)
            for d in (-spacing / 2.0, spacing / 2.0)]
    return one_solid(bar.fuse(*ends), "capsule_slot_tool")


# ---------------------------------------------------------------------------
# Base quadrants


@lru_cache(maxsize=1)
def full_base():
    return one_solid(annulus(M1.base_inner_radius, M1.base_outer_radius, 0, M1.base_thickness),
                     f"{M1.namespace}_base_source_annulus")


def _base_plain(index: int):
    start = -45.0 + 90.0 * index
    return one_solid(deepcopy(full_base()).intersect(sector_mask(start, 90.0, -0.2, 6.2)),
                     f"{M1.namespace}_base_Q{index + 1}_plain")


@lru_cache(maxsize=4)
def base_quadrant(index: int):
    if index not in range(4):
        raise ValueError("base quadrant index must be 0..3")
    shape = _base_plain(index)
    start = -45.0 + 90.0 * index
    end = start + 90.0

    # End seam owns the upper 3 mm tongue; start seam receives the prior tongue.
    donor = local_box(end, M1.base_lap_r0, M1.base_lap_r1,
                      -0.5, M1.base_lap_half_t,
                      M1.base_lap_split_z, M1.base_thickness)
    receiver_cut = local_box(start, M1.base_lap_r0 - M1.base_lap_edge_clearance,
                             M1.base_lap_r1 + M1.base_lap_edge_clearance,
                             -M1.base_lap_edge_clearance,
                             M1.base_lap_half_t + M1.base_lap_edge_clearance,
                             M1.base_lap_split_z, M1.base_thickness + 0.2)
    shape = one_solid(shape.fuse(donor).cut(receiver_cut),
                      f"{M1.namespace}_base_Q{index + 1}")

    # Each end donor carries the two vertical screw paths and bottom captive nuts.
    for radius in M1.base_screw_radii:
        bore = vertical_cylinder(end, radius, M1.base_lap_half_t / 2.0,
                                 M1.m3_clearance_diameter, M1.bottom_skin, 6.2)
        head = vertical_cylinder(end, radius, M1.base_lap_half_t / 2.0,
                                 M1.m3_head_diameter, 3.0, 6.2)
        nut = hex_prism(end, radius, M1.base_lap_half_t / 2.0,
                        M1.m3_nut_af, M1.bottom_skin, M1.bottom_skin + M1.m3_nut_depth)
        access = local_box(end, radius - M1.m3_nut_af / 2.0,
                           radius + M1.m3_nut_af / 2.0,
                           M1.base_lap_half_t / 2.0,
                           M1.base_lap_half_t + 0.4,
                           M1.bottom_skin, M1.bottom_skin + M1.m3_nut_depth)
        shape = one_solid(shape.cut(bore, head, nut, access),
                          f"{M1.namespace}_base_Q{index + 1}")
    shape.color = srgb("#B8B0A3")
    return shape


# ---------------------------------------------------------------------------
# Ring sectors


def _role_index(role: str | int) -> int:
    if isinstance(role, int):
        if role not in range(3):
            raise ValueError("role index must be 0..2")
        return role
    names = tuple(r.name for r in M1.roles)
    return names.index(role)


@lru_cache(maxsize=3)
def full_role_ring(role: str | int):
    index = _role_index(role)
    spec = M1.roles[index]
    teeth = pgw.SpurRingGear(
        number_of_teeth=M1.ring_teeth,
        module=M1.gear_module,
        height=spec.body_z1 - spec.relief_z1,
        center=[0.0, 0.0, spec.relief_z1],
        backlash=0.10,
    ).build_part().solid().rotate(Axis.Z, M1.tooth_phase_deg)
    body = annulus(M1.ring_root_radius, M1.ring_outer_radius,
                   spec.body_z0, spec.body_z1)
    race = annulus(M1.race_radius, M1.ring_root_radius,
                   spec.body_z0, spec.race_z1)
    ring = one_solid(body.fuse(race, teeth),
                     f"{M1.namespace}_{spec.name}_full_258T_source")
    ring.color = srgb(spec.color)
    return ring


def _fin(role_index: int):
    role = M1.roles[role_index]
    half_angle = degrees((role.fin_width / 2.0) / ((M1.fin_r0 + M1.fin_r1) / 2.0))
    fin = annulus(M1.fin_r0, M1.fin_r1, role.body_z0, role.fin_z1).intersect(
        sector_mask(-half_angle, 2.0 * half_angle, role.body_z0 - 0.2, role.fin_z1 + 0.2)
    )
    return one_solid(fin, f"{M1.namespace}_{role.name}_fin")


def _joint_pad(role_index: int, seam_angle: float):
    role = M1.roles[role_index]
    pad = local_box(seam_angle, role.pad_r0, role.pad_r1,
                    -M1.lap_half, M1.lap_half, role.pad_z0, role.pad_z1)
    if role.name == "minute":
        neck = local_box(seam_angle, M1.minute_neck_r0, M1.minute_neck_r1,
                         -M1.lap_half, 0.0, M1.minute_neck_z0, M1.minute_neck_z1)
        pad = pad.fuse(neck)
    return one_solid(pad, f"{M1.namespace}_{role.name}_joint_pad")


def _ring_joint_cut(shape, role_index: int, seam_angle: float, owner_end: bool):
    """Make a printable complementary axial lap within one localized pad.

    The ending sector owns the lower half and the starting sector owns the upper
    half.  Each pad remains connected through its body-overlap lane (or the
    frozen minute neck) before the cuts are made.
    """
    role = M1.roles[role_index]
    split = (role.pad_z0 + role.pad_z1) / 2.0
    if owner_end:
        # Keep the complete pad on the owning (negative-tangent) side and only
        # lower the extension that crosses the seam.
        remove = local_box(seam_angle, role.pad_r0 - 0.2, role.pad_r1 + 0.2,
                           M1.seam_clearance_total / 2.0, M1.lap_half + 0.2,
                           split + M1.seam_clearance_total / 2.0, role.pad_z1 + 0.2)
    else:
        # The receiving sector retains only the upper crossing lap on the
        # positive-tangent side.  Delete its duplicate pad on the previous
        # sector's negative-tangent ownership side.
        remove = local_box(seam_angle, role.pad_r0 - 0.2, role.pad_r1 + 0.2,
                           M1.seam_clearance_total / 2.0, M1.lap_half + 0.2,
                           role.pad_z0 - 0.2, split - M1.seam_clearance_total / 2.0)
        duplicate = local_box(seam_angle, role.pad_r0 - 0.2, role.pad_r1 + 0.2,
                              -M1.lap_half - 0.2, -M1.seam_clearance_total / 2.0,
                              role.pad_z0 - 0.2, role.pad_z1 + 0.2)
        shape = shape.cut(duplicate)
    shape = shape.cut(remove)
    screw_t = M1.lap_half / 2.0
    bore = vertical_cylinder(seam_angle, (role.pad_r0 + role.pad_r1) / 2.0,
                             screw_t, M1.m3_clearance_diameter,
                             role.pad_z0 - 0.2, role.pad_z1 + 0.2)
    shape = shape.cut(bore)
    if not owner_end:
        head = vertical_cylinder(seam_angle, (role.pad_r0 + role.pad_r1) / 2.0,
                                 screw_t, M1.m3_head_diameter,
                                 role.pad_z1 - M1.m3_head_depth, role.pad_z1 + 0.2)
        shape = shape.cut(head)
    else:
        nut_z1 = split - M1.seam_clearance_total / 2.0
        nut = hex_prism(seam_angle, (role.pad_r0 + role.pad_r1) / 2.0,
                        screw_t, M1.m3_nut_af,
                        nut_z1 - M1.m3_nut_depth, nut_z1)
        access = local_box(seam_angle,
                           (role.pad_r0 + role.pad_r1) / 2.0 - M1.m3_nut_af / 2.0,
                           (role.pad_r0 + role.pad_r1) / 2.0 + M1.m3_nut_af / 2.0,
                           0.0, M1.lap_half + 0.4,
                           nut_z1 - M1.m3_nut_depth, nut_z1)
        shape = shape.cut(nut, access)
    return shape


@lru_cache(maxsize=9)
def _ring_sector_raw(role: str | int, sector_index: int):
    role_index = _role_index(role)
    if sector_index not in range(3):
        raise ValueError("sector index must be 0..2")
    role_spec = M1.roles[role_index]
    start = M1.sector_start_deg + M1.sector_span_deg * sector_index
    end = start + M1.sector_span_deg
    raw = deepcopy(full_role_ring(role_index)).intersect(
        sector_mask(start, M1.sector_span_deg, role_spec.pad_z0 - 1.0, role_spec.pad_z1 + 1.0)
    )
    if not raw:
        raise RuntimeError("sector crop produced no solid")
    sector = max(raw.solids(), key=lambda s: s.volume)
    # Every sector owns one complete fin in its uninterrupted center only on the
    # role-selected sector; the other sectors remain plain.
    fin_sector = role_index  # separated angles for assembled inspection
    if sector_index == fin_sector:
        sector = sector.fuse(_fin(role_index).rotate(Axis.Z, 120.0 * role_index))

    # Each sector carries a pad at both ends.  Complementary Z laps make the
    # assembled joint; union-before-cut keeps each sector a connected solid.
    start_pad = _joint_pad(role_index, start)
    end_pad = _joint_pad(role_index, end)
    sector = sector.fuse(start_pad, end_pad)
    sector = _ring_joint_cut(sector, role_index, start, owner_end=False)
    sector = _ring_joint_cut(sector, role_index, end, owner_end=True)
    label = f"{M1.namespace}_{role_spec.name}_sector_{sector_index + 1}_86T"
    result = one_solid(sector, label)
    result.color = srgb(role_spec.color)
    return result


@lru_cache(maxsize=9)
def ring_sector(role: str | int, sector_index: int):
    """Finished sector with deterministic prior-joint ownership.

    Boolean kernels can retain a small common wedge where the exact involute
    root and the localized crossing pad meet.  The preceding sector owns that
    joint.  Cutting the measured common BREP from the receiving sector makes
    the exported parts genuinely disjoint instead of merely trusting interval
    arithmetic.
    """
    role_index = _role_index(role)
    shape = deepcopy(_ring_sector_raw(role_index, sector_index))
    previous = _ring_sector_raw(role_index, (sector_index - 1) % 3)
    common = list(deepcopy(shape).intersect(deepcopy(previous)).solids())
    if common:
        shape = shape.cut(Compound(children=common))
    label = f"{M1.namespace}_{M1.roles[role_index].name}_sector_{sector_index + 1}_86T"
    solids = list(shape.solids())
    if len(solids) > 1:
        # Exact removal can leave a microscopic seam-boundary remnant.  It is
        # not a printable occurrence; retain the connected structural sector.
        shape = max(solids, key=lambda solid: solid.volume)
    result = one_solid(shape, label)
    result.color = srgb(M1.roles[role_index].color)
    return result


# ---------------------------------------------------------------------------
# Guide towers and printed rollers


@lru_cache(maxsize=2)
def tower_body(trim: bool = False):
    angle = 0.0
    foot = local_box(angle, M1.tower_foot_r0, M1.tower_foot_r1,
                     -M1.tower_foot_half_t, M1.tower_foot_half_t,
                     M1.tower_foot_z0, M1.tower_foot_z1)
    axle_boss = vertical_cylinder(angle, M1.tower_axle_radius, 0.0, 12.0,
                                  M1.tower_foot_z0, M1.tower_axle_under_head_z)
    shape = foot.fuse(axle_boss)
    # Axle screw head loads into a blind upward seat; shaft exits at Z18.
    head = vertical_cylinder(angle, M1.tower_axle_radius, 0.0,
                             M1.m3_head_diameter, 14.9, 18.0)
    axle = vertical_cylinder(angle, M1.tower_axle_radius, 0.0,
                             M1.m3_clearance_diameter, 17.8, 18.2)
    shape = shape.cut(head, axle)
    for tangent in M1.tower_mount_t:
        if trim:
            tool = capsule_slot(angle, 115.0, tangent, M1.m3_clearance_diameter,
                                M1.m3_clearance_diameter + M1.trim_total,
                                M1.tower_foot_z0 - 0.2, M1.tower_foot_z1 + 0.2)
        else:
            tool = vertical_cylinder(angle, 115.0, tangent, M1.m3_clearance_diameter,
                                     M1.tower_foot_z0 - 0.2, M1.tower_foot_z1 + 0.2)
        shape = shape.cut(tool)
    result = one_solid(shape, f"{M1.namespace}_guide_tower_{'trim' if trim else 'fixed'}")
    result.color = srgb("#58626A")
    return result


def placed_tower(index: int):
    angle = M1.tower_angles[index]
    shape = deepcopy(tower_body(trim=index == 2)).rotate(Axis.Z, angle)
    shape.label = f"{M1.namespace}_guide_tower_{index + 1}_{'trim' if index == 2 else 'fixed'}"
    return shape


@lru_cache(maxsize=3)
def roller_local(role: str | int):
    index = _role_index(role)
    role_spec = M1.roles[index]
    z0, z1 = M1.roller_z[index]
    groove0, groove1 = M1.roller_groove_z[index]
    lower = Cylinder(M1.roller_flange_radius, groove0 - z0,
                     align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0)))
    tread = Cylinder(M1.roller_tread_radius, groove1 - groove0,
                     align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, groove0)))
    upper = Cylinder(M1.roller_flange_radius, z1 - groove1,
                     align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, groove1)))
    bore = Cylinder(M1.roller_bore_diameter / 2.0, z1 - z0 + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0 - 0.2)))
    result = one_solid(lower.fuse(tread, upper).cut(bore),
                       f"{M1.namespace}_{role_spec.name}_roller")
    result.color = srgb(role_spec.color)
    return result


def placed_roller(role: str | int, tower_index: int):
    index = _role_index(role)
    angle = M1.tower_angles[tower_index]
    x, y = polar(M1.tower_axle_radius, angle)
    shape = deepcopy(roller_local(index)).moved(Location((x, y, 0)))
    shape.label = f"{M1.namespace}_{M1.roles[index].name}_roller_T{tower_index + 1}"
    return shape


# ---------------------------------------------------------------------------
# Assemblies and print layouts


def passive_parts():
    parts = []
    parts.extend((f"base_Q{i + 1}", deepcopy(base_quadrant(i))) for i in range(4))
    for role_index, role in enumerate(M1.roles):
        parts.extend((f"{role.name}_sector_{i + 1}", deepcopy(ring_sector(role_index, i)))
                     for i in range(3))
    parts.extend((f"guide_tower_{i + 1}", placed_tower(i)) for i in range(3))
    for tower_index in range(3):
        parts.extend((f"{role.name}_roller_T{tower_index + 1}",
                      placed_roller(role_index, tower_index))
                     for role_index, role in enumerate(M1.roles))
    if len(parts) != M1.passive_part_count:
        raise RuntimeError(f"passive manifest mismatch: {len(parts)}")
    for label, shape in parts:
        shape.label = f"{M1.namespace}_{label}"
    return tuple(parts)


def passive_assembled():
    return Compound(children=[shape for _, shape in passive_parts()],
                    label=f"{M1.namespace}_assembled_25_printed_parts")


def passive_table_assembly():
    children = [shape for _, shape in passive_parts()]
    table = Cylinder(152.0, 0.20, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, -0.20)))
    table.label = f"{M1.namespace}_table_plane_REFERENCE"
    table.color = srgb("#E7E1D7", 0.35)
    children.append(table)
    return Compound(children=children, label=f"{M1.namespace}_table_assembly")


def passive_exploded():
    children = []
    for label, shape in passive_parts():
        moved = deepcopy(shape)
        if label.startswith("base_"):
            index = int(label[-1]) - 1
            x, y = polar(18.0, 45.0 + 90.0 * index)
            moved = moved.moved(Location((x, y, 0)))
        elif "sector" in label:
            role_index = next(i for i, r in enumerate(M1.roles) if label.startswith(r.name))
            moved = moved.moved(Location((0, 0, 18.0 + 12.0 * role_index)))
        elif "tower" in label:
            moved = moved.moved(Location((0, 0, -8.0)))
        elif "roller" in label:
            role_index = next(i for i, r in enumerate(M1.roles) if label.startswith(r.name))
            moved = moved.moved(Location((0, 0, 35.0 + 8.0 * role_index)))
        moved.label = f"{label}_exploded"
        children.append(moved)
    return Compound(children=children, label=f"{M1.namespace}_bottom_up_exploded")


def sector_print_layout():
    children = []
    x_slots = (-280.0, 0.0, 280.0)
    y_slots = (-280.0, 0.0, 280.0)
    count = 0
    for role_index, role in enumerate(M1.roles):
        for sector_index in range(3):
            shape = deepcopy(ring_sector(role_index, sector_index)).rotate(Axis.Z, -120.0 * sector_index)
            box = shape.bounding_box()
            cx = (box.min.X + box.max.X) / 2.0
            cy = (box.min.Y + box.max.Y) / 2.0
            shape = shape.moved(Location((x_slots[sector_index] - cx,
                                          y_slots[role_index] - cy,
                                          -box.min.Z)))
            shape.label = f"{M1.namespace}_{role.name}_sector_{sector_index + 1}_print"
            children.append(shape)
            count += 1
    return Compound(children=children, label=f"{M1.namespace}_nine_sector_print_layout")


# ---------------------------------------------------------------------------
# Separate M1B provisional motor mesh


def motor_station(q: float = 0.0):
    if abs(q) > M1B.adjustment + 1e-9:
        raise ValueError("motor adjustment outside +/-3 mm")
    plate = local_box(0.0, M1B.station_r0 + q, M1B.station_r1 + q,
                      -M1B.station_half_t, M1B.station_half_t,
                      M1B.station_plate_z0, M1B.station_plate_z1)
    for tangent in (-7.7, 7.7):
        plate = plate.cut(capsule_slot(0.0, 114.0 + q, tangent, M1B.slot_width,
                                      M1B.slot_overall_length,
                                      M1B.station_plate_z0 - 0.2,
                                      M1B.station_plate_z1 + 0.2))
    result = one_solid(plate, f"{M1B.namespace}_adjustable_motor_station_q{q:+.2f}")
    result.color = srgb("#637C8A")
    return result


def provisional_pinion(face_z0: float = M1.roles[0].relief_z1,
                        face_z1: float = M1.roles[0].body_z1,
                        q: float = 0.0):
    ring_reference = pgw.SpurRingGear(
        number_of_teeth=M1.ring_teeth, module=M1.gear_module,
        height=face_z1 - face_z0, center=[0, 0, face_z0], backlash=0.10,
    )
    gear = pgw.SpurGear(
        number_of_teeth=M1B.pinion_teeth, module=M1.gear_module,
        height=face_z1 - face_z0, center=[0, 0, face_z0],
        pressure_angle=radians(M1B.pressure_angle_deg), backlash=0.10,
        enable_undercut=True,
    )
    gear.mesh_to(ring_reference, target_dir=pgw.RIGHT, backlash=0.10)
    shape = gear.build_part().solid().moved(Location((q, 0, 0)))
    bore = Cylinder(M1B.provisional_shaft_diameter / 2.0,
                    face_z1 - face_z0 + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((M1B.nominal_center_distance + q, 0, face_z0 - 0.2))
    )
    result = one_solid(shape.cut(bore), f"{M1B.namespace}_18T_pinion_PROVISIONAL")
    result.color = srgb("#D9A72E")
    return result


def motor_bench(q: float = 0.0):
    return Compound(children=[motor_station(q), provisional_pinion(q=q)],
                    label=f"{M1B.namespace}_bench_q{q:+.2f}")


def motor_bench_three_positions():
    children = []
    for i, q in enumerate((-3.0, 0.0, 3.0)):
        bench = motor_bench(q).moved(Location((0, i * 80.0, 0)))
        bench.label = f"{M1B.namespace}_q{q:+.1f}_REFERENCE"
        children.append(bench)
    return Compound(children=children, label=f"{M1B.namespace}_three_adjustment_positions")
