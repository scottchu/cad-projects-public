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

The records above remain immutable blocked product-gate evidence. The user has
since authorized a new non-candidate sequential scaffold contract in
`SCAFFOLD_BRIEF.md`; that clarification does not rewrite either result.

## P20-SCAFFOLD-IMPL-01 — evidence-only scaffold implementation (complete)

- Owner identity: `/root/p20_scaffold_implementer`, distinct from critic,
  validator, and formal reviewer.
- Role/model: CAD implementer; strong/high reasoning.
- Dependencies: exact `SCAFFOLD_INPUT_MANIFEST.sha256` and no other design
  interpretation.
- Objective: implement only the scaffold delta mask: zero outer rod rails and
  zero substitute apertures, axle at `A=(-15,-11)`, centered constant axle
  guides, and shared `-45/+45 deg` outer motion. Preserve and explicitly
  report the known rod/solid-outer-plate collisions.
- Allowed reads: scaffold manifest inputs and exact P19 source/test/artifacts.
- Exclusive writes: new P20 scaffold source, focused tests, explicit scaffold
  STEP/sidecar/snapshots, implementation receipt, and immutable scaffold
  candidate manifest.
- Forbidden: P19 mutation, clearance holes/windows, adding back any rod rail,
  changing frozen geometry, hiding/zeroing expected collisions, 3MF, slicing,
  printing, or product/physical acceptance language.
- Done gate: pure transform tests; exact required-absence census; actual-solid
  collision report with all six expected pairs named; no other unintended
  collision; source/export parity; visibly labeled scaffold snapshots; exact
  immutable fingerprint for independent gates.
- Ceiling/stop: one implementation plus at most two focused corrections.
  Immediately stop on scope reopening, any substitute rod aperture, any
  unexpected collision, or inability to label the result non-candidate.

Receipt: replacement candidate SHA-256
`59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`,
verified `20/20`; P20 `8/8`, combined regression `16/16`. One focused repair
resolved `SC-01/02/03` without adding a rail or aperture.

## P20-SCAFFOLD-CRIT-01 — independent scaffold critique (complete: PASS)

- Owner identity: `/root/p20_scaffold_critic`, distinct from
  implementer/validator/reviewer.
- Role/model: independent scope/mechanism critic; strong/high reasoning.
- Dependencies: exact frozen scaffold candidate fingerprint.
- Objective: challenge contract fidelity, especially the absence of all outer
  rod apertures, truthful collision disclosure, centered-equivalent guide,
  `90 deg` relative travel, and non-candidate labeling.
- Exclusive write: future `SCAFFOLD_CRITIQUE.md` only.
- Forbidden: design/source/test/artifact edits or proposing future rail order.
- Done gate: verified fingerprint, severity findings, exact scope coverage,
  collision-label audit, and PASS/BLOCK for scaffold conformance only.
- Stop: fingerprint mismatch, hidden clearance feature, or any product claim.

Receipt: initial critique SHA-256 `994f38fb...d203` blocked the first candidate;
focused-repair recheck SHA-256
`6531dea20ed5d4d744259f5c6a4c8896d2c0ec929ff47395a5757f0282d10819`
passes the replacement candidate.

## P20-SCAFFOLD-VAL-01 — independent scaffold validation (complete: PASS)

- Owner identity: `/root/p20_scaffold_validator`, distinct from
  implementer/critic/reviewer.
- Role/model: independent CAD/test validator; strong/high reasoning.
- Dependencies: the same frozen fingerprint as P20-SCAFFOLD-CRIT-01; may run
  in parallel because both are read-only.
- Objective: independently run transform, state, occurrence, absence,
  actual-solid collision, STEP validation/parity, and snapshot gates.
- Exclusive write: future `SCAFFOLD_VALIDATION.md` only.
- Forbidden: repair, source/test/artifact edits, collision suppression, or
  candidate/product acceptance.
- Done gate: exact commands/hashes, six expected pair results individually
  reported, unexpected-collision census, parity, visual observations, and
  PASS/FAIL for the evidence-only scaffold.
- Stop: provenance mismatch or any result outside the exact expected-collision
  class.

Receipt: replacement-candidate recheck SHA-256
`73312ac348745ce6a1a513283e752094bc826f1effcda028961f43d3b23a10b0`,
verdict `PASS`. The earlier validation is preserved as stale history for the
superseded first candidate.

## P20-SCAFFOLD-REVIEW-01 — formal scaffold review join (complete: ACCEPT)

- Owner identity: `/root/p20_scaffold_reviewer`, distinct from every prior
  role.
- Role/model: formal independent reviewer; strong/high reasoning.
- Dependencies: matching-fingerprint scaffold implementation, critique, and
  validation receipts with all findings dispositioned.
- Objective: decide only whether the evidence scaffold conforms to the frozen
  clarification and preserves truthful provenance/labels.
- Exclusive write: future `SCAFFOLD_REVIEW.md` only.
- Forbidden: product/CAD/print/physical acceptance, design changes, clearance
  features, rail sequencing, or acting as another role.
- Done gate: ACCEPT/BLOCK for scaffold conformance, exact non-candidate label,
  known collisions, remaining risks, and explicit STOP boundary.
- Stop: any candidate mutation, missing independent receipt, unresolved
  material finding, or acceptance wording beyond scaffold conformance.

Receipt: `SCAFFOLD_REVIEW.md`, SHA-256
`3f57e45432591b13ed7fcc71011185534c18107f099ac251b93c5dc6ee131130`;
`ACCEPT` for scaffold conformance only, followed by mandatory `STOP`.

## Active scaffold dependency order

```text
SCAFFOLD_INPUT_MANIFEST --> P20-SCAFFOLD-IMPL-01
                                      |
                         frozen scaffold fingerprint
                              /               \
              P20-SCAFFOLD-CRIT-01   P20-SCAFFOLD-VAL-01
                              \               /
                         P20-SCAFFOLD-REVIEW-01 --> STOP
```

The previously planned product-candidate implementation and review tasks
below are superseded and must not be dispatched for this scaffold.

No future rod order is selected here. After this scaffold reaches its formal
STOP, a separately authorized iteration may add exactly one named outer rail,
validate it against its corresponding inner path and all already-present
neighboring outer rails, and freeze it before another rail begins. A failure
must roll back only that attempted rail. Simultaneous multi-rail work is
forbidden because it obscures inner/outer path coupling and neighboring-rail
spacing, overlap, web, and collision effects.

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
