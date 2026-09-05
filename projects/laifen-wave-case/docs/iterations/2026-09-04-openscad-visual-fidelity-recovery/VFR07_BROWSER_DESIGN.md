# VFR-07 browser Diamond enablement design

Status: **READY FOR ONE BOUNDED IMPLEMENTATION — private real-worker evidence first; visible Diamond controls remain disabled until the independent C1 join passes.**

Owner role: `/root/openscad_vfr07_browser_designer`, independent browser-enablement design. Sole write: this document.

## Frozen input and boundary

Verified `inputs/VFR07_BROWSER_DESIGN_INPUTS.sha256`: **10/10 OK**, manifest fingerprint **`ca6a10c1affb1d627257e1d3463002db4d90eaf67960974a0860b7373ab78f1e`**. The input binds C1 source `48b4ac84dc0cf4b8274200e9e2e13f145cfc01a5f721f975c37d1166c91ebd31`, VFR-06, and current schema `fe77d55cc91f9e526559b307a70db3fa03aefe35a84c4c87cf5d4ee42f242f1a`, main `98af41e1377afb873208977eedc679ea9e887b04b96253bc2025b3896fbeb353`, and worker `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`.

C1 is source/mesh implementation evidence only. Its receipt stops before V06-3B/V06-3C because the browser schema drops `diamond_*` and rejects `surface_style="diamond"`; it contains no real browser-worker timing. VFR-06 remains controlling: a cold actual worker result, including runtime creation, probe, compile, and byte delivery, must complete in <=60 s for body before cap. Node or direct-WASM evidence cannot substitute.

No geometry, SCAD argument meaning, vendor/runtime or lock byte, output mode, deployment/service, CAD/STEP, slicer, or physical acceptance changes. `BROWSER_PRESET` remains smooth. The UI’s 180 s watchdog is not an acceptance threshold and must not be extended.

## Exact delta mask

| Path | Allowed change | Invariants and forbidden scope |
|---|---|---|
| `preview/openscad-wasm-simulator/src/schema.mjs` | Set `JOB_ALLOWLIST = ALLOWLIST`; make `snapshot()` validate every allowlisted field through existing enums/ranges and remove only its smooth-only rejection; use the existing `argv()`, canonical serializer and `identity()` with that complete immutable snapshot. | Defaults, ranges, enums, numeric constraints, source/lock hashing, identity formula, canonical sorting, `-D` quoting, and output selection. `BROWSER_PRESET.surface_style` stays `"smooth"`. |
| `preview/openscad-wasm-simulator/src/main.mjs` — private candidate | **No change.** Controls and Diamond option remain disabled; help remains “pending optimization.” Private validation drives the worker protocol with a frozen snapshot. | Render, stale/download, cancellation, timeout, toast, focus, diagnostics, camera, mobile behavior, worker messaging and network behavior. |
| `preview/openscad-wasm-simulator/workers/openscad.worker.js` | **No change.** It already executes supplied argv and returns the supplied identity/source/lock tuple. | Manifold backend/probe, fresh-runtime sequence, active-job logs, transferable bytes, protocol fields, vendor path and timeouts. |
| `tests/test_openscad_wasm_simulator.py` plus a narrowly scoped private browser-worker fixture if required | Add only assertions and the real-browser protocol test below. | Fake worker, Node-only substitute, relaxed threshold, C1 geometry change, artifact/deployment/continuity writes. |

The private execution change is schema-only. The worker has no Diamond-specific filter. Restoring all source fields to the snapshot makes argv, canonical parameters and identity describe the exact SCAD job. A Diamond parameter cannot be silently omitted from either identity or `-D`.

## Private C1 worker gates

Run locally built, unserved candidate bytes in real Chromium with the production schema, worker URL and vendor files. Do not copy to 8448 or expose Diamond controls. Record each complete canonical snapshot, expected and returned identity, source hash, lock fingerprint, STL SHA-256, stage/probe messages and wall-clock timing.

1. **P0 schema and smooth regression.** Assert all four Diamond keys occur once in `snapshot`, argv, canonical JSON and identity. Verify the smooth default snapshot/argv/identity remains byte-for-byte equal to the prior result. Preserve source constraints and reject depth >0.6.
2. **P1 private body.** Run default C1 Diamond values with `output_mode="body"`. Assert all `diamond_*` argv values occur once; expected identity equals the returned tuple; downloaded bytes equal transferred bytes. Measure cold `worker created → result received`, separately recording probe and compile; require <=60,000 ms. Then apply V06-3B final-mesh gates: topology, dimensions/walls/protected geometry, error <=0.025 mm, parity <=0.05 mm and exterior triangles <=250,000. Any timeout, tuple mismatch, missing/duplicate argument, invalid/stale result or mesh failure stops cap.
3. **P2 private cap and pair.** Only after P1, run `output_mode="cap"` under the same cold <=60,000 ms and tuple/byte rules. Apply V06-3C final-cap checks, including effective bore/entry relief, 2.99 mm floor, groove/drain checks and actual body/cap seam. Report cap timing separately; never average it with body.
4. **P3 interaction regression.** Exercise the unmodified production main on smooth: change a control after success and prove stale/download invalidation; cancel an in-flight job and prove late result cannot restore download; send wrong id/identity/source/lock and prove rejection; cause validation, compiler and timeout failures and prove status, toast, collapsed raw diagnostics and focus return remain unchanged. At 390 x 844 verify sticky preview, scrollable form, reachable Generate action and disabled Diamond controls.

The harness must fail closed when a result lacks the exact C1 identity tuple; a parseable STL or echoed id is insufficient. Record browser version, timing boundaries and artifact hashes in the implementation receipt. This design reports no real-worker timing because none was run.

## Independent join and public controls

After P0–P3, freeze a candidate manifest with changed browser hashes, C1 source/test hashes, runtime/lock hashes, private worker records and STL hashes. Distinct critic and validator owners inspect that exact fingerprint; a distinct formal reviewer joins their dispositions. They must confirm V06-3P smooth/depth-zero/protected-geometry preservation, P1/P2 timing and identity evidence, and P3 stale/cancel/toast/mobile results. No implementer self-approval or public control change precedes this join.

After the three independent gates pass, make the smallest public-only follow-up in `main.mjs`: replace unconditional Diamond disabling at control creation with the approved enabled state and remove the pending-only help for those enabled fields. Keep every listener and CSS/layout rule unchanged; do not change index, schema or worker. Rebuild and rerun P0 smooth regression plus visible Diamond body/cap generation, identity/download, stale, cancel, error/toast/focus and 390 x 844 mobile checks before delivery review. Served-route review and hosting need separate authorization.

## Budget, rollback, and stop

One implementation attempt may make the private schema/test delta and run P0–P3. One focused repair is allowed only for one diagnosed local projection, canonical identity, protocol assertion or UI-enable conditional defect. It may not change geometry, constraints, thresholds, runtime/vendor bytes, worker protocol, time ceilings or layout. Freeze a new fingerprint and rerun the failed and dependent gates.

A second failure, body/cap timeout, identity failure, mesh failure or needed broader change records **browser OpenSCAD Diamond blocked under the 0.025 mm / 60 s contracts** and restores the pre-attempt browser bytes. Before work, save all four manifest browser hashes and use transactional staged replacement. On a private-gate failure restore those bytes; smooth defaults and disabled controls remain usable. If the public follow-up fails, restore only its `main.mjs` enablement conditional to the approved private candidate.

## Receipt

- Status: design complete; no implementation, worker execution, browser run, artifact, service, or public-control change by this role.
- Verified input fingerprint: `ca6a10c1affb1d627257e1d3463002db4d90eaf67960974a0860b7373ab78f1e` (10/10).
- Coverage: C1 private worker, complete parameter/identity binding, body/cap 60 s gates, smooth/stale/cancel/toast/mobile regression, independent approval before visible Diamond controls.
- Open risks: actual C1 browser timing, final mesh gates and independent review are unmeasured; CAD, slicer and physical acceptance remain outside this task.
- Output SHA-256 is computed after this write and reported by the task owner; a document cannot truthfully contain its own final SHA-256.
