"""Immutable generic-cylinder inputs and the R3 derived design constraints (mm)."""
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
    wall: float = 2.4
    floor: float = 3.0
    thread_pitch: float = 2.0
    engagement: float = 6.0
    thread_clearance: float = 0.25
    clearance_budget: float = 0.30
    thread_height: float = 0.6
    root_wall: float = 1.8
    max_od: float = 39.0
    skin_axial_pitch: float = 4.8
    skin_arc_pitch_target: float = 3.63
    skin_height: float = 0.45
    plateau_half_fraction: float = 0.18
    skin_phase_theta: float = 0.0
    skin_phase_z: float = 0.0
    smooth_margin: float = 2.0
    fade_length: float = 2.0
    min_grip_band: float = 24.0
    skin_style: str = "diamond"


@dataclass(frozen=True)
class Derived:
    body_inner_radius: float
    cap_inner_radius: float
    body_radius: float
    cap_radius: float
    thread_root: float
    thread_crest: float
    shoulder_radius: float
    neck_height: float
    full_thread_start: float
    full_thread_end: float
    collar_end: float
    taper_length: float
    cap_straight_start: float
    body_flange: float
    body_flare: float
    body_depth: float
    body_band: tuple[float, float]
    cap_band: tuple[float, float]
    minimum_cavity_length: float
    cap_height_range: tuple[float, float]
    lattice_count: int
    body_arc_pitch: float
    cap_arc_pitch: float
    body_plateau_width: float
    cap_plateau_width: float
    skin_slope_bound: float
    thread_flank_slope: float
    thread_lead_slope: float
    outer_length: float
    minimum_wall: float


def require(condition, message):
    if not condition:
        raise ValueError(message)


def derive(p: Params) -> Derived:
    """Reject unsupported/infeasible input before any expensive solid work."""
    for f in fields(p):
        value = getattr(p, f.name)
        if f.name != "skin_style":
            require(isinstance(value, (float, int)) and not isinstance(value, bool)
                    and isfinite(value), f"{f.name} must be finite")
    for name, lo, hi in (("body_bore",20,40),("cap_bore",20,40),
                         ("wall",1.8,4),("floor",2,5),("thread_pitch",1.8,3.2),
                         ("thread_height",.3,.6),("root_wall",1.8,3),
                         ("thread_clearance",.2,.3),("skin_axial_pitch",3,8)):
        value = getattr(p, name)
        require(lo <= value <= hi, f"{name}: {lo} <= {value} <= {hi} required")
    for name, hi in (("cavity_length",300),("cap_height",300),("max_od",80),
                     ("skin_height",.6)):
        require(0 < getattr(p,name) <= hi, f"0 < {name} <= {hi} required")
    require(2*p.thread_pitch <= p.engagement <= 4*p.thread_pitch,
            "engagement must satisfy 2*p <= E <= 4*p")
    require(p.clearance_budget >= p.thread_clearance,
            "clearance_budget >= thread_clearance required")
    require(0 < p.plateau_half_fraction < .5, "0 < plateau_half_fraction < 0.5 required")
    require(p.skin_arc_pitch_target > 0, "skin_arc_pitch_target > 0 required")
    require(p.smooth_margin >= 2 and p.fade_length >= 2,
            "smooth_margin >= 2 and fade_length >= 2 required")
    require(p.min_grip_band > 0, "min_grip_band > 0 required")
    require(p.skin_style in ("diamond", "smooth_crosswave"), "unknown skin_style")
    rb,rc = p.body_bore/2,p.cap_bore/2
    Rb,Rc = rb+p.wall,rc+p.wall
    root = rb+p.root_wall
    crest = root+p.thread_height
    Rs = max(Rb,Rc,crest+p.clearance_budget+1.8)
    T = 1.5*p.thread_pitch+p.engagement
    J = T+.6*p.thread_pitch
    Q = max(Rs-Rc,crest+p.clearance_budget-rc,.2)
    A = J+Q
    F,K = 2.0,max(Rs-Rb,.2)
    B = p.cavity_length-(p.cap_height-p.floor)
    s = p.smooth_margin
    body_band = (-B+s,-(F+K)-s)
    cap_band = (A+s,p.cap_height-p.floor-s)
    Cmin = 2*p.min_grip_band+A+F+K+4*s
    Hrange = (p.floor+A+2*s+p.min_grip_band,
              p.cavity_length+p.floor-(F+K)-2*s-p.min_grip_band)
    eps = 1e-10
    require(p.cavity_length+eps >= Cmin,
            f"cavity_length >= {Cmin:.10g} required for both grip bands; got {p.cavity_length:g}")
    require(Hrange[0]-eps <= p.cap_height <= Hrange[1]+eps,
            f"cap_height must be in [{Hrange[0]:.10g}, {Hrange[1]:.10g}]")
    for name,band in (("body",body_band),("cap",cap_band)):
        length = band[1]-band[0]
        require(length+eps >= p.min_grip_band, f"{name} band >= min_grip_band required")
        require(2*p.fade_length < length, f"2*fade_length < {name} band required")
    require(crest+.20 >= rc, "thread_crest + minimum coupon clearance >= cap_inner_radius required")
    require(2*Rs <= p.max_od+eps and 2*(max(Rb,Rc)+p.skin_height) <= p.max_od+eps,
            "collar and skin outside diameter must be <= max_od")
    minwall = min(p.wall,p.root_wall,Rs-crest-p.clearance_budget)
    require(minwall >= 1.8-eps, "minimum structural wall >= 1.8 required")
    flank = p.thread_height/(.35*p.thread_pitch)
    lead = p.thread_height/(.5*p.thread_pitch)
    require(flank <= 1, "thread flank slope <= 1 required")
    raw_n = 2*pi*Rc/p.skin_arc_pitch_target
    require(isfinite(raw_n) and 7.5 <= raw_n < 128.5, "rounded lattice_count must be in [8,128]")
    N = floor(raw_n+.5)
    Pb,Pc = 2*pi*Rb/N,2*pi*Rc/N
    width = lambda P: 2*p.plateau_half_fraction*P*p.skin_axial_pitch/hypot(P,p.skin_axial_pitch)
    require(min(width(Pb),width(Pc)) >= 1-eps, "minimum developed plateau width >= 1 mm required")
    fz = (1/(p.skin_axial_pitch*(.5-p.plateau_half_fraction))
          if p.skin_style == "diamond" else 2*pi/p.skin_axial_pitch)
    slope = p.skin_height*(fz+pi/(2*p.fade_length))
    require(slope <= 1, "skin radial slope bound <= 1 required")
    # Phase arithmetic must retain a resolvable cell fraction, not merely be finite.
    require(abs(p.skin_phase_theta*N/(2*pi)) < 2**40
            and abs(p.skin_phase_z/p.skin_axial_pitch) < 2**40,
            "skin phase too large to represent cell fractions reliably")
    d = Derived(rb,rc,Rb,Rc,root,crest,Rs,T,p.thread_pitch,p.thread_pitch+p.engagement,
                J,Q,A,F,K,B,body_band,cap_band,Cmin,Hrange,N,Pb,Pc,width(Pb),width(Pc),
                slope,flank,lead,p.cavity_length+2*p.floor,minwall)
    for value in asdict(d).values():
        require(all(isfinite(x) for x in value) if isinstance(value,tuple) else isfinite(value),
                "derived dimension is not representable")
    return d


def preset(name: str, **overrides) -> Params:
    """Presets are data; Laifen's unresolved full-case split stays explicit."""
    require(name in ("short-grip", "generic", "laifen-provisional"), "unknown preset")
    if name == "laifen-provisional":
        raise ValueError("laifen-provisional pending: full-case cap split and end-contact decision required")
    p = replace(Params(), **overrides)
    if name == "short-grip":
        require(p.max_od == 39, "short-grip preset locks max_od=39; use generic for another limit")
    return p


def parameter_fingerprint(p: Params) -> str:
    return sha256(json.dumps(asdict(p),sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
