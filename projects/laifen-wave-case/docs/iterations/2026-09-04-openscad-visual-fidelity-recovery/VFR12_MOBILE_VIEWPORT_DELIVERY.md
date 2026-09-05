# VFR12 C3 private delivery validation

Status: **PASS — exact private HTTPS delivery in Chromium**. Actual user Safari acceptance remains pending. Validator: VFR12-V (`/root/openscad_vfr11_mobile_validator`), independent of implementation, critique, formal review, and deployment. Validation date: 2026-09-05.

## Immutable chain and scope

- Approved candidate: `candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256`, SHA-256 `2a58f483d2ba653c7e3c7de747bec8466837dd7f46ee4cd493ef9e8b61199433`; 9/9 members reverified.
- Formal PASS: `VFR12_MOBILE_VIEWPORT_FORMAL_REVIEW.md`, SHA-256 `20d3d88b843c0529110691a66c229dd40c4f496d2cfb957904d860e054d7e8fe`, verified.
- Project-relative build manifest: `scratch/vfr12-mobile-delivery-c3/build.sha256`, SHA-256 `1eef2a2157c2dec7f22e45cc474bdb167c7127307a93b57333cb8851688761b2`, verified; 6/6 local build members match.
- Exact browser and curl URL: `https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/`.
- Parent-deployed directory: `scratch/presentation/openscad-simulator`; parent-reported recoverable backup: `scratch/presentation/openscad-simulator.pre-vfr12-c3-1788582054`. Validator made no deployment or service changes.
- Writes limited to this report and `scratch/vfr12-mobile-delivery-c3/validation/` (abbreviated **E/** below). No source, tests, continuity, live files, manifests supplied by parent, Tailscale, services, or CAD edits.

## Exact delivery and execution evidence

Normal TLS verification was retained. Each build member was fetched with curl to E/served/; `https-assets.json` records exact URLs, HTTP/MIME, expected and actual SHA-256, exit status, and errors. All six returned HTTP 200, curl exit 0, empty errors, and matching bytes:

| Served member | MIME | SHA-256 |
| --- | --- | --- |
| index.html | text/html | `53210be5e3b21a509c449261c69a271619f6ce0475a32a6eff90af70098b30bb` |
| assets/index-BhzfQkbi.js | text/javascript | `b06d5c28972d004bc9121cb3a2b09d94fb85369b6d268d9478e3ff13d12a40ca` |
| assets/index-Bpj16hNa.css | text/css | `4e463043db2ac4a2bb5d1a97205aa5ab8e60b44df0afe4d589f134e92524b367` |
| assets/openscad-CutNEzGH.js | text/javascript | `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` |
| assets/openscad-DIKIGOy4.wasm | application/wasm | `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26` |
| assets/openscad.worker-Csx1v_-i.js | text/javascript | `cf543214d381e56ac230d6853810786ae70c52977d408e64695db595574fd46e` |

The exact directory route was separately fetched as E/served-route.html: HTTP 200 text/html, identical to index.html. Fresh browser sessions used the exact HTTPS route, not local files, loopback, request mocks, or modified styles. Chromium `151.0.7922.34`, Playwright through root `uv run`, device scale factor 1, headless with `--enable-unsafe-swiftshader`.

Commands executed from repository root unless noted:

```sh
shasum -a 256 projects/laifen-wave-case/scratch/vfr12-mobile-delivery-c3/build.sha256
shasum -a 256 -c projects/laifen-wave-case/scratch/vfr12-mobile-delivery-c3/build.sha256
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-delivery-c3/validation/viewport.py
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-delivery-c3/validation/states.py
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-delivery-c3/validation/measure_ink.py
shasum -a 256 -c projects/laifen-wave-case/scratch/vfr12-mobile-delivery-c3/validation/evidence.sha256
```

All listed checks exited 0; evidence manifest 34/34 OK. Browser command stdout is retained in `viewport-output.log`, `states-output.log`, and `ink-output.log`. Curl was invoked by a root `uv run python` loop over the six frozen build entries; its per-request results and fetched bytes are retained. Inline root Python assertions compared delivery hashes, mobile geometry, final-field hit tests, paint thresholds, state outcomes, and response statuses; `gates.json` records PASS for every size, paint gate, and states.

Candidate verification command, run from project directory: `shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256` → 9/9 OK. One earlier attempt from repo root could not resolve its project-relative members; rerunning from the declared project directory resolved all nine. A summary-only Python read initially used the wrong JSON key and raised KeyError; corrected to `runs`. Neither issue affected browser evidence or required candidate repairs. No browser infrastructure retries, source repairs, or rebuilds were performed during this delivery validation.

## Requirement matrix and measured browser result

All measurements are CSS pixels. Full rectangles, computed styles, accessibility snapshots, CDP pseudo-element boxes, hit tests, and browser responses are in E/viewport.json.

| Viewport | Result/canvas x, width, height | Initial first label y range / input y range | Minimum action target | Final output input y range / clearance above action bar |
| --- | --- | --- | --- | --- |
| 360×640 | 0, 360, 190 | 257–275 / 283–329 | 64.39×46 | 372–416 / 165 |
| 390×844 | 0, 390, 219.4375 | 286.4375–304.4375 / 312.4375–358.4375 | 70.39×46 | 605.4375–649.4375 / 135.5625 |
| 430×932 | 0, 430, 220 | 287–305 / 313–359 | 78.39×46 | 694–738 / 135 |
| 700×844 | 0, 700, 219.4375 | 286.4375–304.4375 / 312.4375–358.4375 | 132.39×46 | 605.4375–649.4375 / 135.5625 |

- **PASS mobile title/status:** header `display:none`; status is clipped at −1,−1 with a 1×1 box and `clip:rect(0px,0px,0px,0px)`, retaining text, `aria-live=polite`, and accessibility-tree paragraph “Ready to generate a smooth STL.” Completed status also remains visually clipped. No routine status consumes visible space.
- **PASS edge-to-edge:** initial canvas and result at x=0, y=0, exactly viewport width; computed margin, border, padding, radius all zero. Heights meet 190–220. Preview region and five actions visible on fresh load.
- **PASS fields:** page scroll and form scroll both zero initially; device-length label and usable 46px input completely visible and hit-testable. At each mobile maximum form scroll (2755, 2551, 2463, 2551 respectively), page scroll remains zero, final output label and 44px selector are fully visible. `elementFromPoint` at selector top+1, center, bottom−1 returns `output_mode` all three times. Action bar does not overlap it.
- **PASS actions/accessibility:** five controls form one row, all ≥44×44. Text has computed font size 0 on mobile, mask pseudo content is empty, and clean accessible names remain Generate STL, Cancel, Reset, Reset camera, Download STL; no Unicode pseudo prefixes. Disabled Download initially has no href and remains readable accessibility text; after generation it becomes the named link. Existing wording is unchanged. Native `title` attributes remain absent; no new hover-tooltip behavior is claimed.
- **PASS overflow/sticky:** document scroll width equals viewport width at all six sizes. No screenshot shows horizontal clipping. At page scroll 80 and form scroll 500, viewer stays x=0,y=0,w=390,h=219.4375 and action bar remains visible at y=745.4375–804.4375.
- **PASS desktop boundary:** 701 switches to visible title/caption/status and 580px desktop canvas; 1440×1200 retains title/caption/status, two-column layout, canvas x=485,y=201.875,w=878,h=580 and 16px textual action labels. `desktop-actions.png` confirms the existing wrapped text action layout. No claim of desktop redesign or improvements.

## Actual icon paint and visual inspection

All five CDP pseudo boxes are exactly 24×24; element centers differ from control centers by at most 0.0078125px horizontally and 0 vertically. All have `background-image:none`, background color equal to computed currentColor, SVG mask and `-webkit-mask-image`, contain sizing, and 50% 50% positioning. CSS dimensions alone were not treated as proof of rendered size.

E/measure_ink.py inspects each actual screenshot within its CDP pseudo box, comparing RGB to nearby control background with a ≥10-channel-difference threshold. Painted bounds and their centers relative to target centers, identical across fresh 360/390/430 captures:

| Action | Actual painted dimensions | Center delta x, y |
| --- | --- | --- |
| Generate | 22×22 | −0.1953125, 0 |
| Cancel | 20×20 | +0.40625, 0 |
| Reset | 21×21 | +0.5078125, +0.5 |
| Reset camera | 19×19 | −0.890625, +0.5 |
| Download | 20×20 | +0.203125, 0 |

Every painted extent exceeds 18px in both axes and its bounding-box optical-center proxy is within 1px on both axes. Generate has actual white center pixel RGB 255,255,255 against navy RGB 17,34,51 (approximately 16.15:1 contrast). Cancel and Download paint gray RGB 188,188,188 against 248,248,248; opacity 0.46 visibly distinguishes their disabled state. Enabled controls remain navy. This confirms the mask tint repair, with no black SVG background-image overpaint.

Validator personally opened and inspected all 15 PNGs: `360x640-initial.png`, `390x844-initial.png`, `430x932-initial.png`, their matching `-final.png` captures, `700x844-initial.png`, `700x844-final.png`, `701x844-initial.png`, `1440x1200-initial.png`, `desktop-actions.png`, `mobile-generated.png`, `mobile-scrolled.png`, `mobile-stale.png`, and `mobile-toast.png`. The star, stop square, two distinct directional reset silhouettes, and download arrow/tray are visibly substantial, centered, and discernible. The initial empty preview is expected before Generate; the generated capture visibly contains the compiled smooth case.

## Live interaction and error results

E/states.json records actual UI interaction on the private route at 390×844:

- Invalid device length 0 produces a visible error toast at x=0,y=720,w=380,h=114, role alert, assertive live region; focus moves to Dismiss. Dismiss hides toast and restores focus to Generate.
- Real smooth generation completes with status `Complete 04109b17a9e3`, no fallback note or error toast, visible model and enabled Download.
- Actual download succeeds, 12,160,971 bytes, filename `laifen-04109b17a9e394ae9bdd97d43ca4af573c48b32ecbfcff85507dc3650f380d3e.stl`, SHA-256 `b1b9db18e21cafed5237afb90e57831b72246c6ac2e4b4c88f736738fd0cf169`; E/smooth-download.stl retained.
- Editing length to 209 displays stale warning and focused input outline, sets Download aria-disabled true, and removes href. All five Diamond controls remain disabled.
- No page errors or failed network requests. Viewport run records 18 responses, states run 13; all HTTP 200, including actual worker and WASM loading. Console contains only SwiftShader/WebGL “GPU stall due to ReadPixels” performance warnings (four per run), not application errors.

No blocking or major findings. Informational: automated screenshot/AX inspection does not establish VoiceOver announcements or human comprehension of the two reset silhouettes. Active compilation cancellation/race behavior was not re-exercised here; its previously documented gate remains outside this delivery CSS change. Successful STL generation/download is delivery functionality evidence, not new CAD, slicer, manufacturing, or physical acceptance. Public Diamond remains disabled under its existing hold.

## Receipt and next action

Evidence manifest E/evidence.sha256 covers all 34 evidence files and verifies 34/34; its SHA-256 is `43a02108c09e8dfe7b5c75df56661ac5031cd371850f2ca3a69c8100737f3677`. It includes exact served bytes, 15 screenshots, download, scripts, raw measurements, browser logs, and assertions. Report hash is supplied externally in the validator receipt to avoid a self-referential digest.

The exact delivered C3 surface passes the specified Chromium gates. Safari/WebKit was not executed: computed `-webkit-mask` support in Chromium is evidence of declarations, not a Safari rendering result. Actual user's Safari viewport, browser chrome/safe-area, device scale, touch, and screen-reader experience remain the next user acceptance gate. No further repair or deployment is authorized by this receipt.
