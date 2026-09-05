# VFR-08 functional repair design task

Status: ready after `inputs/VFR08_FUNCTIONAL_REPAIR_INPUTS.sha256` is frozen.

Task ID: VFR-08-D. Owner role: independent repair designer. Resolve only the
two High findings on VFR-07 C1:

1. selected body-bottom or cap-top drainage holes must cut completely through
   the 3 mm floor without changing their diameter/ring pattern or enabling both
   ends; and
2. `print_layout` must orient both separate pieces vertically with their open
   ends upward, without changing body/cap/assembled output datums.

Specify exact source delta, transforms/cutter extents, regression checks,
actual-solid and written-mesh gates, candidate budget and stop conditions.
Preserve B surface geometry, seam, 39 mm OD, 30/31 mm bores, floors outside the
holes, end chamfers, threads, smooth path, browser files, services and all prior
evidence. Sole write: `VFR08_FUNCTIONAL_REPAIR_DESIGN.md`. Do not edit source,
tests, artifacts, browser/UI, continuity, services or printer state.
