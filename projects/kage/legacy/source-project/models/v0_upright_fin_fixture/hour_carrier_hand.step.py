from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from v0_upright_fin_fixture_geometry import make_hour_carrier_hand

def gen_step():
    return make_hour_carrier_hand()
