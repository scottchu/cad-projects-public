import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_geometry import assembled_shape
def gen_step(): return assembled_shape()
