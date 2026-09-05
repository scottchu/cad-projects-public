# OSW-16 delivery-gate recovery brief

The OSW-12 formal review is BLOCK for local delivery because assembled output was absent, real compiler-error/recovery was not exercised, and worker diagnostics lacked the active job id. This recovery permits only the smallest evidence closure: include the current active job id in worker diagnostic messages, add a focused assertion, and run validation-only smooth assembled success plus real compiler-error/recovery using a safe crafted SCAD/argv.

No production SCAD, UI, route, dependency, CAD, STEP, or other behavior may change. The scope is local-only and smooth-only.
