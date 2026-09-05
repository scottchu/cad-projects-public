# VFR-11 mobile density implementation

Status: candidate implemented; independent review and deployment remain pending.

## Contract and candidate

The frozen input manifest `inputs/VFR11_MOBILE_DENSITY_INPUTS.sha256` verified
with `sha256sum -c` from the project root. The HTML structure and runtime
source bytes were preserved. The mobile media query now hides the page header,
uses a responsive 190–220 px canvas, and keeps the five existing actions in a
single sticky row with 44 px minimum targets and deterministic CSS icons. The
desktop labels remain in the DOM and desktop sizing is unchanged.

Changed paths:

- `preview/openscad-wasm-simulator/style.css`
- `tests/test_openscad_wasm_simulator.py`

The focused test was updated for the new compact-row contract and adds
assertions for all five controls, mobile header/canvas density, icon rules,
and target sizing.

## Validation

`uv run pytest tests/test_openscad_wasm_simulator.py` passed: 6 tests.

The unchanged source fingerprints are:

- `src/main.mjs`: `98af41e1377afb873208977eedc679ea9e887b04b96253bc2025b3896fbeb353`
- `src/schema.mjs`: `894062333ba7370c4b17efc93b788623eb9db86d0117ffc45275886d0f754ae0`
- `workers/openscad.worker.js`: `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`

The real Chromium probe produced screenshots under
`scratch/vfr11-mobile-density/`, but the source-directory probe could not
resolve the bare `three` module. A second probe against the local Vite build
did not complete within the 30 second tool ceiling. Therefore no real-browser
layout pass is claimed here; the PNGs are retained as diagnostic evidence
only. Independent validation should rerun Chromium against the built bundle
and verify 390×844 and desktop screenshots on the delivery surface.

No deployment, service, printer, or public browser state was changed.

## Repair cycle 1

The independent critique measured the final `output_mode` select at
`y=754.4375..798.4375` beneath an action strip beginning at `y=785`. The
repair reserves `64px` of form scroll padding and `64px` after the final
fieldset. A fresh built-bundle Chromium probe at `390x844`, with the form at
its maximum scroll position, measured the select at
`y=690.4375..734.4375`; top, center and bottom hit tests all returned
`output_mode`, while the action strip remained at `y=785..844`.

The repair also changes the reset-camera glyph to `⟳` and applies a distinct
opacity, grayscale, muted-color and border treatment to disabled buttons and
the disabled Download anchor. The focused suite remains `6 passed`. The
repair CSS hash is `d13361dc7519cbe2172ee0107e70e3a0d192b84078d723bd3dc8f686fb637cdb`;
HTML, main, schema and worker fingerprints remain unchanged.

The real built-bundle probe was run with `npm run build:openscad-simulator --
--outDir .../scratch/vfr11-mobile-validation/dist-repair`, a loopback
`uv run python -m http.server 8766`, and Playwright Chromium with
`--enable-unsafe-swiftshader`; page errors were empty. This remains
implementer evidence pending independent rerun and formal review.
