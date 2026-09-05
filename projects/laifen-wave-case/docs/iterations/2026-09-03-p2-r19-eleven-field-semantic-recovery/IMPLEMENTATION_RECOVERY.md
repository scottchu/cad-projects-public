# R19 implementation recovery receipt

**Owner:** `IMP-GCS-R19-REC-02`  
**Status:** candidate frozen; awaiting the independent VAL, CRIT, and REV role join required by R19-10.  
**Frozen design fingerprint:** `cc4d1cd276a1394d000745e1177ae9eb3a3b114ed9bf7994c4622ee7c5432eef` (23 input-manifest entries verified).  
**Candidate fingerprint:** `566aa6bc8c0aa57f1aeea341805a48db7d54c2078a48cebc4f9204a685e2fc74` (`candidate-files.sha256`).  
**Evidence fingerprint:** `01dca854cd3048c0d5adece7e2325a2fb9e5abde3c512d75f5169f555c282966` (`evidence-files.sha256`).

## Implemented scope

- Added the standalone R19 preview renderer, local 84-row map, controls, disclosure, and CSS under `preview/p2-r19-eleven-field-semantic-recovery/`.
- Added the five R19 tests, including local-only category-sheet and six-context browser coverage.
- Added compact collecting evidence and 14 normal/caption-hidden category sheets in `scratch/r19-*` (64 KiB total).
- Repaired the eleven R18 residual mappings with descriptor-local geometry, dimensions, and truthful font metadata. The coverage target uses the actual weighted-field transition bounds and descriptor height.

## Validation

The initial collecting audit was 73/84. The initial implementation reached 82/84; grouped repair 1 corrected the metadata-class extractor and reached 83/84; grouped repair 2 replaced the coverage span with the weighted transition-bound bracket and reached 84/84. No oracle was relaxed.

Commands and results:

```text
node projects/laifen-wave-case/scratch/r19-collecting-audit/audit.mjs
{"pass":84,"fail":0,"fields":[]}

node projects/laifen-wave-case/tests/test_p2_r19_target_contract.mjs
R18 map/source/exact-one passed
node projects/laifen-wave-case/tests/test_p2_r19_render_observability.mjs
R19 84-row PASS 84
node projects/laifen-wave-case/tests/test_p2_r19_visual_families.mjs
R18 10 explicit patterns passed
node projects/laifen-wave-case/tests/test_p2_r19_ui_contract.mjs
R18 UI passed

uv run python projects/laifen-wave-case/tests/test_p2_r19_browser.py
R19 category sheets and strict browser bbox passed: Chromium/Firefox/WebKit desktop/mobile
```

The browser repair selects `surface.envelope=fade_from_bottom` and `label.mode=inset` through the actual R19 controls before checking those conditional targets. It verifies nonzero bboxes for `closure.screw.leadRunoutTurns`, `surface.coverage`, and `label.weight`; no page errors; and no horizontal overflow at `1280x900` and `390x844` in Chromium, Firefox, and WebKit. Normal and caption-hidden category sheets were captured before that matrix.

## Limits and next action

This is conceptual browser-preview evidence only. It makes no CAD, OpenSCAD, export, slicer, printability, fit, drainage, physical, live-route, serving, or delivery claim. The next action is independent validation, caption-hidden critique, and review against this exact candidate/evidence pair.
