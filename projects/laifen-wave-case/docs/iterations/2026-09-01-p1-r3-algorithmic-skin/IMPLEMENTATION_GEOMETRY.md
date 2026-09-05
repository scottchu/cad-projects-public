# IMP-GEN-01b bounded patch implementation receipt

Owner `/root/generator_core`, 2026-09-01. Disposition: STOP at bounded patch after initial attempt plus one focused repair; no complete part or accepted geometry. Surface-route78 inputs verified, fingerprint `a2141125f5c48a39f7491cb601e289ebad276fde4c54690c82697e01840b5a40`. Core75 candidate `44a343bfb2fe89692b887d990a166d0229015a39491ad2e6210591730d43eca2` remains reconstructible from `inputs/geometry-core-baseline/`. Read DES03 mouth prescription and completed CVAL03 evidence; neither thread/config repair nor full generation began.

## Candidate and bounded attempts

Added `cad/p1_r3_generator/surface.py`: algebraic power/Bernstein conversion, rational circular sectors, degree7 fade, affine diamond patches, polygon clipping, exact curve substitution, shared vertex/edge cache, explicit p-curves, sewing/solid gate and representative closed coupon construction. The exact scalar field remains authority. No prior core module, R2 source/artifact, configuration or existing test was modified.

Initial probe `uv run python projects/laifen-wave-case/scratch/generator-core/patch-probe.py` stopped at112 faces against the prescribed100 ceiling. All surfaces/edges in that attempt had been constructed, but sewing was UNATTEMPTED; there was no validity, normal, plateau or actual-surface-deviation result. The observed failure was exclusively the face-count gate, not evidence of invalid geometry. No precise initial timing was captured. Its intended full coupon covered two sectors across the seam, the adjacent smooth-cylinder strip, fade and a whole axial cell interval. Temporary inner closure duplicated outer subdivisions, contributing avoidable faces.

One focused repair replaced those inner subdivisions with two exact cylinder sector faces, preserving boundary vertex splits. This failed before sewing while constructing a canonical inner boundary edge. Exact live repaired source is preserved in `inputs/geometry-failed-variants/surface-repair.py`; initial source is reconstructed there from the recorded edit, with its provenance limitation explicit.

## Concrete repair failure

Read-only diagnostic command: `uv run python projects/laifen-wave-case/scratch/generator-core/patch-failure-diagnostic.py`; exit1. It only wraps the edge method to report the unchanged failure.

At the seam, logical keys `('inner',0.0,3.82)` and `('inner',31.0,3.82)` refer to the same physical point. The key expression rounds after modulo; a coordinate just below the seam becomes31.0 after rounding rather than0.0. The perimeter splitter admits both keys and creates identical UV endpoints `(1.0,0.8305882352941175)`.

Affine line substitution then produces constant homogeneous polynomials:

- X16.9;
- Y-6.938893903907228e-17;
- Z18.336000000000002;
- W1.0.

Thus the attempted rational Bezier edge has degree0, one pole `(16.9,-6.938893903907228e-17,18.336000000000002)`, weight1. OCCT rejects it with `OCP.OCP.Standard.Standard_Failure` in `Geom_BezierCurve(poles,weights)`, called from `Builder.edge` via construction of the first temporary inner cylinder. The diagnostic reached38 faces and94 canonical edges in0.038747709 seconds, with maximum observed shared vertex/curve discrepancy1.464821375527116e-14mm before failure. Those are construction diagnostics, not global geometry acceptance.

Smallest next correction requires a reopened task: normalize seam keys after rounding and deduplicate identical perimeter endpoints; preserve actual coordinates and all true crease vertices. No tolerance increase, skin coarsening or full geometry redesign is suggested. The initial count-only failure can alternatively be reconsidered with an explicit revised bounded coupon cost gate; this worker has not changed its ceiling.

## Evidence and acceptance boundary

Saved outputs: `scratch/generator-core/patch-probe.txt`, `patch-repair.txt`, `patch-failure-diagnostic.txt`; diagnostic script and both source variants preserved. No valid solid was returned, no STEP or mesh was exported, no mandatory snapshot could apply, and no viewer/print acceptance is claimed. Actual skin deviations, normals, plateau width, shared-shell topology, whole parts, threaded path, mouth correction, source/STEP parity and physical tests remain unexecuted. The original five core tests remain the earlier analytic/CLI evidence only.

The authorized Playwright dependency plan was not executed because geometry stopped first; root/project configuration and root lock remain unchanged. Root owns continuity state and any new bounded dispatch. The next manifest binds this failed candidate and its evidence without rewriting historical manifests.
