# Independent HTML validation

Owner: `deck_validation` (distinct from implementation and formal review). Scope: local HTML rendering, behavior and print layout only; no CAD, slicer or physical acceptance.

## Initial candidate — rejected

Manifest `CANDIDATE.sha256` SHA-256 `5e41ff18c3635fab8f8004cbbb96483566de54a2cc0cb1c83a7b10e31bec194e`; index SHA-256 `5318d1901384b08b435cf97cba21580f2399607d01d9a68aeb189f28b83007c9`. All 10 manifest entries verified before and after the initial check.

Commands run from repository root:

```sh
shasum -a 256 -c projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-01-first-deck/CANDIDATE.sha256
env PATH=/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin:$PATH npm run check --workspace projects/cad-agent-lunch-and-learn
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-lunch-and-learn-validation/health.mjs
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-lunch-and-learn-validation/layout.mjs
```

Static checks passed 2/2. Real browser loading failed: `SyntaxError: Unexpected token ')'` in inline script, caused by `current===0)}` at the end of `show()`. DOM contained 22 slides but zero active slides; `show` was undefined. This blocks delivery (P1, REQ-008/009/010).

Additional initial findings:

- P1: `.counts { display:grid }` overrides inactive-slide hiding; slide 4 leaks onto the initial page despite no active slide.
- P2: slide 5 desktop heading overlaps its feature labels; the main CAD image occupies only about 194 × 129 px at 1280 × 800 and is hard to inspect.
- P2: slide 10's conceptual/acceptance caption is below the 1280 × 800 viewport (y805–820), hiding the evidence qualifier.

Temporary diagnostic screenshots exist for all 22 slides at 1280 × 800, 1600 × 900 and 390 × 844 in `/tmp/cad-agent-lunch-and-learn-validation/diagnostic-slides/`. Because the script failed, these used browser-only per-slide display activation to inspect layout; they do **not** validate presentation behavior. No repository source was changed by validation.

The first functional harness stopped at the missing `current` variable. Navigation, source-reference behavior, exercises, offline network behavior and print acceptance remain pending a repaired frozen candidate. The implementation owner and independent reviewer received the findings.

## Environment

Installed Google Chrome, headless, fresh temporary user-data directory; Node 26.7.0 built-in WebSocket/CDP harness. No user browser profile, dependency installation, alternative Python environment, repository `node_modules`, or source-project mutation. Normal Browser plugin execution tools were unavailable after discovery, so the documented isolated-browser fallback was used. Temporary profile is removed when the harness closes.

## Repair 1 — behavior passes; layout/print repair required

Manifest SHA-256 `bcdbdacf4e1d7c86b0345f1edef5d107a22559dc48deaa2146c14c6b1cc54231`; all 10 entries verified before and after. A frozen temporary copy of `index.html` was retained for print diagnosis. No validation rebuild occurred.

Executed the same root npm check (3/3 pass, now including an inline-script parse regression) and:

```sh
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-lunch-and-learn-validation/validate.mjs
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-lunch-and-learn-validation/print.mjs
/usr/bin/swift /tmp/cad-agent-lunch-and-learn-validation/pdf-inspect.swift
```

Normal file-URL browser loading produced 22 slides, exactly one visible slide, 22 presenter notes and both loaded embedded images. Zero runtime JavaScript errors and zero HTTP(S) requests while network was forced offline. Previous/next pointer clicks, background arrows, Home/End, overview jump, notes, source drawer and fresh-page S01 footer citation worked. Arrow keys do not change slides while a navigation button or radio input has focus; input/drawer guards preserve interaction. Overview opens with focus retained on its trigger rather than moved into the overview; this is a keyboard usability limitation.

Fit controls produced the expected nominal diametral clearances 0.05/0.10/0.15/0.20/0.25 mm. Reveal showed the exact five qualitative observations, and reset cleared selection and hid results. Completion choices A/B/C and the operational-observation answer, evidence ladder and reset worked. The complete answer is not evidence of physical acceptance.

All 22 actual slides were captured at 1280 × 800, 1600 × 900 and 390 × 844; both revealed exercises and the notes/source/overview states were also captured. Main slide content was inside the viewport except the remaining slide 10 caption issue. Native screenshots were shared with the independent reviewer.

Remaining findings sent for the second bounded repair:

- **P2, REQ-007/010:** slide 10 caption remains against/below the 1280 × 800 viewport and source footer. The conceptual/acceptance qualifier must remain visible.
- **P2, REQ-008/010:** completion evidence-ladder text is approximately 8 px at 1280 × 800, too small for projection.
- **P2, REQ-009:** at 390 px wide, the single-row mobile control strip requires horizontal scrolling, clips Fullscreen initially and covers source IDs.
- **P1, REQ-008/009:** landscape print has 23 pages instead of 22; page 13 contains only an orphan S03 footer following slide 12. Slide 6's fit answer is clipped at the page bottom and its geometry qualifier is absent; slide 10 loses its guide/caption below the page.

Print evidence clarification: an initial CDP request used `landscape:true` with already-landscape paper dimensions, which rotated the PDF to portrait. A focused repeat corrected this to `landscape:false`, `paperWidth:13.333333`, `paperHeight:7.5`, margins zero and background printing enabled. macOS PDFKit independently confirmed the corrected 960 × 540-point landscape page size, 23 pages, page ordering and the clipping in rendered pages 6 and 10. The final print finding relies on this corrected result. No Poppler or Python dependency was installed.

Temporary evidence: `repair1-report.json`, `repair1-print.pdf`, `print-6.png`, `print-10.png`, and the slide/state screenshots under `/tmp/cad-agent-lunch-and-learn-validation/`. Browser-only and print-emulated geometry checks are diagnostic aids; the PDF was reopened and rendered before reporting its failures. Final acceptance awaits the second repaired frozen candidate.

## Repair 2 — browser gates pass; print pagination still fails

Candidate manifest SHA-256 `8b200517637b42569e8e51e232a51679847bc5e2e6a8476158f400db70b62783`, all 10 entries verified before and after. Repeated the exact normal-browser harness and root npm check: 3/3 static tests; 22 slides, one visible slide, 22 notes, 2/2 images loaded, zero JavaScript errors and zero HTTP requests offline. All 22 slides were recaptured at 1280 × 800, 1600 × 900 and 390 × 844, with zero detected main-content text outside slide bounds. Revealed fit/completion states and notes/sources/overview were recaptured. These screenshots replace the previous normal-candidate screenshot set and are associated with this manifest.

The focused `final-extra.mjs` check used real pointer clicks at mobile width. Fresh S01 then changed S02/S03 references opened their correct full embedded source records without first opening global Sources. Mobile source footers are now clear of the toolbar. Notes and overview work, and the completion answer fits above the controls; its evidence ladder computes to 18 px. Fullscreen remains at the horizontally scrollable end of the mobile toolbar; this is a minor discoverability limitation rather than a blocked primary workflow. Navigation/input focus guards retain the behavior documented above.

Corrected landscape PDF was reopened with PDFKit and pages 6, 10, 12 and 18 (slide 17) visually inspected. Fit answers and qualifier, Kage conceptual qualifier/light label, restart sequence and completion answer/ownership/ladder are present and unclipped. However the file still contains **23 pages**, with a blank page 13 between slides 12 and 13. This remains **P1 / REQ-009**, so overall delivery validation is not yet accepted.

The cause is a CSS selector collision: slide 12 has both `slide` and `sequence` classes, and its inner flow also has `sequence`. The print `.sequence { margin-top:2vh }` rule therefore adds margin to the already full-page section. Its text fits, but the section's outer extent creates an extra print page. This explains why DOM text-bound checks pass while the written PDF fails. The root was notified that the two repair cycles are exhausted; any further correction must use a bounded reopened scope, not an unbounded repair loop.

The independent reviewer separately reported a copied S08 hash typo; factual/source approval is owned by that review and is not overridden by successful source-drawer behavior.

| Requirement | Independent validation coverage at repair 2 |
| --- | --- |
| REQ-001 | English HTML, 22 slides, opens directly from file; speaking duration not rehearsed |
| REQ-002/003/004/006/011 | Narrative, factual history, architecture and role meaning assigned to independent review; no CAD or physical acceptance inferred |
| REQ-005 | Fresh and changing source links work offline; exact factual/hash agreement assigned to independent review |
| REQ-007 | Existing embedded assets load; conceptual caption is visible after repair |
| REQ-008 | Both exercises' values, reveal, reset, radio guards and printed answers pass |
| REQ-009 | Offline runtime, normal navigation, notes, overview, responsive source controls pass; print pagination fails |
| REQ-010 | Actual screenshots at three sizes, zero detected text-boundary overflows, independent visual review provided; projector hardware and live talk remain untested |

Temporary evidence: `repair2-report.json`, `repair2-print.pdf`, `final-extra.json`, `mobile-fit-revealed.png`, `mobile-completion-revealed.png`, the normal `slides/` set, and `print-{6,10,12,18}.png` in `/tmp/cad-agent-lunch-and-learn-validation/`. Temporary tooling uses isolated browser profiles and native PDFKit; no dependency installation or source rebuild. Only this validation record was written in the repository by the validator.

## D2 / I2 final validation — PASS with minor usability limits

**Final candidate:** `CANDIDATE.sha256` SHA-256 `b353bfadf7c274ab126e08d059611a8899c139710fa65ce7a3d254ab98ebdc8d`. Design-input manifest SHA-256 `f7f4e7305af420cd4356e0af476f1c8ff85ddd47c6e144abcee4783099f744b1`. All 10 candidate entries verified before and after independent checks. Root's prescribed build/check rerun preserved the exact candidate bytes; validation itself did not rebuild or edit implementation.

The D2 contract explicitly reopened only source-register embedding, print page/component separation and mobile Kage layout. Correction to the repair-2 wording above: its successful viewport bounds checks did **not** establish that every mobile label was visually separate. R1 found a mobile Kage label/caption overlap despite those passing measurements. I2's mobile diagram was therefore inspected visually as well as checked for clipping.

Final evidence:

- Root npm check passed **4/4**, including JavaScript parsing and all 11 S08 rows.
- Normal isolated-browser file loading: **22 slides, one visible slide, 22 notes, 2/2 images, zero runtime exceptions and zero HTTP(S) requests** with networking forced offline.
- Existing prescribed regression checks passed: pointer previous/next, background arrows/Home/End, guarded radio/drawer input, overview selection, notes, fresh and changing footer sources, fit arithmetic/observations/reveal/reset and completion answer/reveal/reset.
- All **66 actual slide screenshots** regenerated for this candidate at 1280 × 800, 1600 × 900 and 390 × 844. No main-content text-boundary overflow detected. Revealed exercise and drawer states were also regenerated. Screenshots were sent to R1 for independent visual review.
- Mobile Kage screenshot visually confirms a full content-width map, readable H/M/S and guide/light context, with the conceptual/not-accepted caption no longer colliding with the guide/light labels. There is still a minor visual touch between the motor label and the upper-right of the large S; this is recorded as P3 polish and was explicitly referred to R1 rather than concealed by the passing bounds check.
- Mobile footer references S01 → S02 → S03 each opened the correct full source before global Sources was used. The completion evidence ladder is 18 px and fits above the controls.
- Independently compared the **rendered S08 drawer** to the frozen `SOURCES.md`: for each of 11 named amendment files, the next rendered 64-character digest matches the corresponding register row. **11/11 paired matches**, including i3-7.
- Written landscape PDF reopened with native PDFKit: **22 pages in slide order 01–22, no blank/orphan page**. Pages **6, 10, 12 and 17** were rendered and visually inspected; fit observations/qualifier, Kage qualifier/light context, proposed restart sequence, completion answer/ownership/ladder are present and unclipped. The print-emulated text-bound check also reports no overflow, but actual PDF inspection is the acceptance evidence.

Exact browser and print commands remain those listed above: `validate.mjs`, `final-extra.mjs`, and `pdf-inspect.swift` under `/tmp/cad-agent-lunch-and-learn-validation/`, using Node 26.7.0, isolated installed Chrome and native Swift/PDFKit. Correct landscape parameters: 13.333333 × 7.5 inches, `landscape:false`, zero margins, print backgrounds, CSS page size preferred. Source-row comparison separately parsed the frozen Markdown table and compared it to the browser-extracted S08 article; it did not import the builder's parsing logic.

Final requirement disposition: REQ-001 format and REQ-005 runtime references pass; REQ-007 asset/caption delivery passes; REQ-008 interaction and printed-answer gates pass; REQ-009 offline/browser/responsive/print gates pass; REQ-010 screenshot/independence evidence is supplied, with the final visual verdict owned by R1. Narrative/factual/architecture coverage under REQ-002/003/004/006/011 remains the independent review's responsibility. The final printed pagination failure and source-digest typo are resolved; no P1/P2 validation finding remains.

Minor limits: arrows intentionally do not advance while a button has focus; overview retains focus on its trigger; Fullscreen sits at the scrollable end of the mobile toolbar; the motor/S touch remains visual polish. Fullscreen permission behavior, a physical projector, assistive-technology testing, actual speaking duration and live audience delivery were not tested. No CAD, slicer, printer or physical mechanism acceptance is implied.

Final temporary evidence: `i2-report.json`, `i2-print.pdf`, `final-extra.json`, `slides/{laptop,projector,mobile}-01.png` through `-22.png`, revealed exercise/drawer screenshots, and `print-{6,10,12,17}.png`. Earlier rejection evidence remains in this record and the `repair1-*` / `repair2-*` files. The validator's only repository mutation is this validation record.
