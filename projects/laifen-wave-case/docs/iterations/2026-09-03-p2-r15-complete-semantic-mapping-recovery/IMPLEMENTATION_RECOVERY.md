# IMP-GCS-R15-01 stop receipt

**Status:** STOPPED NONCANDIDATE before browser work.

R15's 24 frozen inputs, including the R14 compact audit, verified before implementation. The frozen fingerprint is `550dfb50af2b9ea950471d114ac9485a9ec507742225e6dcb80c219f88b15301`. Writes stayed in the R15 preview, R15 tests, R15 scratch audit, and this receipt; R14/R13/core/live/CAD remained read-only.

The source-ban/exact-one target gate passed. The collecting 84-row audit ran after the two permitted grouped repairs and returned **70/84 PASS**, not the required 84/84. Its remaining failures are:

- `container.sideCount`
- `closure.screw.radialClearance`, `closure.bayonet.radialClearance`
- `surface.reliefMode`, `surface.minWall`, `surface.fadeMetric`, `surface.keepout`
- `label.mode`, `label.openScadFontFamily`, `label.orientation`, `label.target`, `label.axialFromTargetEnd`, `label.patchMargin`
- `attachment.attachHalf`

The two repairs addressed nonsemantic clamping in the initial general mapping, but the grouped audit remains below the mandatory cheap gate. Browser/category-sheet work, candidate manifest, evidence manifest, delivery, and serving were not started. A new refrozen attempt must replace the residual generic mapping with the per-group local semantic features specified in R15 DESIGN, then rerun the complete audit rather than a first-failure assertion.

Exact commands:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r15-complete-semantic-mapping-recovery/inputs/frozen-inputs.sha256
node projects/laifen-wave-case/tests/test_p2_r15_target_contract.mjs
node projects/laifen-wave-case/scratch/r15-exhaustive-audit/audit.mjs
```
