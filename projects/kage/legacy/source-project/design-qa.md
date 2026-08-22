# Design QA

Final result: blocked pending rendered post-fix screenshots

The rejected decor facade has been removed and the frozen V0R2 structural simulator restored. Source, local Three.js bundle, controls, Python/JavaScript/CLI parity, and the existing Tailscale-served runtime passed automated review. Fresh visual comparison and interaction capture could not be completed because neither the Codex in-app browser nor the connected Chrome surface was available to this implementation session.

Required visual gate:

- Capture the default Assembly / Cutaway view at desktop and mobile widths and confirm quartz, mask, three carriers/fins, LED, glare cap and rays are visible.
- Capture Wall shadow and confirm only the warm halo, central dark mask and H/M/S shadows remain visible.
- Open Side section, Exploded and Orbital close-up and confirm the real stack remains readable.
- Verify the optical inset starts collapsed and cannot obscure the focal clock on mobile.
- Confirm repeated view and renderer changes do not resize the page or flatten the 3D scene.

Automated evidence:

- V0R2 source distance, carrier radii, base/tip planes and hand-profile parity across JavaScript, Python, and CLI.
- Default 3D mode is Assembly / Cutaway with structural visibility enabled.
- Regression rejects the former 260 mm facade, fake orbital tracks/markers/ticks, internal corona and Day/Evening substitution controls.
- Wall view explicitly suppresses mechanics, source hardware, shell and helper rays.
- Exactly one projection light casts shadows.
- All 147 collected tests pass.
- Tailscale-served assets match local hashes.
