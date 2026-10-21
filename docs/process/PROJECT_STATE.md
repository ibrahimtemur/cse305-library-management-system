<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Living tracker for current project phase, completed tasks, upcoming work, architectural decisions, and open questions.
-->
# Project State — CSE305 Library Management System

- **Last Updated:** 2026-10-21
- **Active Team Member:** Ibrahim Temur (`231805033`)
- **Active Branch:** `develop`
- **Repository:** `https://github.com/ibrahimtemur/cse305-library-management-system` (Private)
- **Current Phase:** **HW01 — Project Proposal & Solution Outline (`docs/01-proposal/`, Deadline: Oct 27) — COMPLETED & PACKAGED** → Ready for **HW02: Inception & Scrum Product Backlog (`docs/02-inception/`, Deadline: Nov 10)**

---

## 1. What Is Done
- **[2026-10-21 | Ibrahim Temur]** Audited local Windows 11 Pro (`10.0.26300`, 64-bit) workstation: verified Oracle JDK `25` LTS, Git `2.55.0.windows.3`, Python `3.11.9` (`pip 26.2.1`), and GitHub CLI `2.102.0` (`ibrahimtemur`).
- **[2026-10-21 | Ibrahim Temur]** Installed Apache Maven `3.9.16` (verified via official SHA-512 checksum `ed41650d...`) into `%LOCALAPPDATA%\Programs\apache-maven-3.9.16`, configured User `PATH` and `JAVA_HOME`, and generated the Maven Wrapper (`mvnw`, `mvnw.cmd`, `.mvn/wrapper/maven-wrapper.properties`).
- **[2026-10-21 | Ibrahim Temur]** Verified GitHub CLI/MCP authentication and documented all 16 Stitch MCP tools without invoking Stitch design generation.
- **[2026-10-21 | Ibrahim Temur]** Created Spring Boot `3.5.16` project skeleton (`edu.adu.lms`, Java 17 target) with `spring-boot-starter-web`, `spring-boot-starter-thymeleaf`, `spring-boot-starter-data-jpa`, `spring-boot-starter-validation`, `com.h2database:h2` (file mode in main, in-memory in test), and `spring-boot-starter-test` (JUnit 5). Verified `mvn test` and `.\mvnw.cmd test` pass (`Tests run: 1, Failures: 0, Errors: 0`).
- **[2026-10-21 | Ibrahim Temur]** Created standard repository layout (`docs/00-course`, `docs/01-proposal`, `docs/02-inception`, `docs/03-design`, `docs/03-design/ui`, `docs/04-sprints`, `docs/process`, `data/seed`, `tools`, `src`) with mandatory file headers verified across all first-party files.
- **[2026-10-21 | Ibrahim Temur]** Created `AGENTS.md`, `README.md`, `.gitignore`, `.gitattributes`, `tools/set-author.{ps1,cmd}` (`ibrahim` / `omer`), and `tools/package.{ps1,cmd}` (`cse305_hwNN_231805033_231805026.zip`).
- **[2026-10-21 | Ibrahim Temur]** Initialized Git repository, set local author to Ibrahim Temur, created initial commit (`db0acd1`), created private GitHub repository `ibrahimtemur/cse305-library-management-system`, and pushed both `main` and `develop` branches.
- **[2026-10-21 | Ibrahim Temur]** Authored `docs/01-proposal/PROJECT_PROPOSAL.md` and `docs/01-proposal/SOLUTION_OUTLINE.md` (and updated `docs/01-proposal/README.md`, commit `fb11f34`) defining the problem statement, stakeholders, MoSCoW scope, explicit `ASSUMPTION` domain policies, Scrum milestone timeline, 5-tier layered architecture, Stitch UI pipeline, Open Library + synthetic data strategy, and candidate GoF/GRASP design patterns.
- **[2026-10-21 | Ibrahim Temur]** Finalized Scrum role assignments across `docs/01-proposal/PROJECT_PROPOSAL.md` and `README.md` (commit `cb254a6`): **Ibrahim Temur** as **Product Owner (PO)** and **Omer Faruk Kuş** as **Scrum Master (SM)** (with both contributing as Developers/Architects/QA/Reviewers).
- **[2026-10-21 | Ibrahim Temur]** Ingested official CSE305 Lecture 0 syllabus (Assoc. Prof. Dr. Fatih Soygazi) into `docs/00-course/COURSE_SYLLABUS_AND_SCHEDULE.md` and `AGENTS.md` (5 assignments = 40%, Final = 60%; `HW01: Oct 27`, `HW02: Nov 10`, `HW03: Dec 8`, `HW04: Dec 22`, `HW05: Jan 5`; individual ADUZEM upload rule) and packaged **`dist/cse305_hw01_231805033_231805026.zip`** via `tools\package 01`.

---

## 2. What Is Next
1. **Upload HW01 to ADUZEM (Deadline: Oct 27):** Both **Ibrahim Temur** (`231805033`) and **Omer Faruk Kuş** (`231805026`) must individually upload `dist\cse305_hw01_231805033_231805026.zip` from their own personal ADUZEM accounts.
2. **HW02 — Inception & Scrum Product Backlog (`docs/02-inception/`, Deadline: Nov 10) [NEXT CHAT]:**
   - Create `docs/02-inception/VISION_AND_CONTEXT.md`: Vision statement and System Context Diagram (Mermaid).
   - Create `docs/02-inception/PERSONAS.md`: Detailed user personas for Librarian/Admin, Student Member, Academic Staff Member, and Guest.
   - Create `docs/02-inception/REQUIREMENTS.md`: Supplementary Specification — traceable Functional Requirements (`FR-*`), Non-Functional Requirements (`NFR-*`), and Business Rules (`BR-*`).
   - Create `docs/02-inception/USE_CASES.md`: Use-case diagram (Mermaid) and structured use-case specifications for catalog, checkout/return, overdue fine, and reservation workflows.
   - Create `docs/02-inception/DOMAIN_GLOSSARY.md`: Ubiquitous language glossary (`Book`, `BookCopy`, `Loan`, `Fine`, `Reservation`, `LoanPolicy`, etc.).
   - Create `docs/02-inception/PRODUCT_BACKLOG.md`: Agile Scrum Themes, Epics, User Stories (`US-*`), Tasks, Story Points, Sprint Planning / Iteration Plan (Sprint 1 / Sprint 2 / Sprint 3), PSI (Potentially Shippable Increment) & MVP definition, Definition of Ready (DoR), Definition of Done (DoD), and Given/When/Then Acceptance Criteria.
3. **HW03 — Elaboration & Sprint 1 (`docs/03-design/`, `docs/04-sprints/sprint-1/`, `src/`, Deadline: Dec 8):**
   - Document layered architecture, Use-Case Diagram, System Sequence Diagrams (SSD), Domain & Design Class Diagrams, TDD/Git/Maven plan, and justified GoF/GRASP design patterns in `docs/03-design/`.
   - Design UI screens first with the Stitch MCP and save HTML exports/screenshots under `docs/03-design/ui/`.
4. **Collaborator Setup:** Collect Omer Faruk Kuş's GitHub username to invite him as a collaborator on `ibrahimtemur/cse305-library-management-system`, and confirm the email linked to his GitHub account for `tools/set-author.ps1`.

---

## 3. Architectural & Process Decisions
| ID | Date | Decided By | Decision | Rationale |
|---|---|---|---|---|
| DEC-01 | 2026-10-21 | Ibrahim Temur | Spring Boot `3.5.16` with `java.version=17` compiled on JDK `25` + Maven `3.9.16` Wrapper | Ensures Java 17 bytecode compatibility while running natively on the installed JDK 25 LTS and allowing zero-install builds via `mvnw.cmd`. |
| DEC-02 | 2026-10-21 | Ibrahim Temur | H2 file mode (`./data/db/lms`) for runtime; in-memory H2 (`mem:lms_test`) for JUnit tests | Provides persistent local storage during runs while keeping automated tests fast, isolated, and repeatable. |
| DEC-03 | 2026-10-21 | Ibrahim Temur | Branching model: `main` (user-approved releases only) ← `develop` ← `feature/*`, `docs/*`, `fix/*` | Enforces protected `main` policy and clean Scrum increment integration. |
| DEC-04 | 2026-10-21 | Ibrahim Temur | Shared-computer author switching via `tools/set-author` (`--local` git config only) | Guarantees accurate per-student commit attribution without touching OS-wide `--global` Git settings. |
| DEC-05 | 2026-10-21 | Ibrahim Temur | Mandatory native-comment file headers on all first-party files | Enforces academic authorship headers across code, config, scripts, and Markdown docs while preserving Apache 2.0 headers on third-party Maven Wrapper files. |
| DEC-06 | 2026-10-21 | Ibrahim Temur | Hybrid Data Strategy: Open Library API book metadata cached in `data/seed/` + 100% synthetic member/loan data | Combines realistic bibliographic catalog data with offline reproducibility and strict personal data privacy compliance (`AGENTS.md` Section 7). |
| DEC-07 | 2026-10-21 | Ibrahim Temur | Core GoF Pattern Selection: `Strategy` (loan/fine policies), `State` (`BookCopy` lifecycle), `Observer` (return/overdue events), `Factory/Builder` (`Loan` creation), `Adapter` (Open Library ingestion) | Directly addresses domain variability and state invariants without artificial over-engineering. |
| DEC-08 | 2026-10-21 | Ibrahim Temur | Explicit `ASSUMPTION` tagging (`ASSUMPTION-01`..`09`) for all lending/fine rules | Prevents inventing unverified facts about ADU's real library policies while establishing clear, testable business rules. |
| DEC-09 | 2026-10-21 | Ibrahim Temur | Scrum Roles: **Ibrahim Temur** = Product Owner (PO); **Omer Faruk Kuş** = Scrum Master (SM); both = Developers/Architects/QA | Establishes clear Scrum accountability while enabling full-stack pair collaboration on a 2-person academic team. |
| DEC-10 | 2026-10-21 | Ibrahim Temur | Official 5-Homework Mapping (`HW01` Oct 27, `HW02` Nov 10, `HW03` Dec 8, `HW04` Dec 22, `HW05` Jan 5) & Dual UP/Scrum Inception Coverage | Aligns every repository phase and `cse305_hwNN_231805033_231805026.zip` package with Assoc. Prof. Dr. Fatih Soygazi's Lecture 0 project schedule. |

---

## 4. Open Questions & Follow-ups
- **[OPEN-01]** What is Omer Faruk Kuş's GitHub username so we can send the collaborator invitation (`gh api -X PUT repos/ibrahimtemur/cse305-library-management-system/collaborators/<username> -f permission=push`)?
- **[OPEN-02]** Is `231805026@stu.adu.edu.tr` added to Omer Faruk Kuş's GitHub account emails, or should `tools/set-author.ps1` be updated with his primary GitHub email?
- **[OPEN-03]** The workspace is located inside OneDrive (`OneDrive\Masaüstü\LibraryManagementSystem`). Monitor for any OneDrive file-locking during Maven builds or H2 file writes; relocate outside OneDrive if locks occur.
