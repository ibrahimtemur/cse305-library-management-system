<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Ordered Scrum product backlog (LMS-001..LMS-020) with estimates, sprint targets, and FR-UC-BR-story traceability; DRAFT pending Product Owner approval of estimates.
-->
# Product Backlog — Library Management System (LMS)

> [!NOTE]
> **DRAFT (estimates proposed, awaiting Product Owner approval).** Totals are produced by `tools/agile/validate_backlog.py` from the table below. `Human h` = human effort (steering agents, review, manual testing, documents); agent working time is not counted. Estimates will be re-calibrated with actual Sprint 1 hours.

## 1. Ordered Backlog

<!-- BACKLOG-TABLE:START -->
| ID | Epic | Story | MoSCoW | Pts | Classic h | Human h | Agent sessions | Sprint | Depends on | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LMS-001 | E1 | Domain model and persistence skeleton | Must | 5 | 8 | 3.5 | 2 | S1 | — |  | Proposed |
| LMS-002 | E1 | Seed loader with date shifting | Must | 8 | 13 | 5 | 3 | S1 | LMS-001 |  | Proposed |
| LMS-003 | E2 | Login/logout with BCrypt demo passwords and RBAC | Must | 8 | 13 | 5 | 3 | S1 | LMS-001, LMS-002 |  | Proposed |
| LMS-004 | E3 | Catalog search and book detail | Must | 5 | 8 | 3.5 | 2 | S1 | LMS-002, LMS-003 |  | Proposed |
| LMS-005 | E3 | Book CRUD, copy registration and copy lifecycle | Must | 13 | 18 | 7.5 | 3 | S1 | LMS-003, LMS-004 |  | Proposed |
| LMS-008 | E8 | Design spike: compensation tracking and reservation terminal states | Must | 2 | 4 | 4 | 1 | S1 | LMS-001 |  | Proposed |
| LMS-006 | E4 | Member registration, profile update and suspension | Must | 5 | 8 | 3.5 | 2 | S2 | LMS-003 |  | Proposed |
| LMS-007 | E5 | Checkout with eligibility, cooldown and referenceOnly enforcement | Must | 13 | 22 | 9 | 4 | S2 | LMS-005, LMS-006 |  | Proposed |
| LMS-009 | E7 | Overdue detection and uncapped fine calculation | Must | 5 | 8 | 3.5 | 2 | S2 | LMS-001 |  | Proposed |
| LMS-010 | E5 | Return of a copy (copy to AVAILABLE only) | Must | 5 | 8 | 3.5 | 2 | S2 | LMS-007, LMS-009 |  | Proposed |
| LMS-013 | E2 | Member self-service portal and librarian member inspection | Must | 8 | 13 | 5 | 3 | S2 | LMS-007, LMS-009, LMS-010 |  | Proposed |
| LMS-017 | E6 | Reservation, FIFO queue, hold promotion and in-app notification | Should | 13 | 21 | 8.5 | 4 | S3 | LMS-010, LMS-008 |  | Proposed |
| LMS-014 | E5 | Loan renewal with reserved guard | Should | 5 | 8 | 3.5 | 2 | S3 | LMS-007 |  | Proposed |
| LMS-011 | E7 | Fine payment and waiver | Should | 5 | 8 | 3.5 | 2 | S3 | LMS-009, LMS-010 |  | Proposed |
| LMS-012 | E6 | Reservation cancellation and hold expiry | Should | 5 | 8 | 3.5 | 2 | S3 | LMS-017 |  | Proposed |
| LMS-016 | E8 | Lost-copy process with runtime appraised value | Should | 8 | 13 | 5.5 | 3 | S3 | LMS-010, LMS-011, LMS-008 |  | Proposed |
| LMS-015 | E9 | Dashboard KPIs and overdue/unpaid report | Should | 8 | 12 | 5 | 2 | S3 | LMS-009, LMS-010 |  | Proposed |
| LMS-018 | E3 | Public guest catalog portal | Could | 3 | 5 | 2 | 1 | S3 | LMS-004 |  | Proposed |
| LMS-019 | E9 | CSV export of overdue and inventory reports | Could | 3 | 5 | 2 | 1 | S3 | LMS-015 |  | Proposed |
| LMS-020 | E3 | Open Library ISBN lookup helper | Could | 5 | 8 | 3.5 | 2 | S3 | LMS-005 |  | Proposed |
<!-- BACKLOG-TABLE:END -->
