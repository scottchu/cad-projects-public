# IMP-R6-04 native runout production repair

Owner `/root/case39_impl`, implementation role. Production patch applies the demonstrated native trim correction from EXPORT_REPAIR_TRIAL.md. Independent validator, critic and formal reviewer own acceptance; this receipt is implementation evidence only.

## Immutable inputs and preserved baseline

Before mutation, all144 path/content pairs in `inputs/native-repair-contract.sha256` verified, fingerprint `8770dd5e76e5227d99481f5487f371a69f3c4e8e0e91acd63274982c415907b1`. This binds the official135 baseline, exact successful trial and review preparation. Original135 fingerprint is `4c2750ad632639be5547074173408aa14dfc579faed8d45890ed7233b00c0351`.

The six existing files authorized to change were archived before mutation under `scratch/fullcase-export-repair/production/before/` with original path/hash mapping in `before-map.json` and archive manifest `before-map.sha256`: parts.py, README.md, test_full_case.py and cap_c25/closed_c25/print_layout STEP. The body STEP, all four wrapper sources, params.py, thread_profile.py, skin.py, surface.py, review.py and earlier iterations are preserved. The archived map retains the original135 evidence despite the intentional production updates.

## Minimal correction

New `cad/p1_r6_full_case/runout.py` selects the upper female helical/conical shared-edge role by surface types, shared topology, neck-height and crest-radius datums. No face index is used. It isolates topology while sharing exact geometry, projects the existing topological vertex onto the existing3D curve, updates the edge range across all representations and updates that vertex's edge parameter with its existing tolerance. There is one call from `build_cap` after floor-drain Boolean/cleanup. No body construction, profile law, dimension, coordinates, surface geometry or tolerance metadata is altered.

Production witness: residual0.002561321256408349mm becomes5.8723005580186607e-8mm, range[0,1] becomes[0,0.998849758492207], vertex tolerance remains0.002561321406033683mm. Guards require at most one role match, residual correction<=0.01mm, a projection inside the existing interval and within1e-7mm, trim fraction<=1percent, unchanged tolerance and a valid single closed solid. Copy isolation prevents the correction mutating the cached raw female tool or other occurrences.

## Focused gates and generation

The raw native-tool regression reproduces the actual tolerance-covered endpoint mismatch, checks correction to<=1e-7mm and verifies the cached raw tool remains unchanged. The cap regression uses the generated source and written cap STEP with adaptive volume integration at eps1e-10; the original absolute delta<=0.001mm3 gate remains unchanged. Unaffected body/math field tests are not repeated for this repair.

Only cap_c25, closed_c25 and print_layout are regenerated. The production driver executes the installed `gen --write` launcher for those exact wrapper sources using the root uv Python3.12. Each owned process group is bounded to600s; cumulative generation is bounded to1800s. No mesh substitute, manual STEP edit, roundtrip canonicalization, broad healing or relaxed threshold is used.

```sh
uv run pytest projects/laifen-wave-case/tests/test_full_case.py -q -o addopts='' -k native_runout
uv run python projects/laifen-wave-case/scratch/fullcase-export-repair/production/generate.py
uv run pytest projects/laifen-wave-case/tests/test_full_case.py -q -s -o addopts='' -k 'native_runout or repaired_cap'
```

The driver records exact installed launcher commands, native correction witnesses and stage timings in `production/generation.log`; focused evidence is in `production/focused-tests.log`. The first endpoint-only test passed in2.11s. Both final focused regressions passed in83.88s (2passed,3deselected). Adaptive source cap volume35022.740669795305mm3 and written volume35022.740655030386mm3 differ by0.000014764918887522072mm3 at eps1e-10, passing the unchanged0.001mm3 gate. Cap export completed in63.243s with6593faces, valid single solid; cap SHA256 `5b47075e5ee27dc57b8089c7955856e15119b8a7692569c2f0f532d4a21f4afe`.

At cap completion, source/helper/tests/README plus cap/body and archived inputs were frozen in `production/cap-ready.sha256`:143 entries, fingerprint `92aeb54c592d2b0d6c98914f7b4bb6e4de58871dca9795deb716ae83e329ae42`. Moving closed/layout exports are excluded from that interim manifest. This enabled independent cap review while the remaining two exports ran.

## Status and next action

Implementation completed in one production attempt with no repair retry. Final immutable manifest `inputs/implementation-repaired.sha256` has145 entries, SHA256 `a3873490fc7d7742698d9d73aceb6a8a29131fd8b846c76973d7133afb438bdc`. It updates the original135 path list, adds the native helper and binds the native repair contract, archive map and all six preserved originals. Both final focused tests pass. Affected written occurrence/visual acceptance is delegated to the independent validator/critic; no additional broad tests were run by the implementer. The repaired source and STEP must undergo independent runout law/parity, affected occurrence and visual review before formal acceptance. Slicer/process and physical thread, strength, loaded fit, drainage under blocked conditions and device-end noncontact remain separate open evidence. This repair adds no device retention and makes no physical acceptance claim.


## Final export and preservation receipt

| Target | Generation seconds | SHA256 |
|---|---:|---|
| cap_c25.step |63.243250458|`5b47075e5ee27dc57b8089c7955856e15119b8a7692569c2f0f532d4a21f4afe`|
| closed_c25.step |177.582933333|`31e4125fcfc6d6c543312491298d8a508f0d2db9a5da247b6a933b6fa7d3efa6`|
| print_layout.step |294.198662125|`be27b1c7962bcc241babea257aa85b11bc1675b83072f475bf684e865d166410`|

Total generation535.026878458s. Largest observed stage: body Boolean99.690s during layout generation; largest outer stage93.760s. All target/stage/cumulative limits were met. The source body and cap remain valid one-solid parts with10584 and6593 final faces respectively. Every cap-containing target logged the same single endpoint correction and preserved tolerance. The original body STEP hash remains `b5d425acecb35a57264e4267b7958608af289d2975c53c6d94c059083226fbdd`.

Exact installed export commands, invoked sequentially by the bounded production driver:

```sh
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/cap_c25.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/closed_c25.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/print_layout.step.py --write
uv run python projects/laifen-wave-case/scratch/fullcase-export-repair/production/freeze.py
```

The driver uses the absolute root `.venv/bin/python3` for each child and sets `CADGEN_WARM=0`. Driver SHA256 `6b769a04a04ed7633d449fc577a8b7511eb21152b2c166abfe79bfdc00b5eb36`. The final stdout result and exact artifact sizes/timings/hashes are in `production/candidate.json`; the readable source diff is `production/source-changes.diff`.

Post-mutation preservation verification checked all135 original-candidate entries and all144 native-repair inputs, substituting only the six declared exact before-archives. Thus129 original-candidate paths and138 native-contract paths are unchanged at their original paths; all six changed originals retain verified archived bytes. All143 interim cap-ready entries verified unchanged before the final145 manifest was written. `production/preservation.json` records every original/verified path and hash. The final145 manifest was rechecked after receipt completion.

Changed authoritative paths are exactly `parts.py`, new `runout.py`, README.md, test_full_case.py and the three cap-containing STEP files. Source dimensions, pattern laws, radial thread law, bores, drains, skin accuracy, native datum/pose construction and all earlier-iteration files remain frozen. The correction resolves the demonstrated source/export parity failure without weakening the gate; independent source-law, STEP occurrence and visual evidence remain the authority for final CAD/STEP acceptance.
