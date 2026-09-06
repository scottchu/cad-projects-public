# Pattern performance implementation — PERF-IMP

Status: **implemented; candidate frozen for independent validation**. This receipt does not approve the candidate.

## Provenance

- Owner: `/root/drain_validation`, reassigned after the original implementation worker was interrupted without writing files.
- Baseline commit/source: `7f15b1649a5d83c77512c9ba0864943ac68996b6`, SCAD SHA-256 `3b96cc2d5a5100e2daa2fe5a14c21e510728f108cfbc9afd5ae80bf1ef5dde40`.
- Frozen baseline copy: `/tmp/pattern-performance-design/baseline.scad`, same SHA-256.
- Corrected 41-path design manifest SHA-256: `4a0d35663c572177fcf8c588654651aad7675fabd2c23c436393363bf842711c`.
- The earlier manifest was verified before work. Root then restored 14 omitted blank lines in the historical pattern-family DESIGN only. After correction, all 40 immutable inputs reverified exactly, including that file's restored SHA `426729855f05805f16661cc3728a6145b2eac291b56f60199fc6ca7528cc3e61`; the sole manifest mismatch is the authorized SCAD edit below.

## Changes

- `openscad/laifen_case_customizer_v1.scad` SHA-256 `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`.
  - `wave_edge_cut` now decodes the edge row first and returns `undef` when both endpoint cones equal `outer_radius`. Since every wave field radius is `outer_radius - wave_depth*(1-cos(...))/2 <= outer_radius`, those endpoints cannot cross the cone and need no point/field evaluation.
  - `wave_face_polys` emits the same two original triangle ID lists directly when both row cones equal `outer_radius`, avoiding sign/clipping work in an uncut row band.
  - Both predicates use exact equality and the unchanged cone expression. Surviving cuts retain the original point calls, sign test, interpolation arithmetic, primitive IDs, vertex/face order and winding.
  - Smooth and Diamond do not enter this shared Ribs/Rings/Spiral wave path and remain unchanged.
- `tests/mesh/pattern-performance/benchmark.mjs` SHA-256 `9bb3d10f9ce2a9b7d8e5fa961133c3edef0b3831ca02dadb434f271eaa9d79ba`.
  - Durable fresh-process runner requires explicit runtime, source and output paths; pins both official runtime hashes; supports all five styles, four roles and CSG/ASCII STL/binary STL; records initialization, `callMain`, compiler render, read and write times plus exact bytes/hashes/messages.
- `tests/node/pattern-performance.test.mjs` SHA-256 `733ca2f006209a03f160b24edac899a318382504d99e2481ab8ab7ded5100483`.
  - Protects exact predicate/source arithmetic, proves sampled skipped rows cannot cross the cone, and checks the durable runner contract/pins.

No UI, worker, engine, dependency, density, guard or service source changed. The standard build temporarily replaced the live preview `dist`; it was restored exactly as recorded below.

## Implementation benchmark

Each row is one sequential baseline/candidate pair in fresh Node processes with no competing benchmark. Runtime: official pinned JS `904a47f2…18a62e`, WASM `f72ce246…f26`; default tuple; ASCII STL; Manifold backend. These samples demonstrate the implementation direction; the independent validator owns three-pair medians and boundary-role parity.

| Case | Baseline callMain | Candidate callMain | Reduction | Exact STL bytes / SHA-256 | Compiler render |
| --- | ---: | ---: | ---: | --- | ---: |
| Rings body | 25.426 s | 18.257 s | 28.195% | 39,958,888 / `d1b73da0…fa849` | 1.342 / 1.350 s |
| Spiral body | 26.146 s | 19.204 s | 26.551% | 39,798,602 / `54856286…20e1c` | 1.341 / 1.351 s |
| Spiral assembled | 45.429 s | 32.637 s | 28.158% | 66,650,851 / `10774d30…84277` | 4.049 / 4.033 s |

All three baseline/candidate artifacts are byte-identical. A separate Rings CSG check was also byte-identical at 5,125,335 bytes/SHA `d8b403dd…5458`, with `callMain` 24.652 -> 17.212 s (30.178%). Receipts and artifacts are under `/tmp/pattern-performance-implementation`; exploratory baseline/design receipts remain under `/tmp/pattern-performance-design`.

## Commands and results

- `node tests/mesh/pattern-performance/benchmark.mjs RUNTIME SOURCE OUT LABEL STYLE stl ROLE RUN`, executed sequentially for the three pairs above: PASS, exact byte parity.
- `node --test tests/node/pattern-performance.test.mjs tests/node/pattern-families-implementation.test.mjs tests/node/pattern-families-independent.test.mjs`: PASS, 25/25.
- `uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -q`: PASS, 9/9.
- `node projects/laifen-wave-case/openscad/run_math_probe.mjs`: PASS, all existing `VFR04_*` witnesses present.
- `/Users/scottchu/.asdf/shims/npm run build:openscad-simulator --workspace laifen-wave-case`, run from the repository root: PASS, 20 modules in 517 ms. This command had no `--outDir`; despite the initial “isolated build” label, it wrote directly to `preview/openscad-wasm-simulator/dist` before review.
- Final process audit: no pattern benchmark process remained active.

## Build-boundary correction

The unreviewed candidate `dist` was first preserved intact at `/tmp/pattern-performance-implementation/candidate-dist` (six files, including `index.html` SHA `3845efdea8db81003569971cfb2b2594c5c783b0de96dc46323b22204b1ecafa` and `index-glg6xAxA.js` SHA `a5866ab371b6d46b4916a5bb56e89e810043b5ff1a6a32941b812750d72c0d71`). No compiler was run during rollback.

The prior reviewed R2 artifact manifest `/tmp/pattern-families-full-r2/candidate-artifacts.sha256` passed before copy. Its exact six-file `dist` then replaced the accidental build; a path/size/SHA comparison against the reviewed source directory passed:

| Restored file | Bytes | SHA-256 |
| --- | ---: | --- |
| `index.html` | 12,964 | `a3f7c3300d772c4c2e6477c773bdcd3e4163621e9da36ec2c128189ed312f130` |
| `assets/index-DIOcam4t.js` | 561,639 | `d60fe5e20dc8ef8c60663b81ca112a66cf9bcb7e0e108a919fa55c684f4ba0d8` |
| `assets/index-iRxz8EXK.css` | 7,133 | `bb0c812317830060d51da5e56d7412a8b911cf75ab6ddc7c68c588e5285ace67` |
| `assets/openscad-CutNEzGH.js` | 124,567 | `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` |
| `assets/openscad-DIKIGOy4.wasm` | 9,603,115 | `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26` |
| `assets/openscad.worker-Csx1v_-i.js` | 1,823 | `cf543214d381e56ac230d6853810786ae70c52977d408e64695db595574fd46e` |

The live artifact directory is therefore back at the previously reviewed R2 bytes; candidate build artifacts remain scratch-only pending independent review and authorized delivery.

## Coverage and limits

- PERF-01/PERF-02: implements the measured shared wave bottleneck with exact-output evidence; all five paths were audited by DESIGN, while unchanged Smooth/Diamond are intentionally not rewritten.
- PERF-03/PERF-05: no internals, controls, worker/runtime/lock, cancellation, output transform or service path changed.
- PERF-04: stage timings and exact artifacts are reproducible with the durable runner; independent paired medians remain required.
- PERF-06: no STEP, slicer, fit, strength, grip or physical acceptance claim.

Next action: freeze the three changed implementation paths, then run distinct PERF-VAL and PERF-CRIT against that exact candidate before formal review or delivery.
