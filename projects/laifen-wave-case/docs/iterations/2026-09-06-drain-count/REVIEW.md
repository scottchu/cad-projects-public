# DC-REV-01 — formal independent review

## Verdict

**PASS for the scoped drain-hole count source and behavior; approved for a
commit to the existing draft PR 19.** No blocking or medium finding remains.
This review does not authorize merge or the next pattern item, and makes no
slicer, print-ready, drainage-performance, fit, strength, or physical-
acceptance claim.

## Provenance and independence

- Baseline commit: `2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f`.
- Baseline manifest: `inputs/baseline.sha256`, SHA-256
  `e0304165a054bd228d59d48b024bd9eeed2dfd1f7140f1a202b69411e08390aa`.
- Frozen design: `DESIGN.md`, SHA-256
  `41c1717355117185850b8d17783278ca81a65b6bcf020a83c0a32f6b6e017ce0`.
- Frozen C3 candidate: `inputs/candidate-03.sha256`, SHA-256
  `6fa4bb84a83bc859b95b0568d43e34227a5bc2be7f82fe8fb6a2f11796953f57`;
  all 22 declared paths passed `shasum -a 256 -c` in this review.
- Final evidence join: `inputs/review-join.sha256`, SHA-256
  `50ca3ccc31295996104de8244e31ec32faf26753d8ac2eb2303a53801a4e522c`;
  its candidate manifest and distinct implementation, critique, and validation
  receipts all passed `shasum -a 256 -c`.
- DC-IMP-01, DC-CRIT-01, DC-VAL-01, and DC-REV-01 have distinct role
  identities. I inspected the frozen brief/design, authoritative source and
  focused test changes, scope diff, and joined receipts. I did not rerun the
  already-passing build or tests, inspect the browser independently, start a
  service, mutate source/tests, or make a delivery action.

Mutable continuity indexes are outside the candidate manifest and remain
root-owned. Their concurrent updates do not change the frozen C3 source or the
joined evidence.

## Requirement disposition

- **DC-01 passes.** The browser exposes one shared raw-text **Number of holes**
  input and paired integer range for every selected end. Source, schema,
  adapter, controller, Reset, and generation values agree on range `1..24`,
  step `1`, and default `7`.
- **DC-02 passes.** The SCAD and browser helper implement `N=1` as center only
  and `N>=2` as center plus `N-1` equally spaced ring holes beginning at `+X`.
  The validator independently checked `N=1`, `2`, and `7`; default `N=7`
  retains the exact prior six-ring-hole angles and the default smooth
  assembled Bottom-only STL is byte-identical to baseline at
  `b1b9db18e21cafed5237afb90e57831b72246c6ac2e4b4c88f736738fd0cf169`.
- **DC-03 and DC-04 pass for source and compiled geometry.** Browser `d=3 mm`
  and `R=min(9,D/2-2)` remain unchanged. The schema and authoritative SCAD
  independently enforce the `g=0.4 mm` center, sidewall, center-to-ring, and
  adjacent-ring equations for directly edited valid `d` and `R` values. The
  independent pinned-WASM evidence counted the requested actual openings,
  retained solid mid-ligaments and sidewalls, closed positive-volume meshes,
  and unchanged bounds for `N=1,2,7,17` and the `D=10/11/30` boundaries.
- **DC-05 passes.** Dynamic maxima are exactly `D10 -> 1`, `D11 -> 7`, and
  `D30 -> 17`. Invalid raw text and out-of-range/coupled values remain exact,
  produce the specified direct or shared count/diameter errors, disable
  Generate, and never clamp or generate. The count range pauses for malformed
  drafts and displays the nearest valid repair maximum for a valid coupled
  draft.
- **DC-06 passes within the scoped regression evidence.** All four drain
  selections, Bottom-only Reset, explicit generation, stale-result marking,
  active-work cancellation, output modes, source/worker lock, compact
  desktop/mobile layout, and private-preview boundaries are preserved. The
  focused receipt records 29 passing Node checks and 12 passing Python checks;
  root Safari covered the prescribed 1440 x 900 and 390 x 700 states. The six
  private route responses matched the validated local build byte-for-byte.
- **DC-07 passes.** With neither end selected, both count controls are disabled,
  the raw draft is remembered, invalid count syntax does not block drain-free
  generation, and a safe canonical `7` is emitted only for an invalid inactive
  source value. Re-enabling an end restores and validates the unchanged raw
  draft.

## Finding disposition

- C1-01, the adapter ignoring and replacing explicit count, is resolved in C2.
- C1-02, malformed count leaving its range enabled, is resolved in C2.
- C1-03, coupled-error range showing `1` instead of the nearest repair, is
  resolved in C2.
- C2-04, malformed active count disabling the exact repair input, is resolved
  in C3. C3 source, focused recovery tests, and Safari evidence show the exact
  field remains editable while only its paired range is unavailable.
- No open critic or validator finding blocks this scoped delivery.

## Source/version preservation and limits

The baseline comparison confines authoritative implementation changes to the
SCAD count parameter/assertions/polar loop; count UI; browser
schema/adapter/bounds/controller; the new pure drain-layout helper; and focused
controller coverage. Candidate-manifest hashes preserve the unrelated
controls, dimensions, lifecycle, main, viewer, style, Python contract/tests,
desktop regression test, and prior functional-repair test. No pattern selector
or pattern geometry is introduced: pattern remains the user's next separate
item.

This review accepts source behavior, compiled mesh evidence, the prescribed
browser states, default artifact parity, and private served-byte parity only.
No STEP regeneration, slicer validation, print, water-passage, occlusion,
durability, fit, or physical acceptance was performed. Any candidate-manifest
path change invalidates the affected downstream gates. This reviewer wrote only
`REVIEW.md`.

## Commands run by this reviewer

```text
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/inputs/candidate-03.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/inputs/candidate-03.sha256
git diff --name-status 2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f -- projects/laifen-wave-case
git diff --stat 2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f -- projects/laifen-wave-case
git status --short -- projects/laifen-wave-case
git diff --unified=100 2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f -- projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad projects/laifen-wave-case/preview/openscad-wasm-simulator/index.html projects/laifen-wave-case/preview/openscad-wasm-simulator/src/adapter.mjs projects/laifen-wave-case/preview/openscad-wasm-simulator/src/bounds.mjs projects/laifen-wave-case/preview/openscad-wasm-simulator/src/controller.mjs projects/laifen-wave-case/preview/openscad-wasm-simulator/src/schema.mjs projects/laifen-wave-case/tests/node/compact-controller.test.mjs
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/inputs/review-join.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/inputs/review-join.sha256
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/REVIEW.md
git diff --check -- projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/REVIEW.md
```
