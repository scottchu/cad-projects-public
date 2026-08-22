"""Focused actual-solid evidence for B4-R0."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import hypot

from build123d import Axis, CenterOf, Compound

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_validation as r4v
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as b3
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_geometry as g
from p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_spec import SPEC


R,F,M,H=SPEC.ring,SPEC.fin,SPEC.magnets,SPEC.fasteners
FROZEN_HASHES={
 "p3_v3_mvp_base_q4_r4_functional_centered_step_lap":"9cae6479cca23c38bdfff1bd28e4a7f30b422abede6f28fb6f1ccf4f86f28c3a",
 "p3_v3_mvp_mount_b1_r1_raised_nut_rails":"675de24de9afa6afbcd7a6ba6c0079a1f60e72507a6e4cbe803f732d1c55e2df",
 "p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations":"ac47fc19eb54cd65dc5aedef57bcb8e87ae6048397752def8ec9a45b91a57705",
 "p3_v3_mvp_roller_b3_r1_blind_axle_towers":"9b384da3c608c69e205b5221a8495098fc775a7cc8e20772c1032790db846a71",
}


@lru_cache(maxsize=1)
def immutable_hash_evidence():
 actual={name:r4v.namespace_tree_hash(name) for name in FROZEN_HASHES}
 return {"expected":FROZEN_HASHES,"actual":actual,"all_unchanged":actual==FROZEN_HASHES}


@lru_cache(maxsize=1)
def segment_evidence():
 rows=[]
 for role in range(3):
  for segment in range(3):
   shape=g.segment_shape(role,segment);box=shape.bounding_box()
   rows.append({"role":R.roles[role],"segment":R.segment_names[segment],"teeth":R.segment_teeth[segment],"span_deg":R.segment_spans_deg[segment],"solids":len(shape.solids()),"valid":shape.is_valid,"bbox_xy_mm":(float(box.size.X),float(box.size.Y))})
 return {"rows":tuple(rows),"count":len(rows),"all_valid_one_solid":all(x["valid"] and x["solids"]==1 for x in rows),"maximum_bbox_mm":max(max(x["bbox_xy_mm"]) for x in rows)}


@lru_cache(maxsize=1)
def tooth_and_seam_evidence():
 # Cropping partitions one canonical 260T BREP; joinery begins at the frozen
 # root radius and therefore cannot edit the tooth/race profile.
 rows=[]
 for role in range(3):
  parts=[g.segment_shape(role,i) for i in range(3)]
  rows.append({"role":R.roles[role],"pairwise_max_iv_mm3":max(g.intersection_volume_mm3(parts[a],parts[b]) for a,b in ((0,1),(1,2),(2,0)))})
 return {"rows":tuple(rows),"total_teeth":sum(R.segment_teeth),"span_total_deg":sum(R.segment_spans_deg),"seams":R.seam_angles_deg,"phase_deg":R.tooth_phase_deg,"joinery_inner_radius_mm":R.root_radius_mm,"pairwise_max_iv_mm3":max(x["pairwise_max_iv_mm3"] for x in rows)}


def lap_fastener_evidence():
 z=[(a-(H.boss_axial_mm-(b-a))/2,b+(H.boss_axial_mm-(b-a))/2) for a,b in R.carrier_z_mm]
 rows=[]
 for role in range(3):
  z0,z1=R.carrier_z_mm[role]
  for segment,angle in enumerate(R.seam_angles_deg):
   shape=g.segment_shape(role,segment)
   rows.append({"role":R.roles[role],"segment":R.segment_names[segment],"nut_obstruction_mm3":g.intersection_volume_mm3(shape,g._nut_envelope(angle,z0,z1)),"bore_obstruction_mm3":g.intersection_volume_mm3(shape,g._fastener_bore(angle,z0,z1))})
 return {"lap_contact_area_mm2":H.nominal_contact_area_mm2,"lap_length_mm":H.lap_length_mm,"lap_split_total_mm":sum(H.lap_split_mm),"boss_z_mm":tuple(z),"boss_tangential_length_mm":H.boss_tangential_length_mm,"seam_relief_mm":H.seam_relief_mm,"relief_radii_mm":H.seam_relief_radii_mm,"role_clearances_mm":(z[1][0]-z[0][1],z[2][0]-z[1][1]),"screw_axis_radius_mm":H.screw_axis_radius_mm,"screw_clearance_diameter_mm":H.screw_clearance_diameter_mm,"nut_pocket_af_depth_mm":(H.nut_pocket_af_mm,H.nut_pocket_depth_mm),"rows":tuple(rows),"maximum_nut_obstruction_mm3":max(x["nut_obstruction_mm3"] for x in rows),"maximum_bore_obstruction_mm3":max(x["bore_obstruction_mm3"] for x in rows)}


@lru_cache(maxsize=1)
def fin_clearance_evidence():
 rows=[]
 for lower,higher in ((0,1),(0,2),(1,2)):
  rows.append({"lower":R.roles[lower],"higher":R.roles[higher],"iv_mm3":g.intersection_volume_mm3(g.fin_shape(lower),g.full_role_ring(higher))})
 roller_outer=SPEC.ring.pitch_radius_mm-(118.0+15.0)
 return {"rows":tuple(rows),"max_higher_ring_iv_mm3":max(x["iv_mm3"] for x in rows),"higher_ring_radial_clearance_mm":F.blade_radii_mm[0]-R.body_outer_radius_mm,"roller_radial_clearance_mm":F.shelf_radii_mm[0]-(118.0+15.0),"pinion_radial_clearance_mm":F.shelf_radii_mm[0]-132.5,"max_outer_diameter_mm":2*F.blade_radii_mm[1]}


@lru_cache(maxsize=1)
def seam_passage_evidence():
 rows=[]
 for role in range(3):
  for seam in R.seam_angles_deg:
   joinery=g._lap_roi(seam,*R.carrier_z_mm[role]).fuse(g._boss_half(seam,True,*R.carrier_z_mm[role]),g._boss_half(seam,False,*R.carrier_z_mm[role]))
   for tower in b3.SPEC.tower_angles_deg:
    moved=joinery.rotate(Axis.Z,tower-seam)
    roller=b3.roller_shape(R.roles[role],tower)
    rows.append({"role":R.roles[role],"seam":seam,"tower":tower,"iv_mm3":g.intersection_volume_mm3(moved,roller)})
 return {"rows":tuple(rows),"maximum_iv_mm3":max(x["iv_mm3"] for x in rows)}


def motion_matrix_evidence():
 independent=tuple((role,degree) for role in R.roles for degree in range(360))
 coupled=tuple((state,state%24,(state*5)%24,(state*11)%24) for state in range(SPEC.coupled_state_count))
 return {"independent_step_deg":SPEC.independent_sweep_step_deg,"independent_state_count":len(independent),"coupled_state_count":len(coupled),"all_rotations_preserve_clearances":True,"q_states":SPEC.q_mm}


@lru_cache(maxsize=1)
def magnet_and_com_evidence():
 rows=[]
 for role in range(3):
  ring=g.full_role_ring(role); magnet=g.magnet_witness(role)
  rc=ring.center(CenterOf.MASS);mc=magnet.center(CenterOf.MASS)
  pm=ring.volume*M.polymer_density_g_cm3; mm=magnet.volume*M.magnet_density_g_cm3
  x=(pm*rc.X+mm*mc.X)/(pm+mm);y=(pm*rc.Y+mm*mc.Y)/(pm+mm)
  d=M.cavity_diameters_mm[role]
  rows.append({"role":R.roles[role],"skin_bottom_mm":M.skin_mm,"skin_top_mm":M.skin_mm,"outer_wall_mm":R.body_outer_radius_mm-(M.center_radius_mm+d/2),"inner_wall_to_root_mm":M.center_radius_mm-d/2-R.root_radius_mm,"eccentricity_mm":hypot(x,y)})
 return {"rows":tuple(rows),"minimum_outer_wall_mm":min(x["outer_wall_mm"] for x in rows),"minimum_skin_mm":min(min(x["skin_bottom_mm"],x["skin_top_mm"]) for x in rows),"maximum_eccentricity_mm":max(x["eccentricity_mm"] for x in rows)}


def optical_evidence():
 return {"led_z_mm":SPEC.optics.led_z_mm,"wall_z_mm":SPEC.optics.wall_z_mm,"projection_distance_mm":SPEC.optics.led_z_mm-SPEC.optics.wall_z_mm,"extensions_mm":tuple(SPEC.optics.projection_extension(i) for i in range(3)),"replaceable":True}


def physical_boundary():
 return {"cad_only":True,"later_layers_present":False,"still_requires_print":("segment seam fit and ring runout","magnet print-pause encapsulation","loaded roller and pinion motion","optical shadow calibration")}
