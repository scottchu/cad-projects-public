"""Cheap contract checks for the self-contained OpenSCAD Customizer V1."""
from pathlib import Path
import subprocess
import sys

PROJECT = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT))

from openscad.customizer_contract import (
    derive,
    diamond_constraints,
    diamond_coordinates,
    diamond_count,
    diamond_field,
    diamond_global_z,
    diamond_patch_coordinates,
    diamond_patch_inverse,
    diamond_radius,
    diamond_wrap,
    split_from_mode,
)


SCAD = PROJECT / "openscad" / "laifen_case_customizer_v1.scad"


def test_default_contract_matches_p1_r7_envelope_and_split_projection():
    result = derive()
    assert result.cavity == 213
    assert result.engagement == 6
    assert result.overlap == 9
    assert result.body_height == 144
    assert result.cap_height == 84
    assert result.split_percent == 84 / 219 * 100
    assert result.lattice_count >= 8 and result.arc_pitch > 0


def test_split_mode_round_trip_and_boundaries_are_explicit():
    total = 219
    percent = 100 * 84 / total
    assert split_from_mode(total, "distance", 84, 1) == 84
    assert split_from_mode(total, "percentage", 1, percent) == 84
    assert derive(split_mode="percentage", split_percent_from_top=percent).cap_height == 84
    for kwargs in ({"outer_diameter": 35}, {"thread_clearance": .31}, {"split_distance_from_top": 14}):
        try:
            derive(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected invalid contract: {kwargs}")


def test_scad_declares_customizer_groups_outputs_and_original_functional_features():
    source = SCAD.read_text(encoding="utf-8")
    for group in ("Preset / device", "Envelope", "Split — one canonical source", "Thread", "Surface", "Drainage", "Output"):
        assert f"/* [{group}] */" in source
    for option in ("assembled", "body", "cap", "print_layout", "none", "top", "bottom", "smooth", "diamond"):
        assert option in source
    for module in ("body_shell", "cap_shell", "body_thread", "female_thread_void", "drain_pattern", "diamond_exterior"):
        assert f"module {module}" in source
    assert "closure_overlap = engagement + 3" in source
    assert "assert(" in source
    assert "import(" not in source and "use <" not in source


def test_real_female_thread_and_constructive_chamfers_cannot_regress():
    source = SCAD.read_text(encoding="utf-8")
    assert "cylinder(r=thread_root_radius+thread_clearance, h=closure_overlap);" in source
    assert "translate([0,0,thread_transition]) female_thread_groove();" in source
    assert "threaded cap wall below 1.8mm" in source
    assert "h=.4" in source and "thread_root_radius+thread_clearance+.4" in source
    assert "thread_crest_radius+thread_clearance+thread_depth" not in source
    assert "body_outer_blank" in source and "cap_outer_blank" in source
    assert "translate([0,0,-.01]) cylinder(r1=" not in source
    assert "sphere(" not in source
    assert "polyhedron(points=mesh[0],faces=mesh[1]" in source
    assert "function v06_data(" in source and "function v06_direct(" in source
    assert "diamond_first_index" not in source and "search(" not in source
    assert "helical_v_groove_field" not in source and "diamond_grooves" not in source


def test_thread_roots_have_positive_constructive_overlap_without_moving_crests():
    source = SCAD.read_text(encoding="utf-8")
    assert "THREAD_EMBED_EPS = .05;" in source
    assert "THREAD_EMBED_EPS > 0 && THREAD_EMBED_EPS < min(thread_depth, thread_clearance)" in source
    profile = "[[-THREAD_EMBED_EPS,-thread_pitch*.32],[thread_depth,0],[-THREAD_EMBED_EPS,thread_pitch*.32]]"
    # Both root volumes now overlap the respective cylinder/void.  The crest
    # coordinate remains thread_depth, so radial clearance is unchanged.
    assert source.count(profile) == 2
    assert "translate([thread_root_radius,0]) polygon(" in source
    assert "translate([thread_root_radius+thread_clearance,0]) polygon(" in source


def test_diamond_field_uses_valley_count_shared_seam_phase_and_single_exterior():
    source = SCAD.read_text(encoding="utf-8")
    assert "diamond_plateau_half_fraction = 0.18" in source
    assert "diamond_count(valley_radius, diamond_arc_pitch)" in source
    assert "floor(2 * PI * r_valley / target_arc + 0.5)" in source
    assert "diamond_coordinates(theta_deg, z_global, phase_deg, seam_z" in source
    assert "diamond_exterior(body_thread_z, 0)" in source
    assert "diamond_exterior(cap_height, cap_close_z)" in source
    assert "surface_style != \"diamond\" || diamond_depth == 0" in source
    assert "DIAMOND_MAX_EXTERIOR_TRIANGLES = 250000" in source
    assert "translate([0,0,body_thread_z-1]) cylinder(r=outer_radius, h=1);" in source
    assert "if (surface_style != \"diamond\" || diamond_depth == 0)" in source


def test_vfr04_independent_math_oracle_covers_count_field_phase_and_constraints():
    result = derive()
    assert result.lattice_count == 33
    assert abs(result.arc_pitch - 3.627111518234579) < 1e-12
    assert abs(result.diamond.plateau_width - 1.041776914) < 1e-9
    assert abs(result.diamond.axial_slope - 0.29296875) < 1e-12
    assert abs(result.diamond.body_valley_wall - 4.05) < 1e-12
    assert abs(result.diamond.cap_valley_wall - 3.55) < 1e-12
    assert abs(result.diamond.female_thread_valley_wall - 1.9) < 1e-12
    assert result.diamond.estimated_exterior_triangles <= 250_000

    # Positive half-up differs from Python's round at an even .5 boundary.
    target = 3.63
    from math import pi
    assert diamond_count(8.5 * target / (2 * pi), target) == 9
    assert diamond_count((8.5 - 1e-9) * target / (2 * pi), target) == 8
    for t in (-1.5, -0.5, 0.5, 1.5):
        assert diamond_wrap(t) == -0.5
    assert diamond_wrap(-0.5 + 1e-9) > -0.5
    assert diamond_field(0, 0, .18) == 1
    assert diamond_field(.5, 0, .18) == 0
    assert 19.05 <= diamond_radius(19.05, .45, .24, .11, .18) <= 19.5

    uv_body = diamond_coordinates(0, diamond_global_z("body", 135, 135), 0, 135, 33, 4.8)
    uv_cap = diamond_coordinates(0, diamond_global_z("cap", 0, 135), 0, 135, 33, 4.8)
    assert uv_body == uv_cap == (0, 0)
    assert diamond_coordinates(360, 135, 0, 135, 33, 4.8)[0] == 33
    st = (1.25, -.75)
    assert diamond_patch_inverse(*diamond_patch_coordinates(*st)) == st

    for kwargs in (
        {"depth": .6},
        {"plateau_half_fraction": .10},
        {"target_arc": .1},
        {"band_height": 400},
    ):
        try:
            diamond_constraints(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected invalid diamond contract: {kwargs}")


def test_depth_zero_diamond_is_exact_smooth_equivalent_and_ignores_plateau_constraints():
    c = diamond_constraints(depth=0, plateau_half_fraction=0.5)
    assert c.plateau_width == 0 and c.axial_slope == 0
    assert diamond_radius(19.5, 0, .5, .5, .18) == 19.5
    source = SCAD.read_text(encoding="utf-8")
    assert 'surface_style == "diamond" && diamond_depth > 0' in source
    assert 'surface_style != "diamond" || diamond_depth == 0' in source


def test_real_pinned_openscad_executes_vfr04_math_witnesses():
    runner = PROJECT / "openscad" / "run_math_probe.mjs"
    completed = subprocess.run(
        ["node", str(runner)], cwd=PROJECT.parents[1], text=True,
        capture_output=True, timeout=20, check=True,
    )
    output = completed.stdout
    assert '"VFR04_COUNT", 33' in output
    assert '"VFR04_HALF_UP", 9' in output
    assert '"VFR04_FIELD", 1, 0' in output
    assert '"VFR04_PATCH", [1.25, -0.75]' in output
    assert '"VFR04_SEAM", [0, 0], [0, 0]' in output
