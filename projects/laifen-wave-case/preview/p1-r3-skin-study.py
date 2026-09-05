"""Analytic design study only; no CAD or manufacturing claims.

Run from repository root: uv run python projects/laifen-wave-case/preview/p1-r3-skin-study.py
"""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

OUT = Path(__file__).resolve().parent
N, PZ, H, A, FADE = 31, 4.8, .45, .18, 2.
plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none", "font.size": 10})


def wave(t):
    return t - np.floor(t + .5)


def skin(theta, z, lo, hi, style="diamond"):
    u, v = N * theta / (2 * np.pi), z / PZ
    if style == "diamond":
        m = np.maximum(np.abs(wave(u + v)), np.abs(wave(u - v)))
        field = np.clip((.5 - m) / (.5 - A), 0, 1)
    else:
        field = 1 - np.sin(np.pi * (u + v)) ** 2 * np.sin(np.pi * (u - v)) ** 2
    d = np.minimum(z - lo, hi - z)
    envelope = np.where(d <= 0, 0, np.where(d >= FADE, 1, .5 * (1 - np.cos(np.pi * np.clip(d, 0, FADE) / FADE))))
    return H * envelope * field


def silhouette(ax, role):
    cap = role == "cap"
    height = 43.4 if cap else 44.1
    lo, hi = (14.4, 38.4) if cap else (-30.1, -6.1)
    radius = 17.9 if cap else 17.4
    y = np.unique(np.r_[np.linspace(0, height, 141),5,7,27,29])
    th = np.linspace(-np.pi / 2, np.pi / 2, 125)
    def projected(t, yy):
        zz = 43.4-yy if cap else yy-35.1
        if cap:
            rr = 19.5 if zz <= 10.2 else 19.5-(zz-10.2)*1.6/2.2 if zz < 12.4 else radius
        else:
            rr = 16.8 if zz >= 0 else 19.5 if zz >= -2 else 17.4+(zz+4.1) if zz >= -4.1 else radius
        return ((rr+skin(t,zz,lo,hi))*np.sin(t), yy)
    polygons, colors = [], []
    for j in range(len(y)-1):
        ym = (y[j]+y[j+1])/2
        z = 43.4-ym if cap else ym-35.1
        if cap:
            r0 = 19.5 if z <= 10.2 else 19.5-(z-10.2)*1.6/2.2 if z < 12.4 else radius
        else:
            r0 = 16.8 if z >= 0 else 19.5 if z >= -2 else 17.4+(z+4.1) if z >= -4.1 else radius
        for i in range(len(th)-1):
            tm=(th[i]+th[i+1])/2
            dz=1e-4
            dr=skin(tm,z,lo,hi)
            rz=(skin(tm,z+dz,lo,hi)-skin(tm,z-dz,lo,hi))/(2*dz)
            rt=(skin(tm+dz,z,lo,hi)-skin(tm-dz,z,lo,hi))/(2*dz)
            # Lambert shade from analytic derivatives, not an ornamental bitmap.
            normal=np.array([np.sin(tm)-rt/(r0+dr)*np.cos(tm), np.cos(tm)+rt/(r0+dr)*np.sin(tm), -rz*(-1 if cap else 1)])
            normal/=np.linalg.norm(normal)
            light=np.array([-.45,.72,.53]); light/=np.linalg.norm(light)
            tone=.29+.68*max(0,float(normal@light))
            base=np.array([.77,.65,.46]) if cap else np.array([.43,.66,.64])
            colors.append(np.clip(base*tone+.10,0,1))
            polygons.append([projected(t,yy) for t,yy in [(th[i],y[j]),(th[i+1],y[j]),(th[i+1],y[j+1]),(th[i],y[j+1])]])
    ax.add_collection(PolyCollection(polygons, facecolors=colors, edgecolors="face", linewidths=.1, antialiaseds=False, rasterized=False))
    ax.set(xlim=(-24,30),ylim=(-3,51),aspect="equal")
    ax.axis("off")
    bottom, top = (5,29) if cap else (5,29)
    ax.annotate("",(23,top),(23,bottom),arrowprops={"arrowstyle":"|-|","color":"#267776"})
    ax.text(25,(bottom+top)/2,"24 mm\ngrip band",va="center",fontsize=10,color="#185958")
    ax.text(0,48,"CAP · 43.4 mm" if cap else "BODY · 44.1 mm",ha="center",weight="bold",fontsize=12)
    ax.text(0,-2,"Closed floor on bed",ha="center",fontsize=9,color="#546575")
    ax.text(0,40 if cap else 39,"Smooth joint",ha="center",fontsize=8,color="#ffffff")


def unrolled(ax, style, title):
    x=np.linspace(0,3*2*np.pi*17.9/N,91)
    z=np.linspace(14.4,38.4,161)
    xx,zz=np.meshgrid(x,z)
    theta=xx/17.9
    f=skin(theta,zz,14.4,38.4,style)
    ax.pcolormesh(xx,zz-14.4,f,cmap="YlGnBu_r",vmin=0,vmax=H,shading="auto",rasterized=False)
    ax.axhline(2,color="white",ls="--",lw=.7)
    ax.axhline(22,color="white",ls="--",lw=.7)
    ax.set(title=title,xlabel="Developed surface width (mm)",ylabel="Band height (mm)",ylim=(0,24))
    ax.set_xticks([0,3.628,7.256,10.884]);ax.set_xticklabels(["0","3.63","7.26","10.88"])
    ax.set_yticks([0,2,12,22,24]);ax.tick_params(labelsize=8)


def main():
    fig=plt.figure(figsize=(15,10.5),facecolor="#f7f9fb")
    fig.text(.045,.955,"A full skin you can hold and twist",fontsize=23,weight="bold",color="#193448")
    fig.text(.045,.922,"P1 R3 analytic study · Generic screw-cap cylinder · Not CAD or print validation",fontsize=11,color="#526575")
    gs=fig.add_gridspec(2,4,left=.045,right=.965,bottom=.18,top=.87,height_ratios=[1,.16],width_ratios=[1.15,1.15,.9,.9],wspace=.40)
    silhouette(fig.add_subplot(gs[0,0]),"body")
    silhouette(fig.add_subplot(gs[0,1]),"cap")
    unrolled(fig.add_subplot(gs[0,2]),"diamond","DEFAULT · blunt diamonds")
    unrolled(fig.add_subplot(gs[0,3]),"smooth","OPTION · smooth ridges")
    fig.text(.048,.235,"One body + caps c0.20 / 0.25 / 0.30\nCavity72.5 · closed length78.5 · maximum OD39",fontsize=11,color="#193448")
    fig.text(.535,.235,"Same exact field as the contract\nFull band24 · fades2 +2 · full amplitude20",fontsize=11,color="#193448")
    fig.text(.048,.145,"FIXED: 4.8 mm axial pitch · 31 repeats around · raised0.45 mm · shared phase\nDERIVED: repeat count and grip length change with body/cap dimensions; cells never stretch.",fontsize=12,color="#193448",linespacing=1.6)
    fig.text(.048,.065,"Review: Are these broad diamond-covered areas enough to hold and twist comfortably?\nIs the blunt diamond character what you intended? The actual hand test remains pending.",fontsize=12,weight="bold",color="#185958",linespacing=1.6)
    fig.savefig(OUT/"p1-r3-skin-study.svg")
    fig.savefig(OUT/"p1-r3-skin-study.png",dpi=120)
    values={}
    for name,radius in [("body",17.4),("cap",17.9)]:
        p=2*math.pi*radius/N
        values[name]={"arc_pitch":p,"plateau_min_width":2*A*p*PZ/math.sqrt(p*p+PZ*PZ)}
    bound=H*(1/(PZ*(.5-A))+math.pi/(2*FADE))
    values.update({"diamond_slope_bound":bound,"diamond_angle_degrees":math.degrees(math.atan(bound)),"smooth_slope_bound":H*(2*math.pi/PZ+math.pi/(2*FADE)),"minimum_cavity":2*24+12.4+4.1+8,"band_periods":24/PZ,"body_band":[-30.1,-6.1],"cap_band":[14.4,38.4]})
    print(json.dumps(values,indent=2))


if __name__=="__main__":
    main()
