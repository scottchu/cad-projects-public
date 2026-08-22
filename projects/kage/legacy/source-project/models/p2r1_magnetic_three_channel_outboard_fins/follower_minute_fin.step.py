from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p2r1_magnetic_three_channel_outboard_fins_geometry import make_follower
def gen_step(): return make_follower("minute", 1.5)
