# OSW-05 recovery handoff

**Status:** design frozen; implementation not started  
**Owner:** OSW-05 design

Implement only the worker argv addition `--backend=Manifold`, the real-WASM tiny-cube preflight, hard timeout, and diagnostic capture described in `DESIGN.md`. Preserve geometry, UI, source paths, dependency lock, routes, and existing controls. Do not claim case mesh success from cube success.

Implementation must freeze the worker, focused tests, cube and case reports, native/WASM mesh parity, and served-byte evidence before distinct critique, validation, and formal review. A timeout, unsupported flag, or parity failure stops delivery and leaves the prior candidate clearly marked BLOCKED.
