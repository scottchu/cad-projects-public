# VFR-01U independent UI validation

**Verdict: PASS** for the frozen UI candidate `09eb7635454e890130c609e9ef5e85ac0e9155dd019359baf284436eaece305e`. This is a bounded presentation and diagnostic validation. It is not a geometry, CAD/STEP, slicer, physical-print, deployment, or final-review approval.

## Role, candidate, and scope

- Validation owner: `/root/openscad_mobile_toast_validator`, independent of implementation owner `/root/openscad_mobile_toast_impl`.
- Candidate manifest: `candidate/UI_CANDIDATE.sha256`, SHA-256 `09eb7635454e890130c609e9ef5e85ac0e9155dd019359baf284436eaece305e`.
- `shasum -a 256 -c candidate/UI_CANDIDATE.sha256`: PASS; all seven listed candidate paths matched.
- Candidate UI main: `11caaede00f6cb7266de6dcdc628370c389d545fdd1719549976c7549ed0fa16`; stylesheet: `2da7d5b1e50db178ec6859f182a0b232e7d586654071cb9fa93af5c003a07530`; HTML: `997c2fbc80f453911c3ba68fed55ab17b3c9d2d56d7bb99ceee43a9e0ee82d6f`; focused test: `84519ffa75da97e29e5dc222bde36672b34a5fca45923a920f4dd825769e8856`.
- UI input manifest remained `4d09d530b31e1e74b0467edfb1d594abca9b33fd56280508c511f5c723fc0cd6`.
- No candidate source, tests, OpenSCAD, worker, schema, geometry, pattern, public-hosting, slicer, or printer file was edited by this validator.

## Focused validation

| Gate | Evidence | Result |
| --- | --- | --- |
| Candidate integrity | `shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/UI_CANDIDATE.sha256` | PASS — all seven paths matched. |
| Focused source contract | `uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q` | PASS — `5 passed`. |
| Production build | `npm --workspace laifen-wave-case run build:openscad-simulator -- --outDir /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/openscad-ui-validation/vfr-01u/dist` | PASS — Vite 6.4.3, 11 modules, 547 ms. Output was confined to permitted scratch. |
| Mobile layout | Real Chromium against the staged production build at `http://127.0.0.1:8771/`, viewport `390x844` | PASS — grid areas `"preview" "controls"`; preview `.result` computed `position: sticky; top: 0px`; parameter form `overflow-y: auto`, computed max-height `454px`; actions `position: sticky; bottom: 0px`; raw details initially closed. |
| Successful generation | Same real browser, default assembled controls | PASS — OpenSCAD compilation completed as `Complete 58895df4a50f`; download was enabled (`aria-disabled=false`, href present), stale state hidden, toast hidden. Compiler diagnostics included the known localization warning only in the collapsed raw-details region. |
| Validation failure | Set `outer_diameter=20`, then Generate; this violates the actual `snapshot()` wall constraint | PASS — status `OD must retain minimum wall`; visible assertive toast said `Check the parameter values, then try generating again.`; focus moved to `dismiss-toast`; download stayed disabled; raw details stayed closed. |
| Dismissal and focus | Clicked Dismiss in the same real failure flow | PASS — toast became hidden and focus returned to `generate`. |
| Localization demotion | Successful browser run plus DOM check outside `.diagnostic-details` | PASS — `Could not initialize localization (application path is '/').` remained in raw diagnostics; no visible primary-surface localization text or toast was emitted. Normal compiler statistics also remained raw details. |
| Geometry/source identity | Read-only source and runtime identity inspection | PASS — authoritative `openscad/laifen_case_customizer_v1.scad` is `b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`; unchanged worker is `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`; unchanged schema is `fe77d55cc91f9e526559b307a70db3fa03aefe35a84c4c87cf5d4ee42f242f1a`. The main module imports that raw OpenSCAD source, calculates source and lock fingerprints, and accepts a result only when worker `identity`, `sourceHash`, and `lockFingerprint` match. The successful browser result therefore came from the unchanged OpenSCAD worker/source identity path. |

An initial `npm run build:openscad-simulator` at the repository root reported `Missing script` because the script is workspace-scoped. It made no candidate change; the workspace-qualified production build above is the passing build evidence.

## Independently reported staged-route evidence

The root coordinator separately exercised its staged candidate route, `http://127.0.0.1:8972/openscad-simulator-candidate/`, at `390x844`. This validator did not run that route. Root reported the same mobile computed layout; after scroll, canvas top `62px` and height `260px`; form height `454px`; action bottom `844px`; and Generate height `44px`. Root also reported the same real validation toast/focus sequence and, after restoring OD 39, completion identity `58895df4a50f` with download enabled, collapsed raw details, and retained raw localization/statistics diagnostics. Treat this as separately identified corroboration, not this validator's command execution.

## Limits and next action

This candidate was served from an isolated local scratch build. The existing Tailscale route was deliberately not changed or claimed as revalidated here; delivery-surface validation remains a separate post-deployment gate. No claim is made about diamond performance, geometry correctness, CAD/STEP artifact parity, slicer/process, or physical acceptance. Route this receipt to the distinct formal reviewer; if the candidate is deployed, validate the exact served bytes and mobile interaction on that delivery route before presenting it as delivered.

## Repair cycle 1 — actionable validation toast and real diagnostic newlines

**Verdict: PASS** for repaired frozen candidate `9f01d5eca03a58263a7716c57f39979128520021a670f59ab960f8a6e2778ebd`. Only `src/main.mjs` and the focused test changed from the candidate validated above: their repaired SHA-256 values are respectively `98af41e1377afb873208977eedc679ea9e887b04b96253bc2025b3896fbeb353` and `363bcfdb85ab3ef27951c2d6e45c1a7c769e532c5489215c39d4071cb429ac37`. The other five manifest members, including worker and schema, still match their prior hashes.

- `shasum -a 256 -c candidate/UI_CANDIDATE.sha256`: PASS — all seven repaired candidate paths matched; the candidate-manifest SHA-256 was `9f01d5eca03a58263a7716c57f39979128520021a670f59ab960f8a6e2778ebd`.
- `uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q`: PASS — `5 passed`.
- `npm --workspace laifen-wave-case run build:openscad-simulator -- --outDir /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/openscad-ui-validation/vfr-01u-repair1/dist`: PASS — Vite 6.4.3, 11 modules, 516 ms; build output remained in permitted scratch.
- Real Chromium against that isolated production build at `http://127.0.0.1:8772/`, viewport `390x844`: entering `outer_diameter=20` yielded status `OD must retain minimum wall` and visible toast `OD must retain minimum wall. Adjust that value and try again.`. Raw details remained collapsed and focus moved to `dismiss-toast`; clicking Dismiss hid the toast and returned focus to `generate`.
- In the same browser session, restoring `outer_diameter=39` generated the default assembled result: `Complete 58895df4a50f`, download enabled, toast hidden, and raw details still collapsed. Raw diagnostics contained the known localization line and twenty actual newline-delimited nonempty lines; they contained no literal backslash-plus-`n` text. The unchanged result identity confirms the same OpenSCAD source/worker contract exercised by the original validation.

This repair revalidation covers only the corrected gates. The delivery, CAD, artifact/slicer, and physical limits above remain unchanged.
