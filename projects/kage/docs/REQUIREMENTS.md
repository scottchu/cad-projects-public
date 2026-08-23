# Kage requirements

## Invariants

- `KAGE-REQ-001`: three independently controlled hour, minute, and second shadow fins.
- `KAGE-REQ-002`: center remains optically clear for the LED.
- `KAGE-REQ-003`: positive, tunable ring drive is preferred for the mechanical MVP; one motor per ring.
- `KAGE-REQ-004`: motors and drive hardware stay inside the ring system; fins occupy the useful outer/light region.
- `KAGE-REQ-005`: approximately 300 mm design is intentionally segmented for a Snapmaker U1 270 x 270 x 270 mm envelope; written footprint plus brim is the evidence gate.
- `KAGE-REQ-006`: assembled base lies flat for bench assembly and testing.
- `KAGE-REQ-007`: hard mechanics precede electronics packaging and decoration.
- `KAGE-REQ-008`: PETG is the primary structural/internal material.
- `KAGE-REQ-009`: CAD/source, written artifact/slicer, and physical print/assembly acceptance remain separate.
- `KAGE-REQ-010`: parametric source is authoritative; generated artifacts are regenerated from named source, never hand-edited.
- `KAGE-REQ-011`: migration preserves exact clean-restart authority, selected provenance, failures, and observations without promoting historical candidates.

## Derived constraints and design choices

- `KAGE-DC-001`: one canonical 120-degree base sector printed three times is preferred only if identical interfaces and U1 footprint are proven.
- `KAGE-DC-002`: the prior four-M3-holes-per-seam pattern is a candidate to revalidate, not frozen truth.
- `KAGE-DC-003`: guidance, gear mesh, motor dimensions, homing lanes, fin dimensions, and PETG running clearances remain provisional.

## Non-goals for this migration

- `KAGE-NG-001`: no CAD redesign, regeneration, electronics packaging, slicer release, print, or physical acceptance.
- `KAGE-NG-002`: no adoption of Half-Z, low-Z, M1/M1B, Q4, I3/R1/R2, or a later-looking namespace as current.
- `KAGE-NG-003`: no XT60 or repository-policy changes.

## Physical unknowns

Actual motor dimensions; gear selection and backlash; PETG guide clearance, seam fit/strength/flatness and long-term sag; Hall module behavior; shadow readability; LED thermal behavior; runout, drag, wear, acoustic noise, service access, and full assembly behavior all require measured evidence.

