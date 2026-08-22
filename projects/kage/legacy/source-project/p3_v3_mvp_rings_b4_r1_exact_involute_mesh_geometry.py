"""B4-R1 composition: accepted B4-R0 rings with B2-R3 exact pinion witnesses."""
from copy import deepcopy
from build123d import Compound,Location

import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_geometry as b2r3
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_geometry as b4r0
from p3_v3_mvp_rings_b4_r1_exact_involute_mesh_spec import NAMESPACE


def assembled_shape():
 children=[];replacement=0
 for child in b4r0.assembled_shape().children:
  if "purchased_16T_output_pinion" in child.label:
   children.append(b2r3.exact_output_pinion(replacement,0.0,0.0));replacement+=1
  else: children.append(deepcopy(child))
 if replacement!=3: raise RuntimeError(f"expected 3 exact pinion replacements, got {replacement}")
 return Compound(children=children,label=f"{NAMESPACE}_assembled")


def exploded_shape():
 children=[];replacement=0
 for child in b4r0.exploded_assembly_order_shape().children:
  if "purchased_16T_output_pinion" in child.label:
   pinion=b2r3.exact_output_pinion(replacement,0.0,0.0).moved(Location((0,0,-25)))
   pinion.label=f"{NAMESPACE}_exact_pinion_install_{replacement+1}";children.append(pinion);replacement+=1
  else: children.append(deepcopy(child))
 if replacement!=3: raise RuntimeError(f"expected 3 exact pinion replacements, got {replacement}")
 return Compound(children=children,label=f"{NAMESPACE}_assembly_order_exploded")


def printable_occurrences(): return b4r0.printable_occurrences()
