# P2 R9 modular visual-generator design contract

## 1. Frozen baseline and delta mask

R9 replaces R8 as a new candidate namespace; it does not repair R8 in place. The exact blocked predecessor is the five-file R8 candidate declared by `../2026-09-03-p2-r8-end-inset-parse-recovery/CANDIDATE_MANIFEST.sha256`, whose manifest fingerprint is `59f9aa1438f185979a47f888988833647aff43a1959969e13f54d1217431d655`. R8 critique SHA-256 `0aaf54d6b064cf6b83c8e9ce186b5e5756f640ecb3e2f285e4351d9fcf9c389b` and critique evidence manifest `836300355fadddba0dcabd7e773610d7ccd1ad980f9b6fcdcc4ea527e6f69d09` define the four P1 visual regressions. There is no completed R8 independent-validation receipt at this design freeze; `VALIDATION_INPUTS.sha256` is only a pending-gate input record.

Permitted R9 implementation deltas are a new `preview/p2-r9-modular-generator/**` tree, one new `tests/test_p2_r9_modular_generator.mjs`, and R9 receipts/manifests/scratch evidence. Every earlier source, test, candidate, route, service, CAD, artifact, project state/index, decision, requirement, experience, and observation path is protected.

## 2. Coordinate frame, topology, and scale

All lengths are millimetres. Global `+Z` runs from the bottom exterior apex/face at `z=0` to the top exterior apex/face at `z=H`. The nominal section is in XY; `theta=0` points +X and positive theta is counter-clockwise when viewed from +Z. The lower piece spans the bottom end to `z0=H-S`; the upper piece spans `z0` to the top end. `S` is the upper-piece axial extent in the assembled state.

The model has exactly two core exterior identities: `lower-piece` and `upper-piece`. A fine seam marker, cutaway, closure proxy, arrow, label, drain axis, dimension, comparison thumbnail, and envelope wireframe are annotations or features, not core pieces. Optional accessories are separately named bodies or intentional attached extensions. Base OD is `container.outerDiameter`; derived crest OD may grow only through explicit outward Surface relief. Both remain continuous across the pieces and closure zone; no external collar or thick thread band is allowed.

The main scene uses `1 scene unit = 1 mm` with identical X/Y/Z scaling and unexaggerated surface/text relief. “True scale” means geometry uses one common numerical scale; it does not mean a screen pixel or ruler is physically calibrated. Comparison thumbnails, cutaways, and detail views disclose their independent fit-to-view or magnification factor.

## 3. Canonical state and presentation state

The sole canonical model state has seven keys:

```js
{
  container: { height, outerDiameter, wall, floor, splitFromTop, crossSection, sideCount, cornerRoundness, rotationDeg },
  closure: { mode, matchPatternClosed, screw: {...}, bayonet: {...} },
  ends: { linked, bottom: { profile, size }, top: { profile, size } },
  surface: { pattern, reliefMode, depth, minWall, axialPitch, arcPitch, envelope, coverage, fadeMetric, pattern-specific subobjects... },
  ventDrain: { mode, linked, bottom: { count, diameter, ringRadius }, top: { count, diameter, ringRadius } },
  label: { mode, text, fontFamily, openScadFontFamily, weight, size, relief, orientation, target, angleDeg, axialFromTargetEnd, patch, patchMargin },
  attachment: { mode, presentation, attachHalf, mountAngleDeg, common: {...}, mode-specific subobjects... }
}
```

`uiState={controlTier, selectedPresetId, assembledState, selectedComparison}` is presentation state. Applying a preset deep-merges a patch into a fresh clone of `DEFAULT_STATE`; selecting Basic/Advanced or assembled/exploded never changes canonical values. Raw edits remain editable. `deriveModel(rawState)` returns either one complete immutable derived state or field errors; rendering never reads raw values directly.

## 4. Immutable field schema

`core/schema.mjs` exports deeply frozen `FIELD_SCHEMA`, `MODULE_SCHEMA`, `DEFAULT_STATE`, and enum options. Each leaf field record has:

```js
{
  path, module, label, help, control, valueType,
  unit, min, max, step, defaultValue, tier,
  options, visibleWhen, enabledWhen, exportKey
}
```

`visibleWhen` is a serializable predicate AST over canonical paths (`all`, `any`, `eq`, `in`), evaluated by one pure interpreter. It is not a DOM callback. Bounds may reference named pure bound functions. The UI creates labels, controls, units, help, and error IDs from this schema; `app.mjs` contains no parallel list of field IDs, numeric casts, defaults, bounds, or visibility rules. Registry field fragments must reference paths present in `FIELD_SCHEMA`. `deepFreeze` tests must prove attempts to mutate schemas, defaults, registry entries, preset patches, and export mapping fail or leave values unchanged.

### Basic and Advanced exposure

| Module | Basic | Advanced, only when relevant |
| --- | --- | --- |
| Container | preset action, assembled/exploded view, height, OD, split in mm/% projection, round/polygon | wall, floor; polygon sides, corner roundness, rotation |
| Closure | screw or bayonet | screw pitch, turns, lead/runout, form height, radial clearance; **or** bayonet lugs, lock angle, capture, ramp rise, radial clearance; shared locked pattern-phase toggle |
| Ends | linked/independent and linked family/size | independent bottom and top family/size when unlinked; same values remain in state when hidden |
| Surface | named pattern, relief placement (`inset|outset|balanced`), and envelope choice | common axial/arc pitch, depth and minimum-wall constraint only when used; derived base/crest OD and residual-wall readout; coverage/fade metric; selected pattern's stitch, flute, flowing-wave, soft-spiral, or quilt controls |
| Vent & Drain | none/bottom/top/both and linked/independent | count, diameter, ring radius for enabled bottom/top; linked `both` shows one shared set |
| Label | none/inset/outset and text | font preview, future OpenSCAD family string, weight, size, relief, orientation, target, angle, axial position, patch and margin |
| Attachment | none or named mode | fixed/separate visual, attach half, mount angle, common member/opening values and only the selected accessory's dimensions |

Basic is the initial tier at desktop and mobile. Switching tier changes visibility only. Hidden inactive-family fields retain their canonical values and are excluded from active plugin validation until selected. Structural state validation always runs.

## 5. Plugin registries

`plugins/closures.mjs`, `plugins/ends.mjs`, `plugins/patterns.mjs`, and `plugins/accessories.mjs` each export one deeply frozen registry. Every entry conforms to:

```js
{
  id, label, disclosure,
  defaults, fields,
  derive(state, sharedMath),
  validate(state, derived, errors),
  visual: { mainBuilder, comparisonBuilder, detailBuilder, annotationBuilder }
}
```

Derive/validate functions and builder identifiers are deterministic. Plugin modules do not import Three.js or the DOM. `render/builders.mjs` resolves visual hook IDs; unknown or duplicate IDs are fatal. Shared equations live under `core/math/` and every plugin calls them rather than copying geometry or phase logic.

## 6. Presets, R8 equivalence, and future export

`PRESET_PATCHES` contains frozen deep override patches named `generic`, `laifen_wave_reference`, and `wide_short_makeup_jar`. `DEFAULT_STATE` corresponds to the R8 generic effective state plus valid R9 defaults: `reliefMode=inset`, `minWall=1.2`, drains `none`, linked drain records of count 7/diameter 3/ring radius 10, and clearer soft-spiral defaults. The Laifen patch sets `minWall=1.8` and retains its shallow 0.45 mm recessed-diamond depth, so its base and crest OD both remain 39 mm. Presets do not contain a full cloned state.

`fromR8Flat(flat)` is a pure compatibility fixture helper used by tests, never a second runtime state. It maps every R8 field to one nested R9 path. For all three R8 presets, a stable comparable projection must equal the mapped R9 preset for every pre-existing field. Derived equivalence includes:

| Preset | required retained facts |
| --- | --- |
| generic | `H=120`, `OD=60`, `S=60`, screw `p=2`, `N=2`, `Lr=1.5`, `E=4`, `P=7`, round, blunt diamond, total envelope 60 when label/accessory/drains are off |
| laifen_wave_reference | `H=219`, `OD=39`, `S=84`, screw `p=2`, `N=3`, `Lr=1.5`, `E=6`, `P=9`, round, recessed diamond, linked 1.2 chamfers |
| wide_short_makeup_jar | `H=55`, `OD=80`, `S=27.5`, bayonet angle 90, 3 lugs, capture 2, ramp 1, `E=2`, `P=3`, rounded hexagon at 15 degrees, linked 3 fillets, flowing flutes with bottom fade |

`core/export-map.mjs` owns one deeply frozen `OPENSCAD_EXPORT_MAP` and the only `flattenForOpenScad(state)` function. No plugin, UI control, preset, or renderer may invent export names. Inactive values are included deterministically so a future Customizer can preserve them; this is a naming/data boundary only and does not claim that an OpenSCAD generator exists.

| Canonical group | explicit future variable names |
| --- | --- |
| Container | `container_height`, `container_outer_diameter`, `container_wall`, `container_floor`, `container_split_from_top`, `section_mode`, `section_sides`, `section_corner_roundness`, `section_rotation_deg` |
| Closure | `closure_mode`, `match_pattern_closed`, `screw_pitch`, `screw_turns`, `screw_lead_runout_turns`, `screw_form_height`, `screw_radial_clearance`, `bayonet_lock_angle_deg`, `bayonet_lug_count`, `bayonet_capture`, `bayonet_ramp_rise`, `bayonet_radial_clearance` |
| Ends | `ends_linked`, `bottom_end_profile`, `bottom_end_size`, `top_end_profile`, `top_end_size` |
| Surface | `surface_pattern`, `surface_relief_mode`, `surface_depth`, `surface_min_wall`, `surface_axial_pitch`, `surface_arc_pitch`, `surface_envelope`, `surface_coverage`, `surface_fade_metric`, `stitch_tightness`, `flute_count`, `flute_duty`, `flute_wave_amplitude`, `flute_wave_wavelength`, `flute_wave_phase`, `flute_wave_direction`, `spiral_pitch`, `spiral_band_width`, `spiral_softness`, `spiral_direction`, `quilt_groove_width`, `quilt_pillow_height`, `quilt_edge_softness`, `quilt_rotation_deg` |
| Vent & Drain | `drain_mode`, `drains_linked`, `bottom_drain_count`, `bottom_drain_diameter`, `bottom_drain_ring_radius`, `top_drain_count`, `top_drain_diameter`, `top_drain_ring_radius` |
| Label | `label_mode`, `label_text`, `label_font_family`, `label_openscad_font_family`, `label_weight`, `label_size`, `label_relief`, `label_orientation`, `label_target`, `label_angle_deg`, `label_axial_from_end`, `label_patch`, `label_patch_margin` |
| Attachment | `attachment_mode`, `attachment_presentation`, `attachment_half`, `attachment_mount_angle_deg`, `attachment_opening_width`, `attachment_opening_height`, `attachment_member_thickness`, `attachment_pivot_clearance`, `attachment_keyring_hole_diameter`, `attachment_bridge_span`, `attachment_standoff` |

## 7. Shared pure math and feasibility

Pure functions accept plain immutable data and return plain data. They cannot access Three.js, canvas, DOM, browser globals, time, randomness, or mutable module state. Required modules cover section support/frame, closure accounting/phase, end profiles, surface fields/envelopes, label placement, drains, accessory bounds, camera-fit bounds, deep merge, schema predicates, and export flattening.

Retain R8 closure accounting:

```text
screw:   E = pitch * turns
         P = pitch * (turns + leadRunoutTurns)
bayonet: E = capture
         P = rampRise + capture
K = max(surfaceKeepout, bottomEndExtent, topEndExtent, surfaceAxialPitch/2)
Smin = floor + P + K
Smax = H - (floor + P + K)
require H >= 2*(floor + P + K), Smin <= S <= Smax
```

Retain the R5 section-support equation and one shared global theta/Z pattern field. Closure rotation is `2*pi*turns` for screw and `lockAngle*pi/180` for bayonet. Closed upper pattern sampling uses the same phase-compensation equation as R8; the section frame itself always aligns in the locked view.

All parameter domains must be finite. Retain R8 enum/range behavior unless this contract narrows it. Active plugin validators add their fields; inactive plugin settings remain stored but do not invalidate the selected candidate.

### Common relief placement and envelopes

Every pattern plugin returns a pure raw radial field and its exact finite range `[rawMin,rawMax]` before the common keepout/envelope stage. Let `span=rawMax-rawMin`. The common `surface.reliefMode` places that unchanged shape relative to `container.outerDiameter`, which is the **base OD**:

```text
inset:    placed = raw - rawMax
          insetDepth = span; outsetHeight = 0
outset:   placed = raw - rawMin
          insetDepth = 0;    outsetHeight = span
balanced: placed = raw - (rawMin+rawMax)/2
          insetDepth = span/2; outsetHeight = span/2

baseOD = container.outerDiameter
crestOD = baseOD + 2*outsetHeight
minimumResidualWall = container.wall - insetDepth
```

`surface.depth` remains the common pattern depth input. A plugin may add a bounded shape parameter such as quilt pillow height, but it must report its raw range so placement and derived envelopes stay centralized. Pattern sampling, keepouts, fades, and phase operate on the placed field; no renderer may recompute range placement. The derived readout always displays relief mode, inset depth, outset height, base OD, crest OD, minimum residual wall, and resulting total envelope.

Require `minimumResidualWall >= surface.minWall`. `surface.minWall` is a visual design constraint, not physical proof; the Laifen preset sets it to the preserved 1.8 mm requirement and uses a nonaggressive inset depth. For outward `rugged_hex` with `outsetHeight>0.8`, validity is allowed only with nonblocking warnings that name the enlarged `crestOD` and state that overhang/support behavior is unverified. Any outward mode makes core envelope `crestOD`; total envelope is `max(crestOD,textEnvelope,attachmentEnvelope)`. The same base/crest values and relief placement continue across both core pieces and never form a seam collar.

## 8. Closure visual contract

The integrated scene and comparison card both show the active closure in an exposed seam cutaway/detail while preserving the continuous core exterior.

- `screw_thread`: render a true helical proxy over the declared engagement band with pitch equal to `screw.pitch`, turn count equal to `screw.turns`, visible lead/runout, and a rotation-plus-axial-travel arrow. Name it `closure-screw-helix-annotation`. It is an internal/cutaway visual proxy and cannot enlarge core OD.
- `bayonet_twist_lock`: render exactly `lugCount` discrete lugs, paired entry channels/ramps, capture shelf, and a twist arrow spanning `lockAngleDeg`. Name groups `closure-bayonet-lugs-annotation` and `closure-bayonet-ramps-annotation`. It must not contain helical geometry.

Text labels “Screw: rotate + axial travel” and “Bayonet: insert + twist to lock” accompany the proxies and are present in accessible text. A same-dimension automated screenshot comparison must differ, and the independent critic must identify the modes without consulting the selected control/readout. These are visual operation proxies, not mating or retention proof.

`upperLockTransform(closure, assembledState)` is a shared pure transform. Let `R=closureRotation(...)`. In locked assembled state the renderer applies upper-group world rotation `R` and zero exploded offset. The upper local section samples `support(localTheta+R)`, so its world silhouette aligns to the lower section; its pattern samples `F(localTheta+phaseCompensation,z)`, so matching on yields `F(worldTheta,z)`. In exploded/open state the upper world rotation is zero and the named exploded axial offset applies. Screw `R=2*pi*N` is still applied and recorded even when its matrix is visually identity; bayonet non-full-turn rotation must be observable in scene metadata and its lock annotation. Tests inspect the actual upper group transform, local precompensation, locked section/pattern equality, and presence/count of closure annotation geometry. A readout value without the renderer transform does not pass.

## 9. End-profile geometry

End plugins supply a deterministic meridian/profile function and cap builder. Flat, chamfer, rounded fillet, and dome are rendered at the same comparison scale.

- `flat`: side support reaches the exterior plane and a planar face closes it; size is exactly zero.
- `chamfer`: over axial extent `e`, support transitions linearly from `R-e` at the exterior face to `R`; its straight bevel is visible in silhouette.
- `rounded_fillet`: over radius `e`, a quarter-circle tangent joins a smaller planar face to the sidewall; its meridian has nonzero curvature and differs from the chamfer line.
- `dome`: with rise `e>0`, use a spherical-cap visual proxy. For local support radius `rBase`, `sphereRadius=(rBase^2+e^2)/(2e)` and cap offset at radial coordinate `r` is `sphereRadius-sqrt(sphereRadius^2-r^2)`, mirrored at the top. The dome builder spans the whole end to a curved apex and must not add a planar end-cap mesh across it.

Retain conservative R8 size limits: chamfer `0..min(R,floor,hPiece-K)`, fillet `0..min(R,floor,(hPiece-K)/2)`, dome `0..min(R/2,hPiece-K)` with nonzero size required when the selected profile is not flat. Linked edits project profile and size to both end records in one transaction; unlinked edits change only the target record.

The schema bound functions and end plugin validator both enforce these limits on each active end. `flat` requires size exactly zero. Negative, nonfinite, above-limit, or positive flat size marks the specific bottom/top size field invalid and clears all visual output. The renderer may consume only the validated derived profile; it cannot clamp or silently reinterpret an invalid value.

## 10. Surface plugins and the soft spiral

All R8 patterns remain registry entries: `smooth`, `blunt_diamond`, `recessed_diamond`, `knit_stitch`, `straight_micro_flutes`, `flowing_flutes`, `rugged_hex`, `shallow_helix`, and `wave_flutes`. R9 adds the original `quilted_diamond` entry. Existing patterns retain their global periodic equations, sign, constant-pitch behavior, keepouts, upper phase compensation, and envelope/fade logic through shared pure functions.

The user-facing label for `shallow_helix` is **Soft spiral (wide shallow helix)**. Its Advanced controls are:

| field | meaning and domain |
| --- | --- |
| `spiral.pitch` | axial travel per revolution; positive; larger values make a wider/open spiral |
| `spiral.bandWidth` | surface band width measured along the local surface; positive and below half the local circumference |
| `surface.depth` | shallow inward/outward magnitude, constrained by the common relief limit |
| `spiral.softness` | edge transition 0…1; 0 is crisp, 1 is broad/soft |
| `spiral.direction` | left or right handed visual direction |

These fields affect only the Surface pattern. They never change screw pitch, screw form, closure engagement, or closure rotation. The Basic help and comparison caption state this separation.

### Original quilted-diamond field

The supplied reference is used only to identify a general diagonal-quilt visual character. No product outline, toothbrush-head geometry, brand text, mesh, dimensions, or reference topology enters the plugin.

`quilted_diamond` reuses common `surface.axialPitch` as diamond axial pitch, `surface.arcPitch` as diamond circumferential arc pitch, `surface.depth` as groove depth, the common global phase/closure compensation, keepout, envelope, coverage, and fade metric. Its additional fields are `quilt.grooveWidth>0`, `quilt.pillowHeight>=0`, `quilt.edgeSoftness in [0,1]`, and `quilt.rotationDeg in [0,360)`. The UI/readout reports `diamondAspect=axialPitch/arcPitch`; rotation is the circumferential pattern start/orientation around the container, while the axial/arc aspect controls the physical diagonal slope.

Let `C=round(pi*(OD-2*max(depth,pillowHeight))/arcPitch)`, require `C>=3`, `u=C*(theta-rotationDeg*pi/180)/(2*pi)`, `v=(z-zPhase)/axialPitch`, `a=abs(wrap(u+v))`, `b=abs(wrap(u-v))`, and `d=min(a,b)`. Convert groove width to `w=clamp(grooveWidth/min(arcPitch,axialPitch),epsilon,0.45)`. Let `G=1-smootherstep(d/w)` and `P=smootherstep(d/0.5)` with its exponent/interpolation continuously controlled by `edgeSoftness`. Before the common envelope/keepout multiplier, return a relief bounded at or below the nominal support:

```text
quiltedDiamond = pillowHeight*P - depth*G
```

This raw quilt field ranges from recessed grooves to convex pillow centers. The common relief-placement transform then positions the full raw range as inset, outset, or balanced and derives crest OD and residual wall. Because `C` is integral and `u±v` use wrapped global coordinates, the field is periodic at `theta+2*pi` and `z+axialPitch`, is independent of the split and exploded offset, and uses the existing upper closed-phase compensation. The common depth/density envelope multiplies/activates the completed field without changing axial or arc pitch.

The quilt plugin reports `rawMin=-depth` and `rawMax=pillowHeight`; the common placement therefore uses `span=depth+pillowHeight`. Emit a nonblocking wall-depth warning when the resulting inset depth approaches the selected minimum-wall boundary; reject and clear when the common `minimumResidualWall < surface.minWall`, groove width reaches the half-cell boundary, or any field is nonfinite. Tests cover theta and Z periodicity, seam equality for screw and bayonet, all three relief placements, envelope/fade compatibility, warning and rejection boundaries, and independent sensitivity to axial pitch, arc pitch/aspect, groove width, groove depth, pillow height, softness, and rotation. Browser evidence includes one assembled and one detail/section state at desktop and 390x844 mobile; the view must read as grooved quilted pillows without importing reference brand text.

## 11. Attachment geometry and envelopes

Each accessory has a unique builder and semantic silhouette:

| ID | required geometry | identity and presentation |
| --- | --- | --- |
| `integrated_lanyard_eyelet` | one teardrop/oval eyelet with a clear opening and attach pad | belongs to selected half in fixed mode; whole eyelet offsets with a dashed assembly datum in separate visual mode |
| `captured_loop` | two small ears plus a separate oval loop passing through their pivot axis | loop is a named extra body; pivot clearance is visible; fixed/separate changes its shown assembly position |
| `separate_clip_link` | open C-shaped clip/link with a visible mouth, shown beside a receiving eye/tab | always names the clip as a separate part; fixed preview shows engaged pose, separate preview shows displaced pose and path |
| `keyring_tab` | flat radial tab with a circular through-hole | hole diameter and tab web are visible; optional metal ring is a dashed labelled reference excluded from geometry/envelope |
| `bridge_handle` | two distinct standoffs joined by a spanning bridge/arch | bridge span and standoff are visible; it cannot reuse any ring/torus builder |

`attachment.presentation=fixed|separate_visual` changes contact/offset and material/legend without changing the selected plugin or core identities. Fixed uses the core-half material at an explicit attach allowance; separate uses an accessory material, gap, and dashed assembly path. Pure accessory bounds return a full XY/Z bounding box and radial maximum. The render layer measures built vertices; validation requires its envelope to equal the pure prediction within a documented visual tolerance. `totalEnvelope=max(crestOD,textEnvelope,attachmentEnvelope)`; reference metal is excluded and labelled. Two named accessory modes may not use the same `mainBuilder` or produce pixel-identical prescribed comparison images.

`attachment.mountAngleDeg` must be finite and in `[0,360)`. NaN, positive/negative Infinity, 360, and negative values are invalid at schema and active-plugin validation; there is no implicit coercion or modulo repair of invalid input. The validated derived radians value is the only angle consumed by attachment and collision builders.

## 12. Outward-readable label contract

`sectionFrame(theta)` returns support point, outward normal, global axial up, and `outwardRight = axialUp × outwardNormal`. Horizontal glyph advance uses `outwardRight`; vertical advance uses global +Z. Canvas or glyph UV mapping must place glyph-left at negative `outwardRight` and glyph-right at positive `outwardRight`, so an observer outside along the normal reads left-to-right. No `lookAt(origin)` shortcut may flip this basis. The upper piece uses the same global frame after its locked transform.

The preview must differentiate relief visually:

- `outset`: glyph face sits at `support + relief*outwardNormal`, includes visible side/rim lighting, and casts/receives a consistent outward shadow cue.
- `inset`: glyph channel sits below the support reference, uses a dark recessed floor and inward rim/shadow, and never increases text envelope.
- a labelled same-scale section detail shows `+ relief outward` or `- relief inward`; color reinforces but is not the sole cue.

Preserve the R6 conservative label box, safe 1…48-code-point allowlist, `textContent`/canvas-only rendering, generic browser font stacks, explicit future `openScadFontFamily`, and font/glyph parity warning. Validate seam/end/closure/surface-keepout/attachment overlap for each target. `labelBoxes(state)` returns one box for lower/upper and two independent boxes for `target=both`; patch suppression tests the sampled point against **every** returned target box. Patch suppresses texture under each expanded label rectangle and restores it outside each one. A shared shortcut that selects only one target is forbidden. Invalid text clears the entire preview and exposes field-linked errors. `textEnvelope=crestOD+2*max(0,labelOutsetRelief)` before combining with the attachment envelope.

## 13. Vent & Drain module

`ventDrain.mode` is `none|bottom|top|both`. `linked=true` means edits to one drain record atomically project count, diameter, and ring radius to the other record. When mode is `both`, the Basic/Advanced UI shows one shared set if linked and two end-labelled sets if unlinked. When only one end is enabled, the inactive end values remain stored but hidden and do not generate holes.

For enabled end `q`, count is integer 1…24, diameter is positive, and ring radius is nonnegative. Count one requires ring radius zero and places one axial hole at the center; count greater than one requires positive ring radius and places centers at `theta_i=2*pi*i/count` in the shared global section frame. Bottom hole axes run +Z from the exterior end through the bottom floor; top axes run -Z from the exterior end through the top floor. End views and the section inset must show true openings through the floor, not colored discs painted on a closed face.

Define the fixed visual feasibility reference `webRef=max(0.8,min(container.wall,container.floor)/2)`. For each enabled end, shared pure math samples the minimum available support along the whole visual floor path after its end profile:

```text
rSafe = min(theta,z through floor path) outerSupport(theta,z) - container.wall
edgeWeb = rSafe - (ringRadius + diameter/2)
pairWeb = count == 1 ? +infinity
          : 2*ringRadius*sin(pi/count) - diameter
require edgeWeb >= webRef
require pairWeb >= webRef
```

The drain angular envelope must not intersect an attachment's explicit attach pad on the same half. A drain cannot cross the closure/seam band because it is confined to the relevant floor. Any failed check associates errors with that end's count/diameter/ring-radius fields and clears model, detail, scale, and envelopes. Drain subtraction never increases `baseOD`, `crestOD`, `attachmentEnvelope`, or `totalEnvelope`; validation compares before/after bounds. These checks only make the visual arrangement internally feasible. They do not prove drainage rate, cleaning, watertightness, roof/ceiling support, bridging, floor strength, slicing, or printability.

## 14. Invalid-state transaction

Input processing is one deterministic transaction:

```text
event -> typed raw nested edit -> schema structural validation
      -> active plugin validation -> deriveModel
      -> if valid: synchronize projections/readouts and render
      -> if invalid: retain editable raw state; clear scene/detail/scale/envelopes; render errors only
```

No last-valid geometry survives behind an invalid control. Every error has one stable field path and error ID. Controls receive `aria-invalid` and `aria-errormessage`; a polite live region summarizes a valid update and an alert region announces a submitted/committed invalid update without repeating on every keystroke. Switching Basic/Advanced must reveal any invalid active field or place an error summary link that focuses it.

## 15. Mobile and accessibility contract

- Semantic fieldsets/legends follow the seven modules. Every control has a visible label, unit, help association, keyboard operation, and at least a 44 by 44 CSS-pixel touch target where practical.
- Basic loads expanded; Advanced is a deliberate toggle and module sections remember only presentation expansion. Focus order follows Container through Attachment, then derived state.
- At 360x800 and 390x844 there is no page or control horizontal overflow, clipped label, unreachable submit/reset action, or canvas overlay blocking controls. The model/comparison surface precedes the long Advanced list, while the user's focused field remains in view after a change.
- Meaning never depends only on color: closure shapes/arrows, accessory silhouettes/names, text section signs, and drain end labels provide redundant cues.
- Text/background and focus indicators meet WCAG 2.2 AA contrast; `prefers-reduced-motion` disables auto-rotation and nonessential transitions. Resize and orientation changes refit the actual model plus attachment bounds.
- The main viewer has a concise accessible description of current pieces, closure, end profiles, drain ends, label mode, and attachment. Comparison images have captions; decorative mesh canvases are not exposed as dozens of nodes.

## 16. Required test and browser matrix

### Deterministic Node tests

| ID | Credible defect caught | Check |
| --- | --- | --- |
| T-R9-01 | drift between schema, DOM, state, and export | every leaf path/default/type/export key is unique and covered; generated control inventory equals active schema inventory |
| T-R9-02 | plugin silently omits or reuses behavior | each registry entry conforms, defaults validate, field paths exist, and visual hook IDs meet uniqueness rules |
| T-R9-03 | preset cloning or shallow merge loses nested defaults | patches are immutable, deep merge is deterministic, arrays/enums do not alias, applying a preset twice is idempotent |
| T-R9-04 | refactor changes accepted R8 visual accounting | all three R8 preset comparable projections and E/P/K/S bounds/section/envelope facts match their frozen values |
| T-R9-05 | UI layer owns geometry math | pure modules load under Node with no Three.js/DOM/browser global; production renderers call exported pure functions |
| T-R9-06 | screw/bayonet phase or feasibility regression | nominal/boundary domains, N 1/2/3, non-90 bayonet, closed phase equality, and inactive-field isolation |
| T-R9-07 | dome is still a flat cap | end meridian samples distinguish all four profiles; dome has curved nonplanar samples/apex and its builder contract forbids planar dome cap |
| T-R9-07A | R8 accepted invalid end sizes | flat nonzero and negative/nonfinite/above-profile-bound sizes fail per end, clear output, and never reach the renderer |
| T-R9-08 | pattern pitch/phase/fade regression | every carried pattern plus `quilted_diamond` has nominal/boundary sensitivity and global split/exploded equality; quilt periodicity/warning/fade tests pass; soft-spiral fields do not alter closure values |
| T-R9-08A | relief placement lies about wall or envelope | raw ranges map exactly for inset/outset/balanced; base/crest OD and residual wall derive centrally; Laifen 1.8 mm limit rejects; rugged outset above 0.8 warns and enlarges total envelope |
| T-R9-09 | mirrored or misplaced labels | outward frame handedness, glyph-left/right world points, lower/upper/both targets, polygon faces, inset/outset signed relief, patch restoration, collision rejection |
| T-R9-09A | `both` patch masks only upper label | sampled texture is zero inside each independent lower/upper expanded box and unchanged outside both |
| T-R9-10 | accessory names reuse one shape or lie about bounds | unique builder IDs, expected primitives/part roles, fixed/separate transforms, pure/render bound parity, core OD invariance |
| T-R9-10A | nonfinite mount angle reaches geometry | NaN, positive/negative Infinity, negative and 360 reject with attachment-angle error and cleared output |
| T-R9-11 | drain overlap or painted-hole substitution | none/bottom/top/both and link projection, counts/axes, center case, edge/pair/attachment boundaries, through-floor interval, unchanged envelope |
| T-R9-12 | invalid state leaves stale authority | active invalid cases return no derived geometry/envelope; inactive plugin values do not invalidate until activated |
| T-R9-13 | future OpenSCAD names diverge | `flattenForOpenScad` is the sole map, covers every leaf exactly once, has stable order/types, and round-trips through a test-only inverse |
| T-R9-14 | derived lock rotation never reaches scene | actual upper group matrix equals shared assembled/open transform; section/pattern precompensation agrees; required helix or lug/ramp annotation objects exist |

### Real browser matrix

| Browser / viewport | Required scenarios |
| --- | --- |
| Chromium current, 1440x1000 and 1024x900 | Basic first view; Advanced conditional controls; all presets; assembled/exploded plus actual upper lock transform; closure geometry/comparison; four end silhouettes and invalid bounds; all patterns including quilted diamond; all accessories fixed/separate and invalid angle; inset/outset plus both-target patches; drains; invalid clearing; console/page/request errors |
| Chromium mobile emulation, 390x844 and 360x800 | Basic flow, Advanced reveal, keyboard/touch targets, no overflow, viewer refit, readable comparison captions, invalid-field focus |
| Firefox current, 1280x900 | module loading, schema controls, representative screw/bayonet/end/accessory/text/drain states, errors and resize |
| WebKit current, 1280x900 and 390x844 | the same representative states, outward-readable text, responsive layout, canvas/context failures and accessibility labels |

Browser dependencies must load from repository-managed/static assets or the root workspace build, with no unverified remote CDN dependency. Every run records exact browser version, viewport, candidate fingerprint, console/page/request failures, state fixture, and screenshot hash.

### Independent visual acceptance

CRIT receives same-camera comparison sheets and integrated views. PASS requires all of the following without reading the selected dropdown as the answer:

1. screw helix and motion differ unmistakably from bayonet lugs/ramps/twist;
2. the five accessories are individually nameable and fixed/separate is visible;
3. flat, chamfer, fillet, and dome silhouettes are individually recognizable, with a curved dome face;
4. `WAVE` reads outward left-to-right and inset/outset show opposite relief;
5. bottom, top, and both drain modes show openings on the named ends;
6. Basic omits inactive tuning and Advanced reveals only tuning for the active choice;
7. two core pieces, middle split, continuous core OD/no collar, scale disclosure, and visual-only boundaries remain clear.
8. the quilted-diamond representative state reads as an original diagonal groove lattice with smooth convex pillow cells, retains constant pitch through fades, and contains no reference brand text or toothbrush-head geometry.

Any candidate change after freeze creates a new candidate fingerprint and reruns the affected independent gates. After an initial attempt plus two focused implementation repairs, reopen the design rather than broadening scope. No formal or delivery PASS can override a P1 visual failure.
