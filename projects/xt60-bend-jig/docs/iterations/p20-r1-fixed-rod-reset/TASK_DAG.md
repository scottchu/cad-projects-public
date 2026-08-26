# P20 R1 task DAG

Frozen orchestration input: `DESIGN_INPUT_MANIFEST.sha256`. Every runtime
owner must verify its declared fingerprint before work. At most three workers
may be active; there is one writer for the P20 source/test/artifact namespace.
An initial attempt plus at most two focused repair cycles is the shared retry
ceiling. Any contract or candidate change invalidates only downstream gates
whose manifest includes it.

## P20-DESIGN-01 — fixed-rod reference kinematics (complete: BLOCKED)

- Owner identity: `/root/p20_mechanism_design`.
- Role/model: mechanism designer; strong/high reasoning.
- Dependencies: this exact design-input manifest and user-confirmed intent.
- Objective: derive the minimum feasible farther-lower-left fixed-axle datum
  and a single pure-math law for the two centered-equivalent side-local axle
  guides under exact `-45/+45 deg` travel, with all frozen P19 geometry and
  required rail absence/presence represented.
- Allowed reads: declared manifest paths and read-only P19 CAD artifacts needed
  to measure the exact baseline.
- Exclusive writes: this iteration's future `DESIGN.md` and its phone-readable
  FRONT-YZ design-gate media only.
- Forbidden: P20/P19 source, tests, STEP, continuity indexes, mesh, 3MF,
  slicing, printing, or acceptance claims.
- Done gate: one exact candidate or bounded infeasibility proof; numeric
  datums/transforms; object/rail census; OPEN/mid/END diagram; analytic
  topology, closure, collision, web, service, and centered-equivalence checks;
  unresolved physical risks; user confirmation request.
- Ceiling/stop: one concise candidate comparison and one recommended gate;
  checkpoint before any expanded search. Stop immediately on a failed cheap
  invariant or need to change a frozen object.

Receipt: `DESIGN.md` and `DESIGN_CANDIDATE.sha256`; candidate-manifest
SHA-256
`fd00b98112ddcd83eb4cb5bcecf384b93fa34764e4b09cfe7e9653ac3acddc89`.
The task stopped before implementation after proving six unavoidable OPEN
rod/solid-outer-plate collisions.

## P20-CRITIC-01 — independent analytic design critique (complete: BLOCKED)

- Owner identity: `/root/p20_design_critic`, distinct from the designer.
- Role: independent mechanism/topology critic.
- Dependency: exact P20-DESIGN-01 candidate fingerprint above.
- Exclusive write: `DESIGN_CRITIQUE.md` only.
- Result: verified `4/4` candidate entries and `14/14` nested input entries;
  independently reproduced the centered-equivalence math, `-45/+45 deg`
  motion, conservative clearance checks, and six OPEN collisions totaling
  `241.274316 mm3`.
- Receipt SHA-256:
  `fe5762cef497214c4da7291fc89e7f05ebcb0789f61c8912580110680860abfc`.
- Disposition: PASS the designer's BLOCKED conclusion; FAIL the frozen
  contract as an implementation candidate. Await explicit user topology
  choice.

## P20-IMPL-01 — source-first implementation

- Owner identity: unassigned; must be distinct from design, critic, validator,
  and formal reviewer.
- Role/model: CAD implementer; strong/high reasoning because the change affects
  mechanism constraint and actual-solid motion.
- Dependencies: user-confirmed P20-DESIGN-01 contract and a new immutable
  implementation-input manifest.
- Objective: implement only the accepted delta masks, extract the shared pure
  transform, add focused regressions, generate explicit P20 STEP targets, and
  freeze one candidate fingerprint.
- Allowed reads: frozen design/implementation manifests and authoritative P19
  source/tests/artifacts.
- Exclusive writes: new P20 source, focused P20 tests, P20 CAD/STEP/sidecar
  namespace, implementation receipt, and candidate manifest.
- Forbidden: editing P19/P18/P17 history, redesign, self-approval, 3MF,
  slicing, printing, new lock/parts, or physical claims.
- Done gate: pure-math tests first; required absence/presence census; core
  evidence categories; full-motion/service checks; valid written STEP;
  source/export parity; deterministic snapshots; immutable candidate ready for
  independent review.
- Ceiling/stop: one implementation plus at most two critic/validator-directed
  focused repairs. Stop before BREP if the analytic gate fails, and stop on any
  required scope reopening.

## P20-CRIT-01 — independent mechanism critique

- Owner identity: unassigned; must differ from design and implementation.
- Role/model: independent mechanical/intent critic; strong/high reasoning.
- Dependencies: exact frozen P20 implementation candidate fingerprint.
- Objective: challenge whether removing all six outer rod rails actually
  resolves the reported overlap while preserving support, constraint closure,
  usability, service, plate integrity, centered-equivalent guide behavior, and
  `90 deg` relative motion.
- Allowed reads: frozen candidate source/tests/artifacts, exact snapshots, and
  declared requirement/evidence records.
- Exclusive write: this iteration's future `CRITIQUE.md` only.
- Forbidden: source/test/artifact/design edits, validation execution ownership,
  or acceptance.
- Done gate: severity-ranked findings, requirement coverage, exact fingerprint,
  falsifiable repair requests, unresolved physical risks, and PASS/BLOCK
  recommendation for the formal join.
- Ceiling/stop: one bounded report; no speculative redesign. Stop if fingerprint
  mismatch or stale artifacts are detected.

## P20-VAL-01 — independent digital validation

- Owner identity: unassigned; must differ from design, implementation, critic,
  and formal reviewer.
- Role/model: independent CAD/test validator; strong/high reasoning.
- Dependencies: same exact candidate fingerprint as P20-CRIT-01; may run in
  parallel with that read-only task.
- Objective: independently execute focused math, constraint, actual-solid,
  motion/service, required presence/absence, STEP validation, source/export
  parity, and snapshot-inspection gates.
- Allowed reads: candidate fingerprint and declared source/tests/artifacts.
- Exclusive write: this iteration's future `VALIDATION.md` only.
- Forbidden: source/test/artifact/design edits, repair, or acceptance beyond a
  PASS/FAIL validation verdict.
- Done gate: exact commands/results, verified hashes, requirement mapping,
  limiting measurements and named collisions/clearances, artifact census,
  visual observations, unresolved risks, and PASS/FAIL.
- Ceiling/stop: one deterministic run plus focused rerun only after a new
  fingerprint. Stop on provenance mismatch or any cheap-gate failure.

## P20-REVIEW-01 — formal independent review join

- Owner identity: unassigned; must differ from every preceding role.
- Role/model: formal independent reviewer; strong/high reasoning.
- Dependencies: matching-fingerprint P20-CRIT-01 and P20-VAL-01 receipts and
  dispositions for every material finding.
- Objective: audit scope, baseline, traceability, role independence, candidate
  provenance, evidence sufficiency, and whether findings were resolved without
  violating the frozen contract.
- Allowed reads: immutable candidate, critic/validator reports, receipts, and
  concise continuity records.
- Exclusive write: this iteration's future `REVIEW.md` only.
- Forbidden: design/source/test/artifact edits, acting as implementer, or
  promoting CAD evidence to physical/print acceptance.
- Done gate: ACCEPT/BLOCK for the exact candidate, acceptance layers stated
  separately, remaining risks, and next bounded action.
- Ceiling/stop: one join review. Any candidate mutation or missing independent
  receipt blocks review and routes the smallest correction through the root.

## Dependency order

```text
P20-DESIGN-01 -- user confirms exact 2D gate --> P20-IMPL-01
                                                   |
                                  frozen candidate fingerprint
                                      /            \
                             P20-CRIT-01       P20-VAL-01
                                      \            /
                                       P20-REVIEW-01
```
