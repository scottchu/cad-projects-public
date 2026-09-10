"""Four printable P2 parts built independently from the accepted P1 source."""

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Rectangle, loft

from pill_click.p0_mechanical_fit_v23_keyboard_durable_latch.geometry import (
    make_keyboard_button as make_v23_keyboard_button,
    make_planar_latch_rear_cover as make_v23_rear_cover,
    make_rear_rail_stop_bosses,
)
from pill_click.p1_hollow_magnetic_dispenser.geometry import (
    _cylinder_y,
    make_hopper_void,
    make_outer_port_tool,
    make_ported_outer_housing as make_p1_ported_outer_housing,
)
from .spec import P2_BAYONET_REFILL_8MM_REBOUND


def _two_cylinders(diameter, y_bounds, centres_x, z=0.0):
    result = None
    for x in centres_x:
        tool = _cylinder_y(diameter, y_bounds, x, z)
        result = tool if result is None else result + tool
    return result.clean()


def _pick_tools(centres_x, y_bounds, p, label):
    tools = _two_cylinders(p.magnet_pick_bore_diameter, y_bounds, centres_x, p.return_magnet_center_z)
    tools.label = label
    return tools


def make_refill_bore_tool(p=P2_BAYONET_REFILL_8MM_REBOUND):
    tool = _cylinder_y(p.refill_clear_bore_diameter, p.refill_bore_y, 0, 0)
    tool.label = "p2_d16_refill_bore_connected_to_upper_chamber"
    return tool


def make_refill_neck(p=P2_BAYONET_REFILL_8MM_REBOUND):
    outer = _cylinder_y(p.refill_neck_outer_diameter, (p.refill_neck_base_y, p.refill_neck_front_y), 0, 0)
    neck = (outer - make_refill_bore_tool(p)).clean()
    neck.label = "p2_d20_refill_neck"
    return neck


def make_refill_neck_lugs(p=P2_BAYONET_REFILL_8MM_REBOUND):
    """Two true 30-degree annular-sector lugs integral to the refill neck."""
    outer_radius = p.neck_lug_outer_radius
    inner_radius = p.refill_neck_outer_diameter / 2 - p.refill_neck_lug_body_overlap
    axial = p.refill_neck_lug_axial_thickness_y
    result = None
    # Cylinder arc_size starts at +X.  A centered 30-degree sector therefore
    # uses -15 degrees; the opposed sector is offset by 180 degrees.
    for angle in (-p.refill_neck_lug_arc_degrees / 2, 180 - p.refill_neck_lug_arc_degrees / 2):
        outer = Cylinder(
            outer_radius,
            axial,
            arc_size=p.refill_neck_lug_arc_degrees,
            rotation=(0, 0, angle),
            align=(Align.MIN, Align.MIN, Align.MIN),
        )
        inner = Cylinder(
            inner_radius,
            axial + 0.2,
            arc_size=p.refill_neck_lug_arc_degrees,
            rotation=(0, 0, angle),
            align=(Align.MIN, Align.MIN, Align.MIN),
        )
        lug = (outer - inner).rotate(Axis.X, -90).moved(Location((0, p.refill_lug_y[0], 0)))
        result = lug if result is None else result + lug
    result = result.clean()
    result.label = "p2_two_opposed_30deg_neck_lugs"
    return result


def make_inner_magnet_pocket_tools(p=P2_BAYONET_REFILL_8MM_REBOUND):
    bounds = (p.inner_magnet_pocket_y[0] - p.magnet_boolean_overshoot_y, p.inner_magnet_pocket_y[1])
    tools = _two_cylinders(p.inner_magnet_pocket_diameter, bounds, p.return_magnet_centres_x)
    tools.label = "p2_two_d8p1_inner_rebound_seats"
    return tools


def make_inner_magnet_protection_bosses(p=P2_BAYONET_REFILL_8MM_REBOUND):
    """Explicit protected solids surrounding both inner rebound seats."""
    bounds = (p.inner_magnet_pocket_y[0], p.inner_magnet_pocket_y[1] + p.inner_pick_medicine_barrier_y)
    bosses = _two_cylinders(p.inner_magnet_protection_diameter, bounds, p.return_magnet_centres_x)
    bosses.label = "p2_two_d11_inner_magnet_protection_solids"
    return bosses


def make_inner_magnet_pick_bore_tools(p=P2_BAYONET_REFILL_8MM_REBOUND):
    bounds = (p.inner_magnet_pick_bore_y[0] - p.magnet_boolean_overshoot_y, p.inner_magnet_pick_bore_y[1])
    return _pick_tools(p.inner_pick_bore_centres_x, bounds, p, "p2_two_inner_pick_access_bores")


def make_hollow_keyboard_container(p=P2_BAYONET_REFILL_8MM_REBOUND):
    body = make_v23_keyboard_button(p)
    body = body + make_refill_neck(p) + make_refill_neck_lugs(p) + make_inner_magnet_protection_bosses(p)
    body = body - make_hopper_void(p) - make_refill_bore_tool(p)
    body = body - make_inner_magnet_pocket_tools(p) - make_inner_magnet_pick_bore_tools(p)
    body = body.clean()
    body.label = "p2_hollow_keyboard_container_d8_rebound_with_bayonet_neck"
    return body


def make_ported_outer_housing(p=P2_BAYONET_REFILL_8MM_REBOUND):
    housing = make_p1_ported_outer_housing(p)
    housing.label = "p2_p1_preserved_fail_closed_outer_housing"
    return housing


def make_cover_magnet_bosses(p=P2_BAYONET_REFILL_8MM_REBOUND):
    bosses = _two_cylinders(p.cover_magnet_boss_diameter, p.cover_magnet_boss_y, p.return_magnet_centres_x)
    bosses.label = "p2_two_d11_rebound_bosses"
    return bosses


def make_cover_m1_bore_tools(p=P2_BAYONET_REFILL_8MM_REBOUND):
    tools = _two_cylinders(p.fridge_magnet_pocket_diameter, p.cover_m1_seat_y, p.return_magnet_centres_x)
    tools.label = "p2_two_d6p1_fridge_seats"
    return tools


def make_cover_m2_bore_tools(p=P2_BAYONET_REFILL_8MM_REBOUND):
    tools = _two_cylinders(p.rebound_magnet_pocket_diameter, p.cover_m2_seat_y, p.return_magnet_centres_x)
    tools.label = "p2_two_d8p1_rebound_seats"
    return tools


def make_cover_m1_pick_bore_tools(p=P2_BAYONET_REFILL_8MM_REBOUND):
    return _pick_tools(p.fridge_pick_bore_centres_x, p.cover_m1_pick_bore_y, p, "p2_two_m1_pick_access_bores")


def make_cover_m2_pick_bore_tools(p=P2_BAYONET_REFILL_8MM_REBOUND):
    return _pick_tools(p.rebound_pick_bore_centres_x, p.cover_m2_pick_bore_y, p, "p2_two_m2_pick_access_bores")


def make_magnetic_rear_cover(p=P2_BAYONET_REFILL_8MM_REBOUND):
    cover = make_v23_rear_cover(p) - make_rear_rail_stop_bosses(p)
    cover = cover + make_cover_magnet_bosses(p)
    cover = cover - make_cover_m1_bore_tools(p) - make_cover_m2_bore_tools(p)
    cover = cover - make_cover_m1_pick_bore_tools(p) - make_cover_m2_pick_bore_tools(p)
    cover = cover.clean()
    cover.label = "p2_rear_cover_d6_fridge_d8_rebound_no_hard_stops"
    return cover


def _cap_entry_slot(start_angle, p):
    """Straight, open-ended leg of one L-slot."""
    radial_start = p.refill_neck_outer_diameter / 2 - p.refill_neck_lug_body_overlap - p.cap_radial_clearance_per_side
    radial_depth = p.cap_outer_diameter / 2 - radial_start + 0.2
    tangential = p.neck_lug_arc_length + 2 * p.cap_radial_clearance_per_side
    slot = Box(radial_depth, p.cap_internal_depth_y - p.cap_rotation_stop_thickness, tangential,
               align=(Align.MIN, Align.MIN, Align.CENTER))
    slot = slot.moved(Location((radial_start, 0, 0)))
    return slot.rotate(Axis.Y, start_angle)


def _cap_entry_lead_in(start_angle, p):
    """Lofted 0.60 mm lead-in at each open slot mouth."""
    radial_start = p.refill_neck_outer_diameter / 2 - p.refill_neck_lug_body_overlap - p.cap_radial_clearance_per_side
    radial_depth = p.cap_outer_diameter / 2 - radial_start + 0.2
    tangential = p.neck_lug_arc_length + 2 * p.cap_radial_clearance_per_side
    flare = 2 * p.cap_lead_in_chamfer
    mouth = Rectangle(radial_depth + p.cap_lead_in_chamfer, tangential + flare).moved(
        Location((radial_start + (radial_depth + p.cap_lead_in_chamfer) / 2, 0, 0), (90, 0, 0))
    )
    throat = Rectangle(radial_depth, tangential).moved(
        Location((radial_start + radial_depth / 2, p.cap_lead_in_chamfer, 0), (90, 0, 0))
    )
    return loft([mouth, throat], ruled=True).rotate(Axis.Y, start_angle)


def _cap_lock_path(start_angle, p):
    """Sampled 90 degree circumferential leg; the unswept end is the stop."""
    radial_start = p.refill_neck_outer_diameter / 2 - p.refill_neck_lug_body_overlap - p.cap_radial_clearance_per_side
    radial_depth = p.cap_outer_diameter / 2 - radial_start + 0.2
    # A full lug-width cutter is required at every sampled angle; using half
    # the arc width created two real locked-state interferences.
    tangential = p.neck_lug_arc_length + 2 * p.cap_radial_clearance_per_side
    result = None
    steps = int(p.cap_rotation_degrees / p.cap_slot_sampling_degrees)
    for index in range(steps + 1):
        angle = start_angle + index * p.cap_slot_sampling_degrees
        # Keep the whole lug envelope open throughout the quarter turn.  The
        # slot floor rises by the specified 1.2 mm, but its enlarged axial
        # height preserves clearance instead of cutting into the lug.
        rise = p.cap_ramp_rise_y * index / steps
        cutter_height = p.cap_slot_axial_height_y + p.cap_ramp_rise_y + 0.20
        cutter = Box(radial_depth, cutter_height, tangential,
                     align=(Align.MIN, Align.MIN, Align.CENTER))
        cutter = cutter.moved(Location((radial_start,
                                       p.refill_neck_projection_y - cutter_height + rise, 0)))
        cutter = cutter.rotate(Axis.Y, angle)
        result = cutter if result is None else result + cutter
    return result.clean()


def make_bayonet_cap(p=P2_BAYONET_REFILL_8MM_REBOUND):
    """Separate cup cap with two open-ended, 90-degree L slots."""
    outer = _cylinder_y(p.cap_outer_diameter, (0, p.cap_total_depth_y), 0, 0)
    inner = _cylinder_y(p.cap_internal_running_diameter, (-0.05, p.cap_internal_depth_y), 0, 0)
    cap = outer - inner
    for start_angle in (0.0, 180.0):
        cap = cap - _cap_entry_slot(start_angle, p) - _cap_entry_lead_in(start_angle, p) - _cap_lock_path(start_angle, p)
    cap = cap.clean()
    cap.label = "p2_quarter_turn_bayonet_refill_cap"
    return cap


__all__ = [name for name in globals() if name.startswith("make_")]
