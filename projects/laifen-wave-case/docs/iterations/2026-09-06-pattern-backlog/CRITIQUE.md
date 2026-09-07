# PB-CRIT — recessed-diamond appearance study

## Verdict

Status: **PASS after focused repair 1**. No remaining actionable appearance or
phone-usability finding in this study's frozen scope.

The initial candidate was **HOLD** for two findings: phone section annotations
were reduced to about 5–6 CSS px, and exact-entry controls were 42 px high
against the 44 px minimum. Repair 1 resolves both without changing the analytic
math or comparison layout.

## Provenance

I verified all 38 paths in `inputs/candidate.sha256`, SHA-256
`8d71809de30441b9f0c0c62fb5191524f06f125c0d010ff71b33d0b6f9ff5779`.
Final study hashes are `index.html` `5edb9e9a…ac8b2`, `math.mjs`
`85148315…e9d1a`, `study.mjs` `f480e5fd…fee32e`, and `style.css`
`f6118a47…507bd`. The implementation receipt is `0017189e…cd87bb`.

I directly inspected the fresh 1280×900 capture
`/tmp/pattern-backlog-review/desktop-r1.png`, SHA-256 `b94c04aa…d6185cc`,
and 390×844 capture `mobile-r1.png`, SHA-256 `d31e5a89…5f5b658`.

## Appearance and interaction critique

1. **Default comparison — healthy.** Without relying on captions, the current
   field reads as broad high, faceted flat centers with depressed crossings;
   the proposal reads as smooth recessed centers separated by high crossing
   ridges. Neutral material, light direction, patch size, phase, and scale are
   visibly matched.
2. **Section evidence — healthy.** True-proportion sections preserve equal
   horizontal and depth units. The ×6 sections retain the same sign and
   horizontal profile while enlarging depth. Repair 1 draws against CSS size
   and device pixel ratio; datum, depth, ×6, and 5 mm annotations are legible
   on both inspected viewports.
3. **Beginner controls — healthy.** Size and Depth pair exact numeric entry with
   sliders, units, limits, a clear render action, and a reset icon. Exact inputs
   now measure 44 px high. Controls remain compact and understandable.
4. **Phone layout — healthy.** Cards stack in current-then-proposal order, all
   evidence remains visible, and the 390 px state reports no horizontal
   overflow. Icon actions and sliders retain 44 px targets.
5. **Rendered-state integrity — healthy.** The supplied resize probe keeps all
   six canvas datasets at the last rendered Size 4.8 while an unrendered 4.83
   draft is present. Resize therefore does not silently accept stale input.

## Evidence boundary

The screenshots and source inspection do not independently prove keyboard
order, focus visibility, assistive-technology output, invalid recovery, or the
analytic oracle; PB-VAL owns those checks. This study makes no CAD, STL,
printability, or physical-performance claim. Proceed to formal review and the
user appearance gate.
