"""STEP-first P0 v3 housing, shuttle, solid shutters, and blind cover."""

import math

from build123d import (
    Align,
    Box,
    BuildLine,
    BuildSketch,
    Line,
    Location,
    Matrix,
    Part,
    Plane,
    Polygon,
    Rectangle,
    Shape,
    ThreePointArc,
    extrude,
    loft,
    make_face,
)

from .spec import P0V3, P0V3Spec


def _make_snap_root_prism(p: P0V3Spec = P0V3) -> Part:
    """Exact coupon-local V3.1 root shared by C4 and the four cover arms.

    Coupon axes are X=radial bending, Y=axial insertion, and Z=arm width.
    The 0.20 mm rear/radial extensions provide finite grip and beam overlap;
    the exact R0.80 quarter arc is the exposed stress-relief boundary.
    """

    radius = p.rear_snap_root_fillet
    overlap = p.rear_snap_root_overlap
    tangent_y = p.rear_snap_root_tangent_y
    arc_midpoint = (
        -radius + radius / math.sqrt(2),
        tangent_y - radius / math.sqrt(2),
    )
    with BuildLine(Plane.XY) as outline:
        Line((-radius, -overlap), (overlap, -overlap))
        Line((overlap, -overlap), (overlap, tangent_y))
        Line((overlap, tangent_y), (0.0, tangent_y))
        ThreePointArc((0.0, tangent_y), arc_midpoint, (-radius, 0.0))
        Line((-radius, 0.0), (-radius, -overlap))
    root = extrude(make_face(outline.line), p.rear_snap_width)
    root = root.moved(Location((0.0, 0.0, -p.rear_snap_width / 2)))
    root.label = "V3p1_exact_R0p80_snap_root_prism"
    return root


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
    return shape if center == (0.0, 0.0, 0.0) else shape.moved(Location(center))


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


def _box_bounds(
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
    z_bounds: tuple[float, float],
) -> Part:
    return _box(
        x_bounds[1] - x_bounds[0],
        y_bounds[1] - y_bounds[0],
        z_bounds[1] - z_bounds[0],
        center=(
            sum(x_bounds) / 2,
            sum(y_bounds) / 2,
            sum(z_bounds) / 2,
        ),
    )


def _rail(side: float, z_center: float, p: P0V3Spec) -> Shape:
    """One side rail with its frozen 0.70 mm rear insertion ramp."""

    root_x = side * p.rail_root_x
    tip_x = side * p.rail_inner_tip_x
    if side < 0:
        points = (
            (root_x, p.rail_start_y),
            (tip_x, p.rail_start_y + p.rail_rear_lead_in),
            (tip_x, p.rail_end_y),
            (root_x, p.rail_end_y),
        )
    else:
        points = (
            (root_x, p.rail_start_y),
            (root_x, p.rail_end_y),
            (tip_x, p.rail_end_y),
            (tip_x, p.rail_start_y + p.rail_rear_lead_in),
        )
    rail = extrude(Polygon(*points), p.rail_tangential_width)
    return rail.moved(Location((0.0, 0.0, z_center - p.rail_tangential_width / 2)))


def make_housing(p: P0V3Spec = P0V3) -> Part:
    """Fixed housing from Y=-18.70 forward, including tracks and blind pockets."""

    body = _box_between_y(
        p.housing_size,
        p.housing_fixed_rear_y,
        p.housing_half,
        p.housing_size,
    )

    # Rear channel and 35.60 main key guide. Localized stop pads are restored
    # after the guide cut; they are the only 34.90 throat regions.
    rear_channel = _box_between_y(
        p.rear_channel_width,
        p.housing_fixed_rear_y - 0.2,
        p.front_shoulder_y,
        p.rear_channel_height,
    )
    front_guide = _box_between_y(
        p.front_key_guide_width,
        p.front_shoulder_y,
        p.housing_half + 0.2,
        p.rear_channel_height,
    )
    body = body - rear_channel - front_guide

    stop_pad_width = (p.rear_channel_width - p.captive_stop_throat_width) / 2
    for side in (-1.0, 1.0):
        pad_center_x = side * (
            p.captive_stop_throat_width / 2 + stop_pad_width / 2
        )
        body = body + _box_between_y(
            stop_pad_width,
            p.front_shoulder_y,
            p.housing_half,
            p.captive_stop_pad_height,
        ).moved(Location((pad_center_x, 0.0, 0.0)))

    # Rear-fed captured tracks. Their web slots stop at the opaque 0.80 mm
    # shrouds; the shrouds are native housing material, not thin added skins.
    top_flange_track = _box_bounds(
        (-p.track_flange_width / 2, p.track_flange_width / 2),
        (p.housing_fixed_rear_y - 0.2, p.top_opaque_shroud_rear_y),
        (p.top_track_floor_z, p.top_lip_underside_z),
    )
    top_web_track = _box_bounds(
        (-p.track_web_width / 2, p.track_web_width / 2),
        (p.housing_fixed_rear_y - 0.2, p.top_opaque_shroud_rear_y),
        (p.top_lip_underside_z, p.housing_half + 0.2),
    )
    bottom_flange_track = _box_bounds(
        (-p.track_flange_width / 2, p.track_flange_width / 2),
        (p.housing_fixed_rear_y - 0.2, p.bottom_opaque_shroud_rear_y),
        (p.bottom_lip_inner_z, p.bottom_track_floor_z),
    )
    bottom_web_track = _box_bounds(
        (-p.track_web_width / 2, p.track_web_width / 2),
        (p.housing_fixed_rear_y - 0.2, p.bottom_opaque_shroud_rear_y),
        (-p.housing_half - 0.2, p.bottom_lip_inner_z),
    )
    body = body - top_flange_track - top_web_track - bottom_flange_track - bottom_web_track

    # Fixed negative-Y track mouths flare by 0.40 total width and 0.20 height.
    mouth_y = (
        p.housing_fixed_rear_y - 0.2,
        p.housing_fixed_rear_y + p.shutter_lead_in_length,
    )
    body = body - _box_bounds(
        (
            -(p.track_flange_width + p.track_mouth_extra_width) / 2,
            (p.track_flange_width + p.track_mouth_extra_width) / 2,
        ),
        mouth_y,
        (p.top_track_floor_z - p.track_mouth_extra_height, p.top_lip_underside_z),
    )
    body = body - _box_bounds(
        (
            -(p.track_web_width + p.track_mouth_extra_width) / 2,
            (p.track_web_width + p.track_mouth_extra_width) / 2,
        ),
        mouth_y,
        (p.top_lip_underside_z, p.housing_half + 0.2),
    )
    body = body - _box_bounds(
        (
            -(p.track_flange_width + p.track_mouth_extra_width) / 2,
            (p.track_flange_width + p.track_mouth_extra_width) / 2,
        ),
        mouth_y,
        (p.bottom_lip_inner_z, p.bottom_track_floor_z + p.track_mouth_extra_height),
    )
    body = body - _box_bounds(
        (
            -(p.track_web_width + p.track_mouth_extra_width) / 2,
            (p.track_web_width + p.track_mouth_extra_width) / 2,
        ),
        mouth_y,
        (-p.housing_half - 0.2, p.bottom_lip_inner_z),
    )

    # The fixed ports are explicit subsets of the exposed web track.
    body = body - _box(
        p.fixed_fill_width,
        p.fixed_fill_length,
        2.4,
        center=(0.0, p.fixed_fill_center_y, 18.8),
    )
    body = body - _box(
        p.fixed_outlet_width,
        p.fixed_outlet_length,
        2.4,
        center=(0.0, p.fixed_outlet_center_y, -18.8),
    )

    # The translated medicine openings sit beneath true four-layer shrouds,
    # not beneath the original 2.10 mm housing wall.  Remove the central wall
    # below each shroud while retaining the specified native 0.80 mm exterior
    # skin and the structural side strips outside X=+/-12.70.
    body = body - _box_bounds(
        (-p.opaque_shroud_width_x / 2, p.opaque_shroud_width_x / 2),
        (p.top_opaque_shroud_rear_y, p.housing_half + 0.2),
        (-p.rear_channel_half_height - 0.2, p.top_lip_underside_z),
    )
    body = body - _box_bounds(
        (-p.opaque_shroud_width_x / 2, p.opaque_shroud_width_x / 2),
        (p.bottom_opaque_shroud_rear_y, p.housing_half + 0.2),
        (p.bottom_lip_inner_z, p.rear_channel_half_height + 0.2),
    )

    # Rear-open coupling keep-out channels, closed only by the final cover.
    body = body - _box_bounds(
        (-p.coupling_channel_width / 2, p.coupling_channel_width / 2),
        (p.housing_fixed_rear_y - 0.2, p.top_coupling_channel_front_y),
        (15.4, 18.6),
    )
    body = body - _box_bounds(
        (-p.coupling_channel_width / 2, p.coupling_channel_width / 2),
        (p.housing_fixed_rear_y - 0.2, p.bottom_coupling_channel_front_y),
        (-18.6, -15.4),
    )

    # Four C4-mapped snap passages and blind pockets in the 2.10 top/bottom
    # walls. Pockets retain 1.20 mm exterior skin.
    for x_center in (-p.rear_snap_center_x, p.rear_snap_center_x):
        x_bounds = (
            x_center - p.rear_snap_pocket_width_x / 2,
            x_center + p.rear_snap_pocket_width_x / 2,
        )
        body = body - _box_bounds(
            x_bounds,
            (p.housing_fixed_rear_y - 0.2, p.rear_snap_pocket_front_y),
            (16.75, p.rear_snap_top_beam_outer_z),
        )
        body = body - _box_bounds(
            x_bounds,
            (p.rear_snap_pocket_rear_y, p.rear_snap_pocket_front_y),
            (p.rear_snap_top_beam_outer_z, p.rear_snap_pocket_outer_z),
        )
        body = body - _box_bounds(
            x_bounds,
            (p.housing_fixed_rear_y - 0.2, p.rear_snap_pocket_front_y),
            (p.rear_snap_bottom_beam_outer_z, -16.75),
        )
        body = body - _box_bounds(
            x_bounds,
            (p.rear_snap_pocket_rear_y, p.rear_snap_pocket_front_y),
            (-p.rear_snap_pocket_outer_z, p.rear_snap_bottom_beam_outer_z),
        )

    for side in (-1.0, 1.0):
        for z_center in (-p.rail_z_offset, p.rail_z_offset):
            body = body + _rail(side, z_center, p)

    body.label = "p0_v3_fixed_housing_tracks_shrouds_rails_snap_pockets"
    return body


def _flange_with_leading_taper(
    rear_y: float,
    front_y: float,
    *,
    top: bool,
    p: P0V3Spec,
) -> Part:
    full_front = front_y - p.shutter_lead_in_length
    if top:
        full_center_z = 18.6
        tip_center_z = 18.8
    else:
        full_center_z = -18.6
        tip_center_z = -18.8
    full = _box_between_y(
        p.shutter_flange_width,
        rear_y,
        full_front,
        p.shutter_flange_thickness,
        center_z=full_center_z,
    )
    full_section = Rectangle(
        p.shutter_flange_width,
        p.shutter_flange_thickness,
    ).moved(Location((0.0, full_front, full_center_z), (90.0, 0.0, 0.0)))
    tip_section = Rectangle(
        p.shutter_web_width,
        p.shutter_flange_thickness / 2,
    ).moved(Location((0.0, front_y, tip_center_z), (90.0, 0.0, 0.0)))
    return full + loft([full_section, tip_section])


def _make_shutter(*, top: bool, p: P0V3Spec) -> Part:
    rear_y = p.top_shutter_local_rear_y if top else p.bottom_shutter_local_rear_y
    front_y = p.top_shutter_local_front_y if top else p.bottom_shutter_local_front_y
    web_center_z = 19.4 if top else -19.4
    web = _box_between_y(
        p.shutter_web_width,
        rear_y,
        front_y,
        p.shutter_web_thickness,
        center_z=web_center_z,
    )
    shutter = web + _flange_with_leading_taper(rear_y, front_y, top=top, p=p)

    if top:
        lug_y = p.top_lug_local_y
        lug_z = (17.4, 18.2)
        neck_z = (17.4, 19.02)
        notch_z = (17.0, 17.6)
        notch_y = (-20.6, -19.8)
        boss_y = (-22.3, -18.1)
        flange_z = (18.2, 19.01)
    else:
        lug_y = p.bottom_lug_local_y
        lug_z = (-18.2, -17.4)
        neck_z = (-19.02, -17.4)
        notch_z = (-17.6, -17.0)
        notch_y = (-14.6, -13.8)
        boss_y = (-16.3, -12.1)
        flange_z = (-19.01, -18.2)
    # Boss sidewalls need a local flange relief; the 3.00-wide coupling neck
    # passes through the open 3.40 socket and joins the lug to the solid web.
    shutter = shutter - _box_bounds((-2.7, 2.7), boss_y, flange_z)
    lug = _box_bounds(
        (-p.coupling_lug_width_x / 2, p.coupling_lug_width_x / 2),
        lug_y,
        neck_z,
    )
    # The underside detent land receives the shuttle-owned nub without
    # positive-volume overlap while retaining the frozen lug envelope.
    lug = lug - _box_bounds((-1.51, 1.51), notch_y, notch_z)
    shutter = shutter + lug
    shutter.label = (
        "p0_v3_top_solid_shutter_lug" if top else "p0_v3_bottom_solid_shutter_lug"
    )
    return shutter


def make_top_shutter(p: P0V3Spec = P0V3) -> Part:
    return _make_shutter(top=True, p=p)


def make_bottom_shutter(p: P0V3Spec = P0V3) -> Part:
    return _make_shutter(top=False, p=p)


def _rear_land_backing_rib(side: float, z_center: float, p: P0V3Spec) -> Part:
    rib_inner_x = p.groove_bottom_x - p.rear_land_backing_radial_thickness
    rib_center_x = side * (
        rib_inner_x + p.rear_land_backing_radial_thickness / 2
    )
    rib_rear_y, rib_front_y = p.rear_land_backing_local_y
    return _box(
        p.rear_land_backing_radial_thickness,
        rib_front_y - rib_rear_y,
        p.bearing_boss_width,
        center=(
            rib_center_x,
            (rib_rear_y + rib_front_y) / 2,
            z_center,
        ),
    )


def _add_bearing_lands(shuttle: Part, p: P0V3Spec) -> Part:
    boss_outer_x = p.groove_bottom_x + p.groove_radial_depth
    boss_depth = boss_outer_x - p.shuttle_width / 2
    groove_cutter_depth = p.groove_radial_depth + 1.0
    for side in (-1.0, 1.0):
        boss_center_x = side * (p.shuttle_width / 2 + boss_depth / 2)
        groove_center_x = side * (p.groove_bottom_x + groove_cutter_depth / 2)
        mouth_depth = groove_cutter_depth + p.groove_mouth_extra_depth
        mouth_center_x = side * (
            p.groove_bottom_x - p.groove_mouth_extra_depth + mouth_depth / 2
        )
        for z_center in (-p.rail_z_offset, p.rail_z_offset):
            for y_center in (p.rear_land_local_y, p.front_land_local_y):
                shuttle = shuttle + _box(
                    boss_depth,
                    p.land_length,
                    p.bearing_boss_width,
                    center=(boss_center_x, y_center, z_center),
                )
                shuttle = shuttle - _box(
                    groove_cutter_depth,
                    p.land_length + 0.02,
                    p.groove_width_nominal,
                    center=(groove_center_x, y_center, z_center),
                )
                # The positive-Y edge leads during rear-to-front insertion.
                mouth_center_y = y_center + p.land_length / 2 - p.groove_mouth_length / 2
                shuttle = shuttle - _box(
                    mouth_depth,
                    p.groove_mouth_length,
                    p.groove_width_nominal + p.groove_mouth_extra_width,
                    center=(mouth_center_x, mouth_center_y, z_center),
                )

            # The strengthened rear lands extend behind the main medicine
            # body.  Four ribs stop at the frozen groove-bottom datum, overlap
            # the body by 0.20 mm in Y, and overlap each rear boss by positive
            # volume.  They do not enter the rail running-clearance envelope.
            if p.rear_land_backing_radial_thickness > 0.0:
                shuttle = shuttle + _rear_land_backing_rib(side, z_center, p)
    return shuttle


def _add_couplings(shuttle: Part, p: P0V3Spec) -> Part:
    # Remove compliant-finger reliefs from the roof and floor first.
    shuttle = shuttle - _box_bounds((-1.7, 1.7), (-20.8, -11.8), (15.6, 17.3))
    shuttle = shuttle - _box_bounds((-1.7, 1.7), (-14.8, -5.8), (-17.3, -15.6))

    top_boss = _box_bounds((-2.5, 2.5), (-21.3, -18.1), (16.8, 18.4))
    bottom_boss = _box_bounds((-2.5, 2.5), (-15.3, -12.1), (-18.4, -16.8))
    top_root = _box_bounds((-2.3, 2.3), (-11.8, -10.6), (15.6, 17.1))
    bottom_root = _box_bounds((-2.3, 2.3), (-5.8, -4.6), (-17.1, -15.6))
    top_beam = _box_bounds((-1.5, 1.5), (-19.8, -11.8), (16.3, 17.1))
    bottom_beam = _box_bounds((-1.5, 1.5), (-13.8, -5.8), (-17.1, -16.3))
    shuttle = shuttle + top_boss + bottom_boss + top_root + bottom_root + top_beam + bottom_beam

    top_socket = _box_bounds((-1.7, 1.7), p.top_socket_local_y, (17.2, 18.5))
    bottom_socket = _box_bounds((-1.7, 1.7), p.bottom_socket_local_y, (-18.5, -17.2))
    shuttle = shuttle - top_socket - bottom_socket

    # Preload nubs are restored after the socket cuts and seat in the shutter
    # lug underside lands. The 0.80 axial length is the two-sided entry ramp.
    top_nub = _box_bounds((-1.5, 1.5), (-20.6, -19.8), (17.1, 17.6))
    bottom_nub = _box_bounds((-1.5, 1.5), (-14.6, -13.8), (-17.6, -17.1))
    return shuttle + top_nub + bottom_nub


def make_shuttle(p: P0V3Spec = P0V3) -> Part:
    """Hollow medicine shuttle with eight lands, reliefs, sockets, and fingers."""

    outer = _box_between_y(
        p.shuttle_width,
        p.shuttle_rear_local_y,
        p.shuttle_front_local_y,
        p.shuttle_height,
    )
    inner = _box_between_y(
        2 * p.shuttle_inner_half_x,
        p.shuttle_inner_rear_y,
        p.shuttle_inner_front_y,
        2 * p.shuttle_inner_half_z,
    )
    shuttle = outer - inner
    # Cut completely through the 2.00 mm roof/floor and deliberately overshoot
    # both the cavity and the exterior by 0.20 mm.  Centering a 3.00 mm cutter
    # on the outer surface left 0.50 mm of material on the cavity side, which
    # made the nominally aligned apertures visually open but BREP-occluded.
    shuttle = shuttle - _box_bounds(
        (-p.moving_fill_width / 2, p.moving_fill_width / 2),
        (
            p.moving_fill_local_center_y - p.moving_fill_length / 2,
            p.moving_fill_local_center_y + p.moving_fill_length / 2,
        ),
        (p.shuttle_inner_half_z - 0.20, p.shuttle_height / 2 + 0.20),
    )
    shuttle = shuttle - _box_bounds(
        (-p.moving_outlet_width / 2, p.moving_outlet_width / 2),
        (
            p.moving_outlet_local_center_y - p.moving_outlet_length / 2,
            p.moving_outlet_local_center_y + p.moving_outlet_length / 2,
        ),
        (-p.shuttle_height / 2 - 0.20, -p.shuttle_inner_half_z + 0.20),
    )

    key = _box_between_y(
        p.key_face_size,
        p.shuttle_front_local_y,
        p.key_front_local_y,
        p.key_face_size,
    )
    for side in (-1.0, 1.0):
        x_bounds = (17.25, 17.70) if side > 0 else (-17.70, -17.25)
        for z_center in (-p.rail_z_offset, p.rail_z_offset):
            key = key - _box_bounds(
                x_bounds,
                (p.key_relief_rear_local_y, p.key_relief_front_local_y),
                (
                    z_center - p.key_rail_relief_width / 2,
                    z_center + p.key_rail_relief_width / 2,
                ),
            )
        key = key - _box_bounds(
            x_bounds,
            (p.key_relief_rear_local_y, p.key_relief_front_local_y),
            (p.key_stop_relief_min_z, p.key_stop_relief_max_z),
        )
    shuttle = shuttle + key

    tab_extension = (p.captive_tab_span - p.shuttle_width) / 2
    for side in (-1.0, 1.0):
        shuttle = shuttle + _box_bounds(
            (
                side * p.shuttle_width / 2,
                side * p.captive_tab_span / 2,
            )
            if side > 0
            else (
                side * p.captive_tab_span / 2,
                side * p.shuttle_width / 2,
            ),
            (p.tab_local_rear_y, p.tab_local_front_y),
            (-p.captive_tab_height / 2, p.captive_tab_height / 2),
        )
    assert tab_extension > 0

    shuttle = _add_bearing_lands(shuttle, p)
    shuttle = _add_couplings(shuttle, p)
    shuttle.label = "p0_v3_medicine_shuttle_eight_lands_preload_fingers"
    return shuttle


def _hook_prism(
    x_center: float,
    *,
    top: bool,
    p: P0V3Spec,
) -> Part:
    base_z = p.rear_snap_top_beam_outer_z if top else p.rear_snap_bottom_beam_outer_z
    apex_z = p.rear_snap_top_hook_apex_z if top else p.rear_snap_bottom_hook_apex_z
    with BuildSketch(Plane.YZ) as profile:
        Polygon(
            (p.rear_snap_pocket_rear_y, base_z),
            (
                p.rear_faceplate_interior_y + p.rear_snap_hook_apex_y,
                apex_z,
            ),
            (p.rear_snap_pocket_front_y, base_z),
        )
    hook = extrude(profile.sketch, p.rear_snap_width)
    return hook.moved(Location((x_center - p.rear_snap_width / 2, 0.0, 0.0)))


def _snap_root_material(
    x_center: float,
    *,
    top: bool,
    p: P0V3Spec,
) -> Part:
    """Rigidly map the shared coupon-local V3.1 root into the cover."""

    beam_inner_z = (
        p.rear_snap_top_beam_outer_z - p.rear_snap_bending_thickness
        if top
        else p.rear_snap_bottom_beam_outer_z + p.rear_snap_bending_thickness
    )
    radial_sign = 1.0 if top else -1.0
    transform = Matrix(
        [
            [0.0, 0.0, 1.0, x_center],
            [0.0, 1.0, 0.0, p.rear_faceplate_interior_y],
            [radial_sign, 0.0, 0.0, beam_inner_z],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    root = _make_snap_root_prism(p).transform_geometry(transform)
    root.label = "V3p1_mapped_exact_R0p80_snap_root_prism"
    return root


def _snap_root_relief_cutter(
    x_center: float,
    *,
    top: bool,
    p: P0V3Spec,
) -> Part:
    """Exact V3.1 pilot cutter; it must not enter the hidden rear overlap."""

    radial_bounds = (
        (
            p.rear_snap_top_beam_outer_z
            - p.rear_snap_bending_thickness
            - p.rear_snap_root_fillet,
            p.rear_snap_top_beam_outer_z,
        )
        if top
        else (
            p.rear_snap_bottom_beam_outer_z,
            p.rear_snap_bottom_beam_outer_z
            + p.rear_snap_bending_thickness
            + p.rear_snap_root_fillet,
        )
    )
    return _box_bounds(
        (x_center - p.rear_snap_width / 2, x_center + p.rear_snap_width / 2),
        (p.rear_faceplate_interior_y, p.rear_cover_pilot_front_y + 0.01),
        radial_bounds,
    )


def _make_blind_rear_cover(
    p: P0V3Spec = P0V3,
    *,
    include_snap_roots: bool,
) -> Part:
    """Build the cover, optionally omitting only the four V3.1 root prisms."""

    cover = _box_between_y(
        p.rear_faceplate_width,
        p.rear_faceplate_exterior_y,
        p.rear_faceplate_interior_y,
        p.rear_faceplate_height,
    )
    cover = cover + _box_between_y(
        p.rear_cover_pilot_width,
        p.rear_faceplate_interior_y,
        p.rear_cover_pilot_front_y,
        p.rear_cover_pilot_height,
    )
    # The full pilot preserves its frozen outer envelope while four internal
    # reliefs pass the fixed rails during the last axial cover insertion.
    for side in (-1.0, 1.0):
        x_bounds = (17.25, 18.55) if side > 0 else (-18.55, -17.25)
        for z_center in (-p.rail_z_offset, p.rail_z_offset):
            cover = cover - _box_bounds(
                x_bounds,
                (p.rear_faceplate_interior_y - 0.01, p.rear_cover_pilot_front_y + 0.01),
                (z_center - 1.4, z_center + 1.4),
            )

    # The accepted -9 mm coupling relocation brings the top cantilever into
    # the pilot envelope during future s=-1 lost motion.  Continue both rear
    # coupling-channel sections through the pilot, but stop at the full blind
    # 1.30 mm faceplate so rear coverage remains uninterrupted.
    cover = cover - _box_bounds(
        (-p.coupling_channel_width / 2, p.coupling_channel_width / 2),
        (p.rear_faceplate_interior_y - 0.01, p.rear_cover_pilot_front_y + 0.01),
        (15.4, 18.6),
    )
    cover = cover - _box_bounds(
        (-p.coupling_channel_width / 2, p.coupling_channel_width / 2),
        (p.rear_faceplate_interior_y - 0.01, p.rear_cover_pilot_front_y + 0.01),
        (-18.6, -15.4),
    )

    # Remove the pilot's rectangular embed around each snap root.  Within the
    # C4 local root envelope this leaves only the 1.20 beam and the mapped
    # R0.80 quarter-root material added below; outside the 3.60 arm width the
    # pilot remains continuous and still supports the faceplate perimeter.
    for x_center in (-p.rear_snap_center_x, p.rear_snap_center_x):
        cover = cover - _snap_root_relief_cutter(x_center, top=True, p=p)
        cover = cover - _snap_root_relief_cutter(x_center, top=False, p=p)

    for x_center in (-p.shutter_stop_nib_center_x, p.shutter_stop_nib_center_x):
        cover = cover + _box_bounds(
            (
                x_center - p.shutter_stop_nib_width_x / 2,
                x_center + p.shutter_stop_nib_width_x / 2,
            ),
            (p.shutter_stop_nib_rear_y, p.shutter_stop_nib_front_y),
            (18.2, 19.0),
        )
        cover = cover + _box_bounds(
            (
                x_center - p.shutter_stop_nib_width_x / 2,
                x_center + p.shutter_stop_nib_width_x / 2,
            ),
            (p.shutter_stop_nib_rear_y, p.shutter_stop_nib_front_y),
            (-19.0, -18.2),
        )

    for x_center in (-p.rear_snap_center_x, p.rear_snap_center_x):
        top_beam = _box_bounds(
            (x_center - p.rear_snap_width / 2, x_center + p.rear_snap_width / 2),
            (p.rear_faceplate_interior_y, p.rear_snap_pocket_front_y),
            (
                p.rear_snap_top_beam_outer_z - p.rear_snap_bending_thickness,
                p.rear_snap_top_beam_outer_z,
            ),
        )
        bottom_beam = _box_bounds(
            (x_center - p.rear_snap_width / 2, x_center + p.rear_snap_width / 2),
            (p.rear_faceplate_interior_y, p.rear_snap_pocket_front_y),
            (
                p.rear_snap_bottom_beam_outer_z,
                p.rear_snap_bottom_beam_outer_z + p.rear_snap_bending_thickness,
            ),
        )
        cover = cover + top_beam + bottom_beam
        if include_snap_roots:
            cover = cover + _snap_root_material(x_center, top=True, p=p)
            cover = cover + _snap_root_material(x_center, top=False, p=p)
        cover = cover + _hook_prism(x_center, top=True, p=p)
        cover = cover + _hook_prism(x_center, top=False, p=p)

    cover.label = "p0_v3_full_blind_faceplate_pilot_stops_four_c4_snaps"
    return cover


def _make_blind_rear_cover_rootless(p: P0V3Spec = P0V3) -> Part:
    """V3.1 accounting baseline: complete cover without the four root prisms."""

    return _make_blind_rear_cover(p, include_snap_roots=False)


def make_blind_rear_cover(p: P0V3Spec = P0V3) -> Part:
    """Full 40x40 blind faceplate, pilot, four stops, and four C4 snap arms."""

    return _make_blind_rear_cover(p, include_snap_roots=True)


__all__ = [
    "make_blind_rear_cover",
    "make_bottom_shutter",
    "make_housing",
    "make_shuttle",
    "make_top_shutter",
]
