# V4 independent validation

Status: PASS after repair 1. Owner: `/root/slide4_validation`.

## Accepted repair 1

HTML SHA-256 `021a0510235ac59b6e66c687f0041a2294925a16fd12814a70748130ac7e1280`; candidate manifest SHA-256 `42516d298d5aba333a83edc262e7d33216a6d9c175526f37216f8f9d68e9dbd6` (8/8 entries verified). Frozen-input manifest remains `2d61d3f9a52579ce10eb601ef3c04c64210e566b3954bbd5b1a19551a8d7a1fc` (7/7 entries verified). All values were independently checked before and after the focused rerun.

REQ-017 PASS: pixel inspection at 1280x800, 855x882, 390x844, and actual PDF page 4 shows each number adjacent to its readable explanation, with the numeral 5 now clear of the label. The caveat and dated snapshot are grouped beneath the counts. No horizontal or vertical document overflow occurred at any of the three viewports. The fresh PDF has 22 pages at 960x540 points. Complete outer-section preservation again finds 22 slides, only slide 4 changed; both inline script hashes below still match the preserved baseline. The visible numbers, descriptions, caveat, date, and source are unchanged.

The same Node and Swift commands below were rerun successfully (exit 0); only the expected candidate fingerprints in the temporary helper changed. No tests or navigation/simulator gates were added or repeated. C4 reports repair-1 rebuild at 22 slides and existing checks at 5/5. All four fresh images were inspected using `view_image`.

Current evidence remains at `/tmp/cad-agent-slide4-validation/`: `report.json`, three viewport PNGs, `deck-print.pdf`, `print-4.png`, and `print-text.txt`. The initial failed candidate images, PDF, and report are retained under its `initial/` subdirectory. Only this validation receipt and the allowed temporary evidence directory were written. No unresolved slide-4 layout finding remains; formal independent review is the next gate. Browser/PDF rendering does not imply physical or CAD acceptance.

## Initial candidate failure history (superseded by repair 1)

Verified before and after browser capture:

- HTML SHA-256: `23420e32b2c6768cded7dd796f4a6aa239fe014df5389b7ebd6d7335b366302c`.
- `CANDIDATE.sha256`: `3a2c288f5960954554cf781cd2e1ab751a2c8e8b951b92c5b125837f243f257c`; all 8 entries matched.
- `FROZEN_INPUTS.sha256`: `2d61d3f9a52579ce10eb601ef3c04c64210e566b3954bbd5b1a19551a8d7a1fc`; all 7 entries matched.
- Preserved baseline HTML: `ebb4113fb57951ba62cfa2760fdec40d918991b265b8c688a07d713c61797ee4`, independently hashed at `/tmp/cad-slide4-before/index.html`.

## Findings and coverage

- **P1 / REQ-017: FAIL.** At 1280x800, 855x882, and rendered PDF page 4, the descending bottom of Georgia's numeral `5` visibly overlaps the first label line, `formal XT60 iteration`. Browser element rectangles have approximately 7.19 px separation, but painted glyphs extend beyond the short numeral line box. Increase the numeral line box or label clearance in the existing slide-4-only rules, then recapture these affected views.
- **PASS:** mobile 390x844 places each numeral beside its complete readable description; the two pairs are separated.
- **PASS:** document scroll width equals viewport width at all three sizes (1280, 855, 390). Document heights also equal the viewports (800, 882, 844).
- **PASS:** nesting-aware comparison of all 22 complete outer slide sections, including nested slide 6, found only slide 4 changed. Both executable inline scripts are byte-identical, with hashes `46bbeeaff09ac40519039278258b883dc7bedd67fbc5288f430e69f97c719335` and `83807e30a7253078715001614dda38e7ef74600b70660eee37e3cff28571fd99`.
- **PASS:** direct slide-4 source comparison preserves the exact two numbers and labels, count caveat, repository snapshot date, S08 source/footer, and full template speaker note. Only structural count-card wrappers were added to the heading. The empty browser `template.textContent` field in the JSON report is not a speaker-note omission; the source template is intact.
- **PASS:** generated PDF contains exactly 22 pages, each 960x540 points. Page 4 was rendered and visually inspected; its count-label overlap prevents print acceptance.
- Existing build and 5/5 check results are carried from C4's implementation receipt. Navigation, simulator, and offline gates were not rerun because their source/scripts are unchanged.

## Commands and evidence

- `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-slide4-validation/validate.mjs` — exit 0, preservation/fingerprints/browser captures/PDF generation completed.
- `swift /tmp/cad-agent-slide4-validation/pdf-inspect.swift /tmp/cad-agent-slide4-validation` — exit 0, 22 pages; page 4 PNG generated.
- `view_image` — inspected all three viewport captures and rendered page 4.

Initial evidence, now retained under `/tmp/cad-agent-slide4-validation/initial/`, contains `report.json`, `1280x800-slide-4.png`, `855x882-slide-4.png`, `390x844-slide-4.png`, `deck-print.pdf`, `print-4.png`, and `print-text.txt`, with the exact temporary scripts for repeatability.

Initial execution attempts failed with file-descriptor exhaustion before any process started. Root recovered execution with `/bin/zsh`, `login=false`, `tty=false`; no system settings or unrelated processes were changed. The temporary preservation helper needed one correction to exclude non-slide outer sections. An inadvertently attempted PDF inspection before PDF generation failed as unreadable; the subsequent actual generated PDF inspection passed. These were tooling failures, not candidate source repairs.

Initial next action was the minimal glyph-clearance repair; repair 1 above completed that action and its focused revalidation. No CAD, artifact fabrication, or physical acceptance is asserted.
