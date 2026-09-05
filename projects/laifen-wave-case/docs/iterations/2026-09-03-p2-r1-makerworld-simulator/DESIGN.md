# P2 R1 MakerWorld simulator design contract

## Exact coordinate system and part semantics

All values are millimetres. The closed, assembled exterior has a global axial coordinate `z`:

```text
z = 0                         lower closed outer-end datum
z = H = 219                   upper closed outer-end datum (the top reference)
```

`split_from_top_mm = S` is measured down from `z=H` to the lower visual seam plane. Thus `z_seam = H - S`. It is the only persisted split parameter. `split_from_top_percent = 100*S/H` is derived on every render. When a percent control is edited, set `S = H*percent/100`; when the mm control is edited, recompute percent. Do not keep a second rounded source of truth.

The upper piece spans `z_seam .. H`; the lower piece spans `0 .. z_seam + P`, so they visibly/mathematically overlap through the nominal thread penetration. This is deliberately a mid-body joint. The word “cap” may appear only in a historical R7-baseline note, never as the simulator's part identity.

## Parameter contract

| Name | Class | Default | Allowed range / rule |
| --- | --- | ---: | --- |
| `device_length_mm` | inherited reference | 208 | `>0`; displayed only in this phase. |
| `axial_allowance_mm` | inherited reference | 5 | `>=3`; `C=device_length_mm+axial_allowance_mm`. |
| `floor_mm` | locked R7 reference | 3 | fixed in P2 R1. |
| `outer_diameter_mm` | locked R7 reference | 39 | fixed in P2 R1. |
| `body_bore_mm`, `upper_bore_mm` | locked R7 reference | 30, 31 | fixed in P2 R1. |
| `thread_pitch_mm` | locked R7 reference | 2 | fixed in P2 R1. |
| `thread_engagement_mm` | simulator design choice | 6 | 5..6; controls readout only. |
| `thread_penetration_mm` | derived visual band | 9 | `thread_engagement_mm + 1.5*thread_pitch_mm`; not editable. |
| `cavity_overlap_mm` | inherited axial-accounting reference | 5 | fixed in P2 R1. |
| `split_from_top_mm` (`S`) | canonical user control | 84 | 50..169. |
| `split_from_top_percent` | derived/user input adapter | 38.356164 | `100*S/H`; allowed input maps into the S range. |
| `pattern` | user choice | `blunt-diamond` | `smooth`, `blunt-diamond`, `shallow-helix`, `wave-flutes`. |
| `pattern_phase_z_mm`, `pattern_phase_theta_rad` | locked continuity datum | 0, 0 | fixed in P2 R1. |
| `skin_axial_pitch_mm`, `skin_count`, `skin_height_mm`, `plateau_half_fraction` | R7 visual reference | 4.8, 33, 0.45, 0.18 | fixed in P2 R1. |

The split range leaves at least 47 mm upper-cavity and 52 mm lower-cavity accounting length. It is a UI safety range, not a fabrication feasibility proof.

## Derived axial accounting and default readout

Let `C=device_length_mm+axial_allowance_mm`, `U=S-floor_mm`, `O=cavity_overlap_mm`, and `P=thread_penetration_mm`.

```text
closed_outer_length H = C + 2*floor_mm
upper_cavity_length U = S - floor_mm
lower_cavity_accounting_length B = C - U + O
upper_outer_length = U + floor_mm = S
lower_outer_length = B + floor_mm + (P - O)
H = lower_outer_length + upper_outer_length - P
z_seam = H - S
thread_band = [z_seam, z_seam + P]
effective_thread_band = [z_seam + 1.5, z_seam + 1.5 + thread_engagement_mm]
```

At the default, `C=213`, `H=219`, `S=84` (38.356%), `U=81`, `B=137`, `P=9`, lower outer length `144`, upper outer length `84`, and `z_seam=135`. The displayed full thread band is global `z=135..144`; the nominal effective portion is `z=136.5..142.5`. The 5 mm cavity-overlap accounting term and 9 mm visual thread penetration describe separate abstractions, so the simulator must label them separately.

## Pattern law and clipping contract

For every rendered surface sample, first calculate `z_global` in the assembled frame. Calculate its radial modifier from that global coordinate, then include the vertex only if it lies in the selected piece's global-Z interval. Never calculate a local `z` by subtracting a piece origin before evaluating the field.

For blunt diamond, use R7's visual law:

```text
u = skin_count * (theta - pattern_phase_theta_rad) / (2*pi)
v = (z_global - pattern_phase_z_mm) / skin_axial_pitch_mm
wrap(x) = x - floor(x + 0.5)
diamond = clamp((0.5 - max(abs(wrap(u+v)), abs(wrap(u-v))))
                / (0.5 - plateau_half_fraction), 0, 1)
```

`smooth` returns zero relief. `shallow-helix` is a bounded continuous sinusoid with a 0.30 mm maximum visual relief. `wave-flutes` is a bounded continuous 12-lobe azimuthal wave, with optional continuous axial modulation and a 0.30 mm maximum visual relief. Their exact implementation coefficients must be declared beside the pure math function and covered by range tests. All patterns use `z_global`; clipping at `z_seam`, `z_seam+P`, and the closed ends must not restart pattern phase.

## Readouts and warnings

The simulator must show these readouts in text, not colour alone:

- split: `S` mm and derived percent; seam global `z`;
- upper/lower outer and cavity-accounting lengths; `C` and `H`;
- full and effective thread bands in global Z, pitch and engagement;
- nominal radial reference gaps: `(30-device_diameter_mm)/2` and `(31-device_diameter_mm)/2`;
- visual skin residual wall estimate: `(outer_diameter_mm/2-skin_height_mm)-upper_bore_mm/2`;
- inherited R7 thread-root value `1.4 mm` marked as a design assumption, not a validated minimum wall.

Warn red for non-finite values, an S-range violation, negative radial gap, `axial_allowance_mm<3`, or engagement outside 5..6. Warn amber when either cavity-accounting length is below 60 mm, the visual skin residual-wall estimate is below 1.8 mm, or the user must consult CAD before treating a readout as a wall/thread claim. Do not calculate a printable-thread clearance from this visual model; show the inherited R7 `0.25 mm per-side` reference only as a non-validated note.

## Focused validation plan

| Gate | Credible defect caught | Target |
| --- | --- | --- |
| Math | percent/mm drift, wrong axial closure, negative derived length | pure `deriveSimulator()` default/boundary/round-trip tests. |
| Constraint | upper-lid topology, lost lower/upper labels, hidden warning | semantic DOM and accessibility assertions. |
| User requirement | local-coordinate phase reset at a moved split | compare global field at fixed `(theta,z)` before/after different S values; seam-neighbour samples remain equal. |
| Visual | seam or effective thread band is unclear on desktop/mobile | deterministic screenshot review at default, both S boundaries, all four patterns. |

No object-collision or actual-solid gate applies because there is no CAD solid. No CAD/export/slicer/physical acceptance follows from passing these simulator gates.

## Delta mask and implementation stop conditions

Allowed implementation change: new simulator namespace and one new static route after formal review. Forbidden: existing preview files, R7 source/artifacts, root/project indexes, requirements/decisions, existing routes, CAD Viewer route, public route and printer/slicer state.

Stop before static delivery if Three.js cannot load from the chosen declared dependency route, if global-Z continuity fails, if the user intent gate fails, or if the only route option would change an unrelated path. Record the issue and return to the smallest responsible role.
