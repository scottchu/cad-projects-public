"""Exact involute purchased output-pinion witness for B2-R3."""

from copy import deepcopy
from functools import lru_cache
from math import radians

from build123d import Axis,Compound,Location
import py_gearworks as pgw

import p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_geometry as b2
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as b3
from p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_spec import NAMESPACE,SPEC


def exact_output_pinion(role_index:int,q_mm:float=0.0,theta_deg:float=0.0):
 z0,z1=SPEC.role_faces_z_mm[role_index]
 ring=pgw.SpurRingGear(number_of_teeth=SPEC.ring_teeth,module=SPEC.module_mm,height=z1-z0,center=[0,0,z0],backlash=SPEC.ring_backlash_mm)
 pinion=pgw.SpurGear(number_of_teeth=SPEC.teeth,module=SPEC.module_mm,height=z1-z0,center=[0,0,z0],pressure_angle=radians(SPEC.pressure_angle_deg),backlash=SPEC.backlash_mm,tip_truncation=SPEC.tip_truncation_mm,enable_undercut=SPEC.enable_undercut)
 pinion.mesh_to(ring,target_dir=pgw.RIGHT,backlash=SPEC.mesh_backlash_mm)
 shape=pinion.build_part().solid().moved(Location((q_mm,0,0)))
 alpha=SPEC.station_angles_deg[role_index]
 axis_radius=SPEC.output_axis_radius_mm+q_mm
 phase=(SPEC.ring_phase_deg-alpha+theta_deg)*SPEC.ratio
 shape=shape.rotate(Axis((axis_radius,0,0),(0,0,1)),phase).rotate(Axis.Z,alpha)
 shape.label=f"{NAMESPACE}_{SPEC.role_names[role_index]}_purchased_exact_16T_q{q_mm:+.2f}_theta{theta_deg:+.6f}"
 return shape


def exact_ring_tooth_witness(role_index:int,theta_deg:float=0.0):
 z0,z1=SPEC.role_faces_z_mm[role_index]
 shape=pgw.SpurRingGear(number_of_teeth=SPEC.ring_teeth,module=SPEC.module_mm,height=z1-z0,center=[0,0,z0],backlash=SPEC.ring_backlash_mm).build_part().solid()
 shape=shape.rotate(Axis.Z,SPEC.ring_phase_deg+theta_deg)
 shape.label=f"{NAMESPACE}_{SPEC.role_names[role_index]}_existing_exact_260T_tooth_witness_theta{theta_deg:+.6f}"
 return shape


def inherited_children_with_exact_pinions(q_mm:float=0.0):
 children=[];replacement=0
 for child in b3.inherited_b2_children_with_clean_input_bevels(q_mm):
  if "purchased_16T_output_pinion" in child.label:
   children.append(exact_output_pinion(replacement,q_mm,0.0));replacement+=1
  else: children.append(deepcopy(child))
 if replacement!=3: raise RuntimeError(f"expected 3 output pinions, replaced {replacement}")
 return tuple(children)


def assembled_shape(q_mm:float=0.0):
 return Compound(children=list(inherited_children_with_exact_pinions(q_mm)),label=f"{NAMESPACE}_assembled_q{q_mm:+.2f}")


def printed_geometry_unchanged_evidence():
 before=b2.model_only_shape();after=Compound(children=[deepcopy(row["shape"]) for row in b2.printable_occurrences()])
 return {"before_solids":len(before.solids()),"after_solids":len(after.solids()),"volume_delta_mm3":abs(sum(s.volume for s in before.solids())-sum(s.volume for s in after.solids())),"bounds_equal":before.bounding_box()==after.bounding_box()}
