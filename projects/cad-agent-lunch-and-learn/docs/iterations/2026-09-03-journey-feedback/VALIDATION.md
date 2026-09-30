# J-V validation

## Initial candidate — REPAIR REQUIRED

Owner: `/root/first_layer_validator`; 2026-09-03. Source gate released after capture and demo checks. This is presentation/artifact validation, not CAD, slicer or physical acceptance.

Frozen identity: HTML `f79f24460dc7aff7cd80455cfb28f3acd93a5120020001379b8f9dc37502497e`; CANDIDATE.sha256 `ce5303954c8b9db721204ec6ef202b65f32ded7cadcbe83924bc02d8d11f0fd0`, 148 entries. Manifest checked before and after full captures with no drift. Source, 99 evidence snapshots and local assets are included. Read IMPLEMENTATION, PRESENTER_GUIDE and source audit boundaries; no source edits or device actions by validator.

### Evidence and commands

Commands ran from repository root, zsh without login. Node is `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node`.

- `shasum -a 256 -c projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-03-journey-feedback/CANDIDATE.sha256`: 148/148 PASS, `/tmp/cad-journey-feedback-validation/manifest-check.log`.
- `node /tmp/cad-journey-feedback-validation/capture.mjs ce5303954c8b9db721204ec6ef202b65f32ded7cadcbe83924bc02d8d11f0fd0 20`: exit 0. All 20 slides captured at 1280×800 and 390×844, with mobile scroll continuations. Full before/after fingerprints, navigation, WebGL and overflow measurements in `report.json`; browser exceptions zero; external requests zero. End/Home/arrow navigation and 20 overview entries checked.
- `swift /tmp/cad-journey-feedback-validation/pdf-inspect.swift /tmp/cad-journey-feedback-validation 20`: exit 0, actual PDF has 20 pages; extracted text and all rendered pages inspected through print sheets and critical full pages.
- `swift /tmp/cad-journey-feedback-validation/sheets.swift`: exit 0. All desktop, mobile top/bottom and actual PDF sheets reviewed. Capture directory contains `1280x800-slide-1.png` through `-20.png`, corresponding `390x844-slide-N*.png`, `print-N.png`, and sheets.
- `node /tmp/cad-journey-feedback-validation/demo.mjs`: exit 0; final `demo.json` has no exceptions. Initial iframe lookup failure was repaired in the temporary harness by attaching the out-of-process iframe target; no product change.
- `node /tmp/cad-journey-feedback-validation/title-nogpu.mjs`: exit 0; clean same-source title capture with GPU disabled. Writer reports existing build/check 6/6 PASS; validator did not regenerate source during the source freeze.

### Results and findings

**High — PDF clipping blocks release.** Actual 20-page PDF applies stacked mobile layouts and clips lower content on numerous pages, including 3–9, 11–13, 16–17 and 20. Page 9 loses lower fit-table rows, page 17 loses the contact comparison and page 20 loses the shared return path. Evidence: `print-sheet-1.png` through `print-sheet-3.png`. Candidate CSS has unscoped max-width media rules; writer must isolate screen responsiveness and revalidate all 20 actual PDF pages. Initial PDF is diagnostic only: `/tmp/cad-journey-feedback-validation/deck-print.pdf`, SHA-256 `c6bb582b96fed90c6e024611a1ce45a1b898f1dbd5ebee2c4c7451a45649565a`. No final release PDF produced.

**Medium — source clarity and teaching geometry.** Independent editorial findings accepted for focused repair: define XT60 on slide 3; name guided CLI/skills separately from read-only U1 MCP on 14; name the printed jobs and acceptance scope on 15; add case/end boundaries to the centered/resting comparison on 17; replace internal audit cues in presenter guidance with speaking cues. Validator concurs that the current bars on 17 lack the boundary needed to see contact.

**Closed capture anomaly — slide 1.** SwiftShader produced a repeated four-quadrant title in two fresh captures. DOM contains one title (1000×131.8 bounding box, within viewport). Mobile and PDF page 1 are clean. An isolated `--disable-gpu` capture of the same frozen HTML is clean: `1280x800-slide-1-nogpu.png`. This is a capture compositor artifact; preserve source title. `fromSurface:false` was unsupported by this headless browser.

**PASS — screen layout and runtime.** Remaining desktop pages render without clipping. Mobile continuation exposes the entire content, including table rows and architecture return path, without horizontal page overflow. The real read-only fit scene on slide 9 produces WebGL contexts/draws offline; forced no-WebGL produces the labeled static fallback without exception. Captured canvas dimensions are 551×310 desktop and 335×280 mobile. Main-slide interaction is limited to the approved presenter demo launcher and deck navigation.

**PASS — isolated Laifen demo.** Dialog is outside main slides; iframe sandbox is exactly `allow-scripts`; srcdoc contains the exact archived Lgate fragment. Offline default q=0.5 gives upper/lower 2.5/2.5 mm; bottom preset q=0 gives 5/0 mm and explicit contact; reset restores q=0.5. Fallback shows all three archived images, and close returns to slide 17. Screenshots `demo-centered.png`, `demo-bottom.png`, `demo-fallback.png`. The long original diagram scrolls inside the iframe; presenter should scroll to its lower end when showing contact. This is an earlier nominal-envelope study, not R6 CAD controls or physical dynamics.

**PASS — evidence boundaries, with the clarity repairs above.** Actual P25 UI states are preserved later artifacts, explicitly not the missing original rail customizer; prescribed poses make no force/friction/retention claim. The rod coupon records physical fit; thin-web toolpaths remain prepared/physical-pending. Recorded operation and current MCP capabilities are separately classified. The UI image is labeled synthetic. Earlier Laifen closure feedback is not R6 full-case fit acceptance. Software fixture and sensor/arm ideas remain illustrative/future. Digital model evidence and physical observations remain distinct in the shared feedback architecture. Provenance assets and frozen source records match the manifest; no invented physical photo or full-physics claim found.

### Next action

Writer applies the single consolidated repair. On new fingerprint, compare exact source/body/runtime parity, capture affected desktop/mobile pages 3/14/15/17, use clean alternate title capture, render and inspect every actual PDF page, and release `releases/journey-feedback.pdf` only after PASS. Carry runtime evidence only when simulator and demo script/fragment hashes are unchanged. Final PDF checksum and command must be appended here.

## Repair 1 — PASS; final PDF released

Owner: `/root/first_layer_validator`; 2026-09-03. Final HTML `bbbbf1ec72ea4841aaa7b13f27edc934def4b86f85a50cb1d054bb59c4e4f55e`; CANDIDATE.sha256 `fd81903eba6c8253a345825b0821dff6eaf1fc72923788af44c529eb6bb4492f`, 148 entries. Exact initial baseline is `/tmp/cad-journey-repair1-baseline`. All final manifest entries verified before and after capture.

Independent parity comparison confirms changed sections exactly 3, 14, 15 and 17; the other 16 sections are byte-identical. `simulator.mjs`, the inlined simulator bundle, all 21 manifest asset/provenance paths, and navigation/demo source template are identical. The rendered first script differs only because it embeds revised notes; the execution template is unchanged. CSS diff consists of screen-only scoping for both responsive blocks plus a selector scoped to the new gap SVGs. Evidence: `/tmp/cad-journey-repair1-validation/parity.json`. This supports carrying initial full-deck screen, offline WebGL/fallback and Laifen interaction evidence; no runtime rerun was needed.

Executed:

- `node /tmp/cad-journey-feedback-validation/capture.mjs fd81903eba6c8253a345825b0821dff6eaf1fc72923788af44c529eb6bb4492f 20 /tmp/cad-journey-repair1-validation 3,14,15,17`: exit 0; affected desktop/mobile captures, actual full PDF, zero exceptions, 20-slide count/navigation and before/after manifest PASS.
- `swift /tmp/cad-journey-feedback-validation/pdf-inspect.swift /tmp/cad-journey-repair1-validation 20`: exit 0, actual 20 pages. All 20 rendered PDF pages inspected. Print clipping is resolved: full fit table, three P25 states, evidence table, comparison, complete Laifen contact schematic and architecture return path are visible.
- `swift /tmp/cad-journey-repair1-validation/sheets.swift`: final exit 0, changed desktop/mobile and all-page PDF sheets inspected. An initial sheet-only missing-bottom-file error for the now-shorter slide 15 was corrected by using its complete top capture; no source or PDF change.
- `node --test projects/cad-agent-lunch-and-learn/test/deck.test.mjs`: 6/6 PASS. Exact asset-copy equality, script parsing, offline resources, show-and-tell, Three.js fallback and isolated Laifen requirements covered; log `check.log`.

Changed-slide checks PASS: XT60 is defined; guided Snapmaker Orca CLI execution is visibly distinct from read-only U1 Print Studio MCP; the PETG example identifies two cam-plate parts and separates completed printing from failed assembly. This wording matches frozen pilot record lines 14, 28 and 153, without assigning an unrecorded project identity. Laifen now has identical outlined cavities and a bottom boundary, with centered clearance versus resting contact clearly visible and nominal/exaggerated status retained. All four changed mobile slides remain fully accessible through scrolling without horizontal clipping. The guide supplies the iframe scroll cue. The clean title capture from the initial candidate carries by exact title/section and applicable screen-style parity; no title source modification was needed.

Final PDF: `projects/cad-agent-lunch-and-learn/releases/journey-feedback.pdf`, copied byte-for-byte from the inspected `/tmp/cad-journey-repair1-validation/deck-print.pdf`. SHA-256 **`570b95d4e979f1bd1cb34233407b76dae83085f0198baf6768a2bf4d8a349274`**. Generated by the capture command above via Chromium `Page.printToPDF({printBackground:true,preferCSSPageSize:true})`, 13.333×7.5 inch CSS page size, 20 pages. Release copy command: `cp /tmp/cad-journey-repair1-validation/deck-print.pdf projects/cad-agent-lunch-and-learn/releases/journey-feedback.pdf`; checksum checked with `shasum -a 256`.

No material validation issue remains. Known limitations remain explicit in the deck: prescribed simulation poses are not physics, historical print evidence is scoped, R6 full-case physical fit is pending, fixture readings are synthetic, and future integrations are illustrative. PDF is static and uses the labeled fit fallback; live Laifen interaction remains in the HTML. Next action: root completes distinct formal review/provenance join and provides HTML plus this PDF.
