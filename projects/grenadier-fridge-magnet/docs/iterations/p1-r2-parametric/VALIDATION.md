# Validation
P2-D ran node projects/grenadier-fridge-magnet/scripts/face-candidate-manifest.mjs: exit0, verified10 entries, accepted fingerprint f893d8fbf98750be9e7366a5cfd8c78c90e58a0d4d0c73d5c2480ba471b7e652. Viewed accepted D4 and new BMW photo via view_image. No CAD/mesh/slicer tests run by design.

Planned focused gates (not results):
1. Math/domain: XY transform roundtrip and2x area/length laws; XY scaling leaves Z unchanged; reject nonpositive scale/depth or invalid height order.
2. Partition/collision: exact color+semantic coverage of accepted foreground, zero positive-area mask overlap; actual generated closed meshes have consistent winding/positive volume and no positive-volume overlap other than explicitly fused same-material parts.
3. Constraint/parity: actual written bounds/heights equal parameters; back union continuous; every face component's bottom meets back; top-view exact source color projection. Flat coplanarity, relief order and plate local flushness tested on actual geometry.
4. Requirement/visual: both variants, all five visible classes mapped to four real intents, four lamps, both texts, paleglass/white border. Compare snapshot front + oblique; no holes. No motion test (static). Slicing and physical acceptance explicitly pending.

