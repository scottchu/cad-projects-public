# P0 Mechanical Fit V2.3 — Keyboard Silhouette + Durable Latch

## CAD brief

- Model: new three-part derivative. V2.2 remains unchanged as a rejected
  prototype because its stepped key silhouette and thin-looking retaining
  tooth did not satisfy the physical-design review.
- Units: millimetres; +Y is button travel toward the user.
- Preserve: accepted V2 rail/spine/channel cross-sections and front endpoints,
  four rail front stops, released top at Y=38.40 and the 13.55 mm absolute
  pull limit. The working states are now 3.40 mm pressed and 13.40 mm
  released, for a physical travel of 10.00 mm and a pressed top at Y=28.40.
- Correct the key shape: the functional shuttle ends at local Y=1.50, then one
  uninterrupted loft narrows from a 34.20 mm rounded square to a 27.50 mm face
  at local Y=20.50. There is no flange, skirt step or neck.
- Extend the functional shuttle rear to local Y=-20.80 and the rail/spine rear
  to Y=-21.60. The body ends 0.80 mm ahead of the rail rear, preserving a
  two-nozzle-width insertion lead while making the inward stop rail-driven.
- Add four cover-mounted stop bosses aligned with the accepted rail bands.
  Their X width is 1.00 mm, Z width is 2.20 mm, and Y span is -18.70 to
  -13.70 mm. The extended rails touch those bosses at state 3.40, clear at
  3.41, and interfere at 3.39.
- Correct the rear retention: keep the in-plane dual-beam cover, but replace the
  thin tooth with a full 10.00 mm tall, 1.60 mm radially deep hook carried by a
  2.00 mm thick tower. The receiver provides 0.10 mm rear seating clearance,
  0.20 mm front clearance, and a 1.50 mm retaining wall.
- Keep both 10.00 mm-tall squeeze surfaces flush with the 40.00 mm cover
  envelope; no release tab may protrude beyond either side.
- Put both compliant side strips directly on the outside edges at
  X=+/-18.00...20.00 mm. Each strip is 2.00 mm wide (five 0.40 mm nozzle
  widths); its isolation slot sits inboard at X=+/-16.00...18.00 mm and stops
  at Z=+/-18.00 mm to retain top and bottom anchor bridges through the rounded
  corners.
- Align the long slot and branch ends at Z=+/-18.00 mm and relieve the forward
  pilot back to X=+/-13.80 mm. A continuous full-height stop rail spans
  X=+/-13.80...15.00 mm; the 1.20 mm open slot reaches the paddle at
  X=+/-16.20 mm. Overlapping R0.50 cutters provide rounded terminal corners
  without stepped scallops. The surrounding 40 mm cover keeps its rounded
  exterior corners.
- Manufacturing assumption: 0.40 mm nozzle, 0.20 mm nominal layer height, rear
  cover printed exterior-face-down.
- Keep the forward rear-cover pilot profile matched to the housing rear cavity:
  a 34.20 mm/R3.00 straight pilot inside a 34.60 mm/R3.20 guide, providing
  0.20 mm clearance per side and at the corner radius. The pilot is 3.20 mm
  deep: 2.80 mm straight plus a 0.40 mm, 45-degree entry loft to a
  33.40 mm/R2.60 tip.

## Keyboard profile

| Feature | Value |
|---|---:|
| Shuttle body local Y | -20.80 to +1.50 |
| Shuttle body axial length | 22.30 mm |
| Body-to-rail rear offset | 0.80 mm |
| Rail/spine rear | -21.60 mm |
| Loft local Y | +1.50 to +20.50 |
| Loft base | 34.20 mm, R3.00 |
| Loft face | 27.50 mm, R4.50 |
| Face edge fillet | 0.90 mm |
| Spherical dish footprint radius | 12.25 mm |
| Dish depth | 0.00 mm default; nonzero remains parametric |
| Front guide | 35.20 mm, R3.50 |
| Housing front chamfer | 1.00 mm |
| Seam hidden at maximum pull | 0.45 mm |

The two-section loft is linear and strictly monotonic over its full 19.00 mm
length. The face is flat by default while retaining the R0.90 edge fillet,
rounded corners and continuous keyboard taper. The 34.20 mm base is only
0.50 mm smaller than the 35.20 mm guide, so the seam stays behind the housing
even at the 13.55 mm absolute pull limit.

## Durable retaining tooth

| Feature | Value | Print interpretation |
|---|---:|---:|
| Tower | 2.00 × 6.40 × 10.00 mm | 5 nozzle widths radially |
| Hook envelope | 1.60 × 3.60 × 10.00 mm | full-height tooth |
| Axial plateau | 1.20 mm | 6 layers at 0.20 mm |
| Radial engagement | 0.80 mm | 2 nozzle widths |
| Receiver pocket | 0.80 × 1.50 × 10.80 mm | 0.10 rear / 0.20 front clearance |
| Retaining wall | 1.50 mm | broad, planar pull-off shoulder |
| Tower passage clearance | 0.20 mm | one half-nozzle radial clearance |
| Housing outer skin | 1.20 mm | 3 nozzle widths |
| Release squeeze | 0.90 mm | 0.10 mm hook clearance |
| Physical squeeze stop | 1.20 mm | modeled fixed stop surface |
| Side squeeze surface | flush × 10.00 mm tall | isolated by the outer slots |
| Compliant strip width | 2.00 mm | 5 nozzle widths; mirrored both sides |

The hook is extruded through the entire 10.00 mm Z height. Its long front and
rear ramps are integral gussets in the XY profile, rather than separate thin
features. The tower overlaps the 2.40 mm faceplate by 1.60 mm in Y. The front
ramp relief begins after the receiver's 0.20 mm front clearance, while the rear
shoulder remains the retaining surface.

## Geometry acceptance checks

1. Key section width decreases at every 0.50 mm sample from 34.20 to 27.50 mm.
2. Button has no housing or rear-cover collision at every 0.10 mm from the
   3.40 mm inward/pressed state through 13.50 mm, plus the exact 13.55 mm
   maximum-pull endpoint.
3. Each latch lock is collision-free against its receiver at every 0.10 mm of
   squeeze from 0.00 through the real 1.20 mm stop.
4. Each released lock has a collision-free insertion envelope at every 0.10 mm
   from 4.00 mm behind the seated position to seated.
5. The cover is clear at the seated position and at 0.10 mm rearward pull; a
   0.11 mm rearward pull intersects the retention wall.
6. Inner, housing and cover are each one valid solid; pressed/released
   assemblies contain exactly three valid solids.
7. Rear-cover X bounds are exactly -20.00 to +20.00 mm; neither squeeze
   surface exceeds the 40.00 mm cover envelope.
8. Both compliant strips span X=18.00 to 20.00 mm before mirroring, with their
   isolation slots immediately inboard at X=16.00 to 18.00 mm.
9. Actual solid sampling verifies the continuous stop rail, a fully open
   1.20 mm squeeze gap, R0.50 terminal caps, no isolated internal ledges, and
   solid cover material immediately beyond Z=+/-18.00 mm.
10. The four rear bosses have 8.80 mm2 combined nominal contact area. Rail/boss
    contact is zero-volume at state 3.40, clear by 0.01 mm at 3.41, and
    interfering by 0.01 mm at 3.39.
11. Rear-feed insertion is collision-free against the housing from centre
    Y=-39.40 to +7.90 at each named 0.50 mm test step.

Physical cycling remains required; geometric checks do not certify fatigue
life. Print the cover exterior-face-down with at least four walls and test 100
squeeze cycles plus 25 install/removal cycles before accepting the latch.
