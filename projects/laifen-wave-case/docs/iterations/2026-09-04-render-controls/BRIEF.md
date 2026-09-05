# CAD Viewer render-controls brief

**Task:** `RCV-01`  
**Owner:** render-controls design architect  
**Status:** frozen design contract; implementation pending  
**Baseline:** accepted P1 R7 grouped package `cad/container_generator_v1/`; read-only preview candidate `d2b7afa66d0464455722e6257365eb26702b2704c070498594696049185848be`

## User outcome

Let the user reshape, separate, and restyle the already-generated closed case in
CAD Viewer without rebuilding CAD. The controls are an exploratory render of
the existing tessellated body and cap. They do not alter build123d source,
topology, dimensions, joints, STEP bytes, manufacturing feasibility, or physical
acceptance.

The existing 41-row source/derived parameter snapshot remains present and
read-only. Interactive controls appear before it under a prominent
`VISUAL PREVIEW ONLY` notice.

## Baseline and frame

- Source authority: `cad/container_generator_v1/`.
- Immutable oracle: `cad/p1_r7_end_chamfer/`.
- Closed assembly axis: world `+Z`; shared shoulder/seam datum: `(0,0,0)`.
- Body occurrence: `#o1.1`, exact authored name
  `R7 body: 39mm diamond skin; new B right-hand thread; smooth chamfer with seven drains`.
- Cap occurrence: `#o1.2`, exact authored name
  `R7 cap C25: new B thread; 39mm diamond skin; smooth end chamfer; seven drains`.
- At rest, body spans approximately `Z=-135..0` and cap `Z=0..84`; the
  assembly spans 39 mm crest diameter and 219 mm total axial length.
- Viewer features must target the exact authored names. The observed refs are
  validation witnesses only because positional occurrence ids can shift after a
  rebuild.

## Requirements

| ID | Requirement |
| --- | --- |
| `RCV-BASELINE` | Keep the accepted body, cap, closed, and print-layout STEP files byte-identical at their frozen hashes. Do not change P1 R7 CAD source, topology, labels, datums, placements, or outputs. |
| `RCV-DISCLOSURE` | The first row says `VISUAL PREVIEW ONLY` and states that controls deform or style the displayed mesh while CAD and STEP stay unchanged. Every interactive description repeats the render-only boundary. |
| `RCV-READOUT` | Preserve all existing 41 read-only rows, ids, order, values, classifications, one-option enum form, and source-driven generation. Append no editable behavior to a source or derived row. |
| `RCV-CONTROLS` | Add exactly the ten controls frozen in `DESIGN.md`: four visual scale percentages, cap unscrew turns, cap extra lift, two colors, and two opacities. Defaults reproduce the current visual state. |
| `RCV-MATH` | Use one pure, exported transform solver. Scale both parts around the shoulder datum; derive cap screw motion from the locked 2 mm/rev pitch; compose scale, then +Z rotation, then +Z translation. Clamp in code as well as in the manifest. |
| `RCV-TARGETS` | Resolve exactly one body and one cap through stable authored occurrence names. Missing or ambiguous targets block acceptance. |
| `RCV-ZERO` | At defaults, `update()` makes no effects call. Module enabled, disabled, and reset states must therefore show the same baseline pose and source colors. |
| `RCV-EFFECTS` | Use only Viewer 0.4.28 `effects.transform()` and `effects.style()`. Do not mutate Three.js meshes/materials directly, add geometry, create a second scene, or edit Viewer runtime. |
| `RCV-NATIVE` | Keep Viewer-owned orbit/camera, fit/reset, tree visibility, generic explode, clip/section, display/edge mode, and global theme controls in native UI. Do not duplicate them in the sidecar. |
| `RCV-MOBILE` | On the exact private delivery page at 390 x 844, the disclosure and all ten controls must be usable, reset must restore the exact baseline, and read-only rows must remain discoverable below them. |
| `RCV-BOUNDARY` | No CAD/STEP regeneration, no OpenSCAD/STL/3MF/slicer/printer work, no service or route changes, and no claim that a deformed render is printable or dimensionally valid. |

## Per-object delta mask

| Object | Allowed viewer-time delta | Invariants and forbidden changes |
| --- | --- | --- |
| Body display occurrence | Scale X/Y by global radial scale; scale Z by global axial scale times body axial scale; style surface color and opacity. All scale pivots are `(0,0,0)`. | No translation, rotation, topology change, source edit, STEP rewrite, hidden-by-sidecar state, or datum movement at the shoulder. |
| Cap display occurrence | Same global radial scale; Z scale by global axial scale times cap axial scale; rotate about world `+Z` through the shoulder; translate only along `+Z` by screw travel plus extra lift; style color and opacity. | No X/Y translation, tilt, topology change, source edit, STEP rewrite, hidden-by-sidecar state, or alternate screw law. |
| 41 read-only rows | Remain after the interactive block exactly as the reviewed snapshot. | No mutable options, slider conversion, value relabeling, new derivation, or effect binding. |
| Native Viewer UI | Continue to provide its own reset, visibility, generic explode, clip, display, theme, camera, and tree tools. | No Viewer source/configuration edit and no duplicated sidecar control for these functions. |

## Task DAG

| Task | Owner role / dependencies | Done gate | Allowed writes |
| --- | --- | --- | --- |
| `RCV-01` | architect; accepted preview baseline | Freeze brief, design, handoff, and exact `INPUTS.sha256`. | This iteration's `BRIEF.md`, `DESIGN.md`, `HANDOFF.md`, `INPUTS.sha256`; continuity pointers. |
| `RCV-02` | prescribed implementer; `RCV-01` | Generate the exact sidecar, focused tests, candidate/evidence manifests, and receipt without changing STEP bytes. | `preview_parameters.py`, `closed.params.js`, focused preview test, this iteration's implementation records and scratch namespace. |
| `RCV-03` | independent critic; frozen `RCV-02` candidate | Challenge disclosure, false geometry implications, targeting, transform order, bounds, mobile density, and native-control duplication. | Critique receipt/manifests and critic scratch only. |
| `RCV-04` | independent validator; frozen `RCV-02` candidate, parallel with `RCV-03` | Reproduce deterministic tests, exact effects, zero state, endpoint readiness, desktop/mobile states, and unchanged STEP hashes. | Validation receipt/manifests and validator scratch only. |
| `RCV-05` | independent formal reviewer; `RCV-03` and `RCV-04` | Join one exact candidate and issue render-preview PASS/BLOCK separately from CAD, STEP, slicer, and physical states. | Review receipt/join manifest only. |

One design attempt and one implementation attempt plus at most two focused
repair cycles are the ceiling. Any STEP hash change, source-geometry edit,
direct mesh/material mutation, non-identity default effect, wrong occurrence
target, or misleading editable-CAD presentation stops downstream work and
reopens the contract.

