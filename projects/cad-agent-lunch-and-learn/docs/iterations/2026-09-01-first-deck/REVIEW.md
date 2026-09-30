# Independent review

## R0 — provisional narrative and source review

- Owner: `deck_review`, independent from design, implementation and validation.
- Status: provisional narrative/source pass; **not final HTML approval**.
- Reviewed design-input manifest: `DESIGN_INPUTS.sha256`, SHA-256 `520a8871f4056ae9278c7210f2f543cb5a7be627cbb65245776400f0bc94cb46`; all 26 entries verified on 2026-09-01.
- Exact checks: `shasum -a 256 DESIGN_INPUTS.sha256`; `shasum -a 256 -c DESIGN_INPUTS.sha256` from the repository root using the full project-relative manifest path. Read all slide-plan sections, REQUIREMENTS and SOURCES; compared primary source sections below with `sed`. Recomputed counts using Node `fs.readdirSync` with top-level `isDirectory()` and the exact Kage amendment filename expression declared in S08.

### Findings and coverage

No material factual or narrative defect found in the frozen plan. The planned narrative connects purpose and hypothesis to actual gaps, specific responses, risk-driven decomposition, subsystem composition, ownership and feedback. It does not promise accepted source-project mechanisms or integrated runtime capability.

- S01, `EXPERIENCE.md` lines 5–15, 24–29, 69–76 and 262–281: coupon observations, source repair, rejected simulation and later 2D gate/digital acceptance are faithfully represented; nominal clearance remains separate from printed measurement and acceptance.
- S02, P20 R2 `HANDOFF.md` lines 64–87: shared diagonal-wire assumption and fixed 90-degree conflict are accurately represented. The correction is explicitly proposed in this record.
- S03, restart lines 121–152 and 408–474: reported 11/11 and three overlap values are correctly identified as actual-solid geometry evidence from a rejected namespace; physical restart gates remain proposed.
- S05/S07: Preparation and Operations are peer subsystems; product-facing roles retain long-term-direction and consequential-authority boundaries.
- S06, pilot lines 89–168: wrong logical tool, repaired profile resolution, observed printing/completion and later mechanism rejection remain distinct. The one-environment finding is not generalized to proven automation.
- S08 counts independently matched: canonical XT60 25 top-level iteration directories, worktree XT60 12, named Kage amendment family 11. Visible counts are scoped records, not print counts.
- S09, repository delegated execution protocol: development ownership and same-candidate evidence are present separately from product Manager/Teacher/Engineer-Operator roles.

### Remaining gate

R1 must inspect exact frozen HTML candidate, all rendered slides, revealed interaction states, source drawer and presentation UX, and join V1 results before final verdict. R0 does not establish layout, browser behavior, accessibility, print quality, or offline asset correctness.

## R1 — first HTML candidate, changes required

- Candidate: `CANDIDATE.sha256` SHA-256 `5e41ff18c3635fab8f8004cbbb96483566de54a2cc0cb1c83a7b10e31bec194e`, 10/10 entries verified. HTML hash `5318d1901384b08b435cf97cba21580f2399607d01d9a68aeb189f28b83007c9`.
- Owner: `deck_review`; source/narrative inspection only so far, waiting for final renders. Same reviewed primary-source fingerprint as R0.
- Commands: `shasum -a 256` and `shasum -a 256 -c` on candidate manifest; `sed -n '1,240p' build.mjs`; numbered source inspection with `nl -ba`.

### Material findings

1. **R1-001 / P2 — Citation buttons depend on prior drawer state.** In `build.mjs:56`, each footer source button queries a source article from the current live DOM, although articles are initially only in the `allSources` JavaScript string. On a fresh load, a primary-source button falls back to “cited as a synthesis.” Selecting one article also discards the other articles. Resolve IDs from a persistent source map or template independent of the current drawer. This blocks REQ-005's direct readable source references. Source inspection finding; V1 asked to exercise it after script repair.
2. **R1-002 / P2 — Product-direction qualifier missing from visible slide 18.** `build.mjs:45` says “The agent owns continuity” and lists roles, but omits the frozen design's visible “Long-term product direction” label. The caveat exists only in hidden presenter notes. Restore it on the audience canvas so standalone and printed slides do not imply present integrated capability (REQ-006). A matching lifecycle qualifier on slide 14 is a useful bounded clarification.
3. **R1-003 / P2 — Standalone source provenance is incomplete.** `build.mjs:21` gives S08's SHA field as “see SOURCES.md inventory table,” without embedding the named inventory or exact Kage method/path. S09 (`build.mjs:22`) lists two repository sources but supplies only the AGENTS canonical path/hash. Embed the declared inventory/method and both S09 provenance records in the source drawer; do not require the adjacent repository for verification (REQ-005).

### Validation join and remaining scope

V1 independently reported a fatal JavaScript parse error on fresh file load; the candidate has no active slide and cannot advance. This is a validator finding, not independently reproduced here. All-slide visual review must occur after the implementation role repairs the script and issues a new immutable candidate. No HTML approval is given, and no source or artifact was modified by review.

### Diagnostic visual pass (same first candidate, not functional acceptance)

Inspected all 22 V1 diagnostic laptop images individually at 1280×800 with `view_image`: `/tmp/cad-agent-lunch-and-learn-validation/diagnostic-slides/laptop-01.png` through `laptop-22.png`; also mobile 05, 10 and 17. V1 activated slides only in the browser to expose layout behind the fatal script error. These captures do not validate normal navigation or initial display.

- **R1-004 / P2 — Main CAD visual too small and title overlaps tags (slide 05).** The image is approximately 190×130 on the 1280×800 stage, while the large title crosses the Fit/Motion line. Separate heading/tags and place the main image outside the narrow body-width constraint so the artifact can explain coupling (REQ-007/010, DESIGN slide 05).
- **R1-005 / P2 — Numeric caption collision (slide 04).** The 25 descender overlaps its caption. Give each number/caption an explicit group and adequate line spacing; keep count scope unchanged.
- **R1-006 / P2 — Kage visual loses its boundary and purpose (slide 10).** Its conceptual/not-accepted caption is wholly below the laptop viewport. The visible drawing has only H/M/S, guide and motor labels and omits the planned light/shadow context, so the central example is unexplained without notes. Reserve caption space and retain the planned short shadow-clock/light-to-shadow context. This is a scope-preserving fix, not a new topic.
- **R1-007 / P2 — Completion exercise needs room for its answer (slide 17).** In the unrevealed desktop state, controls already end near y=750 on an 800-pixel stage. The answer/ladder cannot fit in the remaining space. Reserve space for both exercise states, for example with a desktop prompt/exercise split. V1 must test revealed state on the repaired candidate.
- **R1-008 / P3 — Angle glyph touches body copy (slide 08).** Add a small gap between the conceptual angle marks and “still wrong.”

Other baseline laptop slides are readable. Broad headline wrapping and deliberate whitespace do not warrant a theme change for this first draft. The development flow on slide 20 remains understandable, and its product-role distinction is visible. Mobile samples remain readable in their initial states; revealed-state, notes, overview, and print acceptance are still pending V1 and final captures.

## R1 — repair 1 verification

Candidate `bcdbdacf4e1d7c86b0345f1edef5d107a22559dc48deaa2146c14c6b1cc54231`, 10/10 manifest entries verified. Read repaired builder and inspected all 22 normal V1 laptop screenshots individually at 1280×800 (`/tmp/cad-agent-lunch-and-learn-validation/slides/laptop-01.png` through `laptop-22.png`), plus normal `fit-revealed.png`, `completion-revealed.png`, `sources.png`, `notes.png`, `overview.png` and mobile slides 04/05/10/17. These are actual normal browser renders, replacing the diagnostic-only evidence for visual inspection.

Resolved: R1-001 source lookup now uses an independent source container; R1-002 visible long-term qualifier restored; S09 component of R1-003 now supplies both source hashes/paths; R1-005 caption collision resolved; R1-008 angle spacing resolved. CAD image size in R1-004 is repaired. Other baseline slides remain readable with consistent visual hierarchy. Notes and source drawer show readable content and provenance only when opened. Factual meanings and source-project acceptance boundaries are unchanged.

One final bounded repair batch remains:

- R1-003 S08 still says “Kage individual hashes below” but embeds none, then redirects to external SOURCES.md. Include the declared hashes in the standalone source article.
- R1-004 tags still cross the slide 05 title near “decisions.” Image enlargement alone did not resolve text layering; place tags below the title in flow.
- R1-006 slide 10 disclaimer sits at y≈789 at the bottom edge, under the footer; reduce diagram height and reserve the caption above footer. The planned short shadow-clock/light-to-shadow context remains absent.
- R1-007 completion answer is visible but its evidence ladder is approximately 8 px and final outcome approximately 7 px at laptop size. This fails projected legibility. Use available width for a readable exercise/answer layout, retain the planned phase ownership labels, and avoid shrinking essential evidence to fit.
- **R1-009 / P2:** mobile toolbar covers the source-ID footer links. Reserve a separate source row above the toolbar.
- **R1-010 / P3:** overview removes `<br>` without spacing, joining words such as “modelpasses.” Preserve word spacing in overview labels.

Verdict: changes required. Final approval awaits the focused repaired candidate and V1's completed browser/print evidence. This review has not edited implementation source or artifacts.

V1 repair-1 join: validator reports 22 slides/one visible, both images decoded, 22 notes, zero runtime errors and zero HTTP requests, fresh-source success, correct five nominal clearances, and both reveal/reset interactions passing. Print gate remains failed: 23 PDF page objects for 22 slides, clipped fit qualifier and Kage content in print bounds. These independent findings reinforce changes-required; consult `VALIDATION.md` and V1's exact report for commands and numeric evidence. Review did not reproduce or substitute for those functional tests.

## R1 — repair 2 verification

Candidate `8b200517637b42569e8e51e232a51679847bc5e2e6a8476158f400db70b62783`, 10/10 manifest entries verified. Rechecked source and independently scanned every declared Kage amendment SHA against generated HTML with Node: 10/11 matched, i3-7 did not. Inspected all 22 newly regenerated normal laptop screenshots individually, completion revealed, and mobile 05/10 after V1 confirmed screenshot provenance.

Resolved visual defects: slide 05 image/title/tags now separate; slide 10 desktop caption is in the viewport with light-to-shadow context; completion evidence ladder is readable at 18 px with phase ownership; mobile source footer is above controls. Other laptop slides remain readable; source semantics and evidence distinctions remain intact.

Remaining material defects:

- **R1-003 / P2:** embedded S08 i3-7 hash is incorrect. It contains `7dc3657a2cea56bf5061d7be06303f7b265df48e821b55098dfe9864d57248fe48`; frozen source register requires `7dc3657a2cea56bf5061d7be06303f7b265df48b1c55098dfe9864d57248fe48`. All other ten amendment hashes match.
- **R1-011 / P2:** mobile slide 10 regressed. The final generic `.kage-map` width overrides its previous mobile width, rendering a roughly 187 px diagram with H/M/S wrapping and guide/light/disclaimer text overlapping. Restore a mobile width/layout that separates those labels and the disclaimer; the desktop composition does not need another redesign.
- V1's final actual PDF still has 23 pages, including a blank page 13 after slide 12. Screen bounds and print DOM bounds alone did not catch pagination; the actual PDF remains the acceptance evidence. This fails the declared one-slide-per-page delivery gate.

R1-010 overview spacing also remains (P3): the attempted late string replacement targets a builder expression already interpolated out of the HTML. It is not a blocker independent of the material findings above.

Verdict: cannot approve this candidate. The remaining corrections are precise provenance, responsive-regression and print-pagination fixes; no additional style expansion is requested.

## Final R1 verdict — D2 / I2 pass for local first-draft delivery

**PASS with minor limitations.** All material review and validation findings are resolved for the exact candidate below. This supersedes prior changes-required verdicts only for this candidate; the history above remains evidence of why the repairs were needed.

- Owner: `deck_review`, independent from design, implementation and validation.
- Final candidate manifest: `b353bfadf7c274ab126e08d059611a8899c139710fa65ce7a3d254ab98ebdc8d`, all 10 entries verified both before and after review.
- Final `index.html`: SHA-256 `911353124f9ab5a7537333d126ff4ad0da3a9d162491a2f4dac33f605f89d81f`.
- D2 design-input manifest: `f7f4e7305af420cd4356e0af476f1c8ff85ddd47c6e144abcee4783099f744b1`, all 26 entries independently verified. D2 changes only the three bounded implementation mechanisms and retains the original narrative/evidence contract.

### Final independent evidence

Commands: `shasum -a 256` and `shasum -a 256 -c` on the two manifests; read `build.mjs`, D2 contract, source register and final `VALIDATION.md`; Node `fs.readFileSync`/`matchAll` independently extracted the eleven named Kage rows and required each exact `filename = digest` pair to occur in generated HTML. Result: **11/11 exact paired matches**, old mistyped digest absent. The builder now derives the rows from the frozen register and guards the eleven distinct names.

After V1 confirmed final-candidate regeneration, inspected each of the 22 normal laptop screenshots individually at 1280×800, final mobile slide 10, revealed fit/completion states and PDF page renders 6, 10, 12 and 17. Captures are under `/tmp/cad-agent-lunch-and-learn-validation/`; no screenshot or PDF was treated as source-project CAD or physical evidence. Desktop image/title/tags, Kage conceptual boundary and light/shadow context, completion ownership/ladder and mobile footer/diagram are readable. Both printed answers and the key captions are present without clipping.

Joined independent V1's final durable evidence: fresh file loading, navigation, source references, notes, overview, exact exercise values, reveal/reset and input guards; 22 slides with one visible; two embedded images; zero runtime errors or network requests offline; normal captures at laptop/projector/mobile sizes. The actual written landscape PDF was reopened and has **22 pages, slides 01–22**, with no extra/orphan page after slide 12. This closes the print gate using the artifact itself.

### Requirement coverage

- REQ-001/009: English offline HTML, 22 slides, notes/navigation/references/overview and complete printed slides. Speaking duration remains a working assumption, not rehearsed evidence.
- REQ-002/003: purpose → expected/observed gap → understanding → smaller tests/phases → composition → feedback through real XT60 and Kage histories. Proposed Kage restart and P20 correction remain distinct from completed observations/repairs.
- REQ-004/006/011: concrete slicer pilot connects to peer Preparation/Operations responsibilities; product roles remain long-term direction, with separate bounded development roles and candidate ownership. Command, operational completion, CAD validity and physical acceptance remain distinct.
- REQ-005/007: source records and hashes are readable offline; counts retain declared scope; visuals are existing digital assets or explicitly conceptual. Canonical repository paths stay in source notes, with no printer identity or private runtime-job paths on the audience canvas.
- REQ-008/010: both teaching exercises preserve nominal-versus-observed meaning; the completed render review and distinct validation role establish readable first-draft delivery and useful interaction.

### Minor limitations and next action

No remaining P1/P2 finding. R1-010 overview labels still join some words at former line breaks (P3). The mobile Kage motor/gear label touches the large S, but the label and ring identity remain readable (P3). V1 documents mobile Fullscreen requiring toolbar horizontal scrolling and overview focus remaining on its trigger; these do not block the reviewed first-draft workflow. Do not describe this as exhaustive accessibility certification, live-projector testing or rehearsed timing.

Next: hand the local HTML to the user for presentation/content review. This verdict authorizes no source-project CAD acceptance, physical mechanism acceptance, printer operation, deployment or publication. Review wrote only this `REVIEW.md`; implementation artifacts were not changed by the reviewer.
