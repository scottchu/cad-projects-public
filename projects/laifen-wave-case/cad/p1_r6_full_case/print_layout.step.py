"""R6 default 39mm full-case review target; no physical acceptance implied."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent.parent))
from p1_r6_full_case.params import Params
from p1_r6_full_case.parts import print_layout

def gen_step():
    return print_layout(Params())
