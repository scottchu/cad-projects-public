"""STEP-ready solids for P0 v2 captured shutters and blind rear cover."""

from build123d import Align, Box, Compound, Location, Part, Polygon, Shape, extrude

from .spec import P0V2, P0V2Spec


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


def _rail_with_rear_lead_in(
    side: float,
    z_center: float,
    p: P0V2Spec,
) -> Shape:
    """Return one rail whose first 0.7 mm ramps from root to full height."""

    root_x = side * p.rail_root_x
    tip_x = side * p.rail_tip_x
    if side < 0:
        points = (
            (root_x, p.rail_start_y),
            (tip_x, p.rail_start_y + p.rail_rear_lead_in),
            (tip_x, p.rail_end_y),
            (root_x, p.rail_end_y),
        )
    else:
        # Keep the face normal +Z on both sides so the subsequent placement is
        # symmetric.  A mirrored vertex order would reverse the extrusion.
        points = (
            (root_x, p.rail_start_y),
            (root_x, p.rail_end_y),
            (tip_x, p.rail_end_y),
            (tip_x, p.rail_start_y + p.rail_rear_lead_in),
        )
    profile = Polygon(*points)
    rail = extrude(profile, p.rail_tangential_width)
    rail = rail.moved(
        Location((0.0, 0.0, z_center - p.rail_tangential_width / 2))
    )
    return rail


def make_housing(p: P0V2Spec = P0V2) -> Part:
    """Return the 40 mm fixed housing, shutter tracks, rails, and hook pockets."""

    body = _box(p.housing_size, p.housing_size, p.housing_size)

    rear_channel = _box_between_y(
        p.rear_channel_width,
        -p.housing_size / 2 - 1.0,
        p.front_shoulder_y,
        p.rear_channel_height,
    )
    front_guide = _box_between_y(
        p.front_guide_width,
        p.front_shoulder_y,
        p.inward_stop_plane_y,
        p.rear_channel_height,
    )
    key_recess = _box_between_y(
        p.key_recess_size,
        p.inward_stop_plane_y,
        p.housing_size / 2 + 1.0,
        p.key_recess_size,
    )
    body = body - rear_channel - front_guide - key_recess

    # Rear-fed flange and web pockets. The web pocket leaves a 0.05 mm opaque
    # outer skin outside the fixed aperture; its exposed face is 0.10 mm low.
    track_y_rear = -p.housing_size / 2 - 0.4
    track_y_front = p.housing_size / 2 + 0.4
    track_length = track_y_front - track_y_rear
    track_center_y = (track_y_rear + track_y_front) / 2

    top_flange_track = _box(
        p.shutter_track_flange_width,
        track_length,
        p.top_track_lip_underside_z - p.top_track_floor_z,
        center=(
            0.0,
            track_center_y,
            (p.top_track_lip_underside_z + p.top_track_floor_z) / 2,
        ),
    )
    top_web_track = _box(
        p.shutter_track_web_width,
        track_length,
        p.housing_size / 2
        - p.track_skin_thickness
        - p.top_track_lip_underside_z,
        center=(
            0.0,
            track_center_y,
            (
                p.housing_size / 2
                - p.track_skin_thickness
                + p.top_track_lip_underside_z
            )
            / 2,
        ),
    )
    bottom_flange_track = _box(
        p.shutter_track_flange_width,
        track_length,
        p.bottom_track_floor_z - p.bottom_track_lip_underside_z,
        center=(
            0.0,
            track_center_y,
            (p.bottom_track_floor_z + p.bottom_track_lip_underside_z) / 2,
        ),
    )
    bottom_web_track = _box(
        p.shutter_track_web_width,
        track_length,
        p.bottom_track_lip_underside_z
        - (-p.housing_size / 2 + p.track_skin_thickness),
        center=(
            0.0,
            track_center_y,
            (
                p.bottom_track_lip_underside_z
                + (-p.housing_size / 2 + p.track_skin_thickness)
            )
            / 2,
        ),
    )
    body = (
        body
        - top_flange_track
        - top_web_track
        - bottom_flange_track
        - bottom_web_track
    )

    # Fixed exterior apertures cut through the track floor and outer skin.
    top_aperture = _box(
        p.fixed_fill_width,
        p.fixed_fill_length,
        3.2,
        center=(0.0, p.fixed_fill_center_y, 18.7),
    )
    bottom_aperture = _box(
        p.fixed_outlet_width,
        p.fixed_outlet_length,
        3.2,
        center=(0.0, p.fixed_outlet_center_y, -18.7),
    )
    body = body - top_aperture - bottom_aperture

    # Hidden longitudinal coupling channels connect track lugs to shuttle
    # sockets without opening an exterior path.
    top_coupler_min_y = (
        p.latched_center_y
        + p.inward_state
        + p.top_coupling_local_y
        - 1.5
    )
    top_coupler_max_y = (
        p.latched_center_y
        + p.maximum_pull_state
        + p.top_coupling_local_y
        + 1.5
    )
    bottom_coupler_min_y = (
        p.latched_center_y
        + p.inward_state
        + p.bottom_coupling_local_y
        - 1.5
    )
    bottom_coupler_max_y = (
        p.latched_center_y
        + p.maximum_pull_state
        + p.bottom_coupling_local_y
        + 1.5
    )
    top_coupler_channel = _box_between_y(
        5.4,
        top_coupler_min_y,
        top_coupler_max_y,
        p.top_track_floor_z - p.housing_inner_half_z + 0.5,
        center_z=(p.top_track_floor_z + p.housing_inner_half_z) / 2,
    )
    bottom_coupler_channel = _box_between_y(
        5.4,
        bottom_coupler_min_y,
        bottom_coupler_max_y,
        -p.housing_inner_half_z - p.bottom_track_floor_z + 0.5,
        center_z=(p.bottom_track_floor_z - p.housing_inner_half_z) / 2,
    )
    body = body - top_coupler_channel - bottom_coupler_channel

    # Four blind snap pockets receive hook tips without opening the side skin.
    hook_pocket_center_y = -14.5
    for side in (-1.0, 1.0):
        pocket_center_x = side * (
            p.rear_channel_half_width + 0.45
        )
        for z_center in (-p.rear_hook_z_offset, p.rear_hook_z_offset):
            pocket = _box(
                1.1,
                2.4,
                p.rear_hook_height + 0.6,
                center=(pocket_center_x, hook_pocket_center_y, z_center),
            )
            body = body - pocket

    for side in (-1.0, 1.0):
        for z_center in (-p.rail_z_offset, p.rail_z_offset):
            body = body + _rail_with_rear_lead_in(side, z_center, p)

    body.label = "p0_v2_fixed_housing_tracks_four_rails"
    return body


def _make_shutter(
    *,
    rear_y: float,
    front_y: float,
    opening_width: float,
    opening_length: float,
    opening_center_y: float,
    top: bool,
    coupling_local_y: float,
    p: P0V2Spec,
) -> Part:
    length = front_y - rear_y
    center_y = (rear_y + front_y) / 2
    if top:
        web_center_z = p.top_shutter_exterior_z - p.shutter_web_thickness / 2
        flange_center_z = p.top_web_bottom_z - p.shutter_flange_thickness / 2
        lug_center_z = p.top_flange_bottom_z - p.coupling_lug_engagement / 2
    else:
        web_center_z = p.bottom_shutter_exterior_z + p.shutter_web_thickness / 2
        flange_center_z = p.bottom_web_top_z + p.shutter_flange_thickness / 2
        lug_center_z = p.bottom_flange_top_z + p.coupling_lug_engagement / 2

    web = _box(
        p.shutter_web_width,
        length,
        p.shutter_web_thickness,
        center=(0.0, center_y, web_center_z),
    )
    flange = _box(
        p.shutter_flange_width,
        length,
        p.shutter_flange_thickness,
        center=(0.0, center_y, flange_center_z),
    )
    shutter = web + flange
    opening = _box(
        opening_width,
        opening_length,
        p.shutter_web_thickness + p.shutter_flange_thickness + 1.0,
        center=(0.0, opening_center_y, web_center_z),
    )
    shutter = shutter - opening
    lug = _box(
        p.coupling_lug_width,
        p.coupling_lug_length,
        p.coupling_lug_engagement,
        center=(0.0, coupling_local_y, lug_center_z),
    )
    return shutter + lug


def make_top_shutter(p: P0V2Spec = P0V2) -> Part:
    shutter = _make_shutter(
        rear_y=p.top_shutter_local_rear_y,
        front_y=p.top_shutter_local_front_y,
        opening_width=p.moving_fill_width,
        opening_length=p.moving_fill_length,
        opening_center_y=p.moving_fill_local_center_y,
        top=True,
        coupling_local_y=p.top_coupling_local_y,
        p=p,
    )
    shutter.label = "p0_v2_top_captured_shutter"
    return shutter


def make_bottom_shutter(p: P0V2Spec = P0V2) -> Part:
    shutter = _make_shutter(
        rear_y=p.bottom_shutter_local_rear_y,
        front_y=p.bottom_shutter_local_front_y,
        opening_width=p.moving_outlet_width,
        opening_length=p.moving_outlet_length,
        opening_center_y=p.moving_outlet_local_center_y,
        top=False,
        coupling_local_y=p.bottom_coupling_local_y,
        p=p,
    )
    shutter.label = "p0_v2_bottom_captured_shutter"
    return shutter


def make_shuttle(p: P0V2Spec = P0V2) -> Part:
    """Return the medicine shuttle without the rejected rear roof tongue."""

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

    top_opening = _box(
        p.moving_fill_width,
        p.moving_fill_length,
        p.medicine_wall + 2.0,
        center=(
            0.0,
            p.moving_fill_local_center_y,
            p.shuttle_height / 2 - p.medicine_wall / 2,
        ),
    )
    bottom_opening = _box(
        p.moving_outlet_width,
        p.moving_outlet_length,
        p.medicine_wall + 2.0,
        center=(
            0.0,
            p.moving_outlet_local_center_y,
            -p.shuttle_height / 2 + p.medicine_wall / 2,
        ),
    )
    shuttle = shuttle - top_opening - bottom_opening

    key_face = _box_between_y(
        p.key_face_size,
        p.shuttle_front_y,
        p.shuttle_front_y + p.key_face_thickness,
        p.key_face_size,
    )
    shuttle = shuttle + key_face

    tab_extension = (
        p.captive_tab_overall_width - p.shuttle_width
    ) / 2
    tab_center_y = (p.tab_local_rear_y + p.tab_local_front_y) / 2
    for side in (-1.0, 1.0):
        tab_center_x = side * (
            p.shuttle_width / 2 + tab_extension / 2
        )
        shuttle = shuttle + _box(
            tab_extension,
            p.captive_tab_depth,
            p.captive_tab_height,
            center=(tab_center_x, tab_center_y, 0.0),
        )

    boss_radial_depth = p.bearing_boss_outer_x - p.shuttle_width / 2
    groove_cutter_depth = p.groove_radial_depth + 1.0
    for side in (-1.0, 1.0):
        boss_center_x = side * (
            p.shuttle_width / 2 + boss_radial_depth / 2
        )
        groove_center_x = side * (
            p.groove_bottom_x + groove_cutter_depth / 2
        )
        mouth_depth = groove_cutter_depth + p.groove_mouth_extra_depth
        mouth_center_x = side * (
            p.groove_bottom_x
            - p.groove_mouth_extra_depth
            + mouth_depth / 2
        )
        for z_center in (-p.rail_z_offset, p.rail_z_offset):
            for y_center in (p.rear_land_local_y, p.front_land_local_y):
                shuttle = shuttle + _box(
                    boss_radial_depth,
                    p.land_length,
                    p.bearing_boss_tangential_width,
                    center=(boss_center_x, y_center, z_center),
                )
                shuttle = shuttle - _box(
                    groove_cutter_depth,
                    p.land_length + 0.4,
                    p.groove_width_nominal,
                    center=(groove_center_x, y_center, z_center),
                )
                mouth_center_y = (
                    y_center
                    - p.land_length / 2
                    + p.groove_mouth_length / 2
                )
                shuttle = shuttle - _box(
                    mouth_depth,
                    p.groove_mouth_length,
                    p.groove_width_nominal + p.groove_mouth_extra_width,
                    center=(mouth_center_x, mouth_center_y, z_center),
                )

    # Coupling bosses and clearance sockets mechanically bind shutters in Y.
    top_boss = _box(
        5.0,
        2.0,
        1.3,
        center=(0.0, p.top_coupling_local_y, 17.75),
    )
    bottom_boss = _box(
        5.0,
        2.0,
        1.3,
        center=(0.0, p.bottom_coupling_local_y, -17.75),
    )
    shuttle = shuttle + top_boss + bottom_boss
    top_socket = _box(
        p.coupling_lug_width + 2 * p.coupling_socket_clearance,
        p.coupling_lug_length + 2 * p.coupling_socket_clearance,
        0.7,
        center=(0.0, p.top_coupling_local_y, 18.35),
    )
    bottom_socket = _box(
        p.coupling_lug_width + 2 * p.coupling_socket_clearance,
        p.coupling_lug_length + 2 * p.coupling_socket_clearance,
        0.7,
        center=(0.0, p.bottom_coupling_local_y, -18.35),
    )
    shuttle = shuttle - top_socket - bottom_socket
    shuttle.label = "p0_v2_medicine_shuttle_eight_lands"
    return shuttle


def _hook_tip(side: float, z_center: float, p: P0V2Spec) -> Shape:
    beam_outer = side * (p.rear_channel_half_width - 0.05)
    tip_outer = side * p.rear_hook_tip_x
    chamfered_outer = side * (p.rear_hook_tip_x - p.rear_hook_chamfer)
    beam_inner = side * (
        p.rear_channel_half_width - 0.05 - p.rear_hook_cantilever_thickness
    )
    if side > 0:
        points = (
            (beam_inner, 3.6),
            (tip_outer, 3.6),
            (chamfered_outer, 5.0),
            (beam_inner, 5.0),
        )
    else:
        points = (
            (beam_inner, 3.6),
            (beam_inner, 5.0),
            (chamfered_outer, 5.0),
            (tip_outer, 3.6),
        )
    tip = extrude(Polygon(*points), p.rear_hook_height)
    return tip.moved(
        Location((0.0, 0.0, z_center - p.rear_hook_height / 2))
    )


def make_blind_rear_cover(p: P0V2Spec = P0V2) -> Part:
    """Return the flush blind cover with four compliant snap hooks."""

    cover = _box(
        p.rear_cover_width,
        p.rear_cover_thickness,
        p.rear_cover_height,
    )
    for side in (-1.0, 1.0):
        beam_center_x = side * (
            p.rear_channel_half_width
            - 0.05
            - p.rear_hook_cantilever_thickness / 2
        )
        for z_center in (-p.rear_hook_z_offset, p.rear_hook_z_offset):
            beam = _box(
                p.rear_hook_cantilever_thickness,
                p.rear_hook_beam_length,
                p.rear_hook_height,
                center=(
                    beam_center_x,
                    p.rear_cover_thickness / 2
                    + p.rear_hook_beam_length / 2,
                    z_center,
                ),
            )
            cover = cover + beam + _hook_tip(side, z_center, p)
    cover.label = "p0_v2_blind_flush_snap_cover_four_hooks"
    return cover


def make_rail_coupon(
    groove_width: float,
    p: P0V2Spec = P0V2,
) -> Compound:
    """Return separate fixed-rib and receiver solids for clearance printing."""

    if groove_width not in (p.groove_width_nominal, p.groove_width_loose):
        raise ValueError("coupon groove must be the frozen nominal or loose width")
    rail_base = _box(2.0, 18.0, 7.0, center=(-6.0, 0.0, 0.0))
    rail = _box(
        p.rail_radial_height,
        18.0,
        p.rail_tangential_width,
        center=(-4.4, 0.0, 0.0),
    )
    rail_part = rail_base + rail
    rail_part.label = "coupon_fixed_rail_2.2x1.2"

    receiver = _box(4.0, 12.0, 7.0, center=(6.0, 0.0, 0.0))
    groove = _box(
        p.groove_radial_depth + 1.0,
        12.4,
        groove_width,
        center=(4.85, 0.0, 0.0),
    )
    receiver = receiver - groove
    receiver.label = f"coupon_receiver_groove_{groove_width:.1f}mm"
    return Compound(
        children=[rail_part, receiver],
        label=f"p0_v2_rail_coupon_{groove_width:.1f}mm",
    )


__all__ = [
    "make_blind_rear_cover",
    "make_bottom_shutter",
    "make_housing",
    "make_rail_coupon",
    "make_shuttle",
    "make_top_shutter",
]
