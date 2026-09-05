"""DES-SKIN-02 deterministic patch counting and polynomial error arithmetic.
No CAD generation. Run from repository root through uv.
"""
import importlib.util
import json
import math
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT/'projects/laifen-wave-case/cad/p1_r3_generator'))
from params import Params,derive
from skin import facet_polygons


def clip(poly,axis,bound,sign):
    result=[]
    if not poly:return result
    prev=poly[-1]; ap=sign*(prev[axis]-bound)
    for curr in poly:
        ac=sign*(curr[axis]-bound)
        if (ac>=0)!=(ap>=0):
            t=ap/(ap-ac)
            result.append(tuple(prev[k]+t*(curr[k]-prev[k]) for k in range(2)))
        if ac>=0:result.append(curr)
        prev,ap=curr,ac
    return result


def area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2 if poly else 0


def count(p,role):
    d=derive(p);N=d.lattice_count
    lo,hi=getattr(d,role+'_band');lo=(lo-p.skin_phase_z)/p.skin_axial_pitch;hi=(hi-p.skin_phase_z)/p.skin_axial_pitch
    f=p.fade_length/p.skin_axial_pitch
    ranges=[(lo,lo+f,'fade'),(lo+f,hi-f,'core'),(hi-f,hi,'fade')]
    counts={'core':0,'fade':0};areas=0.;polygons=0
    for i in range(math.floor(lo)-2,math.ceil(N+hi)+3):
        for j in range(math.floor(-hi)-2,math.ceil(N-lo)+3):
            for poly in facet_polygons(p,i,j):
                for low,high,zone in ranges:
                    q=clip(clip(list(poly),1,low,1),1,high,-1)
                    if area(q)<1e-12:continue
                    start=max(0,math.floor(min(v[0] for v in q)))
                    end=min(N,math.ceil(max(v[0] for v in q)))
                    for strip in range(start,end):
                        r=clip(clip(q,0,strip,1),0,strip+1,-1)
                        a=area(r)
                        if a>1e-12:counts[zone]+=1;areas+=a
    expected=N*(hi-lo)
    assert abs(areas-expected)<1e-8,(areas,expected)
    return dict(counts,total=sum(counts.values()),developed_area=areas,expected_area=expected)


def main():
    p=Params();d=derive(p)
    c=np.zeros(8);c[2]=math.pi**2/4
    matrix=np.array([[1,1,1,1],[4,5,6,7],[12,20,30,42],[24,60,120,210]],float)
    c[4:]=np.linalg.solve(matrix,[1-c[2],-2*c[2],-math.pi**2/2-2*c[2],0])
    b=[sum(c[i]*math.comb(k,i)/math.comb(7,i) for i in range(k+1)) for k in range(8)]
    derivative=max(abs(7*(b[i+1]-b[i])) for i in range(7))
    delta=2*math.pi/d.lattice_count
    half=delta/2
    angular=.5*max(delta-2*math.sin(half),4*math.tan(half/2)-delta)
    fade=math.pi**8/(2*math.factorial(8)*256)
    R=max(d.body_radius,d.cap_radius)+p.skin_height
    slope_u=1/(.5-p.plateau_half_fraction)
    radial=p.skin_height*(slope_u*d.lattice_count/(2*math.pi)*angular+fade)
    min_width=min(d.body_plateau_width,d.cap_plateau_width) if hasattr(d,'body_plateau_width') else 1.0231383170253368
    result={'body':count(p,'body'),'cap':count(p,'cap'),'cosine_fade_power_coefficients':c.tolist(),'cosine_fade_bernstein':b,'fade_value_error_bound':fade,'angular_parameter_error_bound_radians':angular,'radial_error_bound':radial,'fade_derivative_bound':derivative,'surface_slope_bound':p.skin_height*(1/(p.skin_axial_pitch*(.5-p.plateau_half_fraction))+derivative/p.fade_length),'angular_metric_ratio_min':math.sin(half)/half,'plateau_width_lower_bound_default':min_width*math.sin(half)/half}
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
