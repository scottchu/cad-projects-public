from html.parser import HTMLParser
import json
import math
from pathlib import Path
import shutil
import subprocess
from urllib.parse import urlsplit

import pytest


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "vendor" / "kage-three.bundle.js"
SOURCE = ROOT / "src" / "three-scene.js"


def node_binary() -> str | None:
    return next((candidate for candidate in (shutil.which("node"), "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node") if candidate and Path(candidate).is_file()), None)


def run_three(expression: str):
    node = node_binary()
    if node is None:
        pytest.skip("node unavailable")
    program = "const fs=require('fs'),vm=require('vm');const c={console};vm.createContext(c);" + f"vm.runInContext(fs.readFileSync({json.dumps(str(BUNDLE))},'utf8'),c);console.log(JSON.stringify(({expression})));"
    result = subprocess.run([node, "-e", program], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = set(); self.external = []; self.scripts = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"): self.ids.add(values["id"])
        if tag == "script" and values.get("src"): self.scripts.append(values["src"])
        for key in ("src", "href"):
            if values.get(key, "").startswith(("http://", "https://", "//")): self.external.append(values[key])


def test_three_runtime_is_local_pinned_and_page_has_no_network_dependency():
    parser = Parser(); parser.feed((ROOT / "index.html").read_text())
    assert parser.external == []
    runtime_urls = parser.scripts[-2:]
    assert [urlsplit(url).path for url in runtime_urls] == ["vendor/kage-three.bundle.js", "simulator.js"]
    assert all(urlsplit(url).query.startswith("v=") and len(urlsplit(url).query) > 2 for url in runtime_urls)
    assert {"heroCanvas3d", "heroCanvas2d", "sectionCanvas", "threeStatus"} <= parser.ids
    assert BUNDLE.is_file() and BUNDLE.stat().st_size > 300_000
    assert BUNDLE.read_text().startswith("/*! KAGE Three.js runtime · three r176 · MIT")
    assert "fetch(" not in SOURCE.read_text()


def test_scene_contract_is_the_frozen_upright_rim_fin_architecture():
    contract = run_three("c.KageThreeScene.sceneContract({})")
    assert contract["architecture"] == "p3-v3-stacked-three-motor-90deg"
    assert contract["axisConvention"] == "wall z=0; +Z points toward room/viewer"
    assert contract["sourceZ"] == 40
    assert contract["maskZ"] == 1.5
    assert contract["projectedMaskRadius"] == 130
    expected = {"hour": (138.1, 2.8, 17.904, 161.520467836, 250), "minute": (136.5, 6.2, 21.8, 177.272727273, 300), "second": (134.9, 12.4, 24.582857143, 196.934306569, 350)}
    for name, values in expected.items():
        actual = contract["fins"][name]
        assert tuple(actual[key] for key in ("radius", "baseZ", "tipZ", "projectedStart", "projectedTip")) == pytest.approx(values)
    assert [contract["fins"][name]["shadowOcclusionTopZ"] for name in ("hour", "minute", "second")] == pytest.approx([5.8, 9.2, 12.6])
    assert [contract["fins"][name]["projectedBaseWidth"] for name in ("hour", "minute", "second")] == pytest.approx([3.50877193, 2.597402597, 1.751824818])
    assert contract["fieldFullAngle"] == pytest.approx(180)
    assert contract["fieldHalfAngle"] == pytest.approx(90)


def test_three_scene_converts_full_angle_to_spotlight_half_angle_at_180_boundary():
    values = run_three("({default:c.KageThreeScene.sceneContract({}),max:c.KageThreeScene.sceneContract({model:{fieldFullAngle:180}}),over:c.KageThreeScene.sceneContract({model:{fieldFullAngle:999}}),helper:[c.KageThreeScene.fullAngleToHalfAngle(150),c.KageThreeScene.fullAngleToHalfAngle(180),c.KageThreeScene.fullAngleToHalfAngle(999)]})")
    assert (values["default"]["fieldFullAngle"],values["default"]["fieldHalfAngle"]) == pytest.approx((180,90))
    assert (values["max"]["fieldFullAngle"],values["max"]["fieldHalfAngle"]) == pytest.approx((180,90))
    assert (values["over"]["fieldFullAngle"],values["over"]["fieldHalfAngle"]) == pytest.approx((180,90))
    assert values["helper"] == pytest.approx([75,90,90])
    assert all(math.isfinite(value) for value in values["helper"])
    assert "spot.angle = THREE.MathUtils.degToRad(c.fieldHalfAngle)" in SOURCE.read_text()


def test_model_projected_tip_widths_survive_scene_contract_and_drive_each_shadow_mesh():
    custom = {
        "model": {
            "fins": {
                "hour": {"projectedTipWidth": 6.125},
                "minute": {"projectedTipWidth": 7.25},
                "second": {"projectedTipWidth": 8.375},
            }
        }
    }
    contract = run_three(f"c.KageThreeScene.sceneContract({json.dumps(custom)})")
    assert [contract["fins"][name]["projectedTipWidth"] for name in ("hour", "minute", "second")] == pytest.approx([6.125, 7.25, 8.375])
    source = SOURCE.read_text()
    assert "function defaultFin(name)" in source
    assert "createShadowGeometry(data.projectedStart, data.projectedTip, data.projectedBaseWidth, data.projectedTipWidth)" in source


def test_fins_are_constant_radius_profiled_uprights_not_flat_xy_hands():
    source = SOURCE.read_text()
    for name in ("hour", "minute", "second"):
        assert f'`${{name}}-constant-section-upright-fin`' in source
    assert "constant-radius-carrier" in source
    assert "carrier.userData.fin.position.set(0, data.radius, data.baseZ - carrierCenterZ)" in source
    assert "createFinGeometry(profile, height, thickness)" in source
    for rejected in ("createNormalizedBlocker", "blocker-blade", "leaf-kite", "visualBladeRoot"):
        assert rejected not in source
    assert "star-shaped" not in source.lower()
    assert "counter-fin" not in source.lower()
    assert "carrier-spoke" not in source.lower()


def test_four_structural_camera_modes_are_finite():
    presets = run_three("c.KageThreeScene.CAMERA_PRESETS")
    assert set(presets) == {"assembly", "wall", "section", "orbital"}
    for preset in presets.values():
        assert all(math.isfinite(value) for value in preset["position"] + preset["target"])
        assert set(preset) == {"label", "position", "target"}
    assert presets["assembly"]["position"][0] != 0
    assert presets["wall"]["position"][:2] == [0, 0]
    assert presets["section"]["position"][0] > 200


def test_camera_can_zoom_well_beyond_the_full_300mm_assembly():
    limits = run_three("c.KageThreeScene.CAMERA_DISTANCE_LIMITS")
    assert limits == {"min": 65, "max": 1600, "far": 2500}
    assert limits["max"] >= 5 * 300
    source = SOURCE.read_text()
    assert "controls.enableZoom = true" in source
    assert "controls.maxDistance = CAMERA_DISTANCE_LIMITS.max" in source
    assert "CAMERA_DISTANCE_LIMITS.far" in source


def test_wall_camera_is_the_only_output_only_presentation_and_toggles_map_to_named_objects():
    source = SOURCE.read_text()
    assert 'shadowGroup.name = "wall-shadow-only-presentation"' in source
    assert 'wallMask.name = "projected-central-mask-shadow"' in source
    assert 'const wallOnly = currentView === "wall"' in source
    assert 'mechanicsGroup.visible = !wallOnly' in source
    assert 'sourceGroup.visible = !wallOnly' in source
    assert 'shellGroup.visible = !wallOnly' in source
    assert 'helperGroup.visible = !wallOnly' in source
    assert 'glareCap.name = "room-side-glare-cap-not-wall-mask"' in source
    assert 'mask.name = "wall-side-physical-mask"' in source
    assert 'wallHalo.name = "single-calculated-wall-halo-no-source-mechanics"' in source
    assert "shadowGroup.add(wallHalo, wallMask)" in source
    assert "wallHaloMaterial.uniforms.haloColor.value.copy(spot.color)" in source
    assert "wallHaloMaterial.uniforms.haloIntensity.value" in source
    mapping = {
        "showQuartz": "quartz.visible",
        "showShell": "shell.visible",
        "showPhysicalMask": "mask.visible",
        "showSourceHardware": "led.visible",
        "showGlareCap": "glareCap.visible",
        "showProjectionRays": "rays.visible",
        "showMaskShadow": "wallMask.visible",
        "showWallHalo": "wallHalo.visible",
        "lightEnabled": "spot.visible",
    }
    for flag, target in mapping.items():
        assert f"{target} = snapshot.{flag} === true" in source
    assert 'carriers.hour.visible = snapshot.showCarriers === true' in source
    assert 'shadows.hour.visible = snapshot.showHandShadows === true' in source
    assert 'wall: { label: "WALL SHADOW"' in source


def test_arrangement_is_independent_and_light_is_separate_from_source_hardware():
    source = SOURCE.read_text()
    assert 'currentArrangement = snapshot.stackArrangement === "exploded" ? "exploded" : "assembled"' in source
    assert 'applyExplode(currentArrangement === "exploded")' in source
    assert 'setActualShadowCasting(!exploded)' in source
    assert 'object.position.z = displayZ(base, explodedOffsets.get(object), exploded)' in source
    assert 'spot.intensity = snapshot.lightEnabled === true ?' in source
    assert 'wallHaloMaterial.uniforms.haloIntensity.value = enabled ?' in source
    assert 'led.visible = snapshot.showSourceHardware === true' in source
    assert 'spot.visible = snapshot.lightEnabled === true' in source


def test_canvas_buffer_is_bounded_across_repeated_extreme_resizes():
    sizes = run_three("Array.from({length:100},(_,i)=>c.KageThreeScene.boundedBufferSize(i%2?1600:320,i%2?1200:440,2))")
    assert all(item["bufferPixels"] <= 2_073_600 for item in sizes)
    assert sizes[0] == sizes[2] == sizes[-2]
    css = (ROOT / "styles.css").read_text()
    assert "contain: layout paint size" in css
    assert "height: clamp(560px, calc(100dvh - 28px), 1040px)" in css
    assert ".viewer > canvas" in css and "position: absolute" in css and "width: 100%" in css
    assert "renderer.setSize(next.cssWidth, next.cssHeight, false)" in SOURCE.read_text()


def test_runtime_has_one_shadow_light_stable_loop_and_disposal_contract():
    source = SOURCE.read_text()
    assert source.count("new THREE.SpotLight(") == 1
    assert "renderer.setAnimationLoop(drawFrame)" in source and "renderer.setAnimationLoop(null)" in source
    assert "resizeObserver?.disconnect()" in source and "intersectionObserver?.disconnect()" in source
    assert "renderer.dispose()" in source and "controls.dispose()" in source
    assert 'canvas.addEventListener("webglcontextlost", onContextLost, false)' in source
    assert "carrier.userData.ringKey !== ringKey" in source
    assert "source-to-wall-projection-rays" in source
    assert source.count("setInterval(") == 1
    assert "snapshot?.useRealTime === true && reducedMotion && externallyActive" in source
    assert "function setActive(active)" in source
    assert "externallyActive && !loopActive" in source


def test_one_mutually_exclusive_realtime_clock_path_per_renderer():
    three = SOURCE.read_text()
    simulator = (ROOT / "simulator.js").read_text()
    assert three.count("setInterval(") == 1
    assert simulator.count("setInterval(") == 1
    assert "state.timeSource===\"realtime\"&&state.renderer===\"2d\"&&pageVisible" in simulator
    assert "threeScene?.setActive(Boolean(three))" in simulator
    assert "syncTwoDClockTimer()" in simulator
    assert "beforeunload" in simulator and "threeScene?.dispose()" in simulator
    assert "setInterval(()=>{if(state.timeSource===\"realtime\")renderAll();},1000)" not in simulator


def test_blocker_rotation_maps_noon_and_three_oclock_from_room_view():
    result = run_three("({noon:c.KageThreeScene.blockerWorldTip(0,40),three:c.KageThreeScene.blockerWorldTip(Math.PI/2,40),rotation:c.KageThreeScene.blockerRotation(Math.PI/2)})")
    assert result["noon"] == pytest.approx({"x": 0, "y": 40}, abs=1e-9)
    assert result["three"] == pytest.approx({"x": 40, "y": 0}, abs=1e-9)
    assert result["rotation"] == pytest.approx(-math.pi / 2)
