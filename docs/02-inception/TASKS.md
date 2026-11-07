<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Technical tasks per user story (LMS-001..LMS-021), including Stitch design and TDD test tasks, whose planned human hours sum exactly to each story estimate.
-->
# Tasks — Library Management System (LMS)

- **Version:** 1.0 — 2026-11-07
- Task hours are human hours (steering agents, review, manual testing, documents), the same unit as the stories in [`PRODUCT_BACKLOG.md`](PRODUCT_BACKLOG.md). Planned hours per story must equal the story estimate; `tools/agile/validate_backlog.py` checks this (`LMS-015` `2.0 h` + `LMS-021` `3.0 h` = `5.0 h` combined).
- **"Actual human h" is empty on purpose** and is filled during the sprints; Sprint 1 actuals are used to re-calibrate all estimates.
- UI stories start with the Stitch design task; test tasks come before implementation tasks (TDD).

<!-- TASKS-TABLE:START -->
| Task | Story | Task description | Type | Planned human h | Actual human h |
|---|---|---|---|---|---|
| T-001-1 | LMS-001 | Write persistence and invariant tests first | TDD tests | 1.0 | |
| T-001-2 | LMS-001 | Steer agent: entities, enums, repositories | Implementation (steer agent) | 1.0 | |
| T-001-3 | LMS-001 | Review mapping against the HW01 domain model | Review | 1.0 | |
| T-001-4 | LMS-001 | Run tests, fix findings, update AI log | Docs and AI log | 0.5 | |
| T-002-1 | LMS-002 | Write loader count and date-shift tests first | TDD tests | 1.5 | |
| T-002-2 | LMS-002 | Steer agent: seed loader | Implementation (steer agent) | 1.0 | |
| T-002-3 | LMS-002 | Review date shifting (OPEN-04) and idempotency | Review | 1.0 | |
| T-002-4 | LMS-002 | Check loaded counts against the seed JSON | Manual test | 0.5 | |
| T-002-5 | LMS-002 | Document startup behaviour, update AI log | Docs and AI log | 1.0 | |
| T-003-1 | LMS-003 | Stitch login screen | Stitch design | 0.5 | |
| T-003-2 | LMS-003 | Write security tests first | TDD tests | 1.0 | |
| T-003-3 | LMS-003 | Steer agent: login, BCrypt demo passwords (OPEN-05), RBAC | Implementation (steer agent) | 1.5 | |
| T-003-4 | LMS-003 | Review security configuration (no secrets) | Review | 1.0 | |
| T-003-5 | LMS-003 | Manual test of each role | Manual test | 0.5 | |
| T-003-6 | LMS-003 | Document demo accounts handling, update AI log | Docs and AI log | 0.5 | |
| T-004-1 | LMS-004 | Stitch search and detail screens | Stitch design | 0.5 | |
| T-004-2 | LMS-004 | Write search tests first | TDD tests | 1.0 | |
| T-004-3 | LMS-004 | Steer agent: search and detail | Implementation (steer agent) | 1.0 | |
| T-004-4 | LMS-004 | Manual search checks | Manual test | 0.5 | |
| T-004-5 | LMS-004 | Update AI log | Docs and AI log | 0.5 | |
| T-005-1 | LMS-005 | Stitch book form and copy table | Stitch design | 1.0 | |
| T-005-2 | LMS-005 | Write CRUD and state machine tests first | TDD tests | 1.5 | |
| T-005-3 | LMS-005 | Steer agent: CRUD, copies, State pattern | Implementation (steer agent) | 2.0 | |
| T-005-4 | LMS-005 | Review state transitions | Review | 1.5 | |
| T-005-5 | LMS-005 | Manual test | Manual test | 1.0 | |
| T-005-6 | LMS-005 | Update AI log | Docs and AI log | 0.5 | |
| T-006-1 | LMS-006 | Stitch member form | Stitch design | 0.5 | |
| T-006-2 | LMS-006 | Write member tests first | TDD tests | 1.0 | |
| T-006-3 | LMS-006 | Steer agent: member CRUD and suspension | Implementation (steer agent) | 1.0 | |
| T-006-4 | LMS-006 | Manual test | Manual test | 0.5 | |
| T-006-5 | LMS-006 | Update AI log | Docs and AI log | 0.5 | |
| T-007-1 | LMS-007 | Stitch checkout desk screen | Stitch design | 1.0 | |
| T-007-2 | LMS-007 | Write quota, cooldown, referenceOnly boundary tests first | TDD tests | 2.5 | |
| T-007-3 | LMS-007 | Steer agent: checkout service and controller | Implementation (steer agent) | 2.5 | |
| T-007-4 | LMS-007 | Review rule enforcement | Review | 1.5 | |
| T-007-5 | LMS-007 | Manual desk test | Manual test | 1.0 | |
| T-007-6 | LMS-007 | Update AI log | Docs and AI log | 0.5 | |
| T-008-1 | LMS-008 | Analyse HW01 limitations | Review | 1.5 | |
| T-008-2 | LMS-008 | Write decision record (new DEC) | Docs and AI log | 1.0 | |
| T-008-3 | LMS-008 | Draw reservation state diagram | Docs and AI log | 1.0 | |
| T-008-4 | LMS-008 | Review effect on LMS-016 and LMS-017 | Review | 0.5 | |
| T-009-1 | LMS-009 | Write fine boundary tests first (0, 1, 2000 days) | TDD tests | 1.5 | |
| T-009-2 | LMS-009 | Steer agent: FineCalculator | Implementation (steer agent) | 0.5 | |
| T-009-3 | LMS-009 | Review arithmetic and end-date rules | Review | 1.0 | |
| T-009-4 | LMS-009 | Update AI log | Docs and AI log | 0.5 | |
| T-010-1 | LMS-010 | Stitch return screen | Stitch design | 0.5 | |
| T-010-2 | LMS-010 | Write return tests first | TDD tests | 1.0 | |
| T-010-3 | LMS-010 | Steer agent: return service | Implementation (steer agent) | 1.0 | |
| T-010-4 | LMS-010 | Manual test | Manual test | 0.5 | |
| T-010-5 | LMS-010 | Update AI log | Docs and AI log | 0.5 | |
| T-011-1 | LMS-011 | Stitch fine settlement screen | Stitch design | 0.5 | |
| T-011-2 | LMS-011 | Write settlement tests first | TDD tests | 1.0 | |
| T-011-3 | LMS-011 | Steer agent: pay and waive | Implementation (steer agent) | 1.0 | |
| T-011-4 | LMS-011 | Manual test | Manual test | 0.5 | |
| T-011-5 | LMS-011 | Update AI log | Docs and AI log | 0.5 | |
| T-012-1 | LMS-012 | Stitch cancel action | Stitch design | 0.5 | |
| T-012-2 | LMS-012 | Write cancel and expiry tests first | TDD tests | 1.0 | |
| T-012-3 | LMS-012 | Steer agent: cancellation and expiry job | Implementation (steer agent) | 1.0 | |
| T-012-4 | LMS-012 | Manual test | Manual test | 0.5 | |
| T-012-5 | LMS-012 | Update AI log | Docs and AI log | 0.5 | |
| T-013-1 | LMS-013 | Stitch self-service screen | Stitch design | 0.5 | |
| T-013-2 | LMS-013 | Write self-service tests first | TDD tests | 1.0 | |
| T-013-3 | LMS-013 | Steer agent: portal and librarian view | Implementation (steer agent) | 1.5 | |
| T-013-4 | LMS-013 | Review privacy (member A cannot see member B) | Review | 1.0 | |
| T-013-5 | LMS-013 | Manual test | Manual test | 0.5 | |
| T-013-6 | LMS-013 | Update AI log | Docs and AI log | 0.5 | |
| T-014-1 | LMS-014 | Stitch renew action | Stitch design | 0.5 | |
| T-014-2 | LMS-014 | Write renewal and guard tests first | TDD tests | 1.0 | |
| T-014-3 | LMS-014 | Steer agent: renewal and reserved-guard query | Implementation (steer agent) | 1.0 | |
| T-014-4 | LMS-014 | Manual test | Manual test | 0.5 | |
| T-014-5 | LMS-014 | Update AI log | Docs and AI log | 0.5 | |
| T-015-1 | LMS-015 | Stitch dashboard KPI summary cards | Stitch design | 0.5 | |
| T-015-2 | LMS-015 | Write KPI query tests first | TDD tests | 0.5 | |
| T-015-3 | LMS-015 | Steer agent: dashboard KPI summary service and view | Implementation (steer agent) | 0.5 | |
| T-015-4 | LMS-015 | Verify KPI values against direct database counts and update AI log | Review | 0.5 | |
| T-016-1 | LMS-016 | Stitch lost-copy dialog | Stitch design | 0.5 | |
| T-016-2 | LMS-016 | Write lost-copy tests first | TDD tests | 1.5 | |
| T-016-3 | LMS-016 | Steer agent: petition, window, assessment | Implementation (steer agent) | 1.5 | |
| T-016-4 | LMS-016 | Review compensation arithmetic and states | Review | 1.0 | |
| T-016-5 | LMS-016 | Manual test | Manual test | 0.5 | |
| T-016-6 | LMS-016 | Update AI log | Docs and AI log | 0.5 | |
| T-017-1 | LMS-017 | Stitch reserve, my-reservations, notification panel | Stitch design | 1.0 | |
| T-017-2 | LMS-017 | Write FIFO, promotion and window tests first | TDD tests | 2.0 | |
| T-017-3 | LMS-017 | Steer agent: reservation service, promotion, notification | Implementation (steer agent) | 2.5 | |
| T-017-4 | LMS-017 | Review state flow against LMS-008 | Review | 1.5 | |
| T-017-5 | LMS-017 | Manual test | Manual test | 1.0 | |
| T-017-6 | LMS-017 | Update AI log | Docs and AI log | 0.5 | |
| T-018-1 | LMS-018 | Stitch guest page (reuse LMS-004 design) | Stitch design | 0.5 | |
| T-018-2 | LMS-018 | Write guest access tests first | TDD tests | 0.5 | |
| T-018-3 | LMS-018 | Steer agent: guest portal | Implementation (steer agent) | 0.5 | |
| T-018-4 | LMS-018 | Manual test | Manual test | 0.5 | |
| T-019-1 | LMS-019 | Write CSV tests first | TDD tests | 0.5 | |
| T-019-2 | LMS-019 | Steer agent: CSV export | Implementation (steer agent) | 0.5 | |
| T-019-3 | LMS-019 | Manual test (Turkish characters) | Manual test | 0.5 | |
| T-019-4 | LMS-019 | Update AI log | Docs and AI log | 0.5 | |
| T-020-1 | LMS-020 | Stitch fetch button states | Stitch design | 0.5 | |
| T-020-2 | LMS-020 | Write lookup tests with stubbed service first | TDD tests | 1.0 | |
| T-020-3 | LMS-020 | Steer agent: lookup helper | Implementation (steer agent) | 1.0 | |
| T-020-4 | LMS-020 | Manual test | Manual test | 0.5 | |
| T-020-5 | LMS-020 | Update AI log | Docs and AI log | 0.5 | |
| T-021-1 | LMS-021 | Stitch overdue and unpaid fines report table | Stitch design | 0.5 | |
| T-021-2 | LMS-021 | Write overdue/unpaid report ordering and filtering tests first | TDD tests | 0.5 | |
| T-021-3 | LMS-021 | Steer agent: overdue/unpaid report query and controller | Implementation (steer agent) | 1.0 | |
| T-021-4 | LMS-021 | Review report consistency against KPI cards | Review | 0.5 | |
| T-021-5 | LMS-021 | Manual test and update AI log | Manual test | 0.5 | |
<!-- TASKS-TABLE:END -->
