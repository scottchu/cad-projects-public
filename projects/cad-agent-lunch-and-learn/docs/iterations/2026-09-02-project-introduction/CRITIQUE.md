# C5 independent novice-clarity and visual critique

Status: **P2 — focused repair required before formal review.**

## Verified candidate and inputs

- Candidate HTML SHA-256: `2fa49a591e721a53051888e98b2562aaa8cba4b06d4f23ecb0dac8570f86790c`, matching `CANDIDATE.sha256` (`c7eb0b08ead8fb5b4cefd8bf1fe347dce9dc22c53abeb9278efe6b38c111e4f1`).
- Frozen-input manifest SHA-256: `66b2da24389cde4b5281ec74643e9b3e2424894d4fbd614f6f63ba66a32a2b78`.
- Read: project `README.md`; this iteration's `BRIEF.md`, `DESIGN.md`, and `IMPLEMENTATION.md`.
- Pixel evidence supplied by V5 and inspected directly: `/tmp/cad-agent-intro-validation/{1280x800,855x882,390x844,print}-slide-{3,4,5,10}.png`, plus `390x844-slide-4-bottom.png`.

## Finding

### P2 — slide 3’s narrow CAD image crop weakens the new explanation

At 855 × 882, `855x882-slide-3.png` uses a cover crop that cuts through the outer green and blue plates of A01. The adjacent text succeeds at explaining that XT60 is a connector and that the jig holds its two wires at 90 degrees while soldering and cooling, but the supporting “Early CAD concept for the wire holder” now looks like a partial, unexplained exploded object. This contradicts the iteration’s purpose for A01: it must support the new introduction rather than create visual uncertainty.

Repair the slide-3 image treatment at this breakpoint so the complete existing concept is visible (for example, contain within the allocated image frame) and then recapture slide 3 at wide, narrow, mobile, and print sizes. Preserve the existing A01 source and its early-CAD caption; this is a presentation layout repair, not CAD evidence or a physical-function claim.

### P2 — slide 10’s mobile diagram labels collide

In `390x844-slide-10.png`, the underlined `hour / minute / second pieces` label overlaps the smaller `light → shadow plane` label. That collision makes the relationship map harder to parse exactly where the audience has least room to infer it. Remove the redundant `light → shadow plane` label in this constrained layout (the purpose sentence already explains the moving-pieces/light/shadow relationship), or reposition the two labels so they remain separately legible. Recheck slide 10 at mobile after the focused repair.

## Requirement coverage that passed this critique

- Slide 3 precedes the retained rod/hole example and states, in newcomer language, what XT60 is and why the holder is intended: two insulated wires held at a fixed 90-degree bend during soldering and cooling. It labels A01 as an early CAD concept rather than a proven physical result.
- Slide 4 remains a legible rod/hole test story at wide, narrow, mobile (including the supplied lower scroll capture), and print views. Slide 5 remains legible as a count statement and retains its qualification that the counts are records, not prints or total attempts.
- Slide 10 gives Kage’s clock goal before the conceptual mechanism map. “Kinetic” is made meaningful by the adjacent statement that moving pieces cast shadows to show hours, minutes, and seconds; the H/M/S diagram is accompanied by the corresponding hour/minute/second label. The conceptual-layout caption remains visible. Its mobile label collision remains the focused P2 above.
- No undefined `pigtail` terminology appears in the reviewed introduction slides, and no claim says either project physically works.

## Evidence and limits

Commands run from the repository root: `shasum -a 256 projects/cad-agent-lunch-and-learn/index.html`; `shasum -a 256 projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-02-project-introduction/*`; direct image inspection with the supplied V5 captures. This is an independent visual/novice-clarity critique only. It does not re-run the browser/PDF capture, source-preservation comparison, executable-script comparison, CAD validation, artifact/slicer validation, or physical validation; V5 owns the applicable validation evidence.

Next action: I5 performs the two focused responsive corrections; V5 recaptures and verifies the repaired candidate, then C5 performs focused slide-3 and slide-10 rechecks (within the iteration repair ceiling).
