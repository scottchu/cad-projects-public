# VAL-R6-02 independent repair validation

Owner `/root/case39_validate`, independent validation role, 2026-09-02. **VAL-R6-02A/B PASS for the repaired default source/CAD and written-STEP gates.** The repaired native source and standalone cap meet the unchanged0.001mm3 parity limit, and the final closed/layout occurrences match the validated standalone parts. VAL-R6-01-F01 is resolved for repaired candidate145 identified below. This independent validation receipt supplies the affected deterministic gates; the distinct critic and formal reviewer still own their visual and final acceptance join. Original `VALIDATION.md` remains historical evidence of the prior failure.

## Phase A provenance and scope

Production cap-ready143 manifest `scratch/fullcase-export-repair/production/cap-ready.sha256`, SHA256 `92aeb54c592d2b0d6c98914f7b4bb6e4de58871dca9795deb716ae83e329ae42`, verified before and after. Corrected cap STEP SHA256 `5b47075e5ee27dc57b8089c7955856e15119b8a7692569c2f0f532d4a21f4afe`; body SHA256 `b5d425acecb35a57264e4267b7958608af289d2975c53c6d94c059083226fbdd` unchanged. Closed/layout generation was still in progress and those official STEP files were not read in Phase A.

Own task inputs152 were frozen before geometry execution in `scratch/fullcase-validation/repair/cap-inputs.sha256`, SHA256 `17698609d89708bb4f8e047d77c49be1ad6f56c27072cd77743f29a903772f3d`; all152 were reverified after completion. They bind candidate paths/manifest, independent scripts/plan, original validation/trial receipt and archived defective source BREP. Cap evidence11 is frozen in `repair/cap-evidence.sha256`, SHA256 `71be300136f9e3441bd5fe4ba2126a5755b2f298c682c3fe208bcda33b723645`.

Read-only candidate, source and artifacts. Writes only the validator's new repair scratch, this receipt and validation manifests. No source/STEP regeneration, parameter/tolerance adjustment, environment/service/Git/slicer/printer action. Root owns continuity and the distinct critic/formal reviewer roles own visual and final acceptance gates.

## Native defect regression and helper safety

Independent `endpoints.py` selects cone/helical-BSpline shared edges by geometric role and inspects all3D/pcurve ranges plus the stored vertex parameter; it does not call the implementation's defect selector. Archived original cap has exactly one endpoint defect: residual0.002561321256401561mm at vertex[-16.1585575799622,5.74660916846158,9]. Production helper changes range[0,1] to[0,0.9988497584922102], consistently in3D and both pcurves; stored vertex parameter agrees. Corrected residual5.872301100285205e-8mm satisfies1e-7.

All native vertex coordinates remain exactly equal, original tolerance0.00256132140603368mm is retained, face count6593 and one-solid validity remain intact. Original input endpoint records, all vertices and adaptive volume remain unchanged after normalization, demonstrating topology isolation. Applying normalization a second time returns the same corrected shape without further mutation. A real two-witness compound is rejected with `multiple upper-runout defects need separate diagnosis`.

Source inspection confirms only the targeted native range and stored vertex parameter are updated on an isolated topology copy. Guards limit one defect, correction residual<=0.01mm, projection residual<=1e-7, projection inside the existing parameter range, noncollapsed edge and trim fraction<=1%. No face index, global healing, underlying curve/surface or coordinate change, tolerance reduction, or STEP-roundtrip normalization is used. Rejection branches other than the real ambiguity case were inspected in source, not represented as additional runtime tests.

New production cap rebuilt independently in memory also has a consistent source endpoint residual5.87230055801866e-8mm. Imported exact new cap has residual5.872334454253297e-8mm; its3D/pcurve ranges and stored parameter agree. Its imported tolerance is3.3939133e-5mm; this ordinary import representation is recorded separately from the unchanged native before/after tolerance. Both source and written cap are valid single solids with6593faces and nominal39x38.996548x84 bounds. All eight source datum/joint names are present.

## Original parity criterion

Method unchanged: `BRepGProp.VolumeProperties_s(shape.wrapped, GProp_GProps(), eps, True, False)`. Rows were recorded before assertions; no loose default-volume acceptance or threshold relaxation.

| eps | Source mm3 | Written mm3 | Difference mm3 | Source / written returned error |
|---|---:|---:|---:|---|
|1e-8|35022.740705324|35022.740682047726|0.000023276275897|5.96491519476e-9 /5.96466056853e-9|
|1e-10|35022.740669795305|35022.740655030386|0.000014764918888|1.01751737089e-10 /1.01745663000e-10|

Both differences are below0.001mm3. The earlier approximately0.00380mm3 defect is not waived; the new native trim fixes the reproducible discrepancy on this exact repaired cap.

## Affected and retained geometry gates

- 130 actual written cap radial probes across upper full form/runout/tip/relief/taper satisfy the independent selected radius law, maximum error0.000042712520mm (<0.001 focused comparison). No thread dimensions or axial datums changed.
- 792 written exterior probes across all33 angular repeats and critical end/seam/upper-runout/long-cap stations match archived old cap radii exactly (maximum delta0). Independent exterior law error<=0.000201451mm, outward normals and sampled slopes<1. Original comprehensive exterior evidence remains applicable because skin/surface/parameter source hashes are unchanged and the targeted mutation affects an internal runout edge.
- At cap printZ0.01/0.20 the actual written sections have1 connected material face,8 wires and7 radius1.5 circles. Areas1091.908306405735/1101.617112775421mm2 are exactly equal to archived old cap sections. Prior deep floor/drain evidence is retained via unchanged source functions and this changed-artifact check.
- Actual repaired cap against unchanged body using shared-Z clipping:0/90/180/360/720degrees with matching gaps0/0.5/1/2/4mm and open10mm all yield0mm3 intersection. Overtravel−18degrees/−0.1mm yields23.747774760907383mm3, confirming positive stop. No full-body common was used.
- Independently compared prior input hashes: body.step, params.py, thread_profile.py, skin.py, surface.py, review.py and body.step.py are byte-identical. AST comparisons against archived old parts.py show add_datums, drain_centers, drain_cutters, build_body, build_assembly and print_layout unchanged. Only build_cap adds the targeted normalization call. Thus prior body topology/parity/bores/floors, global math/field, nominal device-envelope and unchanged source placement evidence are retained rather than rerun. New assembly occurrences still require their own written-artifact check.

## Commands and results

Repository root, root UV/Python3.12, non-login shell:

```sh
uv run python projects/laifen-wave-case/scratch/fullcase-validation/repair/cap.py > projects/laifen-wave-case/scratch/fullcase-validation/repair/cap.log 2>&1
uv run python projects/laifen-wave-case/scratch/fullcase-validation/motion.py --manifest projects/laifen-wave-case/scratch/fullcase-export-repair/production/cap-ready.sha256 --fingerprint 92aeb54c592d2b0d6c98914f7b4bb6e4de58871dca9795deb716ae83e329ae42 --cad projects/laifen-wave-case/cad/p1_r6_full_case --output projects/laifen-wave-case/scratch/fullcase-validation/repair/motion.json > projects/laifen-wave-case/scratch/fullcase-validation/repair/motion.log 2>&1
shasum -a 256 -c projects/laifen-wave-case/scratch/fullcase-validation/repair/cap-inputs.sha256
```

Cap command exit0,186.99s; motion exit0,188.06s. First independent execution succeeded; no validation-method repair. Source rebuild outer30.11s/Boolean59.66s stays below600s stage limits. Preservation results are recorded in `repair/preserved-inputs.json`; candidate and own manifests supply exact hashes.

## Phase B final candidate and occurrence checks

Full repaired145 manifest `inputs/implementation-repaired.sha256` SHA256 `a3873490fc7d7742698d9d73aceb6a8a29131fd8b846c76973d7133afb438bdc` was verified before and after the final occurrence command. Its body/cap and source hashes preserve the exact Phase A candidate. Final task inputs158, frozen before Phase B, are in `inputs/validation-repair-inputs.sha256`, SHA256 `3679717b59d3eeca3f3bfbb7cf98967106b304a2557e8e43bb37dfbd8062fab7`. Final evidence is bound in `inputs/validation-repair-evidence.sha256`.

| Final artifact under cad/p1_r6_full_case | SHA256 |
|---|---|
| body.step | b5d425acecb35a57264e4267b7958608af289d2975c53c6d94c059083226fbdd |
| cap_c25.step | 5b47075e5ee27dc57b8089c7955856e15119b8a7692569c2f0f532d4a21f4afe |
| closed_c25.step | 31e4125fcfc6d6c543312491298d8a508f0d2db9a5da247b6a933b6fa7d3efa6 |
| print_layout.step | be27b1c7962bcc241babea257aa85b11bc1675b83072f475bf684e865d166410 |

```sh
uv run python projects/laifen-wave-case/scratch/fullcase-validation/repair/occurrences.py --manifest projects/laifen-wave-case/docs/iterations/2026-09-02-p1-r6-full-case/inputs/implementation-repaired.sha256 --fingerprint a3873490fc7d7742698d9d73aceb6a8a29131fd8b846c76973d7133afb438bdc > projects/laifen-wave-case/scratch/fullcase-validation/repair/occurrences.log 2>&1
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-02-p1-r6-full-case/inputs/validation-repair-inputs.sha256
```

The occurrence command exited0 in48.44s, without a cap rebuild or broad rerun. New closed and layout each are valid two-solid/17177-face assemblies; each constituent has a closed shell and positive adaptive volume. Closed body/cap volumes65524.00259379072/35022.740655030386mm3 exactly match standalone written parts. Placed body/cap volumes in the layout65524.00259379106/35022.7406550304mm3 exactly match transformed references. All occurrence volume differences are0; bidirectional vertex distances are0 except cap print placement2.97e-27mm.

Closed dimensions39x38.996548x219 and print layout85x38.996548x144 hold within kernel tolerance. BodyT(+23,0,135) and capT(−23,0,84)*Rx180 remain single placements, bedsZ0, openings up,7mm nominal crest-envelope separation. No device reference or duplicate part enters the two fabrication assemblies.

## Final disposition and evidence reuse

VAL-R6-01-F01 is **closed for repaired candidate145**, based on independently passing source/STEP adaptive parity at both prescribed eps settings and correct final occurrences. The historical failure on candidate135 remains documented in VALIDATION.md; it is not retrospectively erased or waived. The unchanged body/source hashes and function comparisons explicitly retain prior body parity/topology, full dimensional math, bores/drain floors, fixed skin equations and nominal device-reference evidence. Reopened cap runout/native safety/parity/motion/exterior/floor/occurrence gates pass as documented here. No change to the physical requirement interpretation or0.001 threshold was used.

Scoped default source/CAD and written STEP deterministic gates PASS; this receipt is ready for the distinct critic/formal-review join. Slicer/process and physical acceptance remain pending as documented in the original validation. No hardware fit, strength, retention, literal both-end noncontact, five-cycle durability or drying claim follows from this export fix. Root may now join this immutable receipt with the critic's affected-artifact confirmation and final formal review. No further validator rerun is needed unless a declared candidate input changes.
