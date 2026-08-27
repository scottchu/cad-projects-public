# P20 R2 task DAG

Frozen input: `DESIGN_INPUT_MANIFEST.sha256`. At most three workers may be
active. One writer owns each source/artifact namespace. Every task verifies
the declared fingerprint and returns status, changed paths, commands/results,
hashes, requirement coverage, risks, and next action. Initial work plus at
most two focused repair cycles is the shared retry ceiling.

## P20R2-DESIGN-01 — curved fixed-axle rail design (complete: PASS)

- Owner: distinct mechanism designer; strong/high reasoning.
- Dependency: exact design-input manifest.
- Objective: verify `A=(-15,-11)` under the corrected `C=(0,0)` kinematics;
  derive both curved inverse-frame loci and rail cutter construction; produce
  the required FRONT-YZ/axial 2D gate and analytic checks.
- Exclusive writes: `DESIGN.md`, `DESIGN_CANDIDATE.sha256`, and design-gate
  media under `docs/review/p20-r2-fixed-rod-arc-rail/`.
- Forbidden: source, tests, BREP, STEP, continuity indexes, white-rod outer
  rails/holes, or changing `C` to `A`.
- Done: one exact PASS candidate or bounded blocker; exact equations,
  dimensions/tolerances, object/rail census, web/containment, known collision
  boundary, visible 2D gate, and unresolved physical risks.
- Stop: any cheap-gate failure or need to reopen a frozen object.

Receipt: focused visual-gate repair candidate file SHA-256
`c3aaa10589408db6d24fcde9b46ed89f8cbd95e41764c4a4db0672cbd3fd2c30`,
verified `5/5`. Independent focused recheck SHA-256
`f737c6c075c726500ae7c251c4dcef84c6726b2b5700dae46939e7778cebcb3b`
closed the original media-traceability blocker and passed the exact repaired
analytic candidate. The original blocked critique remains immutable history.

## P20R2-IMPL-01 — source-first correction

- Owner: CAD implementer distinct from designer/review roles; strong/high.
- Dependency: accepted design candidate above and exact
  `IMPLEMENTATION_INPUT_MANIFEST.sha256`, aggregate SHA-256
  `acec208df5f1de3abcc9b245c51c6161f099363517f92616852c146677fcfb26`,
  verified `36/36`.
- Objective: implement only the delta mask in new P20 R2 source/tests/artifact
  namespaces, extracting one pure transform used by both rail generators.
- Exclusive writes: P20 R2 source, focused tests, STEP generators/outputs,
  snapshots, implementation receipt, and candidate manifest.
- Forbidden: P19/P20 R1 edits, white-rod outer rails or substitute apertures,
  rotation about `A`, collision suppression, mesh/3MF/slicing/printing.
- Done: analytic tests first; exact rail census; stationary-axle
  reconstruction; physical left/right `+45/-45 deg` about `C`; actual-solid collision map; web/constraints;
  valid STEP and source/export parity; visibly reviewable curved rails.
- Stop: failed analytic gate, unexpected collision, stale provenance, or scope
  reopening.

Implementation authority is invalidated by any mismatch or mutation of any
implementation-manifest entry. Such a change also invalidates all downstream
candidate, critic, validator, and formal-review gates; it does not authorize
the implementer to reinterpret or repair the design contract.

## P20R2-CRIT-01 — independent mechanism critique

- Owner: independent critic, distinct from designer/implementer/validator.
- Dependency: exact frozen implementation candidate.
- Exclusive write: `CRITIQUE.md`.
- Objective: challenge fixed `C`, true curved-rail presence and completeness,
  absence of all white-rod outer apertures, visibility, web, collision truth,
  service preservation, and non-product labeling.
- Done: severity findings, requirement map, exact fingerprint, PASS/BLOCK.
- Stop: fingerprint mismatch or any source/artifact mutation.

## P20R2-VAL-01 — independent digital validation

- Owner: independent validator, distinct from all prior roles.
- Dependency: same frozen candidate as critic; may run in parallel with critic.
- Exclusive write: `VALIDATION.md`.
- Objective: independently execute math, inverse reconstruction, boundary and
  sampled states, occurrence/rail census, actual-solid collision, web,
  STEP/parity, and original-resolution visual gates.
- Done: exact commands/results/hashes, limiting measurements, named expected
  and unexpected collisions, visual observations, PASS/FAIL.
- Stop: provenance mismatch or failed cheap gate; no repairs.

## P20R2-REVIEW-01 — formal join

- Owner: independent formal reviewer, distinct from every preceding role.
- Dependencies: matching candidate, critique, and validation receipts with all
  material findings dispositioned.
- Exclusive write: `REVIEW.md`.
- Objective: audit contract, independence, provenance, evidence sufficiency,
  visible rail proof, and STOP/non-product boundaries.
- Done: ACCEPT/BLOCK for exact digital intermediate only, remaining physical
  unknowns, explicit no-next-rail STOP.
- Stop: candidate mutation, missing receipt, or product/print acceptance claim.

```text
DESIGN_INPUT -> DESIGN -> user-confirmable gate -> IMPLEMENTATION_INPUT
             -> IMPLEMENTATION_CANDIDATE
                   /                 \
                CRITIC            VALIDATOR
                   \                 /
                    FORMAL REVIEW -> STOP
```

No later white-rod outer rail is selected here. Each future rail requires its
own one-factor contract and must be checked against its inner rail path and
every already-present neighboring outer rail before another rail begins.
