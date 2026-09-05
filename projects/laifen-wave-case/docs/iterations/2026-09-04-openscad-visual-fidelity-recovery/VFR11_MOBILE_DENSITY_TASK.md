# VFR-11 mobile density task

Status: ready after `inputs/VFR11_MOBILE_DENSITY_INPUTS.sha256` is frozen.

User-confirmed mobile UI contract:

- hide the visible page title and explanatory caption at widths <=700 px so
  the status and sticky canvas start at the top of project content;
- render Generate, Cancel, Reset, Reset camera and Download as one compact row
  of icon-only controls on mobile;
- reduce the mobile canvas from its current 260 px to a responsive target near
  220 px (bounded by viewport height) so a 390 x 844 first screen contains the
  complete sticky preview/action strip and at least one complete Basic field;
- keep every touch target at least 44 x 44 px and retain explicit accessible
  names through text in the DOM and/or `aria-label`/`title`;
- keep desktop labels, all existing element IDs, order, listeners, states,
  focus, toast, stale/download behavior and disabled Diamond controls;
- do not modify SCAD geometry, schema, worker, vendor/runtime, service routes or
  browser acceptance state.

Implementation may edit only `preview/openscad-wasm-simulator/index.html`,
`style.css`, focused UI tests, new evidence under
`scratch/vfr11-mobile-density/`, and `VFR11_MOBILE_DENSITY_IMPLEMENTATION.md`.
Use inline SVG or deterministic CSS icons; do not add a dependency. Verify at
390 x 844 and desktop width. One candidate plus one focused repair. No deploy
in the implementation role; deployment follows independent validation/review.
