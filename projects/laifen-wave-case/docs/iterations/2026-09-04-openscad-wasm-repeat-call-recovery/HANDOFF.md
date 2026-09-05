# OSW-12 repeat-call recovery handoff

**Status:** formal review **BLOCK for local delivery**  
**Owners:** OSW-14 validation; OSW-15 formal review

The exact repeat-call candidate remains worker
`74dca2b782b6ca858a715e4dd1814016863effc3a5572835891cf3aff5290c9e`
and focused test
`049a71bc9a7f7c44ff87732771d06802cc3e6d55aca781a27479cdac809d72ff`.
OSW-14 independently proved fresh-runtime cube, default smooth body, and default
smooth cap success with Manifold diagnostics, watertight one-component meshes,
native parity, exact download identity, and bounded UI/mobile/network evidence.
Its validation receipt is
`33c09c80f62a293ba5fffcd83b282b15c61c8d778b2b5b1b14bbb27c07ba72c7`;
evidence-manifest fingerprint is
`99b1e16aae37cbb377f3406b17bab1455e6bd20f294229ad8a91ba8dacf4fc39`.

OSW-15 found three P1 delivery gaps in `FORMAL_REVIEW.md`: no completed
assembled job or mesh/parity/identity evidence; no real compiler-error and
recovery state; and worker log events omit the job id, causing the application
to discard compiler diagnostics even though the validation harness can observe
them externally.

The next bounded repair must attach the active job id to diagnostics without
changing geometry or dependency bytes. Freeze the repaired candidate, then use
a distinct validator to capture a successful default smooth assembled result
and compiler-error/recovery behavior on the exact candidate. Repeat formal
review before any local delivery or route work.

Diamond remains disabled and unaccepted. MakerWorld, public hosting, route
changes, slicer work, printer actions, and physical acceptance remain outside
scope. Browser mesh evidence, CAD/STEP acceptance, slicer acceptance, and
physical acceptance stay separate.
