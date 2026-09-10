# P0 mechanical-fit V2.1 keyboard-identity specification

## CAD brief

- Model: cosmetic V2.1 derivative of the accepted V2 three-part assembly.
- Task type: source modification in a separate package; V2 remains frozen.
- Inputs: user-provided giant keyboard-fidget photographs and the accepted V2 CAD.
- Units: millimetres.
- Coordinate convention: unchanged from V2; travel is along Y, key face points +Y.
- Functional invariants: 40 x 40 housing, four continuous rails, blind rail
  stops, their clearances, and 13.40 travel remain unchanged after successful
  V2 physical testing.
- Physical-test correction: the two-sided rear snap remains squeeze-releasable,
  but its beam and hook engagement are strengthened because the V2 cover could
  be removed too easily with two fingers.
- Changed feature: the solid inner receives a taller, strongly tapered keycap
  with a shallow spherical finger dish like a sculpted keycap.
- Primary outputs: pressed and released assembly STEP plus standalone inner STEP.
- Assumption: the photograph is aesthetic inspiration rather than a dimensioned
  reproduction; proportions are inferred from the 40 mm housing envelope.

## Frozen V2.1 parameters

| Parameter | Value |
| --- | ---: |
| `key_skirt_size_xz` | 34.20 |
| `key_skirt_corner_radius_xz` | 4.00 |
| `key_face_size_xz` | 29.00 |
| `key_face_corner_radius_xz` | 5.50 |
| `key_face_edge_fillet_y` | 1.00 |
| `key_local_y` | `[12.50,20.50]` |
| `keycap_height` | 8.00 |
| `key_face_dish_radius_xz` | 14.00 |
| `key_face_dish_depth_y` | 0.55 |
| `travel` | 13.40 |
| `pressed_key_proud_y` | 5.00 |
| `released_key_proud_y` | 18.40 |
| `side_latch_beam_thickness_x` | 1.10 |
| `side_latch_hook_engagement_x` | 0.60 |
| `side_latch_pocket_depth_x` | 0.70 |
| `side_latch_pad_release_travel_x` | 0.48 |

The 8.00 mm loft tapers directly from the 34.20 mm inner body to the 29.00 mm
face, matching the straight sloped wall of a keyboard key rather than creating
an hourglass between spline stations. A 1.00 mm face-edge fillet softens the
front rim. The finger dish is a 0.55 mm-deep spherical cap with a 14.00 mm
footprint radius.
The footprint sits only 0.50 mm from the face's straight edges, so its shaded
surface reads as a broadly sculpted key rather than a small circular inset.

## Validation contract

1. The four male rails retain their physically accepted V2 bounds, engagement,
   front stops, and 13.40 mm travel.
2. Rear-latch beam thickness rises from 1.00 to 1.10 mm and the hook engagement
   rises from 0.45 to 0.60 mm while pad travel still fully releases both hooks.
3. The V2.1 inner is one valid positive solid.
4. The keycap is 8.00 mm tall and 5.00 mm proud of the housing when pressed.
5. The released state is exactly 13.40 mm farther forward than pressed.
6. The face centre is recessed 0.55 mm while its perimeter remains solid.
7. Pressed and released assemblies contain exactly three labeled solids.
8. Baseline STEP inspection and saved multi-view snapshot review must pass.

## V2 physical-test evidence received 2026-08-07

- Four inverted rails: smooth and accepted; freeze dimensions.
- Rail-based front stop: solid and accepted; freeze geometry.
- Rear side-squeeze cover: functional but insufficiently retentive; it could be
  removed easily with two fingers and therefore receives the V2.1 changes above.
- Clamp underside: support is required in the slicer; the photographed loose
  bridge/stringing is not treated as a CAD fit failure.

## Print-orientation note

The 13.40 mm stroke is deliberately long-throw compared with a normal keyboard
switch; it follows the user's measured giant-fidget reference. The dish makes
the old face-down print pose undesirable because it would bridge the recessed
face. V2.1 print packaging is intentionally deferred until the standalone
inner is reviewed; the likely production pose is face-up with localized
support beneath rear rail extensions.
