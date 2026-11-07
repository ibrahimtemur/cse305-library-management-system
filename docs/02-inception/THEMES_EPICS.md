<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Four themes and nine epics of the LMS product with story assignment and totals generated from the product backlog.
-->
# Themes and Epics — Library Management System (LMS)

- **Version:** 1.0 — 2026-11-07
- **Hierarchy:** Theme -> Epic -> User story -> Task ([`USER_STORIES.md`](USER_STORIES.md), [`TASKS.md`](TASKS.md)). Counts and hours are produced from [`PRODUCT_BACKLOG.md`](PRODUCT_BACKLOG.md) by `tools/agile/` scripts.

## 1. Theme and Epic Overview

| Theme | Epic | Goal | Stories | Points | Human h |
|---|---|---|---|---|---|
| **T1 Platform Foundation** | | Data and access foundations every other feature relies on | 4 | 29 | 18.5 |
| | E1 Data import and seed loader | Load seed v2 reproducibly with dates shifted to the start day (OPEN-04). | 2 | 13 | 8.5 |
| | E2 Authentication, RBAC and member self-service | Local login with BCrypt demo passwords (OPEN-05), role-based access, member self-service. | 2 | 16 | 10.0 |
| **T2 Collection and Membership** | | Who and what the library holds | 5 | 31 | 20.0 |
| | E3 Catalog, search and copy lifecycle | Find books, maintain books and copies, enforce copy states and referenceOnly display. | 4 | 26 | 16.5 |
| | E4 Member management | Register, edit and suspend synthetic members. | 1 | 5 | 3.5 |
| **T3 Circulation** | | Lending, returning, renewing and holding books | 5 | 41 | 28.0 |
| | E5 Borrowing, returning and renewal | Desk checkout, return and single renewal under confirmed ADU rules. | 3 | 23 | 16.0 |
| | E6 Reservations and pickup holds | Title-level FIFO holds, in-app notification, 3-day pickup window. | 2 | 18 | 12.0 |
| **T4 Compliance and Insight** | | Fines, lost copies and management information | 6 | 31 | 23.5 |
| | E7 Overdue and fines | Deterministic overdue days and uncapped 0.25 TRY/day fines; payment and waiver. | 2 | 10 | 7.0 |
| | E8 Lost-copy handling | Lost-copy petition, 30-day window, 2x appraised value entered at runtime; design spike. | 2 | 10 | 9.5 |
| | E9 Dashboard and CSV reports | Operational KPIs, overdue/unpaid report, CSV export. | 2 | 11 | 7.0 |
| **Total** | 9 epics | | 20 | 132 | 90.0 |

## 2. Diagram

```mermaid
flowchart LR
  P["LMS Product"]
  P --> T1["T1 Platform Foundation"]
  T1 --> E1["E1 Data import and seed loader"]
  T1 --> E2["E2 Authentication, RBAC and member self-service"]
  P --> T2["T2 Collection and Membership"]
  T2 --> E3["E3 Catalog, search and copy lifecycle"]
  T2 --> E4["E4 Member management"]
  P --> T3["T3 Circulation"]
  T3 --> E5["E5 Borrowing, returning and renewal"]
  T3 --> E6["E6 Reservations and pickup holds"]
  P --> T4["T4 Compliance and Insight"]
  T4 --> E7["E7 Overdue and fines"]
  T4 --> E8["E8 Lost-copy handling"]
  T4 --> E9["E9 Dashboard and CSV reports"]
```

## 3. Stories per Epic

| Epic | Stories |
|---|---|
| E1 Data import and seed loader | LMS-001 (Must, S1), LMS-002 (Must, S1) |
| E2 Authentication, RBAC and member self-service | LMS-003 (Must, S1), LMS-013 (Must, S2) |
| E3 Catalog, search and copy lifecycle | LMS-004 (Must, S1), LMS-005 (Must, S1), LMS-018 (Could, S3), LMS-020 (Could, S3) |
| E4 Member management | LMS-006 (Must, S2) |
| E5 Borrowing, returning and renewal | LMS-007 (Must, S2), LMS-010 (Must, S2), LMS-014 (Should, S3) |
| E6 Reservations and pickup holds | LMS-017 (Should, S3), LMS-012 (Should, S3) |
| E7 Overdue and fines | LMS-009 (Must, S2), LMS-011 (Should, S3) |
| E8 Lost-copy handling | LMS-008 (Must, S1), LMS-016 (Should, S3) |
| E9 Dashboard and CSV reports | LMS-015 (Should, S3), LMS-019 (Could, S3) |
