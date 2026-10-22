<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Ubiquitous language glossary aligning domain entities, policies, GoF pattern collaborators, and exact JSON field names and enums from data/seed/*.json.
-->
# Domain Glossary (Ubiquitous Language) — Library Management System (LMS)

- **Course:** CSE305 Software Engineering — Adnan Menderes University (ADU)
- **Phase:** Inception (`HW02`)
- **Date:** 2026-10-22

This document defines the **Ubiquitous Language** shared across Requirements (`FR-*`, `NFR-*`), Business Rules (`BR-*`), Use Cases (`UC-*`), Java/Spring Boot domain classes (`edu.adu.lms.*`), JUnit 5 tests, and the seed data files under [`data/seed/`](../../data/seed/) (documented in [`data/README.md`](../../data/README.md)).

---

## 1. Core Domain Entities & Ubiquitous Language Terms

| Ubiquitous Term | Seed File / Target Java Type | Exact Seed JSON Field Names & Types | Definition & Domain Invariants |
|---|---|---|---|
| **`Book`** | [`data/seed/books-openlibrary.json`](../../data/seed/books-openlibrary.json)<br>`edu.adu.lms.entity.Book` | **In current seed v1:** `isbn13` (`String`, PK/NK), `title` (`String`), `subtitle` (`String?`), `authors` (`List<String>`, `1..5`), `publisher` (`String`), `firstPublishYear` (`Integer`), `category` (`String`, 1 of 11), `subjects` (`List<String>`, `1..5`), `pageCount` (`Integer`, work median), `coverId` (`Long`), `coverUrl` (`String`), `openLibraryWorkKey` (`String`).<br>**PLANNED: will exist after seed v2 (`OPEN-06`):** `referenceOnly` (`Boolean`, default `false`). | A distinct bibliographic work/edition in the library catalog, uniquely identified by a validated 13-digit `isbn13` (e.g., `"9780321573513"`, *Algorithms* by Robert Sedgewick). Owns `1..4` physical `BookCopy` instances. If `referenceOnly == true` (encyclopedia, dictionary, catalog — *PLANNED: will exist after seed v2 (`OPEN-06`)*), its copies cannot be loaned or reserved (`BR-014`). |
| **`BookCopy`** | [`data/seed/copies.json`](../../data/seed/copies.json)<br>`edu.adu.lms.entity.BookCopy` | **In current seed v1:** `barcode` (`String`, PK/NK, `LMS-COPY-1001`..), `isbn13` (`String`, FK -> `Book`), `status` (`BookCopyStatus`: `AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, `LOST`). | A physical book item on the shelf or in circulation, tracked individually by its unique `barcode` (e.g., `"LMS-COPY-1001"`). Governed by the GoF **State** pattern (`BookCopyState`); at most one `ACTIVE` loan may reference a `barcode` at any time (`BR-017`). |
| **`Member`** | [`data/seed/members.json`](../../data/seed/members.json)<br>`edu.adu.lms.entity.Member` | **In current seed v1:** `memberId` (`String`, PK/NK: `SYN-STU-0001`.., `SYN-STF-0001`..), `firstName` (`String`), `lastName` (`String`), `email` (`String`, `*@synthetic.lms.local`), `memberType` (`STUDENT`, `ACADEMIC_STAFF`), `status` (`ACTIVE`, `SUSPENDED`), `department` (`String`), `registeredOn` (`LocalDate`, `YYYY-MM-DD`).<br>**PLANNED: will exist after seed v2 (`OPEN-06`):** `memberType = ADMINISTRATIVE_STAFF` and `memberId = SYN-ADM-0001`.. | A synthetic university borrower (`ROLE_MEMBER`). Confirmed ADU borrowing limits (`BR-002`): `ACADEMIC_STAFF` = max `7` books; `ADMINISTRATIVE_STAFF` *(PLANNED: will exist after seed v2 (`OPEN-06`))* = max `3` books; `STUDENT` = max `3` books; all for `30 calendar days` (`BR-003`). Real examples in seed v1: `SYN-STU-0001` (`Tutkucan Ergül`) and `SYN-STF-0003` (`Atasagun Öcalan`). |
| **`Librarian`** | [`data/seed/librarians.json`](../../data/seed/librarians.json)<br>`edu.adu.lms.entity.Librarian` | **In current seed v1:** `username` (`String`, PK/NK, `syn-lib-0001`..), `displayName` (`String`), `email` (`String`, `*@synthetic.lms.local`), `role` (`String`, `"ROLE_LIBRARIAN"`). | An authenticated library staff member and system administrator (`ASSUMPTION-01`). Seed JSON contains **no password field**; BCrypt-hashed demo passwords are initialized at startup (`BR-018`). Real example in seed v1: `syn-lib-0001` (`Enginiz Yıldırım`). |
| **`Guest`** | Session / Security Role<br>`ROLE_GUEST` | Unauthenticated user | An anonymous visitor who can browse and search the public catalog (`UC-01`, `FR-030`) in read-only mode but cannot borrow, renew, reserve, or view member records (`BR-001`). |
| **`Loan`** | [`data/seed/loans.json`](../../data/seed/loans.json)<br>`edu.adu.lms.entity.Loan` | **In current seed v1:** `loanId` (`String`, PK/NK, `LOAN-0001`..), `memberId` (`String`, FK -> `Member`), `copyBarcode` (`String`, FK -> `BookCopy`), `checkoutDate` (`LocalDate`), `dueDate` (`LocalDate`), `returnDate` (`LocalDate?`), `status` (`ACTIVE`, `RETURNED`), `renewalCount` (`Integer`: `0` or `1`), `renewedOn` (`LocalDate?`).<br>**PLANNED: will exist after seed v2 (`OPEN-06`):** `lostReportedOn` (`LocalDate?`). | A circulation transaction recording the lending of one `BookCopy` (`copyBarcode`) to one `Member` (`memberId`) in person (`BR-016`). Standard `dueDate = checkoutDate + 30 * (1 + renewalCount)`. Real examples in seed v1: `LOAN-0001` (`SYN-STU-0026`, `LMS-COPY-1758`, `RETURNED`) and `LOAN-0099` (`SYN-STU-0001`, `LMS-COPY-2119`, `ACTIVE`). |
| **`Fine`** | [`data/seed/fines.json`](../../data/seed/fines.json)<br>`edu.adu.lms.entity.Fine` | **In current seed v1:** `fineId` (`String`, PK/NK, `FINE-0001`..), `loanId` (`String`, FK -> `Loan`, unique), `memberId` (`String`, FK -> `Member`), `overdueDays` (`Integer`), `amount` (`BigDecimal` / 2-digit string, e.g., `"5.00"`), `currency` (`String`, `"TRY"`), `status` (`UNPAID`, `PAID`, `WAIVED`), `assessedOn` (`LocalDate`), `settledOn` (`LocalDate?`), `settledBy` (`String?`, FK -> `Librarian.username`). | A monetary penalty assessed on an overdue loan (`overdueDays > 0`). Under confirmed ADU rule `BR-008` and `BR-009` (`ASSUMPTION-10`), `amount = 0.25 * overdueDays` in `TRY` with **no maximum cap**. Any `UNPAID` fine blocks the member from new checkouts or renewals (`BR-011`). |
| **`Reservation` (Hold)** | [`data/seed/reservations.json`](../../data/seed/reservations.json)<br>`edu.adu.lms.entity.Reservation` | **In current seed v1:** `reservationId` (`String`, PK/NK, `RES-0001`..), `isbn13` (`String`, FK -> `Book`), `memberId` (`String`, FK -> `Member`), `queuePosition` (`Integer`, `1..n` FIFO), `status` (`WAITING`, `READY`), `createdOn` (`LocalDate`), `readyCopyBarcode` (`String?`, FK -> `BookCopy`).<br>**PLANNED: will exist after seed v2 (`OPEN-06`) / runtime:** hold pickup window expiration & in-app notification tracking. | A title-level hold placed on an `isbn13` when zero copies of that book are `AVAILABLE` (`BR-012`). When a copy is returned, the head reservation (`queuePosition == 1`) becomes `READY`, binds `readyCopyBarcode`, and holds the `RESERVED` copy for **2–3 days** (`3 calendar days` target) (`BR-013`). Real example in seed v1: `RES-0009` (`SYN-STU-0003`, `isbn13: "9780345451323"`, `status: "READY"`, `readyCopyBarcode: "LMS-COPY-1599"`). |

---

## 2. Policy, Calculation & Architectural Terms

| Term | Definition in LMS Domain |
|---|---|
| **`LoanPolicy` / `LoanPolicyStrategy`** | GoF **Strategy** interface (`edu.adu.lms.policy.LoanPolicyStrategy`) encapsulating member-type lending rules (`BR-002`, `BR-003`): `AcademicStaffLoanPolicy` (`maxActiveLoans = 7`, `loanPeriodDays = 30`), `AdministrativeStaffLoanPolicy` (`maxActiveLoans = 3`, `loanPeriodDays = 30`), and `StudentLoanPolicy` (`maxActiveLoans = 3`, `loanPeriodDays = 30`). |
| **`FineStrategy` / `FineCalculationStrategy`** | GoF **Strategy** interface (`edu.adu.lms.policy.FineCalculationStrategy`) encapsulating deterministic overdue fine computation (`BR-007`..`BR-009`): `StandardDailyFineStrategy` computes `amount = 0.25 * overdueDays` in `TRY` with no upper cap. |
| **`BookCopyState`** | GoF **State** interface (`edu.adu.lms.state.BookCopyState`) governing valid transitions between `AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, and `LOST` (`BR-017`, `FR-005`). |
| **`Barcode` (`copyBarcode`)** | Unique synthetic identifier printed on a physical `BookCopy` following the format `LMS-COPY-1001`, `LMS-COPY-1002`, ... (`ASSUMPTION-09`). |
| **`ISBN-13` (`isbn13`)** | 13-digit International Standard Book Number with a valid modulo-10 check digit (`lms_seed_common.is_valid_isbn13`). Valid 10-digit ISBNs from Open Library are converted to `978`-prefixed ISBN-13 during seed ingestion. |
| **`Reference Only` (`referenceOnly`)** | **PLANNED: will exist after seed v2 (`OPEN-06`):** Boolean attribute marking non-circulating reference works—specifically **encyclopedias, dictionaries, and catalogs**—which cannot be checked out or reserved under confirmed ADU rule `BR-014`. *(Periodicals and unpublished theses are Out of Scope).* |
| **`Overdue` & `overdueDays`** | A loan is overdue when `effectiveEndDate > dueDate` (zero grace period; a loan due on `effectiveEndDate == dueDate` is **not** overdue, `BR-007`). Calculated as `overdueDays = max(0, (effectiveEndDate - dueDate).days)`. |
| **`Due Soon`** | Operational dashboard convention (`data/README.md` §5): an `ACTIVE` loan that is not yet overdue and whose `dueDate` falls within `0..3` calendar days of `currentDate`. |
| **`Post-Renewal Cooldown`** | Confirmed ADU rule (`BR-006`): when a member extends (`renewalCount >= 1`) a loan and subsequently returns the copy on `returnDate`, that same member is barred from borrowing the same book (`isbn13`) again for **1 month** (`30 calendar days` under `ASSUMPTION-12`). |
| **`Pickup Hold Window`** | Confirmed ADU rule (`BR-013`): when a reserved book is returned, an in-app notification is generated (`ASSUMPTION-13` — *PLANNED: will exist after seed v2 (`OPEN-06`) / runtime*) and the `RESERVED` copy (`readyCopyBarcode`) is held for the `queuePosition == 1` (`READY`) member for **2–3 days** (`3 calendar days` target under `ASSUMPTION-13`). |
| **`Lost Copy Petition` (`lostReportedOn`) & `Appraised Value` (`appraisedValue`)** | **PLANNED: will exist after seed v2 (`OPEN-06`) / runtime input:** Confirmed ADU rule (`BR-015`): when a borrower files a lost-book petition on `lostReportedOn`, daily overdue fine accrual freezes on that date. If the book is not replaced within **1 month (`30 calendar days`)**, the copy becomes `LOST` and the member is charged **twice (`2x`) the book value** determined by the Valuation Commission (`2.00 * appraisedValue`, entered manually by the Librarian under `ASSUMPTION-15`). |
| **`Settlement` (`PAID`) & `Waiver` (`WAIVED`)** | Resolution of an `UNPAID` fine or lost-book charge at the circulation desk by a Librarian (`ROLE_LIBRARIAN`), recording `settledOn` (`LocalDate`) and `settledBy` (`librarian.username`, e.g., `"syn-lib-0001"`). |
| **`Reference Date` (`REFERENCE_DATE`)** | Fixed anchor date (`2026-10-22` in `tools/data/lms_seed_common.py`) used to generate deterministic synthetic dates in `data/seed/*.json`. Evaluated for startup date-shifting (`OPEN-04`). |

---

## 3. Enumerated Values & Identifier Patterns Reference

| Domain Concept | Allowed Enum Values | Seed Identifier / Value Pattern |
|---|---|---|
| **System Security Role** | `ROLE_LIBRARIAN`, `ROLE_MEMBER`, `ROLE_GUEST` | Spring Security / Session authority |
| **`Member.memberType`** | `STUDENT`, `ACADEMIC_STAFF`, `ADMINISTRATIVE_STAFF` *(PLANNED: will exist after seed v2 (`OPEN-06`))* | `SYN-STU-0001`.., `SYN-STF-0001`.., `SYN-ADM-0001`.. *(PLANNED: will exist after seed v2 (`OPEN-06`))* |
| **`Member.status`** | `ACTIVE`, `SUSPENDED` | Uppercase string |
| **`Book.category`** | `Computer Science`, `Software Engineering`, `Programming`, `Databases`, `Mathematics`, `Physics & Natural Sciences`, `Engineering`, `Fiction`, `History`, `Philosophy & Social Sciences`, `Turkish Literature` | 11 fixed categories in `lms_seed_common.CATEGORIES` |
| **`BookCopy.status`** | `AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, `LOST` | Barcode: `LMS-COPY-1001`.. |
| **`Loan.status`** | `ACTIVE`, `RETURNED` | Loan ID: `LOAN-0001`.. |
| **`Fine.status`** | `UNPAID`, `PAID`, `WAIVED` | Fine ID: `FINE-0001`.. (`currency = "TRY"`) |
| **`Reservation.status`** | `WAITING`, `READY` | Reservation ID: `RES-0001`.. (`queuePosition = 1..n`) |
