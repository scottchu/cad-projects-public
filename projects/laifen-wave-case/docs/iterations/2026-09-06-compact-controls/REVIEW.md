# MC-REV-01 — formal independent review

## Verdict

**APPROVED for commit to the existing draft PR 19 with an explicit browser-gap
disclosure. NOT approved for merge, release, or UI acceptance.**

No actionable P0/P1/P2 source finding remains against the compact-controls
contract as amended by `RULES-REVISION.md`. C5 may be committed as a reviewable
source and deterministic-test checkpoint. The draft PR must state that fresh C5
browser interaction evidence is blocked by the unavailable desktop provider and
that the unchanged-CSS C4 captures establish layout continuity only.

## Provenance

- `inputs/candidate-05.sha256` has SHA-256
  `f51607ab4e80b2d2b6fa753d90f55f1cb64504c42c3b5919e6175d27e100e714`;
  all 23 declared paths passed `shasum -a 256 -c` during this review.
- `inputs/review-join.sha256` has SHA-256
  `92b560f3a96085f4c2ca87a675c684ce2a64916502d5b13be959b9cc3dcd3072`;
  all five joined candidate/evidence paths passed.
- Governing revision SHA-256 is
  `53f9dd990507ec640f615cac30dbc466e1ecff325494886af2535c96e586a6ca`.
  The original BRIEF/DESIGN remain authoritative except for the clauses
  explicitly superseded by that revision.
- SCAD, schema, worker, and dependency lock retain the frozen hashes. CSS is
  `a25b47f668009b1d8b15c29179b566ae5fd5018105f8c4d2ca03a3cee2c643be`,
  byte-identical to C4.

The implementer, critic, validator, and formal reviewer are distinct identities.
The implementation receipt, independent critique, and independent validation
are present in the verified join. I inspected the frozen controller, pure draft
derivation, control binding, HTML/CSS, lifecycle boundary, and focused tests. I
did not repeat the already-passing broad test suite or mutate source/tests.

## Findings and coverage

- **P0/P1/P2: none.** One pure `deriveDraftState(raw,lastValidDimensions)` owns
  issues, error projections, slider rules/state, summary, generation values,
  Generate eligibility, and the complete last-valid snapshot. Raw invalid text
  is preserved; invalid dimensions pause every slider with truthfully labeled
  last-valid ranges; selector errors do not disturb coherent dimension sliders.
- **MC-REQ-01/02:** layout source passes. C4's eight Safari captures establish
  the pinned mobile preview, independent parameter scrolling, fixed dock,
  760/761 breakpoint, and desktop two-pane layout because CSS is unchanged.
  They do not accept C5's added form-error markup.
- **MC-REQ-03:** source provides compact 44 px local-SVG controls, exact labels
  and titles, stable Generate/Cancel slot, pressed/disabled styling, focus ring,
  and edge-aware tooltips. Fresh keyboard, focus, and tooltip observation is open.
- **MC-REQ-04/05/06:** deterministic evidence passes: 25 Node tests, four
  Python tests, 26 independently derived intervals, and 22,458 slider ticks.
  Controller tests cover coherent invalid ownership, raw retention, whole-state
  fallback, slider synchronization without generation, and active-job
  invalidation.
- **MC-REQ-07:** source and deterministic lifecycle tests preserve Auto/manual
  lid, drains/output, reset, views, epochs, exact Blob ownership, and stale-result
  rejection. A real C5 WASM generation/current-only STL download remains open.
- **MC-REQ-08:** unchanged hashes plus schema tests support no-CAD-change and the
  advertised 4 mm floor. No mesh, slicer, printability, assembly, or physical
  acceptance is established.

## Remaining risk and closure gate

Browser acceptance is **BLOCKED**, severity **P1 acceptance gap**, because every
fresh Safari/Chrome attempt returned `CUA-10005 cgWindowNotFound` and no browser
provider was available. Exact HTTP byte parity for all six built assets proves
the private URL serves C5; it does not prove browser behavior.

After the desktop is unlocked, reverify the C5 manifest and run one narrow fresh
browser gate: capture mobile invalid state and desktop default state; inspect
error associations, icon names/tooltips/focus, and the Generate/Cancel slot;
exercise blank/70 plus manual/Auto coupled recovery, slider no-generation,
Reset, and an edit during generation; then generate and download one current
nonempty STL and prove an edit disables that download. Reuse the C4 size matrix
unless CSS changes. Only a passing receipt on the same fingerprint can promote
the draft from this commit checkpoint to merge/UI acceptance.

Review scope authorizes no merge, public deployment, printer action, or physical
claim. This reviewer changed only `REVIEW.md`.
