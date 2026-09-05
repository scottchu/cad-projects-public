"""R5 39mm full skin, new thread B, textured end bevels and seven floor drains."""
from dataclasses import replace
from functools import lru_cache
from math import cos,pi,sin
from time import monotonic
import json
import sys
from build123d import Axis,Color,Compound,CylindricalJoint,Location,Plane,RigidJoint,Solid
from .params import Params,derive,require
from .surface import build_outer_blank
from .thread_profile import female_void,male_neck,turned


def add_datums(part,p,role):
    d=derive(p)
    datums={'shoulder':0.,'tip':d.neck_height,'full_thread_start':d.full_thread_start,
            'full_thread_end':d.full_thread_end,'skin_phase':p.skin_phase_z,
            'bed':p.cap_height if role=='cap' else -d.body_depth-p.floor,
            'inner_floor':p.cap_height-p.floor if role=='cap' else -d.body_depth}
    for name,z in datums.items():RigidJoint(name,part,Location((0,0,z)))
    CylindricalJoint('screw_axis',part,Axis.Z,linear_range=(-.1,d.neck_height+2),angular_range=(-10,2500))
    return part


def drain_centers(p):
    """Original polar pattern: center plus six equally spaced floor openings."""
    return [(0.,0.)]+[(p.drain_ring_radius*cos(2*pi*k/p.drain_ring_count),
                       p.drain_ring_radius*sin(2*pi*k/p.drain_ring_count))
                      for k in range(p.drain_ring_count)]


def drain_cutters(p,role):
    """Axial cylinders span only floor plus .01mm at each end; no sidewall tool."""
    d=derive(p);require(role in ('body','cap'),'unknown role')
    z=d.body_band[0] if role=='body' else p.cap_height-p.floor
    return [Solid.make_cylinder(p.drain_diameter/2,p.floor+.02,
                               Plane(origin=(x,y,z-.01))) for x,y in drain_centers(p)]


@lru_cache(maxsize=6)
def build_body(p=Params()):
    d=derive(p);outer,_,report=build_outer_blank(p,'body')
    print(json.dumps({'stage':'body_outer',**report}),file=sys.stderr,flush=True)
    start=monotonic()
    bore=turned([(0,-d.body_depth),(d.body_inner_radius,-d.body_depth),
                 (d.body_inner_radius,d.neck_height),(0,d.neck_height)])
    body=outer.cut(bore).fuse(male_neck(p)).clean()
    body=body.cut(*drain_cutters(p,'body')).clean()
    require(body.is_valid and len(body.solids())==1 and body.volume>0,'invalid final body')
    body.label='R5 body: 39mm diamond skin; new B right-hand thread; beveled end with seven drains'
    body.color=Color('#7097b3')
    require(monotonic()-start<180,'body Boolean exceeded180seconds')
    print(json.dumps({'stage':'body_boolean','seconds':monotonic()-start,'volume':body.volume,'faces':len(body.faces())}),file=sys.stderr,flush=True)
    return add_datums(body,p,'body')


@lru_cache(maxsize=12)
def build_cap(p=Params()):
    outer,_,report=build_outer_blank(p,'cap')
    print(json.dumps({'stage':'cap_outer',**report}),file=sys.stderr,flush=True)
    start=monotonic()
    cap=outer.cut(female_void(p)).clean()
    cap=cap.cut(*drain_cutters(p,'cap')).clean()
    require(cap.is_valid and len(cap.solids())==1 and cap.volume>0,'invalid final cap')
    cap.label=f'R5 cap C{round(p.thread_clearance*100):02}: new B thread; 39mm diamond skin; seven drains'
    cap.color=Color({.2:'#da9773',.25:'#77b09a',.3:'#b291c8'}.get(p.thread_clearance,'#77b09a'))
    require(monotonic()-start<180,'cap Boolean exceeded180seconds')
    print(json.dumps({'stage':'cap_boolean','seconds':monotonic()-start,'volume':cap.volume,'faces':len(cap.faces())}),file=sys.stderr,flush=True)
    return add_datums(cap,p,'cap')


def build_assembly(p=Params(),beta_degrees=0.,gap=None):
    body=build_body(p).moved(Location());cap=build_cap(p).moved(Location())
    gap=p.thread_pitch*beta_degrees/360 if gap is None else gap
    body.joints['screw_axis'].connect_to(cap.joints['shoulder'],position=gap,angle=beta_degrees)
    return Compound(label=f'R5 new B threaded cylinder C{round(p.thread_clearance*100):02}; angle{beta_degrees:g}; gap{gap:g}',children=[body,cap])



def print_layout(p=Params()):
    d=derive(p);spacing=p.outer_diameter+7
    body=build_body(p).moved(Location((spacing/2,0,d.body_depth+p.floor)))
    cap=build_cap(p).moved(Location((-spacing/2,0,p.cap_height),(180,0,0)))
    return Compound(label=f'R5 body and C{round(p.thread_clearance*100)} cap; both openings up; two print objects',
                    children=[body,cap])
