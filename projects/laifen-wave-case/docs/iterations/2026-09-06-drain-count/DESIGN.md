# Drain-hole count design contract

## Geometry and limits

Let `N=drain_count`, hole diameter `d`, ring radius `R`, inner-radius limit
`I=min(body_inner_radius,cap_inner_radius)`, and assumed ligament `g=0.4 mm`.
For an active drain end, centers are:

```text
N = 1: (0,0)
N >= 2: (0,0) plus (R*cos(360*i/(N-1)), R*sin(360*i/(N-1)))
          for integer i = 0..N-2
```

This preserves the old `N=7,d=3,R=9` construction exactly. Count controls only
membership in this fixed family. The user's separate next item is “pattern”;
this contract does not classify or change it.

The authoritative rules are:

1. Always require integer `1 <= N <= 24` and the existing numeric domains for
   `d` and `R`.
2. With an active end, require center edge clearance `I-d/2 >= g`.
3. With `N>=2`, require ring sidewall clearance `I-(R+d/2) >= g` and
   center-to-ring ligament `R-d >= g`.
4. With `N>=3`, require adjacent ring ligament
   `2*R*sin(180/(N-1))-d >= g`.
5. With `drainage_mode="none"`, skip physical spacing rules because no cutter
   exists; integer/range validation still applies to emitted source values.

For active browser drains, `d=3` and `R=min(9,D/2-2)`. If center and ring rules
pass, the slider maximum is
`Nmax=min(24,1+floor(pi/asin((d+g)/(2R))))`; otherwise it is `1`, subject to the
center-hole edge rule. Examples: `D=10 -> Nmax=1`, `D=11,R=3.5 -> Nmax=7`, and
`D>=22,R=9 -> Nmax=17`. These are geometric non-overlap limits, not print proof.

## UI, state and error contract

- Place **Number of holes** under Top/Bottom. Use a text input with
  `inputmode="numeric"` so the whole-number parser can preserve exact raw text,
  plus a paired range (`1..Nmax`, step `1`) with an explicit rule/readout such as
  `Allowed now: 1-7 holes at 11 mm inside diameter`.
- Keep raw count as a string. A blank/non-decimal/non-integer active value says
  `Enter a whole number.`; an active integer outside `1..24` says
  `Use a whole number from 1 to 24.` Both are count-only direct errors.
- A valid active `N>Nmax` is one coupled issue on `diameter` and `drainCount`:
  `At D mm inside diameter, use at most Nmax holes to keep 0.4 mm between openings.`
  Generate is disabled. No value changes silently.
- A coupled count/diameter issue does not become the generic screw-closure
  error and does not invalidate an otherwise coherent last-valid dimension
  snapshot. The count slider exposes `1..Nmax`; diameter bounds are computed
  against the current valid count so either slider offers only repairing values.
  Direct invalid diameter disables count bounds; direct invalid count preserves
  its exact text and disables its range rather than allowing range coercion.
- With neither drain checkbox selected, the pair is visibly disabled and no
  count error blocks Generate. Preserve the raw string. If it is a legal
  integer, emit it; otherwise emit canonical `7` only to satisfy the source
  schema. Re-enabling either end validates the untouched raw string.
- Count edits use the existing `edit()` lifecycle: invalidate/terminate active
  work, clear download currency, mark prior geometry stale, and never call the
  runtime until explicit Generate. Reset restores count `7`, Top off, Bottom on.

Keep one pure drain-layout/feasibility helper shared by schema and bounds logic.
Dimension preflight must use neutral `N=1` or geometry-independent checks, then
add the named drain issue separately; it must accept valid `D=10,N=1` and never
mislabel count spacing as a screw-closure failure. SCAD independently asserts
the same equations and generates the same centers.

## Focused evidence plan

- Math/schema: exact center lists and `Nmax` for `D=10,11,30`; accept
  `D10/N1`, `D11/N7`, default `D30/N7`, and `D30/N17`; reject `D10/N2`,
  `D11/N8`, `D30/N18`, fractional/blank/out-of-range counts, and source-edited
  `d/R` cases at both sides of each equation.
- User behavior: all four checkbox modes share the count; none disables and
  remembers raw state; re-enable reveals it; Reset returns 7/Bottom; exact and
  range stay synchronized; invalid/coupled drafts, stale output, cancellation,
  and explicit-generation behavior remain deterministic.
- Actual geometry: compile selected body/cap endpoints with the pinned WASM and
  count actual openings for `N=1,2,7,Nmax`, including `D11/N7` and `D10/N1`.
  Point/section probes must find every intended void, solid mid-ligaments and
  retained sidewall. Expected independent-cylinder volume loss plus pairwise
  circle clearance establishes no cutter overlap; mesh closure/positive volume
  and unchanged bounds remain required.
- Regression: default smooth assembled Bottom-only `N=7` must be byte-identical
  to baseline. Source/schema center lists must agree. Compact desktop/mobile
  review checks readable labels, integer affordance, embedded maximum, none
  disabled state, invalid recovery and no automatic generation.

Evidence remains separate: these checks can establish source/browser/compiled
geometry only. Slicer behavior, support-free printing, strength, water passage,
occlusion, fit and physical acceptance remain pending.
