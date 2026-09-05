# VFR-11 C2 independent mobile density critique

Status: **PASS for the bounded local C2 mobile-density candidate.** The prior form/action overlap is resolved at the exact failing 390 x 844 state, disabled controls now have a clear visual state, the icon-only toolbar matches the user's explicit density request, accessible action wording remains meaningful, and the inspected desktop layout remains usable. Actual-phone delivery acceptance and the separate Diamond/cancellation HOLD remain open.

Owner: `VFR11-C` / `/root/openscad_vfr11_mobile_critic`, independent critique role. The C2 candidate, implementation, validation, tests, evidence, continuity records, services, deployment and geometry were read-only. This report is the sole write.

## Provenance

Project: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`.

Iteration: `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/`.

- Candidate manifest: `candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256`
- Candidate manifest SHA-256: `ad7c14d9f40f354c70cbaf0394b89a9a03f795ec9e4d767c55c263096f054968`
- Candidate members: 8/8 verified before critique
- Independent validation: `VFR11_MOBILE_DENSITY_C2_VALIDATION.md`
- Validation SHA-256: `367e0c351c35562ef43931de48c93c07bc09bec0c51c1d79c3dbf4f5a2210574`
- Validation evidence: `scratch/vfr11-mobile-c2-validation/evidence.sha256`
- Evidence manifest SHA-256: `58c9e14211b610a6be670cbbfad998485da6e911690270371a54a26c83e17ed7`
- Evidence members: 22/22 verified

The critique inspected the nine manifest-bound C2 screenshots at native dimensions: six 390 x 844 mobile captures and three 1440-wide desktop captures. Browser measurements and accessibility snapshots came from the exact built bundle bound by the evidence inventory.

## Evidence steps

1. **Initial mobile surface — healthy.** The title and explanatory caption are absent, the status and 219.4375 px preview begin at the top of project content, the complete Device length field is visible, and the five icon actions fit in one row.

   ![Initial 390 x 844 mobile surface](../../../scratch/vfr11-mobile-c2-validation/mobile-initial.png)

2. **Form maximum at the initial page position — healthy.** With document `scrollY=0` and the form at its maximum scroll, the final Output select is completely visible above the action strip.

   ![Final Output field above the sticky actions](../../../scratch/vfr11-mobile-c2-validation/mobile-final-field.png)

3. **Generated/action state — healthy.** Generate remains the visually dominant action, Cancel remains visibly disabled, and Download becomes visibly enabled after a real smooth result.

   ![Generated mobile state with enabled Download](../../../scratch/vfr11-mobile-c2-validation/mobile-generated.png)

4. **Error recovery — healthy within the inherited contract.** The actionable toast is readable, its Dismiss target is visible, and the recorded interaction returns focus to Generate after dismissal.

   ![Mobile actionable error toast](../../../scratch/vfr11-mobile-c2-validation/mobile-toast.png)

5. **Desktop preservation — healthy.** The title, caption, 580 px canvas and visible text action labels remain in their established desktop layout. Disabled Cancel and Download are now intentionally muted without reflow.

   ![Desktop action and layout state](../../../scratch/vfr11-mobile-c2-validation/desktop-actions.png)

## Findings

No High or Medium finding remains within the frozen C2 scope.

### Resolved — prior High overlap and touch-target failure

The C1 critique found the final 44 px `output_mode` select partly covered by the sticky action strip. C2 reserves form-end scroll space. At the same formerly failing state, the select is `y=690.4375..734.4375`, the action strip begins at `y=785`, and the clearance is 50.5625 px. Hit tests at top+1, center and bottom-1 all return `output_mode`. The form can reach its last field without moving the page, and the complete 44 px control remains usable.

### Resolved — disabled action states

Initial Cancel and Download use opacity `0.46`, grayscale, muted foreground `rgb(100,112,123)`, background `rgb(238,241,244)` and border `rgb(197,205,213)`. Enabled actions use opacity `1` with no grayscale. The initial and generated screenshots visibly distinguish Download before and after it receives a valid `href`; Cancel stays muted. This closes the prior state-affordance defect.

### Low — icon comprehension remains a qualitative delivery question

The toolbar meets the explicit icon-only request: five large, bordered targets stay in one row, Generate is primary, unavailable actions are muted, and the glyphs are visibly distinct as `✦`, `■`, `↻`, `⟳` and `⇩`. Requiring visible word labels would contradict the user's requested mobile treatment.

The two circular-arrow glyphs still require some learning to distinguish Reset from Reset camera, and `✦` communicates creation more generally than “Generate STL.” This is not a local blocker because the adjacent actions retain stable positions and the accessibility tree preserves the explicit wording `Generate STL`, `Cancel`, `Reset`, `Reset camera` and `Download STL`. The pseudo-element glyphs prefix those names, but the operative wording is intact and meaningful. A real user check on the delivered phone remains the correct gate for icon comprehension; the local screenshots alone cannot prove it.

### Low — actual-phone and responsive-edge evidence remains open

The C2 browser evidence is controlled Chromium at 390 x 844. It does not cover Safari, dynamic browser chrome, safe-area behavior, text scaling, zoom, an on-screen keyboard or nearby mobile widths/heights. The action strip still ends at viewport bottom in the controlled capture. This is a delivery-surface limitation, not evidence of a C2 layout defect.

## Requirement coverage

| User complaint or requirement | Critique result | Evidence |
| --- | --- | --- |
| Remove space-wasting title/caption on phone | PASS | Header is `display:none` with zero geometry; initial screenshot begins with status/preview. |
| One compact icon-only action row | PASS | Five controls remain in one 348 px row; each is about 66.4 x 46 px. |
| Clear action affordances | PASS with Low comprehension caveat | Primary, enabled and disabled states are visually distinct; glyph meanings are supported by stable placement and explicit accessible wording. Actual user recognition remains a delivery check. |
| At least one complete field on first screen | PASS | Device length label/input are completely visible at `y=371.4375..443.4375`; input is 348 x 46 px and hit-testable. |
| Usable sticky scrolling | PASS | Final select is completely exposed and hit-testable at form maximum with page `scrollY=0`; preview/actions remain sticky in the recorded scroll states. |
| Touch and accessibility | PASS for bounded evidence | Five actions are about 66.4 x 46 px; final select retains all 44 px; keyboard/focus recovery passes; explicit action words remain in computed names. No broad WCAG or actual touch-device claim is made. |
| Desktop unaffected | PASS for behavior/layout | Title/caption, two-column layout, 580 px canvas and 16 px text labels remain. Intentional disabled styling changes pixels but does not alter desktop structure or behavior. |
| Existing IDs/runtime/geometry/Diamond state | PASS for preservation | Candidate verifies 8/8; HTML/main/schema/worker retain their frozen hashes and all five surface/Diamond controls remain disabled. |

## Separate pre-existing risks

This PASS applies only to the C2 mobile-density candidate. The VFR-09 correctly identified late-result cancellation race remains unresolved because VFR-10 restored its browser code after the bounded repair attempt. Public Diamond enablement remains HOLD independently. C2 does not close the missing Diamond assembled/print-layout browser gates, CAD/STEP/slicer validation, physical print acceptance or actual delivered-phone acceptance.

## Commands and evidence

Commands actually run for the decisive checks were:

```text
# cwd: projects/laifen-wave-case
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR11_MOBILE_DENSITY_C2_VALIDATION.md scratch/vfr11-mobile-c2-validation/evidence.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256

# cwd: projects/laifen-wave-case/scratch/vfr11-mobile-c2-validation
shasum -a 256 -c evidence.sha256
sips -g pixelWidth -g pixelHeight mobile-initial.png mobile-final-field.png mobile-form-scroll.png mobile-page-scroll.png mobile-toast.png mobile-generated.png desktop-top.png desktop-actions.png desktop-initial.png
jq '.runs.mobile_form_max_page_top' measurements.json
jq '.actionStyles' measurements.json
jq '{errors,failedRequests,desktop_top,initialHitTests,tabOrder,generated,generatedAccessibility,generatedThenEdit}' supplement.json
```

The exact PNGs were opened and visually inspected. No local browser rerun was needed because the manifest-bound C2 evidence directly exercises the prior failing state, records top/center/bottom hit tests, captures the resulting screen, and verifies the built candidate. No source, test, manifest, evidence, service or deployment mutation occurred.

## Disposition

Advance this exact local C2 fingerprint to the distinct formal review join. The reviewer should preserve the Low icon-comprehension and actual-phone limitations as delivery checks rather than reintroducing mobile word labels. Any later source change must refreeze the candidate and rerun the affected layout, state, accessibility and desktop gates.
