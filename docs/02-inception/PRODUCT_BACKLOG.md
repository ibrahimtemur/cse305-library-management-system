<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Ordered Scrum product backlog (LMS-001..LMS-020) with estimates, sprint targets, and FR-UC-BR-story traceability; Sprint 3 commitment line pending Product Owner approval.
-->
# Product Backlog — Library Management System (LMS)

> [!NOTE]
> **Estimates approved by the Product Owner on 2026-11-07; the Sprint 3 order and commitment line are a proposal awaiting approval.** All totals below are pasted from the output of `tools/agile/validate_backlog.py` (re-run it after any table change). `Human h` = human effort (steering agents, review, manual testing, documents); agent working time is not counted. Estimates will be re-calibrated with the actual Sprint 1 hours.

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
| LMS-017 | E6 | Reservation, FIFO queue, hold promotion and in-app notification | Should | 13 | 21 | 8.5 | 4 | S3 | LMS-010, LMS-008 |  | Proposed: commit |
| LMS-011 | E7 | Fine payment and waiver | Should | 5 | 8 | 3.5 | 2 | S3 | LMS-009, LMS-010 |  | Proposed: commit |
| LMS-015 | E9 | Dashboard KPIs and overdue/unpaid report | Should | 8 | 12 | 5 | 2 | S3 | LMS-009, LMS-010 |  | Proposed: commit |
| LMS-012 | E6 | Reservation cancellation and hold expiry | Should | 5 | 8 | 3.5 | 2 | S3 | LMS-017 |  | Proposed: stretch |
| LMS-014 | E5 | Loan renewal with reserved guard | Should | 5 | 8 | 3.5 | 2 | S3 | LMS-007 |  | Proposed: stretch |
| LMS-016 | E8 | Lost-copy process with runtime appraised value | Should | 8 | 13 | 5.5 | 3 | S3 | LMS-010, LMS-011, LMS-008 |  | Proposed: stretch |
| LMS-018 | E3 | Public guest catalog portal | Could | 3 | 5 | 2 | 1 | S3 | LMS-004 |  | Proposed: stretch |
| LMS-019 | E9 | CSV export of overdue and inventory reports | Could | 3 | 5 | 2 | 1 | S3 | LMS-015 |  | Proposed: stretch |
| LMS-020 | E3 | Open Library ISBN lookup helper | Could | 5 | 8 | 3.5 | 2 | S3 | LMS-005 |  | Proposed: stretch |
<!-- BACKLOG-TABLE:END -->

Epics: E1 Data import and seed loader, E2 Authentication, RBAC and member self-service, E3 Catalog, search and copy lifecycle, E4 Member management, E5 Borrowing, returning and renewal, E6 Reservations and pickup holds, E7 Overdue and fines, E8 Lost-copy handling, E9 Dashboard and CSV reports (see [`THEMES_EPICS.md`](THEMES_EPICS.md)). Story details: [`USER_STORIES.md`](USER_STORIES.md). `Owner` stays empty until sprint planning.

## 2. Totals (script output)

- Story points: 132
- Human hours: 90.0 (classic effort 211.0)
- Agent sessions: 46
- Must: 11 stories, 77 pts, 53.0 h
- Should: 6 stories, 44 pts, 29.5 h
- Could: 3 stories, 11 pts, 7.5 h

## 3. Capacity and Must-fit check (script output)

| Sprint | Gross | Ceremonies | HW docs | Buffer | Net for stories | Planned | Must | Should | Could | Planned - Net |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 (Nov 11–Dec 08) | 46.9 | 4.0 | 8.0 | 4.7 | 30.2 | 28.5 | 28.5 | 0.0 | 0.0 | -1.7 |
| S2 (Dec 09–Dec 22) | 32.0 | 4.0 | 4.0 | 3.2 | 20.8 | 24.5 | 24.5 | 0.0 | 0.0 | +3.7 |
| S3 (Dec 23–Jan 05) | 32.0 | 4.0 | 7.0 | 3.2 | 17.8 | 37.0 | 0.0 | 29.5 | 7.5 | +19.2 |

- Must human hours: 53.0 (in S1+S2: 53.0)
- S1+S2 net capacity: 51.0
- Result: KNOWN GAP, ACCEPTED RISK (Must - Net = +2.0 h = 4.0 percent of net; trigger is 10 percent)

> [!WARNING]
> **Known gap (accepted by the Product Owner, 2026-11-07):** Must stories need 53.0 h in Sprint 1 + Sprint 2 against a net capacity of 51.0 h, a gap of 2.0 h (about 4 percent of net, below the estimate uncertainty). The buffer is **not** reduced. Sprint 3 Should stories act as shock absorber (see [`SPRINT_PLAN.md`](SPRINT_PLAN.md)).

## 4. Sprint 3 Commitment Line (proposed order, script output)

- Sprint 3 net capacity: 17.8
| Rank | Story | MoSCoW | Human h | Cumulative h | Line |
|---|---|---|---|---|---|
| 1 | LMS-017 Reservation, FIFO queue, hold promotion and in-app notification | Should | 8.5 | 8.5 | COMMIT |
| 2 | LMS-011 Fine payment and waiver | Should | 3.5 | 12.0 | COMMIT |
| 3 | LMS-015 Dashboard KPIs and overdue/unpaid report | Should | 5.0 | 17.0 | COMMIT |
| 4 | LMS-012 Reservation cancellation and hold expiry | Should | 3.5 | 20.5 | STRETCH |
| 5 | LMS-014 Loan renewal with reserved guard | Should | 3.5 | 24.0 | STRETCH |
| 6 | LMS-016 Lost-copy process with runtime appraised value | Should | 5.5 | 29.5 | STRETCH |
| 7 | LMS-018 Public guest catalog portal | Could | 2.0 | 31.5 | STRETCH |
| 8 | LMS-019 CSV export of overdue and inventory reports | Could | 2.0 | 33.5 | STRETCH |
| 9 | LMS-020 Open Library ISBN lookup helper | Could | 3.5 | 37.0 | STRETCH |

Rationale for the order (proposal, **not final until approved by the Product Owner**): `LMS-017` first because the reservation queue is part of the MVP named in the course schedule and the hold promotion is the core library value; `LMS-011` second because without payment/waiver an `UNPAID` fine can never be cleared and `BR-011` would block the member forever; `LMS-015` third because the course schedule names the dashboard in the MVP. `LMS-012`, `LMS-014`, `LMS-016` follow by value; `LMS-016` also needs the `LMS-008` decision and `LMS-011`.

## 5. Traceability: FR -> UC -> BR -> Story (script output)

Every Must FR (`FR-001`..`FR-019`) is covered by a story in Sprint 1 or Sprint 2; every Should/Could FR has a story in Sprint 3. Check: `python3 tools/agile/validate_backlog.py` prints "Must FR not covered in S1+S2: none".

| FR | MoSCoW | UC | BR | Story | Sprint |
|---|---|---|---|---|---|
| FR-001 | Must Have | UC-03 | BR-014, BR-017 | LMS-005 | S1 |
| FR-002 | Must Have | UC-01 | BR-001, BR-014 | LMS-004 | S1 |
| FR-003 | Must Have | UC-01 | BR-014, BR-017 | LMS-004 | S1 |
| FR-004 | Must Have | UC-03 | BR-017 | LMS-005 | S1 |
| FR-005 | Must Have | UC-03, UC-05, UC-06, UC-09 | BR-015, BR-017 | LMS-005 | S1 |
| FR-006 | Must Have | UC-04 | BR-002, BR-018 | LMS-006 | S2 |
| FR-007 | Must Have | UC-04 | BR-011, BR-018 | LMS-006 | S2 |
| FR-008 | Must Have | UC-04, UC-10 | BR-002, BR-006, BR-011 | LMS-013 | S2 |
| FR-009 | Must Have | UC-05 | BR-002, BR-006, BR-011, BR-016 | LMS-007 | S2 |
| FR-010 | Must Have | UC-05 | BR-013, BR-014, BR-017 | LMS-007 | S2 |
| FR-011 | Must Have | UC-05 | BR-002, BR-003, BR-013, BR-016, BR-017 | LMS-007 | S2 |
| FR-012 | Must Have | UC-06 | BR-007, BR-008, BR-013, BR-017 | LMS-010 | S2 |
| FR-013 | Must Have | UC-05, UC-06 | BR-006 | LMS-007 | S2 |
| FR-014 | Must Have | UC-06, UC-09, UC-11 | BR-007, BR-015 | LMS-009 | S2 |
| FR-015 | Must Have | UC-06, UC-09, UC-11 | BR-008, BR-009, BR-010 | LMS-009 | S2 |
| FR-016 | Must Have | UC-02 | BR-001, BR-018 | LMS-003 | S1 |
| FR-017 | Must Have | UC-02 | BR-001 | LMS-003 | S1 |
| FR-018 | Must Have | UC-10 | BR-001, BR-010, BR-013 | LMS-013 | S2 |
| FR-019 | Must Have | System Startup | BR-017, BR-018 | LMS-002 | S1 |
| FR-020 | Should Have | UC-08 | BR-011, BR-012, BR-014 | LMS-017 | S3 |
| FR-021 | Should Have | UC-08 | BR-012 | LMS-017 | S3 |
| FR-022 | Should Have | UC-06, UC-08, UC-10 | BR-013 | LMS-017 | S3 |
| FR-023 | Should Have | UC-08 | BR-012, BR-013 | LMS-012 | S3 |
| FR-024 | Should Have | UC-07 | BR-003, BR-004, BR-005, BR-011 | LMS-014 | S3 |
| FR-025 | Should Have | UC-09 | BR-010, BR-011 | LMS-011 | S3 |
| FR-026 | Should Have | UC-09 | BR-010, BR-011 | LMS-011 | S3 |
| FR-027 | Should Have / Could Have | UC-09 | BR-005, BR-015, BR-017 | LMS-016 | S3 |
| FR-028 | Should Have | UC-11 | BR-001, BR-007, BR-008 | LMS-015 | S3 |
| FR-029 | Should Have | UC-11 | BR-007, BR-008, BR-011 | LMS-015 | S3 |
| FR-030 | Could Have (`C1`) | UC-01 | BR-001, BR-014 | LMS-018 | S3 |
| FR-031 | Could Have (`C2`) | UC-03 | BR-001 | LMS-020 | S3 |
| FR-032 | Could Have (`C3`) | UC-11 | BR-001 | LMS-019 | S3 |
