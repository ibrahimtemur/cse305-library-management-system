<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Directory index for HW01 project proposal, technical solution outline, domain model, and consolidated submission documents.
-->
# 01 — Project Proposal, Solution Outline & Domain Model (`docs/01-proposal`)

Contains the **HW01 (`v1.2`)** deliverables for the **CSE305 Library Management System** (due **Tuesday, November 3, 2026**, following the instructor's `2026-10-27` announcement postponing `HW01` from October 27 and expanding its scope to include the **Problem Description**, **Solution Outline**, and **Domain Model**).

All documents in this directory are reconciled with the confirmed Adnan Menderes University (ADU) library lending regulations (`docs/02-inception/BUSINESS_RULES.md`, `BR-001`..`BR-018`) and the reproducible `seed v2` dataset (`data/README.md`, `data/seed/*.json`).

## Documents in This Directory

- [`HW01_Problem_Solution_DomainModel.md`](HW01_Problem_Solution_DomainModel.md) — **Single Consolidated HW01 Submission Document (`v1.2`):** Cover block, **Part 1: Problem Description**, **Part 2: Solution Outline**, and **Part 3: Domain Model** (Larman conceptual class diagram, enumerations, seed traceability table, attribute dictionary, associations & multiplicities, key modelling decisions, known limitations, and design-level concepts deferred to `HW03`).
- [`HW01_Problem_Solution_DomainModel.pdf`](HW01_Problem_Solution_DomainModel.pdf) — Print-ready PDF export of [`HW01_Problem_Solution_DomainModel.md`](HW01_Problem_Solution_DomainModel.md) with rendered diagrams.
- [`PROJECT_PROPOSAL.md`](PROJECT_PROPOSAL.md) — Detailed **Part 1** reference (`v1.2`): Problem statement, motivation, stakeholders & roles, in/out-of-scope features, MoSCoW prioritization, confirmed ADU library rules & explicit `ASSUMPTION` register (`ASSUMPTION-01`..`17`), Agile Scrum process & sprint timeline, agentic development approach, and risk mitigation matrix (`RISK-01`..`07`).
- [`SOLUTION_OUTLINE.md`](SOLUTION_OUTLINE.md) — Detailed **Part 2** reference (`v1.2`): Five-tier layered web architecture (`Thymeleaf UI -> Controller -> Service -> Repository -> H2`), technology stack (`pom.xml` active vs. planned), Stitch MCP UI-first design workflow, Open Library + synthetic `seed v2` data strategy, candidate GoF/GRASP design patterns, and agentic verification governance.
- [`images/`](images/README.md) — Mermaid `.mmd` sources and pre-rendered `.png` / `.svg` diagrams (`domain-model.{mmd,png,svg}`, `architecture-overview.{mmd,png,svg}`).
