"""Actual short threaded-cylinder parts, joints and print transforms."""
from dataclasses import replace
from functools import lru_cache
from build123d import Axis,Color,Compound,CylindricalJoint,Face,Location,RigidJoint,Solid
from .params import Params,derive,require
from .surface import build_outer_blank
from .thread_profile import female_void,male_neck,polygon,turned


def add_datums(part,p,role):
    d=derive(p)
    datums={'shoulder':0.,'tip':d.neck_height,'full_thread_start':d.full_thread_start,
            'full_thread_end':d.full_thread_end,'skin_phase':p.skin_phase_z,
            'bed':p.cap_height if role=='cap' else -d.body_depth-p.floor,
            'inner_floor':p.cap_height-p.floor if role=='cap' else -d.body_depth}
    for name,z in datums.items():RigidJoint(name,part,Location((0,0,z)))
    CylindricalJoint('screw_axis',part,Axis.Z,linear_range=(-.1,d.neck_height+2),angular_range=(-10,2500))
    return part


def label_cutters(p):
    """Original seven-segment marks recessed0.20 away from the nominal cavity."""
    if p.thread_clearance not in (.20,.25,.30):return []
    z=p.cap_height-p.floor
    segments={'a':(0,3.2,2.2,.6),'g':(0,1.6,2.2,.6),'d':(0,0,2.2,.6),
              'f':(0,1.9,.6,1.6),'b':(1.6,1.9,.6,1.6),'e':(0,.3,.6,1.6),'c':(1.6,.3,.6,1.6)}
    glyphs={'0':'abcdef','2':'abged','3':'abgcd','5':'afgcd'}
    require(p.floor-.2>=1.8-1e-10,'recessed label leaves less than1.8mm floor')
    cutters=[]
    for index,char in enumerate(f'{round(p.thread_clearance*100):02}'):
        for seg in glyphs[char]:
            x,y,w,h=segments[seg];x+=index*3-2.6;y-=1.9
            y=-y-h  # Rx180 print pose restores upright glyph Y for viewing into opening.
            face=Face(polygon([(x,y,z-.001),(x+w,y,z-.001),(x+w,y+h,z-.001),(x,y+h,z-.001)]))
            cutters.append(Solid.extrude(face,(0,0,.201)))
    return cutters


@lru_cache(maxsize=6)
def build_body(p=Params()):
    d=derive(p);outer,_,_=build_outer_blank(p,'body')
    bore=turned([(0,-d.body_depth),(d.body_inner_radius,-d.body_depth),
                 (d.body_inner_radius,d.neck_height),(0,d.neck_height)])
    body=outer.cut(bore).fuse(male_neck(p)).clean()
    require(body.is_valid and len(body.solids())==1 and body.volume>0,'invalid final body')
    body.label='Body: closed floor; original right-hand thread; continuous diamond skin'
    body.color=Color('#7097b3')
    return add_datums(body,p,'body')


@lru_cache(maxsize=12)
def build_cap(p=Params()):
    outer,_,_=build_outer_blank(p,'cap')
    cap=outer.cut(female_void(p)).clean()
    cutters=label_cutters(p)
    if cutters:cap=cap.cut(*cutters).clean()
    require(cap.is_valid and len(cap.solids())==1 and cap.volume>0,'invalid final cap')
    cap.label=f'Cap C{p.thread_clearance:g}: recessed clearance mark; continuous diamond skin'
    cap.color=Color({.2:'#da9773',.25:'#77b09a',.3:'#b291c8'}.get(p.thread_clearance,'#77b09a'))
    return add_datums(cap,p,'cap')


def build_assembly(p=Params(),beta_degrees=0.,gap=None):
    body=build_body(p).moved(Location());cap=build_cap(p).moved(Location())
    gap=p.thread_pitch*beta_degrees/360 if gap is None else gap
    body.joints['screw_axis'].connect_to(cap.joints['shoulder'],position=gap,angle=beta_degrees)
    return Compound(label=f'Original threaded cylinder C{p.thread_clearance:g}; angle{beta_degrees:g}; gap{gap:g}',children=[body,cap])


def build_coupon_set(p=Params()):
    require(p.clearance_budget>=.3,'all three coupon caps require clearance_budget>=0.30')
    return {'body':build_body(p),**{f'cap_c{round(c*100)}':build_cap(replace(p,thread_clearance=c)) for c in (.2,.25,.3)}}


def print_layout(p=Params()):
    d=derive(p);spacing=2*d.shoulder_radius+7
    children=[]
    for (role,part),(x,y) in zip(build_coupon_set(p).items(),((-1,-1),(1,-1),(-1,1),(1,1))):
        loc=Location((0,0,d.body_depth+p.floor)) if role=='body' else Location((0,0,p.cap_height),(180,0,0))
        children.append(part.moved(loc).moved(Location((x*spacing/2,y*spacing/2,0))))
    return Compound(label='Body plus C20 C25 C30; open sides up; separate print objects',children=children)
