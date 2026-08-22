"""build123d geometry for the four-part P0 optics fixture."""

from __future__ import annotations

from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cone, Cylinder, Face, Location, Vector, Wire, extrude

from p0_optics_fixture_spec import HandSpec, P0, FixtureSpec


def _centered_cylinder(radius: float, height: float, z_center: float = 0.0) -> Cylinder:
    return Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(Location((0, 0, z_center)))


def make_pedestal_mask(spec: FixtureSpec = P0):
    """One closed solid: tapered mask pedestal plus fixed stepped arbor."""
    body = Cone(
        spec.body_rear_diameter_mm / 2.0,
        spec.body_mask_diameter_mm / 2.0,
        spec.body_depth_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, spec.wall_z_mm)))

    hands = spec.hands
    # Lands are centered on the hand planes.  The 0.30 mm gaps between lands
    # are conical lead transitions.  There is no retaining bead or cap.
    overlap = 0.02
    first_land_end = hands[0].plane_z_mm + spec.journal_land_mm / 2.0
    arbor = Cylinder(
        hands[0].journal_diameter_mm / 2.0,
        first_land_end + 0.20,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, -0.20)))
    for index, hand in enumerate(hands):
        z0 = hand.plane_z_mm - spec.journal_land_mm / 2.0
        if index > 0:
            land = Cylinder(
                hand.journal_diameter_mm / 2.0,
                spec.journal_land_mm + overlap,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((0, 0, z0 - overlap)))
            arbor = arbor.fuse(land)
        if index < len(hands) - 1:
            next_hand = hands[index + 1]
            transition = Cone(
                hand.journal_diameter_mm / 2.0,
                next_hand.journal_diameter_mm / 2.0,
                spec.journal_lead_mm + 2.0 * overlap,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((0, 0, z0 + spec.journal_land_mm - overlap)))
            arbor = arbor.fuse(transition)
        else:
            # Terminal lead is a short chamfered insertion nose, not a cap.
            nose = Cone(
                hand.journal_diameter_mm / 2.0,
                max(0.2, hand.journal_diameter_mm / 2.0 - 0.6),
                spec.journal_lead_mm + 2.0 * overlap,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((0, 0, z0 + spec.journal_land_mm - overlap)))
            arbor = arbor.fuse(nose)

    result = body.fuse(arbor)
    result.label = "p0_pedestal_mask_with_fixed_stepped_arbor"
    return result


def _blade_prism(hand: HandSpec, thickness_mm: float):
    hub_radius = hand.hub_outer_diameter_mm / 2.0
    tip_center_x = hand.radial_length_mm - hand.tip_radius_mm
    blade_wire = Wire.make_polygon(
        [
            Vector(hub_radius - 0.3, -hand.root_width_mm / 2.0, 0),
            Vector(tip_center_x, -hand.tip_width_mm / 2.0, 0),
            Vector(tip_center_x, hand.tip_width_mm / 2.0, 0),
            Vector(hub_radius - 0.3, hand.root_width_mm / 2.0, 0),
        ],
        close=True,
    )
    blade_face = Face(blade_wire)
    blade = extrude(blade_face, amount=thickness_mm).moved(Location((0, 0, -thickness_mm / 2.0)))
    tip = _centered_cylinder(hand.tip_radius_mm, thickness_mm).moved(Location((tip_center_x, 0, 0)))
    return blade.fuse(tip)


def make_hand(hand: HandSpec, spec: FixtureSpec = P0):
    """Single tapered hand with rounded tip and compliant three-pad slit hub."""
    t = spec.hand_thickness_mm
    hub_radius = hand.hub_outer_diameter_mm / 2.0
    relief_radius = hand.relief_bore_diameter_mm / 2.0
    solid = _centered_cylinder(hub_radius, t).fuse(_blade_prism(hand, t))
    relief = _centered_cylinder(relief_radius, t + 1.0)
    solid = solid.cut(relief)

    # Three local press contacts are intentionally small; the remainder of the
    # Ø+0.20 relief bore prevents a rigid full-circumference press fit.
    pad_radial_length = spec.contact_pad_radial_protrusion_mm + 0.25
    pad_center_radius = relief_radius - spec.contact_pad_radial_protrusion_mm / 2.0 + 0.125
    for angle in (0.0, 120.0, 240.0):
        pad = Box(
            pad_radial_length,
            spec.contact_pad_tangential_mm,
            t,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((pad_center_radius, 0, 0)))
        pad = pad.rotate(Axis.Z, angle)
        solid = solid.fuse(pad)

    # The slit is opposite the blade (+X), opening the hub toward -X.
    slit_length = hub_radius - relief_radius + 1.4
    slit_center_x = -(relief_radius + slit_length / 2.0 - 0.4)
    slit = Box(
        slit_length,
        spec.hub_slit_mm,
        t + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((slit_center_x, 0, 0)))
    solid = solid.cut(slit)
    solid.label = f"p0_{hand.name}_tapered_rounded_blocker_with_compliant_slit_hub"
    return solid


def make_hour_hand(spec: FixtureSpec = P0):
    return make_hand(spec.hands[0], spec)


def make_minute_hand(spec: FixtureSpec = P0):
    return make_hand(spec.hands[1], spec)


def make_second_hand(spec: FixtureSpec = P0):
    return make_hand(spec.hands[2], spec)


ASSEMBLY_ANGLES_DEG = {"hour": 225.0, "minute": 20.0, "second": 300.0}


def placed_hand(hand: HandSpec, spec: FixtureSpec = P0):
    shape = make_hand(hand, spec)
    angle = ASSEMBLY_ANGLES_DEG[hand.name]
    shape = shape.rotate(Axis.Z, angle)
    shape = shape.moved(Location((0, 0, hand.plane_z_mm)))
    shape.label = f"p0_{hand.name}_blocker_at_z_{hand.plane_z_mm:g}"
    return shape


def make_assembly(spec: FixtureSpec = P0):
    children = [make_pedestal_mask(spec), *(placed_hand(hand, spec) for hand in spec.hands)]
    assembly = Compound(children=children, label="p0_four_part_shadow_fixture_assembly")
    return assembly


def part_factories(spec: FixtureSpec = P0):
    return (
        ("pedestal_mask", lambda: make_pedestal_mask(spec)),
        ("hour_hand", lambda: make_hour_hand(spec)),
        ("minute_hand", lambda: make_minute_hand(spec)),
        ("second_hand", lambda: make_second_hand(spec)),
    )
