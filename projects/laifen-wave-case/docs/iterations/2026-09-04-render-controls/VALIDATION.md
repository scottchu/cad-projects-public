# RCV-04 independent render-controls validation

- Owner / role: `/root/render_controls_validate_b`, independent validator
- Date: 2026-09-04
- Verdict: **PASS with one P3 mobile presentation limitation**
- Frozen design fingerprint: `2ac420ce1eb43f6adb12d39d41416a24167a7ef7a3990a490107f8caed5a80e4`
- Candidate manifest fingerprint: `8e6ac223dd9e8ff5539120bfb0d8ffcc20dd7d38f801bb0e08a945a5520c3a60`

## Frozen candidate and deterministic checks

The candidate manifest itself matched the assigned fingerprint. All eight
listed paths passed SHA-256 verification, including the four accepted STEP
artifacts. The focused suite passed:

```text
/usr/bin/shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-04-render-controls/candidate-files.sha256
  all eight files: OK

uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_preview_parameters.py -q
  7 passed
```

A separate Node effects mock imported the committed self-contained sidecar and
confirmed 52 rows, zero effect calls at defaults, common 120% radial scaling
targeting both body and cap, a one-turn cap transform of +360 degrees and
+2 mm, and cap-only color/opacity styling. The exact mock output is frozen in
`scratch/render-controls-validation/node-effects.json`.

## Exact private delivery route

The reviewed page was:

```text
https://mac-mini.duckbill-ionian.ts.net:8449/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case?file=cad/container_generator_v1/closed.step.py
```

Read-only endpoint evidence:

- exact page: HTTP 200;
- `GET /__cad/artifact` with the absolute project `dir` and exact source `file`:
  HTTP 200, `state == "ready"`;
- direct served `closed.params.js`: HTTP 200 and SHA-256
  `20abaef22b3dbe6c381aa528f5ace3d7b253ed99dcda352d70a5520dd2aa1076`,
  byte-identical to the committed sidecar;
- generated descriptor: `sourceKind == "python"`, `sourcePath ==
  "closed.step.py"`, `paramsPath == "closed.params.js"`, accepted closed STEP
  hash, two occurrences, and two shapes;
- descriptor occurrence `o1.1` is the authored body name and `o1.2` is the
  authored cap name required by the two sidecar features.

The exact machine-readable summary is
`scratch/render-controls-validation/endpoint-summary.json`.

## Mobile and interaction evidence

At an explicit 390 x 844 Chrome viewport, the Parameters tab visibly showed
the `00 VISUAL PREVIEW ONLY` disclosure, all ten control labels and sliders,
the unchanged read-only snapshot, and no error state. The disclosure explicitly
says the display mesh changes while CAD and STEP remain unchanged.

The validator changed common radial scale from 100 to 125 and AX reported
`125 %`. The emitted screenshot changed from SHA-256
`f1246422e37cada02225cf58d0ee319b5308206ce0955bb6c9358f9fda9ab1a9` to
`483508605bb7f326cfb8589296b2575d7e23bc7ecba2d18674e7afb09a0df9fe`.

The root agent completed the remaining bounded actions on the same exact live
artifact and reported them for this independent evidence review: 120% radial
scale visibly widened both parts; 1.00 cap turn plus 0.4 cap opacity visibly
opened a 2 mm seam and made the cap translucent; Reset restored all scale
fields to 100, turn/lift to 0, opacity to 1, source colors, and the accepted
closed pose. Native Tree controls independently expose Hide for body and cap.
The normal viewport and CUA kernel were restored afterward.

The attributed and independent UI observations are frozen in
`scratch/render-controls-validation/ui-observations.md`.

## Finding and acceptance boundary

### P3 — mobile numeric boxes clip at 390 px

At 390 x 844, the STEP sheet occupies most of the viewport and clips the
right-hand numeric value boxes horizontally. The labels and sliders remain
visible and usable, the disclosure remains visible, and the exact-value fields
are accessible at a normal viewport. This is a minor responsive presentation
limitation, not a render-control correctness or reset failure, so it does not
block this candidate.

This PASS covers only the frozen Viewer-time effects and the private delivery
surface. CAD/source and written STEP acceptance remain inherited and
byte-identical. These display deformations do not establish fit, wall
thickness, thread clearance, collision, printability, slicer, or physical
acceptance. No printer action was performed.
