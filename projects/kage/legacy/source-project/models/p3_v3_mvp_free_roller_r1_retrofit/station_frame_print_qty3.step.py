from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_mvp_free_roller_r1_retrofit_geometry import make_station_frame_print


def gen_step():
    return make_station_frame_print()
