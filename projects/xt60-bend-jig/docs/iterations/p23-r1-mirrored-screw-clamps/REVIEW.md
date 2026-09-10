# P23 R1 mirrored screw-clamp independent critique

日期：`2026-08-29`
Owner：`P23-CRITIC-01`
Role：independent critic
Status：**BLOCKED / NOT ACCEPTED**

Disposition：P23 R1 可作為 source-level 診斷材料繼續討論，但不能接受為使用者指定 candidate。兩個 written STEP 的 SHA-256 與使用者指定 fingerprint 不符；目前 STEP 只作為「現況診斷證據」。即使忽略 provenance mismatch，P23 module 內仍有實體重疊、未建模的 positive pull-back、以及未被 yoke 正向保留的 follower/shoe capture，不能通過 mechanical topology / user operation critique。

## Verified fingerprint

| Path | Observed SHA-256 | Expected | Result |
|---|---:|---:|---|
| `docs/iterations/p23-r1-mirrored-screw-clamps/BRIEF.md` | `d2aa3a42198e6d51a6a0e6d7b290e3dff47797eccfa418e8db74211dc1362872` | coordination observed | match |
| `docs/iterations/p23-r1-mirrored-screw-clamps/DESIGN.md` | `f78d26ab0ee09727b07b13616d1b3109a26106f8000f83b5d4a439bdbe48249a` | same | match |
| `src/xt60_bend_jig/p23_r1_mirrored_screw_clamps.py` | `9923d4d855a08a0daedc8c5304b1fb965b3ded468b00291f0bcdebf5459ceb72` | same | match |
| `tests/test_p23_r1_mirrored_screw_clamps.py` | `5740aa29723174446b5fca7a11db723fb1ee7f18d2009684c2536c5c1ae3567d` | same | match |
| `cad/p23_r1_mirrored_screw_clamps/p23_r1_open.step.py` | `1911287d5245fead223e6db2f5a6eb40fcb8562df540e71eb4fb041aa2928883` | no user hash; root observed | observed only |
| `cad/p23_r1_mirrored_screw_clamps/p23_r1_clamped.step.py` | `c53d9a8a6adc374757543d5d0da920f04f707551cb3c8a1883c4c5d40998ec2d` | no user hash; root observed | observed only |
| `cad/p23_r1_mirrored_screw_clamps/p23_r1_open.step` | `6273bb1782cce4a145023f52f41cef7c1102892c4b271f9b8ec9067f7fd96e68` | `aaa1b1bc8e1bb285190d1f5db7bd207a6a40669acad0363a24a882a952a25349` | **mismatch** |
| `cad/p23_r1_mirrored_screw_clamps/p23_r1_clamped.step` | `f00a2a0752e50d9672825b03a55e528a6a7f4ea61129d14f9b17fd508fc5eb38` | `39647c5a1b49719098833a629a83c0de4a9638580caeec1a8698a078fbd54bda` | **mismatch** |

## Scope

已讀根目錄 `AGENTS.md`、`docs/CAD_WORKFLOW.md`、CAD skill `SKILL.md` 與 `inspection-and-validation.md`、`snapshot-review.md`、`positioning.md`。專案規則/背景讀取包含 `PROJECT_STATE.md`、`NEXT_AGENT.md`、`docs/REQUIREMENTS.md`、`docs/EXPERIENCE.md`、`docs/decisions/README.md`、`docs/iterations/CURRENT`。設計合約完整讀取 `BRIEF.md` 與 `DESIGN.md`。實質 CAD 檢查限制在 P23 source/tests/entrypoints/current STEP；為核對 inherited rod path/cap/XT60 claims，只讀取 `src/xt60_bend_jig/p20_r4_custom_profile_full_cad.py` 的必要段落。

未產生 snapshot；理由是使用者指定 STEP fingerprint 已 mismatch，目前 written STEP 不能作為指定 candidate 視覺 acceptance。仍執行 source-level 與 current-STEP 診斷。

## Blocking intent errors

1. **BLOCKER-PROV-01：written STEP provenance mismatch。** `p23_r1_open.step` 與 `p23_r1_clamped.step` 均不符合使用者指定 SHA-256。這本身阻擋 candidate acceptance；後續 STEP 結論只能描述現況，不可接受指定 candidate。

2. **BLOCKER-GEOM-01：P23 module 內存在未允許實體重疊，違反 DESIGN preview gate。** `DESIGN.md:81-84` 要求 OPEN/CLAMPED assemblies 無 unintended solid overlap；但 current STEP pairwise 檢查顯示 P23 clamp 自身在 OPEN 有 8 組重疊、CLAMPED 有 10 組重疊。代表值：yoke vs knob `530.060651404 mm3`、screw vs knob `471.238898038 mm3`、orange shoe vs screw `126.808713787 mm3`；CLAMPED 還有 Blue follower vs Orange shoe `0.390453177 mm3`。source 也重現同樣數值，不是 STEP import 假象。相關 source construct：`build_side_module()` 將 yoke、Blue follower、Orange shoe、screw、knob 作為分離 children 輸出（`p23...py:435-450`），但沒有 pairwise allow-list 或 fused/component semantics。

3. **BLOCKER-MECH-01：positive pull-back 只存在於文字與 label，不存在於機構拓撲。** `DESIGN.md:42-44` 指定 Orange shoe 需 anti-rotation guided 並使用 captive mushroom-head screw nose，使反轉螺桿可拉回 OPEN；`DESIGN.md:76-77` 也要求 reverse equal turns pull back。source 實際上用 `_axis_cylinder()` 建立單純 screw cylinder（`p23...py:418-431`），Orange shoe 只加 outboard bridge、thrust arm、thrust pad（`p23...py:346-386`）。沒有 mushroom head、undercut、thread/nut flank、retaining collar、或 screw-to-shoe joint；反而以 `126.808713787 mm3` 重疊碰撞呈現接觸區。這不能證明「不靠 gravity 也能 positive pull-back」。

4. **BLOCKER-CAPTURE-01：Blue follower 與 Orange shoe 的 rod-end capture 不是 module-level axial capture。** Green 是固定 yoke 內的 blind socket；但 Blue/Orange 在固定 yoke 中是 through guide cut：`blue_inner` 與 `orange_inner` 以 `params.yoke_thickness_x + 2.0` 穿切（`p23...py:274-295`），再從 yoke 中扣除（`p23...py:332`）。Blue follower 與 Orange shoe 本身是可分離 cup/body（`p23...py:340-386`），沒有 flange、dovetail、retainer 或端部 stop 讓它們被 yoke 沿 X 留住。因此 rod end 雖進入 blind cup，cup 本身可脫離 yoke，未達 `BRIEF.md:32-33` 所要求「all three rod ends against axial escape；pure end-face pressure insufficient」的正向 module capture。

5. **BLOCKER-ORANGE-01：Orange shoe 的 anti-rotation guide 未依設計落地。** `DESIGN.md:42` 寫 `9.00 x 6.00` anti-rotation shoe；source 卻將 `orange_shoe_width` 當作 `_blind_socket_body()` 的圓柱 outer diameter 使用（`p23...py:346-348`），guide inner width 為 `9.4 mm`、shoe body 為圓形 `Ø9.0 x 6.0`。單一圓形 cup 在 obround slot 中不能提供設計文字宣稱的 anti-rotation；再加上 screw axis 對 Orange center 有 `8.00 mm` 偏置（`p23...py:65-66`, `p23...py:350-377`），操作力會引入扭矩，而目前 CAD 沒有對應的抗扭幾何。

6. **BLOCKER-INHERITED-01：若 P23 宣稱 complete OPEN assembly 無 unintended overlap，繼承 P20 context 已使此 claim 失效。** P23 明確 delegate P20 context（`p23...py:453-466`），P20 source 保留 OPEN bottom/Blue rod 與 XT60 reference（`p20...py:73-82`, `p20...py:437-464`）。full pairwise 診斷在 OPEN 顯示 `fixed_reference_XT60_body` vs `bottom_OD4_rod_L50.00` 為 `186.980487361 mm3`，這與既有 P20 R4 已知 Blue/XT60 blocker 一致。這不是 P23 新增錯誤，但阻擋任何「OPEN/CLAMPED assemblies zero unintended overlap」的完整 claim。

## Physical / manufacturing risks after intent repair

- 兩側獨立螺桿沒有同步機構；`DESIGN.md:73-77` 要求人工 alternate equal indexed turns。即使未來幾何修好，左右不同步仍可能讓 Orange skew、增加 rod/slot binding 與 wobble。
- Printed trapezoidal thread、nut engagement、mushroom capture、sliding shoe clearance、Blue follower clearance都只是名義 CAD；thread strength、磨耗、PETG 層向、扭矩、back-drive holding force 尚未被切片或物理測試。
- 若 follower/shoe 補上真正 retention，需重新檢查裝配順序：OPEN 時如何把兩側 yoke 同時套入六個 rod ends、如何避免預載、以及如何拆卸 completed pigtail。
- 現有 side yoke 可能比六個獨立 caps 更能約束 rod ends，但目前沒有 X 向 cross-link、無抗扭 shoe、無同步；「合理減少 tilt/wobble」只能算未證明，不能 acceptance。

## Requirement coverage

| Requirement | Critic result |
|---|---|
| 1. 左右 mirrored screw-clamp | **Partial.** Source X datums 符合鏡像：left/right yoke center `±24.3`、inner face `±21.3`、socket center `±23.3`、screw axis `±30.3`；但 current STEP mismatch 且 module collision 未解。 |
| 2. 移除所有 caps | **Pass for source/current STEP.** P23 context 不呼叫 P20 `build_cap()`；census 為 `capCount=0`，current STEP 沒有 `permanent_cap` labels。含 `capture` 字樣的 labels 是 P23 sockets，不是舊 caps。 |
| 3. 所有 rod ends axial capture | **Fail.** 六個 blind capture labels 存在，socket end 相對 rod end 有 `0.30 mm` clearance；但 Blue/Orange cups 未被 yoke 正向保留，module-level axial capture 不成立。 |
| 4. 引導 Orange | **Partial / fail.** Orange center path 精確沿 inherited OPEN-to-CLAMPED travel `12.150910844 mm`，`6.075455422` screw turns；但 anti-rotation shoe、screw pull-back 與 collision 都失敗。 |
| 5. 正確處理 Blue motion | **Partial.** Blue center 使用 inherited P20 path，OPEN `(-7.511545,14.127161)` 到 CLAMPED `(2.228078,5.248302)`，source 不是固定 Blue；但 follower retention 不足，CLAMPED 時 Blue follower 與 Orange shoe 重疊 `0.390453177 mm3`。 |
| 6. 不靠 gravity positive pull-back | **Fail.** 沒有實體 captive screw nose / retained joint；source 只輸出相交的 screw、shoe、knob solids。 |
| 7. 減少 tilt/wobble | **Unproven / not accepted.** 兩側 yoke 概念方向有幫助，但目前靠人工等轉、未保留 followers、Orange 抗扭未建模，不能合理聲稱 wobble 已降低到可操作。 |

## Exact command evidence

- `shasum -a 256 ...BRIEF.md ...DESIGN.md ...p23_r1_mirrored_screw_clamps.py ...test_p23...py ...p23_r1_open.step.py ...p23_r1_clamped.step.py ...p23_r1_open.step ...p23_r1_clamped.step`：DESIGN/SOURCE/TEST match；OPEN STEP observed `6273bb...96e68` mismatch expected `aaa1b1...25349`；CLAMPED STEP observed `f00a2a...eb38` mismatch expected `39647c...54bda`。
- `uv run pytest projects/xt60-bend-jig/tests/test_p23_r1_mirrored_screw_clamps.py -q`：`7 passed`。
- `uv run python .../scripts/inspect refs ...p23_r1_open.step --facts --planes --positioning --format text`：faces `837`、edges `2259`、size `[66.6,47.9327,59.7765]`、kind `assembly`。
- `uv run python .../scripts/inspect refs ...p23_r1_clamped.step --facts --planes --positioning --format text`：faces `837`、edges `2259`、size `[66.6,63.6396,64.7193]`、kind `assembly`。
- `uv run python .../scripts/inspect validate ...p23_r1_open.step --skip-self-intersection --format text`：`occurrences: 22`，`PASS - all solids valid, closed, and positive volume`。
- `uv run python .../scripts/inspect validate ...p23_r1_clamped.step --skip-self-intersection --format text`：`occurrences: 22`，`PASS - all solids valid, closed, and positive volume`。
- `uv run python - <<'PY' ... occurrence_census/build_preview ... PY`：OPEN/CLAMPED census 均為 `leafCount=22`、`rodCount=3`、`capCount=0`、`moduleCount=2`、`captureCount=6`；socket X 左 `center=-23.3/end=-25.3/rod_end=-25.0`，右 `center=23.3/end=25.3/rod_end=25.0`；Orange travel `12.150910844186997`，turns `6.075455422093499`。
- `uv run python - <<'PY' ... STEP_P23_PAIRWISE ... PY`：current STEP P23-only pairwise overlap，OPEN `hitCount=8`，CLAMPED `hitCount=10`；最大與代表 overlap 如 blocking findings。
- `uv run python - <<'PY' ... FULL_PAIRWISE ... PY`：OPEN full assembly `hitCount=14`，包含 inherited `fixed_reference_XT60_body` vs `bottom_OD4_rod_L50.00` `186.980487361 mm3`；CLAMPED full assembly `hitCount=15`。
- `grep -nE "CLAMP|arrow|index|mark|mushroom|anti-rotation|thread|helix|Thread|trapezoid" ...`：source 只有 knob label `indexed_knob_12_marks`，沒有實體 arrow/marks、mushroom、thread/helix construct；相關設計文字只在 `DESIGN.md`。
- `git status --short -- P23 paths`：P23 docs/source/tests/cad 目前皆為 untracked；本 critic 只新增本 `REVIEW.md`。

## Unresolved risks and next action

Unresolved：指定 STEP candidate 不可驗收；current STEP 雖 topology valid，但沒有 collision-clean preview；positive pull-back、anti-rotation、follower retention、equal-turn operation、Blue follower binding、manufacturing/thread/torque/holding force均未解。

Next action：先由 implementation/design 修正 provenance，重新凍結 matching source/test/entrypoint/STEP fingerprint；再最小修正 P23 module topology：明確定義 screw/nut/shoe 是否為分離零件或 fused printed assembly、加入真正 captive pull-back interface、加入 follower/shoe axial retention 與 anti-rotation geometry，並在 source/current STEP 上加入 P23-only pairwise collision gate。完成後才重新交給 critic/validator。

---

## Repair-cycle-1 focused re-critique — 2026-08-29

Owner：`P23-CRITIC-01`  
Role：independent critic（同一 bounded critic workstream）  
Status：**PASS — EVIDENCE-ONLY FIRST-DESIGN INTENT PREVIEW**

本節追加於 first critique 之後；上方 `BLOCKED / NOT ACCEPTED`、舊 hashes 與舊 findings 保留為 repair 前歷史，已由本節的 matching repair-cycle-1 candidate 與下列 closure 判定取代。此 PASS 只接受 first-design 的機構意圖、拓撲與操作 preview；不是 mesh、3MF、slicer、print、強度、扭矩、磨耗、容差或 physical acceptance。

### Verified repair-cycle-1 fingerprints

| Frozen item | Observed SHA-256 | Result |
|---|---:|---|
| `src/xt60_bend_jig/p23_r1_mirrored_screw_clamps.py` | `5f92bda26ef931f5a614c02c5b72756b4b39987878f7a1b5db19e49160607a52` | match |
| `tests/test_p23_r1_mirrored_screw_clamps.py` | `22596c141bbf2cf7614b9ae8948c68064613e2c1f5935899cfb43104fb4fb7f3` | match |
| `cad/p23_r1_mirrored_screw_clamps/p23_r1_open.step` | `69c20491b6ee8aac79587c325b418807e9f05afdd2288580da947a1c4a5f7a50` | match |
| `cad/p23_r1_mirrored_screw_clamps/p23_r1_clamped.step` | `a4a3133d4ae2bda76b6f67f3ee11e2d648ee0c6c58e84f065b2f8b1cb0933978` | match |
| `docs/iterations/p23-r1-mirrored-screw-clamps/VALIDATION.md` | `9be75b7f1a2b7358a593b675ac0bd7aaebc486e9dc96ba12a6655e57ad8f582c` | match |

五個 frozen repair-cycle-1 inputs 均在 critic 檢查前 matching；本次沒有 regenerate 或修改 source、tests、STEP、artifact。

### Focused intent topology / operation 判定

| 檢查項目 | Re-critique | 證據與界線 |
|---|---|---|
| 1. 左右 mirrored modules | **PASS** | yoke centers `X=-24.3/+24.3 mm`、screw axes `X=-32.6/+32.6 mm`；兩側同 pitch `2.0 mm`、同 Orange travel `12.150910844187 mm`，OPEN/CLAMPED 皆各有一個 module。 |
| 2. no legacy caps | **PASS** | source preview 不呼叫 inherited `build_cap()`；source census 與兩個 imported STEP 均為 `capCount=0`，沒有 `permanent_cap` occurrence。 |
| 3. 所有 rod-end axial capture | **PASS（geometry-level intent）** | 每側 Green 為固定 blind socket；Blue follower 與 Orange shoe 各有 blind socket 加 X-retention flange，固定 yoke 有 face lips。lip `1.2 mm`、flange `3.2 mm`、cavity `3.6 mm`，每側名義 X clearance `0.2 mm`；兩狀態皆 `captureCount=6`。這已修正上一版「cup 可連 rod 一起軸向脫出」的 module-level topology。 |
| 4. Orange anti-rotation | **PASS（geometry-level intent）** | Orange shoe 現為沿 travel 方向定向的非正方矩形 `9.0 x 6.0 mm` keyed section，而不是上一版 `Ø9` 圓 cup；兩側皆為一個真實 solid，具旋轉方向約束的幾何拓撲。 |
| 5. positive screw pull-back without gravity | **PASS（intent topology only）** | screw 已有實體 captive T-head：head `D6.0 x 2.0 mm`、cavity `D6.5 x 2.5 mm`、neck `D3.0 mm`、slot `D3.5 mm`，head 對 neck slot 的 diametral capture margin `2.5 mm`。反轉時 head 可對 shoe cavity 施加拉回方向接觸，不再是上一版僅靠相交 cylinder/文字 label；不需要 gravity 才能表達 pull-back。實體 thread engagement、back-drive holding force仍不在此 PASS 內。 |
| 6. Blue motion | **PASS（intent path）** | Blue 仍被動委派 inherited P20 authority，center 由 OPEN `(-7.511545005, 14.127161486)` 移到 CLAMPED `(2.228077655, 5.248301944)`；不是被固定或換 rod identity。`u=0,.25,.5,.75,1` 抽樣時 Blue follower 所在 module 對 rods/outer plate 及 module 內部均無 `>1e-7 mm3` 相交。 |
| 7. reduced tilt/wobble plausibility | **PASS AS PLAUSIBLE；未宣稱物理證明** | 兩側鏡像 yoke 同時對 Green 反力、Blue follower 與 keyed Orange shoe 提供 blind-end/X retention，且 sampled travel collision-clean；相較六個獨立 caps，這在拓撲上合理增加兩端共同導引並降低 axial escape/Orange rotation 自由度。左右仍靠人工 equal turns，實際 wobble、flex、binding 與 clearance stack 留待後續。 |
| 8. assembly/service clarity | **PASS FOR INTENT PREVIEW；service-path evidence pending** | `DESIGN.md` 已明列 OPEN 裝配、followers/shoes 對 OPEN marks、兩側 yoke 安裝、alternate equal turns、雙 CLAMPED marks、反轉拉回的操作順序；source labels 清楚區分 fixed yoke、Blue follower、Orange shoe、screw-with-knob。因本 candidate 沒有 exploded/insertion/removal state，face-lip retention 的實際裝入/拆出路徑仍是 later assembly risk，但不足以否決本次 evidence-only intent preview。 |

### Prior blocker closure

| First-critique blocker | Repair-cycle-1 result | Closure |
|---|---|---|
| `BLOCKER-PROV-01` STEP fingerprint mismatch | 兩個 current STEP 與本輪 frozen SHA-256 完全相符；SOURCE、TEST、VALIDATION report 也 match。 | **CLOSED** |
| `BLOCKER-GEOM-01` disconnected yoke / module overlaps / knob penetration / Blue-Orange collision | 左右 fixed yoke 各為 `1` connected solid；source module pairwise 在 `u=0,.25,.5,.75,1` 均為 `0` hits，包含 OPEN/CLAMPED；knob-to-nut clearance 依序 `13.150910844187, 10.113183133140, 7.075455422094, 4.037727711047, 1.000000000000 mm`。兩個 written STEP 各 `20` occurrences 並通過 closed/positive-volume validation。 | **CLOSED** |
| `BLOCKER-MECH-01` positive pull-back 未建模 | Captive T-head、neck、head cavity 與 neck slot 都是實體 geometry；head 大於 neck slot，形成雙向 retained pull-back relation。 | **CLOSED FOR INTENT TOPOLOGY** |
| `BLOCKER-CAPTURE-01` Blue/Orange cup 未被 yoke 沿 X 保留 | fixed-yoke face lips、follower/shoe retention flanges 與 `0.2 mm/side` cavity clearance 已落地；六個 rod ends 都有 blind capture 加 module-level axial retention。 | **CLOSED FOR GEOMETRY-LEVEL INTENT** |
| `BLOCKER-ORANGE-01` 圓 cup 無 anti-rotation | Orange 改為 `9 x 6 mm` rectangular keyed shoe，並保有 X-retention flange/captive-head pocket。 | **CLOSED** |
| `BLOCKER-INHERITED-01` OPEN XT60 vs Blue overlap | 獨立重測仍為 OPEN `186.980487360803 mm3`、CLAMPED `0 mm3`。這不是 P23 repair 修掉的問題；它是 inherited P20 full-assembly/interface issue。 | **NOT CLOSED；明確隔離為 later inherited risk，不阻擋 focused P23 intent preview** |

### Exact command evidence

- `shasum -a 256 <P23 source> <P23 test> <OPEN STEP> <CLAMPED STEP> <VALIDATION.md>`：五項 observed hashes 逐一 match frozen repair-cycle-1 fingerprints。
- `uv run pytest projects/xt60-bend-jig/tests/test_p23_r1_mirrored_screw_clamps.py -q`：`11 passed`，exit `0`。
- `uv run python <cad-skill>/scripts/inspect validate .../p23_r1_open.step --format text`：`20 occurrences`；`PASS - all solids valid, closed, and positive volume`，exit `0`。
- `uv run python <cad-skill>/scripts/inspect validate .../p23_r1_clamped.step --format text`：`20 occurrences`；同樣 PASS，exit `0`。
- `uv run python - <<'PY' ... source/imported-STEP topology probe ... PY`：兩狀態 census 都是 `leaf=20 / rods=3 / caps=0 / modules=2 / captures=6`；左右 yoke、Orange shoe、screw-with-knob 各為一 solid；OPEN/CLAMPED P23 module pairwise `hits=0`；imported STEP 皆 `leaf=20 / caps=0 / captures=6 / valid=True`；另確認 pull-back、retention、Orange key、Blue endpoints 與 inherited overlap 數值。
- `uv run python - <<'PY' ... u=(0,.25,.5,.75,1) motion probe ... PY`：每個 sampled `u`、每一 side 都是 `internal_hits=0`、`rod_or_plate_hits=0`（threshold `1e-7 mm3`）。

本 critic 未生成 snapshot：本輪沒有產生或修改 STEP，且 matching `VALIDATION.md` 已記錄 exact repaired STEP 的 fresh snapshot review；本次獨立 re-critique 以 source、tests、imported written STEP 與 deterministic probes 為判定依據，沒有把 validator 的 visual PASS 當作自身 CAD 證明。

### Evidence-only preview disposition

**ACCEPT / PASS：P23 R1 repair-cycle-1 可前進為 evidence-only first-design intent preview。** 上一輪 P23 provenance、module collision/connectedness、Orange anti-rotation、Blue/Orange X retention 與 captive positive pull-back blockers 已由 matching source/current STEP 實質修好。唯一未修好的舊 finding 是 inherited OPEN XT60/Blue overlap；它必須在 full-system 或 print-readiness claim 前另行處理，但依本輪 focused contract 不否決 P23 mirrored screw-clamp intent preview。

Later risks：實際 printed male/female thread 與 nut engagement、左右人工 equal-turn 同步、扭矩與 back-drive holding、clearance stack、flex/wear、Blue binding、wobble、rod retention、以及 flange/lip 的實際裝入、拆卸與 completed-pigtail service path。這些均未被本次接受，也不應被描述為已製造或物理證明。

---

## P23-REVIEW-01 formal final review — 2026-08-29

Owner：`P23-REVIEW-01`  
Role：formal reviewer  
Final disposition：**PASS / ACCEPT — 僅限 evidence-only first-design intent preview**

本 formal review 接受 P23 R1 repair-cycle-1 作為第一版 mirrored screw-clamp 的
機構意圖、拓撲與 OPEN／CLAMPED 視覺預覽。它不接受、也不授權 mesh、3MF、
slicing、printing、thread fit、強度、扭矩、保持力、耐久、製造可行性或實體操作
驗收。

### Frozen candidate fingerprint verification

Formal review 前逐項重新計算 SHA-256；六項均與 frozen candidate 完全一致：

| Frozen item | Observed SHA-256 | Result |
|---|---:|---|
| `src/xt60_bend_jig/p23_r1_mirrored_screw_clamps.py` | `5f92bda26ef931f5a614c02c5b72756b4b39987878f7a1b5db19e49160607a52` | match |
| `tests/test_p23_r1_mirrored_screw_clamps.py` | `22596c141bbf2cf7614b9ae8948c68064613e2c1f5935899cfb43104fb4fb7f3` | match |
| `cad/p23_r1_mirrored_screw_clamps/p23_r1_open.step` | `69c20491b6ee8aac79587c325b418807e9f05afdd2288580da947a1c4a5f7a50` | match |
| `cad/p23_r1_mirrored_screw_clamps/p23_r1_clamped.step` | `a4a3133d4ae2bda76b6f67f3ee11e2d648ee0c6c58e84f065b2f8b1cb0933978` | match |
| `docs/iterations/p23-r1-mirrored-screw-clamps/VALIDATION.md` | `9be75b7f1a2b7358a593b675ac0bd7aaebc486e9dc96ba12a6655e57ad8f582c` | match |
| 本文件的 pre-formal-review critic state | `3e7a6168cff03499266fdd3210dedf40d02c298ecc03a384c3d135294c85d91d` | match |

另外重新執行 focused test：

```text
uv run pytest projects/xt60-bend-jig/tests/test_p23_r1_mirrored_screw_clamps.py -q
11 passed; exit 0
```

未重新產生或修改 STEP。Formal review 讀取 current source、tests、兩個 explicit
entrypoints、完整 critic history 與 validator history，並確認 implementation、
repair、critic 與 deterministic validation 指向同一組 source/test/STEP fingerprints。

### Snapshot provenance correction and visual review

`VALIDATION.md` 的 repair-cycle-1 snapshot subsection 重用了 repair 前的 stale
snapshot bytes，因此該 subsection 的四張圖及其 visual claim 在此明確標記為
**superseded，不納入 formal acceptance evidence**。

Root 已針對 exact repaired STEP hashes 強制重建 imported-STEP artifacts；force
結果指向 OPEN `69c204...f7a50`、CLAMPED `a4a313...933978`，且兩者皆為
`meshCount=20`。Formal reviewer 重新核對下列檔案 hashes，並以 original detail
直接檢視：

| State | Corrected final snapshot | SHA-256 | Result |
|---|---|---:|---|
| OPEN | `/private/tmp/p23-r1-final-snapshots/open_iso_20260829T161022Z.png` | `3d219b72d85817f69565c4db8f15932acfa2d9b9f37566f6b69e04a436edf6a4` | verified and reviewed |
| CLAMPED | `/private/tmp/p23-r1-final-snapshots/clamped_iso_20260829T161024Z.png` | `6e1692953b9bda8d3825d250faf52d0652dbfd84c8564513a326d16b522a0e0d` | verified and reviewed |

Corrected visual evidence 顯示兩側 mirrored clamp modules、兩組 screw/knob、
retained Blue/Orange/Green rod-end context，以及 OPEN 到 CLAMPED 的預期位置改變；
未再看到先前明顯的 knob/yoke 穿透、Blue/Orange endpoint collision、floating P23
part 或新的左右不對稱。隱藏接觸、clearance 與 connectedness 的正式依據仍是
matching source/tests/STEP 的 deterministic checks，不以 snapshot 單獨證明。

因此 provenance chain 的判定是：**deterministic chain 原本已 matching；visual
chain 經本 formal-review snapshot correction annex 後 matching。** 舊 snapshot
section 不是此 PASS 的證據。

### Accepted intent scope

- 三支 purchased rods 維持 `OD4.00 x 50.00 mm`，沒有改桿長或 inherited YZ paths。
- 六個舊 caps 已移除；左右各一個 mirrored side clamp module。
- 每側 Green fixed capture、Blue retained follower、Orange rectangular keyed shoe
  與 captive T-head screw pull-back 已達 geometry-level intent。
- OPEN／CLAMPED 兩個 endpoint 的 P23 module topology、connectedness、axial
  retention intent、Orange anti-rotation intent 與 P23-only collision regression
  可接受為 first-design preview。
- Equal `2.00 mm` nominal pitch 與 `12.150910844187 mm` Orange travel 是設計／
  pure-math intent；目前 smooth preview screw 並不是可列印 thread geometry 證明。

### Explicitly unresolved blockers for later stages

1. **Inherited full-system blocker：** OPEN 的 XT60 reference 與 Blue rod overlap
   `186.980487360803 mm^3`；CLAMPED 為 `0 mm^3`。它不是 P23 clamp module 新增
   問題，所以不否決本次 focused intent preview，但在 full-system acceptance、
   print preparation 或 physical test candidate 前必須另案處理並重新驗證。
2. **Manufacturing blocker：** male/female trapezoidal thread、nut engagement、
   printer-specific clearances、layer orientation、support／bridging、strength、wear
   與 heat 尚未建模或驗證；目前不得輸出 print-authority 3MF/STL。
3. **Operation blocker：** 左右螺桿仍靠使用者 alternate equal turns；不同步造成的
   Orange tilt、rod/rail binding 與 wobble 尚未由同步機構或 physical test 排除。
4. **Holding/release blocker：** back-drive holding force、操作 torque、是否能穩定
   保持 LOCKED、以及反轉後是否真的不靠重力順暢回 OPEN，尚未經實體測試。
5. **Assembly/service blocker：** face-lip/flange 的實際裝入、拆卸、預載、rod-end
   retention、completed-pigtail service path 與 XT60 線材 clearance 尚未驗證。

### Formal receipt

- Disposition：`PASS / ACCEPT`，只限 evidence-only first-design intent preview。
- Frozen fingerprint verification：`6/6 match`。
- Focused test rerun：`11 passed`，exit `0`。
- Corrected snapshot verification：`2/2 hashes match`，兩張皆以 original detail
  檢視；stale validator snapshots 已明確 superseded。
- Source/tests/STEP/CAD entrypoints：未修改、未重新生成。
- 唯一 formal-review write：本節追加至 `REVIEW.md`。
- 下一個合法 gate：先由使用者確認此 first-design operation/shape intent；若接受，
  再另開 bounded iteration 處理 inherited XT60/Blue overlap、thread/clearance、
  synchronization 與 assembly/service，而不是直接切片或列印。
