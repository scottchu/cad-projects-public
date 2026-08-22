# P13 R2 center-hole fit repair brief

- Iteration ID: `p13-r2-center-hole-fit-repair`
- Date opened: `2026-08-22`
- Repository baseline: `b0b79253373c7cf80943e99df8ab799958c50d49`
- Baseline iteration: `p13-r1-monorepo-migration`
- Baseline authoritative source: `src/xt60_bend_jig/p13_four_plate_three_rod.py`
- Baseline source SHA-256: `e424fac8064d35713ed15748bb8a0e1f966ef429b507ba4be5a5dc31cfc7c72b`
- Integrated repository policy baseline: `a5e21e6760d383f900ee30e4457edfb13267e09d`
- Final integrated repository policy baseline:
  `1484955cc1cfa64164dbdd1ca1222be658933c8e`
- Status: digital repair complete and independently accepted for repaired
  print; physical acceptance pending reprint

## Frozen design contract

The design contract below was frozen before source implementation. The later
fast-forward from `b0b7925` to `a5e21e6` changed only repository-wide workflow
policy/templates/tests and did not overlap project source, tests, artifacts, or
this contract.

## User outcome and physical observation

Repair the latest printed P13 assembly so the user's "middle stick" fits through the responsible "center hole", while preserving the approved P13 mechanism and all unrelated fits. The latest P13 has been printed; this is a real physical assembly failure. Physical acceptance remains failed/pending after the CAD repair until the repaired parts are printed and observed.

## Intended use sequence

Identify the exact printed stick/shaft and mating printed hole from authoritative source, generated release artifacts, and assembly sequence; represent the failed fit with a focused regression; enlarge only that source-controlled hole through one meaningful parameter; regenerate affected outputs; independently validate; then hand back a Tailscale-reachable CAD Viewer link for the repaired artifact.

## Scope

- Diagnose the exact printed mating parts and feature without guessing.
- Add a focused regression for the concrete insertion/clearance failure before source repair.
- Make the smallest responsible parametric source change to only the failed hole.
- Regenerate affected STEP, 3MF, provenance, checksum, release, snapshot, and handoff artifacts from source.
- Validate actual solids, the relevant assembly/service states, source/export parity, mesh integrity, DfAM, source-defined print orientation, and focused regressions.
- Use separate design, implementation, critique, review, and validation/test agents; implementation does not approve its own work.
- Commit the completed iteration and push to `main` only after confirming the branch is safely based on current `origin/main`.

## Requirements and invariants

- Preserve `REQ-001` through `REQ-008`, `CON-001` through `CON-006`, and the approved P13 four-plate/three-purchased-rod equal-travel architecture.
- Preserve three uncut purchased `OD4.00 x 50.00 mm` stainless rods and their role-specific fit constraints.
- Preserve fixed `90 deg` outcome, open/first-contact/locked motion contract, and `wire_preload` domain.
- Preserve all source-authored print orientations and the approved print-kit object census.
- The defect repair must satisfy `CON-007`: exactly one diagnosed printed shaft/stick to printed-hole interface, with only the responsible hole clearance changed.
- Keep legacy source directories untouched and retain source as the authority for all regenerated artifacts.

## Explicit non-goals

- No P13 architecture redesign, new frame, handle, motor, electronics, or adjustable angle.
- No change to purchased rod diameter, length, or source-defined sliding rod holes unless the diagnosed failure proves that exact role is responsible.
- No blanket enlargement of rod, shaft, center, cap, or keeper bores.
- No slicer-side flip, negative Z, `Lay on face`, or generated-artifact hand editing.
- No claim of physical acceptance from CAD, mesh, slicer, or viewer evidence.

## Risks and physical unknowns

- The user-facing terms are not yet mapped to an unambiguous source feature.
- A hole-only change could reduce wall/ligament, introduce play, affect torque transfer, or touch an unintended repeated interface if the parameter is shared.
- Written outputs could retain stale geometry or transforms if regeneration/provenance is incomplete.
- Repaired printed fit, binding, actuation effort, cycling, cap retention, wire behavior, heat response, and springback remain physical unknowns.

## Planned evidence and acceptance targets

- Source/release/assembly-sequence trace that identifies both printed mating parts and the responsible hole.
- A focused failing-before/passing-after regression tied to `CON-007` and the physical defect.
- Source diff showing one meaningful hole parameter and only the intended geometry path changed.
- Core object-collision, math, constraint, and user-requirement checks plus relevant motion/service checks.
- Actual-solid validation for primary repaired STEP and relevant assemblies; before/after geometry comparison where useful.
- Regenerated production STEP/3MF/provenance/release hashes with source/export parity, mesh-manifold and orientation checks, DfAM measurement, and slicer validation if an available slicer can run.
- Mandatory deterministic snapshots reviewed after the repaired geometry is generated.
- Tailscale-reachable CAD Viewer URL confirmed to resolve the repaired artifact.
- Independent critic, review, and validation findings recorded in `REVIEW.md` and `VALIDATION.md`.

## Mutable delegated execution plan and status

| ID | Role | Deps | Immutable inputs | Exclusive write scope | Done condition | Parallel group | Model / effort / time / token ceiling | Status |
|---|---|---|---|---|---|---|---|---|
| `P13R2-D01` | design | none | baseline requirements, frozen contract, baseline source/artifacts | `DESIGN.md` only | exact mate and numeric repair contract frozen | design | strong / high / one turn / concise receipt | complete |
| `P13R2-I01` | implementation | `P13R2-D01` | frozen design contract and baseline candidate | P13 source, focused tests, generated artifacts, implementation evidence | failing-before witness, source repair, regeneration | implementation | balanced / medium / bounded implementation / two repair cycles | complete |
| `P13R2-I02` | implementation closeout | `P13R2-I01` | current generated implementation snapshot | release manifest and implementation-only evidence records | manifest hashes/status match current outputs; no source/test/geometry change | closeout | balanced / medium / one turn / concise receipt | complete |
| `P13R2-C01` | critic | `P13R2-I02` | frozen candidate fingerprint | critic section of `REVIEW.md` only | mechanical/DfAM/fit risks challenged against exact candidate | independent-a | strong / high / one turn / concise receipt | complete after affected recheck |
| `P13R2-V01` | validation/test | `P13R2-I02` | same frozen candidate fingerprint | `VALIDATION.md` and validation scratch only | prescribed deterministic, artifact, DfAM, slicer, snapshot and viewer checks recorded | independent-a | strong / high / one turn plus long tests / two focused retries | complete after one focused repair cycle; 60 passed |
| `P13R2-I03` | implementation repair | `P13R2-V01` | first frozen candidate and validator finding | one exact label expectation plus implementation-only evidence | preserve fixed-three-decimal label contract and make isolated regression pass | repair-cycle-1 | balanced / medium / one turn / one focused repair | complete |
| `P13R2-R01` | formal independent review | `P13R2-C01`, `P13R2-V01` | same candidate plus critic/validator receipts | formal-review section of `REVIEW.md` only | provenance, scope, traceability, findings and dispositions joined | independent-join | strong / high / one turn / concise acceptance receipt | complete |
| `P13R2-O01` | orchestration closeout | `P13R2-R01` | accepted receipts and exact evidence | concise continuity indexes and final handoff only | state/handoff/viewer URL/acceptance boundaries current; commit/push safety checked | closeout | root coordination / concise | complete pending delivery commit |

## Frozen candidate manifest for independent gates

- Current candidate fingerprint:
  `9f123ad24f46d60fcb89ae305455ba1a0c3b38d4738f82766ec91d02c1350db9`.
- Freeze time: after the bounded `P13R2-I03` repair and before affected-gate
  rechecks began.
- Superseded first-cycle fingerprint:
  `616b951822ed302ef71de8a3ee0752406dd1f84efb1edc99617af403bf8bc6a9`.
  `P13R2-V01` found one blocking fixed-decimal label-expectation defect on that
  candidate; `P13R2-I03` changed only
  `tests/test_p13_four_plate_three_rod.py` and recorded failing-before/passing-
  after evidence. All source geometry and written artifacts are byte-identical
  across the two candidate fingerprints.
- Manifest rule: sort by path the SHA-256 lines for the frozen-design-contract
  section of this brief; all of `DESIGN.md`; `docs/REQUIREMENTS.md`;
  `docs/EXPERIENCE.md`; the P13 source-domain amendment, parameter table,
  parameter manifest, source-domain, source certificate, and continuous
  certificates; the authoritative P13 source; `p13_geometry_case.py` and the
  three relevant P13 test modules; `scripts/export_p13_3mf.py`; the release
  manifest; both P13 provenance JSON files; and every artifact path indexed by
  the release manifest. Hash that sorted manifest text with SHA-256.
- Release-manifest SHA-256:
  `406325612e34c5c6fce95d96a2fe074591fdf502f592f172c47d016df5a54356`.
  It indexes all 24 P13 STEP files, both P13 3MFs, both snapshots, and six
  unchanged calibration artifacts; the manifest rule above additionally names
  the two P13 provenance JSON files.
- Mutable orchestration/evidence records (`BRIEF.md` outside its frozen design
  section, `VALIDATION.md`, `REVIEW.md`, `HANDOFF.md`, `PROJECT_STATE.md`, and
  `NEXT_AGENT.md`) are deliberately excluded so independent receipts can be
  appended without changing the candidate.

### Task detail: `P13R2-D01`

- Owner identity and role: `/root/design_diagnosis`, independent design agent.
- Objective and done gate: identify the exact printed mate, freeze the smallest hole-only numeric repair and regression plan.
- Project / iteration / exact baseline: `projects/xt60-bend-jig`; this iteration; `b0b79253373c7cf80943e99df8ab799958c50d49`.
- Immutable input manifest: baseline `docs/REQUIREMENTS.md`, this frozen contract, baseline authoritative source, production manifest/provenance, and assembly/service contract.
- Allowed reads: project source, tests, artifacts, requirements, experience, decisions, prior/current iterations.
- Exclusive write scope: `DESIGN.md`.
- Forbidden scope: CAD source, tests, generated artifacts, acceptance, commit/push.
- Deliverables and evidence: exact mate trace; selected `5.75 / 5.30 mm` shared cam-D-bore contract; alternatives and risk margins.
- Model / reasoning effort: strong / high.
- Time / token / output / retry / concurrency ceilings: one bounded design turn; concise receipt; no implementation retry.
- Stop or escalation conditions: stop if source/artifact/assembly evidence does not identify one interface.

### Task detail: `P13R2-I01`

- Owner identity and role: `/root/implementation`, implementation agent.
- Objective and done gate: add the focused failing regression, apply only the selected source parameters, regenerate source-derived outputs without self-approval.
- Project / iteration / exact baseline: `projects/xt60-bend-jig`; this iteration; design contract from `P13R2-D01` on `b0b7925`.
- Immutable input manifest: frozen requirements/brief/design plus baseline source, focused tests, STEP wrappers, exporter, and release paths.
- Allowed reads: project-local source/tests/docs/artifacts and installed CAD skill instructions.
- Exclusive write scope: P13 source/test/current contract, explicit P13 STEP/3MF/evidence outputs, implementation evidence.
- Forbidden scope: independent critique/review/validation acceptance, commit/push, CAD Viewer.
- Deliverables and evidence: failing-before result; passing-after focused result; regenerated 24 STEP outputs, 3MFs, evidence/provenance, snapshots.
- Model / reasoning effort: balanced / medium.
- Time / token / output / retry / concurrency ceilings: bounded implementation; initial attempt plus at most two focused repairs; concise receipt.
- Stop or escalation conditions: stop if the repair requires changing the shaft, fixed journals, rods, caps, architecture, or print orientation.

### Task detail: `P13R2-I02`

- Owner identity and role: assigned implementation-closeout agent; same bounded implementation workstream, distinct receipt.
- Objective and done gate: reconcile current implementation outputs to the release manifest and implementation evidence without changing candidate source/tests/geometry.
- Project / iteration / exact baseline: `projects/xt60-bend-jig`; this iteration; repository policy baseline `a5e21e6` with preserved dirty P13 candidate.
- Immutable input manifest: current P13 source, tests, current contract, all 24 STEP outputs, both 3MFs, evidence/provenance JSON, snapshots, and prior implementation evidence.
- Allowed reads: project-local candidate and continuity records.
- Exclusive write scope: `releases/p13-petg-test/release-manifest.json` and implementation-only sections of `VALIDATION.md`/`HANDOFF.md`.
- Forbidden scope: source, tests, STEP/3MF/JSON geometry/provenance, snapshots, independent findings, acceptance, commit/push, Viewer.
- Deliverables and evidence: current hashes/generation commands/status; truthful physical-pending boundary; explanation of any prior test-tolerance change for independent audit.
- Model / reasoning effort: balanced / medium.
- Time / token / output / retry / concurrency ceilings: one turn; concise receipt; no candidate mutation retry.
- Stop or escalation conditions: stop if any expected artifact/provenance hash is inconsistent or a candidate file would need regeneration.

### Task detail: `P13R2-C01`

- Owner identity and role: assigned independent critic; distinct from implementer, validator, and formal reviewer.
- Objective and done gate: challenge exact candidate mechanical intent, insertion/service paths, margins, DfAM, physical risks, and scope.
- Project / iteration / exact baseline: current project/iteration; candidate fingerprint recorded after `P13R2-I02`.
- Immutable input manifest: frozen requirements/brief/design, source/tests, release manifest/provenance, primary STEP/3MF, service/motion artifacts and snapshots.
- Allowed reads: full project candidate and exact validator-independent tool outputs already stored in artifacts.
- Exclusive write scope: critic provenance/findings section of `REVIEW.md`.
- Forbidden scope: source/tests/artifacts/provenance/release manifest, validation section, formal conclusion, commit/push.
- Deliverables and evidence: severity-ranked findings, requirement coverage, unresolved physical risks, candidate-fingerprint receipt.
- Model / reasoning effort: strong / high.
- Time / token / output / retry / concurrency ceilings: one read-only turn; concise receipt; at most one focused follow-up after a repair.
- Stop or escalation conditions: fail closed on fingerprint mismatch or material source/artifact inconsistency.

### Task detail: `P13R2-I03`

- Owner identity and role: `/root/implementation_repair`, bounded
  implementation repair distinct from validator and reviewers.
- Objective and done gate: correct only the validator-found label-expectation
  formatting defect while preserving the source's fixed-three-decimal naming
  contract and all candidate geometry/artifacts.
- Project / iteration / exact baseline: current project/iteration; superseded
  first-cycle fingerprint `616b9518...bc6a9`.
- Immutable input manifest: first frozen candidate plus the `P13R2-V01`
  deterministic failure receipt.
- Allowed reads: project candidate and independent validator finding.
- Exclusive write scope: the exact label assertion in
  `tests/test_p13_four_plate_three_rod.py` plus labeled implementation receipts.
- Forbidden scope: CAD source, other tests, STEP/3MF/provenance/release/snapshot,
  independent findings, acceptance, Viewer, and git.
- Deliverables and evidence: failing-before label test, exact fixed-format test
  repair, passing-after label test, focused fit regression, non-target hash guard.
- Model / reasoning effort: balanced / medium.
- Time / token / output / retry / concurrency ceilings: one turn; one focused
  edit; two isolated test commands; concise receipt.
- Stop or escalation conditions: stop if any non-test candidate input needs to
  change.

### Task detail: `P13R2-V01`

- Owner identity and role: assigned independent validation/test agent; distinct from implementer, critic, and formal reviewer.
- Objective and done gate: independently run focused/full relevant tests, actual-solid/source-export checks, CAD inspection, snapshots, DfAM, available slicer checks, and Tailscale Viewer verification.
- Project / iteration / exact baseline: current project/iteration; same candidate fingerprint as `P13R2-C01`.
- Immutable input manifest: frozen requirements/brief/design, source/tests, release manifest/provenance, all relevant written artifacts and snapshots.
- Allowed reads: candidate and installed CAD/DfAM/Viewer/slicer tools.
- Exclusive write scope: `VALIDATION.md`; temporary validation/slicer scratch outside committed release paths; Viewer process state.
- Forbidden scope: source/tests/artifacts/provenance/release manifest/snapshots, critic/formal-review findings, commit/push.
- Deliverables and evidence: exact commands/results/hashes, acceptance boundaries, working Tailscale URL, candidate-fingerprint receipt.
- Model / reasoning effort: strong / high.
- Time / token / output / retry / concurrency ceilings: one validation turn with long-running tests; initial run plus at most two focused reruns; concise receipt.
- Stop or escalation conditions: fail closed on candidate mutation, topology/parity/slicer failure, or unreachable Viewer.

### Task detail: `P13R2-R01`

- Owner identity and role: assigned formal independent reviewer; distinct from implementer, critic, and validator.
- Objective and done gate: join critic and validator receipts, audit provenance/scope/traceability/dispositions, and determine CAD/artifact advancement without physical overclaim.
- Project / iteration / exact baseline: current project/iteration; exact shared candidate fingerprint.
- Immutable input manifest: critic and validator candidate manifest plus their completed evidence records.
- Allowed reads: full candidate, `REVIEW.md`, `VALIDATION.md`, handoff/state indexes.
- Exclusive write scope: formal-review provenance/findings/conclusion in `REVIEW.md`.
- Forbidden scope: source/tests/artifacts/provenance/release manifest, validator evidence, commit/push.
- Deliverables and evidence: independent join-gate conclusion, requirement coverage, remaining risks, exact candidate receipt.
- Model / reasoning effort: strong / high.
- Time / token / output / retry / concurrency ceilings: one read-only review turn; concise receipt; one focused follow-up only if a disposition is unclear.
- Stop or escalation conditions: do not accept if either independent role used a different fingerprint or any material finding is unresolved.
