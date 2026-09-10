# P25-REVIEW-01 formal independent review

日期：`2026-09-05`  
角色：`P25-REVIEW-01`（formal independent reviewer；未參與設計、實作、Repair 1／2、critique 或 validation）  
唯一候選 commit：`a1932fb19ffeb6d584153d1c201ebe24b2e06d6a`  
候選 manifest file SHA-256：`88fdcd25585c35277d66a769b5c35208f8e5b8c7534d93efdbcb57493638a845`  
判定範圍：**只限 user-facing first-CAD preview；不是 print candidate 或 physical acceptance**

## Formal decision

**ACCEPT — frozen `a1932fb` 可作為 P25 R1 user-facing first-CAD preview。**

Critic 與 validator 均指向同一個 frozen Repair 2 candidate，且最後一個幾何 blocker 已關閉：未按 release tab 時，front bar 的開啟路徑會被 positive retention barrier 阻擋；receiver 沿指定方向移動 `1.50 mm` 後，front bar 才能無碰撞旋開。候選同時保留使用者確認的三指受力拓撲、左右兩個鏡像模組、既有 `OD4 x 50 mm` 金屬桿與 P20 rod paths。

本 ACCEPT 僅表示「值得讓使用者在 Viewer 中檢查概念、零件關係與操作順序」。它不表示夾具已可列印、可以保持實際負載，或會在解扣後自動彈開。

## Frozen authority and provenance join

Reviewer 在 repository root 進行只讀核對：

- `git rev-parse HEAD`：`a1932fb19ffeb6d584153d1c201ebe24b2e06d6a`。
- `git show -s a1932fb`：commit subject 為 `Add positive P25 latch retention path`。
- `shasum -a 256 CANDIDATE_MANIFEST.sha256`：精確為 `88fdcd25585c35277d66a769b5c35208f8e5b8c7534d93efdbcb57493638a845`。
- `shasum -a 256 -c CANDIDATE_MANIFEST.sha256`：`13/13 OK`。
- `git diff --name-status a1932fb -- <13 candidate paths>`：無輸出；目前 working candidate bytes 與 frozen commit／manifest 一致。
- `shasum -a 256 -c DESIGN_INPUT_MANIFEST.sha256`：`16/16 OK`。
- `CRITIQUE.md` 與 `VALIDATION.md` 都明確指定 `a1932fb...` 及同一 manifest SHA；舊 `7354f85`、`7287e69` 與 Repair 1 結論未混入本 join。
- `IMPLEMENTATION.md` 的 final Repair 2 source、tests、四個 STEP 與 candidate manifest 位於 `a1932fb`；該 receipt 的初版／Repair 1 數據只保留為歷史，不作 final acceptance authority。

工作樹中的 Repair 2／validation PNG、`CRITIQUE.md` 與 `VALIDATION.md` 不在 13-file candidate manifest。它們只作獨立 evidence receipts／review media，不被誤當成 frozen CAD source authority。

## Acceptance-gate disposition

| First-CAD gate | Joined disposition |
|---|---|
| 使用者三指動作：拇指把 Orange 往下推；食指＋中指把 Blue、Green 從後往前推；三桿皆手動 | **PASS**。Clamp state 不改 rod centers，只在既有 `u=1` END state 接手。 |
| Rear member 同時承托 Blue＋Green | **PASS**。左右 rear-yoke/Blue、rear-yoke/Green 皆為零距離、零正體積穿透。 |
| Front bar／pad 只作用 Orange | **PASS**。左右 front-bar/Orange 為零距離、零穿透；對 Blue、Green 有正間隙。 |
| 兩個左右鏡像 module | **PASS**。對應幾何 X 鏡像最大差 `7.1054e-15 mm`，YZ bounds 相同。 |
| 金屬桿維持 `OD4.00 x 50.00 mm` | **PASS**。端點仍為 `X=+/-25.00 mm`；module 停在 `|X|=24.50 mm`，保留 `0.50 mm` tip margin。 |
| 零 cap、零 screw cassette／pressure plate／floating shoe | **PASS**。Occurrence 與 labels 均符合。 |
| 不修改 P20 rail／rod path | **PASS**。Blue／Orange／Green 在 `u=0,0.25,0.5,0.75,1` 的 delegation 最大差為 `0 mm`。 |
| Locked neutral latch 有 positive retention | **PASS for rigid geometry**。`1–5 deg` 均遇 positive-volume barrier；dense sweep 約在 `0.9 deg` 開始阻擋；實測 tooth projection `1.20 mm`。 |
| 按下 `1.50 mm` 後才可釋放 | **PASS for rigid geometry**。Actuated `0/1/2/3/4/5/10/30/60 deg` 全部零正體積碰撞；`5 deg` gap `0.737800 mm`。 |
| Released state 離開 Orange | **PASS for modeled pose**。`60 deg` 時 pad/Orange clearance `15.032383 mm`，latch gap `23.735288 mm`。 |
| Written STEP validity and parity | **PASS**。三個 assembled STEP 均為 source/export `21/21` solids，exploded 為 `8/8`；valid、closed、positive-volume；bounds 最大差 `3.0625e-12 mm`。 |
| User-facing Viewer available | **PASS for live service/artifact readiness，有限定**。詳見下一節；Repair 2 browser canvas 尚未重新做 browser-level visual confirmation。 |

## Viewer and review media

目前 live Tailscale Viewer：

<https://mac-mini.duckbill-ionian.ts.net:8452/?file=projects%2Fxt60-bend-jig%2Fcad%2Fp25_r1_rear_loop_front_pusher_clamp%2Fp25_r1_latched_end.step>

Reviewer 的即時只讀核對結果：

- `tailscale serve status` 顯示 `:8452`（tailnet only）proxy 至 `127.0.0.1:3252`。
- 上述 exact Viewer URL：HTTP `200`、`text/html`。
- `GET /__cad/server`：HTTP `200`，回報 `cad-viewer 0.5.0`，rootPath 為本 repository。
- Exact Repair 2 latched STEP 的 artifact endpoint：`state=rendered`。

因此 Viewer service 與 exact candidate artifact 現在可供使用者開啟。此證據不等於 Repair 2 browser canvas 已重新人工確認；先前 CUA transport 無法完成該層檢查。Validator 另由 current STEP 重新產生並人工檢視三張 `1600 x 1200` validation snapshots；formal reviewer亦檢視 locked、released `60 deg` 與 exploded 三張圖，確認左右模組與主要狀態可辨識，但 latch tooth／receiver 細節在整體視圖中仍不夠清楚。

## Evidence joined from independent roles

- Critic final：**PASS first-CAD preview only**；確認 neutral retention、actuated release、三桿接觸身份、左右鏡像與禁止架構均通過，並保留 physical unknowns。
- Validator final：**PASS first-CAD preview only**；focused P25 `23/23 PASS`，targeted P20 R4＋P24＋P25 `42/42 PASS`，actual-solid sweep、STEP reopen/parity、snapshots 與 Viewer readiness 通過。
- Reviewer 未把測試數量本身當成品質證明；接受依據是測試與 actual-solid measurements 對 frozen requirements 的逐項覆蓋。

## Explicitly not accepted

下列項目**沒有 physical acceptance**，不得從本次 ACCEPT 推論為已完成：

- spring force、spring selection 或重力方向無關的 opening bias；
- 解扣後「立即彈開」的速度或可靠性；
- cantilever release-tab 的所需按力、局部 strain、回彈、疲勞、蠕變與壽命；
- rear-yoke、Orange pad、OD2 hinge pin 與實際列印件的 fit／公差；
- 真實 holding force、摩擦、preload、抗鬆與 vibration；
- zero-cap module 的軸向留置；
- 左右 module 的實際負載均衡與避免 rod tilt；
- saddle／pad 最終接觸面。Source 目前仍以局部 tangent support／flat Orange pad 表達，尚未實作 DESIGN 文字中的 `120 deg`／`70 deg` concave profiles；
- slicing、print orientation、材料、support、列印品質、組裝或完整 physical prototype。

P20 inherited `RELEASED_OPEN` Blue/XT60 collision `186.980487360803 mm3` 仍存在；P20 print-kit fixture 亦有兩個既有 SHA-drift failures。兩者不是 P25 clamp 新增問題，但會阻擋把此 preview 說成完整機構／print release。

## Next smallest physical gate

下一步不是直接列印完整雙側夾具。先建立 **單側 latch／hinge functional coupon**，使用最終選定材料、列印方向、實際 OD4 rod 與實際 OD2 hinge pin，並加入真實 opening spring／等效 bias。這個 coupon 一次只回答以下可否決問題：

1. Neutral latch 是否能保持，不會因現有約 `0.9 deg` take-up 而明顯鬆動；
2. Release tab 的實際 travel 是否可在約 `1.50 mm` 內完成，按力是否可接受，且放手後能可靠回位；
3. 解扣後 front bar 是否在裝置正放、側放、倒放三種方向都主動離開 Orange surrogate，而不是靠重力；
4. `20` 次手動循環後是否仍可保持與釋放，沒有白化、裂紋、永久變形或 receiver 不回位。

若任一項 FAIL，先修 latch/flexure/spring，不製作完整雙側 prototype。Coupon PASS 後，再做兩側 full-module fit／axial retention／holding-force gate；在該 gate 前，應先把 saddle/pad profile 與 DESIGN claim 對齊。

## Final status

- **P25 R1 first-CAD preview：ACCEPT，僅限 frozen `a1932fb`。**
- **Written STEP：ACCEPT for preview／artifact inspection。**
- **Live Viewer：available on tailnet；service/artifact rendered verified；Repair 2 browser canvas not rechecked。**
- **Print candidate：NOT ACCEPTED。**
- **Physical mechanism：NOT ACCEPTED。**
