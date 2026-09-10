"""V2.1 keyboard-identity inner geometry; V2 housing and lock remain frozen."""

from build123d import Location, Part, Sphere, loft

from pill_click.p0_mechanical_fit_v2_keyboard_inverted_rails.geometry import (
    _male_rail,
    _rail_spine,
    _rounded_prism_xz,
    _rounded_section_xz,
    make_blind_two_side_latch_rear_cover as _make_v2_rear_cover,
    make_outer_housing as _make_v2_outer_housing,
)

from .spec import P0_MECHANICAL_FIT_V21, P0MechanicalFitV21Spec


def make_outer_housing(
    p: P0MechanicalFitV21Spec = P0_MECHANICAL_FIT_V21,
) -> Part:
    return _make_v2_outer_housing(p)


def make_blind_two_side_latch_rear_cover(
    p: P0MechanicalFitV21Spec = P0_MECHANICAL_FIT_V21,
) -> Part:
    return _make_v2_rear_cover(p)


def make_keyboard_identity_keycap(
    p: P0MechanicalFitV21Spec = P0_MECHANICAL_FIT_V21,
) -> Part:
    outer = loft(
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
    keycap.label = "p0_mechanical_fit_v21_tall_tapered_spherical_dish_keycap"
    return keycap


def make_keyboard_identity_button(
    p: P0MechanicalFitV21Spec = P0_MECHANICAL_FIT_V21,
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
    button.label = "p0_mechanical_fit_v21_keyboard_identity_button_v2_rails"
    return button


__all__ = [
    "make_blind_two_side_latch_rear_cover",
    "make_keyboard_identity_button",
    "make_keyboard_identity_keycap",
    "make_outer_housing",
]
