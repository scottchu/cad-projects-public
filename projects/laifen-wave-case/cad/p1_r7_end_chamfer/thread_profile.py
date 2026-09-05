"""Original thread construction family, reparameterized to selected R7 thread B.

Scalar sections are defined only along the neck 0 <= z <= neck_height.
Tool overbuild is mathematically redundant, not functional thread material.
"""
from functools import lru_cache
from math import pi

try:
    from .params import Params, derive, require
except ImportError:
    from params import Params, derive, require

EMBED = .05
CLIP_OVERBUILD = .10


def infinite_radius(p, theta, z, clearance=0.0):
    q = (z-p.thread_pitch*theta/(2*pi)+p.thread_pitch/2) % p.thread_pitch-p.thread_pitch/2
    return p.body_bore/2+p.root_wall+clearance+max(0.,min(p.thread_height,
            (.425*p.thread_pitch-abs(q))*p.thread_height/(.35*p.thread_pitch)))


def male_radius(p, theta, z):
    T = 1.5*p.thread_pitch+p.engagement
    lead = p.thread_height/(.5*p.thread_pitch)
    envelope = 0 if z <= .5*p.thread_pitch else min(p.thread_height,lead*(z-.5*p.thread_pitch),lead*(T-z))
    return min(infinite_radius(p,theta,z),p.body_bore/2+p.root_wall+envelope)


def female_radius(p, theta, z, clearance=None):
    c = p.thread_clearance if clearance is None else clearance
    lead = p.thread_height/(.5*p.thread_pitch)
    envelope = (p.thread_height if z <= .5*p.thread_pitch else
                max(0.,lead*(p.thread_pitch-z),lead*(z-p.thread_pitch-p.engagement)))
    return max(infinite_radius(p,theta,z,c),p.body_bore/2+p.root_wall+c+envelope)


def polygon(points):
    from build123d import Vector, Wire
    return Wire.make_polygon([Vector(*p) for p in points],close=True)


def turned(rz):
    from build123d import Axis, Face, revolve
    return revolve(Face(polygon([(r,0,z) for r,z in rz])),axis=Axis.Z)


def one_shape(result):
    if isinstance(result,list):
        if len(result) != 1:
            raise ValueError(f"expected one connected shape, got {len(result)}")
        return result[0]
    return result


@lru_cache(maxsize=12)
def infinite_thread(p: Params, clearance=0.0):
    """Actual BREP sweep with new root/height and slope-derived tool overbuild."""
    from build123d import Face, Helix, sweep
    d = derive(p)
    root = d.thread_root+clearance
    z0 = -p.thread_pitch
    half_base = .425*p.thread_pitch+EMBED/d.thread_flank_slope
    wire = polygon([(root-EMBED,0,z0-half_base),
                    (d.thread_crest+clearance,0,z0-.075*p.thread_pitch),
                    (d.thread_crest+clearance,0,z0+.075*p.thread_pitch),
                    (root-EMBED,0,z0+half_base)])
    path = Helix(p.thread_pitch,d.neck_height+2.5*p.thread_pitch,root,
                 center=(0,0,z0),lefthand=False)
    ridge = sweep(Face(wire),path=path,is_frenet=True)
    core = turned([(0,-1.5*p.thread_pitch),(root,-1.5*p.thread_pitch),
                   (root,d.neck_height+2*p.thread_pitch),(0,d.neck_height+2*p.thread_pitch)])
    return core.fuse(ridge).clean()


def male_envelope(p):
    d = derive(p)
    dz = CLIP_OVERBUILD/d.thread_lead_slope
    return turned([(d.body_inner_radius,0),(d.thread_root,0),
                   (d.thread_root,.5*p.thread_pitch),
                   (d.thread_crest+CLIP_OVERBUILD,d.full_thread_start+dz),
                   (d.thread_crest+CLIP_OVERBUILD,d.full_thread_end-dz),
                   (d.thread_root,d.neck_height),(d.body_inner_radius,d.neck_height)])


def male_neck(p):
    """Intermediate trimmed neck; final body union must be validated separately."""
    return one_shape(infinite_thread(p).intersect(male_envelope(p)))


def female_void(p):
    """DES03: redundant tools begin at -pitch; outer blank owns the mouth plane."""
    d=derive(p);c=p.thread_clearance
    tool_bottom=-p.thread_pitch
    tool_radius=d.thread_crest+p.clearance_budget+CLIP_OVERBUILD
    threaded=one_shape(infinite_thread(p,c).intersect(turned([
        (0,tool_bottom),(tool_radius,tool_bottom),(tool_radius,d.neck_height),(0,d.neck_height)])))
    relief=turned([(0,tool_bottom),(d.thread_crest+c,tool_bottom),
                   (d.thread_crest+c,.5*p.thread_pitch),(d.thread_root+c,d.full_thread_start),
                   (d.thread_root+c,d.full_thread_end),(d.thread_crest+c,d.neck_height),
                   (d.thread_crest+c,d.collar_end),(d.cap_inner_radius,d.cap_straight_start),
                   (d.cap_inner_radius,p.cap_height-p.floor),(0,p.cap_height-p.floor)])
    result=threaded.fuse(relief).clean()
    require(result.volume>0 and len(result.solids())==1,
            'empty or disconnected female thread void: this parameter set has no validated BREP construction')
    return result


def untextured_cap(p):
    """Bounded diagnostic for female mouth quality before expensive skin Boolean."""
    d=derive(p)
    outer=turned([(0,0),(d.shoulder_radius,0),(d.shoulder_radius,d.collar_end),
                  (d.cap_radius,d.cap_straight_start),(d.cap_radius,p.cap_height-.3),
                  (d.cap_radius-.3,p.cap_height),(0,p.cap_height)])
    return outer.cut(female_void(p)).clean()
