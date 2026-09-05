# OSW-08 independent final-argv validation

**Owner/role:** `/root/render_controls_validate_b`, independent real-browser/WASM validator.  
**Recovery manifest:** `0123a62c15f2e173ac65ddebb8a95b6e6b4ac3df447cfc60068230fb874a17a0`.  
**Current candidate:** worker `6938e8d9f1fdfdeff6606084c621db890263644d9b42ff6a649b8bfdac3070d4`, test `40780e6ac959b91a0fa79639680d4c510703a8efe092907e9f6de931321a5f09`, SCAD `b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`.  
**Verdict:** **BLOCK** — the reordered same-backend cube probe still aborts before producing STL bytes, so the body/cap dependency gate remains closed.

## Deterministic gates

The recovery manifest remains the verified frozen pre-repair baseline. Current candidate hashes match the OSW-08 handoff. `npm --workspace laifen-wave-case run setup:openscad-wasm` passed. `npm --workspace laifen-wave-case run build:openscad-simulator` passed with Vite 6.4.3 in `509 ms`. The focused suite passed:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
.... [100%]
```

## Real-browser cube result

The built app was served only from `http://127.0.0.1:8766/`. Headless Chromium loaded the page, main bundle, module worker, official OpenSCAD JavaScript, and official 9.6 MB WASM. Every observed request used `127.0.0.1`; the WASM response was HTTP 200 with `Content-Type: application/wasm`.

The current worker invokes the cube with the repaired ordering:

```text
/probe.scad --enable=manifold --backend=Manifold -o /probe.stl
```

The worker posted `loading`, then the official module aborted after `0.125 s`:

```text
Requested GUI mode but can't open display!
program has already aborted!
```

No successful `probe` event, probe bytes, case `compiling` stage, result, blob, preview, or download existed. This exactly reproduces the prior real-browser backend failure after changing only argv order. Because it is reproducible candidate behavior, no environmental retry was justified.

## Dependency stop and remaining gates

The frozen recovery design requires a nonempty cube STL from the exact backend before compiling the Laifen case. The validator therefore stopped immediately. Smooth body/cap completion, the 180-second bounds, STL manifold/bounds/native parity, exact preview/download identity, stale/reset/cancel behavior, crafted diamond rejection, and mobile 390 px layout remain unproven for this candidate.

Local-only request and correct WASM MIME checks pass independently. Static build/tests also pass, but neither category overrides the failed real compiler probe.

## Cleanup and next action

The isolated server was stopped and port `8766` has no listener. No application source, route, continuity record, CAD/SCAD, generated STL, slicer artifact, printer action, or physical acceptance state changed.

Evidence is under `scratch/openscad-wasm-validation/final-argv/`: exact Playwright source, structured worker/network record, commands, and server access. `EVIDENCE.sha256` binds those files and has SHA-256 `e0709b17d183d13a4df80b0625ec8a6582de2da179abc5b9146f7e46ee34acbf`. The next recovery must test a WASM-supported CLI contract with the cube alone; body/cap and UI validation should stay stopped until that minimal program produces an STL.
