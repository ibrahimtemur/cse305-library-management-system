<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: User stories LMS-001..LMS-021 with Given/When/Then acceptance criteria, MoSCoW priority, Fibonacci points, human-hour estimates, and target sprints for the HW02 Scrum backlog.
-->
# User Stories — Library Management System (LMS)

- **Version:** 1.0 (Product Owner approved 2026-11-07) — 2026-11-07
- **Product Owner:** Ibrahim Temur · **Scrum Master:** Omer Faruk Kuş
- **Sources:** [`REQUIREMENTS.md`](REQUIREMENTS.md) (`FR`/`NFR`), [`USE_CASES.md`](USE_CASES.md) (`UC`), [`BUSINESS_RULES.md`](BUSINESS_RULES.md) (`BR`), [`PERSONAS.md`](PERSONAS.md)
- **Backlog and totals:** [`PRODUCT_BACKLOG.md`](PRODUCT_BACKLOG.md) (numbers are produced by `tools/agile/validate_backlog.py`; the `Meta` lines below are checked against it)

> [!NOTE]
> **Estimation convention.** `Human h` is human effort only (steering AI agents, review, manual testing, documents); agent working time is not counted. Points are Fibonacci (`88` points total across `21` stories; merging the three story pairs and splitting `LMS-015` into `LMS-015` + `LMS-021` preserve the `88`-point baseline without point inflation). Human hours reflect ~`0.40 x` classic coding effort plus fixed per-story human review/manual-test/documentation overhead, the `4.0 h` human design spike (`LMS-008`), and PO-approved safety buffers on `LMS-005` (`7.5 h`) and `LMS-007` (`9.0 h`), **to be re-calibrated with the actual Sprint 1 hours**. `Agent sessions` is the expected number of heavy AI chats, relevant for the weekly AI quota risk. Merged stories keep their acceptance criteria separate (labelled AC-a, AC-b, ...).

> [!NOTE]
> **Stitch design step.** Every story marked "UI" starts with a Stitch MCP design task (screen exported to `docs/03-design/ui/`) *before* any Thymeleaf template is written (`NFR-001`).

**Actors:** Librarian (`ROLE_LIBRARIAN`), Member (`ROLE_MEMBER`: `STUDENT`, `ACADEMIC_STAFF`, `ADMINISTRATIVE_STAFF`), Guest (`ROLE_GUEST`), Developer team.

---

## Epic E1 — Data Import and Seed Loader

### LMS-001 — Domain model and persistence skeleton
**Meta:** E1 | Must | 3 pts | 3.5 h (classic 6) | 2 agent sessions | S1 | FR: enabler (`DR-001`..`DR-007`, `NFR-010`) | UC: — | BR: `BR-017`

**As a** developer, **I want** the JPA entities, enumerations, and repositories of the confirmed domain model on an H2 database, **so that** every later story builds on one persistent model that matches seed v2.

- **AC-1:** *Given* the application starts with an empty H2 database, *when* the schema is generated, *then* tables exist for `Book`, `BookCopy`, `Member`, `Librarian`, `Loan`, `Fine`, `Reservation` with the HW01 attributes and enumerations (`BR-017` states, `Loan.status` incl. `LOST`).
- **AC-2:** *Given* a `BookCopy` bound to an `ACTIVE` loan, *when* a second `ACTIVE` loan for the same `copyBarcode` is saved, *then* the save is rejected (single-loan invariant, `BR-017`).
- **AC-3:** *Given* `./mvnw -q test`, *when* the persistence tests run, *then* they pass offline (`NFR-004`).

### LMS-002 — Seed loader with date shifting
**Meta:** E1 | Must | 5 pts | 5 h (classic 10) | 3 agent sessions | S1 | FR: `FR-019` | UC: System Startup | BR: `BR-017`, `BR-018`

**As a** librarian demo user, **I want** the application to load seed v2 on first startup and shift all dates relative to the application start day (`OPEN-04`), **so that** active, due-soon, and overdue loan scenarios never go stale.

- **AC-1:** *Given* an empty database, *when* the application starts, *then* it loads `782` books, `1,706` copies, `60` members (`40/10/10`), `3` librarians, `164` loans, `47` fines, `22` reservations from `data/seed/` (`FR-019`, counts verified by a test against the JSON files).
- **AC-2:** *Given* seed dates are relative to `REFERENCE_DATE = 2026-10-22`, *when* the application starts on day D, *then* every date in loans, fines, reservations, and members is shifted by `D - REFERENCE_DATE` so that overdue day counts are preserved (`BR-007`).
- **AC-3:** *Given* the database is already populated, *when* the application restarts, *then* the loader does nothing (idempotent).
- **AC-4:** *Given* the seed contains a `LOST` loan, *when* it is loaded, *then* `returnDate` stays `null` and `lostReportedOn` is shifted like the other dates (`BR-015`, `BR-017`).

### LMS-008 — Design spike: compensation tracking and reservation terminal states
**Meta:** E8 | Must | 2 pts | 4 h (classic 4) | 1 agent session | S1 | FR: supports `FR-022`, `FR-023`, `FR-027` (design only) | UC: UC-08, UC-09 | BR: `BR-013`, `BR-015`

**As a** product team, **I want** a timeboxed design decision for the two HW01 known limitations, **so that** Sprint 3 stories can be built without rework.

- **AC-1:** *Given* HW01 defers lost-copy compensation payment/waiver tracking, *when* the spike ends, *then* a decision record (new `DEC-xx`) states where `compensationAmount` (`2.00 x appraisedValue`, runtime only) and its `PAID`/`WAIVED` outcome are stored (entity/fields) and how it relates to `Fine`.
- **AC-2:** *Given* HW01 only names `FULFILLED`, `CANCELLED`, `EXPIRED` reservation states, *when* the spike ends, *then* a state diagram documents all `Reservation` transitions (`WAITING -> READY -> FULFILLED`, `CANCELLED`, `EXPIRED`) and the `Notification` entity.
- **AC-3:** *Given* the decisions, *when* reviewed, *then* the effect on `LMS-016` and `LMS-017` estimates is noted in `docs/04-sprints/`.
- Timebox: 4 human hours. Not a UI story.

---

## Epic E2 — Authentication, RBAC and Member Self-Service

### LMS-003 — Login/logout with BCrypt demo passwords and RBAC
**Meta:** E2 | Must | 5 pts | 5 h (classic 10) | 3 agent sessions | S1 | FR: `FR-016`, `FR-017` | UC: UC-02 | BR: `BR-001`, `BR-018`

**As a** librarian or member, **I want** to log in and out with a local account, **so that** I only see and do what my role allows.

UI story: Stitch login screen first.

- **AC-a (login):** *Given* demo passwords are generated at startup and stored only as BCrypt hashes (`OPEN-05`, no password in `data/seed/`, `NFR-008`), *when* a seeded librarian or member submits valid credentials, *then* a session is created and the role home page opens (`FR-016`).
- **AC-b (invalid):** *Given* wrong credentials, *when* submitted, *then* the login is rejected with a generic message and no session exists.
- **AC-c (logout):** *Given* an authenticated session, *when* the user logs out, *then* the session ends and protected URLs redirect to login.
- **AC-d (RBAC):** *Given* a `ROLE_MEMBER` session, *when* the user requests a librarian-only URL (catalog CRUD, member management, desk checkout/return, fine settlement), *then* access is denied (`FR-017`, `NFR-007`); *and given* a `ROLE_GUEST`, *when* the user requests any page except the login page, *then* access follows the role matrix of `BR-001`.
- **AC-e (suspended):** *Given* a `SUSPENDED` member, *when* the member logs in, *then* login succeeds but borrowing, renewing, and reserving stay blocked (`BR-011`).

### LMS-013 — Member self-service portal and librarian member inspection
**Meta:** E2 | Must | 5 pts | 5 h (classic 10) | 3 agent sessions | S2 | FR: `FR-008`, `FR-018` | UC: UC-10, UC-04 | BR: `BR-002`, `BR-006`, `BR-010`, `BR-011`

**As a** member, **I want** a personal page with my loans, history, cooldowns, and fines, **so that** I know my due dates and what I owe without asking the desk.

UI story: Stitch self-service screen first. **Scope fix:** this story shows active loans, history, cooldowns, and fines **only**; active reservations, holds, and in-app notifications belong to `LMS-017`.

- **AC-a (active loans):** *Given* a logged-in member with active loans, *when* the self-service page opens, *then* it lists only that member's `ACTIVE` loans with `dueDate` and `OVERDUE` badge when `endDate > dueDate` (`BR-007`).
- **AC-b (history):** *Given* the member has returned loans, *when* the history section is opened, *then* closed loans (`RETURNED`, `LOST`) appear newest first.
- **AC-c (cooldowns):** *Given* a returned loan with `renewalCount >= 1` within 30 days of `returnDate`, *when* the page opens, *then* the book title and the first re-borrow date are shown (`BR-006`).
- **AC-d (fines):** *Given* the member has `UNPAID`, `PAID`, or `WAIVED` fines, *when* the page opens, *then* each fine shows amount and status and the total unpaid amount is displayed (`BR-010`).
- **AC-e (privacy):** *Given* member A is logged in, *when* A requests the page of member B, *then* access is denied.
- **AC-f (librarian view):** *Given* a librarian, *when* a member's circulation profile is opened, *then* it shows `memberType`, maximum quota (`7/3/3`), current loans, blocks, and cooldowns (`FR-008`, `BR-002`).

---

## Epic E3 — Catalog, Search and Copy Lifecycle

### LMS-004 — Catalog search and book detail
**Meta:** E3 | Must | 3 pts | 3.5 h (classic 6) | 2 agent sessions | S1 | FR: `FR-002`, `FR-003` | UC: UC-01 | BR: `BR-001`, `BR-014`, `BR-017`

**As a** logged-in user, **I want** to search the catalog and open a book detail page, **so that** I can find a title and see whether a copy is available.

UI story: Stitch search and detail screens first.

- **AC-a (search):** *Given* the seeded catalog, *when* a user searches a partial, case-insensitive title, author, or `isbn13`, *then* matching books are listed and can be filtered by category and availability (`FR-002`).
- **AC-b (detail):** *Given* a book, *when* its detail page opens, *then* all bibliographic fields and the status of every copy (`AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, `LOST`) are shown (`FR-003`).
- **AC-c (reference works):** *Given* a book with `referenceOnly = true`, *when* its detail page opens, *then* a "REFERENCE ONLY - NOT FOR LOAN" banner is shown (`BR-014`).
- **AC-d (empty):** *Given* no match, *when* a search runs, *then* an empty-state message is shown.

### LMS-005 — Book CRUD, copy registration and copy lifecycle
**Meta:** E3 | Must | 8 pts | 7.5 h (classic 16) | 3 agent sessions | S1 | FR: `FR-001`, `FR-004`, `FR-005` | UC: UC-03 | BR: `BR-014`, `BR-015`, `BR-017`

**As a** librarian, **I want** to maintain books and their physical copies on one screen and have copy states enforced, **so that** the catalog stays correct and copies never reach an illegal state.

UI story: Stitch book form and copy table first. Merged story; acceptance criteria stay separate.

- **AC-a (book create/update):** *Given* a librarian, *when* a book with a unique valid `isbn13` is created or updated, *then* it is saved including the `referenceOnly` flag; a duplicate or invalid `isbn13` is rejected (`FR-001`).
- **AC-b (archive):** *Given* a book with active loans, *when* a librarian archives it, *then* the archive is rejected until all copies are returned.
- **AC-c (copy registration):** *Given* an existing book, *when* a librarian adds a copy with a unique `LMS-COPY-*` barcode, *then* the copy is created as `AVAILABLE` (`FR-004`); a duplicate barcode is rejected.
- **AC-d (state machine):** *Given* a copy, *when* a transition is requested, *then* only the legal transitions of the GoF State design are accepted and an illegal one (for example `LOANED -> MAINTENANCE`) is rejected with a clear message (`FR-005`, `BR-017`).
- **AC-e (counts):** *Given* a title, *when* copies are added, *then* the title keeps its copy count within the documented model (`BR-017`).

---

## Epic E4 — Member Management

### LMS-006 — Member registration, profile update and suspension
**Meta:** E4 | Must | 3 pts | 3.5 h (classic 6) | 2 agent sessions | S2 | FR: `FR-006`, `FR-007` | UC: UC-04 | BR: `BR-002`, `BR-011`, `BR-018`

**As a** librarian, **I want** to register synthetic members, edit them, and suspend or reactivate them, **so that** only eligible members borrow.

UI story: Stitch member form first.

- **AC-a (register):** *Given* a librarian, *when* a member with a unique `memberId` (`SYN-STU-`, `SYN-STF-`, or `SYN-ADM-` pattern) and a `memberType` is saved, *then* the member is `ACTIVE` with the quota of the type (`7/3/3`) (`FR-006`).
- **AC-b (validation):** *Given* a duplicate `memberId` or a non-synthetic e-mail domain, *when* saved, *then* it is rejected (`BR-018`).
- **AC-c (update):** *Given* an existing member, *when* the profile is edited, *then* changes are stored and `memberId` is immutable (`FR-007`).
- **AC-d (suspend):** *Given* an `ACTIVE` member, *when* a librarian suspends the member, *then* status is `SUSPENDED` and borrowing, renewing, and reserving are blocked (`BR-011`); reactivation restores `ACTIVE`.

---

## Epic E5 — Borrowing, Returning and Renewal

### LMS-007 — Checkout with eligibility, cooldown and referenceOnly enforcement
**Meta:** E5 | Must | 8 pts | 9 h (classic 18) | 4 agent sessions | S2 | FR: `FR-009`, `FR-010`, `FR-011`, `FR-013` | UC: UC-05 | BR: `BR-002`, `BR-003`, `BR-006`, `BR-011`, `BR-013`, `BR-014`, `BR-016`, `BR-017`

**As a** librarian, **I want** to check out a copy to a member at the desk with all rules enforced, **so that** every loan is valid and traceable.

UI story: Stitch checkout desk screen first (keyboard/barcode entry, `NFR-002`). Merged story (checkout + re-borrow cooldown); criteria stay separate.

- **AC-a (member and ID):** *Given* the librarian enters the borrower's own `memberId` (personal ID card), *when* the member is `ACTIVE`, *then* checkout may continue; a `SUSPENDED` member is rejected (`FR-009`, `BR-016`).
- **AC-b (quota):** *Given* a `STUDENT` with `3` active loans, *when* a fourth is attempted, *then* it is rejected; *and given* an `ACADEMIC_STAFF` with `6` loans, *then* the seventh succeeds and the eighth is rejected (`BR-002`, boundary tests `3` and `7`).
- **AC-c (blocks):** *Given* a member with an overdue active loan or an `UNPAID` fine, *when* checkout is attempted, *then* it is rejected (`BR-011`).
- **AC-d (cooldown):** *Given* a returned loan of the same member and `isbn13` with `renewalCount >= 1` and `returnDate` less than 30 days ago, *when* checkout of that title is attempted, *then* it is rejected with the first allowed date; on day 30 after `returnDate` it succeeds (`FR-013`, `BR-006`; the cooldown applies to borrowing only).
- **AC-e (referenceOnly):** *Given* a book with `referenceOnly = true`, *when* checkout is attempted, *then* it is rejected with "reference work, not for loan" (`FR-010`, `BR-014`).
- **AC-f (copy state):** *Given* a copy that is not `AVAILABLE`, *when* checkout is attempted, *then* it is rejected; a `RESERVED` copy may only be taken by the reservation owner once `LMS-017` exists (`BR-013`, `BR-017`).
- **AC-g (execution):** *Given* all checks pass, *when* confirmed, *then* one transaction creates an `ACTIVE` loan with `dueDate = checkoutDate + 30 days` and sets the copy `LOANED`; on any failure nothing is persisted (`FR-011`, `BR-003`, `NFR-003`).

### LMS-010 — Return of a copy (copy to AVAILABLE only)
**Meta:** E5 | Must | 3 pts | 3.5 h (classic 6) | 2 agent sessions | S2 | FR: `FR-012` | UC: UC-06 | BR: `BR-007`, `BR-008`, `BR-017`

**As a** librarian, **I want** to scan a returned copy and close its loan, **so that** the copy is available again and any overdue fine is created.

UI story: Stitch return screen first. **Dependency fix:** this story returns the copy only to `AVAILABLE`. The `RESERVED` transition and hold promotion belong to `LMS-017`.

- **AC-a (close loan):** *Given* a copy with one `ACTIVE` loan, *when* its barcode is scanned, *then* the loan gets `returnDate = today`, status `RETURNED`, and the copy becomes `AVAILABLE` (`FR-012`, `BR-017`).
- **AC-b (no active loan):** *Given* a copy without an `ACTIVE` loan, *when* scanned, *then* a clear error is shown and nothing changes.
- **AC-c (on time):** *Given* `returnDate == dueDate`, *when* returned, *then* no fine is created (`BR-007`, zero grace period, `0` overdue days).
- **AC-d (late):** *Given* `returnDate` is 1 day after `dueDate`, *when* returned, *then* one `UNPAID` fine of `0.25 TRY` is created through the `LMS-009` calculator (`BR-008`).
- **AC-e (atomic):** *Given* any failure during return, *then* loan, copy, and fine remain unchanged (`NFR-003`).

### LMS-014 — Loan renewal with reserved guard
**Meta:** E5 | Should | 5 pts | 3.5 h (classic 8) | 2 agent sessions | S3 | FR: `FR-024` | UC: UC-07 | BR: `BR-003`, `BR-004`, `BR-005`, `BR-011`, `BR-006`

**As a** member or librarian, **I want** to renew an eligible loan once, **so that** I keep the book for another 30 days.

UI story: Stitch renew action first.

- **AC-a (renew):** *Given* an `ACTIVE`, non-overdue loan with `renewalCount = 0` and no blocks, *when* renewed, *then* `renewalCount = 1` and `dueDate = checkoutDate + 30 x (1 + renewalCount)` (`BR-005`).
- **AC-b (second renewal):** *Given* `renewalCount = 1`, *when* renewal is attempted, *then* it is rejected (`BR-005`).
- **AC-c (overdue/blocks):** *Given* an overdue loan, or the member has an `UNPAID` fine, *when* renewal is attempted, *then* it is rejected (`BR-004`, `BR-011`).
- **AC-d (reserved guard stub):** *Given* the "reserved" guard is implemented as a repository query (`existsActiveReservationByIsbn13`), *when* no reservation exists, *then* it returns `false` and renewal is allowed; the query returns `false` until `LMS-017` creates reservations, and from then on it blocks renewal when another member has a `WAITING` or `READY` reservation (`BR-004`).
- **AC-e (cooldown link):** *Given* a renewed loan is returned, *then* the 30-day re-borrow cooldown of `LMS-007` AC-d applies (`BR-006`).

---

## Epic E6 — Reservations and Pickup Holds

### LMS-017 — Reservation, FIFO queue, hold promotion and in-app notification
**Meta:** E6 | Should | 8 pts | 8.5 h (classic 16) | 4 agent sessions | S3 | FR: `FR-020`, `FR-021`, `FR-022` | UC: UC-08, UC-06, UC-10 | BR: `BR-011`, `BR-012`, `BR-013`, `BR-014`

**As a** member, **I want** to reserve a title with no available copy and be notified in the application when a copy is held for me, **so that** I get the book without checking the catalog repeatedly.

UI story: Stitch reserve button, my-reservations list, and notification panel first. Design inputs: decision from `LMS-008`.

- **AC-a (place):** *Given* zero `AVAILABLE` copies of a title and an `ACTIVE` member without a loan or open reservation for it, *when* the member reserves, *then* a `WAITING` reservation with the next FIFO `queuePosition` is created (`BR-012`).
- **AC-b (preconditions):** *Given* an available copy exists, or the title is `referenceOnly`, or the member is `SUSPENDED` or already holds a reservation, *when* reserving, *then* it is rejected (`BR-012`, `BR-014`, `BR-011`).
- **AC-c (promotion on return):** *Given* a title with a `WAITING` queue, *when* a copy is returned through the `LMS-010` flow, *then* the copy becomes `RESERVED` (not `AVAILABLE`), is bound as `readyCopyBarcode` to position `1`, and that reservation becomes `READY` (`BR-013`, `BR-017`).
- **AC-d (notification and window):** *Given* a promoted reservation, *when* the member opens the application, *then* an in-app notification shows the title and the pickup deadline of `3` calendar days; no e-mail or SMS is sent (`CON-004`).
- **AC-e (only position 1):** *Given* a `RESERVED` copy, *when* another member requests checkout, *then* it is rejected; position `1` succeeds and the reservation becomes `FULFILLED`.
- **AC-f (self-service extension):** *Given* `LMS-013` exists, *then* active reservations, holds, and notifications appear on the self-service page (added by this story).

### LMS-012 — Reservation cancellation and hold expiry
**Meta:** E6 | Should | 3 pts | 3.5 h (classic 7) | 2 agent sessions | S3 | FR: `FR-023` | UC: UC-08 | BR: `BR-012`, `BR-013`

**As a** member or librarian, **I want** to cancel a reservation and have unclaimed holds expire, **so that** the queue keeps moving.

UI story: Stitch cancel action first.

- **AC-a (cancel):** *Given* a `WAITING` or `READY` reservation, *when* the member or a librarian cancels it, *then* status becomes `CANCELLED` and later positions move up (`BR-012`).
- **AC-b (expiry):** *Given* a `READY` reservation older than the 3-day window, *when* the expiry check runs, *then* status becomes `EXPIRED` and the copy is promoted to the next `WAITING` reservation or becomes `AVAILABLE` (`BR-013`).

---

## Epic E7 — Overdue and Fines

### LMS-009 — Overdue detection and uncapped fine calculation
**Meta:** E7 | Must | 3 pts | 3.5 h (classic 6) | 2 agent sessions | S2 | FR: `FR-014`, `FR-015` | UC: UC-06, UC-09, UC-11 | BR: `BR-007`, `BR-008`, `BR-009`, `BR-010`, `BR-015`

**As a** librarian, **I want** deterministic overdue days and a fine of `0.25 TRY` per day with no cap, **so that** every fine is reproducible and correct.

Non-UI domain service (`FineCalculator`); TDD tests first (`NFR-011`).

- **AC-a (no grace):** *Given* `endDate == dueDate`, *then* `overdueDays = 0` and no fine is due (`BR-007`).
- **AC-b (one day):** *Given* `endDate = dueDate + 1`, *then* `overdueDays = 1` and `amount = 0.25 TRY`.
- **AC-c (no cap):** *Given* `overdueDays = 2000`, *then* `amount = 500.00 TRY` (no `250.00 TRY` ceiling, `BR-008`, `BR-009`).
- **AC-d (end date):** *Given* a loan with `lostReportedOn`, *then* `endDate = lostReportedOn`; else `returnDate` if returned, else the current date (`BR-007`, `BR-015`).
- **AC-e (one fine per loan):** *Given* a loan already has a fine, *when* recalculated, *then* the existing `UNPAID` record is updated, never duplicated (`BR-010`).

### LMS-011 — Fine payment and waiver
**Meta:** E7 | Should | 3 pts | 3.5 h (classic 7) | 2 agent sessions | S3 | FR: `FR-025`, `FR-026` | UC: UC-09 | BR: `BR-010`, `BR-011`

**As a** librarian, **I want** to record that an `UNPAID` fine was paid or waived at the desk, **so that** the member is unblocked.

UI story: Stitch fine settlement screen first.

- **AC-a (paid):** *Given* an `UNPAID` fine on a returned loan, *when* a librarian marks it paid, *then* status `PAID`, `settledOn`, and `settledBy` (librarian username) are stored (`BR-010`, `FR-025`).
- **AC-b (waived):** *Given* an `UNPAID` fine, *when* a librarian waives it, *then* status `WAIVED` with `settledOn` and `settledBy` are stored (`FR-026`).
- **AC-c (still active):** *Given* the loan is still `ACTIVE`, *when* settlement is attempted, *then* it is rejected (`BR-010`).
- **AC-d (unblock):** *Given* a member's last `UNPAID` fine was settled and no overdue loan remains, *then* borrowing is allowed again (`BR-011`).
- **AC-e (role):** *Given* a member session, *when* settlement is requested, *then* access is denied (`FR-017`).

---

## Epic E8 — Lost-Copy Handling

### LMS-016 — Lost-copy process with runtime appraised value
**Meta:** E8 | Should | 8 pts | 5.5 h (classic 12) | 3 agent sessions | S3 | FR: `FR-027` | UC: UC-09 | BR: `BR-005`, `BR-015`, `BR-017`

**As a** librarian, **I want** to record a lost-book petition and, after 30 days without replacement, assess `2x` the appraised value, **so that** lost copies are handled according to ADU rules.

UI story: Stitch lost-copy dialog first. Design inputs: decision from `LMS-008`.

- **AC-a (petition):** *Given* an `ACTIVE` loan, *when* a librarian records `lostReportedOn`, *then* overdue fine accrual stops on that date (`BR-015`, `LMS-009` AC-d).
- **AC-b (window):** *Given* a petition, *then* the member has 30 calendar days to replace the book; replacement closes the loan as `RETURNED` and the copy becomes `AVAILABLE`.
- **AC-c (assessment):** *Given* 30 days passed without replacement, *when* the librarian enters `appraisedValue` at runtime (no price exists in the seed), *then* the loan closes as `LOST` with `returnDate = null`, the copy becomes `LOST`, and `compensationAmount = 2.00 x appraisedValue` is charged in addition to the frozen overdue fine (`BR-015`, `BR-017`).
- **AC-d (validation):** *Given* an `appraisedValue <= 0` or empty, *when* submitted, *then* it is rejected.
- **AC-e (settlement):** *Given* the compensation, *then* it is paid or waived through the design from `LMS-008` and `LMS-011` (`BR-010`).

---

## Epic E9 — Dashboard and CSV Reports

> [!NOTE]
> **Story split (`LMS-015` -> `LMS-015` + `LMS-021`, Product Owner decision 2026-11-07):** The original `5`-point (`10` classic h / `5.0` human h) dashboard and reporting story is split into **`LMS-015` (`015a`: Operational dashboard KPI summary cards, `2 pts`, `4` classic h, `2.0` human h — Sprint 3 Commit)** and **`LMS-021` (`015b`: Actionable overdue loans and unpaid fines report, `3 pts`, `6` classic h, `3.0` human h — Sprint 3 Stretch)** so that KPI summary cards fit inside the Sprint 3 commitment line (`17.5 h <= 17.8 h` net) while preserving the exact combined sum (`2 + 3 = 5 pts`, `4 + 6 = 10` classic h, `2.0 + 3.0 = 5.0` human h).

### LMS-015 — Operational dashboard KPI summary cards (015a)
**Meta:** E9 | Should | 2 pts | 2 h (classic 4) | 1 agent session | S3 | FR: `FR-028` | UC: UC-11 | BR: `BR-001`, `BR-007`, `BR-008`

**As a** librarian, **I want** an operational dashboard showing real-time KPI summary cards (active loans, overdue loans, unpaid fine totals, and title/copy counts by state), **so that** I can monitor circulation health at a glance.

UI story: Stitch dashboard KPI cards first.

- **AC-a (KPIs):** *Given* the loaded seed, *when* the dashboard opens, *then* it displays KPI cards for total distinct titles, total physical copies, copies by state (`AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, `LOST`), active loans, overdue loans, and total unpaid fine amount (`TRY`), each matching the exact database count/sum (`FR-028`).
- **AC-b (role):** *Given* a member or guest session, *when* the dashboard URL is requested, *then* access is denied (`FR-017`, `BR-001`).

### LMS-021 — Actionable overdue loans and unpaid fines report (015b)
**Meta:** E9 | Should | 3 pts | 3 h (classic 6) | 1 agent session | S3 | FR: `FR-029` | UC: UC-11 | BR: `BR-007`, `BR-008`, `BR-011`

**As a** librarian, **I want** a prioritized report table of overdue active loans and unpaid fines, **so that** I can see which borrowers require immediate follow-up or desk settlement.

UI story: Stitch overdue and unpaid report table first. Stretch story in Sprint 3 (`015b`).

- **AC-a (report table):** *Given* overdue active loans and `UNPAID` fines exist, *when* the report view opens, *then* it lists them ordered by `overdueDays` descending with `memberId`, member name, book title, `copyBarcode`, `dueDate`, `overdueDays`, and accrued fine amount (`FR-029`, `BR-007`, `BR-008`).
- **AC-b (consistency):** *Given* the report rows, *when* compared against the KPI cards of `LMS-015`, *then* the overdue loan count and unpaid fine total match identically.
- **AC-c (role):** *Given* a member session, *when* the report is requested, *then* access is denied (`FR-017`).

### LMS-019 — CSV export of overdue and inventory reports
**Meta:** E9 | Could | 3 pts | 2 h (classic 5) | 1 agent session | S3 | FR: `FR-032` | UC: UC-11 | BR: `BR-001`

**As a** librarian, **I want** to download the overdue report and the copy inventory as CSV, **so that** I can use them in a spreadsheet.

- **AC-a:** *Given* the report page (`LMS-021`) or inventory table (`LMS-005`), *when* the librarian clicks export, *then* a UTF-8 CSV with a header row and Turkish characters intact is downloaded (`FR-032`).
- **AC-b:** *Given* a member session, *when* export is requested, *then* access is denied.

---

## Stretch (Could) stories

### LMS-018 — Public guest catalog portal
**Meta:** E3 | Could | 2 pts | 2 h (classic 4) | 1 agent session | S3 | FR: `FR-030` | UC: UC-01 | BR: `BR-001`, `BR-014`

**As a** guest, **I want** to search the catalog without logging in, **so that** I can check availability before visiting the library.

UI story: Stitch guest page first (reuses the `LMS-004` design).

- **AC-a:** *Given* an unauthenticated visitor, *when* the catalog is opened, *then* search, filter, and detail work read-only and no loan, member, or fine data is visible (`FR-030`).
- **AC-b:** *Given* a guest, *when* a librarian URL is requested, *then* access is denied.

### LMS-020 — Open Library ISBN lookup helper
**Meta:** E3 | Could | 3 pts | 3.5 h (classic 6) | 2 agent sessions | S3 | FR: `FR-031` | UC: UC-03 | BR: `BR-001`

**As a** librarian, **I want** a "Fetch by ISBN" button on the book form, **so that** I can fill bibliographic fields faster.

UI story: Stitch button state first.

- **AC-a:** *Given* the book form, *when* a valid `isbn13` is fetched and the service answers, *then* title, authors, and publisher are pre-filled and editable (`FR-031`).
- **AC-b:** *Given* the service is unreachable, *when* fetching, *then* a non-blocking message is shown and manual entry still works (`NFR-004`: the application and its tests stay offline-capable).
