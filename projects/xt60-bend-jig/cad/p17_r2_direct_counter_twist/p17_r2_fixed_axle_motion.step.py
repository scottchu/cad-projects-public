from xt60_bend_jig.p17_r2_direct_counter_twist import (
    build_fixed_axle_focus_state,
    parameters_from_env,
)


def gen_step():
    return {
        "shape": build_fixed_axle_focus_state(0.0, parameters_from_env()),
        "params": "p17_r2_fixed_axle_motion.params.js",
    }
