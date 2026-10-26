# Direct rail editing

Request revision 3, 2026-10-26. Baseline 14756a2.

User explicitly requires no OPEN/END mode toggle: dragging either endpoint moves
that endpoint, dragging a line translates the whole path, and a separate dot
shapes the curve. Both inverse outer rails update from the same world path.

## Frozen requirements

- DE-1: Both endpoint handles always directly draggable; remove toggle controls.
- DE-2: Drag any inner rail line to translate both endpoints by one common delta.
- DE-3: A visible midpoint curve dot per rod controls a smooth bowed path.
- DE-4: Keep endpoints exact, zero bend recovers archived straight defaults,
  and inverse/forward rail closure stays exact across edited states.
- DE-5: Legacy JSON loads with zero bend; new bend survives JSON/local storage
  and SVG exports. Numeric/keyboard alternatives remain available.
- DE-6: Validate the actual existing Tailscale URL, retain CAD/physical boundaries,
  and update the same PR.

No mechanism/CAD redesign or fabrication. The new curve function is a declared
reconstruction feature, not a claim to recover the missing original algorithm.

## Design

Store bendMm=[dy,dz], the curve midpoint offset from the OPEN/END midpoint.
P(u)=(1-u)OPEN+u END+4u(1-u)bendMm. The draggable curve dot is P(0.5).
This is a quadratic Bezier, with endpoint interpolation preserved exactly.
Dragging an endpoint retains bend offset; whole-line dragging translates both
endpoints and retains bend offset. Curve dragging changes bend offset only.
Legacy profiles omit bendMm and normalize to [0,0]. Bend component range ±60mm.
Viewport radius bound adds bend norm because 0≤4u(1-u)≤1.
Near-coincident controls use short leader lines to separate hit targets; they
retain actual coordinates and drag deltas, avoiding a jump at pointer-down.

## Verification and plan

Root implements and self-checks. Reuse independent critic/validator/formal join
for a frozen candidate; up to two focused repairs. Test endpoint preservation,
midpoint control, both inverse frames, viewport, legacy import and exports.
Browser: endpoint O/E drag without toggles, line translation, curve-dot drag,
JSON persistence, responsive layout, unchanged local cuts while scrubbing.
Root npm and repository checks; reuse unchanged Python baseline regression
receipt. User-authorized private hosting at port8480 serves only the HTML via
loopback5208, runtime ownership recorded in ignored scratch/rail-hosting.
