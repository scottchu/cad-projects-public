"""V2.2 geometry with rear-cover-plane dual-beam side latches."""

from build123d import (
    BuildSketch,
    Location,
    Matrix,
    Part,
    Plane,
    Polygon,
    Sphere,
    extrude,
    loft,
)

from pill_click.geometry import rounded_box
from pill_click.p0_mechanical_fit_v2_keyboard_inverted_rails.geometry import (
    _box_bounds,
    _male_rail,
    _outer_keyboard_shell,
    _rail_spine,
    _rounded_prism_xz,
    _rounded_section_xz,
    _side_bounds,
)

from .spec import P0_MECHANICAL_FIT_V22, P0MechanicalFitV22Spec


def make_keyboard_identity_keycap(
    p: P0MechanicalFitV22Spec = P0_MECHANICAL_FIT_V22,
) -> Part:
    """Wide-base mechanical key with a short printable flare transition."""
    flare = loft(
        [
            _rounded_section_xz(
                p.inner_body_size_xz,
                p.inner_body_corner_radius_xz,
                p.key_local_y[0],
            ),
            _rounded_section_xz(
                p.key_skirt_size_xz,
                p.key_skirt_corner_radius_xz,
                p.key_flare_local_y,
            ),
        ]
    )
    tapered_key = loft(
        [
            _rounded_section_xz(
                p.key_skirt_size_xz,
                p.key_skirt_corner_radius_xz,
                p.key_flare_local_y,
            ),
            _rounded_section_xz(
                p.key_face_size_xz,
                p.key_face_corner_radius_xz,
                p.key_local_y[1],
            ),
        ]
    )
    outer = (flare + tapered_key).clean()
    face_edges = [
        edge
        for edge in outer.edges()
        if abs(edge.bounding_box().min.Y - p.key_local_y[1]) < 1e-6
        and abs(edge.bounding_box().max.Y - p.key_local_y[1]) < 1e-6
    ]
    outer = outer.fillet(p.key_face_edge_fillet_y, face_edges)
    sphere_radius = p.key_face_dish_sphere_radius
    sphere_center_y = p.key_local_y[1] + sphere_radius - p.key_face_dish_depth_y
    dish_tool = Sphere(sphere_radius).moved(Location((0.0, sphere_center_y, 0.0)))
    keycap = (outer - dish_tool).clean()
    keycap.label = "p0_mechanical_fit_v22_wide_tapered_spherical_dish_keycap"
    return keycap


def make_keyboard_identity_button(
    p: P0MechanicalFitV22Spec = P0_MECHANICAL_FIT_V22,
) -> Part:
    button = _rounded_prism_xz(
        p.inner_body_size_xz,
        p.inner_body_local_y,
        p.inner_body_corner_radius_xz,
    )
    button = button + make_keyboard_identity_keycap(p)
    for side in (-1.0, 1.0):
        for z_center in p.male_rail_centres_z:
            button = button + _male_rail(side, z_center, p)
            button = button + _rail_spine(side, z_center, p)
    button = button.clean()
    button.label = "p0_mechanical_fit_v22_wide_keyboard_button_v2_rails"
    return button


def _rounded_cut_xz(
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
    z_bounds: tuple[float, float],
    radius: float,
) -> Part:
    return rounded_box(
        x_bounds[1] - x_bounds[0],
        y_bounds[1] - y_bounds[0],
        z_bounds[1] - z_bounds[0],
        radius,
        center=(
            sum(x_bounds) / 2,
            sum(y_bounds) / 2,
            sum(z_bounds) / 2,
        ),
    )


def _cut_planar_latch_receivers(
    body: Part,
    p: P0MechanicalFitV22Spec,
) -> Part:
    for side in (-1.0, 1.0):
        body = body - _box_bounds(
            _side_bounds(side, p.planar_latch_broad_notch_x),
            p.planar_latch_broad_notch_y,
            p.planar_latch_receiver_z,
        )
        body = body - _box_bounds(
            _side_bounds(side, p.planar_latch_tower_passage_x),
            p.planar_latch_tower_passage_y,
            p.planar_latch_receiver_z,
        )
        body = body - _box_bounds(
            _side_bounds(side, p.planar_latch_receiver_pocket_x),
            p.planar_latch_receiver_pocket_y,
            p.planar_latch_receiver_z,
        )
    return body


def make_outer_housing(
    p: P0MechanicalFitV22Spec = P0_MECHANICAL_FIT_V22,
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
    body = _cut_planar_latch_receivers(body, p).clean()
    body.label = "p0_mechanical_fit_v22_outer_v2_rails_planar_latch_receivers"
    return body


def _mirror_x(side: float) -> Matrix:
    return Matrix(
        [
            [side, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


def make_planar_latch_hook(
    side: float,
    p: P0MechanicalFitV22Spec = P0_MECHANICAL_FIT_V22,
) -> Part:
    with BuildSketch(Plane.XY) as profile:
        Polygon(
            (p.planar_latch_tower_x[1] - 0.50, p.planar_latch_hook_rear_base_y),
            (p.planar_latch_hook_shoulder_inner_x, p.planar_latch_hook_shoulder_y),
            (p.planar_latch_hook_apex_x, p.planar_latch_hook_shoulder_y),
            (p.planar_latch_hook_apex_x, p.planar_latch_hook_apex_front_y),
            (p.planar_latch_hook_shoulder_inner_x, p.planar_latch_hook_front_base_y),
            (p.planar_latch_tower_x[1] - 0.50, p.planar_latch_hook_front_base_y),
        )
    hook = extrude(profile.sketch, p.planar_latch_tower_width_z).moved(
        Location((0.0, 0.0, p.planar_latch_tower_z[0]))
    )
    if side < 0:
        hook = hook.transform_geometry(_mirror_x(side))
    hook.label = f"v22_planar_latch_hook_{'positive_x' if side > 0 else 'negative_x'}"
    return hook


def make_planar_latch_lock(
    side: float,
    p: P0MechanicalFitV22Spec = P0_MECHANICAL_FIT_V22,
) -> Part:
    """Return the moving tower and hook for collision-path validation."""
    tower = _box_bounds(
        _side_bounds(side, p.planar_latch_tower_x),
        p.planar_latch_tower_y,
        p.planar_latch_tower_z,
    )
    lock = (tower + make_planar_latch_hook(side, p)).clean()
    lock.label = f"v22_planar_latch_lock_{'positive_x' if side > 0 else 'negative_x'}"
    return lock


def make_deflected_planar_latch_lock(
    side: float,
    travel: float,
    axial_offset_y: float = 0.0,
    p: P0MechanicalFitV22Spec = P0_MECHANICAL_FIT_V22,
) -> Part:
    """Rigid-envelope approximation of the lock at an inward squeeze travel."""
    if side not in (-1.0, 1.0):
        raise ValueError("side must be -1.0 or +1.0")
    if not 0.0 <= travel <= p.planar_latch_hard_stop_travel_x:
        raise ValueError("travel is outside the physical latch-stop range")
    moved = Location((-side * travel, axial_offset_y, 0.0)) * make_planar_latch_lock(side, p)
    moved.label = f"v22_planar_latch_lock_deflected_{travel:.2f}"
    return moved


def make_planar_latch_stop(
    side: float,
    p: P0MechanicalFitV22Spec = P0_MECHANICAL_FIT_V22,
) -> Part:
    """Return the fixed faceplate nub that limits inward paddle travel."""
    stop_x = (
        p.planar_latch_inner_slot_x[0] - 0.02,
        p.planar_latch_stop_surface_x,
    )
    stop = _box_bounds(
        _side_bounds(side, stop_x),
        (p.rear_faceplate_exterior_y, p.rear_faceplate_interior_y),
        p.planar_latch_stop_z,
    )
    stop.label = f"v22_planar_latch_stop_{'positive_x' if side > 0 else 'negative_x'}"
    return stop


def _planar_latch_extension(
    side: float,
    p: P0MechanicalFitV22Spec,
) -> Part:
    extension = _box_bounds(
        _side_bounds(side, (p.half_housing, p.planar_latch_paddle_x[1])),
        (p.rear_faceplate_exterior_y, p.rear_faceplate_interior_y),
        p.planar_latch_paddle_z,
    )
    return (extension + make_planar_latch_lock(side, p)).clean()


def make_planar_latch_rear_cover(
    p: P0MechanicalFitV22Spec = P0_MECHANICAL_FIT_V22,
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
    through_y = (p.rear_faceplate_exterior_y - 0.1, p.rear_faceplate_interior_y + 0.1)
    pilot_y = (p.rear_faceplate_interior_y - 0.1, p.rear_pilot_front_y + 0.1)
    for side in (-1.0, 1.0):
        cover = cover - _rounded_cut_xz(
            _side_bounds(side, p.planar_latch_inner_slot_x),
            through_y,
            p.planar_latch_inner_slot_z,
            p.planar_latch_slot_corner_radius,
        )
        for z_bounds in (
            p.planar_latch_upper_outer_slot_z,
            p.planar_latch_lower_outer_slot_z,
        ):
            cover = cover - _rounded_cut_xz(
                _side_bounds(side, p.planar_latch_outer_slot_x),
                through_y,
                z_bounds,
                p.planar_latch_slot_corner_radius,
            )
        cover = cover - _box_bounds(
            _side_bounds(side, p.planar_latch_pilot_relief_x),
            pilot_y,
            p.planar_latch_pilot_relief_z,
        )
        cover = cover + make_planar_latch_stop(side, p)
        cover = cover + _planar_latch_extension(side, p)
    cover = cover.clean()
    cover.label = "p0_mechanical_fit_v22_rear_cover_dual_in_plane_side_paddles"
    return cover


__all__ = [
    "make_keyboard_identity_button",
    "make_keyboard_identity_keycap",
    "make_outer_housing",
    "make_deflected_planar_latch_lock",
    "make_planar_latch_hook",
    "make_planar_latch_lock",
    "make_planar_latch_rear_cover",
    "make_planar_latch_stop",
]
