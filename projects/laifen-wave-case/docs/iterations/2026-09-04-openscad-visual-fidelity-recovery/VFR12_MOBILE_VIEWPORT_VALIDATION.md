# VFR-12 independent viewport validation

Status: **PASS for V12-01 through V12-07 on the exact built local candidate.** V12-08 private delivery and actual iPhone/Safari acceptance remain pending. No blocking finding was observed in the frozen mobile presentation contract.

Owner: `VFR12-V` / `/root/openscad_vfr11_mobile_validator`, independent validator, distinct from implementation/critique/formal review. Project `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`; iteration `2026-09-04-openscad-visual-fidelity-recovery`. Writes were limited to this report and `scratch/vfr12-mobile-validation/`. No source, tests, candidate manifests, continuity, deployment, services, Tailscale or CAD changes. No repair or infrastructure retry was needed.

## Provenance

Candidate manifest `candidate/VFR12_MOBILE_VIEWPORT_CANDIDATE.sha256`: SHA-256 `024e441289844b118d8f4fbc9a5a26cabdab6dca50507dfcbbe7b9827a18320c`. All nine members verified before and after browser work. The manifest binds the task, implementation, frozen input manifest and six current source/test files. Current CSS is `176209d8c82940c74083b229f42585f3339c892109c18f9d9ceafca6c522359d`; focused test is `168e3bc9cc6f5d84965dd4f1ae163a1952bf7617e9c12bfed5857daf603ec708`.

Unchanged HTML/main/schema/worker match their frozen hashes. Additional build inputs (SCAD, installed runtime, dependency lock, Vite config, root/workspace package files) are bound by `scratch/vfr12-mobile-validation/build-inputs.sha256`, hash `a92147f83fd81b842ab32d9309105fc428b6a60eccd95682932c419f6820c84c`, identical to the previously reviewed C2 supplemental build-input manifest. SCAD remains `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.

Evidence inventory `scratch/vfr12-mobile-validation/evidence.sha256`: SHA-256 `566d54d64cdd548d2217241813309706bed07b650b39c7a275d7805f336366f6`, binding 28 files including built bundle, scripts, JSON/logs and 15 PNGs. The validator built into its exclusive scratch directory and served only that exact bundle at `http://127.0.0.1:8772/`.

## Commands and results

Repository cwd: `/Users/scottchu/.codex/worktrees/4f8c/design-projects` unless noted.

```text
# project cwd, before work and member verification again afterward
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_CANDIDATE.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_CANDIDATE.sha256
# repository cwd
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
npm run build:openscad-simulator --workspace projects/laifen-wave-case -- --outDir /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/vfr12-mobile-validation/dist
uv run python -m http.server 8772 --bind 127.0.0.1 --directory projects/laifen-wave-case/scratch/vfr12-mobile-validation/dist
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-validation/viewport.py > projects/laifen-wave-case/scratch/vfr12-mobile-validation/viewport-output.log 2>&1
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-validation/states.py > projects/laifen-wave-case/scratch/vfr12-mobile-validation/states-output.log 2>&1
```

Results: nine manifest members OK before/after; seven focused tests passed; Vite 6.4.3 build passed with eleven modules in 513ms; both real browser scripts exited 0. Only the standard >500kB bundle-size advisory appeared during build. Server stopped with Ctrl-C afterward, exit 0. No validation server remains running.

An additional inline `uv run python` read the saved JSON and asserted all mobile edge/frame/height, status, first-field hit, one-row/minimum-target, pseudo-font/size/centering, final-select clearance/hit and desktop boundary gates. All six viewport rows passed. It also compared CSS bytes before `@media` in the new built CSS against retained C2 `scratch/vfr11-mobile-c2-validation/dist/assets/index-BBglacgV.css`; they are identical, confirming unchanged desktop/global CSS. Exact underlying numeric observations are preserved in `viewport.json`, not merely passing assertions.

## Measurement method

Real Chromium 151.0.7922.34 ran headless with `--enable-unsafe-swiftshader` and device scale factor 1. Fresh pages were created at 390×844, 360×640, 430×932, 700×844, 701×844 and 1440×1200. No injected CSS, mocked worker or geometry substitution was used.

Normal element geometry/styles came from `getBoundingClientRect` and `getComputedStyle`. For pseudo icons the validator used Chromium CDP `DOM.getDocument` with depth−1/pierce, located each real `::before` pseudo node, then obtained its **actual layout box** with `DOM.getBoxModel`. Pseudo box centers were compared with both target content and target border box centers. Center hit tests used `document.elementFromPoint`. Thus icon centering is measured from browser layout, not inferred from `justify-content:center` alone.

## Responsive numeric results

All mobile result and canvas rectangles start at x0/y0 and end at the full viewport width; result bottom equals canvas bottom exactly. Border widths, padding and radius are all 0px. All first inputs are 46px high with 11px side inset. Final-select results are measured with document scrollY 0 and the form independently at its maximum scroll.

| Viewport | Canvas height | First label y range | First input y range | Action target size | Final select y range | Final-to-action clearance |
|---|---:|---|---|---|---|---:|
|390×844|219.4375|286.4375–304.4375|312.4375–358.4375|70.39–70.41×46|605.4375–649.4375|135.5625|
|360×640|190|257–275|283–329|64.39–64.41×46|372–416|165|
|430×932|220|287–305|313–359|78.39–78.41×46|694–738|135|
|700×844|219.4375|286.4375–304.4375|312.4375–358.4375|132.39–132.41×46|605.4375–649.4375|135.5625|

All first-input center hits return `device_length`. Every mobile row contains exactly five actions sharing the same y position. Every final-select top+1/center/bottom−1 hit returns `output_mode`; each final control is 44px high and clears actions by more than the required 8px. Document scrollWidth=clientWidth at all six viewports: 390, 360, 430, 700, 701 and 1440 respectively.

## Requirement coverage

- **V12-01 PASS — invisible visual status, preserved semantics.** At all mobile widths, header is display:none. Status is display:block, visibility:visible, position:absolute, 1×1px at (−1,−1), clip `rect(0px,0px,0px,0px)`, zero border/padding and no flow height. `aria-live="polite"` and the ready sentence remain. Actual accessibility snapshot includes `paragraph: Ready to generate a smooth STL.` The screenshot shows no ready sentence or title. After real generation, hidden status text updates to `Complete 04109b17a9e3` with clipping preserved.
- **V12-02 PASS — edge-to-edge initial pane.** At390×844 result and canvas are exactly `[0,0,390,219.4375]`; all mobile frame measurements are zero. No result-card frame or canvas rounding is visible. The table covers minimum/maximum responsive heights.
- **V12-03 PASS — fields/actions.** Initial complete Basic label/input is visible and hit-testable in every mobile row; fields have 11px inset. All action controls are simultaneously visible, single-row, and above 44×44. Final output select remains wholly exposed at maximum form scroll. No horizontal overflow.
- **V12-04 PASS — measured icon boxes and visual centering.** All 20 measured mobile pseudo boxes are exactly 24×24 with computed font-size 24px and centered inline-flex alignment. Maximum absolute center error is 0.0078125px horizontally and 0px vertically against both content/border center; all center hits identify their intended action. Initial, final and generated PNGs visually show centered icons. Unicode glyph ink footprints differ naturally: camera rotation remains optically smaller than the other rotation glyph, but its box is centered and there is no evident displacement. No claim of equal drawn-ink dimensions is made.
- **V12-05 PASS — responsive boundary.** At 700px the full mobile treatment applies. At 701px the header/status/card return, status clip becomes auto, canvas 580px and action text 16px; no overflow. This is the specified breakpoint, not a mobile failure at 701px.
- **V12-06 PASS — state/scroll.** At390×844, document scroll 80 and form scroll 500 leave viewer/result at x0/y0,390×219.4375; actions remain visible at y745.4375–804.4375. Invalid device length 0 exposes readable actionable role=alert/aria-live=assertive toast and focuses Dismiss. Dismiss hides it and restores Generate focus. Real smooth generation visibly renders the model and enables Download. Edit to 209 keeps the stale warning visibly present at x0/y16/390×36, removes download href and sets aria-disabled=true. All five surface/Diamond fields remain disabled.
- **V12-07 PASS — desktop preservation.** Fresh 1440×1200 has visible heading/caption and ready sentence, 580px canvas at x485/y201.875/878px width, 16px action labels, and unchanged global/desktop CSS prefix. The immutable HTML/main/schema/worker hashes remain unchanged; seven tests pass.
- **V12-08 PENDING — delivery.** No private-route deployment/check or actual-user acceptance is part of this local validator task.

## Visual evidence, findings and limits

All 15 PNGs were opened and inspected: `{390x844, 360x640, 430x932, 700x844}-initial.png` and corresponding `-final.png`; `701x844-initial.png`; `1440x1200-initial.png`; `desktop-actions.png`; `mobile-toast.png`; `mobile-generated.png`; `mobile-stale.png`; `mobile-scrolled.png`. Files reside under `scratch/vfr12-mobile-validation/`.

No blocking finding. Disabled Cancel/Download remain visibly muted; generated Download becomes enabled. Existing action wording is retained in the accessibility tree, with decorative glyph prefixes as before. HTML remains immutable and no title attribute/tooltips exist on the five actions; no tooltip-presence claim is made. This preserves the reviewed baseline rather than adding tooltip behavior. Actual screen-reader pronunciation and user understanding of the two rotation glyphs remain untested.

Both browser runs record empty page-error and failed-request lists, and no console errors. Console warnings are only software-WebGL `GPU stall due to ReadPixels` performance warnings. Geometry acceptance, cancellation-race repair, public Diamond enablement, mesh/slicer and physical acceptance are not implied by smooth browser rendering.

This independent PASS covers real desktop Chromium at the declared CSS viewports. The user's Safari, dynamic browser chrome/safe areas, keyboard, zoom/text scaling and native assistive technology remain outside it. Next action: distinct critic/formal reviewer joins this exact fingerprint; after authorization and formal PASS, verify served bytes and the actual private route, then obtain the user's phone feedback.

Final evidence verification: `shasum -a 256 -c evidence.sha256` from the validation scratch root passed all 28 members.
