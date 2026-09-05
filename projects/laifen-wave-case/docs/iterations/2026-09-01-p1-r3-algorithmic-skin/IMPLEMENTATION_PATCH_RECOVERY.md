# IMP-GEN-02 representative-patch recovery

Owner `/root/generator_core`, 2026-09-02. DES04 inputs12/12 verified, fingerprint4490fc3feb8209557bf9270519ecaa0f5030641e189aee6edde2d2819e676c37. Recovery first attempt passed; no repair cycle used. This is implementation evidence, pending distinct independent review.

Changed key identity to `round(u % N,11) % N`, preserving actual UV/3D coordinates. Added paired logical/UV duplicate removal with deferred actual-surface agreement checks; split candidates are unique by identity and restricted to the same layer. Distinct-UV seam points remain. Degree/zero-length guards fail before OCC construction. Restored mirrored inner patch topology, preserving all genuine boundary subdivisions and common 3D edges/p-curves. Existing1e-8 join and1e-7 sewing tolerances are unchanged.

The first98-face recovery checkpoint used the earlier clipped plateau window and passed in0.1155s. For the final gate, the temporary top extent was increased from one to1.2 axial pitches beyond the band start so a COMPLETE full-amplitude plateau is present for measurement. This diagnostic extension stays inside the newly authorized128-face coupon budget and changes no final-case dimensions or skin field.

Final representative coupon:116 faces, one valid closed solid, volume50.5688739337mm3. Every canonical edge occurs exactly twice; sewing reports no free or multiple edges. Construction0.09818s, sewing0.000862s, solid validity0.01414s, complete probe0.12501s. Maximum shared vertex/curve discrepancy1.46499e-14mm. Actual surface sample radial discrepancy at actual theta/Z is0.0002313373mm; separate global rational-route proof bound0.0014097477mm. Direct surface-derivative normals yield maximum sampled axial/radial ratio0.359234; the independent conservative derivative bound is0.757638. Smooth cylindrical boundary radius discrepancy3.55e-15mm.

The actual complete plateau boundary was sampled from the rational BREP surfaces along its trimmed boundary, then developed using actual angle and constant terrace radius. The sampled-boundary convex hull's minimum directional width is1.0577941631mm. This is a geometric lower bound on the directional width of the whole developed boundary, distinct from the global analytic angular-metric bound1.0213879205mm. No bounding-box width or nominal-only assertion substitutes for this boundary measurement. The six plateau face portions include the complete plateau spanning the seam.

Reproduce from repository root:

```sh
uv run python projects/laifen-wave-case/scratch/generator-core/patch-recovery-probe.py
uv run pytest projects/laifen-wave-case/tests/test_generator.py projects/laifen-wave-case/tests/test_generator_geometry.py -q
```

Seven tests PASS, including exact seam witnesses, idempotence/periodicity, duplicate preservation and actual closed-patch geometry. Outputs are `scratch/generator-core/patch-recovery-final.txt` and `patch-fixed-pytest.txt`. Final tested source snapshot and test are in `inputs/patch-fixed-source/`; `inputs/patch-fixed-candidate.sha256` fingerprint3ea716c194ed438d3005a3ed7c2f1fae9389418b66df1ee031d85c86d0ac6c78. The snapshot includes later cap-blank helper code, but this receipt's acceptance scope is only the representative patch. Earlier98-face and failed112-face evidence remain separate and unchanged.

Authorized snapshot repair was completed afterward using `uv add --package laifen-wave-case --group cad-preview 'playwright==1.62.0' --no-sync` and root `uv sync --all-packages --all-groups`. Only project pyproject/root lock changed; added Playwright1.62.0, greenlet3.5.5 and pyee13.0.1. Headless Chromium151.0.7922.34 launch/close succeeded from root uv. Existing unrelated cadgen pin was not changed. Updated configs are bound in the passing snapshot manifest; prior config snapshots remain under scratch/generator-core/config-before.

The next authorized full cap exterior also passed:2234 faces, valid positive solid, construction4.199s, sewing0.05855s, total4.851s, volume46359.1999mm3 and maximum common-edge discrepancy3.28e-14mm. Its command/output are `scratch/generator-core/cap-blank-probe.py/.txt`. This is a filled outer blank, not a usable cap or accepted full case. The subsequent DES03 untextured C20 mouth probe reached a native tolerance-metadata gate; actual boundary diagnostics are recorded separately pending the design disposition. No full threaded cap export occurred yet. No STEP/mesh was generated, so primary-artifact snapshot and viewer remain pending; physical acceptance is unchanged.
