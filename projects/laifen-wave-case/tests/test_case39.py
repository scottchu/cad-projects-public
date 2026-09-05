"""Focused R5 regressions: resized interface, unscaled skin, bevel and floor drains."""
from dataclasses import replace
from math import cos,hypot,pi,sin
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).parents[1]/'cad'))
from p1_r5_39mm_case.params import Params,derive
from p1_r5_39mm_case.skin import field,radius
from p1_r5_39mm_case.surface import route_bounds,skin_patches
from p1_r5_39mm_case.parts import drain_centers,drain_cutters


def test_selected_new_thread_and_independent_taper():
    """Catch old 40mm thread geometry leaking into the selected39mm budget."""
    p=Params();d=derive(p)
    assert d.thread_root == pytest.approx(16.4)
    assert d.thread_crest == pytest.approx(16.9)
    assert d.thread_root-d.body_inner_radius == pytest.approx(1.4)
    assert d.female_minimum_wall == pytest.approx(1.85)
    assert p.thread_height-p.clearance_budget == pytest.approx(.2)
    assert d.thread_flank_slope == pytest.approx(.5/.7)
    assert p.thread_clearance/d.thread_flank_slope == pytest.approx(.35)
    assert (d.neck_height,d.collar_end,d.cap_straight_start)==pytest.approx((9,10.2,12.4))
    assert d.taper_length == 2.2
    wider=derive(replace(p,outer_diameter=40.))
    for name in ('neck_height','collar_end','cap_straight_start','taper_length','thread_root','thread_crest'):
        assert getattr(d,name)==getattr(wider,name)
    with pytest.raises(ValueError,match='locked'):
        derive(replace(p,root_wall=1.8,thread_height=.15))
    with pytest.raises(ValueError,match='ligament'):
        derive(replace(p,outer_diameter=38.8))


def test_shared_pattern_beveled_ends_and_bounded_route():
    """Catch global Z scaling, independent phases, smooth collars or steep bevels."""
    p=Params();d=derive(p);b=route_bounds(p)
    assert d.lattice_count==33 and d.outer_crest_radius==19.5
    assert b['m']==1 and b['radial_bound']<=.004 and b['plateau_bound']>=1
    assert b['slope_bound']==pytest.approx(.89296875)
    longer=replace(p,cavity_length=p.cavity_length+p.skin_axial_pitch)
    assert derive(longer).body_band[0]==pytest.approx(d.body_band[0]-4.8)
    assert derive(longer).lattice_count==33
    for k in range(101):
        a=2*pi*k/100
        assert radius(p,'body',a,0)==radius(p,'cap',a,0)
        assert field(p,a,-5)==field(longer,a,-5)
        assert field(p,a,-5)==pytest.approx(field(p,a,-5+4.8))
        for role,z in [('body',d.body_band[0]),('cap',d.cap_band[1])]:
            assert radius(p,role,a,z)==pytest.approx(d.outer_valley_radius+p.skin_height*field(p,a,z)-.3)
    for role in ('body','cap'):
        assert len(list(skin_patches(p,role)))+2 <=6000


def test_seven_floor_only_tools_and_ligaments():
    """Catch accidentally drilled thread/sidewall and a center glyph over the drain."""
    p=Params();d=derive(p);centers=drain_centers(p)
    assert len(centers)==7 and centers[0]==(0,0)
    nearest=min(hypot(a[0]-b[0],a[1]-b[1]) for i,a in enumerate(centers) for b in centers[i+1:])
    assert nearest-p.drain_diameter==pytest.approx(6)
    assert d.body_inner_radius-p.drain_ring_radius-p.drain_diameter/2==4.5
    for role,z in [('body',-35.1),('cap',40.4)]:
        for cutter in drain_cutters(p,role):
            bb=cutter.bounding_box()
            assert (bb.min.Z,bb.max.Z)==pytest.approx((z-.01,z+3.01))


def test_written_topology_floors_holes_and_placements():
    """Catch filled drains, disconnected floors and duplicated STEP transforms."""
    from build123d import import_step
    p=Params();base=Path(__file__).parents[1]/'cad'/'p1_r5_39mm_case'
    shapes={n:import_step(str(base/(n+'.step'))) for n in ('body','cap_c25','closed_c25','print_layout')}
    for name,shape in shapes.items():
        assert shape.is_valid and shape.volume>0
        assert len(shape.solids())==(1 if name in ('body','cap_c25') else 2)
    for name,z0 in [('body',-35.1),('cap_c25',40.4)]:
        solid=shapes[name].solids()[0]
        for x,y in drain_centers(p):
            for dz in (.01,1.5,2.99):
                assert not solid.is_inside((x,y,z0+dz))
                assert not solid.is_inside((x+1.49,y,z0+dz))
                assert solid.is_inside((x+1.51,y,z0+dz))
        assert solid.is_inside((0,4,z0+1.5))
    assert shapes['body'].solids()[0].is_inside((0,4,-32.11))
    assert not shapes['body'].solids()[0].is_inside((0,4,-32.09))
    assert shapes['cap_c25'].solids()[0].is_inside((0,4,40.41))
    assert not shapes['cap_c25'].solids()[0].is_inside((0,4,40.39))
    for solid in shapes['print_layout'].solids():
        bb=solid.bounding_box();assert bb.min.Z==pytest.approx(0,abs=1e-5)
        center_x=(bb.min.X+bb.max.X)/2
        assert abs(center_x)==pytest.approx(23,abs=.01)
        assert not solid.is_inside((center_x,0,bb.max.Z-.1))
    bb=shapes['print_layout'].bounding_box()
    assert bb.max.Z==pytest.approx(44.1,abs=1e-5)
    assert bb.size.X<=85.02 and bb.size.Y<=39.02
    assert shapes['closed_c25'].bounding_box().size.Z==pytest.approx(78.5,abs=1e-5)


def test_written_selected_thread_sections_and_textured_end_bevel():
    """Detect stale R4 thread radii, radius-derived taper drift or circular end bands."""
    from build123d import import_step
    from p1_r5_39mm_case.thread_profile import male_radius,female_radius
    p=Params();d=derive(p);base=Path(__file__).parents[1]/'cad'/'p1_r5_39mm_case'
    body=import_step(str(base/'body.step')).solids()[0]
    cap=import_step(str(base/'cap_c25.step')).solids()[0]
    for theta in (0.,pi/3,.7):
        def pt(r,z):return (r*cos(theta),r*sin(theta),z)
        for z in (.5,1.5,2.45,4.15,7.5,8.5):
            rm=male_radius(p,theta,z);rf=female_radius(p,theta,z)
            assert body.is_inside(pt(rm-.015,z)) and not body.is_inside(pt(rm+.015,z))
            assert not cap.is_inside(pt(rf-.015,z)) and cap.is_inside(pt(rf+.015,z))
        for z in (9.5,10.1,11.3,12.5):
            rf=(d.thread_crest+p.thread_clearance if z<d.collar_end else
                d.cap_inner_radius if z>=d.cap_straight_start else
                d.thread_crest+p.thread_clearance-(z-d.collar_end)/d.taper_length*
                (d.thread_crest+p.thread_clearance-d.cap_inner_radius))
            assert not cap.is_inside(pt(rf-.015,z)) and cap.is_inside(pt(rf+.015,z))
        for solid,role,z in [(body,'body',-35.09),(body,'body',-34.85),
                             (body,'body',-34.6),(body,'body',-.01),
                             (cap,'cap',.01),(cap,'cap',43.39),(cap,'cap',43.15)]:
            r=radius(p,role,theta,z)
            assert solid.is_inside(pt(r-.015,z)) and not solid.is_inside(pt(r+.015,z))
