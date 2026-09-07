# Drain-hole count gate

Baseline commit `2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f`; frozen 19-path
manifest `inputs/baseline.sha256`, SHA-256
`e0304165a054bd228d59d48b024bd9eeed2dfd1f7140f1a202b69411e08390aa`.
All 19 entries verified before design. The user accepted independent Top/Bottom
drain checkboxes and requested one item at a time: hole count now, pattern next.

## Outcome and requirements

- DC-01: Add one shared **Number of holes** integer exact input plus range
  slider. It is the total opening count on every selected end, range `1..24`,
  step `1`, default and Reset `7`.
- DC-02: Preserve the existing family: `N=1` is the center hole; `N>=2` is the
  center plus `N-1` equally spaced ring holes. `N=2` therefore has center and
  one `+X` ring hole. `N=7` must reproduce the exact existing center-plus-six
  geometry at angles `0,60,...,300` degrees.
- DC-03: Keep hole diameter `d=3 mm` and browser ring radius
  `R=min(9,D/2-2)` unchanged. Authoritative SCAD/schema must also remain valid
  when their existing general `d` and `R` parameters are edited directly.
- DC-04: Apply a `g=0.4 mm` minimum clear material ligament between openings
  and the inner sidewall. This is a design assumption based on one nominal
  nozzle diameter, not slicer, strength, drainage, or physical proof.
- DC-05: Embed the current safe count maximum in the slider and report exact
  count or coupled diameter/count errors. Preserve raw invalid text; never
  clamp, round, generate automatically, or replace it through browser range
  coercion.
- DC-06: Preserve all four drain selections, Bottom-only default/Reset,
  stale-result clearing, active-work cancellation, explicit Generate, output
  modes, source/worker lock, and private-preview boundaries.
- DC-07: With neither end selected, disable but remember the raw count. Count
  syntax/spacing does not block drain-free generation; re-enabling an end
  restores the same raw value and exposes any error. A safe emitted integer is
  distinct from the remembered raw draft when the inactive raw value is not a
  valid source parameter.

## Scope and acceptance

Change only the active count UI/state, browser schema/adapter/bounds, the
authoritative SCAD count parameter/polar loop/assertions, focused tests, and
iteration evidence. Pattern choices, hole-size/radius UI, per-end counts,
other geometry, CAD/STEP regeneration, slicing, printing, drainage performance,
public hosting, 8448, Tailscale and printer actions are excluded.

Accept only after focused source/controller tests, pinned-WASM actual-opening
checks, default `N=7` Bottom-only byte parity, compact desktop/mobile review,
independent critique and validation, and a distinct formal evidence join.

## Bounded task DAG

`DC-DES-01 -> DC-IMP-01 -> (DC-CRIT-01 || DC-VAL-01) -> DC-REV-01`.

| Task | Role / owner | Done gate | Bounds |
|---|---|---|---|
| DC-DES-01 | design, `/root/drain_count_design` | this brief and exact design contract | strong/high; checkpoint 3 min; ceiling 6 min / ~4k output |
| DC-IMP-01 | distinct implementer | source, focused tests, receipt against frozen design | balanced/medium; initial + 2 focused repairs |
| DC-CRIT-01 | distinct critic | read-only UX/scope critique of frozen candidate | strong/high; no candidate writes |
| DC-VAL-01 | distinct validator | independent math/source/compiled-solid evidence | strong/high; no candidate writes |
| DC-REV-01 | distinct formal reviewer | join verified candidate, critic and validator receipts | strong/high; no candidate writes |

Each task verifies its immutable manifest/candidate fingerprint and reports
status, changed paths, commands/results, hashes, requirement coverage, risks and
next action. One writer per namespace; at most three workers. Stop on baseline
drift, unrelated geometry/service scope, or after two focused repair cycles.
