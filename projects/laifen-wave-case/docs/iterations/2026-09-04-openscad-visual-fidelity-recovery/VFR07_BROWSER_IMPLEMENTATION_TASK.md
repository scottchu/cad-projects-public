# VFR-07 private browser implementation task

Implement only the private schema/test delta in `VFR07_BROWSER_DESIGN.md`
against current VFR-08 source. Keep public Diamond controls disabled. Run P0,
real Chromium P1 body, P2 cap and P3 interaction/mobile gates. Exclusive writes:
schema, focused browser tests/harness/evidence under
`scratch/vfr07-browser-implementation/`, and `VFR07_BROWSER_IMPLEMENTATION.md`.
Main and worker remain byte-identical. No deployment/services. One attempt plus
one focused repair; restore browser bytes on failure. No self-approval.
