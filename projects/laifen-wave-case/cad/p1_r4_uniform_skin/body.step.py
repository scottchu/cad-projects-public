"""R4 default short-cylinder review target; no physical acceptance implied."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent.parent))
from p1_r4_uniform_skin.params import Params
from p1_r4_uniform_skin.parts import build_body

def gen_step():
    return build_body(Params())
