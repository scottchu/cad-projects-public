# DES-05: rendered numeric representability recovery

Frozen scope, 2026-09-01. Project `projects/laifen-wave-case`; iteration `2026-09-01-p1-r2-fit-feedback`; baseline `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`. This is a new design owner and a narrow reopening after IMP-04's saved candidate `inputs/recovery-candidate.sha256`, fingerprint `8e2276d24b8c7457a06010af2f489666a190397b22ddd0a64985d4572baf5437`, failed C04-01. Preserve that candidate, its source/test snapshots, and critique evidence; none are accepted or to be overwritten.

## Required correction

Keep all DES-03/DES-04 dimensions, arithmetic, controls, labels, leader placement, and invalid-input wording. Do not add a physical diameter limit, alter the editable values, clamp input, resize bores, or otherwise change UX or geometry. The correction is only a numeric-renderability guard.

After `compute` has accepted physical/domain values and after the render scale and all screen-space geometry have been derived, require every essential emitted SVG numeric value to be finite and representable before writing the viewBox, dimensions, or SVG markup. This includes the viewport width/height and scale; every `x()` and `z()` result used by cavity outlines, floor references, the pending band, device x/y/width/height, spans, leaders, stops, gravity, labels, and gap annotations; and derived leader/label offsets. The device width `D * scale` and device X coordinate are explicitly essential. A finite physical D alone is insufficient.

Render must report failure to `update`, which must enter the existing invalid-state clear path: show the existing finite-values error and clear `section`, `state`, `gaps`, `targets`, and `dimensions`. It must not leave a partially written SVG, old values, or accepted-looking warnings. Ordinary finite cases continue to render as before; the default `L=208, D=29, slack=5, q=.5` must remain valid. This recovery does not make any fit, CAD, export/slicer, or physical-acceptance claim.

## Focused regression prescription

Extend only the existing Node + DOM harness. At both true content widths 360 and 736 px, execute this exact sequence in one initialized DOM instance:

1. Default `L=208, D=29, slack=5, q=.5`: no error; emitted device geometry is present and every parsed numeric SVG coordinate/value is finite.
2. Change only `D` to `1.7e308`: error is nonempty and `section`, `state`, `gaps`, `targets`, and `dimensions` are each empty. The DOM contains no `NaN` or `Infinity` SVG output and no stale warning/readout.
3. Restore only `D=29`: error clears; default device geometry and ordinary readouts return; every parsed numeric SVG coordinate/value is finite.

The implementation owner may make the smallest preview/test change needed for this sequence. Freeze a new candidate manifest after the change, then route the exact manifest to distinct affected critic and validator reruns and formal review. The implementer must not approve its own work.

## Input boundary and ownership

`inputs/des05-inputs.sha256` is derived from the prior `recovery-inputs.sha256` content set plus the immutable snapshot `inputs/des05-numeric.contract.md` of this note. The old candidate manifest is preserved evidence, not a dependency to rewrite. Mutable handoff/status records, runtime, coupon work, CAD, exports, slicer/printer state, and all source/tests are outside this design task.

This role exclusively writes this note and `inputs/des05-*` snapshots/manifests. A new implementation owner exclusively owns any future live preview/test/candidate changes. Stop if frozen inputs no longer verify or if the correction requires a physical dimension/UX change.
