from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p2r2_magnetic_three_channel_300mm_geometry import make_assembled
def gen_step(): return make_assembled(2.0)
