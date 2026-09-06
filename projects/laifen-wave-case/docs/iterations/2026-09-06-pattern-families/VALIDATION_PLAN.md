# PF-VAL — risk-driven validation plan

Planning inputs: DESIGN `426729855f05805f16661cc3728a6145b2eac291b56f60199fc6ca7528cc3e61`;
BRIEF `28483df404ab8b99528cdedb71ba98ef4f2f1146015a0b110904a7d4c78f71b6`;
failed pilot validation `95ed14bea5171a4b7789d8072782d31b555418e485cb49ca2e12f6a183faa2eb`.
This plan makes no claim about the moving repair. Bind every run to a frozen candidate manifest and retain source/runtime/argv/output hashes and timings under `/tmp/pattern-families-validation/<manifest-sha>/`.

## Gate 1 — repaired Spiral pilot; stop on any failure

1. Verify the candidate before and after the run: `shasum -a 256 -c "$candidate_manifest"`.
2. With pinned JS/WASM hashes `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e`/`f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26`, compile fresh D30/H60/W4.6/T3/manual-lid25.3/Spiral-s4-d0.6/Bottom-N7 Body, Cap and Assembled STLs:
   `node /tmp/pattern-families-validation/compile_matrix.mjs --manifest "$candidate_manifest" --set repaired-pilot --out "$run_dir"`.
3. Rebuild the existing certifier warning-clean:
   `clang++ -O3 -std=c++17 -Wall -Wextra -pedantic projects/laifen-wave-case/tests/mesh/surface-pattern-global/mesh_certifier.cpp -o "$run_dir/mesh_certifier"`.
4. Run it at 1e-6 mm on Body and Cap, then Assembled with the derived seam Z; require zero nonadjacent intersections and geometric T-junctions:
   `uv run python /tmp/pattern-families-validation/run_pilot_certification.py --certifier "$run_dir/mesh_certifier" --artifact-dir "$run_dir" --output "$run_dir/global.json"`.
5. Run `uv run python /tmp/pattern-families-validation/mesh_probe.py "$stl"` for all three; require outward/positive signed volume, zero non-two-use edges, degenerates and duplicate faces, Body/Cap one component, and two component shells in Assembled.
6. Explicit regression: failed hashes `71914b7d35dd75d0807b41309fb72bf7420e352bdd63eeb0fe2d27aca8be06fc`, `c33e58dab14d5f525a664f1cfb48e470ceb03ef0cd8839d3d69003e5beeab4e9`, `a7008ef90eb992640ee94398b5ebcfb89abb884955636e2078346d4b02a77428` had negative orientation and 8,055/2,513/19,015 intersections; no repaired artifact may reuse those bytes or face defects.
7. Only after 1–6 pass, probe exact 15/15.5 bores, floors including cap 0.01 overshoot, male/female thread profiles, seven Bottom drains, no external collar, zero positive Body/Cap collision, and exact shared seam XY ring/phase.
8. Classify actual exterior vertices, edge midpoints and centroids against Spiral `r=R-d*(1-cos(phi))/2` plus the owned chamfer clip; require maximum radial error <=0.025 mm, including the envelope-facet chord contribution.
9. Extract baseline SCAD with `git show c181dda780a3b9c407ebe3419702419254266792:projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad > "$run_dir/baseline.scad"`; compile baseline and candidate with the same pinned runtime and compare default Smooth/Diamond bytes.
10. Known sentinels must remain exact: Smooth Body `db78a5eb2a24a16d47ae0e8837003115ee573812016ef443715997aea07474a2`, Cap `646efb49c116b47b49521872c0e35af724053f9fbaa619c412aca40009e0b7d0`, Assembled `b1b9db18e21cafed5237afb90e57831b72246c6ac2e4b4c88f736738fd0cf169`; Diamond Body `6789c6b1ade20b205646bcc2e5eb17d22b515e47c6e3fd1fd5688390376f60c8`, Cap `e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514`, Assembled `5cfe2f06339bcc3df70dbc7072448789e5078aee9998a6599016298a148260fe`, Print layout `73dc750bd9bea35d1e65e4cd05ec7a56b1cc5cdd42faf8a1649455694d83062e`. Generate the missing baseline Smooth Print-layout witness before comparing it.

## Gate 2 — finite source/math/state witnesses before broader CAD

- Independent oracle: each new family at spacing 4/16 and depth 0.10/0.60; wall equality `W=3.95+d+0.01` and 0.01 below; all source bore/thread/entry residuals; finite/NaN/Infinity rejection.
- Ribs count rounding: spacing `6.13818872316775` and +/-1e-9 at default R/d; assert round-half-up and `n=max(192,32*N)`.
- Rings/Spiral ceil: spacing `6` and +/-1e-9 at default Body h=135; assert the exact `M=ceil(h/(s/16))`, extra-row, clip and `E<=250000` operation order for Body and Cap.
- Diamond: size/depth endpoints, derived arc exact default 3.63, count/plateau/slope/wall guards and the preserved literal 136.8 ceil boundary.
- Slider/state: 4.83→Right4.9/Left4.8; 0.43→Right0.45/Left0.40; Home/End, pointer tie-up, blank/non-numeric thumb hiding, coupled disable/repair, switch-away/back invalid-memory preservation, inactive exclusion and normalized full-snapshot identity.
- Commands: `node --test projects/laifen-wave-case/tests/node/*.test.mjs` and `PYTHONDONTWRITEBYTECODE=1 uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -p no:cacheprovider`.

## Gate 3 — bounded five-family artifacts

- Fresh matrix: default Diamond/Ribs/Rings/Spiral Body+Cap, default Spiral Assembled+Print layout, edited Diamond, and one valid just-below-allocation-limit new-family witness. This covers all four roles without a Cartesian parameter grid.
- Apply topology/orientation/global certifier, protected-feature, drain and radial-error probes to every Body/Cap; apply exact volume/collision semantics to Assembled and two closed components, 7 mm X gap and openings-up checks to Print layout.
- Require each selected field equation and global phase; Ribs must be axial, Rings horizontal and Spiral six-start with one ridge rising `6*s` per revolution. Require depth zero parity with Smooth where supported.
- Run one scratch build only after deterministic gates:
  `npm run build:openscad-simulator --workspace laifen-wave-case -- --outDir "$run_dir/dist" --emptyOutDir`.

## Gate 4 — browser and acceptance boundary

- Root-owned Chrome checks at 1280x900 and true 390x844: five labelled 44 px cards/cues, 3+2 mobile wrap, selected group placement, no overflow, exact/off-grid sliders, invalid repair, independent memories, explicit Generate, stale/current download and Blob/STL byte identity.
- Generate representative real jobs for every family and all four output roles across the set; inspect the actual returned STL/render, not selector text or a proxy mesh. Reuse the corrected real-worker Cancel/supersession harness if lifecycle code changed.
- Safari/iPhone, STEP/CAD authority, slicing, supports, grip, cleaning, drainage-in-use, thread strength/wear, print, fit and physical acceptance remain separate and open.
