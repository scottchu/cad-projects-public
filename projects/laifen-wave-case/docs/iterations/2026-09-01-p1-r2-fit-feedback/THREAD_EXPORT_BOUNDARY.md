# CVAL-03 mouth-boundary diagnosis

Owner `/root/thread_export_validate`, independent validation continuation, 2026-09-01. R2 baseline `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`. Verified all59 entries of `inputs/coupon-fixed-candidate.sha256` before and after: unchanged fingerprint `3da2cac2b8d29b379b3be6309e3b7eb623fc50f6766dd5a573438a49517f6e4d`.

**Disposition: local mouth-boundary difference PASS against the unchanged0.01mm contract; exact parity is false.** The anomaly is a pre-existing source BREP trim-range defect that the STEP round trip changes. It is not merely volume-integration noise. The affected source edge extends below its Z0 topological vertex; the written/imported edge stops at approximatelyZ0. This supersedes CVAL-02's uncertainty about whether that particular area discrepancy reflects changed trimming. Complete four-part/global boundary parity, other assembly exports and physical acceptance remain outside this focused result.

## Concrete finding

The C20 mouth face is a cylinder of radius17.6, vertex Z extent0..1, with15 unique boundary edges in both representations. Its area was104.26063384581829mm2 in source and104.19255670531636mm2 after STEP import.

Source mouth edge7 is a nonrational degree4 B-spline with8 poles/3 knots. Its parameter range is0..1. Its final 3D curve point is `(15.894587800104269, 7.557914968083225, -0.008715486393865796)`. Its associated surface p-curve reaches that same negative Z. The corresponding topological vertex is at `(15.894552855204806, 7.557988458119648, 0)` with tolerance0.008715866281130259mm. That large vertex tolerance explains how ordinary topology checks can report valid while the curve endpoint and nominal mouth plane disagree.

The matching written/imported edge8 retains the same underlying B-spline geometry but changes the trim interval to approximately`[2.2263686709454047e-8, 0.9709483780722801]`. Its endpoint is at Z=-1.9701459609897013e-10; its Z0 vertex tolerance is8.139643081955159e-5mm. Maximum matched 3D boundary discrepancy occurs on this edge:0.008715486196876739mm. Distance from the source's negative-Z curve endpoint to the nearest written mouth boundary is0.008715486393865796mm.

Thus the round trip trims away an approximately0.008715mm source-edge extension. The original source already contains the inconsistency; this is not evidence that serialization introduced a new large functional thread shape. This task did not separate STEP writer behavior from importer healing, so the responsible round-trip stage remains unidentified.

Other matched 3D edges differ by at most1.20722021e-7mm in the initial101-point-per-edge correspondence samples. For those unaffected pairs, lifted p-curve differences are at most1.07897072e-7mm. The largest same-representation 3D-edge versus lifted-p-curve mismatch is approximately3.4843e-5mm on another thread-intersection edge; it is present in both source and STEP. The source/STEP radius differs only by floating-point rounding. These observations distinguish the dominant trim-range change from smaller p-curve approximation effects.

## Bound against the contract

The follow-up checks every one of the15 matched edge pairs with a continuous normalized-parameter correspondence, covering each complete trimmed edge interval. Pairing is bijective; all pairs preserve parameter direction. A correspondence upper bound also bounds bidirectional set distance, since every point in either interval has a corresponding point on the other.

For each edge pair, letL be the sum of the two maximum normalized-parameter speeds. Lines/circles use their exact analytic speed. Nonrational, nonperiodic B-splines use the maximum norm of the derivative control points, with the actual expanded knot sequence and parameter-range scale. By the B-spline convex-hull property this bounds curve speed throughout the interval. ForN equal parameter intervals, the unsampled maximum correspondence distance is at most the sampled maximum plusL/(2N). N is chosen to make that additional term<=0.0002mm; it is an error-bound budget, not a relaxed acceptance threshold.

Across1,289,725 point pairs, the maximum resulting whole-edge upper bound is **0.008915379530528766mm**, on source edge7/written edge8. It is below0.01mm by0.001084620469471234mm. That pair uses1,480 samples andL=0.5912844809426967mm per normalized parameter. The bound incorporates gaps between samples; unlike CVAL-02's finite ray list, this is a continuous bound for the compared mouth 3D edge sets. Double-precision arithmetic and OCCT curve evaluation are used; this is not an interval-arithmetic proof or a whole-solid surface certificate.

No assumption of exact source/STEP equality, zero Boolean difference, or arbitrary mass tolerance is used. CVAL-02's radial-section and g6 results remain valid and separately scoped. The local trim change is below the contract, but it consumes most of that tolerance and should not be silently inherited as a clean source boundary.

## Required next action and acceptance limits

**Medium source-quality finding:** the female mouth construction produces a tolerance-supported trim endpoint outside its intended mouth plane. Before treating the R3 inherited helper as canonical, its implementation/design owner should ensure the authoritative female BREP curve ranges end at their actual boundary vertices/planes before export, and add a focused edge-endpoint-versus-mouth regression. Repair must preserve the female profile/clearance and intended Z0 plane; increasing vertex tolerance or relying on STEP healing would hide the defect. This validation task prescribes the failing condition and required outcome, not an untested source-edit algorithm.

The supplemental scratch body reconstruction reproduces the same approximately-0.00871549mm endpoint before grip/label addition, suggesting the thread/relief Boolean is responsible. It uses literal rounded17.6 in place of the source's floating expression17.4+0.2, so it is supporting localization only and is not an exact source-stage proof. The primary finding above comes directly from the frozen generator's actual final solid.

No CAD/source, tests, STEP, configuration, requirements, runtime or dependencies changed. No exports, meshes, snapshots or printer actions occurred. The R2 grip remains superseded; there is no new visual or physical acceptance. R3 should repeat the affected boundary gate on its own generated source and STEP after any correction. Whole-solid source/export parity remains unclaimed.

## Commands and evidence

From repository root using its uv-managed Python3.12:

- `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/coupon-fixed-candidate.sha256 > projects/laifen-wave-case/scratch/thread-export-validation/cval03-before.txt`: all59 OK.
- `uv run python projects/laifen-wave-case/scratch/thread-export-validation/cval03-probe.py > projects/laifen-wave-case/scratch/thread-export-validation/cval03-probe.txt 2>&1`: exit0; 3D/p-curve samples, edge types/ranges/tolerances, matching and `cval03-results.json`.
- `uv run python projects/laifen-wave-case/scratch/thread-export-validation/cval03-bound.py > projects/laifen-wave-case/scratch/thread-export-validation/cval03-bound.txt 2>&1`: exit0; derivative bounds, endpoint/vertex diagnosis, `cval03-bounds.json`, final59-entry hash verification.

Both processes completed; no owned stalled process remains. Exclusive changes are this receipt and `scratch/thread-export-validation/cval03*`. Root maintains continuity indexes.

SHA-256: `cval03-probe.py`6708bb9ac84e352887bb62251e063331d062d4446c2268d6171f80a0621be06a; `cval03-probe.txt`11c5dc2163879f705c7ae1934b2ecba783427e54b8765ac8bec15c3a7d202cb2; `cval03-results.json`df892e490a0c45a35f07e7d702e8e48c93f618a6367cd51bd9da4a3d50767f62; `cval03-bound.py`177d4222cabd1a51752640a33946c6ed0aca5de8ce7ace784013e839151ed6e4; `cval03-bound.txt`3c436474b3d0f2785f24ede7bd45d812e9db6ae76f1bb521b7b2761e7b066755; `cval03-bounds.json`82d4010e7e8e09c5583bc1d1f24a40b706a9b2082523a8f6d851953ff65735c1.
