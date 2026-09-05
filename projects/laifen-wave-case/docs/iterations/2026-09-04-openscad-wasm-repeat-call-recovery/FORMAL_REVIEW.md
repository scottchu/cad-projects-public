# OSW-15 formal independent review

**Owner/role:** `/root/openscad_wasm_formal_review`, formal reviewer distinct from implementation and validation  
**Verdict:** **BLOCK for local delivery**

## Provenance join

The supplied chain matches the reviewed bytes:

```text
dd111388da60cbdea439341c7fd7c264d506a2625c613df37e2bb3fee6a8859b  inputs/MANIFEST.sha256
74dca2b782b6ca858a715e4dd1814016863effc3a5572835891cf3aff5290c9e  workers/openscad.worker.js
049a71bc9a7f7c44ff87732771d06802cc3e6d55aca781a27479cdac809d72ff  tests/test_openscad_wasm_simulator.py
33c09c80f62a293ba5fffcd83b282b15c61c8d778b2b5b1b14bbb27c07ba72c7  VALIDATION.md
99b1e16aae37cbb377f3406b17bab1455e6bd20f294229ad8a91ba8dacf4fc39  scratch/openscad-wasm-validation/repeat-call/EVIDENCE.sha256
```

The frozen manifest is the pre-repair baseline: its own fingerprint matches,
its validation and dependency-lock entries still verify, and its worker/test
entries now differ exactly because OSW-13 replaced them with the candidate
hashes above. All 21 entries in the repeat-call evidence manifest verify from
the repository root.

Focused review reruns passed:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
# 4 passed
npm run build:openscad-simulator --workspace projects/laifen-wave-case
# PASS, Vite 6.4.3, 507 ms
```

## Accepted evidence

The repeat-call repair itself is credible. The worker imports one factory and
creates a fresh `OpenSCAD({noInitialRun:true,...})` module for each cube or case
`callMain`; obsolete `--enable=manifold` is absent and
`--backend=Manifold` is retained. Real Chromium completed default smooth body
and cap jobs in 0.381 s and 0.303 s. Their browser meshes are watertight,
winding-consistent single components with exact native bounds and relative
volume deltas below `3.5e-6`. Result/download hashes match. Stale, reset,
cancel, crafted-diamond rejection, local-only network, WASM MIME, and 390 px
layout evidence is internally consistent. Visual review of the bound desktop
body/cap and mobile screenshots confirms visible meshes and no page overflow.

Diagnostics for both case jobs say `Top level object is a 3D object
(manifold)` and `Status: NoError`, with no unknown-feature or fallback warning.
That is sufficient evidence that this pinned build accepted the requested
Manifold backend for those two jobs.

## Blocking findings

### P1 — retained assembled case gate is absent

The recovery chain retains body, cap, and assembled case generation. The brief
and runtime contract name a fresh module for an assembled request, the prior
runtime-recovery contract requires default smooth body/cap/assembled gates, and
OSW-13 lists assembled validation as remaining. OSW-14 completes body and cap
only. Its assembled interaction is cancelled; it produces no assembled STL,
mesh inspection, bounds/contact result, native comparison, or download identity.
Local delivery cannot join the retained gate from this evidence.

### P1 — required compiler-error state is absent

The repeat-call acceptance contract requires the UI error state. The bound
browser record exercises stale, reset, cancel, success, and crafted preflight
rejection, but never a real worker/compiler error and recovery. Static
source-string assertions do not replace that real-browser state gate.

### P1 — compiler diagnostics are dropped by the application

`workers/openscad.worker.js` posts log messages without the active job `id`.
`src/main.mjs` returns immediately for every message where `d.id !== id`, so
those log messages never reach the visible diagnostics element. OSW-14 captured
them by instrumenting the Worker externally, which proves backend behavior but
does not satisfy the application contract that compiler diagnostics remain
visible and copyable.

## Scope and disposition

Diamond remains disabled and rejected before worker creation; smooth is the
only reviewed browser output. This review authorizes no MakerWorld integration,
public hosting, route change, slicer work, printer action, or publication.
Browser execution and mesh transport have partial PASS evidence for body and
cap only. CAD/STEP acceptance is inherited separately, and slicer,
printability, fit, and physical acceptance remain open.

The smallest repair is to attach the active job id to worker diagnostics, then
freeze a new candidate and independently capture a successful default smooth
assembled result plus compiler-error/recovery behavior. The new evidence must
bind the exact candidate before formal review is repeated.
