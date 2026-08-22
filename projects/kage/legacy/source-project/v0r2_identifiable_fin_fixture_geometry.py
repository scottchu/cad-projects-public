"""build123d geometry for V0R2 identifiable upright-fin fixture."""

from __future__ import annotations

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Compound,
    Cone,
    Cylinder,
    Location,
    Plane,
    Polygon,
    extrude,
)

from v0r2_identifiable_fin_fixture_spec import CarrierSpec, IdentifiableFinFixtureSpec, V0R2


def _cylinder(radius, height, z0=0):
    return Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0)))


def make_fake_standard_quartz_body(spec=V0R2):
    body = Box(spec.body_x, spec.body_y, spec.body_depth, align=(Align.CENTER, Align.CENTER, Align.MIN))
    body = body.fillet(spec.body_corner_radius, body.edges().filter_by(Axis.Z))
    overshoot = 0.02
    offset = spec.body_depth
    arbor = _cylinder(6, 5.883333333 + overshoot, offset - overshoot)
    arbor = arbor.fuse(_cylinder(4, 1.2 + 2 * overshoot, offset + 5.883333333 - overshoot))
    arbor = arbor.fuse(_cylinder(3, 3.958333334 + 2 * overshoot, offset + 7.083333333 - overshoot))
    arbor = arbor.fuse(_cylinder(2, 5.758333333 + overshoot, offset + 11.041666667 - overshoot))
    arbor = arbor.fuse(
        Cone(2, 1.7, 0.4 + overshoot, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((0, 0, offset + 16.8 - overshoot))
        )
    )
    result = body.fuse(arbor)
    result.label = "fake_standard_quartz_body_representative_aa_envelope"
    return result


def _ring(carrier, spec):
    return _cylinder(carrier.radius + spec.ring_radial_width / 2, spec.ring_axial_thickness).cut(
        _cylinder(carrier.radius - spec.ring_radial_width / 2, spec.ring_axial_thickness + 0.4, -0.2)
    )


def _spokes(carrier, hub_radius, spec):
    length = carrier.radius + spec.ring_radial_width / 2 - hub_radius + 0.05
    center = hub_radius - 0.1 + length / 2
    result = None
    for angle in (0, 120, 240):
        spoke = Box(
            length,
            spec.spoke_tangential_width,
            spec.ring_axial_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((center, 0, 0))).rotate(Axis.Z, angle)
        result = spoke if result is None else result.fuse(spoke)
    return result


def fin_profile_yz(carrier: CarrierSpec, spec: IdentifiableFinFixtureSpec = V0R2):
    """Closed tangential-width/axial-height profile used by the real BREP fin."""
    identity = spec.fin_identities[carrier.name]
    root_z = spec.ring_axial_thickness - spec.fin_root_overlap
    crown_base = carrier.local_height - identity.crown_height
    return (
        (-identity.stem_width / 2, root_z),
        (identity.stem_width / 2, root_z),
        (identity.stem_width / 2, crown_base),
        (identity.crown_width / 2, carrier.local_height),
        (-identity.crown_width / 2, carrier.local_height),
        (-identity.stem_width / 2, crown_base),
    )


def _fin(carrier, spec):
    # Sketch coordinates are tangential Y and axial Z; the Plane normal is
    # radial +X.  The taper moves inward only, so every crown wall is <=45 deg.
    plane = Plane(
        origin=(carrier.radius - spec.fin_radial_thickness / 2, 0, 0),
        x_dir=(0, 1, 0),
        z_dir=(1, 0, 0),
    )
    with BuildPart() as part:
        with BuildSketch(plane):
            Polygon(*fin_profile_yz(carrier, spec))
        extrude(amount=spec.fin_radial_thickness)
    result = part.part
    result.label = f"{carrier.name}_identifiable_{spec.fin_identities[carrier.name].stem_width:g}mm_fin"
    return result


def _lower_hub(carrier):
    hub = _cylinder(carrier.hub_od / 2, carrier.hub_height).fuse(
        _cylinder(carrier.tower_od / 2, carrier.tower_height)
    )
    return hub.cut(_cylinder(carrier.bore_diameter / 2, carrier.tower_height + 0.4, -0.2))


def _hour_hub(carrier, spec):
    hub = _cylinder(carrier.hub_od / 2, carrier.hub_height).cut(
        _cylinder(spec.hour_bore_diameter / 2, carrier.hub_height + 0.4, -0.2)
    )
    pad_r = spec.hour_pad_radial_protrusion + 0.30
    pad_c = spec.hour_bore_diameter / 2 - spec.hour_pad_radial_protrusion / 2 + 0.15
    for angle in (0, 120, 240):
        pad = Box(
            pad_r,
            spec.hour_pad_tangential_width,
            carrier.hub_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((pad_c, 0, 0))).rotate(Axis.Z, angle)
        hub = hub.fuse(pad)
    slit_l = carrier.hub_od / 2 - spec.hour_bore_diameter / 2 + 1
    slit = Box(
        slit_l,
        spec.hour_slit_width,
        carrier.hub_height + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((-(spec.hour_bore_diameter / 2 + slit_l / 2 - 0.3), 0, -0.2)))
    return hub.cut(slit)


def make_carrier_hand(carrier, spec=V0R2):
    hub = _hour_hub(carrier, spec) if carrier.name == "hour" else _lower_hub(carrier)
    result = hub.fuse(_ring(carrier, spec)).fuse(_spokes(carrier, carrier.hub_od / 2, spec)).fuse(_fin(carrier, spec))
    result.label = f"{carrier.name}_carrier_hand_identifiable_upright_fin"
    return result


def make_hour_carrier_hand(spec=V0R2):
    return make_carrier_hand(spec.by_name["hour"], spec)


def make_minute_carrier_hand(spec=V0R2):
    return make_carrier_hand(spec.by_name["minute"], spec)


def make_second_carrier_hand(spec=V0R2):
    return make_carrier_hand(spec.by_name["second"], spec)


PART_FACTORIES = (
    ("fake_standard_quartz_body", make_fake_standard_quartz_body),
    ("hour_carrier_hand", make_hour_carrier_hand),
    ("minute_carrier_hand", make_minute_carrier_hand),
    ("second_carrier_hand", make_second_carrier_hand),
)


def part_factories():
    return PART_FACTORIES


def placed_body(spec=V0R2):
    return make_fake_standard_quartz_body(spec).moved(Location((0, 0, -spec.body_depth)))


def placed_carrier(name, angle=0, spec=V0R2):
    carrier = spec.by_name[name]
    return make_carrier_hand(carrier, spec).rotate(Axis.Z, angle).moved(Location((0, 0, carrier.ring_bottom_z)))


ANGLES = {"second": 300, "minute": 20, "hour": 225}


def make_assembly(spec=V0R2):
    return Compound(
        children=[placed_body(spec), *(placed_carrier(name, ANGLES[name], spec) for name in ("second", "minute", "hour"))],
        label="v0r2_identifiable_fin_four_part_fixture",
    )


def make_exploded_assembly(spec=V0R2):
    children = [placed_body(spec)]
    for index, name in enumerate(("second", "minute", "hour"), 1):
        children.append(placed_carrier(name, ANGLES[name], spec).moved(Location((0, 0, 6 * index))))
    return Compound(children=children, label="v0r2_identifiable_fin_four_part_fixture_exploded")
