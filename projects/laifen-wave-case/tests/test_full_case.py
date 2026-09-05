"""Focused full-case regressions for derived dimensions and written full geometry."""
from dataclasses import fields,replace
from math import pi
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).parents[1]/'cad'))
from p1_r6_full_case.params import Params,derive
from p1_r6_full_case.skin import field
from p1_r6_full_case.surface import check_patch_budget,route_bounds
from p1_r6_full_case.parts import drain_centers
from p1_r6_full_case.review import device_envelope,device_readouts


def test_full_lengths_fixed_bores_reference_and_unscaled_pattern():
    """Catch short substitution, duplicate editable lengths or implicit bore widening."""
    p=Params();d=derive(p);r=device_readouts(p)
    assert p.cavity_length==213 and p.cap_height==84 and d.body_depth==132
    assert d.body_band==(-135,0) and d.cap_band==(0,84)
    assert d.outer_length==219 and d.neck_height==9
    assert r['body_cavity']+r['cap_cavity']-r['overlap']==213
    assert (r['device_lower_z'],r['device_upper_z'],r['bottom_gap'],r['top_gap'])==(-129.5,78.5,2.5,2.5)
    resting=device_readouts(p,'bottom-resting')
    assert (resting['device_lower_z'],resting['device_upper_z'],resting['bottom_gap'],resting['top_gap'])==(-132,76,0,5)
    assert r['reference_only'] and not r['retained']
    assert (d.body_straight_wall,d.cap_straight_wall)==pytest.approx((4.05,3.55))
    assert (d.body_radial_gap,d.cap_radial_gap)==(.5,1.)
    assert not {'cavity_length','cap_height','wall'}&{f.name for f in fields(p)}
    bigger=replace(p,device_diameter=32);bd=derive(bigger)
    assert (bigger.body_bore,bigger.cap_bore)==(30,31)
    assert (bd.body_radial_gap,bd.cap_radial_gap)==(-1,-.5)
    longer=replace(p,device_length=p.device_length+4.8);ld=derive(longer)
    assert ld.body_depth==pytest.approx(d.body_depth+4.8)
    assert longer.cap_height==84 and ld.lattice_count==33
    for theta,z in [(0,-100),(.3,-5),(pi,30)]:
        assert field(p,theta,z)==field(longer,theta,z)
        assert field(p,theta,z)==pytest.approx(field(p,theta,z+4.8))
    for change in [dict(device_length=0),dict(device_diameter=-1),dict(axial_allowance=2),dict(cap_cavity_length=1)]:
        with pytest.raises(ValueError):derive(replace(p,**change))
    env=device_envelope(p);bb=env.bounding_box()
    assert env.is_valid and len(env.solids())==1
    assert (bb.min.Z,bb.max.Z,bb.size.X)==pytest.approx((-129.5,78.5,29))
    assert set(env.joints)=={'device_lower','device_upper'}


def test_full_polygon_budget_and_preserved_radial_thread():
    """Catch runaway full topology or accidental changes to frozen R5 radial equations."""
    from p1_r5_39mm_case.params import Params as PreviousParams
    from p1_r5_39mm_case.thread_profile import male_radius as old_male,female_radius as old_female
    from p1_r6_full_case.thread_profile import male_radius,female_radius
    p=Params();d=derive(p);old=PreviousParams()
    assert check_patch_budget(p)=={'body':10562,'cap':6569}
    assert d.female_minimum_wall==pytest.approx(1.85)
    assert (d.thread_root,d.thread_crest,d.cap_straight_start)==pytest.approx((16.4,16.9,12.4))
    route=route_bounds(p)
    assert route['radial_bound']<=.004 and route['plateau_bound']>=1
    assert route['slope_bound']==pytest.approx(.89296875)
    for theta,z in [(0,.5),(.6,1.5),(1.2,2.4),(pi,7.6),(3.8,8.5)]:
        assert male_radius(p,theta,z)==old_male(old,theta,z)
        assert female_radius(p,theta,z)==old_female(old,theta,z)


def test_written_full_solids_drains_bores_and_two_part_outputs():
    """Catch malformed long shells, misplaced floors/holes, reference leakage or transforms."""
    from build123d import import_step
    p=Params();base=Path(__file__).parents[1]/'cad'/'p1_r6_full_case'
    shapes={name:import_step(str(base/(name+'.step'))) for name in ('body','cap_c25','closed_c25','print_layout')}
    for name,shape in shapes.items():
        assert shape.is_valid and shape.volume>0
        assert len(shape.solids())==(1 if name in ('body','cap_c25') else 2)
    body=shapes['body'].solids()[0];cap=shapes['cap_c25'].solids()[0]
    for solid,z0 in [(body,-135),(cap,81)]:
        for x,y in drain_centers(p):
            for dz in (.01,1.5,2.99):
                assert not solid.is_inside((x,y,z0+dz))
                assert not solid.is_inside((x+1.49,y,z0+dz))
                assert solid.is_inside((x+1.51,y,z0+dz))
        assert solid.is_inside((0,4,z0+1.5))
    for z in (-131.9,-100.,-50.,-.1):
        assert not body.is_inside((14.99,0,z)) and body.is_inside((15.01,0,z))
    for z in (12.5,45.,80.9):
        assert not cap.is_inside((15.49,0,z)) and cap.is_inside((15.51,0,z))
    assert body.is_inside((0,4,-132.01)) and not body.is_inside((0,4,-131.99))
    assert cap.is_inside((0,4,81.01)) and not cap.is_inside((0,4,80.99))
    assert body.bounding_box().size.Z==pytest.approx(144,abs=1e-5)
    assert cap.bounding_box().size.Z==pytest.approx(84,abs=1e-5)
    closed=shapes['closed_c25'].bounding_box()
    assert closed.size.Z==pytest.approx(219,abs=1e-5)
    assert closed.size.X<=39.02 and closed.size.Y<=39.02
    heights=[]
    for part in shapes['print_layout'].solids():
        bb=part.bounding_box();heights.append(bb.max.Z)
        assert bb.min.Z==pytest.approx(0,abs=1e-5)
        center=(bb.min.X+bb.max.X)/2
        assert abs(center)==pytest.approx(23,abs=.01)
        assert not part.is_inside((center,0,bb.max.Z-.1))
    assert sorted(heights)==pytest.approx([84,144],abs=1e-5)
    layout=shapes['print_layout'].bounding_box()
    assert layout.size.X<=85.02 and layout.size.Y<=39.02


def test_native_runout_trim_regression_and_tool_isolation():
    """Catch the real tolerance-covered runout endpoint fault before expensive skins."""
    from p1_r6_full_case.thread_profile import female_void
    from p1_r6_full_case.runout import normalize_female_runout,runout_endpoint_mismatches
    p=Params();raw=female_void(p)
    defects=runout_endpoint_mismatches(raw,p)
    assert len(defects)==1 and defects[0]['residual']>.002
    corrected=normalize_female_runout(raw,p)
    assert corrected.is_valid and len(corrected.solids())==1
    assert not runout_endpoint_mismatches(corrected,p,threshold=1e-7)
    # The actual source tool must stay raw; normalization may not mutate cached
    # geometry used by other occurrences or hide the regression in-place.
    assert runout_endpoint_mismatches(raw,p)[0]['residual']==defects[0]['residual']


def test_repaired_cap_source_written_parity():
    """Catch STEP normalizing an inconsistent native trim into a different volume."""
    from build123d import import_step
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from p1_r6_full_case.parts import build_cap
    from p1_r6_full_case.runout import runout_endpoint_mismatches
    p=Params();source=build_cap(p)
    assert source.is_valid and not runout_endpoint_mismatches(source,p)
    written=import_step(str(Path(__file__).parents[1]/'cad/p1_r6_full_case/cap_c25.step'))
    assert written.is_valid and len(written.solids())==1
    volumes=[]
    for shape in (source,written):
        props=GProp_GProps()
        BRepGProp.VolumeProperties_s(shape.wrapped,props,1e-10,True,False)
        volumes.append(props.Mass())
    print({'source_volume':volumes[0],'written_volume':volumes[1],
           'absolute_delta':abs(volumes[0]-volumes[1]),'gate':.001,'eps':1e-10})
    assert abs(volumes[0]-volumes[1])<=.001,volumes
