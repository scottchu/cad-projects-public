import json
from pathlib import Path
import subprocess
import sys

import pytest

from optical_spec import (
    UPRIGHT_FIN_REFERENCE,
    baffle_clear_radius,
    baffle_clear_radius_for_full_angle,
    carrier_radii,
    cone_radius,
    fin_shadow_interval,
    fin_z_for_projected_radius,
    led_nearest_fin_gap,
    optical_depth,
    project_point_to_wall,
    projected_mask_radius,
    projected_radius,
    projected_tangential_width,
    radial_envelope_clearance,
    required_mask_radius,
    full_angle_to_half_angle_degrees,
    normalize_led_full_angle_degrees,
    upright_fin_reference,
)


def test_frozen_reference_constants_are_the_compact_default():
    assert UPRIGHT_FIN_REFERENCE["source_z"] == pytest.approx(40)
    assert UPRIGHT_FIN_REFERENCE["carrier_pitch"] == pytest.approx(4.75)
    expected = {
        "hour": {"radius":30.0,"base_z":15.0,"tip_z":25.882352941,"target_tip_radius":85.0},
        "minute": {"radius":34.75,"base_z":11.041666667,"tip_z":27.363636364,"target_tip_radius":110.0},
        "second": {"radius":39.5,"base_z":7.083333333,"tip_z":27.846153846,"target_tip_radius":130.0},
    }
    assert set(UPRIGHT_FIN_REFERENCE["fins"]) == set(expected)
    for name, values in expected.items():
        assert UPRIGHT_FIN_REFERENCE["fins"][name] == pytest.approx(values)


def test_normative_upright_fin_equations():
    assert projected_radius(68,30,25.5) == pytest.approx(48)
    assert projected_radius(68,30,44) == pytest.approx(85)
    assert projected_radius(68,35,18.416666667) == pytest.approx(48,abs=1e-6)
    assert projected_radius(68,35,46.363636364) == pytest.approx(110,abs=1e-6)
    assert projected_radius(68,40,11.333333333) == pytest.approx(48,abs=1e-6)
    assert projected_radius(68,40,47.076923077) == pytest.approx(130,abs=1e-6)
    assert [fin_shadow_interval(68,*args)["shadow_length"] for args in ((30,25.5,44),(35,18.416666667,46.363636364),(40,11.333333333,47.076923077))] == pytest.approx([37,62,82],abs=1e-6)
    assert projected_tangential_width(68,2.4,44) == pytest.approx(6.8)
    assert projected_tangential_width(68,2.4,46.363636364) == pytest.approx(7.542857143)
    assert projected_tangential_width(68,2.4,47.076923077) == pytest.approx(7.8)
    assert required_mask_radius(68,50,6) == pytest.approx(45.588235294)
    assert projected_mask_radius(68,45.588235294,6) == pytest.approx(50)
    assert cone_radius(68,130,39.230769231) == pytest.approx(55)
    assert baffle_clear_radius(3,65,1) == pytest.approx(7.433520762)
    assert radial_envelope_clearance((29.2,30.8),(34.2,35.8)) == pytest.approx(3.4)


def test_inverse_fin_sizing_round_trips_and_all_corner_rays_remain_ordered():
    reference=upright_fin_reference()
    source=reference["source_z"]
    for fin in reference["fins"].values():
        assert fin_z_for_projected_radius(source,fin["radius"],fin["start_radius"]) == pytest.approx(fin["base_z"])
        assert fin_z_for_projected_radius(source,fin["radius"],fin["tip_radius"]) == pytest.approx(fin["tip_z"])
        projected=[]
        for radius in (fin["radius"]-.8,fin["radius"]+.8):
            for z in (fin["base_z"],fin["tip_z"]):
                for tangential in (-1.2,1.2):
                    projected.append((projected_radius(source,radius,z),projected_tangential_width(source,abs(tangential),z)))
        assert len(projected)==8
        assert min(radius for radius,_ in projected)>0
        assert max(radius for radius,_ in projected)>fin["tip_radius"]


def test_source_axis_offset_is_explicit_not_silently_radialized():
    zero=project_point_to_wall((0,0,68),(0,30,25.5)); shifted=project_point_to_wall((2,-1,68),(0,30,25.5))
    assert zero == pytest.approx({"x":0,"y":48,"scale":1.6,"source_axis_offset_warning":False})
    assert shifted["source_axis_offset_warning"] is True
    assert (shifted["x"],shifted["y"]) != pytest.approx((0,48))


@pytest.mark.parametrize("call",[
    lambda:projected_radius(10,3,10),lambda:projected_radius(10,-1,2),lambda:fin_z_for_projected_radius(10,3,2),lambda:projected_tangential_width(10,-1,2),lambda:required_mask_radius(10,4,0),lambda:cone_radius(10,4,11),lambda:baffle_clear_radius(3,90,1),lambda:radial_envelope_clearance((3,2),(5,6)),
])
def test_nonphysical_inputs_are_rejected(call):
    with pytest.raises(ValueError): call()


def test_cli_upright_optics_matches_callable_reference():
    executable=Path(sys.executable).parent/"kage-clock"; result=subprocess.run([str(executable),"upright-optics","--json"],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    payload=json.loads(result.stdout); assert payload["calculation"]=="upright-fin-optics"; assert payload["result"]==upright_fin_reference()
    assert payload["custom"]["fin"]["start_radius"] == pytest.approx(48)
    assert payload["custom"]["fin"]["tip_radius"] == pytest.approx(85)
    assert payload["custom"]["mask_physical_radius"] == pytest.approx(42.5)
    assert payload["custom"]["cone_radius"] == pytest.approx(55)
    assert payload["custom"]["baffle_clear_radius"] == pytest.approx(12.196152423)
    assert payload["custom"]["led_clear_full_angle_degrees"] == pytest.approx(150)
    assert payload["custom"]["optical_half_angle_degrees"] == pytest.approx(75)

    custom=subprocess.run([str(executable),"upright-optics","--json","--source-z","80","--fin-radius","32","--base-z","20","--tip-z","50","--fin-width","3","--mask-z","8","--mask-wall-radius","52","--wall-radius","140","--cone-plane-z","40","--baffle-distance","4","--half-angle","60","--margin","1.5"],capture_output=True,text=True)
    assert custom.returncode==0,custom.stderr
    data=json.loads(custom.stdout)["custom"]
    assert data["fin"]["start_radius"] == pytest.approx(projected_radius(80,32,20))
    assert data["fin"]["tip_radius"] == pytest.approx(projected_radius(80,32,50))
    assert data["fin"]["projected_tip_width"] == pytest.approx(projected_tangential_width(80,3,50))


def test_full_angle_boundary_is_finite_or_explicitly_unbounded_and_cli_safe():
    assert normalize_led_full_angle_degrees(999) == pytest.approx(180)
    assert full_angle_to_half_angle_degrees(180) == pytest.approx(90)
    assert full_angle_to_half_angle_degrees(150) == pytest.approx(75)
    assert baffle_clear_radius_for_full_angle(3, 180, 1) is None

    executable=Path(sys.executable).parent/"kage-clock"
    result=subprocess.run([str(executable),"upright-optics","--json","--full-angle","999"],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    custom=json.loads(result.stdout)["custom"]
    assert custom["led_clear_full_angle_degrees"] == pytest.approx(180)
    assert custom["optical_half_angle_degrees"] == pytest.approx(90)
    assert custom["full_angle_was_clamped"] is True
    assert custom["baffle_clear_radius"] is None
    assert custom["baffle_clearance_unbounded"] is True


def test_python_carrier_pitch_helpers_and_reference_match_browser_contract():
    assert carrier_radii(4) == {"hour":30,"minute":34,"second":38}
    assert carrier_radii(5) == {"hour":30,"minute":35,"second":40}
    assert carrier_radii(5.75) == {"hour":30,"minute":35.75,"second":41.5}
    for pitch in (4,5,5.75):
        reference=upright_fin_reference(68,pitch)
        assert reference["carrier_radii"] == carrier_radii(pitch)
        assert reference["radial_clearances"] == pytest.approx({"hour_to_minute":pitch-1.6,"minute_to_second":pitch-1.6})
        assert reference["led_nearest_fin_gap"] == pytest.approx(led_nearest_fin_gap(68,reference["fins"]))
        for fin in reference["fins"].values():
            assert projected_radius(68,fin["radius"],fin["base_z"]) == pytest.approx(48)
            assert projected_radius(68,fin["radius"],fin["tip_z"]) == pytest.approx(fin["tip_radius"])


def test_cli_carrier_pitch_option_matches_callable_reference():
    executable=Path(sys.executable).parent/"kage-clock"
    result=subprocess.run([str(executable),"upright-optics","--json","--source-z","55","--carrier-pitch","5.75"],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["result"] == upright_fin_reference(55,5.75)


def test_compact_default_and_optical_depth_match_browser_handoff():
    reference=upright_fin_reference()
    assert reference["source_z"] == 40
    assert reference["carrier_pitch"] == pytest.approx(4.75)
    assert reference["carrier_radii"] == pytest.approx({"hour":30,"minute":34.75,"second":39.5})
    assert reference["led_nearest_fin_gap"] == pytest.approx(12.153846,abs=1e-6)
    assert reference["optical_depth"] == pytest.approx(46)
    assert [optical_depth(value) for value in (52,60,75)] == pytest.approx([58,66,81])
