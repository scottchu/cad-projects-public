# VFR-06 implementation receipt

Status: **BLOCKED — two candidate V06-0 failures; frozen source and tests restored.** Browser OpenSCAD diamond is **blocked under the 0.025 mm / 60 s contracts**. This attempt did not reach executable mesh-data, topology, accuracy or timing evidence. The block follows the nonrenewable implementation budget; it does not establish that the selected mathematical architecture cannot work or that its runtime exceeds a limit.

Owner: `/root/openscad_vfr06_impl`, sole implementation role. Task: VFR-06-I. Worktree: `/Users/scottchu/.codex/worktrees/4f8c/design-projects`. Project: `projects/laifen-wave-case`. Decision: `VFR06_ARCHITECTURE_DECISION.md`; task: `VFR06_IMPLEMENTATION_TASK.md`. No implementation self-approval is given.

## Provenance and retained scope

Input manifest `inputs/VFR06_IMPLEMENTATION_INPUTS.sha256` verified at **`13001ed4600bb85000b2b11cb518aea264933db744ba22f86cf4112c49e8b04d`**. All 13 entries passed before implementation and again after restoration. Authoritative SCAD is restored to **`4e6ccd68f95d583d0c3b93bc33442d01107af90b5e66267bfe20034732e0d672`**. The focused test is restored to **`9dfbe2421a4daec6f614a5292e7804cb62f351b50ae37d65ce917daaf3b39c8a`**. The original entire source, including all protected field, rejection, smooth, thread, drain and output-transform bytes, is preserved by this equality.

Attempted source introduced the selected period-three knot lattice, B/edge/face numeric slot descriptors, sector carries, axial/trim clipping, owned polygon centers, divide-and-conquer prefix, endpoint ring ownership and direct body/cap profile construction. The candidate was incomplete as evidence: parsing failed before any new function executed. Its mathematical, alias, topology, accuracy and performance properties remain unverified. The attempted test edit replaced the old polyhedron implementation-string assertion with new data-function/no-global-search assertions; it was restored with the source.

Retained new files are this receipt and `scratch/vfr06-implementation/` only. `openscad/generated_vfr06/` was not created. Browser/UI/schema/worker/vendor/runtime/lock files, Python oracle, prior evidence/artifacts, CAD/STEP, slicer, services and printer were not changed. No Diamond enablement, deployment, generated mesh, snapshot or Viewer action occurred.

## Ordered execution and stop

All pytest commands below ran from the worktree repository root using root `uv` Python 3.12.13:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
```

| Run | Result | Observed command wall time | Disposition |
|---|---|---:|---|
| Frozen baseline | 14 passed | 0.161997 s | Baseline cheap checks passed. |
| Initial candidate / attempt 1 | 13 passed, 1 failed | 0.201304 s | Executable pinned-OpenSCAD math regression failed parsing at line 246. Attempt consumed. |
| Sole focused repair / attempt 2 | 13 passed, 1 failed | 0.136287 s | Parsing advanced and failed at line 259. Second attempt consumed; stopped. |
| Restored baseline | 14 passed | 0.282471 s, measured with Python monotonic clock | Restoration gate passed. |

The first three timings are recorded tool command wall times, not mesh timing. The fourth comes from the retained subprocess receipt. No 10 s, 20 s, 30 s or 60 s geometry/worker performance result exists.

**Attempt 1, high severity:** `v06_ring` placed `assert(...)` immediately before list-comprehension `each []`, an unsupported parser sequence. Exact diagnostic: `ERROR: Parser error: syntax error in file /probe.scad, line 246`. The one repair changed this to an `each` expression with a conditional and an assertion returning an empty list. No geometry or architecture change was attempted.

**Attempt 2, high severity:** the next parser error is in `v06_disk` at line 259: the outer list comprehension is missing its closing square bracket. Exact diagnostic: `ERROR: Parser error: syntax error in file /probe.scad, line 259`. No second repair was applied, even though the immediate parse defect is localized. The failed source is retained as noncandidate evidence.

The two read-only diagnosis invocations, from the repository root, were:

```text
node projects/laifen-wave-case/scratch/vfr06-implementation/run-data.mjs projects/laifen-wave-case/scratch/vfr06-implementation/attempt1-parse 'echo("parse");'
node projects/laifen-wave-case/scratch/vfr06-implementation/run-data.mjs projects/laifen-wave-case/scratch/vfr06-implementation/attempt2-parse 'echo("parse");'
```

Both returned code 1 and a 97-byte diagnostic echo; there was no source-emitted mesh data. The new scratch harness reads the exact production source, omits only top-level dispatch for a private expression, and uses the pinned unchanged vendor OpenSCAD/WASM. Attempt 1 initialization/evaluation/total were 22.972 / 15.163 / 38.135 ms; attempt 2 were 25.117 / 17.252 / 42.370 ms. These are parser diagnostics, not successful data proofs or browser worker tests.

Verification commands from the project root:

```text
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR06_IMPLEMENTATION_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR06_IMPLEMENTATION_INPUTS.sha256
```

The final verification output is retained at `scratch/vfr06-implementation/restored-input-verification.txt`; restored pytest output is in `restored-pytest.txt`. `gate-receipt.json` records commands, result categories, timings and restoration provenance. After the second failure, `cp` preserved `attempt2.scad` and `attempted_test_openscad_customizer.py`, then copied `frozen.scad` and `frozen_test_openscad_customizer.py` back to their authoritative paths. No downstream gate ran after either failure.

## Noncandidate evidence hashes

Project-relative evidence manifest: `scratch/vfr06-implementation/EVIDENCE.sha256`, SHA-256 **`0ddc3e8090f4791cae04f18088ac0cec6088f7ccb4cb9d77b8d0cd8f65fc45ca`**. It covers both failed source snapshots, the attempted test, frozen restoration backups, source drafts, private harness, parse diagnostics/timings and restored checks.

| Evidence | SHA-256 |
|---|---|
| `scratch/vfr06-implementation/attempt1.scad` | `cad9140dc33d921f03d480a216d9e4f1ffe373693f23e153ec0b5b9d254d3525` |
| `scratch/vfr06-implementation/attempt2.scad` | `47d0db738e9691e4441d212ba58810cea02f47abca8efbb803d085ae91e7c2e9` |
| `scratch/vfr06-implementation/gate-receipt.json` | `e2ef291a709399d330134e75d500bc3a4489b721f5b7b39050465aa30dae43ff` |

These files are failed implementation evidence, not accepted source or release artifacts. No source-to-artifact-to-independent-review candidate chain exists for VFR-06-I.

## Requirement coverage, unresolved risks and next action

- V06-0 input provenance and baseline/restored regressions passed; both candidate V06-0 executable regressions failed.
- V06-1 source-emitted topology/ownership/affinity/error proof: **not run**.
- V06-1 boundary/annulus/profile/seam fixtures: **not run**.
- V06-1T default-body array cost: **not run**.
- V06-2 real G2 / V06-3B0 direct body / V06-3B actual worker / V06-3C cap: **not run**.
- V06-3P smooth geometry comparison, candidate hash freeze and independent join: **not reached**. Full-source byte restoration and the cheap depth-zero/rejection tests passed, which is not a newly measured geometry comparison.
- B intent, mathematical contract, protected source and prior evidence remain frozen. No new CAD, artifact/slicer or physical acceptance is claimed.

Next action belongs to the root: record the blocked outcome in continuity and retain Diamond disabled. This task has no remaining repair authorization. Any future change requires a separately explicit scope/budget decision; these syntax failures must not be described as an executed topology or performance disproof. Independent candidate critique/validation/review cannot advance without a compiling candidate and its prescribed source-emitted evidence.
