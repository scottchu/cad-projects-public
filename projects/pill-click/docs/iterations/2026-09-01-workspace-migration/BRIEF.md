# Iteration brief

- Opened: 2026-09-01; source-preserving migration independently reviewed and complete.
- Origin baseline: `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`, working tree frozen in `source-manifest.json`.

## Frozen design contract

Move Pill Click development to `design-projects/projects/pill-click` without
changing source, tests or model artifacts. Preserve original documentation,
root P1 legacy evidence and all missing-reference/acceptance gaps. Use only the
root workspace environment and lock. No CAD/design/printing acceptance, no
source repair, no commit/push/PR. Drone is separately parked unchanged at
`design-projects/archives/drone`, outside active workspace membership, for reboot.
Requirements: `docs/REQUIREMENTS.md` MIG-001 through MIG-005.
Planned evidence: hashes, lock diff/check, root continuity tests, import/spec
tests and static P1 package checks. Full CAD and slicer tests are out of scope.

## Mutable delegated execution plan and status

| ID | Role / owner | Deps | Immutable inputs | Exclusive writes | Done condition | Ceiling | Status |
|---|---|---|---|---|---|---|---|
| MIG-IMPLEMENT | implementation / `/root/migrate_pill_click` | root inventory | manifest + frozen contract | pill-click, archives/drone, root uv.lock and normal sync | preserved copy, continuity, bounded tests | inherited model/effort; 15 min; one packaging repair; one worker | complete |
| MIG-VALIDATOR | independent validator / `/root/migration_validator` | MIG-IMPLEMENT | source and candidate manifests | read-only; findings via parent | independent data parity and bounded checks | 5 min; no repair; one worker | pass |
| MIG-CRITIC | independent critic / `/root/migration_critic` | MIG-IMPLEMENT | source candidate plus authority/dependency records | read-only; findings via parent | identify migration risks, not design critique | 4 min; no repair; one worker | complete; two documentation/provenance corrections supplied |
| MIG-REVIEW | distinct formal reviewer / `/root/migration_formal_review` | MIG-VALIDATOR, MIG-CRITIC | review-inputs.sha256 and upstream receipts | read-only; findings via parent | join migration acceptance only | 4 min; no repair; one worker | approved |

Validator, critic and reviewer allowed reads: frozen source/destination inputs and
canonical migration evidence. Forbidden: source, CAD, artifact, dependency, Git,
and printer mutations. Output ceiling: one concise receipt with fingerprint,
commands, findings, requirement coverage and next action. Stop on changed frozen
inputs, hash mismatch, data loss or need for out-of-scope repair. Role identities
are distinct; root collects provenance and updates only mutable continuity records.

### MIG-IMPLEMENT scope and stop conditions

Allowed reads: source project/root legacy spec, destination policy/templates/lock.
Forbidden: original source writes; other projects; AGENTS/root manifests/tests;
package-lock; Git index/branches/commits; CAD regeneration and design repair.
Deliverables: copy, current continuity, manifest, exact command/result receipt.
Escalate on hash mismatch, collision, dependency churn or out-of-scope failure.
Output ceiling: concise canonical records and receipt, no raw agent diaries.
