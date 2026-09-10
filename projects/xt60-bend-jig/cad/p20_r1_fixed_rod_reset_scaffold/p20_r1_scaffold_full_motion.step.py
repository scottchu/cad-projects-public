from xt60_bend_jig.p20_r1_fixed_rod_reset_scaffold import build_full_motion_open, parameters_from_env


def gen_step():
    return {
        "shape": build_full_motion_open(parameters_from_env()),
        "params": "p20_r1_scaffold_full_motion.params.js",
    }
