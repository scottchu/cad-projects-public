# Compact controls follow-up

Baseline HEAD `5acaede2114614882ed92cd362b3bc120deed5d7`, branch `codex/container-desktop-customizer`; frozen paths in `inputs/baseline.sha256`. Previous iteration remains historical C2 acceptance. User phone screenshot reports canvas scrolls away, text buttons consume excessive space; requests icon buttons, parameter sliders and embedded rules showing allowed values. Desktop canvas-left/parameters-right and generation/reset/download behavior remain required. No CAD geometry change requested. Current private review URL https://mac-mini.duckbill-ionian.ts.net:8453/ proxies the built app on 5178; preserve all other services.

## Execution DAG and bounds

`MC-DES-01 → MC-IMP-01 → (MC-VAL-01 || MC-CRIT-01) → MC-REV-01`.
Root coordinates, freezes manifests, runs prescribed browser interactions where worker browser access unavailable, maintains continuity indexes and delivers reviewed build to already-authorized preview.

| Task | Owner | Role / done gate | Dependencies / immutable inputs | Exclusive writes | Ceiling / status |
|---|---|---|---|---|---|
| MC-DES-01 | /root/compact_design | Numeric and responsive interaction contract | baseline.sha256 | DESIGN.md and frozen contract requirements here | strong/high; 6 min checkpoint, 1800 words; ready |
| MC-IMP-01 | assigned after design | Working controls and focused regression coverage | baseline + frozen DESIGN | app HTML/CSS/UI modules, focused test, IMPLEMENTATION.md | balanced/medium, 12 min checkpoint; pending |
| MC-VAL-01 | assigned after implementation | Independent rule/lifecycle and responsive evidence | frozen candidate | VALIDATION.md | strong/high, 8 min checkpoint; pending |
| MC-CRIT-01 | assigned after implementation | Independent UX critique of candidate and captures | frozen candidate | CRITIQUE.md | strong/high, 6 min checkpoint; pending |
| MC-REV-01 | distinct owner after evidence | Formal join of candidate and evidence | frozen candidate + evidence | REVIEW.md | strong/high, 5 min checkpoint; pending |

All workers may read project source, continuity and user attachment. No changes to SCAD/schema/worker, other projects, services or hosting. One writer per namespace. Each task initial attempt plus at most two focused repair cycles, single bounded receipt, no raw diaries. Manifest changes invalidate only affected gates. Stop for baseline drift or need to change mechanics; return status, verified fingerprint, changed paths, commands/results, findings/severity, requirement coverage, risks and next action. Concurrency max three workers. Exact runtime/token controls unavailable; qualitative bounds apply.

## Frozen compact-control requirements

- MC-REQ-01: At widths up to 760 px, the viewport is a two-row workspace: a
  fixed preview row above one independently scrolling parameter row. The model
  remains visible while parameters scroll; the document itself must not be the
  scrolling container.
- MC-REQ-02: At wider widths, retain the full-height canvas-left,
  parameters-right workspace. No page title or development copy is added.
- MC-REQ-03: Replace visible text action/view buttons with compact icon-only
  controls. Each remains at least 44 by 44 CSS px and has an exact `aria-label`,
  an SVG `title`, keyboard focus, disabled/pressed state, and visible tooltip on
  hover or focus. No icon library or network asset is required.
- MC-REQ-04: Each editable dimension provides a slider and a compact, directly
  editable numeric value in millimetres. The slider exposes only values allowed
  by the unchanged schema and the other current dimensions. It never changes a
  dependent dimension to make itself valid.
- MC-REQ-05: A rule line beside each dimension states its currently allowed
  numeric interval. Invalid, empty, or infeasible typed input stays visible and
  disables Generate; it is never clamped, rounded, replaced, or converted to
  zero.
- MC-REQ-06: Slider movement updates the draft, derived dimensions, stale state,
  and rules only. It never starts generation. Generate remains explicit; an edit
  during generation uses the existing cancellation/late-result protections.
- MC-REQ-07: Preserve Auto/manual lid behavior, drains, export selection,
  Cutaway/3D, Reset view, Generate/Cancel, Reset dimensions, and current-only
  Download. Reset dimensions restores all defaults without generating.
- MC-REQ-08: Preserve exact OpenSCAD/schema/worker behavior and the 4 mm
  advertised wall floor. This follow-up creates no new CAD, printability, or
  physical-acceptance claim.
