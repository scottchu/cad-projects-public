from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "adr-direct-gear-race-guidance.html"
CSS = ROOT / "adr-direct-gear-race-guidance.css"
UI = ROOT / "adr-direct-gear-race-guidance-ui.js"
SOURCE = ROOT / "src" / "adr-direct-gear-race-guidance.js"
BUNDLE = ROOT / "vendor" / "kage-direct-gear-race-adr.bundle.js"

ROLLBACK_HASHES = {
    "adr-free-spinner-ring-guidance.html": "303391afda9afd08deb9d8a38f8310480f3ec8dbb685133073a888dc0f1c6cb9",
    "adr-free-spinner-ring-guidance.css": "24f5adb3d6bac81fc3cbb4457983b609c0a4f355c2048645b9c1c218c110a9f9",
    "adr-free-spinner-ring-guidance-ui.js": "24c16ccc076d49375fdf1420f7fcb2fcbda4a9642b597f223a01b4e0c53545ef",
    "src/adr-free-spinner-ring-guidance.js": "89e916f6b59dd2b77e0143cde19eba3096c109260f39537bc6259e435f6bab57",
    "vendor/kage-free-spinner-adr.bundle.js": "e211e6ad71970fdac82b6ab5fdcbe7beffc96454f114bef7c2717329562da827",
    "tests/test_adr_free_spinner_ring_guidance.py": "962ead5d447e282c7892ccfc39bb64619134fed909caf79b486698fe58acbeb5",
}


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


def bun_binary() -> str | None:
    candidate = shutil.which("bun")
    return candidate if candidate and Path(candidate).is_file() else None


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


def test_old_adr_rollback_files_are_byte_identical():
    for relative, expected in ROLLBACK_HASHES.items():
        path = ROOT / relative
        assert path.is_file(), relative
        assert sha256(path.read_bytes()).hexdigest() == expected, relative


def test_new_adr_is_a_separate_local_page_with_complete_controls():
    parser = Parser()
    parser.feed(HTML.read_text())
    assert parser.external == []
    assert [item.split("?", 1)[0] for item in parser.scripts] == [
        "vendor/kage-direct-gear-race-adr.bundle.js",
        "adr-direct-gear-race-guidance-ui.js",
    ]
    assert {
        "adrViewer",
        "adrCanvas",
        "comparisonProposed",
        "comparisonLegacy",
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
    assert BUNDLE.is_file() and BUNDLE.stat().st_size > 300_000
    assert BUNDLE.read_text().startswith("/*! KAGE direct gear-race ADR · three r176 · MIT")


def test_exact_direct_carrier_race_contract():
    contract = run_adr("c.KageDirectGearRaceADR.geometryContract()")
    assert contract["decision"] == "three-direct-gear-race-spinner-towers"
    assert contract["separateGuideFeature"] is False
    assert contract["rollerContactSurface"] == "carrier-inner-root-land-below-tooth-face"
    assert contract["carrierRaceRadiusMm"] == pytest.approx(131.6)
    assert contract["toothTipRadiusMm"] == pytest.approx(129.0)
    assert contract["toothRootRadiusMm"] == pytest.approx(132.5)
    assert contract["rollerAxisRadiusMm"] == pytest.approx(125.5)
    assert contract["rollerHubDiameterMm"] == pytest.approx(6.0)
    assert contract["rollerRunningDiameterMm"] == pytest.approx(12.1)
    assert contract["rollerFlangeDiameterMm"] == pytest.approx(13.8)
    assert contract["contactLandWidthMm"] == pytest.approx(0.6)
    assert contract["nominalRadialGapMm"] == pytest.approx(0.05)
    assert contract["radialCaptureOverlapMm"] == pytest.approx(0.8)
    assert contract["axialReliefMm"] == pytest.approx(0.15)
    assert contract["toothTipRollingAllowed"] is False


def test_role_bands_and_three_tower_adjustment_are_frozen():
    contract = run_adr("c.KageDirectGearRaceADR.geometryContract()")
    assert contract["towerAnglesDegrees"] == [60, 180, 300]
    assert contract["fixedTowerAnglesDegrees"] == [60, 180]
    assert contract["adjustableTowerAngleDegrees"] == 300
    assert contract["adjustableTowerRangeMm"] == pytest.approx([-0.25, 0.25])
    assert contract["raceBandsMm"] == {
        "hour": [-1.5, -0.7],
        "minute": [4.05, 4.85],
        "second": [9.6, 10.4],
    }
    assert contract["contactBandsMm"] == {
        "hour": [-1.4, -0.8],
        "minute": [4.15, 4.75],
        "second": [9.7, 10.3],
    }
    assert contract["towerCount"] == 3
    assert contract["rollersPerTower"] == 3
    assert contract["rollerCount"] == 9
    assert contract["independentlyRotatingRollers"] is True


def test_clearance_math_matches_nominal_and_max_outward_adjustment():
    clearances = run_adr(
        "({nominal:c.KageDirectGearRaceADR.derivedClearances(0),"
        "outward:c.KageDirectGearRaceADR.derivedClearances(.25)})"
    )
    assert clearances["nominal"] == pytest.approx(
        {
            "adjustedAxisRadiusMm": 125.5,
            "runningOuterRadiusMm": 131.55,
            "flangeOuterRadiusMm": 132.4,
            "nominalRaceGapMm": 0.05,
            "toothTipHubClearanceMm": 0.5,
        }
    )
    assert clearances["outward"]["adjustedAxisRadiusMm"] == pytest.approx(125.75)
    assert clearances["outward"]["toothTipHubClearanceMm"] == pytest.approx(0.25)
    assert clearances["outward"]["runningOuterRadiusMm"] == pytest.approx(131.8)
    assert clearances["outward"]["flangeOuterRadiusMm"] == pytest.approx(132.65)


def test_rendering_has_true_lower_carrier_surface_and_separate_tooth_envelope():
    source = SOURCE.read_text()
    assert "carrier-inner-root-land-display-surface-r131p60" in source
    assert "260t-tooth-envelope-separated-above-race" in source
    assert "bare-260t-carrier-with-lower-root-race" in source
    assert "relieved-carrier-race-roller" in source
    assert "createRelievedRollerGeometry" in source
    assert "for (let toothIndex = 0; toothIndex < 260" in source
    assert "new THREE.CylinderGeometry(DIRECT_RACE_MM.carrierRaceRadius" in source


def test_new_fork_contains_no_added_guidance_feature_or_tooth_rolling_claim():
    combined = "\n".join((SOURCE.read_text(), HTML.read_text(), UI.read_text())).lower()
    for forbidden in (
        "guidebead",
        "guide bead",
        "guide-head",
        "guide head",
        "guide-neck",
        "guide neck",
        "t-rail",
        "tooth-tip rolling",
        "tooth flank rolling",
    ):
        assert forbidden not in combined
    assert "separateguidefeature: false" in combined
    assert "toothtiprollingallowed: false" in combined
    assert "carrier-inner-root-land-below-tooth-face" in combined


def test_assembly_and_final_check_text_match_direct_race_order():
    html = HTML.read_text().lower()
    ui = UI.read_text().lower()
    assert "three bare 260t carrier rings" in html
    assert "three bare 260t carrier rings" in ui
    for required in ("carrier-only race contact", "tooth clearance", "axial relief", "free rotation"):
        assert required in ui
    assert "seam bump, friction, wear, noise, and adjustment remain physical test gates" in html
    assert "does not claim physical proof" not in html
    for forbidden in ("physically proven", "guaranteed friction", "print-ready mechanism"):
        assert forbidden not in html


def test_comparison_and_assembly_states_are_exclusive_and_ordered():
    comparison = run_adr(
        "({proposed:c.KageDirectGearRaceADR.comparisonVisibility('proposed'),"
        "legacy:c.KageDirectGearRaceADR.comparisonVisibility('legacy'),"
        "invalid:c.KageDirectGearRaceADR.comparisonVisibility('both')})"
    )
    assert comparison == {
        "proposed": {"directRaceRollers": True, "legacyKeepers": False},
        "legacy": {"directRaceRollers": False, "legacyKeepers": True},
        "invalid": {"directRaceRollers": True, "legacyKeepers": False},
    }
    states = run_adr("Array.from({length:5},(_,step)=>c.KageDirectGearRaceADR.assemblyVisibility(step))")
    assert all(item["rings"] is True for item in states)
    assert states[0]["fixedTowerFrames"] is False
    assert states[1]["fixedTowerFrames"] is True and states[1]["adjustableTowerFrame"] is False
    assert states[2]["adjustableTowerFrame"] is True and states[2]["rollersOrKeepers"] is False
    assert states[3]["rollersOrKeepers"] is True
    assert states[4]["contactAnnotations"] is True


def test_canvas_and_mobile_layout_remain_bounded_without_growth_loop():
    sizes = run_adr(
        "Array.from({length:80},(_,i)=>c.KageDirectGearRaceADR.boundedBufferSize(i%2?1920:320,i%2?1400:480,2))"
    )
    assert all(item["bufferPixels"] <= 2_073_600 for item in sizes)
    assert sizes[0] == sizes[2] == sizes[-2]
    source = SOURCE.read_text()
    css = CSS.read_text()
    assert "@import" not in css
    assert "contain: layout paint size" in css
    assert "height: clamp(560px, calc(100dvh - 28px), 980px)" in css
    assert ".spinner-adr .adr-viewer > canvas" in css
    assert "renderer.setSize(next.cssWidth, next.cssHeight, false)" in source
    assert "new ResizeObserver(resize)" in source
    assert "@media (max-width: 640px)" in css
    assert '.spinner-adr .adr-range input[type="range"] { min-height: 44px; }' in css


def test_ui_parses_and_bundle_is_deterministically_rebuildable(tmp_path):
    node = node_binary()
    if node is None:
        pytest.skip("node unavailable")
    syntax = subprocess.run([node, "--check", str(UI)], capture_output=True, text=True)
    assert syntax.returncode == 0, syntax.stderr
    bun = bun_binary()
    if bun is None:
        pytest.skip("bun unavailable")
    rebuilt = tmp_path / "kage-direct-gear-race-adr.bundle.js"
    command = [
        bun,
        "x",
        "esbuild",
        str(SOURCE),
        "--bundle",
        "--minify",
        "--format=iife",
        "--global-name=KageDirectGearRaceADR",
        f"--outfile={rebuilt}",
        "--banner:js=/*! KAGE direct gear-race ADR · three r176 · MIT · see vendor/THREE-LICENSE.txt */",
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert rebuilt.read_bytes() == BUNDLE.read_bytes()
