# VFR-10 browser implementation receipt

Status: **RESTORED / BLOCKED. No candidate is available for independent review.**

Owner: `/root/openscad_vfr10_browser_impl`, sole V10-I implementation role.
Project: `projects/laifen-wave-case`. Worktree:
`/Users/scottchu/.codex/worktrees/4f8c/design-projects`. Frozen input fingerprint:
`ba2cd28bd118fe6775e36f41bf01477edd92bceb3487f98fc13a0a99608977ec`.
The VFR-10 input manifest verified 18/18 before implementation and again after
restoration.

## Bounded attempt and rollback

The initial private candidate changed only `src/main.mjs`,
`tests/test_openscad_wasm_simulator.py`, and new private test evidence. It
implemented synchronous terminal invalidation, captured `id` before identity
awaits, exact `id/worker/message-id` callback guards, exact result tuple
checks, and moved the 180000 ms watchdog inside worker setup. It preserved the
disabled Diamond surface controls and did not change schema, worker, vendor,
runtime, SCAD, HTML, CSS, dependencies, hosting, CAD, slicer, or printer state.

Before editing, exact baseline main/test bytes and the local dist were retained
under `scratch/vfr10-browser-implementation/c1/baseline/`; its inventory-file
SHA-256 is `da3ffbe2ebb9a0e1058c4a3e137d5816b1521ab61646dde45eab45a73a1c1`.
The first private Chromium run failed at the P0 harness because the test used
placeholder source bytes to calculate frozen migration anchors. The one allowed
focused repair changed only the private harness calculation to use actual source
and lock bytes. The rerun passed P0 but then failed before a mesh gate because
the harness treated the `status` element ID as a guaranteed Chromium global;
that value was `None` while reading the seeded smooth result. This exhausted the
one-repair ceiling. The failure is a harness/protocol-evidence failure, not a
Diamond geometry, timing, topology, or physical finding.

Per VFR-10 rollback rules, the production main and existing test were restored
byte-for-byte and the generated candidate dist was moved to
`scratch/vfr10-browser-implementation/c1/failed-built-dist/`. The temporary
new `tests/vfr10_browser_gate.py` was removed. No public bytes or service were
changed. Restored hashes are:

| Path | SHA-256 |
| --- | --- |
| `preview/openscad-wasm-simulator/src/main.mjs` | `98af41e1377afb873208977eedc679ea9e887b04b96253bc2025b3896fbeb353` |
| `tests/test_openscad_wasm_simulator.py` | `caab4001caf57e36ad3d54e0de366ecb02306cb462c3ea5e0b965568e3fae4eb` |

## Commands and results

```text
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR10_BROWSER_IMPLEMENTATION_INPUTS.sha256
# 18/18 OK before work and after restoration

uv run pytest -p no:cacheprovider projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_vfr08_functional_repair.py -q
# 17 passed before work and 17 passed after restoration

npm run build:openscad-simulator --workspace laifen-wave-case
# exit 0; frozen candidate dist retained privately

uv run python -B projects/laifen-wave-case/tests/vfr10_browser_gate.py
# attempt 1: P0 anchor harness assertion failed
# focused repair: actual source/lock bytes
# attempt 2: status-global harness AttributeError; rollback required
```

No real smooth P3 completion, real parser-error recovery, Diamond body/cap/
assembled/print-layout worker receipt, browser mesh analysis, visual review,
or full identity/download/timing evidence completed. Those requirements remain
HOLD. This implementer makes no approval claim; root must reopen the design or
assign a new bounded task before retrying browser acceptance.
