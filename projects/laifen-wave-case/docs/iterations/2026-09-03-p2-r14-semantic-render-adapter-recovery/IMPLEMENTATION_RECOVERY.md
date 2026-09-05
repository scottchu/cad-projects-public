# IMP-GCS-R14-01 implementation stop receipt

**Status:** STOPPED NONCANDIDATE before browser work. No candidate or evidence manifest was frozen.

## Provenance and scope

- The 24-entry R14 frozen input manifest verified before implementation, including all nested R13 manifests. The verified R14 design fingerprint was `ff0f85197408ec890f0a5870c641f778515d6fc468965b85e3147ca44dd9380f`.
- Writes were confined to the new R14 preview, four cheap-gate tests, and this receipt. R13, R12 core/schema/derive/tests, live routes, CAD, OpenSCAD, STEP, slicer, continuity, and unrelated files remained read-only.

## Work and gate result

The new adapter has a 84-row semantic target map, one primary target per active field, descriptor-only rendering, Basic/Advanced UI, and source-ban checks. The initial target-contract gate passed:

```sh
node projects/laifen-wave-case/tests/test_p2_r14_target_contract.mjs
# R14 target contract passed: source ban, 84-row map, and exact-one active target
```

The required stripped-geometry observability gate then failed. Two focused repairs were used:

1. Added real wall/floor, phase, clearance, minimum-wall, and keepout geometry to replace inert semantic targets.
2. Routed dimension annotations through descriptor-derived rotation and sampled surface values rather than a split fallback.

The rerun still fails on the valid A/B pair for `closure.screw.formHeight`:

```text
AssertionError [ERR_ASSERTION]: closure.screw.formHeight
```

Its stripped primary target remains byte-identical, so the required semantic geometry delta is absent. This is a cheap-gate failure. The R14 contract allows the initial attempt plus only two focused repairs, so no third patch, visual-family run, browser test, capture, candidate manifest, or delivery action was performed.

## Partial source fingerprints

- `target-map.mjs`: `fb7e8b662a614dde8cdb4f0f51f3ff97eaf16b87fc26a7cae8f0608b706881c3`
- `render/renderer.mjs`: `c34090e0d8b5f152f4572f97525a8efa94ac27a9e21b3e3d0a4d6c78043486a6`
- `app.mjs`: `246db66e079be488d74a71f80fe6dd9f5a73b29340b8c04894b6cef511ee24d7`
- `test_p2_r14_render_observability.mjs`: `3127d9fdf41e62bb276902b0430e145479ba2887450cb9c38c0764ecec7e477d`

## Next action

The coordinator must reopen or reduce the R14 contract before another implementation attempt. The smallest correction is to make the screw form-height primary target a true magnified thread-profile height dimension derived from `descriptor.closure.primitive.height`, then restart the cheap-gate repair ledger and rerun all cheap gates before any browser work.
