"""Focused R4 regressions for the reported bulged, partly unpatterned exterior."""
from dataclasses import replace
from math import pi
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).parents[1]/'cad'))
from p1_r4_uniform_skin.params import Params,derive
from p1_r4_uniform_skin.skin import field,radius
from p1_r4_uniform_skin.surface import route_bounds,skin_patches
from p1_r3_generator.params import Params as OriginalParams,derive as original_derive


def test_uniform_envelope_wall_budget_and_full_coverage():
    """Reject old collar OD at full texture depth and catch hidden blank zones."""
    p=Params();d=derive(p)
    with pytest.raises(ValueError,match='ligament'):
        derive(replace(p,outer_diameter=39))
    assert d.outer_crest_radius == 20
    assert d.outer_valley_radius-d.thread_crest-p.clearance_budget >= 1.8
    assert d.body_band == (-35.1,0.) and d.cap_band == (0.,43.4)
    assert d.lattice_count == 34 and route_bounds(p)['plateau_bound'] >= 1
    assert route_bounds(p)['radial_bound'] <= .004
    assert route_bounds(p)['slope_bound'] <= 1
    for role,z in [('body',-35.),('body',-4.),('body',-.01),('cap',.01),
                   ('cap',5.),('cap',11.),('cap',23.),('cap',43.3)]:
        values=[radius(p,role,2*pi*k/3400,z,d) for k in range(100)]
        assert max(values)-min(values) > .15, (role,z)
    for k in range(101):
        theta=2*pi*k/100
        assert radius(p,'body',theta,0,d)==radius(p,'cap',theta,0,d)
    assert all(x.kind not in ('smooth','lower','upper') for x in skin_patches(p,'cap'))


def test_functional_derivation_and_length_are_independent_of_outside_radius():
    """Catch the silent J/A female-taper change caused by a new outside radius."""
    p=Params();old=original_derive(OriginalParams());d=derive(p)
    names=('body_inner_radius','cap_inner_radius','body_radius','cap_radius','thread_root',
           'thread_crest','shoulder_radius','neck_height','full_thread_start','full_thread_end',
           'collar_end','taper_length','cap_straight_start','body_depth','thread_flank_slope',
           'thread_lead_slope','outer_length')
    for name in names:assert getattr(d,name)==getattr(old,name),name
    bigger=derive(replace(p,outer_diameter=40.2))
    for name in names:assert getattr(d,name)==getattr(bigger,name),name
    longer=replace(p,cavity_length=p.cavity_length+p.skin_axial_pitch)
    ld=derive(longer)
    assert ld.body_band[0]==pytest.approx(d.body_band[0]-p.skin_axial_pitch)
    assert ld.lattice_count==d.lattice_count
    for theta,z in [(0.,-5.),(.3,2.4),(pi,10.2)]:
        assert field(p,theta,z)==field(longer,theta,z)
        assert field(p,theta,z)==pytest.approx(field(p,theta,z+p.skin_axial_pitch))
    with pytest.raises(ValueError,match='locked'):
        derive(replace(p,thread_pitch=2.4,engagement=7.2))


def test_written_parts_topology_counts_floors_and_print_orientation():
    """Catch malformed planar closures, filled bores or the obsolete four-part layout."""
    from build123d import import_step
    base=Path(__file__).parents[1]/'cad'/'p1_r4_uniform_skin'
    shapes={name:import_step(str(base/(name+'.step'))) for name in ('body','cap_c25','closed_c25','print_layout')}
    for name,shape in shapes.items():
        assert shape.is_valid and shape.volume>0
        assert len(shape.solids()) == (1 if name in ('body','cap_c25') else 2)
    body=shapes['body'].solids()[0];cap=shapes['cap_c25'].solids()[0]
    assert body.is_inside((8,0,-32.11)) and not body.is_inside((8,0,-32.09))
    assert cap.is_inside((8,0,40.41)) and not cap.is_inside((8,0,40.39))
    for solid in shapes['print_layout'].solids():
        bb=solid.bounding_box()
        assert bb.min.Z == pytest.approx(0.,abs=1e-5)
        center=solid.center()
        assert not solid.is_inside((center.X,center.Y,bb.max.Z-.1))
    assert shapes['print_layout'].bounding_box().max.Z == pytest.approx(44.1,abs=1e-5)
