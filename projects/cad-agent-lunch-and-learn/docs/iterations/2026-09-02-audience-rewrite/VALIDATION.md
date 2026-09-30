# Q22V independent final-candidate validation

Status: **FAIL — focused visual repairs required**. Owner `/root/intro_validation`, distinct from implementation and critique. This receipt covers HTML `35fcd69804a85a4df829779bc1ab320f46c2e896ce41681168907bf8faf5280b`; CANDIDATE.sha256 `03bbe512fce537f3d432ad583ef63dcfe9790a6dc7dc018672567043881c6e90` (14/14 entries); FROZEN_INPUTS.sha256 `504a544c1d982a0efd3fc0436cc9ae0089181a9d25c72a03789ab1ca59e443d1` (16/16 entries). All entries were verified before and after all-slide capture; HTML was also verified before and after focused interaction checks. Source read gate was released to root after evidence collection.

## Blocking findings

- P2: slides 7, 8 and 11 scale their complete SVG diagrams to mobile width, reducing labels to roughly 6–8 px. The main copy is readable, but the diagrams' object/state labels are not. Evidence: `390x844-slide-7.png`, `390x844-slide-8.png`, `390x844-slide-11.png`. Use readable responsive diagram arrangements.
- P2: slide 8's dashed diagonal reference crosses its `Diagonal end reference` label at desktop/compact/print sizes. Evidence: `1280x800-slide-8.png`, `1178x820-slide-8.png`, `print-8.png`. Separate the line and text.
- P2: no-WebGL fallback leaves the empty canvas area above the section diagram. At 1178×820, it pushes the explanatory caption and lesson beneath the viewport/navigation. `fit-no-webgl.png` shows the blank rectangle and clipped lower copy. Collapse the unused canvas space when displaying fallback. Functional fallback checks pass; that is not a visual-layout pass.

## Passed evidence

All 22 slides individually captured at 1280×800 and 390×844, plus slides 6–8 at 1178×820: 47 primary screenshots, with scrolling continuations where needed. No horizontal document overflow. All desktop/mobile screens were visually inspected individually or through six-slide contact sheets; focused 1–8 and exercise renders were inspected at full size. Mobile 6's complete model and lesson are visible in its bottom-scroll capture. Desktop/compact default model is fully framed with explicit rod/test-piece labels. The desktop story and visible conclusions now explain objects and evidence rather than hiding essential explanations in notes. Formal audience acceptance belongs to Q22C.

Actual Chromium PDF contains exactly 22 pages, each 960×540 pt. All pages were rendered and inspected in contact sheets, including the named print fallback on slide 6. No extra pages or missing slide content were found; slide 8's line/label crossing remains a defect. PDF page 17 includes the completion explanation, as intended by print styles.

Focused interaction checks ran offline with network disabled, using native pointer dispatch for buttons/radios:

- Slide 6 default: 4.05 mm selected, +0.05 mm nominal clearance, real WebGL canvas, observations hidden.
- Choosing 4.15: +0.15 mm nominal, +0.075 mm radial clearance. Reveal shows all recorded outcomes and PETG/0.4 mm nozzle/4.00 mm rod context.
- Optional hypothetical error −0.20: assumed hole 3.95 mm; diametral −0.05 mm; radial −0.025 mm; geometric interference. Error value was set through its input event, not pointer-drag precision testing.
- Front, isometric and reset-camera controls rendered; full model remained framed; reset-camera matches isometric. Exercise Reset returns 4.05/+0.05 and hides observations.
- Slide 17 selection, reveal and reset work. Reset clears choices and explanation; reveal distinguishes completion report from fit/mechanism proof.
- Forced no-WebGL context produces the analytic section, status and working nominal-choice/reveal controls. Pixel inspection nevertheless fails its layout as described above. The initial progress message calling fallback PASS referred to functional state and is superseded by this visual finding.

## Commands and artifacts

Commands: `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-audience-final/capture.mjs`; `swift /tmp/cad-audience-final/pdf-inspect.swift /tmp/cad-audience-final`; `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-audience-final/interact.mjs`; `swift /tmp/cad-audience-final/contact.swift`. All completed successfully; no harness assertions failed. Existing build and 5/5 source gates remain implementer evidence, not a new V execution.

Evidence root `/tmp/cad-audience-final/`: viewport-slide screenshots; `print-1.png` through `print-22.png`; `deck-print.pdf`; `print-text.txt`; `report.json`; `interactions.json`; `fit-revealed.png`, `fit-front.png`, `fit-iso.png`, `fit-view-reset.png`, `fit-no-webgl.png`; contact sheets. Paths were sent to root and Q22C as available. Only this receipt and temporary evidence were written. No source, tests, dependencies, locks, Git, hosting, CAD, slicing or printer changes.

REQ-019's explanation, real exercise and evidence distinctions are implemented; mobile diagram and fallback layout gates remain open. No physical acceptance follows. Next: scoped source repair and new immutable fingerprint; rerun affected 7/8/11 desktop/mobile/PDF and fallback captures, verify unaffected section/script/style identity before carrying forward their evidence, then join Q22C and formal review.

## Focused repair 1 — current PASS

Q22V status: **PASS** for HTML `06d289e8bc325f42b5e308ef449b971d77f2e6691178f864cdf1358ecda76895`. The preceding FAIL receipt remains historical. Candidate manifest `25ac949a2e5ed0cc8bf897abe8165c913f2e96bff9259dff00b80ef38d1e6a10` (14/14) and frozen manifest `67b865a128fe7943c2720d77c3698f34e7ffea8a7d3088dd1df1270a89bd056c` (20/20) matched before/after capture and again after fallback/pixel inspection.

Independent nesting-aware comparison to `/tmp/cad-audience-repair1-baseline/index.html` verifies exactly 22 sections, only 7/8/11 changed, and the other 19 byte-identical. Both inline scripts remain exact; simulator hash `d178097111b89b44d237848f21462d90234d8ca883c501a1d67ba5aaa35a91e6` and test hash `17cfe54de80aa25396594896d8df4830bf8696b5c57431241f767dd2bbb89bd7` match the prior verified candidate. Existing stylesheet content is preserved except trailing whitespace; the appended CSS affects only new `.case-mobile` elements and slide 6's unavailable canvas. The first parity attempt stopped on trailing-whitespace placement; trimming only that suffix confirms no existing CSS rule changed. This justifies carrying forward the prior all-22 desktop/mobile/PDF and focused 6/17 behavior evidence for unaffected content.

Fresh pixels cover slides 6/7/8/11 at 1280×800 and 390×844, compact 7/8 at 1178×820, and scrolling continuations. No horizontal overflow. Mobile 7/8 now stack large labelled panels; mobile 11 clearly names gear, shaft and overlapping material. All original tiny-label findings are resolved. Slide 8's diagonal line clears its text at desktop, compact, mobile and PDF sizes. Required wire geometry and proposed-only correction qualification remain visible. No blocking clipping/overlap was found in these fresh captures.

Forced no-WebGL capture at 1178×820 now has `#fit-canvas` display none, a complete section diagram/caption and the lesson ending at y=621.875, with document height 820. Mobile fallback is complete and readable through ordinary vertical scrolling; the empty canvas gap is gone. Choice 4.15 and observation reveal still work offline (+0.15 mm, observations visible). Functional checks use DOM click events in this focused rerun; prior native-pointer interaction evidence remains valid through exact script/control parity.

A newly printed PDF again has 22 pages, 960×540 pt. Pages 6/7/8/11 were freshly rendered and visually inspected; no missing content, extra page or line/label crossing remains. Normal WebGL slide 6 and print fallback remain fully framed and readable.

Fresh evidence: `/tmp/cad-audience-repair1/report.json`, `parity.json`, `added-css.txt`, `fallback.json`, `final-verification.json`; viewport-slide images and bottom continuations; `1178x820-fallback.png`, `390x844-fallback.png`, `390x844-fallback-bottom.png`; `deck-print.pdf`, `print-{6,7,8,11}.png`. Paths were sent to Q22C promptly. Commands: Node `capture.mjs` and `fallback.mjs` under this directory, Swift `pdf-inspect.swift` with this directory, and a focused final manifest verification via the same Node 26.7.0 executable. All completed; only the temporary harness whitespace assumption required adjustment. No candidate source or other repository files were mutated by Q22V.

REQ-019 visual and interaction gates pass with independently preserved prior coverage. Scope remains presentation validation; physical/CAD/printer acceptance is unchanged. Next: join Q22C's fresh audience receipt and formal review on this exact candidate. No further validation rerun is needed unless declared inputs change.
