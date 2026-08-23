# ADR-0002: Controlled monorepo migration

Status: current

## Context

The untracked legacy directory contains useful parametric history and continuity mixed with gigabytes of generated artifacts, caches, local environments, and stale candidates.

## Decision

Expose a small active project and preserve meaningful historical source in an exact source-only mirror. Copy only the locked assembled STEP and Q3-R0 four-artifact set. Adapt metadata to root uv/npm workspaces and record every selection, exclusion, relocation, and hash.

## Consequences and evidence

History remains recoverable without making rejected tests normal acceptance or importing reproducible bulk. The original directory stays untouched. Migration manifests provide provenance because the source directory itself was untracked.

