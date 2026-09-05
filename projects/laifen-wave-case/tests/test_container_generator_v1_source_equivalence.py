"""Direct immutable-P1-R7 to standalone-native equivalence gates."""
from hashlib import sha256
from pathlib import Path
import sys
from collections import Counter

import pytest
from build123d import Compound, Plane, Solid
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

sys.path.insert(0, str(Path(__file__).parents[1]/'cad'))
from container_generator_v1 import derive, preset
from container_generator_v1.assembly import build_assembly, print_layout
from container_generator_v1.parts import build_body, build_cap, drain_centers


PROJECT = Path(__file__).parents[1]
BASELINE = PROJECT/'cad'/'p1_r7_end_chamfer'
PACKAGE = PROJECT/'cad'/'container_generator_v1'
FROZEN = PROJECT/'docs'/'iterations'/'2026-09-04-cad-foundation-v1'/'inputs'/'frozen-inputs.sha256'


def adaptive_volume(shape):
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped, props, 1e-10, True, False)
    return props.Mass()


def center_of_mass(shape):
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped, props, 1e-10, True, False)
    point = props.CentreOfMass()
    return point.X(), point.Y(), point.Z()


def bounds(shape):
    box = shape.bounding_box()
    return (box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z)


def intersection_volume(left, right):
    common = left.intersect(right)
    if common is None:
        return 0.0
    if isinstance(common, list):
        return sum(piece.volume for piece in common)
    return common.volume


def assert_native_equivalent(old, new):
    assert old.is_valid and new.is_valid
    assert len(old.solids()) == len(new.solids()) == 1
    assert len(old.faces()) == len(new.faces())
    assert len(old.edges()) == len(new.edges())
    assert len(old.vertices()) == len(new.vertices())
    assert bounds(new) == pytest.approx(bounds(old), abs=1e-6)
    assert center_of_mass(new) == pytest.approx(center_of_mass(old), abs=1e-6)
    assert adaptive_volume(new) == pytest.approx(adaptive_volume(old), abs=.001)
    assert Counter(face.geom_type for face in new.faces()) == Counter(
        face.geom_type for face in old.faces())
    old_vertices = sorted((round(v.X, 7), round(v.Y, 7), round(v.Z, 7))
                          for v in old.vertices())
    new_vertices = sorted((round(v.X, 7), round(v.Y, 7), round(v.Z, 7))
                          for v in new.vertices())
    assert new_vertices == old_vertices


def test_frozen_p1_r7_remains_hash_clean_and_new_package_is_standalone():
    entries = []
    for line in FROZEN.read_text().splitlines():
        digest, relative = line.split('  ', 1)
        if relative.startswith('projects/laifen-wave-case/cad/p1_r7_end_chamfer/'):
            path = PROJECT.parents[1]/relative
            entries.append(relative)
            assert sha256(path.read_bytes()).hexdigest() == digest
    assert len(entries) == 20
    runtime = '\n'.join(path.read_text() for path in PACKAGE.glob('*.py'))
    assert 'p1_r7_end_chamfer' not in runtime
    assert 'import_stl' not in runtime and 'import_mesh' not in runtime


def test_default_body_and_cap_match_old_native_solids_and_datums():
    from p1_r7_end_chamfer.params import Params as OldParameters
    from p1_r7_end_chamfer.parts import build_body as old_body, build_cap as old_cap

    resolved = derive(preset())
    pairs = ((old_body(OldParameters()), build_body(resolved)),
             (old_cap(OldParameters()), build_cap(resolved)))
    expected_datums = {'shoulder', 'tip', 'full_thread_start', 'full_thread_end',
                       'skin_phase', 'bed', 'inner_floor', 'screw_axis'}
    for old, new in pairs:
        assert_native_equivalent(old, new)
        assert set(old.joints) == set(new.joints) == expected_datums
    assert drain_centers(resolved) == list(resolved.drain_centers)


def test_native_closed_and_print_placements_preserve_identity_and_collision_contract():
    resolved = derive(preset())
    closed = build_assembly(resolved)
    assert len(closed.solids()) == 2
    assert bounds(closed)[5] - bounds(closed)[2] == pytest.approx(219, abs=1e-6)
    # The only possible closed-state overlap is inside the 0..9 mm thread zone;
    # crop the actual solids before the Boolean to avoid duplicating dense skin.
    zone = Solid.make_cylinder(17.5, resolved.neck_height-.002,
                               Plane(origin=(0, 0, .001)))
    thread_regions = []
    for part in closed.solids():
        pieces = part.intersect(zone)
        thread_regions.append(Compound(children=list(pieces)) if isinstance(pieces, list) else pieces)
    assert intersection_volume(*thread_regions) <= 1e-7
    layout = print_layout(resolved)
    solids = layout.solids()
    assert len(solids) == 2
    boxes = [solid.bounding_box() for solid in solids]
    assert all(box.min.Z == pytest.approx(0, abs=1.1e-7) for box in boxes)
    assert sorted(box.max.Z for box in boxes) == pytest.approx([84, 144], abs=1e-6)
    assert sorted((box.min.X+box.max.X)/2 for box in boxes) == pytest.approx([-23, 23], abs=1e-6)
    assert min(box.min.X for box in boxes if (box.min.X+box.max.X)/2 > 0) - max(
        box.max.X for box in boxes if (box.min.X+box.max.X)/2 < 0) == pytest.approx(7, abs=1e-6)
