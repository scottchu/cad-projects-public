# VFR-11 independent mobile density critique

Status: **BLOCKED for the bounded mobile-density candidate.** The candidate removes the mobile page heading, materially improves first-screen density, preserves a full five-action row, and leaves the inspected desktop presentation intact. It does not yet provide a fully usable independently scrolling form at the initial 390 x 844 position, and its icon-only action meanings and disabled state are not visually clear enough to satisfy the stated affordance contract.

Owner: `VFR11-C` / `/root/openscad_vfr11_mobile_critic`, independent critique role. The implementer and validator source, manifests, evidence, services, and continuity records were read-only. This report is the sole write.

## Provenance

Project: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`.

Iteration: `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/`.

- Candidate manifest: `candidate/VFR11_MOBILE_DENSITY_CANDIDATE.sha256`
- Candidate manifest SHA-256: `dfa8ff0c1ea51daab363b48756747d7a6e26a392fa125c321d4dd4536c294077`
- Candidate members: 8/8 verified before and after critique
- Independent validation: `VFR11_MOBILE_DENSITY_VALIDATION.md`
- Validation SHA-256: `a3c4c1f344df8adccd7a0033b6cd067f65d169a4db33f4d8ada650bdedc9e5ad`
- Validation evidence inventory: `scratch/vfr11-mobile-validation/evidence.sha256`
- Evidence inventory SHA-256: `94f4e43781d444d64eb52b8243fba5bd30f5689eb25d0bb972e76229a5dfefc2`
- Evidence members: 21/21 verified

The critique visually inspected all eight supplied PNGs at their native dimensions: the five 390 x 844 mobile captures and the three 1440-wide desktop captures. It also queried the manifest-bound built page in Chromium at 390 x 844 without altering application bytes.

## Findings

### High — the sticky action strip partially covers the last form control at the initial mobile page position

The implementation makes the form independently scrollable, but its box extends behind the sticky action strip before the document itself is scrolled. At the initial 390 x 844 position (`scrollY=0`), the form occupies `y=325.4375..834.4375` while the action strip occupies `y=785..844`, an overlap of 49.4375 px.

With the form independently scrolled to its maximum while the page remains at `scrollY=0`, the final `output_mode` select occupies `y=754.4375..798.4375`. The action strip begins at `y=785`, so the lower 13.4375 px of that 44 px control is covered. A hit test five pixels above the select's bottom returns `reset`, not `output_mode`; only about 30.6 px of its height is unobscured. The control's DOM box is 44 px high, but its usable exposed touch area is not.

This is a direct failure of the 44 x 44 touch and usable sticky-scrolling requirements. The validator's `mobile-form-scroll.png` was captured only after the page had already moved to `scrollY=112`, where the form ends above the actions. That capture therefore does not exercise the conflicting state. A passing repair must keep every field fully visible and hit-testable when the form alone is scrolled from the initial page position; requiring a separate page scroll to uncover it contradicts the promised independent parameter scrolling.

### Medium — icon-only action meanings and state affordances are ambiguous

The five controls are visibly button-shaped and comfortably wide, but the glyph set is not self-explanatory enough for an unlabeled touch surface. `▶` reads primarily as media play rather than STL generation, and `⌾` does not communicate “Reset camera” without prior knowledge. The initial and generated screenshots also show the Download icon with the same outline treatment even though it changes from a disabled anchor with no `href` to an enabled download.

The underlying DOM text preserves screen-reader names, so this is not a total accessible-name failure. The controls have no explicit `aria-label` or `title`, however, and Chromium includes the generated pseudo-element glyph in names such as `▶ Generate STL` and `⌾ Reset camera`. More recognizable deterministic icons, an explicit accessible name that excludes decorative glyph speech, and a visible enabled/disabled distinction are needed while retaining the requested icon-only row.

### Low — controlled Chromium evidence does not establish the actual phone delivery surface

The evidence is strong for one headless Chromium CSS viewport, but it does not cover Safari, dynamic browser chrome, safe-area behavior, text scaling, zoom, an on-screen keyboard, or nearby mobile sizes. The action strip ends exactly at viewport bottom `y=844` in the initial capture. This is a delivery-surface acceptance gap rather than proof of a second local defect. It should be checked on the actual phone after the local overlap and affordance findings are repaired and independently revalidated.

## Passing coverage

| User complaint or requirement | Critique result | Evidence |
| --- | --- | --- |
| No space-wasting title/caption on phone | PASS | At 390 x 844 the header is `display:none` with a zero rectangle; `mobile-initial.png` begins with status and preview. |
| Compact five-action mobile row | PASS for density and presence | All five actions appear in one row; each DOM box is about 66.4 x 46 px and all action centers pass hit tests. |
| Clear action affordances | BLOCKED | Generate and Reset camera glyphs are ambiguous; disabled Download has no distinct visual treatment. |
| At least one complete field on the first screen | PASS | The complete Device length label and 348 x 46 input appear unobscured at `y=371.4375..443.4375`. Several later Basic fields are also visible. |
| Usable sticky scrolling | BLOCKED | Preview and actions remain sticky, but the action strip covers part of the form and 13.4375 px of the final select at the initial page position. |
| Touch/accessibility | BLOCKED in the overlapping state; otherwise partial PASS | Action boxes and the first field meet nominal sizing and DOM text supplies names. The final select has only about 30.6 px unobscured height at form maximum; pseudo glyphs also pollute computed names. |
| Desktop unaffected | PASS for inspected presentation | At 1440 x 1200 the title/caption remain visible, canvas remains 580 px high, and all five action labels remain visible at 16 px. No desktop visual regression is evident in the supplied captures. |
| Existing IDs, runtime, geometry, worker and Diamond disabled state | PASS for candidate preservation | All eight manifest members verify. Main, schema and worker retain their frozen hashes; the browser evidence observes all five Diamond/surface inputs disabled. |

## Separate pre-existing risks

This disposition concerns only the VFR-11 mobile CSS candidate. The VFR-09 correctly identified late-result cancellation race remains unresolved because VFR-10 restored the browser code after its repair attempt. Public Diamond enablement therefore remains HOLD independently of this critique. VFR-11 does not worsen or close that protocol defect, the missing Diamond assembled/print-layout browser gates, CAD/STEP/slicer acceptance, or physical print acceptance.

No deployment or actual-user delivery surface was inspected. Local VFR-11 acceptance would still require a distinct formal review after repair and independent reruns; any deployment would need a separate actual-phone check.

## Commands and evidence

Commands actually run for the decisive checks were:

```text
# cwd: projects/laifen-wave-case
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_CANDIDATE.sha256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR11_MOBILE_DENSITY_VALIDATION.md scratch/vfr11-mobile-validation/evidence.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_CANDIDATE.sha256

# cwd: projects/laifen-wave-case/scratch/vfr11-mobile-validation
shasum -a 256 -c evidence.sha256
sips -g pixelWidth -g pixelHeight mobile-initial.png mobile-page-scroll.png mobile-form-scroll.png mobile-toast.png mobile-generated.png desktop-top.png desktop-actions.png desktop-initial.png

# cwd: repository root
uv run python -m http.server 8767 --bind 127.0.0.1 --directory projects/laifen-wave-case/scratch/vfr11-mobile-validation/dist
PYTHONDONTWRITEBYTECODE=1 uv run python -B - <<'PY'
from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width":390,"height":844}, device_scale_factor=1)
    page.goto("http://127.0.0.1:8767/", wait_until="networkidle")
    def rect(sel):
        return page.locator(sel).evaluate("""e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,top:r.top,bottom:r.bottom,left:r.left,right:r.right}}""")
    initial = {
        "scrollY": page.evaluate("scrollY"),
        "form": rect("#controls"),
        "actions": rect(".actions"),
        "output": rect("#output_mode"),
        "formScrollTop": page.locator("#controls").evaluate("e=>e.scrollTop"),
        "formScrollMax": page.locator("#controls").evaluate("e=>e.scrollHeight-e.clientHeight"),
    }
    page.locator("#controls").evaluate("e=>e.scrollTop=e.scrollHeight")
    final = {
        "scrollY": page.evaluate("scrollY"),
        "form": rect("#controls"),
        "actions": rect(".actions"),
        "output": rect("#output_mode"),
        "formScrollTop": page.locator("#controls").evaluate("e=>e.scrollTop"),
        "formScrollMax": page.locator("#controls").evaluate("e=>e.scrollHeight-e.clientHeight"),
        "outputCenterHit": page.locator("#output_mode").evaluate("""e=>{const r=e.getBoundingClientRect();const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return h&&h.id}"""),
        "outputTopHit": page.locator("#output_mode").evaluate("""e=>{const r=e.getBoundingClientRect();const h=document.elementFromPoint(r.left+r.width/2,r.top+5);return h&&h.id}"""),
        "outputBottomHit": page.locator("#output_mode").evaluate("""e=>{const r=e.getBoundingClientRect();const h=document.elementFromPoint(r.left+r.width/2,r.bottom-5);return h&&h.id}"""),
    }
    page.locator("#output_mode").scroll_into_view_if_needed()
    afterScrollIntoView = {
        "scrollY": page.evaluate("scrollY"),
        "formScrollTop": page.locator("#controls").evaluate("e=>e.scrollTop"),
        "output": rect("#output_mode"),
        "actions": rect(".actions"),
        "centerHit": page.locator("#output_mode").evaluate("""e=>{const r=e.getBoundingClientRect();const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return h&&h.id}"""),
    }
    explicit = page.locator(".actions > *").evaluate_all("""els=>els.map(e=>({id:e.id,title:e.getAttribute('title'),ariaLabel:e.getAttribute('aria-label'),text:e.textContent}))""")
    print(json.dumps({"initial":initial,"formMaxAtPageTop":final,"afterScrollIntoView":afterScrollIntoView,"explicitNames":explicit},indent=2))
    browser.close()
PY
```

The temporary loopback server was stopped with Ctrl-C and exited 0. The focused probe reproduced the overlap without source changes, injected CSS, mocks, screenshots, or evidence-file writes.

## Disposition

Do not advance this fingerprint to formal acceptance. Route one small CSS/icon repair that (1) reserves enough non-overlapped space for the final form control at every form scroll position, (2) preserves the compact one-row mobile actions and first-screen field, and (3) gives each icon a visually unambiguous meaning and distinct disabled state while keeping clean explicit accessible names. Refreeze the changed candidate and rerun the initial-page/form-maximum hit test, the existing 390 x 844 screenshots and interactions, nearby mobile viewport checks, desktop preservation, and independent critique/validation.
