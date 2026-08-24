# P17 R1 counter-twist permanent-caps brief

- Iteration ID: `p17-r1-counter-twist-permanent-caps`
- Date opened: `2026-08-23`
- Repository baseline branch: `codex/xt60-p17-counter-twist`
- Repository baseline commit: `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1`
- Baseline project: `projects/xt60-bend-jig`
- Baseline supported candidate being superseded: P13 four-plate, three-rod mechanism
- Status: design contract drafted for simulator-first implementation; no CAD, STEP, 3MF, source, package, or test mutation in this design task.

## Frozen input manifest

The design task used this declared SHA-256 path-and-content list. The manifest hash is the SHA-256 of the sorted lines below as shown: `b71a2bf9aafe949618ef9a1356bce54eae1241b19c24e4e539849d99209f1293`.

| Path | SHA-256 |
|---|---|
| `PROJECT_STATE.md` | `24bc2fee0c94508704701ff257ddbbbafab3f9698161491798932d78c9ad137d` |
| `NEXT_AGENT.md` | `795077f38587d80f915d441d0caed8dba17f7de542ff5f54e343d58d5fe7b223` |
| `docs/REQUIREMENTS.md` | `e2330d2f689b116bec1f48f967156bd26f3023673d73e3b126190d4983b29209` |
| `docs/EXPERIENCE.md` | `0d41544bd2a94c9a9d230f9c606e5e311fafa413e02c7421e904e188e6a07f56` |
| `docs/decisions/ADR-0001-p13-four-plate-three-rod.md` | `93cc52a2de04033041273aefca9a1769a186d66ddc2249db1281c1f1b09f95e2` |
| `docs/iterations/p13-r2-center-hole-fit-repair/BRIEF.md` | `588ef22b8b4d6159eac38185a73b5bc626bb35497cfbbf46d37ae26badc1cb2c` |
| `src/cam-contract.js` | `a58f5057116027bab0f1678f525d61f457c1d5a85774ba0727f666979d55eca3` |
| `src/app.js` | `f9961b6b9d0a2dc27cfadb32371fb004ff499864ed4c32a216e1dfe8dce584a4` |
| `src/scene.js` | `3edc5d5166de72cf3901dd7202c6e9d590bcc6a8e6c1624bfad91fe4563388b2` |
| `index.html` | `a7aa9770d4ea5b3473f1ab43bd1007751fc2736bb5a35084f78d87b6866e1c35` |
| `package.json` | `f2cc0542c9056bf85119c3d4394d3e7e74a44676bb972d315a9c3c21e92b250e` |
| `photos/1-Photo-1.jpg` | `8604131d1b6ba3e636492a964d0c3d92811041bbf93696afefe0a8a20a976f93` |
| `photos/2-Photo-2.jpg` | `d740f4e252e0bd1636dd674480c865949c3dbde21c6c6e2522d3a4e602c362ec` |
| `photos/3-Photo-3.jpg` | `8d12c39427823ff36c4205e70716db6df1f166aab87d113b7a0a767bb7f079fe` |

Photo source paths were `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/{1-Photo-1.jpg,2-Photo-2.jpg,3-Photo-3.jpg}`.

## User outcome and use sequence

Create a simulator-first P17 architecture for an XT60 bend jig where the user grips and counter-twists two larger outer plates, while two smaller inner plates are grounded and do not rotate. Three straight purchased rods still form the wire path, but all six rod-end caps are permanent. The simulator must make the required opposite-rotation relationship, rod-end coincidence, ground/reaction path, and lock concept visible before any CAD or print artifact is generated.

Use sequence for the simulator:

1. Load the wire/workpiece envelope with the inner guide frame grounded.
2. User grips both outer plates; the primary force/actuator outer plate is visually larger.
3. A single relative twist input closes the mechanism by rotating the outer plates in opposite directions.
4. Inner fixed tracks keep each rod on its straight guide line while the complementary outer tracks drive both rod ends to the same world position.
5. At the closed pose, a visible grounded detent/hard-stop lock concept holds the relative twist in the simulator.
6. Reopen by releasing the lock and reversing the same relative twist.

## Physical observations and authority

- Six rod-end caps are permanent; no cap is removable or part of service.
- Four physical P13 caps fit on nominal rods; two were too tight to push onto the same nominal rods. This is process/fit variability and does not prove one rigid interference value.
- The two inner plates are grounded, non-rotating plates.
- The two outer plates are user-gripped rotating elements and rotate in opposite directions. P13's shared D-shaft, which keys both rotating plates to the same direction, is not retained.
- The outer plates must be larger than the inner plates. The primary force/actuator outer plate must be slightly larger and visually obvious.
- P13's prescribed `LOCKED` pose is not proof of locking. P17 must state a real reaction path and a lock concept while keeping force/self-lock proof pending.
- Verified nominal P13 facts indicate architecture failure rather than a manufacturing cut error: fixed inner clear span `26.2 mm`, XT60 body width `15.9 mm`, surplus `10.3 mm`; rods `50.0 mm`; central printed D-shaft total `45.275 mm`; principal plate stack `37.4 mm`; left cap socket `3.90 mm` on an `OD4.00 mm` rod, or `0.10 mm` diametral interference.
- Photo 3 shows the physical P13 assembly with rods protruding, caps on rod ends, and large middle spacing.

## Scope

- Document the P17 simulator architecture, exact handedness, required mechanical relationship, provisional dimensions, lock concept, ground/reaction path, risks, tests, and supersession from P13.
- Update project requirements, experience, decision index, and ADR history to preserve this architecture change.
- Initialize pending validation, review, and handoff records for later implementation and independent gates.

## Explicit non-goals

- No CAD/Python, generated STEP/3MF/STL/GLB/DXF, JS source, test, package, root config, git, or PR mutation in this design task.
- No physical acceptance claim for caps, lock force, grip force, wire holding, heat response, cycling, or springback.
- No claim that a sign-flipped animation is a mechanical counter-twist solution.
- No retention of a shared same-direction D-shaft for the two outer rotating plates.
- No new print artifact until the user reviews simulator motion.

## Requirement mapping

| ID | P17 treatment |
|---|---|
| `REQ-001` | Preserve: clamp/form only wires, not the XT60 body. |
| `REQ-002` | Preserve as intended outcome: fixed 90-degree wire path remains the target. |
| `REQ-003` | Preserve: three purchased, uncut `OD4.00 x 50.00 mm` rods. |
| `REQ-004` | Superseded for P17 by `REQ-010` and `REQ-011`: two inner fixed plates plus two counter-rotating outer plates replace P13's two fixed guides plus two synchronized same-shaft cams. |
| `REQ-005` | Superseded for P17 by `REQ-011` and `CON-009`: one relative twist input, not one shared shaft angle, drives equal scalar rod travel through complementary tracks. |
| `REQ-006` | Preserve: loading, motion, soldering, cooling, service, and removal remain required. |
| `REQ-007` | Preserve: source-derived, parametric outputs when implementation begins. |
| `REQ-008` | Superseded for P17 by `REQ-009`: all six rod-end caps are permanent; no removable right caps. |
| `REQ-009` | New: six permanent rod-end caps. |
| `REQ-010` | New: two inner plates fixed/grounded, no rotation. |
| `REQ-011` | New: two outer plates user-gripped and counter-rotating under one relative twist input; no P13 shared same-direction D-shaft. |
| `REQ-012` | New: outer plates larger than inner; primary actuator outer plate slightly larger and visually obvious. |
| `REQ-013` | New: explicit ground/reaction path and lock concept, with kinematic demonstration separated from physical force/self-lock proof. |
| `REQ-014` | New: simulator-first review before any new CAD or print artifact. |

## Mutable material task DAG

| ID | Role / owner | Deps | Immutable inputs | Exclusive writes | Done gate | Model / effort / ceilings | Status |
|---|---|---|---|---|---|---|---|
| `P17-D01` | Design / `/root/p17_design` | none | Baseline `7ca4d99...`, iteration `p17-r1-counter-twist-permanent-caps`, manifest `b71a2bf...` | This iteration's `BRIEF.md`, `DESIGN.md`, pending `VALIDATION.md`, `REVIEW.md`, `HANDOFF.md`; `docs/iterations/CURRENT`; `docs/EXPERIENCE.md`; `docs/REQUIREMENTS.md`; `ADR-0003`; `decisions/README.md` | Frozen simulator architecture, requirement mapping, ADR supersession, pending gates initialized; no implementation or approval | strong / high; one bounded design turn; concise receipt; no repair beyond doc correction; keep concurrency to this worker | complete |
| `P17-I01` | Implementation / `/root/p17_implementation` | `P17-D01` | Frozen `BRIEF.md` and `DESIGN.md`, current JS simulator files, requirements, photos | Simulator JS/CSS/HTML/tests only; implementation evidence in iteration docs | Runnable simulator encodes counter-twist kinematics, grounded inner plates, permanent caps, visual hierarchy, lock concept, and focused tests; no CAD artifacts | balanced / medium; initial attempt plus at most two focused repairs; stop on architecture ambiguity | complete |
| `P17-C01` | Critic / `/root/p17_critic` | `P17-I01` | Frozen implementation candidate fingerprint and design contract | Critic section of `REVIEW.md` only | Mechanical intent, ground path, lock concept, visual affordances, DfAM risks, and physical overclaim challenged | strong / high; read-only; one pass plus one focused follow-up | complete, no blocker |
| `P17-V01` | Validation/test / `/root/p17_validator` | `P17-I01` | Same candidate fingerprint as critic plus frozen tests and simulator source | `VALIDATION.md` and temporary validation scratch only | Focused simulator tests and browser/screenshot checks pass or fail with exact commands; no source mutation | strong / high; read-only except validation record; one validation turn plus two focused reruns | deterministic complete; browser blocked |
| `P17-R01` | Formal review / `/root/p17_formal_review` | `P17-C01`, `P17-V01` | Same candidate fingerprint plus critic and validator receipts | Formal-review section of `REVIEW.md` only | Provenance, scope, requirement traceability, findings, and dispositions joined without physical overclaim | strong / high; read-only; one join pass | conditional PR-delivery pass |
| `P17-H01` | Continuity / root orchestrator | `P17-R01` | Accepted simulator candidate and independent receipts | `PROJECT_STATE.md`, `NEXT_AGENT.md`, final `HANDOFF.md`, optional PR text | Active state/handoff updated; simulator acceptance and physical/CAD/artifact gaps explicit | root coordination; concise; no material design/implementation self-approval | complete |

### Task detail: `P17-D01`

- Owner identity and role: `/root/p17_design`, independent design owner.
- Objective and done gate: freeze a smallest falsifiable simulator architecture for counter-twist permanent-cap P17 and record the supersession from P13.
- Project / iteration / baseline: `projects/xt60-bend-jig`; `p17-r1-counter-twist-permanent-caps`; commit `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1`.
- Input manifest: `b71a2bf9aafe949618ef9a1356bce54eae1241b19c24e4e539849d99209f1293`.
- Allowed reads: entire project, repository workflow docs, CAD skill instructions, memory pointers, and the three supplied photos.
- Exclusive writes: project docs listed in the row above.
- Forbidden scope: CAD/Python, generated artifacts, JS implementation, tests, package files, root config, git, PR, physical acceptance.
- Deliverables/evidence: `BRIEF.md`, `DESIGN.md`, initialized `VALIDATION.md`/`REVIEW.md`/`HANDOFF.md`, requirement and ADR updates, exact physical observations.
- Output/retry/concurrency ceilings: one design receipt; documentation-only repair if formatting/provenance is wrong; no parallel worker spawned by this design owner.
- Stop/escalation: stop if user requirements conflict on which plates move or if simulator implementation would require immediate CAD source changes.

### Task detail: `P17-I01`

- Owner identity and role: future implementation owner, distinct from `/root/p17_design`.
- Objective and done gate: implement the simulator and tests from the frozen design without approving the result.
- Project / iteration / baseline: same project/iteration; begin from a clean read of `DESIGN.md`.
- Input manifest: recompute from frozen design files plus JS/HTML/CSS/tests before source edits.
- Allowed reads: project source/tests/docs/photos and installed Three.js/npm workspace.
- Exclusive writes: simulator source, browser surface, simulator tests, implementation evidence sections only.
- Forbidden scope: CAD/Python, STEP/3MF, release artifacts, critic/review/validation approval, PR.
- Deliverables/evidence: focused test names and browser/screenshot evidence covering all required failure modes.
- Output/retry/concurrency ceilings: initial implementation plus at most two focused repairs; stop if rod-end coincidence requires changing the design contract.
- Stop/escalation: stop if a mere visual sign flip is the only implementation path or if inner plates cannot remain fixed.

### Task detail: `P17-C01`

- Owner identity and role: future critic, independent from design/implementation/validation/review.
- Objective and done gate: challenge whether the implemented simulator meaningfully represents the mechanism and physical unknowns.
- Input manifest: frozen design and implementation candidate fingerprint.
- Allowed reads: full project candidate and photos.
- Exclusive writes: critic findings in `REVIEW.md`.
- Forbidden scope: source/test/artifact mutation, validator results, formal acceptance.
- Deliverables/evidence: severity findings for same-direction rotation, ground path, lock concept, cap wording/fit, visual hierarchy, and overclaim.
- Ceilings: one read-only pass plus one focused follow-up.
- Stop/escalation: fail closed on fingerprint mismatch or unimplemented mechanical relationship.

### Task detail: `P17-V01`

- Owner identity and role: future validator/test owner, independent from implementation/critic/review.
- Objective and done gate: run deterministic simulator tests and browser verification on the exact candidate.
- Input manifest: frozen design, implementation candidate, tests, package lock/workspace state.
- Allowed reads: project candidate and local browser/dev-server tooling.
- Exclusive writes: validation record and temporary scratch.
- Forbidden scope: source/test/artifact mutation, critic/review acceptance.
- Deliverables/evidence: commands/results for unit tests, static source checks, browser screenshot or pixel checks, and requirement trace.
- Ceilings: one validation pass plus two focused reruns after implementation repairs.
- Stop/escalation: fail closed on nonzero tests, blank/incorrect canvas, same-direction outer rotations, inner plate rotation, cap wording error, or missing lock/ground representation.

### Task detail: `P17-R01`

- Owner identity and role: future formal reviewer, independent from implementation, critic, and validator.
- Objective and done gate: join critic and validation receipts and decide whether simulator review can go to the user.
- Input manifest: exact critic and validator candidate fingerprints.
- Allowed reads: full candidate records.
- Exclusive writes: formal-review section of `REVIEW.md`.
- Forbidden scope: source/test/artifact mutation and physical/CAD acceptance.
- Deliverables/evidence: traceability and disposition audit.
- Ceilings: one read-only join pass.
- Stop/escalation: do not accept if critic or validator used different fingerprints or any blocking finding remains unresolved.

### Task detail: `P17-H01`

- Owner identity and role: root orchestrator continuity closeout.
- Objective and done gate: update durable restart files after independent review.
- Input manifest: accepted simulator candidate and independent receipts.
- Allowed reads: full project.
- Exclusive writes: `PROJECT_STATE.md`, `NEXT_AGENT.md`, final handoff updates, optional delivery text.
- Forbidden scope: adding CAD/print artifacts before user simulator review.
- Deliverables/evidence: current active iteration, acceptance boundaries, next action.
- Ceilings: concise coordination pass.
- Stop/escalation: stop if simulator is rejected or physical feedback changes requirements.
