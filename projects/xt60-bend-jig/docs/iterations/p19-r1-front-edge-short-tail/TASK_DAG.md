# P19 R1 task DAG

## P19-DESIGN-01 — front-edge 2D kinematics

- Owner: `/root/p19_kinematic_solver` (second bounded replacement after both
  earlier owners exceeded their checkpoint without a reviewable deliverable).
- Role: mechanism designer.
- Dependencies: frozen task input and P18 baseline manifest.
- Objective: produce a parametric 2D design with the complete three-rod
  triangle translated to the upper-right/front boundary, minimal inner/world
  paths, deterministically derived opposite outer rails, explicit fixed axle,
  plate/web checks, and short-tail solder-service corridor.
- Exclusive writes: this iteration's `DESIGN.md` and
  `docs/review/p19-r1-front-edge-short-tail/design-*`.
- Forbidden: P18/P19 source CAD, tests, STEP, continuity indexes, or 3MF.
- Done gate: one feasible recommended candidate, exact parameters, rendered
  OPEN/END/sweep 2D evidence, and stated unresolved risks. Further variants are
  deferred until this candidate is user-reviewed.

## P19-CRIT-01 — independent service/kinematic critique

- Owner: `/root/p17_optimizer_math_audit`
- Role: independent critic.
- Dependencies: frozen task input and P18 evidence; may critique the design
  candidate after it appears but must not edit it.
- Objective: identify whether the proposed front-edge placement truly gives a
  short-tail solder corridor and whether shortened/curved paths preserve
  topology, identity, support, force direction, boundary web, and deterministic
  outer-rail derivation.
- Exclusive write: this iteration's `SERVICE_CRITIQUE.md`.
- Forbidden: design, source CAD, tests, STEP, or review acceptance.

## P19-IMPL-01 — parametric 3D implementation

- Owner: to be assigned after user accepts the 2D gate.
- Dependencies: frozen accepted `DESIGN.md` plus critique disposition.
- Objective: implement source-first P19 CAD and explicit STEP targets without
  changing the accepted 2D parameters.

## P19-OPT-02 — minimum-travel parametric re-optimization

- Owner: `/root/p19_min_rail_optimizer`.
- Role: mechanism/optimizer designer, distinct from prior critic and
  validator.
- Dependencies: `REOPTIMIZE_INPUT.sha256` and the user's explicit option-2
  decision in `TASK_INPUT.md`.
- Objective: produce one replacement 2D candidate in the same P19 R1 design
  space with every outer rod rail centre travel `>=2.00 mm`, without manual
  rail extension or regression of topology, service keepout, plate envelope,
  web, axle support, identity or deterministic inverse derivation.
- Exclusive writes: `REOPTIMIZED_DESIGN.md` and
  `docs/review/p19-r1-front-edge-short-tail/reoptimized-*`.
- Forbidden: P18/P19 CAD source, tests, STEP, continuity indexes, 3MF, slicing
  or physical-acceptance claims.
- Done gate: deterministic search/derivation, one feasible recommended
  candidate, all six rail lengths, explicit comparison to repair 1, 2D
  OPEN/END/service/rail PNG, and a complete requirement table.

## P19-CRIT-02 — independent re-optimized 2D critique

- Owner: `/root/p17_optimizer_math_audit`.
- Role: independent critic who did not create the candidate.
- Dependencies: exact re-optimized candidate fingerprint.
- Objective: accept or block user review by reproducing the minimum-travel,
  topology, service, web, force-direction, closure and parametric-rail gates.
- Exclusive write: `REOPTIMIZED_CRITIQUE.md`.
- Forbidden: redesign, CAD source/tests/STEP or acceptance beyond the 2D gate.

## P19-RAIL-01 — isolated short-outer-rail diagnostic

- Owner: `/root/p18_validator`.
- Role: independent kinematic/math validator.
- Dependencies: repaired P19 `DESIGN.md`, `SERVICE_CRITIQUE.md`, and the exact
  fingerprinted 2D PNG; no 3D candidate is required.
- Objective: isolate the left/bottom and right/upright short outer rails and
  quantify centre travel, chord, sagitta, clearance-to-travel ratio, endpoint
  tangents/crossing angles, local constraint contribution and sensitivity to
  PETG/rod clearance. State whether each short rail is mathematically valid,
  marginal, or functionally indistinguishable from a round clearance hole.
- Exclusive write: this iteration's `RAIL_LENGTH_ANALYSIS.md`.
- Forbidden: design changes, CAD source/tests/STEP, continuity or release
  acceptance.
- Done gate: deterministic calculations from the frozen rail law, comparison
  against at least the middle/long outer rail on each side, and a falsifiable
  recommendation without silently changing parameters.

## P19-VAL-01 / P19-REVIEW-01

- Owners: distinct validator and formal reviewer, assigned only after a frozen
  implementation fingerprint exists.
- Objective: independently validate math, constraints, collisions, service
  path, actual solids, exports and visual evidence, then accept or reject the
  exact candidate. Physical force/fit/heat acceptance remains separate.

## P19-OPT-03 — four-millimetre minimum-travel re-optimization

- Owner: `/root/p19_min_rail_optimizer` continuing its bounded design role.
- Role: mechanism/optimizer designer.
- Dependencies: exact `REOPTIMIZE_4MM_INPUT.sha256` and the cycle-3 decision
  in `TASK_INPUT.md`.
- Objective: solve one replacement P19 2D candidate with all six physical
  inverse outer rod rails at least `4.00 mm` centre travel and complete
  capsule aspect proxy at least `1.963855`, while preserving the cycle-3
  delta mask.
- Exclusive writes: `REOPTIMIZED_4MM_DESIGN.md` and
  `docs/review/p19-r1-front-edge-short-tail/reoptimized-4mm-*`.
- Forbidden: edits to older evidence, CAD source/tests/STEP, continuity
  indexes, 3MF, slicing, manual rail extension or physical claims.
- Done gate: deterministic bounded search; one feasible candidate or exact
  infeasibility proof; all six arc/chord/aspect values; full topology,
  service, web, crossing and conditioning evidence; phone PNG; comparison to
  the superseded cycle-2 candidate.

## P19-CRIT-03 — independent four-millimetre 2D critique

- Owner: `/root/p17_optimizer_math_audit`.
- Role: independent critic.
- Dependencies: frozen P19-OPT-03 output fingerprint.
- Objective: independently reproduce the six `>=4.00 mm` rail gates, aspect,
  topology, identity, web, service, axle, inverse transform, crossing and
  closure evidence and accept or block user review.
- Exclusive write: `REOPTIMIZED_4MM_CRITIQUE.md`.
- Forbidden: redesign, CAD source/tests/STEP or downstream acceptance.

## P19-OPT-04 — OPEN-upright minimum reopening

- Owner: `/root/p19_min_rail_optimizer` continuing the bounded mechanism role.
- Role: mechanism/optimizer designer.
- Dependencies: the cycle-3 infeasibility proof, the user's cycle-4 decision,
  and exact `REOPTIMIZE_4MM_OPEN_UPRIGHT_INPUT.sha256`.
- Objective: vary only `OPEN_upright_Z` in addition to the previously allowed
  twist and common END translation; select the smallest downward OPEN change
  that satisfies every six-rail, OPEN-service, web, topology, conditioning and
  synchronized-motion gate.
- Exclusive writes: `REOPTIMIZED_4MM_OPEN_UPRIGHT_DESIGN.md` and matching
  `docs/review/p19-r1-front-edge-short-tail/open-upright-*` 2D evidence.
- Forbidden: CAD source/tests/STEP, older evidence, continuity indexes, plate
  enlargement, C/A movement, manual rail extension, new parts or physical
  acceptance claims.
- Done gate: one exact feasible candidate or proof of infeasibility, complete
  rail/service/web/conditioning table, and readable phone 2D gate.

## P19-CRIT-04 — independent cycle-4 2D critique

- Owner: `/root/p17_optimizer_math_audit`.
- Role: independent critic.
- Dependencies: exact P19-OPT-04 output fingerprint.
- Objective: independently reproduce the complete analytic gate and accept or
  block the exact 2D candidate for implementation.
- Exclusive write: `REOPTIMIZED_4MM_OPEN_UPRIGHT_CRITIQUE.md`.
- Forbidden: redesign, CAD source/tests/STEP or downstream acceptance.

## P19-IMPL-04 — source-first CAD implementation

- Owner: a distinct implementation agent assigned only after P19-CRIT-04
  accepts the exact candidate.
- Role: CAD implementer, not critic, validator or formal reviewer.
- Dependencies: frozen accepted cycle-4 2D fingerprint and implementation
  manifest.
- Objective: implement the exact P19 parameters in parametric source, pure
  motion/rail math and focused tests; generate explicit OPEN/END/full-motion
  STEP targets without changing the accepted 2D geometry.
- Exclusive writes: new P19 CAD source/tests/generated STEP namespace and its
  implementation receipt.
- Forbidden: redesign, P18/P17 mutation, 3MF/slicing/printing, self-lock or
  physical-fit claims.
- Done gate: source tests, exact BREP collision/web/service checks, source to
  STEP parity, mandatory snapshots and immutable candidate fingerprint ready
  for distinct validation and formal review.

## P19-REPAIR-01 — removal-service correction

- Owner: `/root/p19_cad_implementer` continuing the bounded implementation
  role; it may not approve its own repair.
- Dependencies: exact blocked implementation candidate, P19-VAL-04 report and
  `REPAIR1_INPUT.sha256`.
- Objective: rederive only the completed-pigtail rigid-removal waypoints and
  correct pairwise evidence aggregation until every finite actual solid has
  `>=0.75 mm` clearance through the complete path.
- Exclusive writes: P19 source, focused P19 tests, implementation receipt and
  replacement candidate manifest. Generated STEP may be regenerated only to
  prove unchanged geometry/parity.
- Forbidden: any product geometry, rail, OPEN/END, C/A, OD, part/topology,
  tool/cup or physical-acceptance change.
- Done gate: deterministic bounded path search, pairwise actual-solid result,
  focused tests, unchanged STEP fingerprints/parity, and a new immutable
  candidate fingerprint ready for independent revalidation.

Disposition: **superseded/infeasible under the former 0.50 mm OPEN
clearance**. The seated start itself had only 0.50 mm clearance, so a path-only
repair could not satisfy the 0.75 mm gate.

## P19-IMPL-05 — repaired 0.75 mm source-first CAD

- Owner: `/root/p19_cad_implementer`.
- Dependencies: `REPAIR2_IMPLEMENTATION_INPUT.sha256`, P19-OPT-04 repaired
  design, and independent P19-CRIT-05 acceptance.
- Result: **complete**. Exact candidate manifest
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`
  verifies 20/20 files. Focused tests pass 8/8, the repaired rigid removal path
  has minimum 0.75 mm clearance and zero intersection, and all six regenerated
  STEP artifacts pass source/export parity.

## P19-VAL-05 — independent repaired-candidate validation

- Owner: `/root/p18_validator`, distinct from the implementer.
- Result: **PASS**. `VALIDATION.md` SHA-256
  `304239aecb3b939a6ef1412d1b31979b4bafda2b2e997ca7e7311b36adfb88ef`.
- Coverage: shared motion, six rails, OPEN/END topology, web, closure,
  65-state actual solids, support, caps, axle, tool service, completed-pigtail
  removal, historical collision regression, six STEP validate/refs/diff, and
  exact snapshot review.

## P19-REVIEW-05 — formal review

- Owner: `/root/p17_optimizer_formal_review`, distinct from design,
  implementation, critique, and validation.
- Result: **ACCEPT** for CAD, six written STEP artifacts, and exact-artifact
  Viewer handoff only. `REVIEW.md` SHA-256
  `7b5436c57070547b14241bc3de6cbc7047c07cbd1e4070b036f0d8d51040aba3`.
- Physical force, fit, friction, heat, solder ergonomics, mesh/3MF, slicing,
  printing, and physical acceptance remain outside this gate.
