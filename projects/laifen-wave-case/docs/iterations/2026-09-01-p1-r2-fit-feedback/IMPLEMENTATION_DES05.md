# IMP-05 implementation receipt

Candidate manifest: `inputs/des05-candidate.sha256`  
Fingerprint: `f0fe32796fcfae64591565b2f48983325b2c7d407e6152cf2272c3e9536eb788`

`preview/measurement-gate.html` now derives screen-space values before it writes
the SVG and rejects the render when any essential viewport, scale, cavity,
device, leader, label, stop, gravity, or gap coordinate is non-finite. The
existing invalid-state path then clears the section and all readouts. This adds
no input cap, control, dimension, or geometry change.

`tests/test_measurement_gate.mjs` adds the prescribed one-instance sequence at
360 and 736 px: default values render finite SVG values; `D=1.7e308` produces
the existing error with all five display regions empty; restoring `D=29` renders
ordinary finite geometry and readouts again. Its DOM stub now gives `innerHTML`
and `textContent` the browser clearing behavior needed to verify no stale state.

Ran from the repository root:

```sh
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/des05-inputs.sha256
node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/des05-candidate.sha256
```

All 16 frozen inputs verified. The Node harness passed 9 tests, including all
prior checks and the new rendered-numeric regression. This is an implementation
receipt only; independent critic, validator, and formal review remain required.

## Focused V05-01 repair

The prior candidate remains preserved at `inputs/des05-candidate.sha256`, with
its pre-repair source copied to `inputs/des05-pre-repair-source.html` (SHA-256
`2449f34f94fcd768e06873d1fa99f095a3f20fd6758a2b896c24b2153860cb13`).
The upper-ID span stays at y48; only its `上段參考 ID 31` label moved from the
central cavity at y64 to the existing external label column at y40. This clears
the upper floor/device region without changing any numeric, domain, control, or
geometry behavior.

Repair candidate: `inputs/des05-repair-candidate.sha256`  
Fingerprint: `9f1fdb44f7b350f7ca903c37ca2383ba195dd2f7235bbe69d2b1596f86ae4f61`

`sha256sum -c` verified every repair-manifest entry and the Node harness again
passed 9/9. The distinct validator must remeasure V05-01 at 360/736 light/dark;
this implementation receipt does not approve the repair.
