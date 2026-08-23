"""build123d geometry for the P1 adjustable LED cartridge."""

from __future__ import annotations

from build123d import Align, Axis, Box, Compound, Cylinder, Location

from p1_adjustable_led_cartridge_spec import AdjustableLedCartridgeSpec, P1


def _box(x, y, z, at=(0.0, 0.0, 0.0)):
    return Box(x, y, z, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location(at))


def _cylinder(radius, height, z0=0.0):
    return Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, z0))
    )


def _fuse_all(shapes):
    iterator = iter(shapes)
    result = next(iterator)
    for shape in iterator:
        result = result.fuse(shape)
    return result


def make_rail_frame(spec: AdjustableLedCartridgeSpec = P1):
    rail_height = spec.rail_z_max - spec.rail_z_min
    rails = [
        _box(spec.rail_x_size, spec.rail_y_size, rail_height, (x, 0, spec.rail_z_min))
        for x in (-spec.rail_x, spec.rail_x)
    ]
    # All connectors lie at/beyond the x=+/-25 free-air boundary. The rear
    # crossbar and mounting ears sit behind y=-25, producing one fused body.
    frame_base_z = spec.rail_z_min - 2.0
    front_bar = _box(68, 8, 2, (0, -30, frame_base_z))
    rail_arms = [
        _box(spec.rail_x_size, 27.5, 2, (x, -16.25, frame_base_z))
        for x in (-spec.rail_x, spec.rail_x)
    ]
    # Stop shoulders are outboard of the sliding bearing envelopes.  Their top
    # face at z=34 contacts the carriage tabs only at source z=36.
    front_stops = [
        _box(4, 12, spec.front_stop_top_z - frame_base_z, (x, 0, frame_base_z))
        for x in (-34, 34)
    ]
    stop_base_connectors = [
        _box(5, 8, 2, (x, 0, frame_base_z)) for x in (-31.5, 31.5)
    ]
    mount_ears = [
        _box(10, 10, 2, (x, -30, frame_base_z)).cut(
            _cylinder(2.25, 4, frame_base_z - 1).moved(Location((x, -30, 0)))
        )
        for x in (-29, 29)
    ]
    frame = _fuse_all([*rails, front_bar, *rail_arms, *front_stops, *stop_base_connectors, *mount_ears])
    frame.label = "rail_frame_two_5mm_guides_50mm_useful_travel"
    return frame


def _bearing_block(x: float, clamp: bool, spec: AdjustableLedCartridgeSpec):
    body = _box(spec.bearing_outer_x, 12, spec.bearing_land, (x, 0, -spec.bearing_land / 2))
    guide = _box(
        spec.rail_x_clearance_size,
        spec.rail_clearance_size,
        spec.bearing_land + 2,
        (x, 0, -spec.bearing_land / 2 - 1),
    )
    body = body.cut(guide)
    if clamp:
        screw = Cylinder(
            spec.m4_clearance_diameter / 2,
            16,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).rotate(Axis.X, 90).moved(Location((x, 0, 0)))
        nut = _box(spec.m4_nut_af, spec.m4_nut_thickness + 0.8, spec.m4_nut_af, (x, 2.0, -spec.m4_nut_af / 2))
        body = body.cut(screw).cut(nut)
    return body


def make_moving_carriage(spec: AdjustableLedCartridgeSpec = P1):
    """Printable carriage in source-plane-local coordinates (LED plane z=0)."""
    bearings = [
        _bearing_block(-spec.rail_x, True, spec),
        _bearing_block(spec.rail_x, False, spec),
    ]
    # Structural links stay behind the LED/MCPCB plane and outside all hot
    # metal. They support four finite clips tangent to the heatsink x faces.
    side_links = [
        _box(7, 38, 4, (x, 0, -5.5)) for x in (-19.5, 19.5)
    ]
    transverse_links = [
        _box(47, 5, 4, (0, y, -5.5)) for y in (-18, 18)
    ]
    bearing_links = [
        _box(7, 6, 4, (x, 0, -5.5)) for x in (-24.5, 24.5)
    ]
    edge_clips = [
        _box(spec.edge_clip_depth, spec.edge_clip_width, 7.2, (x, y, -1.6))
        for x in (-(20 + spec.edge_clip_depth / 2), 20 + spec.edge_clip_depth / 2)
        for y in (-17, 17)
    ]
    clip_mount = _box(spec.clip_mount_size, spec.clip_mount_size, 5, (32, 16, -4.5))
    clip_mount.label = "cool_side_strain_relief_slide_peg_0p3_clearance"
    clip_mount_arm = _box(7, 4.4, 4, (26.5, 16, -4.5))
    # Outboard tabs establish hard-stop source planes without reducing the full
    # 12 mm guide engagement.
    stop_tabs = [
        _box(4.1, 8, 2 * spec.carriage_stop_tab_half_height, (x, 0, -spec.carriage_stop_tab_half_height))
        for x in (-33.95, 33.95)
    ]
    # Tabs join the bearing bodies at x=+/-32, so placement and BREP collision
    # checks treat each real stop as part of the moving solid.
    carriage = _fuse_all([
        *bearings, *side_links, *transverse_links, *bearing_links,
        *edge_clips, clip_mount, clip_mount_arm, *stop_tabs,
    ])
    carriage.label = "moving_carriage_petg_four_outer_heatsink_pads_m4_clamp"
    return carriage


def make_rear_service_bridge(spec: AdjustableLedCartridgeSpec = P1):
    # The crossbar lives behind the 5 mm free-air envelope (y <= -28). Long
    # outboard fingers reach the stop tabs without entering x=+/-25.
    crossbar = _box(68, 4, 8, (0, -30, 88))
    stop_fingers = [_box(4, 36, 8, (x, -12, 88)) for x in (-34, 34)]
    bridge = _fuse_all([crossbar, *stop_fingers])
    bridge.label = "rear_service_bridge_removable_anti_withdraw_max_stop"
    return bridge


def make_strain_relief_clip(spec: AdjustableLedCartridgeSpec = P1):
    body = _box(10, 8, 5)
    channel = _box(
        spec.clip_mount_size + 2 * spec.clip_mount_clearance,
        spec.clip_mount_size + 2 * spec.clip_mount_clearance,
        6,
        (0, 0, -0.5),
    )
    clip = body.cut(channel).cut(_box(2, 5, 6, (0, -4, -0.5)))
    clip.label = "optional_two_lead_strain_relief_clip"
    return clip


def placed_carriage(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    return make_moving_carriage(spec).moved(Location((0, 0, source_z)))


def placed_strain_relief(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    return make_strain_relief_clip(spec).moved(
        Location((32, 16, source_z - 4.5))
    )


def make_mcpcb_reference(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    shape = _cylinder(spec.mcpcb_diameter / 2, spec.mcpcb_thickness, source_z)
    shape.label = "reference_mcpcb_20x1p6_nonprintable"
    return shape


def make_emitter_reference(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    shape = _box(
        spec.emitter_size,
        spec.emitter_size,
        spec.emitter_thickness,
        (0, 0, source_z - spec.emitter_thickness),
    )
    shape.label = "reference_xhp35p2_emitter_3p45_square_nonprintable"
    return shape


def make_heatsink_reference(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    z0 = source_z + spec.heatsink_front_offset
    base = _box(spec.heatsink_x, spec.heatsink_y, spec.heatsink_base, (0, 0, z0))
    fin_height = spec.heatsink_depth - spec.heatsink_base
    fins = []
    for x in (-15, -9, -3, 3, 9, 15):
        for y in (-15, -9, -3, 3, 9, 15):
            fins.append(_box(2.6, 2.6, fin_height, (x, y, z0 + spec.heatsink_base)))
    shape = _fuse_all([base, *fins])
    shape.label = "reference_heatsink_40x40x30_base_and_pin_array_nonprintable"
    return shape


def make_m4_hardware_reference(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    screw = Cylinder(2, 18, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(Axis.X, 90).moved(
        Location((-spec.rail_x, 0, source_z))
    )
    screw.label = "reference_m4_clamp_screw_nonprintable"
    nut = _box(spec.m4_nut_af, spec.m4_nut_thickness, 3.2, (-spec.rail_x, 4.2, source_z - 1.6))
    nut.label = "reference_m4_captive_nut_envelope_nonprintable"
    return Compound(children=[screw, nut], label="reference_m4_hardware_nonprintable")


def make_wire_envelope_reference(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    anchor_z = source_z + spec.moving_wire_anchor_offset
    lead_a = _box(22, 1.2, 38, (38, -2, anchor_z))
    lead_b = _box(22, 1.2, 38, (38, 2, anchor_z))
    lead_a.label = "reference_wire_lead_a_80mm_u_loop_envelope_nonprintable"
    lead_b.label = "reference_wire_lead_b_80mm_u_loop_envelope_nonprintable"
    return Compound(children=[lead_a, lead_b], label="reference_two_lead_wire_side_channel_nonprintable")


def make_fixed_references(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    mask = _cylinder(50, 0.2, spec.mask_z - 0.1)
    mask.label = "reference_conceptual_mask_plane_z6_nonprintable"
    keepout = _cylinder(
        spec.v0r2_keepout_radius,
        spec.v0r2_keepout_z_max - spec.v0r2_keepout_z_min,
        spec.v0r2_keepout_z_min,
    )
    keepout.label = "reference_v0r2_keepout_r40p3_zminus16_to_27p846_nonprintable"
    free_air = _box(50, 50, spec.heatsink_depth + spec.free_air_rear, (0, 0, source_z + spec.mcpcb_thickness))
    free_air.label = "reference_heatsink_free_air_envelope_5mm_nonprintable"
    pla_keepout = _box(60, 60, spec.heatsink_depth + spec.decorative_pla_keepout, (0, 0, source_z + spec.mcpcb_thickness))
    pla_keepout.label = "reference_decorative_pla_keepout_10mm_nonprintable"
    driver = _box(20, 30, 12, (75, 0, source_z + 10))
    driver.label = "reference_driver_keepout_over_30mm_from_heatsink_nonprintable"
    return Compound(
        children=[mask, keepout, free_air, pla_keepout, driver],
        label="fixed_nonprintable_reference_envelopes",
    )


def make_free_air_envelope(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    """Exact occupied-free volume required around the moving heatsink."""
    shape = _box(
        spec.heatsink_x + 2 * spec.free_air_lateral,
        spec.heatsink_y + 2 * spec.free_air_lateral,
        spec.heatsink_depth + spec.free_air_rear,
        (0, 0, source_z + spec.mcpcb_thickness),
    )
    shape.label = "reference_required_heatsink_free_air_volume_nonprintable"
    return shape


def make_stack_references(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    return Compound(
        children=[
            make_emitter_reference(source_z, spec),
            make_mcpcb_reference(source_z, spec),
            make_heatsink_reference(source_z, spec),
            make_m4_hardware_reference(source_z, spec),
            make_wire_envelope_reference(source_z, spec),
        ],
        label=f"moving_reference_metal_stack_source_z_{source_z:g}_nonprintable",
    )


def make_assembly(source_z: float = P1.source_z_default, spec: AdjustableLedCartridgeSpec = P1):
    return Compound(
        children=[
            make_rail_frame(spec),
            make_rear_service_bridge(spec),
            placed_carriage(source_z, spec),
            placed_strain_relief(source_z, spec),
            make_stack_references(source_z, spec),
            make_fixed_references(source_z, spec),
        ],
        label=f"p1_adjustable_led_cartridge_source_z_{source_z:g}_labeled_assembly",
    )


def service_bridge_transform(progress: float) -> Location:
    """Collision-free service path after release: -Y 30 mm, then +Z 12 mm."""
    if not 0.0 <= progress <= 1.0:
        raise ValueError("progress must be in [0, 1]")
    if progress <= 0.75:
        return Location((0, -40 * progress, 0))
    return Location((0, -30, 48 * (progress - 0.75)))


def service_carriage_transform(progress: float) -> Location:
    """After bridge removal, withdraw carriage and metal stack through +Z."""
    if not 0.0 <= progress <= 1.0:
        raise ValueError("progress must be in [0, 1]")
    return Location((0, 0, 76 * progress))


def make_service_exploded(spec: AdjustableLedCartridgeSpec = P1):
    source_z = spec.source_z_default
    return Compound(
        children=[
            make_rail_frame(spec),
            make_rear_service_bridge(spec).moved(service_bridge_transform(1.0)),
            placed_carriage(source_z, spec).moved(service_carriage_transform(1.0)),
            placed_strain_relief(source_z, spec).moved(service_carriage_transform(1.0)),
            make_stack_references(source_z, spec).moved(service_carriage_transform(1.0)),
            make_fixed_references(source_z, spec),
        ],
        label="p1_adjustable_led_cartridge_exploded_service_assembly",
    )


def make_integration_reference_assembly(spec: AdjustableLedCartridgeSpec = P1):
    """Nonprintable installation story; V0R2 remains an independent design."""
    from v0r2_identifiable_fin_fixture_geometry import make_assembly as make_v0r2

    wall = _box(110, 110, 0.4, (0, 0, -0.4))
    wall.label = "integration_reference_wall_z0_nonprintable"
    v0r2 = make_v0r2()
    v0r2.label = "integration_reference_standalone_v0r2_quartz_and_moving_carriers_nonprintable"
    cartridge = make_review_assembly(spec.source_z_default, spec)
    cartridge.label = "integration_stationary_kage_bridge_and_adjustable_led_stack"
    clearance = _cylinder(
        spec.v0r2_keepout_radius + 1.7,
        0.154,
        spec.v0r2_keepout_z_max,
    )
    clearance.label = "integration_support_clearance_v0r2_to_stationary_frame_0p154_axial_nonprintable"
    glare_z = spec.source_z_max + spec.heatsink_rear_offset + spec.free_air_rear
    glare_ring = _box(76, 76, 1, (0, 0, glare_z)).cut(_box(48, 48, 2, (0, 0, glare_z - 0.5)))
    glare_ring.label = "integration_room_side_glare_shield_mounting_datum_only_no_dome_nonprintable"
    viewer = _box(20, 20, 1, (0, 0, glare_z + 30))
    viewer.label = "integration_room_side_viewer_datum_nonprintable"
    optical_path = _cylinder(1.0, spec.source_z_default, 0)
    optical_path.label = "integration_wall_facing_led_optical_axis_open_path_nonprintable"
    return Compound(
        children=[wall, v0r2, cartridge, clearance, glare_ring, viewer, optical_path],
        label="p1_nonprintable_integration_wall_to_viewer_reference_assembly",
    )


def _clearance_outline(size: float, front_z: float, depth: float, label: str):
    """Sparse review-only outline; not a printable or occupied volume."""
    half = size / 2
    members = [
        _box(1, 1, depth, (x, y, front_z))
        for x in (-half, half)
        for y in (-half, half)
    ]
    members.extend(
        [
            _box(size, 1, 1, (0, y, front_z + depth)) for y in (-half, half)
        ]
    )
    result = Compound(children=members, label=label)
    return result


def make_review_assembly(source_z: float = P1.source_z_default, spec: AdjustableLedCartridgeSpec = P1):
    """Readable visual packet assembly without opaque conceptual envelopes."""
    front_z = source_z + spec.mcpcb_thickness
    free_air = _clearance_outline(
        spec.heatsink_x + 2 * spec.free_air_lateral,
        front_z,
        spec.heatsink_depth + spec.free_air_rear,
        "review_outline_minimum_5mm_free_air",
    )
    pla = _clearance_outline(
        spec.heatsink_x + 2 * spec.decorative_pla_keepout,
        front_z,
        spec.heatsink_depth + spec.decorative_pla_keepout,
        "review_outline_minimum_10mm_decorative_pla_keepout",
    )
    mask_axis = _cylinder(1.2, source_z - spec.mask_z, spec.mask_z)
    mask_axis.label = "review_optical_axis_mask_to_source"
    return Compound(
        children=[
            make_rail_frame(spec),
            make_rear_service_bridge(spec),
            placed_carriage(source_z, spec),
            make_emitter_reference(source_z, spec),
            make_mcpcb_reference(source_z, spec),
            make_heatsink_reference(source_z, spec),
            make_m4_hardware_reference(source_z, spec),
            make_wire_envelope_reference(source_z, spec),
            free_air,
            pla,
            mask_axis,
            make_aperture_holder_datum_reference(source_z, spec),
        ],
        label=f"p1_cartridge_readable_review_source_z_{source_z:g}",
    )


def make_aperture_holder_datum_reference(source_z: float, spec: AdjustableLedCartridgeSpec = P1):
    ring = _cylinder(15, 1.2, source_z - 3.0).cut(
        _cylinder(11, 2, source_z - 3.4)
    )
    for angle in (0, 120, 240):
        x = 13 * __import__("math").cos(__import__("math").radians(angle))
        y = 13 * __import__("math").sin(__import__("math").radians(angle))
        ring = ring.cut(_cylinder(1.1, 2, source_z - 3.4).moved(Location((x, y, 0))))
    ring.label = "reference_future_aperture_holder_ring_three_m2_datums_no_optic_nonprintable"
    return ring


def make_axial_xz_section_review(spec: AdjustableLedCartridgeSpec = P1):
    """0.8 mm thick XZ axial slice through y=0 for visual section review."""
    source_z = spec.source_z_default
    slab = _box(160, 0.8, 130, (0, 0, -20))
    section_children = []
    for shape in (
        make_rail_frame(spec),
        make_rear_service_bridge(spec),
        placed_carriage(source_z, spec),
        make_emitter_reference(source_z, spec),
        make_mcpcb_reference(source_z, spec),
        make_heatsink_reference(source_z, spec),
    ):
        section = shape.intersect(slab)
        if section is None:
            continue
        solids = list(section.solids()) if hasattr(section, "solids") else list(section)
        section_children.extend(solid for solid in solids if solid.volume > 0)
    axis = _box(1, 0.8, source_z - spec.mask_z, (0, 0, spec.mask_z))
    axis.label = "section_optical_axis_mask_z6_to_led_z40"
    section_children.append(axis)
    return Compound(children=section_children, label="p1_true_xz_axial_section_y0")


PRINTABLE_FACTORIES = (
    ("rail_frame", make_rail_frame),
    ("moving_carriage", make_moving_carriage),
    ("rear_service_bridge", make_rear_service_bridge),
    ("strain_relief_clip", make_strain_relief_clip),
)


def wire_u_loop_metrics(spec: AdjustableLedCartridgeSpec = P1) -> dict[str, float]:
    return {
        "nominal_length": spec.wire_nominal_u_loop,
        "travel": spec.travel,
        "slack_after_travel": spec.wire_nominal_u_loop - spec.travel,
        "minimum_bend_radius": spec.wire_min_bend_radius,
        "moving_anchor_offset": spec.moving_wire_anchor_offset,
    }
