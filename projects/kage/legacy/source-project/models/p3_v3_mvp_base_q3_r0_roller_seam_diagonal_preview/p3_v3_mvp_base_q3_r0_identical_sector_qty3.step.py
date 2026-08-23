"""One Q3 sector in the validated U1 diagonal print orientation.

Print this identical part three times.  This source intentionally contains no
slicer or printer profile payload.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import printable_sector_shape


def gen_step():
    return printable_sector_shape(1)
