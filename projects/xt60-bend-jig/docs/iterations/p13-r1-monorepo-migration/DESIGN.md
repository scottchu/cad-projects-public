# P13 R1 monorepo migration design record

## Alternatives considered

1. Copy the complete `1.5 GB` legacy tree. This preserves convenience data but imports a `1.1 GB` environment, Node install, caches, and unreviewable generated churn.
2. Import only P13. This is compact but discards the design progression, rejected mechanisms, calibration source, and lessons that later agents may need.
3. Import meaningful source and history plus a selected release set. This preserves reasoning and reproducibility while keeping runtime debris out of Git.

## Selected approach and rationale

Use option 3. Bulk-copy 206 source, configuration, test, and design files under explicit exclusions. Add the imported vendor XT60 STEP, selected P13 and P14–P16 releases, and five high-value historical P13 review views. Preserve legacy summaries under `docs/legacy/` and create normalized continuity records.

## Parameters, interfaces, and datums

- No geometry parameter or datum changes are authorized.
- Preserve P13 source hash `e424fac8064d35713ed15748bb8a0e1f966ef429b507ba4be5a5dc31cfc7c72b`.
- Preserve P13 brief hash `9c2102114cbf87ccabaa4388ed3814b91cdf3f8f654c775f5ddd8a5d05272322`.
- Preserve controlling amendment hash `b50e850ac5425fe7bad0e49555de10b0e30f63e04934bdbf66d4220f44e1f590`.

## Assumptions

- The restart copy is a byte-identical convenience mirror of the original project after prior checksum verification.
- `cadgen==0.4.15` remains installable in the root workspace.
- Historical binary hashes are comparison evidence, not current acceptance until reproduced.

## Rejected or failed approaches

- Importing `.venv`, `node_modules`, nested locks, `__cadgen__`, logs, `dist`, and bulk review output.
- Treating the legacy handoff as the current canonical state without path and acceptance normalization.
- Upgrading CAD dependencies while trying to prove the migration baseline.
- Guessing which CAD hole the user's "center hole" names during migration.

## Decisions promoted to ADRs

- `ADR-0002`: source-first controlled migration boundary.
