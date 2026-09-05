"""R5 default 39mm short-cylinder review target; no physical acceptance implied."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent.parent))
from p1_r5_39mm_case.params import Params
from p1_r5_39mm_case.parts import build_assembly

def gen_step():
    return build_assembly(Params())
