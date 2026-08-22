import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import diagonal_bed_preview_shape


def gen_step():
    return diagonal_bed_preview_shape()
