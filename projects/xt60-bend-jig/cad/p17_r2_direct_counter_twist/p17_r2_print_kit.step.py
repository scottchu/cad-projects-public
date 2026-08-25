from xt60_bend_jig.p17_r2_direct_counter_twist import build_artifact, parameters_from_env


def gen_step():
    return build_artifact("print_kit", parameters_from_env())
