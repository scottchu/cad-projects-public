"""R7 39mm full skin, new thread B, smooth circular end chamfers and seven floor drains."""
from functools import lru_cache
from time import monotonic
import json
import sys
from build123d import Axis,Color,CylindricalJoint,Location,Plane,RigidJoint,Solid
from .derive import require
from .surface import STAGE_SECONDS,build_outer_blank
from .thread import female_void,male_neck,turned
from .runout import normalize_female_runout
from .ends import apply_end_chamfer,normalize_end_trim


def add_datums(part,p,role):
    require(role in ('body','cap'),'unknown role')
    for name,z in getattr(p,role+'_datums'):RigidJoint(name,part,Location((0,0,z)))
    CylindricalJoint('screw_axis',part,Axis.Z,linear_range=(-.1,p.neck_height+2),angular_range=(-10,2500))
    return part


def drain_centers(p):
    """Original polar pattern: center plus six equally spaced floor openings."""
    return list(p.drain_centers)


def drain_cutters(p,role):
    """Axial cylinders span only floor plus .01mm at each end; no sidewall tool."""
    require(role in ('body','cap'),'unknown role')
    z=p.body_band[0] if role=='body' else p.cap_cavity_length
    return [Solid.make_cylinder(p.drain_diameter/2,p.floor+.02,
                               Plane(origin=(x,y,z-.01))) for x,y in drain_centers(p)]


@lru_cache(maxsize=6)
def build_body(p):
    d=p;outer,_,report=build_outer_blank(p,'body')
    print(json.dumps({'stage':'body_outer',**report}),file=sys.stderr,flush=True)
    return body_from_outer(p,outer)


def body_from_outer(p,outer):
    d=p;start=monotonic()
    outer=apply_end_chamfer(outer,p,'body')
    bore=turned([(0,-d.body_depth),(d.body_inner_radius,-d.body_depth),
                 (d.body_inner_radius,d.neck_height),(0,d.neck_height)])
    body=outer.cut(bore).fuse(male_neck(p)).clean()
    body=body.cut(*drain_cutters(p,'body')).clean()
    body=normalize_end_trim(body,p,'body')
    require(body.is_valid and len(body.solids())==1 and body.volume>0,'invalid final body')
    body.label='R7 body: 39mm diamond skin; new B right-hand thread; smooth chamfer with seven drains'
    body.color=Color('#7097b3')
    require(monotonic()-start<STAGE_SECONDS,'body Boolean exceeded600seconds')
    print(json.dumps({'stage':'body_boolean','seconds':monotonic()-start,'volume':body.volume,'faces':len(body.faces())}),file=sys.stderr,flush=True)
    return add_datums(body,p,'body')


@lru_cache(maxsize=12)
def build_cap(p):
    outer,_,report=build_outer_blank(p,'cap')
    print(json.dumps({'stage':'cap_outer',**report}),file=sys.stderr,flush=True)
    return cap_from_outer(p,outer)


def cap_from_outer(p,outer):
    start=monotonic()
    outer=apply_end_chamfer(outer,p,'cap')
    cap=outer.cut(female_void(p)).clean()
    cap=cap.cut(*drain_cutters(p,'cap')).clean()
    cap=normalize_female_runout(cap,p)
    cap=normalize_end_trim(cap,p,'cap')
    require(cap.is_valid and len(cap.solids())==1 and cap.volume>0,'invalid final cap')
    cap.label=f'R7 cap C{round(p.thread_clearance*100):02}: new B thread; 39mm diamond skin; smooth end chamfer; seven drains'
    cap.color=Color({.2:'#da9773',.25:'#77b09a',.3:'#b291c8'}.get(p.thread_clearance,'#77b09a'))
    require(monotonic()-start<STAGE_SECONDS,'cap Boolean exceeded600seconds')
    print(json.dumps({'stage':'cap_boolean','seconds':monotonic()-start,'volume':cap.volume,'faces':len(cap.faces())}),file=sys.stderr,flush=True)
    return add_datums(cap,p,'cap')

