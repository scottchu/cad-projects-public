# VFR-12 mobile viewport implementation

Status: implementation candidate complete; independent validation, critique and formal review pending.

The VFR12 input manifest verified 17/17 with fingerprint `adffc64b4e496b15a3e023c8704bb254db732c0aa62d0558994f56276e933ef4` before edits. The only source change is mobile CSS. HTML, runtime, schema, worker, SCAD, geometry and service state remain untouched.

The mobile media query now clips `#status` to an accessible 1px live region without `display:none` or `visibility:hidden`; makes `.result` and `#viewer` edge-to-edge at x=0 with zero border, radius, padding and margin; keeps the responsive `clamp(190px,26vh,220px)` canvas; preserves the 64px form/end clearance; and centers 24px pseudo-icon boxes with 24px font size using both flex alignment properties. Existing disabled styling and one-row 44px action targets remain.

## Validation

- `uv run pytest tests/test_openscad_wasm_simulator.py`: 7 passed.
- `npm run build:openscad-simulator -- --outDir .../scratch/vfr12-mobile-implementation/dist`: Vite 6.4.3 build passed, 11 modules transformed.
- Real Chromium 151 with `--enable-unsafe-swiftshader` served the built bundle from a temporary loopback server at 390x844, 360x640, 430x932, 700x844, 701x844 and 1440x1200. Page errors were empty.
- Evidence screenshots and JSON measurements are under `scratch/vfr12-mobile-implementation/`.

At 390x844, initial layout measured result/canvas x=0..390 and height 219.4375px; status display `block`, visibility `visible`, position `absolute`, 1x1px clipped box, text preserved and `aria-live=polite`; first Basic input x=11, y=312.4375, 368x46; actions x=11, y=785, 368x59; document scrollWidth=clientWidth=390. At maximum form scroll, output-mode measured y=605.4375..649.4375 and top/center/bottom hit tests returned `output_mode`. Every action target was at least 44x44; pseudo styles reported 24px width, 24px height and 24px font size with `justify-content:center` and `align-items:center`. The 360 and 430 probes also had no horizontal overflow and full-width borderless viewers. At 701 and 1440, desktop status, card styling, 580px canvas and labels remained active.

The screenshots were visually inspected, including `mobile-initial.png` and `desktop.png`. No deployment, public route, printer, CAD or physical acceptance action occurred. Controlled Chromium does not establish Safari/iPhone delivery acceptance. The output-mode hit test and the desktop measurements are implementer evidence and require independent rerun.

## Fingerprints

- `preview/openscad-wasm-simulator/style.css`: `176209d8c82940c74083b229f42585f3339c892109c18f9d9ceafca6c522359d`
- `tests/test_openscad_wasm_simulator.py`: `168e3bc9cc6f5d84965dd4f1ae163a1952bf7617e9c12bfed5857daf603ec708`
- `preview/openscad-wasm-simulator/index.html`: `997c2fbc80f453911c3ba68fed55ab17b3c9d2d56d7bb99ceee43a9e0ee82d6f`
- `preview/openscad-wasm-simulator/src/main.mjs`: `98af41e1377afb873208977eedc679ea9e887b04b96253bc2025b3896fbeb353`
- `preview/openscad-wasm-simulator/src/schema.mjs`: `894062333ba7370c4b17efc93b788623eb9db86d0117ffc45275886d0f754ae0`
- `preview/openscad-wasm-simulator/workers/openscad.worker.js`: `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`

## Repair cycle 1

The independent critique measured Unicode glyph ink as undersized and optically low. The repair replaces mobile pseudo-element Unicode glyphs with five deterministic currentColor mask icons. Each uses `content:""`, a fixed 24x24 box, contain/no-repeat centering, and both `-webkit-mask` and standard mask properties; the DOM action wording remains the accessible name source. Generate, Cancel, Reset, Reset camera and Download use distinct filled marks. Existing disabled opacity/grayscale/color treatment and the form bottom clearance remain intact.

Fresh initial screenshots were captured before form scrolling at `mobile360-mask.png`, `mobile390-mask.png` and `mobile430-mask.png`; `desktop-mask.png` is the desktop comparison. Real Chromium built-bundle probes had no page errors. At 360/390/430, viewers were x=0..viewport width with heights 190, 219.4375 and 220px; first Basic inputs were complete at y=283, 312.4375 and 313; scroll widths equaled viewport widths; all five action targets were 46px high. Computed pseudo boxes were 24x24 with empty content, `currentColor` backgrounds, mask URLs, and center alignment. At form maximum, output-mode top/center/bottom hit tests returned `output_mode` at all three sizes. Desktop remained 580px canvas with visible heading/status and labels.

Commands: `uv run pytest tests/test_openscad_wasm_simulator.py` passed 7 tests; `npm run build:openscad-simulator -- --outDir .../scratch/vfr12-mobile-implementation/dist-mask` passed; a temporary loopback `uv run python -m http.server 8773` served the bundle for Chromium and was stopped after the probe. The screenshots and `mask-measurements.json` are implementer evidence pending independent rerun and formal review. No deployment, runtime, geometry or physical acceptance occurred.

## Repair cycle 2 (final allowed repair)

The C2 validator found black SVG background-image layers overriding currentColor and three painted marks below the 18px bound. The final repair removes every background-image declaration. Each mobile icon is painted only by background-color:currentColor through its prefixed and standard mask. Cancel, camera and Download paths were enlarged; Reset was vertically recentered. Generate now paints light on the navy primary button.

Fresh built-bundle Chromium probes at 360x640, 390x844 and 430x932 found no page errors. Screenshot pixel bounds at all three sizes were stable: Generate 22x22 (delta 0,0), Cancel 20x20 (0,0), Reset 21x21 (+0.5,+0.5), Reset camera 19x19 (-0.5,+0.5), Download 20x20 (0,0). All painted bounds meet the >=18px gate and center delta is <=1px. Computed styles report empty pseudo content, 24x24 boxes, currentColor background, both mask URLs, and no background-image paint. Generate sampled light icon pixels against the navy button. Max form scroll hit tests still return output_mode at top, center and bottom for all phone sizes.

Evidence screenshots and final-measurements.json are under scratch/vfr12-mobile-implementation/. The final focused suite passes 7 tests and the Vite build passes. Final CSS hash: b530ae8870b5b2c0eb9548192edeb96fb122860ead203eb1295bd9ebb3893114. Final focused-test hash: bf9ee06d1d3648f9d0fcec27c626f50a8d501db0395d9f071d86a1808b28a79c. HTML, main, schema and worker hashes remain unchanged. This remains implementer evidence pending independent rerun and formal review; no deployment or actual iPhone/Safari acceptance is claimed.
