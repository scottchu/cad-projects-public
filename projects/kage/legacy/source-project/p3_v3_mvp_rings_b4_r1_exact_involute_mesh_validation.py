"""Compact actual-BREP acceptance probes for B4-R1."""
from copy import deepcopy
from functools import lru_cache
import json
from math import cos,radians,sin
from pathlib import Path
import subprocess
import sys
from build123d import Axis,Location

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_validation as r4v
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_geometry as pinions
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_spec as ps
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_geometry as rings
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_spec as rs
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as b3
from p3_v3_mvp_rings_b4_r1_exact_involute_mesh_spec import SPEC

P=ps.SPEC;R=rs.SPEC.ring
FROZEN={"p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations":"ac47fc19eb54cd65dc5aedef57bcb8e87ae6048397752def8ec9a45b91a57705","p3_v3_mvp_rings_b4_r0_segmented_fins_magnets":"c8bdf02cd21e5af35e90ebe6dec49025097687ee4752ac7c4c2acdb852bf0da2"}

def immutable_evidence():
 actual={n:r4v.namespace_tree_hash(n) for n in FROZEN};return {"expected":FROZEN,"actual":actual,"all_unchanged":actual==FROZEN}

def _iv(a,b):
 c=deepcopy(a).intersect(deepcopy(b));return 0.0 if c is None else float(sum(s.volume for s in c.solids()))

def _probe(role,q,theta,kind):
 ring=pinions.exact_ring_tooth_witness(role,theta);pin=pinions.exact_output_pinion(role,q,theta)
 return {"kind":kind,"role":P.role_names[role],"q_mm":q,"theta_deg":theta,"intersection_mm3":_iv(ring,pin),"nearest_flank_mm":ring.distance_to(pin),"engagement_mm":P.output_axis_radius_mm+q+9.0-R.tip_radius_mm}

@lru_cache(maxsize=1)
def mesh_probe_evidence():
 script="import json,sys;import p3_v3_mvp_rings_b4_r1_exact_involute_mesh_validation as v;print(json.dumps(v._probe_group(int(sys.argv[1]))))"
 processes=[subprocess.Popen([sys.executable,"-c",script,str(role)],cwd=Path(__file__).resolve().parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for role in range(3)]
 rows=[]
 for role,process in enumerate(processes):
  stdout,stderr=process.communicate(timeout=420)
  if process.returncode: raise RuntimeError(f"mesh probe role {role} failed: {stderr}")
  rows.extend(json.loads([line for line in stdout.splitlines() if line.strip()][-1]))
 return {"rows":tuple(rows),"count":len(rows),"maximum_iv_mm3":max(x["intersection_mm3"] for x in rows),"minimum_flank_mm":min(x["nearest_flank_mm"] for x in rows),"maximum_flank_mm":max(x["nearest_flank_mm"] for x in rows),"minimum_engagement_mm":min(x["engagement_mm"] for x in rows),"maximum_engagement_mm":max(x["engagement_mm"] for x in rows),"kinds":tuple(sorted({x["kind"] for x in rows}))}


def _probe_group(role):
 pitch=360/P.ring_teeth;rows=[]
 if role==0:
  for q in P.q_mm:
   for theta in (0.0,pitch/2): rows.append(_probe(0,q,theta,"q_theta_representative"))
 alpha=P.station_angles_deg[role];seam=R.seam_angles_deg[role]
 for delta in (-pitch/20,pitch/20): rows.append(_probe(role,0.10,alpha-seam+delta,"qmax_every_seam"))
 if role==0:
  nominal=dict(next(x for x in rows if x["q_mm"]==0 and x["theta_deg"]==0));nominal["kind"]="nominal_role";rows.append(nominal)
 else: rows.append(_probe(role,0.0,0.0,"nominal_role"))
 for index,state in enumerate(SPEC.compact_coupled_states):
  if index%3==role: rows.append(_probe(role,0.10 if index==4 else 0.0,state[role],"compact_coupled_worst"))
 return rows

@lru_cache(maxsize=1)
def measured_lap_contact_evidence():
 eps=SPEC.contact_skin_mm;rows=[]
 for role in range(3):
  parts=[rings.segment_shape(role,i) for i in range(3)]
  for trailing,leading in ((0,1),(1,2),(2,0)):
   volume=_iv(parts[trailing],parts[leading].moved(Location((0,0,-eps))))
   rows.append({"role":R.roles[role],"seam":(trailing,leading),"skin_iv_mm3":volume,"area_mm2":volume/eps})
 areas=[x["area_mm2"] for x in rows]
 return {"rows":tuple(rows),"epsilon_mm":eps,"minimum_area_mm2":min(areas),"maximum_area_mm2":max(areas),"spread_mm2":max(areas)-min(areas)}

@lru_cache(maxsize=1)
def nearest_fin_evidence():
 rows=[]
 for role in range(3):
  fin=rings.fin_shape(role)
  if role<2: rows.append({"role":R.roles[role],"target":"higher_ring","iv_mm3":_iv(fin,rings.full_role_ring(role+1)),"distance_mm":fin.distance_to(rings.full_role_ring(role+1))})
  nearest_tower=60.0
  roller=b3.roller_shape(R.roles[role],nearest_tower)
  rows.append({"role":R.roles[role],"target":"roller","iv_mm3":_iv(fin,roller),"distance_mm":fin.distance_to(roller)})
  pin=pinions.exact_output_pinion(role,0,0)
  rows.append({"role":R.roles[role],"target":"pinion","iv_mm3":_iv(fin,pin),"distance_mm":fin.distance_to(pin)})
 return {"rows":tuple(rows),"maximum_iv_mm3":max(x["iv_mm3"] for x in rows)}

def magnet_sensor_position_evidence():
 rows=[]
 for role,(z0,z1) in enumerate(R.carrier_z_mm):
  a=radians(rs.SPEC.magnets.angle_deg);radius=rs.SPEC.magnets.center_radius_mm
  rows.append({"role":R.roles[role],"angle_deg":180.0,"center_xyz_mm":(radius*cos(a),radius*sin(a),(z0+z1)/2)})
 return {"rows":tuple(rows),"no_sensor_solids_added":True}

def physical_boundary(): return {"cad_only":True,"b5_present":False,"still_requires_print":("involute mesh under load","seam runout","fin clearance under flex","magnet sensing")}
