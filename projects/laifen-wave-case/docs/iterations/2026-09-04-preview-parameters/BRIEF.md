# Preview parameter readout brief

**Task:** `PPV-01`  
**Owner:** preview-parameters design architect  
**Status:** frozen design contract; implementation pending  
**Baseline:** accepted P1 R7 parametric package `cad/container_generator_v1/`, candidate `6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`

## User outcome

Show the current grouped container parameters in the existing private CAD Viewer preview for `closed.step.py`. The display must be useful on the user's phone and must not suggest that changing a CAD Viewer control regenerates build123d geometry.

This is a presentation-only addition to the accepted P1 R7 parametric package. It does not change the container shape, exported STEP files, source-level joints, print layout, slicer state, or physical acceptance.

## Viewer capability finding

CAD Viewer 0.4.28 can load a JavaScript sidecar declared by a generated STEP entry. Its native STEP Parameters tab supports `number`, `boolean`, `enum`, `color`, `string`, and `button` controls and applies their changes only through JavaScript viewer effects. It has no read-only field type and no hook that passes changed values back into Python `gen_step()` to regenerate build123d geometry.

The selected design therefore uses fixed one-option enum rows as readouts. No row has a second legal value. The first row states that the panel is a read-only snapshot and that source editing plus STEP regeneration is required for geometry changes. The sidecar performs no viewer effect and defines no animation.

## Requirements

| ID | Requirement |
| --- | --- |
| `PPV-BASELINE` | Keep the four accepted STEP files byte-identical: body `02bfc1ca52ef97dcba3451c930408f64d0f383293933f6183029e36409e1c05a`, cap `b9561b34b96667d1af6e84d145c03d9aa319694fbf11f2cc3c0b60d6b6f18cf0`, closed `cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2`, and print layout `cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b`. |
| `PPV-SOURCE` | Generate the sidecar deterministically from `PARAMETER_SPECS` and `derive(preset())`; do not maintain a second hand-authored parameter table. Commit the generated sidecar and prove regeneration parity. |
| `PPV-COVERAGE` | Display all 26 current registry values and their classifications, plus the compact derived readouts named in `DESIGN.md`. Preserve registry order within the defined display groups. |
| `PPV-GROUPS` | Make groups scan clearly in the flat native panel by stable numeric order and group-prefixed labels. Do not claim native collapsible grouping. |
| `PPV-READONLY` | Every displayed value is a one-option enum readout. Include a prominent read-only/regeneration notice; define no numeric sliders, free-text controls, booleans, buttons, colors, features, or animations. |
| `PPV-NOEFFECT` | The sidecar `update()` is an explicit no-op and may not call an `effects` method, return transforms/styles, hide parts, or alter geometry presentation. |
| `PPV-ENTRY` | Only `closed.step.py` declares `closed.params.js` through the supported `{"shape": ..., "params": ...}` envelope. The three other entrypoints and all build123d builders remain unchanged. |
| `PPV-VIEWER` | The exact Tailscale review page and artifact endpoint must return HTTP 200/ready, and a visual mobile-width review must show the Parameters tab, the read-only notice, representative rows from every group, and the unchanged closed assembly with no visible error state. |
| `PPV-BOUNDARY` | No service/runtime modification, no CAD Viewer source edit, no new web customizer, no STEP rewrite, no STL/3MF/slicing/printer work, and no claim of live CAD regeneration or physical acceptance. |

## Immutable behavior

- The accepted default remains the exact `laifen_wave_r7` preset.
- Python/build123d and `PARAMETER_SPECS` remain the CAD source of truth.
- Closing placement, geometry, occurrence labels, datums, and four written STEP artifacts remain unchanged.
- Selecting or toggling anything in CAD Viewer cannot create a different CAD candidate in this iteration.

## Task DAG

| Task | Owner role / dependency | Done gate |
| --- | --- | --- |
| `PPV-01` | design architect; accepted P1 R7 baseline | Freeze this brief, selected design, and exact input manifest. |
| `PPV-02` | prescribed implementation; `PPV-01` | Add deterministic readout generator, generated sidecar, minimal closed entry envelope, focused test, and implementation receipt without changing STEP bytes. |
| `PPV-03` | independent validation; frozen `PPV-02` candidate | Reproduce sidecar parity/coverage/no-effect checks, verify STEP hashes, verify Viewer descriptor and live endpoints, and capture mobile-width evidence. |
| `PPV-04` | independent formal review; `PPV-03` | Join one exact candidate and issue preview PASS/BLOCK separately from CAD, STEP, slicer, and physical state. |

One implementation attempt plus at most two focused repairs is the ceiling. Any STEP byte change, CAD shape change, mutable-looking control, non-no-op effect, Viewer runtime edit, or unavailable truthful readout stops the task and reopens design.
