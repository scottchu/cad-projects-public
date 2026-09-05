# VFR-11 C2 independent validation

Status: **PASS for the assigned local browser layout/state gates**, with a remaining accessibility-name/affordance caveat for independent critique and formal review. This does not declare every prior critique finding resolved or grant deployment, actual-phone, Diamond, geometry or physical acceptance.

Owner: `VFR11-V` / `/root/openscad_vfr11_mobile_validator`, independent validator. Writes were limited to this report and `scratch/vfr11-mobile-c2-validation/`. No source, tests, continuity, deployment, services, CAD or geometry bytes were changed. No candidate repair or infrastructure retry was needed.

## Frozen provenance

Project: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`.
Iteration: `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery`.
Candidate: `candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256`.
Candidate SHA-256: `ad7c14d9f40f354c70cbaf0394b89a9a03f795ec9e4d767c55c263096f054968`.
All eight declared members verified before and after validation. CSS hash is `d13361dc7519cbe2172ee0107e70e3a0d192b84078d723bd3dc8f686fb637cdb`; HTML/main/schema/worker retain their candidate hashes.

Prior critique addressed: `VFR11_MOBILE_DENSITY_CRITIQUE.md`, assigned SHA-256 `5c46ea2fa774ecf7fa2e0ad487ed13cbd2a452f221159aeced0e673666f24171`. Its initial-page/form-maximum overlap was specifically reproduced as a test condition in this C2 run.

Scratch evidence root: `scratch/vfr11-mobile-c2-validation/`. Its `evidence.sha256` binds 22 files, including both probe scripts, measurements, console logs, screenshots, and the exact built bundle; manifest SHA-256 `58c9e14211b610a6be670cbbfad998485da6e911690270371a54a26c83e17ed7`. Supplemental build inputs are bound by `build-inputs.sha256`, SHA-256 `a92147f83fd81b842ab32d9309105fc428b6a60eccd95682932c419f6820c84c`, covering SCAD, Vite config, root/workspace package files, lock and installed WASM runtime.

## Commands and results

Repository-root cwd for tooling: `/Users/scottchu/.codex/worktrees/4f8c/design-projects`.

- From project cwd: `shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256` and `shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256`: expected manifest fingerprint, 8/8 members OK. Member check repeated after browser work, 8/8 OK.
- `uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q`: exit 0, six passed.
- `npm run build:openscad-simulator --workspace projects/laifen-wave-case -- --outDir /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/vfr11-mobile-c2-validation/dist`: exit 0, Vite 6.4.3, eleven modules, 526 ms. Standard >500 kB chunk advisory only.
- `uv run python -m http.server 8768 --bind 127.0.0.1 --directory projects/laifen-wave-case/scratch/vfr11-mobile-c2-validation/dist`: temporary loopback endpoint `http://127.0.0.1:8768/`. Server stopped with Ctrl-C after testing, exit 0.
- `uv run python projects/laifen-wave-case/scratch/vfr11-mobile-c2-validation/validate.py > projects/laifen-wave-case/scratch/vfr11-mobile-c2-validation/browser-output.log 2>&1`: exit 0. Real initial mobile, final-field max-scroll, hit tests, scroll, toast/focus, stale/reset/Diamond state and desktop styles.
- `uv run python projects/laifen-wave-case/scratch/vfr11-mobile-c2-validation/supplement.py > projects/laifen-wave-case/scratch/vfr11-mobile-c2-validation/supplement-output.log 2>&1`: exit 0. Fresh desktop title capture, desktop actions, initial hit tests/keyboard order, real smooth generation and subsequent stale invalidation.

Browser: Chromium 151.0.7922.34, headless, device scale factor 1, `--enable-unsafe-swiftshader`. No CSS injection or mocked compiler. Main measurements are in `measurements.json`; supplemental states are in `supplement.json`. Probe scripts were adapted from the previous validation into the exclusive C2 scratch directory; previous evidence was not edited.

## Requirement evidence

All dimensions below are CSS pixels at 390×844 unless explicitly desktop.

| Gate | Result and measured evidence |
|---|---|
| Mobile title/caption hidden | PASS: header display:none, zero rectangle; screenshot starts with status and preview. |
| Canvas 190–220 px | PASS: x21, y71, width348, height219.4375, bottom290.4375. |
| First complete Basic field initially visible | PASS at scrollY 0: label y371.4375–389.4375; enabled `device_length` input x21, y397.4375, width348, height46, bottom443.4375. Center hit returns the input; first Tab reaches it; editing succeeds. |
| Full five-icon row initially visible | PASS: action strip y 785–844; five targets y792–838, each 66.39–66.41×46. Font-size0 hides text visually; rendered pseudo icons are 20px. All five center hit tests return their respective controls. |
| Final field usable at form maximum without page scroll | PASS: document scrollY 0; form scrollTop=max 2551. `output_mode` x21, y690.4375, width348, height44, bottom734.4375. Action top 785 gives 50.5625 clearance. Hit tests at top+1, center, bottom−1 all return `output_mode`. This closes the previous 13.4375 px overlap condition at the tested viewport. |
| Disabled controls visibly distinct | PASS: initial Cancel and Download computed opacity 0.46, grayscale(1), muted foreground rgb(100,112,123), background rgb(238,241,244), border rgb(197,205,213). Enabled controls have opacity 1/filter:none. Initial versus generated screenshot visibly shows Download becoming dark/enabled; Cancel remains muted after completion. |
| Accessible action wording retained | PASS for retention: accessibility snapshot contains `✦ Generate STL`, `■ Cancel` disabled, `↻ Reset`, `⟳ Reset camera`; generated Download is link `⇩ Download STL`. Caveat: glyph prefixes remain; aria-label/title are absent. |
| Icons actually render | PASS: all five glyphs visibly render in initial/final-field/generated PNGs. This does not prove that the two different circular-arrow glyphs communicate Reset versus Reset camera without learning. |
| Sticky behavior | PASS: at document scrollY 120, preview stays at top0 and actions stay y 785–844; form scrolling changes fields beneath the sticky preview. Initial-page/form-max state is independently exercised above. |
| No horizontal overflow/clipping | PASS: scrollWidth=clientWidth=390 in initial, final-field, scroll and toast states; controls/canvas fit x21–369. Desktop widths both 1440. Intentional vertical field clipping during intermediate form scrolling is not horizontal overflow. |
| Toast/focus | PASS: device_length 0 yields actionable alert, focuses Dismiss, and dismissal hides alert and restores focus to Generate. Reset restores 208. |
| Stale, Download, Diamond | PASS on exercised paths: all five surface/Diamond inputs disabled; real smooth success enables Download; edit to 209 subsequently shows stale, removes href and sets aria-disabled=true. |
| Desktop preservation | PASS for layout/title/text: fresh 1440×1200 header display:block, rect x60/y41.4375/1320×77.4375; title/caption visible; canvas 580px; all five text labels 16px. The intentional disabled styling also applies on desktop, so desktop pixels are not literally unchanged. |

Smooth generation completed `Complete 04109b17a9e3`; download name `laifen-04109b17a9e394ae9bdd97d43ca4af573c48b32ecbfcff85507dc3650f380d3e.stl`. Preview rendered without error note/toast and retained the compact dimensions. This is browser evidence, not STL geometry acceptance.

## Visual inspection and findings

Validator inspected these exact C2 screenshots: `mobile-initial.png`, `mobile-final-field.png`, `mobile-form-scroll.png`, `mobile-toast.png`, `mobile-generated.png`, `desktop-top.png`, `desktop-actions.png`. They show the complete first Basic field, the final Output field above the actions, distinct disabled treatment, visible glyphs, intact alert and retained desktop title/text. `desktop-initial.png` is a diagnostic capture from the reused page with retained scrollY 161; fresh `desktop-top.png` at scrollY 0 supplies initial desktop evidence. `mobile-page-scroll.png` is retained alongside numerical sticky evidence.

- **High overlap finding: resolved at 390×844.** The final 44px select is completely exposed with 50.5625px clearance at the exact formerly failing initial-page/form-maximum state.
- **Medium prior affordance finding: only partially resolved.** Disabled-state distinction is visibly corrected and glyphs render. Clean explicit accessible names were not implemented: unchanged HTML has no aria-label/title, and CSS glyphs still prefix accessible names. Reset `↻` and camera reset `⟳` remain visually similar, and the star does not itself establish user understanding of Generate STL. The assigned retention/render gates pass; independent critique/formal review must explicitly decide this remaining qualitative requirement. Do not treat this validation as closing that entire prior finding.
- **Low delivery limitation: remains.** This is controlled desktop Chromium at 390×844, not the user's phone/Safari or private delivered URL. Browser chrome, safe areas, keyboard, zoom/text scaling and nearby viewport sizes were not exercised.

Both probes record no page errors, console errors or failed requests. Console output is limited to repeated WebGL `GPU stall due to ReadPixels` software-rendering/screenshot performance warnings (four per probe).

Existing VFR-09 cancellation-race/Diamond HOLD is not repaired or retested by C2. No CAD, exported mesh, slicer or physical acceptance is claimed. Formal review should verify C2 provenance and join this scoped validation with the critic's disposition of the remaining names/icon-meaning issue before advancing.

Evidence verification: `shasum -a 256 -c evidence.sha256` from the C2 scratch root passed all 22 members.
