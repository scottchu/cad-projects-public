"""Focused regressions for the concrete seam-key/temporary-patch defect."""
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).parents[1]/'cad'))
from p1_r3_generator.params import Params
from p1_r3_generator.surface import Patch,build_patch,cleanup_perimeter,vertex_key


def test_periodic_identity_and_duplicate_cleanup():
    for u in (-31.,-5e-13,0.,5e-13,31.,30.25):
        key=vertex_key('outer',u,3.82,31)
        assert key==vertex_key('outer',u+31,3.82,31)
        assert key==vertex_key('outer',key[1],key[2],31)
    assert vertex_key('outer',-5e-13,3.82,31)[1]==0
    keys=[('outer',0.,0.),('outer',0.,0.),('outer',1.,0.),('outer',1.,1.),('outer',0.,1.)]
    p=Patch((),[(0,0),(0,0),(1,0),(1,1),(0,1)],keys,'witness')
    cleanup_perimeter(p)
    assert p.polygon==[(0,0),(1,0),(1,1),(0,1)]
    assert len(p.deferred_duplicates)==1
    # Distinct local UV endpoints remain even with the same logical seam key.
    p=Patch((),[(0,0),(1,0),(1,1),(0,1)],[keys[0],keys[0],keys[3],keys[4]],'seam')
    cleanup_perimeter(p)
    assert len(p.polygon)==4


def test_closed_patch_actual_geometry():
    solid,builder,report=build_patch(Params())
    assert solid.is_valid and solid.volume>0 and len(solid.solids())==1
    assert report['faces']<=128 and report['seconds']<60
    assert set(builder.uses.values())=={2}
    assert report['maximum_radial_error']<=.01
    assert report['maximum_normal_slope']<=1
    assert report['actual_plateau_width_lower_bound']>=1
    assert report['smooth_radius_error']<1e-8


def test_written_solids_floors_and_print_pose_labels():
    """Catch missing floors, malformed outputs, raised/reversed clearance marks."""
    from build123d import import_step,Location
    from p1_r3_generator.params import derive
    p=Params();d=derive(p);base=Path(__file__).parents[1]/'cad'/'p1_r3_generator'
    body=import_step(str(base/'body.step'))
    assert body.is_valid and len(body.solids())==1 and body.volume>0
    solid=body.solids()[0]
    assert solid.is_inside((8,0,-d.body_depth-.01))
    assert not solid.is_inside((8,0,-d.body_depth+.01))
    segments={'a':(1.1,3.5),'g':(1.1,1.9),'d':(1.1,.3),'f':(.3,2.7),
              'b':(1.9,2.7),'e':(.3,1.1),'c':(1.9,1.1)}
    glyphs={'0':'abcdef','2':'abged','3':'abgcd','5':'afgcd'}
    for clearance in (20,25,30):
        cap=import_step(str(base/f'cap_c{clearance}.step'))
        assert cap.is_valid and len(cap.solids())==1 and cap.volume>0
        cs=cap.solids()[0]
        assert not cs.is_inside((8,0,p.cap_height-p.floor-.01))
        assert cs.is_inside((8,0,p.cap_height-p.floor+.01))
        printed=cap.moved(Location((0,0,p.cap_height),(180,0,0))).solids()[0]
        for index,char in enumerate(str(clearance)):
            for segment,(x,y) in segments.items():
                point=(x+index*3-2.6,y-1.9,p.floor-.1)
                assert printed.is_inside(point)==(segment not in glyphs[char]),(clearance,segment,point)
        assert min(v.Z for v in cap.vertices())>=-1e-4
        assert max(v.Z for v in cap.vertices())<=p.cap_height+1e-4
    for name,count in (('closed_c25',2),('exploded_c25',2),('print_layout',4)):
        assembly=import_step(str(base/(name+'.step')))
        assert assembly.is_valid and len(assembly.solids())==count


def test_written_actual_screw_path_and_stop():
    """Catch the original filled-valley collision on complete exported parts."""
    from build123d import import_step,Location
    base=Path(__file__).parents[1]/'cad'/'p1_r3_generator';body=import_step(str(base/'body.step'))
    def volume(shape):
        if shape is None:return 0.
        if isinstance(shape,list):return sum(x.volume for x in shape)
        return shape.volume
    for c in (20,25,30):
        cap=import_step(str(base/f'cap_c{c}.step'))
        for beta in (0,15,45,90,180,360,720,1080,1440,1620):
            moved=cap.moved(Location((0,0,2*beta/360),(0,0,beta)))
            interference=volume(body.intersect(moved))
            print('written_screw_pose',c,beta,interference,flush=True)
            assert interference<=1e-6,(c,beta,interference)
        for gap in (9,10,11):
            assert volume(body.intersect(cap.moved(Location((0,0,gap),(0,0,1620)))))<=1e-6
        assert volume(body.intersect(cap.moved(Location((0,0,-.02),(0,0,-3.6)))))>.1


def test_empty_changed_pitch_void_is_rejected():
    """Regression: the p2.4/E7.2 Boolean must never silently yield a filled cap."""
    from dataclasses import replace
    import pytest
    from p1_r3_generator.thread_profile import female_void
    p=replace(Params(),thread_pitch=2.4,engagement=7.2,cavity_length=82.1,cap_height=47)
    with pytest.raises(ValueError,match='female thread void'):
        female_void(p)
