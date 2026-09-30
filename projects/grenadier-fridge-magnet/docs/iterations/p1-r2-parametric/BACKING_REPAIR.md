# P2-D2 — backing-only connectivity repair

## Superseded clause and observed defect
This addendum supersedes only DESIGN.md's exact-foreground backing footprint clause. Original BRIEF/DESIGN, input-manifest and candidate1e5f22bf7437b8cf29b7ae612e04258a2f507aa94908d05ae1cb8631458fcb3d remain historical bytes; do not overwrite old candidate artifacts.

Independent validator /root/parametric_mesh_validation reports from written GLB:179 backing components; total1,011,482 source-pixel². Main component1,011,159 pixel² with NO holes, bounds[3,126,1250,1142].178 exterior islands total323 pixel²; all outside main outerloop, nearest boundary distance0 or1 source units. Overall bounds[1,126,1251,1144]. Filling the main exterior adds0 and includes0 islands. These tiny background-adjacent fragments were retained by exact source classification; they are not demonstrated physical vehicle parts. Bitmap classification artefact is the likely cause, not independently proven provenance. Exact foreground backing and continuous backing are incompatible.

## Frozen selected repair
Preserve ALL accepted visible color masks and every original foreground pixel. Modify only black backing at0..back_thickness. Add deterministic source-grid connectors that merge every footprint component into one FOUR-neighbour connected footprint; point/corner contact is insufficient. Choose shortest background-cell paths from components to the connected main footprint, preferring fewer added cells with a deterministic lexicographic tie-break. Reuse connectors rather than duplicating them. No deletion, smoothing, global dilation, convex hull or recoloring. No disconnected component may remain as a floating face.

Conservative permitted delta ceiling: at most2 added source pixels per original detached island, at most356 added pixels total, every added cell within Chebyshev distance2 cells of original foreground, and within existing overall pixel-grid bounds[1,126,1251,1144]. This ceiling is a bounded design allowance, NOT a measured required addition. Record actual added-cell list/count and connection proof. If these ceilings cannot produce one footprint, STOP and report the smallest unsatisfied link; do not expand allowance silently.

The visible artwork above backing is unchanged. Added black backing is physically visible through previously empty near-contour cells, so overall combined top-view silhouette is not bit-identical. At default0.1 mm/source-unit this bounds local connector reach to0.2 mm; it scales with XY. This is an expressly disclosed local development repair within continuous-blackback intent, requires fresh front/oblique visual review, and does not reopen final-size selection. No physical minimum-strength claim: these connectors may remain too thin until later scale/slicer work. Blackback connected geometrically is not yet magnet-strength proof.

## Per-object delta mask
- D4, accepted SVG, five face masks, letters/lamp regions, semantic heights: immutable.
- Black backing only: addition of bounded grid connectors, same Z0..1.2 development thickness parameter; one connected footprint, no exterior-bounds growth.
- Source: implement named backing_connectivity helper; expose actual delta report; no arbitrary smoothing knobs.
- New exports: new repair namespace; regenerate both variants from source; retain historical candidate artifacts/manifests.
- Indexed mesh representation repair (pinch topology/serialization) may preserve the exact geometry; it may not change face masks under this contract. This addendum does not claim to solve STL welding defects; indexed GLB remains development delivery until independently checked.

## Focused acceptance gates
1. Original mask subset of repaired backing; added pixels satisfy every ceiling and bounds; FOUR-neighbour component count=1.
2. Actual written backing mesh one watertight connected shell with positive volume; volume equals repaired pixel area times XY area scale times backing depth.
3. Every original color column contacts backing; no positive-volume overlap; exact face masks and heights unchanged.
4. Independent front/oblique snapshot, actual silhouette addition disclosed. Main face/type/lamps unchanged. Structural and print acceptance remain separate.

## Task/receipt
P2-D2 owner /root/parametric_magnet_design; design-only, initial+1repair/2minute target, read frozen candidate and independent V measurements, exclusive new backing contract/manifest/status, no implementation/network/printer. P2-I2 depends on revised immutable input manifest; C/V/R must bind to new generated fingerprint. Historical candidate is rejected for disconnected backing, not erased. Next action implement connector algorithm and report measured delta before full exports.
