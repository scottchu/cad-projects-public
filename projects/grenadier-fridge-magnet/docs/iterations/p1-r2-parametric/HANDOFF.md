# P1 R2 final handoff

Current candidate: `color-corrected-candidate-manifest.json`, 18 verified entries, fingerprint `1f66199dfbd9b35780aee9cb93af0179277805085e9ac1bc61bbf2c9999b2fc0`. Current source is `src/parametric_magnet.py`; review artifacts are `GLB/p1-r2-color-corrected/{flat,relief}.glb`. `FORMAL_REVIEW.md` records the final P2-R join and approval for development preview.

Evidence chain: P2-V2 passes connected geometry after the permitted backing-only 176-cell repair; P2-V3 proves unchanged geometry and exact color encoding in the final GLBs; P2-C3 passes fresh flat/relief color and visual review. Root's final Chrome reload also loaded both variants without a visible error. The failed 179-component candidate and cyan-rendering connected candidate remain historical evidence.

Live review is `https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-model`. It proxies `127.0.0.1:60896`; PID 57483 is recorded in `/tmp/grenadier-model-server.pid`, has no autostart, and will not survive reboot. See `PREVIEW_DELIVERY.md` before touching service state.

Accepted now: editable source and both GLBs as a development-mesh preview, plus Mac-browser rendering evidence. Pending: user-device inspection, STEP/BREP, slicer-ready STL/3MF, actual slicing, final size, local logo/text survival, thin/pinched contacts, glass mixing, magnet retention/strength, and all physical print evidence. Next action is user comparison of both drafts; later slice first and choose scale from real toolpaths. No final width is selected.
