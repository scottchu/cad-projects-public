"""Original R3 generic-cylinder default review target."""
from pathlib import Path
import sys
from dataclasses import replace
sys.path.insert(0,str(Path(__file__).parent.parent))
from p1_r3_generator.params import Params
from p1_r3_generator.parts import build_body,build_cap,build_assembly,print_layout

def gen_step():
    return print_layout(Params())
