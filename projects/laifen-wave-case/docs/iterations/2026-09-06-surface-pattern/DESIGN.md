# Surface-pattern design contract

## Selected control

Use one native-radio fieldset after drain count and before Container options:
`surface-pattern`, radios `surface-smooth` / `surface-diamond`, raw state
`pattern: "smooth" | "diamond"`, and help/error nodes
`surface-pattern-rule` / `surface-pattern-error`. Each labelled 44 px card has
a small CSS-only swatch (plain fill or repeating diamond lines), visible radio,
text label, selected state and focus ring. Default/Reset is Smooth. No Figma,
raster asset, icon-only parameter label, disclosure panel, or texture control.

Generation maps `pattern` only to `surface_style`; the four already allowlisted
Diamond values remain fixed at `4.8`, `3.63`, `0.45`, and `0`, while plateau
half-fraction remains source-bound at `0.18`. All five facts must stay in the
schema/source contract and exact job identity. Smooth must still receive the
same full canonical tuple and produce unchanged geometry.

## Numeric feasible set

Let browser inside diameter be `D`, wall `W`, outside diameter `OD=D+2W`,
valley radius `r=OD/2-0.45`, and
`N=floor(2*pi*r/3.63+0.5)`. With existing `20 <= OD <= 80`, Diamond has
`9.55 <= r <= 39.55` and `17 <= N <= 68`, safely inside source `[8,128]`.
The rounded actual arc pitch is conservatively `3.523235..3.736765 mm`;
therefore fixed plateau developed width is `1.022487..1.061497 mm >= 1`,
and fixed axial slope is `0.29296875 <= 1`.

Diamond wall residuals are body `W-0.45`, cap `W-0.95`, female thread
`W-2.60`, and entry relief `W-2.50`. The existing minima therefore reduce to
`W >= 4.4 mm`; at that boundary they are `3.95`, `3.45`, `1.80`, and `1.90 mm`.
Smooth retains its accepted `W >= 4.0 mm` browser minimum.

For either patterned role of axial height `h`, the source estimate is
`E=16*N*(ceil(h/(4.8/8))+1) <= 250000`. Apply that exact floating-point expression independently to
`capHeight` and `bodyThreadZ=outsideHeight-capHeight`. At default
`D30/W4.5/H213/T3/lid84`, `N=33`, body `E=119328`, cap `E=74448`.
At worst `N=68`, the real-number boundary is `136.8 mm`, but the source's
floating division makes literal `136.8` reach the next `ceil` bucket and fail
with `E=250240`; `136.799999999` passes. The truthful browser step is `0.1 mm`,
so its maximum is `136.7 mm` (`E=249152`). This is numeric parity with the
source, not a physical safety margin; do not add an epsilon or rounded formula.

## State, bounds and errors

- Store the raw pattern choice; radios never generate automatically. Switching
  while busy terminates the owned worker through the existing `edit()` path.
- Validate base dimensions separately from pattern feasibility. A pattern-only
  incompatibility must not discard the coherent last-valid dimension snapshot
  or disable every repair slider. Recompute diameter/height/wall/ends/lid
  intervals through the exact selected-pattern predicate.
- Invalid/missing enum: pattern-only direct error `Choose a surface pattern.`
- Diamond with `W<4.4`: coupled pattern/wall error `Diamond needs wall
  thickness of at least 4.4 mm. Increase wall thickness or choose Smooth.`
  Keep the entered value and expose a repairing wall range beginning at `4.4`.
- Triangle-cap failure: coupled pattern/size error `Diamond is too detailed at
  this size. Reduce outside diameter or patterned-part height, or choose
  Smooth.` The applicable slider rules expose only values satisfying both role
  estimates; no clamp, hidden wall change, timeout, or generic closure message.
- Fixed count/plateau/slope/shell invariants above are unreachable throughout
  the offered feasible domain. Any such schema/source mismatch is a candidate
  failure, not a user-correctable compiler error.
- Returning to Smooth immediately restores the unchanged smooth bounds. Reset
  restores Smooth and all accepted defaults. Pattern changes preserve drains,
  count, output, auto-lid and exact raw dimension text.

## Focused evidence targets

- Math/schema: prove the ranges and formulas above; test `W4.39` fail/`W4.40`
  pass, `OD20/N17`, `OD80/N68`, default estimates, and `N68` role heights
  `136.7` pass / literal `136.8` fail. Verify each slider endpoint passes snapshot and
  the adjacent 0.1 mm value outside a reported endpoint fails when applicable.
- State/lifecycle: Smooth default/Reset; selection memory; no automatic run;
  stale/download invalidation; active cancellation; late correct result after
  Cancel/Reset/timeout; superseded async identity; old timer; duplicate result;
  invalid-parameter/compiler-error recovery. Require current id plus full
  identity/source/lock tuple and fresh worker per accepted job.
- Actual browser jobs: with pinned WASM and a fresh worker per role, generate
  default Diamond body, cap, assembled, then print layout, each `<=60 s` and
  inside the unchanged 180 s timeout. Verify argv occurrence, transferred/Blob/
  download byte identity, nonempty render, filename/current/stale behavior and
  no external or missing worker/WASM requests.
- Actual mesh: original returned STL only; finite positive oriented closed
  geometry, no degenerate/duplicate faces, invalid links, T-junctions or
  nonadjacent self-intersections. Check body Bottom N7 holes and closed cap,
  protected bores/floors/threads, body/cap seam equality and shared phase,
  exhaustive exterior classification/error `<=0.025 mm`, and each standalone
  exterior count `<=250000`.
- Combined outputs: assembled uses source/native union/contact as oracle and
  allows only the zero-volume shoulder plane; do not assert standalone triangle
  concatenation after re-tessellation. Print layout has exactly two closed parts,
  7 mm X gap, standalone transform parity, zero collision and both openings up.
- Visual/service: inspect seam/end/drain/assembly/layout views at `1280x900` and
  `390x844`; labels, swatches, focus, errors and Generate remain reachable.
  Build once, hash before/after observation, verify six served files on private
  8453, and leave 8448 unchanged.

This can establish browser/source and written STL evidence only. CAD/STEP
authority remains P1 R7; slicer, support-free printing, grip, fit, drainage,
thread wear/strength and physical acceptance remain pending.
