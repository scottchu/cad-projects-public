"""One end-local 45-degree annular cutter; raw diamond geometry stays unscaled."""
from time import monotonic
import json
import sys
from build123d import Plane,Solid
from .derive import require

CUTTER_EPSILON=.01


def end_chamfer_radius(p,t):
    """Nominal conical radius at inward distance t from the closed outer end."""
    return p.outer_crest_radius-p.end_chamfer_size+t


def end_chamfer_cutter(p,role):
    d=p;require(role in ('body','cap'),'unknown end role')
    end=d.body_band[0] if role=='body' else d.cap_band[1]
    direction=1 if role=='body' else -1
    # Extend both limits by .01mm. The cone continues the SAME line, so its
    # radii at t=0 and t=c remain R-c and R. Outer overshoot is radial only.
    eps=CUTTER_EPSILON;c=p.end_chamfer_size
    plane=Plane(origin=(0,0,end-direction*eps),z_dir=(0,0,direction))
    outside=Solid.make_cylinder(d.outer_crest_radius+1,c+2*eps,plane)
    core=Solid.make_cone(end_chamfer_radius(p,-eps),end_chamfer_radius(p,c+eps),c+2*eps,plane)
    cutter=outside.cut(core)
    require(cutter.is_valid and len(cutter.solids())==1,'invalid annular end cutter')
    return cutter


def apply_end_chamfer(outer,p,role):
    start=monotonic()
    result=outer.cut(end_chamfer_cutter(p,role)).clean()
    require(result.is_valid and len(result.solids())==1 and result.volume>0,'invalid end-chamfered blank')
    print(json.dumps({'stage':role+'_end_chamfer','size':p.end_chamfer_size,
                      'end_radius':end_chamfer_radius(p,0),'seconds':monotonic()-start}),file=sys.stderr,flush=True)
    return result
