import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_mvp_base_q4_r2_screw_only_geometry import service_exploded_shape


def gen_step():
    return service_exploded_shape()
