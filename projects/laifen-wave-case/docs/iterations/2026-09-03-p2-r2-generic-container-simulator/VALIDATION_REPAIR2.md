# VAL-GCS-01 repair 2 independent validation

**Owner:** `/root/mw_sim_validate`, independent validation role.  
**Status:** **FAIL / HOLD.** Repair 2 closes the camera, invalid-state suppression, field-error association, end-treatment, drain, marker/scale and collapsible-control failures on the actual page. One P1 interaction failure remains in the user's primary split control: editing percent updates the model and derived text but leaves the visible raw-mm field stale, so the next mm edit causes a large discontinuous jump. The candidate must not advance to formal review or delivery.

## Frozen provenance and scope

- Verified design baseline fingerprint: `aea717d84cc31b67b345ed9367f6c5ae72b2a370291aa55e75ce1662238574df`.
- Verified implementation-candidate manifest-file SHA-256: `32429b0817e918343959be9cfe783a8ae76a2d00e0a35b9903b77c71ef6f34b6`; all five entries passed before final execution.
- Validator input manifest SHA-256: `05a21353cd7be5dd072754b51d9a0fc3e474710ab4d0277c665c1e86084695e1`. It binds BRIEF/DESIGN/current implementation receipt, candidate source/test, prior HOLD evidence manifests, root UV inputs and independent repair-2 helpers.
- Runtime: root UV Python `3.12.13`, project Playwright `1.62.0`, installed Chromium, Node, and temporary loopback HTTP `127.0.0.1:8997`.
- Candidate source/tests, CAD, routes, indexes and services remained read-only. Writes are limited to this receipt, `inputs/validation-repair2-*.sha256`, and `scratch/generic-container-validation/repair2/`.

## Finding

### GCS-R2-V01 — P1 blocker — percent edit leaves the canonical raw-mm control stale

At H261, the page exposes percent bounds `4.75095785440613..95.24904214559388`. Editing percent to the minimum correctly changes internal/derived `S` to 12.4 mm, and editing it to the maximum correctly changes internal/derived `S` to 248.6 mm. In both cases the visible `Split from top S (mm)` input remains `60`.

The discrepancy is visible in the full-page screenshot: the status/readout and model use `S=248.6 mm / 95.24904%`, while the adjacent editable raw-mm input still says `60`. Focusing that stale mm field and pressing ArrowUp changes it to 60.4, abruptly moving internal S from 248.6 to 60.4 and percent from 95.249% to 23.14176%.

This fails GCS-02's percent-on-edit and percent-on-render adapter contract at the actual control surface and directly undermines the user's requirement that either percentage or distance from top can be modified to locate the thread. The pure conversion function remains exact; the missing UI synchronization is the defect. Evidence: `percent-sync.json`, `desktop-percent-max-full.png`, `desktop-percent-then-mm-full.png`, and the `pctMin`/`pctMax` states in `ui-evidence.json`.

### GCS-R2-V02 — P2 provenance — implementation receipt still identifies repair 1

The current `IMPLEMENTATION.md` calls itself repair 1, describes the earlier candidate, and does not record repair-2 camera fitting, invalid readout suppression, field associations, collapsible controls, axial scale, chamfer transitions or drain apertures. The five-entry implementation candidate manifest correctly freezes the repair-2 source/test bytes, but formal review should receive a matching implementation receipt rather than the stale narrative. Any receipt update must be included in the next review input manifest; it does not change this source-validation result.

## Closed repair-1 findings and passing evidence

- **Camera/framing:** `Box3` fitting and `ResizeObserver` produce a fresh non-null fit after every preset, custom and exploded build. Desktop and 390/412px captures show both orange and teal pieces for Laifen, jar and H88/OD120. All detected model bounds have substantial margins: for example Laifen is `[204,82,287,474]` inside 514×591 desktop and `[105,86,147,290]` inside 264×391 phone; H88/OD120 is `[111,163,374,435]` desktop and `[57,125,192,267]` phone. No supported geometry touches a canvas edge.
- **Two pieces and split topology:** assembled screenshots show one continuous two-color vessel with a mid-body seam; exploded screenshots show two separated exterior pieces. Scene names contain exactly `lower-piece` and `upper-piece`, one seam, full/effective brackets and no thread-tube mesh. The Laifen and wide-short aspect ratios are visibly distinct.
- **Closed ends, chamfer and drains:** scene evidence contains both `lower-closed-end` and `upper-closed-end`. With chamfer 5/drains on/count 5 it contains both transition rings and five aperture objects under each end. The rotated pointer-operated view clearly exposes the upper closed end and five apertures; assembled/exploded captures keep the split interface separate from the outer-end disc. Compared with chamfer0/drains off, the rendered canvas changes 16,309 pixels desktop, 4,555 pixels at 390px and 5,257 pixels at 412px.
- **Markers and scale:** the main scene shows small external full/effective line brackets without a tube or hoop occlusion. The separate global-Z scale labels H/0 and the full/effective intervals in readable text. All band boxes remain within the scale at all viewports. The rotated `global Z` label extends one CSS pixel beyond the viewer frame's right edge but remains readable; this is minor presentation residue rather than an acceptance failure.
- **Invalid/infeasible suppression:** floor `-1` and jar H20 clear the scene to zero children, hide the scale, blank the detail canvas behind `Unavailable until parameters are valid`, replace all nine derived values with that same unavailable text, switch status to assertive alert, and report the exact error. Floor receives `aria-invalid=true`, `aria-describedby=status`, and `aria-errormessage=status`; infeasibility associates the shared error with every contributing control.
- **Strict domains/math:** the independent runner passes 71,197 checks with zero failures, including 21 bad type/domain cases, both presets, null/override bores, dynamic infeasibility, 1/2/3 turns at several pitches, exact H55/120/219/261/311 percent endpoint math, camera-fit math, pattern bounds and 71,148 global-Z phase comparisons.
- **Patterns/detail:** smooth, blunt diamond, shallow helix and wave/flutes are visually distinct in independent detail captures. Main relief remains true scale and the magnifier disclosure remains explicit.
- **Responsive/accessibility:** desktop `1024x900`, phone `390x844`, and phone `412x915` load HTTP 200 with no console/page errors. Document width equals viewport width. Panels stack without overlap on phones. All controls have programmatic names, the three semantic details groups collapse/reopen by click, and their contained controls become hidden while collapsed.
- **Pinned delivery bytes:** the served `index.html` is byte-identical to the frozen candidate entry and the pinned Three.js module loads successfully.

## Requirement disposition

| Requirement | Repair-2 result |
| --- | --- |
| GCS-01 generic presets | **PASS.** Both presets and wide custom are fully framed and visually distinct. |
| GCS-02 canonical S adapter | **FAIL UI / PASS math.** Percent changes internal S but does not synchronize the editable mm field. |
| GCS-03 global closed-end frame | **PASS visual/semantic.** |
| GCS-04 1/2/3 turns | **PASS.** |
| GCS-05 dynamic bounds/infeasibility | **PASS.** |
| GCS-06 two exteriors/no tube/markers | **PASS.** |
| GCS-07 patterns/global Z/count | **PASS.** |
| GCS-08 true scale/magnifier | **PASS.** |
| GCS-09 text/accessibility/markers | **PASS**, with one-pixel scale-label residue. |
| GCS-10 route isolation | **DEFERRED.** Candidate remains on HOLD. |

## Commands and next action

Executed from the repository root:

```sh
node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs
node projects/laifen-wave-case/scratch/generic-container-validation/repair2/validate_math.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-validation/repair2/validate_ui.py
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-validation/repair2/analyze_images.py
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-validation/repair2/inspect_scale.py
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-validation/repair2/inspect_percent.py
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r2-generic-container-simulator/inputs/validation-repair2-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r2-generic-container-simulator/inputs/implementation-candidate.sha256
```

No validation-method repair was required and no acceptance threshold changed. Synchronize the visible `S` input from canonical `raw.S` after a percent edit without parsing rounded percentage text back into state. Add a browser regression which edits percent to both dynamic endpoints, asserts the mm input equals the unrounded canonical S, then edits the mm control and checks continuity. Update the implementation receipt to the matching candidate before formal review.

CDN availability and comprehension on the user's actual desktop/phone remain external acceptance boundaries. This simulator supplies no CAD, thread-solid, mesh, slicer, printability, fit, drainage, strength or physical acceptance.
