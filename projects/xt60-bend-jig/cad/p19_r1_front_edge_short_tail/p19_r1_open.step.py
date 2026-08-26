from xt60_bend_jig.p19_r1_front_edge_short_tail import build_artifact, parameters_from_env


def gen_step():
    return build_artifact("open", parameters_from_env())
