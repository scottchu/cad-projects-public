# Drain checkbox follow-up

Baseline HEAD `7b9c960f1a2ef1e0b211c3cbd3f9c0c3a0ab42ef` on existing
`codex/container-desktop-customizer`, draft PR19. Frozen baseline path/content
list: inputs/baseline.sha256. User asks why drains cannot be on both ends and
requests check marks. Exact requested interaction: independent Top and Bottom
checkboxes; none selected maps none, Top only top, Bottom only bottom, both both.
Existing Bottom-only default/reset persists. This explicitly supersedes the
previous iteration's immutable SCAD/schema boundary ONLY to enable both drain
locations using the existing cutters. No hole size/location/thread/shape change.

## Requirements

- DR-01: Labeled Drain holes group, independent Top/Bottom native checkboxes;
  neither, either or both selectable; accessible labels and44px touch rows.
- DR-02: Both state reaches authoritative SCAD and actually cuts both end faces
  in smooth/body/cap/assembled/print-layout; existing diamond branches accept
  same condition, without enabling the disabled Diamond UI.
- DR-03: All validators/enums agree on none/top/bottom/both. Checkbox edits use
  existing stale/cancel protection and never compile automatically; Reset
  restores Bottom only, invalid dimension issues remain intact.
- DR-04: Preserve default geometry exactly; validate end openings in actual
  compiled parts for all4 modes, plus focused controller toggle/reset tests.
  No new print-ready, slicer or physical acceptance. Preserve8448 services.

## Bounded task DAG

`DR-IMP-01 → (DR-VAL-01 || DR-CRIT-01) → DR-REV-01`.
This is a prescribed UI/boolean-extension task; user supplies the complete
selection semantics. No separate mechanism design is needed. Root owns
coordination/manifests/continuity indexes and prescribed runtime serving.

| Task | Owner | Scope / done gate | Frozen inputs | Bounds |
|---|---|---|---|---|
| DR-IMP-01 | /root/drain_implementation | active appcheckbox UI/controller/enums, SCAD4drain conditions, relevant Python contract if needed, focusedtests, IMPLEMENTATION | baseline+thisbrief | balanced/medium;5min checkpoint; initial+2focusedrepairs |
| DR-VAL-01 | /root/drain_validation | independent tests and compiled-end geometry evidence, VALIDATION only | frozen candidate | strong/high;5min checkpoint; no sourcewrites |
| DR-CRIT-01 | assigned after candidate | read-only checkbox UX/scope critique, CRITIQUE only | frozen candidate/screenshots | strong/high;3min checkpoint |
| DR-REV-01 | distinct owner after gates | REVIEW only, formal evidencejoin | candidate+receipts | strong/high;3min checkpoint |

Allowed reads: relevant project continuity/source/tests and this contract.
Forbidden: other projects, unrelatedgeometry, sourceversion substitutions,
engine/worker/lock changes, printer/publichosting/8448 changes. One writer per
namespace, max3workers. Each receipt names verifiedmanifest/hash, changedpaths,
commands/results, findings/coverage/risks/nextaction. Stop for drift or unrelated
mechanics changes. Browser may still be blocked by CUA window access; record
that separately from deterministic/compiled evidence. Root will rebuild the
already-authorized private8453 preview after source freeze and preserve PRdraft.
