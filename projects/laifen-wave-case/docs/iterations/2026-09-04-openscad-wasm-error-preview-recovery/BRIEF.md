# OSW-19 stale-preview-on-error recovery brief

## Contract

OSW-18 validated assembled smooth generation, diagnostics, recovery, and the
served browser surface, but found that a failed compile revoked the download
while leaving the previous assembled canvas pixel-identical. That stale mesh is
an unsafe false success state.

This design reopens only preview invalidation in `src/main.mjs`. It may clear
and dispose the current rendered mesh when a new generation starts, or at the
latest when the worker reports an error. The existing stale-edit download
revocation remains required. No worker, SCAD, layout, dependency, route, CAD,
or artifact changes are in scope.

## Acceptance

In a real browser, generate valid assembled output, trigger a safe real
compiler error, verify the canvas is empty/non-stale and the download is
revoked, then generate valid assembled output again. Focused assertions must
cover disposal, error/cancel invalidation, and recovery.
