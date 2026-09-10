# P23 R1 independent geometry and requirement validation

Date: `2026-08-29`  
Owner: `P23-VALIDATE-01`  
Disposition: **SUPERSEDED — see repair-cycle-1 focused revalidation below**  
Scope: evidence-only first-design CAD; not print, strength, torque, tolerance, or physical authority.

## Candidate fingerprint

The supplied candidate matched exactly before regeneration:

```text
f78d26ab0ee09727b07b13616d1b3109a26106f8000f83b5d4a439bdbe48249a  DESIGN.md
9923d4d855a08a0daedc8c5304b1fb965b3ded468b00291f0bcdebf5459ceb72  p23_r1_mirrored_screw_clamps.py
5740aa29723174446b5fca7a11db723fb1ee7f18d2009684c2536c5c1ae3567d  test_p23_r1_mirrored_screw_clamps.py
aaa1b1bc8e1bb285190d1f5db7bd207a6a40669acad0363a24a882a952a25349  p23_r1_open.step
39647c5a1b49719098833a629a83c0de4a9638580caeec1a8698a078fbd54bda  p23_r1_clamped.step
```

Explicit regeneration kept DESIGN, source, and test hashes unchanged, but did
not reproduce the original STEP byte hashes. The current regenerated files are:

```text
6273bb1782cce4a145023f52f41cef7c1102892c4b271f9b8ec9067f7fd96e68  p23_r1_open.step
f00a2a0752e50d9672825b03a55e528a6a7f4ea61129d14f9b17fd508fc5eb38  p23_r1_clamped.step
```

The exact supplied artifact-byte fingerprint is therefore not reproducible in
this run. The remaining checks below apply to the current STEP files regenerated
from the verified source hash.

## Commands and direct results

All commands ran from the repository root through the root `uv` environment.

```text
uv run pytest projects/xt60-bend-jig/tests/test_p23_r1_mirrored_screw_clamps.py -q
....... [100%]  (7 passed; exit 0)

uv run python <cad-skill>/scripts/gen \
  projects/xt60-bend-jig/cad/p23_r1_mirrored_screw_clamps/p23_r1_open.step.py \
  projects/xt60-bend-jig/cad/p23_r1_mirrored_screw_clamps/p23_r1_clamped.step.py \
  --write --json
Both explicit targets built successfully; exit 0.

uv run python <cad-skill>/scripts/artifact <OPEN-or-CLAMPED.step> --force
Both imported-STEP review packages rebuilt successfully from the current STEP hashes.

uv run python <cad-skill>/scripts/inspect refs <STEP> \
  --facts --planes --positioning --format text
OPEN:    faces=825, edges=2291, 8 major plane groups.
CLAMPED: faces=825, edges=2291, 8 major plane groups.

uv run python <cad-skill>/scripts/inspect validate <STEP> --format text
OPEN:    22 occurrences, PASS — all solids valid, closed, positive volume.
CLAMPED: 22 occurrences, PASS — all solids valid, closed, positive volume.
```

The Viewer/inspect package reports a conservative transformed AABB for the
rotated CLAMPED outer plates. Direct build123d import of each written STEP was
therefore used for source/export parity. It found `22` matching leaf occurrences;
per-occurrence bounding-box size/center and volume matched source within
`1e-7 mm` / `1e-6 mm^3` apart from STEP label punctuation normalization.

## Requirement coverage

### Passed

- Purchased rods remain exactly `OD4.00 x 50.00 mm`: three rods in OPEN and
  three in CLAMPED; their solid bounds are `50 x 4 x 4 mm`.
- All six legacy caps are absent: `capCount=0` in both states.
- Two X-mirrored modules are present, with yoke centers `X=-24.3/+24.3 mm`
  and screw axes `X=-30.3/+30.3 mm`.
- Six labeled blind captures are present: Green, Blue, and Orange on each side.
  Rod-end insertion is `3.70 mm` into a `4.00 mm` socket, leaving the specified
  `0.30 mm` blind-end clearance; socket ID is `4.15 mm` around OD4 rods.
- Left and right share screw pitch `2.00 mm` and Orange travel
  `12.150910844187 mm`, equal to `6.075455422093` turns per side.
- P23 rod centers delegate exactly to the inherited P20 path authority at OPEN
  and CLAMPED; measured source deltas are `0.0 mm` for Blue, Orange, and Green.
- Orange travel vector is `(-2.835630844, -11.815406555) mm` in world YZ.
- Written OPEN and CLAMPED STEP occurrences are real, closed, valid,
  positive-volume solids.
- P23 modules do not intersect the purchased rods or outer plates in the two
  endpoint states at the test tolerance `1e-7 mm^3`.

### Failed blockers

1. **Fixed yoke is disconnected.** Each left/right `fixed_side_yoke` is two
   separate solids rather than one connected structural part. The nut/screw
   support group is not joined to the lower rod-capture frame.
2. **Knob penetrates the fixed yoke/nut block.** Written-STEP intersection
   volumes are:
   - OPEN: `530.060651404 mm^3` on both left and right.
   - CLAMPED: `374.901450789 mm^3` left and `374.901479379 mm^3` right.
   This is visible in the refreshed isometric snapshots and prevents a usable
   knob/nut relationship.
3. **Blue follower and Orange shoe collide at CLAMPED.** Intersection is
   `0.390453177 mm^3` on each side. This violates the explicit no-unintended-
   overlap preview gate and can create the same binding/skew behaviour the new
   concept is intended to remove.
4. **Artifact-byte fingerprint drift.** Regeneration from unchanged source and
   test hashes changed both STEP SHA-256 values. Geometry parity was checked,
   but the supplied exact artifact fingerprint cannot be approved as reproduced.

The existing seven focused tests do not catch blockers 1–3. In particular,
they check each module leaf against rods and outer plates but do not check yoke
connectivity or module-internal pairwise collisions.

## Snapshot review

Fresh snapshots were generated only after forcing the imported-STEP packages
to rebuild from the current STEP hashes:

```text
4f2e21a1b0e66ccb200b76f4852c68e9563e75f16bd226d47109976133a37fb3  /private/tmp/p23-r1-validator/open_iso_refreshed_20260829T153206Z.png
a125025f33a95af3a117b3c6faf604a330f83d0db0c6651287b66eef5acd2a77  /private/tmp/p23-r1-validator/open_front_transparent_refreshed_20260829T153206Z.png
457f48f777a103048867bc0b3ff9ca30a9b0f16a15c76d340e09ac9624e5d406  /private/tmp/p23-r1-validator/clamped_iso_refreshed_20260829T153206Z.png
04b8de7cbc549270573bf0845226f54aea69b03ecc29f5748f11f8dbe482eaa6  /private/tmp/p23-r1-validator/clamped_front_transparent_refreshed_20260829T153206Z.png
```

The first snapshot attempt exposed stale same-stem imported-STEP review
packages. Those images were rejected; only the refreshed packet above supports
this report.

## Unresolved risks and next action

This validation does not address thread printability, strength, torque,
back-drive resistance, wear, synchronized two-hand use, assembly order,
manufacturing tolerance, or physical retention.

Smallest repair loop:

1. connect each fixed yoke into one solid;
2. move the knob clear of the nut block through the entire `0..1` travel;
3. separate Blue follower and Orange shoe at CLAMPED with a declared clearance;
4. add focused regressions for yoke connectivity and module-internal collision;
5. regenerate a newly fingerprinted candidate and rerun this validator.

Do not advance this candidate to print preparation or physical acceptance.

---

## Repair-cycle-1 focused revalidation — 2026-08-29

Owner: `P23-VALIDATE-01`  
Final disposition: **PASS — PRIOR P23 GEOMETRY BLOCKERS CLOSED FOR EVIDENCE-ONLY INTENT PREVIEW**  
Authority boundary: this is still not print, strength, torque, tolerance, or
physical acceptance authority.

### Verified repaired-candidate fingerprint

The supplied repair-cycle-1 hashes matched the files before this revalidation:

```text
5f92bda26ef931f5a614c02c5b72756b4b39987878f7a1b5db19e49160607a52  src/xt60_bend_jig/p23_r1_mirrored_screw_clamps.py
22596c141bbf2cf7614b9ae8948c68064613e2c1f5935899cfb43104fb4fb7f3  tests/test_p23_r1_mirrored_screw_clamps.py
69c20491b6ee8aac79587c325b418807e9f05afdd2288580da947a1c4a5f7a50  cad/p23_r1_mirrored_screw_clamps/p23_r1_open.step
a4a3133d4ae2bda76b6f67f3ee11e2d648ee0c6c58e84f065b2f8b1cb0933978  cad/p23_r1_mirrored_screw_clamps/p23_r1_clamped.step
```

No STEP regeneration was needed or performed in this focused revalidation.

### Commands and results

All repository commands ran from the repository root through the root `uv`
environment.

```text
uv run pytest projects/xt60-bend-jig/tests/test_p23_r1_mirrored_screw_clamps.py -q
........... [100%]  (11 passed; exit 0)

uv run python <cad-skill>/scripts/inspect validate \
  projects/xt60-bend-jig/cad/p23_r1_mirrored_screw_clamps/p23_r1_open.step \
  --format text
OPEN: 20 occurrences; PASS — every occurrence is valid, closed, and has positive volume.

uv run python <cad-skill>/scripts/inspect validate \
  projects/xt60-bend-jig/cad/p23_r1_mirrored_screw_clamps/p23_r1_clamped.step \
  --format text
CLAMPED: 20 occurrences; PASS — every occurrence is valid, closed, and has positive volume.

uv run python - <<'PY'
# Independent source-solid and imported-STEP probes for connectivity,
# pairwise intersections, clearances, retention dimensions, census,
# inherited path parity, and purchased-rod bounds.
PY
Exit 0; focused measurements are recorded below.
```

### Prior-blocker closure and requirement coverage

| Focused gate | Independent result |
|---|---|
| Fixed-yoke connectedness | PASS: left and right yokes are each exactly one connected solid. |
| P23-only unintended collisions | PASS: all pairwise intersection volumes among the eight P23 module parts are `0 mm^3` in both OPEN and CLAMPED, in source solids and independently imported written STEP solids. |
| Screw-with-knob nut clearance | PASS: clearance decreases monotonically over normalized travel `u=0, 0.25, 0.5, 0.75, 1` as `13.150910844187, 10.113183133140, 7.075455422094, 4.037727711047, 1.000000000000 mm`; the endpoint minimum is the declared `1.0 mm`. |
| Rectangular anti-rotation shoe | PASS: each Orange shoe is one real solid with the declared `9.0 x 6.0 mm` keyed rectangular section. |
| Captive T-head pull-back relation | PASS at geometry level: real head `D6.0 x 2.0 mm`, cavity `D6.5 x 2.5 mm`, neck `D3.0 mm`, and neck slot `D3.5 mm`; head-to-slot diametral capture margin is `2.5 mm`. |
| X-retention flanges/lips | PASS at geometry level: lip `1.2 mm`, flange `3.2 mm`, cavity `3.6 mm`, giving declared `0.2 mm` clearance per side. |
| Purchased rods and caps | PASS: three written-STEP rods in each state, each bounded `50 x 4 x 4 mm`; `rod OD=4.0 mm`, `rod length=50.0 mm`, and `capCount=0`. |
| Inherited motion authority | PASS: Blue, Orange, and Green rod-center deltas against the inherited P20 path authority are exactly `0.0 mm` at both OPEN and CLAMPED. |
| Mirrored modules and captures | PASS: `moduleCount=2`, `captureCount=6`, and both states contain `20` leaf occurrences. |
| Real written solids | PASS: both STEP files pass `inspect validate`; Orange shoes and screw-with-knob bodies are each one solid on both sides and in both endpoint states. |

The repaired source therefore closes the earlier disconnected-yoke,
knob/yoke penetration, and Blue/Orange collision blockers. The new focused
tests also directly cover these failure modes.

### Fresh snapshot review

Fresh snapshots were generated from the exact verified OPEN and CLAMPED STEP
files and inspected at original image detail:

```text
4f2e21a1b0e66ccb200b76f4852c68e9563e75f16bd226d47109976133a37fb3  /private/tmp/p23-r1-revalidation-cycle1/open_iso_20260829T155823Z.png
a125025f33a95af3a117b3c6faf604a330f83d0db0c6651287b66eef5acd2a77  /private/tmp/p23-r1-revalidation-cycle1/open_front_transparent_20260829T155823Z.png
457f48f777a103048867bc0b3ff9ca30a9b0f16a15c76d340e09ac9624e5d406  /private/tmp/p23-r1-revalidation-cycle1/clamped_iso_20260829T155823Z.png
04b8de7cbc549270573bf0845226f54aea69b03ecc29f5748f11f8dbe482eaa6  /private/tmp/p23-r1-revalidation-cycle1/clamped_front_transparent_20260829T155823Z.png
```

Visual review found two symmetric modules in both states, no recurrence of the
large knob/yoke penetration, no obvious Blue/Orange endpoint collision, no
floating P23 part, and no new visible left/right asymmetry. The rectangular
Orange shoes, top screw/nut structures, X-retaining arrangements, and three
retained rods are visible. Deterministic solid checks remain the authority for
the less visually legible transparent views.

### Separately reported inherited overlap

The inherited XT60-versus-Blue overlap measures:

```text
OPEN:     186.980487360803 mm^3
CLAMPED:    0.000000000000 mm^3
```

Per the focused revalidation contract, this is reported separately and is not
classified as a new P23 mirrored-module blocker. It remains an inherited
assembly/interface issue requiring its own disposition before any claim of
full-system or print readiness.

### Remaining risks and final disposition

The focused P23 geometry candidate passes the repair-cycle-1 intent-preview
gates. Remaining unvalidated matters include thread printability, tolerance and
fit, strength, screw torque/back-drive resistance, wear, assembly order,
two-handed operation, and physical retention. The inherited OPEN XT60/Blue
overlap also remains unresolved outside this focused P23 module gate.

**Final disposition: PASS for evidence-only first-design intent preview. Do not
treat this result as print authority or physical acceptance.**
