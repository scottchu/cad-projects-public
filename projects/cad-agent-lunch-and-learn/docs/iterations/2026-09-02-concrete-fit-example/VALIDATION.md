# TV independent validation

Status: PASS for the revised slide 3. Owner: `/root/slide3_validation`, distinct from writer and critic. No blocking finding. Read AGENTS, project state/next action, requirements, experience, decision index, BRIEF, DESIGN, IMPLEMENTATION, manifests and S01 source observation. Work was bounded to preservation, the changed slide, existing checks and print; no new geometry, simulation or physical acceptance.

## Verified identity and preservation

- HTML: `ebb4113fb57951ba62cfa2760fdec40d918991b265b8c688a07d713c61797ee4`.
- CANDIDATE: `4f79f9740e85eb0e11b16cdd2ff219324a69756b5d444add18b870fa81dedda1`, 8/8 entries verified before and after browser capture.
- FROZEN_INPUTS: `af0b1d453916bf6f65b2c6609024cfe719f7e78a22979131f7f4d84e954ced9a`, 10/10 entries verified before and after.
- Both complete inline script bodies match PRESERVATION_BASELINE. Its section regex stops early at slide 6's nested section; therefore its 21 matching section hashes alone were insufficient evidence of complete preservation.
- Independently recovered the complete accepted baseline from `/tmp/cad-opening-served.html` and verified its SHA-256 as `c991fae1a02be21e60a6f84e6d7284c6a5b58affdb456a81a362f7333299d904`. Compared intervals from each outer `<section class="slide ` start to the next outer slide, with the final interval ending at `</main>`. All 21 other complete sections, including nested content and presenter notes, are byte-identical; only slide 3 differs. Evidence: `/tmp/cad-agent-slide3-validation/full-preservation.json`.

## Commands and evidence

Run from repository root, shell `/bin/sh`, login disabled; no Python or dependency installation:

```sh
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-slide3-validation/validate.mjs
/usr/bin/swift /tmp/cad-agent-slide3-validation/pdf-inspect.swift /tmp/cad-agent-slide3-validation
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node --test projects/cad-agent-lunch-and-learn/test/deck.test.mjs
```

The isolated Chrome CDP harness uses the frozen local HTML. Existing five checks PASS. Browser report records matching candidate/input manifests before and after. PDFKit reopened the actual Chrome-written PDF and confirmed 22 pages, each 960 × 540 pt; page 3 was rendered from that PDF and visually inspected. PDF SHA-256: `8e04565f695cda3f16e5fdddbc87b7ad85705fea0c8cee041f0d1ae729a2f882`.

Inspected actual pixels in `/tmp/cad-agent-slide3-validation/`:

- `1280x800-slide-3.png` and `1920x1080-slide-3.png`: complete title, labels, insertion arrow, Hole callout, Design/Print/Try explanation and lesson. No text/diagram overlap or clipping.
- `390x844-slide-3.png` and `390x844-slide-3-bottom.png`: diagram and labels fit the 390 px width; normal vertical scrolling across a 959 px document exposes the complete lesson and S01 link. No horizontal document overflow. The existing fixed toolbar truncates the Fullscreen label and covers the slide number at this width; inherited interface limitation, outside this slide-only revision, nonblocking for reading the example.
- `print-3.png`: complete, legible single slide page; schematic and lesson preserved without browser controls. `deck-print.pdf`, `print-text.txt` and `report.json` retain supporting temporary evidence.

## Requirement coverage and limits

REQ-016 PASS: the audience can identify the metal rod, printed test piece, hole and insertion action before reading the general lesson. The 4.05 mm label explicitly says Hole in CAD; the 4.00 mm rod and very-tight trial requiring the rod to be pushed back out agree with S01. The schematic is visibly labeled not to scale. No measured printed-hole diameter, shrinkage cause, force, friction simulation or successful final assembly is asserted.

REQ-005/006/007 evidence boundaries and REQ-009/010 changed-slide rendering PASS. Other slide and simulator acceptance carries forward through exact preservation; this narrow run does not re-establish physical/CAD acceptance. Only this VALIDATION.md and temporary validation files were written. An initial harness mismatch was resolved by matching the declared section-hash format, followed by the stronger complete-baseline comparison above; no candidate repair occurred. Next: distinct critique and formal review join against these same fingerprints, then root continuity and user review.
