# IMP-R6-01 full-case implementation receipt

Owner `/root/case39_impl`, sole source implementation role. Status: full implementation complete; four explicit STEP targets generated and three focused implementation tests pass. Frozen candidate135 is ready for independent critic/validator/formal review. This receipt is implementation evidence, not independent acceptance. Root owns continuity and viewer publication; separate critic/validator/formal-review identities own downstream gates.

Frozen inputs: all116 declared path/content pairs in `inputs/design-contract.sha256` verified before work and again at freeze. Manifest SHA256 `f72529fe2f5333e80859496453f720635590b11c46a55ec2bb2bc0c942f079b4`. Candidate manifest `inputs/implementation-candidate.sha256` has135 paths, SHA256 `4c2750ad632639be5547074173408aa14dfc579faed8d45890ed7233b00c0351`; it includes all116 inputs, design manifest, new R6 source/wrappers/README/four STEP files and focused test. Mutable orchestration/evidence and reproducible caches are excluded. R5short111 remains preserved implementation-only; no R5/R4/R3 files are edited. The direct-full user request supersedes short-first and pre-full-CAD measurement gates for this provisional CAD. Actual device measurements, thread strength/fit and both-end noncontact remain unproven.

New source `cad/p1_r6_full_case/` derives C213/H84/bodydepth132/outside219 from deviceL208/allowance5/capcavity81, with editable approximate D29 and fixed bores30/31. The old inert wall input is removed; meaningful straight valley walls4.05/3.55 and nominal radial gaps0.5/1.0 are derived. The R5 B thread and original N33/pitch4.8/shared-phase skin/end-bevel/drain equations are retained. Full sidewall domains are[-135,0] and[0,84]. Native assembly joints remain; body print pose(+23,0,135), capRx180 then(-23,0,84), exactly two primary assembly objects.

`review.py` provides source-defined nominal device readouts, envelope end joints and a diagnostic section helper accepting exact written case solids. Centered endpoints-129.5/78.5 give nominal2.5/2.5 gaps; bottom-resting comparison-132/76 gives0/5. The helper states reference-only/unretained and is excluded from all four primary generators. No fifth fabrication target or device object is added to primary assemblies.

Source guards count both polygon domains before BREP allocation, enforce16000 exterior faces per part/26000 combined, preserve rational accuracy and canonical shared edges, and check600s outer/Boolean stages. `generate.py` invokes the installed CAD generator on each explicit target with`--write`, root UV Python3.12,600s owned-process-group timeout per target and1800s total; stage/export timings are logged. No environment, service, mesh, slicer, printer or Git change is in scope.

Commands from repository root:

```sh
uv run pytest projects/laifen-wave-case/tests/test_full_case.py -q -k 'not written'
uv run python projects/laifen-wave-case/cad/p1_r6_full_case/generate.py
uv run pytest projects/laifen-wave-case/tests/test_full_case.py -q -o addopts=''
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/inspect refs projects/laifen-wave-case/cad/p1_r6_full_case/closed_c25.step.py --facts --planes --positioning
```

The generation wrapper executes these installed explicit commands under the root `.venv/bin/python3` with enforced timeouts:

```sh
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/body.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/cap_c25.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/closed_c25.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/print_layout.step.py --write
```

Observed command outcomes: fast2 tests pass, generation exits0 with all four targets `built`, full3 tests pass in94.78s, refs exits0 with `ok:true` and no warnings. The `addopts` override only restores the elapsed-time summary suppressed by the repository's double-quiet setting. Exact exterior polygon count body10562/cap6569,total17131, first count1.1265s. Scalar tests establish full dimensions, no duplicate editable lengths, fixed bores under D changes, negative radial-gap readouts when D32, L+4.8 without changing pitch/count/phase, positive/allowance/domain guards, nominal reference-envelope dimensions/end joints, unchanged R5 thread section laws and route bounds. No broad nondefault CAD certification is implied.

## Actual implementation evidence

| Check | Result |
|---|---|
| Source construction topology | Body and cap each one valid positive-volume solid. Exterior faces10562/6569, final faces10584/6593. Canonical edge mismatches at most1.142e-13mm body and4.640e-14mm cap. Actual noncircular planar closures reuse shared boundary edges; no free or multiple sewn edges. |
| Outer construction/sewing | Body55.009–57.867s; cap24.018–24.347s over generation calls, below600s. |
| Final Booleans | Body29.295–32.082s; cap27.983–31.302s, below600s. |
| Written target completion | Body95.123s, cap63.317s, closed154.555s, layout155.124s; each below600s. Entire four-target run468.120s, below1800s. No timeout or repair cycle was triggered. |
| Written topology/counts | Imported body/cap each1 valid positive solid; closed/layout each2 valid positive solids. Diagnostic device does not appear in any primary target. |
| Closed artifact facts |2 leaf occurrences,2 shapes,17177faces; bounds[-19.5,-19.498274,-135] to[19.5,19.498274,84], dimensions39x38.996548x219. CLI refs success only proves resolution; validity and counts were separately tested on imported solids. |
| Full floors/bores/drains | Actual inner-floor datums-132/81 verified across each floor transition. Body bore straddled at radii14.99/15.01 at four full-body stations; cap at15.49/15.51 at three straight-bore stations. All14 holes verified at three depths: center and radius1.49 void, radius1.51 material. Floor material between holes remains present. |
| Written poses | Body height144, cap84, closed219; layout exactly two objects, both bedsZ0 and openings up, centerX approximately±23, heights144/84. Layout within85.02x39.02mm, nominal85x39x144. |
| Reference and parametric behavior | Source reference cylinder is a valid diameter29/length208 solid with lower/upper joints at-129.5/78.5. Readouts show nominal2.5/2.5 gaps and0/5 bottom-resting comparison, explicitly unretained. The section helper is supplied for independent visual use; its large actual-solid cut was not redundantly run by implementation. |

The lightweight source-volume accessor reports body65524.001433mm3 and cap35022.734842mm3. These are diagnostics, not adaptive source/STEP parity evidence. Independent parity must use the prescribed BRepGProp integration and <=0.001mm3 tolerance; no loose accessor comparison is claimed.

## Exact artifact identity

| Artifact | SHA256 |
|---|---|
| `cad/p1_r6_full_case/body.step` | `b5d425acecb35a57264e4267b7958608af289d2975c53c6d94c059083226fbdd` |
| `cad/p1_r6_full_case/cap_c25.step` | `7165de16ff6e8b1246b5fe654e0e023a90c2e6e226f721606731616b7c8cb6fc` |
| `cad/p1_r6_full_case/closed_c25.step` | `1b32f20cd81a5765bec7caa39870fded0f56aad660443acea790c260ee2d96f3` |
| `cad/p1_r6_full_case/print_layout.step` | `b147fd200524ca0471c5d22519e27fd27ad07d1a0311a10dd272a21da3efbe4b` |

Source, wrapper and test hashes are in candidate135. Source reference helper `review.py` SHA256 `b7dcdb05eba4b62391a120398b28fa58e969c6b070d4e58cfd642cf9259536da`; meaningful parameter module `params.py` SHA256 `375d90e90d69c9c67db1625d05ef13a7562b49cbe8c19013777fa0a401949c7f`. After freeze only this receipt was updated; no candidate file changed.

## Coverage, remaining gates and handoff

REQ01/03/05/08/09/11/12: original full source, derived213 cavity/219 outside,39 envelope, fixed bores, original field, wall budget, fourteen floor holes, native datums and four two-part outputs have implementation evidence. REQ06/07: R5 thread family and external-stop geometry are retained, with selected scalar law comparisons; actual interface/motion/negative-stop evidence belongs to independent validation. REQ10: intended opening-up poses and arithmetic slope bounds are implemented; actual worst normals/new-phase first-layer footprint and later slicer/process remain distinct gates. REQ02/04/13/14: measurements, loaded physical fit and literal both-end noncontact remain open; user explicitly authorized provisional full CAD and declined another short version.

High physical risk remains the1.4mm male root wall/new B thread. Medium physical risks remain fit/wobble and loaded/table-occluded drainage. No geometry contradiction, topology failure or generation ceiling breach occurred; one full implementation attempt, no geometry repair cycle. No physical, slicer or broad parameter-domain acceptance is claimed.

Scratch evidence: `scratch/fullcase-impl/{scalar-tests.log,generation.log,tests.log,refs.json,refs.log,freeze.json}`; not release assets. Changed authoritative paths are the new R6 CAD namespace, `tests/test_full_case.py`, this receipt and candidate manifest. Root may now publish the full review viewer and schedule the distinct critic/validator on candidate135, then the formal reviewer. Mandatory STEP snapshots and dimensioned nominal-device section, actual collisions/motion/envelope path, source/STEP parity and independent wall/normal/first-layer evidence remain downstream. Root owns PROJECT_STATE/HANDOFF/NEXT_AGENT updates.
