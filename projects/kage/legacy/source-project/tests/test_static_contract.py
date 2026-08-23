from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

import pytest

from p3_v3_stacked_three_motor_90deg_spec import P3_V3


ROOT = Path(__file__).resolve().parents[1]


def node_binary() -> str | None:
    return next((candidate for candidate in (shutil.which("node"), "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node") if candidate and Path(candidate).is_file()), None)


def run_js(expression: str):
    node = node_binary()
    if node is None: pytest.skip("node unavailable")
    program = f"const k=require({json.dumps(str(ROOT / 'simulator.js'))});console.log(JSON.stringify(({expression})));"
    result = subprocess.run([node, "-e", program], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.ids=set(); self.external=[]
    def handle_starttag(self, tag, attrs):
        values=dict(attrs)
        if values.get("id"): self.ids.add(values["id"])
        for key in ("href","src"):
            if values.get(key,"").startswith(("http://","https://","//")): self.external.append(values[key])


def test_page_is_the_simplified_simulator_not_editorial_card_clutter():
    html=(ROOT/"index.html").read_text(); parser=Parser(); parser.feed(html)
    assert parser.external == []
    assert html.count('class="viewer"') == 1
    assert html.count('class="controls"') == 1
    assert 'class="optical-inset is-collapsed"' in html
    assert "BUILD WALKTHROUGH" not in html
    assert "presets-row" not in html
    assert "dimensions-panel" not in html
    assert "sim-header" not in html
    for label in ("Assembly / cutaway", "Wall shadow", "Side section", "Orbital close-up", "Assembled", "Exploded"):
        assert f">{label}</button>" in html
    assert "Design layers" in html and 'id="scenarioSelect"' not in html
    assert '<option value="structure">Structure</option>' in html
    assert "P0" not in html and "P1" not in html and "P2" not in html
    controls_start=html.index('class="controls"')
    controls_end=html.index("</aside>",controls_start)
    assert html.index('id="renderer3dButton"') < controls_start
    assert controls_start < html.index('id="threeCameraToolbar"') < controls_end
    viewer_start=html.index('class="viewer"')
    viewer_end=html.index('</section>',viewer_start)
    assert viewer_start < html.index('id="renderer3dButton"') < viewer_end


def test_all_simulator_dom_lookups_exist_and_no_old_script_is_loaded():
    parser=Parser(); parser.feed((ROOT/"index.html").read_text())
    source=(ROOT/"simulator.js").read_text()
    referenced=set(re.findall(r'\$\("([A-Za-z][A-Za-z0-9_-]*)"\)',source))
    generated={f"param-{key}" for key in run_js("Object.keys(k.PARAMETERS)")} | {f"out-{key}" for key in run_js("Object.keys(k.PARAMETERS)")}
    assert referenced - parser.ids - generated == set()
    assert '<script src="script.js"></script>' not in (ROOT/"index.html").read_text()


def test_parameter_audit_is_complete_nondecorative_and_matches_visible_controls():
    audits=run_js("k.PARAMETERS")
    required={"group","label","variable","units","meaning","min","max","step","default","dependency","affected","derivedOutput","validation"}
    assert set(audits) == {"sourceZ","hourTip","minuteTip","secondTip","finWidth","finThickness","ringGap","projectedMaskRadius","maskZ","fieldFullAngle","pointIntensity","pointTemperature","shellRadius","glareCapDiameter"}
    for key,audit in audits.items():
        assert required <= set(audit)
        assert audit["variable"] == key
        if key == "fieldFullAngle":
            assert audit["min"] < audit["default"] <= audit["max"]
        else:
            assert audit["min"] < audit["default"] < audit["max"]
        assert audit["meaning"] and audit["affected"] and audit["derivedOutput"] and audit["validation"]
        assert audit["group"] in {"optics","fins","body"}

    ui=run_js("k.UI_CONTROL_AUDIT")
    expected={"renderer","cameraView","stackArrangement","opticalMode","timeSource","ambienceMode","manualHour","manualMinute","manualSecond","showQuartz","showShell","showPhysicalMask","showCarriers","showSourceHardware","showGlareCap","showProjectionRays","showHandShadows","showMaskShadow","showWallHalo","lightEnabled"}
    assert set(ui)==expected
    ui_required={"label","variable","units","physicalMeaning","min","max","allowed","default","dependency","affectedGeometryRender","derivedOutput","validationErrorBehavior"}
    for key,audit in ui.items():
        assert ui_required <= set(audit)
        assert audit["variable"]==key
        assert audit["physicalMeaning"] and audit["affectedGeometryRender"] and audit["validationErrorBehavior"]


def test_every_visible_numeric_parameter_changes_observable_state():
    result=run_js("Object.fromEntries(Object.entries(k.PARAMETERS).map(([key,a])=>{const base={...k.defaults,...(['hourTip','minuteTip','secondTip'].includes(key)?{opticalMode:'solveTargets'}:{})};const changed={...base,[key]:a.default===a.max?a.min:a.max};return [key,{before:k.observableSignature(base),after:k.observableSignature(changed)}]}))")
    for key,pair in result.items():
        changed=[field for field in pair["before"] if pair["before"][field] != pair["after"][field]]
        assert changed, f"{key} is an inert visible control"

    ui=run_js("({renderer:['3d','2d'],cameraView:['assembly','wall'],stackArrangement:['assembled','exploded'],opticalMode:['fixedHardware','solveTargets'],timeSource:['manual','realtime'],manualHour:[10,11],manualMinute:[10,11],manualSecond:[35,36],...Object.fromEntries(k.VISIBILITY_KEYS.map(key=>[key,[false,true]]))})")
    for key,(before,after) in ui.items():
        pair=run_js(f"([k.observableSignature({{...k.defaults,{key}:{json.dumps(before)}}}),k.observableSignature({{...k.defaults,{key}:{json.dumps(after)}}})])")
        assert pair[0] != pair[1], f"{key} is an inert visible UI control"


def test_presets_are_one_shot_visibility_actions_and_never_geometry_authority():
    presets=run_js("k.PRESET_VISIBILITY")
    assert set(presets) == {"structure","mechanism","optics"}
    result=run_js("(()=>{const before={...k.defaults,renderer:'2d',cameraView:'orbital',stackArrangement:'exploded',timeSource:'realtime',manualHour:7,sourceZ:73};const after=k.applyPreset(before,'mechanism');after.showShell=true;return {before,after,modelBefore:k.buildModel(before),modelAfter:k.buildModel(after)}})()")
    assert result["after"]["showQuartz"] is False and result["after"]["showShell"] is True
    for key in ("renderer","cameraView","stackArrangement","timeSource","manualHour","sourceZ"):
        assert result["after"][key] == result["before"][key]
    assert result["modelAfter"] == result["modelBefore"]


def test_global_defaults_and_independent_shadow_combinations_match_control_contract():
    defaults=run_js("k.defaults")
    assert (defaults["renderer"],defaults["cameraView"],defaults["stackArrangement"],defaults["timeSource"],defaults["ambienceMode"]) == ("3d","assembly","assembled","manual","day")
    assert (defaults["manualHour"],defaults["manualMinute"],defaults["manualSecond"]) == (10,10,35)
    assert {key:defaults[key] for key in run_js("k.VISIBILITY_KEYS")} == run_js("k.PRESET_VISIBILITY.structure")
    combos=run_js("Array.from({length:8},(_,bits)=>{const s={...k.defaults,showWallHalo:Boolean(bits&1),showMaskShadow:Boolean(bits&2),showHandShadows:Boolean(bits&4)};return [s.showWallHalo,s.showMaskShadow,s.showHandShadows]})")
    assert len({tuple(item) for item in combos}) == 8


def test_realtime_uses_clock_without_overwriting_stored_manual_values():
    result=run_js("(()=>{const manual={...k.defaults,manualHour:7,manualMinute:8,manualSecond:9,timeSource:'manual'};const realtime={...manual,timeSource:'realtime'};const now=new Date(2026,7,11,12,34,56);return {manual,manualAngles:k.clockAngles(manual,now),realtime,realtimeAngles:k.clockAngles(realtime,now)}})()")
    assert (result["realtime"]["manualHour"],result["realtime"]["manualMinute"],result["realtime"]["manualSecond"]) == (7,8,9)
    assert result["manualAngles"] != result["realtimeAngles"]


def test_reset_and_2d_fallback_contract_are_explicit_in_ui_source():
    source=(ROOT/"simulator.js").read_text()
    assert 'Object.assign(state,DEFAULT_STATE)' in source
    assert 'setTimeSource("manual")' in source
    assert 'setStackArrangement("assembled")' in source
    assert 'setCameraView("assembly")' in source
    assert 'setRenderer("3d")' in source
    assert 'resetView: () => setView(currentView)' in (ROOT/"src"/"three-scene.js").read_text()
    assert "if (state.cameraView !== 'wall')" in source
    assert 'state.cameraView=' not in source[source.index("function setRenderer"):source.index("function wireUI")]


def test_rejected_decor_redesign_cannot_reenter_the_simulator():
    sources = "\n".join((ROOT / path).read_text() for path in ("index.html", "simulator.js", "src/three-scene.js"))
    rejected = (
        "260mm-chalk-mineral-clock-body",
        "shallow-plaster-face-recess",
        "three-daylight-orbital-tracks-and-markers",
        "visible-daylight-rim-marker",
        "mineral-hour-index",
        "warm-central-corona",
        "Day</button>",
        "Evening</button>",
    )
    for token in rejected:
        assert token not in sources
    assert 'data-camera-view="assembly" class="is-active"' in (ROOT / "index.html").read_text()
    assert ".optical-inset canvas { display: none; }" in (ROOT / "styles.css").read_text()


def test_coupled_tip_constraints_clamp_and_report_impossible_optics():
    result=run_js("({normalized:k.normalizedState({...k.defaults,hourTip:200,minuteTip:201,secondTip:202}),model:k.buildModel({...k.defaults,fieldFullAngle:140,secondTip:350,projectedMaskRadius:150})})")
    normalized=result["normalized"]
    assert normalized["minuteTip"] >= normalized["hourTip"] + 10
    assert normalized["secondTip"] >= normalized["minuteTip"] + 10
    assert result["model"]["warnings"]


def test_led_full_angle_control_clamps_and_preserves_half_angle_optics():
    result=run_js("(()=>{const d=k.buildModel(k.defaults),max=k.buildModel({...k.defaults,fieldFullAngle:180}),over=k.buildModel({...k.defaults,fieldFullAngle:999}),nan=k.normalizedState({...k.defaults,fieldFullAngle:NaN});return {audit:k.PARAMETERS.fieldFullAngle,d,max,over,nan,helper:[k.fullAngleToHalfAngle(150),k.fullAngleToHalfAngle(180),k.fullAngleToHalfAngle(999)]}})()")
    assert result["audit"] == {**result["audit"], "label":"LED clear full angle", "min":140, "max":180, "default":180}
    assert result["d"]["fieldFullAngle"] == pytest.approx(180)
    assert result["d"]["fieldHalfAngle"] == pytest.approx(90)
    assert result["max"]["fieldFullAngle"] == pytest.approx(180)
    assert result["max"]["fieldHalfAngle"] == pytest.approx(90)
    assert result["over"]["fieldFullAngle"] == pytest.approx(180)
    assert result["over"]["fieldHalfAngle"] == pytest.approx(90)
    assert result["nan"]["fieldFullAngle"] == pytest.approx(180)
    assert result["helper"] == pytest.approx([75,90,90])
    assert all(math.isfinite(result[key]["fieldHalfAngle"]) for key in ("d","max","over"))


def test_mask_plane_is_dependently_clamped_wallward_of_nearest_fin_base():
    result=run_js("({state:k.normalizedState({...k.defaults,sourceZ:55,maskZ:10}),model:k.buildModel({...k.defaults,sourceZ:55,maskZ:10})})")
    nearest=min(fin["baseZ"] for fin in result["model"]["fins"].values())
    assert result["state"]["maskZ"] == pytest.approx(nearest - 1.0)
    assert result["model"]["maskFinClearance"] == pytest.approx(1.0)
    assert result["model"]["maskZ"] < nearest
    assert run_js("k.MASK_FIN_CLEARANCE") == 1.0


def test_js_python_upright_projection_parity_and_exact_normative_values():
    js=run_js("({reference:k.P3_V3_REFERENCE,model:k.buildModel({...k.defaults})})")
    model=js["model"]
    assert model["architecture"] == "p3-v3-stacked-three-motor-90deg"
    assert model["sourceZ"] == P3_V3.source_z == 40
    assert list(model["carrierAnnulus"]) == pytest.approx(P3_V3.carrier_radii)
    assert list(model["frameRadii"]) == pytest.approx(P3_V3.frame_radii)
    for actual, expected in zip(model["carrierLayers"].values(), P3_V3.carrier_layers, strict=True):
        assert actual == pytest.approx(expected)
    for index,name in enumerate(P3_V3.roles):
        fin=model["fins"][name]
        assert fin["radius"] == pytest.approx(P3_V3.fin_lane_centers[index])
        assert fin["baseZ"] == pytest.approx(P3_V3.fin_bases[index])
        assert fin["tipZ"] == pytest.approx(P3_V3.fin_tip_zs[index])
        assert fin["height"] == pytest.approx(P3_V3.fin_heights[index])
        assert fin["visibleBaseZ"] == pytest.approx(P3_V3.common_visible_fin_base_z)
        assert fin["shadowOcclusionTopZ"] == pytest.approx(P3_V3.shadow_occlusion_top_zs[index])
        assert fin["visibleHeight"] == pytest.approx(P3_V3.visible_fin_heights[index])
        assert fin["stemWidth"] == pytest.approx(P3_V3.fin_tangential_widths[index])
        assert fin["projectedStart"] == pytest.approx(P3_V3.projected_base_radii[index])
        assert fin["projectedTip"] == pytest.approx(P3_V3.target_tip_radii[index])
        assert fin["projectedLength"] == pytest.approx(P3_V3.projected_shadow_lengths[index])
    assert model["finRadialThickness"] == pytest.approx(P3_V3.fin_radial_width)
    assert model["nearestFinGap"] == pytest.approx(P3_V3.led_nearest_tip_gap)


def test_source_offset_projection_warns_and_zero_offset_stays_radial():
    result=run_js("({zero:k.projectPointToWall([0,0,68],[0,30,25.5]),offset:k.projectPointToWall([2,-1,68],[0,30,25.5])})")
    assert result["zero"] == pytest.approx({"x":0,"y":48,"scale":1.6,"sourceAxisOffsetWarning":False})
    assert result["offset"]["sourceAxisOffsetWarning"] is True
    assert result["offset"]["x"] != 0 and result["offset"]["y"] != 48


def test_javascript_and_python_reject_nonphysical_ordering():
    node=node_binary(); assert node
    result=subprocess.run([node,"-e",f"const k=require({json.dumps(str(ROOT/'simulator.js'))});try{{k.projectedRadius(10,3,10);process.exit(1)}}catch(e){{process.exit(0)}}"],capture_output=True,text=True)
    assert result.returncode == 0
    source=(ROOT/"simulator.js").read_text()
    assert "flatXYBladesAllowed: false" in source
    assert "constant-radius-rectangular-axial-upright-fin" in source


def test_javascript_parses_and_css_has_mobile_bounded_layout():
    node=node_binary()
    result=subprocess.run([node,"--check",str(ROOT/"simulator.js")],capture_output=True,text=True)
    assert result.returncode == 0,result.stderr
    css=(ROOT/"styles.css").read_text()
    assert "@media (max-width: 980px)" in css and "@media (max-width: 580px)" in css
    assert "height: clamp(520px, 66dvh, 760px)" in css
