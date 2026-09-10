from xt60_bend_jig.p20_r2_fixed_rod_arc_rail import parameters_from_env
from xt60_bend_jig.p20_r3_wire_90deg import build_full_motion_open


def gen_step():
    return {
        "shape": build_full_motion_open(parameters_from_env()),
        "params": "p20_r3_full_motion.params.js",
    }
