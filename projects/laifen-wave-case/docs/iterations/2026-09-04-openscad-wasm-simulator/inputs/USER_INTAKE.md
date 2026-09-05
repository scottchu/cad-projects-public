# User intake — local OpenSCAD WASM simulator

The user wants the existing source-native OpenSCAD customizer to become an
interactive browser simulator. The same
`openscad/laifen_case_customizer_v1.scad` must remain the geometry authority:
parameter changes must compile real geometry in the browser and must never be
represented by scaling or reshaping a substitute mesh in the viewer.

The controls must support a wide, short container as well as the current Laifen
case. The split is between the two pieces, with the seam position adjustable as
distance from top or percentage from top. Thread parameters must be editable,
including short one- or two-turn engagement for makeup and similar containers.
Core dimensions, split, thread, chamfer, drains, surface, and output selection
must be available, with Generate, progress/error feedback, reset, cancellation,
and STL download. The app must remain usable on a phone.

The recovered OpenSCAD source is the current simulator input, SHA-256
`b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`.
OSC-07 independently passed the smooth body/cap/layout and closed-state evidence,
but default diamond body and cap each exceeded the 60-second limit. Therefore
this local simulator V1 intentionally generates and downloads smooth geometry
only. Diamond and its parameters stay visible but disabled with the label
`pending optimization`; they must not start a compile or display a substitute
texture. This is a deliberate minimal-simulator scope reduction, not a claim
that diamond geometry is accepted.

This is a fully local simulator first. Its only delivery surfaces are a local
static app and a private Tailscale review route. MakerWorld integration is
explicitly deferred because website integration would slow local iteration. No
MakerWorld API, embed, upload, compatibility adapter, publishing flow, or public
hosting is authorized in this iteration.

The implementation must use the exact official prebuilt selected by the
official OpenSCAD playground, rather than compiling OpenSCAD WASM as part of this
project. The frozen package is
`OpenSCAD-2025.03.25.wasm24456-WebAssembly-web.zip`, SHA-256
`0968af31b9c9b3bba68d9031de1695ccae51c32231a1aab4ef27b18c86379f3b`.
It is acquired by a verified local setup step and remains an uncommitted binary
dependency.

This design authorizes browser architecture and a future isolated implementation.
It does not authorize edits to the OpenSCAD geometry, build123d CAD, STEP files,
slicer files, printing, physical acceptance, or any existing served route.
