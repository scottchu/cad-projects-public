# DES-PITCH-07: partitioned female-void construction recovery

Frozen scope, 2026-09-02. Project `projects/laifen-wave-case`; iteration `2026-09-01-p1-r3-algorithmic-skin`; baseline `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`. The 53-entry default candidate remains frozen at `inputs/geometry-default-candidate.sha256`, fingerprint `4e1ea38ac083f2f9b708770165bb2281748f129826f1f50bd1782139484a9ffd`. This task changes no canonical geometry, parameters, tests, native tolerances, artifacts, or acceptance state.

## Diagnosis

The guarded nondefault case is `p=2.4`, `E=7.2`, `C=82.1`, `H=47`, with all other short-grip values unchanged. It satisfies the scalar parameter domain: neck height is10.8, root16.8, crest17.4, cap inner radius15.5, collar end12.24, and cap straight start14.44.

The frozen pre-guard source has valid positive one-solid tools through construction: infinite female thread volume18081.9826108392, clipped thread intersection volume12479.433178089756, and relief volume37990.34449828889mm3. The failure is precisely the overlapping `threaded.fuse(relief)` stage: its result is valid but has zero solids, zero faces, and zero volume. `clean()` cannot proceed. The outer cap is otherwise valid and positive, volume49809.93560526339mm3. This is a Boolean construction failure, not an infeasible pitch, a functional-interference result, or a reason to narrow the published pitch domain.

## Selected smallest construction correction

Preserve the existing `infinite_thread`, its `-p..neck_height` clipping cylinder, the relief meridian, all functional radii, thread pitch/engagement/lead math, and the DES03 mouth ownership rule. Replace only the overlapping cutter-union operation with a partitioned subtraction from the cap blank:

1. Build `threaded` and `relief` exactly as today.
2. Form `thread_residual = threaded.cut(relief).clean()`. It represents only thread-tool material outside the relief; it must be valid and contain positive volume before use. It may have more than one solid, because it is a cutter set rather than the final cap.
3. Build the unchanged outer cap blank and subtract `relief`, then subtract every solid in `thread_residual` in a deterministic order; clean only the final cap. Do not fuse overlapping cutters. Mathematically, this is `outer \ (relief union threaded)` with the overlapping portion removed before Boolean application.

This is selected because a scratch probe makes a valid one-solid, positive p2.4 cap: volume13903.736874997805mm3,23 faces, and its axis point `(0,0,5)` is void. It does not alter physical dimensional inputs or hide the rejected behavior with a guard/tolerance change. Direct sequential subtraction of the two overlapping original cutters was rejected: it perturbs the default untextured cap by0.265584923mm3. The partitioned route changes the comparable frozen-stage default untextured volume by only0.000693049760mm3, so the implementation must prove default functional geometry with actual sections and the existing default gates; it must not claim byte or BREP-face identity.

## Focused implementation and regression gates

The distinct implementation owner may edit only the shared female-void construction and its focused tests/candidate evidence. Keep the present defensive error for any failed construction; do not remove it. Before a general-pitch claim, run:

```sh
uv run python projects/laifen-wave-case/scratch/pitch-diagnosis/stage_probe.py
uv run pytest -q projects/laifen-wave-case/tests/test_generator_geometry.py
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --preset short-grip --thread-pitch 2.4 --engagement 7.2 --cavity-length 82.1 --cap-height 47 --write-step --target cap --output-dir projects/laifen-wave-case/scratch/pitch-recovery-output
```

The focused test must inspect actual solids, not scalar radii alone. For p2.4 it must record finite positive thread residual, final valid one-solid cap with positive volume, a void axis witness, and no `Infinity`/empty tool. For the unchanged default C20/C25/C30 it must rerun the established actual radial thread/bore sections, mouth-plane edge checks, positive shoulder stop, and written-STEP validity/count checks. Preserve the default design dimensions and clearances; compare computed sections to the same normalized profile within the current0.01mm geometry tolerance, while retaining DES05 mouth limits. Do not replace these with a volume-equality assertion or a new arbitrary BREP tolerance.

After the focused candidate is frozen, a distinct validator must repeat p2.4 actual-solid and written-STEP checks plus the unchanged default gates; a distinct critic/formal reviewer must join the same candidate. Passing this recovery only validates the named p2.4 case and default preservation gates. It does not validate the full pitch domain, slicer behavior, physical fit, wear, or full Laifen design.

## Boundaries

`inputs/pitch-recovery-inputs.sha256` binds the unchanged default manifest, frozen mouth-stage source, recorded pre-guard failure, this immutable snapshot, and the diagnostic script. Scratch alternatives are evidence only. Coupon implementation, independent default export validation, CAD artifacts, source/tests/configuration, and runtime services remain excluded. Stop if the partitioned cut cannot preserve actual default functional sections or if it needs a changed dimension, a widened/narrowed domain, native tolerance edit, guard removal, or a broader thread rewrite.
