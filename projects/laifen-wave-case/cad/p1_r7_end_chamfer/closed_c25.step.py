"""R7 default 39mm full-case review target; no physical acceptance implied."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent.parent))
from p1_r7_end_chamfer.params import Params
from p1_r7_end_chamfer.parts import build_assembly

def gen_step():
    return build_assembly(Params())
