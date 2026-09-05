# Frozen user intake — P2 R2 generic container simulator

Captured 2026-09-03. This supersedes P2 R1 before any delivery.

- Build a generic parametric threaded-container simulator, rather than a simulator only for the Laifen case.
- It must support short, wide containers such as a makeup jar as well as the Laifen Wave reference.
- Thread-related controls must be editable. The user specifically needs one- and two-rotation thread choices; three rotations must remain available for the Laifen reference.
- Keep one canonical split distance from the closed top, with a derived/adapted percentage control.
- Keep fixed physical pattern pitch through size changes and evaluate the pattern in assembled global Z before clipping it into the two pieces.
- Start with HTML/Three.js. The parameter contract must also be suitable for a future OpenSCAD implementation.

This authorizes a design contract and later visual intent simulator only. It does not authorize changes to R7 CAD, a printable generator, exports, slicing, printing, MakerWorld publishing, or a Tailscale-route change.
