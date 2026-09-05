"""Cheap parameter-registry and single-derivation gates for CV1-PARAMETERS/DERIVE."""
from dataclasses import asdict, fields, replace
from math import pi
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]/'cad'))
from container_generator_v1 import PARAMETER_SPECS, Parameters, derive, preset


def test_registry_classifies_every_input_truthfully():
    rows = {row['id']: row for row in PARAMETER_SPECS}
    assert len(rows) == len(PARAMETER_SPECS) == len(fields(Parameters)) == 26
    assert set(rows) == {field.name for field in fields(Parameters)}
    assert {row['classification'] for row in rows.values()} == {
        'adjustable_geometry', 'reference_readout_only', 'locked'}
    for row in rows.values():
        assert {'id', 'group', 'unit', 'default', 'domain', 'classification',
                'affects_geometry', 'geometry_targets', 'validation_oracle'} <= set(row)
        assert row['default'] == getattr(Parameters(), row['id'])
    assert rows['device_diameter']['classification'] == 'reference_readout_only'
    assert rows['device_diameter']['affects_geometry'] is False
    assert rows['device_diameter']['geometry_targets'] == ()
    assert {row['id'] for row in rows.values() if row['classification'] == 'adjustable_geometry'} == {
        'device_length', 'axial_allowance', 'cap_cavity_length', 'thread_clearance',
        'outer_diameter', 'skin_axial_pitch', 'skin_arc_pitch_target', 'skin_height',
        'plateau_half_fraction', 'skin_phase_theta', 'skin_phase_z', 'end_chamfer_size'}


def test_default_resolved_contract_and_placements():
    r = derive(preset())
    assert (r.cavity_length, r.cap_height, r.body_depth, r.neck_height, r.outer_length) == (213, 84, 132, 9, 219)
    assert (r.body_band, r.cap_band) == ((-135, 0), (0, 84))
    assert (r.outer_crest_radius, r.outer_valley_radius, r.body_inner_radius,
            r.cap_inner_radius) == pytest.approx((19.5, 19.05, 15, 15.5))
    assert (r.thread_root, r.thread_crest, r.female_minimum_wall,
            r.minimum_wall) == pytest.approx((16.4, 16.9, 1.85, 1.4))
    assert r.lattice_count == 33
    assert (r.end_chamfer_radius, r.end_chamfer_axial_height,
            r.end_chamfer_slope, r.end_chamfer_smooth_band) == pytest.approx((18.3, 1.2, 1, .75))
    assert len(r.drain_centers) == 7 and r.drain_centers[0] == (0, 0)
    assert all((x*x+y*y)**.5 == pytest.approx(9) for x, y in r.drain_centers[1:])
    assert r.body_print_translation == (23, 0, 135)
    assert r.cap_print_translation == (-23, 0, 84)
    assert r.cap_print_rotation == (180, 0, 0)
    assert dict(r.body_datums) == {'shoulder': 0, 'tip': 9, 'full_thread_start': 2,
                                   'full_thread_end': 8, 'skin_phase': 0,
                                   'bed': -135, 'inner_floor': -132}
    assert dict(r.cap_datums) == {'shoulder': 0, 'tip': 9, 'full_thread_start': 2,
                                  'full_thread_end': 8, 'skin_phase': 0,
                                  'bed': 84, 'inner_floor': 81}


@pytest.mark.parametrize('change', [
    {'device_length': 0}, {'device_diameter': 0}, {'axial_allowance': 2.999},
    {'cap_cavity_length': 0}, {'thread_clearance': .199}, {'thread_clearance': .301},
    {'outer_diameter': 0}, {'outer_diameter': 80.01}, {'skin_axial_pitch': 2.99},
    {'skin_axial_pitch': 8.01}, {'skin_arc_pitch_target': 0}, {'skin_height': 0},
    {'skin_height': .601}, {'plateau_half_fraction': 0}, {'plateau_half_fraction': .5},
    {'end_chamfer_size': .799}, {'end_chamfer_size': 1.501},
    {'skin_phase_theta': float('nan')}, {'thread_pitch': 2.01},
    {'drain_ring_count': 7}, {'skin_style': 'smooth'},
])
def test_invalid_inputs_stop_at_pure_derivation(change):
    with pytest.raises(ValueError):
        derive(replace(Parameters(), **change))


def test_reference_diameter_changes_only_reference_readouts():
    baseline = derive(Parameters())
    changed = derive(replace(Parameters(), device_diameter=31.5))
    ignored = {'device_diameter', 'body_radial_gap', 'cap_radial_gap'}
    assert {k: v for k, v in asdict(baseline).items() if k not in ignored} == {
        k: v for k, v in asdict(changed).items() if k not in ignored}
    assert (changed.body_radial_gap, changed.cap_radial_gap) == (-.75, -.25)
    with pytest.raises(ValueError):
        preset('generic')
