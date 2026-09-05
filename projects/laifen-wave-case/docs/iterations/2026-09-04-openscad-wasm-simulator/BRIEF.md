# OpenSCAD WASM simulator brief

**Owner:** OSW-01 design  
**Status:** frozen design contract; no implementation

## Outcome

Create a minimal responsive browser app that compiles the recovered
`openscad/laifen_case_customizer_v1.scad` in a Web Worker using the official
OpenSCAD WebAssembly port. Three.js displays the resulting STL and provides only
camera/orbit presentation. It must not calculate, imitate, scale, or otherwise
replace model geometry.

The frozen source is
`b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`.
OSC-07 validation `d4323bae7effad0a5f9436fbce78ef933129ddaddfe06a622d73fea23cd12e21`
passes the smooth candidate: body and cap are one-component watertight solids,
print layout has exactly two solids, closed contact has zero volumetric
collision, and default bounds are exactly OD39, body144, cap84, and closed219.
Its evidence manifest is
`6e6d01b20f2b29fba73ca4097322f0e880e3c6d970325eb0e528d11a209737f3`.
Diamond body and cap both timed out at the independent 60-second ceiling, so
diamond remains a performance block.

Use the exact official web binary selected by official `openscad-playground`
commit `012111f06bb6d8dac2b8d30318512494d87d6932`: its `libs-config` pins
`https://files.openscad.org/playground/OpenSCAD-2025.03.25.wasm24456-WebAssembly-web.zip`.
The verified archive is 2,947,329 bytes with SHA-256
`0968af31b9c9b3bba68d9031de1695ccae51c32231a1aab4ef27b18c86379f3b`
and contains `openscad.js` (124,567 bytes) and `openscad.wasm` (9,603,115
bytes). A verified setup script fetches it for local use; the binary is not
committed.

The app is a local design tool for quickly trying proportions and closure
choices. It must let the user make a wide, short container, move the seam using
distance from top or percentage from top, and reduce the threaded engagement to
one or two turns. The visible result and downloaded STL must come from the exact
parameter snapshot accepted by OpenSCAD.

## V1 controls and actions

- Core dimensions: device length, axial allowance, outer diameter, body bore,
  cap bore, minimum wall, floor thickness.
- Split: mode, distance from top, and percentage from top. Only the selected
  mode is authoritative for a job.
- Thread: pitch, turns, clearance, depth, and root wall. The source range is
  preserved, including one- and two-turn values.
- End chamfer.
- Drainage: none/top/bottom, diameter, and ring radius.
- Surface: smooth is the only V1 generated/downloadable surface. Diamond plus
  its existing pitch, depth, and phase controls remain visible but disabled and
  labelled `pending optimization`.
- Output: assembled, body, cap, or print layout.
- Generate, Cancel while active, Reset, progress/stage and compiler error
  feedback, camera reset, and download of the latest successful STL.

Edits are staged until Generate. While staged values differ from the generated
snapshot, the viewer and download area must say that the displayed STL is stale.
Download is disabled until a matching job succeeds.

Generate must reject any non-smooth surface job before worker startup. There is
no diamond preview, proxy texture, background compile, or diamond download in
V1.

## Boundaries

The browser app may add an isolated implementation and focused tests later. It
must not change the authoritative `.scad`, `customizer_contract.py`, build123d
source, reviewed STEP artifacts, existing preview candidates, or existing
Tailscale routes. CAD validity, mesh/export validity, slicer validity, and
physical fit remain separate evidence gates.

The only intended delivery is a self-contained local static app followed, after
independent review, by a private Tailscale route at `/openscad-simulator/` on the
existing loopback 8972/private 8448 service. MakerWorld integration and all
public or third-party hosting are deferred non-goals for this iteration.

## Done gate

Implementation is complete only when frozen source and dependency provenance,
verified setup and exact prebuilt-byte parity, parameter-to-`-D` parity, real
smooth WASM STL generation, disabled diamond behavior, stale-job suppression,
cancel/restart behavior, exact STL display/download parity, accessibility,
desktop/mobile evidence, performance measurements, CSP behavior, and local plus
Tailscale served-byte parity have independent PASS receipts. A successful HTTP
response or plausible screenshot alone does not satisfy the gate.
