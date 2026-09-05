# CAD Viewer render-controls design

## Selected presentation model

Extend the generated `closed.params.js` sidecar. Insert a fixed one-option enum
as the first row:

```text
00 VISUAL PREVIEW ONLY
Deforms or styles the displayed mesh. CAD and STEP stay unchanged.
```

Place the ten controls next, then append the current `readout_rows()` unchanged.
The result has 52 rows: one new disclosure, ten interactive controls, and the
existing 41-row read-only snapshot. Keep `READOUT_SCHEMA` for compatibility and
add explicit `renderOnly: true` and `geometryRegeneration: false` metadata.

Every interactive description must say: `Render only. Changes the displayed
mesh, not CAD, STEP, fit, wall thickness, thread clearance, or printability.`
Scale labels use percent and motion labels use `visual` or `preview` language;
none is named after an authoritative CAD parameter.

## Exact controls

| Order / id | Type | Default | Bounds / step | Meaning |
| --- | --- | ---: | --- | --- |
| `01 visual_radial_scale_pct` | number | 100 | 60..160 / 1 `%` | Common X/Y display scale for both parts around the shoulder axis. |
| `01 visual_axial_scale_pct` | number | 100 | 60..160 / 1 `%` | Common Z display scale for both parts around the shoulder plane. |
| `01 visual_body_axial_scale_pct` | number | 100 | 60..160 / 1 `%` | Additional body-only Z display scale, anchored at the shoulder. |
| `01 visual_cap_axial_scale_pct` | number | 100 | 60..160 / 1 `%` | Additional cap-only Z display scale, anchored at the shoulder. |
| `02 visual_cap_unscrew_turns` | number | 0 | 0..3 / 0.25 `rev` | Rotate the cap about `+Z` and lift it by 2 mm per turn. This illustrates the existing right-hand screw relationship only. |
| `02 visual_cap_extra_lift_mm` | number | 0 | 0..60 / 1 `mm` | Additional straight `+Z` inspection separation after screw travel. It is not thread engagement. |
| `03 visual_body_color` | color | `#7097b3` | hexadecimal color | Body surface color override when changed. |
| `03 visual_cap_color` | color | `#77b09a` | hexadecimal color | Cap surface color override when changed. |
| `03 visual_body_opacity` | number | 1 | 0.10..1 / 0.05 | Body surface and edge opacity multiplier. |
| `03 visual_cap_opacity` | number | 1 | 0.10..1 / 0.05 | Cap surface and edge opacity multiplier. |

The 60–160% scale limits are exploratory but bounded: they permit obvious
proportion studies without zero, negative, mirrored, or extreme transforms.
Opacity stops at 0.10 because native tree visibility already provides hide/show
and a fully invisible part would make the control target hard to recover.

Do not add visibility toggles, generic explode, clip/section, edge/display,
camera, background, lighting, or global-theme controls. Viewer 0.4.28 already
owns those functions. The cap controls remain because screw-coupled rotation and
one-sided axial inspection are specific to this assembly and are not equivalent
to the native generic explode control.

## Stable features

Declare two features using `names`, not positional refs:

```javascript
features: {
  body: {
    label: "Body display mesh",
    names: ["R7 body: 39mm diamond skin; new B right-hand thread; smooth chamfer with seven drains"],
    axis: [0, 0, 1],
    origin: [0, 0, 0]
  },
  cap: {
    label: "Cap display mesh",
    names: ["R7 cap C25: new B thread; 39mm diamond skin; smooth end chamfer; seven drains"],
    axis: [0, 0, 1],
    origin: [0, 0, 0]
  }
}
```

The current descriptor proves those names correspond to `#o1.1` and `#o1.2`.
Validation must require `features.body.partIds` and `features.cap.partIds` each to
contain exactly one distinct occurrence. A name change is a blocking source/
sidecar mismatch rather than permission to fall back silently to an id.

## Pure transform and style law

Export a deterministic `solveVisualPreview(rawParams)` from the self-contained
sidecar so Node tests can call the same math as `update()`.

For `clamp(x, lo, hi) = min(max(Number(x), lo), hi)` with the declared default
used for non-finite input:

```text
r  = clamp(visual_radial_scale_pct, 60, 160) / 100
az = clamp(visual_axial_scale_pct, 60, 160) / 100
bz = az * clamp(visual_body_axial_scale_pct, 60, 160) / 100
cz = az * clamp(visual_cap_axial_scale_pct, 60, 160) / 100
u  = clamp(visual_cap_unscrew_turns, 0, 3)
e  = clamp(visual_cap_extra_lift_mm, 0, 60)
theta_deg = 360 * u
cap_z_mm  = 2 * u + e
```

The body effect matrix is `S_body = scale(r,r,bz)` about `(0,0,0)`.
The cap effect matrix is:

```text
M_cap = Translate(0,0,cap_z_mm)
        * Rotate(+Z, theta_deg, origin=(0,0,0))
        * Scale(r,r,cz, origin=(0,0,0))
```

This matches Viewer 0.4.28 `transforms` array order when the sidecar supplies
`[scale, rotate, translate]`: each step is premultiplied. The shoulder remains
fixed through all scale and rotation steps; only the explicit cap translation
moves it. The locked P1 R7 thread pitch provides the 2 mm/rev visual screw law.
This law illustrates the existing source joint and is not collision, engagement,
or printable-geometry evidence.

`update({params, effects})` must call:

- `effects.transform("body", ...)` only if `(r,r,bz)` differs from identity;
- `effects.transform("cap", ...)` only if cap scale, rotation, or translation
  differs from identity;
- `effects.style("body", {color, opacity, edgeOpacity: opacity})` only if body
  color differs from `#7097b3` or body opacity differs from 1;
- the equivalent cap style only if it differs from `#77b09a` / 1.

Do not call `effects.clear()`, `visible()`, `highlight()`, `render()`, or any
Three.js API. Viewer rebuilds the effect map on every update, so omission means
baseline state. This is also the exact zero-state rule: default parameters cause
zero calls to every effects method.

## Generated-source structure

Keep `preview_parameters.py` as the only generator of the self-contained
sidecar. Preserve `readout_rows()` and its 41 current rows. Add pure Python data
for the ten control definitions and deterministic JavaScript templates for the
solver/update logic. No sibling JavaScript import is allowed.

`closed.step.py` remains unchanged. It already declares `closed.params.js` in
the supported generated-model envelope. No other entrypoint receives a sidecar.

## Focused test plan

The implementation test must catch the following credible failures:

1. **Disclosure/readout regression:** require 52 rows in insertion order, the
   visual-only notice first, exact ten controls next, and the prior 41 rows
   byte-for-byte equivalent as structured values.
2. **Control contract drift:** require exact ids/types/defaults/units/bounds,
   color defaults matching source occurrence colors, and render-only text on
   every interactive control.
3. **Math/transform defect:** test default, independent radial and axial values,
   combined body/cap axial factors, 1.25 and 3 turns, extra lift, min/max, and
   non-finite/out-of-range clamping. Assert `cap_z_mm=2*u+e`, positive `+Z`
   rotation, and the ordered `[scale, rotate, translate]` specs.
4. **Target/effect defect:** mock the effects API and require exact target names,
   zero calls at defaults, only the changed part/style at single-control cases,
   and no unsupported effect method or direct Three.js access.
5. **Provenance defect:** preserve deterministic serializer parity, exact
   sidecar declaration, current occurrence-name witnesses, and all four STEP
   hashes.

After cheap tests pass, `RCV-04` must inspect the generated descriptor and exact
served module, then exercise reset/default, one scale case, coupled 1-turn screw
case (360 degrees and +2 mm), full 3-turn plus 60 mm lift, individual colors and
opacity, and native tree visibility. Capture at least one desktop comparison and
mobile 390 x 844 default/changed/reset states. Confirm that native reset restores
the same screenshot-level pose and source colors as module disabled.

## Acceptance and limits

- **Render-preview PASS** covers only the exact sidecar effects and delivery
  presentation for one frozen candidate.
- **CAD/source and written STEP:** inherited PASS and must remain byte-identical.
- **Slicer/process:** HOLD.
- **Physical:** PARTIAL / UNBOUND.
- Any displayed deformation can violate true wall, bore, thread, clearance,
  pattern, drain, or collision relationships. The UI disclosure is part of the
  acceptance contract, not optional copy.

