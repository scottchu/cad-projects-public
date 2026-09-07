# MC-DES-01 — compact responsive control contract

## Workspace and controls

Desktop (`min-width:761px`) stays a fixed viewport grid: canvas fills the left
column and the 360–400 px control rail scrolls independently. Mobile is also a
fixed `100dvh` grid, with rows `clamp(220px,34dvh,280px) minmax(0,1fr)`.
`result` occupies row one; only `.panel-scroll` in row two scrolls. The canvas
therefore remains pinned at the top even after the first controls move. The
action dock is fixed to the bottom of the control row and honors the bottom
safe-area inset. At 390 x 700 this leaves a 238 px preview, a compact dock, and
the remaining height for parameters. Use opaque panel backgrounds and z-order
so controls never show through the canvas.

The preview toolbar contains three 44 px square icon buttons: **3D view**
(cube), **Cutaway view** (sectioned cube), and **Reset view** (frame/target).
The bottom dock shows a one-line status at left and three 44 px controls at
right: **Generate preview** (play/spark), **Reset dimensions** (counter-clockwise
arrow), and **Download STL** (arrow into tray). While compiling, Cancel (x in
circle) occupies Generate's exact slot. Download retains link semantics and is
disabled unless bytes match the current generated snapshot. Do not retain
visible `3D`, `Cutaway`, `Reset view`, `Generate`, `Reset dimensions`,
`Cancel`, or `Download STL` labels.

Icons are local inline 24 px SVG using `currentColor`; no emoji or external
asset. Every control has its full name in `aria-label`, the same text in an SVG
`title`, a visible hover/focus tooltip, a 2 px focus ring, and existing
`aria-pressed`/disabled state. Pressed view state also changes background and
border, so color is not the only cue. Keep 8 px between targets.

Each dimension becomes one compact block:

1. one line with plain label at left and an 88–104 px numeric input plus `mm` at
   right;
2. a full-width range input with a visually 4 px track, 24 px thumb, and at
   least 44 px interactive height;
3. one rule line, for example `Allowed now: 12–69 mm · lid is 1 mm wider`.

Remove the separate explanatory paragraphs. Keep short purpose text in that
rule line. Numeric input and slider represent the same draft field, with 0.1 mm
slider steps; direct entry permits a finite decimal and is never rewritten.
Focusing either control selects its generated dimension overlay. Sliders need
the same accessible name plus `aria-describedby` pointing to rule/error text.

Drain holes stays visible as a compact native select. Lid and export remain in
collapsed Container options. Replace the Auto button with a labeled native
checkbox/switch; when checked, lid value is read-only and shows the derived
value. Unchecking preserves that displayed value as the manual starting value.

## Exact allowed-range model

Let `D` be inside diameter, `H` inside height, `W` wall, `T` end thickness,
manual lid `L`, and `k=84/219`. Bounds are recomputed after every valid draft
edit. Closed interval endpoints are included; `<` and `>` below remain strict.

| Field | Allowed with the other current values held fixed |
|---|---|
| `D` | `max(10,20-2W) <= D <= min(69,80-2W)` |
| `W` | `max(4,(20-D)/2) <= W <= min(35,(80-D)/2)` |
| `H`, Auto | `6<=H<=305`, `H>=2T+9`, `20<=k(H+2T)<=250`, `k(H+2T)>T+11`, `k(H+2T)<H+T-2` |
| `T`, Auto | `2<=T<=8`, `H>=2T+9`, `20<=k(H+2T)<=250`, `k(H+2T)>T+11`, `k(H+2T)<H+T-2` |
| `H`, manual | `6<=H<=305`, `H>=2T+9`, `L>T+11`, `H>L-T+2` |
| `T`, manual | `2<=T<=8`, `T<=(H-9)/2`, `T<L-11`, `T>L-H+2` |
| `L`, manual | `20<=L<=250`, `L>T+11`, `L<H+T-2` |

These equations are the UI oracle and must still pass unchanged `snapshot()`.
For a 0.1 mm slider, round a closed lower bound up and closed upper bound down;
move one tick inside a strict bound. The rule line reports that usable slider
interval, never a broader static schema range. Direct typed values are checked
against the unrounded equations and preserved exactly. Default rules include
`D 11–69`, `W 4–25`, `H 46.2–305`, and `T 2–8` mm; these are verification
witnesses, not copied constants.

## Invalid and lifecycle behavior

The typed string is authoritative. Blank, nonfinite, out-of-range, or
constraint-invalid text remains in its input, sets `aria-invalid=true`, shows a
specific inline error, disables its slider and Generate, and does not move any
other value. Never rely on native range coercion to repair it. Dependent rules
use the last valid value for that dependency and append `using last valid X`;
if no valid dependency exists, disable the affected slider and say which field
must be corrected. An empty computed interval similarly disables only that
slider and names the blocking relationship. On valid correction, remove the
provisional note and restore synchronization.

Slider `input` events update the numeric draft, derived outside dimensions,
rules, dimension focus, and stale label. They invoke the existing invalidate
path once on the first movement and never call Generate on `input`, `change`,
pointer-up, or key-up. Reset restores the complete adapter defaults, Auto,
drains, output, ranges, and slider positions; clears mesh/download; and does
not compile. Existing generation epochs, timeout, cancellation, exact Blob,
and stale-preview behavior remain unchanged.

## Implementation checks

- Pure range-oracle tests cover default witnesses; D/W OD coupling at D10/W5
  and D69/W5.5; Auto H/T near the 20 mm lid floor; manual strict lid endpoints;
  and empty computed intervals. Every slider-produced snapshot must validate.
- DOM tests prove typed invalid text is retained, dependents use labeled
  last-valid bounds, sliders never mutate other fields, and slider events never
  call generation. Auto/manual transition and Reset restore exact defaults.
- Browser checks at 390x700 and 390x844 scroll every parameter while preview
  bounds remain unchanged; no document scroll, overlap, horizontal overflow,
  or hidden dock. Also check 760x800, 761x800, 1280x800, and 1440x900.
- Keyboard and accessibility checks cover range arrows, direct entry, icon
  names/tooltips, 44 px targets, focus, pressed/disabled state, status, and
  error associations. Actual default and edited WASM generations still produce
  current downloadable bytes. UI validation adds no print-ready claim.

## Design receipt

Verified `inputs/baseline.sha256` (`d0efe353a06e7dc48a5b8a055eb45121d4e2cd2a37cff0428572bf36c580bd49`)
with all 16 paths passing `shasum -a 256 -c`. Read project state,
requirements, experience, decision index, prior desktop contract, current
HTML/CSS, adapter, dimensions, main lifecycle wiring, schema assertions, SCAD
assertions, and focused tests. Inspected the supplied phone image and the
390x700 baseline capture. No application, CAD, service, or hosting file changed;
no generation, browser interaction, slicing, or physical test was run. Next:
freeze this contract and assign MC-IMP-01.
