"""R4 full-sidewall skin; original fitted functional dimensions are isolated."""
from dataclasses import asdict, dataclass, fields, replace
from hashlib import sha256
import json
from math import floor, hypot, isfinite, pi


@dataclass(frozen=True)
class Params:
    cavity_length: float = 72.5
    cap_height: float = 43.4
    body_bore: float = 30.0
    cap_bore: float = 31.0
    wall: float = 2.4  # Legacy functional reference, not new outside wall.
    floor: float = 3.0
    thread_pitch: float = 2.0
    engagement: float = 6.0
    thread_clearance: float = 0.25
    clearance_budget: float = 0.30
    thread_height: float = 0.6
    root_wall: float = 1.8
    outer_diameter: float = 40.0
    skin_axial_pitch: float = 4.8
    skin_arc_pitch_target: float = 3.63
    skin_height: float = 0.45
    plateau_half_fraction: float = 0.18
    skin_phase_theta: float = 0.0
    skin_phase_z: float = 0.0
    bed_relief_radial: float = 0.20
    bed_relief_axial: float = 0.30
    skin_style: str = 'diamond'


@dataclass(frozen=True)
class Derived:
    body_inner_radius: float
    cap_inner_radius: float
    body_radius: float  # Original functional reference radius.
    cap_radius: float  # Original functional reference radius.
    thread_root: float
    thread_crest: float
    shoulder_radius: float  # Original positive-stop annulus reference.
    neck_height: float
    full_thread_start: float
    full_thread_end: float
    collar_end: float
    taper_length: float
    cap_straight_start: float
    body_depth: float
    outer_crest_radius: float
    outer_valley_radius: float
    body_band: tuple[float, float]
    cap_band: tuple[float, float]
    lattice_count: int
    arc_pitch: float
    plateau_width: float
    skin_slope_bound: float
    relief_slope_bound: float
    thread_flank_slope: float
    thread_lead_slope: float
    outer_length: float
    female_minimum_wall: float
    minimum_wall: float


def require(condition, message):
    if not condition:
        raise ValueError(message)


def derive(p: Params) -> Derived:
    for f in fields(p):
        value = getattr(p, f.name)
        if f.name != 'skin_style':
            require(isinstance(value, (float, int)) and not isinstance(value, bool)
                    and isfinite(value), f'{f.name} must be finite')
    require(p.skin_style == 'diamond', 'R4 supports diamond skin only')
    # This release intentionally preserves the fitted p2/E6 and bore geometry.
    for name, value in dict(body_bore=30., cap_bore=31., wall=2.4, floor=3.,
                            thread_pitch=2., engagement=6., thread_height=.6,
                            root_wall=1.8, clearance_budget=.30).items():
        require(getattr(p, name) == value, f'R4 fitted functional parameter {name} is locked at {value}')
    require(.20 <= p.thread_clearance <= .30, 'thread_clearance must be in [.20,.30]')
    require(0 < p.skin_height <= .6, 'skin_height must be in (0,.6]')
    require(3 <= p.skin_axial_pitch <= 8, 'skin_axial_pitch must be in [3,8]')
    require(0 < p.plateau_half_fraction < .5, 'invalid plateau fraction')
    require(p.skin_arc_pitch_target > 0, 'arc pitch target must be positive')
    require(0 < p.bed_relief_axial <= .3 and 0 <= p.bed_relief_radial <= .2,
            'bed relief must remain within the .20 radial/.30 axial design allowance')
    rb, rc = p.body_bore/2, p.cap_bore/2
    Rb, Rc = rb+p.wall, rc+p.wall
    root = rb+p.root_wall
    crest = root+p.thread_height
    Rs = max(Rb,Rc,crest+p.clearance_budget+1.8)
    T = 1.5*p.thread_pitch+p.engagement
    J = T+.6*p.thread_pitch
    Q = max(Rs-Rc,crest+p.clearance_budget-rc,.2)
    A = J+Q  # Exactly the original functional taper: 12.4 at defaults.
    B = p.cavity_length-(p.cap_height-p.floor)
    require(B > p.floor and p.cap_height > A+p.floor, 'cavity/cap length leaves no useful shell')
    require(p.cavity_length <= 300 and p.cap_height <= 300, 'length exceeds bounded domain')
    Rcrest = p.outer_diameter/2
    Rvalley = Rcrest-p.skin_height
    female_wall = Rvalley-crest-p.clearance_budget
    require(female_wall >= 1.8-1e-10, 'outer diameter leaves female ligament below1.8mm')
    require(p.outer_diameter <= 80, 'outer diameter exceeds bounded domain')
    N = floor(2*pi*Rvalley/p.skin_arc_pitch_target+.5)
    require(8 <= N <= 128, 'lattice count must be in [8,128]')
    arc = 2*pi*Rvalley/N
    width = 2*p.plateau_half_fraction*arc*p.skin_axial_pitch/hypot(arc,p.skin_axial_pitch)
    require(width >= 1, 'developed plateau width below1mm')
    slope = p.skin_height/(p.skin_axial_pitch*(.5-p.plateau_half_fraction))
    relief_slope = slope+p.bed_relief_radial/p.bed_relief_axial
    require(relief_slope <= 1, 'textured relief slope exceeds45degrees')
    require(abs(p.skin_phase_theta*N/(2*pi)) < 2**40
            and abs(p.skin_phase_z/p.skin_axial_pitch) < 2**40, 'unresolvable phase')
    return Derived(rb,rc,Rb,Rc,root,crest,Rs,T,p.thread_pitch,p.thread_pitch+p.engagement,
                   J,Q,A,B,Rcrest,Rvalley,(-B-p.floor,0.),(0.,p.cap_height),N,arc,width,
                   slope,relief_slope,p.thread_height/(.35*p.thread_pitch),
                   p.thread_height/(.5*p.thread_pitch),p.cavity_length+2*p.floor,
                   female_wall,min(p.root_wall,female_wall))


def preset(name='short-grip', **overrides):
    require(name in ('short-grip','generic'), 'full Laifen remains outside R4 short experiment')
    return replace(Params(), **overrides)


def parameter_fingerprint(p):
    return sha256(json.dumps(asdict(p),sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
