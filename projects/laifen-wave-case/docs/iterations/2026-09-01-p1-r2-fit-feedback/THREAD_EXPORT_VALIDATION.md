# CVAL-02 independent thread/export diagnosis

Owner `/root/thread_export_validate`, validator only, 2026-09-01. Baseline `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`. Scope: frozen R2 four part source/STEP interface comparison and the previously failing g6 collision; the two-row skin is superseded by R3 and is not approved here.

**Disposition: limited interface section and g6 gates PASS; complete source/export parity remains UNRESOLVED.** No tolerances were loosened. This is not CAD release, mesh/slicer, visual, or physical acceptance. The shared thread is supported by the measured interface evidence, but R3 must validate its own written solids and must not inherit complete export acceptance.

## Provenance and execution

All 59 entries in `inputs/coupon-fixed-candidate.sha256` verified before and after execution. Fingerprint unchanged: `3da2cac2b8d29b379b3be6309e3b7eb623fc50f6766dd5a573438a49517f6e4d`. Read the original contract snapshot, COUPON_RECOVERY, IMPLEMENTATION_COUPON_RECOVERY, project continuity/requirements/experience/decision index, repository policy and installed CAD skill. No source, tests, STEP, configuration, requirements, runtime or R3 files were written. Exclusive writes: this receipt and `scratch/thread-export-validation/`.

Commands from repository root, root uv Python 3.12:

- `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/coupon-fixed-candidate.sha256`: all 59 OK, repeated after both probes; final output in `scratch/thread-export-validation/final-input-verification.txt`.
- `uv run python projects/laifen-wave-case/scratch/thread-export-validation/probe.py > projects/laifen-wave-case/scratch/thread-export-validation/probe.txt 2>&1`: exit 0, `LIMITED_GATES_PASS`; structured evidence `results.json`.
- `uv run python projects/laifen-wave-case/scratch/thread-export-validation/integration_probe.py > projects/laifen-wave-case/scratch/thread-export-validation/integration_probe.txt 2>&1`: exit 0. One focused follow-up; no source repair.

Both owned processes finished normally; no stalled process remains. No snapshot was generated: this is a read-only geometric diagnosis, no visible artifact changed, and the old appearance is superseded. Root owns continuity indexes and later review joins.

## Independent measured interface evidence

The probe uses OCCT line/face intersection, independent of the implementation test's binary solid-classifier method. It measures actual source and imported STEP boundaries, comparing them to the frozen min/max analytic thread envelopes. Eight angles (0,45,90,135,180,225,270,315 degrees) and 21 Z positions include leads, phase breaks, full-form boundaries and the failed male valleys: 168 samples per part, 672 total. Intersection tolerance is 1e-8 mm. This is a sampled error bound, not a global Hausdorff certificate; local solver tolerance is not a rigorous global numerical bound.

| Part | Worst STEP/contract radial error mm | Worst source/STEP radial difference mm | STEP minus source volume mm3 |
|---|---:|---:|---:|
| M | 0.000035964308 | 0.000000000005454 | -0.000282883807 |
| C20 | 0.000036377687 | 0.000033969752 | +0.392363683746 |
| C25 | 0.000036481034 | 0.000034068679 | +0.394336359277 |
| C30 | 0.000036584381 | 0.000034167606 | +0.397089428585 |

All measured errors are below the unchanged 0.01 mm profile contract. Worst contract sample is theta180/Z2.85; worst cap parity sample is theta0/Z8.5. The latter small nonzero discrepancy is reported rather than claiming exact equality.

All four written parts are one positive-volume solid, topology-valid and BRepAlgoAPI_Check-valid. Source/STEP face counts agree: M21, each cap360. Twenty ring-bore samples at five heights/four angles measure radius15 exactly; each cap's 12 main-bore samples measure15.5 exactly. Source datums are shoulder0, tip9, full-form2..8 and bed-8/25; matching written axial planes/extents were inspected: ring-8..9 with shoulder0, caps0..25 with interior label21.8/floor22. The full-form datums are corroborated by section samples, not asserted to survive STEP as semantic joint metadata. These are single-part placement checks; the five written assembly exports were outside this bounded task.

Written STEP interpart intersections at beta1080/g6 are zero for C20, C25 and C30, including the exact former 11.0734 mm3 defect pose. Negative closure g-0.02/beta-3.6 gives positive intersections4.429015145,4.318273992,4.207218672 mm3, confirming the external-stop regression is sensitive. This independently reruns the critical written pose, not all 30 source poses. Earlier source motion evidence remains separately attributed to CIM-02.

## Remaining export anomaly

C20 directional Boolean differences independently return zero solids and zero volume in both directions. That does not erase the volume discrepancy, nor establish a sub-0.01 mm global boundary-distance bound.

The focused second integrator uses `BRepGProp.VolumePropertiesGK_s`, adaptive Gauss-Kronrod with BSpline spans, at1e-7 and1e-9. At1e-9 source volume is8545.50539531394 and STEP8545.897785177933 mm3, delta0.392389863993 mm3. Returned relative error estimates are1.4627e-9 and1.5418e-9. The discrepancy persists across two quadrature algorithms and greatly exceeds their reported integration error. Merely tightening numerical integration is insufficient.

**Medium, unresolved:** a concrete localization is the inner mouth cylinder of C20, radius17.6 and vertex Z extent0..1: source face area104.26063384581829 versus STEP104.19255670531636 mm2, difference-0.06807714050193 mm2. Its underlying radius and Z extrema agree; the other eight cylinder faces' reported areas agree within approximately1.65e-7 mm2. This implicates trimming/representation around the mouth, but this probe has not distinguished an inaccurate 2D trim representation/integration from a localized real boundary deviation between the finite sampled rays. It therefore does **not** certify the mass delta as harmless representation-only error. The raw first probe's isolated-face volume diagnostics were exploratory and are not treated as additive volume evidence: individual faces are open, and their integration reference/closure requirements differ from the closed solid.

Next smallest task, only if complete R2/R3 export parity is needed: isolate the C20 radius17.6/Z0..1 face and compare its 3D trimming edges, associated surface p-curves and extrema across source/STEP; measure a bounded bidirectional boundary distance or repair the responsible generator/export operation, then rerun affected sections and g6. Preserve the current frozen candidate; no arbitrary mass threshold increase is justified. Full artifact/visual review, the other assembly transforms, R3 skin, support-free slicing, thread fit/wear and physical strength remain separate gates.

Evidence SHA-256: `probe.py` cdd33806990af88e34a4bbd6b64d2903efae6591f1ed472ed473b6719cd14d28; `probe.txt` 1700ef775b26304fb198fd056e77328ba1747d3aacf187916361a8c28404de81; `results.json` 60131da017092eb4f39b13f1dbfa7cfddb1485269a30768c3e845a1bee02f646; `integration_probe.py` cb64619b95506446bba6a782029bb78737faa460e33f12b6e118e4a5eb6b4e74; `integration_probe.txt` 7701ba44e97ccbcad0636d6cabcfd0afca1a3278cf2695ba8eb05ef223b04007. Scratch is reproducible diagnostic evidence, not a release artifact.
