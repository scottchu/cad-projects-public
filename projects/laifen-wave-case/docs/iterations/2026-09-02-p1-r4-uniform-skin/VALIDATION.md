# R4 independent validation receipt

Owner `/root/uniform_skin_validate`, task VAL-R4-01, 2026-09-02. **PASS for the focused default source/BREP and written STEP gates below.** The distinct critic owns mandatory snapshots and visual acceptance; formal independent review remains the join. No R4 slicing, process/adhesion or physical acceptance is claimed.

## Frozen provenance and scope

Candidate `inputs/implementation-candidate.sha256`:80 entries, SHA-256 `e56a117867e2cb0b77e706068636d56fb2adfa5e0eacf34fb2e7cd40897571cb`; all80 path/content hashes verified before geometry work and again after final motion/plateau work. Design63 SHA-256 `d1413f9b17a4e0e7007cebd4e68c07335b11def9805d24d642d25937e391113f` was independently verified during preparation. Exact default source and four STEP files are under `cad/p1_r4_uniform_skin/`; R3 remains frozen. No candidate, baseline, tests, exports, environment or printer state was changed.

Validation inputs are frozen in `inputs/validation-inputs.sha256`; evidence hashes in `inputs/validation-evidence.sha256`. Independent scripts/results are in `scratch/uniform-skin-validation/`. The scripts directly import exact `.step` files with build123d/OCC; adjacent source wrappers are not silently resolved in place of the written files. Source parts were separately rebuilt in memory. Only this validation scratch namespace, these manifests and this receipt were written.

Commands from repository root using root UV/Python3.12 and non-login shell:

```sh
uv run python projects/laifen-wave-case/scratch/uniform-skin-validation/validate.py > projects/laifen-wave-case/scratch/uniform-skin-validation/validate.log 2>&1
uv run python projects/laifen-wave-case/scratch/uniform-skin-validation/plateau_seam.py > projects/laifen-wave-case/scratch/uniform-skin-validation/plateau-seam.log 2>&1
uv run python projects/laifen-wave-case/scratch/uniform-skin-validation/motion.py > projects/laifen-wave-case/scratch/uniform-skin-validation/motion.log 2>&1
```

The first command completed every math/topology/parity/surface/placement/first-layer/functional-mask stage, then was deliberately terminated (exit143) during the original expensive whole-part closed-pose Boolean, without a collision verdict. One focused validation-method adaptation replaced that remaining stage with the mathematically equivalent clipped-solid motion command, which exited0 and completed all prescribed poses in39.60seconds. The plateau/seam command exited0. No source repair, export repeat, tolerance relaxation or generic all-surface certifier was used.

## Findings and requirement coverage

| Gate | Independent evidence and disposition | Coverage |
|---|---|---|
| Math/domain | Derived minimum OD39.90, valley19.55, budget female wall1.85, N34, warped plateau lower bound1.037682518mm and skin-plus-relief slope0.959635417. Actual `derive` rejects OD39; +4.8 cavity scalar case extends body domain[-35.1,0] to[-39.9,0] while count/pitch/phase remain fixed. Functional J10.2/A12.4/root16.8/crest17.4 retained. PASS; no nondefault CAD release. | R4-01/02/03/04/05/06 |
| Actual topology | Body2975faces/1positive valid closed solid; cap3819faces/1positive valid closed solid; closed/layout6794faces/2positive valid closed solids. Native bounds within1e-6mm: body40x40x44.1; cap40x40x43.4; closed40x40x78.5; layout87x40x44.1. Closed shell flags and independent per-solid positivity checked. PASS. | R4-01/04/07/08 |
| Original fitted geometry | Independently rebuilt original/new male neck and female void each have bidirectional Boolean differences0/0. Final written R3/R4 body and cap functional-mask differences0/0. Body mask covers floor/cavity r<=16.5 and entire neck r<=17.8,z0..9.01; cap covers mouth/full thread/taper r<=17.75 through12.5, then bore/floor/label r<=17.5. These masks exclude intended outer growth while containing functional boundaries. Additional88body/128cap critical radial thread/taper comparisons have maximum delta0. Bores measured30/31. PASS. | R4-03/04 |
| Full exterior and normals |2040body and2856cap actual written ray/one-sided normal probes across every angular repeat and critical axial slices, including both relief boundaries, near seam and entire collar. Independent formula maximum error0.000189770mm (<0.01); observed crest20.000000000000433 radius, numerical overshoot<5e-13mm. All4896 normals point radially outward; maximum absolute radial-z slope0.959635417 in the assigned upright/flipped print poses (<1). Collar sampled radius19.559544..20 establishes full-amplitude coverage. PASS as focused actual-surface evidence, not a universal surface/process certifier. | R4-01/02/05/06/08 |
| Wall and plateau | Preserved thread envelope plus actual valley field gives c25 conservative ligament1.90mm and budget wall1.85; minimum sampled actual c25 radial wall1.900292969mm. Plateau boundary found independently by radius bisection along the narrow developed direction: actual endpoint chord1.053788520mm on body and1.053788684mm on cap (>1); analytic lower bound above protects the route. PASS. | R4-05/06 |
| Seam |136actual written radial comparisons at z=-0.00001/+0.00001: max mismatch3.34e-13mm. Original contact plane remains z0; no broad untextured seam exclusion. CAD phase PASS; physical final tightening registration remains unknown. | R4-01/02/03/09 |
| STEP parity | Source and written adaptive OCC volumes independently measured at eps1e-8 and1e-10, with maximum difference0.000013981mm3 (<0.001). Body eps1e-10 difference0.0000072053; cap0.0000070190. Both accuracy settings pass without inheriting the loose default-integration result. Closed/layout per-part volumes match standalone transformed written parts exactly at recorded precision; bidirectional vertex placement max1.54e-27mm. PASS. | R4-07/08 |
| First layers/layout | Actual written sections at print Z0.01 and0.20 each have one connected material face and one perimeter wire for each part: no disconnected starting islands or holes. Areas body1199.8777/1214.3505mm2, cap1210.5490/1230.3638mm2. Both bed minima0, openings up under bodyT(-23.5,0,35.1) and capT(23.5,0,43.4)*Rx180; intended crest-envelope gap7mm. Geometry PASS; slicer extrusion/adhesion remain pending. | R4-07/08/09 |
| Screw motion/stop | Actual written geometry intersections at0/90/180/360/720degrees and matching gaps0/0.5/1/2/4mm are all0mm3. Open1800degrees/gap10mm has disjoint actual Z ranges. Overtravel-18degrees/gap-0.1 produces24.547567423mm3 overlap, confirming the positive stop. PASS for prescribed representative poses. | R4-03/04 |

### Collision proof and runtime adaptation

The actual imported bounds are bodyZ[-35.1,9.000000000003] and capZ[0,43.4]. For each placed cap, only the shared Z interval can contain a volumetric intersection. Actual solids were intersected with a50x50mm XY box over that shared interval before their Boolean common; excluded slices are provably disjoint by Z. Arithmetic endpoint residuals below1e-9 were mapped to the exact authored planar0/9 datums, consistent with measured endpoints within3e-12mm. At gap0, only the actual15-face neck and831-face cap slice remain; gap-0.1 preserves the actual exterior overtravel slab (220body/832cap faces). This is actual-solid Boolean evidence with a broad-phase proof, not bbox-only collision acceptance. No intersection value came from the terminated original command.

### Accurate volume evidence

| Part | eps | Source mm3 | Written mm3 | Difference mm3 |
|---|---:|---:|---:|---:|
| Body |1e-8|22271.572570398162|22271.572571777768|0.0000013796|
| Body |1e-10|22271.572570763416|22271.572577968713|0.0000072053|
| Cap |1e-8|20528.31919290555|20528.31917892501|0.0000139805|
| Cap |1e-10|20528.31916414049|20528.31915712146|0.0000070190|

Method: `BRepGProp.VolumeProperties_s(shape.wrapped, GProp_GProps(), eps, True, False)` with per-solid results recorded. The loose build123d default integral is unsuitable for the0.001mm3 comparison here; it is not evidence of a measured serializer defect. The two tighter integrations independently resolve that risk.

## Disposition and remaining gaps

No measured blocking geometry finding remains for the frozen default candidate. One resolved evidence/runtime issue: expensive unpartitioned full-part collision, replaced by the proved shared-Z actual-solid test above. CAD/source focused gates PASS and written STEP focused gates PASS; final acceptance awaits the distinct critic/formal reviewer evidence join. This validator did not create or review snapshots because the assigned critic owns that gate.

R4-09 remains physical: collar grip, final seam angle under real tightening, torque/wobble/wear/strength and print finish. Exact slicing/profile/toolpaths, first-layer extrusion/adhesion and physical R4 acceptance are pending. No full Laifen fit, nondefault CAD, global surface certification or print-ready claim. The historical R3 export HOLD is neither inherited acceptance nor an automatic R4 blocker. Next action: formal reviewer joins this exact candidate/evidence with the critic's exact-STEP snapshots, records the focused acceptance boundary, and preserves the physical/slicer gaps.
