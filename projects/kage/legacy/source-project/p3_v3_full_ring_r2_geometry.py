"""Complete STEP-first geometry for KAGE P3 V3 full-ring R2.

Unlike the rejected R1 coupon, every moving carrier here is a complete ring and
every role has its own real pinion, horizontal NEMA8 reference, miter pair,
two-bearing output shaft, guide race, and outward shadow fin.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, degrees, radians, sin, sqrt

import py_gearworks as pgw
from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude
from cadgen import srgb

from p3_v3_full_ring_r2_spec import P3V3FullRingR2Spec, P3_V3_FULL_RING_R2
from p3_v3_transmission_r1_geometry import (
    _d_prism_z,
    make_bearing as r1_make_bearing,
    make_lower_clamp_collar as r1_make_lower_clamp_collar,
    make_lower_miter_shim as r1_make_lower_miter_shim,
    make_miter_pair as r1_make_miter_pair,
    make_motor_body as r1_make_motor_body,
    make_motor_saddle as r1_make_motor_saddle,
    make_motor_shaft as r1_make_motor_shaft,
    make_output_shaft as r1_make_output_shaft,
    make_role_spacer as r1_make_role_spacer,
)


def _annulus(inner_radius: float, outer_radius: float, height: float, z0: float):
    outer = Cylinder(outer_radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0))
    )
    inner = Cylinder(inner_radius, height + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0 - 0.2))
    )
    return outer.cut(inner)


def _polar(radius: float, angle_degrees: float) -> tuple[float, float]:
    angle = radians(angle_degrees)
    return radius * cos(angle), radius * sin(angle)


def _rotate_station(part, angle_degrees: float):
    return part.rotate(Axis.Z, angle_degrees)


def _annular_sector(
    inner_radius: float,
    outer_radius: float,
    tangential_width: float,
    z0: float,
    z1: float,
):
    """Curved radial sector whose outer radius is an exact hard envelope."""

    center_radius = (inner_radius + outer_radius) / 2.0
    half_angle = degrees(tangential_width / (2.0 * center_radius))
    mask_radius = outer_radius + 0.5
    points = [(0.0, 0.0)]
    for index in range(9):
        angle = -half_angle + 2.0 * half_angle * index / 8.0
        points.append(_polar(mask_radius, angle))
    points.append((0.0, 0.0))
    mask = extrude(Polygon(*points), amount=z1 - z0).moved(Location((0.0, 0.0, z0)))
    pieces = _annulus(inner_radius, outer_radius, z1 - z0, z0).intersect(mask)
    if not pieces:
        raise ValueError("annular fin sector crop produced no solid")
    return max(pieces, key=lambda shape: shape.volume)


@lru_cache(maxsize=3)
def _full_role_ring(role_index: int):
    """One complete 260T carrier before its four-way service split."""

    spec = P3_V3_FULL_RING_R2
    layer_z0, layer_z1 = spec.carrier_layers[role_index]
    face_z0, face_z1 = spec.pinion_face_ranges[role_index]
    wrapper = pgw.SpurRingGear(
        number_of_teeth=spec.ring_teeth,
        module=spec.module,
        height=face_z1 - face_z0,
        center=[0.0, 0.0, face_z0],
        backlash=0.10,
    )
    teeth = wrapper.build_part().solid().rotate(Axis.Z, spec.tooth_phase_offset_degrees)
    body = _annulus(
        spec.ring_body_inner_radius,
        spec.ring_body_outer_radius,
        layer_z1 - layer_z0,
        layer_z0,
    )
    rail_z0, _ = spec.race_range(role_index)
    flange = _annulus(
        spec.rail_flange_radii[0],
        spec.rail_flange_radii[1],
        spec.rail_flange_depth,
        rail_z0,
    )
    neck = _annulus(
        spec.rail_neck_radii[0],
        spec.rail_neck_radii[1],
        spec.rail_neck_depth,
        layer_z0 - spec.rail_neck_depth,
    )
    ring = teeth.fuse(body).fuse(neck).fuse(flange)

    # Identical holes at both ends of the canonical 90-degree segment.  Hole
    # envelopes remain wholly outside the active 132.5 mm tooth-root cylinder.
    for angle in (
        spec.joint_hole_edge_angle_degrees,
        spec.quadrant_angle_degrees - spec.joint_hole_edge_angle_degrees,
    ):
        x, y = _polar(spec.joint_hole_radius, angle)
        hole = Cylinder(
            spec.joint_hole_diameter / 2.0,
            layer_z1 - rail_z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, rail_z0 - 0.2)))
        ring = ring.cut(hole)
    # A split vertical dowel bore straddles every quadrant seam.  Each printed
    # quadrant receives a half-bore; the inserted dowel registers both halves.
    for angle in (0.0, 90.0, 180.0, 270.0):
        x, y = _polar(spec.registration_dowel_radius, angle)
        ring = ring.cut(
            Cylinder(
                spec.registration_dowel_diameter / 2.0,
                layer_z1 - layer_z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, layer_z0 - 0.2)))
        )
    return ring


@lru_cache(maxsize=3)
def _canonical_quadrant(role_index: int):
    spec = P3_V3_FULL_RING_R2
    z0, z1 = spec.carrier_layers[role_index]
    race_z0, _ = spec.race_range(role_index)
    size = spec.ring_outer_radius + 1.0
    crop = Box(
        size,
        size,
        z1 - race_z0 + 0.8,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((0.0, 0.0, race_z0 - 0.4)))
    pieces = _full_role_ring(role_index).intersect(crop)
    if not pieces:
        raise ValueError("260T ring quadrant crop produced no solid")
    return max(pieces, key=lambda shape: shape.volume)


def make_ring_quadrant(
    role_index: int,
    quadrant_index: int,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    if not 0 <= quadrant_index < spec.quadrant_count:
        raise ValueError("quadrant index outside 0..3")
    # deepcopy prevents labels on transformed copies aliasing the cached Q1
    # shape, which previously collapsed all four STEP identities to Q4.
    quadrant = deepcopy(_canonical_quadrant(role_index)).rotate(
        Axis.Z, quadrant_index * spec.quadrant_angle_degrees
    )
    fin_quadrant = int(spec.display_fin_angles[role_index] // spec.quadrant_angle_degrees)
    if quadrant_index == fin_quadrant:
        quadrant = quadrant.fuse(make_fin(role_index, spec))
    quadrant.label = (
        f"p3_v3_r2_{spec.roles[role_index]}_M1_260T_"
        f"quadrant_Q{quadrant_index + 1}_65T"
    )
    quadrant.color = srgb(spec.role_colors[role_index])
    return quadrant


def make_ring_quadrants(
    role_index: int,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    return tuple(make_ring_quadrant(role_index, q, spec) for q in range(spec.quadrant_count))


def make_fin(role_index: int, spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    blade_r0, blade_r1 = spec.fin_blade_radial_ranges[role_index]
    blade_z0 = spec.fin_blade_start_zs[role_index]
    fin = _annular_sector(
        blade_r0,
        blade_r1,
        spec.fin_tangential_widths[role_index],
        blade_z0,
        spec.fin_tip_zs[role_index],
    )
    root_range = spec.fin_root_radial_ranges[role_index]
    root_z = spec.fin_root_z_ranges[role_index]
    if root_range is not None and root_z is not None:
        root = _annular_sector(
            root_range[0],
            root_range[1],
            spec.fin_root_tangential_width,
            root_z[0],
            root_z[1],
        )
        root = root.fillet(spec.fin_root_fillet_radius, root.edges().filter_by(Axis.Z))
        fin = fin.fuse(root)
    fin = fin.rotate(Axis.Z, spec.display_fin_angles[role_index])
    fin.label = f"p3_v3_r2_{spec.roles[role_index]}_integral_root_and_shadow_fin"
    fin.color = srgb(spec.role_colors[role_index])
    return fin


def make_fin_fasteners(role_index: int, spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    return ()


def make_seam_hardware(role_index: int, spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    layer_z0, layer_z1 = spec.carrier_layers[role_index]
    hardware = []
    offset = spec.joint_hole_radius * sin(radians(spec.joint_hole_edge_angle_degrees))
    for seam_index, seam_angle in enumerate((0.0, 90.0, 180.0, 270.0)):
        plate = Box(
            spec.splice_plate_radial_width,
            spec.splice_plate_tangential_length,
            spec.splice_plate_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((sum(spec.splice_plate_radii) / 2.0, 0.0, layer_z0)))
        for local_y in (-offset, offset):
            plate = plate.cut(
                Cylinder(
                    spec.joint_hole_diameter / 2.0,
                    spec.splice_plate_thickness + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                ).moved(
                    Location((spec.joint_hole_radius, local_y, layer_z0 - spec.splice_plate_thickness - 0.2))
                )
            )
        plate = plate.rotate(Axis.Z, seam_angle)
        plate.label = f"p3_v3_r2_{spec.roles[role_index]}_seam_{seam_index + 1}_underside_splice"
        plate.color = srgb("#AEB5B9")
        hardware.append(plate)
        # One split registration dowel and two M2 screws make every seam a
        # finite, removable mechanical joint rather than coincident faces.
        dx, dy = _polar(spec.registration_dowel_radius, seam_angle)
        dowel = Cylinder(
            spec.registration_dowel_diameter / 2.0 - 0.05,
            layer_z1 - layer_z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((dx, dy, layer_z0)))
        dowel.label = f"p3_v3_r2_{spec.roles[role_index]}_seam_{seam_index + 1}_3mm_registration_dowel"
        dowel.color = srgb("#778187")
        hardware.append(dowel)
        for screw_index, local_y in enumerate((-offset, offset)):
            sx, sy = _polar(spec.joint_hole_radius, seam_angle)
            # Tangential offset in the seam's local frame.
            sx += -sin(radians(seam_angle)) * local_y
            sy += cos(radians(seam_angle)) * local_y
            core = Cylinder(
                spec.splice_fastener_core_diameter / 2.0,
                spec.splice_plate_thickness + 0.8,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((sx, sy, layer_z0 - spec.splice_plate_thickness)))
            head = Cylinder(
                spec.splice_fastener_head_diameter / 2.0,
                0.8,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
            ).moved(Location((sx, sy, layer_z0 - spec.splice_plate_thickness)))
            screw = core.fuse(head)
            screw.label = (
                f"p3_v3_r2_{spec.roles[role_index]}_seam_{seam_index + 1}_"
                f"M2_screw_{screw_index + 1}_REFERENCE"
            )
            screw.color = srgb("#6B7074")
            hardware.append(screw)
    return tuple(hardware)


def _pinion_wrappers(role_index: int, spec: P3V3FullRingR2Spec):
    face_z0, face_z1 = spec.pinion_face_ranges[role_index]
    ring = pgw.SpurRingGear(
        number_of_teeth=spec.ring_teeth,
        module=spec.module,
        height=face_z1 - face_z0,
        center=[0.0, 0.0, face_z0],
        backlash=0.10,
    )
    pinion = pgw.SpurGear(
        number_of_teeth=spec.pinion_teeth,
        module=spec.module,
        height=face_z1 - face_z0,
        center=[0.0, 0.0, face_z0],
        pressure_angle=radians(spec.pressure_angle_degrees),
        backlash=0.10,
        tip_truncation=0.10,
        enable_undercut=True,
    )
    pinion.mesh_to(ring, target_dir=pgw.RIGHT, backlash=spec.output_mesh_backlash)
    return ring, pinion


def make_output_pinion(role_index: int, spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    _, wrapper = _pinion_wrappers(role_index, spec)
    face_z0, face_z1 = spec.pinion_face_ranges[role_index]
    pinion = wrapper.build_part().solid()
    hub = Cylinder(3.6, face_z1 - face_z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((spec.output_axis_radius, 0.0, face_z0))
    )
    pinion = pinion.fuse(hub).cut(
        _d_prism_z(
            spec.output_axis_radius,
            face_z0 - 0.2,
            face_z1 + 0.2,
            4.10,
            3.60,
        )
    )
    station_angle = spec.motor_station_angles[role_index]
    # The 260T ring is globally phased half a tooth so every quadrant boundary
    # lies in a tooth space.  A station at alpha needs the coupled internal-
    # gear pinion phase delta*N/n + alpha*(1-N/n).
    local_spin = (spec.tooth_phase_offset_degrees - station_angle) * spec.gear_ratio
    pinion = pinion.rotate(
        Axis((spec.output_axis_radius, 0.0, 0.0), (0.0, 0.0, 1.0)),
        local_spin,
    )
    pinion = _rotate_station(pinion, spec.motor_station_angles[role_index])
    pinion.label = f"p3_v3_r2_{spec.roles[role_index]}_real_M1_16T_output_pinion"
    pinion.color = srgb("#D9A441")
    return pinion


def make_mesh_pair_at_phase(
    role_index: int,
    ring_angle_degrees: float,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    """Return the complete segmented ring and coupled pinion at one phase."""

    ring_parts = [
        deepcopy(part).rotate(Axis.Z, ring_angle_degrees)
        for part in make_ring_quadrants(role_index, spec)
    ]
    pinion = make_output_pinion(role_index, spec)
    x, y = _polar(spec.output_axis_radius, spec.motor_station_angles[role_index])
    pinion_angle = ring_angle_degrees * spec.gear_ratio
    pinion = pinion.rotate(Axis((x, y, 0.0), (0.0, 0.0, 1.0)), pinion_angle)
    return tuple(ring_parts), pinion


def make_canonical_mesh_pair_at_phase(
    role_index: int,
    ring_angle_degrees: float,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    """Return one unsplit full-ring solid and its coupled pinion.

    This is the stable validation representation.  The printable model remains
    four labeled quadrants, but involute collision checks should occur before
    quadrant cropping: repeatedly deep-copying/cropping py_gearworks BREP data
    can exhaust or crash OCC despite identical geometry.
    """

    ring = _full_role_ring(role_index).rotate(Axis.Z, ring_angle_degrees)
    pinion = make_output_pinion(role_index, spec)
    x, y = _polar(spec.output_axis_radius, spec.motor_station_angles[role_index])
    pinion_angle = ring_angle_degrees * spec.gear_ratio
    pinion = pinion.rotate(Axis((x, y, 0.0), (0.0, 0.0, 1.0)), pinion_angle)
    return ring, pinion


def make_guide_race(role_index: int, spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    """Compatibility reference for the integral rear T rail."""

    carrier_z0 = spec.carrier_layers[role_index][0]
    rail_bottom = carrier_z0 - spec.rail_total_depth
    flange = _annulus(
        spec.rail_flange_radii[0],
        spec.rail_flange_radii[1],
        spec.rail_flange_depth,
        rail_bottom,
    )
    neck = _annulus(
        spec.rail_neck_radii[0],
        spec.rail_neck_radii[1],
        spec.rail_neck_depth,
        carrier_z0 - spec.rail_neck_depth,
    )
    rail = flange.fuse(neck)
    rail.label = f"p3_v3_r2_{spec.roles[role_index]}_integral_rear_T_rail_REFERENCE"
    return rail


def _translated_r1(part, role_index: int, spec: P3V3FullRingR2Spec):
    shifted = part.moved(
        Location(
            (
                spec.station_radial_translation,
                0.0,
                spec.station_role_z_translations[role_index],
            )
        )
    )
    return _rotate_station(shifted, spec.motor_station_angles[role_index])


@lru_cache(maxsize=3)
def make_motor_station_parts(
    role_index: int,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    """The proven R1 station translated rigidly +0.50 mm and arrayed by role."""

    horizontal, vertical = r1_make_miter_pair()
    parts = [
        _translated_r1(r1_make_motor_body(), role_index, spec),
        _translated_r1(r1_make_motor_shaft(), role_index, spec),
        _translated_r1(horizontal, role_index, spec),
        _translated_r1(vertical, role_index, spec),
        _translated_r1(r1_make_output_shaft(), role_index, spec),
        _translated_r1(r1_make_bearing("lower"), role_index, spec),
        _translated_r1(r1_make_bearing("upper"), role_index, spec),
        _translated_r1(r1_make_role_spacer(role_index), role_index, spec),
        _translated_r1(r1_make_lower_miter_shim(), role_index, spec),
        _translated_r1(r1_make_lower_clamp_collar(), role_index, spec),
        _translated_r1(r1_make_motor_saddle(), role_index, spec),
        make_output_pinion(role_index, spec),
    ]
    for index, part in enumerate(parts):
        # STEP normalizes periods in product names to underscores.  Normalize
        # at source so Python-package and imported-STEP occurrence names are
        # byte-for-byte identical in parity checks.
        native_label = part.label.replace(".", "_")
        part.label = f"p3_v3_r2_{spec.roles[role_index]}_station_{index + 1:02d}_{native_label}"
    return tuple(parts)


def make_station_support_components(
    role_index: int,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    """Return the finite-overlap primitives of one station bracket."""

    x = spec.output_axis_radius
    mount_z0 = spec.chassis_z[1]
    mount_height = 1.0
    upper_z0 = spec.upper_bearing_range[0] + spec.station_support_clearance
    upper_height = spec.upper_bearing_range[1] - upper_z0

    # Motor/saddle chassis mount.  Its top is exactly the purchased saddle's
    # underside datum; the rear face meets the chassis without overlap.
    pad = Box(46.0, 27.0, mount_height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((92.0, 0.0, mount_z0))
    )
    # A finite radial bridge ties the motor pad to the bearing tower and both
    # lateral columns.  This was missing in the rejected three-solid bracket.
    chassis_bridge = Box(
        20.0, 21.0, mount_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((120.0, 0.0, mount_z0)))
    lower = Cylinder(6.0, 8.2, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x, 0.0, mount_z0))
    ).cut(
        Cylinder(4.10, 8.6, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x, 0.0, mount_z0 - 0.2))
        )
    )
    upper_annulus = Cylinder(6.0, upper_height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x, 0.0, upper_z0))
    ).cut(
        Cylinder(4.10, upper_height + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x, 0.0, upper_z0 - 0.2))
        )
    )
    components = [pad, chassis_bridge, lower, upper_annulus]
    for y in (-10.25, 10.25):
        # Columns sit outside the complete miter envelope (|Y| <= 8.88 mm),
        # leaving more than the frozen 0.15 mm clearance.
        pylon = Box(9.0, 2.0, -mount_z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x + 1.5, y, mount_z0))
        )
        # The upper side arm reaches the bearing annulus but begins 0.15 mm
        # above the vertical miter's reference envelope.
        arm_center_y = 7.875 if y > 0 else -7.875
        upper_arm = Box(
            12.0, 5.75, upper_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, arm_center_y, upper_z0)))
        components.extend((pylon, upper_arm))
    z_shift = spec.station_role_z_translations[role_index]
    rotated = tuple(
        _rotate_station(
            component.moved(Location((0.0, 0.0, z_shift))),
            spec.motor_station_angles[role_index],
        )
        for component in components
    )
    return rotated


@lru_cache(maxsize=3)
def make_station_support(role_index: int, spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    """One connected printable chassis/motor/two-bearing station bracket."""

    components = make_station_support_components(role_index, spec)
    support = components[0]
    for component in components[1:]:
        support = support.fuse(component)

    # This printed bracket supports the two MR84 outer races and the motor
    # saddle, but must not occupy the volume of any rigid station component.
    # Cut the assembled moving/electromechanical envelope after the bracket is
    # rotated into its final station.  The 0.15 mm shell is deliberately small:
    # bearing and saddle contact remain explicit, while the motor, shafts,
    # gears, spacer, shim, collar and output pinion have positive clearance.
    # Reuse the exact station occurrences already built for the assembly.
    # Rebuilding both miter gears and the pinion here for every role exhausted
    # OCC during full assembly generation even though their only purpose here
    # is to supply conservative bounding boxes.
    station_parts = make_motor_station_parts(role_index, spec)
    clearance_parts = tuple(
        part for index, part in enumerate(station_parts)
        if index not in (5, 6, 10)  # bearings contact; saddle datum contacts
    )
    for moving in clearance_parts:
        # Do not ask OCC to offset involute/miter faces: that operation is both
        # unstable and unnecessarily expensive.  A conservative axis-aligned
        # bounding envelope guarantees at least the stated clearance and is
        # deterministic in generation and tests.
        envelope = make_station_clearance_envelope(moving, spec.station_support_clearance)
        support = support.cut(envelope)
    support.label = f"p3_v3_r2_{spec.roles[role_index]}_internal_motor_and_bearing_support"
    support.color = srgb("#69737A")
    return support


def make_station_clearance_envelope(part, radial_clearance: float):
    """Conservative deterministic clearance box for a rigid station part."""

    bounds = part.bounding_box()
    allowance = 2.0 * radial_clearance
    envelope = Box(
        bounds.size.X + allowance,
        bounds.size.Y + allowance,
        bounds.size.Z + allowance,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location(bounds.center()))
    envelope.label = f"{part.label}_clearance_envelope_{radial_clearance:g}mm"
    return envelope


def _quarter_annulus(inner: float, outer: float, z0: float, z1: float, q: int):
    ring = _annulus(inner, outer, z1 - z0, z0)
    crop = Box(outer + 1.0, outer + 1.0, z1 - z0 + 0.4, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((0.0, 0.0, z0 - 0.2))
    )
    pieces = ring.intersect(crop)
    if not pieces:
        raise ValueError("quarter annulus crop produced no solid")
    return max(pieces, key=lambda shape: shape.volume).rotate(Axis.Z, 90.0 * q)


def make_frame_segments(spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    parts = []
    for q in range(4):
        part = _quarter_annulus(*spec.frame_radii, *spec.frame_z, q)
        part.label = f"p3_v3_r2_stationary_frame_quadrant_Q{q + 1}"
        part.color = srgb("#D8D0C2")
        parts.append(part)
    return tuple(parts)


def make_chassis_segments(spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    parts = []
    for q in range(4):
        part = _quarter_annulus(*spec.chassis_radii, *spec.chassis_z, q)
        part.label = f"p3_v3_r2_rear_chassis_quadrant_Q{q + 1}"
        part.color = srgb("#59636A")
        parts.append(part)
    return tuple(parts)


def make_keeper_saddle_parts(
    role_index: int,
    guide_index: int,
    radial_clearance: float | None = None,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    """Fixed lower yoke, removable PETG C-cap and POM/UHMW lower shoe.

    ``radial_clearance`` remains accepted for compatibility, but the corrected
    V3 channel is frozen at 0.25 mm per radial face.  It is deliberately not a
    tuning coupon: the whole keeper is a serviceable bolted assembly.
    """

    clearance = spec.keeper_radial_clearance if radial_clearance is None else radial_clearance
    if abs(clearance - spec.keeper_radial_clearance) > 1e-9:
        raise ValueError("corrected V3 keeper channel is frozen at 0.25 mm per side")
    angle = spec.guide_tower_angles[role_index][guide_index]
    carrier_z0 = spec.carrier_layers[role_index][0]
    rail_bottom = carrier_z0 - spec.rail_total_depth
    flange_top = carrier_z0 - spec.rail_neck_depth
    union_overlap = 0.10

    shoe_z0, shoe_z1 = spec.lower_shoe_range(role_index)
    bridge_z0, bridge_z1 = spec.upper_bridge_range(role_index)
    boss_z0, boss_z1 = spec.keeper_boss_range(role_index)

    # A 1.2 mm PETG sole supports the replaceable shoe.  The 0.8 mm inner lip
    # is a frozen capture feature and the R143..145.1 spine ties the keeper to
    # the stationary frame without entering the R<=143 moving/optical lanes.
    sole = _annular_sector(
        spec.keeper_channel_radii[0] - spec.keeper_capture_radial,
        spec.keeper_cap_outer_radius,
        spec.keeper_tangential_width,
        shoe_z0 - spec.keeper_structural_wall_min,
        shoe_z0,
    )
    inner_lip = _annular_sector(
        spec.keeper_channel_radii[0] - spec.keeper_capture_radial,
        spec.keeper_channel_radii[0],
        spec.keeper_tangential_width,
        shoe_z0 - spec.keeper_structural_wall_min,
        bridge_z1,
    )
    anchor_z0 = min(spec.frame_z[0], shoe_z0 - spec.keeper_structural_wall_min)
    anchor_z1 = max(spec.frame_z[1], shoe_z0)
    anchor = _annular_sector(
        spec.keeper_cap_outer_radius - 0.2,
        spec.frame_radii[0] + union_overlap,
        spec.keeper_tangential_width,
        anchor_z0,
        anchor_z1,
    )
    fixed = sole.fuse(inner_lip).fuse(anchor)

    # The cap bosses occupy the sole's outer field.  Clear their complete OD,
    # then add a true lower-yoke ear under each boss with the frozen D2.8 screw
    # passage.  The ear is joined to the outer stationary spine.
    tangent_axis_x = sqrt(
        spec.keeper_fastener_axis_radius**2
        - spec.keeper_fastener_tangent_offsets[1] ** 2
    )
    for tangent in spec.keeper_fastener_tangent_offsets:
        boss_clear = Cylinder(
            spec.keeper_boss_outer_diameter / 2.0 + 0.20,
            boss_z1 - boss_z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((tangent_axis_x, tangent, boss_z0 - 0.2)))
        fixed = fixed.cut(boss_clear)
        ear = Cylinder(
            spec.keeper_boss_outer_diameter / 2.0,
            spec.keeper_structural_wall_min,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((tangent_axis_x, tangent, boss_z0 - spec.keeper_structural_wall_min)))
        passage = Cylinder(
            spec.keeper_cap_fastener_clearance_diameter / 2.0,
            spec.keeper_structural_wall_min + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((tangent_axis_x, tangent, boss_z0 - spec.keeper_structural_wall_min - 0.2)))
        ear = ear.cut(passage)
        ear_rib = Box(
            spec.frame_radii[0] + union_overlap - tangent_axis_x,
            spec.keeper_boss_outer_diameter,
            spec.keeper_structural_wall_min,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((tangent_axis_x, tangent, boss_z0 - spec.keeper_structural_wall_min)))
        fixed = fixed.fuse(ear).fuse(ear_rib)
    fixed = fixed.rotate(Axis.Z, angle)
    fixed.label = f"p3_v3_r2_{spec.roles[role_index]}_keeper_{guide_index + 1}_fixed_lower_yoke"
    fixed.color = srgb("#7A8388")

    # The removable one-sided C-cap overlaps the outer half of the T flange by
    # exactly 0.8 mm.  Its outer lip supplies the 0.25 mm radial guide face and
    # has more than the frozen 1.6 mm axial capture height.
    upper_bridge = _annular_sector(
        spec.rail_neck_radii[1],
        spec.keeper_cap_outer_radius,
        spec.keeper_tangential_width,
        bridge_z0,
        bridge_z1,
    )
    outer_lip = _annular_sector(
        spec.keeper_channel_radii[1],
        spec.keeper_channel_radii[1] + spec.keeper_capture_radial,
        spec.keeper_tangential_width,
        shoe_z0,
        bridge_z1,
    )
    cap = upper_bridge.fuse(outer_lip)
    for tangent in spec.keeper_fastener_tangent_offsets:
        boss = Cylinder(
            spec.keeper_boss_outer_diameter / 2.0,
            spec.keeper_boss_depth,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((tangent_axis_x, tangent, boss_z0)))
        pilot = Cylinder(
            spec.keeper_insert_pilot_diameter / 2.0,
            spec.keeper_insert_pilot_depth,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((tangent_axis_x, tangent, boss_z1)))
        screw_entry = Cylinder(
            spec.keeper_cap_fastener_clearance_diameter / 2.0,
            spec.keeper_boss_depth + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((tangent_axis_x, tangent, boss_z0 - 0.2)))
        cap = cap.fuse(boss.cut(pilot).cut(screw_entry))
    cap = cap.rotate(Axis.Z, angle)
    cap.label = f"p3_v3_r2_{spec.roles[role_index]}_keeper_{guide_index + 1}_M2p5_removable_outer_cap"
    cap.color = srgb("#AEB5B9")

    shoe = _annular_sector(
        spec.keeper_channel_radii[0],
        spec.keeper_channel_radii[1],
        spec.keeper_tangential_width - 0.4,
        shoe_z0,
        shoe_z1,
    ).rotate(Axis.Z, angle)
    shoe.label = (
        f"p3_v3_r2_{spec.roles[role_index]}_keeper_{guide_index + 1}_"
        f"{spec.keeper_liner_material}_lower_shoe_C{clearance:.2f}"
    )
    shoe.color = srgb("#E7E0CF")
    return fixed, cap, shoe


def make_keeper_fastener_references(
    role_index: int,
    guide_index: int,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    """Two M2.5x10 button screws and two 3.8x4 heat-set inserts."""

    angle = spec.guide_tower_angles[role_index][guide_index]
    bridge_top = spec.upper_bridge_range(role_index)[1]
    x = sqrt(
        spec.keeper_fastener_axis_radius**2
        - spec.keeper_fastener_tangent_offsets[1] ** 2
    )
    parts = []
    for index, tangent in enumerate(spec.keeper_fastener_tangent_offsets):
        screw = Cylinder(
            spec.keeper_cap_fastener_nominal_diameter / 2.0,
            spec.keeper_cap_screw_length,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((x, tangent, bridge_top)))
        head = Cylinder(
            spec.keeper_cap_button_head_diameter / 2.0,
            spec.keeper_cap_button_head_height,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((x, tangent, bridge_top - spec.keeper_cap_screw_length)))
        screw = screw.fuse(head).rotate(Axis.Z, angle)
        screw.label = (
            f"p3_v3_r2_{spec.roles[role_index]}_keeper_{guide_index + 1}_"
            f"M2p5x10_button_screw_{index + 1}_REFERENCE"
        )
        screw.color = srgb("#59636A")
        insert = Cylinder(
            spec.keeper_insert_outer_diameter / 2.0,
            spec.keeper_insert_length,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((x, tangent, bridge_top))).rotate(Axis.Z, angle)
        insert.label = (
            f"p3_v3_r2_{spec.roles[role_index]}_keeper_{guide_index + 1}_"
            f"M2p5_heat_set_insert_{index + 1}_REFERENCE"
        )
        insert.color = srgb("#C59B45")
        parts.extend((screw, insert))
    return tuple(parts)


def make_guide_tower(
    role_index: int,
    guide_index: int,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    """Compatibility name for the complete nominal rear keeper saddle."""

    parts = make_keeper_saddle_parts(role_index, guide_index, spec=spec)
    return Compound(
        children=list(parts),
        label=f"p3_v3_r2_{spec.roles[role_index]}_rear_keeper_{guide_index + 1}",
    )


def keeper_service_offset(
    role_index: int,
    guide_index: int,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
) -> tuple[float, float, float]:
    """Frozen radially-outward cap-removal vector after both screws are out."""

    angle = spec.guide_tower_angles[role_index][guide_index]
    dx, dy = _polar(spec.keeper_service_radial_travel, angle)
    return dx, dy, 0.0


def make_outer_front_ring_segments(spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    base = _annulus(
        spec.retainer_radii[0],
        spec.retainer_radii[1],
        spec.retainer_z[1] - spec.retainer_z[0],
        spec.retainer_z[0],
    )
    for angle in spec.retainer_fastener_angles:
        x, y = _polar(spec.retainer_fastener_radius, angle)
        base = base.cut(
            Cylinder(
                spec.retainer_clearance_hole / 2.0,
                spec.retainer_z[1] - spec.retainer_z[0] + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, spec.retainer_z[0] - 0.2)))
        )
    parts = []
    for q in range(4):
        crop = Box(151.0, 151.0, 1.8, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
            Location((0.0, 0.0, spec.retainer_z[0] - 0.4))
        )
        pieces = base.intersect(crop.rotate(Axis.Z, 90.0 * q))
        if not pieces:
            raise ValueError("outer front ring quadrant crop produced no solid")
        part = max(pieces, key=lambda shape: shape.volume)
        part.label = f"p3_v3_r2_stationary_outer_front_ring_quadrant_Q{q + 1}"
        part.color = srgb("#C8BBA8")
        parts.append(part)
    return tuple(parts)


def make_outer_front_ring_posts(spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    posts = []
    for index, angle in enumerate(spec.retainer_fastener_angles):
        x, y = _polar(spec.retainer_fastener_radius, angle)
        post = Cylinder(1.5, spec.retainer_z[0] - spec.frame_z[1], align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x, y, spec.frame_z[1]))
        )
        post.label = f"p3_v3_r2_stationary_outer_front_ring_post_{index + 1}"
        post.color = srgb("#69737A")
        posts.append(post)
    return tuple(posts)


# Compatibility aliases for older call sites.  New assemblies and viewer trees
# use the optical/structural name; this ring no longer retains moving carriers.
make_retainer_segments = make_outer_front_ring_segments
make_retainer_posts = make_outer_front_ring_posts


def make_assembled(spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    children = [*make_chassis_segments(spec), *make_frame_segments(spec)]
    for role in range(3):
        children.extend(make_ring_quadrants(role, spec))
        children.extend(make_seam_hardware(role, spec))
        children.extend(make_motor_station_parts(role, spec))
        children.append(make_station_support(role, spec))
        for guide in range(3):
            children.extend(make_keeper_saddle_parts(role, guide, spec=spec))
            children.extend(make_keeper_fastener_references(role, guide, spec=spec))
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(make_outer_front_ring_segments(spec))
    return Compound(children=children, label="p3_v3_r2_COMPLETE_three_ring_three_motor_assembly")


def make_stationary_module(spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    """Stationary structure exported separately to bound OCC memory."""

    return Compound(
        children=[
            *make_chassis_segments(spec),
            *make_frame_segments(spec),
            *make_outer_front_ring_posts(spec),
            *make_outer_front_ring_segments(spec),
        ],
        label="p3_v3_r2_stationary_chassis_frame_and_outer_front_ring",
    )


def make_role_module(
    role_index: int,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    """One complete moving/drive role for fresh-process staged export."""

    children = [*make_ring_quadrants(role_index, spec)]
    children.extend(make_seam_hardware(role_index, spec))
    children.extend(make_motor_station_parts(role_index, spec))
    children.append(make_station_support(role_index, spec))
    for guide in range(3):
        children.extend(make_keeper_saddle_parts(role_index, guide, spec=spec))
        children.extend(make_keeper_fastener_references(role_index, guide, spec=spec))
    return Compound(
        children=children,
        label=f"p3_v3_r2_{spec.roles[role_index]}_complete_role_module",
    )


def make_service_exploded(spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    children = [*make_chassis_segments(spec)]
    children.extend(part.moved(Location((0.0, 0.0, 4.0))) for part in make_frame_segments(spec))
    for role in range(3):
        z_lift = 15.0 + 13.0 * role
        radial = 8.0 * role
        for quadrant in make_ring_quadrants(role, spec):
            children.append(quadrant.moved(Location((radial, 0.0, z_lift))))
        children.extend(
            hardware.moved(Location((radial, 0.0, z_lift)))
            for hardware in make_seam_hardware(role, spec)
        )
        for station_part in make_motor_station_parts(role, spec):
            children.append(station_part.moved(Location((0.0, 0.0, -12.0 - 8.0 * role))))
        children.append(make_station_support(role, spec))
        for guide in range(3):
            fixed, cap, shoe = make_keeper_saddle_parts(role, guide, spec=spec)
            dx, dy, dz = keeper_service_offset(role, guide, spec)
            children.append(fixed)
            children.append(shoe)
            children.append(cap.moved(Location((dx, dy, dz))))
            fasteners = make_keeper_fastener_references(role, guide, spec)
            for index, fastener in enumerate(fasteners):
                if index % 2 == 0:  # screw removed rearward before radial cap extraction
                    children.append(fastener.moved(Location((dx, dy, -14.0))))
                else:  # heat-set insert remains in the removable cap
                    children.append(fastener.moved(Location((dx, dy, dz))))
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(
        part.moved(Location((0.0, 0.0, 58.0)))
        for part in make_outer_front_ring_segments(spec)
    )
    return Compound(children=children, label="p3_v3_r2_COMPLETE_service_exploded")


def make_stationary_service_module(spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2):
    children = [*make_chassis_segments(spec)]
    children.extend(part.moved(Location((0.0, 0.0, 4.0))) for part in make_frame_segments(spec))
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(
        part.moved(Location((0.0, 0.0, 58.0)))
        for part in make_outer_front_ring_segments(spec)
    )
    return Compound(children=children, label="p3_v3_r2_stationary_service_module")


def make_role_service_module(
    role_index: int,
    spec: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2,
):
    z_lift = 15.0 + 13.0 * role_index
    radial = 8.0 * role_index
    children = [
        quadrant.moved(Location((radial, 0.0, z_lift)))
        for quadrant in make_ring_quadrants(role_index, spec)
    ]
    children.extend(
        hardware.moved(Location((radial, 0.0, z_lift)))
        for hardware in make_seam_hardware(role_index, spec)
    )
    children.extend(
        part.moved(Location((0.0, 0.0, -12.0 - 8.0 * role_index)))
        for part in make_motor_station_parts(role_index, spec)
    )
    children.append(make_station_support(role_index, spec))
    for guide in range(3):
        fixed, cap, shoe = make_keeper_saddle_parts(role_index, guide, spec=spec)
        dx, dy, dz = keeper_service_offset(role_index, guide, spec)
        children.append(fixed)
        children.append(shoe)
        children.append(cap.moved(Location((dx, dy, dz))))
        fasteners = make_keeper_fastener_references(role_index, guide, spec)
        for index, fastener in enumerate(fasteners):
            if index % 2 == 0:
                children.append(fastener.moved(Location((dx, dy, -14.0))))
            else:
                children.append(fastener.moved(Location((dx, dy, dz))))
    return Compound(
        children=children,
        label=f"p3_v3_r2_{spec.roles[role_index]}_service_role_module",
    )


PRIMARY_FACTORIES = (
    ("assembled", make_assembled),
    ("service_exploded", make_service_exploded),
)
