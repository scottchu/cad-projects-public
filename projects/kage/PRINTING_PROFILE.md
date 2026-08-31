# Kage printing profile

Shared checklist: [FDM design rules](../../docs/FDM_DESIGN_RULES.md).

## Profile

- ID / revision / updated: `kage-print-01` / draft-1 / 2026-08-31.
- Applicability: Kage printed structural/internal parts. Exact next-print source,
  revision and part list are pending; this does not adopt a new CAD baseline.
- Status: draft; no slicer preset or print approval. Historical reference CAD
  and current [acceptance boundaries](PROJECT_STATE.md) remain unchanged.
- Evidence labels: available / intended / verified slice / physical observation.
  User print reports below are not yet bound to an artifact/process fingerprint.

## Intended settings

| Setting | Value | Basis / evidence |
|---|---|---|
| Printer / usable build area | Intended Snapmaker U1; nominal 270 x 270 x 270 mm | `KAGE-REQ-005`; actual plate footprint plus brim still needs checking |
| Head / tool mapping / nozzle type | pending | no selected tool/nozzle record |
| Nozzle diameter (mm) | pending selection; 0.4 available | [workshop inventory](../../docs/WORKSHOP.md), not confirmed for these prints |
| Material family / brand / product / color | Intended PETG structural/internal; product/color pending | [requirements](docs/REQUIREMENTS.md), `KAGE-REQ-008` |
| Filament diameter / conditioning | pending | no bound spool/process record |
| Build surface / adhesion preparation | pending | pending |
| First / normal layer height (mm) | pending | pending |
| Extrusion widths (mm) | pending | include first layer/feature overrides |
| Wall count / top and bottom thickness | pending | pending |
| Infill pattern / density | pending | pending |
| Nozzle / bed temperature (first and later layers) | pending | actual product profile required |
| Cooling / speeds / volumetric limit | pending | pending |
| Supports / interface / removal access | pending per part | pending |
| Brim / spacing / fit compensation | pending | no universal clearance selected |

## Part orientation and fits

Print XY is the bed plane; +Z is build direction. Assembled vertical does not
require upright printing. These are assessment items, not authorized transforms.

| Part / quantity / material override | Assembled pose | Bed face / print transform | Main load / critical fits | Evidence / status |
|---|---|---|---|---|
| Segmented base; exact source/quantity binding pending | Lies flat, `KAGE-REQ-006` | pending source-defined placement | Seam seating/flatness and roller mounting | User report below; no complete process record |
| Free-roller upright and station foot; exact identities pending | Upright support in user's preview | Compare separate flat-printed upright with assembled pose | Lateral bending, foot fastening, anti-rotation, insert/nut access | Open concerns; no fracture observed or orientation selected |
| Other printed parts | pending | pending | Running fits, gear/guide wear and clearance | pending |

## Verified slice and print runs

No fully traced run is registered in this profile. The user reported printed
base pieces usable for free-roller mounting, but source/3MF, material, nozzle and
slicer settings for that print have not been bound here. This is limited
physical feedback, not full mechanism or next-version acceptance.

| Run field | Record |
|---|---|
| Run ID / date / profile revision + hash | pending; actual print date unknown |
| Source revision or manifest + SHA-256 / parameters | pending |
| STEP / mesh / 3MF path + SHA-256 | pending |
| Slicer / version / preset paths + SHA-256 | pending |
| Resolved printer / head / nozzle / material | pending |
| Plate / object overrides and print transforms | pending |
| Resolved settings record / G-code path + SHA-256 | pending |
| CAD evidence / written artifact and slicer evidence | unchanged historical scope; no new validation |
| Physical job ID / observations / measurements / verdict | limited user report below; exact job and measurements pending |

Append future exact runs with all fields; retain each prior profile revision/hash
and evidence when settings change.

## Concerns

Captured from the phone continuation and 2026-08-31 discussion. Print dates and
artifact identities are unknown; observations are user reports, not new tests.

| ID / affected part | Observation or hypothesis / evidence | Proposed mitigation or check | Status / closure evidence |
|---|---|---|---|
| KAGE-PRINT-001 / base seams | User reports a little outer-side gap after pushing two pieces together, one piece slightly proud, but usable for free-roller mounting | Bind printed revision, measure seam seating/flatness before a small correction | Deferred by user; not a failed whole base |
| KAGE-PRINT-002 / upright-to-foot joint | User says upright appears insufficiently attached in supplied CAD screenshot, and proposes extending the foot for M3 heat-set inserts OR nuts | Confirm exact parts/load path and mounting intent; then check seating, anti-rotation, hardware dimensions, screw/tool access and underside flatness | Open design concern; no option selected and no CAD changed |
| KAGE-PRINT-003 / upright | Hypothesis: upright printing may be weak under lateral bending; no observed break | Compare load-relative orientations, separately printed/fastened bar and critical-root paths; representative strength/fit check after intent approval | Open; flat printing not yet validated |

Next: confirm the intended upright/foot connection before modeling; select and
record actual process settings before any separately authorized print handoff.
