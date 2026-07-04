# BIM Guidelines for Halls of Worship
**Grail Movement Nigeria — Building Information Modelling Standard**

| | |
|---|---|
| Document no. | GMN-BIM-001 |
| Version | 1.0 (Draft for adoption) |
| Applies to | All design and as-built models of Halls of Worship and ancillary buildings |
| Status | Mandatory once adopted |

---

## 1. Purpose

Every Hall of Worship must have a **single, complete BIM model** that serves
as the source of truth for its design, construction and future maintenance.
The goals are:

1. **Drawings come from the model** — plans, sections, elevations, schedules
   and quantities are extracted, never drawn separately, so they can never
   disagree with each other.
2. **Accurate quantities** — the Bill of Quantities is taken off the model,
   which removes a major source of cost overruns.
3. **Reusability** — a modelled hall becomes a template library for the next
   project instead of starting from zero.
4. **A permanent record** — as-built models support maintenance, extensions
   and repairs for decades.

## 2. Software and File Formats

| Item | Standard |
|---|---|
| Authoring tool | Any capable BIM authoring tool (e.g. Revit, ArchiCAD, FreeCAD/BlenderBIM). **One tool per project**, agreed at Gate 1 and recorded in the BIM Execution Plan. |
| Exchange / archive format | **IFC 2x3 or IFC 4** — every issued model must also be exported to IFC so it remains readable regardless of software. |
| Drawings issue format | PDF (signed issues) + DWG/DXF where a contractor requests it. |
| Coordinates | Real-world site coordinates from the licensed survey plan; project base point at a marked, recoverable site benchmark. Units: **millimetres**, elevations in **metres** above datum. |

Native files, IFC exports and PDFs are all archived — never only the native
file.

## 3. Model Structure

- **One federated project, discipline models separated:** Architecture,
  Structure, MEP (mechanical/electrical/plumbing), Site/External works.
- Each discipline model is linked, not merged, and clash-checked before every
  gate (Section 6).
- Storeys/levels named identically in all discipline models:
  `L00 Ground`, `L01 First`, `RF Roof`, `FD Foundation`.

## 4. Naming Conventions

### 4.1 Project code
As defined in GMN-PG-001 §6: `GMN-<STATE>-<TOWN>-<NN>`, e.g. `GMN-LA-LAGOS-01`.

### 4.2 File names
```
<ProjectCode>-<Originator>-<Discipline>-<Type>-<Number>-<Revision>
```

| Field | Codes |
|---|---|
| Originator | Short code for the firm/person, e.g. `ADO` |
| Discipline | `AR` architecture, `ST` structure, `ME` mechanical, `EL` electrical, `PL` plumbing, `SI` site, `ZZ` federated |
| Type | `M3` model, `DR` drawing, `SC` schedule, `RP` report, `BQ` bill of quantities |
| Revision | `P01, P02…` preliminary; `C01, C02…` issued for construction; `A01…` as-built |

Example: `GMN-EN-ENUGU-01-ADO-AR-M3-0001-P03.ifc`

### 4.3 Drawing numbers
```
<ProjectCode>-<Discipline>-<Series><Sheet>
```
Series: `0` general/site, `1` plans, `2` elevations, `3` sections, `4`
details, `5` schedules, `6` MEP layouts.
Example: `GMN-EN-ENUGU-01-AR-101` = architecture, ground floor plan.

## 5. Level of Development (LOD) by Phase

| Project phase (GMN-PG-001) | Required LOD | Meaning |
|---|---|---|
| Phase 1 — Feasibility | LOD 100 | Massing, site placement, capacity check |
| Phase 2 — Concept design | LOD 200 | Approximate geometry, key spaces sized |
| Phase 2 — Technical design (Gate 2) | **LOD 300** | Precise geometry; quantities can be taken off |
| Phase 3–4 — Construction | LOD 350 | Coordination detail, connections, penetrations |
| Phase 5 — Handover | **LOD 500 (as-built)** | Verified as constructed, with equipment data |

**Minimum modelled content at Gate 2 (LOD 300):** foundations, all structural
members, walls with true build-ups, roof structure and covering, doors/windows
with schedules, floor and ceiling finishes, sanitary fittings, major electrical
(distribution boards, generator, lighting layout), water storage and drainage,
external works within the site boundary.

## 6. Quality Checks Before Every Issue

Before a model or drawing set is issued at any gate:

1. **Clash detection** between all discipline models — zero unresolved
   hard clashes (structure vs. services vs. architecture).
2. **Naming audit** — files, levels, and drawing numbers per Section 4.
3. **Quantity sanity check** — QS compares model take-off against manual spot
   checks on at least concrete, blockwork and roofing.
4. **Model checklist** signed by the Design Lead and filed with the gate
   submission.

## 7. Standard Folder Structure

Every project repository/drive uses exactly this structure:

```
GMN-<STATE>-<TOWN>-<NN>/
├── 01-Admin/          (charter, minutes, approvals, contracts)
├── 02-Brief/          (capacity brief, feasibility, surveys, soil report)
├── 03-Models/
│   ├── native/        (authoring files)
│   └── ifc/           (issued IFC exports, one per gate)
├── 04-Drawings/
│   ├── issued/        (signed PDF issues, by revision)
│   └── superseded/
├── 05-Costs/          (cost plans, BOQ, valuations, certificates — see GMN-CM-001)
├── 06-Site/           (site diaries, weekly reports, photos, instructions)
├── 07-Handover/       (as-built model, O&M info, warranties, final account)
└── 08-Lessons/        (lessons-learned report)
```

## 8. The Hall Template Library

To make future projects faster and cheaper:

- After each project closes, reusable components (pews/seating layouts,
  door/window families, roof truss types, sanctuary/platform arrangements,
  standard finishes) are copied into a shared **`template-library`** folder
  maintained alongside this repository.
- New projects **must start from the template library**, adapting to site and
  capacity, rather than modelling from scratch.
- A standard capacity series should be developed over time (e.g. 150-seat,
  300-seat, 500-seat reference halls) so that a new project begins at
  LOD 200 on day one.

## 9. BIM Execution Plan (BEP)

At Gate 1 the Design Lead submits a one-to-two page BEP recording: authoring
software and versions, model originators per discipline, exchange schedule,
coordinate/benchmark definition, and who runs clash detection. The BEP is
approved by the PM and filed in `01-Admin/`.

## 10. As-Built Requirement

Final payment to the design team and contractor is conditional (GMN-PG-001 §6)
on delivery of:
- as-built model (native + IFC) updated to what was actually constructed,
- as-built drawings (PDF),
- equipment schedules with make/model/capacity for generator, pumps, tanks,
  distribution boards and fixed AV equipment.

## 11. Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-07-04 | First issue for adoption | — |
