# P20 R2 true fixed-rod arc-rail independent design critique

Status: **BLOCKED BEFORE SOURCE/BREP — analytic mechanism passes, but the
frozen 2D intent gate is incomplete.**

Task/role: `P20R2-CRITIC-01`, independent analytic mechanism/rail critic.
This record does not modify or approve source, BREP, STEP, white-rod outer
rails, manufacturing, print, or physical behavior.

The user-approved corrected sign gate later supersedes this receipt's
left/right sign assignment. Its radius, cutter, sampling, web and collision
magnitudes remain applicable.

## Provenance and manifest verification

- Branch observed: `codex/xt60-p20-r1-fixed-rod-reset`.
- HEAD observed: `a48c5697f9126dbb6934d764e48f2a01f6a01475`.
- Candidate-manifest file SHA-256:
  `c38fe2158b150efa946f92a6d110b56be2806a1c4dd7d933f8b50666c2a2860f`.
- `DESIGN_CANDIDATE.sha256`: all `4/4` entries independently recomputed and
  matched.
- Nested `DESIGN_INPUT_MANIFEST.sha256` file SHA-256:
  `07847a8fec788ece8c9f421225ca1301810cf619713904a7da867dfcc6674a55`.
- Nested input manifest: all `20/20` local and
  `git:<commit>:<path>` entries independently recomputed and matched.
- The P19 source input itself matched
  `41c06b8536fbf4e1bb2e9979d74de299232379b4b0ebf87ee81e93c63f581017`;
  its focused test input matched
  `c9733d7a870eb7ca84fb7b1cb4ad6ac86271e513d0eebed3bf0ff3a0118f1ffc`.

Successful verification command shape:

```text
while read expected item; do
  local paths: shasum -a 256 "$item"
  git entries: git show "$commit:$file" | shasum -a 256
done < MANIFEST
```

Result: candidate `PASS entries=4`; nested input `PASS entries=20`.

## Independent kinematic recomputation

I recomputed the candidate without importing its tabulated results.  With
`C=(0,0)`, `A=(-15,-11)`, `r=|A|=sqrt(346)`, shared `u in [0,1]`, and
physical `alpha_L=+45u`, `alpha_R=-45u` degrees, the only correct outer-local point for
the stationary axle is

```text
q_s(u) = C + R(-alpha_s(u)) (A-C).
```

The independently recomputed values are:

| `u` | `q_L=(Y,Z)` mm | `q_R=(Y,Z)` mm |
|---:|---:|---:|
| `0.00` | `(-15.000000,-11.000000)` | `(-15.000000,-11.000000)` |
| `0.25` | `(-16.857773,-7.862283)` | `(-12.565786,-13.714993)` |
| `0.50` | `(-18.067711,-4.422423)` | `(-9.648675,-15.902926)` |
| `0.75` | `(-18.583317,-0.812612)` | `(-6.360772,-17.479719)` |
| `1.00` | `(-18.384776,+2.828427)` | `(-2.828427,-18.384776)` |

Across `1001` evenly spaced states on both sides, the largest independent
world-reconstruction residual was `6.405e-15 mm`; the largest radius residual
was `3.553e-15 mm`. Relative angular separation has magnitude
`|alpha_R-alpha_L|=90u deg`, hence `90 deg` at END.

The exact arc quantities also match:

| quantity | independently recomputed value |
|---|---:|
| radius | `18.601075237738 mm` |
| 45-degree centerline arc | `14.609250328937 mm` |
| endpoint chord | `14.236646635318 mm` |
| whole-arc sagitta | `1.415922542889 mm` |

### Why the rail must be curved

For a constant local journal at `A`, the world point would be `R(alpha_s)A`,
not `A`.  At `45 deg` its displacement from the required stationary point is
the chord `14.236646635318 mm`.  Rotating the plate about `A` would instead
change the frozen rotation center and is exactly the rejected P20 R1 topology.
Because `A != C` and `alpha_s` varies, a nonconstant circular arc about `C` is
necessary.  The candidate's left/right signs agree with the P19 inverse-frame
implementation.

## Cutter, sampling, web, and interaction challenge

### Cutter and samples — PASS analytically

P19 defines a `7.60 mm` outer journal and `0.30 mm` diametral running
clearance, so `7.90 mm` is the correct fixed-axle rail width and gives
`0.15 mm` nominal radial clearance.  It must not use the white-rod
`4.15 mm` width.

With `33` centers (`32` equal chords) over `45 deg`, the independently
recomputed maximum segment sagitta is `0.001400626755 mm`; the conservative
radial clearance is therefore `0.148599373245 mm`.  This passes the analytic
fit gate.  It remains only a cutter-center approximation claim; later BREP
must prove a valid single solid and zero axle/plate intersection at the
required states.

### Boundary web — PASS analytically

Using cutter radius `3.95 mm`:

| gate | recomputed web |
|---|---:|
| left outer, OD54.70 | `4.798924762262 mm` |
| right outer, OD55.00 | `4.948924762262 mm` |
| inner OD54.40 to moved AF8.15 hex corner | `3.893520068366 mm` |

All exceed the frozen `2.20 mm` threshold.  The inner edge of each curved
outer rail stays at radius `14.651075237738 mm`, so the arc does not divide
the disk analytically.

### Purple rail versus white rods and retained inner paths — PASS analytically

Independent continuous-domain optimization of synchronized state and rail
parameter produced these raw minimum surface clearances:

- any moving `OD4` white rod: `18.509746945004 mm`;
- any retained `4.15 mm` inner-rail segment in FRONT-YZ projection:
  `18.434746945008 mm`.

Subtracting the design's declared `0.040 mm` grid/Lipschitz allowance gives
`>18.469 mm` and `>18.394 mm`, respectively, matching the candidate's
conservative claims.  Thus the purple arc does not merge with a white-rod
path analytically.  This does not replace later actual-solid collision
validation.

### Axial stack and keepers — PASS as geometry intent

Independent P19 stack recomputation gives outer-plate X intervals
`[-16.0,-12.8]` and `[12.8,16.0] mm`, keeper centers at
`X=-16.85/+16.85 mm`, and `0.25 mm` keeper-to-outer axial running gaps.  The
axle total length remains `34.90 mm`; each outer plate remains `3.20 mm`
thick.  Keeper OD10 over a `7.90 mm` slot gives `1.05 mm` radial capture.
These facts support the intended retained geometry, but they do not prove
force, torque, wear, or physical retention.

### Required zero outer cuts and six known collisions — PASS analytically

The candidate authorizes and depicts zero white-rod outer holes, windows, or
rails.  Each uncut `OD4 x 50 mm` rod spans both outer-plate X intervals.  Over
the complete P19 rod paths, the smallest full-cross-section containment
ligament in a solid outer disk is `2.630845086139 mm` on the left and
`2.780845086139 mm` on the right.  Therefore all three rods necessarily
intersect both solid outer plates: exactly the six required known collisions.
This is a deliberate non-product boundary, not a movable-mechanism result.

## Blocking finding: frozen phone intent gate is incomplete

**Severity: HIGH / downstream stop.**

The PNG is phone-readable and both true fixed-rod arcs are unmistakably
visible: black `7.90 mm` apertures with cyan/right and purple/left
centerlines, a shared OPEN point, distinct END points, `C`, `A`, outer-disk
boundary, zero white-rod outer cuts, and the axial collision stack.
`P20R2-REQ-08`'s basic rail-visibility requirement therefore passes.

However, the frozen BRIEF's mandatory 2D intent gate also requires:

- OPEN/**mid**/END positions for both side-local loci; and
- motion arrows.

The candidate SVG/PNG contains OPEN and END markers only and contains no
midpoint markers or motion arrows.  The SVG source confirms those elements
are absent.  Its label `INNER rails x3 retained` is also ambiguous in a front
projection because the frozen contract preserves three paths **per inner
plate** (`6` cuts total); it should say `x3 per plate / 6 total` or equivalent.

Per the repository rule that a failed cheap intent gate stops downstream
work, this candidate must not advance to source/BREP on the current
fingerprint.  The smallest repair is review-media/design-record only: add
clearly labeled left/right midpoints and directional arrows, clarify the
inner-rail count, then issue a new candidate manifest for another independent
check.  No equation, datum, cutter width, source, white-rod rail, or topology
change is warranted by this finding.

## Requirement coverage and disposition

| requirement | independent result |
|---|---|
| `REQ-01..03` | manifest/baseline match; zero outer white-rod cuts and retained inner paths are correctly specified |
| `REQ-04..07` | `A=(-15,-11)`, `C=(0,0)`, physical left/right `+45/-45`, inverse reconstruction, two true arcs: PASS |
| `REQ-08` | true arcs are visible, but the broader frozen phone gate lacks mandatory midpoints/arrows: BLOCK |
| `REQ-09` | no unlisted change is authorized by the design record; source preservation remains untested |
| `REQ-10` | six known rod/solid-outer collisions are analytically unavoidable; later BREP must census all collisions |
| `REQ-11` | correctly stopped before implementation |

**Disposition: BLOCKED before source/BREP.**  The analytic two-arc mechanism
is accepted with no math correction, but the current candidate fingerprint
fails its frozen 2D intent-media gate.  Reissue only after the gate contains
the required midpoints, motion arrows, and unambiguous retained-inner count.
