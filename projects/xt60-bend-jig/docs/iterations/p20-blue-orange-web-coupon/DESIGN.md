# P20 Blue-Orange web coupon design

Status: **FROZEN NUMERIC DESIGN; NOT IMPLEMENTED OR PHYSICALLY TESTED**

## Selected construction

Build one rectangular `3.20 mm`-thick plate patch in the simulator's LEFT
outer-local `YZ` coordinates. Subtract exactly two through-cut swept-capsule
rails, Blue and Orange. Each cutter has radius `2.075 mm`, uses the simulator's
exact `361` centerline witnesses (`i=0..360`, `u=i/360`), and joins consecutive
witnesses with straight swept segments and round endpoints. Do not replace the
point chain with a fitted spline. Cutter length along `X` is `5.20 mm`, centered
on `X=0`, giving `1.00 mm` through-cut overrun on each face.

The blank is the smallest **axis-aligned rectangle** that encloses both full
cutter bounds while retaining the ordinary `2.20 mm` boundary web on every
side. Only the Blue-Orange internal ligament receives the temporary exception.
This defined family avoids an arbitrary decorative outline and retains both
complete curved cutters instead of an isolated straight-gap surrogate.

## Named parameters

| Parameter | Frozen value |
|---|---:|
| `path_steps` | `360` |
| `blue_start_angle_deg` | `118.0` |
| `orange_start_angle_deg` | `45.0` |
| `start_radius_mm` | `16.0` for both |
| `inner_arch_mm` | `0.0` for both |
| `inner_arch_peak` | `0.50` (inactive because arch is zero) |
| `end_offset_y_mm` | `-7.3241343806549555` |
| `end_offset_z_mm` | `-2.77402040577638` |
| `left_end_angle_deg` | `45.0` |
| `curve_bias` | `0.0` |
| `rail_cutter_width_mm` | `4.15` |
| `rail_cutter_radius_mm` | `2.075` |
| `outer_plate_thickness_mm` | `3.20` |
| `cutter_overrun_each_face_mm` | `1.00` |
| `ordinary_min_web_mm` | `2.20` |
| `coupon_exception_web_mm` | `1.7150733085690888` (`1.72` displayed) |
| `material` | `PETG` |
| `nozzle_diameter_mm` | `0.40` |

Simulator base END centers before the shared offset are Blue
`(9.552212035894, 8.022322349948)` and Orange
`(15.802212035894, 2.272322349948)` in `(Y,Z)`.

## One deterministic geometry function

For rail `r`, let

```text
s_r = 16 * (cos(start_angle_r), sin(start_angle_r))
e_r = base_end_r + (-7.3241343806549555, -2.77402040577638)
p_r(u) = (1-u) * s_r + u * e_r
q_r(u) = R(-45u deg) * p_r(u)
u_i = i / 360, i=0..360
```

`q_r(u_i)` is the sole centerline authority for both test math and cutter
construction. The implementation must expose this as a deterministic pure
math function; BREP construction and serialization remain outside it.

Exact endpoint and sampled-extrema evidence:

| Rail | inner START | inner END after offset | LEFT local START | LEFT local END | LEFT centerline bounds `(Ymin,Ymax,Zmin,Zmax)` |
|---|---|---|---|---|---|
| Blue | `(-7.5115450045742485,14.127161485742834)` | `(2.228077655239044,5.2483019441716205)` | `(-7.5115450045742485,14.127161485742834)` | `(5.286598713468044,2.135621075408544)` | `(-7.5115450045742485,5.286598713468044,2.135621075408544,14.127161485742834)` |
| Orange | `(11.313708498984761,11.313708498984760)` | `(8.478077655239044,-0.5016980558283803)` | `(11.313708498984761,11.313708498984760)` | `(5.640152104061318,-6.349660298830027)` | `(5.640152104061318,12.033446371474318,-6.349660298830027,11.313708498984760)` |

The frozen simulator witness is Blue `i=360, u=1` at
`(5.286598713468044,2.135621075408544)` and Orange
`i=209, u=209/360` at `(10.641121565936023,-0.2577384749490106)`.
Their center distance is `5.8650733085690888 mm`; subtracting two cutter
radii gives `1.7150733085690888 mm`. The witness midpoint is
`(7.963860139702033,0.9389413002297666)`.

## Coupon envelope

The full two-cutter union has sampled bounds:

```text
Y = [-9.586545004574248, 14.108446371474319]
Z = [-8.424660298830027, 16.202161485742835]
```

Adding `2.20 mm` on all four sides freezes the blank as:

```text
X = [-1.600000000000000, 1.600000000000000]
Y = [-11.786545004574247, 16.308446371474318]
Z = [-10.624660298830026, 18.402161485742834]
size X x Y x Z = 3.20 x 28.094991376048565 x 29.026821784572860 mm
YZ center = (2.2609506834500355, 3.888750593456404)
```

No label, notch, hole, fixed-axle feature, Green rail, or decorative rounding
may enter this envelope. A non-geometric color/metadata label may identify the
artifact and witness, but engraving is forbidden because it could change local
stiffness or print continuity.

## Focused validation gates

1. **Math:** named function is deterministic; endpoints and all `361` witness
   points per rail match the immutable simulator equations within `1e-12 mm`.
   Blue `360` / Orange `209` reproduces center distance
   `5.8650733085690888 mm` and reported boundary gap
   `1.7150733085690888 mm` within `1e-12 mm`.
2. **Constraint:** parameters equal the table; blank bounds and thickness match
   within `1e-9 mm`; every ordinary outer-edge web is `>=2.20 mm`; exactly the
   named Blue-Orange ligament is allowed below `2.20 mm`.
3. **Actual solid:** one valid, closed, positive-volume solid; exactly two
   separate through-slots; no cutter-cutter intersection; BREP minimum surface
   distance must be within `1.714..1.716 mm` and round to `1.72 mm`. The narrow
   tolerance admits the sub-`0.001 mm` distinction between sampled witnesses
   and straight segments while forbidding geometry refit or drift.
4. **User requirement:** artifact contains Blue and Orange only; fixed axle,
   Green, other rails, plate/assembly features, and simulator changes are
   absent. A source-tree check must show no changed path outside the authorized
   new coupon/evidence namespace.
5. **STEP/export parity:** STEP and 3MF each contain one coupon with matching
   volume/bounds after only the declared rigid print-orientation transform;
   mesh is manifold, positive-volume, support-free, and placed with a broad
   face at build `Z=0`.
6. **Visual:** FRONT close-up shows both complete rails and the marked witness;
   oblique and bottom views show two open through-slots and continuous material.
   Snapshot inspection is required but does not prove physical survival.
7. **Physical:** use the exact question and evidence record in `BRIEF.md`.
   Digital acceptance remains separate; a pass cannot approve the full profile.

## Risks and non-goals

- The `1.715073... mm` value is the simulator's discrete witness result. The
  physical coupon uses connected swept segments, so actual-solid distance may
  differ by a few ten-thousandths of a millimeter; the BREP gate records it
  rather than falsifying exact equality.
- A flat coupon does not reproduce the full plate rim, neighboring rails,
  mechanism loads, cyclic force, heat, creep, stress concentration from other
  features, or assembly constraints.
- It does not select slicer settings or authorize upload/start of a print.
- It does not change P20 R3, P20 R2, product versioning, current authority, or
  the immutable simulator.
