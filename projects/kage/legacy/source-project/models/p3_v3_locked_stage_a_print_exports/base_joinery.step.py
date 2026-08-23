from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_locked_stage_a_print_exports import pack_shape
def gen_step(): return pack_shape("base_joinery")
