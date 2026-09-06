from pathlib import Path
import json

PROJECT = Path(__file__).parents[1]
APP = PROJECT / "preview" / "openscad-wasm-simulator"


def test_provenance_lock_and_setup_are_exact_and_atomic():
    lock = json.loads((APP / "dependency-lock.json").read_text())
    assert lock["playgroundCommit"] == "012111f06bb6d8dac2b8d30318512494d87d6932"
    assert lock["archiveSha256"] == "0968af31b9c9b3bba68d9031de1695ccae51c32231a1aab4ef27b18c86379f3b"
    assert lock["members"] == {"openscad.js": 124567, "openscad.wasm": 9603115}
    assert len(lock["installedSha256"]["openscad.wasm"]) == 64
    source = (APP / "scripts" / "setup-openscad-wasm.mjs").read_text()
    assert "redirect: \"error\"" in source and "files.openscad.org" in source
    assert "rename(stage, vendor)" in source and "rename(vendor, backup)" in source and "sha256" in source


def test_worker_uses_only_allowlisted_d_arguments_and_real_wasm_path():
    source = (APP / "workers" / "openscad.worker.js").read_text()
    assert "--enable=manifold" not in source
    assert '"--backend=Manifold"' in source and "cube([1,1,1]);" in source
    assert 'type:"probe"' in source and "probeBytes?.byteLength" in source
    assert 'callMain(["/probe.scad",...BACKEND_ARGS,"-o","/probe.stl"])' in source
    assert 'callMain(["/case.scad",...BACKEND_ARGS,...argv,"-o","/result.stl"])' in source
    assert 'mod.FS.writeFile("/case.scad",scad)' in source
    assert 'mod.FS.readFile("/result.stl"' in source
    assert "callMain" in source and "locateFile" in source
    assert "const {default:factory}=await import" in source and "typeof factory!==\"function\"" in source
    assert "factory({noInitialRun:true,locateFile:" in source
    assert "let factoryPromise;" in source and "const probe=await engine();" in source
    assert "const mod=await engine();" in source and "return factory({noInitialRun:true" in source
    assert "let factoryPromise;" in source and "let activeJobId;" in source
    assert 'postMessage({type:"log",id:activeJobId,text:String(t)})' in source
    schema = (APP / "src" / "schema.mjs").read_text()
    assert "ALLOWLIST" in schema and "JSON.stringify(v[k])" in schema
    assert "Number.isFinite" in schema and "BROWSER_PRESET" in schema


def test_desktop_ui_exposes_labeled_controls_and_distinct_actions():
    # Behavioral lifecycle/adapter coverage lives in tests/node/desktop-customizer.test.mjs.
    html = (APP / "index.html").read_text()
    for control in ("diameter", "height", "wall", "ends"):
        assert f'for="{control}"' in html
        assert f'id="{control}-error"' in html
    for control in ("generate", "cancel", "reset", "camera", "download", "status", "stale"):
        assert f'id="{control}"' in html
    assert '<title>Cylindrical Container Customizer</title>' in html
    assert 'id="status" aria-live="polite"' in html
    assert '<details class="diagnostic-details">' in html


def test_complete_job_identity_and_preflight_guards_are_source_level_contracts():
    schema = (APP / "src" / "schema.mjs").read_text()
    assert "JOB_ALLOWLIST" in schema and "JOB_ALLOWLIST=ALLOWLIST" in schema
    assert 'filter(k=>!k.startsWith("diamond_"))' not in schema
    assert "diamond_axial_pitch" in schema and "diamond_arc_pitch" in schema
    assert "diamond_depth" in schema and "diamond_phase_deg" in schema
    assert "wave_spacing" in schema and "wave_depth" in schema
    assert "assertPatternPreflight" in schema
    assert "thread wall constraint failed" in schema and "drain spacing constraint failed" in schema
    assert "canonical(v)" in schema and "lockFingerprint" in schema
