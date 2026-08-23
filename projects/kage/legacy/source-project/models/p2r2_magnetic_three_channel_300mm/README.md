# KAGE P2R2 — 300 mm magnetic three-channel MVP

P2R2 is an isolated enlargement of the accepted P2R1 architecture. It does not
overwrite P2R1. The overall stationary plate diameter is 300 mm; the Ø52 center
opening and every functional fit cross-section remain unchanged.

## Frozen layout

- Overall diameter: 300 mm
- Center opening: Ø52 mm
- Hour/minute/second radii: 95 / 115 / 135 mm
- Separator choices: 1.0 / 1.5 / 2.0 mm
- Magnets: six Ø6 × 3 mm total, installed in Ø6.15 × 3.10 mm pockets
- Shoe/slot: 9.0 / 4.8 mm, giving 2.10 mm capture per side
- Radial running clearance: 0.30 mm per side
- Outer moving envelope: r139.5 mm
- Stationary spacer inner edge: r140.5 mm (1.0 mm clearance)
- Overall T1.5 assembly envelope: 300 × 300 × 63.6 mm

## Print-bed warning

The 300 mm rear base and separator plates **do not fit a 256 × 256 mm bed**.
This revision deliberately remains unsegmented so the physical test measures
the requested one-piece architecture. Use a printer with at least a 300 mm
nominal bed plus slicer/skirt clearance, or do not print this revision. The
transfer 3MFs are not arranged as a real print plate; use the individual-part
3MF files.

## Recommended first build

Use the `t1p5_individual_plates` directory. Print one part per plate, verify that
the slicer reports no out-of-bounds geometry, and install the 1.5 mm separator.

Assembly order:

1. Place the rear base flat, open side upward.
2. Install the second, minute, and hour hidden driver rings in their races.
3. Install one Ø6 × 3 mm driver magnet per channel with recorded polarity.
4. Fit the 1.5 mm separator and fasten the six outer M3 stack points.
5. Install one follower magnet in each H/M/S follower, with matching attraction.
6. Place each follower into its own annular track.
7. Install cap rings R0–R3; R0 uses six M2 sites, R1/R2 use three each, and R3
   uses the six outer M3 stack screws.

Do not rely on the magnets for axial retention; the cap rings mechanically
capture every follower. CAD proves geometry and clearance only. Coupling force,
wrong-channel attraction, friction, reversal lag, and 100-cycle durability are
physical test gates.

