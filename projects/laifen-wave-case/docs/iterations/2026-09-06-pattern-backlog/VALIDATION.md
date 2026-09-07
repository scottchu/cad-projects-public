# PB-VAL — Recessed Diamond analytic study validation

Status: **PASS** for the isolated appearance-study gate. Recessed Diamond remains a proposal requiring the user's visual decision; this is not CAD or print acceptance.

## Frozen inputs

- Repaired candidate manifest `inputs/candidate.sha256`: 38/38 verified before testing, SHA-256 `8d71809de30441b9f0c0c62fb5191524f06f125c0d010ff71b33d0b6f9ff5779`.
- BRIEF `442c718589ef6a9a2e17037e941e030cad6a3498f33621505aa4a974835e464e`; DESIGN `c81ac2f3b20d8b7a8024b33671c03a6768e77c97ca53646441b86e9032ceb8b8`; IMPLEMENTATION `0017189e52389ea7c678922cb1c9c7f67d23a7a4eba1c951369b5386f3cd87bb`.
- Baseline 19/19 and design-extra 10/10 verified; manifest SHAs `9d08cea42a798c548d54528cb28f715db5335b51d1f06e5cc37b534aeef832bb` and `1bb047310c8904121aa1440139c077673b091c939caf44358d627db836ac65b6`.
- Study: index `5edb9e9a…`, math `85148315…`, repaired renderer `f480e5fd…`, CSS `f6118a47…`; unchanged SCAD `497098af…`.
- Validation input manifest: 10/10 verified, SHA-256 `dfc1c224daddf4f72f2e7e1598231ec9ac0fd48efb9546e8902cacf4050a799c`.

## Independent deterministic checks

Command: `/Users/scottchu/.asdf/shims/node --test projects/laifen-wave-case/tests/node/recessed-diamond-study-independent.test.mjs`.

Result: **7/7 pass** in 37.57 ms. Test SHA-256 `6938eb8d1f0327fdcca342c0024a654885a93a7c106584798802181a624449ab`.

- Bound Current Diamond's wrap, max-absolute field, 0.18 plateau and radius algebra to the frozen SCAD, then compared actual module values with an independently written oracle.
- At depth 0.45, Current center/crossing is `0/-0.45`; Recessed is `-0.45/0`. Both share phase zero.
- A 33×33 four-cell-domain witness at depths 0.10, 0.45 and 0.60 proved both fields stay in `[-d,0]` and repeat under integer u/v shifts.
- Size 4.8, off-grid 4.83 and 8.0 plus depth endpoints matched independent target-arc, count and actual-arc calculations; amplitude tracks depth.
- Both section samplers contain all 513 uniform points and every center, crossing and ±g breakpoint.
- Source checks bind all six canvases to one accepted Size/Depth snapshot, strict blank/nonfinite/range validation, stale edits, reset, device-pixel section redraw, and 44 px exact-input containers.

Commands: `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-pattern-backlog/inputs/{baseline,design-extra,candidate,validation}.sha256` from the repository root. Results: **19/19, 10/10, 38/38 and 10/10 pass**.

## Root-owned browser evidence joined by the validator

On the temporary localhost route, actual Chrome at 1280×900 and 390×844 had document width equal to scroll width. I inspected the repaired screenshots: equal neutral desktop panels, readable section signs/labels, stacked mobile cards, visible 5 mm bars, the analytic truth label and 44 px exact inputs.

The actual input trace exercised blank, off-grid 4.83, depth 0.61, size 9, native slider ArrowRight, Reset and depth 0.50. Invalid edits disabled Render and retained the last plotted snapshot; valid edits marked it stale. Rendering 4.83 and 0.50 put the exact accepted values on all six canvas datasets. The native stepped slider remained 4.8 beside exact raw 4.83, without rounding or changing the raw input.

Repair evidence shows 390 px width/scrollWidth, 44 px inputs, readable 12 CSS px section labels and 21.50 ms initial draw. Resizing while raw Size 4.83 was stale redrew sections from the accepted 4.8/0.45 snapshot and preserved stale state. Browser timing is observational, not a phone-speed guarantee.

Evidence: `/tmp/pattern-backlog-review/browser-trace.json` SHA `ea37b0ab…`; `mobile-r1-state.json` SHA `682d0278…`; `resize-stale-r1.json` SHA `edf5224a…`; repaired desktop/mobile screenshots SHA `b94c04aa…` / `d31e5a89…`.

## Scope and next gate

No production customizer, OpenSCAD, worker, dependency, build, service or compiled artifact was changed or exercised. These checks validate the analytic comparison and state behavior only; they do not establish whole-container geometry, STL, slicing, manufacturability or physical feel. Next: independent critique/formal review, then ask the user whether sunken centers with high crossing ridges are the intended Recessed Diamond appearance.
