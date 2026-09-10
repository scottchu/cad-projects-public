# Iteration design record

## Alternatives considered

In-place redesign and newest-only import were rejected as outside migration scope.
Registering raw drone as an active member was rejected because it has no Python
workspace contract and the user explicitly requested storage for a later reboot.

## Frozen selected design contract

Copy Pill Click meaningful files without transformations except its current README.
Preserve README bytes under `docs/legacy/README.source.md`. Isolate the separate
root P1 spec outside `src/`. Add continuity; keep all design parameters, datums,
interfaces, versions, tests and model bytes unchanged. Exclude nested lock,
environments, caches and filesystem metadata. Do not select an accepted design.
Include this contract, requirements and imported files in the candidate fingerprint.

## Rejected or failed approaches

No packaging repair needed. No design repair attempted. Existing root environment
extraneous packages were removed by prescribed sync; this is recorded, not hidden.

## Decisions promoted to ADRs

ADR-0001 records source-preserving authority boundaries.
