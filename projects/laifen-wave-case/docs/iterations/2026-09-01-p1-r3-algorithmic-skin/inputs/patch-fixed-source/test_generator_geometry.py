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
