# VFR-11 independent mobile density validation

Status: **PASS for the bounded local mobile-density candidate**. This is not deployment, actual-phone delivery acceptance, Diamond-browser acceptance, CAD acceptance, or physical acceptance.

Owner: `VFR11-V` / `/root/openscad_vfr11_mobile_validator`, independent validation role. Implementer source and tests were read-only. Allowed writes used only this report and `scratch/vfr11-mobile-validation/`. Candidate repairs: none. One supplemental browser capture corrected the validation setup's retained desktop scroll position; no application or infrastructure repair was needed.

## Provenance

Project: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`.
Iteration: `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/`.
Candidate manifest: `candidate/VFR11_MOBILE_DENSITY_CANDIDATE.sha256`.
Manifest SHA-256: `dfa8ff0c1ea51daab363b48756747d7a6e26a392fa125c321d4dd4536c294077`.
All eight members verified before testing and again after browser work. No frozen member changed.

The validator built this candidate into its exclusive scratch directory, served that directory on loopback, and exercised the actual Vite bundle with actual Chromium 151.0.7922.34. The main, schema, worker and HTML match the frozen manifest. Additional build inputs absent from that candidate manifest (SCAD, Vite config, dependency lock, vendor runtime, root/workspace package files) are bound by `scratch/vfr11-mobile-validation/build-inputs.sha256`. The SCAD input is `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.

The complete scratch evidence inventory, including built bundle, probe scripts, browser measurements and PNGs, is `scratch/vfr11-mobile-validation/evidence.sha256`, SHA-256 `94f4e43781d444d64eb52b8243fba5bd30f5689eb25d0bb972e76229a5dfefc2`.

## Commands actually run

Unless noted, cwd was `/Users/scottchu/.codex/worktrees/4f8c/design-projects`.

1. Project cwd: `shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_CANDIDATE.sha256` and `shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_CANDIDATE.sha256` — exact expected manifest; 8/8 members OK. Member verification repeated after browser work, 8/8 OK.
2. `uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q` — exit 0, six tests passed.
3. `npm run build:openscad-simulator --workspace projects/laifen-wave-case -- --outDir /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/vfr11-mobile-validation/dist` — exit 0; Vite 6.4.3, eleven modules transformed, build completed in 504 ms. Only the standard >500 kB chunk-size advisory appeared.
4. `uv run python -m http.server 8766 --bind 127.0.0.1 --directory projects/laifen-wave-case/scratch/vfr11-mobile-validation/dist` — temporary loopback server; tested URL `http://127.0.0.1:8766/`.
5. `uv run python projects/laifen-wave-case/scratch/vfr11-mobile-validation/validate.py > projects/laifen-wave-case/scratch/vfr11-mobile-validation/browser-output.log 2>&1` — exit 0. Initial 390×844 page, page/form scroll, invalid-input toast, dismissal/focus, reset, disabled states and desktop styles.
6. `uv run python projects/laifen-wave-case/scratch/vfr11-mobile-validation/supplement.py > projects/laifen-wave-case/scratch/vfr11-mobile-validation/supplement-output.log 2>&1` — exit 0. Fresh desktop at 1440×1200, hit tests, keyboard traversal, real smooth generation, enabled Download name, and subsequent stale invalidation.

Both scripts launch headless Chromium with `--enable-unsafe-swiftshader`, device scale factor 1. No mocked worker, injected CSS, source transformation, external deployment or printer operation was used. The first desktop screenshot from the reused page retained scrollY=161; it is diagnostic only and is superseded for initial-title evidence by the fresh `desktop-top.png` at scrollY=0.

## Requirement matrix and measured browser evidence

Measurements are CSS pixels. Full rectangles/computed styles/state snapshots are in `measurements.json` and `supplement.json` beneath the scratch evidence directory.

| Contract | Result | Evidence |
|---|---|---|
| Mobile title and caption visually absent | PASS | At 390×844, header computed `display:none`; zero rectangle. `mobile-initial.png` visibly begins with status/preview. |
| Canvas height 190–220 | PASS | Initial canvas x21, y71, width348, height219.4375; bottom290.4375. Same dimensions after real generation. |
| Preview and complete five-icon action row visible without scrolling | PASS | At initial scrollY=0, preview panel y10–304.4375; action strip y785–844; all controls y792–838. `mobile-initial.png` and `mobile-generated.png`. |
| One row, visually icon-only, minimum 44×44 targets | PASS | Five controls x21 / 91.390625 / 161.796875 / 232.1875 / 302.59375; each width66.39–66.41, height46. Text computed font-size0, pseudo-element font-size20, five visible glyphs. All centers pass actual `elementFromPoint` hit tests. |
| Accessible names retained | PASS with observation | Chromium accessibility snapshot has `▶ Generate STL`, `■ Cancel` disabled, `↻ Reset`, `⌾ Reset camera`; after generation, link `⇩ Download STL`. Before generation Download remains readable accessibility text, because the inherited disabled anchor has no href. Generated glyphs participate in names, but all explicit action wording is retained. |
| First complete Basic field visible and usable on initial load | PASS | `device length (mm)` text rectangle y371.4375–389.4375; `device_length` enabled input x21, y397.4375, width348, height46, bottom443.4375. It is unobscured, is first in keyboard Tab order, and was successfully edited through the real input. |
| No horizontal overflow/clipping | PASS at tested sizes | Mobile document scrollWidth=clientWidth=390 throughout initial, scrolled and toast states. Canvas, actions and input x21–369 lie inside viewport. Screenshots show no horizontal clipping. Desktop document widths both1440. Intentional vertical form scrolling can partially crop fields at its top/bottom. |
| Sticky use after scroll | PASS | At page scrollY112, preview panel remains y0–294.4375; action strip remains y734.4375–793.4375. Form scrollTop500 changes visible parameters while those rectangles stay fixed. Inspected `mobile-page-scroll.png` and `mobile-form-scroll.png`. |
| Toast, focus, stale/download and Diamond states | PASS for exercised paths | Invalid device_length=0 shows actionable visible alert and focuses Dismiss. Dismiss hides toast and returns focus to Generate. Reset restores208. All five surface/Diamond inputs remain disabled. Real smooth completion enables Download; changing device length to209 then shows stale and removes href with aria-disabled=true. |
| Desktop title and text labels remain | PASS | Fresh 1440×1200: header display:block, x60, y41.4375, width1320, height77.4375. Title and caption visually present in `desktop-top.png`; all five action texts remain16px and visibly readable in `desktop-actions.png`. |

The independent visual inspection covered all eight PNGs: `mobile-initial.png`, `mobile-page-scroll.png`, `mobile-form-scroll.png`, `mobile-toast.png`, `desktop-initial.png` (diagnostic scroll-retained capture), `desktop-top.png`, `desktop-actions.png`, and `mobile-generated.png`.

Real default smooth generation completed as `Complete 04109b17a9e3`, with download name `laifen-04109b17a9e394ae9bdd97d43ca4af573c48b32ecbfcff85507dc3650f380d3e.stl`. The model visibly rendered inside the compact canvas with no preview fallback, toast, or stale state. This is runtime/layout evidence only; no mesh or geometric acceptance was performed.

## Findings, limitations and next action

No blocking finding was observed in the bounded mobile-density contract. Browser page-error arrays and failed-request arrays were empty in the recorded probes. Console messages were only four repeated WebGL `GPU stall due to ReadPixels` performance warnings per probe, associated with software rendering/screenshots; no browser console errors were recorded. An exploratory executable-path lookup emitted a Playwright teardown diagnostic after printing its result; the actual context-managed validation runs both completed cleanly.

Low/informational: pseudo-element glyphs are included in computed accessible names, and the inherited disabled Download anchor is plain accessibility text until it receives an href. Explicit names are preserved. Disabled controls retain DOM/ARIA state; this validation does not assert a new visual disabled treatment or icon-comprehension study.

This is actual desktop Chromium at controlled viewports, not the user's phone/Safari or private Tailscale delivery surface. Browser chrome, on-screen keyboard, safe-area insets, zoom/text scaling and other viewport sizes were not exercised. The first-screen pass is specifically the requested 390×844 CSS viewport. No broad accessibility audit or user comprehension claim is made.

The existing VFR-09 cancellation race and Diamond HOLD remain outside this CSS candidate's acceptance. No cancellation-race retest, Diamond enabling, CAD/STEP/slicer/physical validation or deployment was performed. The separate actual-user delivery check remains required after any authorized deployment.

Next action: distinct formal review should join this local validation with independent critique, verify these exact fingerprints, and decide advancement of the mobile-only candidate. Preserve browser/geometry acceptance boundaries.

Final evidence inventory verification: `shasum -a 256 -c evidence.sha256` from the scratch evidence directory passed all21 members. The loopback server was stopped with Ctrl-C after validation (exit0); no temporary validation server remains running.
