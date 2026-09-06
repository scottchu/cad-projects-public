# PF-VAL-ORACLE preparation

Status: PREPARED. This is a planning-only independent oracle; it imports no moving product code and makes no candidate claim.

Frozen inputs:
- DESIGN `426729855f05805f16661cc3728a6145b2eac291b56f60199fc6ca7528cc3e61`
- BRIEF `28483df404ab8b99528cdedb71ba98ef4f2f1146015a0b110904a7d4c78f71b6`
- VALIDATION_PLAN `2aefb747139641d74a6297e22e63fd6de8b4d91e1170e885e3a4e624a3841399`

Durable oracle: `projects/laifen-wave-case/tests/node/pattern-families-independent.test.mjs`.
It derives Diamond arc/count/plateau/slope/literal-ceil guards; new-family `N/n/M/E` and wall guards; phase continuity; inward radius; and exact off-grid keyboard witnesses.
Finite witnesses include all spacing/depth endpoints, Diamond size endpoints, wall equality and 0.01-mm failure, Ribs count transition, Rings/Spiral ceil transition, and non-finite rejection.

Prepared scratch tools under `/tmp/pattern-families-full-validation/`:
- `compile_matrix.mjs`: source/runtime-hash-bound sequential pinned-WASM compiler with argv, messages, timing, byte hash and receipt.
- `mesh_probe.py`: approved pilot topology/orientation/volume/component probe.
- `approved_spiral_feature_probe.py`: accepted pilot feature/radial/seam probe retained as a candidate-binding reference.

Preparation checks:
- `node --test projects/laifen-wave-case/tests/node/pattern-families-independent.test.mjs`
- `node --check /tmp/pattern-families-full-validation/compile_matrix.mjs`
- `PYTHONDONTWRITEBYTECODE=1 uv run python -c 'import ast,pathlib; [ast.parse(pathlib.Path(p).read_text()) for p in ("/tmp/pattern-families-full-validation/mesh_probe.py","/tmp/pattern-families-full-validation/approved_spiral_feature_probe.py")]'`

After candidate freeze: verify its manifest; bind expected oracle results to candidate schema/adapter/source guards; run focused Node/Python gates; then compile the finite matrix and apply the actual mesh/global/feature probes. Do not infer arbitrary-parameter or physical acceptance from the finite set.

Scope: only this oracle, this record and `/tmp/pattern-families-full-validation`; no source, other tests, browser, build, service or dependency changes.
