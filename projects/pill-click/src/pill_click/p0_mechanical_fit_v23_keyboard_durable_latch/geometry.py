"""V2.3 geometry: one-piece keycap loft and durable planar rear latches."""

from build123d import BuildSketch, Location, Matrix, Part, Plane, Polygon, Sphere, extrude, loft

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

from .spec import P0_MECHANICAL_FIT_V23, P0MechanicalFitV23Spec


def make_keyboard_keycap(
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Part:
    """Single monotonic loft from hidden 34.2 mm seam to 27.5 mm top."""
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
    if p.key_face_dish_depth_y > 0.0:
        sphere_radius = p.key_face_dish_sphere_radius
        sphere_center_y = p.key_local_y[1] + sphere_radius - p.key_face_dish_depth_y
        dish = Sphere(sphere_radius).moved(Location((0.0, sphere_center_y, 0.0)))
        keycap = (outer - dish).clean()
        face_style = "dished"
    else:
        keycap = outer.clean()
        face_style = "flat"
    keycap.label = f"p0_mechanical_fit_v23_single_loft_{face_style}_keyboard_keycap"
    return keycap


def make_keyboard_button(
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Part:
    button = _rounded_prism_xz(
        p.inner_body_size_xz,
        p.inner_body_local_y,
        p.inner_body_corner_radius_xz,
    )
    button = button + make_keyboard_keycap(p)
    # Accepted V2 rail/spine cross-sections and front endpoints are reused. The
    # rear endpoints extend to the cover bosses for the named inward stop.
    for side in (-1.0, 1.0):
        for z_center in p.male_rail_centres_z:
            button = button + _male_rail(side, z_center, p)
            button = button + _rail_spine(side, z_center, p)
    button = button.clean()
    button.label = "p0_mechanical_fit_v23_keyboard_button_accepted_v2_rails"
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
        center=(sum(x_bounds) / 2, sum(y_bounds) / 2, sum(z_bounds) / 2),
    )


def _cut_planar_latch_receivers(body: Part, p: P0MechanicalFitV23Spec) -> Part:
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
        # The forward hook flank slopes back into the tower after its plateau.
        # This relief begins only after the specified 0.20 mm pocket clearance,
        # so the rear pocket shoulder remains the actual retaining surface.
        body = body - _box_bounds(
            _side_bounds(side, p.planar_latch_front_ramp_relief_x),
            p.planar_latch_front_ramp_relief_y,
            p.planar_latch_receiver_z,
        )
    return body


def make_outer_housing(
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Part:
    body = _outer_keyboard_shell(p)
    body = body - _rounded_prism_xz(
        p.main_guide_size_xz,
        (
            p.housing_rear_y - p.housing_guide_boolean_overshoot_y,
            p.front_guide_rear_y,
        ),
        p.main_guide_corner_radius_xz,
    )
    body = body - _rounded_prism_xz(
        p.front_guide_size_xz,
        (
            p.front_guide_rear_y,
            p.housing_front_y + p.housing_guide_boolean_overshoot_y,
        ),
        p.front_guide_corner_radius_xz,
    )
    for side in (-1.0, 1.0):
        channel_x = _side_bounds(side, p.female_channel_x)
        mouth_x = _side_bounds(side, p.female_mouth_x)
        for z_center in p.male_rail_centres_z:
            body = body - _box_bounds(
                channel_x,
                (
                    p.female_channel_rear_y - p.female_channel_boolean_overshoot_y,
                    p.female_channel_blind_front_y,
                ),
                (
                    z_center - p.female_channel_width_z / 2,
                    z_center + p.female_channel_width_z / 2,
                ),
            )
            body = body - _box_bounds(
                mouth_x,
                (
                    p.female_channel_rear_y - p.female_channel_boolean_overshoot_y,
                    p.female_channel_rear_y + p.female_mouth_length_y,
                ),
                (
                    z_center
                    - (p.female_channel_width_z + p.female_mouth_extra_width_z) / 2,
                    z_center
                    + (p.female_channel_width_z + p.female_mouth_extra_width_z) / 2,
                ),
            )
    housing = _cut_planar_latch_receivers(body, p).clean()
    housing.label = "p0_mechanical_fit_v23_outer_accepted_rails_durable_receivers"
    return housing


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
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Part:
    """Full-height retaining tooth with a six-layer axial plateau."""
    with BuildSketch(Plane.XY) as profile:
        Polygon(
            (p.planar_latch_hook_rear_base_x, p.planar_latch_hook_rear_base_y),
            (p.planar_latch_hook_shoulder_inner_x, p.planar_latch_hook_shoulder_y),
            (p.planar_latch_hook_apex_x, p.planar_latch_hook_shoulder_y),
            (p.planar_latch_hook_apex_x, p.planar_latch_hook_apex_front_y),
            (p.planar_latch_hook_front_inner_x, p.planar_latch_hook_front_base_y),
            (p.planar_latch_hook_front_base_x, p.planar_latch_hook_front_base_y),
        )
    hook = extrude(profile.sketch, p.planar_latch_tower_width_z).moved(
        Location((0.0, 0.0, p.planar_latch_tower_z[0]))
    )
    if side < 0:
        hook = hook.transform_geometry(_mirror_x(side))
    hook.label = f"v23_durable_hook_{'positive_x' if side > 0 else 'negative_x'}"
    return hook


def make_planar_latch_lock(
    side: float,
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Part:
    tower = _box_bounds(
        _side_bounds(side, p.planar_latch_tower_x),
        p.planar_latch_tower_y,
        p.planar_latch_tower_z,
    )
    lock = (tower + make_planar_latch_hook(side, p)).clean()
    lock.label = f"v23_durable_lock_{'positive_x' if side > 0 else 'negative_x'}"
    return lock


def make_deflected_planar_latch_lock(
    side: float,
    travel: float,
    axial_offset_y: float = 0.0,
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Part:
    if side not in (-1.0, 1.0):
        raise ValueError("side must be -1.0 or +1.0")
    if not 0.0 <= travel <= p.planar_latch_hard_stop_travel_x:
        raise ValueError("travel is outside the physical latch-stop range")
    moved = Location((-side * travel, axial_offset_y, 0.0)) * make_planar_latch_lock(side, p)
    moved.label = f"v23_durable_lock_deflected_{travel:.2f}"
    return moved


def make_planar_latch_stop(
    side: float,
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Part:
    """Continuous full-height inboard rail carrying the squeeze stop face."""
    stop = _box_bounds(
        _side_bounds(side, p.planar_latch_stop_rail_x),
        (p.rear_faceplate_exterior_y, p.rear_faceplate_interior_y),
        p.planar_latch_inner_slot_z,
    )
    stop.label = f"v23_physical_stop_{'positive_x' if side > 0 else 'negative_x'}"
    return stop


def _planar_latch_extension(side: float, p: P0MechanicalFitV23Spec) -> Part:
    extension = make_planar_latch_lock(side, p)
    if p.planar_latch_paddle_x[1] > p.half_housing:
        paddle = _box_bounds(
            _side_bounds(side, (p.half_housing, p.planar_latch_paddle_x[1])),
            (p.rear_faceplate_exterior_y, p.rear_faceplate_interior_y),
            p.planar_latch_paddle_z,
        )
        extension = paddle + extension
    return extension.clean()


def make_rear_rail_stop_bosses(
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Part:
    """Four cover-mounted bosses aligned with the external rail bands."""
    bosses = None
    for side in (-1.0, 1.0):
        for z_center in p.male_rail_centres_z:
            boss = _box_bounds(
                _side_bounds(side, p.rear_stop_boss_x),
                p.rear_stop_boss_y,
                (
                    z_center - p.male_rail_width_z / 2,
                    z_center + p.male_rail_width_z / 2,
                ),
            )
            bosses = boss if bosses is None else bosses + boss
    if bosses is None:  # pragma: no cover - the frozen rail contract has four bosses
        raise ValueError("rear stop boss pattern is empty")
    bosses = bosses.clean()
    bosses.label = "p0_mechanical_fit_v23_four_rear_rail_stop_bosses"
    return bosses


def make_planar_latch_rear_cover(
    p: P0MechanicalFitV23Spec = P0_MECHANICAL_FIT_V23,
) -> Part:
    cover = _rounded_prism_xz(
        p.housing_size,
        (p.rear_faceplate_exterior_y, p.rear_faceplate_interior_y),
        p.housing_outer_corner_radius_xz,
    )
    straight_pilot = _rounded_prism_xz(
        p.rear_pilot_size_xz,
        (p.rear_faceplate_interior_y, p.rear_pilot_entry_chamfer_rear_y),
        p.rear_pilot_corner_radius_xz,
    )
    pilot_entry = loft(
        [
            _rounded_section_xz(
                p.rear_pilot_size_xz,
                p.rear_pilot_corner_radius_xz,
                p.rear_pilot_entry_chamfer_rear_y,
            ),
            _rounded_section_xz(
                p.rear_pilot_tip_size_xz,
                p.rear_pilot_tip_corner_radius_xz,
                p.rear_pilot_front_y,
            ),
        ]
    )
    cover = cover + straight_pilot + pilot_entry
    through_y = (
        p.rear_faceplate_exterior_y - p.rear_cover_boolean_overshoot_y,
        p.rear_faceplate_interior_y + p.rear_cover_boolean_overshoot_y,
    )
    pilot_y = (
        p.rear_faceplate_interior_y - p.rear_cover_boolean_overshoot_y,
        p.rear_pilot_front_y + p.rear_cover_boolean_overshoot_y,
    )
    for side in (-1.0, 1.0):
        # One overlapping rounded opening preserves the requested round slot
        # caps.  Both branch cuts begin at the stop surface, so their union has
        # no small shelves or scalloped remnants beside the full-height rail.
        side_slot = _rounded_cut_xz(
            _side_bounds(side, p.planar_latch_inner_slot_x),
            through_y,
            p.planar_latch_inner_slot_z,
            p.planar_latch_slot_corner_radius,
        )
        branch_x = (
            p.planar_latch_outer_slot_x[0] - p.planar_latch_slot_overlap_x,
            p.planar_latch_outer_slot_x[1],
        )
        for z_bounds in (
            p.planar_latch_upper_outer_slot_z,
            p.planar_latch_lower_outer_slot_z,
        ):
            side_slot = side_slot + _rounded_cut_xz(
                _side_bounds(side, branch_x),
                through_y,
                z_bounds,
                p.planar_latch_slot_corner_radius,
            )
        cover = cover - side_slot.clean()
        cover = cover - _box_bounds(
            _side_bounds(side, p.planar_latch_pilot_relief_x),
            pilot_y,
            p.planar_latch_pilot_relief_z,
        )
        cover = cover + make_planar_latch_stop(side, p)
        cover = cover + _planar_latch_extension(side, p)
    cover = cover + make_rear_rail_stop_bosses(p)
    cover = cover.clean()
    cover.label = "p0_mechanical_fit_v23_rear_cover_pilot_stops_flush_side_latches"
    return cover


__all__ = [
    "make_keyboard_button",
    "make_keyboard_keycap",
    "make_outer_housing",
    "make_deflected_planar_latch_lock",
    "make_planar_latch_hook",
    "make_planar_latch_lock",
    "make_planar_latch_rear_cover",
    "make_planar_latch_stop",
    "make_rear_rail_stop_bosses",
]
