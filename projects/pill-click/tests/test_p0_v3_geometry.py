"""BREP acceptance tests for the isolated P0 v3 manual slider."""

from dataclasses import replace
from itertools import combinations

import pytest
from build123d import Align, Box, Location, Matrix, Vector

from pill_click.p0_v3 import (
    P0V3,
    make_blind_rear_cover,
    make_bottom_shutter,
    make_c4_snap_arm,
    make_housing,
    make_p0_v3_assembly,
    make_shuttle,
    make_top_shutter,
)
from pill_click.p0_v3.geometry import (
    _box_between_y,
    _make_blind_rear_cover_rootless,
    _rear_land_backing_rib,
    _snap_root_material,
    _snap_root_relief_cutter,
)


BREP_TOLERANCE = 1e-6


def _box(
    size_x: float,
    size_y: float,
    size_z: float,
    center: tuple[float, float, float],
):
    return Box(
        size_x,
        size_y,
        size_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location(center))


def _intersection_volume(first, second) -> float:
    return (first & second).volume


def _bbox_tuple(shape) -> tuple[float, float, float, float, float, float]:
    bbox = shape.bounding_box()
    return (
        bbox.min.X,
        bbox.max.X,
        bbox.min.Y,
        bbox.max.Y,
        bbox.min.Z,
        bbox.max.Z,
    )


@pytest.fixture(scope="module")
def fixed_parts():
    return make_housing(), make_blind_rear_cover()


@pytest.fixture(scope="module")
def moving_parts():
    return make_shuttle(), make_top_shutter(), make_bottom_shutter()


def test_v3_principal_parts_are_valid_single_solids(fixed_parts, moving_parts) -> None:
    parts = [*fixed_parts, *moving_parts]
    assert all(part.is_valid and part.volume > 0.0 for part in parts)
    assert all(len(part.solids()) == 1 for part in parts)


def test_c1r1_backing_ribs_have_exact_bboxes_and_finite_overlaps() -> None:
    p = P0V3
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
    body = outer - inner
    boss_depth = p.groove_bottom_x + p.groove_radial_depth - p.shuttle_width / 2

    for side in (-1.0, 1.0):
        for z_center in (-p.rail_z_offset, p.rail_z_offset):
            rib = _rear_land_backing_rib(side, z_center, p)
            boss = _box(
                boss_depth,
                p.land_length,
                p.bearing_boss_width,
                (
                    side * (p.shuttle_width / 2 + boss_depth / 2),
                    p.rear_land_local_y,
                    z_center,
                ),
            )
            expected_x = (16.45, 17.25) if side > 0 else (-17.25, -16.45)
            assert _bbox_tuple(rib) == pytest.approx(
                (expected_x[0], expected_x[1], -17.20, -12.80, z_center - 2.15, z_center + 2.15)
            )
            assert _intersection_volume(rib, body) == pytest.approx(0.559000, abs=1e-9)
            assert _intersection_volume(rib, boss) == pytest.approx(2.838000, abs=1e-9)


def test_c1r1_change_is_localized_to_land_and_backing_envelopes() -> None:
    old = replace(
        P0V3,
        land_length=3.4,
        bearing_boss_width=3.5,
        rear_land_local_y=-12.1,
        front_land_local_y=-4.9,
        rear_land_backing_radial_thickness=0.0,
        rear_land_backing_body_overlap_y=0.0,
    )
    old_shuttle = make_shuttle(old)
    new_shuttle = make_shuttle(P0V3)
    changed = (old_shuttle - new_shuttle) + (new_shuttle - old_shuttle)
    keepout = None
    for side in (-1.0, 1.0):
        for z_center in (-P0V3.rail_z_offset, P0V3.rail_z_offset):
            region = _box(
                2.0,
                14.2,
                5.3,
                (side * 17.0, -10.1, z_center),
            )
            keepout = region if keepout is None else keepout + region
    assert changed.volume > 0.0
    assert (changed - keepout).volume < BREP_TOLERANCE


def test_all_four_snap_root_sections_equal_rigidly_mapped_c4_brep() -> None:
    """Prove the cover has the C4 R0.80 root, not pilot-embedded beams."""

    p = P0V3
    cover = make_blind_rear_cover(p)
    c4_arm = make_c4_snap_arm(p)
    root_local_y = (-0.19, 0.79)
    root_local_x = (-0.79, 0.19)

    for x_center in (-p.rear_snap_center_x, p.rear_snap_center_x):
        for top in (True, False):
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
            mapped_c4 = c4_arm.transform_geometry(transform)
            world_z = sorted(
                (
                    beam_inner_z + radial_sign * root_local_x[0],
                    beam_inner_z + radial_sign * root_local_x[1],
                )
            )
            crop = _box(
                p.rear_snap_width - 0.02,
                root_local_y[1] - root_local_y[0],
                world_z[1] - world_z[0],
                (
                    x_center,
                    p.rear_faceplate_interior_y + sum(root_local_y) / 2,
                    sum(world_z) / 2,
                ),
            )
            actual_root = cover & crop
            expected_root = mapped_c4 & crop

            # Symmetric BREP difference checks the exact R0.80 curve and both
            # finite overlap regions, rather than merely repeating scalars.
            assert actual_root.volume > 0.0
            assert actual_root.volume == pytest.approx(expected_root.volume)
            assert (actual_root - expected_root).volume < BREP_TOLERANCE
            assert (expected_root - actual_root).volume < BREP_TOLERANCE


def test_v31_cover_root_accounting_and_relief_cutters_preserve_hidden_overlap() -> None:
    p = P0V3
    rootless = _make_blind_rear_cover_rootless(p)
    cover = make_blind_rear_cover(p)
    expected_four_root_addition = 4 * 0.494442631532279

    assert rootless.is_valid and cover.is_valid
    assert len(rootless.solids()) == len(cover.solids()) == 1
    assert rootless.volume == pytest.approx(4227.880800000004, abs=1e-9)
    assert cover.volume == pytest.approx(4229.858570536589, abs=1e-9)
    assert cover.volume - rootless.volume == pytest.approx(
        expected_four_root_addition, abs=1e-6
    )
    assert cover.volume - 4230.288099348127 == pytest.approx(
        -0.429528811538, abs=1e-9
    )

    for x_center in (-p.rear_snap_center_x, p.rear_snap_center_x):
        for top in (True, False):
            root = _snap_root_material(x_center, top=top, p=p)
            cutter = _snap_root_relief_cutter(x_center, top=top, p=p)
            hidden_overlap = root & _box(
                p.rear_snap_width,
                p.rear_snap_root_overlap,
                p.rear_snap_root_fillet + p.rear_snap_root_overlap,
                (
                    x_center,
                    p.rear_faceplate_interior_y - p.rear_snap_root_overlap / 2,
                    16.65 if top else -16.65,
                ),
            )
            assert hidden_overlap.volume == pytest.approx(0.720000, abs=1e-6)
            assert _intersection_volume(cutter, hidden_overlap) < BREP_TOLERANCE
            cutter_bbox = cutter.bounding_box()
            assert cutter_bbox.min.Y == pytest.approx(-18.70)
            assert cutter_bbox.max.Y == pytest.approx(-17.09)


def test_v3_assemblies_have_only_the_five_frozen_parts() -> None:
    expected_fragments = {
        "fixed_housing",
        "full_blind_faceplate",
        "shuttle",
        "top_shutter",
        "bottom_shutter",
    }
    forbidden = ("spring", "magnet", "cam", "follower", "gate", "plunger")
    for state in (P0V3.pressed_state, P0V3.released_state):
        assembly = make_p0_v3_assembly(state)
        labels = {child.label for child in assembly.children}
        assert assembly.is_valid
        assert len(labels) == 5
        assert all(any(fragment in label for label in labels) for fragment in expected_fragments)
        assert not any(token in label for token in forbidden for label in labels)


def test_fixed_envelopes_and_blind_face_are_actual_brep_facts(fixed_parts) -> None:
    p = P0V3
    housing, cover = fixed_parts
    housing_bbox = _bbox_tuple(housing)
    cover_bbox = _bbox_tuple(cover)
    assert housing_bbox == pytest.approx(
        (-p.housing_half, p.housing_half, p.housing_fixed_rear_y, p.housing_half, -p.housing_half, p.housing_half)
    )
    assert cover_bbox[0:2] == pytest.approx((-p.housing_half, p.housing_half))
    assert cover_bbox[2] == pytest.approx(p.rear_faceplate_exterior_y)
    assert cover_bbox[4:6] == pytest.approx((-p.housing_half, p.housing_half))
    assert _intersection_volume(housing, cover) < BREP_TOLERANCE


def test_actual_web_flange_shroud_faceplate_and_stop_thicknesses(
    fixed_parts, moving_parts
) -> None:
    p = P0V3
    housing, cover = fixed_parts
    _, top, bottom = moving_parts

    # The flange and web fuse at a shared face. Measure the flange-only edge
    # section, then subtract it from the adjacent combined section to recover
    # both real BREP thicknesses without trusting source parameters alone.
    top_combined = top & _box(0.1, 2.0, 2.0, (12.40, -16.0, 19.0))
    top_flange = top & _box(0.1, 2.0, 2.0, (12.60, -16.0, 19.0))
    bottom_combined = bottom & _box(0.1, 2.0, 2.0, (12.40, -16.0, -19.0))
    bottom_flange = bottom & _box(0.1, 2.0, 2.0, (12.60, -16.0, -19.0))
    assert top_flange.bounding_box().size.Z == pytest.approx(p.shutter_flange_thickness)
    assert bottom_flange.bounding_box().size.Z == pytest.approx(p.shutter_flange_thickness)
    assert top_combined.bounding_box().size.Z - top_flange.bounding_box().size.Z == pytest.approx(
        p.shutter_web_thickness
    )
    assert bottom_combined.bounding_box().size.Z - bottom_flange.bounding_box().size.Z == pytest.approx(
        p.shutter_web_thickness
    )

    top_shroud = housing & _box(20.0, 2.0, 2.0, (0.0, 12.0, 19.4))
    bottom_shroud = housing & _box(20.0, 2.0, 2.0, (0.0, 17.0, -19.4))
    assert top_shroud.bounding_box().size.Z == pytest.approx(p.opaque_shroud_thickness)
    assert bottom_shroud.bounding_box().size.Z == pytest.approx(p.opaque_shroud_thickness)

    faceplate_skin = cover & _box(0.4, 2.0, 0.4, (19.0, -19.35, 0.0))
    assert faceplate_skin.bounding_box().size.Y == pytest.approx(p.rear_faceplate_thickness)
    for x_center in (-p.shutter_stop_nib_center_x, p.shutter_stop_nib_center_x):
        for z_center in (-18.6, 18.6):
            nib = cover & _box(1.0, 0.4, 1.0, (x_center, -18.50, z_center))
            nib_bbox = nib.bounding_box()
            assert nib_bbox.size.Y == pytest.approx(
                p.shutter_stop_nib_front_y - p.shutter_stop_nib_rear_y
            )
            assert nib_bbox.size.Z == pytest.approx(p.shutter_stop_nib_thickness_z)


def test_dense_point_one_operational_and_lost_motion_sweeps_are_collision_free(
    fixed_parts, moving_parts
) -> None:
    p = P0V3
    housing, cover = fixed_parts
    shuttle, top, bottom = moving_parts
    states = [round(p.shuttle_inward_state + 0.05 * index, 2) for index in range(292)]
    states.append(p.maximum_pull_state)
    assert states[0] == pytest.approx(p.shuttle_inward_state)
    assert len(states) == 293
    assert states[-2] == pytest.approx(13.55)
    assert states[-1] == pytest.approx(p.maximum_pull_state)

    for state in states:
        q = p.shutter_q(state)
        moving = [
            Location((0.0, p.shuttle_center_y(state), 0.0)) * shuttle,
            Location((0.0, p.latched_center_y + q, 0.0)) * top,
            Location((0.0, p.latched_center_y + q, 0.0)) * bottom,
        ]
        assert p.relative_lost_motion(state) == pytest.approx(
            state if state < 0.0 else 0.0
        )
        for part in moving:
            assert _intersection_volume(housing, part) < BREP_TOLERANCE
            assert _intersection_volume(cover, part) < BREP_TOLERANCE
        for first, second in combinations(moving, 2):
            assert _intersection_volume(first, second) < BREP_TOLERANCE


def test_all_390_rear_feed_stack_states_clear_fixed_housing(
    fixed_parts, moving_parts
) -> None:
    p = P0V3
    housing, _ = fixed_parts
    shuttle, top, bottom = moving_parts
    states = p.feed_states()
    assert len(states) == p.feed_sample_count == 390
    assert states[0] == pytest.approx(p.feed_start_center_y)
    assert states[-1] == pytest.approx(p.feed_end_center_y)

    for center_y in states:
        translation = Location((0.0, center_y, 0.0))
        for part in (shuttle, top, bottom):
            assert _intersection_volume(housing, translation * part) < BREP_TOLERANCE
        assert (center_y + p.top_lug_local_y[0], center_y + p.top_lug_local_y[1]) == pytest.approx(
            (center_y - 20.6, center_y - 19.4)
        )
        assert (center_y + p.bottom_socket_local_y[0], center_y + p.bottom_socket_local_y[1]) == pytest.approx(
            (center_y - 14.7, center_y - 12.3)
        )


def test_pressed_dense_full_footprint_normal_rays_reach_medicine_cavity() -> None:
    """A full-footprint BREP prism is stronger than discrete ray samples."""

    p = P0V3
    parts = make_p0_v3_assembly(p.pressed_state).children
    ray_prisms = (
        _box(
            p.fixed_fill_width,
            p.fixed_fill_length,
            4.6,
            (0.0, p.fixed_fill_center_y, 17.5),
        ),
        _box(
            p.fixed_outlet_width,
            p.fixed_outlet_length,
            4.6,
            (0.0, p.fixed_outlet_center_y, -17.5),
        ),
    )
    for ray_prism in ray_prisms:
        assert all(_intersection_volume(part, ray_prism) < BREP_TOLERANCE for part in parts)


def test_coupling_keepouts_remain_disjoint_from_moving_apertures_for_full_stroke() -> None:
    p = P0V3
    shuttle = make_shuttle()
    top_local_prism = _box(
        p.moving_fill_width,
        p.moving_fill_length,
        4.6,
        (0.0, p.moving_fill_local_center_y, 17.5),
    )
    bottom_local_prism = _box(
        p.moving_outlet_width,
        p.moving_outlet_length,
        4.6,
        (0.0, p.moving_outlet_local_center_y, -17.5),
    )
    # Translating both the shuttle and its aperture frame by the same coupled
    # state preserves the measured 1.60/0.90 Y separation exactly.
    assert _intersection_volume(shuttle, top_local_prism) < BREP_TOLERANCE
    assert _intersection_volume(shuttle, bottom_local_prism) < BREP_TOLERANCE
    for state in [0.1 * index for index in range(135)]:
        # Both shapes receive the same rigid translation, so the local BREP
        # result above is invariant.  The named equations independently prove
        # the accepted separating-axis margins at every sampled state.
        assert p.moving_fill_interval(state)[0] - (
            p.shuttle_center_y(state) + p.top_complete_coupling_local_y[1]
        ) == pytest.approx(p.top_coupling_aperture_y_clearance)
        assert p.moving_outlet_interval(state)[0] - (
            p.shuttle_center_y(state) + p.bottom_complete_coupling_local_y[1]
        ) == pytest.approx(p.bottom_coupling_aperture_y_clearance)


def test_released_fixed_ports_first_hit_solid_shutters() -> None:
    p = P0V3
    q = p.shutter_q(p.released_state)
    top = Location((0.0, p.latched_center_y + q, 0.0)) * make_top_shutter()
    bottom = Location((0.0, p.latched_center_y + q, 0.0)) * make_bottom_shutter()
    top_probe = _box(
        p.fixed_fill_width - 0.02,
        p.fixed_fill_length - 0.02,
        0.6,
        (0.0, p.fixed_fill_center_y, 19.5),
    )
    bottom_probe = _box(
        p.fixed_outlet_width - 0.02,
        p.fixed_outlet_length - 0.02,
        0.6,
        (0.0, p.fixed_outlet_center_y, -19.5),
    )
    assert _intersection_volume(top, top_probe) == pytest.approx(top_probe.volume, rel=1e-6)
    assert _intersection_volume(bottom, bottom_probe) == pytest.approx(bottom_probe.volume, rel=1e-6)


def test_released_translated_openings_first_hit_opaque_shrouds(fixed_parts) -> None:
    p = P0V3
    housing, _ = fixed_parts
    top_interval = p.moving_fill_interval(p.released_state)
    bottom_interval = p.moving_outlet_interval(p.released_state)
    top_probe = _box(
        p.moving_fill_width - 0.02,
        p.moving_fill_length - 0.02,
        0.6,
        (0.0, sum(top_interval) / 2, 19.5),
    )
    bottom_probe = _box(
        p.moving_outlet_width - 0.02,
        p.moving_outlet_length - 0.02,
        0.6,
        (0.0, sum(bottom_interval) / 2, -19.5),
    )
    assert _intersection_volume(housing, top_probe) == pytest.approx(top_probe.volume, rel=1e-6)
    assert _intersection_volume(housing, bottom_probe) == pytest.approx(bottom_probe.volume, rel=1e-6)

    top_behind_shroud = _box(
        p.moving_fill_width - 0.02,
        p.moving_fill_length - 0.02,
        0.4,
        (0.0, sum(top_interval) / 2, 18.8),
    )
    bottom_behind_shroud = _box(
        p.moving_outlet_width - 0.02,
        p.moving_outlet_length - 0.02,
        0.4,
        (0.0, sum(bottom_interval) / 2, -18.8),
    )
    assert _intersection_volume(housing, top_behind_shroud) < BREP_TOLERANCE
    assert _intersection_volume(housing, bottom_behind_shroud) < BREP_TOLERANCE


def test_full_faceplate_has_6400_of_6400_global_rear_rays_and_feature_coverage(
    fixed_parts,
) -> None:
    p = P0V3
    _, cover = fixed_parts
    rear_mid_y = (p.rear_faceplate_exterior_y + p.rear_faceplate_interior_y) / 2
    coordinates = [-19.75 + 0.5 * index for index in range(80)]
    assert sum(
        cover.is_inside(Vector(x, rear_mid_y, z), tolerance=1e-7)
        for x in coordinates
        for z in coordinates
    ) == 6400

    feature_regions = (
        (-13.9, 13.9, 18.0, 20.0),
        (-13.9, 13.9, -20.0, -18.0),
        (-2.7, 2.7, 15.4, 18.6),
        (-2.7, 2.7, -18.6, -15.4),
    )
    for xmin, xmax, zmin, zmax in feature_regions:
        x_count = int(round((xmax - xmin) / 0.2))
        z_count = int(round((zmax - zmin) / 0.2))
        assert all(
            cover.is_inside(
                Vector(xmin + 0.1 + 0.2 * ix, rear_mid_y, zmin + 0.1 + 0.2 * iz),
                tolerance=1e-7,
            )
            for ix in range(x_count)
            for iz in range(z_count)
        )


def test_only_four_designated_zero_volume_cover_shutter_stop_contacts() -> None:
    p = P0V3
    cover = make_blind_rear_cover()
    top = Location((0.0, p.latched_center_y, 0.0)) * make_top_shutter()
    bottom = Location((0.0, p.latched_center_y, 0.0)) * make_bottom_shutter()
    assert _intersection_volume(cover, top) < BREP_TOLERANCE
    assert _intersection_volume(cover, bottom) < BREP_TOLERANCE

    expected_half_probe_volume = 1.0 * 0.05 * 0.6
    for x_center in (-p.shutter_stop_nib_center_x, p.shutter_stop_nib_center_x):
        for shutter, z_center in ((top, 18.6), (bottom, -18.6)):
            contact_probe = _box(1.0, 0.10, 0.6, (x_center, -18.40, z_center))
            assert _intersection_volume(cover, contact_probe) == pytest.approx(
                expected_half_probe_volume, rel=1e-6
            )
            assert _intersection_volume(shutter, contact_probe) == pytest.approx(
                expected_half_probe_volume, rel=1e-6
            )

    clear_region = _box(1.0, 0.20, 0.6, (0.0, -18.55, 18.6))
    assert _intersection_volume(cover, clear_region) < BREP_TOLERANCE
    assert _intersection_volume(top, clear_region) < BREP_TOLERANCE


def test_actual_c4_snap_centers_and_outer_skin_map_to_main_parts(fixed_parts) -> None:
    p = P0V3
    housing, cover = fixed_parts
    for x_center in (-p.rear_snap_center_x, p.rear_snap_center_x):
        for z_center in (-17.55, 17.55):
            beam_probe = _box(
                p.rear_snap_width,
                p.rear_snap_local_front_y,
                p.rear_snap_bending_thickness,
                (
                    x_center,
                    p.rear_faceplate_interior_y + p.rear_snap_local_front_y / 2,
                    z_center,
                ),
            )
            assert _intersection_volume(cover, beam_probe) == pytest.approx(
                beam_probe.volume, rel=1e-6
            )

        top_skin_probe = _box(1.0, 0.4, 0.6, (x_center, -10.4, 19.4))
        bottom_skin_probe = _box(1.0, 0.4, 0.6, (x_center, -10.4, -19.4))
        assert _intersection_volume(housing, top_skin_probe) == pytest.approx(
            top_skin_probe.volume, rel=1e-6
        )
        assert _intersection_volume(housing, bottom_skin_probe) == pytest.approx(
            bottom_skin_probe.volume, rel=1e-6
        )


def test_named_detent_and_snap_strain_math_remains_below_two_percent() -> None:
    p = P0V3
    expected_detent_strain = (
        3
        * p.detent_finger_thickness
        * p.detent_maximum_deflection
        / (2 * p.detent_finger_free_length**2)
    )
    expected_nominal_snap_strain = (
        1.5
        * p.rear_snap_bending_thickness
        * p.rear_snap_nominal_deflection
        / p.rear_snap_effective_length**2
    )
    expected_worst_snap_strain = (
        1.5
        * p.rear_snap_bending_thickness
        * p.rear_snap_worst_deflection
        / p.rear_snap_effective_length**2
    )
    assert p.estimated_detent_strain == pytest.approx(expected_detent_strain)
    assert p.nominal_snap_strain == pytest.approx(expected_nominal_snap_strain)
    assert p.worst_snap_strain == pytest.approx(expected_worst_snap_strain)
    assert p.estimated_detent_strain < 0.02
    assert p.nominal_snap_strain < 0.02
    assert p.worst_snap_strain < 0.03
