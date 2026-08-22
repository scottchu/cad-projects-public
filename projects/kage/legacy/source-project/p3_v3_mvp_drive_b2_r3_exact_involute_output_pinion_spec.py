"""Frozen purchased-witness-only B2-R3 involute pinion contract."""

from dataclasses import dataclass
from pathlib import Path

ROOT=Path(__file__).resolve().parent
NAMESPACE="p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion"
MODEL_ROOT=ROOT/"models"/NAMESPACE

@dataclass(frozen=True)
class ExactPinionParameters:
 teeth:int=16
 module_mm:float=1.0
 pressure_angle_deg:float=20.0
 backlash_mm:float=0.10
 tip_truncation_mm:float=0.10
 enable_undercut:bool=True
 face_height_mm:float=2.1
 ring_teeth:int=260
 ring_backlash_mm:float=0.10
 mesh_backlash_mm:float=0.20
 ring_phase_deg:float=0.6923077
 output_axis_radius_mm:float=122.0
 q_mm:tuple[float,...]=(-0.35,0.0,0.10)
 role_names:tuple[str,...]=("hour","minute","second")
 station_angles_deg:tuple[float,...]=(0.0,120.0,240.0)
 role_faces_z_mm:tuple[tuple[float,float],...]=((0.0,2.1),(6.7,8.8),(13.4,15.5))
 brep_tolerance_mm3:float=1e-6

 @property
 def ratio(self): return self.ring_teeth/self.teeth

SPEC=ExactPinionParameters()
