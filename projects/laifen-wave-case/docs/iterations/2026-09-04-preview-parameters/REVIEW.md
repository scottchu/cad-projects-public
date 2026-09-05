# PPV-05 formal independent review join

**Status: PASS for the exact repaired preview-readout candidate.** This verdict
applies only to the read-only parameter snapshot presented by the existing
private CAD Viewer route. It does not create editable CAD regeneration or
change the inherited CAD, STEP, slicer, or physical acceptance states.

## Frozen provenance

- Design fingerprint: `a63279a10cdf763d599f8730c82b81d63f5e73f117c59208b12abd184c474115`.
- Repaired candidate fingerprint: `d2b7afa66d0464455722e6257365eb26702b2704c070498594696049185848be`.
- Implementation evidence fingerprint: `98e7ed345a01b74b9cf34f30edc859b25ee53a3a942297eb676636e3bf8ee813`.
- Critique evidence manifest fingerprint: `e06b4f9c915802e3ca24c749111f9b4ed5a3f837067d0d56225f6111de0db51b`.
- Validation evidence manifest fingerprint: `28baf1b742d57c8e6836efc3202a9a65975ffd5fc91f70f7510d8c222be93469`.
- Formal review join: `inputs/review-join.sha256`, 29 entries, SHA-256
  `382ca75e149570076a0cdfc150dfb526bc05d0773a396a74d5cf1108a99680aa`;
  every entry passed immediately before this receipt was written.

`INPUTS.sha256` itself matches the declared design fingerprint. Its direct
content check reports the five labeled external CAD Viewer inputs absent from
this checkout and the intentionally replaced baseline `closed.step.py`; all
other frozen project inputs match. Current candidate identity is governed by
the repaired candidate manifest, which verifies all four entries.

## Critique and validation join

The independent critic found the repaired source and sidecar truthful and found
no remaining source, provenance, stale-sidecar, path, or STEP-preservation
defect. Its overall `BLOCK` was limited to the then-missing descriptor,
endpoint, and mobile presentation gate. Independent validation subsequently
completed those checks against the same repaired candidate and returned PASS.
The critic's P2 acceptance gap is therefore closed without changing the
candidate.

The earlier radial-gap formatting defect is closed. Candidate, served-module,
focused-test, critique, and validation evidence agree on the exact values:

- `0.5 mm radial, reference only - derived readout`
- `1 mm radial, reference only - derived readout`

## Truthfulness and delivery evidence

The joined evidence and a formal Node spot check establish 41 rows: one
prominent `00 READ ONLY` notice, all 26 registry values, and 14 derived
readouts. Every row is a one-option enum. The schema declares
`geometryRegeneration: false`; `update()` returns `undefined` without reading
context or invoking effects; the manifest has no features or animations.
Only `closed.step.py` declares `closed.params.js`, and the generated descriptor
resolves that exact sidecar with two occurrences and two shapes.

Validation inspected the exact private delivery page at a `390 x 844` Chrome
viewport. It recorded the unchanged closed two-part case, no visible error,
the notice and representative rows from every group, both repaired radial
labels, and one selected option only when the body radial-gap row was opened.
Selecting that option changed neither the model nor presentation. Viewer-owned
module-enable and Reset controls remain visible but have no candidate-defined
effect. Long closed rows are ellipsized at this width; opening a row exposes
its full sole value. This is an accepted mobile readability limit, not an
editable-CAD claim.

The reviewer rechecked the live route read-only after joining the records. The
exact review page returned HTTP 200, and the exact `/__cad/artifact` query
returned HTTP 200 with `state == "ready"`.

## Baseline preservation and disposition

The four accepted STEP artifacts remain byte-identical:

- body: `02bfc1ca52ef97dcba3451c930408f64d0f383293933f6183029e36409e1c05a`
- cap: `b9561b34b96667d1af6e84d145c03d9aa319694fbf11f2cc3c0b60d6b6f18cf0`
- closed: `cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2`
- print layout: `cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b`

All preview requirements `PPV-BASELINE`, `PPV-SOURCE`, `PPV-COVERAGE`,
`PPV-GROUPS`, `PPV-READONLY`, `PPV-NOEFFECT`, `PPV-ENTRY`, `PPV-VIEWER`, and
`PPV-BOUNDARY` pass for this fingerprint. No critical, major, or minor
candidate finding remains.

Acceptance remains separated as required:

- Preview readout: **PASS** for candidate `d2b7afa6...`.
- CAD/source and written STEP: inherited **PASS**; unchanged by this iteration.
- Editable customizer: absent; edit Python/OpenSCAD and regenerate and
  revalidate STEP.
- Slicer/process: **HOLD**.
- Physical: **PARTIAL / UNBOUND**.

## Formal checks performed

- SHA-256 fingerprint and `shasum -a 256 -c` verification of candidate,
  implementation, critique, validation, validation-input, and review-join
  manifests.
- Direct Node import enforcing 41 one-option enum rows,
  `geometryRegeneration == false`, no features/animations, and an effect-free
  `undefined` `update()` result.
- Direct SHA-256 verification of all four accepted STEP files.
- Read-only HTTPS GETs for the exact private review page and artifact endpoint.

The root orchestrator may promote this exact preview-readout candidate while
retaining the acceptance limits above. This review changed no candidate source,
test, CAD artifact, Viewer runtime, route, service, slicer, printer, or
continuity file.
