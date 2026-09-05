# Frozen user intake — P2 R3 control-sync recovery

Captured 2026-09-03 from the authorized recovery request.

- P2 R2 exhausted its implementation repair ceiling and remains HOLD for one exact independent control-state defect.
- Repair only the canonical split control synchronization: after a percent edit, canonical raw `S`, the mm input, the percent input, all readouts, and their bounds must reflect one unrounded state; a later mm action must never overwrite `S` from a stale DOM value.
- After any height edit, derive percent bounds/value from the new `H` and current raw `S`.
- Required regression sequence: `H=261` → percent minimum → mm input `12.4`; percent maximum → mm input `248.6`; `ArrowUp` on the mm input must remain at maximum under native `max` validity rather than jump to `60.4`.
- Preserve passing repair-2 geometry, camera, pattern, accessibility, end-control, and visual behavior byte-for-byte. Repair the active implementation-receipt continuity pointer at the same time.

This authorizes only the recovery design contract and later minimal app/test/receipt changes. It does not authorize CAD, route, service, slicer, print, index, or unrelated UI changes.
