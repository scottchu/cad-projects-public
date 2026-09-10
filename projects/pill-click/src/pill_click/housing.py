"""Fixed 40 mm housing, independent stops, gate, and captured rear cover."""

from build123d import Align, Axis, Box, Cylinder, Location, Part, chamfer, fillet

from .geometry import rounded_box
from .parameters import DEFAULTS, PillClickParameters


def _box(
    size_x: float,
    size_y: float,
    size_z: float,
    center: tuple[float, float, float],
) -> Part:
    return Box(
        size_x,
        size_y,
        size_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location(center))


def make_housing(params: PillClickParameters = DEFAULTS) -> Part:
    """Return the rear-open housing with guide, stops, ports, and gate blade."""

    p = params
    outer = Box(
        p.housing_size,
        p.housing_depth,
        p.housing_size,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    # Y-parallel edges round the XZ keyboard silhouette without shrinking Y.
    outer = fillet(outer.edges().filter_by(Axis.Y), p.corner_radius)

    rear_min_y = -p.housing_depth / 2 - 0.6
    rear_channel = _box(
        p.rear_tab_channel,
        p.shoulder_y - rear_min_y,
        p.front_guide_size,
        (0.0, 0.5 * (rear_min_y + p.shoulder_y), 0.0),
    )
    guide = _box(
        p.front_guide_size,
        p.inward_stop_plane_y - p.shoulder_y,
        p.front_guide_size,
        (0.0, 0.5 * (p.shoulder_y + p.inward_stop_plane_y), 0.0),
    )
    key_pocket_size = p.key_face_size + 2 * p.sliding_clearance
    key_pocket = _box(
        key_pocket_size,
        p.housing_depth / 2 + 0.6 - p.inward_stop_plane_y,
        key_pocket_size,
        (0.0, 0.5 * (p.inward_stop_plane_y + p.housing_depth / 2 + 0.6), 0.0),
    )
    housing = outer - rear_channel - guide - key_pocket

    top_port = _box(
        p.loading_port_width,
        p.loading_port_depth,
        p.wall + 2.0,
        (0.0, p.loading_port_center_y, p.housing_size / 2),
    )
    outlet_center_y = p.latched_shuttle_center_y + p.outlet_local_y
    bottom_outlet = _box(
        p.outlet_width,
        p.outlet_depth,
        p.wall + 2.0,
        (0.0, outlet_center_y, -p.housing_size / 2),
    )
    housing = housing - top_port - bottom_outlet

    # The fixed blade rides in the shuttle floor slot.  Its top overlaps the
    # moving dam by 0.9 mm; X-edge chamfers reduce pill shearing at the gate.
    floor_z = -p.front_guide_size / 2
    gate = _box(
        p.gate_blade_width,
        p.gate_blade_depth,
        p.gate_blade_height,
        (
            0.0,
            p.latched_shuttle_center_y,
            floor_z + p.gate_blade_height / 2,
        ),
    )
    gate = chamfer(gate.edges().filter_by(Axis.X), p.gate_chamfer)
    housing = housing + gate
    housing.label = "housing_with_fixed_gate"
    return housing


def _rear_loaded_pocket(
    params: PillClickParameters,
    x: float,
    z: float,
) -> Part:
    overshoot = 0.2
    tool_depth = params.magnet_pocket_depth + overshoot
    rear_face = -params.back_cover_thickness / 2
    center_y = rear_face + (params.magnet_pocket_depth - overshoot) / 2
    return (
        Cylinder(
            params.magnet_pocket_diameter / 2,
            tool_depth,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        .rotate(Axis.X, 90)
        .moved(Location((x, center_y, z)))
    )


def make_back_cover(params: PillClickParameters = DEFAULTS) -> Part:
    """Return the rear cover with exactly two blind fridge-magnet pockets."""

    p = params
    cover_size = p.housing_size - 2 * p.wall
    cover = rounded_box(
        cover_size,
        p.back_cover_thickness,
        cover_size,
        1.8,
    )
    for x in (-p.fridge_magnet_offset_x, p.fridge_magnet_offset_x):
        cover = cover - _rear_loaded_pocket(p, x, 0.0)
    cover.label = "rear_cover:two_fridge_magnets"
    return cover


def make_back_trap_plate(params: PillClickParameters = DEFAULTS) -> Part:
    """Return the solid outer plate that mechanically traps both magnets."""

    p = params
    plate = rounded_box(
        p.housing_size - 2 * p.wall,
        p.trap_plate_thickness,
        p.housing_size - 2 * p.wall,
        1.8,
    )
    plate.label = "rear_magnet_trap_plate"
    return plate


__all__ = ["make_back_cover", "make_back_trap_plate", "make_housing"]
