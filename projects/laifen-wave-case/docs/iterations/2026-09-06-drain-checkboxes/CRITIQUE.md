# DR-CRIT-01 independent checkbox critique

- Owner / role: `DR-CRIT-01`, independent UX and source critic
- Date: 2026-09-05
- Verdict: **PASS for the scoped checkbox candidate**
- Highest severity: `P3` reviewability note; no functional blocker
- Candidate-manifest fingerprint: `4a716d71c154bcba1264d556946613ec615c50217bba6331e36da8e9f1c67389`
- Baseline HEAD: `7b9c960f1a2ef1e0b211c3cbd3f9c0c3a0ab42ef`

## Provenance and checks

The supplied manifest itself matched the assigned fingerprint and every path in
the manifest matched its recorded SHA-256 before inspection.

```text
shasum -a 256 inputs/candidate-01.sha256
  4a716d71c154bcba1264d556946613ec615c50217bba6331e36da8e9f1c67389

shasum -a 256 -c inputs/candidate-01.sha256
  19/19 paths: OK

node --test tests/node/compact-controller.test.mjs \
  tests/node/desktop-customizer.test.mjs
  27 passed; 0 failed
```

Static inspection covered the small drain UI, controller, browser enums and
adapter, draft validator, authoritative SCAD, and focused tests. A live Safari
observation covered the private `:8453` preview at a 1440 x 900 viewport.

## Findings

The candidate satisfies the requested interaction. `Drain holes` is a native
`fieldset` with a legend and two label-wrapped native checkboxes. `Top` and
`Bottom` are distinct accessible checkbox names. Each full label row has a
44 px minimum height, so the text and checkbox share a practical touch target.
The group remained compact and readable in the live layout.

The controller derives exactly `none`, `top`, `bottom`, or `both` from the two
booleans. Both checkboxes use the existing `edit()` route. The focused tests
confirm all four mappings, no edit-triggered generation, invalid dimension
draft preservation, active-work cancellation, and a Bottom-only reset. In the
live preview, checking Top while Bottom remained checked visibly selected both,
kept the prior render labeled `Previous generation`, and changed status to
`Dimensions changed. Generate to update.` No automatic compile was observed
from that edit. The final observed state was restored to Top off / Bottom on.

The browser schema, draft validator, adapter, and OpenSCAD enum comment all
accept the same four values. In both smooth and diamond source branches,
`bottom || both` subtracts the unchanged body cutter and `top || both`
subtracts the unchanged cap cutter. Body, cap, assembled, and print-layout
outputs all route through these two shell modules, so no output path bypasses
the independent conditions. This critique confirms the branch topology; the
validator's compiled-solid receipt remains the authority for actual openings.

### P3 — full-file CSS formatting churn

`style.css` changed from one minified line to 401 formatted lines while adding
the checkbox styles. The declarations appear behavior-preserving outside the
new drain selectors, and the live layout showed no regression, so this does not
block the candidate. It does make the narrow UI change harder to review and
weakens line-level provenance. Future focused changes should avoid combining a
whole-file format pass with behavior changes unless formatting is itself part
of the task.

## Acceptance boundary

This PASS covers checkbox semantics, accessibility structure, live presentation,
controller lifecycle behavior, enum agreement, and source routing for the exact
frozen candidate. It does not establish compiled geometry, slicer readiness,
printability, or physical drainage performance.
