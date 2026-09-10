# Project state

Last updated: `2026-09-01`

## Baseline

- Canonical path: `design-projects/projects/pill-click`.
- Origin repository baseline: `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`; copied working-tree content, not an assertion of a clean historical revision.
- Exact imported files and SHA-256: active iteration `source-manifest.json`.
- Authority: `src/pill_click/`; preserved tests under `tests/` and P1/P2 exports under `models/`.
- P1 three-part and P2 four-part bayonet experiments remain distinct. No currently accepted release selected by migration.

## Active iteration

- ID: `2026-09-01-workspace-migration`.
- Handoff: `docs/iterations/2026-09-01-workspace-migration/HANDOFF.md`.
- Status: source-preserving migration independently approved; originals recoverably quarantined. This is not design/print acceptance.
- Recovery: `/Users/scottchu/.Trash/3d-print-cleanup-2026-09-01.V3MAHz/design/pill-click` and sibling `pill_click`; see quarantine `RECOVERY.md`.

## Acceptance state

- CAD/source: copied byte-identically; focused spec/import checks pass, full design acceptance not established.
- Written artifact/slicer: preserved hashes and three static P1 3MF checks; no fresh STEP parity or slicer validation.
- Physical: no migration-era print or assembly test. Historical observations remain scoped to their old specimens.

## Open risks and unknowns

- Historical README references missing P0 model/export files and nonexistent V1/V2 artifact tests.
- P2 is an experiment with no standalone brief or physical acceptance evidence.
- Legacy root P1 spec differs materially from canonical P1 and must never be merged implicitly.
- Root sync temporarily removed extraneous `greenlet`, `playwright`, `pyee`; their exact prior versions were restored offline. Lockfile changed only for pill-click/networkx.
- Root repository suite has an unrelated existing XT60 `PROJECT_STATE.md` heading failure; it was not repaired here.

## Next action

Before further CAD or print work, choose one baseline with the user and freeze its
intent and test gates. Use the completed migration's manifest as provenance, not
as a design approval. Commit/PR delivery remains separate from this local cleanup.
