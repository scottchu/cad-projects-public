"""STEP-ready solids for the progressive P0 manual slider."""

from build123d import Align, Box, Location, Part

from .spec import P0, P0Spec


def _box(
    size_x: float,
    size_y: float,
    size_z: float,
    *,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> Part:
    shape = Box(
        size_x,
        size_y,
        size_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    if center != (0.0, 0.0, 0.0):
        shape = shape.moved(Location(center))
    return shape


def _box_between_y(
    size_x: float,
    rear_y: float,
    front_y: float,
    size_z: float,
    *,
    center_z: float = 0.0,
) -> Part:
    return _box(
        size_x,
        front_y - rear_y,
        size_z,
        center=(0.0, (rear_y + front_y) / 2, center_z),
    )


def make_housing(p: P0Spec = P0) -> Part:
    """Return the fixed 40 mm housing with four longitudinal guide ribs."""

    body = _box(p.housing_size, p.housing_size, p.housing_size)

    # Rear assembly channel, narrow front guide throat, then key-face recess.
    rear_channel = _box_between_y(
        p.rear_channel_width,
        -p.housing_size / 2 - 1.0,
        p.front_shoulder_y,
        p.interior_height,
    )
    front_guide = _box_between_y(
        p.front_guide_width,
        p.front_shoulder_y,
        p.inward_stop_plane_y,
        p.interior_height,
    )
    key_recess = _box_between_y(
        p.key_recess_size,
        p.inward_stop_plane_y,
        p.housing_size / 2 + 1.0,
        p.key_recess_size,
    )
    body = body - rear_channel - front_guide - key_recess

    # Fixed external apertures. Cutters overshoot both wall faces.
    fill_cut = _box(
        p.fill_width,
        p.fill_length,
        p.housing_top_bottom_wall + 2.0,
        center=(
            0.0,
            p.fill_fixed_center_y,
            p.housing_size / 2 - p.housing_top_bottom_wall / 2,
        ),
    )
    outlet_cut = _box(
        p.outlet_width,
        p.outlet_length,
        p.housing_top_bottom_wall + 2.0,
        center=(
            0.0,
            p.outlet_fixed_center_y,
            -p.housing_size / 2 + p.housing_top_bottom_wall / 2,
        ),
    )
    body = body - fill_cut - outlet_cut

    # Four ribs: left/right side wall, upper/lower Z locations.
    rail_length = p.rail_end_y - p.rail_start_y
    for side in (-1.0, 1.0):
        rail_center_x = side * (
            p.rail_tip_x + p.rail_radial_height / 2
        )
        for z_center in (-p.rail_z_offset, p.rail_z_offset):
            rail = _box(
                p.rail_radial_height,
                rail_length,
                p.rail_tangential_width,
                center=(
                    rail_center_x,
                    (p.rail_start_y + p.rail_end_y) / 2,
                    z_center,
                ),
            )
            body = body + rail

    body.label = "p0_fixed_housing_with_four_rails"
    return body


def make_back_insert(p: P0Spec = P0) -> Part:
    """Return the rear-assembled retainer with tool and roof-tongue access."""

    insert = _box(
        p.rear_insert_width,
        p.rear_insert_thickness,
        p.rear_insert_height,
    )
    tool_access = _box(
        p.manual_access_width,
        p.rear_insert_thickness + 2.0,
        p.manual_access_height,
    )
    tongue_slot = _box(
        p.roof_tongue_width + 0.4,
        p.rear_insert_thickness + 2.0,
        3.2,
        center=(0.0, 0.0, p.housing_inner_half_z - 1.0),
    )
    insert = insert - tool_access - tongue_slot
    insert.label = "p0_rear_insert_manual_access"
    return insert


def make_shuttle(p: P0Spec = P0) -> Part:
    """Return the hollow medicine shuttle with apertures, lands, and stops."""

    shuttle_depth = p.shuttle_front_y - p.shuttle_rear_y
    outer = _box_between_y(
        p.shuttle_width,
        p.shuttle_rear_y,
        p.shuttle_front_y,
        p.shuttle_height,
    )
    inner = _box_between_y(
        2 * p.shuttle_inner_half_x,
        p.shuttle_inner_rear_y,
        p.shuttle_inner_front_y,
        2 * p.shuttle_inner_half_z,
    )
    shuttle = outer - inner

    fill_cut = _box(
        p.fill_width,
        p.fill_length,
        p.medicine_wall + 2.0,
        center=(
            0.0,
            p.fill_moving_local_center_y,
            p.shuttle_height / 2 - p.medicine_wall / 2,
        ),
    )
    outlet_cut = _box(
        p.outlet_width,
        p.outlet_length,
        p.medicine_wall + 2.0,
        center=(
            0.0,
            p.outlet_moving_local_center_y,
            -p.shuttle_height / 2 + p.medicine_wall / 2,
        ),
    )
    shuttle = shuttle - fill_cut - outlet_cut

    # Rearward roof tongue provides the specified released-state solid skin.
    roof_tongue = _box_between_y(
        p.roof_tongue_width,
        p.roof_closure_local_start_y,
        p.shuttle_rear_y,
        p.medicine_wall,
        center_z=p.shuttle_height / 2 - p.medicine_wall / 2,
    )
    shuttle = shuttle + roof_tongue

    # Blank key face. Its rear face contacts the independent inward stop plane.
    key_face = _box_between_y(
        p.key_face_size,
        p.shuttle_front_y,
        p.shuttle_front_y + p.key_face_thickness,
        p.key_face_size,
    )
    shuttle = shuttle + key_face

    # Opposed side tabs fit through the rear channel and catch the front shoulder.
    tab_extension = (
        p.captive_tab_overall_width - p.shuttle_width
    ) / 2
    tab_center_y = (p.tab_local_rear_y + p.tab_local_front_y) / 2
    for side in (-1.0, 1.0):
        tab_center_x = side * (
            p.shuttle_width / 2 + tab_extension / 2
        )
        tab = _box(
            tab_extension,
            p.captive_tab_depth,
            p.captive_tab_height,
            center=(tab_center_x, tab_center_y, 0.0),
        )
        shuttle = shuttle + tab

    # Eight short C-section bearing lands: two Y stations on each of four rails.
    boss_radial_depth = p.bearing_boss_outer_x - p.shuttle_width / 2
    groove_cutter_radial_depth = p.groove_radial_depth + 1.0
    for side in (-1.0, 1.0):
        boss_center_x = side * (
            p.shuttle_width / 2 + boss_radial_depth / 2
        )
        groove_center_x = side * (
            p.groove_bottom_x + groove_cutter_radial_depth / 2
        )
        for z_center in (-p.rail_z_offset, p.rail_z_offset):
            for y_center in (
                p.rear_land_local_y,
                p.front_land_local_y,
            ):
                boss = _box(
                    boss_radial_depth,
                    p.land_length,
                    p.bearing_boss_tangential_width,
                    center=(boss_center_x, y_center, z_center),
                )
                shuttle = shuttle + boss
                groove = _box(
                    groove_cutter_radial_depth,
                    p.land_length + 0.4,
                    p.groove_width,
                    center=(groove_center_x, y_center, z_center),
                )
                shuttle = shuttle - groove

    shuttle.label = "p0_medicine_shuttle_eight_bearing_lands"
    return shuttle


__all__ = ["make_back_insert", "make_housing", "make_shuttle"]
