# Preview parameter readout design

## Selected approach

Add a generated, self-contained `closed.params.js` STEP sidecar and declare it from `closed.step.py`. The sidecar uses the native CAD Viewer Parameters tab only as a compact readout surface:

1. The first row is `00 READ ONLY` with the sole value `Current values - edit Python and regenerate STEP to change`.
2. Each source input is an enum containing exactly one option. Its id matches the Python registry id. The visible label is prefixed by display order and group, for example `01 Axial - Device length`; its sole option shows the current value and classification, for example `208 mm - adjustable in Python`.
3. Derived values use ids prefixed `derived__` and the same one-option enum form. Their sole option ends with `derived readout`.
4. `update()` accepts the standard Viewer call shape but is an explicit no-op. The sidecar has no features or animations.

This avoids sliders, editable number boxes, free text, or fake geometry reactions. CAD Viewer 0.4.28 has no native read-only parameter row or section heading, so ordered group prefixes provide truthful visual grouping inside its flat list. The native module enable toggle and reset action may still appear because they are Viewer-owned chrome; switching either cannot change geometry or presentation.

## Deterministic source and generated artifact

Add `cad/container_generator_v1/preview_parameters.py` with pure functions that:

- read `PARAMETER_SPECS` in source order;
- read current values from `preset()` and derived values from `derive(preset())`;
- validate one row per registry id, exact default equality, unique ids, supported classifications, and finite/readable values;
- map registry groups through the stable order below;
- serialize one deterministic, standalone ES module with no imports;
- expose a CLI/module entry that writes only `cad/container_generator_v1/closed.params.js` when explicitly invoked.

`closed.params.js` is a generated review artifact. A focused test compares its bytes with the pure serializer output, so a registry change cannot silently leave stale displayed values.

Change `closed.step.py` only from a bare shape return to:

```python
def gen_step():
    return {
        "shape": build_assembly(derive(preset())),
        "params": "closed.params.js",
    }
```

No builder or assembly code changes. Do not rewrite `closed.step` or any other STEP file.

## Display groups and source rows

Stable group order:

| Order | Visible group | Registry group | Source ids |
| ---: | --- | --- | --- |
| 1 | Axial | `axial` | `device_length`, `axial_allowance`, `cap_cavity_length` |
| 2 | Device reference | `reference` | `device_diameter` |
| 3 | Radial | `radial` | `body_bore`, `cap_bore` |
| 4 | Exterior | `exterior` | `outer_diameter` |
| 5 | Thread | `thread` | `thread_pitch`, `engagement`, `thread_clearance`, `clearance_budget`, `thread_height`, `root_wall`, `cap_taper_length` |
| 6 | Skin | `skin` | `skin_axial_pitch`, `skin_arc_pitch_target`, `skin_height`, `plateau_half_fraction`, `skin_phase_theta`, `skin_phase_z`, `skin_style` |
| 7 | Ends | `ends` | `floor`, `end_chamfer_size` |
| 8 | Drains | `drains` | `drain_diameter`, `drain_ring_radius`, `drain_ring_count` |

Within each group, preserve the relative order from `PARAMETER_SPECS`. Human labels derive from ids by replacing underscores with spaces and title-casing. Unit labels normalize `mm_radial` to `mm radial` and retain `mm/rev`, `rad`, `ratio`, `count`, and `enum` truthfully. Format integers without a decimal and other numeric values with enough digits to reproduce the source default.

Classification text:

- `adjustable_geometry` -> `adjustable in Python`
- `reference_readout_only` -> `reference only; does not resize CAD`
- `locked` -> `locked P1 R7 value`

## Derived readouts

Append a ninth group, `Derived`, after all 26 source inputs. Derive every value from the single `Resolved` record; do not repeat CAD equations in the preview module.

| Readout id | `Resolved` source / expression | Default display |
| --- | --- | --- |
| `derived__cavity_length` | `cavity_length` | 213 mm |
| `derived__outer_length` | `outer_length` | 219 mm |
| `derived__body_cavity_depth` | `body_depth` | 132 mm |
| `derived__body_height` | `body_depth + floor + neck_height` | 144 mm |
| `derived__cap_height` | `cap_height` | 84 mm |
| `derived__thread_turns` | `engagement / thread_pitch` | 3 rev |
| `derived__body_radial_gap` | `body_radial_gap` | 0.5 mm radial, reference only |
| `derived__cap_radial_gap` | `cap_radial_gap` | 1 mm radial, reference only |
| `derived__lattice_count` | `lattice_count` | 33 repeats |
| `derived__exact_arc_pitch` | `arc_pitch` | approximately 3.627 mm |
| `derived__female_minimum_wall` | `female_minimum_wall` | 1.85 mm |
| `derived__overall_minimum_wall` | `minimum_wall` | 1.4 mm |
| `derived__drain_hole_count_each_end` | `len(drain_centers)` | 7 holes |
| `derived__print_bounds_separation` | `print_bounds_separation` | 7 mm |

The serializer may compute `body_height` and `thread_turns` only by reading fields from the already derived `Resolved` record. These are presentation arithmetic, not alternative geometry derivation. Tests bind their defaults exactly.

## Sidecar schema

The generated file must have this semantic structure:

```javascript
export const READOUT_SCHEMA = Object.freeze({
  mode: "read_only_parameter_snapshot",
  source: "PARAMETER_SPECS + derive(preset())",
  geometryRegeneration: false
});

export default {
  manifest: {
    schemaVersion: 1,
    step: { path: "cad/container_generator_v1/closed.step" },
    parameters: { /* notice, 26 inputs, 14 derived rows */ }
  },
  update() {}
};
```

Each row must be `{type: "enum", label, description, options: [{value, label}], default: value}` with exactly one option. Descriptions repeat `Read-only snapshot. Edit parameters.py and regenerate STEP to change CAD.` because Viewer 0.4.28 does not render a persistent custom explanatory block. The manifest must omit `features` and `animations` rather than supplying empty interactive contracts.

`manifest.step.path` is the workspace-relative logical exported STEP link required by the Viewer schema. It is provenance only, not a freshness or live-regeneration claim.

## Delta mask

Implementer `PPV-02` has exclusive write access only to:

- `projects/laifen-wave-case/cad/container_generator_v1/preview_parameters.py`
- `projects/laifen-wave-case/cad/container_generator_v1/closed.params.js`
- `projects/laifen-wave-case/cad/container_generator_v1/closed.step.py`
- `projects/laifen-wave-case/tests/test_container_generator_v1_preview_parameters.py`
- `projects/laifen-wave-case/docs/iterations/2026-09-04-preview-parameters/IMPLEMENTATION.md`
- `projects/laifen-wave-case/docs/iterations/2026-09-04-preview-parameters/candidate-files.sha256`
- `projects/laifen-wave-case/docs/iterations/2026-09-04-preview-parameters/evidence-files.sha256`
- `projects/laifen-wave-case/scratch/preview-parameters-implementation/**`

Forbidden writes: all `.step` files, every other `container_generator_v1` module/entrypoint, P1 R7 oracle, old previews, installed Viewer runtime, services/routes, requirements, decisions, printing profile, observations, and unrelated projects.

## Focused verification

### Cheap source and math gate

`test_container_generator_v1_preview_parameters.py` must catch these credible failures:

- a missing, duplicate, reordered, stale, or misclassified registry row;
- a derived readout that disagrees with `derive(preset())`;
- a mutable control type or a row with more than one legal option;
- omission or weakening of the visible read-only/regeneration notice;
- sidecar imports, features, animations, effects calls, transforms/styles, or a non-no-op update;
- `closed.step.py` not declaring the exact relative sidecar path;
- any byte change to the four accepted STEP artifacts;
- nondeterministic serializer output or committed-sidecar drift.

Use Python 3.12 through root `uv run`. Use Node only for importing the generated sidecar and inspecting its exported manifest/update behavior; do not add dependencies.

### Generated Viewer package and endpoint gate

After the cheap gate passes:

1. Trigger only the existing `closed.step.py` Viewer build. Do not run `scripts/gen --write` against any STEP target.
2. Inspect the generated `__cadgen__` descriptor and require its `paramsPath` to resolve exactly to `cad/container_generator_v1/closed.params.js`.
3. Import the served sidecar and require the same row count, ids, one-option contract, read-only schema flag, and no-effect update.
4. Require the exact review page HTTP 200 and exact artifact endpoint HTTP 200 with JSON `state == "ready"`.

### Visual delivery-surface gate

At mobile width, open the existing private URL for `closed.step.py`, open the right file sheet, select Parameters, and record one screenshot showing:

- the unchanged closed case without a visible error state;
- `00 READ ONLY` and its regeneration message;
- enough scrolling evidence to show representative rows from Axial, Device reference, Thread, Skin, Ends, Drains, and Derived;
- no slider, checkbox, free-text box, action button, animation control, or second selectable value for any readout.

If the native one-option select still appears to the user as a live CAD editor, the visual gate is BLOCK and this design stops. Do not hide the ambiguity with explanatory prose outside the preview.

## Acceptance labels and limits

- **Preview readout PASS** means the exact current defaults are visibly and truthfully displayed, the sidecar is effect-free, and the accepted STEP bytes are unchanged.
- Existing **CAD/source PASS** and **written STEP PASS** remain inherited from the reviewed P1 R7 refactor because no CAD or STEP artifact changes.
- **Editable customizer:** not implemented. Changing Python parameters and regenerating/revalidating STEP remains the workflow.
- **Slicer/process:** HOLD.
- **Physical:** PARTIAL / UNBOUND; unchanged from the accepted refactor record.
