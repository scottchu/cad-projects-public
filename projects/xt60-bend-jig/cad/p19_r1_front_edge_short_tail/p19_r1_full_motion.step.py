from xt60_bend_jig.p19_r1_front_edge_short_tail import build_full_motion_open, parameters_from_env


def gen_step():
    return {
        "shape": build_full_motion_open(parameters_from_env()),
        "params": "p19_r1_full_motion.params.js",
    }
