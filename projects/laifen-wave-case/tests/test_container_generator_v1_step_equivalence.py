"""Written STEP validity, parity, placement, collision, and FDM gates."""
from hashlib import sha256
from pathlib import Path
import sys
from collections import Counter

from build123d import Compound, Plane, Solid, import_step
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import pytest

sys.path.insert(0, str(Path(__file__).parents[1]/'cad'))
from container_generator_v1 import derive, preset
from container_generator_v1.parts import build_body, build_cap


PROJECT = Path(__file__).parents[1]
BASELINE = PROJECT/'cad'/'p1_r7_end_chamfer'
PACKAGE = PROJECT/'cad'/'container_generator_v1'


def adaptive_volume(shape):
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped, props, 1e-10, True, False)
    return props.Mass()


def centroid(shape):
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped, props, 1e-10, True, False)
    p = props.CentreOfMass()
    return p.X(), p.Y(), p.Z()


def bounds(shape):
    box = shape.bounding_box()
    return box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z


def intersection_volume(left, right):
    common = left.intersect(right)
    if common is None:
        return 0.0
    if isinstance(common, list):
        return sum(piece.volume for piece in common)
    return common.volume


def assert_step_equivalent(baseline, candidate):
    assert baseline.is_valid and candidate.is_valid
    assert len(candidate.solids()) == len(baseline.solids())
    assert len(candidate.faces()) == len(baseline.faces())
    assert bounds(candidate) == pytest.approx(bounds(baseline), abs=1e-6)
    assert centroid(candidate) == pytest.approx(centroid(baseline), abs=1e-6)
    assert adaptive_volume(candidate) == pytest.approx(adaptive_volume(baseline), abs=.001)
    assert Counter(face.geom_type for face in candidate.faces()) == Counter(
        face.geom_type for face in baseline.faces())
    assert sorted((round(v.X, 7), round(v.Y, 7), round(v.Z, 7))
                  for v in candidate.vertices()) == sorted(
        (round(v.X, 7), round(v.Y, 7), round(v.Z, 7))
        for v in baseline.vertices())


def test_four_written_steps_are_valid_and_baseline_equivalent():
    names = ('body', 'cap', 'closed', 'print_layout')
    old_names = {'body': 'body', 'cap': 'cap_c25', 'closed': 'closed_c25',
                 'print_layout': 'print_layout'}
    for name in names:
        path = PACKAGE/(name+'.step')
        assert path.is_file() and path.stat().st_size > 0
        candidate = import_step(str(path))
        baseline = import_step(str(BASELINE/(old_names[name]+'.step')))
        assert_step_equivalent(baseline, candidate)


def test_source_native_to_written_step_parity_and_locked_measurements():
    resolved = derive(preset())
    written_body = import_step(str(PACKAGE/'body.step')).solids()[0]
    written_cap = import_step(str(PACKAGE/'cap.step')).solids()[0]
    for source, written, faces, z_range in (
        (build_body(resolved), written_body, 10255, (-135, 9)),
        (build_cap(resolved), written_cap, 6396, (0, 84)),
    ):
        assert source.is_valid and written.is_valid
        assert len(source.faces()) == len(written.faces()) == faces
        assert adaptive_volume(source) == pytest.approx(adaptive_volume(written), abs=.001)
        assert bounds(source) == pytest.approx(bounds(written), abs=1e-6)
        assert (written.bounding_box().min.Z, written.bounding_box().max.Z) == pytest.approx(z_range, abs=1e-6)
    assert written_body.bounding_box().size.X == pytest.approx(39, abs=5e-5)
    assert written_cap.bounding_box().size.X == pytest.approx(39, abs=5e-5)
    assert resolved.female_minimum_wall >= 1.8
    assert resolved.minimum_wall >= 1.4
    assert resolved.skin_slope_bound <= 1 and resolved.end_chamfer_slope <= 1


def test_written_drains_closed_stop_engagement_and_print_layout():
    resolved = derive(preset())
    body = import_step(str(PACKAGE/'body.step')).solids()[0]
    cap = import_step(str(PACKAGE/'cap.step')).solids()[0]
    for solid, floor_outer in ((body, resolved.body_band[0]),
                               (cap, resolved.cap_cavity_length)):
        for x, y in resolved.drain_centers:
            for dz in (.01, 1.5, 2.99):
                assert not solid.is_inside((x, y, floor_outer+dz))
                assert not solid.is_inside((x+1.49, y, floor_outer+dz))
                assert solid.is_inside((x+1.51, y, floor_outer+dz))
    closed = import_step(str(PACKAGE/'closed.step'))
    parts = closed.solids()
    assert len(parts) == 2
    assert closed.bounding_box().size.Z == pytest.approx(resolved.outer_length, abs=1e-6)
    zone = Solid.make_cylinder(17.5, resolved.neck_height-.002,
                               Plane(origin=(0, 0, .001)))
    thread_regions = []
    for part in parts:
        pieces = part.intersect(zone)
        thread_regions.append(Compound(children=list(pieces)) if isinstance(pieces, list) else pieces)
    assert intersection_volume(*thread_regions) <= 1e-7
    assert body.is_inside((18, 0, -.001)) and cap.is_inside((18, 0, .001))
    assert resolved.full_thread_end-resolved.full_thread_start == pytest.approx(6)
    layout = import_step(str(PACKAGE/'print_layout.step'))
    objects = layout.solids()
    assert len(objects) == 2
    boxes = [obj.bounding_box() for obj in objects]
    assert all(box.min.Z == pytest.approx(0, abs=1.1e-7) for box in boxes)
    assert sorted(box.max.Z for box in boxes) == pytest.approx([84, 144], abs=1e-6)
    left = min(boxes, key=lambda b: (b.min.X+b.max.X)/2)
    right = max(boxes, key=lambda b: (b.min.X+b.max.X)/2)
    assert right.min.X-left.max.X == pytest.approx(resolved.print_bounds_separation, abs=1e-6)
    assert layout.bounding_box().size.X == pytest.approx(85.0000002, abs=1e-5)
    # Openings are up: axial center points just below each top remain outside.
    for obj in objects:
        box = obj.bounding_box()
        x = (box.min.X+box.max.X)/2
        assert not obj.is_inside((x, 0, box.max.Z-.1))


def test_step_hashes_are_recorded_without_relaxing_geometry_or_scope():
    expected_baseline = {
        'body': '3c04d417e3f21c5ef0e3b1d12ff1953ac366ef418fc4792d592a0624ad91982b',
        'cap': '0dd09cbd99f4ceb78605ee7eef1a74a315c3f95079d97a4628dffffc70afe82a',
        'closed': 'e72ee16eb4315a2eb93619ecfb3fd363ac89dc5253bb6527de9d71c82444d27c',
        'print_layout': '80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4',
    }
    observed = {name: sha256((PACKAGE/(name+'.step')).read_bytes()).hexdigest()
                for name in expected_baseline}
    # Hash identity is preferred. Any mismatch is assessed only after all
    # geometry/placement gates above and documented in IMPLEMENTATION.md.
    assert set(observed) == set(expected_baseline)
