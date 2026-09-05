# P2 R5 cross-section generator brief

**Status:** frozen user-confirmed visual-intent contract; R4 superseded before implementation.

Extend the generic two-piece visual simulator with round and rounded regular-polygon sections. Exactly two core pieces remain, meet at the configurable middle split, and share one section frame. Optional accessory bodies remain explicit extras and report their enlarged envelope. All R4 functionality is retained; this iteration does not create CAD or printable geometry.

| ID | Requirement |
| --- | --- |
| R5-01 | Preserve all R4 closure/pattern/end/envelope/accessory features and visual-only boundaries. |
| R5-02 | Add round/regular_polygon, sides 3…32, roundness 0…1, rotation 0…<360. |
| R5-03 | Both core pieces have identical section support and orientation; locked state aligns cross-section and pattern. |
| R5-04 | Polygon nominal OD is maximum across-corners diameter; show across-flats and maximum envelope without hidden growth. |
| R5-05 | Invalid section/closure/end/accessory values clear preview/detail/scale with field-linked errors. |
| R5-06 | Keep no seam collar/thicker thread zone, continuous core maximum OD, optional-extra accessory semantics, mobile/accessibility and true-scale/magnifier behavior. |
| R5-07 | Keep P1 R7, CAD/OpenSCAD/STEP/slicer/printer/MakerWorld, services/routes and served P2 R3 bytes unchanged. |
| R5-08 | Add original global `flowing_flutes`, distinct from straight micro flutes, with wave amplitude/wavelength/phase/direction and constant pitch. |

## DAG

| ID | role | dependency | exclusive writes | ceiling |
| --- | --- | --- | --- | --- |
| DES-GCS-R5-01 | design | R4 freeze | R5 contract files | complete |
| IMP-GCS-R5-01 | implementation | R5 fingerprint + R4 inventory | simulator/test/R5 implementation evidence | 16 min, initial + 2 repairs |
| VAL-GCS-R5-01 | independent validation | candidate | validation evidence only | 12 min, initial + 2 method repairs |
| CRIT-GCS-R5-01 | independent critique | candidate | critique evidence only | 10 min, initial + 2 findings |
| REV-GCS-R5-01 | formal review | VAL + CRIT | join/review only | 8 min, initial + 2 provenance repairs |
| DEL-GCS-R5-01 | private delivery | formal PASS | isolated delivery only | 6 min, one retry |

Stop implementation if partial R4 files cannot be identified, a third core body appears, a polygon OD is treated as across-flats, or any physical/CAD claim enters the page.
