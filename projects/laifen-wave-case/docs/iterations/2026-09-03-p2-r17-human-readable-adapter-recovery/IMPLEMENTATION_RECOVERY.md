# IMP-GCS-R17-01 implementation receipt

**Status:** implementation PASS and frozen for independent validation and critique. R17 remains conceptual browser-preview evidence only.

- Verified R17 frozen fingerprint `d791f7d51606e0e448ddc7b5443bb66f885700eb7f333bd651a7d1c2d0424d63` and the R16 candidate/evidence input chain before work.
- Only the R17 preview, R17 tests, R17 scratch audit, and R17 receipt/manifests changed. R16/prior, frozen core, routes, CAD, export, slicer, printer, and physical records remained untouched.
- Repaired four feature-anchored dimensions, nine descriptor-source declarations, two stripped surface aliases, bottom/top drain geometry, three default nonzero target regions, and the human-readable surface/label/attachment teaching sheets. OpenSCAD font remains separate truthful metadata.

Ordered gates passed:

```sh
node projects/laifen-wave-case/scratch/r17-independent-audit/audit.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/tests/test_p2_r17_browser.py
```

The independent-style audit reports source-ban/exact-one, descriptor source, stripped family, UI, and **84/84** semantic PASS. Chromium, Firefox, and WebKit pass at 1280×900 and 390×844 with strict nonzero target bounding boxes for the three former zero-area targets, no overflow, and no errors.

Initial browser run found only horizontal overflow. Grouped repair 1 added explicit width/min-width bounds to semantic cards; the complete audit and six-context browser rerun passed. One grouped repair remains unused. No serving or delivery was attempted. Independent VAL, CRIT, then REV remain required.
