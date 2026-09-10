# Printing profile — Pill Click

## Profile

`pill-click-print-01`, draft migration record, updated 2026-09-01. Applies to
preserved experiments only; not a slicer preset or print approval. Separate
intended settings from verified runs and historical physical observations.

## Intended settings

Historical P1 design assumes a 0.40 mm nozzle (`docs/p1-hollow-magnetic-dispenser-spec.md`).
Printer/build area, head mapping, actual nozzle, material/brand/color, filament
diameter/conditioning, surface, layers, extrusion widths, walls, infill,
temperatures, cooling/speeds, supports, brim and compensation are all pending
fresh selection. The old 220 mm plate reference is not a selected current printer.

## Part orientation and fits

P1 print placement is authored by `src/pill_click/p1_hollow_magnetic_dispenser/print_exports.py`;
P2 by `src/pill_click/p2_bayonet_refill_8mm_rebound/print_exports.py`.
P1 has housing, integrated inner, rear cover; P2 adds a bayonet cap.
Read these transforms before slicing. Do not confuse assembly pose with bed pose.
Current process-specific bed faces and fit verification remain pending.

## Verified slice and print runs

No new run. No migrated run binds a printer/material/profile/G-code/job ID to
the current P1/P2 hashes. Record future runs with source/artifact SHA-256,
slicer/version/preset hashes, resolved settings/tool mapping, object transforms,
G-code hash, job ID and separate CAD, slicer and physical verdicts.
Historical P0 observations are summarized in `docs/EXPERIENCE.md` only.

## Concerns

- `PRINT-001`: historical upright latch fractured after roughly 5–10 removals;
  later latch-cycle goals do not prove the current P1/P2 cover durable.
- `PRINT-002`: P1 internal hopper supports must be removable through the port;
  verify on the selected process before real use.
- `PRINT-003`: return force, magnet polarity/retention, fridge holding force,
  rail fit and cap cycling remain physically unverified for this migration.
- `PRINT-004`: food-contact suitability and child resistance are not established.

Next smallest check: select an exact baseline and process with the user before
authorizing any coupon or print. Filling this profile never bypasses design gates.
