"""Focused truthfulness gates for the generated read-only Viewer sidecar."""
from hashlib import sha256
from pathlib import Path
import subprocess
import sys

PROJECT = Path(__file__).parents[1]
PACKAGE = PROJECT / "cad" / "container_generator_v1"
sys.path.insert(0, str(PROJECT / "cad"))

from container_generator_v1 import PARAMETER_SPECS, derive, preset
from container_generator_v1.preview_parameters import (
    BODY_COLOR, BODY_OCCURRENCE_NAME, CAP_COLOR, CAP_OCCURRENCE_NAME,
    DERIVED_IDS, NOTICE_ID, NOTICE_VALUE, VISUAL_CONTROLS, VISUAL_NOTICE_ID,
    manifest, readout_rows, serialize, visual_rows,
)


EXPECTED_STEP_HASHES = {
    "body.step": "02bfc1ca52ef97dcba3451c930408f64d0f383293933f6183029e36409e1c05a",
    "cap.step": "b9561b34b96667d1af6e84d145c03d9aa319694fbf11f2cc3c0b60d6b6f18cf0",
    "closed.step": "cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2",
    "print_layout.step": "cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b",
}


def test_registry_coverage_group_order_and_derived_defaults():
    rows = readout_rows()
    assert rows[0][0] == NOTICE_ID and rows[0][1]["default"] == NOTICE_VALUE
    source_ids = [identifier for identifier, _ in rows[1:27]]
    expected = [
        spec["id"] for group in ("axial", "reference", "radial", "exterior", "thread", "skin", "ends", "drains")
        for spec in PARAMETER_SPECS if spec["group"] == group
    ]
    assert source_ids == expected and len(source_ids) == 26
    assert [identifier for identifier, _ in rows[27:]] == list(DERIVED_IDS)
    parameters = manifest()["parameters"]
    resolved = derive(preset())
    assert parameters["derived__cavity_length"]["default"] == "213 mm - derived readout"
    assert parameters["derived__body_height"]["default"] == "144 mm - derived readout"
    assert parameters["derived__thread_turns"]["default"] == "3 rev - derived readout"
    assert parameters["derived__body_radial_gap"]["default"] == "0.5 mm radial, reference only - derived readout"
    assert parameters["derived__cap_radial_gap"]["default"] == "1 mm radial, reference only - derived readout"
    assert parameters["derived__lattice_count"]["default"] == f"{resolved.lattice_count} repeats - derived readout"
    assert parameters["derived__drain_hole_count_each_end"]["default"] == "7 holes - derived readout"


def test_all_rows_are_immutable_readouts_with_a_visible_regeneration_notice():
    for _, row in readout_rows():
        assert row["type"] == "enum"
        assert len(row["options"]) == 1
        assert row["default"] == row["options"][0]["value"] == row["options"][0]["label"]
        assert "Read-only snapshot" in row["description"]
        assert "regenerate STEP" in row["description"]
    assert readout_rows()[0][1]["label"] == "00 READ ONLY"


def test_visual_controls_precede_the_unchanged_41_row_snapshot():
    visuals = visual_rows()
    combined = manifest()["parameters"]
    assert len(visuals) == 11
    assert visuals[0][0] == VISUAL_NOTICE_ID
    assert visuals[0][1]["label"] == "00 VISUAL PREVIEW ONLY"
    assert tuple(identifier for identifier, _ in visuals[1:]) == tuple(row[0] for row in VISUAL_CONTROLS)
    assert len(combined) == 52
    assert tuple(combined.items())[11:] == readout_rows()
    for identifier, row in visuals[1:]:
        assert row["renderOnly"] is True and row["geometryRegeneration"] is False
        assert "Render only." in row["description"] and "not CAD, STEP" in row["description"]
    exact = {identifier: (row_type, default, minimum, maximum, step, unit)
             for identifier, _, row_type, default, minimum, maximum, step, unit in VISUAL_CONTROLS}
    assert exact["visual_radial_scale_pct"] == ("number", 100, 60, 160, 1, "%")
    assert exact["visual_cap_unscrew_turns"] == ("number", 0, 0, 3, 0.25, "rev")
    assert exact["visual_body_color"][1] == BODY_COLOR
    assert exact["visual_cap_color"][1] == CAP_COLOR


def test_committed_sidecar_is_deterministic_render_only_es_module():
    sidecar = PACKAGE / "closed.params.js"
    assert sidecar.read_text(encoding="utf-8") == serialize()
    assert serialize() == serialize()
    text = sidecar.read_text(encoding="utf-8")
    assert "import " not in text
    assert "features" in text and "solveVisualPreview" in text
    assert "effects.transform" in text and "effects.style" in text
    assert "effects.clear" not in text and "effects.visible" not in text
    assert "THREE" not in text
    result = subprocess.run(
        ["node", "--input-type=module", "--eval", "import definition, { READOUT_SCHEMA, solveVisualPreview } from './closed.params.js'; const calls=[]; const effects={transform:(...x)=>calls.push(['transform',...x]),style:(...x)=>calls.push(['style',...x])}; definition.update({params:{},effects}); const one=solveVisualPreview({visual_cap_unscrew_turns:1.25,visual_cap_extra_lift_mm:3,visual_radial_scale_pct:120,visual_body_axial_scale_pct:80,visual_cap_axial_scale_pct:150}); definition.update({params:{visual_cap_unscrew_turns:1},effects}); console.log(JSON.stringify({schema:READOUT_SCHEMA,count:Object.keys(definition.manifest.parameters).length,calls,one}));"],
        cwd=PACKAGE, check=True, capture_output=True, text=True,
    )
    assert '"geometryRegeneration":false' in result.stdout
    assert '"count":52' in result.stdout
    assert '"calls":[["transform","cap"' in result.stdout
    assert '"theta_deg":450' in result.stdout
    assert '"cap_z_mm":5.5' in result.stdout


def test_solver_clamps_and_effects_target_only_changed_parts():
    result = subprocess.run(
        ["node", "--input-type=module", "--eval", "import definition,{solveVisualPreview} from './closed.params.js'; const calls=[]; const effects={transform:(...x)=>calls.push(['transform',...x]),style:(...x)=>calls.push(['style',...x])}; const bad=solveVisualPreview({visual_radial_scale_pct:Infinity,visual_axial_scale_pct:0,visual_body_axial_scale_pct:999,visual_cap_unscrew_turns:99,visual_cap_extra_lift_mm:-4,visual_body_opacity:0}); definition.update({params:{visual_body_color:'#112233'},effects}); console.log(JSON.stringify({bad,calls}));"],
        cwd=PACKAGE, check=True, capture_output=True, text=True,
    )
    assert '"r":1' in result.stdout
    assert '"az":0.6' in result.stdout
    assert '"bz":0.96' in result.stdout
    assert '"turns":3' in result.stdout
    assert '"cap_z_mm":6' in result.stdout
    assert '"calls":[["style","body"' in result.stdout


def test_closed_entry_declares_sidecar_and_accepted_step_bytes_remain_frozen():
    entry = (PACKAGE / "closed.step.py").read_text(encoding="utf-8")
    assert '"params": "closed.params.js"' in entry
    assert '"shape": build_assembly(derive(preset()))' in entry
    for name, expected in EXPECTED_STEP_HASHES.items():
        assert sha256((PACKAGE / name).read_bytes()).hexdigest() == expected


def test_feature_names_are_stable_authored_occurrence_witnesses():
    features = manifest()["features"]
    assert features["body"]["names"] == [BODY_OCCURRENCE_NAME]
    assert features["cap"]["names"] == [CAP_OCCURRENCE_NAME]
    assert features["body"]["axis"] == features["cap"]["axis"] == [0, 0, 1]
