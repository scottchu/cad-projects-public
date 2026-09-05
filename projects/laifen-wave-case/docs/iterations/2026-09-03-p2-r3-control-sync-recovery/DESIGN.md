# P2 R3 exact control-sync contract

## Canonical state and transaction order

`raw` is the only mutable parameter object. `raw.S` is a finite unrounded number in millimetres. `d=deriveContainer(raw)` and all control/readout/scene values derive from it. DOM field values, `min`/`max`, text formatted with `toFixed`, and `aria-*` attributes are output only; they are never read back as authority after a render.

Every valid edit follows this ordered transaction:

1. Parse the edited control exactly once into `raw` (`percent` uses `raw.S=percentToSplit(Number(percentElement.value), raw.H, bounds)`; all mm controls set their matching raw numeric field).
2. Run `d=deriveContainer(raw)`.
3. If valid, run `syncControlsFromCanonical(raw,d)` before readout/scene rendering. It writes every control from raw/canonical derivation, including S and percent.
4. Render bounds, readout, scene, detail and accessible status exclusively from that same `d`.

On invalid input, retain the text entered in the active invalid control solely to let the user correct it; do not use it to overwrite another raw value. Once valid again, synchronize every projection from canonical state.

## Exact conversion and bounds behavior

`percent=100*raw.S/raw.H`; a percent edit uses `raw.S=raw.H*percent/100` through the existing endpoint-safe `percentToSplit` function. Endpoint tolerance may map numerical representations to exact `S_min`/`S_max`, but neither control may receive a rounded display value as model input.

`syncControlsFromCanonical` must set:

```text
S.min   = String(d.Smin)
S.max   = String(d.Smax)
S.step  = "0.1"
S.value = String(raw.S)

percent.min   = String(100*d.Smin/raw.H)
percent.max   = String(100*d.Smax/raw.H)
percent.step  = "any"
percent.value = String(100*raw.S/raw.H)
```

These assignments apply after a percent edit, an H edit, a preset edit and a successful mm edit which changes any input affecting dynamic bounds. Formatting for readouts can round independently only after this synchronization.

## Required deterministic browser trace

Use the same valid non-S thread/floor/keepout configuration used by the repair-2 finding, then execute this trace against actual input events:

```text
set H = 261
input percent = percent.min        => raw.S = 12.4; S.value = "12.4"
input percent = percent.max        => raw.S = 248.6; S.value = "248.6"
focus S; press ArrowUp             => S.value = "248.6"; raw.S = 248.6
                                     percent.value = percent.max; all S readouts/bands remain at max
```

The exact expected ArrowUp result is **remain at max**. S has step 0.1 and max 248.6, so the attempted 248.7 step is rejected by native max validity; the event must not reintroduce stale `60` or `60.4`. If a browser produces no input event at maximum, canonical state remains unchanged. If it produces an input event, implementation must derive from its valid unchanged control value; it may not use an obsolete value captured before percent synchronization.

The test also changes H while raw.S is valid and asserts that S min/max and percent min/max/value equal direct raw formulas based on the new H and unchanged raw.S. It must compare numeric properties with `<=1e-12` relative/absolute tolerance and assert DOM string values represent those same raw numbers; it must never compare a parsed display value produced by `toFixed`.

## Minimal implementation route

Implement a single synchronization helper and call it from the successful branch of update/render control flow. It may reuse `populateForm` only if that routine writes all fields from `raw` and `d` without changing `raw`, preserving focused-input handling. No handler may cache S in a closure or merge DOM fields into raw after `percent` has updated it.

The recovery candidate has exactly these source deltas from repair 2:

1. `app.js`: synchronization helper/call sites and dynamic `S` attributes/values.
2. `test_generic_container_simulator.mjs`: exact DOM/browser regression and durable source-level guards for the helper/call order.

All other repair-2 candidate files must hash exactly to their entries in P2 R2 `inputs/implementation-candidate.sha256`: index `ace28e8dd08de7f9ca9bf916887911e0d118c6dd4b0d2e6594f2a88950b878a5`, math `b3e4c734b166349251c9b7683aa23d428cb4d2f8f167ff29349def7dc024337b`, and style `a19c755ca5c27dbe602283ba2652c5b2ff005c2a59266b078c5930b58ff6ccf3`.

## Recovery acceptance boundary

PASS requires the exact browser trace and H-change formula check, protected-file hashes, current candidate manifest, independent VAL/CRIT receipts and formal review. It does not reopen or prove CAD, actual thread form, solid geometry, physical wall/clearance, fit, drainage, printing, slicer behavior or user-device comprehension. Private delivery remains a separate post-review task.
