"""Shared diamond field over both full exterior domains, before the smooth end trim."""
from math import floor, pi
from .params import derive, require


def wrap(t):
    return t-floor(t+.5)


def field(p, theta, z, derived=None):
    d=derived or derive(p)
    u=d.lattice_count*(theta-p.skin_phase_theta)/(2*pi)
    v=(z-p.skin_phase_z)/p.skin_axial_pitch
    m=max(abs(wrap(u+v)),abs(wrap(u-v)))
    return min(1.,max(0.,(.5-m)/(.5-p.plateau_half_fraction)))


def radius(p, role, theta, z, derived=None):
    d=derived or derive(p)
    return d.outer_valley_radius+p.skin_height*field(p,theta,z,d)


def facet_polygons(p, i, j):
    a=p.plateau_half_fraction
    outer=[(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]
    inner=[(-a,-a),(a,-a),(a,a),(-a,a)]
    xy=[inner]+[[outer[k],outer[(k+1)%4],inner[(k+1)%4],inner[k]] for k in range(4)]
    return tuple(tuple(((i+x+j+y)/2,(i+x-j-y)/2) for x,y in reversed(poly)) for poly in xy)
