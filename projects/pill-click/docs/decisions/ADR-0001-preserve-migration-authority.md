# ADR-0001: Preserve migration authority boundaries

- Status: accepted for migration, not design acceptance.
- Date: 2026-09-01.

## Context

The source has older README claims, later P1/P2 source and exports, and a separate
root P1 spec with a materially different four-part design.

## Alternatives considered

Merging specs or regenerating artifacts would obscure provenance and exceed scope.
Copying only the newest experiment would lose meaningful history.

## Decision

Copy meaningful source/tests/docs/artifacts, exclude only local environment/lock
and caches, preserve original README under legacy, isolate root spec under
legacy/root-pill-click, and introduce current continuity without choosing a release.

## Consequences

Existing gaps/failures remain visible. Future work must select a baseline and open
a design iteration. Root `uv.lock` registers only pill-click and networkx additions.

## Evidence

Active migration source manifest, validation and handoff records.
