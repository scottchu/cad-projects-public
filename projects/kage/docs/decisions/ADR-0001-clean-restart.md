# ADR-0001: Clean restart boundary

Status: current

## Context

Legacy version names and test counts conflict with later defect evidence. The 2026-08-22 restart record identifies one locked reference and explicitly rejects incremental continuation.

## Decision

Use the exact restart record and locked direct-gear assembled STEP/source/test snapshot as authority. Treat the STEP as a frozen comparison, not a finished product. Start future CAD in a new namespace. Q3-R0 is only a candidate reference.

## Consequences and evidence

No historical namespace becomes current without an intentional new decision and regression evidence. CAD/source, artifact/slicer, and physical acceptance remain separate. Evidence hashes are in `manifests/source-authority.sha256`.

