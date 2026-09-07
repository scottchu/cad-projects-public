# Pattern performance design — PERF-DES
## Measured audit and decision
Source/runtime are frozen by BRIEF. Fresh default body measurements from the
pinned WASM in fresh Node processes, seconds (single exploratory runs):
| Path | CSG tree export | ASCII STL callMain | Compiler render |
| --- | ---: | ---: | ---: |
| Smooth | 0.028 | 0.207 | 0.180 |
| Diamond | 2.136 | 2.638 | 0.486 |
| Ribs | 0.753 | 1.035 | 0.286 |
| Rings | 24.652 | 27.167 | 1.401 |
| Spiral | 25.135 | 26.959 | 1.360 |
Initialization was about19ms. Rings ASCII output was39,958,888 bytes; memory
read/write were about12/13ms. Binary STL was8,025,184 bytes but callMain26.760s,
only1.5% below ASCII: do not change output format or worker for this candidate.
CSG export measures source evaluation plus tree-text emission, not pure evaluation;
compiler render is a nested reported interval, not an independently isolated CSG
stage. Do not subtract unrelated single runs to claim precise serialization cost.
Cumulative Rings source-only probes returning a tiny cube measured grid69,504
points0.960s; full277,632 slots10.186s; slots+prefix15.754s. Together with the
24.652s tree export these locate substantial work before solid rendering:
208,128 candidate edges repeatedly evaluate points and mostly yield undef;
`v06_prefix` still traverses every regular/empty slot. Faces/XYZ/tree emission
account for the remaining combined work, not a separately measured pure stage.
A scratch grid-cache variant preserved exact360-degree seam evaluation and all
CSG/STL bytes, but measured CSG22.119s and STL21.572s; variability requires paired
reruns. Prefer the smaller proven-no-cut fast path: if both edge endpoints have
`wave_cone(z,h,role)==outer_radius`, their field-minus-cone cannot be positive,
so the original edge cut is undef without evaluating its field points. The
scratch band probe measured CSG18.605s with identical5,125,335-byte tree output;
full Rings20.088s and Spiral20.080s retained exact baseline STL bytes (about26%
below their fresh baseline runs). These are exploratory, not delivered, speedups.
## First candidate: preserve exact output
Implement the no-cut fast path in the shared wave construction first. Retain
every slot, primitive ID, vertex/face order, arithmetic operation for surviving
points/cuts, existing wrapped-edge360-degree evaluations and quantization.
Do not use approximate z comparisons or epsilon-expanded cut bands. Evaluate
the same cone expression as the original source; equality to outer_radius is
the exact predicate establishing both signs are nonpositive for positive depth.
This improves Ribs/Rings/Spiral where applicable. Smooth and Diamond were audited
and are already fast; unchanged paths are an acceptable optimization outcome.
After paired measurement, one focused extension may remove credible remaining
prefix cost even if the initial target passes: base slots' rank equals their
index; prefix only the intersection suffix. A further sparse-cut representation
must preserve original surviving edge order and rank mappings exactly, with a
small independent equivalence witness before full compilation. An equivalent
uncut-face fast path may emit the same original triangle IDs/order directly.
Choose at most the smallest measured extension, within the two-repair ceiling.
Do not combine unmeasured rewrites merely because they look simpler.
No tessellation, revolve/twist, density, trigonometric identity, field/pitch,
phase, chamfer, thread, drain, UI-limit or output-format change belongs to this
first candidate. Any later representation that changes output geometry requires
a new design decision; the existing0.025mm error bound alone does not authorize
visible simplification or substitute for protected internals/seam evidence.
## Paired benchmark and acceptance
Before implementation, freeze baseline source from commit7f15b1649a5d83c77512c9ba0864943ac68996b6
to task scratch and verify SHA3b96cc2d5a5100e2daa2fe5a14c21e510728f108cfbc9afd5ae80bf1ef5dde40.
Never benchmark “baseline” by reading the mutable working source after edits.
Freeze candidate bytes separately. Use pinned JS904a47f2… and WASMf72ce246…
(full hashes in preceding family evidence), fresh process/factory per run, same
Node executable, argv, output role/tuple and idle machine. One benchmark at a time.
The exploratory runner is `/tmp/pattern-performance-design/bench.mjs`, invoked
as `node .../bench.mjs STYLE FORMAT VARIANT ROLE RUN`, formats csg/stl/binstl.
Its receipt records source/WASM hash, argv, initialization, callMain, output read
and write, bytes/hash and all compiler messages. Implementation must retain a
durable project-local runner with explicit frozen SOURCE arguments and verify
both JS/WASM hashes; no runtime assets or generated mesh belong in Git.
Run three alternating baseline/candidate pairs for default Rings body, Spiral
body and Spiral assembled; reverse pair order on the middle repeat. Report raw
times, medians and spread, not fastest runs. Target median callMain reduction
>=20% for each slow body and >=15% for Spiral assembled. The measured25% source
tree reduction makes these modest targets credible while leaving render cost
unchanged. If noise exceeds15% within either cohort, rerun only the noisy pair
after checking competing load; do not count that as a demonstrated improvement.
One before/after default-body pair audits Smooth/Diamond/Ribs for regressions;
allow at most max(10%,100ms) slowdown, otherwise investigate/repeat that path.
Keep total independent benchmark/regression work bounded to about15minutes.
## Correctness gate
Require byte-identical ASCII STL for every timed pair. Add exact baseline/candidate
parity for wave cap roles, an edited Diamond size/depth, the prior non-round
Spiral stress body/cap, and one near-allocation-boundary Rings body. Retain the
same tuple/role hashes from the prior21-mesh matrix where used; do not invent a
new exhaustive matrix. Default Smooth/Diamond functions must remain unchanged.
Exact written-byte identity reuses the prior mesh/feature certificates for those
identical artifacts; do not rerun expensive global scans without a new mismatch.
Any mismatch stops the exact-output route; inspect source/point/face differences
before considering geometry acceptance. No STL repair or relaxed certifier.
Run focused source/Node guard and lifecycle tests, isolated build, then observe
one slow-pattern actual browser generation/current download. Report Node compiler
timing separately from browser completion; browser validation retains ownership.
CAD/STEP, slicing and physical acceptance remain separate. Freeze source/evidence
manifests before independent critique and formal review; live8453 changes last.
