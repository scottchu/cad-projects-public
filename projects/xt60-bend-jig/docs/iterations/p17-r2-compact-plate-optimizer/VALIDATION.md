# P17 R2 compact-plate optimizer validation

- Task: `O15-VALIDATE-R1`
- Role: independent read-only numeric and rendered-artifact validation
- Status: **PASS for the exact frozen P17 2D candidate**
- Scope: deterministic optimizer math, focused tests, SVG structure and PNG
  visual review only

## Candidate fingerprint

| Path | SHA-256 |
|---|---|
| `src/xt60_bend_jig/p17_compact_plate_optimizer.py` | `1d36c3809b2b0e42dfad905f5706caae15ec8c6e1110fcb5ee7b2886bc08025f` |
| `tests/test_p17_compact_plate_optimizer.py` | `da9331715e5404049f0051c6d708068833f48b839f7692d3f8f5fd372a93d303` |
| `docs/review/p17-r2-compact-plate-optimizer/p17-compact-plate-open-end.svg` | `23f93ca5500d94078edafa02742dbe49cd5542fcd446359e0be63beb073b0412` |
| `docs/review/p17-r2-compact-plate-optimizer/p17-compact-plate-open-end.png` | `4fd438bf0031128b471ebbf071bcd1a4eb4ac07d8c55e557bc0e64304d35813d` |

## Commands and results

From the repository root through the shared root `uv` environment:

```text
uv run pytest -q projects/xt60-bend-jig/tests/test_p17_compact_plate_optimizer.py
..........                                                               [100%]

xmllint --noout projects/xt60-bend-jig/docs/review/p17-r2-compact-plate-optimizer/p17-compact-plate-open-end.svg
exit 0
```

All four candidate hashes above were independently recomputed and matched.

## Independently checked derived metrics

- Raw inner diameter: `52.932202652842975 mm`.
- Raw left and right outer cutter-envelope diameter:
  `50.30769103922032 mm` each.
- Upward-rounded hierarchy:
  - inner: `52.933 mm`;
  - left outer: `53.933 mm`;
  - right force outer: `54.933 mm`.
- Minimum internal feature web: `2.5977324813688853 mm`.
- Limiting internal pair: right outer `upright` rod rail versus
  `fixed_axle` rail.
- Limiting boundary feature: fixed-inner `bottom_start` track cutter.
- Limiting track center: `(-20.8852813742, 7.5) mm`.
- Cutter-edge point:
  `(-22.838179439690173, 8.201294621257519) mm`.
- Rounded plate-edge point:
  `(-24.909097180865416, 8.944970647475733) mm`.
- Actual rounded boundary web: `2.2003986735785106 mm`, satisfying the
  required `2.20 mm`.

`CompactCandidate` now contains independent inputs only. `derive_metrics()`
recomputes the envelopes, plate hierarchy, internal web and boundary marker;
it does not trust caller-supplied derived diameter or web literals.
Falsification coverage is meaningful: supplying a derived diameter raises
`TypeError`, increasing required web changes the derived diameter, and reducing
the accepted inner diameter by one `0.001 mm` quantum fails the boundary-web
gate.

## Invariant coverage

- Exact current P17 guide identities are preserved for `bottom`, `diagonal`
  and `upright`; no rod swap, crossing, mirror or reversal was introduced.
- OPEN remains upper-left, upper-right and lower-right with the exact right
  vertical leg.
- END remains the accepted upper-left -> middle -> lower-right diagonal chain.
- FRONT orientation remains `+Z` XT60 mating-head/up and `+Y` solder-tail and
  wires/outward-right.
- The aligned wire projection is the exact fixed `└` route:
  `(-5,20.5) -> (-5,1.5) ->` lower-left quarter bend
  `-> (1,-4.5) -> (13,-4.5)`.
- The purple axle `A=(-9.5,-9.5)` remains fixed and left/behind the aligned
  XT60 center at `Y=-5.0`.
- Fixed-inner tracks remain direct straight stationary tracks.
- All six rod rails and both axle rails remain inverse-transform-derived, with
  left/right outer rotations `-45 deg/+45 deg`.
- The diameter hierarchy preserves both outer plates larger than the inner
  plates and the right force plate as the largest.
- Three `OD4 x 50 mm` stainless rods, six permanent caps and the no-extra-part,
  no-lock/no-self-lock boundaries remain unchanged by this 2D gate.

## Visual review and acceptance boundary

The exact PNG was inspected against the exact SVG. OPEN and END are shown in
one fixed FRONT frame; plate hierarchy, rod labels, fixed axle, rotation datum,
opposite twist arrows, straight inner tracks, inverse-derived outer rails and
the exact bottom-start cutter-to-rounded-plate boundary marker are visible.
The SVG is structurally valid XML.

This PASS approves only showing the exact frozen artifact as a **2D proposal**.
It does not authorize or claim 3D CAD implementation, STEP/mesh/3MF or slicer
acceptance, printability, physical fit, hand force, wobble, wire safety, heat,
springback, retention or self-lock.

## Nonblocking generalization note

The non-limiting fixed-inner `AF8.15` bore is represented in the optimizer by
an `AF/2` radial proxy rather than the exact regular-hex polygon. It is far
from the limiting boundary and internal pair for this exact candidate, so it
does not change any result above. Replace that proxy with exact hex-polygon
distance/support before using this function as a general optimizer over
arbitrary fixed-axle locations.
