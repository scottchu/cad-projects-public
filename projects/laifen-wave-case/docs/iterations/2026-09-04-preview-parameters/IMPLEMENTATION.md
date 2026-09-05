# Preview parameter readout implementation

**Task:** `PPV-02`  
**Owner:** `preview_params_impl`  
**Status:** candidate prepared for independent validation  
**Verified input fingerprint:** `a63279a10cdf763d599f8730c82b81d63f5e73f117c59208b12abd184c474115`

## Result

`cad/container_generator_v1/preview_parameters.py` deterministically generates
the committed self-contained `closed.params.js` sidecar from the authoritative
`PARAMETER_SPECS` registry and one `derive(preset())` result.  The sidecar has
one `00 READ ONLY` notice, all 26 registry rows in the frozen display-group
order, and 14 readouts from that resolved record.  Every row is a one-option
enum; the module has no imports, features, animations, or presentation effects.
Its `update(_context)` body is an explicit no-op.

`closed.step.py` alone now returns the supported shape-plus-`closed.params.js`
envelope.  No STEP was regenerated or edited.

## Verification

Commands ran from the repository root unless noted otherwise.

| Gate | Command | Result |
| --- | --- | --- |
| Frozen input identity | `shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-preview-parameters/INPUTS.sha256` | PASS: required fingerprint matched. |
| Frozen present inputs | `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-04-preview-parameters/INPUTS.sha256` | 15 project inputs PASS; 5 archived `external/cad-viewer-0.4.28` entries are absent from this checkout. |
| Generator | `cd projects/laifen-wave-case/cad && uv run python -m container_generator_v1.preview_parameters` | PASS: wrote only `closed.params.js`. |
| Focused source tests | `uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_preview_parameters.py projects/laifen-wave-case/tests/test_container_generator_v1_parameters.py projects/laifen-wave-case/tests/test_container_generator_v1_requirements.py -q` | PASS: 32 tests. |
| STEP byte guard | `shasum -a 256 projects/laifen-wave-case/cad/container_generator_v1/{body.step,cap.step,closed.step,print_layout.step}` | PASS: all four required hashes retained. |
| Whitespace | `git diff --check` | PASS. |

The first focused run exposed the pre-existing AST scope guard that prohibits a
directly named `derive(...)` call in non-entrypoint modules.  The only repair
was to import the same function as `resolve_parameters`; this preserves the
single derivation boundary and lets the new readout module consume the required
resolved record.  The rerun passed.

## Repair cycle 1

Independent critique found that the two derived radial-gap strings placed
`, reference only` before the numeric value. The formatter now keeps that
qualification as a suffix, yielding exactly `0.5 mm radial, reference only -
derived readout` and `1 mm radial, reference only - derived readout`. Focused
regressions assert both frozen labels before regeneration parity is checked.

## Requirement coverage and limits

`PPV-SOURCE`, `PPV-COVERAGE`, `PPV-GROUPS`, `PPV-READONLY`, `PPV-NOEFFECT`,
and `PPV-ENTRY` have focused automated coverage. `PPV-BASELINE` is covered by
the four fixed SHA-256 assertions. `PPV-VIEWER` remains for independent
validation: this implementation task did not start or alter the Viewer runtime,
access its endpoint, or perform the required mobile-width review.

CAD/source and written STEP acceptance remain inherited only; slicer/process is
HOLD and physical acceptance remains PARTIAL / UNBOUND. This implementation
receipt is not an approval of its own candidate.
