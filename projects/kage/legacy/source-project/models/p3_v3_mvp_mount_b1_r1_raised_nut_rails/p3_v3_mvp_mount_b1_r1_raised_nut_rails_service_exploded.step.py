import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry import service_exploded_shape
def gen_step(): return service_exploded_shape()
