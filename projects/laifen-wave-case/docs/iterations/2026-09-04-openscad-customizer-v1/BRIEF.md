# OpenSCAD Customizer V1 brief

**Owner:** OSC-01 design  
**Status:** design contract only; no implementation

Create a self-contained OpenSCAD Customizer V1 for the Laifen Wave two-piece case. It is a new source-native OpenSCAD model, not a mesh imitation and not a modification of the build123d authority. Defaults are OD39, body bore30, cap bore31, device length208, axial allowance5, usable cavity213, closed length219, body144, cap84, floor3, pitch2, total engagement6 over 3 turns, clearance/side0.25, thread height0.5, end chamfer1.2, diamond axial/arc pitches4.8/3.63, depth0.45, and seven drains.

Expose device dimensions, outer diameter, wall and floor, split as one canonical mode (distance from top or percentage), thread pitch/turns/clearance/depth, chamfer, drainage mode (`none`, `top`, `bottom`), output (`assembled`, `body`, `cap`, `print_layout`), surface (`round`, `smooth`, `diamond`). Defer polygon, wave, knit, text, attachments, and any downloaded geometry.

This contract defines formulas, asserts, support-free constraints, phase matching, deterministic tests, CLI mesh validation, and snapshots. OpenSCAD editing and STL generation are future implementation work.
