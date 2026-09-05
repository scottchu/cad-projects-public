# P2 R6 text label system brief

R6 is the current frozen visual contract, superseding R5 before implementation. It retains all R5 behavior and adds optional, safely rendered surface labels for round and polygon sections. It remains browser visual intent only: no CAD/OpenSCAD/STEP/font-parity/print/fit/MakerWorld claim.

| ID | Requirement |
| --- | --- |
| R6-01 | Preserve all R5 visual parameters/invariants, exactly two core pieces, optional explicit accessory bodies, and continuous core OD/no collar. |
| R6-02 | Add validated label modes, text, generic font preset, weight, size, relief, orientation, target, angle, axial location, patch and margin. |
| R6-03 | Escape text and reject empty/overlong/control/unsupported strings; invalid state clears scene/detail/scale and reports accessible field errors. |
| R6-04 | Map text to round/polygon support surface, avoid seam/end/thread/keepout/accessory zones, suppress texture inside patch, and report added text/accessory envelope. |
| R6-05 | Preview font selection is not OpenSCAD parity; future explicit family must enumerate/fallback missing glyphs/fonts. |
| R6-06 | Preserve P1 R7, source/tests/services/routes and served P2 R3 bytes until a new reviewed candidate. |
| R6-07 | Carry accessory modes plus `keyring_tab`/`bridge_handle`, report total envelope, and label metal hardware as reference only. |

| role | dependencies | exclusive writes | ceiling |
| --- | --- | --- | --- |
| IMP-GCS-R6-01 | R6 fingerprint + clean R5 inventory | simulator/test/R6 implementation evidence | 16 min, initial + 2 repairs |
| VAL-GCS-R6-01 | candidate | validation evidence | 12 min, initial + 2 method repairs |
| CRIT-GCS-R6-01 | candidate | critique evidence | 10 min, initial + 2 findings |
| REV-GCS-R6-01 | VAL + CRIT | review/join | 8 min, initial + 2 provenance repairs |
| DEL-GCS-R6-01 | formal PASS | isolated delivery | 6 min, one retry |
