# XT60 bend jig printing profile

Shared checklist: [FDM design rules](../../docs/FDM_DESIGN_RULES.md).

## Profile

- ID / revision / updated: `xt60-print-01` / main-P19-draft-1 / 2026-08-31.
- Applicability: P19 R1 manufacturing planning only. The [current handoff](docs/iterations/p19-r1-front-edge-short-tail/HANDOFF.md)
  accepts CAD, six written STEP artifacts and Viewer handoff, not mesh/3MF,
  slicing, printing or physical performance.
- Status: draft, not a slicer preset or print approval. Historical P13 process
  observations do not release P19 or establish its complete process settings.
- Evidence labels: available / intended / verified slice / physical observation.
  Unknown active settings remain pending, not inherited defaults.

## Intended settings

| Setting | Value | Basis / evidence |
|---|---|---|
| Printer / usable build area | pending selection; Snapmaker U1 available | [workshop inventory](../../docs/WORKSHOP.md); historical U1 preview is not a P19 selection |
| Head / tool mapping / nozzle type | pending | pending |
| Nozzle diameter (mm) | pending for P19; 0.4 historical/available | `CHOICE-003` and PETG coupon in [experience](docs/EXPERIENCE.md) |
| Material family / brand / product / color | pending P19 process selection; PETG prior prototype assumption | [requirements](docs/REQUIREMENTS.md) `CHOICE-003`; reconfirm active candidate and product |
| Filament diameter / conditioning | pending | no bound P19 spool/process record |
| Build surface / adhesion preparation | pending | pending |
| First / normal layer height (mm) | pending for P19 | older P13 0.25/0.20 mm record is not active selection |
| Extrusion widths (mm) | pending | include first layer/feature overrides |
| Wall count / top and bottom thickness | pending | pending |
| Infill pattern / density | pending | pending |
| Nozzle / bed temperature (first and later layers) | pending | actual product profile required |
| Cooling / speeds / volumetric limit | pending | pending |
| Supports / interface / removal access | pending per part | pending |
| Brim / spacing / fit compensation | pending | no automatic reuse of coupon clearance for other fit roles |

## Part orientation and fits

Assembly X is the rod axis; FRONT is YZ (`+Z` up, `+Y` outward). Print XY is
the bed plane, +Z build direction: record the mapping, do not infer it from a
Viewer camera or silently flip source-authored print placement.

| Part / quantity / material override | Assembled pose | Bed face / print transform | Main load / critical fits | Evidence / status |
|---|---|---|---|---|
| Four principal plates | Two fixed inner / two counter-rotating outer plates | pending review of source-authored print placement with selected process | Rod/rail fit, thin webs, hand load and layer orientation | CAD/STEP evidence only; manufacturing unvalidated |
| Six permanent rod-end caps | Three at each axial side | pending process/orientation validation | Socket fit, installation force, layer splitting and retention | No current physical acceptance |
| One printed stepped axle and two keepers | Fixed axle along X; keepers retain stack | pending | Key/journal fits, assembly path, retention and creep | CAD/STEP evidence only |
| Three purchased OD4 x 50 mm rods | Along X | N/A; not printed | Preserve purchased dimensions | Exact P19 handoff |

## Verified slice and print runs

No P19 run is registered or authorized. Historical records in
[EXPERIENCE](docs/EXPERIENCE.md) include a PETG/0.4 mm rod-hole coupon and a
P13 early-layer failure. Their role-specific results are not P19 acceptance.

| Run field | Record |
|---|---|
| Run ID / date / profile revision + hash | pending |
| Source revision or manifest + SHA-256 / parameters | next print binding pending; P19 digital fingerprint is in current handoff |
| STEP / mesh / 3MF path + SHA-256 | no approved P19 print release; existing STEP evidence is separate |
| Slicer / version / preset paths + SHA-256 | pending |
| Resolved printer / head / nozzle / material | pending |
| Plate / object overrides and print transforms | pending |
| Resolved settings record / G-code path + SHA-256 | pending |
| CAD evidence / written artifact and slicer evidence | P19 CAD/STEP accepted historically / no slicing acceptance |
| Physical job ID / observations / measurements / verdict | none for P19 |

Append future exact runs with all fields; preserve prior revision/hash and
observations rather than replacing historical settings with current intentions.

## Concerns

| ID / affected part | Observation or hypothesis / evidence | Proposed mitigation or check | Status / closure evidence |
|---|---|---|---|
| XT60-PRINT-001 / P19 service and travel margins | [P19 review](docs/iterations/p19-r1-front-edge-short-tail/REVIEW.md) records nominal service clearance and rail travels at their required limits, without added manufacturing margin | Evaluate process variation and physical access before a separately authorized print release | Open manufacturing risk; not a new collision claim |
| XT60-PRINT-002 / plates, axle and caps | Hypothesis: layer orientation, flex, friction and retention may compromise operation | Choose per-part load-relative orientation; inspect actual paths and validate fit/load/release physically | Open; no manufacturing/strength acceptance |
| XT60-PRINT-003 / plate first layers | Observed historical P13 floating early-layer preview | Verify source-authored contact, written orientation and actual initial layers for each future artifact | Historical regression; recheck per new artifact |
| XT60-PRINT-004 / cap and running fits | Historical coupon fit depended on role/process; cap variance and center-hole fit failures are recorded | Match fit role and selected process with a coupon; do not transfer sliding-bore results to permanent retention | Open for P19 |

Next: human review and a separately authorized manufacturing/physical test plan.
This profile does not change the accepted P19 geometry or authorize print artifacts.
