# XT60 bend jig project state

Last updated: `2026-10-26`

## Active iteration

- Active iteration: [direct rail editing](docs/iterations/2026-10-26-direct-rail-editing/BRIEF.md).
- Both endpoints are directly draggable, the whole rail translates on line
  drag, and a curve dot shapes each path. Candidate: `preview/xt60-rail-customizer.html`.
- Current gate: direct editing delivered in [PR #27](https://github.com/scottchu/cad-projects/pull/27), ready for user evaluation. User decision: none required for recovery.
- Proven self-checks: archived P20 rail/profile math and coupon web witness;
  offline Chrome OPEN/END drag, fixed local cuts during scrub, keyboard edits,
  JSON save/load/rejection, SVG exports, reset/play and desktop/mobile layout.
- CAD baseline stays P19 R1; P25 remains bounded first-CAD preview history with
  its product-level review/physical gates unresolved. No CAD regenerated.
- Canonical ordered backlog: RC-1 `delivered` simulator recovery; DE-1 `delivered` direct rail editing, source
  and UI evidence in the recovery iteration; RC-2 `deferred` P25 user preview
  decision, CAD evidence in the P25 iteration; RC-3 `deferred` one-side physical
  latch/hinge coupon, contingent on product decision and separate authority.

## Preserved mechanism state (2026-09-10)

## Baseline

- Canonical project: `projects/xt60-bend-jig`.
- P19 R1 remains the latest accepted digital mechanism baseline. P25 is a
  later first-CAD concept preview with a separate, narrower acceptance state.

## Prior mechanism iteration

- The prior mechanism iteration is `p25-r1-rear-loop-front-pusher-clamp`.
- Frozen P25 source candidate: commit `a1932fb19ffeb6d584153d1c201ebe24b2e06d6a`;
  candidate-manifest file SHA-256
  `88fdcd25585c35277d66a769b5c35208f8e5b8c7534d93efdbcb57493638a845`
  with `13/13` entries preserved.
- P25 is accepted only as a user-facing first-CAD preview. It has source and
  written-STEP review evidence, but no manufacturing, slicing, printing,
  holding-force, spring, or physical-operation acceptance.
- The user still moves all three rods manually: thumb pushes Orange DOWN;
  index and middle fingers push Blue and Green BACK-to-FRONT. The two mirrored
  clamp modules act only after the inherited END pose is reached.
- Each rear yoke supports Blue and Green together; each hinged front bar
  contacts Orange only. The three purchased rods remain exactly
  `OD4.00 x 50.00 mm`; cap count and P24 screw-cassette count are zero.
- The frozen review records `23/23` focused P25 checks and `42/42` targeted
  P20 R4 + P24 + P25 checks. These are historical receipts; the delivery
  candidate preserves their bytes and does not regenerate CAD.

## Accepted baseline and preserved history

- P19 R1 remains the latest accepted digital mechanism baseline for parametric
  CAD, its six written STEP artifacts, and exact-artifact Viewer handoff. Its
  manifest SHA-256 remains
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`
  (`20/20`). P25 is a later concept preview and does not promote or replace
  P19's fabrication status.
- P17 through P24 records and artifacts are preserved as historical,
  rejected, superseded, experimental, or bounded preview evidence according
  to each iteration's own review. None is another current iteration.
- P20 R4 remains a superseded preview with the known RELEASED_OPEN Blue/XT60
  collision (`186.980487360803 mm3`) and thin-web blockers. Its print-kit
  parent hash guard now reports two historical drift failures; preserve that
  guard and do not reuse the old accepted fingerprint.
- P24 remains first-design-intent evidence only. P25 superseded its screw-
  cassette direction for forward concept review.

## Acceptance state

- The P25 opening spring is only an `UNVERIFIED` envelope. Immediate pop-open,
  flexure force/strain/fatigue, holding force, zero-cap axial retention,
  tolerance, wear, saddle/pad fidelity, and two-side load balance remain open.
- The inherited P20 RELEASED_OPEN Blue/XT60 collision blocks complete-product
  and print acceptance.
- Preserved STEP, 3MF, G-code, review images, and preparation records retain
  only the status stated by their own iteration. Their presence does not grant
  current slicing, printer, or physical authority.

## Delivery provenance

- This main-reconciliation candidate is based on `cf8ec46` and preserves the
  intentional XT60 branch/WIP bytes from source checkout `a883404` and recovery
  snapshot `design-main-20260910T101124`.
- Delivery records and exact path/hash mappings are in
  `../../docs/iterations/2026-09-10-local-work-delivery/`.
- No geometry was redesigned or regenerated during reconciliation.

## Next action

Open `preview/xt60-rail-customizer.html` for user evaluation. Recovery is delivered
in PR #27; merge was not requested. See the active iteration HANDOFF for evidence
and the retained task worktree. No product CAD or fabrication gate was reopened.

## Preserved mechanism next gate

Obtain independent validation, critique, and formal review of the delivery
candidate. After delivery, the product-level next gate remains explicit user
PASS/FAIL on P25 as a first-CAD preview. Only after that, and only with separate
authorization, consider one single-side latch/hinge physical coupon.
