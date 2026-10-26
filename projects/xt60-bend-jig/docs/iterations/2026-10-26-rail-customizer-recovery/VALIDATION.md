# Simulator validation

Owner self-checks and independent validation, 2026-10-26.

- `uv sync --all-packages --all-groups` from canonical repository root:
  PASS, sole root Python 3.12 environment restored. No project-local environment.
- `uv lock --check`: PASS.
- `npm ci --ignore-scripts` from canonical root: PASS; existing audit reports
  two high-severity findings. No dependency or lockfile changes in this task.
- `npm test --workspaces --if-present` from task root with the canonical root
  install shared through a temporary root symlink: PASS, final XT60 32 tests
  include six recovered-rail checks; Kage's declared build-test passes.
- `npm run build --workspaces --if-present`: PASS, including standalone offline
  rail HTML. Other workspace generated output is unchanged or ignored.
- `git diff --exit-code -- package-lock.json`: PASS.
- `CAD_WORKBENCH_CHECKOUT=/Users/scottchu/projects/personal/design-workbench uv run
  pytest /Users/scottchu/Documents/Codex/2026-10-26/task/xt60-rail-customizer/tests/test_repository_structure.py`:
  PASS, 11 tests. Initial run without explicit provider environment variable
  failed only provider-path resolution; rerun uses the verified pinned checkout.
- Required README P13 regression subset: PASS, all ten named cases, 85.75 s,
  run from primary root using `uv run --project projects/xt60-bend-jig pytest`
  and the exact ten node IDs in root README. Those Python source/tests are
  unchanged by this simulator-only candidate.
- `node --test projects/xt60-bend-jig/tests/rail-customizer.test.mjs`: PASS,
  six tests: preserved-source parity, inverse/forward edited endpoint and axle
  closure, archived 1.7150733085690888 mm coupon witness, import rejection and
  SVG full-path/mm output, and rotated extreme-endpoint viewport envelopes.
  Initial inner-rim expectation incorrectly compared
  the rod-only rim with the historical axle-hex envelope. Added that explicitly
  documented conservative envelope and compared the archived 3-decimal warning.

Final root structure check: 11 PASS after restoring the required Active iteration
heading in the continuity index. Final workspace test/build rerun passes and
standalone output still matches the frozen manifest.

## Independent validation receipt

`/root/rail_validator`, gpt-6.1-sol/medium, read-only, PASS on
manifest `3fe9b64214c53a9e6ecf0c7df753e4e0cab65308267c1c5cebea3357d30641a5`.
Verified all nine entries and pinned Workbench policy hash. Independently ran
the six focused Node tests and the exact offline Chrome command below. Browser
checks PASS after repair, zero page errors. Additional 19,494 boundary-state
forward/inverse reconstructions had maximum component error `3.55e-14`;
seven additional malformed/range-invalid imports were rejected. Each SVG has
four complete 361-point paths with physical mm size matching viewBox scale.
Independently reproduced the original extreme-diagonal clipping and verified
the repair encloses all slot envelopes. No source/doc writes or CAD/physical
acceptance by the validator. Requested model/effort as recorded; effective
telemetry and usage not supplied by host.

## Browser and visual evidence

`uv run python /Users/scottchu/Documents/Codex/2026-10-26/task/xt60-rail-customizer/scratch/rail_browser_check.py`
from canonical root: PASS using installed Chrome, offline `file://` standalone
HTML, 1440×1080 and 390×844 viewports. No page errors. Exercised actual OPEN
and END mouse drags, invariant local slot paths while scrubbing, keyboard
coordinate/arrow edits, JSON download/load/rejection, reset, playback and three
SVG downloads. Reload persistence works in that browser context. Touch pointer
implementation is present; physical touch hardware has not been tested.

Desktop/mobile screenshots were inspected by root. One bounded visual repair
removed inactive endpoint labels to avoid collisions and cleared stale selection
text on reset/mode changes. Independent validator reruns current candidate.
Screenshot evidence is in ignored task-owned `scratch/rail-browser/`; durable
results are recorded here, not dependent on retaining that scratch directory.

Impeccable mechanical detector reported only two Inter font warnings. The
incumbent simulator already uses Inter/system fonts, intentionally preserved
for this scoped recovery. These warnings are not runtime failures.

## Evidence boundaries

This validates a reconstructed kinematic simulator and its offline artifact.
No original-page pixel parity, CAD/STEP regeneration, slicer, printer, force,
locking, wire clearance, heat, wear or physical acceptance. No server installed,
started or reconfigured. Browser inspection is agent evidence, not user acceptance.

Final delivery consistency: root Node FS/crypto readback verified all nine frozen
member hashes and aggregate after independent validation. The shell tool hit
EMFILE after checks; supported Node child-process access restored Git delivery.
No task-owned headless browser processes remained.
