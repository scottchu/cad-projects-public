# P1 Hollow Magnetic Dispenser — Three-Part Print Contract

## Manufactured parts

P1 has exactly three separately printable solids:

1. ported outer keyboard housing;
2. one-piece hollow keyboard/medicine container with integrated rear magnet
   insets and an ordinary flat rear/bottom sealing surface;
3. removable magnetic rear cover.

The inner container is not split and has no bonded rear cap. Its 31.8 × 9.3 mm
bottom opening is intentionally large enough to reach, cut, and remove slicer
support from the connected hopper after printing.

## Motion and bidirectional seal

| Feature | Value |
|---|---:|
| Pressed position | 3.40 mm |
| Released position | 14.20 mm |
| Working travel | 10.80 mm |
| Moving rounded port | 31.80 × 9.30 mm, R2.50 |
| Fixed fail-closed housing port | 31.80 × 6.80 mm, R2.50 |
| Moving-port area | 290.375 mm² |
| Fixed-port area | 210.875 mm² |
| Old 22 × 8 reference area | 170.635 mm² |
| Moving-port area gain | 1.7017× |
| Pressed usable overlap | 6.80 mm |
| Nominal released opening separation | 4.00 mm |
| Allowed vertical release sag | 3.00 mm |
| Separation after 3.00 mm sag | 1.00 mm |
| 8° no-line-of-sight margin after sag | 0.171 mm |

At full press, the fixed housing opening overlaps 6.80 mm of the moving opening.
At full release both possible sight paths are closed:

- the fixed opening in the outer housing is covered by the normal flat
  rear/bottom surface of the moving inner container;
- the moving inner opening remains behind solid outer-housing floor;
- the opening edges have 4.00 mm nominal separation and still have 1.00 mm
  solid separation if gravity leaves the shuttle 3.00 mm below its ideal
  released rail coordinate;
- across the full rounded aperture there is no exposed slit in that sagged
  pose, and a source-level 8° oblique-view check retains 0.171 mm margin.

There is no shutter tongue, fin, or extra sealing part. Dense edge-inclusive
sampling checks the full rounded opening rather than only its centerline.

The 31.80 mm width leaves 1.20 mm of side wall on each side, exactly three
0.40 mm nozzle widths. A strict 2× reference-area port would require either a
wider inner body or walls thinner than this printability contract.

## Hopper

The medicine void is connected from the key cavity to the 31.8 × 9.3 mm bottom
opening. Broad ruled slopes guide pills toward the port without a horizontal
catching shelf. The current print pose may use support, but that support is
reachable and removable through the enlarged opening.

## Rails and stops

- Accepted V2.3 rail cross-sections remain frozen.
- Inner rail and spine rear faces are flush at local Y=-20.80 mm.
- The concealed rail front is extended 4.35 mm so the physical maximum pull is
  exactly the sealed released pose; released endplay is zero.
- Fragile micro-stop tabs are forbidden.
- No rear-cover hard-stop pads are present; the accepted rail geometry owns the
  motion limit.
- The rear cover has no shutter clearance because the sealing fin was removed;
  the exterior rear plate remains closed.
- Full 10.80 mm working travel is collision-checked at 55 positions, including
  both exact endpoints and no more than 0.20 mm between samples.
- Existing V2.3 rear-cover flexures remain 2.00 mm thick. The locating pilot is
  tightened to 0.15 mm clearance per side and the hook engagement is 0.90 mm,
  while preserving the two-finger release travel.

## Coaxial magnet system

All pockets accept one 6.0 × 2.0 mm magnet and are modeled 6.10 × 2.10 mm.

| Seat | Function | Axial extent |
|---|---|---:|
| Inner pair | Moving rebound magnets | Y=-20.80..-18.70 |
| M1 rear-cover pair | Fridge retention | Y=-21.10..-19.00 |
| M2 rear-cover pair | Rebound field | Y=-16.40..-14.30 |

The inner pair is centered at X=±8.50, Z=0 and inset directly into the one-piece
container. A 2.70 mm solid medicine barrier separates the pockets from the
cavity. Each rear-cover location has one rear-loaded M1 fridge magnet and one
front-loaded M2 return magnet, separated by 2.60 mm of solid plastic. Never put
two magnets into one pocket.

The visible M2 cylinder terminates at the front edge of its 2.10 mm seat. There
is no same-diameter access tunnel beyond it, so its complete usable recess is
6.10 mm diameter by 2.10 mm deep and accepts exactly one magnet.

Each of the six magnet seats has one same-face extraction bore at its outward-X
edge. The bore is 1.40 mm diameter, overlaps the magnet seat by 0.20 mm, and
extends 0.50 mm beyond the 2.10 mm seat floor so a dental pick can reach under
the magnet edge. These bores are deliberately far too small for another magnet.
They are blind and preserve 2.20 mm between the inner-container bores and the
medicine cavity, 1.60 mm between the rear-cover M1 and M2 pick-bore floors, and
0.25 mm of boss material beyond each bore in X.

Recommended polarity along +Y:

- M1 forward face: north;
- M2 rear face: south, attracting M1;
- M2 forward face: north;
- inner magnet rear-facing face: north, repelling M2.

Reversing every pole is equivalent. Dry-fit and mark polarity before bonding.

## 0.4 mm nozzle contract

- ordinary shell: 1.20 mm, three nozzle widths;
- key-face membrane: 0.80 mm, two nozzle widths;
- port side walls: 1.20 mm each, three nozzle widths;
- medicine-to-magnet barrier: 2.70 mm;
- magnet pockets: 6.10 × 2.10 mm.
- magnet pick-access bores: 1.40 mm diameter, 2.60 mm nominal depth.

## Verification gates

Automated checks cover exactly three connected manufactured solids, integrated
magnet insets, moving and fixed port areas, 6.80 mm pressed overlap, both
complete released-state seal paths at the actual physical pull stop and the
3.00 mm vertical-sag pose, full-aperture backing coverage, 8° no-line-of-sight
math, dense travel collision sweeps,
flush rails, absence of rear-cover hard-stop pads, complete one-magnet recess depth, magnet
seat dimensions and separation, six depth-limited same-face pick bores,
medicine and rear-cover web barriers, STEP/source identity, 3MF object count and
wrapper compatibility, Orca loading, and frozen V2.3 regressions.

Physical gates remain: remove internal support through the enlarged opening,
verify magnet polarity, cycle the rear cover at least 50 times, and test rebound
and fridge holding force with the actual filament and magnets.
