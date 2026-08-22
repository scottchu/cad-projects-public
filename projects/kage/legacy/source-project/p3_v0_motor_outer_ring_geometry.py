"""STEP-first build123d geometry for the KAGE P3 V0 motor outer ring."""

from __future__ import annotations

from math import ceil, cos, degrees, radians, sin

from build123d import Align, AngularDirection, Axis, Box, BuildPart, BuildSketch, Compound, Cylinder, Edge, Face, Location, Plane, Polygon, Vector, Wire, extrude, revolve

from p3_v0_motor_outer_ring_spec import P3V0MotorOuterRingSpec, P3_V0


def _polar(radius: float, angle_deg: float) -> tuple[float, float]:
    a = radians(angle_deg)
    return radius * cos(a), radius * sin(a)


def _sector_face(inner: float, outer: float, start: float, end: float, z: float = 0.0):
    segments = max(18, ceil(abs(end - start) * 2.0))
    angles = [start + (end - start) * i / segments for i in range(segments + 1)]
    points = [Vector(*_polar(outer, angle), z) for angle in angles]
    points.extend(Vector(*_polar(inner, angle), z) for angle in reversed(angles))
    return Face(Wire.make_polygon(points, close=True))


def _sector(inner: float, outer: float, start: float, end: float, height: float, z0: float = 0.0):
    return extrude(_sector_face(inner, outer, start, end), amount=height).moved(Location((0, 0, z0)))


def _exact_sector(inner: float, outer: float, start: float, end: float, height: float, z0: float = 0.0):
    outer_arc = Edge.make_circle(outer, Plane.XY, start, end)
    outer_end = Vector(*_polar(outer, end), 0.0)
    inner_end = Vector(*_polar(inner, end), 0.0)
    inner_start = Vector(*_polar(inner, start), 0.0)
    outer_start = Vector(*_polar(outer, start), 0.0)
    inner_arc = Edge.make_circle(inner, Plane.XY, end, start, AngularDirection.CLOCKWISE)
    wire = Wire(
        [
            outer_arc,
            Edge.make_line(outer_end, inner_end),
            inner_arc,
            Edge.make_line(inner_start, outer_start),
        ]
    )
    return extrude(Face(wire), amount=height).moved(Location((0, 0, z0)))


def _annulus(inner: float, outer: float, height: float, z0: float = 0.0):
    outer_body = Cylinder(outer, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0)))
    inner_tool = Cylinder(inner, height + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0 - 0.2)))
    return outer_body.cut(inner_tool)


def _cylinder(radius: float, height: float, z0: float = 0.0):
    return Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0)))


def _fuse_all(shapes):
    iterator = iter(shapes)
    result = next(iterator)
    for shape in iterator:
        result = result.fuse(shape)
    return result


def _oriented_box(radial: float, tangential: float, height: float, radius: float, angle: float, z0: float):
    part = Box(radial, tangential, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((radius, 0, z0))
    )
    return part.rotate(Axis.Z, angle)


def _dogbone_shape(angle: float, radial_end: float, radial_neck: float, tangential_length: float, end_length: float, height: float, z0: float, spec: P3V0MotorOuterRingSpec):
    neck_length = tangential_length - 2.0 * end_length
    end_center_offset = (tangential_length - end_length) / 2.0
    shapes = [
        _oriented_box(radial_neck, neck_length, height, spec.carrier_radius, angle, z0),
        _oriented_box(radial_end, end_length, height, spec.carrier_radius, angle, z0).moved(
            Location((*_polar(end_center_offset, angle + 90.0), 0.0))
        ),
        _oriented_box(radial_end, end_length, height, spec.carrier_radius, angle, z0).moved(
            Location((*_polar(end_center_offset, angle - 90.0), 0.0))
        ),
    ]
    return _fuse_all(shapes)


def make_carrier_joint_key(spec: P3V0MotorOuterRingSpec = P3_V0):
    key = _dogbone_shape(
        0.0,
        spec.key_end_radial,
        spec.key_neck_radial,
        spec.key_tangential_length,
        spec.key_end_tangential,
        spec.key_thickness,
        spec.key_installed_z[0],
        spec,
    )
    key.label = "p3_v0_carrier_top_dogbone_key"
    return key


def _key_pocket(angle: float, spec: P3V0MotorOuterRingSpec):
    return _dogbone_shape(
        angle,
        spec.key_end_radial + 2 * spec.key_xy_clearance_per_side,
        spec.key_neck_radial + 2 * spec.key_xy_clearance_per_side,
        spec.key_tangential_length + 2 * spec.key_xy_clearance_per_side,
        spec.key_end_tangential + spec.key_xy_clearance_per_side,
        spec.key_pocket_depth + 0.2,
        spec.spine_z[1] - spec.key_pocket_depth,
        spec,
    )


def _pointed_fin(angle: float, spec: P3V0MotorOuterRingSpec):
    x0 = spec.carrier_radius - spec.fin_radial / 2.0
    # Sink the root into the spine by 0.20 mm so the boolean union is a
    # positive-volume connection, not a fragile coincident-face join.
    root_z = spec.spine_z[1] - 0.20
    points = ((x0, root_z), (x0 + spec.fin_radial, root_z), (spec.carrier_radius, spec.spine_z[1] + spec.fin_height))
    with BuildPart() as fin_builder:
        with BuildSketch(Plane.XZ):
            Polygon(*points)
        extrude(amount=spec.fin_tangential / 2.0, both=True)
    fin = fin_builder.part
    return fin.rotate(Axis.Z, angle)


def make_carrier_segment(index: int, spec: P3V0MotorOuterRingSpec = P3_V0):
    start, end = spec.segment_extents[index]
    flange = _sector(*spec.flange_radii, start, end, spec.flange_z[1] - spec.flange_z[0], spec.flange_z[0])
    spine = _sector(*spec.spine_radii, start, end, spec.spine_z[1] - spec.spine_z[0], spec.spine_z[0])
    segment = flange.fuse(spine)

    for seam in (start, end):
        segment = segment.cut(_key_pocket(seam, spec))

    suffix = "a"
    if index == 1:
        x, y = _polar(spec.carrier_radius, spec.hall_magnet_angle)
        pocket = _cylinder(spec.hall_pocket_diameter / 2.0, spec.hall_pocket_depth + 0.05, spec.flange_z[0] - 0.01).moved(Location((x, y, 0)))
        segment = segment.cut(pocket)
        suffix = "b_hall"
    elif index == 2:
        segment = segment.fuse(_pointed_fin(spec.fin_angle, spec))
        suffix = "c_fin"
    segment.label = f"p3_v0_carrier_segment_{suffix}_120deg"
    return segment


def placed_joint_key(angle: float, spec: P3V0MotorOuterRingSpec = P3_V0):
    return make_carrier_joint_key(spec).rotate(Axis.Z, angle)


def make_frame_splice_plate(spec: P3V0MotorOuterRingSpec = P3_V0):
    half_angle = degrees(spec.splice_arc_length / ((spec.splice_radii[0] + spec.splice_radii[1]) / 2.0)) / 2.0
    splice = _sector(*spec.splice_radii, -half_angle, half_angle, spec.splice_z[1] - spec.splice_z[0], spec.splice_z[0])
    for offset in spec.splice_hole_tangential_offsets:
        angle = degrees(offset / ((spec.splice_radii[0] + spec.splice_radii[1]) / 2.0))
        x, y = _polar((spec.splice_radii[0] + spec.splice_radii[1]) / 2.0, angle)
        splice = splice.cut(_cylinder(spec.splice_hole_diameter / 2.0, 2.4, spec.splice_z[0] - 0.2).moved(Location((x, y, 0))))
    splice.label = "p3_v0_frame_rear_splice_two_m3"
    return splice


def _guide_station(angle: float, spec: P3V0MotorOuterRingSpec):
    half_angle = degrees(spec.guide_arc_length / spec.carrier_radius) / 2.0
    start, end = angle - half_angle, angle + half_angle

    # Outer-sided capture guide.  The floor and wall are the only centering
    # surfaces; there is deliberately no disconnected inner lip and no fixed
    # material inside the r=130 mm optical/mechanical keep-clear circle.
    floor = _exact_sector(
        *spec.guide_floor_radii,
        start,
        end,
        spec.guide_floor_z[1] - spec.guide_floor_z[0],
        spec.guide_floor_z[0],
    )
    outer_wall = _exact_sector(
        *spec.guide_outer_wall_radii,
        start,
        end,
        spec.guide_outer_wall_z[1] - spec.guide_outer_wall_z[0],
        spec.guide_outer_wall_z[0],
    )

    # Revolve the exact 45-degree support-free lip cross-section, then rotate
    # the finite arc into the requested station.
    lip_profile = Face(
        Wire.make_polygon(
            [
                Vector(spec.guide_lip_radii[0], 0.0, spec.guide_lip_top_z),
                Vector(spec.guide_lip_radii[1], 0.0, spec.guide_lip_top_z),
                Vector(spec.guide_lip_radii[1], 0.0, spec.guide_lip_outer_underside_z),
                Vector(140.00, 0.0, spec.guide_lip_outer_underside_z),
            ],
            close=True,
        )
    )
    lip = revolve(lip_profile, axis=Axis.Z, revolution_arc=end - start).rotate(Axis.Z, start)
    return _fuse_all([floor, outer_wall, lip])


def _hole_at(radius: float, angle: float, diameter: float, z0: float, height: float):
    x, y = _polar(radius, angle)
    return _cylinder(diameter / 2.0, height, z0).moved(Location((x, y, 0)))


def _seam_hole_tools(seam_angle: float, spec: P3V0MotorOuterRingSpec):
    radius = (spec.splice_radii[0] + spec.splice_radii[1]) / 2.0
    return [
        _hole_at(radius, seam_angle + degrees(offset / radius), spec.splice_hole_diameter, -2.2, 4.9)
        for offset in spec.splice_hole_tangential_offsets
    ]


def make_frame_quadrant(index: int, spec: P3V0MotorOuterRingSpec = P3_V0):
    start, end = spec.frame_quadrant_extents[index]
    quadrant = _sector(*spec.frame_radii, start, end, spec.frame_z[1] - spec.frame_z[0], spec.frame_z[0])
    for guide_angle in spec.guide_angles:
        normalized = guide_angle if guide_angle <= 315 else guide_angle - 360
        if start - 1e-6 <= normalized <= end + 1e-6:
            quadrant = quadrant.fuse(_guide_station(guide_angle, spec))
    for seam in (start, end):
        normalized = seam % 360
        if normalized in spec.frame_seam_angles:
            quadrant = quadrant.cut(_fuse_all(_seam_hole_tools(normalized, spec)))
    for idler_angle in spec.idler_angles:
        normalized = idler_angle if idler_angle <= 315 else idler_angle - 360
        if start - 1e-6 <= normalized <= end + 1e-6:
            quadrant = quadrant.cut(
                _slot_tool(
                    spec.idler_slot_length,
                    spec.idler_bore_diameter,
                    0.0,
                    spec.idler_axis_radius_nominal,
                    idler_angle,
                    spec.frame_z[0] - 0.2,
                    spec.frame_z[1] - spec.frame_z[0] + 0.4,
                )
            )
    if start <= spec.motor_angle <= end:
        for offset in (-spec.motor_slot_spacing_tangential / 2.0, spec.motor_slot_spacing_tangential / 2.0):
            quadrant = quadrant.cut(
                _slot_tool(
                    spec.motor_frame_slot_length,
                    spec.splice_hole_diameter,
                    0.0,
                    spec.motor_axis_radius_nominal,
                    spec.motor_angle,
                    spec.frame_z[0] - 0.2,
                    spec.frame_z[1] - spec.frame_z[0] + 0.4,
                ).moved(Location((*_polar(offset, spec.motor_angle + 90.0), 0.0)))
            )
    if start <= spec.hall_angle <= end:
        for offset in spec.hall_fastener_tangential_offsets:
            shift = _polar(offset, spec.hall_angle + 90.0)
            x, y = _polar(spec.hall_fastener_radius, spec.hall_angle)
            quadrant = quadrant.cut(
                _cylinder(spec.hall_mount_slot_diameter / 2.0, 2.8, -0.2).moved(
                    Location((x + shift[0], y + shift[1], 0.0))
                )
            )
    suffixes = ("a_guides", "b_hall", "c_guides", "d_motor")
    quadrant.label = f"p3_v0_frame_quadrant_{suffixes[index]}"
    return quadrant


def _slot_tool(radial_length: float, width: float, tangential_offset: float, radius: float, angle: float, z0: float, height: float):
    box = _oriented_box(max(radial_length - width, 0.01), width, height, radius, angle, z0)
    end_offset = (radial_length - width) / 2.0
    ends = [
        _hole_at(radius + end_offset, angle, width, z0, height),
        _hole_at(radius - end_offset, angle, width, z0, height),
    ]
    return _fuse_all([box, *ends])


def make_motor_slide_cradle(spec: P3V0MotorOuterRingSpec = P3_V0):
    angle = spec.motor_angle
    radius = spec.motor_axis_radius_nominal
    plate = _oriented_box(28.0, 28.0, 3.0, radius, angle, spec.motor_face_z - 3.0)
    # Integral ears overlap the plate by 0.20 mm and abut the frame rear at
    # z=0. M3 bolts pass through round ear holes and the frame's radial slots.
    ears = [
        _oriented_box(
            spec.motor_ear_radial,
            spec.motor_ear_tangential,
            spec.motor_ear_z[1] - spec.motor_ear_z[0],
            radius,
            angle,
            spec.motor_ear_z[0],
        ).moved(
            Location((*_polar(offset, angle + 90), 0))
        )
        for offset in (-spec.motor_slot_spacing_tangential / 2.0, spec.motor_slot_spacing_tangential / 2.0)
    ]
    cradle = _fuse_all([plate, *ears])
    x, y = _polar(radius, angle)
    cradle = cradle.cut(
        _cylinder(spec.motor_pilot_relief_diameter / 2.0, 1.8, -6.1).moved(Location((x, y, 0)))
    )
    half_pitch = spec.motor_mount_pitch / 2.0
    for rx in (-half_pitch, half_pitch):
        for ty in (-half_pitch, half_pitch):
            dx, dy = _polar(rx, angle)
            tx, tty = _polar(ty, angle + 90)
            cradle = cradle.cut(_cylinder(spec.motor_mount_clearance_diameter / 2.0, 3.4, spec.motor_face_z - 3.2).moved(Location((x + dx + tx, y + dy + tty, 0))))
    for offset in (-spec.motor_slot_spacing_tangential / 2.0, spec.motor_slot_spacing_tangential / 2.0):
        shift = _polar(offset, angle + 90.0)
        cradle = cradle.cut(
            _cylinder(spec.splice_hole_diameter / 2.0, 7.9, spec.motor_face_z - 3.2).moved(
                Location((x + shift[0], y + shift[1], 0.0))
            )
        )
    cradle.label = "p3_v0_nema8_radial_slide_cradle_provisional_fit"
    return cradle


def make_drive_wheel(spec: P3V0MotorOuterRingSpec = P3_V0):
    wheel = _cylinder(spec.drive_hub_diameter / 2.0, spec.drive_contact_width, spec.drive_z[0])
    wheel = wheel.cut(_cylinder(spec.drive_shaft_bore_diameter / 2.0, spec.drive_contact_width + 0.4, spec.drive_z[0] - 0.2))
    # Split and transverse pinch-bolt clearance make this a compliant clamp hub.
    wheel = wheel.cut(Box(3.6, 0.6, spec.drive_contact_width + 0.4, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((2.0, 0, spec.drive_z[0] - 0.2))))
    pinch = Cylinder(spec.drive_pinch_hole_diameter / 2.0, spec.drive_hub_diameter + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(Axis.X, 90).moved(Location((4.0, -spec.drive_hub_diameter / 2.0 - 0.2, sum(spec.drive_z) / 2.0)))
    wheel = wheel.cut(pinch)
    wheel.label = "p3_v0_petg_split_clamp_drive_hub_dshaft_provisional"
    return wheel


def make_drive_tire(spec: P3V0MotorOuterRingSpec = P3_V0):
    tire = _annulus(spec.drive_hub_diameter / 2.0, spec.drive_tire_diameter / 2.0, spec.drive_contact_width, spec.drive_z[0])
    tire.label = "p3_v0_optional_tpu_friction_tire_od12"
    return tire


def make_idler_wheel(spec: P3V0MotorOuterRingSpec = P3_V0):
    wheel = _annulus(
        spec.idler_bore_diameter / 2.0,
        spec.idler_hub_diameter / 2.0,
        spec.idler_contact_width,
        spec.idler_z[0],
    )
    wheel.label = "p3_v0_petg_passive_idler_hub_m3_running_bore_qty2"
    return wheel


def make_idler_tire(spec: P3V0MotorOuterRingSpec = P3_V0):
    tire = _annulus(
        spec.idler_hub_diameter / 2.0,
        spec.idler_tire_diameter / 2.0,
        spec.idler_contact_width,
        spec.idler_z[0],
    )
    tire.label = "p3_v0_tpu_passive_idler_tire_od8_qty2"
    return tire


def make_official_motor_reference(spec: P3V0MotorOuterRingSpec = P3_V0):
    body = Box(spec.motor_keepout_xy, spec.motor_keepout_xy, spec.motor_keepout_length, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(Location((0, 0, spec.motor_face_z)))
    pilot = _cylinder(8.0, 1.5, spec.motor_face_z)
    shaft = _cylinder(spec.motor_shaft_diameter / 2.0, spec.motor_shaft_length, spec.motor_face_z)
    ref = Compound(children=[body, pilot, shaft], label="REFERENCE_ONLY_OFFICIAL_8HS15_0604S_ENVELOPE_MEASURE_BEFORE_FIT")
    return ref


def make_hall_bracket(spec: P3V0MotorOuterRingSpec = P3_V0):
    angle = spec.hall_angle
    seat = _oriented_box(
        spec.hall_seat_radii[1] - spec.hall_seat_radii[0],
        spec.hall_seat_tangential,
        spec.hall_bracket_z[1] - spec.hall_bracket_z[0],
        sum(spec.hall_seat_radii) / 2.0,
        angle,
        spec.hall_bracket_z[0],
    )
    crossbar = _oriented_box(
        spec.hall_crossbar_radii[1] - spec.hall_crossbar_radii[0],
        spec.hall_crossbar_tangential,
        spec.hall_bracket_z[1] - spec.hall_bracket_z[0],
        sum(spec.hall_crossbar_radii) / 2.0,
        angle,
        spec.hall_bracket_z[0],
    )
    towers = [
        _oriented_box(
            spec.hall_tower_radii[1] - spec.hall_tower_radii[0],
            spec.hall_tower_tangential,
            spec.hall_tower_z[1] - spec.hall_tower_z[0],
            sum(spec.hall_tower_radii) / 2.0,
            angle,
            spec.hall_tower_z[0],
        ).moved(Location((*_polar(offset, angle + 90.0), 0.0)))
        for offset in spec.hall_fastener_tangential_offsets
    ]
    bracket = _fuse_all([seat, crossbar, *towers])
    for offset in spec.hall_fastener_tangential_offsets:
        shift = _polar(offset, angle + 90.0)
        x, y = _polar(spec.hall_fastener_radius, angle)
        hole = _cylinder(spec.hall_mount_slot_diameter / 2.0, 12.6, -12.4).moved(
            Location((x + shift[0], y + shift[1], 0.0))
        )
        bracket = bracket.cut(hole)
    bracket.label = "p3_v0_adjustable_drv5032_module_bracket_provisional_fit"
    return bracket


def make_hall_spacer_pad(spec: P3V0MotorOuterRingSpec = P3_V0):
    radial, tangential, _axial = spec.hall_module_envelope
    pad = _oriented_box(
        radial,
        tangential,
        spec.hall_spacer_nominal_thickness,
        spec.hall_seat_center_radius,
        spec.hall_angle,
        spec.hall_bracket_z[1],
    )
    pad.label = "p3_v0_removable_hall_gap_spacer_5mm_nominal"
    return pad


def make_hall_module_reference(spec: P3V0MotorOuterRingSpec = P3_V0):
    radial, tangential, axial = spec.hall_module_envelope
    module = _oriented_box(radial, tangential, axial, spec.hall_seat_center_radius, spec.hall_angle, -spec.hall_face_gap_nominal - axial + spec.flange_z[0] + spec.hall_rear_recess)
    module.label = "REFERENCE_ONLY_DRV5032_MODULE_15x10x5_MEASURE_BEFORE_FIT"
    return module


def _place_at_polar(shape, radius: float, angle: float):
    return shape.moved(Location((*_polar(radius, angle), 0)))


def make_assembled(spec: P3V0MotorOuterRingSpec = P3_V0):
    children = [make_frame_quadrant(i, spec) for i in range(4)]
    children.extend(make_frame_splice_plate(spec).rotate(Axis.Z, angle) for angle in spec.frame_seam_angles)
    children.extend(make_carrier_segment(i, spec) for i in range(3))
    children.extend(placed_joint_key(angle, spec) for angle in spec.seam_angles)
    children.append(make_motor_slide_cradle(spec).moved(Location((*_polar(spec.motor_axis_radius_start - spec.motor_axis_radius_nominal, spec.motor_angle), 0))))
    children.append(_place_at_polar(make_official_motor_reference(spec), spec.motor_axis_radius_start, spec.motor_angle))
    children.append(_place_at_polar(make_drive_wheel(spec), spec.motor_axis_radius_start, spec.motor_angle))
    children.append(_place_at_polar(make_drive_tire(spec), spec.motor_axis_radius_start, spec.motor_angle))
    for angle in spec.idler_angles:
        children.append(_place_at_polar(make_idler_wheel(spec), spec.idler_axis_radius_start, angle))
        children.append(_place_at_polar(make_idler_tire(spec), spec.idler_axis_radius_start, angle))
    children.append(make_hall_bracket(spec))
    children.append(make_hall_spacer_pad(spec))
    children.append(make_hall_module_reference(spec))
    return Compound(children=children, label="p3_v0_motor_outer_ring_full_assembly")


def make_exploded(spec: P3V0MotorOuterRingSpec = P3_V0):
    children = []
    for i in range(4):
        children.append(make_frame_quadrant(i, spec).moved(Location((0, 0, -4.0 - 3.0 * i))))
    for i, angle in enumerate(spec.frame_seam_angles):
        children.append(make_frame_splice_plate(spec).rotate(Axis.Z, angle).moved(Location((0, 0, -18.0 - 2.0 * i))))
    for i in range(3):
        children.append(make_carrier_segment(i, spec).moved(Location((0, 0, 12.0 + 9.0 * i))))
    for i, angle in enumerate(spec.seam_angles):
        children.append(placed_joint_key(angle, spec).moved(Location((0, 0, 42.0 + 3.0 * i))))
    children.extend([
        make_motor_slide_cradle(spec).moved(Location((0, 0, -12.0))),
        _place_at_polar(make_official_motor_reference(spec), spec.motor_axis_radius_start, spec.motor_angle).moved(Location((0, 0, -25.0))),
        _place_at_polar(make_drive_wheel(spec), spec.motor_axis_radius_start, spec.motor_angle).moved(Location((0, 0, 45.0))),
        _place_at_polar(make_drive_tire(spec), spec.motor_axis_radius_start, spec.motor_angle).moved(Location((0, 0, 49.0))),
        make_hall_bracket(spec).moved(Location((0, 0, -10.0))),
        make_hall_spacer_pad(spec).moved(Location((0, 0, -14.0))),
        make_hall_module_reference(spec).moved(Location((0, 0, -16.0))),
    ])
    for index, angle in enumerate(spec.idler_angles):
        children.append(
            _place_at_polar(make_idler_wheel(spec), spec.idler_axis_radius_start, angle).moved(
                Location((0, 0, 45.0 + 5.0 * index))
            )
        )
        children.append(
            _place_at_polar(make_idler_tire(spec), spec.idler_axis_radius_start, angle).moved(
                Location((0, 0, 48.0 + 5.0 * index))
            )
        )
    return Compound(children=children, label="p3_v0_motor_outer_ring_service_exploded")


def make_axial_section(spec: P3V0MotorOuterRingSpec = P3_V0):
    assembly = make_assembled(spec)
    slab = Box(330.0, 2.0, 120.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((0, 0, 5)))
    children = []
    for index, solid in enumerate(assembly.solids()):
        fragments = solid.intersect(slab) or []
        for fragment_index, section in enumerate(fragments):
            if section.volume > 1e-6:
                section.label = f"p3_v0_axial_section_solid_{index}_{fragment_index}"
                children.append(section)
    return Compound(children=children, label="p3_v0_motor_outer_ring_axial_section")


def pairwise_intersection_volume(a, b) -> float:
    total = 0.0
    for sa in a.solids():
        for sb in b.solids():
            fragments = sa.intersect(sb) or []
            total += sum(max(0.0, float(fragment.volume)) for fragment in fragments)
    return total


PRINTABLE_FACTORIES = (
    ("carrier_segment_a", lambda: make_carrier_segment(0)),
    ("carrier_segment_b_hall", lambda: make_carrier_segment(1)),
    ("carrier_segment_c_fin", lambda: make_carrier_segment(2)),
    ("carrier_joint_key", make_carrier_joint_key),
    ("frame_quadrant_a", lambda: make_frame_quadrant(0)),
    ("frame_quadrant_b_hall", lambda: make_frame_quadrant(1)),
    ("frame_quadrant_c", lambda: make_frame_quadrant(2)),
    ("frame_quadrant_d_motor", lambda: make_frame_quadrant(3)),
    ("frame_splice_plate", make_frame_splice_plate),
    ("motor_slide_cradle", make_motor_slide_cradle),
    ("drive_wheel", make_drive_wheel),
    ("drive_tire", make_drive_tire),
    ("idler_wheel", make_idler_wheel),
    ("idler_tire", make_idler_tire),
    ("hall_bracket", make_hall_bracket),
    ("hall_spacer_pad", make_hall_spacer_pad),
)
