# Printing profile — <project>

Copy this file to the project root. Paths below are project-relative; replace
placeholders. See repository-root `docs/FDM_DESIGN_RULES.md` for shared rules.

## Profile

- ID / revision / updated: `<project>-print-01` / draft-1 / pending.
- Applicability: pending exact design version, parts and source fingerprint;
  or N/A with a reason if this project has no printed parts.
- Status: draft; not a slicer preset or print approval.
- Evidence labels: available / intended / verified slice / physical observation.
  Unknown means pending, not an automatically chosen default.

## Intended settings

| Setting | Value | Basis / evidence |
|---|---|---|
| Printer / usable build area | pending | pending |
| Head / tool mapping / nozzle type | pending | pending |
| Nozzle diameter (mm) | pending | pending |
| Material family / brand / product / color | pending | pending |
| Filament diameter / conditioning | pending | pending |
| Build surface / adhesion preparation | pending | pending |
| First / normal layer height (mm) | pending | pending |
| Extrusion widths (mm) | pending | include first layer and feature overrides |
| Wall count / top and bottom thickness | pending | pending |
| Infill pattern / density | pending | pending |
| Nozzle / bed temperature (first and later layers) | pending | pending |
| Cooling / speeds / volumetric limit | pending | pending |
| Supports / interface / removal access | pending | pending |
| Brim / spacing / fit compensation | pending | pending |

## Part orientation and fits

Print axes: XY is the bed plane; +Z is layer build direction. Record assembled
pose separately. Do not silently override source-authored print placement.

| Part / quantity / material override | Assembled pose | Bed face / print transform | Main load / critical fits | Evidence / status |
|---|---|---|---|---|
| pending | pending | pending | pending | pending |

## Verified slice and print runs

No verified run is implied by intended settings. Append a record per run and
preserve prior records when the profile changes. Reference project-local release
manifests/evidence rather than copying generated files into this document.

| Run field | Record |
|---|---|
| Run ID / date / profile revision + hash | pending |
| Source revision or manifest + SHA-256 / parameters | pending |
| STEP / mesh / 3MF path + SHA-256 | pending |
| Slicer / version / preset paths + SHA-256 | pending |
| Resolved printer / head / nozzle / material | pending |
| Plate / object overrides and print transforms | pending |
| Resolved settings record / G-code path + SHA-256 | pending |
| CAD evidence / written artifact and slicer evidence | pending; separate verdicts |
| Physical job ID / observations / measurements / verdict | pending |

## Concerns

| ID / affected part | Observation or hypothesis / evidence | Proposed mitigation or check | Status / closure evidence |
|---|---|---|---|
| `<project>-PRINT-001` / pending | pending | pending | open |

Next smallest check: pending. A concern closes only for its stated part/process
and evidence; it does not automatically validate a later revision.
