# P23 R1 mirrored screw-clamp first design

Date: `2026-08-29`

Status: **FIRST-DESIGN INTENT PREVIEW ACCEPTED; NOT PRINT AUTHORITY**

## Product-baseline change

P23 replaces six individual rod-end caps with two mirrored side clamp modules.
That changes the part roles, retention interface and user workflow, so it is a
new `P` baseline rather than a P21 fit refinement.

## User-observed basis

- The current physical prototype works when Blue and Green are held while the
  Orange rod is pressed directly into CLAMPED/END.
- Releasing hand force causes immediate back-drive to OPEN.
- The three purchased stainless rods are immutable `OD4.00 x 50.00 mm`.
- User-supplied angle-clamp image is inspiration for a threaded translating
  jaw, not a dimensioned contract and not an instruction source.

## Frozen first-design contract

- Preserve the current four-plate, three-rod, one-stepped-axle assembly as
  context; do not redesign inherited YZ rod paths or rails in this iteration.
- Remove all six individual caps from the forward concept.
- Add one mirrored clamp module on each axial side.
- Each module captures Blue and Green as reaction seats and uses one printed
  threaded screw/knob plus translating shoe to drive the Orange rod toward
  CLAMPED/END.
- The left and right screw modules have equal pitch and equal nominal travel.
- Both modules must visibly retain all three rod ends against axial escape in
  the preview; pure end-face pressure is insufficient.
- First design is an evidence-only STEP preview. Thread strength, print
  tolerance, torque, holding force, wear, synchronized use and manufacturability
  remain open.

## Coordinate frame

- Units: millimetres.
- X: rod axis, left/right side-clamp direction.
- FRONT is world YZ; `+Z` is XT60 mating-head/up and `+Y` is wire-tail/outward.
- OPEN and CLAMPED rod identities and order remain unchanged.

## Immutable input manifest

```text
7d7cd580914ce231af11f6156eac1f9dd9f3ae0a474997230baa518a0f610bd1  docs/REQUIREMENTS.md
54dec75dd5291a4b63b4589cbd61ab403b334a088007d62ab25723dce1a5c3b7  docs/EXPERIENCE.md
b433708178c01a2eb7540085ad4b7241a1b7bc4659217f3b6a0517a7d0176337  docs/iterations/p21-r1-axial-width-cap-fit/BRIEF.md
d37cf982e2c9704234e05121c5d84ea72efbcdcf0e778a15a13b19f691405078  cad/p22_bridge_latch_concept/p22_bridge_latch_common.py
d4c9d5bc428d3e426df1e80099ceef33b1de820fa8af6b4f5a569e97d2480d58  src/xt60_bend_jig/p20_r4_custom_profile_full_cad.py
aa6b1e00798261ba23a7ddf4f3732d7c47eab60c8271dcb0af1f2f82f6b499ec  supplied angle-clamp inspiration image
```

## Execution DAG

| ID | Role | Depends on | Exclusive write scope | Done gate | Status |
|---|---|---|---|---|---|
| P23-DESIGN-01 | design | frozen brief | `DESIGN.md` | numeric first-design contract and risks | complete |
| P23-IMPLEMENT-01 | implementation | DESIGN-01 | P23 source/tests/artifacts | OPEN/CLAMPED STEP states generated | complete after repair cycle 1 |
| P23-CRITIC-01 | critic | IMPLEMENT-01 | `REVIEW.md` critic section | mechanical/usability findings | complete; intent PASS |
| P23-VALIDATE-01 | validator | IMPLEMENT-01 | `VALIDATION.md` | independent geometry/requirement checks | complete; intent PASS |
| P23-REVIEW-01 | formal reviewer | CRITIC-01, VALIDATE-01 | `REVIEW.md` verdict section | intent-preview disposition | complete; ACCEPT |

Default ceilings: one initial attempt plus at most two focused repairs; no
mesh, 3MF, slicing, upload or print; at most three workers concurrently.
