from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_transmission_r1_geometry import make_assembled


def gen_step():
    return make_assembled()
