# P1 R1 — face-only intent

<!-- frozen:start -->
## Frozen design contract

2026-09-06，新專案。baseline git `a8834040afe401637d36e94bd8fdd9e1d9874d35` 加 manifest 指定的 dirty policy bytes。D4 SHA-256 `44d20b6b2050d639c44ef00d6396b4150f9ed7280b3d1db4c361be8f31b22171`；Photo 6 `addbd1cf72c604ed3b1fcda40ede9e6cf3319fe99c925eaace0f7296c2fce3e4`。

最新 user scope：「先不選。一步一步來」「洞很好加」。當前只把 D4 轉成可比較的 2D 五類視覺色區（四種實體線材＋玻璃混色意圖），依 REQUIREMENTS GM-01..09 及 DESIGN frozen contract。尺寸、磁鐵和剖面已延後；不再提出相關選擇。所有寫入限專案 namespace。

D5 凍結 intake、範圍、原圖與可操作的 D7 handoff。D7 可立即做 2D separation，無須等磁鐵、mm尺寸或混色 coupon。後續 review 讓使用者觀察固定的原圖與可修正的色區輪廓，問：「分色後的輪廓、四燈、字樣與玻璃有沒有保留你接受的 D4？」這只核准 2D 意圖。

禁止 3D、孔、剖面、slice／print；沒有 release artifact。physical color、nozzle 細節、磁鐵與強度全未驗證。
<!-- frozen:end -->

## Mutable delegated execution plan and status

共同 baseline 如上。`intent-manifest.json` 是 D5 输出與 D7 输入 manifest，依排序 path/content SHA-256，BRIEF/DESIGN 只含 frozen markers 之間 section。排程前 root 必須把後續 owner、範圍及 ceiling 具體化。

| ID | Role / owner | Deps | Immutable inputs | Exclusive writes | Done gate | Group | Ceiling | Status |
|---|---|---|---|---|---|---|---|---|
| D5 | design / /root/magnet_design | accepted D4 | intake＋policy hashes；输出 manifest | 專案全域 | face-only contract＋reference copies＋manifest | A | strong/high, 約8分, 約8k tokens, receipt1200 words | ready for D7 |
| R1 | research / /root/glass_process_research | accepted D4 | root 指定研究 manifest | read-only | 平面混色限制／後續 coupon | A | root bounded task | root收集中；不阻擋D7 |
| D7 | 2D implementation / unassigned | D5 | D5 manifest | root指派 source/review/artifact scope | 向量分色＋對照＋trace receipt | B | balanced/medium，派發前定time/token | dependency ready |
| D8 | critic / unassigned | D7 frozen | D7 manifest | read-only | 輪廓／遺失細節風險 | C | strong/high；派發前定time/token | not scheduled |
| D9 | validator / unassigned | D7 frozen | 同候選指定輸入 | read-only | source/provenance／色區證據 | C | strong/high；派發前定time/token | not scheduled |
| D10 | formal review / unassigned | D8,D9 | candidate＋receipts | read-only | traceability join | D | strong/high；派發前定time/token | not scheduled |
| U6 | user 2D comparison / user | D7＋必要獨立檢查 | concrete2D候選 | root記錄 | D4意圖保留判斷 | E | user-controlled | not yet shown |

### Task detail: D5

Owner `/root/magnet_design`，單一 design/bootstrap 角色；allowed reads policy/templates/供圖/project。exclusive writes 僅專案；forbidden 其他 dirty 工作、root deps/env、CAD、slice/print。deliverables docs、供圖副本、D7 handoff、manifest；exact commands/results 見 VALIDATION。單 writer，R1 read-only 可並行；初次加最多2次聚焦修正，output1200 words，time約8分/token約8k qualitative。最新 scope change 立即停止舊 gate；D5 不自行 trace，不批准自己的 deliverable。完成後釋放寫入給 D7。

D7..D10 派發時需不同 owner（implementer/critic/validator/formal reviewer 不可同身份）、task-specific input manifest、allow/forbid/write scope、time/token/output/retry/concurrency ceiling。最多3 worker、initial+2 repairs，過限重開契約。D7 当前為純2D，不跑 CAD 核心四類實體測試；未來 CAD 再凍結另階段契約。
