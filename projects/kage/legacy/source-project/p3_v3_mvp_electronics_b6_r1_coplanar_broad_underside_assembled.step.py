"""CAD entry generator for the assembled B6-R1 electronics backbone MVP."""

import p3_v3_mvp_electronics_b6_r1_coplanar_broad_underside_geometry as geometry


def gen_step():
    return geometry.assembled_shape()
