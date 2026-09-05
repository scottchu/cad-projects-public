"""Formula-derived 2D profile/section; no generated CAD or fit claim."""
from pathlib import Path
from math import floor, pi, hypot, sin, cos, atan, degrees
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().with_suffix('')
N = floor(2*pi*19.55/3.63+.5)
P = 2*pi*19.55/N
width = 2*.18*P*4.8/hypot(P,4.8)
slope = .45/(4.8*(.5-.18))
facts = dict(outer_diameter=40., minimum_outer_diameter=39.9,
             valley_radius=19.55, thread_crest=17.4, clearance_budget=.3,
             minimum_female_wall_budget=1.85, minimum_female_wall_c25=1.90,
             lattice_count=N, arc_pitch=P, plateau_width=width,
             rational_plateau_bound=width*sin(pi/N)/(pi/N),
             skin_slope_bound=slope, relief_slope_bound=slope+.2/.3,
             relief_angle_degrees=degrees(atan(slope+.2/.3)),
             collar_end=10.2, cap_straight_start=12.4,
             body_floor=-35.1, body_inner_floor=-32.1, cap_inner_floor=40.4,
             cap_height=43.4, closed_length=78.5)
assert facts['minimum_outer_diameter'] <= 40
assert width*sin(pi/N)/(pi/N) >= 1
assert slope+.2/.3 < 1

def F(theta,z,n):
    u=n*theta/(2*pi);v=z/4.8
    wrap=lambda x:x-np.floor(x+.5)
    m=np.maximum(np.abs(wrap(u+v)),np.abs(wrap(u-v)))
    return np.clip((.5-m)/(.5-.18),0,1)

def old(z,role):
    if role=='body':
        base=np.interp(z,[-35.1,-34.8,-4.1,-2,0],[17.1,17.4,17.4,19.5,19.5])
        band=(-30.1,-6.1)
    else:
        base=np.interp(z,[0,10.2,12.4,43.1,43.4],[19.5,19.5,17.9,17.9,17.6])
        band=(14.4,38.4)
    distance=np.minimum(z-band[0],band[1]-z)
    e=.5*(1-np.cos(pi*np.clip(distance/2,0,1)))
    return base+.45*e*F(0,z,31)

def new(z,role):
    t=z+35.1 if role=='body' else 43.4-z
    relief=.2*np.clip(1-t/.3,0,1)
    return 19.55+.45*F(0,z,N)-relief

fig=plt.figure(figsize=(13,8),facecolor='#ffffff')
gs=fig.add_gridspec(1,3,width_ratios=[1,1,1.2],wspace=.20)
axes=[fig.add_subplot(gs[0,i]) for i in range(3)]
for ax,fn,title in zip(axes[:2],[old,new],['R3 existing profile','R4 proposed profile']):
    for role,lo,hi,color in [('body',-35.1,0,'#bcbcbc'),('cap',0,43.4,'#d5d5d5')]:
        z=np.linspace(lo,hi,5000);r=fn(z,role)
        ax.fill_betweenx(z,-r,r,color=color,alpha=.65)
        ax.plot(r,z,color='#252525',lw=.8);ax.plot(-r,z,color='#252525',lw=.8)
    ax.plot([-20,20],[0,0],color='#252525',lw=1)
    ax.text(0,1.8,'cap separation',ha='center',fontsize=9)
    ax.axvline(20,color='#777777',ls=':',lw=.8);ax.axvline(-20,color='#777777',ls=':',lw=.8)
    ax.set_title(title,fontsize=14,pad=30)
    ax.set_xlim(-25,25);ax.set_ylim(-40,49);ax.set_aspect('equal');ax.axis('off')
    od=39 if fn==old else 40
    ax.annotate('',xy=(-od/2,47),xytext=(od/2,47),arrowprops=dict(arrowstyle='<->',color='#252525'))
    ax.text(0,48,f'max OD {od:.1f} mm',ha='center',va='bottom',fontsize=11)
axes[0].annotate('smooth collar',xy=(19.5,6),xytext=(0,20),ha='center',fontsize=10,
                 arrowprops=dict(arrowstyle='->',color='#444444'))
axes[0].text(0,-15,'diamonds only\nin two bands',ha='center',fontsize=10)
axes[1].text(0,24,'diamonds over\nwhole sidewall',ha='center',fontsize=10)
axes[1].text(0,-17,'same crest OD\nthrough joint',ha='center',fontsize=10)
axes[1].text(0,-38,'0.30 mm end relief; still textured',ha='center',fontsize=9)
ax=axes[2];ax.axis('off')
ax.text(0,1,'Why 40 mm?',transform=ax.transAxes,fontsize=16,weight='bold')
ax.text(0,.925,'Thread-section wall budget (radial)',transform=ax.transAxes,fontsize=11)
inset=ax.inset_axes([0,.68,1,.17]);inset.set_xlim(16.5,20.5);inset.set_ylim(-.5,1.5)
inset.axvspan(16.5,17.4,color='#eeeeee');inset.axvspan(17.4,17.7,color='#ffffff')
inset.axvspan(17.7,19.55,color='#d5d5d5',alpha=.65);inset.axvspan(19.55,20,color='#d5d5d5',alpha=.35)
for x,label in [(17.4,'crest\n17.4'),(17.7,'void\n17.7'),(19.55,'valley\n19.55'),(20,'outer\n20.0')]:
    inset.axvline(x,color='#252525',lw=1);inset.text(x,1.58 if x==17.4 else -.62,label,ha='center',va='bottom' if x==17.4 else 'top',fontsize=8)
inset.annotate('',xy=(17.7,.75),xytext=(19.55,.75),arrowprops=dict(arrowstyle='<->'))
inset.text(18.625,.9,'1.85 mm minimum',ha='center',fontsize=9)
inset.axis('off')
ax.text(0,.43,'40.00 = 39.00 + 1.00 mm\n0.45 mm diamond depth retained\n1.8 mm thread-wall requirement retained\n0.30 mm clearance budget retained',transform=ax.transAxes,fontsize=11,linespacing=1.7)
ax.text(0,.20,'Unchanged: bores 30 / 31 mm\npitch 2 mm; engagement 6 mm; C25 cap\nclosed length 78.5 mm; cavity 72.5 mm',transform=ax.transAxes,fontsize=10,linespacing=1.7)
ax.text(0,.02,f'Diamonds: axial pitch 4.8 mm\n{N} repeats; arc pitch {P:.3f} mm\npattern aligned across closed seam',transform=ax.transAxes,fontsize=10,linespacing=1.6)
fig.suptitle('Straight outside profile + full sidewall diamond coverage',fontsize=18,y=.98)
fig.text(.05,.02,'Formula-based axial profiles at theta=0; no CAD or print validation. Thread panel uses a conservative crest/clearance envelope.',fontsize=9,color='#575757')
fig.subplots_adjust(top=.86,bottom=.09,left=.03,right=.97)
fig.savefig(OUT.with_suffix('.svg'))
fig.savefig(OUT.with_suffix('.png'),dpi=160)
print(json.dumps(facts,indent=2))
