# P13/P21 parametric implementation contract

The authoritative source is `src/xt60_bend_jig/p13_four_plate_three_rod.py`.
`P13Parameters` is the sole immutable primary-parameter schema. Generated
STEP and image files are derivatives and are never hand-edited.

Frozen Gate-0 source: `docs/p13-four-plate-three-rod-brief.md`, SHA256
`9c2102114cbf87ccabaa4388ed3814b91cdf3f8f654c775f5ddd8a5d05272322`,
with accepted controlling amendment
`docs/p13-cad-source-domain-amendment.md` SHA256
`b50e850ac5425fe7bad0e49555de10b0e30f63e04934bdbf66d4220f44e1f590`.

## Primary and derived groups

| Group | Primary fields | Named derivations / consumers |
|---|---|---|
| Purchased stock | `rod_diameter`, `rod_length` | exact three rods, cap frames, axial coverage, `rod_withdrawal_distance` |
| Workpiece | `wire_diameter_design`, `wire_x`, bend/strip/cup/body fields | one connected completed 90-degree workpiece, solder joints, removal sweep |
| P21 pivot | `shaft_od`, `wire_diameter_design`, `c_sw`, `bend_radius`, bend centre, `horizontal_z` | `initial_arc_distance`, `pivot_delta`, `shaft_y`, `shaft_z` |
| Motion | `wire_preload`, guide directions, passage/follower allowances | tangent `contact_centres`, three `stroke_requirements`, derived `contact_stroke` + preload `common_stroke`, inverse cam paths |
| Plates | OD/thickness/gap/spacing/lane fields, `fixed_thrust_land_height`, `cam_thrust_land_height` | all four concentric blanks, fixed-only lands, lanes, upward C-journals, `nominal_thrust_land_gap`, rim checks |
| Actuator | shallow-D shaft, bore, head, groove, and engagement fields | one separate printed `OD5.60 / AF5.15` D shaft with stop head; matching `OD5.70 / AF5.25` bores and outward hubs on both cams |
| Normal removal | `rod_exit_clearance`, `removal_end_clearance` | synchronous `rod_withdrawal_distance`, `mechanism_top_z`, `completed_workpiece_min_z`, `removal_lift` |
| Retainers | keeper and cap profile fields | one keeper, three permanent left caps, three removable right caps |
| Diagnostics | coupon values/sizes | one-solid lane and bore coupons; never production selectors |
| Presentation | exploded/print/service offsets and camera jobs | repeatable evidence only; no production stock or cutter changes |

`docs/p13-default-parameter-manifest.json` serializes every primary field,
unit, class, value, and named derived result. `docs/p13-dependency-graph.json`
maps every primary field to its derived data, solids, states, tests, and
exports. Every STEP root label records the Gate-0 brief hash, parameter
manifest hash, and source revision hash.

## Retune boundary

Safe retunes include `c_sw` only over `0.50..0.75 mm`,
`wire_diameter_design` only over `4.20..4.30 mm`, and the declared diagnostic
profile/coupon fields. Every retune still requires clean regeneration,
metamorphic formula checks, BREP checks, source/export parity, and independent
review. Shaft OD, bend radius, topology, occurrence count, operation order,
and workpiece angle are re-Gate fields.

## Frozen nominal invariants

- four OD40.50 circular principal occurrences from three printable definitions;
- retained `main_face_gap = 0.30 mm`, fixed-side `OD10 x 0.20 mm` thrust
  lands, conditionally omitted `cam_thrust_land_height = 0`, and exact derived
  `nominal_thrust_land_gap = 0.10 mm` for both facing pairs;
- authored principal print rotations: left cam `+90 degrees Y` flat-inner-face
  down/hub up, left fixed `+90 degrees Y` plain-face down/land up, right fixed
  `-90 degrees Y` plain-face down/land up, and right actuator `-90 degrees Y`
  flat-inner-face down/hub up; every principal part has a large planar bed face
  at `Z=0` and no negative Z;
- all six caps use `print_cap_rotation_deg = +90 degrees Y`, placing the solid
  closed end on the bed and the blind socket/cavity opening upward; the written
  production 3MF must retain a continuous vertical opening above the supported
  cavity floor;
- exactly three purchased uncut OD4 x 50 rods;
- one separate printed shallow-D shaft, matching D-bored left/right cams, one
  stop head, and one removable shaft keeper; no fused cam/shaft or rectangular
  local key/rib;
- derived pivot `(-2.096372644586, 27.903627355414)` at defaults;
- three independently recomputed OPEN-to-contact stroke requirements with
  `contact_stroke = 3.764213562373 mm`, followed by a parametric `0.25 mm`
  wire-preload stroke over 22..27 degrees (`common_stroke = 4.014213562373 mm`);
- one connected completed XT60 workpiece with exact G1 90-degree wire paths;
- normal REMOVE: valid OPEN, three right caps off, all three rod/permanent-left-
  cap units synchronously `-X`, then the complete workpiece `+Z`; all four
  plates, separate D shaft, and keeper remain assembled;
- service only: keeper radially off, both upward-mouth fixed guides `-Z`, then
  the separate D shaft `+X` through the two stationary D-bored cams. OD5.60
  through an installed ID4.80 fixed journal is a tested forbidden path;
- exact current export census: 14 STEP print-kit occurrences = 12 production
  3MF objects + 2 diagnostic coupons.

## Evidence boundary

CAD evidence covers parametric coherence, solid validity, nominal kinematics,
nominal clearances, exact normal/service path geometry, and source/STEP parity.
Printed fit, tolerance feasible sets, strength, heat, friction, elastic snap
recovery, wire force/springback, final physical angle, and usability remain
physical tests.
