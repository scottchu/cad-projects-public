# VFR-11 C2 independent delivery verification

Status: **PASS on the exact private HTTPS route in real Chromium.** Live bytes match the approved build and the mobile/desktop delivery checks pass. Actual-user Safari/phone acceptance remains pending.

Owner: `VFR11-V` / `/root/openscad_vfr11_mobile_validator`, independent delivery validator. Project: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`. Only this report and `scratch/vfr11-mobile-delivery-c2/validation/` were written. No live files, source, tests, manifests outside that validation namespace, continuity, services, Tailscale configuration or CAD were changed.

Exact tested route: <https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/>.

## Verified provenance

- Approved C2 candidate: `candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256`, SHA-256 `ad7c14d9f40f354c70cbaf0394b89a9a03f795ec9e4d767c55c263096f054968`; all eight members verified unchanged after delivery probes.
- Formal review: `VFR11_MOBILE_DENSITY_FORMAL_REVIEW.md`, full verified SHA-256 `9f3558cff2d5bf6c6aad6149f306eeba6c5e27bf701ddb5e5b4602f5ef36ac2b`. The coordinator's initial delivery assignment omitted the final `b`; the full disk hash was reported back before browser checks.
- Deployed build inventory: `scratch/vfr11-mobile-delivery-c2/build.sha256`, SHA-256 `f6c9cb82f161567f57c26447b5d7494286a308cda92a3fb11b44296e458afc90`; all six local build members verified.
- Delivery evidence: `scratch/vfr11-mobile-delivery-c2/validation/evidence.sha256`, SHA-256 `e21a9783d5a196e01b99c4a893ea733fdc4261249f0a41a70cfbc26a758c5fe9`, binding 24 files: downloaded live assets/root HTML, asset report, probe scripts, browser logs/measurements, screenshots and actual downloaded STL.

Root reported deploying to `scratch/presentation/openscad-simulator` with recoverable sibling backup `openscad-simulator.pre-vfr11-c2-1788576619`. This validator did not alter either location. Acceptance below is based on observed HTTPS bytes and browser behavior, not that report alone.

## HTTPS byte and MIME checks

`curl` used normal TLS verification, without `-k`. All six manifest assets returned HTTP 200 with expected MIME and exact SHA-256 equality to the supplied build; detailed per-URL expected/actual hashes are in `validation/https-assets.json`. The bare route also returned HTTP 200 text/html with the same index hash.

| Live relative path | MIME | Verified SHA-256 |
|---|---|---|
| `index.html` and route `/` | text/html | `c3c51bd393ded8b671c97527023aef2290f27f987b640e1f9b01af71f5c3693c` |
| `assets/index-BB109KGL.js` | text/javascript | `b06d5c28972d004bc9121cb3a2b09d94fb85369b6d268d9478e3ff13d12a40ca` |
| `assets/index-BBglacgV.css` | text/css | `862a576c8ca260c53460d5adb909c3cdef00abbd7aecef20c7be7753e743d732` |
| `assets/openscad.worker-Csx1v_-i.js` | text/javascript | `cf543214d381e56ac230d6853810786ae70c52977d408e64695db595574fd46e` |
| `assets/openscad-CutNEzGH.js` | text/javascript | `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` |
| `assets/openscad-DIKIGOy4.wasm` | application/wasm | `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26` |

The browser independently recorded HTTP 200 for its root, main, CSS, worker, runtime and WASM requests on the exact HTTPS origin. No localhost replacement, certificate bypass, CSS injection or mocked compiler was used.

## Browser gates

Chromium 151.0.7922.34, headless with software WebGL, device scale factor 1. Mobile viewport 390×844; fresh desktop viewport 1440×1200. Exact rectangles, styles, accessibility snapshots, hit tests, network responses and state outcomes are in `validation/measurements.json` and `validation/supplement.json`.

| Gate | Result and direct evidence |
|---|---|
| Mobile title/caption absent | PASS: header display:none and zero rectangle; status/preview begin project content. |
| Mobile canvas 190–220 | PASS: x21, y71, width348, height219.4375; visually present. |
| Complete first Basic field initially visible | PASS at page scrollY 0: label y371.4375–389.4375, input y397.4375–443.4375, width348, height46. Input center hit succeeds; it receives first Tab focus and accepts edits. |
| Five icon-only actions, single row, minimum 44×44 | PASS: actions y785–844; each target approximately 66.4×46 at y792–838, text font-size0 and rendered 20px glyph. Every action center is hit-testable. |
| Final Output select unobscured at form maximum | PASS with page scrollY 0 and form scrollTop=max 2551: select y690.4375–734.4375, width348, height44; 50.5625px clear of action top 785. Top+1/center/bottom−1 hit tests all return `output_mode`. |
| Disabled visuals | PASS: initial Cancel/Download visibly muted with opacity 0.46/grayscale; generated Download visibly becomes enabled. |
| Accessible action wording | PASS for reviewed contract: meaningful DOM action words remain in accessibility names. Glyph prefixes remain as formally accepted Low follow-up; no glyph-free-name claim. |
| Sticky use and no horizontal overflow | PASS: at document scroll 120 and form scroll 500 preview remains at top and actions y785–844; document scrollWidth=clientWidth=390 throughout tested mobile states. All action/input x extents fit 21–369. |
| Toast/focus/reset | PASS: invalid length 0 exposes actionable alert and focuses Dismiss; dismissal returns focus to Generate; Reset restores 208. |
| Real generation/preview/download | PASS: smooth result `Complete 04109b17a9e3`, no preview fallback/toast/stale. Model visibly renders. Clicking Download saves an STL successfully. |
| Subsequent stale handling/Diamond | PASS: edit length 209 shows stale, removes download href and sets aria-disabled=true. All five surface/Diamond controls remain disabled. |
| Desktop title/text | PASS: fresh header x60/y41.4375/1320×77.4375 is visible; title/caption remain; canvas 580px; all five action labels 16px and readable. Desktop document width 1440 has no overflow. |

Actual saved download: `validation/smooth-download.stl`, 12,160,971 bytes, SHA-256 `b1b9db18e21cafed5237afb90e57831b72246c6ac2e4b4c88f736738fd0cf169`; suggested filename `laifen-04109b17a9e394ae9bdd97d43ca4af573c48b32ecbfcff85507dc3650f380d3e.stl`; Playwright download failure was null. This verifies the download flow and artifact receipt only, not mesh/CAD acceptance.

Screenshots independently opened and visually inspected: `mobile-initial.png`, `mobile-final-field.png`, `mobile-form-scroll.png`, `mobile-toast.png`, `mobile-generated.png`, `desktop-top.png`, `desktop-actions.png`, all beneath the validation directory. They substantiate the named gates. `desktop-initial.png` retains a reused-page scroll offset and is diagnostic; fresh `desktop-top.png` supplies initial-header evidence. `mobile-page-scroll.png` is also retained with numerical sticky evidence.

Both real-browser probes completed with no page errors, no console errors and no failed network requests. Recorded response statuses are all 200. The only console messages are software-rendering `GPU stall due to ReadPixels` performance warnings, four per probe.

## Commands actually run

Unless marked project cwd, commands ran from `/Users/scottchu/.codex/worktrees/4f8c/design-projects`.

```text
shasum -a 256 projects/laifen-wave-case/scratch/vfr11-mobile-delivery-c2/build.sha256
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR11_MOBILE_DENSITY_FORMAL_REVIEW.md
shasum -a 256 -c projects/laifen-wave-case/scratch/vfr11-mobile-delivery-c2/build.sha256
uv run python projects/laifen-wave-case/scratch/vfr11-mobile-delivery-c2/validation/validate.py > projects/laifen-wave-case/scratch/vfr11-mobile-delivery-c2/validation/browser-output.log 2>&1
uv run python projects/laifen-wave-case/scratch/vfr11-mobile-delivery-c2/validation/supplement.py > projects/laifen-wave-case/scratch/vfr11-mobile-delivery-c2/validation/supplement-output.log 2>&1
curl --fail --silent --show-error --max-time 30 --output projects/laifen-wave-case/scratch/vfr11-mobile-delivery-c2/validation/served-route.html --write-out '%{http_code} %{content_type}' https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/
# project cwd
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256
```

An inline `uv run python` asset-verification command iterated the six exact build-manifest paths. For each it ran `curl --fail --silent --show-error --max-time 30 --output <validation/served/relative-path> --write-out '%{http_code} %{content_type}' <exact-HTTPS-route/relative-path>`, computed SHA-256 using hashlib, compared with the manifest, recorded results in `https-assets.json`, and asserted all statuses/hashes matched. All commands exited 0. No build, test-suite repetition or service change was necessary during this delivery validation because exact approved bytes were being checked.

## Limits and next action

This PASS establishes actual private-route delivery and functioning Chromium at the specified viewports. It does not establish the user's Safari experience, dynamic browser chrome/safe areas, keyboard behavior, other zoom/text sizes, nearby viewport sizes or icon comprehension. The user still needs to confirm the first screen and controls on their actual phone; meaningful action wording is retained but decorative glyphs remain in accessible names.

Existing Diamond public enablement/cancellation-race HOLD, CAD/STEP/mesh/slicer and physical acceptance remain separate and unchanged. Root can record the verified private-route delivery and request actual-phone user feedback without claiming those unrelated gates passed.

Final evidence verification: `shasum -a 256 -c evidence.sha256` from the delivery validation directory passed all 24 members.
