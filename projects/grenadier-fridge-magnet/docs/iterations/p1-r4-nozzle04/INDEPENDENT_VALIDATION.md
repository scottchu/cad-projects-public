# P4-V independent native-profile comparison

Owner `/root/slice_artifact_validator`, distinct from preparation `/root/slice_settings_diagnosis`. **Both 0.4 mm diagnostic slices complete, but GRENADIER white strokes are incompletely retained at the displayed surface layers compared with the 0.2 mm baseline. No print release.** Source geometry and working size remain unchanged.

## Frozen inputs and execution

Final validator fingerprint `96f8e8046ddb896e59e0bf8e07d10511745defc4fde1e8e0ff1e44a971bcb68f`: `slicer/p1-r4-validation/toolpath-input-manifest.json`. Exact numeric results: `slicer/p1-r4-validation/toolpath-validation.json`. This freezes the P4 brief, preparation manifests, resolved profiles, both Gcodes and archives, independent extractor and P3 comparison evidence. Before parsing, the extractor reverifies every path/content hash in P3 package, toolpath and review-media manifests, preserving that authority chain and exact source packages.

```sh
uv run python projects/grenadier-fridge-magnet/scripts/validate_nozzle04_toolpaths.py 354ccfc88f75ce3ae4040dc92e991f8083cb77d95c17e54d0188298ae87555b0 7c3ba1a39336c0dfd53c05fc0d428658f4ef49d9a1536d713ed438db63b0a326
```

Exit 0, initial parse plus one focused PNG-rendering correction and rerun. All existing P3 scripts and evidence remained unchanged. The dedicated P4 reader retains the prescribed G90/G91, M82/M83, G92, positive-extrusion, object/prime-tower distinction, declared line-width, and tool/layer parsing methods. No extrusion arcs were present. Firmware macros remain unsimulated.

The initial PNG renderer rounded widths at 12 pixels/mm, creating artificial diagonal gaps. At an inspected top-fill path, declared width 0.426079 mm exceeds approximately 0.409 mm perpendicular path spacing; the pronounced low-resolution hatch was therefore not evidence of a physical gap. Final PNGs supersample at 48 pixels/mm and downsample to 12; SVGs retain the exact declared widths and were unchanged by this repair. Use SVGs as path-width authority. Initial parser fingerprint `c96bac9c8e7e2821ed314d5b5db92bc3c22825ae0ead2992d6d00b783f6904b8` is superseded for media; no initial media is delivered.

## Actual outputs and comparison

| Variant | 0.2 profile baseline | 0.4 profile diagnostic | Change |
|---|---|---|---|
| flat | 25 layers; 6h52m1s; 18.37 g; 30 tool changes | 23 layers, Z0.20–1.96; 3h45m53s; 23.15 g; 27 tool changes | Estimated 3h6m8s faster, about45%; +4.78 g |
| relief | 30 layers; 7h12m22s; 19.62 g; 45 tool changes | 29 layers, Z0.20–2.44; 4h12m17s; 22.43 g; 45 tool changes | Estimated 3h0m5s faster, about42%; +2.81 g |

Time and mass are native slicer estimates, not measured print outcomes. Both new children exited0. The independent reader found complete executable blocks and actual T0/T1/T2/T3 extrusion in both. Print-temperature commands include220°C nozzles and65°C bed, with native preheat/cleaning/standby commands retained. Both sliced 3MFs embed Gcode byte-identical to the separate files; neither contains PNG/JPG thumbnails.

- Flat Gcode SHA-256 `354ccfc88f75ce3ae4040dc92e991f8083cb77d95c17e54d0188298ae87555b0`; flat 3MF `feefeb095763afdb98af0662d19fdce93531299f91f251156657d19ec6ba6fc4`.
- Relief Gcode SHA-256 `7c3ba1a39336c0dfd53c05fc0d428658f4ef49d9a1536d713ed438db63b0a326`; relief 3MF `27b2890169d7d2d99ea8a51fdf1920cd6e87c1878a780b7f19a54dae8d324b50`.

Source multipart3MF geometry remains125×101.8 mm with [135,136,0] whole translation. Both 0.4 object extrusion centerline bounds are X72.81–197.09, Y84.71–185.89 mm, versus X72.71–197.19, Y84.61–185.99 for0.2. This inward centerline shift is consistent with wider paths on the same positioned geometry; it is not a scale change or a bead-envelope measurement.

Native machine nozzle arrays verify four0.4 mm entries. Both use nominal0.08 mm High Quality layers, but0.4 uses0.20 mm first layer versus0.10, two walls versus four, wider nominal0.42–0.45 mm paths versus0.22, and different shell/speed defaults. This compares complete native profiles; it does not isolate nozzle diameter as the sole cause of changed detail, time or mass.

## Independent actual-path observations

Final media fingerprint `10e249a13ae7a74f5a449d5755ca21cb145b2402e4cc1f27522f1d2af76a5162`: `slicer/p1-r4-validation/review-media-manifest.json`, 16 SVGs and16 PNGs. Flat crops use Z1.96; relief wordmark uses Z2.04 and plate/lamps Z2.44. The three relief whole views are distinct layer planes, not a simulated final composite. Blue-gray background denotes no depicted path at that layer, not necessarily a through-hole.

Directly inspected flat whole, both plate and wordmark crops, and all eight lamp crops; re-inspected both wordmarks, flat plate and central lamp after the PNG correction. Compared with the P3 actual-path feature views:

- **High for detail acceptance — wordmark (corrected observation):** `GRENADIER` changes from individually readable white strokes to incomplete small white fragments in both0.4 variants. The broad letter-shaped blue-gray region is background `#ccd5de`, meaning no depicted extrusion at that selected layer; it is not fused solid-white lettering. Each0.4 wordmark SVG contains85 white path segments versus499 in each0.2 crop, corroborating reduced white-path presence without quantifying missing area. Do not claim the unchanged wordmark passes small-detail acceptance at this native0.4 profile.
- **Limited pass — plate:** `DJZY 608` remains readable in both0.4 variants, including the main internal spaces of D/6/0/8. Edges are coarser and small local voids/irregularities remain. Blue is still confined to the plate ROI in the selected layers: all546 T3 segments per variant lie there. Legibility in path media is not printed legibility proof.
- **Limited pass — lamps:** all four main circular rings and main internal motifs survive in both variants. Central concentric gray/white details become wider, less separated and locally merged compared with0.2. Fine outer accents remain incomplete/fragmentary. No exact loss-area or global artwork-fidelity metric was performed.
- **Open:** glass and pale-blue plate antialias regions remain provisionally T2 white, so no accepted mixing or original-color-fidelity claim. Very thin variable-width paths still appear; a0.4 nozzle profile does not guarantee physical reproduction of those widths. Structural connectivity, pinched contacts, adhesion, backing strength, magnets and physical detail remain unverified.

中文交付摘要：**0.4原廠設定預估快約42–45%，但GRENADIER字樣嚴重失真，白色筆畫未完整保留；DJZY608仍可辨讀，四個主要燈圈仍在，細環更粗、分離更差。這是整組原廠設定比較，並非只改噴嘴，尚未實印。玻璃暫用白料。**

GM-R4-01 actual native slicing/settings and GM-R4-02 immutable geometry are covered; GM-R4-03 four actual tools and provisional mapping are covered; GM-R4-04 frozen artifacts, independent path/media comparison and honest thumbnail/physical limits are recorded; GM-R4-05 operations stayed within diagnostic scope. No printer or app mutation, upload/start, dependency change, geometry/artwork edit, source scaling or P3 evidence overwrite was performed.

Next: present the frozen profile comparison through the separate delivery role. At this unchanged scale, the wordmark is a concrete0.4 detail blocker; do not automatically enlarge or thicken it. A subsequent scoped local-detail experiment requires a new contract. User-surface rendering is a separate delivery gate; this validator does not claim phone visibility or print readiness.

## Factual observation correction after actual-surface review

Root's live SVG review identified that the broad wordmark area is blue-gray no-path background, while actual white extrusion is limited to small fragments. A focused read-only XML check confirmed background `#ccd5de` and85 `#FFFFFF` path segments in each0.4 wordmark SVG. The earlier report/message characterization “joined, block-like white shape” / “小字黏連、字內空隙縮小或消失” misidentified background as white extrusion and is explicitly superseded by the corrected observation above. The earlier error is retained here for audit; it was an interpretation error, not changed geometry, Gcode or media. Final input/media fingerprints remain unchanged. No claim is made that a blue-gray region is a through-hole or that lower layers contain no material. The supported verdict remains severe wordmark degradation, specifically incomplete white strokes at the depicted surface layer.
