# VFR-12 C3 independent mobile viewport critique

Status: **PASS.** The final C3 repair resolves the C2 color blocker and the remaining painted-size/alignment failures. Actual screenshot pixels at 360, 390 and 430 px show five substantial, centered marks; Generate is now white on navy. The edge-to-edge viewer, removed mobile title/status, complete initial field, final-field clearance, touch/disabled states and desktop presentation remain intact in the inspected evidence. No material critique finding blocks independent C3 validation and formal review.

Owner: `VFR12-C` / `/root/openscad_vfr11_mobile_critic`, independent critique role and distinct from implementation and validation. Candidate source, tests, manifests, implementation evidence, continuity, deployment, services and geometry were read-only. This report is the sole write.

## Provenance

Project: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`.

Iteration: `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/`.

- Candidate manifest: `candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256`
- Candidate manifest SHA-256: `2a58f483d2ba653c7e3c7de747bec8466837dd7f46ee4cd493ef9e8b61199433`
- Candidate members: 9/9 verified before critique
- Frozen input manifest: `adffc64b4e496b15a3e023c8704bb254db732c0aa62d0558994f56276e933ef4`
- C3 implementation receipt: `41eff4fcdcd8628451387d1836fd4559ade1907e889b2216a0247c699e4ce1f8`
- C3 CSS: `b530ae8870b5b2c0eb9548192edeb96fb122860ead203eb1295bd9ebb3893114`
- C3 focused test: `bf9ee06d1d3648f9d0fcec27c626f50a8d501db0395d9f071d86a1808b28a79c`
- Unchanged HTML/main/schema/worker: `997c2fbc...` / `98af41e1...` / `89406233...` / `fabd1535...`
- Prior C2 independent validation SHA-256: `9ebade4791521344d97e5995182e6e591ac566be8a231b1fe2e617767ce83628`
- Prior C2 independent critique SHA-256: `576b9d5badda8d6dd8981db4780faad54f109de9b020e23163c30df26af96550`

The original iPhone screenshot was reopened at original detail. It shows the rejected visible ready-status sentence, inset bordered viewer card and tiny action marks. The C3 screenshots were also opened at original detail and compared against those complaints.

The C3 scratch files are not candidate-manifest members and have no independent evidence manifest. This critique records their exact hashes and treats them as implementation evidence rather than an independent browser rerun. The critic independently verified the frozen candidate bytes, inspected the exact candidate CSS and screenshots, and measured final screenshot pixels without modifying the evidence.

## Evidence steps

1. **Original user surface.** The phone screenshot shows the ready sentence and padded viewer card consuming vertical and horizontal space, with small action marks at the bottom.

2. **C3 mobile initial states at 360, 390 and 430 px — pass.** Each exact viewport-sized image starts with the viewer at x=0/y=0, contains no visible title/status/card frame, and shows a complete Device length label and 46 px input below the viewer.

   ![VFR-12 C3 at 390 px](../../../scratch/vfr12-mobile-implementation/final-390.png)

3. **C3 action row — pass.** The Generate star is visibly white on navy. Cancel and Download are larger but remain distinctly disabled. Reset and Reset camera are substantial circular-arrow marks with stable optical centering across all three widths.

   ![VFR-12 C3 at 360 px](../../../scratch/vfr12-mobile-implementation/final-360.png)

   ![VFR-12 C3 at 430 px](../../../scratch/vfr12-mobile-implementation/final-430.png)

4. **Desktop — pass.** The heading, explanatory caption, visible ready status, bordered viewer card, 580 px canvas and word-labelled actions remain in the desktop treatment. `final-desktop.png` is byte-identical to the previously inspected C2 desktop comparison.

   ![VFR-12 C3 desktop comparison](../../../scratch/vfr12-mobile-implementation/final-desktop.png)

## Findings

### Resolved — C2 black-on-navy Generate regression

The exact C3 CSS contains no `background-image` declaration. Each mark is painted only by `background-color:currentColor` through matching standard and prefixed SVG masks. The final screenshots confirm the result rather than relying on computed CSS alone: within the 390 px Generate icon slot, the dominant icon color includes 88 pure-white pixels and the surrounding navy remains RGB(17,34,51). The former black star is gone. The same white mark repeats at 360 and 430 px.

### Resolved — painted marks meet the assigned size and centering gate

Independent pixel reads of the final PNGs reproduce stable bounds at all three widths:

| Action | Painted bounds | Optical center delta x/y | Critique |
| --- | ---: | ---: | --- |
| Generate | 22 x 22 px | approximately -0.20 / 0 px | Pass; white mark is clear on navy. |
| Cancel | 20 x 20 px | approximately +0.41 / 0 px | Pass; enlarged and visibly disabled. |
| Reset | 21 x 21 px | approximately +0.51 / +0.5 px | Pass; former low placement is corrected. |
| Reset camera | 19 x 19 px | approximately -0.89 / +0.5 px | Pass; former tiny mark is now substantial and centered. |
| Download | 20 x 20 px | approximately +0.20 / 0 px | Pass; enlarged and visibly disabled. |

Every painted mark exceeds the 18 x 18 px minimum, and every center delta remains within 1 px. The result also passes visual inspection: the row reads as five deliberately sized controls rather than mixed font glyphs. These are visible-pixel results, not merely 24 x 24 CSS-box results.

### No regression — mobile density, scrolling and desktop presentation

`final-measurements.json` reports the viewer/result at x=0 through the entire 360/390/430 px viewport, with heights 190/219.4375/220 px, zero horizontal overflow and the status retained as a clipped 1 x 1 live region. Complete first inputs occupy `y=283..329`, `312.4375..358.4375` and `313..359`.

At maximum form scroll, Output remains fully above the sticky row: `y=372..416` versus actions y=581 at 360; `605.4375..649.4375` versus y=785 at 390; and `694..738` versus y=873 at 430. All recorded top/center/bottom hit tests resolve to `output_mode`. All five action targets are 46 px high and remain in one row.

Desktop remains unchanged visually. The final desktop screenshot's byte identity with C2 strengthens the comparison, while the unchanged HTML/main/schema/worker hashes preserve runtime and geometry inputs.

### Informational — icon comprehension and actual Safari delivery are still external limits

Reset and Reset camera use distinct circular-arrow silhouettes, but their comprehension has not been tested with the user. The requested mobile surface is explicitly icon-only, so this critique does not demand visible word labels. Empty pseudo content leaves the meaningful DOM wording — Generate STL, Cancel, Reset, Reset camera and Download STL — available as the accessible-name source.

The screenshots and measurements come from controlled Chromium. Actual iPhone/Safari behavior, browser safe areas, dynamic chrome, text scaling, WebKit rendering and the exact privately served bundle remain delivery-surface checks. These are not grounds for another CSS repair in this critique.

## Requirement coverage

| User complaint or contract gate | Critique result | Evidence |
| --- | --- | --- |
| Remaining title/status removed visually on mobile | PASS locally | Header is absent and the status is clipped to a 1 x 1 live region; no title or sentence consumes the viewport in any final mobile screenshot. |
| Viewer full width, edge-to-edge, borderless | PASS locally | Result/canvas span x=0 through 360/390/430 with no visible card border, radius or gutter. |
| At least one complete field on the first screen | PASS in fresh implementation evidence | Device length and its full 46 px input are visible at all three exact viewport sizes. |
| Icons are substantial and centered | PASS | All five marks are 19–22 px in both dimensions and remain within 1 px of their target centers across 360/390/430. |
| Generate and enabled icon color | PASS | Generate contains white pixels on navy; enabled Reset/Reset camera paint navy on white. No `background-image` remains. |
| Compact controls and disabled/touch affordances | PASS locally | Five 46 px-high targets remain in one row; Cancel and Download are visibly muted while enabled controls remain distinct. |
| Sticky row does not obscure the final field | PASS in implementation evidence | Output has 135–165 px vertical separation from the action-row start, and all recorded select hit tests pass. |
| No horizontal overflow | PASS in implementation evidence | `scrollWidth==clientWidth` at all three mobile widths. |
| Desktop preserved | PASS visually | Desktop screenshot retains the prior heading/status/card/580 px viewer/text actions and is byte-identical to the C2 desktop evidence. |
| Runtime and geometry preserved | PASS by frozen hashes | HTML, main, schema and worker are unchanged in the 9-member candidate. No CAD, exported-artifact, slicer or physical acceptance follows. |

## Inspected implementation-evidence hashes

These hashes identify the unmanifested scratch files used by this critique:

| File | SHA-256 |
| --- | --- |
| `final-360.png` | `a8b805b5a9921c8da67b453c876bf587c29fe85e04dbea6b74744be7c4b40eeb` |
| `final-390.png` | `d946ad286905ac86951dc87489930a70ac6763267ec8282e3e6d5e7b39b5a5a6` |
| `final-430.png` | `c9f7d20ac690565b3249b4d2113482dd2d6d8a0c80d988dba97db564468caa08` |
| `final-desktop.png` | `18091f4aaae06271b4c55aea9063674ba282ea3d05804b48f6e9b5cfa59dbb86` |
| `final-measurements.json` | `76b88221a4b9833851c6c8925a2f8eedbedc88eaa1892e96cd7ea99fdd63eb58` |

## Separate existing risks

VFR-12 C3 changes mobile presentation only. It does not repair or retest the existing late-result cancellation race, and public Diamond controls remain HOLD. It also does not establish Diamond assembled/print-layout browser acceptance, CAD/STEP/slicer acceptance or physical print acceptance. These risks are separate from this passing mobile viewport critique.

## Commands and evidence

Commands actually run for the decisive checks included:

```text
# cwd: projects/laifen-wave-case
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR12_MOBILE_VIEWPORT_C2_VALIDATION.md docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR12_MOBILE_VIEWPORT_C2_CRITIQUE.md
shasum -a 256 scratch/vfr12-mobile-implementation/final-360.png scratch/vfr12-mobile-implementation/final-390.png scratch/vfr12-mobile-implementation/final-430.png scratch/vfr12-mobile-implementation/final-desktop.png scratch/vfr12-mobile-implementation/final-measurements.json
sips -g pixelWidth -g pixelHeight scratch/vfr12-mobile-implementation/final-360.png scratch/vfr12-mobile-implementation/final-390.png scratch/vfr12-mobile-implementation/final-430.png scratch/vfr12-mobile-implementation/final-desktop.png
/opt/homebrew/bin/rg -n -C 5 "Repair cycle 2|C3|background-image|mask-image|mask-size|mobile.*final|final" docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR12_MOBILE_VIEWPORT_IMPLEMENTATION.md preview/openscad-wasm-simulator/style.css
/opt/homebrew/bin/rg -n "background-image" preview/openscad-wasm-simulator/style.css
PYTHONDONTWRITEBYTECODE=1 uv run python -B - <<'PY'
# Pillow reads of exact 24 x 24 screenshot slots measured each painted bound,
# optical-center delta and dominant rendered colors at 360, 390 and 430 px.
PY
```

The no-match `background-image` search exited 1 as expected. The original phone screenshot and all final implementation screenshots were opened at original detail and visually inspected. No browser, source, test, manifest, evidence, continuity, service, deployment or geometry mutation occurred.

## Disposition and final repair ceiling

This critique passes the exact C3 fingerprint to matching independent validation and formal review. VFR-12 has consumed its initial implementation plus both allowed focused repair cycles. No further VFR-12 implementation repair remains within the frozen task ceiling. If matching validation or formal review discovers a new material defect, stop and reopen or supersede the task rather than silently creating C4. Actual iPhone/Safari/private-route inspection remains the V12-08 delivery gate after formal approval.
