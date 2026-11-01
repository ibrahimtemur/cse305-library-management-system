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

## PDF Export Pipeline & Link Sanitization Rule

To prevent leaking local workstation paths (`file:///C:/Users/...`) and ensure offline grading readability, all PDF deliverables (`HW01_Problem_Solution_DomainModel.pdf` and upcoming HW02 deliverables) are generated via `tools/export-pdf.ps1` (or `python tools/export-pdf.py`).

### Key Rules Enforced by the Pipeline
1. **Zero Local Path / `file://` Links:** Hyperlinks pointing to local files or temporary scratch folders are strictly prohibited. All repository file references (`.md`, `.svg`, `.mmd`, `README`) are rendered in the PDF as plain text with repository-relative paths in code style (e.g., `<code>docs/02-inception/BUSINESS_RULES.md</code>`).
2. **Public Repository URL (Sole Permitted External Link):** Following the repository visibility switch to public on 2026-11-01, `https://github.com/ibrahimtemur/cse305-library-management-system` is preserved as a clickable external link in the PDF. It is the sole external URL permitted by the export tool's allowlist; all other external links and all local `file://` links remain strictly prohibited.
3. **Internal Document Anchors Only:** Table of Contents links are rendered as verified internal PDF page anchors (`/Dest`). If an anchor cannot be resolved to an existing page, it is converted to plain text.
4. **Base64 Embedded Images:** All architectural diagrams and domain models are inlined as base64 Data URIs (`data:image/png;base64,...`) so Chrome headless resolves zero external image files.
5. **Dedicated Landscape Layout:** Section 3.1 (Class Diagram) is styled with `@page dm-landscape` on a dedicated A4 landscape page (11 pages total).
6. **Automated Leak Assertion:** The export script parses the generated PDF with `pypdf` and fails loudly if any `file://`, `C:\Users`, `OneDrive`, `antigravity`, `.gemini`, or `scratch` path is detected in annotations, page text, or metadata.

### Toolchain Dependencies & Execution
- **Markdown Renderer:** `marked@18.1.2` (invoked via `npx --yes marked@18.1.2 --gfm`).
- **PDF Inspection & Leak Scanning:** `pypdf==6.21.1` (pinned in [`tools/requirements-export.txt`](../../tools/requirements-export.txt)).
- **Browser Engine:** Google Chrome headless. Discovered via `CHROME_PATH` environment variable, standard Windows installation locations (`%ProgramFiles%\Google\Chrome\Application\chrome.exe`), or system `PATH`.
- **Command:**
  ```powershell
  .\tools\export-pdf.ps1
  # or
  python tools\export-pdf.py --input docs/01-proposal/HW01_Problem_Solution_DomainModel.md --output docs/01-proposal/HW01_Problem_Solution_DomainModel.pdf --root-output HW01_Problem_Solution_DomainModel.pdf
  ```
