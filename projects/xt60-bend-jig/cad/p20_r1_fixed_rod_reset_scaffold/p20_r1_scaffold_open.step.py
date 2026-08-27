from xt60_bend_jig.p20_r1_fixed_rod_reset_scaffold import build_motion_state, parameters_from_env


def gen_step():
    return build_motion_state("open", parameters_from_env())
