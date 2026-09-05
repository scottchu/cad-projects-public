# Reduced measurement-preview contract (DES-02)
<!-- FROZEN-CONTRACT-BEGIN -->
Scope: ONE essential axial-clearance and diameter section only, Traditional Chinese, compact and accessible. No radial-thread-budget/texture strips or controls. All full CAD/thread/texture requirements in ../../REQUIREMENTS.md remain unchanged and pending.
Editable defaults: L=208, D=29, axialSlack=5, radialGap=1.5 per side. Fixed displayed references: wall=2.4, floor=3, lower cavity=137, overlap=5. Cap cavity=C-137+5=81 by default.
Derived: C=L+axialSlack; ID=D+2*radialGap; plain-body OD=ID+2*wall=36.8 initially. Plain-body OD does not determine threaded-junction OD.
Validate finite positive L/D, nonnegative slack/radialGap and positive derived cap cavity. Invalid inputs show an error and no plausible stale geometry; do not silently clamp. Report unmet axial>=3/radial>=1 targets without claiming acceptance.
Coordinates mm: inner lower floor z=0; outer lower floor z=-3; inner upper floor z=C; outer upper floor z=C+3. C excludes both floors. Lower mouth137; upper mouth132; dimension overlap5 separately. All drawn boundaries derive from those coordinates.
Draw the provisional device envelope with widthD and lengthL using the same dimension-to-screen mapping as the cavity; no generic silhouette or arbitrary pixel-length substitute. Keep device size constant as axial position changes.
Normalized slider q in[0,1]: device bottom=q*axialSlack, device top=q*axialSlack+L. Bottom gap=q*axialSlack; top gap=(1-q)*axialSlack. Presets「置中」q=.5 and「靠底」q=0. Show both individual gaps, total slack, L/D, C/ID and derived cap depth.
Interior position label「未固定：僅示意位置」; bottom-contact label「由底面承托：底端接觸」; top-contact label「頂端接觸；不代表固定」. If slack=0, label both-end contact regardless of q. Gravity points toward lower floor. Never imply retention or static floating.
External stop annotation, its symbol and leader remain ENTIRELY OUTSIDE the case outer contour; it is only an illustrative datum at z=132. Do not draw any internal stop/contact tab, retention structure or finalized thread geometry.
Keep label「有效咬合5–6目標；尚未定案」separate from overlap5. No thread profile or engagement claim is authorized.
Persistent label「尺寸待實測；此圖不代表已驗證配合」. Edits/presets never grant measurement or intent acceptance. Request measured installed-head L/maxD and end-contact decision outside the fragment.
Open issues persist: total slack cannot enforce neither-end contact; actual dimensions unconfirmed; root-wall/thread-OD and effective engagement unresolved; texture phase unresolved. This preview supplies no solution or waiver.
Checks: independently verify default and changed dimensions; q=0,.5,1 including zero slack; actual rendered floor positions/widths; invalid-input behavior; external-only stop annotation; keyboard interaction; readable labels at736/360px and light/dark. No CAD, STEP/mesh, slicing or physical acceptance.
Recovery scope is deliberately smaller after IMP-01 initial attempt plus two repair cycles. DES-02 reopens design under the documented retry escalation; it does NOT reset, waive or conceal IMP-01's exhausted ceiling. New recovery owner is case_preview_recovery, Sol/high, with root-assigned bounded scope.
<!-- FROZEN-CONTRACT-END -->
## Supersession and progress (mutable)
DES-02 supersedes the original preview scope only. Initial frozen sections retained as inputs/DESIGN.initial.contract.md and inputs/BRIEF.initial.contract.md; original seven-input manifest and fingerprint retained as inputs/contract.initial.sha256 and inputs/fingerprint.initial.txt. Historical manifest entries retain their original path names; the corresponding initial section content is preserved under the initial snapshot names.
Root-reported cause: initial dimensional/runtime defects; repair1 fixed most; repair2 text transformation corrupted SVG coordinates and was not frozen. No failed evidence is promoted to acceptance. Root owns current execution/index updates; this task changes design documentation only.
