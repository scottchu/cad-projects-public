# IMP-R4-01 implementation receipt

Owner `/root/uniform_skin_impl`, CAD implementation only, 2026-09-02. Strong/high bounded role, qualitative20minute/18k-token ceiling, initial construction succeeded without geometry repair. Baseline HEAD `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c` plus frozen worktree inputs. All63 design-contract entries verified before writing, SHA256 `d1413f9b17a4e0e7007cebd4e68c07335b11def9805d24d642d25937e391113f`. Final manifest and completion status appended below.

## Candidate scope

Exclusive new `cad/p1_r4_uniform_skin/` holds params, exact copied original thread construction, shared radial field, rational Bezier surface route, part/joint/print transforms, README and four STEP/source targets. `tests/test_uniform_skin.py` contains three focused regressions. Scratch command logs/scripts and JSON evidence are under `scratch/uniform-skin-impl/`. R3 source/artifacts/tests and all unrelated project files are preserved. Root's assigned namespace replaces the brief's provisional `p1_r4_generator` path as a routing choice only.

Outer crest40mm, inward depth0.45, common N34/phase, full body[-35.1,0] and cap[0,43.4] domains, textured0.20rad/0.30axial bed relief. Functional radius fields remain legacy values17.4/17.9/19.5 and produce identical J10.2/A12.4. The new outer fields never feed `female_void()`. Original `thread_profile.py` is byte-identical. No DES07, downloaded geometry or per-diamond Boolean was used. Both noncircular planar closures reuse exact existing perimeter edges; no disk substitute, added seam clearance or relaxed sewing tolerance. Original label and source datums/joints remain. Print layout is exactly one body plus one C25 cap, open upward.

Usable scalar exterior inputs and length changes have guards; fitted bores/floors/pitch/engagement/root/height/budget are explicitly locked. Alternate clearance0.20..0.30 remains an optional single-cap parameter. Only the default geometry is submitted for acceptance, and a +4.8mm length case has scalar evidence only.

## Commands and observations

Run from repo root, non-login shell, root uv Python3.12:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-02-p1-r4-uniform-skin/inputs/design-contract.sha256
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r4_uniform_skin/body.step.py projects/laifen-wave-case/cad/p1_r4_uniform_skin/cap_c25.step.py projects/laifen-wave-case/cad/p1_r4_uniform_skin/closed_c25.step.py projects/laifen-wave-case/cad/p1_r4_uniform_skin/print_layout.step.py --write --verbose
uv run pytest projects/laifen-wave-case/tests/test_uniform_skin.py -q
uv run python projects/laifen-wave-case/scratch/uniform-skin-impl/check_candidate.py
uv run python projects/laifen-wave-case/scratch/uniform-skin-impl/volume_parity.py
```

Cheap polygon estimate: body2960, cap3776 exterior faces, about0.22/0.25seconds; both below6000. Analytic rational radial bound0.001000087mm, plateau lower bound1.037682518mm, slope bound0.959635417. One sewn positive valid blank per part with all canonical edge incidences2, no free/multiple sewn edges. Maximum actual canonical join discrepancies2.14e-14/2.58e-14mm. Example first installed-gen timings: body exterior6.66s, body Boolean3.02s, cap exterior10.73s, cap Boolean10.96s. Initial complete four-target installed-gen run102.5seconds. A second installed-gen pass records only stdout-to-stderr progress routing and parameterized cap label; default geometry is unchanged.

Own tests:3 passed. They cover forbidden OD39 at full depth, constant full-coverage field including seam/collar and bed relief, original functional derive invariance under outside change, +4.8 scalar pitch/phase stability, explicit unsupported thread-pitch rejection, written solid counts/floors and open-up print placement. These tests are implementation regressions, not independent approval.

Actual new versus original male neck: matching1850.6383840833478mm3, bidirectional Boolean differences0/0. Female void: matching34737.150464259175mm3, differences0/0. Actual R4/R3 written geometry differences under functional masks are0/0 for both parts. Body mask includes r<=17 below seam and r<=17.8 through the neck; cap mask r<=17.8 through z12.5 and r<=17.5 above, covering mouth/full-form/taper/bore/floor/label while excluding intentional outer growth. The first diagnostic script attempted `.cut` on a ShapeList; one focused script repair wraps it in Compound. No CAD geometry changed for that diagnostic repair.

Written standalone body is valid,1solid,2975faces; cap valid,1solid,3819faces. Closed and print layout are valid,2solids,6794faces. Nominal written bounds within1e-6mm: body40x40x44.1, cap40x40x43.4, closed40x40x78.5, layout87x40x44.1 with both minimaZ0. Layout/body cap details are in `own-checks.json`.

Default build123d volume integration gave source/body22271.579301728 versus STEP22271.576807137, a0.002494591mm3 discrepancy above the design's0.001mm3 gate. Controlled adaptive OCC integration resolved it without geometric or tolerance changes:

| Part | Eps | Source volume mm3 | Written volume mm3 | Absolute delta mm3 |
|---|---:|---:|---:|---:|
| Body |1e-8|22271.572570398162|22271.572571777768|0.0000013796|
| Body |1e-10|22271.572570763416|22271.572577968713|0.0000072053|
| Cap |1e-8|20528.31919290555|20528.31917892501|0.0000139805|
| Cap |1e-10|20528.31916414049|20528.31915712146|0.0000070190|

Method: `BRepGProp.VolumeProperties_s(shape.wrapped, GProp_GProps(), eps, True, False)` on source and imported STEP. Both accuracy settings satisfy0.001mm3 without interpreting the loose default integral as changed geometry. Independent validation must verify this evidence on the frozen final candidate.

An additional installed `scripts/inspect validate .../closed_c25.step` invocation was terminated after about2minutes without its final result because it was consuming a long whole-assembly check during candidate generation. Its partial stdout is not validation evidence. Direct actual source and imported STEP `is_valid`, positivity, counts, dimensions and functional masks did complete as described above; no CLI validate PASS is claimed.

## Acceptance boundary and next action

Implementation candidate only; CAD/source and written STEP independent acceptance pending. The root assigned mandatory actual-STEP snapshots/section, visible full-collar/constant-envelope critique and viewer handoff to the distinct critic. Distinct validator owns actual surface radial/normal/plateau/ligament checks, critical sections, full screw path/stop checks and independent artifact placement/parity. Those are deliberately not claimed by this receipt. Slicer/process/physicalR4 remain pending; no print readiness, physical fit, slicing, upload, start or printer action is claimed. Freeze candidate, then send the same fingerprint to the distinct critic and validator before formal independent-review join.

## Final frozen handoff

Status: implementation complete, pending independent gates. Final four-target installed-gen run98.9seconds completed successfully. Final design-contract verification: all63 entries unchanged. Candidate `inputs/implementation-candidate.sha256` has80 sorted SHA256 path/content entries; fingerprint `e56a117867e2cb0b77e706068636d56fb2adfa5e0eacf34fb2e7cd40897571cb`. It includes all63 frozen design inputs, the design manifest itself, all new authoritative source/README/tests and the four written STEP files. Render caches and mutable implementation evidence are excluded. Byte-identical R3/R4 thread construction SHA256 `5f4ab31f844551780415dc528d5ae01e0bc626ba9ab5e5c74b3789a8ac25b13a`. No geometry repair was required. No further candidate mutations are authorized while downstream reviewers use this freeze.
