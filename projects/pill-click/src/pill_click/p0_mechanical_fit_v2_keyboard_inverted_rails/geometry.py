"""Direct STEP-first geometry for the V2 keyboard/inverted-rail prototype."""

import math

from build123d import (
    Align,
    Box,
    BuildLine,
    BuildSketch,
    Location,
    Matrix,
    Part,
    Plane,
    Polygon,
    RectangleRounded,
    Shape,
    ThreePointArc,
    extrude,
    loft,
    make_face,
)

from pill_click.geometry import rounded_box

from .spec import P0_MECHANICAL_FIT_V2, P0MechanicalFitV2Spec


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


def _rounded_prism_xz(
    size: float,
    y_bounds: tuple[float, float],
    radius: float,
) -> Part:
    return rounded_box(
        size,
        y_bounds[1] - y_bounds[0],
        size,
        radius,
        center=(0.0, sum(y_bounds) / 2, 0.0),
    )


def _rounded_section_xz(size: float, radius: float, y: float) -> Shape:
    return RectangleRounded(size, size, radius).moved(
        Location((0.0, y, 0.0), (90.0, 0.0, 0.0))
    )


def _outer_keyboard_shell(p: P0MechanicalFitV2Spec) -> Part:
    chamfer_rear = p.housing_front_y - p.front_bezel_chamfer
    straight = _rounded_prism_xz(
        p.housing_size,
        (p.housing_rear_y, chamfer_rear),
        p.housing_outer_corner_radius_xz,
    )
    chamfered_front = loft(
        [
            _rounded_section_xz(
                p.housing_size,
                p.housing_outer_corner_radius_xz,
                chamfer_rear,
            ),
            _rounded_section_xz(
                p.housing_size - 2 * p.front_bezel_chamfer,
                p.housing_outer_corner_radius_xz - p.front_bezel_chamfer,
                p.housing_front_y,
            ),
        ]
    )
    return (straight + chamfered_front).clean()


def _side_bounds(side: float, positive: tuple[float, float]) -> tuple[float, float]:
    return positive if side > 0 else (-positive[1], -positive[0])


def _cut_side_latch_receivers(
    body: Part,
    p: P0MechanicalFitV2Spec,
) -> Part:
    """Cut two split receiver paths while preserving each retention shoulder."""
    for side in (-1.0, 1.0):
        body = body - _box_bounds(
            _side_bounds(side, p.side_latch_broad_notch_x),
            p.side_latch_broad_notch_y,
            (
                -p.side_latch_broad_notch_width_z / 2,
                p.side_latch_broad_notch_width_z / 2,
            ),
        )
        body = body - _box_bounds(
            _side_bounds(side, p.side_latch_rear_connector_slot_x),
            p.side_latch_broad_notch_y,
            (
                -p.side_latch_flex_slot_width_z / 2,
                p.side_latch_flex_slot_width_z / 2,
            ),
        )
        body = body - _box_bounds(
            _side_bounds(side, p.side_latch_forward_beam_passage_x),
            p.side_latch_forward_beam_passage_y,
            (
                -p.side_latch_flex_slot_width_z / 2,
                p.side_latch_flex_slot_width_z / 2,
            ),
        )
        body = body - _box_bounds(
            _side_bounds(side, p.side_latch_pocket_x),
            p.side_latch_pocket_y,
            (
                -p.side_latch_pocket_width_z / 2,
                p.side_latch_pocket_width_z / 2,
            ),
        )
    return body


def make_outer_housing(
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Part:
    body = _outer_keyboard_shell(p)
    body = body - _rounded_prism_xz(
        p.main_guide_size_xz,
        (p.housing_rear_y - 0.2, p.front_guide_rear_y),
        p.main_guide_corner_radius_xz,
    )
    body = body - _rounded_prism_xz(
        p.front_guide_size_xz,
        (p.front_guide_rear_y, p.housing_front_y + 0.2),
        p.front_guide_corner_radius_xz,
    )

    for side in (-1.0, 1.0):
        channel_x = _side_bounds(side, p.female_channel_x)
        mouth_x = _side_bounds(side, p.female_mouth_x)
        for z_center in p.male_rail_centres_z:
            body = body - _box_bounds(
                channel_x,
                (p.female_channel_rear_y - 0.01, p.female_channel_blind_front_y),
                (
                    z_center - p.female_channel_width_z / 2,
                    z_center + p.female_channel_width_z / 2,
                ),
            )
            body = body - _box_bounds(
                mouth_x,
                (
                    p.female_channel_rear_y - 0.01,
                    p.female_channel_rear_y + p.female_mouth_length_y,
                ),
                (
                    z_center
                    - (p.female_channel_width_z + p.female_mouth_extra_width_z) / 2,
                    z_center
                    + (p.female_channel_width_z + p.female_mouth_extra_width_z) / 2,
                ),
            )

    body = _cut_side_latch_receivers(body, p)
    body = body.clean()
    body.label = "p0_mechanical_fit_v2_outer_female_channels_two_side_latch_receivers"
    return body


def _male_rail(
    side: float,
    z_center: float,
    p: P0MechanicalFitV2Spec,
) -> Part:
    return _box_bounds(
        _side_bounds(side, p.male_rail_source_x),
        p.male_rail_local_y,
        (
            z_center - p.male_rail_width_z / 2,
            z_center + p.male_rail_width_z / 2,
        ),
    )


def _rail_spine(
    side: float,
    z_center: float,
    p: P0MechanicalFitV2Spec,
) -> Part:
    return _box_bounds(
        _side_bounds(side, (p.spine_inner_x, p.inner_body_half)),
        p.spine_local_y,
        (
            z_center - p.male_rail_width_z / 2,
            z_center + p.male_rail_width_z / 2,
        ),
    )


def make_solid_keyboard_button(
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Part:
    button = _rounded_prism_xz(
        p.inner_body_size_xz,
        p.inner_body_local_y,
        p.inner_body_corner_radius_xz,
    )
    keycap = loft(
        [
            _rounded_section_xz(
                p.key_skirt_size_xz,
                p.key_skirt_corner_radius_xz,
                p.key_local_y[0],
            ),
            _rounded_section_xz(
                p.key_face_size_xz,
                p.key_face_corner_radius_xz,
                p.key_local_y[1],
            ),
        ]
    )
    button = button + keycap
    for side in (-1.0, 1.0):
        for z_center in p.male_rail_centres_z:
            button = button + _male_rail(side, z_center, p)
            button = button + _rail_spine(side, z_center, p)
    button = button.clean()
    button.label = "p0_mechanical_fit_v2_solid_keyboard_button_four_continuous_male_rails"
    return button


def _side_latch_root_local(p: P0MechanicalFitV2Spec) -> Part:
    radius = p.side_latch_root_radius
    overlap = p.side_latch_root_overlap
    tangent_y = p.side_latch_root_tangent_local_y
    arc_midpoint = (
        -radius + radius / math.sqrt(2),
        tangent_y - radius / math.sqrt(2),
    )
    with BuildLine(Plane.XY) as outline:
        from build123d import Line

        Line((-radius, -overlap), (overlap, -overlap))
        Line((overlap, -overlap), (overlap, tangent_y))
        Line((overlap, tangent_y), (0.0, tangent_y))
        ThreePointArc((0.0, tangent_y), arc_midpoint, (-radius, 0.0))
        Line((-radius, 0.0), (-radius, -overlap))
    concave = extrude(make_face(outline.line), p.side_latch_width_z).moved(
        Location((0.0, 0.0, -p.side_latch_width_z / 2))
    )
    mandatory_overlap = _box_bounds(
        (0.0, p.side_latch_beam_thickness_x),
        (-p.side_latch_root_faceplate_overlap_y, p.side_latch_root_tangent_local_y),
        (-p.side_latch_width_z / 2, p.side_latch_width_z / 2),
    )
    return (concave + mandatory_overlap).clean()


def _side_latch_transform(side: float, p: P0MechanicalFitV2Spec) -> Matrix:
    return Matrix(
        [
            [side, 0.0, 0.0, side * p.side_latch_beam_inner_x],
            [0.0, 1.0, 0.0, p.rear_faceplate_interior_y],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


def make_side_latch_arm(
    side: float,
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Part:
    beam = _box_bounds(
        _side_bounds(
            side,
            (
                p.side_latch_beam_inner_x,
                p.side_latch_beam_inner_x + p.side_latch_beam_thickness_x,
            ),
        ),
        p.side_latch_beam_y,
        (-p.side_latch_width_z / 2, p.side_latch_width_z / 2),
    )
    hook = make_side_latch_hook(side, p)
    connector_pad = make_side_latch_connector_pad(side, p)
    root = _side_latch_root_local(p).transform_geometry(_side_latch_transform(side, p))
    arm = (beam + hook + root + connector_pad).clean()
    arm.label = f"C5_V2_side_latch_{'positive_X' if side > 0 else 'negative_X'}"
    return arm


def make_side_latch_hook(
    side: float,
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Part:
    with BuildSketch(Plane.XY) as hook_profile:
        Polygon(
            (0.80, p.side_latch_hook_base_local_y[0]),
            (
                p.side_latch_hook_shoulder_inner_x - p.side_latch_beam_inner_x,
                p.side_latch_hook_shoulder_local_y,
            ),
            (
                p.side_latch_hook_apex_x - p.side_latch_beam_inner_x,
                p.side_latch_hook_shoulder_local_y,
            ),
            (
                p.side_latch_hook_apex_x - p.side_latch_beam_inner_x,
                p.side_latch_hook_apex_local_y,
            ),
            (0.80, p.side_latch_hook_base_local_y[1]),
        )
    hook_local = extrude(hook_profile.sketch, p.side_latch_width_z).moved(
        Location((0.0, 0.0, -p.side_latch_width_z / 2))
    )
    hook = hook_local.transform_geometry(_side_latch_transform(side, p))
    hook.label = f"C5_V2_side_latch_hook_{'positive_X' if side > 0 else 'negative_X'}"
    return hook


def make_side_latch_connector_pad(
    side: float,
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Part:
    connector = _box_bounds(
        _side_bounds(side, p.side_latch_connector_x),
        p.side_latch_pad_y,
        (-p.side_latch_connector_width_z / 2, p.side_latch_connector_width_z / 2),
    )
    pad = _box_bounds(
        _side_bounds(
            side,
            (
                p.side_latch_pad_inner_x,
                p.side_latch_pad_inner_x + p.side_latch_pad_thickness_x,
            ),
        ),
        p.side_latch_pad_y,
        (-p.side_latch_pad_width_z / 2, p.side_latch_pad_width_z / 2),
    )
    connector_pad = (connector + pad).clean()
    connector_pad.label = f"C5_V2_side_latch_connector_pad_{'positive_X' if side > 0 else 'negative_X'}"
    return connector_pad


def _root_relief(
    side: float,
    p: P0MechanicalFitV2Spec,
) -> Part:
    return _box_bounds(
        _side_bounds(
            side,
            (
                p.side_latch_beam_inner_x - p.side_latch_root_radius - 0.01,
                p.side_latch_beam_inner_x + p.side_latch_root_overlap + 0.01,
            ),
        ),
        (
            p.rear_faceplate_interior_y - 0.01,
            p.rear_faceplate_interior_y
            + p.side_latch_root_tangent_local_y
            + 0.01,
        ),
        (-p.side_latch_width_z / 2 - 0.01, p.side_latch_width_z / 2 + 0.01),
    )


def make_blind_two_side_latch_rear_cover(
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Part:
    cover = make_rear_cover_core(p)
    for side in (-1.0, 1.0):
        cover = cover + make_side_latch_arm(side, p)
    cover = cover.clean()
    cover.label = "p0_mechanical_fit_v2_blind_rear_cover_exactly_two_side_squeeze_latches"
    return cover


def make_rear_cover_core(
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Part:
    cover = _rounded_prism_xz(
        p.housing_size,
        (p.rear_faceplate_exterior_y, p.rear_faceplate_interior_y),
        p.housing_outer_corner_radius_xz,
    )
    cover = cover + _rounded_prism_xz(
        p.rear_pilot_size_xz,
        (p.rear_faceplate_interior_y, p.rear_pilot_front_y),
        p.rear_pilot_corner_radius_xz,
    )
    for side in (-1.0, 1.0):
        cover = cover - _root_relief(side, p)
    cover = cover.clean()
    cover.label = "p0_mechanical_fit_v2_blind_rear_cover_core"
    return cover


def make_deflected_side_latch_arm(
    side: float,
    deflection: float,
    p: P0MechanicalFitV2Spec = P0_MECHANICAL_FIT_V2,
) -> Part:
    if not 0.0 <= deflection <= p.predicted_hook_stop_travel:
        raise ValueError("side-latch deflection exceeds the pad-stop hook envelope")
    arm = Location((-side * deflection, 0.0, 0.0)) * make_side_latch_arm(side, p)
    arm.label = f"C5_V2_side_latch_deflected_{deflection:.2f}"
    return arm


__all__ = [
    "make_blind_two_side_latch_rear_cover",
    "make_outer_housing",
    "make_deflected_side_latch_arm",
    "make_rear_cover_core",
    "make_side_latch_connector_pad",
    "make_side_latch_hook",
    "make_side_latch_arm",
    "make_solid_keyboard_button",
]
