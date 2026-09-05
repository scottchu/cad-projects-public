# P2 R2 generic threaded-container simulator contract

## Scope and coordinate semantics

This is one portable parameter model. HTML and future OpenSCAD consume the same quantities in millimetres/radians; UI labels, translated text, rendering library and browser formatting do not change its state semantics.

```text
global z = 0            lower closed outer-end datum
global z = H            upper closed outer-end datum and split reference
split S                 measured downward from z=H
seam z0 = H - S
```

The lower exterior occupies `[0,z0]`; the upper exterior occupies `[z0,H]`. These intervals touch at exactly one seam plane and must never be extended by the thread-band length. This removes P2 R1's co-planar exterior overlap. In a sectional/annotated visual, the internal mating interval is reported as `[z0,z0+P]`, never drawn as a third opaque or hidden cylindrical object.

An exploded view separates the two existing piece groups along global Z. Each group retains its own end of a dashed, labelled bracket identifying the same `P` interval. The assembled view puts one bracket outside the silhouette and two labelled ticks at `z0` and `z0+P`; both views use markers/lines only, not a surrogate thread tube.

## Language-neutral schema

The canonical object contains finite numbers, booleans, enums or `null`; there are no display strings, locale decimals or UI percentages in stored state. A future OpenSCAD customizer maps these names 1:1 to named parameters, retaining units in comments/metadata.

| Field | Type / default | Constraint and purpose |
| --- | --- | --- |
| `closed_outer_height_mm` (`H`) | number, 219 | `>0`; assembled exterior height. |
| `maximum_outer_diameter_mm` (`OD`) | number, 39 | `>0`; exterior crest/display envelope. |
| `wall_mm` | number, 2.4 | `>0`; generic nominal shell target. |
| `floor_mm` (`F`) | number, 3 | `>0`; closed-end reference floor. |
| `lower_bore_override_mm`, `upper_bore_override_mm` | `null`, `null` | optional positive reference bores; otherwise each resolves to `OD-2*wall_mm`. |
| `split_from_top_mm` (`S`) | number, 84 | canonical stored split; dynamic bounds below. |
| `thread_pitch_mm` (`p`) | number, 2 | `>0`; axial distance per turn. |
| `thread_turns` (`Nturn`) | enum 1, 2 or 3; 3 | selected effective rotations. |
| `thread_clearance_per_side_mm` | number, 0.25 | `>=0`; nominal reference readout, not fabrication clearance proof. |
| `thread_form_height_mm` | number, 0.5 | `>0`; visual thread-form reference only. |
| `lead_runout_turns` (`Lr`) | number, 1.5 | `>=0`; total non-effective lead/runout allowance in turns. |
| `smooth_keepout_mm` | number, 2.4 | `>=0`; smooth axial reservation around interface/end zones. |
| `pattern_id` | enum, `blunt_diamond` | `smooth`, `blunt_diamond`, `shallow_helix`, `wave_flutes`. |
| `pattern_axial_pitch_mm` | number, 4.8 | `>0`; physical axial pitch, never Z-scaled. |
| `pattern_arc_pitch_target_mm` | number, 3.63 | `>0`; desired physical developed arc pitch. |
| `pattern_depth_mm` | number, 0.45 | `>=0`; requested true radial relief. |
| `pattern_phase_z_mm`, `pattern_phase_theta_rad` | number, 0, 0 | global phase datum. |
| `chamfer_mm` | number, 1.2 | `>=0`; end treatment visual reference. |
| `drain_enabled`, `drain_count` | boolean/number, true/7 | count is integer `>=0`; visual open-hole indicator only. |
| `exploded` | boolean, false | view state only; never affects derivation. |

Controls use `split_from_top_percent` only as a transient adapter: `S=H*percent/100` on percent edit and `percent=100*S/H` on render. UI may round for display but must retain the unrounded Number. Bounds checks run against raw `S`; no value may become accepted/rejected because a formatted percentage string was parsed back.

## Derived model and dynamic split bounds

```text
resolved_inner_diameter = OD - 2*wall_mm
lower_bore = lower_bore_override_mm ?? resolved_inner_diameter
upper_bore = upper_bore_override_mm ?? resolved_inner_diameter
lower_wall_readout = (OD - lower_bore)/2
upper_wall_readout = (OD - upper_bore)/2

effective_engagement E = p * Nturn
full_thread_band P = p * (Nturn + Lr)
non_effective_allowance = P - E = p * Lr

K = max(smooth_keepout_mm, chamfer_mm, 0.5*pattern_axial_pitch_mm)
S_min = F + P + K
S_max = H - (F + P + K)
feasible iff H >= 2*(F + P + K) and S_min <= S <= S_max
z0 = H - S
```

`P` is a readout for the internal mating/lead/runout band. It scales with pitch and is deliberately distinct from `E`. An implementation must say “visual axial thread band” beside it; selecting a turn count does not create a verified thread profile.

If infeasible, render no false assembled split. Preserve the inputs, show `Required H >= 2*(F+P+K) = … mm; received H = … mm` and list `F`, `P`, `K`, `S_min`, and `S_max`. If `S` alone is out of range, state the valid raw-mm range. The bounds adapt on every H/floor/pitch/turn/lead/keepout/chamfer/pattern-pitch edit, which makes wide-short forms either valid or precisely rejected.

## Presets

| Preset ID | Input values that differ from generic defaults | Derived evidence |
| --- | --- | --- |
| `laifen_wave_reference` | `H=219`, `OD=39`, `wall=2.4`, `F=3`, lower/upper bore overrides `30/31`, `S=84`, `p=2`, `Nturn=3`, `Lr=1.5`, `pattern axial/arc/depth=4.8/3.63/0.45`, chamfer `1.2`, drains `true/7` | `E=6` mm = 3 turns; `P=9` mm; `K=2.4`; `S_min=14.4`, `S_max=204.6`; R7 reference only, not regenerated CAD. |
| `wide_short_makeup_jar` | `H=55`, `OD=80`, `wall=3`, no bore overrides, `S=27.5`, `p=3`, `Nturn=1`, `Lr=1.5`, `smooth_keepout=4`, pattern axial/arc/depth `8/6/0.35`, chamfer `1`, drains `false/0` | inner diameter `74`; `E=3` mm = 1 turn; `P=7.5`; `K=4`; `S_min=14.5`, `S_max=40.5`; valid at `S=27.5`. |

The control explicitly exposes 1, 2 and 3 selections. A change from one to two turns changes `E` by one pitch and `P` by one pitch; it also recomputes the split range. The makeup preset demonstrates one rotation; the Laifen reference demonstrates three.

## Pattern contract and modular API

Reference diameter `Dref=OD-2*pattern_depth_mm`; `circumference=pi*Dref`; `circumference_count=max(1,round(circumference/pattern_arc_pitch_target_mm))`; actual developed arc pitch is `circumference/circumference_count`. Thus changing length or diameter changes a count, never the requested physical axial/arc pitch by Z scaling.

For every sample, calculate `z_global` first, evaluate `radialOffset(theta,z_global,params,derived)`, then clip the vertex to `[0,z0]` or `[z0,H]`. The global phase functions must be independent of `S`, piece identity and exploded position. At fixed `(theta,z_global)`, changing S must return the same field value; samples on opposite sides of the seam follow the same phase law.

```text
PatternDefinition = {
  id, label_key, radialOffset(theta, z_global, params, derived),
  max_relief_mm(params), magnifier_description_key
}
```

- `smooth`: zero relief.
- `blunt_diamond`: current R7-style wrapped diamond with `u=count*(theta-phaseTheta)/(2*pi)`, `v=(z_global-phaseZ)/axialPitch`, and plateau fraction 0.18.
- `shallow_helix`: continuous bounded sinusoid, maximum relief is `pattern_depth_mm`.
- `wave_flutes`: continuous 12-lobe azimuthal wave with optional continuous axial modulation, maximum relief is `pattern_depth_mm`.

The full model is rendered at true requested radial depth. If depth is below `0.25 mm`, an optional separate magnifier may display a fixed 4× radial exaggeration. It must carry text such as “detail magnifier: 4× radial display; requested relief 0.20 mm; full model is true scale”, never silently inflate the main object.

## Interface/readouts and safety language

Render these in text and expose them through semantic elements: raw-mm split and derived percent; `H`, `OD`, bores, wall readouts; `E`, `P`, non-effective allowance and full/effective global-Z bands; dynamic split range and feasibility formula; pitch/turns/clearance reference; pattern count/actual pitches/depth; chamfer and drains state.

Inputs have programmatic labels/units, error and help relationships, keyboard operation and focus preservation. A single `aria-live` status reports a named valid/invalid/warning state and the reason. Do not use colour or the 3D image as the only state channel. Scene objects carry stable semantic names (`lower-piece`, `upper-piece`, `assembled-thread-band-marker`, `exploded-thread-band-marker`) so DOM/scene checks can prove there are exactly two exterior pieces and no thread-tube mesh.

Warnings must say that wall/clearance/readout values are geometric references only. Warn for non-finite/negative input, `OD<=2*wall`, bore above OD, pattern depth exceeding a wall readout, a pattern depth below magnifier threshold, and any dynamic split failure. The HTML simulator has no collision/solid/print proof; future OpenSCAD output needs fresh math, BREP/mesh, export, slicer and physical gates.

## Focused implementation tests and stop conditions

| Target | Defect it catches |
| --- | --- |
| `deriveContainer()` unit tests | wrong E/P scaling, split bounds, infeasible message, bore/wall derivation, mm/percent raw-value round trip. |
| preset tests | lost Laifen 3-turn/E6 reference or invalid 1-turn makeup jar. |
| `patternField()` tests | local-Z reset, changed phase after split/explosion, bad derived count/pitches. |
| semantic DOM/scene tests | third-thread tube, exterior overlap, omitted assembled/exploded markers, inaccessible/error-only colour state. |
| deterministic visual review | misleading shallow relief, confusing seam/band/preset layout at desktop and narrow mobile widths. |

Allowed future source changes are the new P2 R2 preview/test namespace and, after formal review only, its one isolated private route. Stop delivery if the renderer lacks two-piece/non-overlap semantics, raw conversion changes a valid boundary, the field resets at the seam, a magnifier cannot be honestly labelled, or the new route would modify an unrelated service. No generated model advances as printable from this contract.
