# PF-VAL-FULL independent validation

Status: **PASS for the bounded source/state and written-STL gates**. Browser/visual review, slicing and physical acceptance remain separate.

## Frozen provenance

- R1 geometry/source manifest: `/tmp/pattern-families-full-r1/candidate-source.sha256`, 37/37, SHA `cb8c804aa0e52ff64d4fe50cbddd4d09b805dbe9a662b7aa28ba694ff08a6b6d`.
- R1 build/evidence manifest: `/tmp/pattern-families-full-r1/candidate-artifacts.sha256`, 11/11, SHA `002c5675328de0f4c2b4099d99d9ff24ce5afec43069f7c8d9b6489963d82bc7`.
- R2 final UI/source manifest: `/tmp/pattern-families-full-r2/candidate-source.sha256`, 37/37, SHA `6701e4c3667e718455cf8ee622684c3d0e0f74971e51bc4f279f98b13554fc1d`.
- R2 build/evidence manifest: `/tmp/pattern-families-full-r2/candidate-artifacts.sha256`, 7/7, SHA `7e6cedbb7e104ecdacfde7199011449a24d9ebbb930689ef6af2bee3f5a2b0b4`.
- Geometry source is identical in R1/R2: `laifen_case_customizer_v1.scad` SHA `3b96cc2d5a5100e2daa2fe5a14c21e510728f108cfbc9afd5ae80bf1ef5dde40`.
- Independent candidate-binding test SHA `439d980c62bb3a7f6395ac86262620ad33805afe72eb9d83a0daf7eb73909491`; this reserved validator edit is outside the candidate manifest and invalidates only its oracle gate.

The initial C1 freeze exposed a real equality defect: new families rejected exact W4.56 at depth0.60 because subtractive floating arithmetic produced a value below1.8. R1 rearranged the same inequality additively. Independent tests now accept4.56 and reject4.55; actual source probes also reject4.5599999 and accept4.5600001 for all three families. R2 changed only controller accessibility and its regression; R1 geometry evidence remains bound to the identical SCAD hash.

## Source, math and state

Commands from repository root:

```sh
node --test projects/laifen-wave-case/tests/node/*.test.mjs
PYTHONDONTWRITEBYTECODE=1 uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -p no:cacheprovider
node projects/laifen-wave-case/tests/mesh/pattern-families/probe_wall_boundaries.mjs /tmp/pattern-families-full-validation/wall-probe-r1
node /tmp/pattern-families-full-validation/source_boundary_probe.mjs
```

Results: R2 Node **56/56**, Python **13/13**, independent oracle/binding **16/16**. The oracle independently derives Diamond fixed aspect/arc, count, actual arc, plateau, slope and literal ceil; Ribs `N/n`; Rings/Spiral `M`; all new-family `E`; wall equality; field/phase; and off-grid slider transitions. It binds those expected values to schema, adapter, bounds and controls. Actual pinned-WASM source assertions pass12/12 wall cases. Separate source witnesses accept Diamond136.7 and Rings `E=249984`, while rejecting Diamond136.8 and Rings `E=250368`.

## Fresh finite compile matrix

```sh
node /tmp/pattern-families-full-validation/compile_matrix.mjs \
  --source projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad \
  --source-sha 3b96cc2d5a5100e2daa2fe5a14c21e510728f108cfbc9afd5ae80bf1ef5dde40 \
  --runtime-dir /tmp/pattern-families-full-r1 \
  --matrix /tmp/pattern-families-full-validation/full-matrix.json \
  --out /tmp/pattern-families-full-validation/r1-matrix-01
```

All **21/21** jobs compiled without ERROR/WARNING using pinned JS `904a47f...18a62e` and WASM `f72ce24...c5ecf26`. Matrix receipt SHA `621c2f1f424e13fd36f0d80325957d419b78011ead0fd23c94df648058a515ad` retains every argv, output SHA/size and timing.

Coverage: Smooth and Diamond all four roles; default Ribs/Rings body+cap; default Spiral all four roles; edited Diamond body; Rings just-below-limit body; and the accepted stress Spiral body/cap/assembled. Exact byte parity passed for all eight original Smooth/Diamond roles and all three accepted Spiral-pilot roles; parity receipt SHA `4c9738dac8028cd1d519eda88f2b041fee50193dc6fb7fa3c207c1a2b4e156a6`.

## Actual mesh and geometry results

Basic mesh probes covered default Ribs/Rings/Spiral body+cap, Spiral assembled/print layout, edited Diamond body and the allocation-limit Rings body. Every mesh has positive signed volume, zero non-two-use edges, zero degenerate/duplicate faces, zero same-direction two-use edges, and the expected one or two components.

The warning-clean durable global certifier was rebuilt as SHA `4097183b2e3b5fe59e690af41c29e9072a649f89655d61340343f725decb9fca`; its adjacent/crossing/coplanar/T-junction self-tests passed. At1e-6mm it found zero unexpected nonadjacent intersections and zero geometric T-junctions in nine actual meshes: each default new-family body/cap, Spiral assembled/print layout, and the Rings allocation-limit body. Edited Diamond body also passed.

Independent field/feature probes compared every default new-family body/cap against default Smooth internals. All retain 15/15.5mm bores, body floor0..3, cap floor81.01..84, one outer plus seven drain loops, exact shared seam XY (Ribs640 vertices; Rings/Spiral192), and pattern excursion adjacent to both seam sides. Across actual exterior vertices, edge midpoints and centroids, maximum analytic radial error was **0.001314mm Ribs**, **0.006850mm Rings**, and **0.005203mm Spiral**, all below0.025mm. Protected thread/internal comparisons sampled672 rays per family; maximum delta from Smooth was `7.11e-15mm`. Receipts: Ribs `8c34ec...2082b7`, Rings `a47231...e8b0f`, Spiral `f2a374...66040b`.

Default Spiral assembled has two closed components, zero global intersections, and volume minus Body+Cap `5.82e-11mm3`. Print layout has two closed components, exact7mm X gap, volume delta `-9.17e-10mm3`, and center-offset ray witnesses show both openings face +Z; receipt SHA `ad944afb4921fbcb0c8cf22624541a8a87b184bf28bfe1c196f70e3ef6a32988`.

## Limits and next gate

This is the contract's finite risk set, not an exhaustive proof over arbitrary parameters. It does not replace actual browser/assistive-technology review, visual motif judgment, STEP or slicer validation, printing, drainage-in-use, grip, cleaning, thread strength/wear, fit or physical acceptance. Join this receipt with the distinct critic and root-owned browser evidence before formal approval.
