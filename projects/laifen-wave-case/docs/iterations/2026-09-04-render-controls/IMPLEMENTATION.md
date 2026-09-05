# RCV-02 implementation receipt

**Owner/role:** `/root/render_controls_impl_b`, prescribed implementation agent.
**Status:** PASS — candidate frozen for independent critique and validation.
**Frozen input manifest:** `INPUTS.sha256`, SHA-256 `2ac420ce1eb43f6adb12d39d41416a24167a7ef7a3990a490107f8caed5a80e4`.

## Delivered scope

`preview_parameters.py` remains the sole source for the self-contained `closed.params.js` sidecar. It now emits one `VISUAL PREVIEW ONLY` disclosure, ten bounded render-only controls, two authored-name Viewer features, and then the unchanged 41 read-only rows. The module exports `solveVisualPreview(rawParams)` and uses only `effects.transform()` and `effects.style()` in `update()`.

The transform solver clamps all declared bounds, scales around the shoulder origin, and uses ordered scale, `+Z` rotation, and `+Z` translation for the cap. Its screw illustration is exactly `360 * turns` degrees and `2 * turns + extra_lift` millimetres. Identity defaults emit no effects calls.

## Changed paths

- `cad/container_generator_v1/preview_parameters.py`
- `cad/container_generator_v1/closed.params.js` (regenerated from the source)
- `tests/test_container_generator_v1_preview_parameters.py`
- `docs/iterations/2026-09-04-render-controls/candidate-files.sha256`
- this receipt

No STEP, CAD generator, service, route, slicer, or printer file changed.

## Evidence

1. `/usr/bin/shasum -a 256 -c docs/iterations/2026-09-04-render-controls/INPUTS.sha256` passed all 23 frozen inputs before editing.
2. `uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_preview_parameters.py -q` passed: `7 passed`.
3. The Node effects mock checked 52 rows, zero effects at defaults, a one-turn cap result of 360 degrees and +2 mm screw travel, transform ordering, style targeting, and out-of-range/non-finite clamping.
4. `candidate-files.sha256` binds the source, generated sidecar, focused test, unchanged entrypoint, and all four frozen STEP bytes.

## Limits and next action

This is a Viewer-time presentation candidate only. It does not regenerate CAD or establish fit, wall thickness, thread clearance, collision, printability, slicer, or physical acceptance. RCV-03 must critique the frozen candidate and RCV-04 must independently validate it, including the private mobile page, before RCV-05 formal review.
