"""Frozen B4-R1 actual-involute probe contract."""
from dataclasses import dataclass
from pathlib import Path

ROOT=Path(__file__).resolve().parent
NAMESPACE="p3_v3_mvp_rings_b4_r1_exact_involute_mesh"
MODEL_ROOT=ROOT/"models"/NAMESPACE

@dataclass(frozen=True)
class ProbeParameters:
 flank_distance_mm:tuple[float,float]=(0.04,0.25)
 engagement_mm:tuple[float,float]=(1.65,2.10)
 seam_phase_fraction:float=0.05
 contact_skin_mm:float=0.02
 contact_area_min_mm2:float=76.8
 contact_area_spread_max_mm2:float=0.5
 brep_tolerance_mm3:float=1e-6
 compact_coupled_states:tuple[tuple[float,float,float],...]=((0,0,0),(.6923077,0,0),(0,.6923077,0),(0,0,.6923077),(.6923077,.6923077,.6923077),(-.06923077,.06923077,0))

SPEC=ProbeParameters()
