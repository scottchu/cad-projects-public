# VFR-12 C2 independent SVG-mask validation

Status: **BLOCKED — the actual rendered icons fail color, painted-size and optical-centering gates.** The responsive layout, accessible status, clean action names, first/final fields and exercised runtime states pass. Do not advance this fingerprint as a successful icon repair.

Owner: `VFR12-V` / `/root/openscad_vfr11_mobile_validator`, independent validator. Project `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`, active iteration `2026-09-04-openscad-visual-fidelity-recovery`. Writes used only this report and `scratch/vfr12-mobile-c2-validation/`; no source, tests, candidate manifests, continuity, deployment, services or CAD changes. One validation attempt, no repairs or infrastructure retry.

## Provenance and evidence

Candidate `candidate/VFR12_MOBILE_VIEWPORT_C2_CANDIDATE.sha256`, SHA-256 `86b208a98eff4d5fd34558de1050ccf6224593209210236a060027b9a0192bbf`; all nine members verified before and after browser work. Prior critique reviewed: `VFR12_MOBILE_VIEWPORT_CRITIQUE.md`, assigned fingerprint `5349b3638c3d7e65740caa9722c8cbe89d822c8cd8c2ba014920c59aa772de3c`.

Exclusive evidence inventory: `scratch/vfr12-mobile-c2-validation/evidence.sha256`, SHA-256 `b3b3b923bfca685c101c2c09100893c6bbbace2082d2c39a3da0cf444ad98f18`, binding 32 files including built bundle, browser scripts/JSON/logs, screenshot pixel-analysis script/results and PNGs. Supplemental build inputs were rehashed and verified against prior reviewed inputs, then recorded in `build-inputs.sha256`; its hash remains `a92147f83fd81b842ab32d9309105fc428b6a60eccd95682932c419f6820c84c`.

The validator built this candidate into its own scratch `dist` and used real Chromium 151.0.7922.34, device scale factor 1, `--enable-unsafe-swiftshader`, against `http://127.0.0.1:8774/`. No injected CSS or mocked compiler. Fresh initial viewport crops were captured before scrolling at 360×640, 390×844, 430×932, 700×844, 701×844 and 1440×1200.

## Blocking findings

### High — black SVG background images override the intended currentColor paint

The Generate button's computed color and pseudo background-color are white, but its actual icon is black on the navy button. At the center of the filled star the screenshot pixel is RGB(0,0,0), while the adjacent button background is RGB(17,34,51). This repeats in fresh 360/390/430 screenshots and is plainly visible in `390x844-initial.png` and `mobile-generated.png`.

Each pseudo element sets both `background-color:currentColor` and a `background-image` containing an SVG with `fill='black'`, then masks the combined background with the same SVG. The opaque black image paints over the currentColor layer. The mask controls coverage, not that image's black paint. Thus computed currentColor alone gives false confidence: the visible enabled Generate mark has lost its intended white foreground and is difficult to see. The enabled reset/download marks also render black instead of the declared navy foreground.

The smallest responsible repair is in the mobile icon paint rules: ensure only the intended currentColor paint is exposed through the mask, without an opaque black background image covering it. This report does not implement that correction.

### High — actual marks still fail the assigned painted-size/optical gates

All pseudo layout boxes are 24×24 and centered, but the painted pixels fail the explicit >=18×18 and <=1px optical-center gates:

| Action | Painted bounds at 360/390/430 | Painted center delta x/y from target at 390 | Result |
|---|---|---|---|
|Generate|22×22|−0.1953125 / 0|Size/center pass; color fails above|
|Cancel|16×16|+0.40625 / 0|Both dimensions below 18|
|Reset|21×21|+0.5078125 /+1.5|Vertically lower than 1px gate|
|Reset camera|17×17|−0.890625 /+0.5|Both dimensions below 18|
|Download|16×18|+0.203125 / 0|Width below 18|

Values repeat across all three fresh phone-size screenshots. Pixel analysis was confined to each CDP-measured pseudo box, excluding button borders. It detects pixels differing from sampled adjacent button background by at least 10 in any RGB channel. A threshold-sensitivity check at 390 using 1,5,10,20 and 32 gives identical failing Cancel/Camera/Download dimensions and Reset +1.5px y offset. Generate's antialiased extent shrinks to 20×20 at threshold 32 but remains centered. Full pixel coordinates, background samples and centers are preserved in `ink.json` and `ink-thresholds.json`; the reproducible main analysis is `measure_ink.py`.

Visual inspection agrees: the fourth mark is more substantial than the previous Unicode glyph but remains smaller than the intended minimum, while Reset's mark is low. The SVG masks have different marks, but the requested size/currentColor/centering contract is not met. No claim of standard, unambiguous action comprehension is made for the two circular-arrow silhouettes.

## Passing coverage

Actual CDP `DOM.getDocument` pseudo nodes and `DOM.getBoxModel` establish all 20 mobile pseudo boxes are 24×24; maximum layout-box center error remains 0.0078125px horizontally and 0px vertically. All pseudo center hit tests return the intended target. Empty pseudo content removes the Unicode prefixes: accessibility names are exactly Generate STL, Cancel, Reset, Reset camera and, after generation, link Download STL. This closes the prior name-prefix issue. It does not close the painted-pixel failures above.

| Viewport | Viewer/result initial rectangle | First input y range | Final output y range at page top/form max | Clearance above actions |
|---|---|---|---|---:|
|360×640|x0/y0/360×190|283–329|372–416|165|
|390×844|x0/y0/390×219.4375|312.4375–358.4375|605.4375–649.4375|135.5625|
|430×932|x0/y0/430×220|313–359|694–738|135|
|700×844|x0/y0/700×219.4375|312.4375–358.4375|605.4375–649.4375|135.5625|

All mobile viewer/result borders, radius and padding are zero. Each first Basic label is fully visible above its 46px-high input; all inputs start 11px from the side and center hits succeed. Five actions share one row, each 46px high and 64.39px or wider. Final select top+1/center/bottom−1 hits all return `output_mode` at document scrollY 0/form maximum. Document scrollWidth equals clientWidth for all six viewports.

Mobile header is hidden; status is clipped to an absolute 1×1 box, display:block/visibility:visible, and remains an accessible paragraph with `aria-live=polite`. It updates after generation while remaining visually hidden. At 701px desktop presentation returns; at 1440×1200 the heading, visible ready status, 16px text labels and 580px canvas remain. New built CSS before `@media` matches the previous built desktop/global CSS prefix exactly.

State checks pass: invalid length 0 shows readable alert and focuses Dismiss; dismissal returns focus to Generate. Smooth generation completes `04109b17a9e3`, visibly renders a model and enables Download with clean link name. Edit to 209 makes stale text visible, removes href and sets aria-disabled=true. All five surface/Diamond controls remain disabled. Disabled controls still receive opacity 0.46/grayscale styling and look muted, although their SVG paint color is affected by the black-image defect. At document scroll 80/form scroll 500, preview remains sticky at x0/y0 and actions remain visible.

## Commands actually run

Repository cwd `/Users/scottchu/.codex/worktrees/4f8c/design-projects` unless marked otherwise.

```text
# project cwd, before and after browser work
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C2_CANDIDATE.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C2_CANDIDATE.sha256
# repository cwd
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
npm run build:openscad-simulator --workspace projects/laifen-wave-case -- --outDir /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/vfr12-mobile-c2-validation/dist
uv run python -m http.server 8774 --bind 127.0.0.1 --directory projects/laifen-wave-case/scratch/vfr12-mobile-c2-validation/dist
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-c2-validation/viewport.py > projects/laifen-wave-case/scratch/vfr12-mobile-c2-validation/viewport-output.log 2>&1
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-c2-validation/states.py > projects/laifen-wave-case/scratch/vfr12-mobile-c2-validation/states-output.log 2>&1
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-c2-validation/measure_ink.py > projects/laifen-wave-case/scratch/vfr12-mobile-c2-validation/ink-output.log
```

All commands exited 0. Seven focused tests passed; Vite 6.4.3 built eleven modules in 527ms with only the standard >500kB chunk advisory. The scripts completing successfully means observations were collected, not that the visual acceptance gates passed. Additional inline `uv run python` checks wrote the threshold-sensitivity JSON, compared the desktop CSS prefixes and rehashed supplemental build inputs/evidence. The temporary server was stopped with Ctrl-C, exit 0. No server or public route change remains.

Browser page-error and failed-request arrays are empty. No console errors; only repeated software-WebGL `GPU stall due to ReadPixels` performance warnings. Exact computed styles, rectangles, masks, accessibility snapshots and CDP quads are in `viewport.json`; state details are in `states.json`.

Screenshots opened and inspected: initial 360/390/430/700/701/1440 captures, final 360/390/430 captures, desktop-actions, mobile-generated, mobile-toast, mobile-stale and mobile-scrolled. All reside under the C2 validation scratch directory and are manifest-bound.

## Disposition and limits

Keep this candidate blocked. Route the smallest CSS/SVG paint, path-size and optical-placement correction within the existing repair ceiling, refreeze, then rerun actual painted-pixel measurements and independent visual critique. Do not accept a 24px CSS box as evidence that the mark itself is 24px or correctly colored.

This is controlled Chromium validation, not private delivery or actual iPhone/Safari acceptance. Screen-reader pronunciation, tooltip presence and icon comprehension were not user-tested; unchanged HTML has no title-based tooltips. Public Diamond/cancellation-race HOLD, CAD/mesh/slicer and physical acceptance remain separate. No deployment is approved by this receipt.

Final evidence verification: `shasum -a 256 -c evidence.sha256` from the C2 validation directory passed all 32 members.
