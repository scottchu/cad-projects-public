# Downloaded-print diagnosis — DIA-01

Status: read-only diagnostic complete; physical cause unresolved. Owner `/root/case_download_diagnosis`, Sol/high; repository baseline `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`. Frozen input manifest `inputs/download-diagnosis.sha256`, fingerprint `f9cbc5fdfee95a80849414f7bcbffaff647ae69b875108421d41b4d150fbf207`, verified before and after inspection (10/10 entries).

The user's observation is that the downloaded print reaches contact but cannot screw together. Empty-versus-loaded behavior, contact location, installed toothbrush length and exact printed file remain unknown. No new case CAD exists. This inspection does not authorize copying the downloaded geometry or diagnose the physical root cause.

## Triangle evidence

Inspected the original `/Users/scottchu/Downloads/Laifen+Wave+case.3mf`, SHA-256 `25e041b622ce184f9290858d52c76855097186483c856c5dbe677ea3f4030f10`. Units are millimeters; object component transforms are identity. Print build placements were omitted to study the original coaxial object frames. Lower object is `3D/Objects/object_2.model` (41,466 triangles); cap is `3D/Objects/object_3.model` (46,280 triangles). Both pass trimesh's watertight edge test; no general self-intersection or thread-fit acceptance follows from that test.

Broad coplanar triangle faces establish the following datums. The JSON evidence retains their zero-based triangle IDs, areas and radius ranges; dimensions are not inferred merely from bounding boxes.

| Measured surface | Lower Z | Cap original Z |
|---|---:|---:|
| Inner closed-end floor | -62 | 37.7502518 |
| Open mouth | 65 | -43.2497482 |
| External shoulder / cap bore transition | 60 | -38.2497482 |
| Central exterior end plane | -65 | 43.2502518 |

Therefore lower cavity depth is **127 mm**, cap mouth-to-floor depth **81 mm**, lower central floor thickness **3 mm**, and cap central end thickness **5.5 mm**. There are openings through the lower floor; thickness does not imply a sealed base.

The lower cavity's nominal vertex radius is 15 mm; horizontal triangle intersections at several heights give a minimum inscribed radius approximately **14.98011 mm** because it is faceted. Cap main-bore radius is nominally 15.5 mm, minimum sampled inscribed radius **15.48010 mm**. The lower throat stays the same bore through its male-thread region. With a provisional concentric D29 cylinder, lower radial clearance is approximately **0.480 mm per side**, below the new case's >=1 mm target. This is a comparison with a provisional envelope, not a measurement of the real device.

## Defensible conditional closure relationship

Translate the downward-opening cap by **+103.2497482 mm Z** so its broad mouth annulus meets the lower external shoulder at Z60. Their annular radius ranges overlap. Independently, that placement puts the cap's internal bore-transition plane exactly at the lower mouth Z65. These two matching planar pairs support a nominal closed axial datum; they do not establish rotational thread phase or prove the pose is collision-free.

At that pose, the internal floors are Z-62 and Z141, so usable axial length is:

**127 + 81 - 5 = 203 mm.**

At zero axial overlap, mouth-to-mouth placement instead gives **127 + 81 = 208 mm**. Advancing the cap through the nominal **5 mm** closure overlap consumes that space. Thus, **if the loaded brush is 208 mm long and the print matches this reference**, it can consume all axial space at zero overlap and would exceed the shoulder-closed cavity by **5 mm**. This directly supports an axial-obstruction hypothesis matching “touches but cannot screw,” but neither conditional premise is confirmed. No root-cause conclusion is warranted until the empty-case result is known.

The section PNG shows both the cavity and junction in the conditional pose. Visible thread-profile crossings are at an arbitrary unverified rotational phase and must not be presented as proof of an empty-thread defect. Nominal axial overlap is 5 mm; effective engagement, lead/runout, pitch fit and print tolerance remain unvalidated.

## Regression and next discriminator

Record this metric before any later design change: `gap_after_shoulder_stop = measured_closed_inner_floor_distance - measured_installed_brush_L`; the new original case must satisfy **>=3 mm**, independently of thread friction. Evaluate written geometry at the explicit external shoulder-stop pose and check the real device envelope does not intersect either end during closure. For this downloaded reference and provisional L208, the metric is **-5 mm**, an 8 mm shortfall from the >=3 target. This numeric comparison is diagnostic only; neither downloaded geometry nor provisional dimensions become authoritative new-design input.

The smallest physical discriminator is whether the **empty** halves screw fully together. If yes, investigate loaded axial/radial obstruction and measure installed L. If no, the empty-thread engagement path/tolerance needs its own evidence before blaming brush length. Both failures could coexist. REQ-02 remains unmeasured; REQ-03/04 have a concrete conditional axial regression; REQ-06 engagement and REQ-13 physical cycles/full loaded closure remain pending. Literal both-end noncontact is still unresolved.

## Reproduction and limits

From repository root:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r1-measurement-gate/inputs/download-diagnosis.sha256
uv run python projects/laifen-wave-case/scratch/download-diagnosis/inspect_download.py
```

Script output/evidence: `scratch/download-diagnosis/triangle-evidence.json` (SHA-256 `fb98790554ebed29839cb599e996bfbbfe7d84986d473c4c01e78b5074edbae5`); inspected image `scratch/download-diagnosis/conditional-section.png` (`c5a61be4df4465a0d337f51d9b29851b19d77f2251e3d0c0a2690295fc91317e`); script hash `741b9781899ba954ef5fcc7974f723435dd33f34d0294e4864b5bb731caf45a1`.

Original mesh coordinates only were measured. Prepared variants were hash-checked but not geometrically matched; exact printed identity is unknown. No mesh exports, CAD/source edits, slicing, printer controls or physical acceptance occurred. STEP snapshot/viewer handoff does not apply because no STEP or changed CAD artifact exists; the diagnostic triangle section was visually reviewed. Root owns continuity-index updates.
