# IMP-MW-01 implementation receipt

**Status:** repair 1 candidate remains frozen; repair 2 was interrupted and superseded by the user's expanded generic-container/thread scope. Independent revalidation, re-critique, formal review, delivery, and user-visible gate remain pending under a replacement contract.

> Repair 2 interrupted state is deliberately non-candidate: `scratch/makerworld-simulator-impl/repair2-interrupted/STATUS.md` and `non-candidate.sha256`. Do not use it as repair 1 evidence or restore it speculatively.

## Frozen input and scope

- Verified immutable input manifest SHA-256: `b060787132e71d20b995624e7deced8403d3c76c61507f2287170f28d0dc29b6`.
- Baseline is reviewed P1 R7 candidate `8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1`.
- This implementation changed only the isolated preview namespace, the dedicated Node test, this receipt, and the candidate manifest. It does not alter R7 CAD, existing previews/tests, routes, slicer, printer, or publication state.

## Candidate behavior

`preview/p2-r1-makerworld-simulator/` is a static ES-module Three.js page with pinned `three@0.160.1` and matching `OrbitControls` CDN imports. It catches module/runtime setup failure and renders a visible load error that names the pinned CDN dependency.

`math.mjs` owns the canonical `splitFromTop` millimetre parameter, axial derivation, warning policy, and global-Z pattern laws. `app.js` calls each pattern field with `(theta, zGlobal)` before it clips the separately named `lower-piece` and `upper-piece` BufferGeometry exterior meshes. The seam, full thread band, and effective thread band are separate overlays. The upper piece remains described as an upper piece throughout.

The page exposes the required mm and percentage adapters, preserves the canonical mm split when device length changes, offers assembled/exploded display, OrbitControls, all four pattern choices, text readouts, warning text, datum language, responsive layout, and the requested explicit pass/fail intent question. It labels all wall/thread/clearance values as visual prompts rather than fabrication or fit proof.

## Repair 1 against attempt 1

Attempt 1 remains frozen at `inputs/implementation-candidate-attempt1.sha256` (manifest SHA-256 `26e5717885bfd4dcc6a473f455a405767011cca3f94a4ec1cd47ee5fda4fcb6d`). The existing VAL-MW-01 and CRIT-MW-01 evidence is attempt-1 **HOLD** evidence; it does not approve this repair.

This repair makes the input event's `currentTarget` the only value source for each mm/percent adapter. Percent bounds are now derived from `S=50..169` and current `H` after every render; the percent range uses `step="any"` so its own maximum maps exactly to `S=169`. Changing device length preserves `S` and recalculates percentage bounds/value.

The two exterior BufferGeometry surfaces now meet only at global `z_seam`; the visual penetration/effective overlays are concentric inner bands. This removes competing outer surfaces through the 9 mm penetration while retaining the visual thread accounting. In exploded mode, the seam follows the upper piece and the inner full/effective bands follow the lower piece. The page also now exposes a live textual summary of split, spans, pattern, bands, and display mode, with explicit accessible labels for each numeric adapter.

## Requirement coverage

| Requirement | Candidate evidence |
| --- | --- |
| MW-REQ-01 | separately named upper/lower meshes, labels, seam and band overlays |
| MW-REQ-02–05 | `deriveSimulator()` and global-Z `patternRelief()` plus focused Node assertions |
| MW-REQ-06 | four select options and bounded field laws |
| MW-REQ-07 | textual axial, gap, wall-prompt, band and warning readouts |
| MW-REQ-08 | static local HTTP smoke only; route/service and user-surface work are explicitly deferred |

## Commands and results

- `node projects/laifen-wave-case/tests/test_makerworld_simulator.mjs` → passed: defaults, closure, conversion, H=311-derived percent bounds, boundary warnings, field bounds/global-Z continuity, accessible semantics and no-overlap source assertions.
- `/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 -m http.server 8991 --directory projects/laifen-wave-case/preview` plus `curl --fail http://127.0.0.1:8991/p2-r1-makerworld-simulator/` → HTTP 200 and HTML returned.
- `/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 scratch/makerworld-simulator-impl/repair1_smoke.py` → passed in Chromium: slider-origin event propagation, percent-max conversion, H=311 range recalculation, exploded live summary, and mobile screenshot `scratch/makerworld-simulator-impl/repair1-mobile.png`.

## Risks and next action

This is an open outer visual surface, not a CAD solid. Remote CDN availability and actual mobile/browser presentation remain unverified. Give VAL-MW-01 and CRIT-MW-01 the exact candidate manifest; only delivery may configure the new private route after formal review passes.
