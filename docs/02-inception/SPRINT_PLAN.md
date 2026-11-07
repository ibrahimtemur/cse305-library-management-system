<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Three-sprint iteration plan with capacity model, Must gap, Sprint 3 commitment line, dependency proof, Definition of Ready/Done, and risk list.
-->
# Sprint Plan and Iteration Plan — Library Management System (LMS)

- **Version:** 1.0 (draft; Sprint 3 order pending Product Owner approval) — 2026-11-07
- **Numbers:** every figure below is pasted from `tools/agile/validate_backlog.py`.

## 1. Sprints

| Sprint | Dates | Homework | Goal |
|---|---|---|---|
| Sprint 1 | Nov 11 – Dec 8 | HW03 (Elaboration + Sprint 1) | Foundation: domain model, seed loader with date shifting, login/RBAC, catalog search, book/copy management, design spike (`LMS-008`) |
| Sprint 2 | Dec 9 – Dec 22 | HW04 (Construction + Sprint 2) | Circulation core: members, checkout, return, fine calculation, self-service |
| Sprint 3 (MVP) | Dec 23 – Jan 5 | HW05 (Transition + MVP) | Reservations with hold promotion, fine settlement, dashboard; stretch items below the commitment line |

Midterm weeks Nov 17 – Nov 28 reduce capacity. The iteration plan follows the Unified Process phases of the course: Inception (HW01–HW02), Elaboration (HW03), Construction (HW04), Transition (HW05).

## 2. Capacity Model (assumptions, to be re-calibrated with actual Sprint 1 hours)

| Assumption | Value |
|---|---|
| Unit | Human hours of two students (steering agents, review, manual tests, documents); agent working time is not counted |
| Weekly hours per person | 8 h normal weeks, 3 h during midterm weeks (Nov 17 – Nov 28); prorated per calendar day |
| Ceremonies (planning, review, retrospective) | 4 h per sprint (2 people x 2 h) |
| HW document and delivery work | HW03 8 h (use case diagram 1.5, system sequence diagrams 2, class diagram 2, TDD/Git/Maven plan 1, Stitch UI review 1.5), HW04 4 h, HW05 7 h (user guide, test report, project retrospective review) |
| Buffer | 10 percent of gross capacity, not reduced |
| Estimation ratio | Human hours are about 0.40 x classic effort (assumption). **Sprint 1 actuals will be used to re-calibrate.** |

| Sprint | Gross | Ceremonies | HW docs | Buffer | Net for stories | Planned | Must | Should | Could | Planned - Net |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 (Nov 11–Dec 08) | 46.9 | 4.0 | 8.0 | 4.7 | 30.2 | 28.5 | 28.5 | 0.0 | 0.0 | -1.7 |
| S2 (Dec 09–Dec 22) | 32.0 | 4.0 | 4.0 | 3.2 | 20.8 | 24.5 | 24.5 | 0.0 | 0.0 | +3.7 |
| S3 (Dec 23–Jan 05) | 32.0 | 4.0 | 7.0 | 3.2 | 17.8 | 37.0 | 0.0 | 29.5 | 7.5 | +19.2 |

## 3. Must Gap (accepted risk)

- Must human hours: 53.0 (in S1+S2: 53.0)
- S1+S2 net capacity: 51.0
- Result: KNOWN GAP, ACCEPTED RISK (Must - Net = +2.0 h = 4.0 percent of net; trigger is 10 percent)

**Must S1+S2 = 53.0 h, net 51.0 h, gap 2.0 h.** The gap is documented, not hidden; the buffer is not reduced. Rules agreed with the Product Owner on 2026-11-07:

1. **Shock absorber:** if Must work overruns in Sprint 2, the overrun is taken from the Sprint 3 Should stories (lowest rank first), never from the buffer.
2. **Re-plan trigger:** if at the end of Sprint 1 the ratio *actual human hours / classic effort* exceeds 0.45, or if the Sprint 2 Must estimate exceeds the net capacity by more than 10 percent, the Sprint 2 plan is redone and the scope decision is asked from the Product Owner.
3. The gap is also listed in the risk list (RISK-H01).

## 4. Sprint Backlogs

### Sprint 1 (Nov 11 – Dec 8)

| Story | Title | MoSCoW | Pts | Human h | Cumulative h | Depends on |
|---|---|---|---|---|---|---|
| LMS-001 | Domain model and persistence skeleton | Must | 5 | 3.5 | 3.5 | — |
| LMS-002 | Seed loader with date shifting | Must | 8 | 5.0 | 8.5 | LMS-001 |
| LMS-003 | Login/logout with BCrypt demo passwords and RBAC | Must | 8 | 5.0 | 13.5 | LMS-001, LMS-002 |
| LMS-004 | Catalog search and book detail | Must | 5 | 3.5 | 17.0 | LMS-002, LMS-003 |
| LMS-005 | Book CRUD, copy registration and copy lifecycle | Must | 13 | 7.5 | 24.5 | LMS-003, LMS-004 |
| LMS-008 | Design spike: compensation tracking and reservation terminal states | Must | 2 | 4.0 | 28.5 | LMS-001 |

### Sprint 2 (Dec 9 – Dec 22)

| Story | Title | MoSCoW | Pts | Human h | Cumulative h | Depends on |
|---|---|---|---|---|---|---|
| LMS-006 | Member registration, profile update and suspension | Must | 5 | 3.5 | 3.5 | LMS-003 |
| LMS-007 | Checkout with eligibility, cooldown and referenceOnly enforcement | Must | 13 | 9.0 | 12.5 | LMS-005, LMS-006 |
| LMS-009 | Overdue detection and uncapped fine calculation | Must | 5 | 3.5 | 16.0 | LMS-001 |
| LMS-010 | Return of a copy (copy to AVAILABLE only) | Must | 5 | 3.5 | 19.5 | LMS-007, LMS-009 |
| LMS-013 | Member self-service portal and librarian member inspection | Must | 8 | 5.0 | 24.5 | LMS-007, LMS-009, LMS-010 |

### Sprint 3 (Dec 23 – Jan 5) — proposed order and commitment line

Should stories are ordered by value; the line is drawn where the cumulative hours reach the Sprint 3 net capacity. **Stories at or above the line are the commitment; stories below are stretch.** The MVP is defined as **all Must stories plus the Should stories above the line**. Items below the line are marked *at risk*. This order is a **proposal until the Product Owner approves it**.

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

Rationale: `LMS-017` is the core library value and part of the MVP named in the course schedule; `LMS-011` is needed so that `UNPAID` fines can be cleared (otherwise `BR-011` blocks the member permanently); `LMS-015` is the dashboard named in the course schedule; `LMS-012` (hold expiry), `LMS-014` (renewal), and `LMS-016` (lost copy, needs `LMS-008`) follow by value. Could stories `LMS-018`..`LMS-020` are stretch. **Items below the line are at risk** (see RISK-H02).

## 5. Dependency Fixes

- `LMS-010` (Return) only returns the copy to `AVAILABLE`; the `RESERVED` transition and hold promotion belong to `LMS-017`.
- `LMS-013` (Self-service) shows active loans, history, cooldowns, and fines only; holds, reservations, and notifications are added by `LMS-017`.
- `LMS-014` (Renewal) implements the "reserved" guard as a repository query that returns `false` until reservations exist (`LMS-017`).
- `LMS-016` and `LMS-017` consume the `LMS-008` design decisions.

### Dependency proof (script output)

No story depends on a story of a later sprint:

| Story | Sprint | Depends on | Dependency sprint | OK |
|---|---|---|---|---|
| LMS-001 | S1 | — | — | yes |
| LMS-002 | S1 | LMS-001 | S1 | yes |
| LMS-003 | S1 | LMS-001 | S1 | yes |
| LMS-003 | S1 | LMS-002 | S1 | yes |
| LMS-004 | S1 | LMS-002 | S1 | yes |
| LMS-004 | S1 | LMS-003 | S1 | yes |
| LMS-005 | S1 | LMS-003 | S1 | yes |
| LMS-005 | S1 | LMS-004 | S1 | yes |
| LMS-006 | S2 | LMS-003 | S1 | yes |
| LMS-007 | S2 | LMS-005 | S1 | yes |
| LMS-007 | S2 | LMS-006 | S2 | yes |
| LMS-008 | S1 | LMS-001 | S1 | yes |
| LMS-009 | S2 | LMS-001 | S1 | yes |
| LMS-010 | S2 | LMS-007 | S2 | yes |
| LMS-010 | S2 | LMS-009 | S2 | yes |
| LMS-011 | S3 | LMS-009 | S2 | yes |
| LMS-011 | S3 | LMS-010 | S2 | yes |
| LMS-012 | S3 | LMS-017 | S3 | yes |
| LMS-013 | S2 | LMS-007 | S2 | yes |
| LMS-013 | S2 | LMS-009 | S2 | yes |
| LMS-013 | S2 | LMS-010 | S2 | yes |
| LMS-014 | S3 | LMS-007 | S2 | yes |
| LMS-015 | S3 | LMS-009 | S2 | yes |
| LMS-015 | S3 | LMS-010 | S2 | yes |
| LMS-016 | S3 | LMS-010 | S2 | yes |
| LMS-016 | S3 | LMS-011 | S3 | yes |
| LMS-016 | S3 | LMS-008 | S1 | yes |
| LMS-017 | S3 | LMS-010 | S2 | yes |
| LMS-017 | S3 | LMS-008 | S1 | yes |
| LMS-018 | S3 | LMS-004 | S1 | yes |
| LMS-019 | S3 | LMS-015 | S3 | yes |
| LMS-020 | S3 | LMS-005 | S1 | yes |

OVERALL: PASS

## 6. Definition of Ready (DoR)

- Story has role, goal, benefit, and Given/When/Then acceptance criteria with `FR`/`UC`/`BR` references.
- Estimate (points, human hours) and dependencies are set; no dependency in a later sprint.
- UI stories have a Stitch design task scheduled before the template task.
- Test data needed exists in `data/seed/` or is created in the test.

## 7. Definition of Done (DoD)

- `./mvnw -q test` is green (on the VM: `tools/mvnw-vm.sh -q test`); Python tests are green (`python3 -m unittest discover -s tools/data/tests`).
- Every new source file has the mandatory header (generated JSON excepted).
- `docs/process/ai-usage-log.md` is updated with the exact model name; human review notes say "Pending human review" until a human confirms.
- Cross-model review is done.
- Acceptance criteria are demonstrated; UI matches the Stitch design.
- Branch merged into `develop` only after tests pass; the sprint folder `docs/04-sprints/sprint-N/` has review and retrospective notes.

## 8. Risk List

| ID | Risk | Impact | Mitigation / Trigger |
|---|---|---|---|
| RISK-H01 | Must gap of 2.0 h in Sprint 1 + 2 (53.0 h vs net 51.0 h) | Sprint 2 overload | Accepted; Sprint 3 Should stories absorb overrun; re-plan trigger in section 3 |
| RISK-H02 | Sprint 3 Should stories below the line are at risk (cumulative Should hours exceed Sprint 3 net capacity) | MVP lacks stretch features | Commitment line; stretch items are dropped first |
| RISK-H03 | **AI quota bottleneck:** the number of heavy AI chats per week is limited, and the plan needs the agent sessions shown in the backlog | Stories cannot be built in time | Plan agent sessions per week; commit and push after every step; keep `*_PROGRESS.md` checklists |
| RISK-H04 | **Estimates are assumptions** (0.40 ratio) | Over- or under-commitment | Re-calibrate with Sprint 1 actual hours; trigger rule in section 3 |
| RISK-H05 | Midterm weeks Nov 17 – Nov 28 reduce capacity | Sprint 1 slips | Capacity already reduced; Sprint 1 starts with the foundation stories |
| RISK-H06 | Only the VM-specific `tools/mvnw-vm.sh` makes Maven work behind the proxy | Build breaks on other machines | Standard `./mvnw` stays unchanged; the script is a documented workaround |
| RISK-H07 | HW01 known limitations (compensation tracking, reservation terminal states) | Rework in Sprint 3 | Design spike `LMS-008` in Sprint 1 |
| RISK-H08 | Both students must upload from their own ADUZEM accounts by the deadline | Missed submission | Reminder at packaging time |
