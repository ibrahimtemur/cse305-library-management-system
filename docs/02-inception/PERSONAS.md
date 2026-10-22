<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: User personas for Librarian/Admin, Student Member, Academic Staff Member, Administrative Staff Member, and Guest, grounded in real seed records from data/seed/*.json and confirmed ADU lending policies.
-->
# User Personas — Library Management System (LMS)

- **Course:** CSE305 Software Engineering — Adnan Menderes University (ADU)
- **Phase:** Inception (`HW02`)
- **Date:** 2026-10-22

> [!IMPORTANT]
> **100% Synthetic Identities Grounded in `data/seed/*.json`:** Every named persona and circulation example below is read directly from the committed synthetic seed files ([`data/seed/librarians.json`](../../data/seed/librarians.json), [`data/seed/members.json`](../../data/seed/members.json), [`data/seed/books-openlibrary.json`](../../data/seed/books-openlibrary.json), [`data/seed/copies.json`](../../data/seed/copies.json), [`data/seed/loans.json`](../../data/seed/loans.json), [`data/seed/fines.json`](../../data/seed/fines.json), and [`data/seed/reservations.json`](../../data/seed/reservations.json)). None of these profiles correspond to any real Adnan Menderes University student, staff member, or librarian. See [`data/README.md`](../../data/README.md) for seed dataset documentation.

---

## 1. Persona Summary Matrix

| Persona | System Role | Member Type (`memberType`) | Representative Seed Record | Confirmed Borrowing Quota (`BR-002`) | Confirmed Loan Period (`BR-003`) | Primary Interface Focus |
|---|---|---|---|---|---|---|
| **1. Librarian / Admin** | `ROLE_LIBRARIAN` | N/A (Staff Account) | `username: "syn-lib-0001"` (`Enginiz Yıldırım`) in [`librarians.json`](../../data/seed/librarians.json) | Operational Administrator | N/A | Circulation Desk, Catalog & Copy CRUD, Member Mgmt, Fine & Lost-Book Settlement, KPI Dashboard |
| **2. Student Member** | `ROLE_MEMBER` | `STUDENT` | `memberId: "SYN-STU-0001"` (`Tutkucan Ergül`) & `"SYN-STU-0044"` (`Peren Erdoğan`) in [`members.json`](../../data/seed/members.json) | Max **3 books** (`CONFIRMED`) | **30 calendar days** (`CONFIRMED`) | Self-Service Catalog Search, Own Loans/Fines View, Online Renewal, Hold Queue |
| **3. Academic Staff Member** | `ROLE_MEMBER` | `ACADEMIC_STAFF` | `memberId: "SYN-STF-0003"` (`Atasagun Öcalan`) & `"SYN-STF-0002"` (`Baydu Arsoy`) in [`members.json`](../../data/seed/members.json) | Max **7 books** (`CONFIRMED`) | **30 calendar days** (`CONFIRMED`) | Research Catalog Lookup, Higher-Quota Borrowing (`7` books), Self-Service Renewal & Holds |
| **4. Administrative Staff Member** | `ROLE_MEMBER` | `ADMINISTRATIVE_STAFF` | `SYN-ADM-0001` *(planned in upcoming seed regeneration per `OPEN-06`)* | Max **3 books** (`CONFIRMED`) | **30 calendar days** (`CONFIRMED`) | Self-Service Catalog Lookup, Borrowing up to `3` Books, Own Loans/Fines View |
| **5. Guest Visitor** | `ROLE_GUEST` | Unauthenticated | Anonymous browser session | **0 books** (Read-Only) | N/A | Public Read-Only Catalog Search & Shelf Availability Lookup |

---

## 2. Detailed Persona Profiles

### Persona 1 — Librarian / System Administrator (`ROLE_LIBRARIAN`)

- **Seed Record Reference ([`data/seed/librarians.json`](../../data/seed/librarians.json)):**
  ```json
  {
    "username": "syn-lib-0001",
    "displayName": "Enginiz Yıldırım",
    "email": "syn-lib-0001@synthetic.lms.local",
    "role": "ROLE_LIBRARIAN"
  }
  ```
  *(Additional seeded librarian colleagues: `syn-lib-0002` `Sonad Zengin` and `syn-lib-0003` `Muvahhide Yorulmaz`.)*
- **Role Context:** Full-time circulation desk librarian and catalog administrator (`ASSUMPTION-01` unifies Librarian and Admin responsibilities in the MVP). Authenticates locally using `username: "syn-lib-0001"` and a BCrypt-hashed demo password seeded at application startup (`BR-018`).
- **Goals:**
  - Process book checkouts and returns rapidly using a member's personal university ID card number (`memberId`) and the physical copy's barcode (`barcode`, e.g., `LMS-COPY-1001`) without manual date arithmetic.
  - Rely on the system to automatically enforce confirmed ADU borrowing rules: member-type quotas (`7` for `ACADEMIC_STAFF`, `3` for `ADMINISTRATIVE_STAFF` and `STUDENT`), `30`-day due dates, non-circulating reference book restrictions (`BR-014`), 1-month (`30`-day) post-renewal re-borrowing cooldowns (`BR-006`), and automatic borrowing blocks when a member holds an overdue item or an unpaid fine (`BR-011`).
  - Maintain accurate copy-level states (`AVAILABLE`, `LOANED`, `RESERVED`, `MAINTENANCE`, `LOST`), handle lost-book petitions (`BR-015`: freezing overdue fines on the report date and assessing `2 * appraisedValue` if unreplaced after 1 month), and record desk fine payments (`PAID`) or administrative waivers (`WAIVED`) with full auditability (`settledBy: "syn-lib-0001"`).
  - Monitor daily library health via the Operational Dashboard (active loans, due-soon loans within `0..3` days, overdue loans, and unpaid fine balances).
- **Pain Points:**
  - Checking manually whether a returned book has a waiting reservation queue—and remembering to set the copy aside in `RESERVED` state for the `2–3 day` pickup window (`BR-013`) instead of reshelving it—is error-prone without automated prompts.
  - Verifying whether a student trying to borrow a book is acting on their own behalf (`BR-016`) or recently returned a renewed copy of the same title within the last 1 month (`BR-006`) is impossible to track reliably on paper.
  - Calculating overdue penalties (`0.25 TRY/day` per overdue book, `BR-008`) or halting fine accrual when a student submits a lost-book petition requires deterministic date tracking.
- **Typical Scenarios:**
  1. **Desk Checkout (`UC-05`):** Student `Tutkucan Ergül` (`SYN-STU-0001`) presents her personal university ID card at the desk to borrow copy `LMS-COPY-1002` of Yașar Kemal's *İnce Memed* (`isbn13: "9780002615075"`). `Enginiz Yıldırım` (`syn-lib-0001`) enters `SYN-STU-0001` and `LMS-COPY-1002`; the system verifies she has no overdue loans or unpaid fines, is below her 3-book limit, and creates a 30-day loan.
  2. **Copy Return & Hold Allocation (`UC-06`):** When a borrowed copy of Robert Sedgewick's *Algorithms* (`isbn13: "9780321573513"`) is returned at the desk, the system detects active `WAITING` reservation `RES-0004` (`memberId: "SYN-STU-0032"`, `queuePosition: 1`), transitions the copy to `RESERVED` instead of `AVAILABLE`, binds `readyCopyBarcode`, and triggers an in-app pickup notification for the 2–3 day hold window.
  3. **Fine Settlement & Waiver (`UC-09`):** `Enginiz Yıldırım` reviews an `UNPAID` fine (such as `FINE-0019` on `LOAN-0105` for member `SYN-STU-0025`, or `FINE-0005` on `LOAN-0028` for `SYN-STU-0038` which `syn-lib-0001` settled as `PAID` on `2026-03-20`) and records payment or waiver, immediately clearing the financial block on the member's profile.

---

### Persona 2 — Student Member (`ROLE_MEMBER`, `memberType = "STUDENT"`)

- **Seed Record Reference ([`data/seed/members.json`](../../data/seed/members.json)):**
  ```json
  {
    "memberId": "SYN-STU-0001",
    "firstName": "Tutkucan",
    "lastName": "Ergül",
    "email": "syn-stu-0001@synthetic.lms.local",
    "memberType": "STUDENT",
    "status": "ACTIVE",
    "department": "Chemistry",
    "registeredOn": "2025-07-28"
  }
  ```
  *(Additional representative student records in [`members.json`](../../data/seed/members.json): `SYN-STU-0044` `Peren Erdoğan` in `Computer Engineering`, and `SYN-STU-0003` `Hazrat Yorulmaz` who holds `READY` reservation `RES-0009` on `isbn13: "9780345451323"` with `readyCopyBarcode: "LMS-COPY-1599"`.)*
- **Role Context:** Undergraduate student who borrows course textbooks and general reading books. Subject to confirmed ADU student rules: maximum **3 active loans** simultaneously (`BR-002`) for **30 calendar days** per loan (`BR-003`), with a daily overdue fine of **0.25 TRY/day** (`BR-008`).
- **Goals:**
  - Search the catalog by title, author, `isbn13`, or subject category (e.g., `Computer Science`, `Programming`, `Databases`, `Chemistry`) before walking to the library.
  - Log in to the **Member Self-Service Portal (`UC-10`)** to inspect her own active loans, exact due dates, historical returned loans, and any accrued overdue fines.
  - Renew an active loan online (`UC-07`) once (`renewalCount: 0 -> 1`, `+30` days) when she needs extra study time, provided the book is not overdue and no other member has reserved it (`BR-004`, `BR-005`).
  - Place a title-level reservation (`UC-08`) when all copies of a required textbook (such as *Algorithms*, `isbn13: "9780321573513"`) are currently `LOANED`, and see an in-app notification when a returned copy is held as `READY` for her for `2–3 days` (`BR-013`).
- **Pain Points:**
  - Visiting the library desk only to discover that all copies of a textbook are checked out, or that a dictionary/encyclopedia she wanted to take home is a non-circulating reference work (`BR-014`).
  - Forgetting a due date and discovering at the circulation desk that an overdue loan (such as `LOAN-0099` on `LMS-COPY-2119`) or a small unpaid fine (`0.25 TRY/day`) blocks her from checking out any new books (`BR-011`).
  - Not realizing that once she renews a book and returns it, she must wait **1 month (`30 calendar days`)** before borrowing that same title again (`BR-006`).
- **Typical Scenarios:**
  1. **Self-Service Loan & Fine Tracking (`UC-10`):** `Tutkucan Ergül` (`SYN-STU-0001`) logs in and views her active loan (`LOAN-0099`, copy `LMS-COPY-2119`) alongside its due date and any accruing overdue fine.
  2. **Joining and Picking Up from the Hold Queue (`UC-08`, `UC-05`):** Student `Hazrat Yorulmaz` (`SYN-STU-0003`) places a reservation (`RES-0009`) on `isbn13: "9780345451323"` when no copies are `AVAILABLE`. When copy `LMS-COPY-1599` is returned, `RES-0009` transitions to `status: "READY"` with `readyCopyBarcode: "LMS-COPY-1599"`; `SYN-STU-0003` sees the in-app notification and visits the desk with his ID card within the 2–3 day pickup window to check out `LMS-COPY-1599`.

---

### Persona 3 — Academic Staff Member (`ROLE_MEMBER`, `memberType = "ACADEMIC_STAFF"`)

- **Seed Record Reference ([`data/seed/members.json`](../../data/seed/members.json)):**
  ```json
  {
    "memberId": "SYN-STF-0003",
    "firstName": "Atasagun",
    "lastName": "Öcalan",
    "email": "syn-stf-0003@synthetic.lms.local",
    "memberType": "ACADEMIC_STAFF",
    "status": "ACTIVE",
    "department": "Computer Engineering",
    "registeredOn": "2023-08-18"
  }
  ```
  *(Additional representative academic staff records: `SYN-STF-0002` `Baydu Arsoy` in `Mathematics` holding `RES-0001` on `9780130960160` *SQL Fundamentals*, and `SYN-STF-0001` `Gülçe Akdeniz` in `Philosophy`.)*
- **Role Context:** Faculty member and researcher preparing lecture materials and conducting academic research. Under confirmed ADU library regulations, `ACADEMIC_STAFF` members are granted a higher simultaneous borrowing quota of up to **7 books** (`BR-002`) for **30 calendar days** per loan (`BR-003`).
- **Goals:**
  - Keep up to `7` specialized reference and technical books checked out simultaneously across a 30-day research cycle.
  - Check how many physical copies of a textbook exist in the library catalog (`M1`) when recommending course readings to students.
  - Use the Member Self-Service Portal (`UC-10`) to track all active loans, renew non-reserved titles (`UC-07`), and queue for high-demand titles (`UC-08`, e.g., `RES-0007` held by `SYN-STF-0003` at `queuePosition: 1` on `isbn13: "9780345309884"`).
- **Pain Points:**
  - High-demand computing and mathematics titles are frequently checked out by students during midterm and final weeks, requiring a transparent FIFO reservation queue (`BR-012`) and prompt hold-ready notifications (`BR-013`).
  - Even with a 7-book quota, a single forgotten overdue book or unpaid `0.25 TRY/day` fine immediately blocks new checkouts and renewals across the entire account (`BR-011`).
  - Cannot dispatch a teaching assistant or student to borrow books on his behalf because ADU rules strictly require personal ID presentation and prohibit proxy borrowing (`BR-016`).
- **Typical Scenarios:**
  1. **Multi-Book Research Checkout (`UC-05`):** `Atasagun Öcalan` (`SYN-STF-0003`) borrows multiple Computer Science and Software Engineering titles in person at the desk; `LoanPolicyStrategy` resolves `AcademicStaffLoanPolicy` (`maxActiveLoans = 7`, `loanPeriodDays = 30`).
  2. **Reservation Queue Priority (`UC-08`):** `Baydu Arsoy` (`SYN-STF-0002`) places reservation `RES-0001` (`queuePosition: 1`, `createdOn: "2026-10-12"`) on John J. Patrick's *SQL Fundamentals* (`isbn13: "9780130960160"`), ahead of student `SYN-STU-0034` (`RES-0002`, `queuePosition: 2`, `createdOn: "2026-10-13"`), and monitors his queue position via the self-service portal.

---

### Persona 4 — Administrative Staff Member (`ROLE_MEMBER`, `memberType = "ADMINISTRATIVE_STAFF"`)

- **Seed Convention Reference (`ASSUMPTION-17`, `OPEN-06`):**
  ```json
  {
    "memberId": "SYN-ADM-0001",
    "firstName": "<Faker tr_TR synthetic first name>",
    "lastName": "<Faker tr_TR synthetic last name>",
    "email": "syn-adm-0001@synthetic.lms.local",
    "memberType": "ADMINISTRATIVE_STAFF",
    "status": "ACTIVE",
    "department": "Business Administration",
    "registeredOn": "2024-03-15"
  }
  ```
  *(Note: The initial `data/seed/members.json` snapshot generated under HW01 assumptions included `STUDENT` and `ACADEMIC_STAFF` rows; `ADMINISTRATIVE_STAFF` rows using `SYN-ADM-*` will be included when `tools/data/generate_synthetic.py` is regenerated for the confirmed ADU rules as tracked in `OPEN-06`.)*
- **Role Context:** University administrative personnel borrowing general literature, history, or professional development books. Under confirmed ADU rules (`BR-002`, `BR-003`), administrative staff share the same borrowing quota and duration as students: at most **3 active loans** simultaneously for **30 calendar days**.
- **Goals:**
  - Browse Turkish Literature, History, and Business Administration books during lunch breaks, check shelf availability, borrow up to `3` books in person with their university staff ID card (`BR-016`), and review due dates or renew loans via the Member Self-Service Portal (`UC-07`, `UC-10`).
- **Pain Points:**
  - Needs clear visibility into due dates (`30` days) and non-circulating reference restrictions (`BR-014`) without having to call the circulation desk.
- **Typical Scenarios:**
  1. **Self-Service Lookup & Renewal (`UC-01`, `UC-07`):** Checks copy availability online, borrows a book at the circulation desk (`AdministrativeStaffLoanPolicy`: `maxActiveLoans = 3`, `loanPeriodDays = 30`), and renews the loan once online before its due date.

---

### Persona 5 — Guest Visitor (`ROLE_GUEST`)

- **Identity Context:** Unauthenticated public user browsing the web application without signing in (`ROLE_GUEST`).
- **Goals:**
  - Search and filter the library's bibliographic catalog by title, author, `isbn13`, or subject category (`UC-01`).
  - Inspect whether physical copies of a book (e.g., `9780002614511`, *Ağrıdağı efsanesi*, copy `LMS-COPY-1001`) are currently `AVAILABLE` on the shelf or marked as non-circulating reference material (`BR-014`).
- **Pain Points:**
  - Wants immediate, friction-free catalog search without mandatory login walls, while understanding that borrowing, renewing, or reserving requires signing in as a registered library member.
- **Typical Scenarios:**
  1. **Public Catalog Browse (`UC-01`):** A visitor opens the public catalog portal (`C1`), searches for `"Yaşar Kemal"`, views the book details and copy availability counts, and sees a prompt to sign in (`UC-02`) if they click "Reserve Book".
