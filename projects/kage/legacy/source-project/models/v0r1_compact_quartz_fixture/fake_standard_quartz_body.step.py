from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from v0r1_compact_quartz_fixture_geometry import make_fake_standard_quartz_body
def gen_step(): return make_fake_standard_quartz_body()
