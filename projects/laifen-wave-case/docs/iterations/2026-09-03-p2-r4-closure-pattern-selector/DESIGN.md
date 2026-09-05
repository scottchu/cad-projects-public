# P2 R4 exact visual-intent design contract

## Frozen baseline and delta mask

Baseline candidate is P2 R3 manifest `15c7c0503e87ec0f0b1a828fb62d471baaefc9a6caecf629d14d4504d0d19224`. The implementation may change only the generic simulator source/test and new P2 R4 receipts/manifests. It may not alter P1 R7, any CAD/STEP, the P2 R3 served copy, routes/services, project continuity files, or prior evidence.

The existing `raw` object remains the single canonical parameter state. Every successful input transaction is `event → raw mutation → deriveContainer(raw) → sync controls from canonical raw/derived state → render`. Invalid active text stays editable but does not become authority; invalid state clears scene/detail/scale and emits field-associated errors.

## Parameters and domains

All lengths are millimetres and angles are degrees. Existing parameter domains remain unless stated here.

| canonical field | domain/default | meaning |
| --- | --- | --- |
| `closureMode` | `screw_thread` default; enum | selects annotation/accounting family |
| `p`, `N`, `Lr`, `formHeight`, `clearance` | existing retained domains/defaults | screw pitch, 1/2/3 turns, lead/runout turns, visual form-height reference, radial clearance per side |
| `bayonetLockAngle` | `5 < a < 360/lugCount`; default 90 | twist from entry to locked state |
| `bayonetLugCount` | integer 2…8; default 3 | repeated lug/slot count |
| `bayonetCapture` | `0.25…10`; default 2.0 | axial capture/engagement after ramp |
| `bayonetRampRise` | `0…10`; default 1.0 | axial rise from entry to capture |
| `bayonetClearance` | `0…2`; default 0.30 | visual radial clearance per side |
| `pattern` | existing four plus `recessed_diamond` | global pattern selection |
| `depth` | `0…min(lowerWall,upperWall)-0.20`; default existing | recess/relief reference depth |
| `endProfile` | `flat`, `chamfer`, `rounded_fillet`, `dome`; default `chamfer` | external end family |
| `linkedEnds` | Boolean; default true | one size applies to both ends |
| `bottomEndSize`, `topEndSize` | profile-specific, defaults 1.20 / 1.20 | lower/upper closed-end size; linked mode writes both from edited size |

`flat` requires sizes exactly 0. `chamfer` requires `0 ≤ e ≤ min(R, F, h_piece-K)`. `rounded_fillet` requires `0 ≤ e ≤ min(R, F, (h_piece-K)/2)`. `dome` requires `0 ≤ e ≤ min(R/2, h_piece-K)`. Here `R=OD/2`; `h_lower=H-S`, `h_upper=S`; `K=max(keepout,chamfer,axial/2)`. At either invalid end input, the full preview clears. The current R7 behavior maps to `endProfile=chamfer`, `linkedEnds=true`, and both sizes 1.20; it is a visual migrated preset, not an R7 modification.

## Derived closure accounting and feasibility

For screw mode, retain:

```text
E_s = p*N
P_s = p*(N+Lr)
K = max(keepout, chamfer, axial/2)
B = P_s
Smin = F + B + K
Smax = H - (F + B + K)
require H >= 2*(F+B+K), Smin <= S <= Smax.
```

For bayonet mode:

```text
slotPitch = 360/lugCount
require 5 < bayonetLockAngle < slotPitch
E_b = bayonetCapture
P_b = bayonetRampRise + bayonetCapture
B = P_b
Smin = F + B + K
Smax = H - (F + B + K)
require H >= 2*(F+B+K), Smin <= S <= Smax.
```

The displayed bayonet twist is `a=bayonetLockAngle`, entry/lug radial reference is `R-bayonetClearance`, and lock ramp is a non-solid annotation with axial progression `z(t)=z_entry + t*bayonetRampRise`, `t∈[0,1]`, followed by `bayonetCapture`. Annotation count equals `bayonetLugCount`; it never creates a third exterior tube. Screw parameters retain values in bayonet mode but do not determine its closure band; bayonet controls retain values in screw mode but do not determine its closure band.

## Global recessed-diamond field

No pattern can derive phase from either part's local height, current split, or exploded offset. Let `theta0` and `zPhase` be global constants, `C=round(pi*(OD-2*depth)/arc)`, `u=C*(theta-theta0)/(2*pi)`, `v=(z-zPhase)/axial`, `wrap(x)=x-floor(x+0.5)`, and:

```text
q = max(abs(wrap(u+v)), abs(wrap(u-v)))
dDiamond = clamp((0.5-q)/(0.5-g), 0, 1), with g=0.14
recessed_diamond(theta,z) = -depth * smoothstep(0,1,dDiamond)
```

The negative sign is mandatory: recessed diamonds cut inward from the base cylinder with non-recessed crossing ridges. This makes the pattern distinct from the existing positive `blunt_diamond`. `axial` and `arc` are physical pitches, not repeat counts, so changing H adds/removes whole/split repeats without Z-scaling. The same `(theta,z)` must return the same field for lower/upper parts before/after split and exploded rendering. Smooth keepout multiplies this field by an end/seam fade derived only from global distance to `z=0`, `z=H`, and `z=H-S`; it may fade magnitude but never reset phase.

## Required implementation tests

| ID | credible failure caught | deterministic check |
| --- | --- | --- |
| T-R4-01 | extra/collapsed parts | valid scene has exactly `lower-piece` and `upper-piece`; seam is a marker only |
| T-R4-02 | old screw regression | screw `E_s`, `P_s`, domains and P2 R3 split/ArrowUp trace remain exact |
| T-R4-03 | unsafe bayonet state | limits reject noninteger lugs, angle outside `(5,360/lugs)`, negative capture/ramp/clearance, and infeasible H/S |
| T-R4-04 | quarter-turn not represented | default bayonet yields angle 90, 3 lugs, `E_b=2`, `P_b=3` |
| T-R4-05 | copied/locally reset recess pattern | field is negative in a diamond interior, equal at same global theta/z across split/exploded objects, and has constant axial/arc pitch |
| T-R4-06 | end profile spills into seam/bores | exact end bounds reject values above R/F/piece-height limit; sidewall/seam OD remains base OD |
| T-R4-07 | linked ends desynchronize | linked edit writes both canonical sizes; independent edit changes only requested end |
| T-R4-08 | invalid image misleads user | invalid closure/end/pattern domain clears canvas, detail and scale and reports controls with `aria-invalid`/error association |
| T-R4-09 | visual regression | browser screenshots at Laifen, wide-short screw, wide-short bayonet and each end family retain visible two-piece framing, controls, labels, true-scale and magnifier disclosure |
| T-R4-10 | forbidden scope drift | candidate manifest and diff prove only allowed simulator/test/R4 files changed; P1 R7 and routes/services untouched |

## Review and delivery boundary

IMP freezes a candidate manifest after cheap math/DOM tests. VAL independently tests pure math and actual browser state; CRIT independently reviews the two-piece/topology, closure labels, original pattern identity, end-family comprehension and mobile presentation. REV joins their exact manifests and receipts. Only after formal PASS may DEL copy the reviewed static bytes to an isolated private route and test the actual private page. No delivery result validates the user's device or any physical/container claim.

## Frozen amendment — closure rotation, knit, and envelope

Add pure functions `closureRotation(mode,N,lockAngleDeg)` and `upperPhaseCompensation(match,rotation)`. They return radians: screw is `2*pi*N`; bayonet is `lockAngleDeg*pi/180`; compensation is rotation when matching and zero otherwise. With upper open local angle `phi`, `R=closureRotation`, `Delta=upperPhaseCompensation`, and global selected field `F`, the upper material field is `F(phi+Delta,z)`. At closed world theta `phi=theta-R`, so `upperLocked(theta,z)=F(theta-R+Delta,z)` and lower is `F(theta,z)`. Therefore matching gives exact same global seam phase for screw N=1/2/3 and any valid bayonet lock angle. The readout names mode, locked rotation, open precompensation and residual; matching residual is `0° (visual phase)`. In exploded/open state it shows `F(theta+Delta,z)`. No local-Z reset and no physical invisibility claim.

Add `knit_stitch` with no imported mesh: `u=C*(theta-theta0)/(2*pi)`, `v=(z-zPhase)/axial`, `row=floor(v)`, `stagger=(row mod 2)*0.5*stitchTightness`, `x=wrap(u-stagger)`, `y=wrap(v)`, `loop=exp(-((x/(0.33+0.12*stitchTightness))^2+((abs(y)-0.23)/(0.22+0.10*stitchTightness))^2))`, and `knit_stitch=depth*clamp(loop,0,1)`. `arc`, `axial`, and `depth` remain width, row height, and shallow relief; `stitchTightness∈[0,1]` is the only added stitch control. It uses global theta/Z and the same closure compensation/keepout pipeline as every pattern.

Add `patternEnvelope∈{full,fade_from_bottom,fade_from_top,center_band}`, `patternCoverage∈(0,1]`, and `fadeMetric∈{depth,density}`. Let `smootherstep(t)=clamp(t,0,1)^3*(10-15*clamp(t,0,1)+6*clamp(t,0,1)^2)`, `q=z/H`, and coverage `c`. The continuous envelope weight is `1` for full; `smootherstep(q/c)` bottom; `smootherstep((1-q)/c)` top; and `smootherstep((c/2-abs(q-.5)+c/2)/(c/2))` center. `depth` metric returns `field*weight`; `density` uses deterministic cell activation `weight >= fract(hash(cellU,cellV))` while preserving the original cell pitch. Existing global end/thread/seam keepout multiplies the result afterward. Laifen defaults full; wide-short may default bottom fade. Envelope cannot Z-scale or alter `arc`/`axial` pitches.

Add tests: exact locked seam equality for screw N1/2/3 and bayonet 90/non-90 when match on; normalized nonzero residual when off; knit same-theta/Z equality across parts and sensitivity to arc/axial/depth/tightness; envelope boundary values, monotonic bottom/top fades, symmetric center band, fixed pitch under all envelopes, and invalid parameter clearing.

Add `straight_micro_flutes` with `fluteCount` integer 8…180 (or `fluteAngularPitch=2*pi/fluteCount`), `fluteDuty∈(0.05,0.95)`, and shared `depth`. With global theta and upper phase compensation, `w=fract(fluteCount*(theta-theta0)/(2*pi))`; `straight_micro_flutes=-depth*smootherstep((fluteDuty-w)/fluteDuty)` when `w<fluteDuty`, otherwise zero. It is independent of z before the shared global keepout/envelope multiplier, so it has straight axial flutes, constant angular pitch, and exact closed seam matching through the same `upperLocked` mapping. Test count/duty/depth sensitivity, global seam equality for both closure modes, envelope preservation, and invalid enum/domain clearing.

All patterns use a base cylindrical radius whose maximum is `OD/2`. Positive relief may never exceed that radius; recesses go inward. Closure bands/lugs remain annotations inside or at the base radius. The seam receives only the fine joint marker: never a raised collar or thicker thread zone. No lanyard, loop, hole, or other hardware is added from visual references.

Optional `accessoryMode` is `none|integrated_lanyard_eyelet|captured_loop|separate_clip_link`; `attachHalf` is `upper|lower`; numeric `loopOpeningWidth`, `loopOpeningHeight`, `memberThickness`, and `pivotPrintClearance` must be finite and positive, with `memberThickness < min(openingWidth,openingHeight)/2` and clearance nonnegative. `none` adds no object. Eyelet belongs to one core piece and is an intentional extension outside core OD; `captured_loop` is a third visual body; `separate_clip_link` is a separate visual part. Core remains exactly lower/upper pieces regardless. The readout reports `coreMaxOD=OD` and `accessoryMaxEnvelope=max(OD, OD+2*(memberThickness+pivotPrintClearance))`; it never hides the added envelope. Validate no accessory/core unexpected overlap except an explicit attach interface, invalid-state clearing, and mode/attach/envelope changes. No physical print-in-place, support-free, collision-free, strength, or lanyard claim.

Add original `rugged_hex` without copied geometry: with global `u=C*(theta-theta0)/(2*pi)`, `v=(z-zPhase)/axial`, `h=1-max(abs(wrap(u)),abs(wrap(v)),abs(wrap(u+v)))`, return `depth*clamp(h,0,1)` before global keepout/envelope/phase compensation. Test periodicity, seam matching, pitch sensitivity and enum/domain handling. It is visual only.
