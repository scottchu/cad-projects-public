"""Rigid print-pose and plate-layout checks for accepted P0 V3 geometry."""

from itertools import combinations

import numpy as np
import pytest
import trimesh
from build123d import export_stl

from pill_click.p0_v3 import (
    make_c1r1_rail_coupon,
    make_c2_legacy_rail_coupon,
    make_blind_rear_cover,
    make_bottom_shutter,
    make_housing,
    make_shutter_track_coupon,
    make_shuttle,
    make_top_shutter,
)
from pill_click.p0_v3.coupons import make_c4_snap_coupon
from pill_click.p0_v3.print_exports import (
    PRINT_ITEM_FACTORIES,
    make_p0_v3_print_bundle,
)


SOURCE_FACTORIES = {
    "housing": make_housing,
    "inner_medicine_shuttle": make_shuttle,
    "top_shutter": make_top_shutter,
    "bottom_shutter": make_bottom_shutter,
    "rear_cover": make_blind_rear_cover,
    "c1r1_nominal_L6p80_lip0p80_coupon": make_c1r1_rail_coupon,
    "c1r1b_nominal_L6p80_lip1p20_coupon": lambda: make_c1r1_rail_coupon(thick_lip=True),
    "c2_loose_original_L3p40_coupon": make_c2_legacy_rail_coupon,
    "c3_shutter_track_coupon": make_shutter_track_coupon,
    "c4_rear_snap_coupon": make_c4_snap_coupon,
}


def test_print_items_are_only_rigidly_reoriented_accepted_solids() -> None:
    assert set(PRINT_ITEM_FACTORIES) == set(SOURCE_FACTORIES)
    for name, factory in PRINT_ITEM_FACTORIES.items():
        source = SOURCE_FACTORIES[name]()
        exported = factory()
        assert exported.is_valid
        assert exported.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)
        assert len(exported.solids()) == len(source.solids())
        assert exported.volume == pytest.approx(source.volume, rel=1e-9, abs=1e-6)


def test_print_bundle_preserves_ten_named_groups_and_fifteen_solids() -> None:
    bundle = make_p0_v3_print_bundle()
    assert bundle.is_valid
    assert len(bundle.children) == 10
    assert {child.label for child in bundle.children} == set(PRINT_ITEM_FACTORIES)
    assert len(bundle.solids()) == 15
    assert bundle.bounding_box().size.X <= 220.0
    assert bundle.bounding_box().size.Y <= 220.0
    assert bundle.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)
    for first, second in combinations(bundle.children, 2):
        first_bbox = first.bounding_box()
        second_bbox = second.bounding_box()
        assert (
            first_bbox.max.X <= second_bbox.min.X
            or second_bbox.max.X <= first_bbox.min.X
            or first_bbox.max.Y <= second_bbox.min.Y
            or second_bbox.max.Y <= first_bbox.min.Y
        )


@pytest.mark.parametrize(
    ("name", "expected_components"),
    [
        ("inner_medicine_shuttle", 1),
        ("c1r1_nominal_L6p80_lip0p80_coupon", 2),
        ("c1r1b_nominal_L6p80_lip1p20_coupon", 2),
        ("rear_cover", 1),
        ("c4_rear_snap_coupon", 2),
    ],
)
def test_strengthened_and_snap_exports_pass_coordinate_welded_mesh_gate(
    name: str,
    expected_components: int,
    tmp_path,
) -> None:
    path = tmp_path / f"{name}.stl"
    export_stl(
        PRINT_ITEM_FACTORIES[name](),
        path,
        tolerance=0.02,
        angular_tolerance=0.05,
    )
    mesh = trimesh.load_mesh(path, process=False)
    assert isinstance(mesh, trimesh.Trimesh)
    mesh.merge_vertices(digits_vertex=6, merge_tex=True, merge_norm=True)
    mesh.remove_unreferenced_vertices()

    faces = np.asarray(mesh.faces)
    canonical_faces = np.sort(faces, axis=1)
    _, face_counts = np.unique(canonical_faces, axis=0, return_counts=True)
    edges = np.sort(
        faces[:, [[0, 1], [1, 2], [2, 0]]].reshape((-1, 2)),
        axis=1,
    )
    _, edge_counts = np.unique(edges, axis=0, return_counts=True)

    assert np.all(mesh.area_faces > 1e-18)
    assert np.all(face_counts == 1)
    assert np.all(edge_counts == 2)
    assert len(mesh.split(only_watertight=False)) == expected_components
    assert mesh.is_watertight
    assert mesh.is_winding_consistent
    assert mesh.volume > 0.0
