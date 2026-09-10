# P0 v2 captured-shutter specification

All dimensions are millimetres.  X is left/right, Y is rear (-) to key/front
(+), and Z is bottom/top.  This P0 validates manual translation, aperture
closure, guidance, and rear assembly only.  It intentionally excludes springs,
magnets, a push-push latch, transfer gate, and any rigid installed plunger.

## Frozen motion contract

| Variable | Value | Meaning |
| --- | ---: | --- |
| `Y0` | 4.50 | common moving-part center at pressed/open |
| `s_in` | -1.00 | inward hard stop |
| `s_pressed` | 0.00 | pressed/open test state |
| `s_ready` | 13.40 | released/closed state |
| `s_pull_max` | 13.55 | captive maximum pull |

Every moving part uses `Y(s) = Y0 + s`.  The executable sweep is
`s = -1.00, -0.90, ... 13.50, 13.55` (147 samples).

## Aperture and shutter equations

For an aperture with center `c` and Y length `L`, its interval is
`[c-L/2, c+L/2]`.

- Fixed fill: `c=+0.5`, `23 x 10`, hence `Y=[-4.5,+5.5]`.
- Moving fill: local `c=-4.0`, `23.4 x 10.4`. At `s=0`,
  `Y=[-4.7,+5.7]`, providing 0.2 Y oversize on both ends. At ready it is
  `[+8.7,+19.1]`, under opaque housing with 0.9 front margin.
- Top shutter bounds: local `[-22.9,+2.1]`. At pressed its envelope is
  `[-18.4,+6.6]`; at ready it is `[-5.0,+20.0]` and backs the fixed fill
  with 0.5 rear margin.
- Fixed outlet: `c=+3.5`, `22 x 4.8`, hence `Y=[+1.1,+5.9]`.
- Moving outlet: local `c=-1.0`, `22.4 x 5.2`. At `s=0`,
  `Y=[+0.9,+6.1]`, providing 0.2 Y oversize on both ends. At ready it is
  `[+14.3,+19.5]`, under opaque housing with 0.5 front margin.
- Bottom shutter bounds: local `[-17.4,+2.1]`. At pressed its envelope is
  `[-12.9,+6.6]`; at ready it is `[+0.5,+20.0]` and backs the fixed outlet
  with 0.6 rear margin.

The shutters' exterior faces are at `Z=+19.9` and `Z=-19.9`, so a released
fixed opening shows a solid surface only 0.1 below the 40 mm housing exterior.
Translated moving openings sit under a continuous 0.05 opaque prototype skin.

## Captured shutter section

- Visible web: 25.0 wide x 0.8 thick.
- Lower flange: 27.0 wide x 0.4 thick, or 1.0 projection per side.
- Flange track width: `27.0 + 2(0.2) = 27.4`.
- Web slot width: `25.0 + 2(0.2) = 25.4`.
- Housing lip capture: `(27.0 - 25.4)/2 = 0.8` per side.
- Vertical flange-to-lip clearance: 0.15.
- Track-floor clearance: 0.20.
- Exterior step: 0.10; all named seams/clearances are at most 0.25.

Hidden lugs on the shutters engage clearance sockets in two shuttle bosses.
The lugs, sockets, and their closed housing channels couple the shutters in Y
without creating an exterior opening.

## Guidance and rear closure

The housing retains four rails and the shuttle retains eight short bearing
lands. Rails are 1.2 radial x 2.2 tangential with 0.20 radial running clearance.
The nominal groove is 2.7, giving `(2.7-2.2)/2 = 0.25` tangential clearance per
side; the loose coupon is 2.8.  Each rear rail entrance ramps over 0.7 and each
land has a widened/deepened 0.6 rear mouth.

The rear insertion channel is `37.3 W x 35.8 H`. The 35.2 key has 0.30
vertical clearance per side. The blind cover core is `37.0 x 35.4 x 2.4`,
flush at `Y=-20`, with 0.15 side and 0.20 vertical clearance. Four compliant
hooks use a 38.9 tip span in the 37.3 channel:
`(38.9-37.3)/2 = 0.8` extraction overlap per side. Each has a 0.7 insertion
chamfer and 1.2 cantilever thickness. There is no tool hole.

Assembly order is: rear-feed both shutters, rear-insert the shuttle while
engaging both coupling sockets, manually verify the full stroke, and snap the
blind cover last. A detachable setup wand may be used during assembly but is
not part of the sealed configuration.

## Executable acceptance checks

`tests/test_p0_v2_spec.py` freezes all interval, overlap, clearance, state,
rail, land, channel, cover, and snap equations. `tests/test_p0_v2_geometry.py`
checks valid single solids, the 147-state sweep with every named pairwise BREP
collision volume below `1e-6 mm^3`, pressed through-rays across the full fixed
apertures, released shutter backing, released translated openings under opaque
housing, blind rear-cover rays, absence of a cover tool hole, and both 2.7/2.8
coupon artifacts.

This remains a fit/feasibility prototype. In particular, the 0.05 opaque skin,
printed cantilever hooks, and near-flush 0.1 shutter step need print trials and
independent review before the model is treated as production-ready.
