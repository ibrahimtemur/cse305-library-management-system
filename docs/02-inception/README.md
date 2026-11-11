<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Directory index for HW02 Inception phase artifacts (consolidated submission document/PDF, UP requirements specifications, Agile Scrum backlog, and rendered diagrams).
-->
# 02 — Inception (`docs/02-inception`)

Holds the **HW02 Inception Phase** deliverables (Deadline: **Tuesday, November 10, 2026**) covering both the **Unified Process (UP) Inception** requirements artifacts and the **Agile Scrum** Product Backlog & Iteration Plan artifacts.

## Consolidated HW02 Submission Document (`v1.0`)

- **[`HW02_Inception_Agile.md`](HW02_Inception_Agile.md)** & **[`HW02_Inception_Agile.pdf`](HW02_Inception_Agile.pdf)** *(also copied to repository root as [`../../HW02_Inception_Agile.pdf`](../../HW02_Inception_Agile.pdf))* — Single consolidated submission document containing **Part 1: UP Inception Overview** and **Part 2: Agile Scrum Product Backlog & Iteration Plan** (`18` pages, `4` embedded PNG diagrams, `0` local path leaks).

## Part 1 — Unified Process (UP) Inception Artifacts

1. [`VISION_AND_CONTEXT.md`](VISION_AND_CONTEXT.md) — Product vision statement, problem recap, project goals (`GOAL-01`..`GOAL-05`), target success metrics (`MET-01`..`MET-05`), stakeholder analysis, explicit scope constraints, and System Context Diagram (Mermaid).
2. [`PERSONAS.md`](PERSONAS.md) — Detailed user personas (`Librarian / Admin`, `Student Member`, `Academic Staff Member`, `Administrative Staff Member`, `Guest`) grounded in synthetic seed records from [`data/seed/`](../../data/seed/) and confirmed ADU library rules.
3. [`REQUIREMENTS.md`](REQUIREMENTS.md) — Supplementary Specification: numbered Functional Requirements (`FR-001`..`FR-032`) grouped by MoSCoW features (`M1`–`M6`, `S1`–`S4`, `C1`–`C3`), Non-Functional Requirements (`NFR-001`..`NFR-012`), constraints (`CON-001`..`CON-006`), and seed data requirements (`DR-001`..`DR-007`).
4. [`BUSINESS_RULES.md`](BUSINESS_RULES.md) — Official ADU Library rule verification sources (`CONFIRMED`), superseded `HW01` assumptions table, new proposed assumptions (`ASSUMPTION-10`..`ASSUMPTION-17`), and numbered business rules (`BR-001`..`BR-018`) with deterministic formulas.
5. [`DOMAIN_GLOSSARY.md`](DOMAIN_GLOSSARY.md) — Ubiquitous Language glossary aligning domain entities, GoF pattern collaborators, and exact JSON field names and enumerated values in [`data/seed/*.json`](../../data/seed/).
6. [`USE_CASES.md`](USE_CASES.md) — Use Case Diagram (Mermaid `flowchart` approximation), summary table, fully-dressed (`UC-01`, `UC-05`, `UC-06`, `UC-09`) and brief (`UC-02`, `UC-03`, `UC-04`, `UC-07`, `UC-08`, `UC-10`, `UC-11`) use case specifications, and end-to-end traceability matrix (`FR` ↔ `UC` ↔ `BR`).

## Part 2 — Agile Scrum Product Backlog & Iteration Plan Artifacts

7. [`THEMES_EPICS.md`](THEMES_EPICS.md) — Product hierarchy decomposing **4 Themes** (`T1`–`T4`) and **9 Epics** (`E1`–`E9`) into `21` stories (`88` story points, `173.0` classic hours, `90.0` human hours).
8. [`USER_STORIES.md`](USER_STORIES.md) — Full catalog of **21 User Stories** (`LMS-001`..`LMS-021`) with role/goal/benefit statements, Given/When/Then acceptance criteria, `FR`/`UC`/`BR` traceability tags, Fibonacci story points, classic/human hour estimates, and budgeted AI agent sessions (`46` total).
9. [`PRODUCT_BACKLOG.md`](PRODUCT_BACKLOG.md) — Ordered Scrum Product Backlog (`LMS-001`..`LMS-021`), script-generated point and hour totals, capacity/Must-fit summary, Product Owner-approved Sprint 3 commitment line (`17.5 h <= 17.8 h`), and `FR-001`..`FR-032` → `UC` → `BR` → Story → Sprint traceability table.
10. [`SPRINT_PLAN.md`](SPRINT_PLAN.md) — Three-sprint iteration plan (`Sprint 1` Nov 11–Dec 08 / `HW03`, `Sprint 2` Dec 09–Dec 22 / `HW04`, `Sprint 3` Dec 23–Jan 05 / `HW05`), two-student human-hour capacity model, accepted `+2.0 h` Must gap governance (`RISK-H01`), Sprint 3 commitment line (`LMS-017`, `LMS-011`, `LMS-012`, `LMS-015` committed; `LMS-014`, `LMS-016`, `LMS-021`, `LMS-018`..`LMS-020` stretch), dependency proof (`OVERALL: PASS`), Definition of Ready (DoR), Definition of Done (DoD), and Risk Register (`RISK-H01`..`RISK-H08`).
11. [`TASKS.md`](TASKS.md) — Decomposition of `LMS-001`..`LMS-021` into **105 Technical Tasks** (`1.0`–`4.0` human h each, summing to `90.0` human h), with Stitch MCP UI tasks scheduled before Thymeleaf view tasks, JUnit 5 TDD test tasks on every story, and an empty `Actual human h` column for Sprint 1–3 tracking.
12. [`PSI_AND_MVP.md`](PSI_AND_MVP.md) — Potentially Shippable Increment (PSI) per sprint, formal MVP definition (`15` committed stories = `11` Must `48 pts / 53.0 h` + `4` Should above the line `16 pts / 17.5 h` = `64 pts / 70.5 h`), stretch slice (`6` stories = `24 pts / 19.5 h`), and explicit MVP exclusions.
13. [`images/`](images/README.md) — Rendered Mermaid diagrams (`system-context`, `use-case-diagram`, `themes-epics`, `sprint-roadmap` in `.mmd`, `.png`, and `.svg`) and regeneration instructions.
14. [`TRELLO_BOARD.md`](TRELLO_BOARD.md) — Trello sprint board specification, public URL ([`https://trello.com/b/34K6O3Y1/cse305-lms-sprint-board`](https://trello.com/b/34K6O3Y1/cse305-lms-sprint-board)), 6-list workflow architecture, MoSCoW color labels, 21 story cards (88 pts, 90.0 h), LMS-001 technical task checklist, and workflow rules.
