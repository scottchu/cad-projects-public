# P1 upright rim-fin optical specification

## Status and scope

This document freezes the optical architecture for the next simulator and CAD
revision. It defines geometry and executable math only. It does not select the
final carrier drive, clock movement, LED mount, or manufacturing method.

The accepted mechanism uses hidden concentric carriers with one small upright
blocker fin on each carrier rim. It explicitly rejects conventional flat clock
hands.

All dimensions are millimetres.

## Coordinate system and stack

- Wall plane: `z = 0`.
- Positive `z`: outward from the wall toward the room/viewer.
- Optical axis: the `z` axis.
- Point-source approximation: `S = (0, 0, 68)`.
- The LED emits toward `-z`. A wide-angle single emitter is preferred over a
  true omnidirectional source because useful power must go toward the wall.
- Quartz movement and carrier supports stay near the axis and behind the
  central optical mask.
- Three carrier rings are parallel to the wall. Their working geometry is
  hidden inside the projected central mask.
- Each blocker is a constant-radius upright fin extending in `+z`, toward the
  LED.
- The fin broad face spans the tangential and axial directions. Its normal is
  approximately radial, facing the source. A radial-axial plate would present
  only its thin edge to the source and is not the intended blocker.
- A room-side glare cap sits in front of the LED. It must not be placed between
  the LED and wall.

## Projection model

For an ideal point source at axial coordinate `S_z`, a fin centreline point at
radius `r`, azimuth `theta`, and axial coordinate `z` is:

```text
P = (r cos(theta), r sin(theta), z)
```

The source-to-point ray intersects the wall at radial distance:

```text
R(r, z, S_z) = r * S_z / (S_z - z)
```

Therefore a fin held at constant radius but spanning `z_base .. z_tip` casts a
radial shadow interval:

```text
R_start = R(r, z_base, S_z)
R_tip   = R(r, z_tip,  S_z)
L_shadow = R_tip - R_start
```

The inverse used to size a fin for a required projected radius is:

```text
z_for_projected_radius(r, R_target, S_z)
    = S_z * (1 - r / R_target)
```

The projected tangential width of a fin of physical tangential width `w` at a
particular `z` is:

```text
W(r, z, S_z, w) = w * S_z / (S_z - z)
```

This is the core design principle: axial fin height becomes radial shadow
length. The blocker itself does not need to be a long radial hand.

## Numeric starting geometry

Use `S_z = 68`. All three shadows begin at a projected radius of exactly `48`.
Their tips intentionally end at three distinct radii.

| Hand | Fin radius `r` | Base `z` | Tip `z` | Fin height | Projected start | Projected tip | Visible radial length |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hour | 30 | 25.500000 | 44.000000 | 18.500000 | 48 | 85 | 37 |
| Minute | 35 | 18.416667 | 46.363636 | 27.946970 | 48 | 110 | 62 |
| Second | 40 | 11.333333 | 47.076923 | 35.743590 | 48 | 130 | 82 |

The decimals above are derived rather than independently tuned:

```text
z_base = 68 * (1 - r / 48)
z_tip  = 68 * (1 - r / R_tip)
```

Initial fin section:

- radial thickness: `1.6` (`r +/- 0.8`);
- tangential width: `2.4`;
- rounded wallward and sourceward edges: `R0.6` maximum;
- one fin per carrier;
- no counter-fin, X, star, or spoke outside the central mask.

The projected tangential widths at each tip are:

- hour: `6.80`;
- minute: `7.542857`;
- second: `7.800000`.

These are starting values for physical shadow legibility, not final aesthetic
widths.

## Carrier and collision envelopes

Use carrier/fin radial envelopes:

- hour: `29.2 .. 30.8`;
- minute: `34.2 .. 35.8`;
- second: `39.2 .. 40.8`.

Adjacent radial clearance is `3.4`. Because every moving feature belonging to
one carrier remains inside its own radial envelope, the fins cannot collide at
any relative clock angle even though their axial ranges overlap.

Initial carrier ring section:

- radial width: no more than `1.6`;
- axial thickness: no more than `1.2`;
- its centre plane is the matching fin base `z`;
- all hubs, ring webs, fasteners, and drive details must remain inside the
  projected central mask.

Minimum deterministic checks:

1. Every adjacent radial-envelope gap is at least `3.0`.
2. Pairwise carrier/fin intersection volume is zero at coincident azimuths and
   at a swept set of relative angles over `0 .. 360 degrees`.
3. Each fin is one connected solid with its carrier attachment.
4. Nothing except the intended upright fin projects beyond the mask shadow.

## Fixed mask and open optical cone

Use a projected central mask radius of `50`, slightly beyond the common
`48`-radius fin bases. A suitable first mask plane is `z_mask = 6`, giving:

```text
mask_physical_radius
    = 50 * (68 - 6) / 68
    = 45.588235

mask_physical_diameter = 91.176471
```

The mask must be wallward of every fin base. It hides the quartz body, carrier
rings, hubs, and the lower ends of all three fins.

The annular optical path from LED to wall must remain open. For a desired wall
radius `R_wall`, the ray-cone radius at plane `z` is:

```text
cone_radius(z, R_wall, S_z)
    = R_wall * (S_z - z) / S_z
```

For a `130` wall radius and an opaque cylindrical shell of radius `55`, the
ideal limiting shell lip is `z = 39.230769`. Add manufacturing and alignment
margin: the wall-facing edge of such a shell must be at `z >= 41`. The region
from that lip to the wall must be open, flared beyond the cone, or supported
only by members hidden inside the central mask. A radius-55 opaque tube running
all the way to the wall would clip the projected clock and is prohibited.

## LED baffle and glare-cap rules

- Put the single small emitter on-axis at `z = 68`, facing the wall.
- The required outer wall radius `130` subtends `62.386972 degrees` from the
  axis. Keep a clear half-angle of at least `65 degrees` from the LED toward the
  wall.
- Any annular baffle lip a distance `d` wallward of the emitter must satisfy:

```text
baffle_clear_radius(d) >= d * tan(65 degrees) + 1.0
```

- Example: at `d = 3`, the clear radius is at least `7.433521`, or a clear
  diameter of at least `14.867042`.
- Use a matte-black room-side cap of initial diameter `20 .. 24`, positioned
  entirely in front of the emitter (`z > 68`). It blocks direct viewer glare
  but cannot intrude into the wallward 65-degree optical cone.
- Interior surfaces outside the useful cone should be matte and dark. Do not
  use a reflector, TIR lens, diffuser, LED strip, or large COB in the point
  projection path.
- LED die size and aperture remain physical-test variables. They control
  penumbra but do not change the geometric centreline equations above.

## Explicitly rejected flat-hand architecture

The previous flat XY blades were conventional clock hands lying parallel to
the wall. They were wrong for this concept because:

1. their visible radial length came from an already-long printed blade rather
   than optical magnification of a compact rim blocker;
2. they exposed the mechanism outside the central mask;
3. they did not match the orbit-clock and magnet-clock references, whose
   carriers are hidden and whose functional blockers rise at the carrier rim;
4. they encouraged X/star/spoke geometry and large moving collision envelopes;
5. they failed to demonstrate the intended relationship between axial blocker
   height and projected radial shadow length.

No future P1 model or simulator may represent the functional hands as flat XY
blades.

## Callable math API contract

The simulator/CLI implementation must expose pure callable functions equivalent
to:

```text
projected_radius(source_z, fin_radius, point_z) -> radius
fin_z_for_projected_radius(source_z, fin_radius, projected_radius) -> z
fin_shadow_interval(source_z, fin_radius, base_z, tip_z)
    -> {start_radius, tip_radius, shadow_length}
projected_tangential_width(source_z, physical_width, point_z) -> width
projected_mask_radius(source_z, mask_radius, mask_z) -> radius
required_mask_radius(source_z, projected_radius, mask_z) -> radius
cone_radius(source_z, projected_wall_radius, plane_z) -> radius
baffle_clear_radius(distance_from_source, half_angle_degrees, margin) -> radius
radial_envelope_clearance(inner_envelope, outer_envelope) -> clearance
```

All functions must reject nonphysical ordering, including `source_z <= point_z`,
negative radii, negative widths, and mask/carrier planes outside `0 < z < S_z`.

## Required regression cases

The following values are normative:

1. `projected_radius(68, 30, 25.5) == 48`.
2. `projected_radius(68, 30, 44) == 85`.
3. `projected_radius(68, 35, 18.416666667) == 48` within `1e-6`.
4. `projected_radius(68, 35, 46.363636364) == 110` within `1e-6`.
5. `projected_radius(68, 40, 11.333333333) == 48` within `1e-6`.
6. `projected_radius(68, 40, 47.076923077) == 130` within `1e-6`.
7. Shadow lengths are `37`, `62`, and `82` within `1e-6`.
8. `projected_tangential_width(68, 2.4, 44) == 6.8`.
9. `projected_tangential_width(68, 2.4, 46.363636364) == 7.542857143`.
10. `projected_tangential_width(68, 2.4, 47.076923077) == 7.8`.
11. `required_mask_radius(68, 50, 6) == 45.588235294`.
12. `projected_mask_radius(68, 45.588235294, 6) == 50`.
13. `cone_radius(68, 130, 39.230769231) == 55`.
14. `baffle_clear_radius(3, 65, 1) == 7.433520762` within `1e-6`.
15. Both adjacent radial-envelope clearances equal `3.4`.
16. Sweeping all three carriers independently through a representative full
    cycle produces zero pairwise collision volume.
17. A source-axis offset of zero keeps every projected hand radial and centred;
    a nonzero source offset must be reported as a warning and exercised by a
    separate projection-offset test.
18. Source, mask, carrier, fin-tip, and wall planes obey the required ordering
    for every point used by the solver.

Passing these equations validates ideal point-source geometry only. LED source
size, brightness distribution, carrier runout, wall flatness, print tolerance,
and room visibility require the physical P1 test fixture.

## Carrier-pitch simulator variable

The simulator exposes `carrierPitch = 4.00..5.75 mm` in `0.25 mm` steps,
defaulting to `4.75 mm`. The compact simulator source distance defaults to
`60.0 mm` with an audited `52.0..75.0 mm` range. The hour lane stays at `r30`; minute and second are
`30 + pitch` and `30 + 2*pitch`. Adjacent clearances are
`pitch - finRadialThickness`.

Every base and tip z plane is re-derived with the unchanged projection target:

`z = sourceZ * (1 - carrierRadius / projectedWallRadius)`.

Pitch therefore changes the physical radial lanes without changing the
accepted wall-shadow radii. Browser and Python expose matching pure helpers for
carrier radii and LED-to-nearest-fin axial gap, and the CLI accepts
`upright-optics --carrier-pitch`.
