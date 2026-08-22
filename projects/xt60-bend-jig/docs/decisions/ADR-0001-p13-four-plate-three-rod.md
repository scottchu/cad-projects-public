# ADR-0001: P13 four-plate, three-rod mechanism

- Status: accepted
- Date: `2026-08-21`
- Supersedes: earlier P0–P12 mechanism concepts as the supported prototype
- Superseded by:

## Context

The jig must hold and form two insulated XT60 pigtail wires through a fixed 90-degree path without clamping the XT60 plastic body. It must remain open enough for loading, soldering, cooling, service, and removal while using three purchased `OD4.00 x 50.00 mm` rods.

## Alternatives considered

Earlier frames, sliders, scrolls, three-disc, and quarter-turn concepts are preserved in source and design briefs. They introduced combinations of synchronization, access, printability, removal, or unnecessary frame complexity that P13 was intended to address.

## Decision

Use four circular plates—two fixed guides and two synchronized cams—with one rotary input. Move three functionally asymmetric rods by the same scalar travel along three different straight guide directions. Keep `0 deg` open, contact near `22 deg`, and `27 deg` locked. Exclude a base, decorative handle, and adjustable bend angle.

## Consequences

The mechanism remains compact and parametric but depends on printed plate, shaft, cap, and rod fits. CAD can validate nominal motion and geometry; physical testing must establish force, retention, heat response, insulation safety, removal, and springback.

## Evidence

- `docs/p13-four-plate-three-rod-brief.md`
- `docs/p13-cad-source-domain-amendment.md`
- `src/xt60_bend_jig/p13_four_plate_three_rod.py`
- `tests/test_p13_four_plate_three_rod.py`
- `tests/test_p13_motion.py`
