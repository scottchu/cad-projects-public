# Independent recovery validation — VAL-04

Status: **FAIL**, publication blocked. Owner `/root/preview_validate`, independent validator of IMP-04; 2026-09-01. No preview source, tests, requirements, coupon, dependency, runtime-service or printer changes.

Candidate manifest `inputs/recovery-candidate.sha256` fingerprint `8e2276d24b8c7457a06010af2f489666a190397b22ddd0a64985d4572baf5437`. All 18 declared path/content entries matched before and after validation. Preview SHA-256: `bc0655e513aff9cab1efda8701a04ce8ee1f33c2d8d4b7a8fc687326fddc2662`.

## Blocking finding

**VAL-04-F01 — high: finite diameter produces nonfinite SVG geometry.** Actual Chrome DOM at 360 px, light theme, L208 / slack5 / q0.5 / D=`1.7e308` returned an empty error string and retained a device rectangle with `width="Infinity"`, `x="-1.4748858447488582e+308"`, `height="360.9132420091324"`. Both radial contact warnings remained displayed. Thus the input is accepted by the arithmetic layer while the rendered geometry overflows. DES-03 finite rendered geometry and DES-04 derived-infinity/invalid-state clearing requirements fail. This independently reproduces the critic's reported failure; ordinary contact/interference warnings do not substitute for invalid-geometry clearing.

Exact captured browser response: `scratch/width-recovery-validation/extreme-d-dom.json`. Reproduction: render the candidate, set the native D field to `1.7e308`, dispatch its bubbling `input` event, and inspect `[data-role="error"]` and `[data-geometry="device"]`. The probe restored D29 afterward.

## Commands and outcomes

Commands ran from repository root, shell login disabled; Python used root `uv run`.

```text
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/recovery-candidate.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/recovery-candidate.sha256
node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs
uv run /Users/scottchu/.codex/plugins/cache/openai-bundled/visualize/1.0.27/skills/visualize/scripts/render.py /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/preview/measurement-gate.html /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/width-recovery-validation/wrapped.html
node projects/laifen-wave-case/scratch/width-recovery-validation/check.mjs
```

Manifest check passed, 18/18. Existing Node suite passed, 8/8: fixed bores and D edits; q and contact states; invalid/recovery; joint labels/gravity; scope exclusions; decimal slack0.1/5.1 at q0/.5/1; lost increments; emitted exterior leader coordinates at360/736 and L140/208/400. These are VM/source-emission checks, not a browser acceptance claim.

The installed visualize renderer now emits an outer sandboxed iframe. Initial scratch harness incorrectly queried the outer document, then was corrected by extracting the renderer's unchanged `srcdoc` via Python `html.parser` into `flat.html`. A subsequent launch first encountered a stale task-owned `DevToolsActivePort` file; deleting only that scratch file allowed the owned Chrome to start. No EMFILE occurred.

The actual browser harness executed the 360/light state sequence and native ArrowRight interaction before stalling at its first `Page.captureScreenshot` call. The accumulated ordinary-state results were not written before that call, so they are **not retained passing evidence**. No screenshots were produced or visually approved; 736/dark runs and full browser coverage remain incomplete. A separate CDP read of the same running page captured VAL-04-F01 in the JSON named above. The owned Chrome PID23337 was terminated; Node PID23336 exited13 with an unsettled await at the screenshot call. No second owned Chrome ran concurrently.

## Coverage, limits, and next action

REQ-03/12 width arithmetic and scoped DES-04 ordinary decimal/exterior corrections have passing existing Node evidence. Browser finite-geometry validation fails. Browser layout, screenshot, decimal/preset and exterior-leader acceptance remain incomplete rather than assumed passed. No CAD, STEP/mesh, slicer or physical validation was attempted or conferred.

Root is explicitly reopening the remaining diameter-to-screen overflow guard in DES-05. After a corrected immutable candidate exists, run the affected overflow/clear/recovery gate first, then complete the prescribed ordinary browser states and 360/736 light/dark screenshots. The scratch harness should persist DOM evidence before requesting screenshots and bound each CDP call; its current screenshot stall is a harness limitation, not evidence that the candidate layout passed or failed.

Changed paths: this receipt plus task-owned `scratch/width-recovery-validation/` harness, renderer wrappers, browser response and temporary Chrome profile/log. Scratch files are reproducible validation data, not release artifacts.
