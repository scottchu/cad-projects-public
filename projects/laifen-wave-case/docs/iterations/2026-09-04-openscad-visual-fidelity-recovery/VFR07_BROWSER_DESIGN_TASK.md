# VFR-07 browser worker enablement design task

Design the smallest safe browser/schema/UI delta that lets the existing worker
accept the already-supported Diamond parameters and execute C1 without changing
geometry, output identity, stale/cancel/toast behavior or smooth defaults.
Preserve the mobile layout. Specify private worker validation first, then public
control enablement only after candidate critic/validator/formal-review gates.
Include exact regression and real-worker timing/identity gates, delta mask,
rollback and one implementation plus one focused repair budget. Sole write:
`VFR07_BROWSER_DESIGN.md`. Do not edit browser/source/tests/artifacts/services or
continuity.
