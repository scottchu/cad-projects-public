# P25 R1 task DAG

日期：`2026-09-05`  
輸入 manifest：`DESIGN_INPUT_MANIFEST.sha256`  
並行上限：三個 worker；同一 source/artifact namespace 同時只允許一位 writer。  
修復上限：初次實作後最多兩次 focused repair；超過即重開設計。

## Frozen scope

所有 task 均使用同一份已驗證的 immutable input manifest。只有本目錄的 orchestration／receipt 文件可在下游追加；manifest 所列 source、P24 history、rails、rods 與 baseline artifacts 不得變更。

## DAG

`P25-DESIGN-02 -> P25-IMPLEMENT-01 -> (P25-CRITIC-01 || P25-VALIDATE-01) -> P25-REVIEW-01`

有 material finding 時：`CRITIC/VALIDATE -> P25-IMPLEMENT-01-REPAIR-n -> CRITIC/VALIDATE focused rerun -> REVIEW`。

## Task contracts

### P25-DESIGN-02 — independent mechanical design authority

- 角色：strong/high mechanical designer；與 implementer、critic、validator、reviewer 身份不同。
- 目標：凍結已確認的三指操作、後軛＋前壓桿拓撲、兩側鏡像模組、鉸鏈、快扣與立即離開 Orange 的 release gate。
- 依賴：immutable manifest 驗證成功。
- 允許讀取：manifest 所列檔案、`AGENTS.md`、`docs/CAD_WORKFLOW.md`。
- 獨占寫入：本目錄 `BRIEF.md`、`DESIGN.md`、`TASK_DAG.md`。
- 禁止：CAD、tests、artifact、continuity、P24、slicer、printer。
- 完成 gate：三份文件明確保留 `OD4x50`、零 cap、零 screw cassette、既有 paths，並列出參數、states、contacts、tests、risks、stop conditions。
- 證據：三個路徑及 `shasum -a 256 -c DESIGN_INPUT_MANIFEST.sha256` 結果。
- 上限：一次設計交付；約四分鐘；無 retry。

### P25-IMPLEMENT-01 — bounded parametric CAD implementer

- 角色：balanced/medium CAD implementer；不得批准自己的設計。
- 目標：建立 source-first 參數化兩側模組與三個 required states。
- 依賴：`P25-DESIGN-02` 完成；重新驗證 immutable manifest；凍結 BRIEF/DESIGN hashes。
- 允許讀取：P25 三份設計文件、manifest inputs、CAD skill references、現有 P20 source/tests。
- 獨占寫入：新的 P25 source、focused tests、`cad/p25_r1_rear_loop_front_pusher_clamp/` artifacts、`IMPLEMENTATION.md`、candidate manifest。
- 禁止：修改 P20/P24、rails、rod dimensions、continuity、slicer、printer、其他 project。
- 完成 gate：pure-math checks 先通過；三個 STEP 成功；actual-solid contacts/collisions、state labels、mirror parity 與 source/export parity 可重現。
- 證據：exact commands/results、artifact hashes、occurrence census、collision/contact table、candidate fingerprint。
- 上限：初次實作加最多兩次 targeted repairs；單次只修最小 source delta。
- 停止：任何 DESIGN stop condition、manifest drift、或需擴大 scope。

### P25-CRITIC-01 — independent mechanical critic

- 角色：strong/high critic；只讀 candidate，不執行修復。
- 目標：尋找錯誤受力圈、錯桿接觸、左右傾斜風險、重力依賴、裝卸阻塞、過度約束及與照片觀察不符之處。
- 依賴：P25 candidate fingerprint 凍結。
- 允許讀取：frozen design、candidate source/tests/STEP/snapshots、manifest inputs。
- 唯一寫入：`CRITIQUE.md`。
- 禁止：source、tests、artifact、continuity。
- 完成 gate：逐項判定 topology、causality、contact、release、two-side support；findings 有 severity、evidence、最小修正及 PASS/FAIL。
- 上限：一次完整 review；repair 後只 rerun 受影響項目。

### P25-VALIDATE-01 — independent geometry validator

- 角色：strong/high validator；身份不得與 implementer/critic 相同。
- 目標：獨立重跑 math、constraint、requirement、actual-solid collision/contact、motion sweep、STEP parity 與 snapshots。
- 依賴：與 critic 共用同一 frozen candidate fingerprint；可與 critic 平行。
- 允許讀取：frozen design、candidate、tooling；可執行 read-only inspection。
- 唯一寫入：`VALIDATION.md`；若事前授權，可在 P25 artifact namespace 產生 deterministic validation snapshots。
- 禁止：修 source/tests、continuity、slicer、printer。
- 完成 gate：每個 DESIGN required check 有 command、數值結果與 disposition；baseline collision 分開列出；明確區分 CAD、artifact、physical status。
- 上限：一次完整 validation；repair 後只重跑受影響 gate，再做 final focused regression。

### P25-REVIEW-01 — formal independent reviewer

- 角色：strong/high formal reviewer；不得是前述任一角色。
- 目標：以 frozen fingerprint join design、implementation、critique 與 validation receipts，決定是否接受為 user-facing first-CAD preview。
- 依賴：critic 與 validator 均完成且指向同一 candidate；重大 finding 已關閉或明確阻擋。
- 允許讀取：所有 P25 frozen inputs、candidate、receipts、Viewer readiness evidence。
- 唯一寫入：`REVIEW.md`。
- 禁止：修改 candidate、continuity、slicer、printer。
- 完成 gate：`ACCEPT`、`REJECT` 或 `BLOCKED`；列出 requirement coverage、未解風險、Viewer surface、candidate fingerprint 與下一個最小 physical gate。
- 上限：一次 formal join；若 candidate 改變，舊 review 失效並建立新的 review receipt。

## Root coordination after formal review

只有在 `P25-REVIEW-01` 接受同一 frozen candidate 後，root 才可更新 `PROJECT_STATE.md`、`docs/iterations/CURRENT`、active `HANDOFF.md`、`NEXT_AGENT.md` 與必要的 `EXPERIENCE.md`。更新只能陳述已驗證證據，不得把 first-CAD acceptance 提升成 print 或 physical acceptance，也不得建立 PR、部署 Tailscale、切片或啟動列印，除非使用者另行明確要求。
