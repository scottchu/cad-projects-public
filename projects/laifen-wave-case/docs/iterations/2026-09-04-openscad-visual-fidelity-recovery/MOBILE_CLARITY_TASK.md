# VFR-03M mobile clarity task

This is a reopened, reduced-scope presentation task after the completed VFR-03 repair ceiling. It does not reopen the mathematical A/B contract.

Baseline candidate: `candidate/PATTERN_GATE_CANDIDATE.sha256`, fingerprint `6bfa2c2225e0abcf9fdb4f841f759196630a7f5daf544731ef57306c99732e8e`.

Allowed changes: `preview/openscad-pattern-gate/index.html` and `styles.css`, plus focused validation records. Keep the A/B control, deterministic SVG, all numeric facts, exact pass/fail question, and `app.js` unchanged.

Done gate on a 390 x 844 viewport:

- The first screen asks one plain question such as `Which middle seam looks right?`.
- The title is a compact single line and does not dominate the first screen.
- A/B controls and two simple case silhouettes appear above the fold. A is labeled `現在：中間空一圈 / smooth gap`; B is labeled `要做：紋路接到接縫 / continuous pattern`.
- The selected A/B state visibly highlights the matching simple silhouette using the existing `aria-pressed` state and CSS; do not add a second control.
- The unwrapped technical SVG, fixed facts, inspection instructions, and exact technical question follow the simple comparison or sit inside collapsed engineering details.
- Desktop remains readable with no horizontal overflow.

No OpenSCAD, CAD, worker, schema, STL, public hosting, or printer changes are allowed.
