"""Original formula-only design study. No CAD kernel, mesh or physical fit claim."""
from pathlib import Path
from math import pi, floor, hypot, sin, atan, degrees
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

OUT = Path(__file__).resolve().with_suffix('')
R, H, PZ, TARGET, A = 19.5, .45, 4.8, 3.63, .18
RV = R-H
N = floor(2*pi*RV/TARGET+.5)
ARC = 2*pi*RV/N
WIDTH = 2*A*ARC*PZ/hypot(ARC,PZ)
SLOPE = H/(PZ*(.5-A))
facts = dict(outer_diameter=2*R, valley_radius=RV, male_root=16.4,
             male_crest=16.9, male_root_wall=1.4, thread_height=.5,
             thread_clearance=.25, clearance_budget=.3,
             female_wall_budget=RV-16.9-.3, female_wall_c25=RV-16.9-.25,
             radial_interlock_c25=.5-.25, radial_interlock_c30=.5-.3,
             flank_slope=.5/.7, lead_slope=.5,
             axial_flank_free_travel_c25=.25/(.5/.7),
             lattice_count=N, arc_pitch=ARC, axial_pitch=PZ,
             plateau_width=WIDTH, rational_plateau_bound=WIDTH*sin(pi/N)/(pi/N),
             skin_slope=SLOPE, relief_slope=SLOPE+.3/.5,
             relief_angle_degrees=degrees(atan(SLOPE+.3/.5)),
             neck=9, collar_end=10.2, taper_end=12.4, taper_slope_budget=1.7/2.2,
             drain_count_per_end=7, drain_diameter=3, drain_circle_radius=9,
             drain_area_per_end=7*pi*1.5**2, drain_min_ligament=6,
             drain_to_body_bore_margin=4.5, drain_to_cap_bore_margin=5,
             short_cavity=72.5, short_closed_length=78.5,
             full_conditional_cavity=208+5, full_conditional_closed_length=208+5+6,
             full_leading_face_count=10*N*(208+5+6)/PZ)
assert N == 33 and facts['female_wall_budget'] >= 1.8
assert facts['radial_interlock_c30'] >= .2
assert facts['rational_plateau_bound'] >= 1
assert facts['relief_slope'] < 1 and facts['taper_slope_budget'] < 1
assert RV-.3 > 15+1.8

def field(u,z):
    v=z/PZ
    wrap=lambda x:x-np.floor(x+.5)
    m=np.maximum(np.abs(wrap(u+v)),np.abs(wrap(u-v)))
    return np.clip((.5-m)/(.5-A),0,1)

plt.rcParams.update({'font.size':10,'font.family':'DejaVu Sans'})
fig,axes=plt.subplots(2,2,figsize=(14,10),facecolor='white')
fig.subplots_adjust(left=.07,right=.97,top=.87,bottom=.10,wspace=.27,hspace=.40)
fig.suptitle('39 mm outside | original diamond pattern | new short thread test',fontsize=18,y=.965)
fig.text(.5,.914,'Bores 30 / 31 unchanged. New thread/root strength and fit need a new physical test.',ha='center',fontsize=11)

ax=axes[0,0]
ax.set_title('1  Radial budget at thread crest (mm)',loc='left',weight='bold')
for lo,hi,color,label in [(15,16.4,'#6595a6','male root\n1.40'),(16.4,16.9,'#a8c6cf','tooth\n0.50'),(16.9,17.2,'white','gap\n0.30'),(17.2,19.05,'#88b6a0','female wall\n1.85'),(19.05,19.5,'#d8e8de','skin\n0.45')]:
    ax.add_patch(Rectangle((lo,0),hi-lo,1,fc=color,ec='#263c40',lw=.8))
    ax.text((lo+hi)/2,.5,label,ha='center',va='center',fontsize=9,rotation=90 if hi-lo<.6 else 0)
for k,x in enumerate([15,16.4,16.9,17.2,19.05,19.5]):
    ax.plot([x,x],[1,1.16+.18*(k%2)],color='#536567',lw=.7)
    ax.text(x,1.19+.18*(k%2),f'{x:g}',ha='center',fontsize=9)
ax.text(15,-.4,'C25 clearance 0.25 per side; budget shown at C30\nRadial interlock: 0.25 nominal / 0.20 worst\nRoot wall 1.40 is a NEW design assumption',va='top',linespacing=1.6)
ax.set(xlim=(14.8,19.7),ylim=(-1.3,1.8));ax.axis('off')

ax=axes[0,1]
ax.set_title('2  Same small bevel at both closed ends',loc='left',weight='bold')
t=np.linspace(0,1.8,1800)
r=RV+H*field(0,t)-.3*np.maximum(0,1-t/.5)
ax.fill_betweenx(t,18.55,r,color='#d8e8de');ax.plot(r,t,color='#325f52',lw=2)
ax.plot([19.2,19.5],[0,.5],ls='--',color='#586d73',label='crest envelope')
ax.plot([18.7,19.6],[0,0],color='#333333',lw=1)
ax.annotate('',xy=(19.5,.5),xytext=(19.5,0),arrowprops={'arrowstyle':'<->'})
ax.text(19.53,.25,'0.50 axial',va='center')
ax.annotate('',xy=(19.2,-.16),xytext=(19.5,-.16),arrowprops={'arrowstyle':'<->'})
ax.text(19.35,-.25,'0.30 radial',ha='center')
ax.text(18.58,1.45,'Full texture continues through bevel\nNo smooth collar; no seam bevel',linespacing=1.5)
ax.text(18.58,.93,f'Combined slope {facts["relief_slope"]:.3f}\n{facts["relief_angle_degrees"]:.1f} degrees from vertical (<45)',linespacing=1.5)
ax.set(xlim=(18.5,20.0),ylim=(-.4,1.8));ax.axis('off')

ax=axes[1,0]
ax.set_title('3  Original polar drain / vent layout, each end',loc='left',weight='bold')
ax.add_patch(Circle((0,0),19.2,fc='#e5eeea',ec='#41695c'))
ax.add_patch(Circle((0,0),15,fill=False,ec='#728e8d',ls='--'))
ax.add_patch(Circle((0,0),9,fill=False,ec='#b4bfbd',ls=':'))
pts=[(0,0)]+[(9*np.cos(k*pi/3),9*np.sin(k*pi/3)) for k in range(6)]
for xy in pts:ax.add_patch(Circle(xy,1.5,fc='white',ec='#315948'))
ax.annotate('7 x diameter 3\nstraight through floor',xy=(9,0),xytext=(23,12),arrowprops={'arrowstyle':'->'},ha='left')
ax.annotate('6 centers at radius 9\n+ one central hole',xy=(-4.5,-7.794),xytext=(23,-1),arrowprops={'arrowstyle':'->'},ha='left')
ax.text(23,-13,'Floor 3; nearest ligament 6\nBore-edge margin >=4.5\nNo hole-edge chamfers',ha='left',linespacing=1.5)
ax.set(xlim=(-23,57),ylim=(-23,23));ax.set_aspect('equal');ax.axis('off')

ax=axes[1,1]
ax.set_title('4  One lattice across seam, no axial scaling',loc='left',weight='bold')
x=np.linspace(0,4*ARC,600);z=np.linspace(-8,8,700)
xx,zz=np.meshgrid(x,z)
ax.imshow(field(xx/ARC,zz),extent=[0,4*ARC,-8,8],origin='lower',cmap='Greys_r',vmin=-.15,vmax=1.1,aspect='equal')
ax.axhline(0,color='#297863',lw=1.7)
ax.text(4*ARC+.4,0,'seam\nshared phase',va='center',color='#256b59')
ax.annotate('',xy=(-.8,0),xytext=(-.8,4.8),arrowprops={'arrowstyle':'<->'})
ax.text(-1.2,2.4,'4.8',rotation=90,va='center')
ax.text(0,-10.3,f'N = {N} on both halves; arc pitch {ARC:.3f}; blunt plateau >= {facts["rational_plateau_bound"]:.3f}',fontsize=10)
ax.set(xlim=(-2,20),ylim=(-10.8,8.5));ax.axis('off')
fig.text(.07,.046,'Formula study only. Full cavity C = L + 5; 213 mm is conditional on measured L = 208. End-contact policy remains open.',fontsize=10)
fig.text(.07,.025,'Short test: cavity72.5 / closed78.5. Drain function shown for unoccluded/tilted halves; loaded drainage is not proven.',fontsize=10)
for extension in ('.svg','.png'):fig.savefig(OUT.with_suffix(extension),dpi=160)
print(json.dumps(facts,indent=2))
