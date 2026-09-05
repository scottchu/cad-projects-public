# VAL-GEN-01 independent default validation

Owner `/root/thread_export_validate`, 2026-09-02; independent validator, baseline `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`. **STEP gate HOLD: global source/export surface correspondence remains unresolved.** No measured geometry failure was found in the completed gates. Do not generate fabrication meshes on this receipt alone. The comparison probe exhausted its initial attempt plus one focused correction and must be reopened with a better correspondence method.

Frozen candidate: all53 entries of `inputs/geometry-default-candidate.sha256` verified before, after the main probe, and after the surface probes. Unchanged fingerprint `4e1ea38ac083f2f9b708770165bb2281748f129826f1f50bd1782139484a9ffd`. Read BRIEF/DESIGN and DES02..DES05, current source/tests and prior patch/thread receipts. No source, tests, configuration, artifacts, services or dependencies changed. Exclusive writes: this receipt and `scratch/generator-validation/`. All owned processes completed.

## Completed gates

### Four parts and source/export sections

Built actual default source body/C20/C25/C30 and reimported each canonical STEP. All are one positive-volume valid solid; source/written face counts agree: body2311, C20/C302274, C252277. Seven CLI STEP outputs are byte-identical to the corresponding seven canonical STEP siblings.

Independent line/face intersections measure104 thread samples per part at eight angles and13 axial positions spanning leads, full-form ends, flanks and the former filled valleys:416 samples total. Worst written/contract radial errors are body0.000035964308, C200.000036377687, C250.000036481034, C300.000036584380mm. Maximum source/written radial difference is0.000034167606mm. All pass the unchanged0.01mm contract. Fifteen body bore measurements give radius15; twelve per cap give15.5, within1e-7mm. These are actual-solid measurements, not merely matching scalar inputs.

Seventy-seven actual skin rays per part cover band ends, fades, cores, seam sides and external smooth margins:308 samples. Worst written/analytic radial discrepancy is0.000229024094mm; source/written discrepancy at those samples is below9e-12mm. Raised height samples cover approximately0..0.45mm, with tiny negative numerical residuals no larger than9e-12. Body/cap band limits used are[-30.1,-6.1]/[14.4,38.4], each24mm; rays1mm outside each band match the smooth radius. This finite sample result does not prove the whole surface by itself.

The body whole-skin probe evaluated2108 written face-interior witnesses: no inward radial normals, maximum normal slope ratio0.352591016, maximum analytic radial error0.000231565454mm, minimum radius residual-8e-12mm and434 full-height plateau witnesses. The DES02 algebraic route independently states whole-field radial bound0.001409747706mm, slope bound0.757638255 and plateau-width lower bound1.021387921mm. Those analytic route values support the construction but do not replace the missing final whole-surface source/export correspondence. Cap whole-skin normals and independent actual plateau-width checks did not run before the probe stopped; implementation representative-patch evidence remains separately attributed.

### Repaired mouth boundary, all three clearances

True mouth boundaries exclude TopAbs_INTERNAL/EXTERNAL edge occurrences. Source includes three internal edges beyond the nine true FORWARD/REVERSED boundary edges; written STEP has nine true edges. Counting internal edges as boundary would create a false mismatch.

All source and written actual mouth endpoint, lifted-p-curve endpoint and complete trimmed-curve Z-bound checks pass DES05's unchanged1e-4mm limits. Source C20 maximum endpoint error0.0000438174495mm and lifted-p-curve endpoint error0.0000438221703mm; C25/C30 maxima are approximately0.00000684/0.00000688mm. Minimum whole-curve Z lower bounds are0 within floating residuals under5e-17mm. Native C20 vertex tolerance0.000134425805mm is retained and triggers these geometric checks, as DES05 requires; it is not rewritten or mistaken for measured error.

Bijectively matched true boundary curves use a normalized-parameter correspondence plus derivative control-polygon/analytic speed bounds. Maximum continuous correspondence bound is0.000200000000004mm for each clearance, below the unchanged0.001mm gate. This independently resolves the old R2 below-mouth extension for the three default caps; it is a complete bound on these compared mouth edge sets, not a whole-solid certificate. The main probe reuses audited endpoint/control-hull helper logic but implements its own true-boundary filtering and assignment; measurements are from newly built source and frozen written STEP.

### Assemblies and motion

Written closed/exploded/layout files are valid with2/2/4 solids. Expected transformed part vertices match the assembly vertex sets with maximum discrepancy below8e-27mm; closed/layout are exactly zero numerically. Closed assembly spans Z=-35.1..43.4, total78.5. Exploded C25 uses gap11/rotation1620 and spans to54.4. Print layout uses body translation(-23,-23,35.1) and cap placements(23,-23),(-23,23),(23,23), each Rx180/Z43.4; minimum Z0, maximum44.1.

Nine independently run written-solid intersections at beta37,333 and1080 for all clearances are zero, including the former g6 defect. Negative closure g-0.02/beta-3.6 yields positive stop volumes (C254.318284756 and C304.207229456mm3; exact C20 value in log), confirming sensitivity. Audited implementation `final-pytest.txt` additionally records all30 prescribed written poses as zero; its test source also requires extraction9..11, positive stops, floor occupancy and print-pose glyph membership. Those broader results are implementation evidence, not rerun independent results.

Cavity72.5 and floors3/label-floor2.8 follow the named source planes/stack and audited implementation floor probes; this validator independently measured external height and bores, but did not complete separate exact inner-plane/OD extrema measurement before the surface stop. DES03 explicitly supersedes raised labels with0.20 recesses, so that construction is authorized. Physical glyph readability is pending.

## Blocking evidence gap and smallest continuation

The full-surface probe attempts to match each source face to a written face before comparing rational surface control nets. Initial UV bounding-box midpoint descriptors produced only1879 unique target matches for2311 body faces. One correction to `Face.center()` still produced1878 unique targets, because that default also fails to distinguish the repeated patch centers. Both runs stop at the bijection assertion. Their reported12.288mm control-net discrepancy is **invalid correspondence evidence**, not an established geometry error, and must not be used to reject CAD or relax tolerances.

No global<=0.01mm source/export boundary/surface certificate follows from the successful radial samples, equal counts, near-equal volumes or this failed match. Source/written volume pairs are body13821.638439489/13821.635948943, C2013638.861946401/13638.864915240, C2513577.338524345/13577.339197355, C3013515.398222429/13515.397965663mm3; no arbitrary mass equality threshold was imposed.

Next bounded validation task: use actual mass centroids (`CenterOf.MASS`) plus face trim/control-net signatures or a global assignment, verify a bijection, and bound equivalent rational supports and true trim-domain correspondence. Handle rational weight normalization and knot differences explicitly; finite support samples are not a whole-surface bound. Then complete cap face-normal witnesses and exact floor/OD measurements, review actual plateau-width evidence, and issue the final STEP decision. Current hold is an incomplete validation deliverable, not a requested source redesign.

## Provenance and unsupported cases

The CLI manifest correctly records generating helper SHA256`25391b9237e75afd07e14e865881b8bbe77ad23522728e6245950bf8a7198404`, preserved at `inputs/geometry-mouth-stage/thread_profile.py`. Current frozen helper is`5f4ab31f844551780415dc528d5ae01e0bc626ba9ab5e5c74b3789a8ac25b13a`. Exact diff adds `require` imports and a positive-volume/one-solid rejection after the unchanged female Boolean; it makes no constructive geometry change. Newly built current default source passes the measured parity gates against those artifacts, but this receipt does not misstate the older generating hash.

Changed p2.4/E7.2/C82.1/H47 currently produces an empty female void and is deliberately rejected. It is outside this default acceptance attempt and needs separate design diagnosis. No general pitch/domain acceptance, mesh/slicer acceptance, visual acceptance, print fit/wear/grip comfort, strength or full Laifen brush fit is claimed. Independent snapshot critic and formal-review joins remain separate.

## Commands and evidence

All commands from repository root through its uv-managed Python3.12:

- `uv run python projects/laifen-wave-case/scratch/generator-validation/validate.py > projects/laifen-wave-case/scratch/generator-validation/validate.txt 2>&1`: exit0, `FOCUSED_VALIDATION_COMPLETE`; checks all53 hashes at start/end; structured `results.json`.
- `uv run python projects/laifen-wave-case/scratch/generator-validation/surfaces.py > projects/laifen-wave-case/scratch/generator-validation/surfaces.txt 2>&1`: initial exit1 at non-bijective face assignment. Original script reconstructed exactly as `surfaces-initial.py` by reversing its one descriptor edit.
- Same command with output `surfaces-corrected.txt` after the one permitted descriptor correction: exit1 at the same assignment gate. No further repair attempted.
- `diff -u .../inputs/geometry-mouth-stage/thread_profile.py .../cad/p1_r3_generator/thread_profile.py`: verified guard-only delta. A final read-only SHA256 loop again verified53/53 unchanged.

SHA256 evidence: `validate.py`2c7e241ec36c8a80cebc7ceaf2e6fbcffb662b7cb99c214fd9204e9c1bd8f0ba; `validate.txt`7fbd83e0a3b538800dd8119e00aa582b5413cef9884f9f9c38994bd2d978559a; `results.json`f2b2fca075315770e8e80951988c1ccdf9da21674b566802420844f9e50a1d95; `surfaces-initial.py`ecec66065961b5bab0f6079c7887bfb2c33ba149251b6890761ea74099e38c2b; `surfaces.py`c2b0f37e097f30c1e81b088dbc6b3f503a0665c944c73450e923fd71f1644716; `surfaces.txt`2f6d81113a5f866bfbfbecd6f8ce38f03781194f7380cb0f69d8338c3479bf00; `surfaces-corrected.txt`ae38390fd6aa864fb23ac91997096637bc515528df8ad4e996e4b9ba004a7263.
