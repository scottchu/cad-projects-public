from xt60_bend_jig.p17_r2_direct_counter_twist import (
    build_full_motion_open,
    parameters_from_env,
)


def gen_step():
    return {
        "shape": build_full_motion_open(parameters_from_env()),
        "params": "p17_r2_full_motion.params.js",
    }
