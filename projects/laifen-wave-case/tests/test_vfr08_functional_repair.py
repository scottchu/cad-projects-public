"""Focused source and transform regressions for VFR-08."""
from pathlib import Path
import re

SCAD = Path(__file__).parents[1] / "openscad" / "laifen_case_customizer_v1.scad"


def test_vfr08_drain_cutters_are_forward_bounded_and_all_callers_keep_extents():
    source = SCAD.read_text(encoding="utf-8")
    block = re.search(r"module drain_pattern\(h\) \{(.*?)\n\}", source, re.S).group(1)
    assert block.count("center=false") == 2
    assert "center=true" not in block
    assert source.count("translate([0,0,-.1]) drain_pattern(floor_thickness+.2);") == 2
    assert source.count("translate([0,0,cap_height-floor_thickness-.1]) drain_pattern(floor_thickness+.2);") == 2


def test_vfr08_print_cap_transform_is_only_layout_change_and_is_open_end_up():
    source = SCAD.read_text(encoding="utf-8")
    layout = re.search(r"module print_layout\(\) \{(.*?)\n\}", source, re.S).group(1)
    assert "translate([outer_diameter/2+3.5,0,0])" in layout
    assert "translate([-outer_diameter/2-3.5,0,cap_height])" in layout
    assert "rotate([180,0,0]) color(\"#77b09a\") cap_shell();" in layout
    assert "translate([0,0,cap_close_z]) color(\"#77b09a\") cap_shell();" in source


def test_vfr08_default_axial_intervals_and_rigid_map():
    floor, height = 3.0, 84.0
    assert (-0.1, floor + 0.1) == (-0.1, 3.1)
    assert (height - floor - 0.1, height + 0.1) == (80.9, 84.1)
    # rotate([180,0,0]) then translate([-23,0,84])
    def pose(p):
        x, y, z = p
        return (-23 + x, -y, 84 - z)
    assert pose((0, 0, height)) == (-23, 0, 0)
    assert pose((0, 0, 0)) == (-23, 0, height)
    assert pose((2.0, 3.0, 11.0)) == (-21.0, -3.0, 73.0)
