# Included and excluded content

## Included

- `103` branch XT60 paths from `a883404` copied byte-for-byte. The remaining
  three branch XT60 paths (`PROJECT_STATE.md`, `NEXT_AGENT.md`, and
  `docs/iterations/CURRENT`) are included through explicit reconciliation.
- `134` recovery-snapshot XT60 paths copied byte-for-byte, covering unique
  source, tests, CAD/STEP/3MF/G-code preparation evidence, review records and
  authored HTML intent gates. This count includes the snapshot versions of
  `docs/REQUIREMENTS.md` and `docs/EXPERIENCE.md`.
- All `158` Pill Click snapshot files copied byte-for-byte, plus the ignored
  `p1_review_job.json` referenced by the preserved migration manifest, copied
  byte-for-byte from the immutable original checkout and explicitly staged.
- All `106` archived drone snapshot files copied byte-for-byte. The archive is
  identified as inactive in the root project-discovery entry.
- Root `uv.lock` regenerated with the current main lock as baseline, adding
  Pill Click and `networkx` only.
- Root README project discovery and XT60 current-state, next-agent, current-
  iteration, P25 handoff and printing-profile reconciliation.

## Excluded or superseded

- Fifteen redundant pre-repair/repair-before XT60 PNGs listed in
  `redundant-media-exclusions.txt` by M1. Their bytes remain in the immutable
  recovery snapshot; final/annotated/validation/repair2 review media remain.
- Source-branch root `AGENTS.md`, `docs/ARCHITECTURE.md`, and
  `docs/CAD_WORKFLOW.md`. Modern main's bound-policy versions supersede them.
- Recovery-snapshot root policy copies, old template copies, Kage state,
  repository checks, and unrelated project files. Modern main is preserved.
- Recovery caches, logs, scratch, nested environments, `.DS_Store`, and Git
  metadata. No such path is part of the candidate.
- The snapshot XT60 `PROJECT_STATE.md`, `NEXT_AGENT.md`,
  `docs/iterations/CURRENT`, and `PRINTING_PROFILE.md` are superseded by the
  reconciled delivery versions. Historical iteration records are unchanged.
- The old snapshot `uv.lock` is superseded by the lock generated from modern
  main plus the imported Pill Click manifest.

Exact source and destination SHA-256 values and status for every imported,
reconciled, or explicitly excluded branch/snapshot path are in
`PROVENANCE.tsv`.
