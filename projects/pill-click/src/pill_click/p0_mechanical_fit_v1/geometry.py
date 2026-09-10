"""Direct STEP-first geometry for the opening-free three-part prototype."""

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
    Shape,
    ThreePointArc,
    extrude,
    make_face,
)

from .spec import P0_MECHANICAL_FIT_V1, P0MechanicalFitV1Spec


def _box_bounds(
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
    z_bounds: tuple[float, float],
) -> Part:
    return Box(
        x_bounds[1] - x_bounds[0],
        y_bounds[1] - y_bounds[0],
        z_bounds[1] - z_bounds[0],
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(
        Location(
            (
                sum(x_bounds) / 2,
                sum(y_bounds) / 2,
                sum(z_bounds) / 2,
            )
        )
    )


def _rail(side: float, z_center: float, p: P0MechanicalFitV1Spec) -> Shape:
    root_x = side * p.rail_root_x
    tip_x = side * p.rail_inner_tip_x
    rear_y, front_y = p.rail_global_y
    if side < 0:
        points = (
            (root_x, rear_y),
            (tip_x, rear_y + p.rail_rear_ramp),
            (tip_x, front_y),
            (root_x, front_y),
        )
    else:
        points = (
            (root_x, rear_y),
            (root_x, front_y),
            (tip_x, front_y),
            (tip_x, rear_y + p.rail_rear_ramp),
        )
    rail = extrude(Polygon(*points), p.rail_tangential_width)
    return rail.moved(
        Location((0.0, 0.0, z_center - p.rail_tangential_width / 2))
    )


def make_outer_housing(
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Part:
    """Plain 40 mm housing with only guide, rails, stops, and C4 receivers."""

    body = _box_bounds(
        (-p.half_housing, p.half_housing),
        (p.housing_fixed_rear_y, p.half_housing),
        (-p.half_housing, p.half_housing),
    )
    body = body - _box_bounds(
        (-p.rear_channel_width / 2, p.rear_channel_width / 2),
        (p.housing_fixed_rear_y - 0.2, p.front_shoulder_y),
        (-p.rear_channel_height / 2, p.rear_channel_height / 2),
    )
    body = body - _box_bounds(
        (-p.front_key_guide_width / 2, p.front_key_guide_width / 2),
        (p.front_shoulder_y, p.half_housing + 0.2),
        (-p.rear_channel_height / 2, p.rear_channel_height / 2),
    )

    for side in (-1.0, 1.0):
        pad_x = (
            (p.captive_stop_throat_width / 2, p.rear_channel_width / 2)
            if side > 0
            else (-p.rear_channel_width / 2, -p.captive_stop_throat_width / 2)
        )
        body = body + _box_bounds(
            pad_x,
            (p.front_shoulder_y, p.half_housing),
            (-p.captive_stop_pad_height / 2, p.captive_stop_pad_height / 2),
        )

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
        for z_center in p.rail_z_centres:
            body = body + _rail(side, z_center, p)

    body = body.clean()
    body.label = "p0_mechanical_fit_v1_outer_housing_plain_guides_rails_blind_C4_receivers"
    return body


def _rear_backing_rib(
    side: float,
    z_center: float,
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Part:
    inner_x = p.groove_bottom_x - p.rear_backing_rib_radial_thickness
    x_bounds = (
        (inner_x, p.groove_bottom_x)
        if side > 0
        else (-p.groove_bottom_x, -inner_x)
    )
    return _box_bounds(
        x_bounds,
        p.rear_backing_rib_local_y,
        (
            z_center - p.bearing_boss_width / 2,
            z_center + p.bearing_boss_width / 2,
        ),
    )


def _add_strengthened_lands(
    button: Part,
    p: P0MechanicalFitV1Spec,
) -> Part:
    boss_depth = p.boss_outer_x - p.inner_body_half
    groove_cut_depth = p.groove_radial_depth + 1.0
    for side in (-1.0, 1.0):
        boss_center_x = side * (p.inner_body_half + boss_depth / 2)
        groove_center_x = side * (p.groove_bottom_x + groove_cut_depth / 2)
        mouth_depth = groove_cut_depth + p.mouth_extra_radial_depth
        mouth_center_x = side * (
            p.groove_bottom_x - p.mouth_extra_radial_depth + mouth_depth / 2
        )
        for z_center in p.rail_z_centres:
            for y_bounds in (p.rear_land_local_y, p.front_land_local_y):
                y_center = sum(y_bounds) / 2
                button = button + _box_bounds(
                    (
                        boss_center_x - boss_depth / 2,
                        boss_center_x + boss_depth / 2,
                    ),
                    y_bounds,
                    (
                        z_center - p.bearing_boss_width / 2,
                        z_center + p.bearing_boss_width / 2,
                    ),
                )
                button = button - _box_bounds(
                    (
                        groove_center_x - groove_cut_depth / 2,
                        groove_center_x + groove_cut_depth / 2,
                    ),
                    (y_bounds[0] - 0.01, y_bounds[1] + 0.01),
                    (
                        z_center - p.nominal_groove_width / 2,
                        z_center + p.nominal_groove_width / 2,
                    ),
                )
                button = button - _box_bounds(
                    (
                        mouth_center_x - mouth_depth / 2,
                        mouth_center_x + mouth_depth / 2,
                    ),
                    (y_bounds[1] - p.mouth_length, y_bounds[1] + 0.01),
                    (
                        z_center - p.mouth_width / 2,
                        z_center + p.mouth_width / 2,
                    ),
                )
                assert y_center in (
                    p.rear_land_local_center_y,
                    p.front_land_local_center_y,
                )
            button = button + _rear_backing_rib(side, z_center, p)
    return button


def make_solid_inner_button(
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Part:
    """Solid CAD button; slicer infill controls its internal material use."""

    outer = _box_bounds(
        (-p.inner_body_half, p.inner_body_half),
        (p.inner_body_rear_local_y, p.inner_body_front_local_y),
        (-p.inner_body_half, p.inner_body_half),
    )
    button = outer

    key = _box_bounds(
        (-p.key_face_size / 2, p.key_face_size / 2),
        p.key_local_y,
        (-p.key_face_size / 2, p.key_face_size / 2),
    )
    for side in (-1.0, 1.0):
        x_bounds = (
            p.key_interface_relief_x
            if side > 0
            else (-p.key_interface_relief_x[1], -p.key_interface_relief_x[0])
        )
        for z_center in p.rail_z_centres:
            key = key - _box_bounds(
                x_bounds,
                p.key_interface_relief_local_y,
                (
                    z_center - p.key_rail_relief_width_z / 2,
                    z_center + p.key_rail_relief_width_z / 2,
                ),
            )
        key = key - _box_bounds(
            x_bounds,
            p.key_interface_relief_local_y,
            p.key_stop_relief_z,
        )
    button = button + key

    for side in (-1.0, 1.0):
        x_bounds = (
            (p.inner_body_half, p.captive_tab_span / 2)
            if side > 0
            else (-p.captive_tab_span / 2, -p.inner_body_half)
        )
        button = button + _box_bounds(
            x_bounds,
            p.captive_tab_local_y,
            (-p.captive_tab_height_z / 2, p.captive_tab_height_z / 2),
        )

    button = _add_strengthened_lands(button, p).clean()
    button.label = "p0_mechanical_fit_v1_solid_inner_button_C1R1_rails_no_internal_void"
    return button


def _make_snap_root_prism(
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Part:
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
    return extrude(make_face(outline.line), p.rear_snap_width).moved(
        Location((0.0, 0.0, -p.rear_snap_width / 2))
    )


def _snap_root_material(
    x_center: float,
    *,
    top: bool,
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Part:
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
    return _make_snap_root_prism(p).transform_geometry(transform)


def _snap_root_relief_cutter(
    x_center: float,
    *,
    top: bool,
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Part:
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


def _hook_prism(
    x_center: float,
    *,
    top: bool,
    p: P0MechanicalFitV1Spec,
) -> Part:
    base_z = (
        p.rear_snap_top_beam_outer_z if top else p.rear_snap_bottom_beam_outer_z
    )
    apex_z = (
        p.rear_snap_top_hook_apex_z if top else p.rear_snap_bottom_hook_apex_z
    )
    with BuildSketch(Plane.YZ) as profile:
        Polygon(
            (p.rear_snap_pocket_rear_y, base_z),
            (p.rear_faceplate_interior_y + p.rear_snap_hook_apex_y, apex_z),
            (p.rear_snap_pocket_front_y, base_z),
        )
    return extrude(profile.sketch, p.rear_snap_width).moved(
        Location((x_center - p.rear_snap_width / 2, 0.0, 0.0))
    )


def make_snap_rear_cover(
    p: P0MechanicalFitV1Spec = P0_MECHANICAL_FIT_V1,
) -> Part:
    """Blind 1.30 mm faceplate, pilot, and four exact C4 V3.1 snaps."""

    cover = _box_bounds(
        (-p.half_housing, p.half_housing),
        (p.rear_faceplate_exterior_y, p.rear_faceplate_interior_y),
        (-p.half_housing, p.half_housing),
    )
    cover = cover + _box_bounds(
        (-p.rear_cover_pilot_width / 2, p.rear_cover_pilot_width / 2),
        (p.rear_faceplate_interior_y, p.rear_cover_pilot_front_y),
        (-p.rear_cover_pilot_height / 2, p.rear_cover_pilot_height / 2),
    )

    for side in (-1.0, 1.0):
        x_bounds = (17.25, 18.55) if side > 0 else (-18.55, -17.25)
        for z_center in p.rail_z_centres:
            cover = cover - _box_bounds(
                x_bounds,
                (p.rear_faceplate_interior_y - 0.01, p.rear_cover_pilot_front_y + 0.01),
                (z_center - 1.4, z_center + 1.4),
            )

    for x_center in (-p.rear_snap_center_x, p.rear_snap_center_x):
        cover = cover - _snap_root_relief_cutter(x_center, top=True, p=p)
        cover = cover - _snap_root_relief_cutter(x_center, top=False, p=p)

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
        cover = cover + _snap_root_material(x_center, top=True, p=p)
        cover = cover + _snap_root_material(x_center, top=False, p=p)
        cover = cover + _hook_prism(x_center, top=True, p=p)
        cover = cover + _hook_prism(x_center, top=False, p=p)

    cover = cover.clean()
    cover.label = "p0_mechanical_fit_v1_snap_rear_cover_blind_face_four_C4_V3p1_snaps"
    return cover


__all__ = [
    "make_solid_inner_button",
    "make_outer_housing",
    "make_snap_rear_cover",
]
