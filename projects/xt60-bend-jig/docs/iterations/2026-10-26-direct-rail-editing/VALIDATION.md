# Validation

Root self-check: eight focused Node tests PASS, including curved midpoint/endpoints,
both inverse-frame reconstructions, translated shape invariance, curved SVG
paths, legacy JSON migration and extreme curved viewport envelopes.

Actual HTTPS Chrome test at https://mac-mini.duckbill-ionian.ts.net:8480/:
PASS endpoint O/E drags without toggles, whole-path drag with equal endpoint
deltas, curve-dot drag preserving endpoints, outer paths updating, fixed cuts
while scrubbing, JSON save/load/reload persistence, keyboard line/curve editing,
separated stationary-Green endpoint controls, desktop/mobile overflow. Zero page
errors. Root inspected the desktop screenshot. Native touchscreen untested.

Command: canonical root .venv/bin/python with task scratch/direct-edit-browser/check.py.
Root environment reused; no additional runtime or dependencies. Full workspace
and structure checks plus independent review pending.

## Final verification

- npm test --workspaces --if-present: PASS, 34 XT60 tests, including eight
  focused rail tests; other declared workspace tests passed.
- npm run build --workspaces --if-present: PASS.
- Canonical-root uv run pytest with explicit CAD_WORKBENCH_CHECKOUT and the
  task repository structure test: PASS, 11 checks. No dependencies, lockfile or
  Python/CAD source changed; prior ten-case Python baseline receipt is reused.
- Permanent browser regression: BROWSER_CHECK.py in this iteration, using the
  sole canonical root .venv interpreter, optional --url argument. Default is
  the offline HTML. Actual --url https://mac-mini.duckbill-ionian.ts.net:8480/
  PASS after both hit-testing fixes, including default Green whole-line drag
  and a stationary Green placed exactly at the axle. elementFromPoint selects
  data-line=2 in both cases; both endpoints move together. Zero page errors.
- Actual HTTPS response 200; served HTML SHA256
  56b9e5144160e73f7a3a439641dc7fcca04caa0ca7c91222cf6348605b9f6cf2
  equals the final standalone artifact and manifest entry.

## Independent numeric validation

/root/rail_validator (medium), packet-based validation in functions.exec V8:
4,332 quadratic Bezier comparisons, 64,980 inverse/forward component checks,
64,980 viewport component checks, 60 saturating translation checks: PASS.
Maximum reconstruction error 2.84e-14, deformation error 3.55e-15. Numeric
functions unchanged during subsequent hit-testing-only fixes. This validator
did not inspect current disk hashes or browser integration; those are root
self-checks. Degenerate endpoints, zero bend, absent legacy bend and extreme
bends passed. No physical-touch, CAD or fabrication claim.
