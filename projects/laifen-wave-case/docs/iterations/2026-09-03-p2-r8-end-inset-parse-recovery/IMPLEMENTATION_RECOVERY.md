# IMP-GCS-R8-REC-01 implementation recovery receipt

**Status:** IMPLEMENTED — the isolated parse repair and prescribed implementation smoke gates pass. Independent validation, critique, and formal review remain separate gates.

## Frozen provenance and authorized delta

- Verified frozen input fingerprint: `f3d758904312bd734d7290f3de1aa8734a017a4f8e9fdf2c963b70ea59502355`.
- `shasum -a 256 -c inputs/frozen-inputs.sha256` passed for all nine declared inputs before the edit.
- Only `preview/p2-r6-text-label-system/app.js` changed. In `endInset`'s dome return on line 8, exactly one closing `)` was inserted before the function close.
- Candidate `app.js` SHA-256 is `a884ca36f46132e532507466f8d8bccd453a6c018f42e54b58090d21216a0a25`. Removing the sole inserted byte reconstructs 10,163 bytes with SHA-256 `58d6f543580238110357991e33394cded1cf79eba3ffded197092fca198a3a16`, exactly the frozen app hash. The candidate is 10,164 bytes; no other source/test byte changed.
- `index.html`, `math.mjs`, `style.css`, and `test_text_label_generator.mjs` retain their frozen SHA-256 values in `CANDIDATE_MANIFEST.sha256`.

## Analytic and module checks

- `node projects/laifen-wave-case/tests/test_text_label_generator.mjs` exited 0: `R6 text label generator analytic checks passed`.
- `node --check projects/laifen-wave-case/preview/p2-r6-text-label-system/app.js` exited 0.

## Fresh Chromium smoke

An ephemeral root loopback server ran at `127.0.0.1:8981`, returning HTTP 200 for the candidate `index.html` and `app.js`; its shell exit trap stopped it after the run. No route or service was altered.

`/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 projects/laifen-wave-case/scratch/r8/browser_smoke.py http://127.0.0.1:8981/projects/laifen-wave-case/preview/p2-r6-text-label-system/index.html` exited 0 with Playwright Chromium. It captured zero page errors, zero failed requests, and zero console errors; four Chromium GPU-stall messages were warnings only.

The exact 50-state matrix passed at desktop `1440x1000` and mobile `390x844`:

- Laifen screw and wide-short bayonet presets.
- Rounded, rotated regular polygons with 3, 5, 6, and 8 sides.
- Flat, chamfer, rounded-fillet, and dome end profiles.
- Shallow helix, flowing flutes, knit stitch, recessed diamond, straight micro flutes, and rugged hex patterns; bottom/top/center envelope fades.
- Integrated lanyard eyelet, keyring tab, bridge handle; safe inset and outset labels.
- Every valid state retained a canvas, exactly two core meshes, and a truthy total envelope. Unsafe text cleared to an invalid state with zero core meshes, null total envelope, and `textString` marked invalid at both viewports.

Machine-readable capture: `scratch/r8/browser-smoke.json`; the fixed matrix runner is `scratch/r8/browser_smoke.py`.

## Scope and remaining risk

No independent runtime defect appeared in this recovery. No CAD/OpenSCAD/STEP/slicer/print, routes/services, continuity records, or unrelated files changed. This receipt establishes implementation evidence only; it does not claim independent validation, review, delivery, CAD, artifact/slicer, or physical acceptance.
