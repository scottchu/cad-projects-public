# J-X historical evidence receipt

Status: complete, read-only source audit, 2026-09-03. Owner: `/root/journey_history`. Brief input manifest verified as `5d587bf2b665ae44469ff2307da520d760b94bf5a51d36aeface1660d813dc97`. Only this report and `HISTORY.sha256` are written. No CAD, slicer, printer, or source-project mutation.

## Source authority and count

`C` below means `/Users/scottchu/Projects/personal/design-projects/projects/xt60-bend-jig`; `W` means this worktree's `projects/xt60-bend-jig`; `K` means canonical `projects/kage`.

Canonical `C/PROJECT_STATE.md:5–28` describes **P24 R1 manual three-slider clamp**, accepted only for user review of first-design intent, with inherited Blue/XT60 OPEN collision still present. The 740e checkout's P19 acceptance is historical, not latest product status. Canonical state has older active sections beneath the newest section; do not flatten these into simultaneous product acceptance.

Node `fs.readdirSync(path,{withFileTypes:true}).filter(x=>x.isDirectory())` counted immediate `docs/iterations` directories: **canonical 25; 740e 12**. Scope includes migration, coupons, scaffold, and design refinements. Safe claim: “25 recorded iteration folders in the canonical snapshot.” This is neither 25 versions nor 25 prints, nor a complete lifetime attempt count. Version labels alone do not establish 20+ attempts/prints. Exact canonical names:

`p13-r1-monorepo-migration`, `p13-r2-center-hole-fit-repair`, `p17-r2-balanced-rail-search`, `p17-r2-compact-plate-optimizer`, `p17-r2-direct-cad-counter-twist`, `p17-r2-fixed-reaction-rod-motion`, `p17-r2-head-up-tail-right-orientation-repair`, `p17-r2-lock-removal`, `p17-r2-locked-rod-layout`, `p17-r2-outer-force-balance`, `p17-r2-outer-rail-length-repair`, `p17-r2-outer-rail-topology-repair`, `p17-r2-three-rod-triangle-motion`, `p18-r1-compact-counter-twist`, `p19-r1-front-edge-short-tail`, `p20-blue-orange-web-coupon`, `p20-r1-fixed-rod-reset`, `p20-r2-fixed-rod-arc-rail`, `p20-r3-wire-90deg`, `p20-r4-blocked-test-print-3mf`, `p20-r4-custom-profile-full-cad`, `p21-r1-axial-width-cap-fit`, `p22-r1-bridge-latch-concept`, `p23-r1-mirrored-screw-clamps`, `p24-r1-manual-three-slider-clamp`.

## Purpose and five turning points

Purpose: hold/form **two insulated XT60 pigtail wires into a fixed 90-degree bend while soldering and cooling**; the plastic connector body is not the clamped load (`C/README.md:3`; legacy handoff below, lines7–20). Three rods contact/form the wires; paired plates guide them. P13 uses one rotary input; later counter-twist and direct finger actuation are different approaches to the same operation.

1. **Aug21–23: nominal geometry meets printed fit.** `C/docs/EXPERIENCE.md:52–69` records PETG/0.4mm nozzle/actual OD4mm rod coupons: 4.05 very tight, 4.10 hand push/pull but tight, 4.15 best sliding fit with slight friction, 4.20 looser, 4.25 wobble. Lines78–113 record actual P13 assembly failure and cap inconsistency. Exact recorded user terms: “middle stick” and “center hole” (line81); the surrounding sentence is a durable paraphrase, not a verbatim transcript. Four caps fit; two were too tight. A rendered LOCKED pose was not proof of locking.
2. **Aug24–26: tests and polished previews still leave the wrong relationship.** EXPERIENCE:116–123 records rejected P17 simulator: holes/slots appeared to move, despite passing deterministic tests. Lines173–203 record fixed-member identity confusion: the purple stepped axle, not a white forming rod, is fixed. Lines242–254 record removal of an unwanted lock, retaining the grip tab and making no self-lock claim. Lines309–328 record user approval of compact P17 2D gate into P18, while force/friction/heat and tool access remain open. This supports a messy correction sequence; it does not prove the exact later simulator was the first breakthrough. J-S owns simulator identification.
3. **Aug27: isolate the uncertain web.** P20 Blue–Orange coupon preserves both complete curved cutters and the thin ligament, rather than testing an unrelated straight strip. Physical question: do the slots remain open and the full-thickness web survive bed removal/ordinary handling? `C/docs/iterations/p20-blue-orange-web-coupon/BRIEF.md:14–33`. Prepared layer toolpaths provide digital evidence; the physical result is pending.
4. **Aug28: physical operation overturns a plausible correction.** EXPERIENCE:24–50 records photos/caliper feedback: inner span needs **+10mm**, caps are too tight, other issues remain. Initial CAD response wrongly lengthened purchased rods to60mm; user corrected them back to50mm. Direct Orange push feels smooth, but release immediately springs the mechanism open. These are supported width, fit and retention failures, not inferred aesthetics.
5. **Aug29–30: redefine the interaction.** EXPERIENCE:5–22 and `C/docs/iterations/p24-r1-manual-three-slider-clamp/HANDOFF.md:15–27`: thumb moves Orange down; index/middle fingers move Blue/Green back-to-front; clamp only holds the hand-reached endpoint. Six tight caps removed. P24 remains an intent preview with physical holding/release/fit unproven. Do not finish this story as a solved jig.

## Partial experiments and photos

**Observed physical test:** rod-hole coupon observations above. No recovered photo of that test. Existing `C/cad/p14_rod_fit_coupon/` contains STEP/3MF/provenance and generator; do not imply these are a photograph or prove exact identity with the Aug21 printed specimen without further binding.

Keep three evidence identities separate: **S01/Aug21 rod-hole observations** are physical results; **H2/P13 kit diagnostic blocks** are a rendered historical kit, not a photograph of S01; **H7/P20 web coupon** answers slot/web printability and is prepared-only. Safe captions: “Observed rod fit, PETG coupon, Aug21 (recorded results)”; “P13 diagnostic blocks in the CAD kit”; “P20 web experiment: prepared toolpaths; 6m12s slicer estimate; physical result pending.”

**Prepared experiment:** `C/docs/iterations/p20-blue-orange-web-coupon/PREPARATION.md:7–12,73–88` says not uploaded/started; real CLI produced valid G-code, 16 layers, **estimated6m12s and1.80g**. These are slicer estimates, not elapsed print time or saved material. Its inspected layer-witness image is directly useful. No full-product strength/assembly claim follows.

**Physical photo records:** EXPERIENCE:92–106 references three supplied images under `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/`. Photo1/2 are Viewer images; `3-Photo-3.jpg` is the physical P13 assembly (recorded SHA256 `8d12c39427823ff36c4205e70716db6df1f166aab87d113b7a0a767bb7f079fe`). Direct existence checks for Photo1 and Photo3 returned false. Referenced Aug28 photos have no recovered file path. No fabricated replacement.

## Inspected visual shortlist (eight)

All paths relative to `C`; all inspected with `view_image`. Labels must retain revision/evidence type. Images have useful light backgrounds. The P19/P20 front renders occlude much of the wire; pair with the P13 cutaway or exploded view to teach the operation.

| ID | Exact path | Visible content / recommended truthful caption |
|---|---|---|
| H1 | `docs/review/p13-historical/contact_22deg_cutaway_20260821T225152Z.png` | Wire bend and three rods; P13 contact cutaway, CAD render |
| H2 | `docs/review/p13-historical/p13_repaired_print_kit_iso_20260822T051402Z.png` | Four plates, shaft/caps/keeper plus two diagnostic blocks; P13 kit and coupons, CAD render |
| H3 | `docs/review/p18-r1-compact-counter-twist/p18-r1-exploded-iso_20260826T050923Z.png` | Two inner/two outer plates, three rods, separate purple axle; P18 R1 exploded CAD |
| H4 | `docs/review/p19-r1-front-edge-short-tail/p19-r1-impl05-open-front_20260826T182611Z.png` | P19 R1 OPEN, shorter rail profile, CAD render |
| H5 | `docs/review/p20-r4-custom-profile-full-cad/p20-r4-open-front-labelrepair_20260827T210320Z.png` | P20 R4 OPEN, changed rail curves, blocked intent preview |
| H6 | `docs/review/p20-r4-custom-profile-full-cad/p20-r4-open-axial-stack-labelrepair_20260827T210316Z.png` | Paired plates, rods/caps and connector span; P20 R4 axial CAD before width correction |
| H7 | `cad/p20_blue_orange_web_coupon/prepared/r1/toolpath-witness-first-middle-top.png` | Three layer slices, actual1.715mm web locator; prepared coupon toolpaths, physical result pending |
| H8 | `cad/p24_r1_manual_three_slider_clamp/p24_r1_operation_annotated.png` | Hand-position-first/clamp-last sequence; P24 first-design intent preview |

## Supported complaints and Kage boundary

Do use actual fit/width, wrong member identity, lock removal, back-drive, solder/removal-clearance concerns. “Bulky” appears as a **P24 design tradeoff**, not a verified user complaint. “No base/frame holder/decorative handle” is a P13 constraint (`C/docs/legacy/HANDOFF-2026-08-21.md:13–20`), not proof a printed base was rejected. No independently recovered literal “awkward” or cable complaint; do not manufacture quotes.

Supporting Kage: `K/PRINTING_PROFILE.md:45–50,72–76` records printed base pieces with slight outer seam gap and one proud piece, yet usable for free-roller mounting; source/process/date unbound. Upright attachment and lateral weakness are concerns, not observed fractures. `K/docs/EXPERIENCE.md:5–10` distinguishes omitted-solid-pair failures from physical results; no complete accepted physical set. This is useful supporting evidence, not a stronger success story than XT60.

## Verification and remaining risks

Read project/root instructions and continuity; searched only with `/opt/homebrew/bin/rg`; used Node read-only directory inventory, `nl`/`sed`/`cat`, direct file existence checks, `git log -6 --date=short --format='%h %ad %s' -- projects/xt60-bend-jig`, and eight image inspections. Git history stops before latest uncommitted canonical records; chronology above follows dated observations, not guessed commit dates. `HISTORY.sha256` freezes exact used primary files and visuals. Parent should copy selected sources/assets into its presentation-owned frozen snapshot before building; if mutable canonical sources drift, use the copied snapshot and record drift rather than silently mixing candidates. Physical photo recovery and total actual print count remain unavailable. No physical success claim is warranted.
