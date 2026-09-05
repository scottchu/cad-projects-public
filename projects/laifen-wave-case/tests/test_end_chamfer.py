"""Focused R7 regression: scalloped closed ends and a real editable chamfer."""
from dataclasses import fields,replace
from math import pi
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).parents[1]/'cad'))
from p1_r7_end_chamfer.params import Params,derive
from p1_r7_end_chamfer.chamfer import end_chamfer_cutter,end_chamfer_radius


def test_chamfer_domain_law_and_replaced_scalloped_end():
    from p1_r6_full_case.params import Params as OldParams,derive as old_derive
    from p1_r6_full_case.skin import radius as old_radius
    from p1_r7_end_chamfer import skin
    from p1_r7_end_chamfer.surface import check_patch_budget
    p=Params();d=derive(p)
    assert p.end_chamfer_size==1.2
    assert not {'bed_relief_radial','bed_relief_axial'}&{f.name for f in fields(p)}
    assert not hasattr(skin,'relief')
    for size in (.8,1.2,1.5):
        q=replace(p,end_chamfer_size=size);e=derive(q)
        assert e.end_chamfer_axial_height==size and e.end_chamfer_slope==1
        assert e.end_chamfer_smooth_band==pytest.approx(size-p.skin_height)
        assert e.cap_end_radial_material>=2.5
        assert end_chamfer_radius(q,size)-end_chamfer_radius(q,0)==pytest.approx(size)
    for size in (.799999,1.500001,float('nan')):
        with pytest.raises(ValueError):derive(replace(p,end_chamfer_size=size))
    old=OldParams();od=old_derive(old)
    scallops=[old_radius(old,'body',a,od.body_band[0]) for a in (0,pi/od.lattice_count)]
    assert abs(scallops[0]-scallops[1])>.05  # Actual reported old source defect.
    assert end_chamfer_radius(p,0)==pytest.approx(18.3)
    for field in ('body_inner_radius','cap_inner_radius','thread_root','thread_crest','neck_height',
                  'full_thread_start','full_thread_end','collar_end','cap_straight_start','body_depth',
                  'outer_crest_radius','lattice_count','arc_pitch','outer_length'):
        assert getattr(d,field)==getattr(od,field)
    assert p.cavity_length==213 and p.cap_height==84
    assert (p.skin_axial_pitch,p.skin_phase_theta,p.skin_phase_z)==(4.8,0.,0.)
    assert sum(check_patch_budget(p).values())<=26000


def test_end_cutters_cannot_reach_floor_bore_or_joint():
    p=Params(end_chamfer_size=1.5);d=derive(p)
    for role in ('body','cap'):
        cutter=end_chamfer_cutter(p,role);bb=cutter.bounding_box()
        assert cutter.is_valid
        if role=='body':assert bb.max.Z < -d.body_depth
        else:assert bb.min.Z > p.cap_height-p.floor
        assert bb.size.Z==pytest.approx(1.52,abs=1e-6)
        # Even its most recessed overshoot stays outside the largest cavity.
        assert end_chamfer_radius(p,-.01)>d.cap_inner_radius
