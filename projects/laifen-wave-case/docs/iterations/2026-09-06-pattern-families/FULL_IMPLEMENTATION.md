# PF-IMP-FULL implementation receipt

Owner `/root/pattern_direct_implementation`, sole implementation writer.
Status: **frozen candidate for independent validation, critique and browser review**.
No implementation approval or live deployment.

## Provenance and changes

Verified all31 entries of `inputs/full-implementation-baseline.sha256`, SHA
`cfde3bd50bde98865f9204c6536a507b54b070d32a70c78b7ce40821aabdd9a9`, before edits.
Read DESIGN SHA `426729855f05805f16661cc3728a6145b2eac291b56f60199fc6ca7528cc3e61`.
The direct Spiral pilot dependency passed independent validation
`fb01f83b31c9e4ba1aede515e0a275885cce27fd6b341b9ca6ee9b3a1ca78bf0`
and visual review `78be0f0e43517105b3f2e34dd58237da4a8fdf4f587fcd5dc8bd6b524dc11ec5`.
Baseline remains `c181dda780a3b9c407ebe3419702419254266792`, branch
`codex/container-desktop-customizer`.

Frozen source manifest `/tmp/pattern-families-full/candidate-source.sha256`:
36 paths, SHA `666f1a437830aa9be5a692617109def4758cd6f9ec04f8400ec73effa6682456`.
Frozen build/smoke evidence `/tmp/pattern-families-full/candidate-artifacts.sha256`:
16 paths, SHA `15616620e284e8e64b79d6acc1d0b2f3cf7d11fd2a6fbc6add13025d7a89b9fd`.
Current SCAD SHA
`c1a8c8ea2c09a66fdf389049e62ae9383f5a1ac91fe89fcac873f9528d6d07c6`.
Source writes stopped at this fingerprint.

Changed project paths:

- `openscad/laifen_case_customizer_v1.scad`: Ribs/Rings family phases and sample
  counts extend the proven direct wave mesh. Ribs uses one axial base segment
  and max(192,32N) angular samples; Rings/Spiral use192 and s/16. All share owned
  clipping, v06 profile/zipper and protected internals. Diamond size/depth and
  derived arc/phase/plateau guards implement the new control domain.
- `preview/openscad-wasm-simulator/src/patterns.mjs`: shared family defaults,
  raw-field mapping, selected-family source guards and conservative allocation.
- `src/schema.mjs`, `src/adapter.mjs`, `src/bounds.mjs`: normalized complete job
  fields, exact selected-family predicate, remembered raw group isolation,
  family-dependent walls and feasible slider grids.
- `src/controller.mjs`, `src/controls.mjs`, `index.html`, `style.css`: five native
  swatches, selected two-field group immediately below the complete selector,
  independent raw memories, exact number entry, step=any thumb rendering,
  deterministic feasible keyboard/pointer steps, disabled blank/non-numeric
  sliders with hidden thumbs, and Reset of all memories. Explicit Generate,
  cancellation, current-only Download, dimensions and drains remain.
- `tests/node/compact-controller.test.mjs` and new
  `tests/node/pattern-families-implementation.test.mjs`: focused ownership,
  off-grid interaction, invalid repair, raw memory and canonical identity checks.
- `tests/test_openscad_wasm_simulator.py`: updates an already obsolete drain
  error-token assertion to the current shared guard, and checks new job fields.
- `tests/mesh/pattern-families/compile_pilot.mjs`: accepts Ribs/Rings short-case
  smoke modes with their default6/.45 pattern values; Spiral remains s4/.6.

No dependencies, pinned worker/engine, services, Tailscale, live dist, unrelated
projects or commits changed. Root owns continuity indexes and handoff.

## UI interpretation and scope

Design owner confirmed read-only interpretation: explicit feasible grid values
and copy “Allowed slider values” need no continuous-boundary solver. Exact
entries use the full predicate, including off-grid values beyond first/last
feasible grid points; render bounds encompass the exact value. Gap copy says
“Slider skips unavailable values”; empty grids say “No slider steps available”.
No render/switch/focus operation normalizes remembered raw text.

The existing accepted invalid-dimension behavior remains: dimension sliders are
all disabled and explicitly labelled Last valid until the coherent dimension
snapshot is repaired. New pattern controls use only current raw counterfactual
inputs. Invalid active pattern fields also disable dimension sliders. No
fallback is labelled Allowed. Root was explicitly informed of this preservation
for critique against any broader interpretation of DESIGN's “every slider”.

## Commands and observed checks

From the repository root:

```sh
node --test projects/laifen-wave-case/tests/node/compact-controller.test.mjs projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs projects/laifen-wave-case/tests/node/pattern-families-implementation.test.mjs
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
npm run build:openscad-simulator --workspace laifen-wave-case -- --outDir /tmp/pattern-families-full/dist
node projects/laifen-wave-case/tests/mesh/pattern-families/compile_pilot.mjs /tmp/pattern-families-full body ribs
node projects/laifen-wave-case/tests/mesh/pattern-families/compile_pilot.mjs /tmp/pattern-families-full body rings
```

Results:38 Node checks and13 Python checks pass. Build succeeds; it emits the
existing bundle-size advisory (>500kB JS), with no new dependency added.
The initial Python run found the stale drain message assertion above; after
that focused test correction the13 checks passed. No source algorithm repair
cycle was required.

Ribs/Rings smoke tuple: UI D30/H60/W4.6/T3/manual lid25.3, Bottom7,
pattern spacing6/depth.45. These are short-case checks with default pattern
parameters, not the full default-size acceptance matrix.

| Artifact | SHA-256 | Compile seconds |
| --- | --- | ---: |
| `/tmp/pattern-families-full/ribs-body.stl` | 83208750c167b349c3b677cfd7a08d36eecb05bce9f0a8848296fa52e73feb5c | 1.009 |
| `/tmp/pattern-families-full/rings-body.stl` | 14d7bb22a2460c30408fe4c7a42ca1acebc2a91d7edb216f89279e265b927c41 | 7.865 |

Both compiled without ERROR/WARNING diagnostics. Per-family JSON beside each
artifact records full argv and pinned runtime SHA. Reused unchanged prior
validator tools for bounded implementation self-check:

```sh
uv run python /tmp/pattern-families-validation/mesh_probe.py /tmp/pattern-families-full/FAMILY-body.stl
/tmp/pattern-families-validation/mesh_certifier /tmp/pattern-families-full/FAMILY-body.stl .000001
```

Both original STLs have positive volume, zero non-two-use edges and degenerates;
both global certifier checks pass with zero intersections/T-junctions. Detailed
probe/global receipts are included in the artifact manifest. The independent
validator retains acceptance ownership and its reserved test path was untouched.

## Coverage and next action

PF-01..04 and PF-07..08 have implementation and focused controller/math evidence.
PF-05..06 use the independently passed direct construction, but the final source
requires refreshed default parity, full family artifact/error/constraint matrix,
and actual browser observations. No browser screenshot, full-size performance,
all-output matrix, formal approval, STEP, slicing or physical claim is made here.
PF-09 remains explicitly unproven. Next action: critique and independent
validation/browser checks against these frozen source/build manifests; route only
concrete findings to this owner before any next source write.

## PF-IMP-R1 — focused independent findings repair

Status: **R1 frozen for independent recheck**. Verified C1's36-path source
manifest before writes. Root authorized the validator's wall-boundary finding
and the critic's error-routing/accessibility findings in this one repair cycle.
The earlier C1 source/build and evidence remain preserved under
`/tmp/pattern-families-full`.

R1 source manifest `/tmp/pattern-families-full-r1/candidate-source.sha256`:
37 paths, SHA `cb8c804aa0e52ff64d4fe50cbddd4d09b805dbe9a662b7aa28ba694ff08a6b6d`.
R1 evidence/build `/tmp/pattern-families-full-r1/candidate-artifacts.sha256`:
11 paths, SHA `002c5675328de0f4c2b4099d99d9ff24ce5afec43069f7c8d9b6489963d82bc7`.
SCAD SHA `3b96cc2d5a5100e2daa2fe5a14c21e510728f108cfbc9afd5ae80bf1ef5dde40`.

1. **Wave boundary equality:** subtracting several radii at W4.56/d0.60
   produced a residual infinitesimally below1.8 and falsely rejected the
   advertised exact boundary. New-family guards in SCAD and `patterns.mjs`
   compare constructed outside-diameter requirements instead:
   `OD >= body_bore + 2*((root_wall+thread_depth+clearance+1.8)+depth+.01)`.
   Corresponding additive comparisons protect both bores and entry relief.
   This is the same ligament inequality rearranged, with identical JS/SCAD
   operation order and no epsilon. Diamond's existing residual arithmetic and
   all geometric functions remain unchanged.
2. **Allocation error routing:** Rings/Spiral errors identify only pattern,
   spacing, height, ends and manual lid. Ribs identifies its radius/count
   participants; Diamond retains radius/count and height participants.
   Shared family-aware messages replace the adapter's hardcoded Diamond copy.
3. **Unavailable slider accessibility:** a blank/non-numeric active pattern
   slider sets `aria-valuetext="Enter a number"`; numeric repair removes the
   override. The exact input remains enabled. The redundant “Diamond diamond
   size” accessible label is now “Diamond size”.

Focused changes: SCAD guards, `patterns.mjs`, `bounds.mjs`, `adapter.mjs`,
`controller.mjs`, one HTML label, two existing implementation test files and
new `tests/mesh/pattern-families/probe_wall_boundaries.mjs`. No worker, geometry,
dependency, live build or service changes.

Executed from root:

```sh
node projects/laifen-wave-case/tests/mesh/pattern-families/probe_wall_boundaries.mjs /tmp/pattern-families-full-r1
node --test projects/laifen-wave-case/tests/node/compact-controller.test.mjs projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs projects/laifen-wave-case/tests/node/pattern-families-implementation.test.mjs
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
npm run build:openscad-simulator --workspace laifen-wave-case -- --outDir /tmp/pattern-families-full-r1/dist
```

All40 Node and13 Python checks pass; isolated build succeeds with the same
bundle-size advisory. Twelve pinned-WASM source-guard probes pass: Ribs/Rings/
Spiral at D30/d0.60 reject W4.55 and4.5599999, accept W4.56 and4.5600001.
The source probe uses existing tiny math output to execute actual source
assertions; it is not a full solid or physical test. Its JSON binds source,
exact argv, runtime hashes, expected/actual decisions and diagnostics.
Adapter/schema/draft tests cover the same boundary witnesses; further tests
cover family-specific error participants/messages and accessible unavailable
state/repair. Geometry was not regenerated in this guard/UI repair.

Next action: distinct validator/critic/browser recheck against R1. Original
Smooth/Diamond and wave geometry parity, broader mesh matrix, actual accessible
snapshot and formal review remain acceptance-role work. Source writes stopped.

## PF-IMP-R2 — unavailable native accessibility range

Status: **R2 frozen for actual accessibility recheck**. Root's independent R1
browser evidence (`/tmp/pattern-families-full-browser/r1-empty-native-ax.json`
and `r1-empty-dom.txt`) still exposed the stale4.8 native range value despite
its DOM `aria-valuetext`. This observation supersedes the R1 implementation
assumption that value text alone would remove the misleading numeric origin.

Only `src/controller.mjs` and its focused controller regression changed.
A pattern range sets `aria-hidden=true` only while it is disabled and its own
raw value has no numeric origin. Numeric repair removes that attribute. The
exact input, rule/error and finite coupled partner remain accessible.
No geometry, schema, guard, source or style change occurred. SCAD remains
`3b96cc2d5a5100e2daa2fe5a14c21e510728f108cfbc9afd5ae80bf1ef5dde40`;
R1 CAD/artifact validation can continue against that same source fingerprint.

R2 source manifest `/tmp/pattern-families-full-r2/candidate-source.sha256`:
37 paths, SHA `6701e4c3667e718455cf8ee622684c3d0e0f74971e51bc4f279f98b13554fc1d`.
R2 build/test manifest `/tmp/pattern-families-full-r2/candidate-artifacts.sha256`:
7 paths, SHA `7e6cedbb7e104ecdacfde7199011449a24d9ebbb930689ef6af2bee3f5a2b0b4`.

```sh
node --test projects/laifen-wave-case/tests/node/compact-controller.test.mjs
npm run build:openscad-simulator --workspace laifen-wave-case -- --outDir /tmp/pattern-families-full-r2/dist
```

All12 controller checks pass; isolated build succeeds with the unchanged
bundle-size advisory. The focused regression checks hidden unavailable range,
its restoration after numeric repair, visible finite partner and available
exact input. No actual native accessibility success is claimed by this role;
root/critic must verify the R2 browser tree. This is the second focused repair;
source writes are stopped at the manifest above.
