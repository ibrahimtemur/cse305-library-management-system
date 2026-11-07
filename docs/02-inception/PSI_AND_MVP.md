<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Potentially Shippable Increment per sprint and the MVP definition with explicit exclusions and the Product Owner-approved Sprint 3 commitment line.
-->
# PSI and MVP Definition — Library Management System (LMS)

- **Version:** 1.0 (Product Owner approved 2026-11-07) — 2026-11-07
- Points, hours, and story lists are produced from [`PRODUCT_BACKLOG.md`](PRODUCT_BACKLOG.md) by `tools/agile/validate_backlog.py`; capacity and risks are in [`SPRINT_PLAN.md`](SPRINT_PLAN.md).

## 1. Potentially Shippable Increment (PSI) per Sprint

A PSI is a tested, integrated, runnable version of the application that meets the Definition of Done (`./mvnw -q test` green, Python seed tests green, mandatory headers present, acceptance criteria verified).

| Sprint | Stories | Points / Human h | PSI after the sprint (what the user can do) |
|---|---|---|---|
| Sprint 1 (HW03) | `LMS-001`, `LMS-002`, `LMS-003`, `LMS-004`, `LMS-005`, `LMS-008` | 26 pts / 28.5 h | The application starts, loads seed v2 with shifted dates (`OPEN-04`), lets librarians and members log in with BCrypt demo passwords (`OPEN-05`) and role-based access, search the catalog, and lets a librarian maintain books and copies with enforced copy states. The reservation and lost-copy compensation design decisions (`LMS-008`) are documented. |
| Sprint 2 (HW04) | `LMS-006`, `LMS-007`, `LMS-009`, `LMS-010`, `LMS-013` | 22 pts / 24.5 h | A librarian registers members, checks books out and returns them with quota (`7/3/3`), 30-day post-renewal cooldown, `referenceOnly`, and block rules; overdue fines are calculated (`0.25 TRY/day`, no cap); members view active loans, history, cooldowns, and fines. This is a complete circulation desk without reservations. |
| Sprint 3 (HW05, MVP) | Committed Should slice (`LMS-017`, `LMS-011`, `LMS-012`, `LMS-015`), then stretch | 16 pts / 17.5 h committed (+ 24 pts / 19.5 h stretch) | Adds title-level FIFO reservations with automatic hold promotion on return and in-app 3-day pickup notifications (`LMS-017`), desk fine payment and waiver (`LMS-011`), reservation cancellation and 3-day hold expiry reallocation (`LMS-012`), and operational dashboard KPI summary cards (`LMS-015`). Stretch stories (`LMS-014`, `LMS-016`, `LMS-021`, `LMS-018`..`LMS-020`) are added only if capacity remains. |

## 2. MVP Definition

Grounded in our project's MoSCoW prioritization ([`PROJECT_PROPOSAL.md`](../01-proposal/PROJECT_PROPOSAL.md)), functional requirements ([`REQUIREMENTS.md`](REQUIREMENTS.md)), and the Sprint 3 capacity analysis ([`SPRINT_PLAN.md`](SPRINT_PLAN.md)), **MVP = all Must stories (`53.0 h`, `48 pts`) + the Should stories above the Sprint 3 commitment line (`17.5 h`, `16 pts`) = `70.5 h` (`64 pts`) across 15 committed stories.**

**Must stories (11 stories, 48 pts, 53.0 h):**

- `LMS-001` Domain model and persistence skeleton (3 pts, 3.5 h)
- `LMS-002` Seed loader with date shifting (5 pts, 5.0 h)
- `LMS-003` Login/logout with BCrypt demo passwords and RBAC (5 pts, 5.0 h)
- `LMS-004` Catalog search and book detail (3 pts, 3.5 h)
- `LMS-005` Book CRUD, copy registration and copy lifecycle (8 pts, 7.5 h)
- `LMS-008` Design spike: compensation tracking and reservation terminal states (2 pts, 4.0 h)
- `LMS-006` Member registration, profile update and suspension (3 pts, 3.5 h)
- `LMS-007` Checkout with eligibility, cooldown and referenceOnly enforcement (8 pts, 9.0 h)
- `LMS-009` Overdue detection and uncapped fine calculation (3 pts, 3.5 h)
- `LMS-010` Return of a copy (copy to AVAILABLE only) (3 pts, 3.5 h)
- `LMS-013` Member self-service portal and librarian member inspection (5 pts, 5.0 h)

**Should stories above the commitment line (4 stories, 16 pts, 17.5 h):**

- `LMS-017` Reservation, FIFO queue, hold promotion and in-app notification (8 pts, 8.5 h)
- `LMS-011` Fine payment and waiver (3 pts, 3.5 h)
- `LMS-012` Reservation cancellation and hold expiry (3 pts, 3.5 h)
- `LMS-015` Operational dashboard KPI summary cards (015a) (2 pts, 2.0 h)

**Stretch, below the commitment line and at risk (6 stories, 24 pts, 19.5 h):**

- `LMS-014` Loan renewal with reserved guard (5 pts, 3.5 h)
- `LMS-016` Lost-copy process with runtime appraised value (8 pts, 5.5 h)
- `LMS-021` Actionable overdue loans and unpaid fines report (015b) (3 pts, 3.0 h)
- `LMS-018` Public guest catalog portal (2 pts, 2.0 h)
- `LMS-019` CSV export of overdue and inventory reports (3 pts, 2.0 h)
- `LMS-020` Open Library ISBN lookup helper (3 pts, 3.5 h)

MVP total committed: **64 pts / 70.5 h** of human effort (`Must` 53.0 h + `Should` above the line 17.5 h).

## 3. Explicit MVP Exclusions

| Excluded | Reason |
|---|---|
| Periodicals / serials | The system manages printed books only (`CON-002`, `BR-014`) |
| Non-printed or unpublished theses | Not lendable and out of material scope (`CON-002`) |
| ADU library card, OBIS/OBS, LDAP/SSO integration | No live institutional integration (`CON-003`); the personal ID card rule is enforced operationally by entering `memberId` (`BR-016`) |
| External SMS or e-mail notifications | Hold notifications are in-app only (`CON-004`) |
| Payment gateways | Fines are settled at the desk as `PAID` or `WAIVED` (`CON-004`) |

## 4. Assumptions and Risks

Estimates are assumptions and will be re-calibrated with the actual Sprint 1 hours; stories below the commitment line are at risk (`RISK-H02`, `RISK-H04` in [`SPRINT_PLAN.md`](SPRINT_PLAN.md)).
