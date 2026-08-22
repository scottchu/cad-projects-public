# Kage R0 monorepo migration brief

## Frozen design contract

- Project: `projects/kage`; display name: **Kage**.
- Iteration: `2026-08-22-r0-monorepo-migration`.
- Repository baseline: `1484955cc1cfa64164dbdd1ca1222be658933c8e` on branch `codex/migrate-kage`.
- Legacy source: `/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator`, an untracked directory beneath parent repository HEAD `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`.
- Restart authority: `docs/CONTINUATION_RESTART_2026-08-22.md` at SHA-256 `f5cf4e42a75ddb6df437cb2bdeeff9a017067f4e41097ec66974130bb0962464`.
- Frozen reference: locked assembled STEP at SHA-256 `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`, plus its exact three-file `source_snapshot` and three-file `tests_snapshot`.
- Source-label authority manifest: eight path-and-content lines, path-sorted, SHA-256 `c838df4fb1edaa4077330db1fb8e24808a065e8738d5646cd76b26077a707cdd`.
- Root current direct-gear source triplet is byte-identical to the locked source snapshot.
- Q3-R0 is a candidate/reference only. Preserve its three source modules, one test, wrapper generators, and four small STEP/3MF artifacts without promoting it to current or physically accepted.
- Preserve the simulator/optics runtime as installed historical compatibility, not normative restart architecture, and preserve meaningful parametric history. Preserve legacy continuity byte-for-byte. Exclude environments, caches, logs, rollback duplication, and bulk generated media/CAD.
- Adapt only workspace metadata: root uv/npm workspaces, Python `>=3.12,<3.13`, project and CLI naming, and existing dependency pins. Do not redesign CAD or regenerate historical artifacts.
- Current authority is a clean-restart boundary, not a new CAD candidate. Half-Z, low-Z, M1/M1B, Q4, I3/R1/R2, and every newer-looking historical namespace remain rejected, untrusted, or historical as stated by the restart document.
- Acceptance is always three layers: CAD/source; written artifact/slicer; physical print/assembly. Migration integrity cannot promote physical evidence.

### Intended outcome and use sequence

A fresh agent can enter `projects/kage`, identify the clean-restart authority and locked comparison artifact, run the active simulator and integrity checks from repository-root workspaces, consult complete legacy evidence, and start a new restart CAD namespace without relying on an agent session.

### Invariants and non-goals

- Preserve every selected byte exactly and publish its provenance.
- Parametric source remains authoritative; binary artifacts are frozen references or candidates only.
- No XT60 changes, no CAD redesign, no generated-artifact edits, no root architecture/policy changes, and no claim that a print, fit, motion, strength, or slicer gate has passed.
- Normal Kage tests must not silently run historical or rejected suites.

### Planned evidence and done gate

Verify the frozen hashes, source-selection manifest, workspace metadata, active integrity tests, simulator build/tests, selected written STEP/3MF structure, exclusion boundary, and three acceptance labels. Independent critic and validator examine one frozen candidate fingerprint; a distinct formal reviewer joins their results.

### Candidate coverage

The frozen candidate manifest is the exact set of both root lockfiles plus every intended file under `projects/kage/`, including this `BRIEF.md`. It excludes only runtime debris, the candidate manifest itself, and these existing mutable/evidence paths: `PROJECT_STATE.md`, `NEXT_AGENT.md`, `docs/iterations/CURRENT`, and the active iteration's `HANDOFF.md`, `REVIEW.md`, and `VALIDATION.md`. Integrity tests require exact set equality, require every exclusion to exist, and reject any new unlisted decision-bearing file. This section and the rest of `BRIEF.md` are frozen after repair-cycle refreeze.

## Delegated task DAG

The immutable design contract above is frozen. Task status below is mutable orchestration state and is excluded from task-input fingerprints.

| ID | Role / owner | Dependencies | Immutable input | Exclusive writes | Done gate | Parallel group | Ceiling | Status |
|---|---|---|---|---|---|---|---|---|
| KAGE-MIG-001 | design / `/root/kage_migration_design` | none | repository baseline + source authority | none | migration boundary and experiment selected | A | strong/high, read-only, one turn | complete |
| KAGE-MIG-002 | implementation / `/root/kage_migration_impl` | 001 | source-label fingerprint `c838df4f…` + frozen contract | `projects/kage/**`, root `uv.lock`, root `package-lock.json` | controlled migration and self-check receipt | B | balanced/medium, ~25 min, <1800-word receipt | complete; candidate frozen |
| KAGE-MIG-003 | critic / distinct identity assigned by root | 002 | frozen candidate fingerprint | none | adversarial scope/mechanical/DfAM findings | C | strong/high, read-only, one turn | pending |
| KAGE-MIG-004 | validator / distinct identity assigned by root | 002 | same frozen candidate fingerprint | none | independent commands and acceptance evidence | C | strong/high, read-only, one turn | pending |
| KAGE-MIG-005 | formal reviewer / distinct identity assigned by root | 003, 004 | same candidate + critic/validator receipts | `REVIEW.md` only if assigned | traceability/disposition join verdict | D | strong/high, one turn | pending |

### KAGE-MIG-001 — design

- Objective: identify exact authority, reject false-current branches, choose the controlled migration boundary and one next experiment.
- Reads: repository policy; all legacy continuity, source, tests, and artifact inventory.
- Writes: none. Forbidden: implementation, artifact generation, acceptance approval.
- Evidence/receipt: restart hash, locked STEP hash, eight-file fingerprint, selected/excluded namespaces, exact experiment.
- Stop/escalate: inconsistent restart authority or conflicting physical evidence.

### KAGE-MIG-002 — implementation

- Objective: migrate the frozen boundary and historical source into a recoverable root-workspace project without changing CAD.
- Reads: all repository policy and legacy project files.
- Exclusive writes: `projects/kage/**`, root `uv.lock`, root `package-lock.json`.
- Forbidden: XT60, root policy/architecture, source project, commits/push/PR, self-approval.
- Deliverables: continuity, legacy preservation/index, source-selection manifests, active runtime, workspace metadata, focused integrity tests, selected artifacts.
- Done gate: hashes and controlled counts agree, normal commands are explicit, locks resolve, receipt returned.
- Ceiling: one initial attempt plus at most two focused repairs; one writer; stop on authority mismatch, unexpected target, lock conflict, uncontrolled selection, or overwrite risk.

### KAGE-MIG-003 — critic

- Objective: challenge migration scope, authority labels, recoverability, mechanical/physical overclaims, and source/artifact provenance.
- Reads: frozen candidate only. Writes: none. Forbidden: repair or acceptance approval.
- Evidence: severity-ranked findings mapped to requirements; exact candidate fingerprint.
- Stop: candidate drift or missing immutable manifest. One attempt plus at most two targeted rechecks.

### KAGE-MIG-004 — validator

- Objective: independently reproduce hashes, run root-workspace tests/builds, inspect selected written artifacts, and audit exclusions.
- Reads: frozen candidate and source provenance. Writes: none except transient ignored caches.
- Forbidden: source repair, continuity redesign, physical-acceptance promotion.
- Evidence: exact commands/results and three-layer acceptance boundaries.
- Stop: candidate drift, destructive command requirement, or unavailable dependency that invalidates evidence. One attempt plus at most two focused reruns.

### KAGE-MIG-005 — formal review join

- Objective: audit scope, requirement traceability, identity separation, critic/validator provenance, and finding disposition.
- Reads: same frozen candidate plus 003/004 receipts. Writes: iteration `REVIEW.md` only when explicitly assigned.
- Forbidden: implementation repair or self-review. Deliverable: independent verdict and unresolved risks.
- Stop: fingerprint mismatch, missing upstream receipt, or unresolved critical finding. One attempt plus at most two focused rechecks.

### Design receipt

KAGE-MIG-001 completed read-only with no changed paths. It identified the clean-restart document and locked STEP as authority, reproduced the eight-file fingerprint, confirmed root/snapshot source equality, rejected historical false-current namespaces, classified Q3-R0 as reference only, and found no completed physical-results JSON/photo set. It concluded that migration may prove source integrity and inspect the locked STEP, but cannot accept a new restart CAD candidate or the physical layer.

### Immutable manifest serialization

`manifests/kage-mig-002-input.sha256` is a final-LF, lexically path-sorted list of `lowercase_sha256`, two ASCII spaces, and the declared source-relative path. Logical `#frozen-contract` and `#selected-contract` entries hash only those frozen sections; mutable status/evidence records are excluded. Any changed declared input invalidates only the dependent gates.
