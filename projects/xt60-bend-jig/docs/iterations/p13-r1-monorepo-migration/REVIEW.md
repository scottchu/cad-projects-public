# P13 R1 monorepo migration review

## Review baseline

- Source: restart copy recorded in `migration-manifest.json`
- Target: `projects/xt60-bend-jig`
- Geometry changes authorized: none

## Findings

| ID | Severity | Finding | Resolution | Status |
|---|---|---|---|---|
| `MIG-REV-001` | medium | Legacy README described P0 as current and used project-local locks and stale CAD runtime paths. | Replaced with P13 current-state and root-workspace commands; legacy text remains in historical source records where needed. | resolved |
| `MIG-REV-002` | medium | Legacy handoff files named old canonical paths and could misdirect a new agent. | Relocated unchanged files under `docs/legacy/` and added canonical `PROJECT_STATE.md` and `NEXT_AGENT.md`. | resolved |
| `MIG-REV-003` | high | Historical test and artifact claims could be mistaken for current-workspace acceptance. | Marked every acceptance category pending until reproduced and retained hashes as comparison evidence only. | resolved |
| `MIG-REV-004` | high | The latest physical print has a center-hole fit failure. | Recorded the exact user observation without guessing the CAD interface; reserved a separate defect-regression iteration after migration. | open-next-iteration |
| `MIG-REV-005` | medium | The complete suite initially failed where generated outputs were intentionally excluded from bulk transfer. | Regenerated current P13 outputs from source. All 59 focused P13 tests now pass; seven unrelated P2–P6 historical export assumptions remain recorded rather than importing stale binaries. | resolved-for-current-baseline |
| `MIG-REV-006` | low | A fresh simulator screenshot could not be captured because no controllable in-app browser runtime was attached. | Contract tests and the production build pass; visual browser review remains explicitly pending. | open-nonblocking |

## Remaining concerns

- Fresh slicer validation and simulator browser review remain pending.
- Physical P13 acceptance remains pending regardless of migration success.

## Review conclusion

The migration and continuity structure are accepted as the P13 source baseline. Current source, focused tests, explicit artifacts, solid validation, and CAD snapshots pass. The printed mechanism is not physically accepted because of the center-hole fit defect.
