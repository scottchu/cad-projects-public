"""Deterministic BREP and mesh acceptance for mechanical-fit v1."""

from itertools import combinations

import numpy as np
import pytest
import trimesh
from build123d import Align, Box, Location, Matrix, Vector, export_stl

from pill_click.p0_mechanical_fit_v1 import (
    P0_MECHANICAL_FIT_V1,
    make_assembly,
    make_solid_inner_button,
    make_outer_housing,
    make_pressed_assembly,
    make_print_bundle,
    make_released_assembly,
    make_snap_rear_cover,
    print_solid_inner_button,
    print_outer_housing,
    print_snap_rear_cover,
)
from pill_click.p0_mechanical_fit_v1.geometry import (
    _box_bounds,
    _hook_prism,
    _rear_backing_rib,
    _snap_root_material,
)
from pill_click.p0_v3 import P0V3, make_c4_snap_arm


TOL = 1e-6


def _box(size_x, size_y, size_z, center):
    return Box(
        size_x,
        size_y,
        size_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location(center))


def _bbox(shape):
    box = shape.bounding_box()
    return (box.min.X, box.max.X, box.min.Y, box.max.Y, box.min.Z, box.max.Z)


def _intersection(first, second) -> float:
    return (first & second).volume


@pytest.fixture(scope="module")
def parts():
    return make_outer_housing(), make_solid_inner_button(), make_snap_rear_cover()


def test_spec_math_is_self_consistent_for_fit_critical_interfaces() -> None:
    p = P0_MECHANICAL_FIT_V1
    assert p.rear_land_local_y == pytest.approx((-17.2, -10.4))
    assert p.front_land_local_y == pytest.approx((-10.0, -3.2))
    assert p.front_land_local_y[0] - p.rear_land_local_y[1] == pytest.approx(0.4)
    assert 2 * p.land_length == pytest.approx(13.6)
    assert (p.bearing_boss_width - p.nominal_groove_width) / 2 == pytest.approx(
        p.normal_lip_per_side
    )
    assert (p.bearing_boss_width - p.mouth_width) / 2 == pytest.approx(
        p.mouth_lip_per_side
    )
    assert p.rear_backing_rib_local_y == pytest.approx((-17.2, -12.8))
    assert p.released_endplay == pytest.approx(0.15)
    assert p.tab_stop_overlap_per_side == pytest.approx(1.0)
    assert p.nominal_snap_strain < 0.02
    assert p.worst_snap_strain < 0.03


def test_exactly_three_valid_positive_single_solid_parts_and_bounds(parts) -> None:
    outer, inner, cover = parts
    for part in parts:
        assert part.is_valid and part.volume > 0
        assert len(part.solids()) == 1
    assert _bbox(outer) == pytest.approx((-20, 20, -18.7, 20, -20, 20))
    # The explicit 35.20 key cap controls Z=+/-17.60; the spec's later
    # +/-17.10 summary is incompatible with that required cap dimension.
    assert _bbox(inner) == pytest.approx((-18.45, 18.45, -17.2, 15.5, -17.6, 17.6))
    assert _bbox(cover)[0:4] == pytest.approx((-20, 20, -20, -9.85))
    assert _bbox(cover)[4:6] == pytest.approx((-20, 20))


def test_assemblies_have_exactly_three_named_parts_and_required_envelopes() -> None:
    pressed = make_pressed_assembly()
    released = make_released_assembly()
    assert len(pressed.children) == len(released.children) == 3
    assert len(pressed.solids()) == len(released.solids()) == 3
    assert _bbox(pressed) == pytest.approx((-20, 20, -20, 20, -20, 20))
    assert _bbox(released) == pytest.approx((-20, 20, -20, 33.4, -20, 20))
    forbidden = (
        "aperture",
        "shutter",
        "track",
        "coupling",
        "spring",
        "magnet",
        "latch",
        "medicine",
        "weekday",
        "text",
    )
    labels = [pressed.label, *(child.label for child in pressed.children)]
    assert not any(token in label.lower() for token in forbidden for label in labels)


def test_inner_body_is_solid_with_no_modeled_internal_void_or_path(parts) -> None:
    p = P0_MECHANICAL_FIT_V1
    _, inner, _ = parts
    # The only subtraction from the nominal body envelope is the externally
    # accessible rail-mouth interface at the side surface. A continuous deep
    # core proves that no enclosed cavity or hidden void is modeled.
    solid_core = _box_bounds(
        (-16.8, 16.8),
        (p.inner_body_rear_local_y, p.inner_body_front_local_y),
        (-p.inner_body_half, p.inner_body_half),
    )
    assert _intersection(inner, solid_core) == pytest.approx(solid_core.volume)
    assert (solid_core - inner).volume < TOL
    assert all(
        inner.is_inside(Vector(x, y, z), tolerance=1e-7)
        for x in (-15.0, -7.5, 0.0, 7.5, 15.0)
        for y in (-11.0, -5.0, 0.0, 5.0, 10.0)
        for z in (-15.0, -7.5, 0.0, 7.5, 15.0)
    )


def test_all_eight_grooves_and_mouths_have_exact_brep_clearance_and_lips(parts) -> None:
    p = P0_MECHANICAL_FIT_V1
    _, inner, _ = parts
    for side in (-1.0, 1.0):
        for z_center in p.rail_z_centres:
            for y_bounds in (p.rear_land_local_y, p.front_land_local_y):
                normal_y = y_bounds[0] + 1.0
                mouth_y = y_bounds[1] - p.mouth_length / 2
                x_sign = side
                groove_center_x = x_sign * (p.groove_bottom_x + 0.35)
                normal_void = _box(
                    0.68,
                    0.10,
                    p.nominal_groove_width - 0.02,
                    (groove_center_x, normal_y, z_center),
                )
                mouth_void = _box(
                    0.96,
                    p.mouth_length - 0.02,
                    p.mouth_width - 0.02,
                    (x_sign * (p.groove_bottom_x + 0.18), mouth_y, z_center),
                )
                assert _intersection(inner, normal_void) < TOL
                assert _intersection(inner, mouth_void) < TOL

                for z_side in (-1.0, 1.0):
                    normal_lip_z = z_center + z_side * (
                        p.nominal_groove_width / 2 + p.normal_lip_per_side / 2
                    )
                    normal_lip = _box(
                        0.60,
                        0.10,
                        p.normal_lip_per_side - 0.02,
                        (x_sign * 17.55, normal_y, normal_lip_z),
                    )
                    mouth_lip_z = z_center + z_side * (
                        p.mouth_width / 2 + p.mouth_lip_per_side / 2
                    )
                    mouth_lip = _box(
                        0.60,
                        0.10,
                        p.mouth_lip_per_side - 0.02,
                        (x_sign * 17.55, mouth_y, mouth_lip_z),
                    )
                    assert _intersection(inner, normal_lip) == pytest.approx(normal_lip.volume)
                    assert _intersection(inner, mouth_lip) == pytest.approx(mouth_lip.volume)


def test_four_backing_ribs_have_exact_bounds_and_finite_body_boss_overlap() -> None:
    p = P0_MECHANICAL_FIT_V1
    body = _box_bounds(
        (-p.inner_body_half, p.inner_body_half),
        (p.inner_body_rear_local_y, p.inner_body_front_local_y),
        (-p.inner_body_half, p.inner_body_half),
    )
    boss_depth = p.boss_outer_x - p.inner_body_half
    for side in (-1.0, 1.0):
        for z_center in p.rail_z_centres:
            rib = _rear_backing_rib(side, z_center, p)
            boss = _box(
                boss_depth,
                p.land_length,
                p.bearing_boss_width,
                (
                    side * (p.inner_body_half + boss_depth / 2),
                    p.rear_land_local_center_y,
                    z_center,
                ),
            )
            expected_x = (16.45, 17.25) if side > 0 else (-17.25, -16.45)
            assert _bbox(rib) == pytest.approx(
                (expected_x[0], expected_x[1], -17.2, -12.8, z_center - 2.15, z_center + 2.15)
            )
            assert _intersection(rib, body) == pytest.approx(0.559, abs=1e-9)
            assert _intersection(rib, boss) == pytest.approx(2.838, abs=1e-9)


def test_293_state_motion_sweep_is_collision_free_and_engagement_is_constant(parts) -> None:
    p = P0_MECHANICAL_FIT_V1
    outer, inner, cover = parts
    states = [round(p.inward_state + 0.05 * index, 2) for index in range(292)]
    states.append(p.maximum_pull_state)
    assert len(states) == 293
    assert {p.pressed_state, p.released_state, p.maximum_pull_state}.issubset(states)
    for state in states:
        moving = Location((0.0, p.inner_center_y(state), 0.0)) * inner
        assert _intersection(outer, moving) < TOL
        assert _intersection(cover, moving) < TOL
        for local_land in (p.rear_land_local_y, p.front_land_local_y):
            global_land = tuple(p.inner_center_y(state) + value for value in local_land)
            assert p.full_depth_rail_y[0] <= global_land[0]
            assert global_land[1] <= p.full_depth_rail_y[1]
        assert sum(bounds[1] - bounds[0] for bounds in (p.rear_land_local_y, p.front_land_local_y)) == pytest.approx(13.6)


def test_390_state_rear_feed_is_collision_free_and_mouth_entries_are_exact(parts) -> None:
    p = P0_MECHANICAL_FIT_V1
    outer, inner, _ = parts
    centers = [round(p.feed_start_center_y + 0.1 * index, 2) for index in range(390)]
    assert centers[0] == pytest.approx(-34.4)
    assert centers[-1] == pytest.approx(4.5)
    for center in centers:
        assert _intersection(outer, Location((0.0, center, 0.0)) * inner) < TOL
    # Positive-Y edges of the two lands meet the full-depth rail rear datum.
    assert p.full_depth_rail_y[0] - p.rear_land_local_y[1] == pytest.approx(-7.6)
    assert p.full_depth_rail_y[0] - p.front_land_local_y[1] == pytest.approx(-14.8)
    assert p.pressed_center_y + p.rear_land_local_y[1] == pytest.approx(-5.9)
    assert p.pressed_center_y + p.front_land_local_y[1] == pytest.approx(1.3)


def test_captivity_endplay_contact_and_pull_rejection(parts) -> None:
    p = P0_MECHANICAL_FIT_V1
    outer, inner, _ = parts
    assert p.inner_center_y(p.released_state) + p.captive_tab_local_y[1] == pytest.approx(15.2)
    assert p.inner_center_y(p.maximum_pull_state) + p.captive_tab_local_y[1] == pytest.approx(15.35)
    at_max = Location((0.0, p.inner_center_y(p.maximum_pull_state), 0.0)) * inner
    assert _intersection(outer, at_max) < TOL
    for x_center in (-17.95, 17.95):
        contact_probe = _box(0.8, 0.10, 4.8, (x_center, p.front_shoulder_y, 0.0))
        assert _intersection(outer, contact_probe) == pytest.approx(contact_probe.volume / 2)
        assert _intersection(at_max, contact_probe) == pytest.approx(contact_probe.volume / 2)
    with pytest.raises(ValueError):
        make_assembly(p.maximum_pull_state + 0.01)


def test_cover_uses_exact_four_mapped_c4_roots_and_overlap_volumes(parts) -> None:
    p = P0_MECHANICAL_FIT_V1
    _, _, cover = parts
    c4_arm = make_c4_snap_arm(P0V3)
    faceplate = _box_bounds((-20, 20), (-20, -18.7), (-20, 20))
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
                    [0, 0, 1, x_center],
                    [0, 1, 0, p.rear_faceplate_interior_y],
                    [radial_sign, 0, 0, beam_inner_z],
                    [0, 0, 0, 1],
                ]
            )
            mapped = c4_arm.transform_geometry(transform)
            root = _snap_root_material(x_center, top=top, p=p)
            beam = _box_bounds(
                (x_center - p.rear_snap_width / 2, x_center + p.rear_snap_width / 2),
                (p.rear_faceplate_interior_y, p.rear_snap_pocket_front_y),
                (
                    (beam_inner_z, p.rear_snap_top_beam_outer_z)
                    if top
                    else (p.rear_snap_bottom_beam_outer_z, beam_inner_z)
                ),
            )
            assert _intersection(root, faceplate) == pytest.approx(0.720000, abs=1e-6)
            assert _intersection(root, beam) == pytest.approx(0.576000, abs=1e-6)
            crop = _box(
                p.rear_snap_width - 0.02,
                0.98,
                0.98,
                (x_center, -18.40, beam_inner_z - radial_sign * 0.30),
            )
            actual = cover & crop
            expected = mapped & crop
            assert (actual - expected).volume < TOL
            assert (expected - actual).volume < TOL


def test_hooks_are_inside_blind_pockets_and_cover_is_seated_without_overlap(parts) -> None:
    p = P0_MECHANICAL_FIT_V1
    outer, _, cover = parts
    assert _intersection(outer, cover) < TOL
    for x_center in (-p.rear_snap_center_x, p.rear_snap_center_x):
        for top in (True, False):
            hook = _hook_prism(x_center, top=top, p=p)
            pocket_z = (
                (p.rear_snap_top_beam_outer_z, p.rear_snap_pocket_outer_z)
                if top
                else (-p.rear_snap_pocket_outer_z, p.rear_snap_bottom_beam_outer_z)
            )
            pocket = _box_bounds(
                (x_center - p.rear_snap_pocket_width_x / 2, x_center + p.rear_snap_pocket_width_x / 2),
                (p.rear_snap_pocket_rear_y, p.rear_snap_pocket_front_y),
                pocket_z,
            )
            assert (hook - pocket).volume < TOL
    assert p.rear_snap_top_hook_apex_z - p.rear_snap_top_beam_outer_z == pytest.approx(
        p.rear_snap_nominal_deflection
    )


def test_blind_rear_face_has_6400_of_6400_solid_grid_probes(parts) -> None:
    p = P0_MECHANICAL_FIT_V1
    _, _, cover = parts
    rear_mid_y = (p.rear_faceplate_exterior_y + p.rear_faceplate_interior_y) / 2
    coordinates = [-19.75 + 0.5 * index for index in range(80)]
    assert sum(
        cover.is_inside(Vector(x, rear_mid_y, z), tolerance=1e-7)
        for x in coordinates
        for z in coordinates
    ) == 6400


def test_print_exports_are_rigid_three_part_single_solid_layout(parts) -> None:
    factories = (print_outer_housing, print_solid_inner_button, print_snap_rear_cover)
    for source, factory in zip(parts, factories, strict=True):
        printed = factory()
        assert printed.is_valid and len(printed.solids()) == 1
        assert printed.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)
        assert printed.volume == pytest.approx(source.volume, abs=1e-6)
    bundle = make_print_bundle()
    assert bundle.is_valid and len(bundle.children) == len(bundle.solids()) == 3
    assert {child.label for child in bundle.children} == {
        "outer_housing",
        "solid_inner_button",
        "snap_rear_cover",
    }
    for first, second in combinations(bundle.children, 2):
        assert _intersection(first, second) < TOL


@pytest.mark.parametrize(
    "name,factory,expected_boundary_shells",
    [
        ("outer", print_outer_housing, 1),
        ("inner", print_solid_inner_button, 1),
        ("cover", print_snap_rear_cover, 1),
    ],
)
def test_each_print_stl_has_expected_closed_consistently_oriented_manifold_shells(
    name, factory, expected_boundary_shells, tmp_path
) -> None:
    path = tmp_path / f"{name}.stl"
    export_stl(factory(), path, tolerance=0.02, angular_tolerance=0.05)
    mesh = trimesh.load_mesh(path, process=False)
    assert isinstance(mesh, trimesh.Trimesh)
    mesh.merge_vertices(digits_vertex=6, merge_tex=True, merge_norm=True)
    mesh.remove_unreferenced_vertices()
    faces = np.asarray(mesh.faces)
    canonical_faces = np.sort(faces, axis=1)
    _, face_counts = np.unique(canonical_faces, axis=0, return_counts=True)
    edges = np.sort(faces[:, [[0, 1], [1, 2], [2, 0]]].reshape((-1, 2)), axis=1)
    _, edge_counts = np.unique(edges, axis=0, return_counts=True)
    assert np.all(mesh.area_faces > 1e-18)
    assert np.all(face_counts == 1)
    assert np.all(edge_counts == 2)
    components = mesh.split(only_watertight=False)
    assert len(components) == expected_boundary_shells
    assert all(component.is_watertight for component in components)
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0
