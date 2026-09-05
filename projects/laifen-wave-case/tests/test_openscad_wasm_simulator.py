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


def test_ui_has_staged_generate_cancel_reset_and_exact_byte_download_contract():
    main = (APP / "src" / "main.mjs").read_text()
    assert "new Worker(new URL" in main
    assert "worker?.terminate" in main and "d.id!==id" in main
    assert "new Blob([bytes]" in main and "STLLoader().parse(out.buffer)" in main
    assert "surface_style:\"smooth\"" in (APP / "src" / "schema.mjs").read_text()
    assert "pending optimization" in main and "d.identity!==key" in main
    assert "sourceHash" in main and "lockFingerprint" in main
    assert "disposeMesh" in main and "WebGL preview is unavailable" in main
    assert "function stop(message){clearTimeout(timeoutId);timeoutId=undefined;worker?.terminate();worker=null;disposeMesh();" in main
    assert "mesh.geometry.dispose();mesh.material.dispose();mesh=null;" in main
    assert "180000" in main and "Compiler timed out; no STL is available." in main
    assert "job++;stop" in main and "clearTimeout(timeoutId)" in main
    assert 'surface_style:["smooth","diamond"]' in (APP / "src" / "schema.mjs").read_text()
    html = (APP / "index.html").read_text()
    for control in ("generate", "cancel", "reset", "camera", "download", "status", "stale"):
        assert f'id="{control}"' in html


def test_mobile_ui_keeps_preview_and_action_reachable_and_demotes_raw_diagnostics():
    html = (APP / "index.html").read_text()
    css = (APP / "style.css").read_text()
    main = (APP / "src" / "main.mjs").read_text()
    assert 'class="control-panel"' in html and 'class="result"' in html
    assert 'id="toast" role="alert" aria-live="assertive"' in html
    assert '<details class="diagnostic-details">' in html and 'Raw compiler diagnostics' in html
    assert 'grid-template-areas:"preview" "controls"' in css
    assert '.result{position:sticky;top:0' in css and '.control-panel form{max-height:' in css
    assert '.actions{position:sticky;bottom:0' in css and '.actions>*{flex:1 1 0;min-width:44px' in css
    assert 'function dismissToast(){toast.hidden=true;lastToastTrigger?.focus();}' in main
    assert 'function showToast(message,trigger=generateButton)' in main
    assert 'message=`${status.textContent}. Adjust that value and try again.`' in main
    assert 'const localizationWarning=' in main and 'function appendDiagnostic(text)' in main
    assert 'diagnostics.textContent+=`${text}\\\\n`' not in main
    assert 'diagnostics.textContent+=`${text}\\n`' in main
    assert 'if(!localizationWarning.test(d.text))status.textContent="Compiler reported diagnostics.' in main
    assert 'showToast("Generation failed. Review the raw compiler diagnostics and adjust the controls.")' in main


def test_complete_job_identity_and_preflight_guards_are_source_level_contracts():
    schema = (APP / "src" / "schema.mjs").read_text()
    assert "JOB_ALLOWLIST" in schema and "JOB_ALLOWLIST=ALLOWLIST" in schema
    assert 'filter(k=>!k.startsWith("diamond_"))' not in schema
    assert "diamond_axial_pitch" in schema and "diamond_arc_pitch" in schema
    assert "diamond_depth" in schema and "diamond_phase_deg" in schema
    assert "thread wall constraint failed" in schema and "drains reach sidewall" in schema
    assert "canonical(v)" in schema and "lockFingerprint" in schema


def test_vfr11_mobile_density_preserves_controls_and_compacts_actions():
    html = (APP / "index.html").read_text()
    css = (APP / "style.css").read_text()
    for control, label in (("generate", "Generate STL"), ("cancel", "Cancel"), ("reset", "Reset"), ("camera", "Reset camera"), ("download", "Download STL")):
        assert f'id="{control}"' in html and label in html
    assert 'header{display:none}' in css
    assert 'canvas{height:clamp(190px,26vh,220px)}' in css
    assert '.actions{position:sticky;bottom:0' in css
    assert '.actions>*{flex:1 1 0;min-width:44px;padding:0 4px;justify-content:center;align-items:center;font-size:0}' in css
    assert all(f':nth-child({n})::before' in css for n in range(1, 6))
    assert '.actions>*{flex:1 1 0;min-width:44px' in css
    assert '.control-panel form{max-height:calc(100vh - 335px);padding-bottom:64px' in css
    assert 'fieldset:last-child{margin-bottom:64px}' in css
    assert '.actions>*:disabled,.actions>*[aria-disabled="true"]' in css
    assert ':nth-child(4)::before' in css


def test_vfr12_mobile_viewport_is_edge_to_edge_and_centers_action_glyph_boxes():
    html = (APP / "index.html").read_text()
    css = (APP / "style.css").read_text()
    assert 'id="status" aria-live="polite"' in html
    assert 'main{padding:0}' in css
    assert '.result{position:sticky;top:0;z-index:1;padding:0;border:0;border-radius:0' in css
    assert '.result #status{position:absolute;width:1px;height:1px' in css
    assert '.result canvas{display:block;width:100%;margin:0;border-radius:0}' in css
    assert '.actions>*{flex:1 1 0;min-width:44px;padding:0 4px;justify-content:center;align-items:center;font-size:0}' in css
    assert '.actions>*::before{content:"";width:24px;height:24px;display:block;background-color:currentColor' in css
    assert '-webkit-mask-position:center;-webkit-mask-size:contain;-webkit-mask-repeat:no-repeat;mask-position:center;mask-size:contain;mask-repeat:no-repeat' in css
    assert 'mask-image:url("data:image/svg+xml' in css and '-webkit-mask-image:url("data:image/svg+xml' in css
    assert 'background-image' not in css
