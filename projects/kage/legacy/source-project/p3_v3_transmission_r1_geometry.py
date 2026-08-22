"""STEP-first geometry for the isolated P3 V3 transmission R1 coupon.

The accepted 300 mm P3 V3 rings and fins are intentionally not imported or
modified here.  This file proves one real motor/shaft/bearing/gear station and
uses only a short 259T internal-ring arc as its load interface.
"""

from __future__ import annotations

from math import pi, radians

import py_gearworks as pgw
from build123d import Align, Axis, Box, Compound, Cylinder, Location
from cadgen import srgb

from p3_v3_transmission_r1_spec import (
    P3V3TransmissionR1Spec,
    P3_V3_TRANSMISSION_R1,
)


def _annulus(inner_radius: float, outer_radius: float, height: float, z0: float):
    outer = Cylinder(
        outer_radius,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, z0)))
    inner = Cylinder(
        inner_radius,
        height + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, z0 - 0.2)))
    return outer.cut(inner)


def _positive_intersection_volume(a, b) -> float:
    total = 0.0
    for first in a.solids():
        for second in b.solids():
            total += sum(
                max(0.0, float(piece.volume))
                for piece in (first.intersect(second) or [])
            )
    return total


def _radial_set_screw_hole(center_x: float, center_z: float, diameter: float):
    return Cylinder(
        diameter / 2.0,
        14.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90.0).moved(Location((center_x, 0.0, center_z)))


def _d_prism_x(
    x0: float,
    x1: float,
    center_z: float,
    diameter: float,
    across_flat: float,
):
    """Return a D-section prism whose axis is X and flat is on +Z."""

    if not 0.0 < across_flat < diameter:
        raise ValueError("D-shaft across-flat must be positive and below diameter")
    center_x = (x0 + x1) / 2.0
    cylinder = Cylinder(
        diameter / 2.0,
        x1 - x0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).moved(Location((center_x, 0.0, center_z)))
    # The box retains the circular section from -R through the flat plane.
    limiter = Box(
        x1 - x0 + 0.4,
        diameter + 0.4,
        across_flat,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((center_x, 0.0, center_z - diameter / 2.0)))
    fragments = cylinder.intersect(limiter)
    if not fragments:
        raise ValueError("D-prism crop produced no solid")
    return max(fragments, key=lambda shape: shape.volume)


def _d_prism_z(
    center_x: float,
    z0: float,
    z1: float,
    diameter: float,
    across_flat: float,
):
    """Return a Z-axis D prism whose flat faces the +Y service side."""

    if not 0.0 < across_flat < diameter:
        raise ValueError("D-shaft across-flat must be positive and below diameter")
    center_z = (z0 + z1) / 2.0
    cylinder = Cylinder(
        diameter / 2.0,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((center_x, 0.0, center_z)))
    limiter = Box(
        diameter + 0.4,
        across_flat,
        z1 - z0 + 0.4,
        align=(Align.CENTER, Align.MIN, Align.CENTER),
    ).moved(Location((center_x, -diameter / 2.0, center_z)))
    fragments = cylinder.intersect(limiter)
    if not fragments:
        raise ValueError("Z-axis D-prism crop produced no solid")
    return max(fragments, key=lambda shape: shape.volume)


def _one_sided_radial_passage(
    center_x: float,
    center_z: float,
    flat_y: float,
    outer_radius: float,
    diameter: float = 1.6,
):
    """M2 tap pilot from the +Y outside face to the D-flat."""

    y0 = flat_y - 0.05
    y1 = outer_radius + 0.30
    return Cylinder(
        diameter / 2.0,
        y1 - y0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90.0).moved(
        Location((center_x, (y0 + y1) / 2.0, center_z))
    )


def _m2_grub_screw_reference(
    label: str,
    center_x: float,
    center_z: float,
    flat_y: float,
    outer_radius: float,
    core_diameter: float,
):
    """M2 thread-core envelope with its flat tip seated on the D-shaft."""

    y0 = flat_y
    y1 = outer_radius + 0.20
    screw = Cylinder(
        core_diameter / 2.0,
        y1 - y0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.X, 90.0).moved(
        Location((center_x, (y0 + y1) / 2.0, center_z))
    )
    screw.label = f"p3_v3_r1_purchased_M2_grub_screw_{label}_REFERENCE"
    screw.color = srgb("#6B7074")
    return screw


def _miter_wrappers(spec: P3V3TransmissionR1Spec):
    cone_angles = pgw.cone_angle_from_teeth(spec.miter_teeth, spec.miter_teeth)
    common = dict(
        number_of_teeth=spec.miter_teeth,
        module=spec.miter_module,
        height=spec.miter_face_width,
        helix_angle=0.0,
        pressure_angle=radians(spec.miter_pressure_angle_degrees),
        backlash=0.10,
        tip_truncation=0.10,
        enable_undercut=True,
    )
    vertical = pgw.BevelGear(cone_angle=float(cone_angles[0]), **common)
    horizontal = pgw.BevelGear(cone_angle=float(cone_angles[1]), **common)
    horizontal.mesh_to(
        vertical,
        target_dir=pgw.LEFT,
        backlash=spec.miter_mesh_backlash,
    )
    return vertical, horizontal


def make_miter_pair(spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1):
    """Return the real 16T straight-miter pair on the frozen X/Z axes."""
    vertical_wrapper, horizontal_wrapper = _miter_wrappers(spec)
    # py-gearworks builds this pair around a local intersection at Z=8.  Flip
    # around that intersection so the motor lies toward the clock centre, then
    # place the common intersection on the frozen station datum.
    flip_axis = Axis((0.0, 0.0, 8.0), (1.0, 0.0, 0.0))
    placement = Location((spec.output_axis_radius, 0.0, -20.0))
    vertical = vertical_wrapper.build_part().solid().rotate(flip_axis, 180.0).moved(placement)
    horizontal = horizontal_wrapper.build_part().solid().rotate(flip_axis, 180.0).moved(placement)

    # Keep the real bevel teeth, but end the vertical gear 0.10 mm below the
    # upper bearing.  The explicit clamp hub provides a deterministic datum.
    trim = Box(40.0, 40.0, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((spec.output_axis_radius, 0.0, spec.miter_vertical_hub_top_z))
    )
    vertical = vertical.cut(trim)
    vertical_hub = Cylinder(
        spec.miter_vertical_hub_diameter / 2.0,
        spec.miter_vertical_hub_height,
        align=(Align.CENTER, Align.CENTER, Align.MAX),
    ).moved(Location((spec.output_axis_radius, 0.0, spec.miter_vertical_hub_top_z)))
    vertical = vertical.fuse(vertical_hub)
    vertical = vertical.cut(
        _d_prism_z(
            spec.output_axis_radius,
            spec.miter_axis_intersection_z - 8.0,
            spec.miter_vertical_hub_top_z + 0.2,
            spec.miter_output_bore_diameter,
            spec.miter_output_bore_across_flat,
        )
    )
    vertical = vertical.cut(
        _one_sided_radial_passage(
            spec.output_axis_radius,
            spec.miter_vertical_hub_top_z - spec.miter_vertical_hub_height / 2.0,
            spec.output_shaft_flat_y,
            spec.miter_outer_radius + 0.30,
            spec.m2_tap_pilot_diameter,
        )
    )

    # Add a positive hub around the real 4 x 7 mm D-shaft.  The bore preserves
    # the 3.60 mm mating flat, so motor torque is not assigned to friction or a
    # decorative round envelope.
    horizontal_center_x = sum(spec.nominal_motor_shaft_range) / 2.0
    horizontal_hub_x = (111.8, 119.0)
    horizontal_hub = Cylinder(
        spec.miter_vertical_hub_diameter / 2.0,
        horizontal_hub_x[1] - horizontal_hub_x[0],
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).moved(
        Location((sum(horizontal_hub_x) / 2.0, 0.0, spec.miter_axis_intersection_z))
    )
    horizontal = horizontal.fuse(horizontal_hub)
    horizontal = horizontal.cut(
        _d_prism_x(
            horizontal_hub_x[0] - 0.2,
            horizontal_hub_x[1] + 0.2,
            spec.miter_axis_intersection_z,
            spec.motor_miter_bore_diameter,
            spec.motor_miter_bore_across_flat,
        )
    )
    # The matching D-bore is the positive motor torque path.  This hub does not
    # carry a redundant radial screw whose axis would miss the motor's +Z flat.

    vertical.label = "p3_v3_r1_real_M1_16T_vertical_miter_clamp_hub"
    horizontal.label = "p3_v3_r1_real_M1_16T_horizontal_miter_clamp_hub"
    vertical.color = horizontal.color = srgb("#D9A441")
    return horizontal, vertical


def _spur_wrappers(role_index: int, spec: P3V3TransmissionR1Spec):
    face_z0, _ = spec.pinion_face_range(role_index)
    ring = pgw.SpurRingGear(
        number_of_teeth=spec.ring_teeth,
        module=spec.ring_module,
        height=spec.output_face_width,
        center=[0.0, 0.0, face_z0],
        backlash=0.10,
    )
    pinion = pgw.SpurGear(
        number_of_teeth=spec.output_pinion_teeth,
        module=spec.ring_module,
        height=spec.output_face_width,
        center=[0.0, 0.0, face_z0],
        pressure_angle=radians(20.0),
        backlash=0.10,
        tip_truncation=0.10,
        enable_undercut=True,
    )
    pinion.mesh_to(ring, target_dir=pgw.RIGHT, backlash=spec.output_mesh_backlash)
    return ring, pinion


def make_ring_arc(
    role_index: int,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    ring_wrapper, _ = _spur_wrappers(role_index, spec)
    full_ring = ring_wrapper.build_part().solid()
    # Short inspectable coupon: enough teeth to judge mesh, not a duplicate of
    # the accepted 300 mm carrier ring.
    sx, sy, sz = (22.0, 44.0, 3.6)
    z0, _ = spec.pinion_face_range(role_index)
    crop = Box(
        sx,
        sy,
        sz,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((spec.ring_pitch_radius - 0.5, 0.0, z0 - 0.4)))
    fragments = full_ring.intersect(crop)
    if not fragments:
        raise ValueError("259T internal-ring crop produced no solid")
    arc = max(fragments, key=lambda shape: shape.volume)
    arc.label = f"p3_v3_r1_{spec.roles[role_index]}_true_M1_259T_ring_arc"
    arc.color = srgb(("#3F8F87", "#E38B48", "#D95D78")[role_index])
    return arc


def make_ring_arc_carriage(
    role_index: int,
    offset_y: float = 0.0,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    """Fuse the true ring arc to a short-stroke tangential backing tongue."""

    if abs(offset_y) > spec.slider_half_stroke + 1e-9:
        raise ValueError("ring-arc carriage exceeds the captured test stroke")
    face_z0, face_z1 = spec.pinion_face_range(role_index)
    x0, x1 = spec.slider_carriage_x
    backing = Box(
        x1 - x0,
        2.0 * spec.slider_carriage_half_length_y,
        face_z1 - face_z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location(((x0 + x1) / 2.0, 0.0, face_z0)))
    carriage = make_ring_arc(role_index, spec).fuse(backing)
    carriage = carriage.moved(Location((0.0, offset_y, 0.0)))
    carriage.label = (
        f"p3_v3_r1_{spec.roles[role_index]}_259T_arc_captured_carriage_"
        f"Y{offset_y:+.2f}"
    )
    carriage.color = srgb(("#3F8F87", "#E38B48", "#D95D78")[role_index])
    return carriage


def make_arc_slider_rails(
    role_index: int,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    """Return lower guide/hard-stops and removable upper capture retainer."""

    face_z0, face_z1 = spec.pinion_face_range(role_index)
    rail_x0, rail_x1 = spec.slider_rail_x
    rail_w = rail_x1 - rail_x0
    rail_y = 2.0 * spec.slider_rail_y_half_length
    t = spec.slider_rail_thickness_z
    c = spec.slider_running_clearance
    lower_z0 = face_z0 - c - t
    upper_z0 = face_z1 + c

    lower = Box(
        rail_w,
        rail_y,
        t,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location(((rail_x0 + rail_x1) / 2.0, 0.0, lower_z0)))
    # The outside wall sets the 0.30 mm radial running clearance.
    outer_wall = Box(
        t,
        rail_y,
        upper_z0 - lower_z0,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((spec.slider_carriage_x[1] + c, 0.0, lower_z0)))
    lower = lower.fuse(outer_wall)
    # Hard stops contact the backing tongue only at +/- the frozen stroke.
    stop_x0 = 132.10
    stop_x1 = spec.slider_carriage_x[1] + c + t
    stop_depth_y = 1.0
    for sign in (-1.0, 1.0):
        inner_face = sign * spec.slider_rail_y_half_length
        center_y = inner_face + sign * stop_depth_y / 2.0
        stop = Box(
            stop_x1 - stop_x0,
            stop_depth_y,
            upper_z0 - lower_z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location(((stop_x0 + stop_x1) / 2.0, center_y, lower_z0)))
        lower = lower.fuse(stop)
    # Two printed posts form the load path to the removable upper retainer.
    # Their feet overlap the lower guide and their 1.60 mm holes are M2 pilots.
    for fastener_y in spec.slider_retainer_fastener_y:
        foot = Box(
            spec.slider_retainer_outer_x - 140.80,
            spec.slider_retainer_post_diameter,
            t,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(
            Location(
                (
                    (140.80 + spec.slider_retainer_outer_x) / 2.0,
                    fastener_y,
                    lower_z0,
                )
            )
        )
        post = Cylinder(
            spec.slider_retainer_post_diameter / 2.0,
            upper_z0 - lower_z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.slider_retainer_fastener_x, fastener_y, lower_z0)))
        pilot = Cylinder(
            spec.m2_tap_pilot_diameter / 2.0,
            upper_z0 - lower_z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.slider_retainer_fastener_x, fastener_y, lower_z0 - 0.2)))
        lower = lower.fuse(foot).fuse(post).cut(pilot)
    lower.label = "p3_v3_r1_arc_slider_lower_guide_with_hard_stops"
    lower.color = srgb("#69737A")

    upper = Box(
        spec.slider_retainer_outer_x - rail_x0,
        rail_y,
        t,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location(((rail_x0 + spec.slider_retainer_outer_x) / 2.0, 0.0, upper_z0)))
    for fastener_y in spec.slider_retainer_fastener_y:
        upper = upper.cut(
            Cylinder(
                spec.slider_retainer_clearance_hole / 2.0,
                t + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(
                Location(
                    (
                        spec.slider_retainer_fastener_x,
                        fastener_y,
                        upper_z0 - 0.2,
                    )
                )
            )
        )
    upper.label = "p3_v3_r1_arc_slider_removable_upper_retainer"
    upper.color = srgb("#AEB5B9")
    return lower, upper


def make_arc_retainer_screw_references(
    role_index: int,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    """Two purchased M2 screws fastening the removable slider retainer."""

    _, face_z1 = spec.pinion_face_range(role_index)
    upper_z0 = face_z1 + spec.slider_running_clearance
    screws = []
    for index, fastener_y in enumerate(spec.slider_retainer_fastener_y):
        core_z0 = upper_z0 - 3.0
        core = Cylinder(
            spec.m2_tap_pilot_diameter / 2.0,
            3.0 + spec.slider_rail_thickness_z + 0.1,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.slider_retainer_fastener_x, fastener_y, core_z0)))
        head = Cylinder(
            1.9,
            1.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(
            Location(
                (
                    spec.slider_retainer_fastener_x,
                    fastener_y,
                    upper_z0 + spec.slider_rail_thickness_z,
                )
            )
        )
        screw = core.fuse(head)
        screw.label = f"p3_v3_r1_purchased_M2_upper_slider_retainer_screw_{index+1}_REFERENCE"
        screw.color = srgb("#6B7074")
        screws.append(screw)
    return tuple(screws)


def make_output_pinion(
    role_index: int,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    _, pinion_wrapper = _spur_wrappers(role_index, spec)
    pinion = pinion_wrapper.build_part().solid()
    face_z0, _ = spec.pinion_face_range(role_index)
    hub = Cylinder(
        spec.output_pinion_hub_diameter / 2.0,
        spec.output_pinion_hub_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((spec.output_axis_radius, 0.0, face_z0)))
    body = pinion.fuse(hub)
    bore = _d_prism_z(
        spec.output_axis_radius,
        face_z0 - 0.2,
        face_z0 + spec.output_face_width + 0.2,
        spec.output_pinion_bore_diameter,
        spec.output_pinion_bore_across_flat,
    )
    body = body.cut(bore)
    output_screw_z = face_z0 + 1.25
    body = body.cut(
        _one_sided_radial_passage(
            spec.output_axis_radius,
            output_screw_z,
            spec.output_shaft_flat_y,
            spec.output_pinion_outer_radius + 0.30,
            spec.m2_tap_pilot_diameter,
        )
    )
    body.label = f"p3_v3_r1_{spec.roles[role_index]}_true_M1_16T_output_pinion_clamp_hub"
    body.color = srgb("#D9A441")
    return body


def make_output_shaft(spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1):
    shaft = _d_prism_z(
        spec.output_axis_radius,
        spec.output_shaft_z[0],
        spec.output_shaft_z[1],
        spec.output_shaft_diameter,
        spec.output_shaft_across_flat,
    )
    shaft.label = "p3_v3_r1_purchased_4x40mm_vertical_D_steel_shaft_3p5AF"
    shaft.color = srgb("#B9C0C5")
    return shaft


def make_motor_shaft(spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1):
    x0, x1 = spec.nominal_motor_shaft_range
    shaft = _d_prism_x(
        x0,
        x1,
        spec.miter_axis_intersection_z,
        spec.motor_shaft_diameter,
        spec.motor_shaft_across_flat,
    )
    shaft.label = "p3_v3_r1_actual_4x7mm_NEMA8_D_shaft_3p5AF_UNTRUNCATED"
    shaft.color = srgb("#B9C0C5")
    return shaft


def make_motor_body(spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1):
    z0 = spec.miter_axis_intersection_z - spec.motor_face_size / 2.0
    body = Box(
        spec.motor_body_length,
        spec.motor_face_size,
        spec.motor_face_size,
        align=(Align.MAX, Align.CENTER, Align.MIN),
    ).moved(Location((spec.motor_face_radius, 0.0, z0)))
    body.label = "p3_v3_r1_NEMA8_20p3_face_x_39p3_body_REFERENCE"
    body.color = srgb("#424A50")
    return body


def make_bearing(
    which: str,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    z_range = spec.lower_bearing_range if which == "lower" else spec.upper_bearing_range
    center = sum(z_range) / 2.0
    bearing = _annulus(
        spec.bearing_id / 2.0,
        spec.bearing_od / 2.0,
        spec.bearing_width,
        center - spec.bearing_width / 2.0,
    ).moved(Location((spec.output_axis_radius, 0.0, 0.0)))
    bearing.label = f"p3_v3_r1_MR84ZZ_4x8x3_{which}_bearing_REFERENCE"
    bearing.color = srgb("#778187")
    return bearing


def make_role_spacer(
    role_index: int,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    z0 = spec.upper_common_datum_z + spec.spacer_axial_relief
    z1 = z0 + spec.spacer_length(role_index)
    spacer = _annulus(
        spec.spacer_bore_diameter / 2.0,
        spec.spacer_outer_diameter / 2.0,
        z1 - z0,
        z0,
    ).moved(Location((spec.output_axis_radius, 0.0, 0.0)))
    spacer.label = f"p3_v3_r1_{spec.roles[role_index]}_role_spacer_L{z1-z0:.2f}"
    spacer.color = srgb(("#3F8F87", "#E38B48", "#D95D78")[role_index])
    return spacer


def make_lower_miter_shim(spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1):
    lower_top = spec.lower_bearing_range[1]
    z0 = lower_top + spec.target_endplay / 2.0
    z1 = spec.miter_vertical_hub_top_z - spec.miter_vertical_hub_height - 0.10
    shim = _annulus(
        spec.spacer_bore_diameter / 2.0,
        spec.spacer_outer_diameter / 2.0,
        z1 - z0,
        z0,
    ).moved(Location((spec.output_axis_radius, 0.0, 0.0)))
    # The long thrust sleeve passes the orthogonal motor shaft and reaches the
    # clamped vertical-miter hub.  Remove only those real hardware envelopes;
    # the remaining C-section stays one printable, shaft-guided part.
    motor_clearance = _d_prism_x(
        spec.motor_face_radius - 0.2,
        spec.worst_case_motor_shaft_tip_radius + 0.2,
        spec.miter_axis_intersection_z,
        spec.motor_shaft_diameter + 0.30,
        spec.motor_shaft_across_flat + 0.30,
    )
    horizontal, vertical = make_miter_pair(spec)
    shim = shim.cut(motor_clearance).cut(horizontal).cut(vertical)
    shim.label = "p3_v3_r1_lower_bearing_to_miter_drive_spacer"
    shim.color = srgb("#AEB5B9")
    return shim


def make_lower_clamp_collar(
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    z0, z1 = spec.lower_collar_z
    collar = Cylinder(
        spec.spacer_outer_diameter / 2.0,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((spec.output_axis_radius, 0.0, z0)))
    collar = collar.cut(
        _d_prism_z(
            spec.output_axis_radius,
            z0 - 0.2,
            z1 + 0.2,
            spec.output_pinion_bore_diameter,
            spec.output_pinion_bore_across_flat,
        )
    )
    collar = collar.cut(
        _one_sided_radial_passage(
            spec.output_axis_radius,
            spec.lower_collar_screw_z,
            spec.output_shaft_flat_y,
            spec.spacer_outer_diameter / 2.0,
            spec.m2_tap_pilot_diameter,
        )
    )
    collar.label = "p3_v3_r1_lower_D_collar_M2_tap_pilot"
    collar.color = srgb("#B9C0C5")
    return collar


def make_set_screw_references(
    role_index: int,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    """Three secondary M2 retainers whose flat tips seat on the output D-flat."""

    face_z0, _ = spec.pinion_face_range(role_index)
    return (
        _m2_grub_screw_reference(
            "vertical_miter_hub",
            spec.output_axis_radius,
            spec.miter_vertical_hub_top_z - spec.miter_vertical_hub_height / 2.0,
            spec.output_shaft_flat_y,
            spec.miter_outer_radius + 0.30,
            spec.m2_tap_pilot_diameter,
        ),
        _m2_grub_screw_reference(
            f"{spec.roles[role_index]}_output_pinion",
            spec.output_axis_radius,
            face_z0 + 1.25,
            spec.output_shaft_flat_y,
            spec.output_pinion_outer_radius + 0.30,
            spec.m2_tap_pilot_diameter,
        ),
        _m2_grub_screw_reference(
            "lower_clamp_collar",
            spec.output_axis_radius,
            spec.lower_collar_screw_z,
            spec.output_shaft_flat_y,
            spec.spacer_outer_diameter / 2.0,
            spec.m2_tap_pilot_diameter,
        ),
    )


def _slot_tool(x: float, y: float, z0: float, length: float, diameter: float, height: float):
    radius = diameter / 2.0
    straight = max(0.0, length - diameter)
    tool = Box(
        straight,
        diameter,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0)))
    for dx in (-straight / 2.0, straight / 2.0):
        tool = tool.fuse(
            Cylinder(
                radius,
                height,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x + dx, y, z0)))
        )
    return tool


def make_fixed_chassis(
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
    role_index: int | None = None,
):
    role_index = spec.selected_role if role_index is None else role_index
    cx = 119.45
    base = Box(
        spec.coupon_size[0],
        spec.coupon_size[1],
        2.5,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((cx, 0.0, -27.0)))
    base = base.cut(
        Cylinder(6.0, 2.9, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((spec.output_axis_radius, 0.0, -27.2))
        )
    )

    lower_plate = Box(
        12.5,
        24.0,
        5.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((122.75, 0.0, -22.0)))
    lower_plate = lower_plate.cut(
        Cylinder(
            spec.bearing_pocket_diameter / 2.0,
            4.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.output_axis_radius, 0.0, -21.1)))
    )
    lower_plate = lower_plate.cut(
        Cylinder(
            spec.bearing_lip_opening / 2.0,
            5.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.output_axis_radius, 0.0, -22.2)))
    )

    upper_plate = Box(
        12.5,
        24.0,
        4.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((122.75, 0.0, -3.0)))
    upper_plate = upper_plate.cut(
        Cylinder(
            spec.bearing_pocket_diameter / 2.0,
            4.40,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.output_axis_radius, 0.0, -3.05)))
    )

    # Real M2 attachment posts for both removable bearing retainers.  Their
    # 1.60 mm bores are tap pilots; the retainer ears carry 2.20 mm clearance.
    bearing_posts = []
    for z0, z1 in ((-17.10, -15.60), (0.10, 1.70)):
        for y in spec.bearing_retainer_fastener_y:
            post = Cylinder(
                spec.bearing_retainer_post_diameter / 2.0,
                z1 - z0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((spec.output_axis_radius, y, z0)))
            pilot = Cylinder(
                spec.m2_tap_pilot_diameter / 2.0,
                z1 - z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((spec.output_axis_radius, y, z0 - 0.2)))
            bearing_posts.append(post.cut(pilot))
    upper_plate = upper_plate.cut(
        Cylinder(
            spec.bearing_lip_opening / 2.0,
            4.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.output_axis_radius, 0.0, -3.2)))
    )

    rails = []
    for y in (-10.5, 10.5):
        rails.append(
            Box(
                10.0,
                3.0,
                25.5,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((124.0, y, -24.5)))
        )
    chassis = base.fuse(lower_plate).fuse(upper_plate)
    for rail in rails:
        chassis = chassis.fuse(rail)
    for post in bearing_posts:
        chassis = chassis.fuse(post)
    for y in spec.bearing_retainer_fastener_y:
        for z0, height in ((-17.30, 2.40), (0.00, 2.60)):
            chassis = chassis.cut(
                Cylinder(
                    spec.m2_tap_pilot_diameter / 2.0,
                    height,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                ).moved(Location((spec.output_axis_radius, y, z0)))
            )
    # Narrow service slots let the retainer necks rise from the outer-race
    # capture ring without sharing volume with the stationary pocket walls.
    for sign in (-1.0, 1.0):
        for z0, height in ((-18.0, 3.4), (-0.1, 2.8)):
            chassis = chassis.cut(
                Box(
                    4.4,
                    1.0,
                    height,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                ).moved(Location((spec.output_axis_radius, sign * 4.0, z0)))
            )
    # Fixed M3 points under the saddle's radial-adjustment slots.
    for x in (80.0, 103.0):
        for y in (-spec.saddle_clamp_y, spec.saddle_clamp_y):
            chassis = chassis.cut(
                Cylinder(1.6, 2.9, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
                    Location((x, y, -27.2))
                )
            )
    # Service access from +Y reaches the vertical miter and lower collar M2
    # grub screws without removing the bearing lips.
    for z in (
        spec.miter_vertical_hub_top_z - spec.miter_vertical_hub_height / 2.0,
        spec.lower_collar_screw_z,
    ):
        chassis = chassis.cut(
            _one_sided_radial_passage(
                spec.output_axis_radius,
                z,
                spec.output_shaft_diameter / 2.0,
                14.0,
                diameter=spec.m2_service_clearance_diameter,
            )
        )

    # The selected ring-arc guide is a fixed chassis feature, not a floating
    # print.  Two broad pylons carry it to the base outside the moving tongue.
    slider_lower, _ = make_arc_slider_rails(role_index, spec)
    lower_z = slider_lower.bounding_box().min.Z
    for y in spec.slider_retainer_fastener_y:
        pylon = Box(
            5.2,
            6.0,
            lower_z - (-24.60) + 0.10,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((142.40, y, -24.60)))
        chassis = chassis.fuse(pylon)
    chassis = chassis.fuse(slider_lower)
    chassis.label = "p3_v3_r1_open_two_MR84ZZ_bearing_chassis"
    chassis.color = srgb("#889197")
    return chassis


def make_bearing_retainer(
    which: str,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    if which not in ("lower", "upper"):
        raise ValueError("bearing retainer must be lower or upper")
    # Capture only the MR84 outer-race band.  The 3.10 mm opening leaves
    # 1.10 mm radial clearance around the 4 mm rotating D-shaft and therefore
    # cannot rub either the shaft or its clamped vertical miter hub.
    z0 = -17.90 if which == "lower" else 0.10
    ring = _annulus(
        spec.bearing_outer_race_inner_radius,
        spec.bearing_od / 2.0,
        spec.bearing_retainer_ring_height,
        z0,
    ).moved(Location((spec.output_axis_radius, 0.0, 0.0)))
    ear_z0 = -15.60 if which == "lower" else 1.70
    retainer = ring
    for y in spec.bearing_retainer_fastener_y:
        sign = -1.0 if y < 0 else 1.0
        neck = Box(
            2.0 * spec.bearing_retainer_ear_half_width_x,
            0.8,
            ear_z0 + spec.bearing_retainer_ear_thickness - z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.output_axis_radius, sign * 4.0, z0)))
        ear = Box(
            2.0 * spec.bearing_retainer_ear_half_width_x,
            4.8,
            spec.bearing_retainer_ear_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.output_axis_radius, sign * 6.6, ear_z0)))
        retainer = retainer.fuse(neck).fuse(ear)
        retainer = retainer.cut(
            Cylinder(
                spec.bearing_retainer_clearance_hole / 2.0,
                spec.bearing_retainer_ear_thickness + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((spec.output_axis_radius, y, ear_z0 - 0.2)))
        )
    retainer.label = f"p3_v3_r1_{which}_bearing_service_retainer"
    retainer.color = srgb("#AEB5B9")
    return retainer


def make_bearing_retainer_screw_references(
    which: str,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    """Two purchased M2 screws fixing each outer-race retainer to chassis."""

    z0 = -17.90 if which == "lower" else 0.10
    ear_top = (-15.60 if which == "lower" else 1.70) + spec.bearing_retainer_ear_thickness
    screws = []
    for index, y in enumerate(spec.bearing_retainer_fastener_y):
        core = Cylinder(
            spec.m2_tap_pilot_diameter / 2.0,
            2.30,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((spec.output_axis_radius, y, ear_top)))
        head = Cylinder(
            1.9,
            1.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.output_axis_radius, y, ear_top)))
        screw = core.fuse(head)
        screw.label = f"p3_v3_r1_purchased_M2_{which}_bearing_retainer_screw_{index+1}_REFERENCE"
        screw.color = srgb("#6B7074")
        screws.append(screw)
    return tuple(screws)


def make_motor_saddle(spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1):
    base = Box(45.0, 34.0, 2.35, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((91.6, 0.0, -24.5))
    )
    # The motor reference body ends at the face datum.  The saddle flange is
    # entirely on the gear side of that datum, so it cannot occupy the motor.
    face = Box(2.5, 24.0, 26.0, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
        Location((spec.motor_face_radius, 0.0, -24.5))
    )
    saddle = base.fuse(face)
    # The mounting flange clears the complete bevel back-face envelope, not
    # merely the 4 mm shaft.  Its four M2 holes remain outside this 18.8 mm
    # central opening on the 15.4 mm square pitch.
    shaft_hole = Cylinder(9.4, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).rotate(
        Axis.Y, 90.0
    ).moved(Location((spec.motor_face_radius + 1.25, 0.0, spec.miter_axis_intersection_z)))
    saddle = saddle.cut(shaft_hole)
    for y in (-spec.motor_mount_pitch / 2.0, spec.motor_mount_pitch / 2.0):
        for z in (
            spec.miter_axis_intersection_z - spec.motor_mount_pitch / 2.0,
            spec.miter_axis_intersection_z + spec.motor_mount_pitch / 2.0,
        ):
            hole = Cylinder(
                1.1,
                3.0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).rotate(Axis.Y, 90.0).moved(Location((spec.motor_face_radius - 2.7, y, z)))
            saddle = saddle.cut(hole)
    slot_length = 3.4 + 2.0 * spec.motor_adjustment
    for x in (80.0, 103.0):
        for y in (-spec.saddle_clamp_y, spec.saddle_clamp_y):
            saddle = saddle.cut(_slot_tool(x, y, -24.7, slot_length, 3.4, 2.9))
    saddle.label = "p3_v3_r1_NEMA8_saddle_plus_minus_0p5_radial_adjustment"
    saddle.color = srgb("#69737A")
    return saddle


def make_motor_saddle_clamp_hardware(
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    """Four tightened M3 bolt/two-washer/nut stacks for the saddle slots."""

    hardware = []
    for index, (x, y) in enumerate(
        (
            x_y
            for x_y in (
                (80.0, -spec.saddle_clamp_y),
                (80.0, spec.saddle_clamp_y),
                (103.0, -spec.saddle_clamp_y),
                (103.0, spec.saddle_clamp_y),
            )
        )
    ):
        core = Cylinder(
            spec.saddle_clamp_bolt_diameter / 2.0,
            spec.saddle_clamp_shank_z[1] - spec.saddle_clamp_shank_z[0],
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, spec.saddle_clamp_shank_z[0])))
        head = Cylinder(
            2.80,
            2.05,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, -29.50)))
        bolt = core.fuse(head)
        bolt.label = f"p3_v3_r1_purchased_M3_saddle_clamp_bolt_{index+1}_REFERENCE"
        bolt.color = srgb("#6B7074")

        lower_washer = _annulus(
            spec.saddle_clamp_clearance_diameter / 2.0,
            spec.saddle_clamp_washer_od / 2.0,
            spec.saddle_clamp_lower_washer_z[1] - spec.saddle_clamp_lower_washer_z[0],
            spec.saddle_clamp_lower_washer_z[0],
        ).moved(Location((x, y, 0.0)))
        lower_washer.label = f"p3_v3_r1_purchased_M3_saddle_lower_washer_{index+1}_REFERENCE"
        lower_washer.color = srgb("#9CA4A9")

        upper_washer = _annulus(
            spec.saddle_clamp_clearance_diameter / 2.0,
            spec.saddle_clamp_washer_od / 2.0,
            spec.saddle_clamp_upper_washer_z[1] - spec.saddle_clamp_upper_washer_z[0],
            spec.saddle_clamp_upper_washer_z[0],
        ).moved(Location((x, y, 0.0)))
        upper_washer.label = f"p3_v3_r1_purchased_M3_saddle_upper_washer_{index+1}_REFERENCE"
        upper_washer.color = srgb("#9CA4A9")

        # A cylindrical clearance envelope is used for the purchased external
        # nut; the BOM fixes M3 / 5.5 mm AF hardware independently of preview.
        nut = _annulus(
            spec.saddle_clamp_thread_minor_diameter / 2.0,
            spec.saddle_clamp_nut_af / 2.0,
            spec.saddle_clamp_nut_z[1] - spec.saddle_clamp_nut_z[0],
            spec.saddle_clamp_nut_z[0],
        ).moved(Location((x, y, 0.0)))
        nut.label = f"p3_v3_r1_purchased_M3_external_nut_5p5AF_{index+1}_REFERENCE"
        nut.color = srgb("#777F84")
        hardware.extend((bolt, lower_washer, upper_washer, nut))
    return tuple(hardware)


def make_assembled(
    role_index: int | None = None,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    role_index = spec.selected_role if role_index is None else role_index
    horizontal, vertical = make_miter_pair(spec)
    _, slider_upper = make_arc_slider_rails(role_index, spec)
    children = [
        make_fixed_chassis(spec, role_index),
        make_motor_saddle(spec),
        make_motor_body(spec),
        make_motor_shaft(spec),
        horizontal,
        vertical,
        make_output_shaft(spec),
        make_bearing("lower", spec),
        make_bearing("upper", spec),
        make_bearing_retainer("lower", spec),
        make_bearing_retainer("upper", spec),
        make_lower_clamp_collar(spec),
        make_lower_miter_shim(spec),
        make_role_spacer(role_index, spec),
        make_output_pinion(role_index, spec),
        make_ring_arc_carriage(role_index, 0.0, spec),
        slider_upper,
        *make_set_screw_references(role_index, spec),
        *make_arc_retainer_screw_references(role_index, spec),
        *make_bearing_retainer_screw_references("lower", spec),
        *make_bearing_retainer_screw_references("upper", spec),
        *make_motor_saddle_clamp_hardware(spec),
    ]
    return Compound(
        children=children,
        label=f"p3_v3_transmission_r1_{spec.roles[role_index]}_station_assembled",
    )


def make_exploded(
    role_index: int | None = None,
    spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1,
):
    role_index = spec.selected_role if role_index is None else role_index
    horizontal, vertical = make_miter_pair(spec)
    _, slider_upper = make_arc_slider_rails(role_index, spec)
    pieces = [
        make_fixed_chassis(spec, role_index),
        make_motor_saddle(spec).moved(Location((18.0, 0.0, 0.0))),
        make_motor_body(spec).moved(Location((34.0, 0.0, 0.0))),
        make_motor_shaft(spec).moved(Location((24.0, 0.0, 0.0))),
        horizontal.moved(Location((12.0, 0.0, 0.0))),
        vertical.moved(Location((0.0, 0.0, 5.0))),
        make_output_shaft(spec).moved(Location((0.0, 0.0, 18.0))),
        make_bearing("lower", spec).moved(Location((0.0, -18.0, 0.0))),
        make_bearing("upper", spec).moved(Location((0.0, 18.0, 0.0))),
        make_bearing_retainer("lower", spec).moved(Location((0.0, -24.0, 0.0))),
        make_bearing_retainer("upper", spec).moved(Location((0.0, 24.0, 0.0))),
        make_lower_clamp_collar(spec).moved(Location((0.0, -12.0, -4.0))),
        make_lower_miter_shim(spec).moved(Location((0.0, 12.0, 0.0))),
        make_role_spacer(role_index, spec).moved(Location((0.0, 22.0, 12.0))),
        make_output_pinion(role_index, spec).moved(Location((0.0, 0.0, 28.0))),
        make_ring_arc_carriage(role_index, 0.0, spec).moved(Location((0.0, 0.0, 38.0))),
        slider_upper.moved(Location((0.0, -18.0, 50.0))),
    ]
    for index, screw in enumerate(make_set_screw_references(role_index, spec)):
        pieces.append(screw.moved(Location((8.0 * index, -32.0, 18.0))))
    service_hardware = (
        *make_arc_retainer_screw_references(role_index, spec),
        *make_bearing_retainer_screw_references("lower", spec),
        *make_bearing_retainer_screw_references("upper", spec),
        *make_motor_saddle_clamp_hardware(spec),
    )
    for index, item in enumerate(service_hardware):
        pieces.append(item.moved(Location((4.0 * (index % 6), -42.0, 8.0 * (index // 6)))))
    return Compound(children=pieces, label="p3_v3_transmission_r1_service_exploded")


def make_print_components(spec: P3V3TransmissionR1Spec = P3_V3_TRANSMISSION_R1):
    horizontal, vertical = make_miter_pair(spec)
    role = spec.selected_role
    _, slider_upper = make_arc_slider_rails(role, spec)
    components = [
        make_fixed_chassis(spec, role),
        make_motor_saddle(spec),
        horizontal,
        vertical,
        make_role_spacer(role, spec),
        make_output_pinion(role, spec),
        make_ring_arc_carriage(role, 0.0, spec),
        slider_upper,
        make_bearing_retainer("lower", spec),
        make_bearing_retainer("upper", spec),
        make_lower_clamp_collar(spec),
        make_lower_miter_shim(spec),
    ]
    return Compound(
        children=components,
        label="p3_v3_transmission_r1_functional_position_catalog_NOT_A_PRINT_PLATE",
    )


INDIVIDUAL_PRINT_FACTORIES = (
    ("fixed_chassis_with_fused_minute_guide", lambda: make_fixed_chassis(role_index=1)),
    ("motor_saddle", make_motor_saddle),
    ("horizontal_miter", lambda: make_miter_pair()[0]),
    ("vertical_miter", lambda: make_miter_pair()[1]),
    ("lower_bearing_retainer", lambda: make_bearing_retainer("lower")),
    ("upper_bearing_retainer", lambda: make_bearing_retainer("upper")),
    ("lower_clamp_collar", make_lower_clamp_collar),
    ("lower_miter_shim", make_lower_miter_shim),
    ("minute_role_spacer", lambda: make_role_spacer(1)),
    ("minute_output_pinion", lambda: make_output_pinion(1)),
    ("minute_arc_carriage", lambda: make_ring_arc_carriage(1)),
    ("minute_upper_slider_retainer", lambda: make_arc_slider_rails(1)[1]),
)


PRIMARY_FACTORIES = (
    ("assembled", make_assembled),
    ("service_exploded", make_exploded),
    ("print_components", make_print_components),
)


positive_intersection_volume = _positive_intersection_volume
