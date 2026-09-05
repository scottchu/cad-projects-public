# OSW-12 repeat-call recovery design contract

## Runtime lifecycle

Each CLI invocation owns a fresh `OpenSCAD({noInitialRun:true,...})` instance and exactly one `callMain`. The cube preflight uses its own instance; body, cap, and assembled jobs each use a separate fresh instance. Do not reuse an exited module, rely on `noExitRuntime`, or make `noExitRuntime` the primary fix without authoritative evidence that the pinned build supports safe repeated calls.

## Backend diagnostics

Construct argv with `--backend=Manifold` when supported by the pinned build. Remove only the obsolete `--enable=manifold` flag that produced the exact warning `Ignoring request to enable unknown feature 'manifold'`. Capture stdout/stderr and require diagnostics to prove the requested backend was accepted; an unknown-feature warning, silent fallback, or ambiguous backend is BLOCK. Preserve all other argv and parameter-to-`-D` mappings.

## Acceptance gates

The real browser must complete, within 180 seconds per job, the cube preflight followed by default smooth body and cap jobs. Validate each returned mesh for nonempty watertight geometry, component count, bounds, volume, and native parity within declared tolerances. Exercise UI states for compiling, success, error, reset, stale-result suppression, and download identity. A cube pass alone is insufficient; any second-call abort, timeout, backend ambiguity, stale result, or parity failure is BLOCK. Diamond remains disabled unless separately covered by the existing performance contract.

No source geometry, UI design, dependency lock, route, STEP, slicer, printer, or physical acceptance is changed or implied.
