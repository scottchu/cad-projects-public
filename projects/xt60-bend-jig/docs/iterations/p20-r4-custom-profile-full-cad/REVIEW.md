# P20 R4 formal independent review

Date: `2026-08-27`

Task: `P20R4-REVIEW-01`

Owner/role: `/root/p20_final_reviewer`, formal independent reviewer. This
role did not design, implement, repair or validate the candidate.

Candidate-manifest SHA-256:
`e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`.

## Decision

- **User-facing full-CAD intent preview: CONDITIONAL PASS.** The exact
  tailnet-only full-motion Viewer page may be handed to the user so they can
  inspect the complete P20 assembly, provided it is explicitly described as a
  collision-revealing preview candidate and not as an accepted final design.
- **Product/final-design acceptance: FAIL.** The Blue rod passes through the
  XT60 body at OPEN and MID. This is a topology error in the frozen 2D profile
  when realized as the complete solid assembly.
- **Manufacturing, mesh, slicing and printing acceptance: FAIL / NOT
  AUTHORIZED.** The XT60 collision and two below-threshold plate webs remain;
  cap height and plate-gap optimization also remain unapproved.

The exact review URL checked by this role is:

```text
https://mac-mini.duckbill-ionian.ts.net:8446/Users/scottchu/Projects/personal/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp20_r4_custom_profile_full_cad%2Fp20_r4_full_motion.step.py
```

It returned HTTP `200` from the tailnet endpoint. This proves page reachability
from the review environment, not the user's visual experience; user-side
loading and visibility remain the delivery-surface confirmation.

## Evidence reviewed

- Frozen `BRIEF.md` and `DESIGN.md`.
- Implementation receipt, candidate manifest, source, full-motion generator
  and parameter sidecar.
- Independent `CRITIQUE.md` and `VALIDATION.md`.
- All five exact manifest-pinned snapshots: OPEN/MID/END FRONT, exploded ISO,
  and OPEN axial stack.
- All `30/30` candidate-manifest rows independently reverified.
- Focused test rerun: `6 passed`.

## Findings

### BLOCKER — Blue rod intersects the XT60 body

The actual-solid evidence reports Blue/XT60 positive intersection volume of
`186.980487 mm3` at OPEN and `63.593308 mm3` at MID, clearing only at END.
This is not intended bending contact: the steel rod occupies the connector
body. The exploded snapshot visibly corroborates the bad relationship. The
profile cannot be called a final design until the Blue/XT60 topology is
repaired and the complete motion is revalidated.

### BLOCKER — plate webs fail the prototype design threshold

- fixed-axle hex to inner rim web: `1.152 mm` versus the existing `2.20 mm`
  threshold;
- left outer Blue-Orange rail web: `1.715 mm`, previously authorized only as
  temporary coupon/test interest, not whole-product acceptance.

These do not prevent showing the geometry, but they prohibit manufacturing.

### MAJOR — workpiece contacts require a functional disposition

The candidate also reports Blue/workpiece overlap of
`27.847560/32.469756/0.0 mm3`, constant Green/workpiece overlap of
`1.558785 mm3`, and Orange/workpiece overlap of `0.294329 mm3` at END. Some
contact is necessary to bend the wires, but current solid-overlap evidence
does not distinguish controlled deformation from trapping. This must be
resolved before product acceptance.

### MAJOR — ordinary FRONT views are too occluded for sole approval

The right outer plate hides the inner plates, XT60 relationship and most of
the fixed axle in the OPEN/MID/END snapshots. The user should use the Viewer
part tree to hide the right outer plate and inspect the exploded artifact in
parallel. The exploded and axial views are necessary evidence, not optional
illustrations.

### MODERATE — cap/plate-gap requirement remains an inspection question

The candidate deliberately preserves the prior `9.05 mm` cap length,
`8.70 mm` engagement, `18.40 mm` inner clear span and `0.30 mm` cap-to-outer
gap. The axial snapshot exposes these dimensions honestly, but this does not
establish that the caps are short enough or that the XT60 has adequate usable
space. User inspection is required; any shortening or stack widening is a
separate constrained change with retention evidence.

## Contract coverage

- The assembly is the complete 18-occurrence P20 candidate, not the coupon:
  four plates, three rods, six caps, fixed stepped axle, two keepers, XT60 and
  the exact P20 R3 90-degree two-conductor workpiece.
- Frame and motion are correct: `X` stack axis, FRONT `YZ`, outer plates rotate
  `+45/-45 degrees` about `C=(0,0)`, inner plates and axle remain world-fixed at
  `A=(-10,-10)`.
- Both outer plates contain all three complete inverse rod rails and the fixed
  axle rail. Both inner plates contain Blue/Orange rails and the correct Green
  round bore.
- The exact 361-point path authority passes inverse reconstruction; the
  practical 33-point BREP rail deviation is at most `0.003066 mm`.
- All five written STEP artifacts have 18 valid positive-volume occurrences,
  correct distinct left/right-inner identities and source/STEP parity.
- Static rod/plate, axle/outer and cap/plate positive-volume intersections are
  zero at OPEN/MID/END; minimum cap-to-outer axial clearance is `0.30 mm`.

## Required user-facing handoff wording

Hand over the exact full-motion Viewer and the exploded/axial snapshots as
the **complete P20 geometry for intent verification**. State plainly that it
has found blockers and ask the user to confirm or reject:

1. the Blue rod versus XT60 relationship;
2. orientation and all rail ownership;
3. cap height and the `18.40 mm` inner clear span;
4. the fixed axle position and invariant `+45/-45 degree` rail motion.

Do not call the candidate final, verified for manufacture, printable or
physically accepted. Do not generate mesh, slice, upload or print from this
fingerprint. The smallest next repair is the Blue/XT60 topology only; rail-web
and cap/stack changes must remain separate follow-on gates.
