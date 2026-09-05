# OSW-19 stale-preview-on-error recovery design

## Frozen baseline

The OSW-18 checkpoint is the current candidate: assembled output passes in the
browser; a real compiler error is visible and recovery succeeds; the remaining
finding is OSW18-B01, the old canvas mesh survives the error byte-for-byte.
The frozen implementation bytes are recorded in `inputs/MANIFEST.sha256`.

## Smallest change

Add one idempotent preview disposal path in `preview/openscad-wasm-simulator/src/main.mjs`.
At generation start, clear the scene reference and remove/dispose its geometry,
material, and object resources before launching a job. If the implementation
needs to retain the old mesh during a job, invoke the same path on worker error
and cancellation before publishing diagnostics. Keep download revocation on
stale edits and apply it to failed/cancelled jobs. Disposal must tolerate an
already-empty scene and repeated calls.

No worker protocol or production SCAD change is permitted. Do not mask errors
with a placeholder mesh. A successful recovery alone may install a newly
owned mesh after its result passes existing validation.

## Gates

Focused tests assert: disposal removes the prior object and releases geometry
and material; generation start/error/cancel leaves no preview or download; a
successful result installs exactly one current object; repeated cleanup is
safe. The real-browser gate is valid assembled -> safe real compiler error
(empty canvas, revoked download, visible error) -> valid assembled recovery.
Existing native/WASM, mesh, diagnostic, route, and artifact parity evidence is
inherited and must remain unchanged. Scope is smooth-only and local-only;
slicer and physical acceptance remain out of scope.
