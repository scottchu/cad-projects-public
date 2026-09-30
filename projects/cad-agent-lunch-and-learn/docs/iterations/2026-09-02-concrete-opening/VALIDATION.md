# OV independent opening validation

Owner: `/root/opening_validation`, distinct from opening writer and critic. Final status: **PASS** after one focused separator repair; no open P1/P2 opening findings. This record covers the opening revision only; prior simulator and source-project acceptance limits remain unchanged.

## Initial candidate

HTML SHA-256 `27c1ed626c5b0a2276fb3f81e80c08be72c485010e867bdc9f29687ee91bb735`; candidate manifest `c93b54284e254ae25822bf4ba374cc181a27d448b1ce377306d184e4fef7e267` verified 8/8 before and after the browser run. Frozen inputs `1625ba8fd661e5945f85dfe9aa641dd9d0758031c391424e922e1295e5fd4d50` verified 11/11 before and after. Final shell hash check matched before releasing the writer gate.

Independent SHA-256 extraction against `PRESERVATION_BASELINE.json` confirmed sections 3–22 (20/20) and both inline scripts byte-identical. The first extraction attempt used an unsuitable regex for nested sections and stopped at slide 6; correcting only the inspection script to terminate at each speaker-note template made the complete comparison pass. No candidate change was involved.

## Commands and evidence

From repository root, `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-opening-validation/validate.mjs` passed manifest/preservation checks and captured actual browser pages. `/usr/bin/swift /tmp/cad-agent-opening-validation/pdf-inspect.swift /tmp/cad-agent-opening-validation` opened the written PDF with PDFKit, confirmed 22 pages at 960 × 540 points, extracted text, and rendered pages 1/2. `shasum -a 256 projects/cad-agent-lunch-and-learn/index.html projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-02-concrete-opening/CANDIDATE.sha256` matched the above candidate after inspection.

Ephemeral evidence directory: `/tmp/cad-agent-opening-validation/`. It contains `report.json`, `validate.mjs`, `{1280x800,1920x1080,390x844}-slide-{1,2}.png`, mobile `-bottom.png` captures, `deck-print.pdf`, `print-{1,2}.png`, `print-text.txt`, and `pdf-inspect.swift`. Browser skill was read; required Node REPL/browser tool was absent from available-tool discovery, so the existing isolated fresh-Chrome CDP helper was used. Initial process creation hit EMFILE; `/bin/sh`, no login, with PTY recovered execution. No Python environment was used.

## Results and requirement coverage

- **REQ-015, desktop opening:** PASS at 1280 × 800 and 1920 × 1080. Clear 3D printing/CAD/AI-agents title and concrete first-person WHY/HOW/WHAT sequence. No text clipping, overlap or horizontal overflow.
- **REQ-009/010, mobile opening:** slide 1 PASS at 390 × 844 with normal vertical scrolling. Slide 2 has **P2-OV-01**: mobile CSS hides authored `<br>` without separating adjacent text, visibly producing `shadow.A jig` and `learnfrom`. Fix the authored separators, regenerate and freeze; focused mobile reinspection required.
- **REQ-009, controls/metadata:** ArrowRight moves slide 1 to slide 2; Notes opens the corresponding presenter notes; overview contains both new titles; document title is `3D Printing with CAD & AI Agents`. Notes identify the user-authorized creative framing, exact project purposes and the transition into slide 3. Existing notes/overview title concatenation at authored line breaks is cosmetic and does not obscure either title.
- **REQ-001/009, actual print:** PASS: written PDF has 22 complete pages. Pages 1 and 2 are visually readable, retain all opening copy/citations, and have no clipped or overlapping text.
- **REQ-003/005/006/007, preservation:** slides 3–22 and scripts are unchanged; new project-purpose sources and requirements are frozen. No new dated event, measurement, success claim or physical acceptance appears in the opening. This gate does not repeat unchanged simulator/geometry tests.

Only P2-OV-01 blocks this candidate. No other P1/P2 opening finding. Root-owned final continuity/HANDOFF was pending when this validation began. Next: focused writer separator repair, same-role OV revalidation, then distinct formal review on the repaired candidate.

## Focused repair — final PASS

Repaired HTML SHA-256 `c991fae1a02be21e60a6f84e6d7284c6a5b58affdb456a81a362f7333299d904`; candidate manifest `23c7635486cb1842054ff8d04833653664d4ecd38c37e8c6097a291ee54f0ab2` verified 8/8 before and after. Frozen inputs remain `1625ba8fd661e5945f85dfe9aa641dd9d0758031c391424e922e1295e5fd4d50`, independently verified 11/11 before and after. Preserved sections 3–22 and both scripts again passed 20/20 and 2/2.

Command: `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-opening-validation/repair.mjs`. Evidence: `repair-report.json` and `repaired-390x844-slide-2.png` in the same temporary directory, shared with the independent critic. The actual mobile rendering now has `shadow. A jig`, `print → try it`, and `learn from`; positive whitespace assertions and negative joined-word assertions pass. Visual inspection confirms readable, properly separated text, no new wrapping issue, and document width 390 px. Page height remains 851 px. Slide 1 notes additionally confirm creative-origin framing and explicitly avoid claiming finished physical success.

**P2-OV-01 resolved.** The repair only adds spaces after four slide-2 line breaks (title plus three body rows), with the title space also appearing in the generated overview. An independent Node reconstruction removed exactly those four spaces plus the generated overview space and recovered the original HTML hash `27c1ed626c5b0a2276fb3f81e80c08be72c485010e867bdc9f29687ee91bb735`, proving the complete bounded delta. Earlier desktop, navigation and actual 22-page PDF checks are carried forward for this bounded whitespace correction; the PDF and its page renders identify the initial candidate, not a newly generated repaired PDF. The screenshot of the affected mobile layout is fresh for the final candidate. No simulator/geometry or unrelated checks repeated. Final requirement coverage: REQ-015 and affected REQ-001/003/005/006/007/009/010 gates pass within this opening-only scope. Next: distinct formal review joins OV and OC on the repaired candidate; root completes continuity and delivery.
