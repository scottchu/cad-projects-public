# P2 R16 final semantic mapping recovery handoff

**Status:** frozen design contract written; implementation not started.  
**Owner:** `DES-GCS-R16-REC-01`.

R16 is a residual-only recovery from R15. R15's frozen fingerprint is `550dfb50af2b9ea950471d114ac9485a9ec507742225e6dcb80c219f88b15301`, and the current collecting audit reproduced **70/84 PASS** with exactly 14 fields remaining:

`container.sideCount`; `closure.screw.radialClearance`; `closure.bayonet.radialClearance`; `surface.reliefMode`; `surface.minWall`; `surface.fadeMetric`; `surface.keepout`; `label.mode`; `label.openScadFontFamily`; `label.orientation`; `label.target`; `label.axialFromTargetEnd`; `label.patchMargin`; `attachment.attachHalf`.

Exact implementer scope:

- `projects/laifen-wave-case/preview/p2-r16-final-semantic-mapping-recovery/**`
- `projects/laifen-wave-case/tests/test_p2_r16_target_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r16_render_observability.mjs`
- `projects/laifen-wave-case/tests/test_p2_r16_visual_families.mjs`
- `projects/laifen-wave-case/tests/test_p2_r16_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r16_browser.py`
- `projects/laifen-wave-case/scratch/r16-*/**`
- R16 receipts/manifests under this iteration directory

Stop before browser/category sheets unless the full collecting audit is 84/84 PASS, source-ban PASS, exact-one PASS, 0 unexpected inactive targets, 0 duplicate primary targets, and <= 1 MB. Stop entirely on prior/core/live/CAD edit need, descriptor-gap claim, value-hash or `.field-witness` mechanism, source-ban failure, target duplication/leak, or retry exhaustion.

Initial attempt plus at most two full-group repair cycles are allowed. No live route, served copy, delivery, CAD/OpenSCAD/STEP/slicer/print, MakerWorld, or physical acceptance is authorized before independent validation, independent critique, and formal review all PASS one R16 candidate fingerprint.

Frozen input manifest: `inputs/frozen-inputs.sha256`, 22 entries, SHA-256/design fingerprint `8604d5a9fb6275a949f385153fcf4f8c3c54551d87058b68b607ebac33766dfc`.
