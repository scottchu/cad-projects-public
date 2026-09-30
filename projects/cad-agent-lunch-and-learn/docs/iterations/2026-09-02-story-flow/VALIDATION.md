# S-V show-and-tell validation

Status: **FAIL — two focused visual repairs required**. Owner `/root/intro_validation`, distinct from writer and independent story reader. HTML `1cd670ac33121db7b091070d43e68b58e5e97ef512f8e2e1162999b48ce31fce`; candidate manifest `6f7a6eebfeda0596d894276edfd92e57436525587f269f1b6f0a0b8c353f6c81` (12/12 entries); frozen inputs `1946896b8ddbcf33155de16cc6761a3b630f7359a28d336744016a8cc9527dda` (20/20). All path/content entries verified before and after complete capture, including no-WebGL fallback captures. No candidate mutations by S-V.

## Findings requiring repair

- P2: slide 5's real 3D contact view hides the orange contact land underneath the opaque green plate. At desktop and mobile sizes the orange arrow is visible, but the actual contact feature named by the caption is not. The fallback/print drawing shows the land clearly; the new 3D view must also make that relationship visible. Evidence: `/tmp/cad-story-validation/1280x800-slide-5.png` and `390x844-slide-5-bottom.png`. Adjust only teaching view/framing/visibility while retaining explicit schematic status and the recorded source-response boundary.
- P2: slide 7's mobile intent sketch scales the whole horizontal SVG, producing roughly 7–9 px labels. Its critical fixed-inner/moving-outer and 90-degree relationship labels are unreadable at 390×844. Evidence: `390x844-slide-7.png`. Use a readable mobile arrangement or labels.

## Completed coverage

All 18 slides captured at 1280×800 and 390×844, plus compact slides 3–6 at 1178×820: 40 primary captures and bottom-scroll continuations. Every slide's desktop/mobile pixels were inspected, individually or in six-slide contact sheets; the new scenes, fallback layouts and reported failure areas were inspected at full size. No horizontal document overflow. Mobile long slides use vertical scrolling; the fit outcomes remain visible without reveal or audience actions.

A newly generated actual PDF has exactly 18 pages, each 960×540 pt. All 18 pages were rendered and inspected. Fit and paired bed views have labelled static print explanations; table and completion results are visible. No extra/missing pages or print clipping was found. The new mobile sketch defect does not affect its desktop/PDF version.

Offline browser checks (network disabled) confirm a real WebGL canvas in each of three ready scene hosts: fit, bed-gap and bed-contact. Scene frames contain their overall objects; contact-land visibility remains the specific failure above. Forced WebGL-unavailable runs display labelled static diagrams for slides 4 and 5 at compact/mobile widths, with complete captions through scrolling and no retained blank canvas gap. These fallbacks tell the same nominal-versus-observed fit and gap/contact stories. Source inspection confirms demand rendering on activation/resize, no OrbitControls, scene pointer controls, animation loop or audience state controls; the only renderer listener handles lost WebGL context.

Show-and-tell requirements pass: 18 slides, no form/input/select/textarea, no content buttons, no visible question marks in any slide content, and zero external runtime resources. All five fit results and the pilot completion distinction are immediately visible. Native keyboard navigation passed: initial slide 1, ArrowRight → 2, End → 18, Home → 1. Source/speaker-note/navigation controls are presentation facilities, not an audience exercise. Static source and rendered content show no remaining radio, slider, reveal/reset quiz or prompt to choose a result.

The visible sequence now names the forming rods and their printed guides before the single fit example; then print setup, bend assumptions, Kage relationships, evidence-driven next actions and the print-file workflow. This is a validation observation, not the independent story-reader acceptance. Reader received only pixel paths/count before its blind read.

## Evidence and execution

Evidence directory `/tmp/cad-story-validation/`: `report.json`, `navigation.json`, viewport-slide images, fallback images, bottom continuations, `deck-print.pdf`, `print-1.png` through `print-18.png`, `print-text.txt`, and contact sheets. The prepared harness was not run until exact READY hashes and count arrived.

Commands: `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-story-validation/capture.mjs`; same Node executable with `navigation.mjs`; `swift /tmp/cad-story-validation/pdf-inspect.swift /tmp/cad-story-validation 18`; `swift /tmp/cad-story-validation/contact.swift`. All completed, no harness assertions failed. Existing build and 5/5 test results are writer evidence, not a repeated S-V broad check.

Only this receipt and temporary evidence were written. No source, tests, dependencies, locks, Git, hosting, CAD, slicing, printer or source-project changes. This review establishes no physical acceptance. Next: writer repairs the contact view and mobile intent sketch, freezes a new candidate, then focused new pixels and exact unaffected-content parity can carry forward this all-18 evidence. Formal review follows independent story and validation PASS on the same candidate.

## S-V repair 1 — PASS

The earlier FAIL remains the history of the previous candidate. The repaired candidate passes this focused validation; no blocking finding remains. HTML `6ce17971db1871cc4bc2c8958359cc6a28e52e16b875f5dae4e838a876a41445`; CANDIDATE `214392b508b8fde520532452ac0ca66074ba5aecd65368f12662f6e88c7f1dca` (12/12 entries); FROZEN_INPUTS `8676ec882ed1b79c555e5bd7a4a3fc351ef333f5345816270777f7e22d70d799` (28/28). Exact manifest hashes and every member verified before and after capture and again at receipt completion.

Independent nesting-aware comparison with `/tmp/cad-story-repair1-baseline/index.html` (the prior HTML above) finds only sections 5, 7, 9, 10, 13 and 14 changed. The other 12 sections and navigation script are byte-identical. Existing style content is preserved apart from trailing whitespace; added rules scope the mobile intent sketch. Fit geometry and the test file are unchanged. Renderer diff changes only contact-plate transparency, shadow/depth handling and outline; its geometry is unchanged. Therefore earlier all-18 desktop/mobile/print coverage carries forward for unaffected content. Evidence: `parity.json` in the repair evidence directory.

Fresh pixels: all six changed slides at 1280×800 and 390×844, compact 5/7 at 1178×820, and scroll continuations. The actual 3D orange contact land is now visible through the outlined translucent plate on desktop/mobile. Slide 7 mobile labels are readable in stacked panels. Changed copy on 9/10/13/14 fits and retains the proposed-restart versus completed-work distinction and the two-PETG-part assembly context. No horizontal overflow or content clipping found. Forced no-WebGL slide 5 retains the visible contact relationship and complete text. A fresh actual PDF has 18 pages at 960×540 pt; affected pages 5/7/9/10/13/14 were rendered and visually inspected with no clipping.

Offline checks confirm three ready real WebGL canvases, zero forms/content buttons/audience questions/external runtime resources, and native navigation 1 → 2 → 18 → 1. Results remain visible without audience actions. Existing writer build and 5/5 checks were not broadly rerun.

Commands: Node `/tmp/cad-story-repair1/capture.mjs`; Node `/tmp/cad-story-repair1/navigation.mjs`; `swift /tmp/cad-story-repair1/pdf-inspect.swift /tmp/cad-story-repair1 18`; independent Node path/content and section/script comparisons. Node executable: `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node`. All completed successfully. Evidence directory `/tmp/cad-story-repair1/` contains report/navigation/parity/final-verification JSON, screenshots, `deck-print.pdf`, affected print PNGs and extracted print text. Pixel paths were shared with the distinct story reader before its verdict.

Only this receipt and temporary evidence were written. No source, tests, dependencies, locks, Git, hosting, CAD or printer mutations. This is presentation validation, not physical validation. The read gate is released; next is formal review of this exact candidate.
