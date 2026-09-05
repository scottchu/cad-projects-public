# DES-EVIDENCE-06: bounded default source/STEP correspondence

Owner `/root/skin_design`, design role, 2026-09-02. Verified all53 paths of `inputs/geometry-default-candidate.sha256`, fingerprint `4e1ea38ac083f2f9b708770165bb2281748f129826f1f50bd1782139484a9ffd`. Read VALIDATION_DEFAULT and both failed surface-matching attempts. This explicitly reopens the **evidence method only** after the validator's repair ceiling. It changes no geometry, source, export, configuration or acceptance tolerance. Changed-pitch failure is outside this task.

## Finding and selected method

Use actual **mass centroids** to propose face correspondence, then certify matched supports and ordered true trim domains. `Face.center()` defaults and rectangular UV midpoints are unsuitable identifiers here. The earlier12.288mm control-net discrepancy came from wrong face pairs and is not geometry evidence.

Read-only body probe using `face.center(CenterOf.MASS)` achieved2311/2311 unique matches in8.717seconds. Maximum matched centroid separation was0.00003707389154mm; minimum distinct source centroid separation was0.08227830058mm. This clean separation identifies a practical candidate assignment; centroid agreement itself does not prove surface parity.

The representation follow-up found2294 Bezier-to-B-spline faces with one span in each direction, three B-spline-to-B-spline faces with2U/9V knots, and14 analytic faces. All matched faces have equal true boundary-edge counts. Positive-weight normalization gives control-net discrepancy bound1.4977292638e-11mm **if their bases are identified**; raw knot discrepancy is3.9757086512e-13. This is useful representation evidence, not permission to ignore knot differences or trimming. Most true p-curves are degree1 (9052 source Beziers/9054 written B-splines), with62 degree2 conversions and a small number of analytic/high-degree thread trims. Some thread p-curves change degree, so equal pole count cannot be a universal curve gate.

## Independent executable procedure

### 1. Candidate pairing and provenance

Verify the53-entry candidate before and after. Build each default source once and import body/C20/C25/C30 canonical STEP once; cache those read-only shapes within the run. Preserve the already completed motion/mouth/radial/assembly evidence; do not rerun it merely because face pairing was repaired.

Group faces by compatible support family (Bezier/B-spline together; analytic types separately). Propose nearest actual mass-centroid pairs; require a bijection and compatible true-wire count, area and support degree/span structure. Area is a descriptor, not a parity tolerance. If a cap has an ambiguous nearest match, use a small candidate graph with mass-centroid distance, true trim endpoint signatures and normalized support signature, then a one-to-one assignment. Never greedily reuse a written face. Default initial spatial candidate radius0.001mm is a search radius, not an acceptance threshold; if no candidate exists, report the exact unmatched class and do not silently expand it across unrelated faces.

Enumerate actual boundary wires and only FORWARD/REVERSED coedges. INTERNAL/EXTERNAL edges are not trimming loops. Preserve outer/inner wire role, orientation and cyclic edge order; require same topology under the assignment. Use exact surface representation and trims to disambiguate repeated supports, not only a global support hash: distinct trimmed faces can share one support.

### 2. Rational support bound, including knots

Convert Bezier supports to B-spline on copies. Apply face locations to poles. Normalize positive rational weights by one common positive scale per net (e.g. maximum weight), which leaves geometry unchanged. Account for U/V reversal or swap only through an explicit parameter transform also applied to trims; no unrecorded pole sorting.

For a corresponding pair of rational Bezier nets on the SAME normalized parameter square, let dN=max norm(wA*PA-wB*PB), dW=max abs(wA-wB), wmin=min of both positive weight sets, and Pmax=max norm(PB). The continuous support distance is bounded by `(dN+Pmax*dW)/wmin`, using the Bernstein convex-hull property. Degree-elevate to a common degree when needed. Nonpositive weights or unsupported periodic support are explicit stops.

For the2294 body one-span supports, normalize each actual knot interval affinely to[0,1] before comparing. That removes harmless differences in interval endpoints exactly; it does not assume raw knot equality. Use the same normalization for p-curves. For the three multispan body faces (probe indices125,126,137; identifiers are diagnostic only), convert each support into its exact rational Bezier knot-span patches on a COPY, retaining knot order/multiplicity. Corresponding source/written spans are mapped independently to[0,1]; the resulting piecewise affine global parameter correspondence accounts for the measured knot displacement. Compare every corresponding span net. Require the same ordered span topology or explicitly form a common subdivision by knot insertion on copies; never dismiss a knot mismatch solely because it is numerically small. Cap representation classes must be inventoried similarly.

### 3. Ordered trims and interior-domain coverage

Support equality on a rectangle does not establish equality of a trimmed face. In the established common parameter coordinates, match boundary loops, then cyclically pair edges by endpoint signature and direction. Establish a continuous normalized-parameter correspondence on each paired true p-curve, handling reversal explicitly.

For degree1 p-curves the endpoint/control comparison is already a whole-curve bound. For rational degree2 or higher, split at all crossed support-span boundaries, convert to rational Bezier segments, and restrict source/written curves to a common normalized edge-parameter partition. Insert knots and degree-elevate on copies, then apply the same positive-weight rational-net bound in2D. Different source/written degrees are allowed. Analytic lines/circles may instead use an analytic whole-interval bound. If correspondence cannot be represented this way, a derivative-bounded adaptive correspondence is permitted only for the isolated unmatched edge class; report the sampling remainder explicitly. Sparse points alone are insufficient.

Record maximum continuous common-UV boundary displacement delta and a bound L on the support's parameter derivative norm over the relevant spans. Convert it to physical trim error `L*delta`, using separate U/V bounds if tighter. Match all outer/inner oriented loops and their winding/domain side. With a pointwise continuous boundary correspondence and preserved loop topology, the straight homotopy changes winding only inside the delta-neighborhood of the boundary; this bounds the corresponding filled trim-domain discrepancy. For convex skin polygons this reduces to matching their cyclic vertices and interpolating the polygon interiors. Do not infer interior coverage from an unordered edge cloud or a UV bounding box.

Combine support error and propagated trim-domain error for each face: **total<=0.01mm**. A useful work allocation is support<=0.002 and trim<=0.008, but the authoritative criterion is their proved sum, not either suggested allocation in isolation. Preserve the separately stricter mouth boundary<=0.001mm and measured mouth endpoint/plane<=0.0001mm gates from DES03/DES05. Do not invent exact volume equality or keep the prior exploratory1e-7 support-only assertion as a replacement for the complete physical error budget.

For the14 body analytic faces (4 planes,6 cylinders,4 cones), compare located analytic axes/origins/radii/angles and bound displacement over their finite trim extent, then apply the same true-loop domain check. Equal type alone is not sufficient. Handle cap plane/cylinder/cone classes identically. A new unsupported family is an escalation with its count and exact face descriptors, not an excuse for broad sampling.

### 4. Skin slope, seam and remaining dimensions

Complete written cap face-interior normal/radial witnesses for all caps, as the validator already did for body; choose an actual point inside the trimmed face (classify it), not a default UV midpoint outside a trim. Retain the analytic DES02 radial/slope/plateau bounds as source construction evidence, and bind that construction to the written one-span nets via the support/trim result.

For a whole-written-skin slope claim, also bound rational first-derivative differences from Bernstein derivative nets (`S_u=(N_u*W-N*W_u)/W^2`, similarlyV), with positive denominator lower bounds. Bound normal perturbation by `|S_u|*eV+|S_v|*eU+eU*eV`. The source skin horizontal-normal magnitude has a positive lower bound from radius, exact-circle angular derivative and nonzero Z-span; compute it per span. Transport the source slope bound0.757638255 using that perturbation and require the resulting bound<=1. This is a coefficient calculation, not a dense normal sweep. If that conservative bound is inconclusive, refine only the affected parameter span; finite normal witnesses remain corroboration, not a global proof.

Verify periodic seam from mapped true boundary incidence/orientation and paired seam curves on both sides; ensure integerN closure, no duplicate endpoint strip, and the same smooth band-boundary circle. Valid solid topology plus correct ordered trim correspondence and bound supports the seam; the existing seam-side rays corroborate it. Complete actual floor/OD extrema and plateau-width checks already named in VALIDATION_DEFAULT. Plateau witnesses alone do not establish minimum width: identify the full-height plateau trim polygons, measure their boundaries/metric or conservatively transport the established1.021387921 lower bound with an explicit positional/metric error budget that still leaves>=1. Do not treat the global0.01 tolerance as automatic plateau acceptance without that budget.

## Bounded execution and stop conditions

New validation workstream gets one initial attempt plus one focused **method** correction, with four parts processed sequentially and checkpointed. Target<=180seconds per part after source construction; hard ceiling12minutes overall for this correspondence continuation. Cache signatures/conversions; keep per-face details only for failures and summarize counts/maxima. No new CAD exports or parameter redesign.

First complete the body bijection and its2294 one-span support/linear-trim branch. Then handle the three multispan supports and small analytic/curved-trim exception set, before repeating the same established method on caps. Stop at the first unsupported support/trim class, ambiguous/nonbijective assignment, orientation/domain inconsistency, nonpositive weight, derived error>0.01 (mouth>0.001), or exhausted time/repair ceiling. Return class/count, exact source/written face/edge descriptors and failed bound. Do not restart all successful gates or extend to the separate changed-pitch failure.

## Receipt

Read-only commands, both exit0:

- `uv run python projects/laifen-wave-case/scratch/export-evidence-design/centroid_probe.py > projects/laifen-wave-case/scratch/export-evidence-design/centroid_probe.txt 2>&1`
- `uv run python projects/laifen-wave-case/scratch/export-evidence-design/representation_probe.py > projects/laifen-wave-case/scratch/export-evidence-design/representation_probe.txt 2>&1`

These probes choose the method and inventory actual representations; they do not complete global export acceptance. Changed paths are this contract, `inputs/export-evidence-*`, and `scratch/export-evidence-design/` only. Candidate fingerprint and exact diagnostic files are bound in `inputs/export-evidence-contract.sha256` / `.fingerprint.txt`. No source/test/artifact/config changes. Root verifies freeze, assigns the bounded reopened validator, then joins independent critique and formal review. Global STEP hold remains until this evidence is completed; no mesh/slicer/physical acceptance is claimed here.
