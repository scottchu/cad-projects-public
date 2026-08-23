from pathlib import Path
import json
import shutil
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]


def node_binary() -> str | None:
    return next((candidate for candidate in (shutil.which("bun"), shutil.which("node"), "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node") if candidate and Path(candidate).is_file()), None)


def run_js(expression: str):
    node = node_binary()
    if node is None:
        pytest.skip("JavaScript runtime unavailable")
    program = f"const k=require({json.dumps(str(ROOT / 'simulator.js'))});console.log(JSON.stringify(({expression})));"
    result = subprocess.run([node, "-e", program], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_renderer_switch_is_canvas_overlay_and_not_in_view_panel():
    html = (ROOT / "index.html").read_text()
    viewer = html[html.index('class="viewer"'):html.index('</section>', html.index('class="viewer"'))]
    controls = html[html.index('class="controls"'):html.index('</aside>', html.index('class="controls"'))]
    assert 'class="renderer-switch renderer-overlay"' in viewer
    assert 'id="renderer3dButton"' in viewer and 'id="renderer2dButton"' in viewer
    assert 'id="renderer3dButton"' not in controls and 'id="renderer2dButton"' not in controls


def test_renderer_round_trip_cannot_mutate_scene_or_optics_state():
    result = run_js("(()=>{const base={...k.defaults,cameraView:'orbital',stackArrangement:'exploded',showShell:true,sourceZ:73,ringGap:.5};const two={...base,renderer:'2d'};const three={...two,renderer:'3d'};return {base:k.observableSignature(base),two:k.observableSignature(two),three:k.observableSignature(three)}})()")
    assert result["three"] == result["base"]
    assert [key for key in result["base"] if result["base"][key] != result["two"][key]] == ["renderer"]


def test_side_section_is_scaled_for_the_300mm_clock_and_contains_all_fins():
    result = run_js("(()=>{const m=k.buildModel(k.defaults),l=k.sideSectionLayout(m,420,240);return {scale:l.radialScale,ys:Object.values(m.fins).map(f=>l.y(f.radius)),top:l.top,axis:l.axisY,annotations:k.sideSectionAnnotations(m,l)}})()")
    assert 0.75 <= result["scale"] <= 1.1
    assert all(result["top"] <= value <= result["axis"] for value in result["ys"])
    assert len(result["annotations"]["finLabels"]) == 3


def test_default_section_endpoints_match_p3_v3_contract():
    model = run_js("k.buildModel(k.defaults)")
    assert (model["sourceZ"], model["maskZ"], model["maskPhysicalRadius"], model["glareCapDiameter"]) == pytest.approx((40, 1.5, 125.125, 22))
    expected = {
        "hour": (138.1, 2.8, 17.904, 161.520467836, 250),
        "minute": (136.5, 6.2, 21.8, 177.272727273, 300),
        "second": (134.9, 12.4, 24.582857143, 196.934306569, 350),
    }
    for name, values in expected.items():
        fin = model["fins"][name]
        assert tuple(fin[key] for key in ("radius", "baseZ", "tipZ", "projectedStart", "projectedTip")) == pytest.approx(values)


def test_side_section_rays_labels_and_toggle_ownership_are_explicit():
    source = (ROOT / "simulator.js").read_text()
    assert 'line(x(model.sourceZ), y(0), x(0), y(model.fins.hour.projectedStart)' in source
    assert 'line(x(model.sourceZ), y(0), x(0), y(model.fins.second.projectedTip)' in source
    for label in ("physical mask", "LED / point source", "viewer glare cap", "Radii H/M/S", "Ring gap", "LED → nearest fin"):
        assert label in source


def test_ring_gap_derives_exact_stack_without_changing_radial_lanes():
    models = run_js("[.2,.4,.8].map(ringGap=>k.buildModel({...k.defaults,ringGap}))")
    for gap, model in zip((.2, .4, .8), models):
        assert model["ringGap"] == pytest.approx(gap)
        assert model["carrierRadii"] == pytest.approx({"hour":138.1,"minute":136.5,"second":134.9})
        assert model["carrierLayers"]["hour"] == pytest.approx([2.8, 5.8])
        assert model["carrierLayers"]["minute"] == pytest.approx([5.8 + gap, 8.8 + gap])
        assert model["carrierLayers"]["second"] == pytest.approx([8.8 + 2 * gap, 11.8 + 2 * gap])
        assert model["commonVisibleFinBaseZ"] == pytest.approx(11.8 + 2 * gap)
        assert all(fin["visibleBaseZ"] == pytest.approx(11.8 + 2 * gap) for fin in model["fins"].values())
        assert tuple(fin["shadowOcclusionTopZ"] for fin in model["fins"].values()) == pytest.approx(tuple(layer[1] for layer in model["carrierLayers"].values()))


def test_source_gap_and_tip_extrema_cross_product_always_builds_visible_fins():
    models = run_js("[30,80].flatMap(sourceZ=>[.2,.8].flatMap(ringGap=>[0,1].map(edge=>k.buildModel({...k.defaults,opticalMode:'solveTargets',sourceZ,ringGap,hourTip:edge?k.PARAMETERS.hourTip.max:k.PARAMETERS.hourTip.min,minuteTip:edge?k.PARAMETERS.minuteTip.max:k.PARAMETERS.minuteTip.min,secondTip:edge?k.PARAMETERS.secondTip.max:k.PARAMETERS.secondTip.min}))))")
    assert len(models) == 8
    for model in models:
        assert all(fin["tipZ"] > model["commonVisibleFinBaseZ"] for fin in model["fins"].values())
        assert all(fin["visibleHeight"] > 0 for fin in model["fins"].values())
        assert model["nearestFinGap"] > 0


def test_fixed_hardware_mode_moves_led_without_resizing_fins():
    models = run_js("[30,40,60,80].map(sourceZ=>k.buildModel({...k.defaults,sourceZ}))")
    assert all(model["opticalMode"] == "fixedHardware" for model in models)
    assert all(tuple(fin["tipZ"] for fin in model["fins"].values()) == pytest.approx((17.904,21.8,24.5828571429)) for model in models)
    expected = ((342.509920635,499.390243902,747.072784810),(250,300,350),(196.835803877,214.397905759,228.533397870),(177.918062355,187.628865979,194.741183749))
    for model, projected in zip(models, expected):
        assert tuple(fin["projectedTip"] for fin in model["fins"].values()) == pytest.approx(projected)


def test_solve_targets_mode_is_explicit_and_round_trips_requested_targets():
    model = run_js("k.buildModel({...k.defaults,opticalMode:'solveTargets',sourceZ:60,hourTip:250,minuteTip:300,secondTip:350})")
    assert model["opticalMode"] == "solveTargets"
    assert tuple(fin["projectedTip"] for fin in model["fins"].values()) == pytest.approx((250,300,350))


def test_default_lane_clearances_and_warning_thresholds_are_exact():
    default = run_js("k.buildModel(k.defaults)")
    assert default["clearances"] == pytest.approx({"carrierHour":.4,"hourMinute":.4,"minuteFrame":2.3,"topCarrierEdge":0})
    assert default["warnings"] == []
    thin_gap = run_js("k.buildModel({...k.defaults,ringGap:.2})")
    assert "Ring axial gap is below the frozen 0.4 mm print/assembly value." in thin_gap["warnings"]
    thin_fin = run_js("k.buildModel({...k.defaults,finThickness:.8})")
    assert "Fin radial thickness is below the frozen three-line 1.2 mm CAD value." in thin_fin["warnings"]


def test_controls_readouts_and_required_cone_are_exact():
    result = run_js("({source:k.PARAMETERS.sourceZ,gap:k.PARAMETERS.ringGap,model:k.buildModel(k.defaults),depths:[30,40,80].map(value=>k.opticalDepth(value))})")
    assert result["source"]["min"] == 30 and result["source"]["max"] == 80 and result["source"]["default"] == 40
    assert result["gap"]["min"] == .2 and result["gap"]["max"] == .8 and result["gap"]["default"] == .4
    model = result["model"]
    assert model["nearestFinGap"] == pytest.approx(15.417142857)
    assert model["requiredFieldHalfAngle"] == pytest.approx(83.480198248)
    assert model["requiredFieldFullAngle"] == pytest.approx(166.960396497)
    assert model["fieldFullAngle"] == 180
    assert result["depths"] == pytest.approx([36, 46, 86])


def test_short_source_and_narrow_cone_are_reported():
    result = run_js("({defaultModel:k.buildModel(k.defaults),narrow:k.buildModel({...k.defaults,fieldFullAngle:140}),short:k.buildModel({...k.defaults,sourceZ:30})})")
    assert result["defaultModel"]["warnings"] == []
    assert any("LED cone is too narrow" in warning for warning in result["narrow"]["warnings"])
    assert result["short"]["requiredFieldHalfAngle"] == pytest.approx(87.700424399)


def test_javascript_parses_and_css_keeps_mobile_canvas_bounded():
    runtime = node_binary()
    result = subprocess.run([runtime, "--check", str(ROOT / "simulator.js")], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    css = (ROOT / "styles.css").read_text()
    assert "@media (max-width: 980px)" in css and "@media (max-width: 580px)" in css
    assert "height: clamp(520px, 66dvh, 760px)" in css
