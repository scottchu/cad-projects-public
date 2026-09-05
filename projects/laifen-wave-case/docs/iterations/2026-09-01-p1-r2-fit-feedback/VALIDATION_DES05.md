# VAL-05 independent numeric and browser validation

Owner `/root/preview_validate`; 2026-09-01; independent of IMP-05 and CRI-05. **PASS for DES-05 numeric recovery and the prescribed DOM interactions; remaining medium visual finding V05-01 requires review disposition before claiming complete presentation acceptance.**

Candidate `inputs/des05-candidate.sha256`, fingerprint `f0fe32796fcfae64591565b2f48983325b2c7d407e6152cf2272c3e9536eb788`; all 19 entries matched before and after validation. No source, tests, configuration, requirements, coupon, runtime-service or printer changes.

## Results and coverage

- Existing Node suite: 9/9 pass, including all DES-04 cases and the new extreme-D sequence.
- Actual Chrome DOM: 22 states at each of true content widths360/736 and light/dark themes, 88 captured states total; harness assertions returned no failures. The same initialized page performs default D29 → D1.7e308 → D29. Extreme D displays the existing error and empties section/state/gaps/targets/dimensions; zero SVG children and no nonfinite output remain. Restoring only D29 restores finite geometry and readouts. VAL-04-F01 is resolved on this fingerprint.
- Default dimensions C213, cap81, outer-end reference219 and lower/upper radial gaps0.5/1 remain unchanged. Actual ID-span screen coordinates divided by actual scale remain30/31 under D29/30/31 and L140/208/400. D30 warns only lower contact; D31 warns both; restoring D29 clears warnings.
- Decimal slack0.1/5.1 at q0/.5/1 renders finite invariant L208/D29 envelopes. Gaps are respectively0/0.1,0.05/0.05,0.1/0 and0/5.1,2.55/2.55,5.1/0. Low-slack warning appears only for0.1. Zero slack retains both-end contact. Blank L, L1e308 and C137 clear all five regions and recover correctly.
- Actual SVG exterior leaders, horizontal endpoints and text anchors remain beyond x17.9 at both widths and changed L scales; minimum observed margin4px. External-stop endpoints also remain outside. Native bottom/center presets update state; native ArrowRight changes q0.50→0.51 at all four layouts. No page overflow; SVG text bounds remain inside the viewport with12px text.
- Four screenshots were produced and visually inspected. Controls wrap and Traditional Chinese text remains visible in both themes. The visual finding below prevents an unconditional whole-preview presentation pass.

## V05-01 — medium, upper-ID annotation intersects geometry

The default `上段參考 ID 31` label occupies SVG y52..67. The upper-floor reference is at y59.2054794521 and the device upper edge at y63.5433789954, both through that label's vertical extent. At360, label x97.0109..176.5891 also intersects the central cavity; at736 it is x239.8909..319.4691. All four screenshots visibly show the upper cavity edge crossing the label. This is inherited placement, not introduced by the DES-05 numeric guard. It does not invalidate the corrected arithmetic but violates the no-label/mark-overlap presentation target.

Smallest correction: move only the upper-ID annotation/dimension stack or reserve drawing space above the cavity, maintaining the numeric geometry and fixed bores. A separate owner must make any correction; validator made no source edits. Alternatively the formal reviewer must explicitly disposition this finding rather than silently claiming visual acceptance.

## Reproduction, provenance and evidence

Commands ran from repository root with shell login disabled:

```text
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/des05-candidate.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/des05-candidate.sha256
node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs
uv run /Users/scottchu/.codex/plugins/cache/openai-bundled/visualize/1.0.27/skills/visualize/scripts/render.py /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/preview/measurement-gate.html /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/width-des05/wrapped.html
node projects/laifen-wave-case/scratch/width-des05/check.mjs
```

The renderer's unchanged iframe `srcdoc` was extracted with root `uv run python`/`html.parser` into `flat.html`, providing exact360/736 content widths without outer-wrapper gutters. Installed visualize skill was consulted during VAL-04 and its renderer reused. Initial browser attempt captured DOM but `fromSurface:false` returned `Unable to capture screenshot`. One allowed harness repair selected Chrome software rendering `--use-angle=swiftshader`, bounded every CDP call to12 seconds, and used `Page.bringToFront` plus `fromSurface:true`. The repaired run exited0 and produced all four screenshots. DOM evidence is persisted before screenshot calls. No EMFILE occurred; task-owned Chrome/Node process checks returned zero matches afterward.

Evidence under `scratch/width-des05/` is reproducible scratch, not release content:

| File | SHA-256 |
|---|---|
| dom-evidence.json | d168d867ae7760f9bad0ab703d50906521f338a5f424d9e148739a1ff8dc9d45 |
| width-360-light.png | 4983e0296045aa27202848968a67f1ef0e69418ec3f84f6540f23d497605fc07 |
| width-360-dark.png | 35195d4f0db339b4a8eda34905f7d6ce304de048921398c20fd9d2b0ea775afb |
| width-736-light.png | 351c0592fcbd7c11969cc5718be1353a13e725aebf172ddf34b9880c02ccec16 |
| width-736-dark.png | 40606d1f67db44b7546d904c51e85cd9272a34b39fd5d1c4f2b7faea82152a87 |

`result.json` records four runs,88 states, zero assertion failures. `check.mjs` preserves the exact real-browser actions and geometric assertions. Its automated text checks cover viewport clipping, not text-versus-mark collisions; V05-01 comes from screenshot inspection plus captured text bounds.

Changed paths: this receipt and task-owned `scratch/width-des05/` only. Requirements REQ-03/12 and DES-03/04/05 arithmetic/interaction evidence pass within preview scope. Remaining risk is V05-01 presentation overlap plus all previously pending real measurements, retention, CAD/export/slicer and physical fit gates. No CAD, artifact/slicer or physical acceptance is conferred. Next: route this exact candidate and V05-01 to the distinct formal reviewer or bounded layout-correction owner.


## Focused V05-01 repair rerun — PASS

Same independent owner `/root/preview_validate`. Repair candidate `inputs/des05-repair-candidate.sha256`, fingerprint `9f1fdb44f7b350f7ca903c37ca2383ba195dd2f7235bbe69d2b1596f86ae4f61`; all19 entries verified before and after. Exact source comparison against `inputs/des05-pre-repair-source.html` confirmed one replacement only: upper-ID text x=cx/y64/center anchor became x=label/y40/default start anchor. The upper-ID dimension span remains y48; computation, geometry, tests and other labels are unchanged. The original f0fe3279 numeric/88-state PASS above remains applicable and was not rerun.

`node projects/laifen-wave-case/scratch/width-des05/repair-check.mjs` exited0. Four actual360/736 light/dark screenshots were captured and visually reviewed: `repair-360-light.png`, `repair-360-dark.png`, `repair-736-light.png`, `repair-736-dark.png`. `repair-dom.json` records upper-label bounds x197.8594..277.4375 at360 and x340.7393..420.3175 at736, y28..43 in every case. The label has zero bounding-box intersections with every other SVG path, rectangle and text, and stays inside the viewport. V05-01 is resolved on this repair candidate; presentation evidence passes within the prescribed scope.

The current renderer produced `repair-wrapped.html`; its unchanged srcdoc was extracted into `repair-flat.html` using root uv Python. The first launcher setup still pointed to the previous scratch profile port and failed before browser validation; that scratch path was corrected before the single completed four-layout run. No candidate repair or numeric-test rerun occurred. Owned Chrome was terminated by harness cleanup. Only this appended receipt and task scratch changed. No CAD, export/slicer or physical acceptance follows. Next action: formal independent-review join on the repair fingerprint, retaining all prior measurement and physical gaps.
