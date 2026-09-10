# P0 v2 captured-shutter brief

- Model: manual pill-slider fit prototype with separate captured top and bottom
  shutters; four manufactured parts plus fixed housing.
- Task type: replacement progressive P0 geometry, preserving rejected P0 v1.
- Units: millimetres.
- Coordinates: X left/right, Y rear (-) to front/key (+), Z bottom/top.
- States: `s=-1.0` inward stop, `s=0` pressed/open, `s=13.4`
  released/closed, `s=13.55` maximum captive pull.
- Fixed body: 40 mm cube, rear insertion channel 37.3 W x 35.8 H.
- Moving parts: hollow medicine shuttle, top shutter, and bottom shutter all
  translate by `Y=4.5+s`.
- Aperture intent: fixed and moving apertures fully align at `s=0`; at release,
  each fixed aperture is backed 0.1 mm below the exterior by solid shutter and
  each translated moving opening remains under opaque housing.
- Shutter section: 0.8 web, 0.4 flange, 0.2 lateral clearance per side, 0.15
  flange-ceiling clearance, 0.2 track-floor clearance, 0.8 lip overlap per
  side, exterior face Z=+/-19.9.
- Guidance: preserve four fixed ribs and eight short bearing lands; add 0.7
  rear lead-in and 0.6 groove mouths.
- Rear retention: blind flush cover, 37.0 x 35.4 x 2.4 core, four compliant
  hooks with 38.9 tip span and 0.8 extraction overlap per side.
- Assembly sequence: feed shutters from rear, insert shuttle, engage the two
  coupling lugs with shuttle sockets, then snap the blind cover last.
- Exclusions: no springs, return magnets, push-push cam/follower, transfer
  gate, rigid plunger, STL, or 3MF.
- Sources: `src/pill_click/p0_v2/`; STEP wrappers under `models/`.
- Validation: exact equations, dense 0.10 mm sweep, BREP aperture probes,
  blind-cover rear probes, collision volume under 1e-6 mm^3, STEP baseline,
  targeted measurements, multi-view and section snapshots.

The geometry remains a fit prototype and requires independent review before
print acceptance.
