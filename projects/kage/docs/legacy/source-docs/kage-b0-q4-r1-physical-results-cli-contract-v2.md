# KAGE B0 Q4-R1 physical-results CLI contract — v2

Status: design handoff only; implementation not started  
Article: `p3_v3_mvp_base_q4_r1`  
Acceptance source: `kage-b0-q4-r1-physical-validation-card-v3.md`  
Scope: evaluate one completed JSON result file; no database, UI, image
analysis, CAD regeneration, template generator, or result-file mutation

## Invocation and implementation boundary

```text
uv run kage-clock b0-evaluate PATH/TO/b0-results.json
uv run kage-clock b0-evaluate PATH/TO/b0-results.json --json
```

Keep the existing `kage-clock` behavior that accepts `--json` before or after
the command. Read one UTF-8 JSON document and write only the report to stdout.

Suggested files:

- `p3_v3_mvp_base_q4_r1_physical_contract.py`: thresholds, explicit parser,
  pure evaluator, JSON payload, and text formatter;
- `kage_cli.py`: parser and dispatch only;
- add that module to `pyproject.toml`'s explicit `py-modules` list;
- `tests/test_p3_v3_mvp_base_q4_r1_physical_cli.py`: seven test groups below.

Use the standard library. Do not add a schema package. Parse JSON numeric tokens
with `parse_float=Decimal`; reject NaN/infinity and booleans in numeric fields.

## Single source of truth

Reference `p3_v3_mvp_base_q4_r1_spec.SPEC` for article namespace, nominal OD,
pin target exposure, and part/hardware counts. Add one frozen
`B0PhysicalAcceptance` value in the physical-contract module for card-only
rules. It owns card version `v3`, card SHA-256
`cb37c040fcf06f1bc807155044638f25ac359b638dd70b586bffa7b7999a046c`,
and these values:

| Name | Value | Unit |
|---|---:|---|
| `od_tolerance_mm` | `0.50` | mm |
| `od_range_max_mm` | `0.50` | mm |
| `od_resolution_max_mm` | `0.25` | mm |
| `gap_resolution_max_mm` | `0.05` | mm |
| `step_resolution_max_mm` | `0.05` | mm |
| `flatness_resolution_max_mm` | `0.10` | mm |
| `seam_gap_min_mm` | `0.05` | mm |
| `seam_gap_max_mm` | `0.30` | mm |
| `seam_step_max_mm` | `0.25` | mm |
| `flatness_max_mm` | `0.50` | mm |
| `reference_plane_feeler_max_mm` | `0.25` | mm |
| `pin_motion_max_mm` | `0.00` | mm at pin-tool resolution |
| `assembly_cycle_count` | `3` | count |
| `unconstrained_wait_min` | `60` | minutes |
| `vertical_dwell_min` | `60` | minutes |
| `vertical_down_quadrant` | `Q1` | identifier |
| `lift_height_min_mm` | `50` | mm |
| `lift_hold_min_seconds` | `3` | seconds |
| `lift_sequence` | `Q1,Q2,Q3,Q4,Q1,Q2,Q3,Q4,Q1,Q3` | identifiers |

Derive OD min/max from `SPEC.base_outer_diameter_mm +/- od_tolerance_mm`.
Derive the pin target from `SPEC.base_split_slip_engagement_mm`. Parser,
evaluator, formatter, and tests must import these values rather than restate
them.

## Input document

Top-level required fields:

```json
{
  "schema": "kage.b0.q4-r1.physical-results.v2",
  "article": "p3_v3_mvp_base_q4_r1",
  "card_version": "v3",
  "card_sha256": "cb37c040fcf06f1bc807155044638f25ac359b638dd70b586bffa7b7999a046c",
  "print": {},
  "measurement_systems": {},
  "reference_plane": {},
  "hardware_fit": {},
  "assembly_attestations": {},
  "cycles": [],
  "checkpoints": {},
  "vertical": {},
  "lift_place": {},
  "photos": {}
}
```

Unknown fields produce warnings and are ignored. A misspelled required field
is still missing. All IDs and enum values are case-sensitive.

### Print and measurement systems

`print` requires nonempty `material`, `printer`, `profile`, and ISO date, plus
finite positive `nozzle_mm` and `layer_height_mm`.

`measurement_systems` requires five named objects:

```json
{
  "od": {"name": "long caliper", "resolution_mm": 0.10, "uncertainty_mm": 0.05, "verified": true},
  "gap": {"name": "feeler set", "resolution_mm": 0.05, "uncertainty_mm": 0.025, "calibrated": true},
  "step": {"name": "feeler/indicator", "resolution_mm": 0.05, "uncertainty_mm": 0.025, "calibrated": true},
  "flatness": {"name": "straightedge/feeler", "resolution_mm": 0.10, "uncertainty_mm": 0.05, "calibrated": true},
  "pin_exposure": {"name": "digital caliper", "resolution_mm": 0.01, "uncertainty_mm": 0.01, "calibrated": true}
}
```

Every resolution is finite and greater than zero. Every uncertainty is finite
and nonnegative. OD must meet its maximum resolution and be verified;
gap/step/flatness must meet their named maximum resolutions and be calibrated.
Pin exposure must be calibrated; its exact 2.50 target is a procedure gate,
not an uncertainty-borderline gate.

`reference_plane` is exactly one of:

- certified: `{"kind":"certified","reference":"certificate or plate id"}`;
- verified: `{"kind":"verified","verification_feeler_mm":0.25,
  "passed":true,"worst_location":"text"}`.

A verified plane needs a calibrated feeler no larger than 0.25 mm. The named
`reference_plane` photo is handled separately below.

### Hardware fit

`hardware_fit.pins` contains exactly eight unique IDs `S1-R78`, `S1-R108`, ...,
`S4-R108`. Every row requires:

```json
{
  "id": "S1-R78",
  "before_mm": 2.50,
  "after_mm": 2.50,
  "steady_nonimpact_pressure": true,
  "free_dropped": false,
  "impact_used": false,
  "released": false,
  "visible_movement": false,
  "damage": false
}
```

`before_mm` must equal the exact SPEC-derived target. `after_mm-before_mm` must
be zero at the recorded pin-tool resolution. These are exact hardware/procedure
rules; do not route them through boundary rechecks.

`hardware_fit.nuts` contains exactly eight unique IDs, two per seam, with
booleans `flat=true`, `below_seat=true`, `spun=false`, and `forced=false`.
`hardware_fit.screws` contains the same eight IDs with
`hard_before_head_contact=false`, `bridge_moved_when_tight=false`,
`paper_remained_at_contact=false`, and `cross_threaded=false`.

### Required assembly attestations

```json
{
  "all_quadrants_supported_in_final_xy": true,
  "bridge_insertion_order": ["S1", "S2", "S3", "S4"],
  "s4_inserted_upward_from_below": true,
  "q4_with_s4_lowering_used": false,
  "all_eight_screws_loose_before_tightening": true,
  "tightening_order": ["S1", "S3", "S2", "S4"],
  "finger_snug_only": true,
  "forced_closure_used": false,
  "unconstrained_wait_minutes": 60,
  "direct_force_or_damage_observed": false
}
```

A missing/false/mismatched method attestation is INCOMPLETE because the card
was not followed. `forced_closure_used=true` or
`direct_force_or_damage_observed=true` is physical FAIL.
`unconstrained_wait_minutes` is a procedure duration: 60 passes, below 60 is
INCOMPLETE, and no boundary recheck applies.

### Cycles and handling

`cycles` contains exactly cycles 1, 2, and 3. Cycle 1 alone has
`initial_assembly=true`. Each row contains `s4_force` in
`free|light|firm|forced` and `damage` as a list. Force order is
`free < light < firm < forced`. Compare Cycle 2 against Cycle 1 and Cycle 3
against Cycle 2. Any increase, any `forced`, or nonempty damage is FAIL.

`vertical` requires `down_quadrant="Q1"`, timezone-aware `started_at` and
`ended_at`, `only_down_quadrant_rim_contact=true`,
`safety_tether_load_bearing=false`, and `movement_or_disengagement=false`.
Derive duration; under 60 minutes is INCOMPLETE. Procedure durations do not use
boundary rechecks.

`lift_place` requires the exact ten-item SPEC/contract sequence, finite
`height_mm>=50`, finite `hold_seconds>=3`,
`seam_click_or_disengagement=false`, and `hardware_moved=false`. A short or
wrong procedure is INCOMPLETE; observed movement/click/disengagement is FAIL.

### Checkpoint measurements and complete rechecks

Require `cycle1_free_state`, `after_vertical`, and `after_lift_place`. Each has:

```json
{
  "s4_hand_pressure_only": true,
  "forced_actions": [],
  "seam_overlap": false,
  "visible_bow": false,
  "diameters_mm": {"d0":300.0,"d45":300.0,"d90":300.0,"d135":300.0},
  "seam_gaps_mm": {
    "S1":{"inner":0.10,"middle":0.10,"outer":0.10},
    "S2":{"inner":0.10,"middle":0.10,"outer":0.10},
    "S3":{"inner":0.10,"middle":0.10,"outer":0.10},
    "S4":{"inner":0.10,"middle":0.10,"outer":0.10}
  },
  "seam_steps_mm": {
    "S1-A":0.10,"S1-B":0.10,"S2-A":0.10,"S2-B":0.10,
    "S3-A":0.10,"S3-B":0.10,"S4-A":0.10,"S4-B":0.10
  },
  "rocking": false,
  "worst_flatness_gap_mm": 0.20,
  "worst_flatness_location": "d45 outer",
  "rechecks": {}
}
```

`rechecks` permits only these family keys, each triggered by a BORDERLINE first
set:

- `od`: a complete new `d0,d45,d90,d135` object; recompute OD min/max/range;
- `seam_gaps`: all 12 new named gap readings;
- `seam_steps`: all 8 new named step readings;
- `flatness`: new `rocking`, `worst_flatness_gap_mm`, and location.

Never accept one replacement scalar or copy the other first-set values into a
partial recheck. Rechecks apply only to OD/OD range, gaps, steps, and flatness.
They do not apply to exact pin target, cycle count/force, waits/dwell, lift
height/hold/count, attestations, or any boolean observation.

### Measurement uncertainty and boundary rules

For a scalar reading `x` with uncertainty `u`, evaluate interval `[x-u,x+u]`:

- strictly inside both acceptance limits: PASS;
- wholly below the minimum or wholly above the maximum: FAIL;
- otherwise touching/crossing a limit: BORDERLINE and require that family's
  complete second set.

For a maximum-only limit `m`, PASS when `x+u < m`, FAIL when `x-u > m`, and
BORDERLINE otherwise. A complete recheck is evaluated the same way; if its
interval still touches/crosses, it remains BORDERLINE.

For four OD readings, compute observed range `r=max(D)-min(D)` and conservative
range interval `[max(0,r-2u_od), r+2u_od]`. Evaluate it against the maximum-only
range limit. An OD recheck always supplies four new diameters and recomputes
range; a typed `range_mm` input is forbidden.

Paper screens are not numeric evidence. Missing calibrated readings are
INCOMPLETE, not FAIL.

### Post-handling gap and step growth

Compare every named gap and step:

- `after_vertical - cycle1_free_state`;
- `after_lift_place - after_vertical`;
- `after_lift_place - cycle1_free_state` (cumulative).

For each delta, combined measurement uncertainty is `u_before + u_after`
(normally twice the family uncertainty). A positive delta greater than the
combined uncertainty is measurable growth and FAIL. A delta equal to the
combined uncertainty is BORDERLINE and triggers a complete recheck for that
family/checkpoint. A smaller delta is PASS/no measurable growth. Report the
largest sequential and cumulative gap/step growth with field paths.

### Named photo evidence

`photos` contains exactly these 15 keys, one view per key:

```text
parts_and_hardware
hardware_fit
reference_plane
supported_quadrants_s1_s3
s4_half_inserted
s4_fully_seated
cycle1_front
cycle1_underside
od_measurement_setup
worst_seam_measurement
worst_flatness_measurement
vertical_start_q1_down
vertical_end_q1_down
final_front
final_underside
```

Each value is exactly one object:

```json
{"kind":"local_path","value":"photos/01-parts.jpg"}
```

or

```json
{"kind":"stable_id","value":"lab-photo:2026-08-20:01"}
```

Resolve `local_path` deterministically relative to the result JSON directory;
it must name an existing regular file. Do not expand globs, follow URLs, or
search other directories. `stable_id` must be nonempty and match
`[A-Za-z0-9][A-Za-z0-9._:/-]*`; it is accepted as an externally managed
identifier without an existence claim. Missing keys, arrays, multiple values,
unknown kinds, nonexistent local files, and invalid stable IDs are INCOMPLETE.

## Exact six-check mapping

Always emit exactly the six card checks. Each input deficiency has one primary
owner so summary counts are stable:

| Check | Owns |
|---|---|
| `01_loop_od` | final-XY/S1-S4/upward-S4/no-Q4-lowering/loose-screws/finger-snug/no-forced-closure attestations; S4/overlap/bow observations; OD system/readings/range/rechecks; supported/S4/cycle1/OD photos |
| `02_seam_gap_step` | gap and step systems; all checkpoint gaps/steps/rechecks; sequential/cumulative growth; worst-seam photo |
| `03_free_state_flatness` | one-hour wait; flatness system; reference-plane qualification; all checkpoint rocking/flatness/rechecks; reference-plane and worst-flatness photos |
| `04_service_cycles` | print provenance; pin system; all pin/nut/screw fit; exact three cycles and previous-cycle force comparison; parts/hardware-fit photos |
| `05_vertical_retention` | Q1-down/contact/tether/timestamps/duration/movement; after-vertical checkpoint presence; vertical start/end photos |
| `06_lift_place` | exact sequence/count/height/hold and movement; after-lift checkpoint presence; final front/underside photos |

Physical hardware/instrument/reference failures never become an uncounted
seventh check. A schema-wide identity/type error is CLI error code 2 before
check evaluation.

## Status, output, and missing data

Statuses are `pass`, `borderline`, `fail`, and `incomplete`.

- FAIL: direct calibrated physical evidence outside limits; forced
  closure/damage; hardware rejection; force escalation; observed movement,
  rocking, overlap, bow, click, or measurable post-handling growth.
- BORDERLINE: only the defined uncertainty/boundary/growth cases awaiting a
  complete family recheck.
- INCOMPLETE: missing evidence, inadequate/unverified instrument, invalid
  reference plane, wrong/missing attestation or procedure, short duration,
  wrong cardinality, or photo-evidence failure.

For well-formed input precedence is `fail > incomplete > borderline > pass`.
A known failure stays FAIL even if another photo is missing. Malformed JSON,
wrong schema/article/card/hash, unreadable input, invalid numeric/type, or
duplicate IDs is a CLI/schema error, not an article verdict.

JSON mode emits one object:

```json
{
  "schema": "kage.b0.q4-r1.physical-evaluation.v2",
  "article": "p3_v3_mvp_base_q4_r1",
  "card_version": "v3",
  "card_sha256": "cb37c040fcf06f1bc807155044638f25ac359b638dd70b586bffa7b7999a046c",
  "input": "/absolute/path/b0-results.json",
  "overall_status": "pass",
  "exit_code": 0,
  "summary": {"pass":6,"borderline":0,"fail":0,"incomplete":0},
  "measurement_systems": {},
  "derived": {
    "cycle1_free_state": {
      "od_values_mm": [300.0,300.0,300.0,300.0],
      "od_range_mm": 0.0,
      "od_range_interval_mm": [0.0,0.1],
      "worst_gap_mm": 0.10,
      "worst_step_mm": 0.10,
      "worst_flatness_mm": 0.20
    },
    "post_handling_growth": {
      "worst_gap_delta_mm": 0.0,
      "worst_gap_path": "...",
      "worst_step_delta_mm": 0.0,
      "worst_step_path": "..."
    }
  },
  "checks": [
    {"id":"01_loop_od","status":"pass","reasons":[]}
  ],
  "missing_fields": [],
  "warnings": []
}
```

Every reason is a stable object with `code`, `path`, `expected`, and `actual`.
JSON stdout has no prose prefix. Parse errors go to stderr.

Text mode is deterministic and uncolored:

```text
KAGE B0 Q4-R1: PASS
01 loop + OD             PASS  D=...; range=...; uncertainty=...
02 seam gap + step       PASS  gaps=...; step=...; growth=...
03 free-state flatness   PASS  worst=...; plane=verified
04 three service cycles  PASS  pins=8; S4=light/light/light
05 vertical retention    PASS  Q1 down; 60 min; post-checks pass
06 ten lift/place cycles PASS  sequence/count pass; post-checks pass
Overall: PASS — evaluator result; independent acceptance still required.
```

Non-pass output adds one indented line per reason. The CLI evaluates; it never
self-approves the article.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | complete PASS |
| `1` | physical FAIL |
| `2` | CLI/unreadable/malformed/schema/type/value error |
| `3` | BORDERLINE with no FAIL or INCOMPLETE |
| `4` | INCOMPLETE with no known FAIL |

FAIL plus missing/borderline evidence exits 1 while retaining other statuses
in detail.

## Seven meaningful test groups

1. **Installed uv CLI, six-check mapping, and output parity.** A complete pass
   fixture returns code 0 through `uv run`; text and JSON agree; exactly six
   mapped checks exist and every hardware/instrument/reference/photo field has
   the owner specified above.
2. **OD uncertainty, complete rechecks, and negatives.** Test intervals wholly
   inside, crossing/touching 299.50/300.50, and wholly outside. Test range with
   the conservative `r +/-2u` interval. A borderline OD accepts only four new
   diameters, recomputes range, and rejects a partial/scalar recheck. Outside
   and range-over-limit fixtures fail.
3. **Gap/step/flatness uncertainty, family rechecks, and boundaries.** Exercise
   wholly inside/crossing/outside intervals at 0.05/0.30 gap, 0.25 step, and
   0.50 flatness. Require full 12-gap, 8-step, or complete-flatness rechecks.
   Prove paper-only data incomplete. Prove no recheck is accepted for pin or
   procedure-duration boundaries.
4. **Hardware and assembly sensitivity.** Exact 2.50 before/after passes;
   mutate pin target/motion/flags, nut fit, and each false-preload flag to FAIL.
   Missing/false method attestations are INCOMPLETE, while forced closure or
   damage is FAIL. Assert S1-S3/S4-upward and one-hour-wait ownership.
5. **Cycles, handling, and post-handling growth.** Prove comparison is C2 vs C1
   and C3 vs C2. Exact vertical/lift procedure passes; method deviations are
   INCOMPLETE and observed movement FAIL. Test sequential and cumulative named
   gap/step deltas below/equal/above combined uncertainty, including full
   recheck at equality.
6. **Missing/malformed/photo evidence.** Omit required fields/cardinalities and
   each named photo in turn for code 4 with exact paths. Test existing relative
   local file, missing file, valid stable ID, invalid ID, array/multiple value,
   wrong schema/card/hash, NaN, boolean-number, and duplicate ID behavior.
7. **Single-source thresholds, precedence, and deterministic reporting.** Tests
   import SPEC/contract thresholds and assert reported intervals/reasons. FAIL
   plus missing photo exits 1; INCOMPLETE plus BORDERLINE exits 4; exact same
   input produces byte-stable JSON key structure and text ordering.

Do not split these into more test groups or add persistence, interactive input,
photo recognition, CAD validation, or UI work.
