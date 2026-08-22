"""build123d geometry for the isolated V0 upright-fin manual fixture."""

from __future__ import annotations

from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cone, Cylinder, Location, Sphere

from v0_upright_fin_fixture_spec import CarrierSpec, V0, FixtureSpec


def _cylinder(radius: float, height: float, z0: float = 0.0):
    return Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0)))


def make_fake_quartz_mask_body(spec: FixtureSpec = V0):
    body = _cylinder(spec.body_diameter / 2, spec.body_height)
    overlap = 0.02
    arbor = _cylinder(6.0, 9.425 - 6.0 + overlap, 6.0 - overlap)
    arbor = arbor.fuse(_cylinder(4.0, 10.625 - 9.425 + 2 * overlap, 9.425 - overlap))
    arbor = arbor.fuse(_cylinder(3.0, 16.5625 - 10.625 + 2 * overlap, 10.625 - overlap))
    arbor = arbor.fuse(_cylinder(2.0, 23.90 - 16.5625 + overlap, 16.5625 - overlap))
    arbor = arbor.fuse(Cone(2.0, spec.arbor_tip_diameter / 2, spec.arbor_tip_chamfer_height + overlap,
                            align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, 23.90 - overlap))))
    result = body.fuse(arbor)
    result.label = "fake_quartz_mask_body_with_integrated_monotonic_arbor"
    return result


def _annular_ring(radius: float, width: float, height: float):
    outer = _cylinder(radius + width / 2, height)
    inner = _cylinder(radius - width / 2, height + 0.4, -0.2)
    return outer.cut(inner)


def _spokes(carrier: CarrierSpec, hub_radius: float, spec: FixtureSpec):
    radial_length = carrier.radius + spec.ring_radial_width / 2 - hub_radius + 0.05
    center_x = hub_radius - 0.1 + radial_length / 2
    combined = None
    for angle in (0.0, 120.0, 240.0):
        spoke = Box(radial_length, spec.spoke_tangential_width, spec.ring_axial_thickness,
                    align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((center_x, 0, 0)))
        spoke = spoke.rotate(Axis.Z, angle)
        combined = spoke if combined is None else combined.fuse(spoke)
    return combined


def _upright_fin(carrier: CarrierSpec, spec: FixtureSpec):
    local_tip = carrier.local_height
    root_z = spec.ring_axial_thickness - spec.fin_root_overlap
    # A 0.6 mm sourceward chamfer/taper removes a fragile square tip while
    # preserving the exact optical endpoint and the specified XY envelope.
    straight_height = local_tip - root_z - spec.fin_tip_radius
    fin = Box(spec.fin_radial_thickness, spec.fin_tangential_width, straight_height,
              align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((carrier.radius, 0, root_z)))
    cap = Sphere(spec.fin_tip_radius).moved(Location((carrier.radius, 0, root_z + straight_height)))
    return fin.fuse(cap)


def _lower_hub(carrier: CarrierSpec):
    assert carrier.tower_od is not None
    disk = _cylinder(carrier.hub_od / 2, carrier.hub_height)
    tower = _cylinder(carrier.tower_od / 2, carrier.tower_height)
    hub = disk.fuse(tower)
    bore = _cylinder(carrier.bore_diameter / 2, carrier.tower_height + 0.4, -0.2)
    return hub.cut(bore)


def _hour_hub(carrier: CarrierSpec, spec: FixtureSpec):
    hub = _cylinder(carrier.hub_od / 2, carrier.hub_height)
    relief = _cylinder(spec.hour_bore_diameter / 2, carrier.hub_height + 0.4, -0.2)
    hub = hub.cut(relief)
    # Three compliant pads reduce the local bore radius from 2.10 to 1.95 mm,
    # producing the frozen 0.05 mm radial interference on a Ø4 shaft.
    pad_radial = spec.hour_pad_radial_protrusion + 0.30
    pad_center = spec.hour_bore_diameter / 2 - spec.hour_pad_radial_protrusion / 2 + 0.15
    for angle in (0.0, 120.0, 240.0):
        pad = Box(pad_radial, spec.hour_pad_tangential_width, carrier.hub_height,
                  align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((pad_center, 0, 0))).rotate(Axis.Z, angle)
        hub = hub.fuse(pad)
    slit_length = carrier.hub_od / 2 - spec.hour_bore_diameter / 2 + 1.0
    slit = Box(slit_length, spec.hour_slit_width, carrier.hub_height + 0.4,
               align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((-(spec.hour_bore_diameter / 2 + slit_length / 2 - 0.3), 0, -0.2)))
    return hub.cut(slit)


def make_carrier_hand(carrier: CarrierSpec, spec: FixtureSpec = V0):
    hub = _hour_hub(carrier, spec) if carrier.name == "hour" else _lower_hub(carrier)
    solid = hub.fuse(_annular_ring(carrier.radius, spec.ring_radial_width, spec.ring_axial_thickness))
    solid = solid.fuse(_spokes(carrier, carrier.hub_od / 2, spec))
    solid = solid.fuse(_upright_fin(carrier, spec))
    solid.label = f"{carrier.name}_carrier_hand_three_spokes_upright_rim_fin"
    return solid


def make_hour_carrier_hand(spec: FixtureSpec = V0):
    return make_carrier_hand(spec.by_name["hour"], spec)


def make_minute_carrier_hand(spec: FixtureSpec = V0):
    return make_carrier_hand(spec.by_name["minute"], spec)


def make_second_carrier_hand(spec: FixtureSpec = V0):
    return make_carrier_hand(spec.by_name["second"], spec)


PART_FACTORIES = (
    ("fake_quartz_mask_body", make_fake_quartz_mask_body),
    ("hour_carrier_hand", make_hour_carrier_hand),
    ("minute_carrier_hand", make_minute_carrier_hand),
    ("second_carrier_hand", make_second_carrier_hand),
)


def part_factories():
    return PART_FACTORIES


def placed_carrier(name: str, angle_degrees: float = 0.0, spec: FixtureSpec = V0):
    carrier = spec.by_name[name]
    shape = make_carrier_hand(carrier, spec).rotate(Axis.Z, angle_degrees)
    shape = shape.moved(Location((0, 0, carrier.ring_bottom_z)))
    shape.label = f"{name}_carrier_hand_assembled"
    return shape


ASSEMBLY_ANGLES = {"second": 300.0, "minute": 20.0, "hour": 225.0}


def make_assembly(spec: FixtureSpec = V0):
    children = [make_fake_quartz_mask_body(spec)]
    for name in ("second", "minute", "hour"):
        children.append(placed_carrier(name, ASSEMBLY_ANGLES[name], spec))
    return Compound(children=children, label="v0_four_part_manual_upright_fin_fixture")


def make_exploded_assembly(spec: FixtureSpec = V0):
    body = make_fake_quartz_mask_body(spec)
    parts = [body]
    for index, name in enumerate(("second", "minute", "hour"), start=1):
        carrier = spec.by_name[name]
        shape = make_carrier_hand(carrier, spec).rotate(Axis.Z, ASSEMBLY_ANGLES[name])
        shape = shape.moved(Location((0, 0, carrier.ring_bottom_z + 8.0 * index)))
        shape.label = f"{name}_carrier_hand_exploded"
        parts.append(shape)
    return Compound(children=parts, label="v0_four_part_manual_upright_fin_fixture_exploded")
