"""Three-part P1 geometry with an integrated magnet-bearing inner body."""

from build123d import Align, Axis, BuildSketch, Cylinder, Location, Plane, RectangleRounded, extrude, loft

from pill_click.p0_mechanical_fit_v2_keyboard_inverted_rails.geometry import _rounded_prism_xz
from pill_click.p0_mechanical_fit_v23_keyboard_durable_latch.geometry import (
    make_keyboard_button as make_v23_keyboard_button,
    make_outer_housing as make_v23_outer_housing,
    make_planar_latch_rear_cover as make_v23_rear_cover,
    make_rear_rail_stop_bosses,
)
from .spec import P1_HOLLOW_MAGNETIC_DISPENSER


def _rounded_section_xz(width, height, radius, y, center_z):
    return RectangleRounded(width, height, radius).moved(Location((0, y, center_z), (90, 0, 0)))


def _rounded_prism_xy(width, length, height, radius, center):
    with BuildSketch(Plane.XY) as sketch:
        RectangleRounded(width, length, radius)
    return extrude(sketch.sketch, height).moved(Location((center[0], center[1], center[2] - height / 2)))


def _cylinder_y(diameter, y_bounds, x, z):
    part = Cylinder(diameter / 2, y_bounds[1] - y_bounds[0], align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(Axis.X, -90)
    return part.moved(Location((x, y_bounds[0], z)))


def make_upper_medicine_chamber(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    floor = p.chamber_boolean_floor_z
    sections = [
        _rounded_section_xz(p.cavity_rear_width_x, p.cavity_rear_roof_z - floor, p.cavity_rear_radius_xz, p.cavity_rear_y, (p.cavity_rear_roof_z + floor) / 2),
        _rounded_section_xz(p.cavity_seam_width_x, p.cavity_seam_roof_z - floor, p.cavity_seam_radius_xz, p.cavity_seam_y, (p.cavity_seam_roof_z + floor) / 2),
        _rounded_section_xz(p.cavity_front_width_x, p.cavity_front_roof_z - floor, p.cavity_front_radius_xz, p.cavity_front_y, (p.cavity_front_roof_z + floor) / 2),
    ]
    chamber = loft(sections, ruled=True).clean()
    chamber.label = "p1_upper_medicine_chamber"
    return chamber


def _hopper_end(width, y, p):
    h = p.hopper_degenerate_section_height_z
    return _rounded_section_xz(width, h, h / 2 - 0.01, y, p.hopper_start_z)


def _hopper_throat(y, p):
    h = p.hopper_boolean_top_z - p.hopper_boolean_floor_z
    return _rounded_section_xz(p.pill_port_width_x, h, p.hopper_blend_radius_xz, y, (p.hopper_boolean_top_z + p.hopper_boolean_floor_z) / 2)


def make_hopper_void(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    rear = loft([_hopper_end(p.cavity_rear_width_x, p.cavity_rear_y, p), _hopper_throat(p.hopper_rear_throat_y, p)], ruled=True)
    throat = loft([_hopper_throat(p.hopper_rear_throat_y, p), _hopper_throat(p.hopper_front_throat_y, p)], ruled=True)
    front = loft([_hopper_throat(p.hopper_front_throat_y, p), _hopper_end(p.cavity_front_width_x, p.cavity_front_y, p)], ruled=True)
    port = _rounded_prism_xy(p.pill_port_width_x, p.pill_port_length_y, p.inner_port_z[1] - p.inner_port_z[0], p.pill_port_corner_radius_xy, (0, sum(p.inner_port_local_y) / 2, sum(p.inner_port_z) / 2))
    result = (make_upper_medicine_chamber(p) + rear + throat + front + port).clean()
    result.label = "p1_connected_hopper_void"
    return result


def make_inner_port_tool(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    """The full moving aperture, kept separate from the fail-closed housing slot."""
    tool = _rounded_prism_xy(
        p.pill_port_width_x,
        p.pill_port_length_y,
        p.inner_port_z[1] - p.inner_port_z[0],
        p.pill_port_corner_radius_xy,
        (0, sum(p.inner_port_local_y) / 2, sum(p.inner_port_z) / 2),
    )
    tool.label = f"p1_inner_{p.pill_port_width_x:g}x{p.pill_port_length_y:g}_port_tool"
    return tool


def make_inner_magnet_pocket_tools(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    tools = None
    bounds = (p.inner_magnet_pocket_y[0] - p.magnet_boolean_overshoot_y, p.inner_magnet_pocket_y[1])
    for x in p.return_magnet_centres_x:
        tool = _cylinder_y(p.magnet_pocket_diameter, bounds, x, p.return_magnet_center_z)
        tools = tool if tools is None else tools + tool
    tools = tools.clean()
    tools.label = "p1_two_inner_magnet_pockets"
    return tools


def _make_pick_bore_tools(y_bounds, label, p):
    tools = None
    for x in p.magnet_pick_bore_centres_x:
        tool = _cylinder_y(p.magnet_pick_bore_diameter, y_bounds, x, p.return_magnet_center_z)
        tools = tool if tools is None else tools + tool
    tools = tools.clean()
    tools.label = label
    return tools


def make_inner_magnet_pick_bore_tools(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    """Two rear-open extraction bores beside the inner magnet seats."""
    bounds = (p.inner_magnet_pick_bore_y[0] - p.magnet_boolean_overshoot_y, p.inner_magnet_pick_bore_y[1])
    return _make_pick_bore_tools(bounds, "p1_two_inner_magnet_pick_access_bores", p)


def make_hollow_keyboard_container(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    body = make_v23_keyboard_button(p)
    body = (body - make_hopper_void(p) - make_inner_magnet_pocket_tools(p) - make_inner_magnet_pick_bore_tools(p)).clean()
    body.label = "p1_one_piece_hollow_keyboard_container_integrated_magnet_insets_with_pick_access"
    return body


def make_outer_port_tool(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    tool = _rounded_prism_xy(p.pill_port_width_x, p.outer_port_length_y, p.outer_port_z[1] - p.outer_port_z[0], p.pill_port_corner_radius_xy, (0, p.outer_port_center_world_y, sum(p.outer_port_z) / 2))
    tool.label = f"p1_outer_{p.pill_port_width_x:g}x{p.outer_port_length_y:g}_fail_closed_port_tool"
    return tool


def make_ported_outer_housing(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    housing = (make_v23_outer_housing(p) - make_outer_port_tool(p)).clean()
    housing.label = "p1_ported_outer_housing"
    return housing


def make_cover_magnet_bosses(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    bosses = None
    for x in p.return_magnet_centres_x:
        boss = _cylinder_y(p.cover_magnet_boss_diameter, p.cover_magnet_boss_y, x, p.return_magnet_center_z)
        bosses = boss if bosses is None else bosses + boss
    bosses = bosses.clean()
    bosses.label = "p1_two_d9_return_magnet_bosses"
    return bosses


def make_cover_m1_bore_tools(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    tools = None
    for x in p.return_magnet_centres_x:
        tool = _cylinder_y(p.magnet_pocket_diameter, p.cover_m1_seat_y, x, p.return_magnet_center_z)
        tools = tool if tools is None else tools + tool
    tools = tools.clean()
    tools.label = "p1_two_rear_open_m1_fridge_seats"
    return tools


def make_cover_m2_bore_tools(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    tools = None
    for x in p.return_magnet_centres_x:
        tool = _cylinder_y(p.magnet_pocket_diameter, p.cover_m2_seat_y, x, p.return_magnet_center_z)
        tools = tool if tools is None else tools + tool
    tools = tools.clean()
    tools.label = "p1_two_front_open_m2_return_seats"
    return tools


def make_cover_m1_pick_bore_tools(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    """Two rear-open extraction bores beside the fridge-facing M1 seats."""
    return _make_pick_bore_tools(p.cover_m1_pick_bore_y, "p1_two_rear_open_m1_pick_access_bores", p)


def make_cover_m2_pick_bore_tools(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    """Two front-open extraction bores beside the rebound-facing M2 seats."""
    return _make_pick_bore_tools(p.cover_m2_pick_bore_y, "p1_two_front_open_m2_pick_access_bores", p)


def make_magnetic_rear_cover(p=P1_HOLLOW_MAGNETIC_DISPENSER):
    cover = make_v23_rear_cover(p)
    cover = cover - make_rear_rail_stop_bosses(p)
    cover = cover + make_cover_magnet_bosses(p)
    cover = cover - make_cover_m1_bore_tools(p)
    cover = cover - make_cover_m2_bore_tools(p)
    cover = cover - make_cover_m1_pick_bore_tools(p)
    cover = cover - make_cover_m2_pick_bore_tools(p)
    cover = cover.clean()
    cover.label = "p1_rear_cover_four_exact_one_magnet_seats_with_pick_access_no_hard_stops"
    return cover


__all__ = [
    "make_cover_m1_bore_tools", "make_cover_m1_pick_bore_tools", "make_cover_m2_bore_tools",
    "make_cover_m2_pick_bore_tools", "make_cover_magnet_bosses",
    "make_hollow_keyboard_container", "make_hopper_void", "make_inner_magnet_pick_bore_tools",
    "make_inner_port_tool",
    "make_inner_magnet_pocket_tools",
    "make_magnetic_rear_cover", "make_outer_port_tool",
    "make_ported_outer_housing", "make_upper_medicine_chamber",
]
