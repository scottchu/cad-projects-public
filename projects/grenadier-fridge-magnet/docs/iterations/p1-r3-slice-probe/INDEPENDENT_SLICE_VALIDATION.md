# P3-V independent diagnostic slice validation

Owner `/root/slice_artifact_validator`, separate from preparation and recovery implementers. Scope: unchanged development meshes, diagnostic packaging and later actual toolpath evidence. No fabrication or physical approval.

## Phase 1 — packaging parity PASS

Validator input fingerprint `6f6797238847e77fcecac99ceb31848b7a3e011959c217bf198700446874203d`; frozen sorted SHA-256 path/content list: `slicer/p1-r3-validation/package-input-manifest.json`. Exact evidence: `slicer/p1-r3-validation/package-validation.json`. Parent color-corrected candidate's 18 entries reverified.

Command, from repository root:

```sh
uv run python projects/grenadier-fridge-magnet/scripts/validate_slice_probe_package.py
```

Exit 0. The independent reader decodes the source GLB binary accessors and 3MF XML directly; it does not call the packaging implementation or repair mesh coordinates. Both packages retain exact vertex counts, indexed triangles and part names. Float decimal serialization error is below 0.00000005 mm. All indexed mesh edges have incidence two; this is indexed closure only and does **not** prove coordinate-welded manifoldness or resolve known point-pinched STL contacts.

| Variant | GLB SHA-256 | 3MF SHA-256 | Parts | Triangles | Written assembly bounds mm |
|---|---|---|---:|---:|---|
| flat | `bb0b2d54dba75530fbcce067229393cea5534d065251a18a5c6c7c60b8c34e77` | `ed08511411e7f0f704002794505bf20ef0b883752667413c595f147675295eaf` | 6 | 286268 | [72.4000015,84.2999992,0]–[197.4000015,186.0999985,2] |
| relief | `143d67d0365a8b7fd9fc7e2425ee925cf59b24527607b98e8f768880b3966638` | `ebc3caadaff4f41c513a3e4b12e6f328730021358deee32067c55cae5577d774` | 14 | 303536 | [72.4000015,84.2999992,0]–[197.4000015,186.0999985,2.4000001] |

Exactly one build object per package references every child once, without child transforms. The only placement is the whole-assembly translation [135,136,0] mm. This preserves back-down Z=0 and the working 125 ×101.8 mm footprint within the 270 mm native bed; no final size is selected.

Part metadata maps black/backing→T0, gray→T1, white→T2, deep-blue→T3. Every glass-mix part also maps provisionally to T2 white; no fifth tool. `glass-mix-high` occupies the plate lettering area as well as the better-known glass regions, so the diagnostic map also makes pale-blue/antialias plate subregions white. Exact input geometry preservation does not establish original plate color fidelity or legibility.

GM-R3-02 packaging preservation passes; GM-R3-03 metadata and four-tool intent pass only for the declared provisional mapping. GM-R3-01 actual slicing, actual tool use and GM-R3-04 output detail survival await frozen successful Gcode. GM-R3-05 remains diagnostic/non-release. No printer contacted or commanded; physical claims remain pending.

## Phase 2 — pending frozen toolpaths

Two preparation CLI exits 139 before toolpaths were reported to this role. These are slicer invocation failures, not evidence that the artwork is unprintable. A separate recovery owner is resolving preset normalization. Once the root freezes successful outputs, independently parse actual extrusion paths and inspect plate, GRENADIER wordmark, all four lamp rings and localized thin detail; emit directly derived SVG review media with real line widths and tool colors. Do not treat slicer exit 0 as detail survival or physical acceptance.

## Phase 2 — complete diagnostic toolpaths; limited feature-survival PASS

The preceding pending state is superseded by frozen actual toolpaths. Independent validator fingerprint `b605c99ed5ce11538a0643ff4ef2fd4353f1d12858936f57fdc322fc3cba54d1`, declared in `slicer/p1-r3-validation/toolpath-input-manifest.json`. Exact numeric output: `slicer/p1-r3-validation/toolpath-validation.json`. This manifest freezes both Gcodes, recovery settings and input manifests, relief archive, packaging manifest and independent parser. No slicing or model change was performed by this validator.

```sh
uv run python projects/grenadier-fridge-magnet/scripts/validate_slice_probe_toolpaths.py
```

Exit 0. The parser honors G90/G91, M82/M83, G92 and actual positive extrusion with XY displacement, excludes prime tower/custom paths from object-layer review, checks four actual tools, monotonic distinct layer markers, and the complete executable-block end. No extrusion arcs were present. It is a static Gcode reader, not a simulator for native machine/firmware macros.

| Frozen output | Independent findings |
|---|---|
| `slicer/p1-r3-recovery/flat-run1/plate_1.gcode`, SHA-256 `8c25bf304f425ca763839839a030a88856afe7aeea336a925a18b27c7c286259` | Complete executable block; 25 layers, Z0.10–2.02 mm; T0/T1/T2/T3 all extrude; 30 actual tool changes. Native estimate 6h52m1s, 18.37 g. Child exit243 was a subsequent absolute export-path failure, not missing Gcode. No flat sliced 3MF delivered. |
| `slicer/p1-r3-recovery/relief-run1/plate_1.gcode`, SHA-256 `dc41c358a0ca015ddc2fae5aa9676e9cdacd13b7dc62a5029aa6db3d20ae54d5` | Complete executable block; 30 layers, Z0.10–2.42 mm; four actual tools; 45 actual tool changes. Native estimate 7h12m22s, 19.62 g. Preparation child exit0. |
| `slicer/p1-r3-recovery/relief-run1/relief-sliced.3mf`, SHA-256 `8e1a4d401631ea0853d559c5474aa8dcfb3d0a02481ffd8222b4482c602e6c57` | Embedded `Metadata/plate_1.gcode` is SHA-256 identical to frozen relief Gcode. No PNG/JPG thumbnails in archive; native preview-thumbnail failure remains. |

Both object extrusion centerline bounds are X72.71–197.19, Y84.61–185.99 mm; these are toolpaths, not the source silhouette bounds or bead-envelope bounds. The native Gcode sets print nozzle temperatures 220°C and bed 65°C, alongside native preheat/cleaning/standby temperatures. No printer was contacted. Time and material totals are slicer estimates, not measured consumption or print duration.

### Feature observations from actual path media

Review-media fingerprint `34a72e4f776b66a48075b2192ead6b9a96a042c774fe31a8db1373244db34c51`, manifest `slicer/p1-r3-validation/review-media-manifest.json`, freezes 16 SVGs. Each SVG draws actual positive-extrusion segments at their declared `;WIDTH`, with one Y inversion to match the source artwork and colors T0 black/T1 gray/T2 white/T3 blue. PNGs with matching basenames are temporary inspection copies, rounded to display pixels, and should not be committed as release artifacts. Blue-gray background means no depicted path at that selected layer, not necessarily a through-hole. Relief whole-layer views are separate Z1.62/2.02/2.42 planes, never a final-surface composite.

The validator directly inspected flat whole face, both plate and wordmark crops, and all eight lamp crops. Results:

- **Informational, main feature presence:** `DJZY 608` remains readable in both plate crops; `GRENADIER` remains readable in both wordmark crops. Flat final-layer plate has 857 T3 blue segments; relief high final-layer plate has 867. These equal all blue segments in the corresponding whole selected layer, confirming that blue extrusion at those heights remains in the plate ROI. White and black plate/background paths remain present. No fifth tool appears.
- **Informational, lamp presence:** all four main rings and their distinct internal motifs remain recognizable in both variants. Every lamp crop contains actual black, gray and white extrusion at the appropriate surface layer. This is observed toolpath presence, not a proof of roundness or physical bead quality.
- **Medium, fine-detail limitation:** the central two lamps' fine gray outer trim has visibly fragmented path coverage; both plate crops show small white/gray gaps within blue strokes and irregular edges. Wordmark main letters survive but small edge voids remain visible. No exact whole-source pixel-loss metric was performed, so do not quantify deleted artwork or assign every visible gap to slicer loss.
- **Medium, thin-line process risk:** declared surface-path widths reach approximately 0.0943 mm in the principal feature crops, despite a nominal 0.2 mm nozzle. Relief intermediate planes include approximately 0.0443 mm lines. Slicer emission of these widths is not proof that the material can reproduce them cleanly. A targeted physical detail coupon is the smallest next evidence step; none is created or authorized here.
- **Open intent/process boundary:** all glass-mix geometry, including pale-blue antialias plate subregions, is provisionally white. There is no accepted blue/white mixing recipe or original-color-fidelity claim.
- **Open structural boundary:** known source point-pinches and thin backing connectors were preserved. This bounded validation did not establish first-layer deposited-bead connectivity, strength, adhesion, or magnet attachment. Do not promote indexed mesh closure or complete Gcode to those claims.

### Verdict and requirement coverage

**Both unchanged development variants have real diagnostic toolpaths, with the two required text features and all four main lamp motifs visibly present. Clean fine-detail acceptance and print release remain pending.** GM-R3-01 is covered for real slicing at the unchanged development scale; GM-R3-02 by exact packaging parity; GM-R3-03 by four-tool metadata plus actual extrusion and the explicit provisional-white limitation; GM-R3-04 by frozen outputs, independent parser, native warnings/exit boundaries, and actual path media; GM-R3-05 by the non-release boundary. No STEP/BREP or physical acceptance is claimed.

Actual user-surface media delivery is a separate role's gate. This validator's image inspection alone does not establish that the user can load or read the review page. Root should collect that delivery receipt, then present the limited slicing result and leave final width deferred. The next smallest material experiment is a scoped detail coupon for plate/wordmark/central lamp trim after user intent, material and printer authorization; no automatic scale change or artwork thickening is justified by this probe alone.
