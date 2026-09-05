# VFR-08 C1 independent critique

Status: **PASS WITH ONE LOW EVIDENCE FINDING — both VFR-07 High defects are
resolved in the exact source and written meshes without a detected regression
to relationship B, threads, chamfers, protected dimensions, drainage-mode
exclusivity, or standalone/assembly geometry.** C1 may advance to independent
validation and formal review. This is digital repair acceptance only; it is not
browser, slicer, fabrication, or physical acceptance.

Owner role: `/root/openscad_vfr07_critic`, continuing as the independent
VFR-08 C1 critic. This document is the sole write. Candidate source, tests,
STLs, browser/runtime/vendor files, services, continuity, STEP/slicer, and
printer state were read only.

Verified critique-input manifest:
`inputs/VFR08_CRITIQUE_INPUTS.sha256`, SHA-256
`fbaeea2c3cc744511bea756f3ca26d1655990e894d19a2771ad902c10442db8c`;
all 9 entries passed. The nested C1 manifest
`candidate/VFR08_C1_CANDIDATE.sha256` passed all 17 entries. Exact reviewed
source: `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.

## Findings

### Resolved — selected drain holes cross the complete floor

The shared cutter now uses `center=false` for its central and six ring
cylinders. With the unchanged caller translations, the body cutter spans
`-0.1..3.1 mm` across the `0..3 mm` floor and the cap cutter spans
`80.9..84.1 mm` across the protected `81.01..84 mm` floor. Both intervals
extend beyond both floor faces.

Independent inspection of `diamond-bottom-body.stl` at `z=1.5` and
`diamond-top-cap.stl` at `z=82.0` found eight disjoint closed section cycles:
one outer contour and seven drain contours. Each drain wall has 96 distinct
XY positions at radius 1.5 mm around the required center. The selected pieces
are positive-volume, watertight, consistently wound single components with
Euler characteristic -12 and every edge used twice. There is no blind-roof
face corresponding to VFR-07's former `z=1.5` pocket roof.

The selected-minus-none volume checks match only the intended seven polygonal
floor columns:

| Style / selected end | Measured removed volume | `7 x 96-gon area x floor` | Difference |
|---|---:|---:|---:|
| Diamond body / bottom | 148.334297094 mm³ | 148.334297094 mm³ | `+5.7e-12 mm³` |
| Diamond cap / top | 147.839849437 mm³ | 147.839849437 mm³ | `-1.6e-12 mm³` |
| Smooth body / bottom | 148.334297094 mm³ | 148.334297094 mm³ | `+2.0e-11 mm³` |
| Smooth cap / top | 147.839849437 mm³ | 147.839849437 mm³ | `-8.8e-12 mm³` |

Drainage remains mutually exclusive. The diamond bottom-mode cap is
byte-identical to both the VFR-08 none-mode cap and the VFR-07 cap probe; the
diamond top-mode body is byte-identical to the VFR-08 none-mode body. The
smooth matrix has the same selected/unselected topology and volume behavior.
REQ-05's digital through-aperture requirement is satisfied. Actual water flow,
debris behavior, bridge quality around the holes, and physical strength remain
physical/slicer unknowns.

### Resolved — print layouts put both closed ends on the bed and openings up

`print_layout()` retains the body placement and maps only the cap by
`translate([-outer_diameter/2-3.5,0,cap_height]) rotate([180,0,0])`. This is a
proper rigid rotation and translation; standalone and assembly cap transforms
remain unchanged.

Both supplied layouts contain exactly two watertight components. Independent
coordinate-level comparison found exact rounded-`1e-7 mm` vertex and triangle
parity between each layout component and its corresponding standalone solid
under the prescribed transform. In both layouts:

- body closed end is at print `Z=0` and its opening is at `Z=144`;
- cap closed end is at print `Z=0`, its 2.99 mm cavity floor faces upward at
  print `Z=2.99`, and its opening is at `Z=84`;
- X envelopes are `[-42.5,-3.5]` and `[3.5,42.5]`, leaving the required 7 mm
  separation.

The former 754.2289 mm² downward cavity ceiling is now an upward floor at
`Z=2.99`; the closed exterior disk is on the bed. The diamond/bottom and
smooth/top layouts therefore satisfy the digital pose and separation portion
of REQ-10. Support-free slicing is still pending and cannot be inferred from
pose and mesh topology alone.

### No geometry regression found outside the authorized masks

The source diff from VFR-07 is limited to the two `center=false` edits, the
cap's print-layout transform, and explanatory comments. All lattice, field,
thread, bore/profile, shoulder, chamfer, standalone output, and assembly code
is byte-identical.

The manifest-bound diamond artifacts retain OD 39 mm, body/cap heights 144/84
mm, 30/31 mm bores, the 135 mm body seam, 3.00/2.99 mm floors outside the drain
mask, and the 1.2 mm end chamfers. Body and cap seam rings still contain the
same 99 exterior XY points after the declared `1e-8 mm` quantization. The
unselected cap's byte identity with the VFR-07 artifact additionally preserves
its B exterior, female thread, bore profile, floor, and chamfer as written.
The corrected depth-zero bottom body is byte-identical to the corrected smooth
bottom body.

All six manifest-bound STLs have positive volume, consistent winding, no
degenerate faces, and edge incidence exactly two. Standalone pieces have one
component; layouts have two. Drained standalone pieces have Euler -12,
undrained standalone pieces Euler 2, and each mixed layout Euler -10 as
expected.

### Low — `hashes.sha256` contains an invalid checksum for itself

The implementation receipt calls `scratch/vfr08-implementation/hashes.sha256`
the complete scratch inventory. Its 34th inventory entry records the empty-file
hash `e3b0c442...` for `hashes.sha256` itself, while the completed file's actual
manifest-bound hash is
`06acda97e079e405e62010bbf26d68fe8884b96327d4f2d3ab869e76f9748140`.
Running the inventory through `shasum -c` from the repository root produces 33
OK results and one self-entry failure.

This does not invalidate the C1 manifest: that separate manifest directly
binds the source, tests, six required STLs, analysis JSON, and completed
inventory and passes 17/17. It also does not cast doubt on the other 33
inventory lines, which all verify. The receipt should stop describing the file
as a fully self-verifying inventory, or a later evidence-only manifest should
omit the impossible self-entry. This low provenance defect does not require a
geometry repair cycle.

## Requirement and gate coverage

| Contract area | Critique result |
|---|---|
| VFR-07 High drain finding / REQ-05 | Resolved digitally for diamond and smooth selected ends; seven through apertures, expected genus, and exact removed volume. Physical flow remains open. |
| VFR-07 High cap-pose finding / REQ-10 | Resolved digitally in both written layouts; exact rigid parity, closed ends on bed, openings up, and 7 mm gap. Slicer evidence remains open. |
| Drainage exclusivity | Pass: `none` cuts neither part, `bottom` only the body, and `top` only the cap; unselected outputs are byte-identical to none references. |
| Relationship B / REQ-08 | Pass for changed scope: N33, plateau 0.18, shared phase, texture-to-seam construction, and exact seam point-set equality are preserved. |
| REQ-06/07 threads | No source regression; pitch, engagement, nominal clearance, embed, groove, and relief code are unchanged. Fit, cycling, elephant foot, torque, and strength remain open. |
| REQ-09 texture and walls | No source or envelope regression detected; default depth and protected wall assertions remain unchanged. Physical strength/feel remain open. |
| Protected dimensions/chamfers | Pass on source and exact artifacts outside drain masks. |
| Depth-zero/smooth equivalence | Pass: corrected bottom-body STLs are byte-identical. |
| Browser/worker performance and delivery | Not exercised and still open. VFR-08 grants no browser enablement. |
| REQ-13 physical acceptance | Open: no slicer, printed C1 parts, drainage-flow observation, fit cycles, loaded clearance, or physical seam inspection. |

The implementation receipt states the acceptance boundary accurately: it calls
the result implementation evidence, gives no implementer approval, and keeps
slicing, drainage, fit, strength, wear, and user-facing browser visibility
pending. Its only misleading evidence statement is the self-verifying
implication of the hash inventory described above.

## Evidence and disposition

Commands run from the assigned roots included:

```text
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR08_CRITIQUE_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR08_CRITIQUE_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR08_C1_CANDIDATE.sha256
diff -u projects/laifen-wave-case/scratch/vfr07-implementation/candidate.scad projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad
shasum -a 256 -c projects/laifen-wave-case/scratch/vfr08-implementation/hashes.sha256
PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider projects/laifen-wave-case/tests/test_vfr08_functional_repair.py projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
uv run python -B -
```

The focused test command passed all 17 tests. The final command was an
in-memory independent `trimesh`/NumPy inspection of the exact candidate and
inventory-bound STLs. It checked topology, dimensions, section cycles, drain
radii/centers, selected-minus-none volume, mode identity, rigid transformed
component parity, layout orientation/separation, horizontal floor normals, and
seam point sets; it wrote no artifact.

Disposition: advance this unchanged C1 fingerprint to the distinct independent
validator and formal-review join. Preserve the Low hash-inventory finding in
that join or correct it later as evidence metadata without presenting the old
self-entry as passing. Browser enablement, slicing, fabrication, drainage flow,
fit, strength, wear, and physical seam appearance remain outside this critique
and unaccepted.
