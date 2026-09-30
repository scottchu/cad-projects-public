# S1 — 平整與浮雕兩版表面提案

2026-09-06；owner /root/surface_variants_intent；status: intent proposal, not CAD.

## Current scope and evidence

使用者已對正面分色候選回覆「通過」。在助理提出「各色齊平或有高低浮雕」後，使用者先說「高低的浮雕。」，再說「都要」。本次採用的明示解讀是：保留同一張已接受美術，準備平整版與浮雕版兩種表面。這不是使用者已批准以下細部高度分區的證據；「都要」也不解讀成現在選尺寸、孔或製程。

本提案是已完成 face-only 階段之後的表面意圖補充；歷史 REQUIREMENTS、BRIEF/DESIGN frozen sections 與已接受 SVG 全不改寫。表面階段僅此提案為當前待確認事項。

## Fixed and proposed relationships

| ID | Status | Relationship |
|---|---|---|
| SV-01 | adopted interpretation | 同一張已接受車形美術，保留平整版及浮雕版兩種變體 |
| SV-02 | invariant | D4 輪廓、四燈、GRENADIER、DJZY 608、白邊及已接受色區不變；背面沿用連續黑色底板意圖 |
| SV-03 | flat proposal | 平整版全部可見色區表面齊平 |
| SV-04 | relief proposal, unconfirmed | 浮雕版：玻璃／水箱護罩較低；車身中間；車燈／保險桿較高。這是相對層級，不指定 mm |
| SV-05 | relief proposal, unconfirmed | 車牌底面與藍字局部齊平，避免細字另作凸起；車牌整體相對高度尚未選 |
| SV-06 | invariant | 色區與高度分區獨立；不按黑灰白藍直接指定高低。淡藍玻璃仍是同一藍＋白的混色意圖，不新增第五卷 |

兩版都是同一平面車形的固定磁貼，無活動零件，沒有把透視圖建成整輛立體車。此步驟只討論由背面向正面觀察的相對起伏；尚未定義 CAD 座標或列印朝向。浮雕高低可調，已接受美術固定。

## One pending user gate

請只觀察並確認浮雕的層級關係：「玻璃／護罩低、車身中、車燈／保險桿高，車牌字與底面局部齊平，這樣的起伏可以嗎？」通過僅接受此關係；不通過則修改被指出的區域。此提案尚未獲使用者確認。

## Scope and delta mask

Allowed now: document two variants and propose relative zones. Forbidden now: source/SVG/HTML edits, recolor/redraw, actual heights or total thickness, size, holes, CAD/STEP/mesh, slicing, printer actions or Tailscale changes. No assertion of nozzle resolution, achievable glass color, printable wall thickness or physical performance.

## S1 task and provenance

DAG: accepted face U6 → S1 bounded design-intent proposal → user relative-zone gate; downstream CAD remains unscheduled. Baseline git a8834040afe401637d36e94bd8fdd9e1d9874d35. Accepted candidate fingerprint f893d8fbf98750be9e7366a5cfd8c78c90e58a0d4d0c73d5c2480ba471b7e652. Exact input path/content hashes are in surface-variants-input-manifest.json. Excluded: mutable status, receipts and handoff indexes only. S1 reads project/policy, writes exclusively project docs, uses one attempt/~2 minutes/no agents; stop on baseline mismatch or scope uncertainty. Runtime model/effort inherited; no override selected.

Verification command: node projects/grenadier-fridge-magnet/scripts/face-candidate-manifest.mjs → exit 0, verified 10 entries, exact accepted fingerprint. This is source/artifact provenance verification only. No CAD, manufacturing or physical test was run.
