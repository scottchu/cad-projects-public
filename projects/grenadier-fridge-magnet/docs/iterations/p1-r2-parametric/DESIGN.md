# P2-D frozen implementation contract

## Development parameters (not user-selected physical dimensions)
source_canvas_units=1254; working_mm_per_source_unit=0.1; xy_scale=1.0. Canvas therefore spans125.4 mm only as a canonical editable study; actual silhouette bounding width is derived. Source transform: X=(u-627)*0.1*xy_scale; Y=(627-v)*0.1*xy_scale. xy_scale>0; do not multiply Z by xy_scale.
back_thickness_mm=1.2; flat_face_depth_mm=0.8. Relief face depths above backing: low=0.4, middle=0.8, high=1.2; plate=high. Thus flat total2.0 mm, relief max2.4 mm are adjustable development values, not adoption/rejection of the user's tentative3 mm question. Require positive backing/depth and low<middle<high. Expose each parameter in source/CLI/config. Both variants share the same XY scale and source; changing one variant's height must not change the other or accepted artwork.

## Exact footprint and material partition
Read the accepted SVG paths with even-odd holes, or reproduce existing classifier masks and verify exact parity to written SVG. Use all five masks without smoothing/filtering. Their union is the black backing footprint. Back occupies0..back_thickness, each visible color column begins at back_thickness and extends to the assigned local face depth. Black face and black backing may be distinct named mesh parts assigned the same filament intent. No positive-volume intersections; shared faces/edges allowed. Thousands of components may be grouped as multipart meshes, but no unsupported floating Z columns; all touch backing.

## Semantic relief regions independent of color
Author source-coordinate regions, intersect with foreground; union of every semantic partition must be exactly foreground. Default body=middle, including tires and outline. Low glass includes glass colors AND reflected white/interior artwork within these source polygons:
windshield [(299,464),(334,292),(365,267),(904,250),(927,279),(931,453),(904,476)]; side-front [(971,285),(1029,307),(1050,497),(978,508)]; side-middle [(1044,313),(1100,326),(1120,490),(1065,500)]; side-rear [(1115,322),(1160,337),(1176,491),(1139,500)].
Low grille polygon [(236,628),(677,626),(681,818),(236,810)].
High lamps: ellipses (cx,cy,rx,ry)=(137,720,60,65),(288,732,59,60),(602,736,60,62),(802,727,65,69).
High bumper polygon [(36,804),(225,811),(263,831),(619,829),(673,809),(938,814),(944,938),(878,961),(690,971),(626,951),(279,951),(234,965),(79,919),(36,889)].
Plate region [(329,838),(583,838),(584,949),(326,949)] at high, including black frame, white plate and blue letters; these colors are locally coplanar. Priority plate > lamps > bumper > low regions > body. Region polygons/ellipse parameters are editable semantic masks, not edits to color/art. Use source-grid pixel-center membership to maintain exact column partition; boundary is native pixel grid. These are development approximations of accepted relative placement and need visual review; don't claim user accepted exact polygon vertices. A later correction can alter only region boundaries/heights.

## Independent feature-edit schema
Provide named feature records plate, grenadier_wordmark, lamps with source bounds, anchor, xy_scale=1 and stroke_offset_source_units=0. Canonical bounds: plate[326,838,584,949], wordmark[716,537,902,613], lamps as above. Default identity must exactly preserve original masks. This experiment need only expose schema and reject nonidentity settings as deferred/unsupported; do not pretend knobs alter art when not implemented. Later local XY scale/stroke changes will re-partition neighboring colors and require collision/spacing/visual evidence. No blanket whole-image dilation.

## Representation choice and risk
Reject per-pixel cubes and automatic tiny-feature deletion. There are6312 simple contour loops including4667 gray loops; all-BREP conversion risks disproportionate cost. Use exact polygon assembly with even-odd hole semantics and collinear reduction only. Available Shapely constrained Delaunay triangulation can triangulate polygon interiors exactly; extrude source polygons to closed manifold multipart meshes with matched boundary edges and outward winding. Preflight one color before full generation. Mesh-first is intentional for this flat artwork study; do not fabricate STEP parity or CAD-solid claims. Deliver parameterized source plus GLB colored study and per-variant/semantic-class STL or3MF only if tool path can preserve identity. No slicer-ready claim for glass-mix. If STEP omitted record not generated. Root may choose genuine BREP if measured cost is acceptable, but no need to block useful source/mesh model on6312 BREP loops.

## Delta mask
Accepted PNG/SVG and existing face source: read-only. New source: editable independent XY and Z, semantic masks, identity feature schema. New artifacts: generated solely from source. Forbidden: changing silhouettes/colors/lettering, adding holes or fifth real filament, choosing final print scale, asserting physically resolved details or glass mix.

