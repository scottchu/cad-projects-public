# Preview parameter readout handoff

**Status:** complete — preview readout PASS; CAD/source and written STEP inherited PASS; slicer HOLD; physical PARTIAL / UNBOUND  
**Task:** `PPV-02`  
**Baseline candidate:** `6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`

The repaired candidate is formally reviewed and available at the private Tailscale CAD Viewer URL: <https://mac-mini.duckbill-ionian.ts.net:8449/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case?file=cad/container_generator_v1/closed.step.py>. It exposes 41 read-only rows (26 parameter entries, 14 derived readouts, and the notice row). The page and artifact are HTTP 200/ready; all four accepted STEP hashes remain unchanged. OpenSCAD is a future editable customizer workflow and is not implemented. The only noted presentation gap is minor mobile ellipsis.

Verify `INPUTS.sha256` and use its file hash as the design-input fingerprint before writing. Implement only the delta mask and done gates in `DESIGN.md`.

The selected mechanism is a generated, read-only STEP sidecar: one-option enum rows derived from all 26 `PARAMETER_SPECS` entries plus 14 derived readouts, a first-row regeneration notice, and an effect-free `update()`. `closed.step.py` declares the sidecar; the four accepted STEP files remain byte-identical. CAD Viewer 0.4.28 does not regenerate build123d geometry from STEP-module controls.

Do not edit services, the installed Viewer, any `.step` file, or any CAD builder. Do not deliver sliders or editable-looking values. If one-option selects remain misleading in the actual mobile UI, stop with a visual BLOCK rather than claiming the panel is truthful.
