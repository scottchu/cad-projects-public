"""Phase-A risks: infeasible stacks, field drift and thread normalization."""
from dataclasses import FrozenInstanceError, asdict, replace
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest

CAD = Path(__file__).parents[1]/"cad"
sys.path.insert(0,str(CAD))
from p1_r3_generator.params import Params, derive, preset
from p1_r3_generator.skin import envelope, facet_polygons, field, radius, tessellation_plan
from p1_r3_generator import thread_profile as thread


def test_default_stack_and_constant_pitch_extension():
    """Catch a misleading short coupon or texture stretched with length."""
    p = Params()
    d = derive(p)
    assert d.body_band == pytest.approx((-30.1,-6.1))
    assert d.cap_band == pytest.approx((14.4,38.4))
    assert d.minimum_cavity_length == pytest.approx(72.5)
    assert d.outer_length == pytest.approx(78.5)
    assert d.lattice_count == 31
    assert d.body_plateau_width >= 1
    with pytest.raises(FrozenInstanceError): p.wall = 9
    with pytest.raises(ValueError,match="cavity_length >= 72.5"):
        derive(replace(p,cavity_length=60))
    longer = replace(p,cavity_length=82.1)
    dl = derive(longer)
    assert dl.body_band[1]-dl.body_band[0] == pytest.approx(24+2*p.skin_axial_pitch)
    assert dl.cap_band == d.cap_band
    assert dl.lattice_count == d.lattice_count
    for theta,z in ((.7,-18.1),(2.1,-22.4)):
        assert field(p,theta,z) == pytest.approx(field(longer,theta,z+2*p.skin_axial_pitch))


def test_feasible_parameter_changes_and_domain_failures():
    """Catch wall, pitch/engagement, bluntness and support budget violations."""
    changed = replace(Params(),thread_pitch=2.4,engagement=7.2,cavity_length=82.1,cap_height=47)
    d = derive(changed)
    assert d.full_thread_end-d.full_thread_start == pytest.approx(7.2)
    smaller = replace(Params(),body_bore=24,cap_bore=25)
    ds = derive(smaller)
    assert ds.body_inner_radius == 12 and ds.cap_inner_radius == 12.5
    for kwargs,reason in (({"wall":1.7},"wall"),({"skin_height":.6,"skin_style":"smooth_crosswave"},"slope"),
                          ({"plateau_half_fraction":.1},"plateau"),({"floor":float("nan")},"finite"),
                          ({"skin_arc_pitch_target":1e-300},"lattice_count"),
                          ({"max_od":38},"diameter"),({"skin_phase_z":1e308},"phase")):
        with pytest.raises(ValueError,match=reason): derive(replace(Params(),**kwargs))
    with pytest.raises(ValueError,match="pending"): preset("laifen-provisional")
    with pytest.raises(ValueError,match="locks"): preset("short-grip",max_od=45)
    assert derive(preset("generic",max_od=45)).minimum_wall >= 1.8-1e-10


def test_exact_field_seam_envelope_and_tessellation_budget():
    """Catch a seam, missing end fades, open cell gaps or optimistic error budget."""
    p = Params()
    d = derive(p)
    assert field(p,0,0) == 1
    assert field(p,math.pi/d.lattice_count,0) == 0
    for role in ("body","cap"):
        band = getattr(d,role+"_band")
        R = getattr(d,role+"_radius")
        for z in (band[0],band[0]+1,band[0]+3,band[1]):
            assert radius(p,role,0,z) == pytest.approx(radius(p,role,2*math.pi,z))
            assert R <= radius(p,role,.4,z) <= R+p.skin_height
        assert envelope(band[0],band,p.fade_length) == 0
        assert envelope(band[0]+p.fade_length,band,p.fade_length) == 1
        plan = tessellation_plan(p,role)
        assert plan.angular_error_bound+plan.axial_error_bound+plan.mixed_error_bound <= .005
        assert plan.crease_split_required
    polys = facet_polygons(p,0,0)
    area = lambda poly: abs(sum(x*y2-x2*y for (x,y),(x2,y2) in zip(poly,poly[1:]+poly[:1])))/2
    assert sum(area(poly) for poly in polys) == pytest.approx(.5)
    # Sample the actual selected field, including fade, for analytic slope errors.
    for z in (-30.1,-29.7,-28.7,-20.3,-6.6):
        for theta in (.021,.17,.71):
            dz = 1e-6
            slope = abs((radius(p,"body",theta,z+dz)-radius(p,"body",theta,z-dz))/(2*dz))
            assert slope <= d.skin_slope_bound+1e-7


def test_default_thread_matches_frozen_r2_equations():
    """Catch phase, flank, lead or root drift in the one shared R3 profile."""
    spec = importlib.util.spec_from_file_location("frozen_r2_coupon",CAD/"p1_r2_coupons"/"coupon.py")
    r2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r2)
    p = Params()
    for theta in (0,math.pi/2,math.pi,3*math.pi/2):
        for z in (0,.5,1,1.15,1.5,2,2.15,2.85,3,4,6.5,7,7.85,8,8.5,8.999,9):
            assert thread.male_radius(p,theta,z) == pytest.approx(r2.male_radius(theta,z),abs=1e-12)
            for c in (.2,.25,.3):
                assert thread.female_radius(p,theta,z,c) == pytest.approx(r2.female_radius(theta,z,c),abs=1e-12)
    assert thread.male_radius(p,0,3) == pytest.approx(16.8)
    assert thread.male_radius(p,0,4) == pytest.approx(17.4)


def test_cli_overrides_rejections_and_honest_acceptance():
    """Catch ignored user input, successful invalid exits or fake CAD acceptance."""
    command = [sys.executable,str(CAD/"p1_r3_generator"/"generator.py")]
    result = subprocess.run(command+["--cavity-length","82.1","--dry-run"],capture_output=True,text=True)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["parameters"]["cavity_length"] == 82.1
    assert payload["acceptance"]["cad"] == "pending"
    for args in (["--cavity-length","60"],["--preset","laifen-provisional"],["--write-step"]):
        result = subprocess.run(command+args,capture_output=True,text=True)
        assert result.returncode == 2
        assert not result.stdout
        assert json.loads(result.stderr)["status"] == "rejected"
