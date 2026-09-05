# PPV-04 critique — independent preview parameter re-critique

- Owner and role: `PPV-04`, independent critic
- Date: 2026-09-04
- Verdict: `BLOCK`
- Highest severity: `P2` acceptance gap
- Frozen design fingerprint: `a63279a10cdf763d599f8730c82b81d63f5e73f117c59208b12abd184c474115`
- Repaired candidate fingerprint: `d2b7afa66d0464455722e6257365eb26702b2704c070498594696049185848be`
- Repaired evidence manifest fingerprint: `98e7ed345a01b74b9cf34f30edc859b25ee53a3a942297eb676636e3bf8ee813`

## Provenance and verification

The frozen design input and repaired candidate identity were verified before
inspection:

```text
/usr/bin/shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-preview-parameters/INPUTS.sha256
  a63279a10cdf763d599f8730c82b81d63f5e73f117c59208b12abd184c474115

/usr/bin/shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-preview-parameters/candidate-files.sha256
  d2b7afa66d0464455722e6257365eb26702b2704c070498594696049185848be

/usr/bin/shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-04-preview-parameters/candidate-files.sha256
  preview_parameters.py, closed.params.js, closed.step.py, and the focused test: all OK

uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_preview_parameters.py \
  projects/laifen-wave-case/tests/test_container_generator_v1_parameters.py \
  projects/laifen-wave-case/tests/test_container_generator_v1_requirements.py -ra
  32 passed in 0.15s

node --input-type=module --eval "import definition, { READOUT_SCHEMA } from './projects/laifen-wave-case/cad/container_generator_v1/closed.params.js'; const result = definition.update({params:{},effects:{fail(){throw new Error('effect')}}}); console.log(JSON.stringify({schema:READOUT_SCHEMA,count:Object.keys(definition.manifest.parameters).length,result}));"
  schema geometryRegeneration=false, parameter count=41, update result undefined

/usr/bin/shasum -a 256 projects/laifen-wave-case/cad/container_generator_v1/{body.step,cap.step,closed.step,print_layout.step}
  all four frozen STEP hashes matched
```

The frozen input check still reports 15 project entries present and 5 archived
`external/cad-viewer-0.4.28` entries absent from this checkout. I did not start
the Viewer, call its service, or edit any source, test, service, or artifact.

## Resolved prior finding

The previous P1 formatting finding is repaired. The generated rows now exactly
match the frozen design contract:

```text
derived__body_radial_gap = 0.5 mm radial, reference only - derived readout
derived__cap_radial_gap  = 1 mm radial, reference only - derived readout
```

The focused test now asserts both values at
`tests/test_container_generator_v1_preview_parameters.py:40-41`, and the
committed sidecar matches the deterministic serializer byte-for-byte.

## Remaining blocker

### P2 — required delivery-surface gate is still open

`IMPLEMENTATION.md` explicitly leaves `PPV-VIEWER` to independent validation.
There is no current descriptor inspection, exact artifact endpoint readiness
receipt, or mobile-width Parameters-tab capture for this repaired candidate.
The design requires a block if a one-option enum still looks like a live editor
in the native Viewer UI. Because this task is read-only and forbids live Viewer
work, that condition cannot be resolved here. PPV-03 must verify the exact
generated package, HTTP 200/`state == "ready"` endpoint, and mobile presentation
for this repaired fingerprint.

## Static passes and no-new-issue check

- The repaired candidate manifest matches the requested fingerprint, and all
  four candidate files match their recorded hashes.
- The four accepted STEP files remain byte-identical to the frozen baseline:
  body `02bfc1ca52ef97dcba3451c930408f64d0f383293933f6183029e36409e1c05a`,
  cap `b9561b34b96667d1af6e84d145c03d9aa319694fbf11f2cc3c0b60d6b6f18cf0`,
  closed `cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2`,
  and print layout `cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b`.
- `closed.step.py` still keeps the same
  `build_assembly(derive(preset()))` shape expression and alone declares
  `closed.params.js`.
- The sidecar remains self-contained and deterministic. Its manifest has
  schema version 1, 41 parameters (notice, 26 source rows, 14 derived rows),
  only one-option `enum` controls, and no imports, `effects`, `features`,
  `animations`, transforms, or styles. `update(_context)` returns `undefined`
  and performs no effect call.
- `manifest.step.path` remains the expected workspace-relative
  `cad/container_generator_v1/closed.step`; it is neither absolute nor a
  parent-directory path.
- No new source, provenance, stale-sidecar, path, or baseline-preservation
  issue was found after the repair. The optional `path` argument in
  `write_sidecar()` remains a low-risk API hardening note, while the default
  module invocation writes only the adjacent sidecar.

## Acceptance recommendation

The static critique is `PASS` for source/sidecar truthfulness after the repair,
but the overall preview-readout gate remains `BLOCK` until PPV-03 completes the
descriptor, endpoint, and mobile UI checks. CAD, written STEP, slicer/process,
and physical acceptance states remain separate; this critique does not alter
the accepted P1 R7 CAD authority.
