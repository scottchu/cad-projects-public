# Pattern performance independent validation — PERF-VAL

Status: **PASS for the bounded performance, exact-output, source/state, isolated-build and browser-artifact gates**.

## Frozen provenance

- Baseline commit: `7f15b1649a5d83c77512c9ba0864943ac68996b6`.
- Corrected design input manifest SHA: `4a0d35663c572177fcf8c588654651aad7675fabd2c23c436393363bf842711c`.
- Candidate 43-path manifest: `inputs/candidate-source.sha256`, SHA `3888018275bfcd05ab1d66a27d5b29a01eaf7268382075f4e2bd2047cc638c4c`; verified before work and after deterministic gates.
- Validator-owned frozen baseline/candidate copies: SHA `3b96cc2d5a5100e2daa2fe5a14c21e510728f108cfbc9afd5ae80bf1ef5dde40` / `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`.
- Runtime: JS `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e`; WASM `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26`.

Only the shared wave edge no-cut predicate and uncut-face fast path changed. Density, phase, clipping, guards, UI, worker, dependencies and output format are unchanged.

## Independent paired performance gate

Runner command shape, once per fresh process:

```sh
node projects/laifen-wave-case/tests/mesh/pattern-performance/benchmark.mjs \
  /tmp/pattern-families-full-r1 SOURCE OUT LABEL STYLE stl ROLE RUN
```

The validator used24 sequential fresh processes: three alternating baseline/candidate pairs per primary case with the middle order reversed, then one pair for each regression audit. Every receipt independently rechecked the expected source SHA and pinned runtime hashes. Every baseline/candidate STL pair is byte-identical.

| Case | Baseline callMain ms | Candidate callMain ms | Reduction | Cohort spread baseline/candidate | Gate |
| --- | ---: | ---: | ---: | ---: | --- |
| Rings body | 26631.020 | 19316.696 | 27.47% | 6.04% / 6.83% | PASS >=20% |
| Spiral body | 26769.413 | 19334.986 | 27.77% | 2.91% / 0.69% | PASS >=20% |
| Spiral assembled | 46639.293 | 33498.782 | 28.17% | 3.74% / 2.88% | PASS >=15% |
| Smooth body | 211.554 | 211.231 | 0.3ms faster | one pair | PASS |
| Diamond body | 2701.408 | 2701.923 | 0.5ms slower | one pair | PASS |
| Ribs body | 1065.322 | 1000.138 | 65.2ms faster | one pair | PASS |

Primary values are medians; raw times and initialization/compiler-render/read/write stages are in `/tmp/pattern-performance-validation/bench/summary.json`, SHA `9019242dd2f7ac06743da1c00882f63d8e3bd79d2a13dc0779897de1cc6b6dad`. All spreads are below15%; no noisy rerun or fastest-run selection was used.

## Exact-output correctness and reused geometry evidence

Seven additional fresh baseline/candidate pairs passed exact expected-hash parity: default Ribs/Rings/Spiral caps, edited Diamond body, non-round Spiral stress body/cap, and the near-allocation Rings body. Receipt SHA: `742a354600cc098e4e362f7f92f1207edad5b670c94be8bbf47d3ade6cb22c9b`.

The timed default hashes are Rings body `d1b73da0bc2a0dfe479cb89b81e51c3fc608cba53e8487d202b2c1e0405fa849`, Spiral body `548562863c900775241caec1239ee54ede9e5c4f07e664dc5ae4c1c8deb20e1c`, and Spiral assembled `10774d307cac4199687d02a5777f5fd084064ffb68821e256d0d496fc1384277`. The regression audit also preserves the exact Smooth, Diamond and Ribs default-body hashes.

Because every written byte matches the source-hash-bound21-mesh matrix in pattern-families `FULL_VALIDATION.md` SHA `62213c2c1c554cbf8eae78d43583b56e8ca7ff7542f7c9f4be0ba4f54f7801e5`, its actual-solid certificates apply unchanged. This explicitly carries forward:

- **Math:** exact phase, clipping, vertex/face ordering and the <=0.025mm field-error witnesses.
- **Constraint:** closed positive oriented solids, zero invalid edges/degenerates, exact seam rings, protected bores/threads/floors and seven drains.
- **Collision:** default Spiral assembled has two components, zero nonadjacent intersections/T-junctions and part-sum volume delta `5.82e-11mm3`; matching bytes preserve that result.
- **Requirement:** all five paths, cap roles, four-role assembled witness, edited Diamond, stress tuple and allocation boundary retain exact output.

No global mesh rescan was repeated because there is no byte mismatch to invalidate those certificates.

## Focused source/state/build gates

```sh
node --test projects/laifen-wave-case/tests/node/*.test.mjs
PYTHONDONTWRITEBYTECODE=1 uv run pytest \
  projects/laifen-wave-case/tests/test_openscad_customizer.py \
  projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -p no:cacheprovider
npm run build:openscad-simulator --workspace laifen-wave-case -- \
  --outDir /tmp/pattern-performance-validation/dist --emptyOutDir
```

Results: Node59/59; Python13/13; isolated build20 modules in513ms. The focused proof checks that exact cone equality implies all skipped samples are uncut, preserves the original cut interpolation, and rejects epsilon predicates. Lifecycle, current-download identity, family controls and source guards remain covered. The build wrote only scratch dist; live8453 was not changed by this validator.

## Root-owned isolated browser join

Root served the validator-built scratch dist at `http://127.0.0.1:8462/` and generated the exact default Rings Body tuple at1280x900 in Chrome. The final state retained Rings, Body, 3D view, `Preview up to date` and a current Download. The isometric screenshot is `/tmp/pattern-performance-validation/browser-preview-isometric.png`.

The current Blob was **39,958,888 bytes**, SHA `d1b73da0bc2a0dfe479cb89b81e51c3fc608cba53e8487d202b2c1e0405fa849`. The validator independently rehashed the actual downloaded `/Users/scottchu/Downloads/container-body-1a7c82e2bca0.stl` to the same size and SHA; verification receipt SHA `9d6725fbac6b9312d1c6ff546cd06164d862dcad44f255dbf7402d2cd479506d`. That is also the exact paired/certified Rings-body hash above.

The cold browser run took minutes and the compiler reported a nested render interval of10.652s. Neither is used as a speedup claim; only the controlled fresh Node pairs establish performance.

## Evidence boundary

The 67-entry evidence manifest is `/tmp/pattern-performance-validation/ARTIFACTS.sha256`. Receipt audit `/tmp/pattern-performance-validation/receipt-audit.json` SHA `cf0bf89800e0403e5ce56c61d3d7513ac82bc6a87ae5b207808269338c99f1d0` independently verifies source/runtime/hash provenance across all38 fresh compile receipts.

This validation demonstrates bounded runtime improvement and exact ASCII STL preservation. It does not establish STEP, slicing, grip, drainage-in-use, cleaning, thread wear, fit, print or physical acceptance. Formal review must join this receipt with the distinct critic and root-owned browser evidence before delivery.
