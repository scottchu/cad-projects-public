# VFR-05A implementation receipt

Status: **STOPPED — G2 topology failed after the one permitted focused repair.**

Owner/role: `/root/openscad_vfr05_impl`, sole implementation owner. This is an
implementation receipt, not independent validation or approval.

## Frozen inputs and preserved authority

`inputs/VFR05A_IMPLEMENTATION_INPUTS.sha256` was verified at
`fea614a467f622919d2db6aaaa4572f26f00467c098d6cddccc5c875f638c152`.
The manifest's fourteen entries were `OK` before implementation and again after
the source restoration. The final source and focused test hashes are unchanged
from those frozen inputs:

```text
4e6ccd68f95d583d0c3b93bc33442d01107af90b5e66267bfe20034732e0d672  openscad/laifen_case_customizer_v1.scad
9dfbe2421a4daec6f614a5292e7804cb62f351b50ae37d65ce917daaf3b39c8a  tests/test_openscad_customizer.py
```

No browser/UI/worker, oracle, CAD/STEP, slicer, service, printer, or generated
body/cap candidate changed. `openscad/generated_vfr05/` contains no VFR-05A
candidate.

## Commands and gates

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py \
  projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
node projects/laifen-wave-case/scratch/vfr04-implementation/run-wasm-export.mjs \
  projects/laifen-wave-case/scratch/vfr05a-implementation/g2-short-band.stl \
  'VFR04_PROBE_MODE="short_band"'
```

The focused regression passed `14`. The temporary V05-1T data probe completed
in `6,714.093 ms` for the full body data setup and emitted `29` row templates,
maximum local polygon count `21`, maximum H/V/I table sizes `7/3/10`, `18,018`
outer points, and `35,574` side faces. It did not establish topology acceptance.

G2 candidate attempt one compiled in `494.812 ms` wall (`472.193 ms` compile),
producing `2,838` triangles. Mesh inspection found `268` boundary edges, `328`
nonmanifold edges, Euler `-428`, not watertight and not winding-consistent.

The one focused repair inserted the H-table subdivisions and ordered the endpoint
ring from the same local scalar ordinals. Its final G2 rerun compiled in
`558.768 ms` wall (`535.330 ms` compile), with `2,838` triangles. It removed all
boundary edges, but still had `277` nonmanifold edges, Euler `-336`, and failed
both watertightness and winding consistency. No degenerate faces were reported.

The artifacts are noncandidate evidence only:

```text
7af665f4f12c4e53a94c0475ecc6daffd5beafb0d224ac356c505c3aff1276b5  scratch/vfr05a-implementation/g2-short-band.stl
7af665f4f12c4e53a94c0475ecc6daffd5beafb0d224ac356c505c3aff1276b5  scratch/vfr05a-implementation/g2-short-band-repair.stl
c28b53d50562522b0bbe593c8299abe47362181c8519f8d599e6bcaa3b721dfe  scratch/vfr05a-implementation/g2-short-band-repair2.stl
```

## Findings and stop condition

The VFR-05A four-class index prototype bounded row/template lookup and met its
data-time checkpoint, but it did not fully reconcile every local patch edge.
The final result has multiply-used edges, so it cannot be a closed exterior,
direct annular body/cap, or G2 acceptance artifact. Attempt one was the initial
candidate G2; the H-table/ring-order repair was the single focused repair.
That repair still failed the same G2 topology invariant, exhausting the stated
budget.

G1 passed. V05-1T was informational only. G2 failed twice. G3 body, G3 cap,
V05-3P, G4 and G5 were not run. Source was restored rather than leaving a failed
candidate path active. The next action requires a newly frozen architecture or
task that specifies complete H/V/internal patch-edge conformity; an independent
role must validate any future candidate.
