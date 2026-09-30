# D5 validation evidence

## Environment

D5 owner `/root/magnet_design`, design role, not independent validator. Branch `codex/grenadier-fridge-magnet`; baseline `a8834040afe401637d36e94bd8fdd9e1d9874d35`. No Python run; root .venv absent per root receipt. Shell/node only; no dependencies or root lock modifications by D5.

Candidate fingerprint: `8a5aad12d7041a5c2f269dd589dd0c51d1dcd142d8e24df17f7988eeb0650bb0`, manifest `intent-manifest.json`. This is face-only intake, not generated geometry. Independent validator provenance pending.

## Commands and results

Executed from repo root:

```sh
shasum -a 256 AGENTS.md docs/CAD_WORKFLOW.md docs/PROJECT_CONTINUITY.md docs/FDM_DESIGN_RULES.md
node projects/grenadier-fridge-magnet/scripts/intent-manifest.mjs --write
node projects/grenadier-fridge-magnet/scripts/intent-manifest.mjs
shasum -a 256 projects/grenadier-fridge-magnet/references/d4-approved.png projects/grenadier-fridge-magnet/references/photo-6-original.jpg
```

Policy hashes exactly matched task intake. Manifest generated and verified 13 declared entries, same fingerprint above. D4 copied hash `44d20b6b2050d639c44ef00d6396b4150f9ed7280b3d1db4c361be8f31b22171`; Photo6 `addbd1cf72c604ed3b1fcda40ede9e6cf3319fe99c925eaace0f7296c2fce3e4`, both match originals supplied by root. `view_image` inspected both original files; four D4 lamps and two text groups visible. No stroke estimation, vector comparison, UI render, CAD checks, pytest, slicing or physical tests ran.

## Requirement coverage

GM-02 source-byte preservation verified; its vector fidelity remains pending. GM-05 latest scope captured in frozen requirements/contract; no actual hole/section UI or geometry created. GM-03/04 physical process unresolved. GM-08 named categories are design targets, not passing vector tests.

## R1 research receipt (root-supplied, not independently rerun by D5)

`/root/glass_process_research`: official [V2.3.6 release](https://github.com/Snapmaker/OrcaSlicer/releases/tag/V2.3.6) and [Full Spectrum introduction](https://www.snapmaker.com/blog/getting-started-with-full-spectrum-slicing/) describe layer-mixed colors; preset / screen estimates do not prove exact pale blue on this flat face. Filament opacity, layer order and material matter. A local color coupon may be useful after2D source exists; no coupon dimensions or print strategy is frozen or authorized in this stage.

## Acceptance boundary

D4 artwork accepted by user per intake. D5 contract hash verified by designer only. D7 vector candidate absent. CAD/source absent; written artifact/slicer absent; physical unverified. No claim on user delivery-surface visibility yet. Scope changed once during D5; prior thickness/diameter draft was never shown as a review surface and is superseded by latest face-only contract.

## D7 implementation evidence

D7 owner `/root/face_vector_implementation` verified D5 fingerprint `8a5aad12d7041a5c2f269dd589dd0c51d1dcd142d8e24df17f7988eeb0650bb0` before writes. Root then ran `uv sync --all-packages --all-groups` with exit 0 and reported CPython 3.12.13, Pillow 11.3.0 and NumPy 2.5.2; root alone updated `uv.lock`/the root environment.

```sh
uv run python projects/grenadier-fridge-magnet/scripts/generate-face-vector.py --input projects/grenadier-fridge-magnet/references/d4-approved.png --output projects/grenadier-fridge-magnet/SVG/p1-r1/face.svg --report projects/grenadier-fridge-magnet/SVG/p1-r1/face-report.json
uv run python projects/grenadier-fridge-magnet/tests/test_face_vector.py
node projects/grenadier-fridge-magnet/scripts/create-face-review.mjs
node projects/grenadier-fridge-magnet/scripts/face-candidate-manifest.mjs --write
node projects/grenadier-fridge-magnet/scripts/face-candidate-manifest.mjs
```

The focused test suite passed four tests: exclusive masks/background boundary, required visible-class/region presence, deterministic regeneration/source preservation, and closed contour preservation for diagonal-only contacts plus an inner hole. D4 remained SHA-256 `44d20b6b2050d639c44ef00d6396b4150f9ed7280b3d1db4c361be8f31b22171`. This is implementer self-check evidence; independent visual/structural validation and user comparison remain pending. There is no CAD, mesh, slicer, print, or physical acceptance claim.

After the C1 repair-1 pass, D7 changed only `create-face-review.mjs` and regenerated the self-contained review page: its two initial panes are fixed at 60vh and fit the complete car; the zoom button deliberately enables a scrollable 150% vector close-up. It did not change the SVG (`732ccba53f271c90c82c9fe86fc2acb133952fc1f3f2ba5b4efdb8dea6803208`) or classifier (`1bdd8a629a3b82bd1e1de6eb1e53b4861f558673d1b986446f0f2b4ca0921dc8`). Candidate manifest verification returned `ec333506f2e6bb27634f9a5f872b57918ad197a6f07e964c80ae935af15bd811`; the HTML hash is `f3657eb6519554a47cd52ddf6620a83f7c1ebd491a9b023128dceff4d78bc799`. Root's live review endpoint is `http://127.0.0.1:54327/review/p1-r1/face-review.html`; root still must verify this delivery surface after the CSS update.

V1 found an actual written-SVG topology defect in that candidate: 13 closed subpaths repeated a self-touching vertex (2 black, 7 gray, 4 white). Its scanline five-class coverage was exact and non-overlapping, but the subpaths were not import-safe. D7 repair 2 changes only contour stitching: `split_self_touching` decomposes every repeated-vertex grid walk into simple closed cycles while retaining all directed boundary segments and even-odd fill. The focused suite now passes seven tests, including a repeated-vertex connected-walk regression and an actual D4 simple-loop assertion. New candidate `f893d8fbf98750be9e7366a5cfd8c78c90e58a0d4d0c73d5c2480ba471b7e652` has SVG `addd63edc72070d1311be76bda1a0d75ce60a192d7ec97e1171659c7c5efc221`, classifier `83d8fc871fee33972e9e4c55f13ecbd68772f1fd78a3c283401344e1d4654580`, and unchanged D4 source hash. V1 revalidation is required; no acceptance follows from this implementation test.

## V1 final independent validation pass

V1 `/root/face_vector_validation` verified the current candidate manifest and ran `uv run python projects/grenadier-fridge-magnet/tests/test_face_vector.py`: 7/7 passed in 4.148 seconds. Its independent SVG scanline plus Shapely inspection found all 6,312 contours closed, axis-aligned, and simple; the previous 13 self-touching loops are resolved. It confirmed exact five-class coverage, no overlap, and byte-identical masks versus the classifier: black 473,660; gray 291,556; white 154,325; deep-blue 5,587; glass-mix 86,354 pixels; foreground 1,011,482 and background 561,034. The embedded SVG and D4 in the portable HTML exactly match their candidate bytes, and the page contains no hole or size controls.

Root separately verified the 11 unchanged parent-intent entries, including frozen requirements/BRIEF/DESIGN, against D5 hashes; superseded `pyproject.toml` and `tests/README.md` were intentionally excluded because the current candidate manifest governs them. Root also confirmed the whole-car browser overview. The live link `http://127.0.0.1:54327/review/p1-r1/face-review.html` is ephemeral to root Node HTTP session 65660; the durable fallback is `review/p1-r1/face-review.html`. R1's physical Full Spectrum pale-glass result remains unknown and deferred. This passes structural/source validation only; print, CAD, exact color, and physical acceptance remain unclaimed.

## U6 user face acceptance — 2026-09-06

After the final Tailscale comparison page was delivered, the user replied exactly 「通過」. This accepts the 2D face-fidelity gate for candidate `f893d8fbf98750be9e7366a5cfd8c78c90e58a0d4d0c73d5c2480ba471b7e652` and supplies sufficient user confirmation that this review was usable; no particular phone or other device is inferred. The accepted content is the separated car face compared with D4, including silhouette, lamps, plate and pale-glass appearance. This is user intent/appearance evidence, not physical color evidence.

A1 owner `/root/record_face_acceptance` reran `node projects/grenadier-fridge-magnet/scripts/face-candidate-manifest.mjs`: exit 0, status verified, 10 entries, matching fingerprint above. Candidate bytes and frozen requirements/contracts are unchanged. Historical pending statements above describe their earlier stages and are superseded by this acceptance entry. CAD, written 3D/slicer and physical acceptance remain absent; actual blue/white glass mixing remains unvalidated. No dimensions, magnet holes, print orientation or CAD generation are authorized by this face-only pass.

Next unconfirmed relationship: 彩色正面各色齊平，還是有高低浮雕。Black backing remains the existing intent and need not be reconfirmed. Explain only this face relationship; do not assign dimensions or generate CAD.

## S2 user relative-height acceptance — 2026-09-06

使用者對兩版及浮雕相對高度說明回覆 exactly「Okay」。已接受的關係：玻璃／水箱護罩較低、車身居中、車燈／保險桿較高；車牌藍字與白底局部齊平。同一已接受美術保留平整版與浮雕版，色區與高度分區獨立。此記錄接受 S1 的相對層級意圖，取代其歷史 pending gate 狀態；不更動已凍結 SURFACE_VARIANTS.md 或 surface-variants-input-manifest.json。

沒有指定任何數值高度、總厚或車牌整體高度；未接受 CAD、實體混色、可列印性或物理成品。下一步僅詢問整體寬度（包含白邊），兩版使用同一寬度；沒有代選預設值。不詢問或實作孔、nozzle、厚度、CAD 或製程。

S2 owner /root/surface_variants_intent；acceptance recorder only。Verified accepted face via exact command node projects/grenadier-fridge-magnet/scripts/face-candidate-manifest.mjs → exit 0, verified 10 entries, f893d8fbf98750be9e7366a5cfd8c78c90e58a0d4d0c73d5c2480ba471b7e652. S1 input fingerprint remains ec049959fa60a65325e73a0f744837a6dfc7424cd958d4d7d9a9268e19ac764a. Docs-only status/evidence updates; candidate/source/artifacts/immutable proposal/manifests unchanged. No further tests.
