# PB-IMP — Recessed Diamond appearance study

Status: **implemented for independent review**. This is an analytic comparison page, not container CAD or a compiled artifact.

## Frozen inputs

- Baseline commit: `191cb37119f9a4e4d23112ecd5bc0d18f0daec86`.
- Current unchanged SCAD: SHA-256 `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`.
- BRIEF: SHA-256 `442c718589ef6a9a2e17037e941e030cad6a3498f33621505aa4a974835e464e`.
- DESIGN: SHA-256 `c81ac2f3b20d8b7a8024b33671c03a6768e77c97ca53646441b86e9032ceb8b8`.
- `inputs/baseline.sha256`: 19/19 verified, manifest SHA `9d08cea42a798c548d54528cb28f715db5335b51d1f06e5cc37b534aeef832bb`.
- `inputs/design-extra.sha256`: 10/10 verified, manifest SHA `1bb047310c8904121aa1440139c077673b091c939caf44358d627db836ac65b6`.
- Superseded candidate manifest `552a252c4ac91379dab79d3655d620172849a5836c686d67d1a34251bec7b269`: independent critique found that intrinsic-canvas section labels shrank below legible size on mobile. Repair 1 retains the same analytic geometry while drawing section annotations in CSS pixels at device resolution and raises number inputs from 42 to 44 px.

## Implementation

All product files are self-contained under `preview/recessed-diamond-study/`:

- `index.html` SHA `5edb9e9a561007c8d74b6df4cef77cea8b1c60b50e152fe7fc0452811f4ac8b2`: semantic comparison, exact Size/Depth inputs and sliders, compact accessible Render/Reset icon actions, required truth label, and exact link to the accepted 8453 customizer.
- `style.css` SHA `f6118a474cb454e468135ecaf98658c121160adafd6b285975ff20d26d3507bd`: equal desktop panels, stacked mobile layout, compact header, neutral material, 44 px controls and no horizontal overflow.
- `math.mjs` SHA `85148315035fc1b62bab27516d696c4036894b0b06b6896ab378f7a227de9d1a`: pure documented `wrap`, field, cubic smoothstep, Current/Recessed height functions, arc/count derivation and section breakpoint sampler.
- `study.mjs` SHA `f480e5fdf5e94fd4c3c5c07b682e327d8535cc074c0e0f8715f0781de4fee32e`: native Canvas rendering, shared lighting/dimensions, pixel-center analytic sampling, symmetric display derivatives, state validation/staleness, Render and Reset. Section canvases use CSS-aware device-pixel backing stores, and a resize redraw uses the last rendered snapshot rather than an unrendered draft.

Both patches use the same four-by-four developed domain, reference radius, pitch, depth, phase, material and light. The patch drawing evaluates roughly 300–412 samples per physical axis over the full allowed range, within the required 256–512. Each v=0 section uses 513 uniform samples plus every applicable center, crossing and g breakpoint: 517 unique points for both profiles. The true section uses equal x/depth units; the repeated section scales radial depth by exactly six and fits every allowed Size/Depth endpoint.

## Focused checks

- `node --check .../math.mjs && node --check .../study.mjs`: PASS.
- Node analytic witness: PASS. At d=.45, Current center/crossing is `0/-0.45`; Recessed is `-0.45/0`. Both stay in `[-d,0]`, repeat periodically, share the default derived `N=33`, target arc 3.63 and actual arc 3.6271115182354885 mm.
- Section witness: PASS, 517 ordered samples per profile containing exact centers, crossings and ±g breakpoints.
- Endpoint draw-limit witness across Size 4.8/8.0 and Depth .10/.60: PASS; patch axes stay within 256–512 evaluations and the ×6 section remains inside its canvas.
- Responsive section bounds at 334×83.5 and 510×127.5 CSS px across Size/Depth endpoints: PASS; every analytic profile remains above its scale bar with 12 CSS px annotations.
- HTML/CSS/render contract search: PASS for the exact accepted-customizer URL, two accessible icon actions, visually hidden names, 44 px targets, CSS-pixel section drawing and rendered-snapshot resize behavior.
- The first exact-zero assertion distinguished JavaScript `-0` from `0`; the corrected numeric-tolerance witness passed without a product-source change.

Static review command from the repository root:

`uv run python -m http.server 5188 --bind 127.0.0.1 --directory projects/laifen-wave-case/preview`

Review route: `/recessed-diamond-study/`. Root owns browser screenshots and any reviewed delivery route.

## Scope and limits

No dependency, main customizer, OpenSCAD, worker, test, production `dist`, service, Tailscale/8448 or printer file changed. The page makes no STL, compiled-container, slicing, manufacturing-normal, speed or print-ready claim. Independent PB-VAL/PB-CRIT must still inspect desktop/mobile rendering, no-caption relief recognition, controls, stale/invalid recovery and candidate fingerprints before the user appearance gate.
