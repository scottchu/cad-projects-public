from xt60_bend_jig.p20_r2_fixed_rod_arc_rail import build_full_motion_open, parameters_from_env


def gen_step():
    return {
        "shape": build_full_motion_open(parameters_from_env()),
        "params": "p20_r2_full_motion.params.js",
    }
