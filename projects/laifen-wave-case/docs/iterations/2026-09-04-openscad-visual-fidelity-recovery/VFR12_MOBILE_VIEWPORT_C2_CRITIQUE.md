# VFR-12 C2 independent mobile viewport critique

Status: **BLOCKED.** C2 resolves the prior Reset camera size/centering blocker and closes the missing fresh-initial evidence at 360, 390 and 430 px. The edge-to-edge viewer, hidden mobile title/status, complete initial field, final-field clearance and desktop treatment remain healthy in the inspected evidence. C2 nevertheless introduces a new high-severity visual defect: the Generate mask is rendered black on the navy primary button, so its visible contrast is approximately 1.30:1 even though the pseudo-element's CSS box is 24 x 24 px.

Owner: `VFR12-C` / `/root/openscad_vfr11_mobile_critic`, independent critique role and distinct from implementation and validation. Candidate source, tests, manifests, implementation evidence, continuity, deployment, services and geometry were read-only. This report is the sole write.

## Provenance

Project: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`.

Iteration: `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/`.

- Candidate manifest: `candidate/VFR12_MOBILE_VIEWPORT_C2_CANDIDATE.sha256`
- Candidate manifest SHA-256: `86b208a98eff4d5fd34558de1050ccf6224593209210236a060027b9a0192bbf`
- Candidate members: 9/9 verified before critique
- Frozen input manifest: `adffc64b4e496b15a3e023c8704bb254db732c0aa62d0558994f56276e933ef4`
- C2 CSS: `6affcec90d8f88fa6a8cdf288b81e71c9770d0e930bac7628271c24f87e0971d`
- C2 focused test: `36a593d0fb268f0af56b0dfbcbcfeb30bc31e27c38ac021c208c1532a7b5d124`
- Unchanged HTML/main/schema/worker: `997c2fbc...` / `98af41e1...` / `89406233...` / `fabd1535...`
- Prior VFR-12 BLOCKED critique SHA-256: `5349b3638c3d7e65740caa9722c8cbe89d822c8cd8c2ba014920c59aa772de3c`

The C2 scratch files are not members of the frozen candidate and have no separate evidence manifest. This critique therefore records their exact hashes and treats them as implementation evidence rather than independent browser proof. The critic independently verified the frozen candidate bytes, inspected the exact screenshots and candidate CSS, and measured rendered screenshot pixels. No browser was launched and no evidence was mutated by this role.

The implementation receipt's top-level `Fingerprints` section still lists the superseded first-candidate CSS and test hashes. Its repair-cycle narrative describes C2, and the frozen C2 candidate manifest binds the current files. This is a low-severity receipt inconsistency; the manifest remains unambiguous.

## Evidence steps

1. **Fresh initial state at 360, 390 and 430 px — passes.** Each exact viewport-sized screenshot shows the viewer at the top, followed by the complete Device length label and 46 px input. This closes the previous evidence gap.

   ![VFR-12 C2 initial state at 390 px](../../../scratch/vfr12-mobile-implementation/mobile390-mask.png)

2. **Action row — camera repair passes; Generate fails.** The SVG Reset and Reset camera marks now occupy substantial, repeatable ink bounds and sit near the center of the 24 px slot. The Generate star is dark against its navy button in all three mobile screenshots.

   ![VFR-12 C2 mobile action row at 360 px](../../../scratch/vfr12-mobile-implementation/mobile360-mask.png)

3. **Final-field clearance — passes in implementation evidence.** At maximum form scroll, the Output field remains fully above the sticky actions at every mobile size, and recorded top/center/bottom hit tests return `output_mode`.

   ![VFR-12 C2 mobile action row at 430 px](../../../scratch/vfr12-mobile-implementation/mobile430-mask.png)

4. **Desktop — passes visually.** At 1440 px, the established heading, caption/status, bordered viewer card, 580 px canvas and visible action wording remain present.

   ![VFR-12 C2 desktop comparison](../../../scratch/vfr12-mobile-implementation/desktop-mask.png)

## Findings

### High — Generate icon is black on navy despite its 24 x 24 mask box

The C2 CSS gives every mobile pseudo-element `background-color:currentColor`, but each icon rule also assigns a `background-image` whose SVG path is filled black while assigning the same SVG as the mask. The painted black background image overlays the intended current-color fill inside the masked region. On the primary Generate button, whose text color is white and background is `#112233`, the actual rendered star is therefore black rather than white.

This is visible in all three screenshots. An independent pixel read of the exact Generate icon slot in `mobile390-mask.png` found 88 black pixels, 420 navy pixels and zero bright icon pixels. Black against `#112233` has an approximate WCAG relative-luminance contrast ratio of 1.30:1. The mask's computed 24 x 24 box and reported white `background-color` do not describe the final painted pixels. The user's complaint concerns the visible icon, so the primary action's nearly invisible mark blocks acceptance.

This finding does not call for visible word labels. Preserve the icon-only mobile action row and meaningful DOM wording. Remove the painted black background image or otherwise render the masked shape from `currentColor`, then verify actual screenshot pixels on the primary button.

### Resolved — Reset camera is no longer tiny or materially off-center

Independent screenshot-pixel measurements on `mobile360-mask.png`, `mobile390-mask.png` and `mobile430-mask.png` are consistent:

- Reset visible ink: 20 x 21 px, horizontal center delta 0 px, vertical center delta +1.5 px.
- Reset camera visible ink: 16 x 16 px, horizontal center delta -1.5 px, vertical center delta 0 px.

The prior candidate's Reset camera font ink was only 12 x 10 px and sat 3 px low. C2's deterministic SVG visibly and measurably resolves that specific defect. The remaining difference between the two shapes is ordinary icon geometry rather than the former tiny, low glyph failure.

### Resolved — fresh-initial responsive evidence covers all requested mobile widths

The new screenshots are exact viewport dimensions: 360 x 640, 390 x 844 and 430 x 932. `mask-measurements.json` records complete first inputs at `y=283..329`, `312.4375..358.4375` and `313..359`, respectively. The images visually agree. Unlike the prior full-page max-scroll captures, these files directly address the first-screen requirement before scrolling.

### Low — implementation evidence is not frozen and Safari delivery remains open

The screenshots and measurements identify the implementation's controlled Chromium outcome, but the candidate manifest does not bind them and this critique did not independently rerun the browser. The actual complaint came from iPhone/Safari on a private delivery surface. Safe-area behavior, dynamic browser chrome, text scaling, WebKit mask rendering and the exact privately served bundle remain unproven. These limits do not negate the inspected local layout improvements or the high Generate-icon defect.

## Requirement coverage

| User complaint or contract gate | Critique result | Evidence |
| --- | --- | --- |
| Remaining title/status removed visually on mobile | PASS locally | All three fresh initial screenshots begin with the viewer; the status remains a clipped 1 px live region at `-1,-1`, and no title/caption consumes screen height. |
| Viewer full width, edge-to-edge, borderless | PASS locally | At 360/390/430, the result and canvas span x=0 through the viewport width with heights 190/219.4375/220 px; screenshots show no outer card border or padding. |
| At least one complete field on the initial screen | PASS in fresh implementation evidence | Device length is fully visible with a 46 px input in each exact viewport-sized initial screenshot. |
| Icons are 24 px and visibly centered | **FAIL overall** | Reset camera is repaired to a visible 16 x 16 centered mark, but Generate is painted black on navy and is effectively lost despite its 24 x 24 CSS slot. |
| Compact controls and touch/disabled affordances | PASS except primary icon contrast | All five action targets are 46 px high and centered in one row; Cancel and Download remain visibly muted. Meaningful DOM action wording remains present while pseudo content is empty. |
| Sticky row does not obscure the final field | PASS in implementation evidence | Output is `y=372..416`, `605.4375..649.4375` and `694..738`; sticky actions begin at y=581, 785 and 873 for 360/390/430, with all three recorded hit-test points resolving to `output_mode`. |
| No horizontal overflow | PASS in implementation evidence | At each mobile size, `scrollWidth==clientWidth`; no lateral clipping is visible. |
| Desktop preserved | PASS visually | The 1440 px screenshot retains the heading, status/caption, card, 580 px canvas and visible text labels. |
| Runtime and geometry preserved | PASS by frozen hashes | HTML, main, schema and worker are unchanged in the 9-member candidate. This does not establish CAD, exported-artifact, slicer or physical acceptance. |

## Inspected implementation-evidence hashes

These hashes identify the unmanifested scratch files used by this critique:

| File | SHA-256 |
| --- | --- |
| `mobile360-mask.png` | `2b1deaf9610a7f3a1f35d7f7263c6ac00116065e0245c910334820bde9e31fe8` |
| `mobile390-mask.png` | `64706979cec192fb5333d8f29c0bfd7cd7bb9a935f75839a6bd13318ffd0aa5b` |
| `mobile430-mask.png` | `8b1acad410f86212bb1752cc21f30454a0748943eb084cff0c85b60818d85a89` |
| `desktop-mask.png` | `18091f4aaae06271b4c55aea9063674ba282ea3d05804b48f6e9b5cfa59dbb86` |
| `mask-measurements.json` | `f16d4bebdccc8c248aca4a3c9a235efec2dd28f1c0ad2f4fa6d9ff94ddb702c6` |

## Separate existing risks

VFR-12 C2 is a mobile presentation candidate. It does not repair or retest the existing late-result cancellation race, and public Diamond controls remain HOLD. It also does not establish Diamond assembled/print-layout browser acceptance, CAD/STEP/slicer acceptance or physical print acceptance. Those risks are separate from this primary-action icon blocker.

## Commands and evidence

Commands actually run for the decisive checks included:

```text
# cwd: projects/laifen-wave-case
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C2_CANDIDATE.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C2_CANDIDATE.sha256
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR12_MOBILE_VIEWPORT_CRITIQUE.md
shasum -a 256 scratch/vfr12-mobile-implementation/mobile360-mask.png scratch/vfr12-mobile-implementation/mobile390-mask.png scratch/vfr12-mobile-implementation/mobile430-mask.png scratch/vfr12-mobile-implementation/desktop-mask.png scratch/vfr12-mobile-implementation/mask-measurements.json
sips -g pixelWidth -g pixelHeight scratch/vfr12-mobile-implementation/mobile360-mask.png scratch/vfr12-mobile-implementation/mobile390-mask.png scratch/vfr12-mobile-implementation/mobile430-mask.png scratch/vfr12-mobile-implementation/desktop-mask.png
/opt/homebrew/bin/rg -n -C 4 "actions.*before|background-image|mask-image|mask-size|#generate|#reset-camera|Generate|Reset camera" preview/openscad-wasm-simulator/style.css preview/openscad-wasm-simulator/index.html
PYTHONDONTWRITEBYTECODE=1 uv run python -B - <<'PY'
# Pillow reads of exact screenshot crops measured Reset and Reset-camera ink bounds,
# counted Generate icon-slot colors, and computed black/#112233 contrast.
PY
```

All referenced screenshots were opened at original detail and visually inspected. No browser, source, test, manifest, evidence, continuity, service, deployment or geometry mutation occurred.

## Disposition

Do not advance this fingerprint to formal acceptance. Route the smallest icon-only CSS repair so the Generate mask actually paints from white `currentColor`; preserve the icon-only row, meaningful DOM wording, SVG geometries, order, 24 px slots, 46 px targets, disabled states, edge-to-edge layout and all other C2 gains. Refreeze the candidate and verify actual rendered icon colors at 360, 390 and 430 px. Independent validation should bind and rerun the built-bundle evidence before formal review.
