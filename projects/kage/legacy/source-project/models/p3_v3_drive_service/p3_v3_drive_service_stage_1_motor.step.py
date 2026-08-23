from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_drive_service_geometry import make_stage_1_motor
def gen_step(): return make_stage_1_motor()
