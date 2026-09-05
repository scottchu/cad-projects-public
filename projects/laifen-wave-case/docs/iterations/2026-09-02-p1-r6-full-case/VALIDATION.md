# VAL-R6-01 independent validation receipt

Owner `/root/case39_validate`, independent validation role, 2026-09-02. **Focused default source/CAD geometry gates PASS; written STEP parity HOLD.** Blocking finding VAL-R6-01-F01: the cap source-to-written adaptive volume difference is about0.00380mm3, above the frozen0.001mm3 maximum at both prescribed integration settings. The body passes. All unaffected measured full-size geometry, thread, motion, floor, placement and nominal-device gates below pass. This is not formal acceptance; the distinct critic owns mandatory snapshots and a separate formal reviewer joins evidence.

## Provenance and scope

Full candidate135 `inputs/implementation-candidate.sha256` SHA256 `4c2750ad632639be5547074173408aa14dfc579faed8d45890ed7233b00c0351` verified before work and again after completed focused scripts; all135 content hashes match. Preparation design116 `f72529fe2f5333e80859496453f720635590b11c46a55ec2bb2bc0c942f079b4` was also verified. Validation inputs144, including candidate paths, candidate manifest, independent plan and seven scripts, are frozen in `inputs/validation-inputs.sha256`, SHA256 `36718f6e48a51ab331b832d307126c26e734b5a5a81288a49826270bc25dbcf0`. Evidence is bound by `inputs/validation-evidence.sha256`.

Read-only candidate, source, tests and STEP scope. Wrote only `scratch/fullcase-validation/`, this receipt and validation manifests. No source repair, regeneration, mesh, slicing, printer/environment/service/Git action. Root owns project continuity indexes. Earlier R5 short validation was cancelled before geometry work when the user explicitly selected direct full CAD; cancellation is not a geometry failure and no short prerequisite is imposed here.

Exact full written artifacts:

| File under `cad/p1_r6_full_case/` | SHA256 |
|---|---|
| body.step | b5d425acecb35a57264e4267b7958608af289d2975c53c6d94c059083226fbdd |
| cap_c25.step | 7165de16ff6e8b1246b5fe654e0e023a90c2e6e226f721606731616b7c8cb6fc |
| closed_c25.step | 1b32f20cd81a5765bec7caa39870fded0f56aad660443acea790c260ee2d96f3 |
| print_layout.step | b147fd200524ca0471c5d22519e27fd27ad07d1a0311a10dd272a21da3efbe4b |

## Commands and execution boundaries

All commands from repository root, root UV/Python3.12, non-login shell. Independent scripts import the exact written `.step` files directly with build123d/OCC, without substituting adjacent wrappers. Source body and cap were separately rebuilt in memory.

```sh
uv run python projects/laifen-wave-case/scratch/fullcase-validation/validate.py > projects/laifen-wave-case/scratch/fullcase-validation/validate.log 2>&1
uv run python projects/laifen-wave-case/scratch/fullcase-validation/interface.py > projects/laifen-wave-case/scratch/fullcase-validation/interface.log 2>&1
uv run python projects/laifen-wave-case/scratch/fullcase-validation/motion.py --manifest projects/laifen-wave-case/docs/iterations/2026-09-02-p1-r6-full-case/inputs/implementation-candidate.sha256 --fingerprint 4c2750ad632639be5547074173408aa14dfc579faed8d45890ed7233b00c0351 --cad projects/laifen-wave-case/cad/p1_r6_full_case --output projects/laifen-wave-case/scratch/fullcase-validation/motion.json > projects/laifen-wave-case/scratch/fullcase-validation/motion.log 2>&1
uv run python projects/laifen-wave-case/scratch/fullcase-validation/parity_cap.py > projects/laifen-wave-case/scratch/fullcase-validation/cap-parity.log 2>&1
uv run python projects/laifen-wave-case/scratch/fullcase-validation/validate.remaining.py > projects/laifen-wave-case/scratch/fullcase-validation/remaining.log 2>&1
```

`validate.py` exited1 at the cap parity assertion after completed math/topology/source rebuild and passing body parity. Its first logging arrangement asserted before emitting the failed cap row. The cap-only diagnostic then recorded both settings and integration errors without early exit (exit0,67.46s); its exit0 means diagnostic completion, not parity PASS. `validate.remaining.py` completed unaffected gates (exit0,204.96s), without repeating source builds. Body source outer88.07s/Boolean87.34s and cap outer25.06s/Boolean30.48s stayed inside600s stage limits; shared-edge maximum mismatch1.142e-13/4.640e-14mm. Exact exterior counts10562/6569,total17131 are below16000 each/26000 total.

`motion.py` exited0 in86.52s. The first interface run established body joint identity, then was deliberately terminated (exit143) during an unnecessarily expensive cap textured-annulus difference, without a cap verdict. Preserved `interface.initial.py/.log/.json` contains that attempt. One focused method adaptation limited the cap identity mask to cylinder radius18,z0..12.5, which contains every functional thread/taper surface; the independent exterior/seam probes cover the omitted texture. Final `interface.py` exited0 in18.69s. Logging/continuation was the second focused method repair. No geometry tolerance or acceptance threshold was relaxed, and no source candidate changed.

## Blocking adaptive-volume finding

Method: `BRepGProp.VolumeProperties_s(shape.wrapped, GProp_GProps(), eps, True, False)`. The loose default build123d volume accessor was not used for acceptance. Integration-error columns below are OCC's returned estimates, not independently guaranteed absolute error bounds.

| Part | eps | Source mm3 | Written mm3 | Absolute difference mm3 | Source / written returned error |
|---|---:|---:|---:|---:|---|
| Body |1e-8|65524.00260981685|65524.002607848895|0.000001967957|6.63211197e-9 /6.63211210e-9|
| Body |1e-10|65524.00258791427|65524.00259379072|0.000005876449|7.57912590e-11 /7.57905434e-11|
| Cap |1e-8|35022.73688590875|35022.740682047726|0.003796138975|5.96491519e-9 /5.96466057e-9|
| Cap |1e-10|35022.73685038005|35022.740655030386|0.003804650332|1.01751737e-10 /1.01745663e-10|

**VAL-R6-01-F01, blocking written-artifact acceptance:** cap residual remains approximately0.00380 when tightening eps100x. This is a reproducible failure of the frozen parity gate, not proof of a specific serializer defect or gross mechanical defect. Root must route focused export-representation/parity diagnosis; do not loosen0.001, hand-edit STEP, or call this numerical noise without new evidence. The written cap occurrence has the same volume in closed/layout, so the cap-containing handoff remains on HOLD. Body parity and unaffected geometry evidence remain valid for their declared unchanged inputs. Root explicitly requested no further eps1e-12 probe at this stage.

## Measured gates and requirement coverage

| Gate | Independent evidence | Coverage / status |
|---|---|---|
| Full math and meaningful inputs |141+81−9=213 cavity;135+84=219 outside; body144/cap84. L+4.8 extends only body domain to[-139.8,0] while N33/pitch4.8/phase persist. D31 leaves bores30/31 and geometry domains fixed and reports radial gaps−0.5/0, demonstrating editable envelope rather than silent bore growth. Derived root wall1.4, female budget wall1.85, interlock0.20 worst/0.25 nominal, flank free travel0.35. | REQ01/03/05/06/08/09/12; PASS selected scalar contract, no nondefault CAD certification. |
| Actual topology and dimensions | Body10584faces and cap6593faces, each1 valid positive solid with closed shell. Closed/layout17177faces, exactly2 case solids. Measured native geometry gives144/84/219 heights and layout85x38.996548x144 within numeric tolerance. N33 permits Yspan below39; maximum radial crest is separately measured. No diagnostic device in primary artifacts. | REQ01/03/05/11; PASS. |
| New thread, wall and retained joint |88 male/136 female actual radial sections cover lead/full form/runout, relief9..10.2 and taper10.2..12.4. Maximum selected-law discrepancy4.08e-5mm. Actual minimum male root radius16.4 against bore15 establishes1.4 wall; sampled female radial ligament minimum1.900917456. Source R6/R5 male and masked female tools each have bidirectional differences0/0. Written body z[-0.1,9.01] joint214faces matches R5 at0/0; cap radius18,z0..12.5 functional19face mask matches0/0. R4's former fitted thread is not assumed. | REQ06/07/09; PASS geometry, strength/fit pending. |
| Full exterior, new end phase and normals |1980 body +2772 cap actual written ray/normal probes across all33 repeats at critical ends, relief boundaries, seam/collar and representative long stations. Independent formula error<=0.000201451mm (<0.01); maximum radius19.500000000000302. All4752 exterior normals outward; max radial-Z slope0.892968750020 (<1). Additional70 male/105 female actual interior joint probes have max slopes0.714287271/0.750000000. Cap normals evaluated in flipped print pose. | REQ05/07/08/09/10; PASS focused actual-surface evidence, no global certifier or slicer claim. |
| Plateau, field and seam | Independent route bound0.001061589 (<0.004), rational-warp plateau lower bound1.040204mm. Actual narrow-direction plateau chord1.056761894 body/1.056760883 cap.132 written seam comparisons at z±1e-5 have maximum radial mismatch1.07e-14mm. Full amplitude continues at both textured end bevels and through collar/seam; no new smooth band. | REQ08/09; PASS CAD field; real tightened registration pending. |
| Full floors and fourteen drains | Written body floor−135..−132 and cap81..84; sections at printZ0.01/0.2/0.501/1.5/2.99 each show1 connected material face with8 wires and exactly7 circular holes of radius1.5. Centers match center+sixR9. Every hole's center/radius1.49 is void and radius1.51 is material at3 depths; floor transition and surviving material checked away from holes. Measured circle geometry gives6mm nearest ligament, margins4.5/5.0, area49.480084mm2 per end. No center glyph or hidden floor roof. | REQ05/09/10; PASS geometry. |
| First layers and placement | At printZ0.01/0.2 body material areas1081.426285/1097.963729mm2; cap1091.908306/1101.617113mm2, all connected with7 openings. Actual closed and print occurrences match standalone written shapes after source transforms, bidirectional vertex distance<=2.97e-27mm and volume differences0. BodyT(+23,0,135), capT(−23,0,84)*Rx180, bed minima0, both openings up and nominal7mm separation. | REQ10/11; PASS written poses/footprints, process/bed/brim/adhesion pending. |
| Actual screw motion and stop | Actual placed body/cap common volumes at0/90/180/360/720degrees with gaps0/0.5/1/2/4 are all0mm3. Gap10 is disjoint by actual Z extents. Overtravel−18degrees/−0.1mm gives23.747774760907mm3, establishing positive external stop. Shared-Z masks preserve the actual overtravel slab and include all possible intersections; excluded Z slices are provably disjoint. | REQ04/06/07; PASS prescribed motion, no hardware retention claim. |
| Nominal device and insertion | Actual source helper cylinderD29/L208 bounds[-14.5,-14.5,-129.5]..[14.5,14.5,78.5];0mm3 intersections with actual full written body and cap. Actual body neck slice z[-0.1,9.1] versus radius14.5 axial passage cylinder also gives0mm3. Full bore section evidence plus the unchanged coaxial cylinder establish monotonic axial passage through the narrow neck, with nominal0.5/1 radial gaps. Centered reference gives2.5/2.5 axial gaps; helper explicitly says unretained. | REQ03/04/11; PASS nominal envelope only. Literal neither-end-contact and physical hardware fit remain unresolved. |

The actual long cylindrical bores were sampled at six body and four cap axial stations across three angles, yielding radii15/15.5 to1e-7mm. End holes and phase were tested at full positions rather than inherited from the cancelled short candidate. Source joint declarations retain shoulder/tip/full_thread_start/end/inner_floor/skin_phase/bed/screw_axis; body rebuild additionally confirmed all eight live joint names.

## Disposition and next action

No blocking mechanism/constraint finding was measured in the scoped source/CAD or written functional geometry. The sole measured digital blocker is VAL-R6-01-F01 cap source/STEP parity. Source/CAD focused evidence can advance to the separate critic/formal review join; written STEP acceptance remains HOLD until that exact discrepancy is diagnosed and any affected candidate/gates are properly refrozen and rerun. Mandatory screenshots belong to the independent critic and are not claimed by this validator.

Slicer/profile/adhesion and physical acceptance remain pending: provisional L208/D29 measurements, loaded full closure, literal both-end noncontact/retention policy,1.4mm root strength, hand fit/wobble/five cycles, wear and unobstructed water passage. Nominal center placement is not a restraint and the drains can be occluded by the device or table. The user's direct-full instruction authorizes this CAD despite those explicitly retained gaps; no mandatory short coupon is reintroduced.

Next action: root routes the cap export/parity diagnosis with exact frozen cap source/written hashes and rows above; preserve all unaffected evidence and the candidate until an intentional repair. No fabrication or delivery-as-accepted STEP is supported by this receipt.
