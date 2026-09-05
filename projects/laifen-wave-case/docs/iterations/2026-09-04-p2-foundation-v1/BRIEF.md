# P2 Foundation V1 brief

**Owner:** `DES-GCS-FOUNDATION-01`  
**Status:** **PASS** on 2026-09-04  
**User response:** `Yes pass`  
**Implementation:** authorized only through the separate Foundation V1 implementation iteration

## Purpose

Start again with the smallest useful parameterized container. Confirm its basic topology and dimensional relationships before building a preview. After V1 passes, add one feature family at a time; do not return to an all-features renderer.

## Fixed in V1

- Two physical identities: lower piece and upper piece.
- Both pieces share one outside-diameter datum along the sidewall.
- The seam is within the body; neither piece is a tiny top cap.
- Smooth exterior sidewall with no pattern or fade.
- Screw closure only.
- Assembled and exploded presentation states.
- Pure math derives a complete descriptor; any later renderer may consume only that descriptor.
- Conceptual, dimensionally proportional intent evidence only.

## Adjustable in V1

- Total outside height; common floor thickness; derived usable axial height.
- Outside diameter and wall thickness; derived minimum clear inside diameter.
- Split input by percentage from the top or distance from the top, with one canonical synchronized split.
- Round or regular-polygon section plus side count; no corner-roundness or rotation controls.
- Independent top and bottom end style: flat, chamfer, or rounded, with a conditional end size/radius.
- Screw pitch, integer turns, derived engagement, radial clearance, profile depth, and profile form.
- Drain location `none`, `top`, or `bottom`; default `bottom`, never `both` in V1. Count, diameter, and bolt-circle diameter are adjustable when a drain is active.
- Presentation state: assembled or exploded.

## Explicit V1 exclusions

No surface patterns, fade envelopes, relief modes, labels/text, patches, attachments, chains, handles, bayonet closure, OpenSCAD, CAD, STEP/mesh export, slicer work, physical claims, MakerWorld publication, or live-route change.

## Acceptance boundary

The user confirmed these fixed and adjustable relationships with the exact response `Yes pass`. This freezes V1 for the bounded preview implementation; it does not approve CAD, a live-route change, or any deferred feature.

P2 R3 remains the live visual authority and P1 R7 remains the CAD authority. Rejected R13-R22 implementations are quarantined and must not be reused.
