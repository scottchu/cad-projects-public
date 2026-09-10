# P20 R4 independent mechanical critique

Date: `2026-08-27`

Task: `P20R4-CRIT-01`

Owner/role: `/root/p20_final_critic`, independent critic. This role did not
implement or repair the candidate.

Status: **CONDITIONAL PASS FOR USER INTENT PREVIEW ONLY; REJECTED AS A FINAL
PRODUCT OR MANUFACTURING CANDIDATE**

## Candidate and evidence reviewed

- Candidate-manifest SHA-256:
  `e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`.
- All `30/30` manifest rows verified against the current filesystem.
- Read the frozen `BRIEF.md`, `DESIGN.md`, `IMPLEMENTATION.md`, task DAG,
  implementation source, focused tests, full-motion sidecar, five written STEP
  files, and all five required review images.
- Independently reran the focused test file: `5 passed`.
- Independently imported every written STEP with build123d. Each is a valid
  `Compound` with `18` leaf occurrences. OPEN/MID/END and full-motion each
  preserve the expected four plate bodies, three rods, six caps, fixed axle,
  two keepers, XT60 reference, and 90-degree two-conductor workpiece.

## Severity-ranked findings

### BLOCKER — Blue rod passes through the XT60 solid envelope

The actual-solid result in the implementation receipt reports Blue/XT60
intersection volumes of `186.980487 mm3` at OPEN and `63.593308 mm3` at MID,
clearing only at END. This is not a small clearance warning or intended
rod/wire contact: a stainless rod occupies the connector body. The accepted 2D
profile therefore does not yet produce a physically coherent whole assembly.

This blocks calling the artifact a final design, blocks mesh/slicing/printing,
and must be shown to the user rather than hidden behind a solid outer plate.

### BLOCKER — two already-known strength margins remain below the prototype rule

- fixed-axle hex to inner rim web: `1.152 mm` versus the existing `2.20 mm`
  design threshold;
- left outer Blue–Orange rail web: `1.715 mm`, allowed only as temporary
  coupon/test interest and never accepted for the whole product.

These are accurately preserved and disclosed, but they remain product and
manufacturing blockers.

### MAJOR — rod/workpiece intersections are not classified tightly enough

The BREP probe also reports rod/workpiece intersections: Blue
`27.847560/32.469756/0.0 mm3`, Green `1.558785 mm3` in all three states, and
Orange `0.294329 mm3` at END. Some contact is required to bend conductors, but
the evidence does not distinguish desired line contact/compression from an
impossible solid overlap or conductor trapping. Before manufacturing, each
contact needs an explicit functional disposition and conductor
deformation/clearance model.

### MAJOR — the normal assembled FRONT snapshots hide the evidence the user most needs

OPEN/MID/END FRONT views are dominated by the opaque right outer plate. They
show that the outer cuts and caps exist, but they hide the inner plates, most
of the fixed stepped axle, XT60/wire relationship, and the Blue/XT60 collision.
The exploded and axial-stack images recover part/cap/stack visibility, but an
assembled cutaway, transparent-plate view, or explicit Viewer visibility
instructions are needed for an honest topology check.

### MODERATE — cap/plate stack is visible but intentionally not optimized

The candidate honestly retains six `9.05 mm` caps, `8.70 mm` engagement,
`18.40 mm` inner clear span, and only `0.30 mm` cap-to-outer axial clearance.
The axial snapshot exposes the stack. The caps sit outside the outer plates, so
their visible head length is not itself inside the XT60 clear span; the current
rod/cap engagement and plate positions define that span. However, this does
not satisfy the later desire to maximize the plate gap—it only preserves the
unmodified baseline for visual review. The `0.30 mm` running gap also deserves
a tolerance/print-fit decision before production.

## Contract coverage

- **Orientation/topology:** correct frame is implemented: assembly axis `X`,
  FRONT `YZ`, `+Z` connector head/up, `+Y` wire tail/right. Left/right outer
  motion signs are `+45/-45 degrees` about `C=(0,0)`.
- **Fixed rod invariance:** the stepped axle stays world-fixed at
  `A=(-10,-10)`; only its inverse guide cuts rotate with the outer plates.
- **Rail ownership:** both outer plates contain all three complete inverse
  white-rod paths plus the fixed-axle arc. Both inner plates contain complete
  Blue/Orange paths and a Green round bore, consistent with Green inner travel
  of zero.
- **Full census:** the physical solids are complete: four plates, three rods,
  six caps, one fixed stepped axle, two keepers, XT60, and the exact P20 R3
  90-degree workpiece. It is not a coupon substitution. The focused repair is
  verified across all five written STEP files: each now has distinct left- and
  right-inner identities (`fixed_left_inner`/`fixed_right_inner`, with matching
  full-motion names).
- **Motion math:** the single 361-point authority and inverse transforms are
  coherent; the 33-point BREP approximation is reported within `0.003067 mm`.
- **Visual evidence:** exploded and axial views are useful. Assembled FRONT
  evidence is too occluded to stand alone.

## Critic disposition

This fingerprint is acceptable to hand to the user **only as a clearly
labeled, collision-revealing full-assembly intent preview**. It is useful for
the user's requested final-design verification because it contains the whole
jig and exposes the exact reason the current profile cannot yet be final.

It must not be described as a verified final design. The user should be asked
to inspect the full assembly and specifically confirm/reject the XT60/Blue-rod
relationship, orientation, rail topology, cap height and plate gap. No mesh,
slicing or print work should continue from this fingerprint.

Smallest next design action after user review: resolve the Blue rod versus
XT60 body topology first, then re-evaluate the rod/workpiece contacts and the
`1.152/1.715 mm` webs. Do not optimize caps or delete rails in the same repair.
