<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Supplementary specification defining functional requirements (FR-001..FR-032), non-functional requirements (NFR-001..NFR-012), constraints (CON-001..CON-006), and seed data requirements (DR-001..DR-007).
-->
# Requirements Specification (Supplementary Specification) — Library Management System (LMS)

- **Course:** CSE305 Software Engineering — Adnan Menderes University (ADU)
- **Phase:** Inception (`HW02`)
- **Date:** 2026-10-22

---

## 1. Functional Requirements (`FR-001`..`FR-032`)

Functional requirements are grouped by the **MoSCoW** feature categories established in [`docs/01-proposal/PROJECT_PROPOSAL.md`](../01-proposal/PROJECT_PROPOSAL.md) (`M1`–`M6`, `S1`–`S4`, `C1`–`C3`) and traced directly to the business rules in [`BUSINESS_RULES.md`](BUSINESS_RULES.md) and use cases in [`USE_CASES.md`](USE_CASES.md).

### 1.1 `M1` — Catalog & Book Copy Management (Must Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-001`** | Must Have | **Book Metadata CRUD & Reference Flag:** The system shall allow a Librarian (`ROLE_LIBRARIAN`) to create, update, and archive bibliographic `Book` records identified by a unique, checksum-validated `isbn13`, storing `title`, optional `subtitle`, `authors` (`1..5`), `publisher`, `firstPublishYear`, `category` (from the 11 catalog categories), `subjects`, work-level `pageCount`, `coverId`/`coverUrl`, `openLibraryWorkKey`, and a boolean **`referenceOnly`** flag (`circulating = false`) designating non-circulating reference works (encyclopedias, dictionaries, catalogs). | `BR-014`, `BR-017` | `UC-03` |
| **`FR-002`** | Must Have | **Catalog Search & Filtering:** The system shall allow any user (`ROLE_LIBRARIAN`, `ROLE_MEMBER`, `ROLE_GUEST`) to search the book catalog by partial case-insensitive `title`, `author`, or exact `isbn13`, and filter results by `category`, copy availability (`AVAILABLE`), and circulation type (`referenceOnly`). | `BR-001`, `BR-014` | `UC-01` |
| **`FR-003`** | Must Have | **Book Detail & Copy Availability View:** The system shall display a detailed view for each `Book` showing all bibliographic attributes, a clear `REFERENCE ONLY — NOT FOR LOAN` badge when `referenceOnly == true`, the list of physical `BookCopy` instances (`barcode` and current `status`), and the current active reservation queue length. | `BR-014`, `BR-017` | `UC-01` |
| **`FR-004`** | Must Have | **Physical Copy Registration:** The system shall allow a Librarian to add new physical `BookCopy` instances to an existing `Book` (`isbn13`) with a unique barcode matching the `LMS-COPY-XXXX` convention and an initial status of `AVAILABLE` or `MAINTENANCE`. | `BR-017` | `UC-03` |
| **`FR-005`** | Must Have | **Copy Lifecycle State Machine:** The system shall enforce valid `BookCopy` state transitions (`AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, `LOST`) via the GoF **State** pattern (`BookCopyState`), preventing a copy from being checked out when in `LOANED`, `MAINTENANCE`, or `LOST` state, or from being manually moved to `MAINTENANCE` while `LOANED`. | `BR-015`, `BR-017` | `UC-03`, `UC-05`, `UC-06`, `UC-09` |

### 1.2 `M2` — Synthetic Member Management (Must Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-006`** | Must Have | **Synthetic Member Registration:** The system shall allow a Librarian to register synthetic library members with a unique `memberId` (`SYN-STU-XXXX`, `SYN-STF-XXXX`, or `SYN-ADM-XXXX`), `firstName`, `lastName`, `@synthetic.lms.local` `email`, `memberType` (`STUDENT`, `ACADEMIC_STAFF`, or `ADMINISTRATIVE_STAFF`), `department`, `status` (`ACTIVE` or `SUSPENDED`), and `registeredOn` date. | `BR-002`, `BR-018` | `UC-04` |
| **`FR-007`** | Must Have | **Member Profile Update & Suspension:** The system shall allow a Librarian to edit member profile attributes and toggle membership `status` between `ACTIVE` and `SUSPENDED` (providing that a member with active loans cannot be suspended until all active loans are resolved, or suspending immediately blocks any further checkouts/renewals). | `BR-011`, `BR-018` | `UC-04` |
| **`FR-008`** | Must Have | **Librarian Member Circulation Inspection:** The system shall allow a Librarian to inspect any member's complete circulation profile, displaying their `memberType`, maximum quota (`7` for `ACADEMIC_STAFF`; `3` for `ADMINISTRATIVE_STAFF` and `STUDENT`), active loans, historical loans, post-renewal cooldown timers, active reservations, unpaid fines/lost-book charges, and current borrowing eligibility status. | `BR-002`, `BR-006`, `BR-011` | `UC-04`, `UC-10` |

### 1.3 `M3` — Loan Checkout & Return Workflow (Must Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-009`** | Must Have | **Member Checkout Eligibility & Personal ID Validation:** Prior to creating a loan at the circulation desk, the system shall verify that: (1) the Librarian identifies the borrower in person by their own university ID card number (`memberId`; proxy borrowing on behalf of another person is prohibited), (2) `member.status == ACTIVE`, (3) the member's current `ACTIVE` loan count is strictly less than their confirmed limit (`7` for `ACADEMIC_STAFF`, `3` for `ADMINISTRATIVE_STAFF`, `3` for `STUDENT`), (4) the member holds zero overdue active loans, (5) the member has zero `UNPAID` fines or lost-book charges (`amount > 0.00 TRY`), and (6) the member is not within the 1-month (`30-day`) post-renewal re-borrowing cooldown for that book title (`isbn13`). | `BR-002`, `BR-006`, `BR-011`, `BR-016` | `UC-05` |
| **`FR-010`** | Must Have | **Book Copy Checkout Eligibility Validation:** Prior to checkout, the system shall verify that: (1) the parent `Book` is not marked `referenceOnly == true` (encyclopedias, dictionaries, and catalogs cannot be loaned), and (2) the physical `BookCopy` is either `AVAILABLE`, or `RESERVED` exclusively for the requesting member who holds the `READY` reservation at `queuePosition == 1` with `readyCopyBarcode == copy.barcode`. | `BR-013`, `BR-014`, `BR-017` | `UC-05` |
| **`FR-011`** | Must Have | **Transactional Loan Checkout Execution:** When both member and copy validations pass, the system shall atomically create a `Loan` record (`loanId`, `memberId`, `copyBarcode`, `checkoutDate = currentDate`, `dueDate = checkoutDate + 30 days` resolved via `LoanPolicyStrategy`, `returnDate = null`, `status = ACTIVE`, `renewalCount = 0`, `renewedOn = null`), transition the `BookCopy` status to `LOANED`, and (if fulfilling a `READY` reservation) mark that reservation fulfilled and advance the remaining queue positions. | `BR-002`, `BR-003`, `BR-013`, `BR-016`, `BR-017` | `UC-05` |
| **`FR-012`** | Must Have | **Transactional Book Copy Return Execution:** When a Librarian processes a returned `copyBarcode`, the system shall locate its single `ACTIVE` `Loan`, set `returnDate = currentDate` and `status = RETURNED`, finalize any overdue fine calculation up to `returnDate`, and transition the `BookCopy` status to `RESERVED` (if at least one `WAITING` reservation exists for that `isbn13`) or to `AVAILABLE` (if no `WAITING` reservation exists). | `BR-007`, `BR-008`, `BR-013`, `BR-017` | `UC-06` |
| **`FR-013`** | Must Have | **Post-Renewal 1-Month Re-Borrowing Cooldown Enforcement:** Whenever a returned loan had its duration extended (`renewalCount >= 1`), the system shall enforce a 1-month (`30 calendar days` under `ASSUMPTION-12`) cooldown window (`returnDate` through `returnDate + 29 days` inclusive) during which the same `memberId` cannot check out or reserve any copy of the same `isbn13`. | `BR-006` | `UC-05`, `UC-06` |

### 1.4 `M4` — Automated Overdue Detection & Fine Calculation (Must Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-014`** | Must Have | **Deterministic Overdue Days Calculation:** The system shall evaluate a loan as overdue whenever `effectiveEndDate > dueDate` (with zero grace period; a loan where `effectiveEndDate == dueDate` is not overdue), where `effectiveEndDate` is `lostReportedOn` (if reported lost), else `returnDate` (if returned), else `currentDate`. Overdue days are computed as `overdueDays = max(0, (effectiveEndDate - dueDate).days)`. | `BR-007`, `BR-015` | `UC-06`, `UC-09`, `UC-11` |
| **`FR-015`** | Must Have | **Daily Overdue Fine Calculation (`0.25 TRY/day`, No Cap):** For every loan with `overdueDays > 0`, the system shall calculate the overdue fine via `FineCalculationStrategy` using the confirmed ADU tariff of `0.25 TRY` (25 kuruş) per overdue calendar day with **no maximum cap**: `amount = 0.25 * overdueDays` (in `TRY`), creating or updating the loan's `Fine` record (`fineId`, `loanId`, `memberId`, `overdueDays`, `amount`, `currency = "TRY"`, `status = UNPAID`, `assessedOn = effectiveEndDate`). | `BR-008`, `BR-009`, `BR-010` | `UC-06`, `UC-09`, `UC-11` |

### 1.5 `M5` — Authentication, Role-Based Views & Member Self-Service (Must Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-016`** | Must Have | **Local Session Authentication (Log In / Log Out):** The system shall provide a login screen and logout action authenticating Librarians (by `username`, e.g., `syn-lib-0001`) and Members (by `memberId` or synthetic `email`, e.g., `SYN-STU-0001` / `syn-stu-0001@synthetic.lms.local`) against BCrypt-hashed synthetic demo passwords initialized at application startup (`ASSUMPTION-16`). | `BR-001`, `BR-018` | `UC-02` |
| **`FR-017`** | Must Have | **Role-Based Access Control (RBAC):** The system shall restrict catalog/copy CRUD, member management, circulation desk checkout/return, fine settlement/waiver, lost-copy assessment, and operational dashboard endpoints exclusively to `ROLE_LIBRARIAN`, while granting `ROLE_MEMBER` access to self-service views/actions and `ROLE_GUEST` read-only access to public catalog pages. | `BR-001` | `UC-02` |
| **`FR-018`** | Must Have | **Member Self-Service Portal:** The system shall provide authenticated `ROLE_MEMBER` users with a personal self-service view displaying: (1) their current active loans, due dates, renewal eligibility, and any accruing overdue fine; (2) their historical returned loans and post-renewal cooldown dates; (3) their unpaid/paid/waived fines and lost-book charges; (4) their active reservations (`WAITING` / `READY` with `queuePosition` and pickup expiration date); and (5) in-app notifications when a reserved copy becomes `READY` for pickup. | `BR-001`, `BR-010`, `BR-013` | `UC-10` |

### 1.6 `M6` — Reproducible Seed Data Pipeline & Startup Loader (Must Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-019`** | Must Have | **Offline Seed Dataset Loader & Demo Credential Initializer:** On application startup (when the H2 database is empty), the system shall load the versioned JSON seed files under `data/seed/` (`books-openlibrary.json`, `members.json`, `librarians.json`, `copies.json`, `loans.json`, `fines.json`, `reservations.json` — documented in [`data/README.md`](../../data/README.md)), initialize BCrypt-hashed synthetic demo passwords for seeded accounts, and support optional date-shifting relative to `REFERENCE_DATE` so seeded active, due-soon, and overdue scenarios remain fresh offline. | `BR-017`, `BR-018` | System Startup |

### 1.7 `S1` — Book Reservation (Hold) Queue & Pickup Hold (Should Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-020`** | Should Have | **Title-Level Reservation Placement & Precondition Check:** The system shall allow an authenticated `ACTIVE` member (via self-service) or a Librarian to place a reservation on a book title (`isbn13`) **only when**: (1) the book is not `referenceOnly`, (2) **zero physical copies** of that title are currently `AVAILABLE`, (3) the member has no borrowing blocks (`BR-011`) or active post-renewal cooldown on that title (`BR-006`), (4) the member does **not** currently hold an `ACTIVE` loan for any copy of that title, and (5) the member does **not** already hold a `WAITING` or `READY` reservation for that title. | `BR-011`, `BR-012`, `BR-014` | `UC-08` |
| **`FR-021`** | Should Have | **FIFO Queue Ordering:** The system shall assign each new reservation on an `isbn13` the next sequential `queuePosition` (`1..n`) ordered strictly First-In, First-Out (FIFO) by `createdOn`, with initial `status = WAITING` and `readyCopyBarcode = null`. | `BR-012` | `UC-08` |
| **`FR-022`** | Should Have | **Automatic Hold Promotion, In-App Notification & 2–3 Day Pickup Window:** When a copy of a book with at least one `WAITING` reservation is returned (`FR-012`), the system (via the GoF **Observer** pattern) shall promote the `queuePosition == 1` reservation to `status = READY`, set `readyCopyBarcode = copy.barcode`, create an **in-app notification** for that member (`ASSUMPTION-13`), and hold the copy in `RESERVED` state for the confirmed **2–3 day pickup window** (`3 calendar days` target under `ASSUMPTION-13`). | `BR-013` | `UC-06`, `UC-08`, `UC-10` |
| **`FR-023`** | Should Have | **Reservation Cancellation & Hold Expiration Reallocation:** The system shall allow a member (self-service) or Librarian to cancel an active reservation—and shall expire a `READY` reservation if unclaimed after `3 calendar days`—removing it from the active queue, decrementing `queuePosition` for all trailing `WAITING` reservations on that `isbn13`, and (if the cancelled/expired reservation was `READY`) either reallocating its `readyCopyBarcode` to the new `queuePosition == 1` reservation or transitioning the copy back to `AVAILABLE`. | `BR-012`, `BR-013` | `UC-08` |

### 1.8 `S2` — Self-Service / Desk Loan Renewal (Should Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-024`** | Should Have | **Self-Service & Desk Loan Renewal:** The system shall allow an authenticated Member (for their own loan) or a Librarian to extend an `ACTIVE` loan once (`renewalCount` transitions from `0` to `1`, `renewedOn = currentDate`, `dueDate` extended by `+30 calendar days`), provided that: (1) `renewalCount == 0`, (2) the loan is not overdue (`currentDate <= dueDate`), (3) no other member holds an active (`WAITING` or `READY`) reservation on that book's `isbn13`, and (4) the borrower is `ACTIVE` and has no overdue loans or `UNPAID` fines (`BR-011`). | `BR-003`, `BR-004`, `BR-005`, `BR-011` | `UC-07` |

### 1.9 `S3` — Fine Settlement, Waiver & Lost-Copy Handling (Should Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-025`** | Should Have | **Desk Fine Payment Recording (`PAID`):** The system shall allow a Librarian (`ROLE_LIBRARIAN`) to settle an `UNPAID` fine or lost-book charge on a returned/resolved loan by marking `status = PAID`, setting `settledOn = currentDate`, and recording the Librarian's `username` in `settledBy`. | `BR-010`, `BR-011` | `UC-09` |
| **`FR-026`** | Should Have | **Administrative Fine Waiver Recording (`WAIVED`):** The system shall allow a Librarian (`ROLE_LIBRARIAN`) to waive an `UNPAID` fine on a returned/resolved loan by marking `status = WAIVED`, setting `settledOn = currentDate`, and recording `settledBy`, restoring the member's borrowing eligibility once all overdue active loans and remaining `UNPAID` balances are cleared. | `BR-010`, `BR-011` | `UC-09` |
| **`FR-027`** | Should Have / Could Have | **Lost Copy Petition, Fine Freeze & 2x Valuation Assessment:** The system shall allow a Librarian to record a member's lost-book petition date (`lostReportedOn`) on an `ACTIVE` loan, which immediately **halts daily overdue fine accrual as of `lostReportedOn`** and starts a **1-month (`30 calendar days`)** replacement window. If the member supplies a replacement copy within 30 days, the loan is closed (`RETURNED`); if not replaced within 30 days, the Librarian enters the Valuation Commission's determined book value (`appraisedValue` in `TRY`), the system bills **twice that value (`2.00 * appraisedValue`)** in addition to any overdue fine accrued up to `lostReportedOn`, and transitions the `BookCopy` to `LOST`. | `BR-005`, `BR-015`, `BR-017` | `UC-09` |

### 1.10 `S4` — Librarian Operational Dashboard (Should Have)

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-028`** | Should Have | **Operational KPI Summary Cards:** The system shall provide a Librarian Dashboard displaying real-time metrics: total distinct book titles, total physical copies broken down by state (`AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, `LOST`), active loan count, due-soon loan count (due within `0..3` days), overdue active loan count, and total `UNPAID` fine balance in `TRY`. | `BR-001`, `BR-007`, `BR-008` | `UC-11` |
| **`FR-029`** | Should Have | **Actionable Overdue Loans & Unpaid Fines Report:** The system shall display a prioritized table of all overdue active loans and `UNPAID` fines on the Librarian Dashboard, showing `loanId`, `memberId`, member name, `copyBarcode`, book `title`, `dueDate`, `overdueDays`, accrued `amount` (`0.25 TRY/day`), and quick links to the member profile or return/settlement desk. | `BR-007`, `BR-008`, `BR-011` | `UC-11` |

### 1.11 `C1`–`C3` — Could Have Stretch Enhancements

| ID | Priority | Requirement Description | Linked Business Rules | Linked Use Cases |
|---|---|---|---|---|
| **`FR-030`** | Could Have (`C1`) | **Public Guest Catalog Portal:** The system shall allow unauthenticated visitors (`ROLE_GUEST`) to access the catalog search, category filter, and book detail pages in read-only mode without exposing member names, loan records, or circulation actions. | `BR-001`, `BR-014` | `UC-01` |
| **`FR-031`** | Could Have (`C2`) | **Live Open Library ISBN Lookup Form Helper:** In the Librarian "Add Book" form, the system shall provide an optional "Fetch by ISBN" button (`OpenLibraryCatalogAdapter`) that queries Open Library to pre-fill title, authors, publication year, and cover URL, degrading gracefully to manual entry when offline. | `BR-001` | `UC-03` |
| **`FR-032`** | Could Have (`C3`) | **CSV Export for Overdue & Inventory Reports:** The system shall allow a Librarian to download the current overdue loans report and physical copy inventory table as UTF-8 CSV files. | `BR-001` | `UC-11` |

---

## 2. Non-Functional Requirements (`NFR-001`..`NFR-012`)

> [!NOTE]
> All quantitative performance and timing thresholds below (`< 200 ms`, `< 10 seconds`, etc.) are engineering **design targets (`ASSUMPTION`)**, not pre-measured benchmarks.

| ID | Category | Non-Functional Requirement Statement | Verification / Target Basis |
|---|---|---|---|
| **`NFR-001`** | **Usability (UI-First)** | All user interface screens shall be designed first as HTML prototypes using the **Stitch MCP** server and saved under `docs/03-design/ui/` prior to implementing Spring MVC + Thymeleaf templates (`AGENTS.md` §6). | Artifact inspection in `docs/03-design/ui/` |
| **`NFR-002`** | **Usability (Desk Efficiency)** | Circulation desk forms shall accept keyboard-entered or USB barcode-scanner-emulated `memberId` (`SYN-STU-*`, `SYN-STF-*`, `SYN-ADM-*`) and `copyBarcode` (`LMS-COPY-*`) values and display clear, human-readable domain rule violation banners (referencing the violated rule, e.g., quota reached, overdue block, reference-only copy, or post-renewal 1-month cooldown). | MockMvc & browser UI review |
| **`NFR-003`** | **Reliability & ACID Integrity** | All multi-entity circulation operations (checkout, return with hold promotion, renewal, fine settlement, lost-copy assessment) shall execute inside declarative Spring `@Transactional` boundaries so that partial failures roll back cleanly without leaving inconsistent `Loan`, `BookCopy`, `Fine`, or `Reservation` states. | `@SpringBootTest` transactional integration tests |
| **`NFR-004`** | **Offline Runtime Reliability** | The application and its automated test suite (`.\mvnw.cmd test`) shall run **100% offline** with zero mandatory dependencies on external internet services, Open Library uptime, or external database servers. | Offline execution of `.\mvnw.cmd test` |
| **`NFR-005`** | **Performance (Query & Desk Latency)** | **Target (`ASSUMPTION`):** Local catalog search/filter queries and single-copy checkout, renewal, or return requests shall complete within a target latency of **`< 200 ms`** (server-side processing time on the reference Windows 11 / JDK 25 LTS workstation) against the embedded H2 dataset seeded from `data/seed/*.json`. | Integration test timing assertions (Target / `ASSUMPTION`) |
| **`NFR-006`** | **Performance (Startup & Seed Initialization)** | **Target (`ASSUMPTION`):** Application startup, JPA schema initialization, and initial loading of `data/seed/*.json` into H2 shall complete within a target duration of **`< 10 seconds`** on the reference development workstation. | Startup log verification (Target / `ASSUMPTION`) |
| **`NFR-007`** | **Security (Role-Based Authorization & Validation)** | Every HTTP controller endpoint shall enforce role-based access rules (`ROLE_LIBRARIAN`, `ROLE_MEMBER`, `ROLE_GUEST`) and validate all form DTO inputs using Jakarta Bean Validation (`@Valid`, `@NotBlank`, `@Pattern`, ISBN-13 checksum validation) to prevent unauthorized actions, SQL injection, and cross-site scripting (XSS via Thymeleaf default escaping). | `@WebMvcTest` security & validation tests |
| **`NFR-008`** | **Security (Credential & Secret Hygiene)** | **No real or secret passwords, API keys, or tokens are stored anywhere in the repository (`AGENTS.md` §7);** the seed JSON files (`data/seed/*.json`) contain zero password fields, and documented synthetic demo passwords for local testing are hashed (e.g., using **BCrypt**) and loaded into the database at application startup (`ASSUMPTION-16`, `OPEN-05`). | Git repository scan & seed unit tests (`test_seed_data.py`) |
| **`NFR-009`** | **Privacy & Synthetic Data Compliance** | `100%` of member and librarian records in `data/seed/` and automated tests shall be strictly synthetic (`Faker('tr_TR')` fictional names, `SYN-STU-*`/`SYN-STF-*`/`SYN-ADM-*` IDs, `@synthetic.lms.local` non-routable email domain), with zero real ADU student/staff names, student numbers, national IDs (TCKN), or phone numbers (`AGENTS.md` §7). | Verified by `tools/data/tests/test_seed_data.py` |
| **`NFR-010`** | **Maintainability & Architectural Layering** | The codebase (`edu.adu.lms`) shall adhere strictly to the 5-tier layered architecture (`Thymeleaf UI -> Controller -> Service/Policy -> Repository -> H2`) and encapsulate domain variability using justified **GoF & GRASP** design patterns (*Strategy* for `LoanPolicyStrategy` & `FineCalculationStrategy`, *State* for `BookCopyState`, *Observer* for return/hold events, *Factory/Builder* for aggregate creation, *Adapter* for Open Library metadata). | Code review & `docs/03-design/` verification |
| **`NFR-011`** | **Testability (TDD)** | Business rules (`BR-001`..`BR-018`) and boundary conditions (e.g., quota boundaries `3` and `7`, exact due date `0` overdue days vs. `1` overdue day, `0.25 TRY/day` fine arithmetic, 30-day post-renewal cooldown boundary, FIFO queue promotion, lost-copy fine freeze) shall be verified by automated JUnit 5 unit and integration tests running against isolated in-memory H2 (`jdbc:h2:mem:lms_test`), complemented by the offline Python `unittest` suite for `data/seed/`. | `.\mvnw.cmd test` & `python -m unittest` |
| **`NFR-012`** | **Portability & OneDrive Safety** | The project shall build and run reproducibly on **Windows 11 + PowerShell** using `.\mvnw.cmd` and `tools\*.cmd` with Java 17 bytecode compatibility (`--release 17`, running on JDK 17+ / JDK 25 LTS), keeping binary build artifacts (`target/`) and runtime H2 files (`data/db/`) gitignored to avoid OneDrive file-locking issues. | Clean build via `.\mvnw.cmd test` |

---

## 3. System & Project Constraints (`CON-001`..`CON-006`)

| ID | Constraint Type | Constraint Description |
|---|---|---|
| **`CON-001`** | **Academic Header & Language Policy** | All repository files (code, Markdown docs, tests, scripts, commits) must be written in **English** and start with the mandatory CSE305 student header (`Ibrahim Temur, Omer Faruk Kuş — 231805033, 231805026`), with the documented exception of machine-generated `data/seed/*.json` files (`AGENTS.md` §1–§2). |
| **`CON-002`** | **Books-Only Material Scope (Periodicals & Theses Excluded)** | Although official ADU library rules define lending rules for periodicals (2 non-latest issues for 2 days) and prohibit lending unpublished theses, **periodicals/serials and unpublished theses are Out of Scope**. The system manages books only (including non-circulating reference books such as encyclopedias, dictionaries, and catalogs via `referenceOnly`). |
| **`CON-003`** | **No Live ADU Institutional Integration** | Integration with ADU OBIS/OBS, institutional LDAP/SSO, or physical smart-card hardware is prohibited and out of scope; the personal university ID card requirement (`BR-016`) is enforced operationally at the Librarian desk using `memberId`. |
| **`CON-004`** | **No External Financial or Messaging Gateways** | Integration with credit-card payment processors, banking APIs, SMTP email servers, or SMS gateways is out of scope; fines are settled at the desk (`PAID`/`WAIVED`) and hold notifications are rendered in-app (`ASSUMPTION-13`). |
| **`CON-005`** | **Shared Workstation Git Authorship** | Because both team members share one computer, `tools\set-author.cmd <ibrahim|omer>` must be executed before every commit to set `--local` Git authorship without ever altering `--global` Git config (`AGENTS.md` §3). |
| **`CON-006`** | **Protected `main` Branch & Packaging Rule** | All feature and documentation work occurs on short-lived branches merged into `develop`; `main` is updated only with explicit user approval, and homework archives (`cse305_hwNN_231805033_231805026.zip`) must be uploaded individually by both team members to ADUZEM (`AGENTS.md` §5, §8). |

---

## 4. Data Requirements (`DR-001`..`DR-007`)

The application's initial dataset is stored as UTF-8 (no BOM), LF-terminated JSON arrays under [`data/seed/`](../../data/seed/) and generated deterministically by the scripts in [`tools/data/`](../../tools/data/). Full schema details, Open Library CC0 licensing, regeneration commands, and validation suites are documented in [`data/README.md`](../../data/README.md).

> [!IMPORTANT]
> **Upcoming Seed Alignment with Confirmed ADU Rules (`OPEN-06`):** Do not treat the initial snapshot row counts in `data/seed/*.json` as fixed constants. The current seed files were generated under the initial `HW01` assumptions (`14/30`-day periods, `3/5` limits, `5.00 TRY/day` fine with `250.00 TRY` cap, and `STUDENT`/`ACADEMIC_STAFF` only) and will be regenerated to reflect the confirmed ADU rules (`30`-day period for all types, `7/3/3` limits including `ADMINISTRATIVE_STAFF`, `0.25 TRY/day` fine with no cap, `referenceOnly` books, and post-renewal cooldowns) as tracked in `OPEN-06` in [`docs/process/PROJECT_STATE.md`](../process/PROJECT_STATE.md).

| Data Req ID | Seed File Path | Primary Natural Key | Foreign Keys & Required Domain Fields |
|---|---|---|---|
| **`DR-001`** | [`data/seed/books-openlibrary.json`](../../data/seed/books-openlibrary.json) | `isbn13` (13-digit valid ISBN-13) | `title`, `subtitle` (nullable), `authors` (array of `1..5` strings), `publisher`, `firstPublishYear`, `category` (one of 11 categories), `subjects` (`1..5` strings), `pageCount` (work-level median), `coverId`, `coverUrl`, `openLibraryWorkKey`, plus `referenceOnly` (`false` by default; `true` for encyclopedias/dictionaries/catalogs per `BR-014`). |
| **`DR-002`** | [`data/seed/copies.json`](../../data/seed/copies.json) | `barcode` (`LMS-COPY-1001`..) | `isbn13` (FK -> `books-openlibrary.json`), `status` (`AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, `LOST`). Each seeded title has `1..4` physical copies (`ASSUMPTION-09`). |
| **`DR-003`** | [`data/seed/members.json`](../../data/seed/members.json) | `memberId` (`SYN-STU-0001`.., `SYN-STF-0001`.., `SYN-ADM-0001`..) | `firstName`, `lastName`, `email` (`*@synthetic.lms.local`), `memberType` (`STUDENT`, `ACADEMIC_STAFF`, `ADMINISTRATIVE_STAFF`), `status` (`ACTIVE`, `SUSPENDED`), `department`, `registeredOn` (`YYYY-MM-DD`). Zero real personal data (`NFR-009`). |
| **`DR-004`** | [`data/seed/librarians.json`](../../data/seed/librarians.json) | `username` (`syn-lib-0001`..) | `displayName`, `email` (`*@synthetic.lms.local`), `role` (`ROLE_LIBRARIAN`). Contains **no password or credential field** in JSON; demo passwords are hashed at startup (`NFR-008`, `OPEN-05`). |
| **`DR-005`** | [`data/seed/loans.json`](../../data/seed/loans.json) | `loanId` (`LOAN-0001`..) | `memberId` (FK -> `members.json`), `copyBarcode` (FK -> `copies.json`), `checkoutDate`, `dueDate` (`checkoutDate + 30 * (1 + renewalCount)`), `returnDate` (`null` while `ACTIVE`), `status` (`ACTIVE`, `RETURNED`), `renewalCount` (`0` or `1`), `renewedOn` (nullable), and optional `lostReportedOn` (nullable, `BR-015`). |
| **`DR-006`** | [`data/seed/fines.json`](../../data/seed/fines.json) | `fineId` (`FINE-0001`..) | `loanId` (FK -> `loans.json`, at most one overdue fine per loan), `memberId` (FK -> `members.json`), `overdueDays`, `amount` (2-decimal string, `0.25 * overdueDays`), `currency` (`"TRY"`), `status` (`UNPAID`, `PAID`, `WAIVED`), `assessedOn`, `settledOn` (nullable), `settledBy` (FK -> `librarians.json` `username`, nullable). |
| **`DR-007`** | [`data/seed/reservations.json`](../../data/seed/reservations.json) | `reservationId` (`RES-0001`..) | `isbn13` (FK -> `books-openlibrary.json`), `memberId` (FK -> `members.json`), `queuePosition` (`1..n`, FIFO by `createdOn`), `status` (`WAITING`, `READY`), `createdOn`, `readyCopyBarcode` (FK -> `copies.json` `RESERVED` copy when `status == READY`, else `null`). |
