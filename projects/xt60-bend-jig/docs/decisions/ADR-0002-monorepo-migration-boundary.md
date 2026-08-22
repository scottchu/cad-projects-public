# ADR-0002: Monorepo migration boundary

- Status: accepted
- Date: `2026-08-22`
- Supersedes:
- Superseded by:

## Context

The legacy XT60 directory was untracked, approximately `1.5 GB`, and dominated by a project-local environment, Node install, CAD render caches, bulk review media, and generated output. A checksum-identical restart copy existed, but historical validation still needed reproduction in the new repository.

## Alternatives considered

- Copy the complete directory, including environments and caches.
- Copy only the current P13 source and discard earlier iterations.
- Import all meaningful source and design history, selected release evidence, and no disposable runtime data.

## Decision

Use the restart copy as migration input while preserving both legacy directories. Import all parametric and simulator source, tests, design documentation, and generation scripts. Retain selected P13 production artifacts, P14–P16 calibration releases, one vendor STEP dependency, and five high-value P13 review views. Exclude nested environments, locks, Node installs, caches, CAD render packages, logs, build output, bulk renders, and stale generated binaries.

Preserve `cadgen==0.4.15` for the first reproduction so dependency upgrade and migration remain separate decisions.

## Consequences

The new project is small enough to review and remains traceable to the legacy baseline. Generated releases must be reproduced before current-workspace acceptance. Earlier generator source remains available without committing every historical binary.

## Evidence

- `docs/iterations/p13-r1-monorepo-migration/migration-manifest.json`
- `docs/legacy/CONTINUATION_SUMMARY-2026-08-22.md`
- `releases/p13-petg-test/release-manifest.json`
