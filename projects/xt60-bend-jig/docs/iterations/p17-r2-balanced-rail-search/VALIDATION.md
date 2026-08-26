# P17-V14 independent design validation

Date: 2026-08-25
Role: `/root/p17_lock_validator`, independent validator
Branch / baseline: `codex/xt60-p17-r2-balanced-rail-search` / `0204c88c021e4e1667c86e967f449f2e3998fb1a`

## Verdict

**BLOCK.** The central bounded-infeasibility proof is independently confirmed: exact fixed-workpiece END contact forces `D=(0,0)`, and the fixed `A=(-29,12)` / AF8.15 inner-hex envelope then leaves only `1.615172394712 mm` to the bottom inner slot, below the frozen `2.20 mm` web gate for every `C`. The rail-only comparison near `C=(4,9.55)` is numerically reproducible but is not a design candidate.

The package nevertheless cannot pass its required cheap 2D gate: the SVG text labels the right states and values, but its red web segment and six local rail curves are schematic coordinates rather than the computed geometry. Because the artifact presents them as the D14 geometry without a schematic disclaimer, this is a wrong visual-evidence claim. This validator did not repair it.

## Frozen-input receipt

- `DESIGN_INPUT_MANIFEST.sha256` SHA-256: `cd8fa18cd1b970c6e611ea43e4e596e2cad575bd6cabb08f84f732f0b48a7892`.
- `wc -l .../DESIGN_INPUT_MANIFEST.sha256`: `18`.
- `shasum -a 256 -c .../DESIGN_INPUT_MANIFEST.sha256`: **18/18 OK** before and after validation.
- Current source SHA-256: `cef1137d68ff5dc2ed5c0131aad11c3499d71ecbc0b4afa826f6edeb7f137475`.
- Current test SHA-256: `68879bd57a03c263684576efd378ec458d853f91659d67cfb302459970b8120a`.
- D14 BRIEF / DESIGN / HANDOFF / SVG hashes: `5bea674b...` / `9993d4da...` / `af1ea464...` / `eeb27b6a...`.

## Independent hard-coded calculations

All calculation scripts ran through root `uv run --project projects/xt60-bend-jig python -`, hard-coding the I10 table rather than importing the design result.

### END contact uniquely fixes the common translation

With preserved contact sides and required center separation `3.90 mm`:

- bottom versus vertical wire: `-6.5 - (-10.4 + Dy) = 3.90`, therefore `Dy=0`;
- upright versus horizontal wire: `-2.5 - (-6.4 + Dz) = 3.90`, therefore `Dz=0`;
- diagonal consistency at `D=0`: distance from diagonal END `(-1.9849242405,2.0150757595)` to bend center `(-0.5,3.5)` is `2.100000000012 mm`; `6.00 - 2.10 = 3.899999999988 mm`.

The opposite absolute-value roots would cross to the other side of the fixed wire features and violate the frozen continuous topology. Thus `D=(0,0)` is the only permitted common translation.

### C-independent fixed-inner web blocker

For bottom OPEN `O=(-20.9852813742,9.5)`, fixed axle `A=(-29,12)`, AF8.15 conservative hex envelope, and the `4.15 mm` slot:

```text
|O-A|                    = 8.395577088607 mm
hex circumradius         = 8.15/sqrt(3) = 4.705404693895 mm
slot radius              = 4.15/2 = 2.075000000000 mm
available web            = 1.615172394712 mm
deficit from 2.20 gate   = 0.584827605288 mm
```

Neither `C` nor an outer-rail quantity occurs in this expression. Therefore broadening the `C` search cannot remove the blocker.

### Rail-only comparison, not a candidate

Independent 129-point full-rail and 33-point CONTACT-to-END polyline integration at `D=(0,0)`, `C=(4,9.55)` reproduced:

| rod | left/right full mm | full ratio | left/right CE mm | CE ratio | minimum CE crossing L/R deg |
|---|---:|---:|---:|---:|---:|
| bottom | `13.474449409 / 13.441391093` | `1.002459442` | `0.288784122 / 0.287926415` | `1.002978911` | `29.627288 / 29.724818` |
| diagonal | `10.359525994 / 11.259061785` | `1.086831752` | `0.256727315 / 0.277041080` | `1.079125843` | `21.062487 / 19.448050` |
| upright | `14.350274514 / 13.387809189` | `1.071891174` | `0.308918475 / 0.283885824` | `1.088178588` | `30.786703 / 33.861605` |

Worst full ratio is `1.086831752`, worst CE ratio `1.088178588`, and minimum CE crossing diagnostic `19.448050387 deg`. The inner-hex-to-plate-boundary margin is `2.203773315710 mm`. These reproduce the design's rail-only comparison closely enough to confirm it is not a candidate; they do not override the `1.615172 mm` invariant inner feature web.

## SVG gate inspection

XML parsing confirmed the correct FRONT label, `D=(0,0)`, `C=(4.000,9.550)`, exact body rectangle, I10 rod-state labels, and the fixed axle center/radius label.

The geometry is not exact:

- Expected conservative web segment endpoints are `(-24.508052,10.598844)` and `(-22.966151,10.117885)`, length `1.615172 mm`. The SVG draws `(-24.294,10.53)` to `(-22.97,10.12)`, length `1.386029 mm`; its start is `0.224851 mm` off the displayed hex-envelope circle.
- The six Bézier rail endpoints differ from the computed local END coordinates by `3.963` to `15.129 mm`. For example, computed bottom-left END is `(-13.134718,-5.902685)`, while the SVG path ends at `(-8,8)`.
- The SVG uses `viewBox="0 0 1200 1200"` but draws the background/content only through `y=650`, leaving an unintended blank lower region.

Consequently the SVG can be retained only if explicitly labelled schematic, or regenerated from the same analytic rail table before it serves as an exact user-confirmable 2D gate.

## Boundary and next action

No source, test, CAD, STEP, Viewer, Git, or non-validation documentation was modified. No CAD/physical/service/force/self-lock/fit claim is made. Do not implement `C=(4,9.55)`. The mathematical infeasibility result stands; separately correct or relabel the SVG through a new authorized design-worker revision, then give the unchanged/revised package a new independent validation input.

## Repair 1 visual-only rerun

**Visual repair verdict: PASS.** This does not change the design disposition: D14 still has no implementation candidate because the independently confirmed `1.615172 mm < 2.20 mm` fixed-inner web blocker remains.

- Prior receipt hashes for source, tests, BRIEF, DESIGN, HANDOFF, input manifest, and this validation file were unchanged before this append. Only the SVG changed, from `eeb27b6a...` to `3af2736fcef75302df9c7f7f886d2220db728ab65dcc0e1b22dd272af7c4cb58`.
- A root-uv XML/math check recomputed the critical web endpoints as `(-24.508052127439,10.598844175858)` and `(-22.966150702540,10.117884863095)`. SVG endpoint error was `4.25e-13 mm`; drawn/data length was `1.615172394712 mm`.
- All six rail paths contain 33 points. Hard-coded inverse-frame recomputation matched every OPEN/intermediate/END point with maximum error `6.65e-10 mm`; all six exact OPEN/END endpoints therefore pass.
- Labels, `1200x650` intrinsic size and `viewBox="0 0 1200 650"` pass. Computed diagram, rail-circle and label envelopes stay inside the canvas.
- `sips -s format png ...svg --out /tmp/.../render.png` produced an actual `1200x650` PNG, SHA-256 `056a5a13af7db517d41e56c1b5ecc37371c61f2a68f1819538a94e5c9217f32a`; visual inspection showed both panels and all labels fully visible, with no former blank lower half or clipping.
