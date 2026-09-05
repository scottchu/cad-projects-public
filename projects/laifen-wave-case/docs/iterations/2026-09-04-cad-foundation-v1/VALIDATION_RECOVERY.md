# VAL-CAD-CV1-02 recovery validation

**Owner:** `VAL-CAD-CV1-02`  
**Role:** fresh independent recovery validator  
**Status:** **PASS** — the bounded missing independent chain named by
`VAL-CAD-CV1-01` is complete for unchanged candidate
`6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`.

This is not formal review, slicer/process acceptance, or physical acceptance.
No candidate source, generated STEP, P1 R7 oracle file, package environment,
simulator/live route, STL/3MF, slicer state, or printer state was changed.

## Provenance

Commands ran from repository root
`/Users/scottchu/.codex/worktrees/4f8c/design-projects` using root `uv`.

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-04-cad-foundation-v1/inputs/frozen-inputs.sha256
```

Result: **PASS**, 57/57 entries. Manifest SHA-256:
`1c233c8c64f0e7cb87919b601435318f6402a96cd3ad19af0fdb7251e908ed83`.

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-04-cad-foundation-v1/candidate-files.sha256
```

Result: **PASS**, 27/27 entries. Candidate manifest SHA-256:
`6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`.

```sh
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-cad-foundation-v1/inputs/frozen-inputs.sha256 projects/laifen-wave-case/docs/iterations/2026-09-04-cad-foundation-v1/candidate-files.sha256 projects/laifen-wave-case/docs/iterations/2026-09-04-cad-foundation-v1/evidence-files.sha256
```

Result:

```text
1c233c8c64f0e7cb87919b601435318f6402a96cd3ad19af0fdb7251e908ed83  .../inputs/frozen-inputs.sha256
6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304  .../candidate-files.sha256
0214bd39e094aed9bf84a0cfedde97cb795a2a946ccb7cd25bb84c989f250acc  .../evidence-files.sha256
```

## Recovery Harness

Scratch harness:
`projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/recovery_harness.py`.

First resumed execution reached report construction and exited **code 1** with
only a harness serialization error:

```text
TypeError: '<' not supported between instances of 'GeomType' and 'GeomType'
```

Focused repair used: **1/1**. The repair stringified `GeomType` keys in the
report's surface census. It did not change candidate source or geometry.

Final command:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run python projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/recovery_harness.py > projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/recovery_harness.json 2> projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/recovery_harness.stderr
```

Tool result: **exit code 0**. Output JSON SHA-256:
`74fd816da9aa312c0aa86bc2a91b7ceff3ed36350440d7b04b451812d79d9b79`.

## Completed Missing Gates

### 1. Native old/new cap equivalence — PASS

The harness built the immutable P1 R7 native cap and new
`container_generator_v1` native cap from source. Under the frozen tolerances
of `1e-6 mm` and `0.001 mm3`, results were:

| Probe | Result |
| --- | ---: |
| Solids | 1 old / 1 new |
| Faces | 6,396 old / 6,396 new |
| Edges | 12,348 old / 12,348 new |
| Vertices | 5,956 old / 5,956 new |
| Adaptive volume, eps `1e-10` | `34973.25083372612 mm3` old and new |
| Volume delta | `0.0 mm3` |
| Max bounds delta | `0.0 mm` |
| Max centroid delta | `0.0 mm` |
| Rounded vertex set | identical at 7 decimal places |
| Surface census | identical |

`VAL-CAD-CV1-01` already completed native old/new body equivalence. This
recovery intentionally did not rerun old body.

### 2. New source-native to actual written STEP parity — PASS

The harness used `build123d.import_step` on the actual candidate files
`cad/container_generator_v1/body.step` and `cap.step`.

| Part | Source volume | Written STEP volume | Delta | Max bounds delta |
| --- | ---: | ---: | ---: | ---: |
| body | `65470.38706421227` | `65470.38707347599` | `+0.000009263720130547881 mm3` | `6.885159109515371e-12 mm` |
| cap | `34973.25083372612` | `34973.25082611402` | `-0.000007612099580001086 mm3` | `6.885159109515371e-12 mm` |

Both deltas pass the required adaptive-volume parity tolerance
`<=0.001 mm3` and bounds tolerance `<=1e-6 mm`.

### 3. Named joint, datum, and assembly placement probes — PASS

Native source datums matched the frozen contract.

| Part | Datum Z values |
| --- | --- |
| body | `shoulder=0`, `tip=9`, `full_thread_start=2`, `full_thread_end=8`, `skin_phase=0`, `bed=-135`, `inner_floor=-132` |
| cap | `shoulder=0`, `tip=9`, `full_thread_start=2`, `full_thread_end=8`, `skin_phase=0`, `bed=84`, `inner_floor=81` |

Native closed placement probe:

- solid count: `2`
- bounds:
  `[-19.500000100000012, -19.498274041206887, -135.00000010000042]`
  to
  `[19.500000100000026, 19.49827404120689, 84.0000000999998]`
- outer length: `219.00000020000022 mm`
- body print translation: `(23, 0, 135)`
- cap print translation/rotation: `(-23, 0, 84)`, `Rx180`

No-sibling hard links were created under
`scratch/container-generator-v1-validation-recovery/inspection/` and verified
by inode and SHA-256. The hard links have the same inodes as the candidate
STEP files:

```text
29051813 body.step / body-written.step
29051852 cap.step / cap-written.step
29052133 closed.step / closed-written.step
29052248 print_layout.step / print-layout-written.step
```

CAD CLI written-STEP probes:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/inspect refs projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/inspection/closed-written.step --facts --planes --positioning
PYTHONDONTWRITEBYTECODE=1 uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/inspect refs projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/inspection/print-layout-written.step --facts --planes --positioning
PYTHONDONTWRITEBYTECODE=1 uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/inspect frame projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/inspection/closed-written.step '#o1.1'
PYTHONDONTWRITEBYTECODE=1 uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/inspect frame projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/inspection/closed-written.step '#o1.2'
PYTHONDONTWRITEBYTECODE=1 uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/inspect frame projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/inspection/print-layout-written.step '#o1.1'
PYTHONDONTWRITEBYTECODE=1 uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/inspect frame projects/laifen-wave-case/scratch/container-generator-v1-validation-recovery/inspection/print-layout-written.step '#o1.2'
```

Results: all six commands exited **0**.

- closed refs: exact candidate hash
  `cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2`,
  2 leaf solids, 16,651 faces, bounds Z `[-135, 84]`, size
  `39 x 38.996548 x 219`.
- closed frames: `#o1.1` body translation `(0,0,0)`, +Z axis; `#o1.2` cap
  translation `(0,0,0)`, +Z axis.
- print-layout refs: exact candidate hash
  `cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b`,
  2 leaf solids, 16,651 faces, bounds Z `[0,144]`, size
  `85 x 38.996548 x 144`.
- print-layout frames: `#o1.1` body translation `(23,0,135)`, +Z axis; `#o1.2`
  cap translation `(-23,0,84)`, local +Z mapped to world `-Z` by `Rx180`.

### 4. Openings-up and no-internal-roof probes — PASS

The recovery harness sampled the written print-layout solids on their axial
voids. Every sample reported `inside=false`.

Body print pose:

- bounds Z: `[-1e-7, 144.0000001000008]`
- center X: `23`
- source-axis void samples: `Z=-131.9`, `-80`, `-1`, `4`, `8.5`

Cap print pose:

- bounds Z: `[-1.0000000224110364e-7, 84.0000001]`
- center X: `-23`
- print-pose void samples: `Z=3`, `30`, `70`, `83.9`

The body and cap mouth samples just below the written print-pose top surfaces
also reported outside material, confirming both openings face upward. These
probes check the axis void/opening relationship only; they do not replace
slicer support analysis or physical print validation.

## Reused VAL-01 Evidence

As directed, this recovery did not rerun dense/global self-intersection,
broad test suites, or all four `inspect validate` commands. It relies on
`VAL-CAD-CV1-01` for already completed evidence covering:

- native old/new body equivalence;
- manifest integrity and implementation evidence fingerprint;
- permitted serialization-only STEP variance;
- actual-written validity/refs;
- thread-zone zero intersection and minimum clearance;
- OD, bores, drains, chamfer, layout, and related source/export facts.

## Limits

This PASS closes only the missing independent recovery chain for the unchanged
candidate. It does not assert physical fit, thread durability, print quality,
tall-part stability, actual drain behavior, slicer support-free proof, or
identity of the user's previously printed artifact. Those remain HOLD exactly
as recorded in the project state and implementation receipt.

Next action: formal independent review may join this recovery PASS with
`CRIT-CAD-CV1-01` and `VAL-CAD-CV1-01` for the same candidate fingerprint.
