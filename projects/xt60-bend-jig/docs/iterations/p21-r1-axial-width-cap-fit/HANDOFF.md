# P21 R1 axial-width and cap-fit handoff

Date: `2026-08-28`

## Corrected result

- inner clear span: `28.40 mm`;
- inner centers: `X=-15.80/+15.80 mm`;
- outer centers: `X=-19.40/+19.40 mm`;
- three purchased transverse rods: immutable `OD4 x 50.00 mm`;
- stepped center axle: `44.90 mm`;
- cap distal socket: `ID4.10 mm` (`0.10 mm` nominal diametral clearance);
- available cap engagement becomes `3.70 mm` per side; cap-to-outer gap remains
  `0.30 mm`.

The earlier STEP/3MF and test result containing `60.00 mm` rods is rejected by
the user's fixed-stock correction. It is not printable authority. Fresh
source/export validation remains pending for the corrected `50.00 mm` rod
contract.

Rejected prior review artifact:
`cad/p20_r4_custom_profile_full_cad/p20_r4_widthfix_review.step`.

The existing regenerated model-only 3MF also carries the rejected 60 mm
assumption and must not be printed. No slicing, upload, print, or physical
acceptance occurred.

## Remaining blockers

This correction does not claim to solve all reported problems. The previously
recorded Blue-rod/XT60 collision, thin plate webs, and rod/workpiece contact
classification remain open and require their own bounded corrections.
