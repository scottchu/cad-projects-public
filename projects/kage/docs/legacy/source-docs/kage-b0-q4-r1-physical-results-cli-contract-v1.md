# KAGE B0 Q4-R1 physical-results CLI contract — v1

Status: design handoff only; implementation not started  
Article: `p3_v3_mvp_base_q4_r1`  
Acceptance source: `kage-b0-q4-r1-physical-validation-card-v3.md`  
Scope: evaluate one completed JSON result file; no database, UI, image analysis,
CAD regeneration, or result-file mutation

## Invocation

Extend the installed `kage-clock` console script with one subcommand:

```text
uv run kage-clock b0-evaluate PATH/TO/b0-results.json
uv run kage-clock b0-evaluate PATH/TO/b0-results.json --json
```

Keep the existing behavior that permits `--json` before or after the command.
Text is the default. The evaluator reads one local UTF-8 JSON file and writes
only its report to stdout. It does not modify the input or create an artifact.

Suggested implementation boundary:

- `p3_v3_mvp_base_q4_r1_physical_contract.py`: frozen thresholds, schema
  parsing, pure evaluation, JSON payload, and text formatter;
- `kage_cli.py`: parser/dispatch only;
- add the module to the explicit `pyproject.toml` `py-modules` list;
- `tests/test_p3_v3_mvp_base_q4_r1_physical_cli.py`: focused CLI tests.

Do not add a JSON-schema dependency. Validate with small explicit Python
functions and return field paths in every diagnostic.

## One threshold source

Geometry-derived values must reference `p3_v3_mvp_base_q4_r1_spec.SPEC`:

- article namespace;
- nominal OD: `SPEC.base_outer_diameter_mm`;
- pin exposure target: `SPEC.base_split_slip_engagement_mm`;
- counts: quadrants, bridges, screws, nuts, dowels.

Add one frozen `B0PhysicalAcceptance` value in the physical-contract module for
card-only limits. It also owns card version `v3` and card SHA-256
`cb37c040fcf06f1bc807155044638f25ac359b638dd70b586bffa7b7999a046c`:

| Name | Value | Unit |
|---|---:|---|
| `od_tolerance_mm` | `0.50` | mm |
| `od_range_max_mm` | `0.50` | mm |
| `od_resolution_max_mm` | `0.25` | mm |
| `seam_gap_min_mm` | `0.05` | mm |
| `seam_gap_max_mm` | `0.30` | mm |
| `seam_step_max_mm` | `0.25` | mm |
| `flatness_max_mm` | `0.50` | mm |
| `reference_plane_feeler_max_mm` | `0.25` | mm |
| `pin_motion_max_mm` | `0.00` | mm at the recorded tool resolution |
| `assembly_cycle_count` | `3` | count |
| `vertical_dwell_min` | `60` | minutes |
| `vertical_down_quadrant` | `Q1` | identifier |
| `lift_place_count` | `10` | count |
| `lift_height_min_mm` | `50` | mm |
| `lift_hold_min_seconds` | `3` | seconds |

Derive OD min/max from nominal plus/minus tolerance. Do not duplicate numeric
limits in parser, evaluator, formatter, and tests. Tests import the same frozen
contract, then probe immediately inside, on, and outside its boundaries.

## Input JSON

Top-level schema is `kage.b0.q4-r1.physical-results.v1`. All numeric values are
finite JSON numbers; booleans are not accepted as numbers. Enum strings are
lowercase exactly as shown. Unknown fields produce warnings but are otherwise
ignored; a misspelled required field is still missing.

Parse numeric tokens with standard-library `json.loads(..., parse_float=Decimal)`
so exact boundary values are not changed by binary floating-point rounding.

```json
{
  "schema": "kage.b0.q4-r1.physical-results.v1",
  "article": "p3_v3_mvp_base_q4_r1",
  "card_version": "v3",
  "card_sha256": "cb37c040fcf06f1bc807155044638f25ac359b638dd70b586bffa7b7999a046c",
  "print": {
    "material": "PETG",
    "printer": "Bambu Lab U1",
    "nozzle_mm": 0.4,
    "layer_height_mm": 0.2,
    "profile": "profile name",
    "date": "2026-08-20"
  },
  "instruments": {
    "od": {"name": "long caliper", "resolution_mm": 0.1, "verified": true},
    "feeler": {"name": "feeler set", "calibrated": true},
    "pin_exposure": {"name": "digital caliper", "resolution_mm": 0.01, "calibrated": true},
    "reference_plane": {
      "kind": "verified",
      "verification_feeler_mm": 0.25,
      "passed": true,
      "worst_location": "45deg center",
      "photo": "photos/reference-plane.jpg"
    }
  },
  "hardware_fit": {
    "pins": [
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
    ],
    "nuts": [
      {"id": "S1-A", "flat": true, "below_seat": true, "spun": false, "forced": false}
    ],
    "screws": [
      {
        "id": "S1-A",
        "hard_before_head_contact": false,
        "bridge_moved_when_tight": false,
        "paper_remained_at_contact": false,
        "cross_threaded": false
      }
    ]
  },
  "cycles": [
    {"cycle": 1, "initial_assembly": true, "s4_force": "light", "damage": []},
    {"cycle": 2, "initial_assembly": false, "s4_force": "light", "damage": []},
    {"cycle": 3, "initial_assembly": false, "s4_force": "light", "damage": []}
  ],
  "checkpoints": {
    "cycle1_free_state": {},
    "after_vertical": {},
    "after_lift_place": {}
  },
  "vertical": {
    "down_quadrant": "Q1",
    "started_at": "2026-08-20T14:00:00-04:00",
    "ended_at": "2026-08-20T15:00:00-04:00",
    "only_down_quadrant_rim_contact": true,
    "safety_tether_load_bearing": false,
    "movement_or_disengagement": false
  },
  "lift_place": {
    "sequence": ["Q1", "Q2", "Q3", "Q4", "Q1", "Q2", "Q3", "Q4", "Q1", "Q3"],
    "height_mm": 50,
    "hold_seconds": 3,
    "seam_click_or_disengagement": false,
    "hardware_moved": false
  },
  "photos": {
    "parts_hardware_fit_plane": "photos/01.jpg",
    "supported_s1_s3": "photos/02.jpg",
    "s4_half_and_seated": ["photos/03a.jpg", "photos/03b.jpg"],
    "cycle1_front_under": ["photos/04a.jpg", "photos/04b.jpg"],
    "measurement_worst_cases": ["photos/05a.jpg", "photos/05b.jpg"],
    "vertical_start_end": ["photos/06a.jpg", "photos/06b.jpg"],
    "final_front_under": ["photos/07a.jpg", "photos/07b.jpg"]
  },
  "boundary_rechecks": {}
}
```

The example abbreviates repeated arrays. Required cardinalities are:

- pins: exactly 8 unique IDs `S1-R78` through `S4-R108`;
- nuts and screws: exactly 8 each, two unique IDs per seam;
- cycles: exactly 1, 2, 3; cycle 1 alone has `initial_assembly=true`;
- checkpoints: exactly the three named checkpoints;
- all seven photo groups present and nonempty.

For `reference_plane.kind="verified"`, require a calibrated feeler no larger
than 0.25 mm, `passed=true`, worst-location text, and a photo. For
`kind="certified"`, require a nonempty certificate/reference string instead.
Derive vertical dwell minutes from the two timezone-aware timestamps; do not
trust a separately typed duration.

Each checkpoint object has this shape:

```json
{
  "s4_hand_pressure_only": true,
  "forced_actions": [],
  "seam_overlap": false,
  "visible_bow": false,
  "diameters_mm": {"d0": 300.0, "d45": 300.0, "d90": 300.0, "d135": 300.0},
  "seam_gaps_mm": {
    "S1": {"inner": 0.10, "middle": 0.10, "outer": 0.10},
    "S2": {"inner": 0.10, "middle": 0.10, "outer": 0.10},
    "S3": {"inner": 0.10, "middle": 0.10, "outer": 0.10},
    "S4": {"inner": 0.10, "middle": 0.10, "outer": 0.10}
  },
  "seam_steps_mm": {
    "S1-A": 0.10, "S1-B": 0.10,
    "S2-A": 0.10, "S2-B": 0.10,
    "S3-A": 0.10, "S3-B": 0.10,
    "S4-A": 0.10, "S4-B": 0.10
  },
  "rocking": false,
  "worst_flatness_gap_mm": 0.20,
  "worst_flatness_location": "d45 outer"
}
```

`boundary_rechecks` is normally empty. Its keys are JSON-style result paths,
for example `checkpoints.cycle1_free_state.diameters_mm.d0`; its values are
second calibrated numeric readings. It is needed only when the first reading
is exactly on an acceptance boundary.

Photo values are paths or stable identifiers. The evaluator requires nonempty
values but does not interpret image contents or require network access. A local
path that is supplied but does not exist relative to the result file is
reported as missing evidence.

## Evaluation rules

Statuses are `pass`, `borderline`, `fail`, and `incomplete`.

### Physical FAIL

A result is `fail` when evidence directly establishes a RED physical result:

- any calibrated OD is outside nominal +/-0.50 mm, or OD range exceeds 0.50;
- any calibrated seam gap is outside 0.05..0.30, seam step exceeds 0.25, or
  free-state flatness exceeds 0.50;
- rocking, seam overlap/bow, forced S4 action, movement, disengagement, or
  hardware movement is observed;
- a pin is not exactly 2.50 mm before the inversion/tug, changes measurably
  afterward, free-drops, needs impact, releases, visibly moves, or damages the
  bridge;
- a nut is not flat/below-seat/nonspinning, or was forced;
- a screw has any false-preload/cross-thread symptom;
- cycle damage is nonempty, S4 becomes more forceful than Cycle 1, or any
  cycle is `forced`; force order is `free < light < firm < forced`;
- vertical or lift/place observations record physical movement/failure.

Use inclusive limits only after valid calibrated measurement. Do not apply an
epsilon that silently turns an outside value into a pass.

### BORDERLINE

A first calibrated value exactly on a numeric boundary is `borderline` until
the matching path appears in `boundary_rechecks`. The second reading is then
evaluated inclusively: inside/on-boundary passes, outside fails.

Paper-screen results never directly pass or fail a numeric gate. They should
not appear as numeric measurements. If the operator provides only paper-screen
language and omits calibrated data, the gate is incomplete, not RED.

### INCOMPLETE

Well-formed results are `incomplete` when the article has not been tested to
the card, including:

- any required field, ID, checkpoint, raw reading, photo group, or result path
  is missing/null;
- OD setup resolution is greater than 0.25 mm or is unverified;
- pin/feeler tools are uncalibrated;
- the reference plane is neither certified nor passed with a 0.25 mm feeler;
- cycles are not exactly 1–3, Cycle 1 is not the initial assembly, a procedure
  field is false/mismatched, timestamps are absent/non-timezone-aware,
  derived vertical dwell is under 60 minutes, the down
  quadrant is not Q1, towel/contact semantics differ, or the lift sequence,
  count, height, or hold time is incomplete;
- a supplied local photo path does not exist.

Procedure insufficiency is not proof that the part failed. Report it as
incomplete and name the fields that need correction/retest.

### Overall precedence

Malformed JSON/schema is an invocation error, not a verdict. For well-formed
input use `fail` > `incomplete` > `borderline` > `pass`. Thus a known physical
failure remains FAIL even if another photo is missing, while a fully measured
but unresolved boundary remains BORDERLINE.

## Output contract

JSON mode emits one object to stdout:

```json
{
  "schema": "kage.b0.q4-r1.physical-evaluation.v1",
  "article": "p3_v3_mvp_base_q4_r1",
  "card_version": "v3",
  "card_sha256": "cb37c040fcf06f1bc807155044638f25ac359b638dd70b586bffa7b7999a046c",
  "input": "/absolute/path/b0-results.json",
  "overall_status": "pass",
  "exit_code": 0,
  "threshold_source": "B0PhysicalAcceptance + p3_v3_mvp_base_q4_r1_spec.SPEC",
  "summary": {"pass": 6, "borderline": 0, "fail": 0, "incomplete": 0},
  "derived": {
    "cycle1_free_state": {
      "od_min_mm": 300.0,
      "od_max_mm": 300.0,
      "od_range_mm": 0.0,
      "worst_seam_gap_mm": 0.10,
      "worst_step_mm": 0.10,
      "worst_flatness_mm": 0.20
    }
  },
  "checks": [
    {"id": "01_loop_od", "status": "pass", "reasons": []}
  ],
  "missing_fields": [],
  "warnings": []
}
```

Always return six check rows, matching the card:

1. `01_loop_od`
2. `02_seam_gap_step`
3. `03_free_state_flatness`
4. `04_service_cycles`
5. `05_vertical_retention`
6. `06_lift_place`

Hardware-fit and instrument/reference validity feed the affected checks and
also appear in `derived`; do not invent a seventh acceptance check.

Every reason uses a stable object with `code`, `path`, `expected`, and `actual`.
JSON stdout contains no prose prefix. Parse/usage errors go to stderr.

Text mode is deterministic, uncolored, and compact:

```text
KAGE B0 Q4-R1: PASS
01 loop + OD             PASS  D=299.9/300.0/300.1/300.0 mm; range=0.2 mm
02 seam gap + step       PASS  gaps=0.08..0.14 mm; worst step=0.18 mm S3-B
03 free-state flatness   PASS  worst=0.30 mm d45 outer; rocking=no
04 three service cycles  PASS  S4=light/light/light; damage=none
05 vertical retention    PASS  Q1 down; 60 min; post-checks pass
06 ten lift/place cycles PASS  sequence/count pass; post-checks pass
Overall: PASS — B0 physical gate may proceed to independent acceptance.
```

For non-pass results, append one indented line per reason. The CLI evaluates;
it does not self-approve the article.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | complete PASS |
| `1` | physical FAIL |
| `2` | CLI usage, unreadable file, malformed JSON, wrong schema/version, or invalid field type/value |
| `3` | BORDERLINE with no FAIL or INCOMPLETE |
| `4` | INCOMPLETE with no known FAIL |

When FAIL coexists with missing/borderline evidence, exit `1` and preserve the
other statuses in the JSON/text detail.

## Seven meaningful tests

1. **Installed uv CLI and output parity.** A complete passing fixture returns
   code 0 through `uv run kage-clock b0-evaluate`; text and `--json` agree on
   all six statuses and derived worst cases.
2. **OD boundaries and negative fixture.** Probe 299.50, 300.50, and range 0.50
   as first readings (BORDERLINE/code 3), add calibrated boundary rechecks
   (PASS/code 0), then use 299.49, 300.51, and range 0.51 (FAIL/code 1).
3. **Gap/step/flatness boundaries.** Parameterize 0.05/0.30 gap, 0.25 step,
   and 0.50 flatness through borderline/recheck/pass; use 0.049/0.301,
   0.251, and 0.501 as deliberate FAIL negatives. Paper-only data is
   INCOMPLETE, never numeric FAIL.
4. **Hardware-fit sensitivity.** Exact 2.50 before/after with all false flags
   passes. Independently mutate to 2.49, a measurable after delta, free-drop,
   impact, release/movement/damage, nut spin/cock, and each false-preload flag;
   every mutation fails.
5. **Workflow and handling semantics.** Exact three-cycle, Q1-down 60-minute,
   and ten-lift sequence passes. Missing Cycle 3, Q2 down, 59 minutes, extra
   towel contact, nine lifts, or short hold is INCOMPLETE. Observed seam or
   hardware movement is FAIL.
6. **Missing/malformed evidence.** Omit each required group/cardinality/photo
   in turn and require code 4 with exact field paths. Malformed JSON, NaN,
   boolean-as-number, wrong schema/article/card version/card hash, or unreadable path returns
   code 2 on stderr with no misleading verdict.
7. **Single-source and precedence.** Tests import thresholds rather than repeat
   literals; JSON reasons expose the contract values. A fixture containing one
   physical failure plus a missing photo exits 1, while incomplete plus
   borderline but no failure exits 4.

These seven tests are sufficient. Do not add database persistence, templates,
interactive prompts, photo recognition, CAD tests, or one test per scalar
field.
