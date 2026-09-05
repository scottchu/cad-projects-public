"""CDE-01 explicit source entry; assembly coordinates unless print_layout."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from coupon import print_layout

def gen_step():
    return print_layout()
