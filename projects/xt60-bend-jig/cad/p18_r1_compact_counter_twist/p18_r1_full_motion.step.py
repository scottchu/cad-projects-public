from xt60_bend_jig.p18_r1_compact_counter_twist import build_full_motion_open, parameters_from_env


def gen_step():
    return {
        "shape": build_full_motion_open(parameters_from_env()),
        "params": "p18_r1_full_motion.params.js",
    }
