## Intent and evidence

The user wants a straight assembled cylinder with the same outside diameter from end to end and diamond texture over its entire visible outer sidewall, including the outside of the female thread collar. No bulge, broad smooth ring, or externally untextured collar. A thin cap separation seam is acceptable. The supplied photo was inspected: one body and three caps, pronounced smooth collars and limited textured bands. It supplies appearance evidence, not dimensions. The user reports all three hand closures are good; exact print provenance and measured performance remain unknown. Canonical observation: `docs/observations/2026-09-02-coupon-fit/` and EXPERIENCE OBS-06/07.

This version deliberately supersedes REQ-08/R3's external2mm smooth exclusions, exterior fades and raised-only skin envelope. Internal threads and functional contact faces remain smooth. R4 deliberately changes the approximate REQ-05 OD39 target to40mm: retaining fitted threads,0.45mm texture depth and1.8mm minimum structural wall with clearance budget0.30 requires at least39.90mm. This is a design choice for the new external intent, to be shown explicitly in the small2D gate.

## Requirements

| ID | Contract and classification |
|---|---|
| R4-01 | Invariant: common cylindrical diamond-crest envelope, selected OD40.00; no outward collar or taper, no broad blank sidewall zone. Only0.30mm axial textured relief at each closed bed edge is allowed. |
| R4-02 | Invariant: shared mathematical diamond generator covers assembled body z[-35.1,0] and cap z[0,43.4], including seam and collar. Common phase at z0,theta0; axial pitch4.8 unchanged when length changes. |
| R4-03 | Invariant: bores30/31, original right-hand thread pitch2, engagement6, root16.8/crest17.4, clearance0.25 default and budget0.30; actual male/female internal geometry and positive shoulder stop z0 preserved. |
| R4-04 | Invariant: cavity72.5, floors3, body inner floor z-32.1, cap inner floor40.4, male tip9 and original internal cap transition10.2..12.4. Short experiment remains closed length78.5. |
| R4-05 | Derived: inward valley depth0.45 from crest radius20, valley radius19.55; minimum female ligament1.85 using budget0.30,1.90 at c25; male root wall remains1.8. No wall thinning to save OD. |
| R4-06 | Design choice: blunt diamonds use plateau fraction0.18, axial pitch4.8 and target arc pitch3.63; derive common integer repeat count from valley radius. Default34 repeats, common actual arc pitch about3.613. |
| R4-07 | Deliver one body and one C25 cap, source-defined closed assembly and two-part print layout. Alternate clearances remain parameters; no three-cap print set is required. |
| R4-08 | Invariant: parts print vertically openings up, cap Rx180. U1/PLA/nozzle0.4/layer0.2/supports off are intended settings only. Actual source solids, exported solids, first-layer geometry and surface normals require focused checks. |
| R4-09 | Physical unknown: new textured collar feel, seam registration under real tightening, print quality, torque/wobble/wear and strength. Existing hand report is useful baseline evidence, not R4 physical acceptance. |

Use sequence: empty short body/cap; start original screw by hand; twist to original shoulder; assess straight profile, coverage and grip; reopen. Full Laifen length, installed brush fit, retention and end-contact policy remain outside this task. No p2.4/DES07 repair, broad parameter-domain certification, drainage redesign, slicing/upload/start or printer control. Any full-length request reopens its own fit gate.

Coordinates: mm; common axis Z, shoulder/seam at z0, body below and cap above. Proposed source namespace `cad/p1_r4_generator/`; primary outputs `body.step`, `cap_c25.step`, `closed_c25.step`, `print_layout.step` from named parametric `.step.py` entrypoints. Diagram `preview/p1-r4-profile-study.svg/.png` is formula-based, not a CAD render.
