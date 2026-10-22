<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Authoritative catalog of confirmed Adnan Menderes University (ADU) library lending rules, superseded HW01 assumptions, new proposed assumptions, and traceable business rules (BR-001..BR-018).
-->
# Business Rules — Library Management System (LMS)

- **Course:** CSE305 Software Engineering — Adnan Menderes University (ADU)
- **Phase:** Inception (`HW02`)
- **Verified By:** Ibrahim Temur (`231805033` — Product Owner) & Omer Faruk Kuş (`231805026` — Scrum Master)
- **Date:** 2026-10-22

---

## 1. Official Verification Sources & Governance

On **2026-10-22**, the project team (**Ibrahim Temur** and **Omer Faruk Kuş**) verified the official circulation regulations of the **Aydın Adnan Menderes University Directorate of Library and Documentation (ADÜ Kütüphane ve Dokümantasyon Daire Başkanlığı)** against the initial domain assumptions drafted in `HW01`.

### 1.1 Official Reference Sources (Verification Basis — Accessed: 2026-10-22)
1. **Aydın Adnan Menderes Üniversitesi Kütüphane ve Dokümantasyon Daire Başkanlığı - Ödünç Verme Hizmetleri:**  
   <https://kutuphane.adu.edu.tr/default.asp?idx=313333> (Accessed: 2026-10-22)
2. **Aydın Adnan Menderes Üniversitesi Kütüphane ve Dokümantasyon Daire Başkanlığı - Sıkça Sorulan Sorular (SSS):**  
   <https://kutuphane.adu.edu.tr/default.asp?idx=323130> (Accessed: 2026-10-22)
3. **Adnan Menderes Üniversitesi Kütüphaneler Yönetmeliği:**  
   (Mevzuat Bilgi Sistemi - <https://www.mevzuat.gov.tr>) (Accessed: 2026-10-22)
4. **ADÜ Kütüphane Resmi Web Portalı ve Duyuru Arşivi:**  
   <https://kutuphane.adu.edu.tr> (Accessed: 2026-10-22)

### 1.2 Confirmed Institutional Rules vs. Project Assumptions
- Every policy rule directly backed by the official sources above is marked **`CONFIRMED (ADU Library Official Rules, 2026-10-22)`**.
- Every implementation sub-detail not explicitly fixed by the official text (such as maximum renewal count, renewal extension duration, 30-day calendar day mapping for "1 month" intervals, exact pickup days within the 2–3 day window, in-app notification channel, membership suspension, or the removal of a fine cap) remains explicitly tagged as **`ASSUMPTION`**.
- **Scope Boundary on Periodicals and Unpublished Theses:** Official ADU rule *(d)* states that encyclopedias, dictionaries, catalogs, the latest issues of periodicals, and unpublished/non-printed theses are non-circulating, while non-latest issues of periodicals (up to 2 issues) may be borrowed for 2 days. Because the **CSE305 Library Management System manages books only**, **periodicals/serials and unpublished theses are explicitly Out of Scope** (`CON-002`). Non-circulating books (encyclopedias, dictionaries, and catalogs) are supported in-scope via a non-circulating reference flag (`BR-014`).

---

## 2. Supersedes HW01 Assumptions (`docs/01-proposal/PROJECT_PROPOSAL.md`)

> [!IMPORTANT]
> To preserve historical milestone integrity, [`docs/01-proposal/PROJECT_PROPOSAL.md`](../01-proposal/PROJECT_PROPOSAL.md) (`HW01`) is **not** modified. The table below documents how the confirmed ADU rules and updated Inception assumptions supersede or refine `ASSUMPTION-01`..`09` from `HW01`.

| HW01 Assumption ID | HW01 Statement Summary | HW02 Disposition | Superseding / Implementing Rule(s) in This Document |
|---|---|---|---|
| **`ASSUMPTION-01`** | Unified Librarian/Admin role (`ROLE_LIBRARIAN`), Member (`ROLE_MEMBER`), Guest (`ROLE_GUEST`). | **Retained (`ASSUMPTION`)** | `BR-001` |
| **`ASSUMPTION-02`** | Borrowing limits: `STUDENT = 3`, `ACADEMIC_STAFF = 5`. | **SUPERSEDED by Confirmed Rule (a)** | `BR-002` (`CONFIRMED`: `ACADEMIC_STAFF = 7` books; `ADMINISTRATIVE_STAFF = 3` books; `STUDENT = 3` books). |
| **`ASSUMPTION-03`** | Standard loan period: `STUDENT = 14` days, `ACADEMIC_STAFF = 30` days. | **SUPERSEDED by Confirmed Rule (a)** | `BR-003` (`CONFIRMED`: `30 calendar days` for all three member types: `ACADEMIC_STAFF`, `ADMINISTRATIVE_STAFF`, and `STUDENT`). |
| **`ASSUMPTION-04`** | At most 1 renewal for 1 standard period if not overdue and no active reservation. | **PARTIALLY CONFIRMED by Rule (b) & Extended** | `BR-004` (`CONFIRMED`: overdue or reserved books cannot be renewed), `BR-005` (`ASSUMPTION`: max `1` renewal of `+30` days), and `BR-006` (`CONFIRMED` + `ASSUMPTION-12`: 1-month / `30-day` cooldown before the same member can re-borrow a renewed book after return). |
| **`ASSUMPTION-05`** | Daily fine of `5.00 TRY/day` with a `250.00 TRY` cap per loan. | **SUPERSEDED by Confirmed Rule (e) & `ASSUMPTION-10`** | `BR-008` (`CONFIRMED`: base tariff is `0.25 TRY` / 25 kuruş per overdue day per book) and `BR-009` (`ASSUMPTION-10`: the invented `250.00 TRY` cap is removed; **no fine cap**). |
| **`ASSUMPTION-06`** | Borrowing block on overdue loan, unpaid fine (`> 0.00 TRY`), or `SUSPENDED` status. | **CONFIRMED by Rule (e) (Overdue & Unpaid Fine) + Retained (`ASSUMPTION` for `SUSPENDED`)** | `BR-011` (`CONFIRMED`: no new loans to members with an overdue book or unpaid fine; `ASSUMPTION`: block also applies to `SUSPENDED` members and renewals). |
| **`ASSUMPTION-07`** | Title-level FIFO reservation queue; returned copy transitions to `RESERVED`. | **PARTIALLY CONFIRMED by Rule (c) & Extended** | `BR-012` (`ASSUMPTION`: title-level FIFO queue when 0 copies are `AVAILABLE` and member neither holds nor queues for the title) and `BR-013` (`CONFIRMED`: notification sent on return and copy held `2–3 days`; `ASSUMPTION-13`: in-app notification channel and exact `3-day` hold window). |
| **`ASSUMPTION-08`** | 100% synthetic personal data and local authentication. | **Retained (`ASSUMPTION`) & Extended by `ASSUMPTION-16`** | `BR-018` |
| **`ASSUMPTION-09`** | 1 to 4 physical copies per seeded title (`LMS-COPY-1001`..). | **Retained (`ASSUMPTION`)** | `BR-017` |

---

## 3. New Proposed Assumptions (`ASSUMPTION-10`..`ASSUMPTION-17`)

The following project assumptions cover operational and technical sub-details not fixed in `PROJECT_PROPOSAL.md` (`ASSUMPTION-01`..`09`) or in the confirmed ADU library regulations:

| ID | Category | Explicit Assumption Statement | Linked Business Rule(s) |
|---|---|---|---|
| **`ASSUMPTION-10`** | **No Overdue Fine Cap** | **ASSUMPTION:** The `250.00 TRY` fine cap from `HW01` (`ASSUMPTION-05`) is removed because at the confirmed tariff of `0.25 TRY/day` it would require 1,000 overdue days. Overdue fines accrue deterministically with **no maximum cap** (`amount = 0.25 * overdueDays`). | `BR-009` |
| **`ASSUMPTION-11`** | **Maximum Renewal Count & Extension Length** | **ASSUMPTION:** An eligible active loan may be renewed at most **1 time** (`renewalCount <= 1`), extending `dueDate` by one additional standard loan period (**`+30 calendar days`**). | `BR-005` |
| **`ASSUMPTION-12`** | **Deterministic 30-Day Mapping for "1 Month"** | **ASSUMPTION:** Where confirmed ADU rules specify a **"1 month"** interval—specifically the post-renewal re-borrowing cooldown (Rule *b*) and the lost-book replacement deadline (Rule *f*)—the system evaluates the interval deterministically as **`30 calendar days`**. | `BR-006`, `BR-015` |
| **`ASSUMPTION-13`** | **Reservation Queue Preconditions, In-App Notification & 3-Day Hold** | **ASSUMPTION:** (1) A reservation can be placed on a book title (`isbn13`) only when **zero physical copies** of that title are `AVAILABLE`, and the requesting member neither currently holds an `ACTIVE` loan for a copy of that title nor already has a `WAITING` or `READY` reservation in that title's queue. (2) Hold-ready notifications (Confirmed Rule *c*) are delivered as **in-app notifications** (since external SMS/SMTP is out of scope). (3) The confirmed **2–3 day** pickup window is fixed at **`3 calendar days`** from the return date before an unclaimed `READY` hold expires. | `BR-012`, `BR-013` |
| **`ASSUMPTION-14`** | **Non-Circulating Reference Flag on Books** | **ASSUMPTION:** Confirmed Rule *(d)* for non-circulating book categories (encyclopedias, dictionaries, catalogs) is modeled via a boolean `referenceOnly` (`circulating = false`) attribute on `Book`; all copies of a `referenceOnly` book are ineligible for checkout or reservation. | `BR-014` |
| **`ASSUMPTION-15`** | **Manual Appraised Value Entry for Lost Books** | **ASSUMPTION:** Because Open Library seed records (`books-openlibrary.json`) do not contain book prices, when a lost copy is not replaced within 1 month (`30 calendar days`) of `lostReportedOn`, the Librarian manually inputs the Valuation Commission's determined value (`appraisedValue` in `TRY`), and the system computes the confirmed **2x penalty** (`compensationAmount = 2.00 * appraisedValue`). | `BR-015` |
| **`ASSUMPTION-16`** | **Startup BCrypt Demo Password Seeding** | **ASSUMPTION:** Seed JSON files (`data/seed/*.json`) store zero passwords or credentials. Documented synthetic demo passwords for local login (`ROLE_LIBRARIAN` and `ROLE_MEMBER`) are hashed (e.g., using BCrypt) and loaded into the database at application startup (`OPEN-05`). | `BR-018` |
| **`ASSUMPTION-17`** | **Administrative Staff Synthetic ID Format** | **ASSUMPTION:** Members with `memberType = "ADMINISTRATIVE_STAFF"` use the synthetic identifier format `SYN-ADM-0001`.. and email domain `syn-adm-0001@synthetic.lms.local`, matching `SYN-STU-*` and `SYN-STF-*`. | `BR-002`, `BR-018` |

---

## 4. Master Catalog of Business Rules (`BR-001`..`BR-018`)

| Rule ID | Category | Rule Statement | Verification Status | Source / Assumption ID | Supported `FR-*` IDs |
|---|---|---|---|---|---|
| **`BR-001`** | Access Control & Roles | The system enforces three role boundaries: `ROLE_LIBRARIAN` (unified Librarian & System Admin operational privileges), `ROLE_MEMBER` (authenticated self-service access for `STUDENT`, `ACADEMIC_STAFF`, and `ADMINISTRATIVE_STAFF`), and `ROLE_GUEST` (unauthenticated read-only catalog access). | `ASSUMPTION` | `ASSUMPTION-01` | `FR-002`, `FR-016`, `FR-017`, `FR-018`, `FR-028`, `FR-030`, `FR-031`, `FR-032` |
| **`BR-002`** | Borrowing Quotas | Maximum simultaneous `ACTIVE` loans per member type: **`ACADEMIC_STAFF` = at most 7 books**; **`ADMINISTRATIVE_STAFF` = at most 3 books**; **`STUDENT` = at most 3 books**. A checkout request that would exceed `MAX_ACTIVE_LOANS[memberType]` is rejected. | **`CONFIRMED`** *(ADU Library Official Rules, 2026-10-22)* | ADU Lending Services (`idx=313333`) & FAQ (`idx=323130`); supersedes `ASSUMPTION-02` (`ASSUMPTION-17` for `SYN-ADM-*` IDs) | `FR-006`, `FR-008`, `FR-009`, `FR-011` |
| **`BR-003`** | Loan Duration | The standard loan period is **30 calendar days** from `checkoutDate` for all three member types (`ACADEMIC_STAFF = 30 days`, `ADMINISTRATIVE_STAFF = 30 days`, `STUDENT = 30 days`). Initial due date: `dueDate = checkoutDate + 30 days`. | **`CONFIRMED`** *(ADU Library Official Rules, 2026-10-22)* | ADU Lending Services (`idx=313333`) & FAQ (`idx=323130`); supersedes `ASSUMPTION-03` | `FR-011`, `FR-024` |
| **`BR-004`** | Renewal Prohibitions | A loaned book **cannot** have its loan period extended (renewed) if (1) the loan is currently overdue (`currentDate > dueDate`) or (2) another member holds an active (`WAITING` or `READY`) reservation on that book title (`isbn13`). | **`CONFIRMED`** *(ADU Library Official Rules, 2026-10-22)* | ADU Lending Services (`idx=313333`) & FAQ (`idx=323130`); confirms part of `ASSUMPTION-04` | `FR-024` |
| **`BR-005`** | Renewal Count & Formula | An eligible `ACTIVE` loan may be renewed at most **1 time** (`renewalCount` transitions from `0` to `1`) for one additional standard period (`+30 calendar days`). Formula: `dueDate = checkoutDate + 30 * (1 + renewalCount)`. | `ASSUMPTION` | `ASSUMPTION-04`, `ASSUMPTION-11` | `FR-024` |
| **`BR-006`** | Post-Renewal Cooldown | A book whose loan period was extended (`renewalCount >= 1`) **cannot be borrowed again by the same member until 1 month (`30 calendar days`) after its `returnDate`** (i.e., checkout is rejected if `currentDate < lastRenewedReturnDate + 30 days` for the same `memberId` and `isbn13`). | **`CONFIRMED`** *(1-month cooldown rule, 2026-10-22)* + `ASSUMPTION` *(30-day calendar mapping)* | ADU Lending Services (`idx=313333`); `ASSUMPTION-12` | `FR-008`, `FR-009`, `FR-013` |
| **`BR-007`** | Overdue Determination | There is **no grace period**. A loan that is due today (`endDate == dueDate`) is **not** overdue. A loan is overdue when `endDate > dueDate` (where `endDate` is `lostReportedOn` if reported lost, else `returnDate` if returned, else `currentDate`). Overdue days: `overdueDays = max(0, (endDate - dueDate).days)`. | `ASSUMPTION` | `ASSUMPTION-05` (date convention in `data/README.md`) | `FR-012`, `FR-014`, `FR-028`, `FR-029` |
| **`BR-008`** | Daily Overdue Fine Rate | Each overdue book loan accrues a base daily overdue fine of **0.25 TRY (25 kuruş) per overdue calendar day**. Formula: `amount = 0.25 * overdueDays` (in `TRY`, formatted to 2 decimal places). | **`CONFIRMED`** *(ADU Library Official Rules, 2026-10-22)* | ADU Lending Services (`idx=313333`) & FAQ (`idx=323130`); supersedes `5.00 TRY/day` in `ASSUMPTION-05` | `FR-014`, `FR-015`, `FR-028`, `FR-029` |
| **`BR-009`** | No Overdue Fine Cap | Overdue fines accrue without an upper monetary ceiling (**no cap**). The `250.00 TRY` cap from `HW01` is removed. | `ASSUMPTION` | `ASSUMPTION-10`; supersedes `250.00 TRY` cap in `ASSUMPTION-05` | `FR-014`, `FR-015` |
| **`BR-010`** | Fine Lifecycle & Settlement | At most one overdue `Fine` record exists per `loanId`. Active overdue loans have `status = UNPAID` with `assessedOn = currentDate` and `settledOn = null`. Only after the loan is returned (or resolved) may a Librarian transition the fine from `UNPAID` to `PAID` or `WAIVED`, recording `settledOn` and `settledBy` (`librarian.username`). | `ASSUMPTION` | `ASSUMPTION-05` & `data/README.md` §6 | `FR-015`, `FR-018`, `FR-025`, `FR-026` |
| **`BR-011`** | Borrowing & Renewal Block | A member who currently holds **any overdue active loan** OR has **any `UNPAID` fine/charge (`amount > 0.00 TRY`)** cannot borrow a new book or renew an existing loan. Additionally, a member whose status is `SUSPENDED` is blocked from borrowing, renewing, or reserving. | **`CONFIRMED`** *(Overdue & unpaid fine block, 2026-10-22)* + `ASSUMPTION` *(`SUSPENDED` status & renewal block)* | ADU Lending Services (`idx=313333`) & `ASSUMPTION-06` | `FR-007`, `FR-008`, `FR-009`, `FR-020`, `FR-024`, `FR-025`, `FR-026`, `FR-029` |
| **`BR-012`** | Reservation Eligibility & FIFO Queue | A member may place a title-level reservation (`isbn13`) **only when zero copies of that title are `AVAILABLE`**, and only if the member is `ACTIVE`, does **not** currently hold an `ACTIVE` loan for any copy of that title, and does **not** already hold a `WAITING` or `READY` reservation for that title. Reservations on a title are ordered strictly FIFO (`queuePosition = 1..n`) by `createdOn`. | `ASSUMPTION` | `ASSUMPTION-07`, `ASSUMPTION-13`, `data/README.md` §6 | `FR-020`, `FR-021`, `FR-023` |
| **`BR-013`** | Hold Allocation, Notification & 2–3 Day Pickup Window | When a copy of a book with a `WAITING` reservation queue is returned, the copy transitions to `RESERVED` (not `AVAILABLE`), is bound via `readyCopyBarcode` to the `queuePosition == 1` reservation (which transitions to `READY`), a notification is sent to the reserving member, and the copy is held for **2–3 days** (`3 calendar days` target) for pickup. Only the `queuePosition == 1` member may check out that `RESERVED` copy. | **`CONFIRMED`** *(Notification & 2–3 day pickup hold, 2026-10-22)* + `ASSUMPTION` *(FIFO `RESERVED` state, in-app notification, exact 3-day window)* | ADU Lending Services (`idx=313333`) & FAQ (`idx=323130`); `ASSUMPTION-07`, `ASSUMPTION-13` | `FR-010`, `FR-011`, `FR-012`, `FR-018`, `FR-022`, `FR-023` |
| **`BR-014`** | Non-Circulating Reference Works & Material Scope | **Encyclopedias, dictionaries, and catalogs** are non-circulating reference works (`referenceOnly = true`) and cannot be borrowed or reserved. *(Periodicals—where ADU allows 2 non-latest issues for 2 days—and unpublished theses are explicitly Out of Scope because the system manages books only).* | **`CONFIRMED`** *(ADU Library Official Rules, 2026-10-22)* + `ASSUMPTION` *(`referenceOnly` flag)* | ADU Lending Services (`idx=313333`) & Regulation; `ASSUMPTION-14` | `FR-001`, `FR-003`, `FR-010`, `FR-020`, `FR-030` |
| **`BR-015`** | Lost Copy Petition, Fine Freeze & 2x Valuation Penalty | When a member submits a lost-book petition (`lostReportedOn`), **daily overdue fine accrual stops immediately on `lostReportedOn`**. The member has **1 month (`30 calendar days`)** from `lostReportedOn` to replace the book. If not replaced within 1 month, the copy status becomes `LOST` and **twice (2x) the book value** determined by the Valuation Commission (`compensationAmount = 2.00 * appraisedValue`, entered manually by the Librarian) is charged to the member in addition to any fine accrued up to `lostReportedOn`. | **`CONFIRMED`** *(Fine freeze on petition date, 1-month window, 2x valuation charge, 2026-10-22)* + `ASSUMPTION` *(30-day mapping & manual `appraisedValue` entry)* | ADU Lending Services (`idx=313333`) & Regulation; `ASSUMPTION-12`, `ASSUMPTION-15` | `FR-005`, `FR-014`, `FR-027` |
| **`BR-016`** | Personal ID Card & No Proxy Borrowing | All circulation desk checkouts must be performed using the borrower's **own personal university ID card** (represented in LMS by the member's unique `memberId`); **borrowing books on behalf of another person is strictly prohibited**. | **`CONFIRMED`** *(ADU Library Official Rules, 2026-10-22)* | ADU Lending Services (`idx=313333`) & FAQ (`idx=323130`) | `FR-009`, `FR-011` |
| **`BR-017`** | Copy Lifecycle State Machine & Single-Loan Invariant | Each `Book` (`isbn13`) has `1..4` seeded physical copies (`LMS-COPY-1001`..), each in exactly one state: `AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, or `LOST`. At most one `ACTIVE` loan may exist for any `copyBarcode` at any point in time; `LOANED` copies are exactly those with an `ACTIVE` loan, and `RESERVED` copies are exactly those bound to a `READY` reservation's `readyCopyBarcode`. | `ASSUMPTION` | `ASSUMPTION-07`, `ASSUMPTION-09`, `data/README.md` §6 | `FR-001`, `FR-003`, `FR-004`, `FR-005`, `FR-010`, `FR-011`, `FR-012`, `FR-019`, `FR-027` |
| **`BR-018`** | Synthetic Privacy & Startup Auth Seeding | All member (`SYN-STU-*`, `SYN-STF-*`, `SYN-ADM-*`) and librarian (`syn-lib-*`) identities use 100% synthetic data (`@synthetic.lms.local`) with zero real PII and zero passwords in `data/seed/*.json`. Documented synthetic demo passwords are hashed (BCrypt) and seeded at application startup. | `ASSUMPTION` | `ASSUMPTION-08`, `ASSUMPTION-16`, `ASSUMPTION-17` | `FR-006`, `FR-007`, `FR-016`, `FR-019` |

---

## 5. Deterministic Formulas & Calculation Reference

All date and monetary calculations in the domain layer (`LoanPolicyStrategy`, `FineCalculationStrategy`) use ISO-8601 calendar dates (`java.time.LocalDate`) and exact decimal arithmetic (`java.math.BigDecimal` with scale `2`, currency `"TRY"`):

```text
1. Borrowing Quota & Standard Loan Period (BR-002, BR-003 — CONFIRMED):
   MAX_ACTIVE_LOANS = {
       "ACADEMIC_STAFF":       7,
       "ADMINISTRATIVE_STAFF": 3,
       "STUDENT":              3
   }
   LOAN_PERIOD_DAYS = {
       "ACADEMIC_STAFF":       30,
       "ADMINISTRATIVE_STAFF": 30,
       "STUDENT":              30
   }

2. Initial Due Date & Renewed Due Date (BR-003, BR-005):
   renewalCount in {0, 1}
   dueDate = checkoutDate + 30 * (1 + renewalCount)   [in calendar days]

3. Post-Renewal 1-Month Re-Borrowing Cooldown (BR-006 — CONFIRMED + ASSUMPTION-12):
   If previousLoan.isbn13 == requestedBook.isbn13
      AND previousLoan.memberId == requestingMember.memberId
      AND previousLoan.renewalCount >= 1
      AND previousLoan.status == "RETURNED":
      earliestNextCheckoutDate = previousLoan.returnDate + 30 days

4. Overdue Days & Daily Fine Calculation (BR-007, BR-008 — CONFIRMED, BR-009 — ASSUMPTION-10):
   effectiveEndDate = loan.lostReportedOn   if loan.lostReportedOn != null
                      else loan.returnDate  if loan.returnDate != null
                      else currentDate
   overdueDays      = max(0, (effectiveEndDate - loan.dueDate).days)
   DAILY_FINE_RATE  = 0.25 TRY
   overdueFineAmount = 0.25 * overdueDays   [in TRY, no upper cap]

5. Lost-Book Compensation Calculation (BR-015 — CONFIRMED + ASSUMPTION-12, ASSUMPTION-15):
   replacementDeadline = lostReportedOn + 30 days
   If not replaced by replacementDeadline:
      compensationAmount = 2.00 * appraisedValue   [in TRY, entered by Librarian]
      totalLiability     = (0.25 * max(0, (lostReportedOn - dueDate).days)) + compensationAmount
```
