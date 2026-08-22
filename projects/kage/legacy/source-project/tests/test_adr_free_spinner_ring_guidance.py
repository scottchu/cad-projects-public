from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "adr-free-spinner-ring-guidance.html"
CSS = ROOT / "adr-free-spinner-ring-guidance.css"
UI = ROOT / "adr-free-spinner-ring-guidance-ui.js"
SOURCE = ROOT / "src" / "adr-free-spinner-ring-guidance.js"
BUNDLE = ROOT / "vendor" / "kage-free-spinner-adr.bundle.js"


def node_binary() -> str | None:
    return next(
        (
            candidate
            for candidate in (
                shutil.which("node"),
                "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node",
            )
            if candidate and Path(candidate).is_file()
        ),
        None,
    )


def run_adr(expression: str):
    node = node_binary()
    if node is None:
        pytest.skip("node unavailable")
    program = (
        "const fs=require('fs'),vm=require('vm');const c={console};vm.createContext(c);"
        + f"vm.runInContext(fs.readFileSync({json.dumps(str(BUNDLE))},'utf8'),c);"
        + f"console.log(JSON.stringify(({expression})));"
    )
    result = subprocess.run([node, "-e", program], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.external = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "script" and values.get("src"):
            self.scripts.append(values["src"])
        for key in ("src", "href"):
            if values.get(key, "").startswith(("http://", "https://", "//")):
                self.external.append(values[key])


def test_standalone_adr_page_is_local_and_has_all_interactive_controls():
    parser = Parser()
    parser.feed(HTML.read_text())
    assert parser.external == []
    assert [item.split("?", 1)[0] for item in parser.scripts] == [
        "vendor/kage-free-spinner-adr.bundle.js",
        "adr-free-spinner-ring-guidance-ui.js",
    ]
    assert {
        "adrViewer",
        "adrCanvas",
        "comparisonProposed",
        "comparisonCurrent",
        "rotationInput",
        "towerAdjustmentInput",
        "toggleLabels",
        "toggleForces",
        "assemblyPrev",
        "assemblyNext",
        "assemblyStepReadout",
        "assemblyStepList",
        "adrStatus",
    } <= parser.ids
    html = HTML.read_text()
    for label in ("Assembled", "Cutaway", "Exploded", "Context", "Decision", "Consequences", "Tests"):
        assert label.lower() in html.lower()
    assert BUNDLE.is_file() and BUNDLE.stat().st_size > 300_000
    assert BUNDLE.read_text().startswith("/*! KAGE free-spinner ADR · three r176 · MIT")


def test_frozen_geometry_contract_names_exact_bands_and_guidance_dimensions():
    contract = run_adr("c.KageFreeSpinnerADR.geometryContract()")
    assert contract["decision"] == "three-free-spinner-towers"
    assert contract["towerAnglesDegrees"] == [60, 180, 300]
    assert contract["fixedTowerAnglesDegrees"] == [60, 180]
    assert contract["adjustableTowerAngleDegrees"] == 300
    assert contract["adjustableTowerRangeMm"] == pytest.approx([-0.25, 0.25])
    assert contract["carrierBandsMm"] == {
        "hour": [-1.5, 1.5],
        "minute": [4.05, 7.05],
        "second": [9.6, 12.6],
    }
    assert contract["guideBeadMm"] == pytest.approx(0.8)
    assert contract["nominalRadialGapMm"] == pytest.approx(0.05)
    assert contract["radialCaptureOverlapMm"] == pytest.approx(0.8)
    assert contract["axialReliefMm"] == pytest.approx([0.10, 0.15])


def test_proposed_architecture_is_three_towers_and_nine_independent_deep_spools():
    contract = run_adr("c.KageFreeSpinnerADR.geometryContract()")
    assert contract["towerCount"] == 3
    assert contract["rollersPerTower"] == 3
    assert contract["rollerCount"] == 9
    assert contract["independentlyRotatingRollers"] is True
    source = SOURCE.read_text()
    assert "TOWER_ANGLES_DEGREES.map(createTower)" in source
    assert "HAND_ORDER.forEach((hand)" in source
    assert "independent-deep-grooved-roller" in source
    assert "three-independent-rollers" in source
    for angle in (60, 180, 300):
        assert str(angle) in source


def test_guide_rollers_run_on_smooth_beads_and_not_internal_gear_teeth():
    contract = run_adr("c.KageFreeSpinnerADR.geometryContract()")
    assert contract["rollerContactSurface"] == "integral-smooth-guide-bead"
    assert contract["gearTeethContactAllowed"] is False
    assert contract["continuousKeeperRailInProposedDesign"] is False
    source = SOURCE.read_text()
    assert "integral-smooth-guide-bead-0p8mm" in source
    assert "internal-gear-teeth-never-roller-contact" in source
    assert "proposed-three-free-spinner-towers-no-continuous-keeper" in source
    assert "current-bulky-continuous-keeper-rails-shoes-caps-spines" in source


def test_comparison_is_mutually_exclusive_and_normalized():
    result = run_adr(
        "({proposed:c.KageFreeSpinnerADR.comparisonVisibility('proposed'),"
        "current:c.KageFreeSpinnerADR.comparisonVisibility('current'),"
        "invalid:c.KageFreeSpinnerADR.comparisonVisibility('both')})"
    )
    assert result == {
        "proposed": {"proposedRollers": True, "currentKeepers": False},
        "current": {"proposedRollers": False, "currentKeepers": True},
        "invalid": {"proposedRollers": True, "currentKeepers": False},
    }
    source = SOURCE.read_text()
    assert "proposed.visible = visibility.proposedRollers" in source
    assert "currentKeepers.visible = visibility.currentKeepers" in source
    ui = UI.read_text()
    assert 'update({ comparison: "proposed" })' in ui
    assert 'update({ comparison: "current" })' in ui


def test_assembly_sequence_reveals_fixed_then_adjustable_then_rollers():
    states = run_adr("Array.from({length:5},(_,step)=>c.KageFreeSpinnerADR.assemblyVisibility(step))")
    assert all(item["rings"] is True for item in states)
    assert states[0] == {
        "rings": True,
        "fixedTowerFrames": False,
        "adjustableTowerFrame": False,
        "rollersOrKeepers": False,
        "guidanceAnnotations": False,
    }
    assert states[1]["fixedTowerFrames"] is True and states[1]["adjustableTowerFrame"] is False
    assert states[2]["adjustableTowerFrame"] is True and states[2]["rollersOrKeepers"] is False
    assert states[3]["rollersOrKeepers"] is True
    assert states[4]["guidanceAnnotations"] is True


def test_adjustable_tower_and_rotation_inputs_are_clamped_and_finite():
    values = run_adr(
        "[c.KageFreeSpinnerADR.normalizeState({adjustmentMm:-9,rotationDegrees:-1}),"
        "c.KageFreeSpinnerADR.normalizeState({adjustmentMm:9,rotationDegrees:721})]"
    )
    assert values[0]["adjustmentMm"] == pytest.approx(-0.25)
    assert values[1]["adjustmentMm"] == pytest.approx(0.25)
    assert values[0]["rotationDegrees"] == pytest.approx(359)
    assert values[1]["rotationDegrees"] == pytest.approx(1)
    html = HTML.read_text()
    assert 'id="towerAdjustmentInput" type="range" min="-0.25" max="0.25" step="0.01"' in html


def test_canvas_resize_is_bounded_stable_and_never_changes_layout_size_from_buffer():
    sizes = run_adr(
        "Array.from({length:80},(_,i)=>c.KageFreeSpinnerADR.boundedBufferSize(i%2?1920:320,i%2?1400:480,2))"
    )
    assert all(item["bufferPixels"] <= 2_073_600 for item in sizes)
    assert sizes[0] == sizes[2] == sizes[-2]
    css = CSS.read_text()
    source = SOURCE.read_text()
    assert "contain: layout paint size" in css
    assert "height: clamp(560px, calc(100dvh - 28px), 980px)" in css
    assert ".spinner-adr .adr-viewer > canvas" in css
    assert "position: absolute" in css and "width: 100%" in css and "height: 100%" in css
    assert "renderer.setSize(next.cssWidth, next.cssHeight, false)" in source
    assert "new ResizeObserver(resize)" in source


def test_adr_text_and_mobile_interactive_targets_meet_accessibility_floor():
    css = CSS.read_text()
    for undersized in ("font-size: 7px", "font-size: 8px", "font-size: 9px", "font-size: 10px", "font-size: 0"):
        assert undersized not in css
    assert ".spinner-adr .adr-segment button { min-width: 44px; min-height: 44px" in css
    assert ".spinner-adr .adr-stepper button { width: 44px; height: 44px" in css
    assert '.spinner-adr .adr-range input[type="range"] { min-height: 44px; }' in css
    assert ".spinner-adr .adr-toggle-grid label { min-height: 44px; }" in css


def test_page_states_cad_intent_and_does_not_claim_physical_proof():
    html = HTML.read_text().lower()
    contract = run_adr("c.KageFreeSpinnerADR.geometryContract()")
    assert "does not claim physical proof" in html
    assert "friction, wear, noise, and preload remain physical gates" in html
    assert contract["physicalValidation"] == "required-for-friction-wear-fit-and-noise"
    for forbidden in ("physically proven", "guaranteed friction", "print-ready mechanism"):
        assert forbidden not in html


def test_ui_script_parses_and_primary_simulator_files_are_untouched_by_page_loading():
    node = node_binary()
    if node is None:
        pytest.skip("node unavailable")
    result = subprocess.run([node, "--check", str(UI)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    html = HTML.read_text()
    assert "index.html" not in html
    assert "simulator.js" not in html
    assert "styles.css" not in html
