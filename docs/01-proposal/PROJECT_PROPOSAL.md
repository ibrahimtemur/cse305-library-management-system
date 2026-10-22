<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Project proposal defining problem statement, stakeholders, scope, MoSCoW feature prioritization, domain assumptions, Scrum process, timeline, and risk management for the CSE305 Library Management System.
-->
# Project Proposal — Library Management System (LMS)

- **Course:** CSE305 Software Engineering — Adnan Menderes University (ADU), Department of Computer Engineering
- **Project Title:** Library Management System (LMS)
- **Team Members:**
  - **Ibrahim Temur** — Student No: `231805033`
  - **Omer Faruk Kuş** — Student No: `231805026`
- **Engineering Methodology:** Agile Scrum & Test-Driven Development (TDD)
- **Document Version:** `1.1` (2026-10-22)

---

## 1. Problem Statement & Motivation

Small-scale university, faculty, and departmental libraries frequently rely on manual ledgers or ad-hoc spreadsheets to manage physical book inventories and lending operations. While inexpensive initially, informal tracking introduces critical operational bottlenecks as the collection and student body grow:

1. **Manual Tracking Overhead & Clerical Errors:** Recording checkouts, due dates, renewals, and returns by hand or in unvalidated spreadsheets is slow at the circulation desk and prone to data-entry inconsistencies (e.g., mistyped ISBNs, duplicate member entries, or overwritten return dates).
2. **Unaccounted & Lost Physical Copies:** Without copy-level lifecycle tracking, librarians cannot reliably distinguish between multiple physical copies of the same title. Books that are misplaced, under maintenance, or never returned quietly become "lost" inventory because there is no strict state machine governing copy availability.
3. **Inconsistent Overdue Detection & Fine Calculation:** Calculating overdue days, applying grace periods or member-type policies, and tracking unpaid penalties manually leads to inconsistent enforcement, calculation mistakes, and checkout privileges being granted to members who still hold overdue items.
4. **Lack of Real-Time Catalog Visibility:** Students and academic staff cannot easily check whether a specific book copy is currently on the shelf before visiting the library desk, nor can they place a structured hold/reservation when all copies of a high-demand textbook are checked out.

### Motivation
The goal of the **Library Management System (LMS)** project is to design, implement, and verify a clean, self-contained, web-based application that automates catalog management, copy-level circulation, reservation queues, and deterministic overdue fine calculation. From a software engineering perspective (CSE305), this domain provides a rich, realistic problem space for applying **Agile Scrum**, **GoF and GRASP Object-Oriented Design Patterns**, **UI-First Prototyping (Stitch MCP)**, and **Test-Driven Development (JUnit 5)**.

---

## 2. Stakeholders & User Roles

The system serves three distinct user roles with clearly separated responsibilities and permissions:

| Role | Stakeholder Profile | Core Responsibilities & Capabilities |
|---|---|---|
| **Librarian / Admin** (`ROLE_LIBRARIAN`) | Library circulation staff and system administrator | - Manage the bibliographic catalog (add, update, archive books) and import metadata via Open Library.<br>- Register and manage physical book copies (`AVAILABLE`, `LOANED`, `RESERVED`, `LOST`, `MAINTENANCE`).<br>- Register, update, and activate/suspend library members.<br>- Execute circulation desk operations: issue loans (checkout), process returns, and approve renewals.<br>- Monitor overdue loans, calculate/collect/waive overdue fines, and view operational dashboard metrics. |
| **Member** (`ROLE_MEMBER`) | University students and academic staff borrowing books | - Search and filter the book catalog by title, author, ISBN, or subject category.<br>- View real-time copy availability and shelf status.<br>- View personal active loans, due dates, historical borrowing records, and accrued overdue fines.<br>- Request loan renewals and place holds/reservations on titles when all copies are currently checked out. |
| **Guest (Optional)** (`ROLE_GUEST`) | Unauthenticated visitor browsing the catalog | - Browse and search the public bibliographic catalog and inspect copy availability in read-only mode.<br>- Cannot borrow books, place reservations, or view member-specific circulation data without signing in. |

---

## 3. Project Scope

### 3.1 In-Scope
- **Bibliographic Catalog Management:** Full CRUD operations for book titles, authors, categories/subjects, and ISBN-13 identifiers, seeded with real bibliographic metadata from the public **Open Library API**.
- **Physical Copy Inventory Tracking:** One-to-many relationship between a `Book` title and its physical `BookCopy` instances, each tracked by a unique barcode/copy code and explicit lifecycle state.
- **Member Management:** Registration and lifecycle management (`ACTIVE`, `SUSPENDED`) for synthetic student and academic staff profiles.
- **Core Circulation Engine:** Issuing loans with policy-driven due dates, validating member eligibility and copy state prior to checkout, processing returns, and handling loan renewals.
- **Automated Overdue & Fine Management:** Deterministic calculation of overdue days and monetary penalties upon return or periodic inspection, plus recording fine payments or librarian waivers.
- **Hold / Reservation Queue:** Allowing eligible members to queue for a book when zero copies are `AVAILABLE`, and automatically prioritizing the queue upon book return.
- **Role-Based Web Interface:** Responsive server-side rendered web views designed first with **Stitch MCP** and implemented with **Spring MVC + Thymeleaf**.

### 3.2 Out-of-Scope
- **Real University IT / SIS Integration:** No connection to Adnan Menderes University's live Student Information System (OBIS/OBS), LDAP, or institutional Single Sign-On (SSO).
- **Real Payment Gateways:** No integration with banking APIs or credit card processors; fine settlements are recorded as manual desk payments within the application.
- **Specialized Hardware Drivers:** No proprietary RFID gates or native USB laser scanner drivers (standard keyboard-emulated barcode text input is supported).
- **Digital E-Book Hosting & DRM:** The system manages physical library inventory and circulation only, not PDF/EPUB file streaming or digital rights management.

---

## 4. Prioritized Feature List (MoSCoW Method)

Features are prioritized using the **MoSCoW** framework to guarantee a shippable, well-tested Minimum Viable Product (MVP) by the final deadline while buffering against midterm exam capacity reductions.

### Must Have (Critical for MVP)
- **`M1` — Catalog & Book Copy Management:** Create, edit, search, and filter book titles and manage individual physical copies (`BookCopy`) with status tracking.
- **`M2` — Synthetic Member Management:** Register, view, update, and activate/deactivate library members with distinct member types (e.g., Student vs. Academic Staff).
- **`M3` — Loan Checkout & Return Workflow:** Issue an available book copy to an eligible member with automatic due-date computation; process copy returns and restore availability.
- **`M4` — Automated Overdue Detection & Fine Calculation:** Identify loans past their due date and calculate accrued fines deterministically using pluggable policy rules.
- **`M5` — Role-Based Views & Access Control:** Separate Librarian operational views from Member self-service catalog and loan-tracking views.
- **`M6` — Reproducible Seed Data Pipeline:** Populate the H2 database at startup with Open Library book metadata and strictly synthetic member and circulation records.

### Should Have (High-Value Enhancements Planned for Sprint 2 / MVP)
- **`S1` — Book Reservation (Hold) Queue:** Allow members to place a hold on a title when all copies are currently `LOANED`, transitioning returned copies to `RESERVED` for the next queued member.
- **`S2` — Self-Service / Desk Loan Renewal:** Extend an active loan's due date if the loan is not overdue, has not exceeded the renewal limit, and has no competing reservation.
- **`S3` — Fine Settlement & Waiver Recording:** Allow librarians to mark accrued fines as `PAID` or `WAIVED` to restore a member's borrowing eligibility.
- **`S4` — Librarian Operational Dashboard:** Display summary KPIs (total titles/copies, active loans, overdue count, unpaid fine total) and an actionable overdue loans report.

### Could Have (Stretch Goals if Velocity Permits)
- **`C1` — Public Guest Catalog Portal:** Unauthenticated read-only catalog search and availability lookup.
- **`C2` — Live Open Library ISBN Lookup Form:** Auto-populate book title, authors, publication year, and cover thumbnail in the Librarian "Add Book" form by querying Open Library by ISBN.
- **`C3` — CSV Export for Overdue & Inventory Reports:** Downloadable tabular reports for library administrators.

### Won't Have (Explicitly Excluded from This Release)
- **`W1` — Online Credit Card Payment Processing, External SMTP/SMS Gateways, and Multi-Branch Inter-Library Shipping.**

---

## 5. Domain Policy Assumptions (`ASSUMPTION`)

> [!IMPORTANT]
> This project is a standalone academic software engineering system and does **not** claim to represent official Adnan Menderes University (ADU) Central Library regulations. Every domain policy rule below is explicitly documented as an **`ASSUMPTION`** and isolated behind configurable classes/strategies in the software architecture.

| ID | Category | Explicit Assumption Statement |
|---|---|---|
| **`ASSUMPTION-01`** | **Role Unification** | **ASSUMPTION:** In the MVP, the *Librarian* and *System Administrator* responsibilities are unified under a single privileged operational role (`ROLE_LIBRARIAN` / `ROLE_ADMIN`), while *Members* (`ROLE_MEMBER`) have self-service privileges and *Guests* (`ROLE_GUEST`) have optional read-only catalog access. |
| **`ASSUMPTION-02`** | **Member Borrowing Limits** | **ASSUMPTION:** An active `STUDENT` member may hold at most **3 active loans** simultaneously, whereas an `ACADEMIC_STAFF` member may hold at most **5 active loans** simultaneously. |
| **`ASSUMPTION-03`** | **Standard Loan Duration** | **ASSUMPTION:** The standard loan period is **14 calendar days** from the checkout date for `STUDENT` members and **30 calendar days** for `ACADEMIC_STAFF` members. |
| **`ASSUMPTION-04`** | **Loan Renewal Rules** | **ASSUMPTION:** An active loan may be renewed at most **1 time** for an additional standard loan period, provided the loan is not currently overdue and no other member holds an active reservation on that book title. |
| **`ASSUMPTION-05`** | **Overdue Fine Rate & Cap** | **ASSUMPTION:** Overdue loans accrue a flat daily penalty of **5.00 TRY per calendar day** past the due date (with a configurable maximum fine cap per loan, e.g., **250.00 TRY**), calculated deterministically without external banking integration. |
| **`ASSUMPTION-06`** | **Borrowing Eligibility Block** | **ASSUMPTION:** A member who has any currently overdue loan or any unpaid fine balance (`> 0.00 TRY`), or whose membership status is `SUSPENDED`, is blocked from checking out new books or renewing loans until the overdue copy is returned and fines are settled/waived. |
| **`ASSUMPTION-07`** | **Reservation Queue Allocation** | **ASSUMPTION:** Reservations are placed at the *book title* level in First-In, First-Out (FIFO) order; when a physical copy of that title is returned, its state transitions to `RESERVED` for the member at the head of the queue rather than immediately becoming `AVAILABLE` to walk-in borrowers. |
| **`ASSUMPTION-08`** | **Synthetic Identity & Local Auth** | **ASSUMPTION:** All user authentication and member records use local database credentials and 100% synthetic personal data; no real ADU student IDs, emails, or institutional systems are accessed. |
| **`ASSUMPTION-09`** | **Seeded Physical Copies per Title** | **ASSUMPTION:** Each seeded book title is initialized with **1 to 4 physical copies (`BookCopy`)** assigned deterministic synthetic barcode identifiers (e.g., `LMS-COPY-1001`) so multi-copy lending and reservation queues can be demonstrated immediately. |

---

## 6. Agile Scrum Process, Team Roles & Timeline

### 6.1 Scrum Roles & Engineering Hats
Because this is a two-person software engineering team, both members collaborate across the full stack while maintaining clear Scrum accountability and explicitly rotating/applying the five engineering hats defined in `AGENTS.md` (*Product Owner, Architect, Developer, QA Engineer, Reviewer*):

| Scrum / Engineering Role | Assigned Team Member(s) | Primary Responsibilities |
|---|---|---|
| **Product Owner (PO)** | **Ibrahim Temur** (`231805033`) | Owns product vision, prioritizes the Product Backlog (MoSCoW), clarifies domain assumptions, and validates story acceptance criteria. |
| **Scrum Master (SM)** | **Omer Faruk Kuş** (`231805026`) | Facilitates Scrum ceremonies, tracks sprint velocity and midterm capacity buffer, removes technical blockers, and enforces Git/process hygiene. |
| **Developers & Architects** | **Ibrahim Temur** (`231805033`) & **Omer Faruk Kuş** (`231805026`) | Co-design layered architecture and GoF/GRASP patterns, design Stitch UI prototypes, implement Spring Boot + Thymeleaf features, and write JUnit 5 tests (TDD). |
| **QA & Peer Reviewers** | **Ibrahim Temur** (`231805033`) & **Omer Faruk Kuş** (`231805026`) | Cross-review pull/branch merges, verify test coverage (`mvn test`), audit file headers, and validate synthetic data compliance. |

### 6.2 Sprint Cadence & Course Milestone Timeline
The project follows an iterative **Agile Scrum** schedule aligned directly with the CSE305 deliverable deadlines and the university academic calendar:

```mermaid
flowchart LR
    S0["Week 4 (Oct 20):\nGroup & Project Selection\n+ Sprint 0 Foundation"] --> HW1["HW01 — Week 5 (Oct 27):\nProject Proposal &\nSolution Outline"]
    HW1 --> HW2["HW02 — Week 7 (Nov 10):\nInception & Scrum\nProduct Backlog"]
    HW2 --> MID["Weeks 8–9 (Nov 17–28):\nMidterm Exam Window\n(Reduced Capacity)"]
    MID --> HW3["HW03 — Week 11 (Dec 8):\nElaboration & Sprint 1\n(Catalog, Copies, Members)"]
    HW3 --> HW4["HW04 — Week 13 (Dec 22):\nConstruction & Sprint 2\n(Circulation, Fines, Patterns)"]
    HW4 --> HW5["HW05 — Week 15 (Jan 5):\nTransition & Final MVP\n(Reservations, Dashboard, Polish)"]
```

| Milestone / Homework | Course Week | Target Deadline | Key Deliverables & Focus |
|---|---|---|---|
| **Group & Project Selection + Sprint 0** | Week 4 | **October 20–21** *(Done)* | Project group & topic selection (*Library Management System*); toolchain setup (JDK 25 / Java 17 target, Maven 3.9.16 Wrapper, Spring Boot 3.5.16, H2, JUnit 5), Git/GitHub repo, `AGENTS.md`, automation scripts. |
| **HW01 — Project Proposal & Solution Outline** | Week 5 | **October 27** *(Done)* | `PROJECT_PROPOSAL.md` and `SOLUTION_OUTLINE.md` (`docs/01-proposal/`), packaged as `cse305_hw01_231805033_231805026.zip`. |
| **HW02 — Inception Phase** | Week 6–7 | **November 10** | Vision & system context diagram, Personas, Functional/Non-Functional Requirements (Supplementary Specification), Use Cases, Domain Glossary, Business Rules, Themes/Epics/User Stories/Tasks, Sprint Planning, Product Backlog, and PSI/MVP definition (`docs/02-inception/`). |
| **Midterm Exam Period** | Weeks 8–9 | *Nov 17 – Nov 28* | **Reduced Capacity Window (~35% normal velocity):** Focus on lightweight JPA entity modeling, unit test scaffolding, and Open Library seed data preparation without heavy UI sprints. |
| **HW03 — Elaboration / Sprint 1** | Weeks 10–11 | **December 8** | Use-case diagram, system sequence diagrams (SSD), domain/design class diagrams, TDD/Git/Maven plan (`docs/03-design/`), Stitch UI prototypes, and working **Sprint 1** increment (Catalog, Physical Copies, Synthetic Members, Open Library seed data, JUnit 5 tests). |
| **HW04 — Construction / Sprint 2** | Weeks 12–13 | **December 22** | Working **Sprint 2** increment: Circulation Service (Checkout, Return, Renewal), Overdue Detection & Fine Calculation Engine, core GoF/GRASP pattern implementations (*Strategy*, *State*, *Builder/Factory*), librarian circulation UI, and integration tests. |
| **HW05 — Transition / MVP Release** | Weeks 14–15 | **January 5** | Complete **MVP Release (Sprint 3)**: Book Reservation/Hold queue (*Observer*/*State* integration), Fine payment/waiver workflow, Librarian Dashboard & KPIs, Guest catalog view, full regression testing (`mvn test`), sprint retrospectives, and final submission archive (`cse305_hw05_231805033_231805026.zip`). |

### 6.3 Agentic Development Approach

 In alignment with Week 15 of the CSE305 syllabus (*AI-based Software Development Lifecycle*), this project uses a disciplined, human-governed **Agentic Development Approach**:

1. **Division of Responsibilities (AI Agents vs. Human Engineers):**
   - **AI Agent Activities:** Drafting and structuring Markdown documentation, generating UI screen prototypes via the **Stitch MCP** server, writing TDD unit/integration test scaffolding (JUnit 5) and Spring Boot implementation code, and performing automated checklist/code review passes.
   - **Human Engineering Decisions:** Defining project scope and MoSCoW priorities, establishing domain business rules and `ASSUMPTION` boundaries, resolving architectural trade-offs, verifying acceptance criteria, inspecting runtime behavior, and approving merges into the `main` branch.
2. **Governance via `AGENTS.md`:**
   - Every AI session is strictly bound by [`AGENTS.md`](../../AGENTS.md), which enforces:
     - **Role-Based Working "Hats":** Explicit perspective switching across *Product Owner*, *Architect*, *Developer*, *QA Engineer*, and *Reviewer*.
     - **`Plan -> Execute -> Record` Cadence:** Every task begins with an explicit plan in Turkish for human approval before modifying repository files, followed by test verification (`mvn test`) and state updates in [`docs/process/PROJECT_STATE.md`](../process/PROJECT_STATE.md).
     - **Language & Header Rules:** Chat communication with the team occurs in Turkish, while 100% of repository content (code, identifiers, comments, Javadoc, tests, documentation, commits) is written in English and starts with the mandatory CSE305 student authorship header.
3. **Human-in-the-Loop Quality Gates:**
   - **Plan & Merge Gate:** No implementation starts without plan approval, and merging `develop` into `main` requires explicit human authorization.
   - **Cross-Model Review Pass:** Significant code and documentation increments undergo a dedicated `Reviewer` hat pass using a **different AI model** than the model that authored the work, reducing single-model blind spots before human sign-off.
   - **Automated Test Gate:** All production changes must pass `mvn test` (`.\mvnw.cmd test`) against the isolated in-memory H2 test database.
4. **Academic Transparency (`docs/process/ai-usage-log.md`):**
   - Every AI-assisted task is recorded in [`docs/process/ai-usage-log.md`](../process/ai-usage-log.md) with the date, active student name, prompt summary, the exact model selected in the Antigravity model selector, generated outputs, and truthful human review status (`Reviewed by ...` vs. `Pending human review`).
5. **Known Limitations of AI Assistance:**
   - Large language models do not possess intrinsic knowledge of local institutional policies, can hallucinate framework methods or subtly flawed state transitions, lose context across separate chat sessions without structured state files (`PROJECT_STATE.md`), and can over-engineer design patterns unless constrained by human architectural review and automated tests.

---

## 7. Risks & Mitigation Matrix

| Risk ID | Risk Description | Likelihood | Impact | Mitigation Strategy |
|---|---|---|---|---|
| **RISK-01** | **Midterm Exam Capacity Drop (Nov 17–28):** Team availability drops sharply during the two-week university midterm examination period, risking Sprint 1 slippage before the Dec 8 deadline. | High | High | Complete all Inception, Architecture, and Stitch UI design artifacts by **Nov 10**; treat Nov 17–28 as a planned low-velocity buffer (~35% capacity) and scope Sprint 1 stories conservatively around core Catalog & Member CRUD. |
| **RISK-02** | **Shared Computer Git Authorship Mix-Up:** Both team members share a single workstation, creating a risk of committing work under the teammate's Git identity. | Medium | Medium | Enforce the mandatory start-of-session check in `AGENTS.md` and run `tools\set-author ibrahim` or `tools\set-author omer` (`--local` Git scope) prior to every commit. |
| **RISK-03** | **External Open Library API Downtime or Rate Limiting:** Live HTTP requests to `openlibrary.org` could fail or time out during grading or offline demos. | Medium | High | Pre-fetch and version-control the curated Open Library book dataset inside `data/seed/` (JSON/SQL) so application startup and automated tests run 100% deterministically offline, while keeping optional live ISBN lookup gracefully fallback-safe. |
| **RISK-04** | **OneDrive File-Locking on H2 or Maven `target/`:** The workspace resides under a OneDrive-synced path, which can occasionally lock rapidly changing binary files during builds or H2 writes. | Medium | Low | Exclude `target/` and `data/db/` from Git, use in-memory H2 (`jdbc:h2:mem:lms_test`) for all automated JUnit 5 tests, and relocate the local clone outside OneDrive if file-locking occurs. |
| **RISK-05** | **Artificial or Over-Engineered Design Patterns:** Forcing GoF patterns where simple object-oriented code suffices can bloat the codebase and obscure business logic. | Low | Medium | Apply GoF/GRASP patterns strictly where domain variation exists (e.g., *Strategy* for member-type lending/fine policies, *State* for `BookCopy` lifecycle) and document the problem-solution rationale in `docs/03-design/`. |
| **RISK-06** | **Scope Creep on Secondary Features:** Spending excessive time on optional features (Guest portal, live API enrichment, complex charts) could delay core circulation reliability. | Medium | Medium | Enforce strict MoSCoW prioritization: all **Must Have (`M1`–`M6`)** items and their JUnit 5 test suites must pass before starting **Should Have** or **Could Have** stories. |
| **RISK-07** | **Incorrect or Hallucinated AI Output & Over-Reliance on Agents:** AI agents may generate hallucinated APIs, unverified domain rules, or subtle logic defects if outputs are accepted uncritically. | Medium | High | Enforce human review of every artifact, strict Test-Driven Development (`mvn test`), cross-model review passes (using a different model for the `Reviewer` hat than the authoring model), explicit `ASSUMPTION` tagging, and full audit logging in `docs/process/ai-usage-log.md`. |
