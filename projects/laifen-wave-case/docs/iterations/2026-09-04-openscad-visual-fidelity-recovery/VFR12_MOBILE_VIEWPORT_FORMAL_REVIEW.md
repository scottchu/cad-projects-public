# VFR-12 C3 independent formal review

Status: **PASS for advancement of the exact C3 candidate to authorized private Tailscale delivery.** V12-01 through V12-07 pass the local presentation gates. V12-08 remains a post-deployment gate: verify the exact served bundle and inspect the private route before claiming delivery, and keep actual-user iPhone/Safari acceptance explicitly open until observed.

Reviewer: `VFR12-F` / `/root/openscad_vfr12_mobile_formal`. Project `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`; iteration `2026-09-04-openscad-visual-fidelity-recovery`. This report is the sole write. Source, tests, manifests, evidence, continuity, services and deployment were read-only. Review used one bounded attempt, with one corrected checksum working-directory invocation; no implementation repair or browser/test rerun. Qualitative ceiling: strong/high review, 15 minutes, one receipt, no subordinate workers.

## Exact authority and independent join

| Item | SHA-256 / verification |
| --- | --- |
| C3 candidate `candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256` | `2a58f483d2ba653c7e3c7de747bec8466837dd7f46ee4cd493ef9e8b61199433`; 9/9 members verified |
| Frozen task `VFR12_MOBILE_VIEWPORT_TASK.md` | `457b3e8d29122e4fd60c8f2dcd74f4fccf727cc246f51d83c98f1ee890573e1d` |
| Frozen baseline input manifest | `adffc64b4e496b15a3e023c8704bb254db732c0aa62d0558994f56276e933ef4` |
| C3 implementation receipt | `41eff4fcdcd8628451387d1836fd4559ade1907e889b2216a0247c699e4ce1f8` |
| C3 independent validation | `6c3c778aa813d515d314e1df4f4356961c16e9f92a1509e6c8463db7c81f7d4f` |
| C3 independent critique | `2f4ec4b3b21a06b80ed692b3071675ffcc75e15fe85fdda3529877d727736935` |
| Independent validation evidence `scratch/vfr12-mobile-c3-validation/evidence.sha256` | `6665df989b43610e0e0ad2c141b646afd4907673d389954a11ff904d56f20404`; 33/33 members verified |
| Supplemental build inputs `scratch/vfr12-mobile-c3-validation/build-inputs.sha256` | `a92147f83fd81b842ab32d9309105fc428b6a60eccd95682932c419f6820c84c`; 8/8 members verified from repository root |
| C3 mobile CSS | `b530ae8870b5b2c0eb9548192edeb96fb122860ead203eb1295bd9ebb3893114` |
| C3 focused test | `bf9ee06d1d3648f9d0fcec27c626f50a8d501db0395d9f071d86a1808b28a79c` |

The baseline manifest's 15 unchanged members still match; its two changed members are the explicitly permitted CSS and focused test. The current C3 manifest binds their replacement bytes. Supplemental SCAD, runtime JS/WASM, dependency lock, build config and root/project package inputs all match. HTML `997c2fbc80f453911c3ba68fed55ab17b3c9d2d56d7bb99ceee43a9e0ee82d6f`, main `98af41e1377afb873208977eedc679ea9e887b04b96253bc2025b3896fbeb353`, schema `894062333ba7370c4b17efc93b788623eb9db86d0117ffc45275886d0f754ae0`, worker `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`, and SCAD `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841` are preserved.

The runtime role identities are distinct: designer `/root/openscad_vfr12_mobile_designer`; implementer `/root/openscad_vfr11_mobile_impl` acting as VFR12-I; validator `/root/openscad_vfr11_mobile_validator`; critic `/root/openscad_vfr11_mobile_critic`; formal reviewer as named above. Reuse of VFR-11 runtime identities within the same implementation/validation/critique roles does not combine independent roles. The validator independently built and ran the browser; the critic independently inspected candidate bytes and implementation screenshots. Their C3 receipts name the same fingerprint. The critic's inspected initial 360/390/430 and desktop screenshots are byte-identical to the corresponding independently generated, manifest-bound validation screenshots, as confirmed by their hashes. This strengthens the join without relabelling the critic's work as a browser rerun.

## Findings and requirement traceability

No unresolved material finding blocks this bounded presentation delivery.

| Gate | Formal disposition and decisive evidence |
| --- | --- |
| V12-01: remove visible mobile title/status | PASS locally. Fresh mobile screenshots show neither title nor ready sentence. Bound DOM observations retain status text and `aria-live=polite` in an absolute clipped 1px box, with display:block and visibility:visible. |
| V12-02: full-width borderless viewer | PASS locally. At 390x844 the canvas/result span x=0..390 and y=0..219.4375, with matching bottoms and zero border/padding/radius. The 360/430 screenshots show the same edge-to-edge treatment at heights 190/220px. Fullscreen means full-width top pane with controls below, as frozen in the task. |
| V12-03: fields/actions usable | PASS locally. Complete first labels and 46px inputs appear at all phone sizes, with 11px horizontal input inset. Five targets share one row, each 46px high and at least 64.39px wide. Final Output has 135–165px clearance above actions and successful top/center/bottom hit tests at maximum form scroll. |
| V12-04: actual icon size, placement and color | PASS. Measured 24x24 pseudo boxes are centered within 0.0078125px. Actual painted marks are Generate 22x22, Cancel 20x20, Reset 21x21, camera 19x19, Download 20x20; maximum painted-bound center error is 0.890625px horizontally and 0.5px vertically across all three phone widths. Generate is white on navy with sampled contrast 16.15:1. The independent screenshots visibly agree. |
| V12-05: responsive edges | PASS locally. Bound fresh initial and max-scroll observations cover 360x640, 390x844, 430x932 and 700x844; 701px restores desktop styling. All six tested widths have scrollWidth=clientWidth. |
| V12-06: sticky viewer and state flows | PASS locally. Bound browser evidence covers document/form scrolling, actionable toast and focus return, real smooth generation and visible model, successful download, subsequent visible stale warning with disabled Download, and all five disabled surface/Diamond controls. No accepted-run page errors, console errors or failed requests were recorded. |
| V12-07: desktop and immutable runtime | PASS for preservation. Desktop heading/status, 16px action words and 580px canvas remain. Formal comparison confirms the built CSS before `@media` is byte-identical to both VFR-11 C2 and VFR-12 C2 validation bundles. Immutable hashes match. The validator records seven focused tests and a successful real Vite build; this review did not rerun them. |
| V12-08: private delivery/user surface | PENDING delivery. This review permits the authorized delivery role to advance the exact bound C3 bundle to the existing private route and verify its bytes and mobile rendering. It does not claim the route already serves C3 or that actual Safari/user acceptance has occurred. |

The original contract described font glyphs with a 24px font-size. The bounded repairs replace font-dependent ink with empty-content SVG masks in the same 24px slots; font-size is no longer the sizing mechanism. This is a disclosed implementation substitution within the mobile icon object scope, directly addressing the observed font-metric failure. The user-facing size, meaning/order, alignment, touch targets and meaningful DOM names remain the acceptance properties. No runtime or geometry scope expansion is involved.

The four CAD evidence categories are not newly exercised by this CSS correction. The established geometry authority is preserved by hashes; browser generation/download confirms flow only. Existing CAD, exported artifact/slicer and physical acceptance cannot be inferred from this PASS.

## Repair history and discrepancies

C1 manifest `024e441289844b118d8f4fbc9a5a26cabdab6dca50507dfcbbe7b9827a18320c` is superseded: its nominal box checks did not close the critic's 12x10px camera ink / 3px-low finding. C2 manifest `86b208a98eff4d5fd34558de1050ccf6224593209210236a060027b9a0192bbf` is superseded: independent validation found black Generate paint, undersized Cancel/camera/Download marks and a low Reset mark. C3 closes those concrete failures with actual screenshot pixels and matching critique/validation. The earlier C1 validation PASS and C2 critic's permissive camera judgement are not carried into current acceptance; the stricter measured failures govern the repair history.

C2 validation hash `9ebade4791521344d97e5995182e6e591ac566be8a231b1fe2e617767ce83628` and critique hash `576b9d5badda8d6dd8981db4780faad54f109de9b020e23163c30df26af96550` were verified. The C2 critique contains a mistyped focused-test hash: its candidate manifest actually binds `36a593d0eb40065aeaf5b2d97bcd24d36741957b7a5d3b72adde4fc41d4087f2`. The implementation receipt also retains a first-candidate status/hash summary above its two chronological repair sections. These are low-severity historical receipt inconsistencies; the C3 manifest and final repair section are unambiguous and all nine current members verify. This report resolves their interpretation without rewriting history.

The initial attempt and both allowed focused repairs are consumed. No further VFR-12 source repair is authorized by this task ceiling. A new material defect requires reopening/superseding the bounded task and refreezing affected inputs, not C4 within this chain.

The validator's failed port-8775 launch and already-dispatched probe are explicitly excluded from acceptance. The accepted 8779 run verified root bytes against the bound built index and produced the verified 33-member inventory. Formal review uses that inventory only. Independently, this reviewer first invoked the supplemental repository-relative input manifest from project cwd; that check failed on wrong paths. Repeating from repository root passed 8/8. This was a review-command correction, not candidate drift.

## Evidence inspected and commands actually run

Read repository `AGENTS.md`, `docs/CAD_WORKFLOW.md`, `docs/PROJECT_CONTINUITY.md`, project state/handoff/requirements/experience/decision index, active BRIEF/DESIGN, VFR-12 task/implementation, C1/C2/C3 manifests and critique/validation reports, source CSS/focused tests, accepted browser JSON and pixel-analysis script. The project state/handoff still describe delivered VFR-11; root should update these concise indexes with the C3 review/delivery receipt when that stage completes.

Opened the original phone image at original detail, then the accepted C3 `360x640-initial.png`, `390x844-initial.png`, `430x932-initial.png`, `390x844-final.png`, `1440x1200-initial.png`, `desktop-actions.png`, `mobile-generated.png`, `mobile-toast.png` and `mobile-stale.png`. These show resolved viewer/status/icon complaints, substantial centered action marks, readable complete fields and visible state feedback. The inherited desktop form is visually preserved; this is not a general desktop usability certification.

Decisive shell commands, with cwd explicitly identified:

```text
# project cwd
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR12_MOBILE_VIEWPORT_C2_VALIDATION.md docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR12_MOBILE_VIEWPORT_C2_CRITIQUE.md scratch/vfr12-mobile-implementation/final-360.png scratch/vfr12-mobile-implementation/final-390.png scratch/vfr12-mobile-implementation/final-430.png scratch/vfr12-mobile-implementation/final-desktop.png scratch/vfr12-mobile-implementation/final-measurements.json
# iteration cwd
shasum -a 256 candidate/VFR12_MOBILE_VIEWPORT_CANDIDATE.sha256 candidate/VFR12_MOBILE_VIEWPORT_C2_CANDIDATE.sha256 candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256 VFR12_MOBILE_VIEWPORT_C3_VALIDATION.md VFR12_MOBILE_VIEWPORT_C3_CRITIQUE.md VFR12_MOBILE_VIEWPORT_IMPLEMENTATION.md inputs/VFR12_MOBILE_VIEWPORT_INPUTS.sha256
# C3 validation scratch cwd
shasum -a 256 evidence.sha256
shasum -a 256 -c evidence.sha256
# repository cwd, correcting the earlier wrong-cwd attempt
shasum -a 256 -c projects/laifen-wave-case/scratch/vfr12-mobile-c3-validation/build-inputs.sha256
git status --short
PYTHONDONTWRITEBYTECODE=1 uv run python -B - <<'PY'
from pathlib import Path
import hashlib,json
p=Path('projects/laifen-wave-case')
i=p/'docs/iterations/2026-09-04-openscad-visual-fidelity-recovery'
for line in (i/'inputs/VFR12_MOBILE_VIEWPORT_INPUTS.sha256').read_text().splitlines():
    expected,name=line.split(maxsplit=1)
    actual=hashlib.sha256((p/name).read_bytes()).hexdigest()
    print('MATCH' if expected==actual else 'CHANGED',name)
s=p/'scratch/vfr12-mobile-c3-validation'
v=json.loads((s/'viewport.json').read_text())
print('viewport keys',list(v))
ink=json.loads((s/'ink.json').read_text())
print('ink',json.dumps(ink,separators=(',',':'))[:7000])
for name in ['vfr11-mobile-c2-validation','vfr12-mobile-c2-validation']:
    base=p/'scratch'/name/'dist/assets'
    if base.exists():
        for css in base.glob('*.css'):
            a=css.read_text().split('@media',1)[0]
            b=next((s/'dist/assets').glob('*.css')).read_text().split('@media',1)[0]
            print('desktop-prefix',name, a==b)
PY
```

Correctly rooted checks exited 0, candidate/evidence/build-input counts were 9/9, 33/33 and 8/8, and both desktop comparisons returned True. The final report hash is returned separately in the role receipt to avoid a self-referential file hash.

## Delivery boundary and next action

Advance only C3 and its bound `scratch/vfr12-mobile-c3-validation/dist/` bytes to the existing authorized private route `https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/`, followed by exact served-byte/MIME and mobile-rendering verification. Record the delivery receipt and refresh continuity indexes. This review performed no deployment or service change.

Actual iPhone/Safari, native WebKit masking, dynamic chrome/safe areas, keyboard, zoom/text scaling, native screen-reader behavior and user comprehension of the two reset icons remain open observations. The Chromium evidence and active `-webkit-mask` computed properties do not establish Safari acceptance. Existing cancellation-race/Diamond browser HOLD remains; no public Diamond enablement, CAD/STEP/mesh/slicer acceptance, print/fit/assembly acceptance, public hosting, MakerWorld action or printer action follows from this presentation review.
