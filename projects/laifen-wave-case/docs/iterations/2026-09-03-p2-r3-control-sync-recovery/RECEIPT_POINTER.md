# Recovery receipt continuity pointer

The active upstream implementation narrative is P2 R2 [`IMPLEMENTATION_REPAIR2.md`](../2026-09-03-p2-r2-generic-container-simulator/IMPLEMENTATION_REPAIR2.md), which describes the exact candidate manifest SHA-256 `32429b0817e918343959be9cfe783a8ae76a2d00e0a35b9903b77c71ef6f34b6`.

P2 R2 `IMPLEMENTATION.md` is an older repair-1 narrative and is not the active source receipt. If implementation completes this recovery, it must create `IMPLEMENTATION_RECOVERY.md` in this P2 R3 iteration, name P2 R2 repair 2 as its baseline, declare its new candidate manifest and list the only permitted app/test/receipt deltas. Formal review must consume that recovery receipt, not the stale P2 R2 `IMPLEMENTATION.md`.
