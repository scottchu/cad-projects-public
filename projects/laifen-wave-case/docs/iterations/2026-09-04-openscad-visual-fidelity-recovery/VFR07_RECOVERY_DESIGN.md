# VFR-07 syntax-first recovery design

Status: **READY — recover attempt 2 through scratch-only preflight; no geometry candidate exists yet.**

Owner: `/root/openscad_vfr07_recovery_designer`, independent recovery-design role. Sole write: this document.

## Provenance and decision

`inputs/VFR07_RECOVERY_DESIGN_INPUTS.sha256` verified **11/11 OK** at fingerprint **`ffb1d5bf59b3a6381b7b747e4843825a43c98f8ebf0c59c0e9214194fdc00b39`**.

Attempt 2 is structurally sound enough to use as the recovery seed. Its diff contains the selected VFR-06 period-three lattice, numeric owner/carry records, edge/face clipping, compaction, endpoint rings, unequal-ring zipper, direct body/cap arrays and retained final Boolean operations. Attempt 1 failed at line 246 on an unsupported `assert ... each` sequence; attempt 2 made the local expression-form correction and parsing advanced. Attempt 2 then failed at line 259 because `v06_disk` lacks one outer-list closing `]`. The exact retained diagnostics are:

```text
attempt1: ERROR: Parser error: syntax error in file /probe.scad, line 246
attempt2: ERROR: Parser error: syntax error in file /probe.scad, line 259
```

This is evidence for recovery from the transcription, not for its types, array shapes, geometry, topology, accuracy or speed. Do not regenerate the architecture unless a scratch gate proves the seed cannot express VFR-06 within the delta below.

## Allowed delta

The recovery owner may work in `scratch/vfr07-implementation/`, then transactionally replace only:

- `openscad/laifen_case_customizer_v1.scad`; and
- the VFR-06 implementation-string assertions in `tests/test_openscad_customizer.py` needed to describe the new production data path.

Start from the exact attempt-2 SHA `47d0db738e9691e4441d212ba58810cea02f47abca8efbb803d085ae91e7c2e9`. Before authoritative integration, edits to its VFR-06 blocks may only correct parser syntax, expression typing, list/record shape, lazily reached assertion form, or a direct transcription mistake demonstrated by a scratch probe. Each correction must record the failing probe, old/new fragment and why its numeric meaning is unchanged.

Preserve relationship B; all dimensions, parameters, tolerances and time/triangle thresholds; the VFR-06 knot/owner/clipping/direct-shell architecture; the `1e-10` developed-coordinate equivalence and `1e-8` output quantization; source-emitted geometry authority; smooth/depth-zero behavior; rejection rules; threads, drains, transforms and output modes. Browser files, worker/runtime/vendor bytes, UI/schema, services, continuity, prior evidence and generated artifacts are forbidden. Host code may inspect SCAD-emitted arrays but may not create, repair or substitute geometry.

## Scratch preflight

Create `scratch/vfr07-implementation/candidate.scad` and `candidate-test.py`, plus a pinned-WASM `run-preflight.mjs`. The runner must read the stated scratch source, remove only the final top-level dispatch at its unique `if (VFR04_PROBE_MODE == "short_band")` sentinel, append the stated SCAD probe verbatim, and invoke the unchanged vendored `openscad.js`/`openscad.wasm`. It writes JSON containing source/probe hashes, return code, diagnostics, echo bytes and timings. Any parser error, OpenSCAD warning, failed assertion, `undef`, nonfinite value, absent marker, or nonzero return stops the stage.

From the repository root, use:

```text
cd /Users/scottchu/.codex/worktrees/4f8c/design-projects
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR07_RECOVERY_DESIGN_INPUTS.sha256
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR07_RECOVERY_DESIGN_INPUTS.sha256
uv run python -B projects/laifen-wave-case/scratch/vfr07-implementation/verify-delta.py
for stage in 00-parse 10-address 20-clip-ownership 30-mesh-data 40-profile-zip-direct; do node projects/laifen-wave-case/scratch/vfr07-implementation/run-preflight.mjs --source projects/laifen-wave-case/scratch/vfr07-implementation/candidate.scad --probe projects/laifen-wave-case/scratch/vfr07-implementation/probes/$stage.scad --out projects/laifen-wave-case/scratch/vfr07-implementation/receipts/$stage.json || exit 1; done
uv run python -B projects/laifen-wave-case/scratch/vfr07-implementation/verify-preflight.py
```

The gates are cumulative and cheap failures stop all later work:

| Gate | Required proof |
|---|---|
| `00-parse` | Pinned WASM parses the complete candidate, so every new function and module definition is syntax-checked. Its first permitted edit is only the missing `v06_disk` list terminator. |
| `10-address` | Directly invoke every leaf/config/address/point/edge helper, including both sides and equality branches. Require expected scalar/vector types and lengths, valid slot ranges and carries, intentional `undef` only, finite values, and unchanged period-three/count/phase facts. |
| `20-clip-ownership` | Directly invoke every record, cell, intersection, clipping, cleanup, area, center, owner and prefix helper on the VFR-06 vertex/edge/axial/interior/coincident fixtures. Require stable owner aliases, bounded polygon size, positive retained areas, exclusive ranks and no nonconsecutive duplicate owner. |
| `30-mesh-data` | Directly invoke every data/ring/index/disk/closed-band helper for the exact G2 band, trimmed G2 band and `v=-0.5..0.5` coincidence case. Require point records of length 3 XYZ, triangular integer faces with three distinct in-range indices, ordered closed rings, no unused emitted slots and source-emitted compact summaries. This is type/shape evidence only; no STL is written. |
| `40-profile-zip-direct` | Directly invoke every profile, reversal, internal-ring, angle, zipper and direct body/cap helper. Cover unequal rings, equal-angle events, wrap and nonzero diamond phase while the 96-ring datum stays fixed. Require well-shaped finite points/faces and the unchanged profile endpoints. Force default body arrays within the inherited 10 s V06-1T ceiling. No `polyhedron`, Manifold call or mesh file is permitted. |

`verify-preflight.py` must compare the set of all modified `diamond_*` and all `v06_*` function definitions against the probes' declared `exercised_helpers`; equality is mandatory. Modules are covered by the full-file parse and later geometry gates. It must also prove every receipt names the same candidate SHA and pinned vendor hashes. A scratch type/shape repair reruns its failed stage and all later stages. Stop rather than broaden the delta if a repair changes a VFR-06 formula, dimension, threshold, topology class or protected region.

## One authoritative integration and candidate budget

Only after all scratch stages pass, use one transactional integration command:

```text
uv run python -B projects/laifen-wave-case/scratch/vfr07-implementation/integrate.py --source projects/laifen-wave-case/scratch/vfr07-implementation/candidate.scad --test projects/laifen-wave-case/scratch/vfr07-implementation/candidate-test.py
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
cmp projects/laifen-wave-case/scratch/vfr07-implementation/candidate.scad projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad
shasum -a 256 projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad projects/laifen-wave-case/tests/test_openscad_customizer.py
```

`integrate.py` must stage both files, verify the allowed delta and exact scratch hashes, replace them without running an intermediate consumer, and restore the frozen baseline on any exception. A mismatch, authoritative parse/test failure or protected-region mismatch stops VFR-07; do not patch authoritative source to repair a failed preflight process.

The first source/test hashes after this gate define **candidate C1**. Run the inherited V06-1, V06-1 boundary/annulus, V06-1T, V06-2, V06-3B0, V06-3B, V06-3C and V06-3P gates unchanged and in order. Scratch preflight does not consume C1 because it emits no mesh and makes no authoritative change.

C1 has **one focused geometry repair total**. It may correct one diagnosed local owner/carry formula, finite clipping case, polygon fan, annular zipper or avoidable template-evaluation defect while preserving the architecture and every protected contract. Freeze a new source/test fingerprint, rerun the failed gate and every dependent gate. A second geometry failure, any timeout, an unbounded/global search, a needed architecture change, a relaxed threshold, host-generated geometry, or a browser/worker change ends the budget and records: **browser OpenSCAD diamond blocked under the 0.025 mm / 60 s contracts**.

No browser enablement or delivery follows until distinct critic, validator and formal-review identities join on the same V06-3P candidate fingerprint. CAD, written artifact/slicer and physical acceptance remain separate and pending.

## Receipt

- Status: recovery design complete; implementation not started.
- Verified fingerprint: `ffb1d5bf59b3a6381b7b747e4843825a43c98f8ebf0c59c0e9214194fdc00b39`, 11/11 entries.
- Attempt-2 disposition: recover through scratch preflight; do not accept or regenerate yet.
- Changed path: this document only.
- Output SHA-256: reported with the worker return because a file cannot contain its own final digest.
