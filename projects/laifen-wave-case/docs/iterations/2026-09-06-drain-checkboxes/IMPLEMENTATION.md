# DR-IMP-01 implementation receipt

Frozen inputs were `BRIEF.md` SHA-256
`7dc049f0734ad7788869b2d8c452dfd95dd5f5b34a49d0fe7dc1da443348bbdd` and
`inputs/baseline.sha256` SHA-256
`16128041328e85ec25bfbaf6c90e0dc937b310ebc9306745a98390c9fcaa8845`.
Baseline HEAD was `7b9c960f1a2ef1e0b211c3cbd3f9c0c3a0ab42ef`.

The Drain holes select is now a native, independently selectable Top/Bottom
checkbox group. The controller maps its four states to `none`, `top`,
`bottom`, and `both`; the existing Bottom-only default and Reset behavior
remain. Checkbox edits use the existing `edit()` invalidation route, so they
never generate automatically and cancel a stale active generation. Dimension
draft validity and lifecycle behavior are otherwise unchanged.

The browser adapter, draft bounds, and runtime schema accept the same four
enum values. The authoritative OpenSCAD source accepts `both` and applies the
existing bottom cutter to the body and the existing top cutter to the cap in
both smooth and diamond shell branches. No cutter dimensions, locations, or
other geometry changed.

Focused checks passed:

```sh
node --test projects/laifen-wave-case/tests/node/compact-controller.test.mjs \
  projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs
uv run --frozen --package laifen-wave-case pytest -q -p no:cacheprovider \
  projects/laifen-wave-case/tests/test_openscad_customizer.py \
  projects/laifen-wave-case/tests/test_vfr08_functional_repair.py
git diff --check
```

The Node suite passed 27 tests, including four checkbox mappings, invalid-draft
preservation, active-generation cancellation, reset, and enum rejection. The
Python suite passed 12 tests. This receipt does not establish compiled geometry,
browser acceptance, slicer readiness, or physical acceptance; those remain for
the independent validation stages.
