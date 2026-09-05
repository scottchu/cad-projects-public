# VFR-11 C2 formal review

Status: **PASS for advancing this exact mobile-density candidate to private Tailscale delivery.** The frozen mobile contract is satisfied by the inspected local candidate. The previous blocking overlap and disabled-state findings are resolved. This is a local formal join, not actual-phone acceptance, Diamond enablement, cancellation-race acceptance, or CAD/physical approval.

Owner: `VFR11-F` / `/root/openscad_vfr11_mobile_formal`, distinct formal reviewer. Project: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`. Iteration: `2026-09-04-openscad-visual-fidelity-recovery`. Sole write: this report. Source, tests, manifests, evidence, continuity, services and deployments were read-only. Review used one bounded evidence pass, no implementation repair and no browser rerun.

## Verified authority and independence

| Authority | SHA-256 | Verification |
| --- | --- | --- |
| `candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256` | `ad7c14d9f40f354c70cbaf0394b89a9a03f795ec9e4d767c55c263096f054968` | Exact assignment match; 8/8 members OK |
| `VFR11_MOBILE_DENSITY_C2_VALIDATION.md` | `367e0c351c35562ef43931de48c93c07bc09bec0c51c1d79c3dbf4f5a2210574` | Exact assignment match |
| `scratch/vfr11-mobile-c2-validation/evidence.sha256` | `58c9e14211b610a6be670cbbfad998485da6e911690270371a54a26c83e17ed7` | Exact assignment match; 22/22 members OK |
| `VFR11_MOBILE_DENSITY_C2_CRITIQUE.md` | `e4049f1945be10679d500f4f1cb2b249fdc5a808efd04c980a3f085ec186c4bf` | Exact assignment match |
| `scratch/vfr11-mobile-c2-validation/build-inputs.sha256` | `a92147f83fd81b842ab32d9309105fc428b6a60eccd95682932c419f6820c84c` | 8/8 members OK from repository root |
| `VFR11_MOBILE_DENSITY_TASK.md` | `11593f5489d6dbc005662db233452d110df4a32ba1dfcf83716238a7117ded19` | Frozen user contract; candidate member |
| `VFR11_MOBILE_DENSITY_IMPLEMENTATION.md` | `c20d234e5bf291cc1b81a78cf9f519c310ff6305eacb49ee35e82afddcab78b6` | Candidate member including repair receipt |
| Prior `VFR11_MOBILE_DENSITY_CRITIQUE.md` | `5c46ea2fa774ecf7fa2e0ad487ed13cbd2a452f221159aeced0e673666f24171` | Verified historical findings |

Supplemental contract bindings read for this review: input manifest `df6116526ef04d7fd589d1c8a8d344a9ce69ca2f0e2745ba029e70ac9e2456f6`; BRIEF `2d853e2be1e1d3b49646d356d83d47b54bc8901e28cf336d685e3a8a2f51e5ce`; DESIGN `fcea1f7507083e6932607c1b5473dbccc9648facc8a7ca057def907d4ab57bb5`. The VFR11 task is the exact bounded mobile contract; broad iteration placeholders and older continuity pointers do not supersede the C2 manifest.

Root explicitly confirmed implementer identity `VFR11-I` / `/root/openscad_vfr11_mobile_impl`. Independent receipts identify validator `VFR11-V` / `/root/openscad_vfr11_mobile_validator` and critic `VFR11-C` / `/root/openscad_vfr11_mobile_critic`; the live agent inventory corroborated those two roles and this distinct reviewer. The implementation receipt lacks its own Owner field; this explicit coordinator attestation closes that documentation gap here. No implementer approval is used as independent acceptance.

## Requirement traceability and findings disposition

| Frozen requirement | Formal result and decisive evidence |
| --- | --- |
| Hide mobile title/caption at widths <=700 px | PASS: source media query and 390x844 capture show no header; status/preview start project content. |
| Compact five-icon action row | PASS: all five actions fit the initial screen in order; measured targets approximately 66.4x46 px, with successful center hit tests. |
| Responsive canvas near 220 px and a complete first Basic field | PASS: source clamp 190–220 px; actual canvas 219.4375 px high; complete first label/input spans y371.4375–443.4375 and remains hit-testable. |
| Independently scrolling fields with sticky preview/actions | PASS at tested states: preview sticks to top and actions remain at y785–844; at initial page scrollY=0 and form maximum 2551, final Output control spans y690.4375–734.4375, leaving 50.5625 px clearance. Top+1, center and bottom-1 hit tests all return `output_mode`. Prior High overlap is closed. |
| At least 44x44 touch targets and retained accessible names | PASS within controlled evidence: actions and final select meet dimensions; DOM words remain and Chromium names contain the explicit action wording. Decorative prefixes remain, so clean glyph-free names and actual screen-reader pronunciation are not claimed. |
| Distinct usable action states | PASS: initial Cancel/Download visibly muted; real smooth generation enables Download; subsequent edit removes href, disables Download and exposes stale. Prior disabled-state defect is closed. |
| Preserve desktop labels, IDs, order, listeners, states, focus/toast behavior | PASS for preservation: unchanged HTML/main, visible desktop words at 16 px, 580 px desktop canvas; fresh desktop-top capture covers heading at scrollY=0. Toast dismissal returns focus to Generate and Reset restores 208. Disabled styles intentionally also affect desktop pixels; layout and behavior are preserved. |
| Preserve source/runtime/geometry and disabled Diamond controls | PASS for preservation: HTML/main/schema/worker match pre-VFR11 input hashes. Supplemental build manifest verifies SCAD `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`, vendor JS/WASM, lock, package inputs and Vite config. All five surface/Diamond controls remain disabled in browser evidence. No geometry acceptance is inferred. |

The initial critic's Medium finding combined several issues. C2 corrected disabled styling and changed the camera glyph. The C2 validator correctly left glyph comprehension/name cleanliness for disposition. I concur with the C2 critic that the remaining issue is **Low**, not an unclosed blocker under the frozen contract: that contract explicitly permits names through DOM text, and meaningful action words remain in computed names. It does not require aria-label/title specifically or glyph-free names. The visually similar Reset and Reset camera arrows and the general creation star still need user comprehension checking. This is an explicit scoped disposition, not a claim that every proposed C1 remedy was implemented.

## Evidence sufficiency and limits

I inspected all nine manifest-bound PNGs: mobile initial, final-field, generated, toast, form-scroll and page-scroll; desktop top, actions and initial. The screenshots agree with the recorded rectangles and interaction outcomes. `desktop-initial.png` retains a prior scroll offset; only `desktop-top.png` is used as initial-heading evidence. The toast temporarily overlays actions and exposes its Dismiss target, matching the inherited dismissal flow.

The independent validator reports six passing focused tests, successful Vite build, and real Chromium generation without compiler mocking or CSS injection. I inspected the bound probe scripts and JSON results; their direct observations substantiate the layout findings beyond the static source assertions. The 22-file evidence inventory includes the exact built HTML/JS/CSS/worker/vendor assets. No page errors are recorded; software-rendering ReadPixels warnings are performance observations. A formal browser rerun was unnecessary for this join because the exact previous failing state is numerically, visually and interactively covered.

Controlled Chromium 151.0.7922.34 at 390x844 is sufficient for the local gate, not the user's delivered phone. Nearby widths/heights, Safari, browser chrome/safe areas, keyboard, zoom/text scaling and real assistive technology remain untested. The earlier suggestion to test nearby viewports is retained as a delivery follow-up; it was not a separately frozen VFR11 numeric acceptance gate. No comprehensive accessibility certification is made.

The pre-existing VFR-09 cancellation race, failed VFR-10 recovery, Diamond browser gates and public enablement HOLD remain unchanged. Source/CAD, written mesh/slicer, support-free fabrication and physical fit/assembly acceptance remain separate. Smooth browser success is not STL geometry proof.

## Exact verification commands

The following read-only commands were run, with project-relative paths unless marked otherwise:

```text
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR11_MOBILE_DENSITY_C2_VALIDATION.md scratch/vfr11-mobile-c2-validation/evidence.sha256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR11_MOBILE_DENSITY_C2_CRITIQUE.md
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR11_MOBILE_DENSITY_C2_CANDIDATE.sha256
# cwd: scratch/vfr11-mobile-c2-validation
shasum -a 256 -c evidence.sha256
# cwd: repository root
shasum -a 256 -c projects/laifen-wave-case/scratch/vfr11-mobile-c2-validation/build-inputs.sha256
# cwd: project root
jq '{finalField,actionStyles,focusAfterDismiss,toastHiddenAfterDismiss,resetLength,errors,failedRequests,mobile_accessibility}' scratch/vfr11-mobile-c2-validation/measurements.json
jq '{errors,failedRequests,initialHitTests,tabOrder,generated,generatedAccessibility,generatedThenEdit}' scratch/vfr11-mobile-c2-validation/supplement.json
```

An initial supplemental build-input check mistakenly ran from project cwd and failed to resolve repository-relative paths; the corrected repository-root command verified 8/8. This was a review command-location error, not candidate corruption. Repository instructions, continuity, requirements, experience, decision index, task/implementation/prior critique, C2 reports, source CSS/HTML/tests and probe scripts were read directly. PNGs were opened with `view_image`; searches used `/opt/homebrew/bin/rg`.

## Delivery decision

Advance exactly C2 `ad7c14d9f40f354c70cbaf0394b89a9a03f795ec9e4d767c55c263096f054968` to the authorized private delivery step, retaining disabled Diamond controls and all existing holds. Root should reconcile continuity with this bounded PASS, verify the served bundle against the reviewed asset chain, and check the actual Tailscale/mobile surface before claiming delivery acceptance. Icon comprehension remains an explicit post-delivery user check. Any changed candidate bytes require refreezing and affected independent gates.

The SHA-256 of this completed report is returned in the detached worker receipt; it cannot be embedded self-referentially in its own bytes.
