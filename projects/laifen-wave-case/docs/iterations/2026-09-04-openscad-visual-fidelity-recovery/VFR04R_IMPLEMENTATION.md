# VFR-04R implementation receipt

Status: **G2 PASS; G3 BODY BLOCKED BY TWO 60-SECOND TIMEOUTS; CAP NOT RUN.**

Owner/role: `/root/openscad_vfr04_impl`, sole VFR-04R implementation owner. This is implementation evidence, not independent approval.

## Frozen input and bounded change

Verified `inputs/VFR04R_IMPLEMENTATION_INPUTS.sha256` before editing. Its SHA-256 was the expected `6fa066049022c113cd3d2d3ec46618a4272daca92d1792895d609db3961db2fd`; all ten entries were `OK`. Selected design was `VFR04R_DESIGN.md` at `8214330a757f458a9a34121d745359c17bece5d50576b3bd08813d690363b524` as recorded in the manifest.

Only the authorized SCAD clipping/index/triangulation/ramp-split region changed. The analytic oracle, existing tests, field helpers, parameters, smooth/depth-zero paths, envelopes, protected internals, output transforms and every browser file remain unchanged from the frozen inputs. New evidence is confined to `scratch/vfr04r-implementation/`; `openscad/generated_vfr04r/` is empty because no G3 part passed.

Current hashes:

```text
4e6ccd68f95d583d0c3b93bc33442d01107af90b5e66267bfe20034732e0d672  openscad/laifen_case_customizer_v1.scad
390ab34f5c14979fe9613202bcab440794cb1eba90397fa39c41d5e41aa54c1b  openscad/customizer_contract.py
9dfbe2421a4daec6f614a5292e7804cb62f351b50ae37d65ce917daaf3b39c8a  tests/test_openscad_customizer.py
363bcfdb85ab3ef27951c2d6e45c1a7c769e532c5489215c39d4071cb429ac37  tests/test_openscad_wasm_simulator.py
5ca9d71af0ba34a9f3bf1aa25980079035b6911f44522593cc958f42d5f37827  scratch/vfr04r-implementation/g2-short-band.stl
b7ebdfbc2007947896c6c1eaa8b45d9453ccaa35eca9859c8a637fd01688c17f  scratch/vfr04r-implementation/measure-g2.py
7e43a878800f91387dff0950cee20d8748089e71231b4056e7b51fbe43f8e862  scratch/vfr04r-implementation/g2-metrics.json
```

## Implementation

The repair now:

- snaps each clip endpoint to the exact half-plane before classification and cleans consecutive/cyclic duplicates after every clip;
- retains closed `[0,N]` geometric support while assigning positive-area ownership by a half-open centroid rule;
- maps `u=N` to canonical `u=0` only in the developed-coordinate registry and evaluates each canonical point once;
- splits every ramp once at its original constant-u midpoint, inserting the corresponding lines in plateau boundaries when they intersect;
- triangulates every cleaned convex child from its true-field interior center, preserving all perimeter subdivisions;
- builds axial end fans from cleaned side-boundary segments using the same canonical indices and corrected positive winding.

The first G3 timeout was diagnosed inside the allowed region: the broad `(i,j)` bounding box constructed many cells whose transformed support could not intersect the finite band. The one focused repair adds an analytic cell-center/support rejection before patch creation. It reduced the identical G2 wall time from `9.589` to `4.192` seconds without changing its measured topology or error behavior.

## G1 and protected-region evidence

Command:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py \
  projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
```

Result before geometry and again after the focused repair: `14 passed`. This retains executable N33/half-up/wrap/field/patch/seam/width/slope witnesses; smooth/depth-zero equivalence; thread roots/clearance/entry relief; bores, chamfer source, drains, output identities, real pinned-WASM path, timeout, mobile layout, toast, stale-state and exact-download assertions. The oracle and both test files retain their manifest hashes above. Source editing was patch-limited to the facet region beginning at `DIAMOND_UV_EPS` and the finite cell filter; no protected source region was modified.

## G2 passing witness

Exact command from repository root:

```text
node projects/laifen-wave-case/scratch/vfr04-implementation/run-wasm-export.mjs \
  projects/laifen-wave-case/scratch/vfr04r-implementation/g2-short-band.stl \
  'VFR04_PROBE_MODE="short_band"'
```

The same 7.13 mm full-circumference witness spans global Z `131.93..139.06`, with both axial boundaries off the shared seam-centered lattice. The final cold run used the pinned WASM Manifold backend and completed in `4191.640 ms` wall / `4169.642 ms` callMain, below the 30-second ceiling. STL size is `1,141,267` bytes.

```text
vertices / triangles               2,480 / 4,956
watertight / winding-consistent     true / true
face components / body count        1 / 1
Euler number                        2
volume                              8319.82297189639 mm3
edge incidence                      boundary0, nonmanifold0, maximum use2
minimum face area / degenerates     0.00198221749 mm2 / 0
bounds                              [-19.5,-19.49826809,0] .. [19.5,19.49826809,7.13]
side radial extrema                 19.04999999396 .. 19.50000000609 mm
analytic maximum error bound        0.00725582416 mm
random samples                      13,479, seed404, three per side triangle
sample error max / p99 / mean       0.00705172583 / 0.00578372285 / 0.00170072388 mm
midpoint+centroid checks            17,972; maximum0.00705186258 mm
angular-wrap midpoint/centroids     208; maximum0.00705185841 mm
required bound/sample maximum       <=0.025 mm
```

Worst random sample: face `4444`, sample `0`, point `[19.2137324105,-0.4586114616,5.4700025284]`, barycentric weights `[0.4967783200,0.5032153591,0.0000063209]`, field coordinates `u=-0.1253385834`, `v=0.5000005267`, expected radius `19.2262566422`, actual `19.2192049164`, error `0.00705172583` mm. Maximum analytic-bound witness: face `3134`, angular span `0.04759988904` rad, radius range `19.05..19.4015625034`, bound `0.00725582416` mm. Full machine-readable evidence is `scratch/vfr04r-implementation/g2-metrics.json`.

## G3 stop

Body command:

```text
node projects/laifen-wave-case/scratch/vfr04-implementation/run-wasm-export.mjs \
  projects/laifen-wave-case/openscad/generated_vfr04r/body.stl \
  'output_mode="body"' 'surface_style="diamond"'
```

Initial attempt passed 60 seconds with no result and was terminated; no body file was written. After the one focused cell-support repair and dependent G1/G2 reruns, the exact body command again passed 60 seconds with no result and was terminated; the output directory remained empty. Each timeout consumes its attempt. This is the second failure in the reopened budget, so no further optimization, body rerun, cap generation or G3 mesh/ligament/protected-geometry measurement was performed.

Gates: G1 PASS, G2 PASS, G3 BODY FAIL (timing), G3 CAP NOT RUN, G4/G5 OUT OF SCOPE. Browser diamond controls remain disabled. No candidate artifact, STEP/slicer/physical claim, service change or delivery action exists. The remaining blocker is full-part evaluation/Boolean performance under the unchanged 60-second ceiling; resolving it requires a newly frozen design or task rather than another retry in this workstream.
