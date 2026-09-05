# VFR-01U formal independent review

**Verdict: PASS for the bounded mobile/toast UI candidate.** The repaired candidate may advance to private deployment verification. This is not a delivered-surface, geometry, diamond/seam intent, CAD/STEP, artifact/slicer, or physical acceptance.

## Identity and frozen evidence

- Formal reviewer: `/root/openscad_mobile_toast_formal_review`.
- Implementation owner: `/root/openscad_mobile_toast_impl`.
- Critic owner: `/root/openscad_mobile_toast_critic_fast`, confirmed by the coordinator; the critique itself names the role but omits its runtime identity.
- Independent validator: `/root/openscad_mobile_toast_validator`.
- Project root: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`.
- Reviewed candidate: `candidate/UI_CANDIDATE.sha256`, independently verified SHA-256 `9f01d5eca03a58263a7716c57f39979128520021a670f59ab960f8a6e2778ebd`; all seven members match.
- Baseline input manifest: `inputs/UI_RECOVERY_MANIFEST.sha256`, independently verified SHA-256 `4d09d530b31e1e74b0467edfb1d594abca9b33fd56280508c511f5c723fc0cd6`.

The candidate includes the baseline manifest, UI HTML/CSS/main, focused test, worker, and schema. Baseline OBSERVATION/BRIEF/DESIGN hashes still match. The baseline manifest records the original UI files; those four deliberately changed files are checked against the candidate manifest, not incorrectly expected to retain baseline hashes.

Supplemental decision-bearing inputs inspected and pinned here because the candidate manifest does not directly include them:

| Input | SHA-256 |
| --- | --- |
| `UI_TASK.md` | `ab2d6ea52bb60ee9e0b5bd5e5a39256e5290b0d50b3e15eb609209916978b212` |
| `openscad/laifen_case_customizer_v1.scad` | `b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e` |
| `preview/openscad-wasm-simulator/dependency-lock.json` | `6d4a6b007f96b00752efd33cf1cf9e4eff5daaf82f011edd0655ea68c20e09b8` |

This verdict is bound to those supplemental hashes as well as the candidate manifest. They must be rechecked before deployment; changing them requires assessment of affected review/validation gates.

Evidence documents inspected at review time: `IMPLEMENTATION.md` (`a5e59f861c08115bd5fb8aab2affef21e642cf601bb75dbb17a7ac50f876604d`), `CRITIQUE_UI.md` (`15bcd4f6290c454667536abcaf80e886bfec2257211bad3d9d54b8258f312e50`), and `VALIDATION_UI.md` (`746db42bda1011ba8e9a748b5461ab1412a4a7c2afff9964fd5f954866d8f120`). The validator's repair-cycle section is the current receipt; its original-candidate section remains historical evidence.

## Requirement coverage and findings

| Requirement | Independent evidence and disposition |
| --- | --- |
| Sticky mobile canvas | CSS places preview first and makes `.result` sticky at top zero. Validator measured this at Chromium `390x844`. PASS within that viewport evidence. |
| Independently scrolling parameters | The mobile form has bounded height and `overflow-y:auto`; validator measured `454px` at the tested viewport. PASS. |
| Reachable Generate | Bottom-sticky actions and full-width Generate are present. Validator confirmed sticky positioning; the separately attributed coordinator observation measured a reachable 44px control at the viewport bottom. PASS. |
| Accessible, specific failure toast | Alert/live-region markup and focus behavior are present. Repaired real OD failure displayed `OD must retain minimum wall. Adjust that value and try again.` PASS; UX-UI-02's blocking generic-message defect is resolved. |
| Focus-safe dismissal | Validator exercised the repaired failure: focus moved to Dismiss, dismissal hid the toast and returned focus to Generate. PASS. |
| Collapsed raw diagnostics | Details initially remain closed; repaired generation retained twenty actual newline-delimited nonempty lines without literal backslash-plus-n text. PASS; UX-UI-03 resolved. |
| Non-fatal localization demotion | Known localization warning remains raw and absent from primary status/toast during successful generation. The explicit worker error branch always stops generation and raises an error toast. PASS for the observed warning and inspected error handling. |
| Geometry, worker, schema and output identity preserved | Worker/schema hashes match the baseline; OpenSCAD hash matches the preserved authority. The main module still loads that source, checks worker result identity/source/lock, displays returned STL, and downloads the returned bytes. Repaired browser generation completed as `58895df4a50f`. PASS for preservation; this does not independently prove mesh geometry or byte-for-byte STL parity across all inputs. |

The critique's UX-UI-04 sentence saying validation text is absent from the toast is stale wording: UX-UI-02's repair disposition, current source, and the repaired browser receipt establish that it is now present. That sentence does not identify an unresolved implementation defect.

No blocking finding remains in this bounded candidate. The broad visual-fidelity and pattern work remains subject to VFR-02/VFR-03. `UI_TASK.md` explicitly separates this presentation-only task from those geometry dependencies; this review does not unlock their downstream geometry implementation.

## Commands and evidence limits

The reviewer used `cat` and `/opt/homebrew/bin/rg` to inspect the root policies, project continuity/requirements/experience/decision index, iteration contracts and receipts, and every candidate source/test file. From the project root, the reviewer ran:

```sh
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/UI_CANDIDATE.sha256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/UI_RECOVERY_MANIFEST.sha256 openscad/laifen_case_customizer_v1.scad
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/UI_CANDIDATE.sha256
```

Both completed successfully; the integrity check reported all seven members OK. Supplemental contract/receipt/lock hashes above were obtained with `shasum -a 256` from the repository root. `git status --short -- projects/laifen-wave-case` reported the project as untracked, so no commit identity is claimed.

The independent validator, not this reviewer, ran the focused `uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q` (5 passed), workspace-qualified production build (passed), and repaired real Chromium flows at `http://127.0.0.1:8772/`. Review did not duplicate those runs or claim firsthand browser validation.

Residual limitations: offending inputs have no dedicated `aria-invalid` association; screen-reader announcement behavior, keyboard-only traversal, zoom/reflow, small/landscape viewports, and physical touch behavior are not proven. The localization regex is broader than the single known warning, although raw diagnostics and explicit failure toasts remain available. These are bounded follow-up concerns, not evidence of the repaired defects persisting.

## Exact deployment gate

1. Reverify all seven candidate members and the three supplemental hashes above. Reconcile `PROJECT_STATE.md`, `NEXT_AGENT.md`, and this iteration's `HANDOFF.md` with the reviewed UI candidate; their currently stale pointers/placeholders must not identify this as an already delivered result. Keep geometry/pattern dependencies explicitly pending.
2. Build this exact UI candidate and record generated bundle paths/hashes and source-to-bundle provenance. Replace only the authorized private `/openscad-simulator/` content, preserving the existing service, other routes, and rollback bytes. This review grants no public hosting, MakerWorld, Tailscale reset/reconfiguration, printer, or production-registration authority.
3. Validate `https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/` itself: confirm page and referenced bundle/vendor bytes match the reviewed build; inspect the mobile canvas/parameter/action behavior; generate successfully with download enabled; trigger the genuine OD failure and verify specific toast/dismissal/focus; confirm diagnostics remain collapsed with the known localization line retained only in raw output. Record exact served hashes, commands, browser evidence and limitations.
4. Claim delivery only after that exact route passes. Agent-side browser evidence must remain distinguished from the user's actual device experience; obtain/record the user's observation before claiming it works on their phone. Any candidate mutation returns to the affected independent gates.

Only `FORMAL_REVIEW_UI.md` was written by this reviewer. Next action: coordinator reconciliation and the bounded private delivery gate above.
