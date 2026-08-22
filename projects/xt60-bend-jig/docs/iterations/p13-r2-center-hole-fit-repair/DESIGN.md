# P13 R2 center-hole fit repair design record

## Alternatives considered and exact mate diagnosis

Complete for design handoff. The user's "middle stick" maps to the printed
`separate_printed_D_shaft_OD5p60_AF5p15_theta_0p00`, built by
`build_actuator_shaft()` from `_separate_shaft_prototype()`. The production 3MF
contains no purchased rods, and its only printed stick-like production object
is this shaft. The "center hole" maps to the shared cam-D-bore functional
interface: the matching center D bores in
`left_D_bore_cam_OD40p50_theta_0p00` and
`right_D_bore_cam_actuator_OD40p50_theta_0p00`. Both are cut by
`_cam_d_bore_cutter()` from the same source-controlled
`cam_d_bore_od`/`cam_d_bore_across_flat` profile. They are one repeated mating
interface, not the three purchased-rod lanes, the two side-entry fixed C
journals, or the side-entry keeper.

Evidence:

- `cad/p13_four_plate_three_rod/p13-3mf-provenance.json` records the 12-object
  production census, including the separate printed D shaft and both D-bored
  cams, while explicitly excluding the three purchased `OD4 x 50 mm` rods.
- `src/xt60_bend_jig/p13_four_plate_three_rod.py` defines the shaft as
  `shaft_od=5.60`, `shaft_d_across_flat=5.15` and both cam holes as
  `cam_d_bore_od=5.70`, `cam_d_bore_across_flat=5.25`; `_cam_d_bore_cutter()`
  is consumed only by the two cam builders (and the fixed thrust-land running
  relief, which must continue to be checked as an affected derived feature).
- `docs/p13-cad-source-domain-amendment.md` requires the shaft to pass through
  the two stationary cams only after the keeper and both upward-C fixed guides
  are radially released. `shaft_service_extraction_certificate()` encodes that
  exact `+X` path and explicitly rejects sending the shaft through the installed
  `ID4.80` fixed journals.
- The current nominal minimum profile clearance is only `0.05 mm` per side:
  `(5.70-5.60)/2` on the circular arc and
  `(5.25-5.70/2)-(5.15-5.60/2)` at the D flat. That is the exact interface
  contradicted by the printed assembly result.

### Alternatives evaluated

1. Enlarge a purchased-rod guide hole. Reject unless the exact failed stick is one of the three purchased rods and the exact hole has that functional role; `4.15 mm` is not universal.
2. Enlarge the D-shaft mating hole in one printed plate/keeper. Select only if the assembly sequence and geometry show that printed D shaft is the middle stick and the diagnosed printed hole is its failed mate.
3. Enlarge a round journal or keeper bore. Select only if that exact journal insertion is the observed failure.
4. Change the printed stick diameter. Disfavored because the requested smallest responsible change is the responsible hole; consider only if source evidence proves no separately controlled mating hole exists.

## Frozen selected design contract

### Selected approach and rationale

Enlarge only the shared cam-D-bore cutter profile and keep the printed shaft
unchanged:

- `cam_d_bore_od: 5.70 -> 5.75 mm`
- `cam_d_bore_across_flat: 5.25 -> 5.30 mm`

This produces a uniform `0.075 mm` nominal one-sided clearance around the
controlling D profile (`0.15 mm` diametral/profile allowance) while retaining
the existing `OD5.60 / AF5.15` shaft. It is the smallest `0.05 mm` increment to
both independent D-hole dimensions that reaches the already observed
same-process `0.15 mm` sliding-fit allowance without transferring the literal
`4.15 mm` purchased-rod bore to this interface. That coupon evidence is a
starting allowance, not physical proof for the printed-to-printed D interface;
the repaired assembly must still be printed.

Candidate calculation, reproduced with
`uv run --project projects/xt60-bend-jig python` using
`d_shaft_one_sided_lash_deg()` and the source formulas:

| Cam D bore OD / AF (mm) | Minimum one-sided D-profile clearance (mm) | One-sided lash (deg) | Hub radial wall (mm) | Disposition |
|---|---:|---:|---:|---|
| `5.70 / 5.25` baseline | `0.050` | `1.9325113633` | `2.150` | rejected by physical fit |
| `5.75 / 5.30` | `0.075` | `2.9405049698` | `2.125` | selected; passes `<=3 deg` and `>=2.075 mm` |
| `5.80 / 5.30` | `0.050` at the flat, `0.100` on the arc | `1.9325113633` | `2.100` | rejected: enlarges only the arc; the controlling flat location is unchanged |
| `5.80 / 5.35` | `0.100` | `3.9802061253` | `2.100` | rejected: exceeds the `3 deg` one-sided lash limit |

The selected values leave `0.050 mm` wall margin above the hub minimum and
`0.0594950302 deg` margin below the one-sided lash ceiling. Those are CAD
margins only; printed torque transfer, play, and wear remain physical unknowns.

### Parameters, interfaces, and datums

- Preserve the existing functional names `cam_d_bore_od` and
  `cam_d_bore_across_flat`; a shallow-D hole requires both dimensions and they
  must change together. Do not introduce a generic `center_hole` or universal
  shaft/rod clearance.
- The shared cutter intentionally changes both matching cam occurrences because
  the same shaft must traverse both. Do not split them into different fits
  without new physical evidence.
- Keep `shaft_od=5.60`, `shaft_d_across_flat=5.15`, both fixed-journal
  `fixed_groove_od=4.80`, both reduced lands `journal_land_od=4.60`,
  `keeper_id=4.80`, all rod/lane/cap dimensions, plate/hub datums, motion
  parameters, and every print-layout transform unchanged.
- The fixed thrust-land running relief currently reuses `cam_d_bore_od`; it may
  grow as a derived non-mating clearance only if source/export diff proves no
  other fixed-plate geometry changed. It is not permission to enlarge the main
  fixed C journal.

### Assumptions

- The user's physical terms refer to the only printed stick-like production
  occurrence and its repeated axial cam-hole interface, as established by the
  production 3MF census and the source-defined assembly/service sequence.
- The `0.15 mm` diametral/profile allowance is a conservative next repair target
  informed by the same PETG process, not physical proof for this D-shaped mate.
- The source-defined shaft geometry and print orientation remain unchanged, so
  a repaired reprint is still required to establish fit, play, torque transfer,
  and wear.

## Regression plan

Add a focused failing-before/passing-after regression named for the physical
defect, for example
`test_printed_D_shaft_cam_bore_fit_regression_p13_r2`. It must:

1. Assert the circular and D-flat profile allowances are each at least
   `0.15 mm` diametral-equivalent. The baseline values are both `0.10 mm`, so
   this is the required failing-before witness.
2. Build the actual male D prism and both final D-bored cam solids; prove the
   aligned shaft and the complete `+X` insertion/extraction envelope have zero
   unintended positive-volume intersection with both stationary cams.
3. Recompute and assert one-sided D lash `<=3 deg`, hub radial wall
   `>=2.075 mm`, and both cam D engagements `>=4.50 mm`.
4. Assert the unrelated-fit freeze: purchased rods/lane width, fixed C-journal
   and journal-land diameters, keeper ID/groove, all cap fits, object census,
   and source-authored print rotations remain the baseline values.

After this focused regression passes, rerun the existing D containment/escape,
staged service extraction, four-plate actual-solid collision, motion, source
dependency, STEP/3MF parity, mesh/orientation, and snapshot gates. The test may
prove the new source contract, but it must not claim that PETG fit is physically
accepted.

## Rejected or failed approaches

- Blanket enlargement of every center, rod, or shaft bore.
- Reusing the `4.15 mm` purchased-rod sliding-fit result without first proving the same role.
- Editing STEP/3MF bytes or applying slicer transforms.
- Redesigning the four-plate/three-rod architecture for a local fit defect.
- Reducing the printed shaft: it would alter both cam fit and all round
  fixed-journal/keeper lands and would violate the requested hole-only repair.

## Decisions promoted to ADRs

No architecture ADR is required: P13 R2 preserves `ADR-0001` and changes only
the current fit values in the accepted source-domain amendment. The iteration
record and amended source-domain contract retain the supersession evidence.
