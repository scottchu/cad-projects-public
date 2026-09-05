# PPV-03 independent preview validation

**Owner:** `preview_params_validate`  
**Status:** **PASS — repaired read-only preview candidate**  
**Verified design fingerprint:** `a63279a10cdf763d599f8730c82b81d63f5e73f117c59208b12abd184c474115`  
**Verified candidate fingerprint:** `d2b7afa66d0464455722e6257365eb26702b2704c070498594696049185848be`  
**Verified implementation-evidence fingerprint:** `98e7ed345a01b74b9cf34f30edc859b25ee53a3a942297eb676636e3bf8ee813`

## Verdict

The repaired candidate passes the preview-readout gate. The exact served
sidecar is a truthful 41-row snapshot: one prominent read-only notice, all 26
source parameters, and all 14 derived readouts. Every row has exactly one
option, and `update()` neither reads the supplied context nor changes geometry
or presentation. The two radial-gap labels now read, in full:

- `0.5 mm radial, reference only - derived readout`
- `1 mm radial, reference only - derived readout`

At an explicit `390 x 844` Chrome viewport, the private delivery page loaded
without a visible error, the unchanged two-part closed case remained present,
and the Parameters sheet showed the read-only notice and representative source
and derived groups. Opening the body radial-gap row exposed one selected option
only; selecting it produced no model, tree, or presentation change. This meets
the clarified acceptance rule that actual editing occurs in source/OpenSCAD and
that these native Viewer rows are a labeled read-only snapshot.

The earlier candidate `ae4e124b450274435cc2bea155fa59db2036120f44e99b167e46f36ead2deb25`
was superseded after its malformed radial labels were observed. No evidence for
that candidate is used to approve this repaired fingerprint.

## Frozen provenance

The assigned manifests were verified before the repaired rerun and again after
the endpoint and visual checks:

| Manifest | SHA-256 | Result |
| --- | --- | --- |
| `INPUTS.sha256` | `a63279a10cdf763d599f8730c82b81d63f5e73f117c59208b12abd184c474115` | PASS |
| `candidate-files.sha256` | `d2b7afa66d0464455722e6257365eb26702b2704c070498594696049185848be` | PASS; all four entries verified |
| `evidence-files.sha256` | `98e7ed345a01b74b9cf34f30edc859b25ee53a3a942297eb676636e3bf8ee813` | PASS; both entries verified |

Validation wrote only this receipt, validation manifests, and
`scratch/preview-parameters-validation/**`. It did not edit candidate source,
tests, STEP, Viewer runtime, routes, services, slicer state, printer state, or
continuity files.

## Independent deterministic checks

The focused suite ran through the root Python 3.12 `uv` environment:

```sh
uv run pytest \
  projects/laifen-wave-case/tests/test_container_generator_v1_preview_parameters.py \
  projects/laifen-wave-case/tests/test_container_generator_v1_parameters.py \
  projects/laifen-wave-case/tests/test_container_generator_v1_requirements.py -q
```

Result: **PASS, 32 tests**. These cover registry order and coverage, source and
derived defaults, classification, the read-only notice, one-option rows,
deterministic committed-sidecar parity, self-contained ES-module form, no
features/animations/effects/transforms/styles, no-effect `update()`, exact
sidecar declaration, and STEP byte guards.

Independent SHA-256 checks retained the four accepted STEP bytes:

- body: `02bfc1ca52ef97dcba3451c930408f64d0f383293933f6183029e36409e1c05a`
- cap: `b9561b34b96667d1af6e84d145c03d9aa319694fbf11f2cc3c0b60d6b6f18cf0`
- closed: `cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2`
- print layout: `cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b`

The served module was fetched from the descriptor-gated `moduleUrl`. Its
SHA-256 was `c4f09c297d3876f1e9823c66f29f468c7f8e27820879c9ba69f82c0798094226`,
byte-identical to committed `closed.params.js`. A Node import of that served
file independently required all 41 ids, one enum option per row,
`geometryRegeneration == false`, no `features`/`animations`, and a no-effect
`update()` guarded by throwing context/effects proxies. It passed and reported
the corrected radial values above.

## Viewer package and endpoints

Viewer `3249` was already running and was not restarted or modified. The first
candidate correctly reported `needs-build` after `closed.step.py` changed; its
single POST build completed with `state: ready`. For this repaired candidate,
the entrypoint and render geometry were unchanged, so the focused GET returned
`state: ready` and no redundant rebuild was needed.

The regenerated descriptor at
`cad/container_generator_v1/__cadgen__/models/closed.step.py/assembly.json`
records:

- `sourceKind: python`, `sourcePath: closed.step.py`;
- `sourceHash: 578a5651c9fdc3f23376e44c9fb804fd0a64200f7fc9cb835dce7734b643756a`;
- `stepPath: closed.step` and the accepted closed STEP hash;
- `paramsPath: closed.params.js`, resolving exactly to
  `cad/container_generator_v1/closed.params.js`;
- two occurrences and two shapes.

Exact private review page:

```text
https://mac-mini.duckbill-ionian.ts.net:8449/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case?file=cad/container_generator_v1/closed.step.py
```

Result: **HTTP 200**.

Exact artifact status endpoint was queried with `dir` equal to the absolute
project path and `file=cad/container_generator_v1/closed.step.py`:

```text
https://mac-mini.duckbill-ionian.ts.net:8449/__cad/artifact
```

Result: **HTTP 200**, JSON `state == "ready"`.

## Mobile visual evidence

CUA used the managed Chrome delivery surface and its viewport capability at
`390 x 844`. It captured three states inline during this validation turn:

1. loaded two-part case plus the top of Parameters, including `00 READ ONLY`,
   the regeneration message, Axial, Device reference, Radial, Exterior, and
   Thread rows;
2. the scrolled bottom with both corrected radial gaps and the remaining
   Derived rows;
3. the opened body-radial-gap combo containing exactly one selected option,
   followed by selecting that option with no visible effect.

The page showed no visible error, slider, number input, free-text input,
checkbox parameter, animation control, or second selectable value. Native
Viewer module-enable and Reset controls remain visible chrome. Long closed-row
labels and values are ellipsized at 390 px, while the opened option exposes its
full value. This is a minor readability limit, not a truthfulness or effect
failure under the clarified gate.

The CUA interface returned screenshots inline rather than a local PNG path.
The bound observations are recorded in
`scratch/preview-parameters-validation/mobile-visual-observation-repaired.md`;
the viewport override was reset after inspection.

## Acceptance boundaries

- **Preview readout:** PASS for repaired candidate `d2b7afa6...`.
- **CAD/source and written STEP:** inherited PASS only; this iteration changed
  no CAD geometry or STEP bytes.
- **Editable customizer:** absent by design; edit source/OpenSCAD and regenerate
  plus revalidate STEP.
- **Slicer/process:** HOLD, unchanged.
- **Physical:** PARTIAL / UNBOUND, unchanged.

One bookkeeping extraction initially invoked unavailable bare `python` and
failed before reading or writing evidence. It was immediately rerun as
`uv run python` through the required root environment and passed. No validation
or candidate state depended on the failed invocation.
