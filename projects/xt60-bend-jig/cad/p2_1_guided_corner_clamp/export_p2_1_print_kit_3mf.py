from pathlib import Path

from xt60_bend_jig.p2_1_guided_corner_clamp import export_print_kit_3mf


if __name__ == "__main__":
    export_print_kit_3mf(Path(__file__).with_name("p2_1_print_kit.3mf"))
