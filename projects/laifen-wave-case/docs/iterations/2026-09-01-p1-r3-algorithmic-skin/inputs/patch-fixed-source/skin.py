"""Exact R3 radial field and conservative, crease-aware tessellation budgets.

This module does not claim to generate a watertight full-body BREP yet.
"""
from dataclasses import dataclass
from math import ceil, cos, floor, isfinite, pi, sin, sqrt
try:
    from .params import derive, require
except ImportError:
    from params import derive, require


def wrap(t):
    return t-floor(t+.5)


def envelope(z, band, fade_length):
    distance = min(z-band[0],band[1]-z)
    if distance <= 0:
        return 0.0
    if distance >= fade_length:
        return 1.0
    return .5*(1-cos(pi*distance/fade_length))


def field(p, theta, z, derived=None):
    d = derived or derive(p)
    u = d.lattice_count*(theta-p.skin_phase_theta)/(2*pi)
    v = (z-p.skin_phase_z)/p.skin_axial_pitch
    if p.skin_style == "diamond":
        m = max(abs(wrap(u+v)),abs(wrap(u-v)))
        return min(1.,max(0.,(.5-m)/(.5-p.plateau_half_fraction)))
    return 1-sin(pi*(u+v))**2*sin(pi*(u-v))**2


def radius(p, role, theta, z, derived=None):
    require(role in ("body","cap"), "skin role must be body or cap")
    d = derived or derive(p)
    R = d.body_radius if role == "body" else d.cap_radius
    band = d.body_band if role == "body" else d.cap_band
    return R+p.skin_height*envelope(z,band,p.fade_length)*field(p,theta,z,d)


@dataclass(frozen=True)
class TessellationPlan:
    angular_step_max: float
    axial_step_max: float
    angular_segments: int
    axial_segments: int
    base_grid_triangles: int
    interpolation_error_budget: float
    angular_error_bound: float
    axial_error_bound: float
    mixed_error_bound: float
    crease_split_required: bool


def tessellation_plan(p, role, tolerance=.005):
    """Conservative Cartesian triangle error, valid inside each smooth facet.

A final tessellator MUST split at all diamond valleys, plateau edges, flank
ridges and band/fade breakpoints before applying these maximum spacings.
The triangle Taylor remainder bound is .5*(Mtt*dt²+2*Mtz*dt*dz+Mzz*dz²).
Each of its three terms receives one third of tolerance. Count is a lower
estimate: crease splitting adds triangles and must never be omitted.
"""
    require(isfinite(tolerance) and 0 < tolerance <= .005, "0 < tessellation tolerance <= .005 required")
    d = derive(p)
    require(role in ("body","cap"), "skin role must be body or cap")
    R = d.body_radius if role == "body" else d.cap_radius
    band = d.body_band if role == "body" else d.cap_band
    n = d.lattice_count/(2*pi)
    if p.skin_style == "diamond":
        ft = n/(.5-p.plateau_half_fraction)
        fz = 1/(p.skin_axial_pitch*(.5-p.plateau_half_fraction))
        ftt = ftz = fzz = 0.
    else:
        ft = 2*pi*n
        fz = 2*pi/p.skin_axial_pitch
        ftt = 8*pi*pi*n*n
        fzz = 8*pi*pi/p.skin_axial_pitch**2
        ftz = 8*pi*pi*n/p.skin_axial_pitch
    ep = pi/(2*p.fade_length)
    epp = pi*pi/(2*p.fade_length**2)
    Mtt = R+p.skin_height+2*p.skin_height*ft+p.skin_height*ftt
    Mzz = p.skin_height*(epp+2*ep*fz+fzz)
    Mtz = p.skin_height*(ep*ft+ftz+ep+fz)
    dt = sqrt(2*tolerance/(3*Mtt))
    dz = sqrt(2*tolerance/(3*Mzz))
    scale = min(1.,sqrt(tolerance/(3*Mtz*dt*dz)))
    dt,dz = dt*scale,dz*scale
    nt,nz = ceil(2*pi/dt),ceil((band[1]-band[0])/dz)
    dt,dz = 2*pi/nt,(band[1]-band[0])/nz
    return TessellationPlan(dt,dz,nt,nz,2*nt*nz,tolerance,
                            .5*Mtt*dt*dt,.5*Mzz*dz*dz,Mtz*dt*dz,True)


def facet_polygons(p, i, j):
    """Five exact developed polygons for one diamond cell in (u,v).

Cell center is x=u+v=i, y=u-v=j. The plateau and four trapezoids
partition the complete cell, including shared zero-width valley boundaries.
These polygons are the crease-preserving seeds for future BREP meshing.
"""
    a = p.plateau_half_fraction
    outer = [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]
    inner = [(-a,-a),(a,-a),(a,a),(-a,a)]
    xy = [inner]+[[outer[k],outer[(k+1)%4],inner[(k+1)%4],inner[k]] for k in range(4)]
    return tuple(tuple(((i+x+j+y)/2,(i+x-j-y)/2) for x,y in reversed(poly)) for poly in xy)
