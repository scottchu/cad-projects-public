# IMP-R5-01 implementation receipt

Status: historical implementation-only candidate. The user subsequently said “不要短的。直接來” and explicitly requested direct full-case work. Short candidate111 remains frozen without acceptance; further short CAD/tests/review are stopped. Owner `/root/case39_impl`, sole implementation role. This receipt does not approve its own design. No slicing, mesh fabrication export, service changes, printer action or Git operation occurred. Root owns project continuity and the new full-case design/cost contract.

Verified input: all94 path/content pairs in `inputs/design-contract.sha256`, fingerprint `64186f7fc3da984878296798305a1189c38d84ae0bedba9356171f95097be2c2`, checked before source work and again at freeze. This includes preserved R4 inputs and accepted artifacts. No R4/R3 file was changed. Frozen candidate: `inputs/implementation-candidate.sha256`,111 paths, SHA256 `06a5e7e2aaa547f4add77718f2d742facdfa39696e06a1e6ca26313ff5d853b5`. It includes all design inputs, the design manifest itself, new R5 modules/wrappers/README/four STEP outputs, and `tests/test_case39.py`; mutable evidence and orchestration records are excluded. Source and artifacts were not changed after freeze.

## Implemented result

New source namespace `cad/p1_r5_39mm_case/`: our R4 source was copied and adapted, with the original rational circle/Bezier patch construction and canonical shared edges retained. Selected thread B uses root16.4/crest16.9, height0.5, pitch2 and engagement6; C25 is the only built candidate. Bores30/31 are preserved. Male root wall1.4 is an explicitly new strength assumption; female wall1.90 at C25,1.85 at C30 budget. Thread flank freedom changes and old physical fit does not transfer.

The2.2 cap taper is independent of exterior radius and preserves axial9/10.2/12.4 datums. Guaranteed shoulder radius is19.05. Shared N33, axialpitch4.8, height0.45, phases0/0 maintain our original motif proportions. The textured end bevel is0.30radial/0.50axial; seven diameter3 axial holes cross each3mm floor, with one center and six at radius9. Hole tools extend only0.01 beyond each floor face and do not reach sidewalls, threads or the stop. The conflicting recessed center glyph is omitted; C25 identity remains in source/artifact labels. Native shoulder/tip/full-thread/inner-floor/skin-phase/bed/screw-axis datums and joints are retained.

Exactly one body and one cap appear in both assemblies. Body print translation(+23,0,35.1); capRx180 then translation(-23,0,43.4). Both openings face up. The short closed cavity remains72.5 and outer length78.5. This does not instantiate a full Laifen case.

## Commands and results

All commands ran from `/Users/scottchu/.codex/worktrees/4f8c/design-projects`, through the root uv environment and installed CAD0.4.28 launcher; no environment/tool source was altered.

```sh
uv run pytest projects/laifen-wave-case/tests/test_case39.py -q -k 'not written'
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r5_39mm_case/body.step.py projects/laifen-wave-case/cad/p1_r5_39mm_case/cap_c25.step.py projects/laifen-wave-case/cad/p1_r5_39mm_case/closed_c25.step.py projects/laifen-wave-case/cad/p1_r5_39mm_case/print_layout.step.py --write
uv run pytest projects/laifen-wave-case/tests/test_case39.py -q
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/inspect refs projects/laifen-wave-case/cad/p1_r5_39mm_case/closed_c25.step.py --facts --planes --positioning
```

Results: fast3 tests pass, complete5 tests pass, generation exits0 with four `built` targets, refs exits0/`ok:true`/no warnings. Exact logs are reproducible scratch evidence in `scratch/case39-impl/{generation.log,tests.log,refs.json,refs.log,freeze.json}` and are not release assets. The CLI refs `ok` only establishes reference resolution; actual solid validity/positive volume and counts were separately checked in pytest and construction.

| Check | Observed result |
|---|---|
| Geometry construction | One valid positive-volume solid per part; exterior body2873faces/cap3665faces; final body2895/cap3689faces. Canonical shared-edge maximum mismatch2.49e-14mm body/2.02e-14mm cap; closed planar noncircular ends, no free or multiple sewn edges. |
| Bounded stage timings | Body outer5.99–6.26s and Boolean3.31–3.39s; cap outer8.88–9.24s and Boolean9.98–10.44s over target-generation calls. Each is below180s. All four STEP writes completed96.144s after shell creation of the generation log: log birth02:20:54.441761UTC, final layout mtime02:22:30.586035UTC on2026-09-03. This provides a whole-run bound for the written exports; no separate export CPU timer was recorded. |
| Reference facts | Closed assembly2 leaf occurrences/2 shapes/6584faces; bounds[-19.5,-19.498274,-35.1] to[19.5,19.498274,43.4], dimensions39x38.996548x78.5. |
| Scalar constraints | Rootwall1.4, female budgetwall1.85, radialinterlock0.20, new flankslope0.714286, axialflankfreedom0.35. Axial datums remain9/10.2/12.4 when exterior radius changes. Invalid legacy-root selection and insufficient39mm wall budget are rejected. |
| Pattern and bevel | N33, route sector multiplier1, route radial bound<=0.004, rationally warped plateau>=1, composed radial-Z slope0.89296875. Shared seam field and +4.8 length-domain check pass without pitch/count/phase changes. Actual exported outer boundary probes straddle the selected law by0.015mm at seam and both closed-end bevel regions. |
| Threads and taper | Actual exported material/void probes straddle the new male/female radius laws by0.015mm at three angles and six lead/full-form/runout heights; four additional relief/taper/straight-bore levels per angle pass. These detect the obsolete R4 radial geometry and radius-driven axial taper drift. |
| Floors and holes | All14 hole centers and radius1.49 are void, radius1.51 is solid, at three levels through each floor. Interior floor material remains connected to each one-solid shell; innerfloor datums-32.1/40.4 pass. Hole-center spacing9 gives6mm ligament; maximum hole radius10.5 leaves4.5mm body-bore and5mm cap-bore margin. |
| Exported placements | Individual targets contain1 solid, closed/layout contain2 each; both layout bedsZ0, centerX approximately±23, openings up, height44.1, bounds within85.02x39.02mm. Closed length78.5. |

The original lightweight volume accessor reports body19545.899277mm3/cap18285.261246mm3 during construction. These values are diagnostic only: independent source/STEP parity must use the prescribed adaptive BRepGProp integration, not the loose accessor difference. No full surface normal certification, independent collision/motion approval, source/STEP parity acceptance, slicer validation or physical acceptance is claimed by this receipt.

## Artifact hashes

| R5 artifact | SHA256 |
|---|---|
| `cad/p1_r5_39mm_case/body.step` | `194abacb5b47519adde369db03479ce91c44ca3ce105d9627de39a54cd7f99fa` |
| `cad/p1_r5_39mm_case/cap_c25.step` | `fdf7563978d8b04609ebdefeaefb44339a8bee81c7394d438b9313fc7e9e0607` |
| `cad/p1_r5_39mm_case/closed_c25.step` | `3a21a7323dd973db7f3455198a444724ba6a256a5c14a9b743d8f905ee1d46d4` |
| `cad/p1_r5_39mm_case/print_layout.step` | `b69128bd8f04935cbe3b32b1a2cb0ed5cb627d32f1d4b2f8a6ee62158e884586` |

## Coverage, risks and next action

REQ01/08/09: original procedural skin, preserved proportions and selected texture-wall budget have implementation evidence. REQ03/05/06/07: bores, short floors/cavity, changed thread, positive-stop geometry, bevels and floor-only drains are implemented; actual screw motion and contact require the independent validator. REQ10: composed slope arithmetic and intended source/export orientations pass; actual normals and eventual slices remain separate gates. REQ11/12: source parameters, native datums and four explicit STEP targets are present. REQ02/04/13/14: installed envelope, full end contact/retention, new-thread physical fit/strength and full-case acceptance remain pending.

High physical risk:1.4mm new male root wall and changed thread profile lack print/strength/fit evidence. Medium physical risk: flank freedom and drainage blocked by device/table contact. No contradiction or topology failure was encountered; one implementation attempt, no geometry repair cycle. Full-case length/topology budget remains gated.

Next: root freezes a new full-case design and topology/cost contract, then assigns full implementation against its exact inputs. Do not resume short-candidate acceptance work after the user scope change. Mandatory primary STEP snapshots, actual screw/negative-stop checks, high-accuracy source/STEP parity and remaining actual-wall/normal evidence were not completed for short111 and are not waived or inherited by a full candidate. The short files are historical implementation evidence only; future full slicing/physical work requires its own exact-artifact gates.
