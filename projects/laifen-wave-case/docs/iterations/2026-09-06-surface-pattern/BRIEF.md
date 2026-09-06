# Surface-pattern gate

Baseline commit `cf4adb08314989f9d52a7afbd2f868756226d799`; frozen 21-path
manifest `inputs/baseline.sha256`, SHA-256
`93cfe95cbc96faf81af3f799a37ac504d71019457152ec502bf82cf468798203`.
All entries verified before design. The user accepted drain count and said
“next”; this gate adds only the existing Smooth/Diamond choice.

## Frozen outcome and requirements

- SP-01: Add a compact **Surface pattern** fieldset with two labelled visual
  swatches backed by native radios: **Smooth** and **Diamond**. Swatches explain
  the choice; they are not geometry evidence. Keep text labels and 44 px targets.
- SP-02: Browser default and Reset remain Smooth. A pattern edit preserves all
  dimensions/drain/output state, cancels active work, invalidates download
  currency, marks an earlier preview stale, and waits for explicit Generate.
- SP-03: Diamond is the existing source-native relationship B with fixed axial
  pitch `4.8 mm`, target arc pitch `3.63 mm`, depth `0.45 mm`, phase `0 deg`,
  plateau half-fraction `0.18`, shared body/cap phase, and no seam collar.
  Expose no new texture slider, motif, or preset.
- SP-04: Preserve raw dimensions. Diamond never silently raises wall thickness.
  At `wall < 4.4 mm`, keep Diamond selected, identify pattern and wall, explain
  the `4.4 mm` minimum, and disable Generate until wall or pattern is changed.
- SP-05: Preflight every existing Diamond assertion, including the per-part
  `250000` estimated exterior-triangle cap. Offer only repairing slider ranges;
  do not defer a known incompatibility to the compiler or coerce the draft.
- SP-06: Preserve the accepted dimensions, drain checkboxes/count, all four
  outputs, smooth geometry/bytes, exact-job identity, current epoch ownership,
  fresh-worker lifecycle, 180 s runtime timeout, and private port 8453 boundary.
- SP-07: The authoritative SCAD and pinned engine/worker are immutable for this
  UI gate because baseline Diamond probes found no source defect. Any contrary
  geometry finding stops implementation and reopens design.

## Scope and acceptance

Implementation may change only the simulator HTML/CSS, browser schema/state/
controller, focused tests, built private candidate, and iteration evidence.
SCAD/CAD/STEP, fixed Diamond math, dependencies, worker, 8448, Tailscale,
printer state, slicing, upload/start, public hosting, new motifs and texture
parameters are excluded.

Accept only after focused math/state/lifecycle tests; real pinned-WASM Diamond
body, cap, assembled and print-layout runs; detailed actual-mesh gates; desktop
and mobile browser review; served-byte parity on private 8453; distinct critic,
validator and formal-review provenance. Each role must compile in `<=60 s`;
the product timeout remains `180 s`.

## Task DAG and mutable status

`(SP-DES-01 || SP-VAL-PREP) -> SP-IMP-01 -> (SP-CRIT-01 || SP-VAL-01) -> SP-REV-01 -> SP-DEL-01`.

| Task | Role / owner | Inputs and exclusive writes | Done gate | Status |
|---|---|---|---|---|
| SP-DES-01 | design, `/root/surface_pattern_design` | baseline manifest; `BRIEF.md`, `DESIGN.md` | frozen numeric/UI/test contract | complete |
| SP-VAL-PREP | discovery validator, `/root/drain_count_validation` | baseline manifest; `/tmp/surface-pattern-validation` only | independent baseline Diamond readiness receipt | active |
| SP-IMP-01 | distinct implementer | frozen design manifest; UI/state/tests/build/evidence | candidate manifest and focused receipt | blocked |
| SP-CRIT-01 | distinct critic | frozen candidate; `CRITIQUE.md` only | UX/scope/DfAM findings | blocked |
| SP-VAL-01 | distinct validator | frozen candidate; `VALIDATION.md` only | independent browser/mesh evidence | blocked |
| SP-REV-01 | distinct formal reviewer | candidate plus critic/validator receipts; `REVIEW.md` | evidence join and disposition | blocked |
| SP-DEL-01 | root delivery owner | reviewed build; continuity/private-service records | 8453 parity/browser receipt and user gate | blocked |

Shared bounds: exact project/iteration/baseline above; design/discovery use
strong/high with 3 min checkpoint and 6 min/~4k-output ceiling; implementation
uses balanced/medium; critique, validation and review use strong/high. One writer
per namespace, at most three workers, initial attempt plus two focused repairs.
Every receipt reports identity, verified fingerprint, changed paths, commands and
results, hashes, requirement coverage, risks and next action. Forbidden to every
task: unrelated projects, 8448/public/printer changes and acceptance promotion.
Stop on manifest drift, source defect, dependency/worker change, missing native
oracle, a role over 60 s, or exhaustion of the repair ceiling.
