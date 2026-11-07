<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Potentially Shippable Increment per sprint and the MVP definition with explicit exclusions and the proposed Sprint 3 commitment line.
-->
# PSI and MVP Definition — Library Management System (LMS)

- **Version:** 1.0 (draft; Sprint 3 commitment line pending Product Owner approval) — 2026-11-07
- Hours and story lists are produced from [`PRODUCT_BACKLOG.md`](PRODUCT_BACKLOG.md) by `tools/agile/validate_backlog.py`; capacity and risks are in [`SPRINT_PLAN.md`](SPRINT_PLAN.md).

## 1. Potentially Shippable Increment (PSI) per Sprint

A PSI is a tested, integrated, runnable version of the application that the Product Owner could release: `./mvnw -q test` is green, acceptance criteria of the finished stories are demonstrated, and the Definition of Done is met. It does not have to contain enough features to be useful to the library.

| Sprint | Stories | PSI after the sprint (what the user can do) |
|---|---|---|
| Sprint 1 (HW03) | `LMS-001`, `LMS-002`, `LMS-003`, `LMS-004`, `LMS-005`, `LMS-008` | The application starts, loads seed v2 with shifted dates, lets librarians and members log in with role-based access, search the catalog, and lets a librarian maintain books and copies with enforced copy states. No lending yet. The reservation and compensation design decisions exist. |
| Sprint 2 (HW04) | `LMS-006`, `LMS-007`, `LMS-009`, `LMS-010`, `LMS-013` | A librarian registers members, checks books out and returns them with quota, cooldown, referenceOnly, and block rules; overdue fines are calculated (`0.25 TRY/day`, no cap); members see loans, history, cooldowns, and fines. This is a usable circulation desk without reservations. |
| Sprint 3 (HW05, MVP) | Commitment line stories, then stretch | Adds reservations with hold promotion and in-app notification, fine payment and waiver, and the dashboard. Stretch stories are added only if capacity remains. |

## 2. MVP Definition

**MVP = all Must stories + the Should stories above the Sprint 3 commitment line.** This order is a proposal until the Product Owner approves it.

**Must stories (11 stories, 53.0 h):**

- `LMS-001` Domain model and persistence skeleton (3.5 h)
- `LMS-002` Seed loader with date shifting (5.0 h)
- `LMS-003` Login/logout with BCrypt demo passwords and RBAC (5.0 h)
- `LMS-004` Catalog search and book detail (3.5 h)
- `LMS-005` Book CRUD, copy registration and copy lifecycle (7.5 h)
- `LMS-008` Design spike: compensation tracking and reservation terminal states (4.0 h)
- `LMS-006` Member registration, profile update and suspension (3.5 h)
- `LMS-007` Checkout with eligibility, cooldown and referenceOnly enforcement (9.0 h)
- `LMS-009` Overdue detection and uncapped fine calculation (3.5 h)
- `LMS-010` Return of a copy (copy to AVAILABLE only) (3.5 h)
- `LMS-013` Member self-service portal and librarian member inspection (5.0 h)

**Should stories above the line (3 stories, 17.0 h):**

- `LMS-017` Reservation, FIFO queue, hold promotion and in-app notification (8.5 h)
- `LMS-011` Fine payment and waiver (3.5 h)
- `LMS-015` Dashboard KPIs and overdue/unpaid report (5.0 h)

**Stretch, below the line and at risk (6 stories, 20.0 h):**

- `LMS-012` Reservation cancellation and hold expiry (3.5 h)
- `LMS-014` Loan renewal with reserved guard (3.5 h)
- `LMS-016` Lost-copy process with runtime appraised value (5.5 h)
- `LMS-018` Public guest catalog portal (2.0 h)
- `LMS-019` CSV export of overdue and inventory reports (2.0 h)
- `LMS-020` Open Library ISBN lookup helper (3.5 h)

MVP total committed: 70.0 h of human effort (Must + Should above the line).

## 3. Explicit MVP Exclusions

| Excluded | Reason |
|---|---|
| Periodicals / serials | The system manages printed books only (`CON-002`, `BR-014`) |
| Non-printed or unpublished theses | Not lendable and out of material scope (`CON-002`) |
| ADU library card, OBIS/OBS, LDAP/SSO integration | No live institutional integration (`CON-003`); the personal ID card rule is enforced operationally by entering `memberId` (`BR-016`) |
| External SMS or e-mail notifications | Hold notifications are in-app only (`CON-004`) |
| Payment gateways | Fines are settled at the desk as `PAID` or `WAIVED` (`CON-004`) |

## 4. Assumptions and Risks

Estimates are assumptions and will be re-calibrated with the actual Sprint 1 hours; stories below the commitment line are at risk (RISK-H02, RISK-H04 in [`SPRINT_PLAN.md`](SPRINT_PLAN.md)).
