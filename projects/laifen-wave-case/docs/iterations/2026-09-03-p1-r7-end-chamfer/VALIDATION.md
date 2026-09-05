# VAL-R7-01 independent validation

Owner `/root/case39_validate`, independent validation role. **Final repaired candidate201 deterministic source/native CAD and written-STEP gates PASS.** Fingerprint8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1. The original written-body parity HOLD is resolved for the repaired hashes. Sections below preserve distinct attempts and their then-current states; the final receipt at the end governs. Source evidence covers default1.2 and selected1.4 sensitivity samples, not broad nondefault fabrication acceptance. Critic/formal acceptance and physical validation remain separate.

Frozen source-ready173 `scratch/end-chamfer-impl/source-ready.sha256` SHA256 `7c3699fe77cbb043fee662bec3b6b564ae4d69541930912536d635612ea2f343`, all173 paths verified before/after source work. Independent source inputs178 `scratch/end-chamfer-validation/source-inputs.sha256` SHA256 `b8bf094f2f1ac0f8183715bf1bed581f5ea63335501251d94380fb1e774a920b` were frozen before execution. Preparation implementation-inputs155 SHA256 `09aa21a9cf7b6b4b39f0365b8348c1ee814085be4356d31136ae5ebaf70bcaf1` was also verified. No moving part caches or STEP files were read.

Root UV/Python3.12, non-login shell, repository-root command:

```sh
uv run python projects/laifen-wave-case/scratch/end-chamfer-validation/source.py > projects/laifen-wave-case/scratch/end-chamfer-validation/source.log 2>&1
```

Exit0. Canonical numeric evidence: `scratch/end-chamfer-validation/source-results.json`.25 common input parameters and all31 common derived fields match R6. Function ASTs for thread geometry, native runout normalization, named datums, drain cutters and original diamond field match the accepted baseline. Removed old relief fields/functions/zones are absent from the R7 route. New size defaults1.2;0.8/1.2/1.4/1.5 accept, immediately adjacent representable values outside0.8..1.5 reject, as do NaN and bool. Recovered arithmetic default end radius18.3, axial height1.2, slope1, circular band0.75 and cap end radial material2.8; maximum size preserves2.5 material.

Actual maximum-size1.5 annular cutters each have1 valid solid/4faces and one cone measured45.00000000000006degrees. Body boundsZ[-135.01,-133.49], cap[82.49,84.01]. Boolean intersection with a full-height radius15.5 protected bore envelope is0mm3 for both. Their worst axial clearance to the inner-floor planes is1.49mm including epsilon; joint/seam protected-range clearances are133.49mm body/70.09mm cap. Minimum cutter radius17.99 including epsilon is outside every bore and the R10.5 drain envelope. Actual cutter rings at two inward stations match the cone equation to numerical precision across12 azimuths. This proves no tool reach into the preserved bore/floor/drain/joint regions; prior thread/motion/device evidence need not be broadly rerun on that basis.

Next: independently inspect frozen source-native body/cap solids at size1.2/1.4 and exact default STEP, with bound source/parameter provenance, circle/slope/sensitivity and protected-region checks, unchanged0.001mm3 adaptive parity, new first layers/drains and two-part occurrences. Critic owns actual end/seam snapshots and a distinct formal reviewer joins. CAD/source, written STEP, slicer/process and physical acceptance remain separate; no source/STEP/printer/environment/service/Git mutation is in validator scope.


## VAL-R7-01B actual native geometry

Immutable sensitivity179 manifest `scratch/end-chamfer-impl/sensitivity-candidate.sha256` SHA256 `b58c6823153eea08093f1aa4ab400672d53d603b8da97598b39836f64c9cd4a3` verified before/after. Own native inputs187 were frozen before execution: `scratch/end-chamfer-validation/native-inputs.sha256`, SHA256 `7eeb50c5fb8a6112888800f32eac8b01c9090bf488fbebe17aff2a2a4f49a6bf`; all187 verified after. Independent `native.py` exited0 in37.59s:

```sh
uv run python projects/laifen-wave-case/scratch/end-chamfer-validation/native.py > projects/laifen-wave-case/scratch/end-chamfer-validation/native.log 2>&1
```

Provenance is explicit: these are implementation-generated **source-native BREP caches**, imported and measured independently; the validator did not duplicate the300s raw-skin build. Frozen `sensitivity.py` calls the same source `build_outer_blank` and `body_from_outer`/`cap_from_outer` finishing functions with Params at1.2/1.4, then writes native BREP. The source/parameter/cache hashes are bound by the179 manifest and checked independently. Default parameter fingerprint556e342ddfe8b483549bcca09876cc8919c04f8f0c01dbae5cd4197c3a15ad3a and1.4 fingerprint360fbc3a0837349d690fad60839e438405def08e2c4ac128b644748b09bbee33 match current frozen parameter serialization. Imported-native adaptive volumes reproduce pre-write source records within3.64e-11mm3; no STEP roundtrip or hidden geometry regeneration supplies this source evidence.

| Native part | BREP SHA256 | Faces | Measured size | Measured radial/axial slope |
|---|---|---:|---:|---:|
| Body1.2 |86995941a6f09c71e105892b18a73b09a779516faf79d9a417d0425d1e62970d|10255|1.200000000000102|0.999999999999641|
| Body1.4 |040f0e804f2a24940a3a1764fd9b4e2d56b250efdaefb6faa743dbfef42ce2b8|10255|1.399999999999984|0.999999999999410|
| Cap1.2 |53b0a03bd641eb01fbefb7ad20f66a38c74f5bfbff8983dabf3c49b6618ddac2|6396|1.199999999999907|0.999999999999641|
| Cap1.4 |f8878358fb9f9c27f0e8f863b3eb4f9257839ef03bfd5ffda5b58f182f84a82f|6396|1.399999999999984|0.999999999999890|

Each is one valid positive closed solid. Independent ray/normal probes at inward t0.05/0.25 over12 azimuths show circular rings following r=19.5−size+t within1e-6mm and actual45-degree slope within1e-5. Increasing1.2 to1.4 reduces radius by0.199999999999882mm body/0.200000000000077mm cap. The twelve sampled non-end radii at bodyZ−50.123/capZ45.234 change by exactly0. No viewer control or nominal-only value supplies this sensitivity result.

Reusable native classifiers verify all seven floor holes are void through their centers/radius1.49 and have material at radius1.51, plus preserved inner-floor transitions−132/81 and bore radii15/15.5, for both sizes. Full heights144/84 remain unchanged. These actual part checks complement the earlier end-cutter locality proof; no joint/motion broad rerun was triggered. Native numeric details: `native-results.json`. Default written STEP parity, first-layer/closed-end sections and assembly occurrence validation remain pending their separate immutable handoff.

## Repair1: end-cone trim consistency

The first writer's written-body parity result was a **HOLD**, reported delta0.06683846554mm3 against the unchanged0.001mm3 limit. That writer result was not an independent validator rerun. The rejected body STEP SHA256405d6769df35dfff7c51b1be38897b631550fbd8b460627812a30b50365a9244, original parts.py/README and four original native caches are preserved in seven `scratch/end-chamfer-impl/repair1/before-map.json` mappings; all seven archive hashes were independently verified. The earlier native profile PASS did not establish endpoint consistency or written parity.

Repair1 source197 `scratch/end-chamfer-impl/repair1/source-candidate.sha256` SHA25664c37fb4b28492981ce453f75975ecfda9ae83d5a51720f92cb886930573d83a was verified before/after. Independent inputs202 `scratch/end-chamfer-validation/repair1/native-inputs.sha256` SHA256a5548580c34444762c98ff7c4a5712c7bec7f04728fb6e35dd5e58645ff82c98 were frozen before execution. Command, exit0,56.71s:

```sh
uv run python projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/native.py > projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/native.log 2>&1
```

Frozen `repair1/regression.py` applies the production `normalize_end_trim` to the retained original source-native caches. It does not use STEP as source or rebuild the raw diamond skin. The validator inspected that provenance, independently imported the four repaired caches, and independently executed the production helper on archived default body/cap defects. Original inputs remained untouched; repeated normalization returned the same already-normalized topology; independent repaired volumes matched the supplied repaired caches. All vertex coordinates and vertex tolerances are exactly unchanged for all four caches. Source-scope evidence also shows all13 other prior source files unchanged; parts.py AST is identical after removing only the new import and two final normalization assignments. Protected dimensions, cutters, thread, runout, field and poses therefore retain their earlier evidence.

| Repaired source native | SHA256 | Defective endpoint incidences before | Maximum endpoint residual after (mm) |
|---|---|---:|---:|
| Body1.2 |5c4de50e63f183489354236b5ee8a664b9f77c1e81c65b8d4f1a3e5fdc8f1afa|33|5.02144208345e-9|
| Body1.4 |1e06cd03c4b771cbdf63d583afe868e886b728bee460347fddada371149833b4|33|2.43826485619e-8|
| Cap1.2 |001e37342a2f8d2a6c986547eebbc1fd257716898d08453c0dc87de6488731b9|32|4.14285904412e-8|
| Cap1.4 |20e59036b77c2fed0e8cd45407ab91ae1192d7bd3d5f10031175bb35a0c01fcb|32|2.87314072980e-8|

Independent edge/vertex inspection reproduces pre-repair residuals2.40e-6..2.77e-6mm and verifies matching 3D/cone-pcurve ranges plus stored vertex-parameter consistency after repair. These are actual curve/vertex measurements with an independent end-cone selector. Each repaired cache is one valid positive closed solid. Actual circular rings/45-degree slopes and1.2→1.4 sensitivity pass again; radius reduction is0.199999999999882mm body and0.200000000000077mm cap, with exactly zero change at the sampled non-end stations both across repair and across parameter settings. Default parameter and1.4 parameter fingerprints remain identical to attempt1. Canonical details and individual endpoint rows: `scratch/end-chamfer-validation/repair1/native-results.json`; source preservation: `source-scope.json`.

The native mass changes are consequences of corrected curve trimming, not permission to waive the source/STEP threshold. Repaired written default gates use these corrected source-native caches with eps1e-8 and1e-10, preserving the0.001mm3 acceptance limit. No raw-skin rebuild, broad thread/motion rerun, slicing, printing, or physical approval is inferred.

## Repair1: written standalone gates

**PASS.** Frozen standalone199 `scratch/end-chamfer-impl/repair1/standalone-candidate.sha256` SHA2564b0b016c7a91a97f895c1278f76165fa3fae00e27784695f508093f71394a6de verified before/after. Own frozen inputs206 `scratch/end-chamfer-validation/repair1/standalone-inputs.sha256` SHA256b7601685cefed5304a15becd3876caeb1ed7229839f52ed41c8cd2f7115e1e54 and native inputs202 both independently reverified after completion. Command exited0 in80.54s:

```sh
uv run python projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/standalone.py > projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/standalone.log 2>&1
```

Written body SHA2563c04d417e3f21c5ef0e3b1d12ff1953ac366ef418fc4792d592a0624ad91982b; cap SHA2560dd09cbd99f4ceb78605ee7eef1a74a315c3f95079d97a4628dffffc70afe82a. Comparison is against the corresponding corrected source-native default caches listed above. Adaptive OCP `BRepGProp.VolumeProperties_s(shape, props, eps, True, False)` is used; default build123d volume is not used for acceptance. All rows were preserved before assertions.

| Part | eps | Native volume mm3 | Written volume mm3 | Absolute difference mm3 | Native / written returned error estimates |
|---|---:|---:|---:|---:|---|
| Body |1e-8|65470.38708537477|65470.38708687826|0.00000150348932948|6.63322470658e-9 /6.63322480459e-9|
| Body |1e-10|65470.38706420824|65470.38707347599|0.00000926775101107|7.56376163369e-11 /7.56369146893e-11|
| Cap |1e-8|34973.250868539144|34973.25085619282|0.0000123463250929|5.97214145260e-9 /5.97191105978e-9|
| Cap |1e-10|34973.250833726|34973.25082611402|0.00000761198316468|1.01818740923e-10 /1.01812977248e-10|

Every difference passes the original0.001mm3 limit. Both written parts are one valid positive closed solid,10255 body/6396 cap faces, heights144/84mm. Actual written end circles and45-degree slope pass the independent ring/normal probes. At printZ0.01 and0.2, each end has exactly one material face/eight wires/eight circular edges: seven radius1.5 drain holes and outer radius18.31/18.50. The measured areas1003.75801653712 and1025.73000139704mm2 match `pi*(outer_radius^2-7*1.5^2)` within2.7e-11mm2. Classifiers separately verify the seven through-floor voids, surrounding material, inner-floor transitions−132/81 and bores15/15.5 on both written parts. Numeric evidence: `repair1/standalone-results.json`.

The first-attempt written-body parity HOLD is resolved for these repaired standalone hashes, with no tolerance relaxation or dimension change. Closed/layout occurrence gates remain a distinct final dependency. The nondefault1.4 result is source-native sensitivity evidence only; no1.4 STEP artifact is approved by the default export checks.

## Repair1: occurrences and coverage

Frozen closed200 `inputs/closed-repaired.sha256` SHA256567223305b9ee32e9809741ac3f5fa186a0a546c16d424da46af5abc6075ff52 and all200 entries verified before/after. Closed STEP SHA256e72ee16eb4315a2eb93619ecfb3fd363ac89dc5253bb6527de9d71c82444d27c. Its independent occurrence check passes: two valid closed solids/16651 faces,219mm overall height, zero bidirectional vertex distance and zero adaptive-volume difference for each occurrence versus the written standalone in its prescribed zero transform.

One validator-method correction was necessary: the first adapted occurrence script stopped at a relocated `helpers` import before reading geometry. Original `occurrences.py`, `closed-occurrences.log` and inputs205 SHA256a8a9b52450c723d691c0ed962a90577da323f4d5f7d1c045f27f1b61f0fbe151 remain preserved. Corrected `occurrences.v2.py` changes only that import path; it was frozen in inputs207 `repair1/closed-inputs-method1.sha256` SHA256eb8a0523428ca70f17c594f4f0ab6a1eaa07a72d4b299a89fbd705e955978556 before execution. No candidate change or extra geometry iteration resulted. Exact corrected command, exit0,55.27s:

```sh
uv run python projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/occurrences.v2.py --assembly closed_c25 --manifest projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/inputs/closed-repaired.sha256 --fingerprint 567223305b9ee32e9809741ac3f5fa186a0a546c16d424da46af5abc6075ff52 > projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/closed-occurrences-method1.log 2>&1
uv run python projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/source_scope.py > projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/source-scope.log
```

Risk-driven core coverage is explicit: object-collision checks use actual maximum-size end cutter/protected-bore intersection and axial/radial separation; math checks recover real circle radius/slope/sensitivity and preserve dimension derivation; constraint checks cover parameter domain, unchanged source, topology, floors, bores, endpoint consistency and STEP parity; user-requirement checks demonstrate the real smooth parameterized end transition, preserved full case/diamond field/seven drains, and actual written first-layer connectivity. Prior accepted R6 thread/closure/motion/device-envelope evidence is retained by unchanged equations/native-runout source plus R7 end-local cutter separation. It is not recast as a new broad physical noncontact or retention claim. Print-layout occurrence validation remains pending its exact freeze; critic snapshots and formal acceptance are separate roles.

## Final repaired candidate receipt

**PASS for the scoped deterministic CAD and written-STEP gates; no open deterministic blocker.** Final201 `inputs/implementation-candidate.sha256` SHA2568d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1 was verified before/after the last prescribed check. Final layout STEP SHA25680fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4. It contains two valid closed solid occurrences/16651 faces. Prescribed placements are body translation(23,0,135) and cap translation(−23,0,84) with180-degree X rotation. Bidirectional vertex distances are0 body/2.97e-27mm cap; adaptive-volume differences are0 for both. Both sit at printZ0 within1.1e-7mm. Overall bounds85.0000002×38.9965480824×144.0000002mm pass; the slightly sub39 Y span is expected for oddN33 while radial crest diameter remains39. Source-defined separation gives7mm between object bounding boxes. Command exited0 in29.70s:

```sh
uv run python projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/occurrences.v2.py --assembly print_layout --manifest projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/inputs/implementation-candidate.sha256 --fingerprint 8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1 > projects/laifen-wave-case/scratch/end-chamfer-validation/repair1/layout-occurrences.log 2>&1
```

Own final219 `inputs/validation-inputs.sha256` SHA25645a53a3cfd45bbd2223a4efcf5e6f5ff78f83532e045f8ea6ffb4f9f37ae3a50 binds candidate201, plans, all executed helpers and stage-input manifests. It was frozen before the final geometry command and verified afterward. `inputs/validation-evidence.sha256` freezes this receipt, final inputs, stage logs/results, archive/source-scope verification and final occurrences; no mutable orchestration records are required. Individual results remain in `scratch/end-chamfer-validation/repair1/{native-results,standalone-results,closed_c25-occurrences,print_layout-occurrences}.json`. Earlier attempt evidence stays in the parent validation scratch, and rejected candidate files stay in the mapped implementation archive.

Finding disposition: original written-body source/export divergence was a blocking failure for its original hash, now closed by targeted native end-edge/vertex parameter normalization plus independent default parity at both original eps values. No threshold, dimension, vertex coordinate or tolerance was loosened. One validator import-path method repair occurred before geometry loading; no further method repair or optional global test was required. Retained gates are scoped to unchanged source/equations and proven disjoint protected regions, with independent actual default exports checked after repair.

Remaining gaps are external to this deterministic receipt: visual critic/formal join, slicer/process validation, physical thread fit, drain behavior, real device-envelope measurement and printed assembly/contact behavior. The nominal full-case device envelope does not establish positive retention or guaranteed no-contact at both ends. No slicing, printer action, physical approval, or authoritative source/artifact modification was performed by this validator. Next action: root joins this exact frozen receipt with independent critique and formal review.
