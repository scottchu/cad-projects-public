# RCV-03 independent render-controls critique

- Owner / role: `RCV-03`, independent critic
- Date: 2026-09-04
- Verdict: **BLOCK pending delivery-surface validation**
- Highest severity: `P2` acceptance gate
- Frozen design fingerprint: `2ac420ce1eb43f6adb12d39d41416a24167a7ef7a3990a490107f8caed5a80e4`
- Candidate manifest fingerprint: `8e6ac223dd9e8ff5539120bfb0d8ffcc20dd7d38f801bb0e08a945a5520c3a60`

## Provenance and deterministic checks

The candidate manifest was verified before inspection. Every listed candidate
file passed its recorded SHA-256, including the four unchanged STEP artifacts.

```text
/usr/bin/shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-04-render-controls/candidate-files.sha256
  preview_parameters.py: OK
  closed.params.js: OK
  focused preview test: OK
  closed.step.py: OK
  body.step, cap.step, closed.step, print_layout.step: OK

uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_preview_parameters.py -q
  7 passed

uv run python .../scripts/inspect refs .../closed.step '#o1.1' '#o1.2' --facts
  both selectors resolved; body label and cap label exactly match the two
  authored names in the frozen design; body bounds 39 x 38.996548 x 144 mm;
  cap bounds 39 x 38.996548 x 84 mm; assembly bounds 39 x 38.996548 x 219 mm

node --input-type=module --eval <sidecar smoke test>
  52 manifest parameters; default update made zero effect calls; one-turn
  case emitted cap rotation 360 degrees and +5 mm total cap translation for
  3 mm extra lift; changed color/opacity targeted only the requested parts
```

## Static critique result

The candidate passes the source and sidecar checks covered by this role:

- The ten controls are inserted before the prior 41 structured readouts, and
  the generated manifest preserves the readout tuple and order.
- The disclosure is first, and every interactive control carries
  `renderOnly: true`, `geometryRegeneration: false`, and the required
  render-only boundary description.
- `solveVisualPreview()` is the one exported math boundary. It clamps the
  declared ranges, defaults non-finite numeric values, derives the body/cap
  axial factors, and derives cap travel as `2 * turns + extraLift`.
- The effect specs use only Viewer 0.4.28 `effects.transform()` and
  `effects.style()`. The transform array is `[scale, rotate, translate]`, with
  the scale and rotation pivot at the shared shoulder `(0,0,0)` and translation
  only along world `+Z`.
- Stable authored occurrence names resolve to exactly one body and one cap in
  the accepted closed STEP witness. The positional `#o1.1` / `#o1.2` ids are
  retained only as inspection witnesses; the sidecar targets feature ids whose
  `names` arrays hold the authored labels.
- Default parameters make no effect calls. No `clear`, `visible`, `highlight`,
  `render`, Three.js, mesh, material, or geometry API is present in the
  generated module.
- The four accepted STEP hashes remain byte-identical, and `closed.step.py`
  remains the sidecar declaration boundary.

The Viewer implementation confirms that `manifest.features` is normalized by
authored `names`, that exact name matches become `partIds`, and that the
effect implementation premultiplies the ordered transform steps. This agrees
with the candidate's target and transform contracts.

## Remaining gate

### P2 — exact delivery surface is not independently evidenced here

This read-only critique did not fetch the current descriptor/module endpoint or
capture the exact private Tailscale page at 390 x 844. RCV-04 must verify the
same candidate fingerprint on the live route, require `state == "ready"`,
confirm one body and one cap target in the generated descriptor, exercise
default / changed / reset states, and check that the ten controls are usable
while the 41 readout rows remain discoverable. Until that receipt exists, the
overall render-preview candidate stays blocked even though the static source
and geometry-preservation checks pass.

This is a delivery-presentation gate only. It does not reopen CAD, STEP,
slicer, printer, or physical acceptance, and no source or artifact was changed
by this critique other than the two critique records in this iteration.

