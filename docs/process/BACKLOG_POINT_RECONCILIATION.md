<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Script-generated story-by-story reconciliation between initial git commit 28c40d9 and calibrated commit df7eaa4 / HEAD.
-->
# Backlog Story Point & Classic Effort Reconciliation (`28c40d9` → `df7eaa4` / `HEAD`)

> [!NOTE]
> **Generated automatically by `python3 tools/agile/make_reconciliation.py` — zero manual typing.**
> This document parses `git show 28c40d9:docs/02-inception/PRODUCT_BACKLOG.md` and the current `docs/02-inception/PRODUCT_BACKLOG.md` (and cross-checks `docs/02-inception/HW02_Inception_Agile.md` §2.2 & §2.3) to provide an exact, verifiable comparison of story IDs, titles, Fibonacci points, classic effort hours, and human hours.

---

## 1. Provenance & Git History Facts

1. **External Prompt Baseline vs. First Git Commit:**
   - A preliminary 23-story outline (`88` story points, `98` classic Must hours) existed only in the external task prompt (`ROADMAP_AND_PROMPTS.md`) and was **never committed to Git**.
   - The first Git commits of the Agile backlog on branch `docs/hw02-agile` were `6b4265c` (`USER_STORIES.md`) and `583e1a2` / `28c40d9` (`PRODUCT_BACKLOG.md`), which consolidated the backlog into **`20` stories (`LMS-001`..`LMS-020`)** totaling **`132` story points**, **`211.0` classic hours**, and **`90.0` human hours** (`46` agent sessions).
2. **Re-Calibration & Story Split in Commit `df7eaa4` (`HEAD` / PDF):**
   - In commit `df7eaa4`, story points and classic hours were re-calibrated across the backlog to **`88` story points** and **`173.0` classic hours** (with Must stories totaling **`48` points** and **`98.0` classic hours**: Sprint 1 = `52.0 h`, Sprint 2 = `46.0 h`), while human-hour estimates remained **`90.0` human hours** (`46` agent sessions).
   - By Product Owner decision, `LMS-015` (*Dashboard KPIs and overdue/unpaid report*) was split into **`LMS-015`** (*Operational dashboard KPI summary cards (015a)*, `2 pts`, `4` classic h, `2.0` human h — Sprint 3 Commit) and **`LMS-021`** (*Actionable overdue loans and unpaid fines report (015b)*, `3 pts`, `6` classic h, `3.0` human h — Sprint 3 Stretch), bringing the backlog to **`21` stories (`LMS-001`..`LMS-021`)**.

---

## 2. Raw Markdown Table Lines Read from Git (`28c40d9` vs `HEAD`)

### 2.1 `git show 28c40d9:docs/02-inception/PRODUCT_BACKLOG.md` (Raw Table Lines)
```text
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
```

### 2.2 Current `docs/02-inception/PRODUCT_BACKLOG.md` (`HEAD`, Raw Table Lines)
```text
| ID | Epic | Story | MoSCoW | Pts | Classic h | Human h | Agent sessions | Sprint | Depends on | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LMS-001 | E1 | Domain model and persistence skeleton | Must | 3 | 6 | 3.5 | 2 | S1 | — |  | Planned (S1) |
| LMS-002 | E1 | Seed loader with date shifting | Must | 5 | 10 | 5 | 3 | S1 | LMS-001 |  | Planned (S1) |
| LMS-003 | E2 | Login/logout with BCrypt demo passwords and RBAC | Must | 5 | 10 | 5 | 3 | S1 | LMS-001, LMS-002 |  | Planned (S1) |
| LMS-004 | E3 | Catalog search and book detail | Must | 3 | 6 | 3.5 | 2 | S1 | LMS-002, LMS-003 |  | Planned (S1) |
| LMS-005 | E3 | Book CRUD, copy registration and copy lifecycle | Must | 8 | 16 | 7.5 | 3 | S1 | LMS-003, LMS-004 |  | Planned (S1) |
| LMS-008 | E8 | Design spike: compensation tracking and reservation terminal states | Must | 2 | 4 | 4 | 1 | S1 | LMS-001 |  | Planned (S1) |
| LMS-006 | E4 | Member registration, profile update and suspension | Must | 3 | 6 | 3.5 | 2 | S2 | LMS-003 |  | Planned (S2) |
| LMS-007 | E5 | Checkout with eligibility, cooldown and referenceOnly enforcement | Must | 8 | 18 | 9 | 4 | S2 | LMS-005, LMS-006 |  | Planned (S2) |
| LMS-009 | E7 | Overdue detection and uncapped fine calculation | Must | 3 | 6 | 3.5 | 2 | S2 | LMS-001 |  | Planned (S2) |
| LMS-010 | E5 | Return of a copy (copy to AVAILABLE only) | Must | 3 | 6 | 3.5 | 2 | S2 | LMS-007, LMS-009 |  | Planned (S2) |
| LMS-013 | E2 | Member self-service portal and librarian member inspection | Must | 5 | 10 | 5 | 3 | S2 | LMS-007, LMS-009, LMS-010 |  | Planned (S2) |
| LMS-017 | E6 | Reservation, FIFO queue, hold promotion and in-app notification | Should | 8 | 16 | 8.5 | 4 | S3 | LMS-010, LMS-008 |  | Planned (S3: commit) |
| LMS-011 | E7 | Fine payment and waiver | Should | 3 | 7 | 3.5 | 2 | S3 | LMS-009, LMS-010 |  | Planned (S3: commit) |
| LMS-012 | E6 | Reservation cancellation and hold expiry | Should | 3 | 7 | 3.5 | 2 | S3 | LMS-017 |  | Planned (S3: commit) |
| LMS-015 | E9 | Operational dashboard KPI summary cards (015a) | Should | 2 | 4 | 2 | 1 | S3 | LMS-009, LMS-010 |  | Planned (S3: commit) |
| LMS-014 | E5 | Loan renewal with reserved guard | Should | 5 | 8 | 3.5 | 2 | S3 | LMS-007 |  | Planned (S3: stretch) |
| LMS-016 | E8 | Lost-copy process with runtime appraised value | Should | 8 | 12 | 5.5 | 3 | S3 | LMS-010, LMS-011, LMS-008 |  | Planned (S3: stretch) |
| LMS-021 | E9 | Actionable overdue loans and unpaid fines report (015b) | Should | 3 | 6 | 3 | 1 | S3 | LMS-009, LMS-010, LMS-015 |  | Planned (S3: stretch) |
| LMS-018 | E3 | Public guest catalog portal | Could | 2 | 4 | 2 | 1 | S3 | LMS-004 |  | Planned (S3: stretch) |
| LMS-019 | E9 | CSV export of overdue and inventory reports | Could | 3 | 5 | 2 | 1 | S3 | LMS-021 |  | Planned (S3: stretch) |
| LMS-020 | E3 | Open Library ISBN lookup helper | Could | 3 | 6 | 3.5 | 2 | S3 | LMS-005 |  | Planned (S3: stretch) |
```

---

## 3. Story-by-Story Reconciliation Table (`28c40d9` vs `HEAD` / `HW02_Inception_Agile.pdf`)

| Old ID (`28c40d9`) | Old Story Title (`28c40d9`) | Old MoSCoW | Old Sprint | Old Pts | Old Classic h | Old Human h | New ID (`HEAD` / PDF) | New Story Title (`HEAD` / PDF) | New MoSCoW | New Sprint | New Pts | New Classic h | New Human h | Δ Pts | Δ Classic h | Δ Human h | Reconciliation Note |
|---|---|---|---|---:|---:|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `LMS-001` | Domain model and persistence skeleton | Must | S1 | 5 | 8 | 3.5 | `LMS-001` | Domain model and persistence skeleton | Must | S1 | 3 | 6 | 3.5 | -2 | -2 | 0 | Re-calibrated in `df7eaa4` (`5 -> 3 pts`, `8 -> 6 classic h`); human hours unchanged (`3.5 h`). |
| `LMS-002` | Seed loader with date shifting | Must | S1 | 8 | 13 | 5.0 | `LMS-002` | Seed loader with date shifting | Must | S1 | 5 | 10 | 5.0 | -3 | -3 | 0 | Re-calibrated in `df7eaa4` (`8 -> 5 pts`, `13 -> 10 classic h`); human hours unchanged (`5.0 h`). |
| `LMS-003` | Login/logout with BCrypt demo passwords and RBAC | Must | S1 | 8 | 13 | 5.0 | `LMS-003` | Login/logout with BCrypt demo passwords and RBAC | Must | S1 | 5 | 10 | 5.0 | -3 | -3 | 0 | Re-calibrated in `df7eaa4` (`8 -> 5 pts`, `13 -> 10 classic h`); human hours unchanged (`5.0 h`). |
| `LMS-004` | Catalog search and book detail | Must | S1 | 5 | 8 | 3.5 | `LMS-004` | Catalog search and book detail | Must | S1 | 3 | 6 | 3.5 | -2 | -2 | 0 | Re-calibrated in `df7eaa4` (`5 -> 3 pts`, `8 -> 6 classic h`); human hours unchanged (`3.5 h`). |
| `LMS-005` | Book CRUD, copy registration and copy lifecycle | Must | S1 | 13 | 18 | 7.5 | `LMS-005` | Book CRUD, copy registration and copy lifecycle | Must | S1 | 8 | 16 | 7.5 | -5 | -2 | 0 | Re-calibrated in `df7eaa4` (`13 -> 8 pts`, `18 -> 16 classic h`); human hours unchanged (`7.5 h`). |
| `LMS-008` | Design spike: compensation tracking and reservation terminal states | Must | S1 | 2 | 4 | 4.0 | `LMS-008` | Design spike: compensation tracking and reservation terminal states | Must | S1 | 2 | 4 | 4.0 | 0 | 0 | 0 | Unchanged between `28c40d9` and `df7eaa4` / `HEAD`. |
| `LMS-006` | Member registration, profile update and suspension | Must | S2 | 5 | 8 | 3.5 | `LMS-006` | Member registration, profile update and suspension | Must | S2 | 3 | 6 | 3.5 | -2 | -2 | 0 | Re-calibrated in `df7eaa4` (`5 -> 3 pts`, `8 -> 6 classic h`); human hours unchanged (`3.5 h`). |
| `LMS-007` | Checkout with eligibility, cooldown and referenceOnly enforcement | Must | S2 | 13 | 22 | 9.0 | `LMS-007` | Checkout with eligibility, cooldown and referenceOnly enforcement | Must | S2 | 8 | 18 | 9.0 | -5 | -4 | 0 | Re-calibrated in `df7eaa4` (`13 -> 8 pts`, `22 -> 18 classic h`); human hours unchanged (`9.0 h`). |
| `LMS-009` | Overdue detection and uncapped fine calculation | Must | S2 | 5 | 8 | 3.5 | `LMS-009` | Overdue detection and uncapped fine calculation | Must | S2 | 3 | 6 | 3.5 | -2 | -2 | 0 | Re-calibrated in `df7eaa4` (`5 -> 3 pts`, `8 -> 6 classic h`); human hours unchanged (`3.5 h`). |
| `LMS-010` | Return of a copy (copy to AVAILABLE only) | Must | S2 | 5 | 8 | 3.5 | `LMS-010` | Return of a copy (copy to AVAILABLE only) | Must | S2 | 3 | 6 | 3.5 | -2 | -2 | 0 | Re-calibrated in `df7eaa4` (`5 -> 3 pts`, `8 -> 6 classic h`); human hours unchanged (`3.5 h`). |
| `LMS-013` | Member self-service portal and librarian member inspection | Must | S2 | 8 | 13 | 5.0 | `LMS-013` | Member self-service portal and librarian member inspection | Must | S2 | 5 | 10 | 5.0 | -3 | -3 | 0 | Re-calibrated in `df7eaa4` (`8 -> 5 pts`, `13 -> 10 classic h`); human hours unchanged (`5.0 h`). |
| `LMS-017` | Reservation, FIFO queue, hold promotion and in-app notification | Should | S3 | 13 | 21 | 8.5 | `LMS-017` | Reservation, FIFO queue, hold promotion and in-app notification | Should | S3 | 8 | 16 | 8.5 | -5 | -5 | 0 | Re-calibrated in `df7eaa4` (`13 -> 8 pts`, `21 -> 16 classic h`); human hours unchanged (`8.5 h`). |
| `LMS-011` | Fine payment and waiver | Should | S3 | 5 | 8 | 3.5 | `LMS-011` | Fine payment and waiver | Should | S3 | 3 | 7 | 3.5 | -2 | -1 | 0 | Re-calibrated in `df7eaa4` (`5 -> 3 pts`, `8 -> 7 classic h`); human hours unchanged (`3.5 h`). |
| `LMS-012` | Reservation cancellation and hold expiry | Should | S3 | 5 | 8 | 3.5 | `LMS-012` | Reservation cancellation and hold expiry | Should | S3 | 3 | 7 | 3.5 | -2 | -1 | 0 | Re-calibrated in `df7eaa4` (`5 -> 3 pts`, `8 -> 7 classic h`); human hours unchanged (`3.5 h`). |
| `LMS-015` | Dashboard KPIs and overdue/unpaid report | Should | S3 | 8 | 12 | 5.0 | `LMS-015` | Operational dashboard KPI summary cards (015a) | Should | S3 | 2 | 4 | 2.0 | -6 | -8 | -3.0 | Split part 1 (`015a`, committed): original `LMS-015` (`8 pts / 12 h / 5.0 h`) was re-calibrated to `5 pts / 10 h / 5.0 h` and split into `LMS-015` (`2 pts / 4 h / 2.0 h`) + `LMS-021` (`3 pts / 6 h / 3.0 h`). |
| `LMS-014` | Loan renewal with reserved guard | Should | S3 | 5 | 8 | 3.5 | `LMS-014` | Loan renewal with reserved guard | Should | S3 | 5 | 8 | 3.5 | 0 | 0 | 0 | Unchanged between `28c40d9` and `df7eaa4` / `HEAD`. |
| `LMS-016` | Lost-copy process with runtime appraised value | Should | S3 | 8 | 13 | 5.5 | `LMS-016` | Lost-copy process with runtime appraised value | Should | S3 | 8 | 12 | 5.5 | 0 | -1 | 0 | Points (`8 pts`) and human hours (`5.5 h`) unchanged; classic effort re-calibrated (`13 -> 12 h`). |
| *(from `LMS-015`)* | *(Included in `LMS-015` in `28c40d9`)* | — | — | — | — | — | `LMS-021` | Actionable overdue loans and unpaid fines report (015b) | Should | S3 | 3 | 6 | 3.0 | +3 | +6 | +3.0 | Split part 2 (`015b`, stretch): newly assigned story ID for the report table slice of `LMS-015` (combined `LMS-015 + LMS-021 = 5 pts / 10 h / 5.0 h`, net `-3 pts / -2 h / 0.0 h` vs `28c40d9` `LMS-015`). |
| `LMS-018` | Public guest catalog portal | Could | S3 | 3 | 5 | 2.0 | `LMS-018` | Public guest catalog portal | Could | S3 | 2 | 4 | 2.0 | -1 | -1 | 0 | Re-calibrated in `df7eaa4` (`3 -> 2 pts`, `5 -> 4 classic h`); human hours unchanged (`2.0 h`). |
| `LMS-019` | CSV export of overdue and inventory reports | Could | S3 | 3 | 5 | 2.0 | `LMS-019` | CSV export of overdue and inventory reports | Could | S3 | 3 | 5 | 2.0 | 0 | 0 | 0 | Unchanged between `28c40d9` and `df7eaa4` / `HEAD`. |
| `LMS-020` | Open Library ISBN lookup helper | Could | S3 | 5 | 8 | 3.5 | `LMS-020` | Open Library ISBN lookup helper | Could | S3 | 3 | 6 | 3.5 | -2 | -2 | 0 | Re-calibrated in `df7eaa4` (`5 -> 3 pts`, `8 -> 6 classic h`); human hours unchanged (`3.5 h`). |
| **TOTAL (`20` stories)** | **`LMS-001`..`LMS-020` in `28c40d9`** | **11M / 6S / 3C** | **S1–S3** | **132** | **211.0** | **90.0** | **TOTAL (`21` stories)** | **`LMS-001`..`LMS-021` in `HEAD` / PDF** | **11M / 7S / 3C** | **S1–S3** | **88** | **173.0** | **90.0** | **-44** | **-38** | **0** | **Programmatically verified sums (`make_reconciliation.py`).** |

---

## 4. Category & Sprint Summary Comparison

| Category / Sprint | `28c40d9` Stories | `28c40d9` Pts | `28c40d9` Classic h | `28c40d9` Human h | `HEAD` / PDF Stories | `HEAD` / PDF Pts | `HEAD` / PDF Classic h | `HEAD` / PDF Human h | Δ Pts | Δ Classic h | Δ Human h |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Must Have** | 11 | 77 | 123.0 | 53.0 | 11 | 48 | 98.0 | 53.0 | -29 | -25 | 0 |
| **Should Have** | 6 | 44 | 70.0 | 29.5 | 7 | 32 | 60.0 | 29.5 | -12 | -10 | 0 |
| **Could Have** | 3 | 11 | 18.0 | 7.5 | 3 | 8 | 15.0 | 7.5 | -3 | -3 | 0 |
| **Sprint 1 (`S1`)** | 6 | 41 | 64.0 | 28.5 | 6 | 26 | 52.0 | 28.5 | -15 | -12 | 0 |
| **Sprint 2 (`S2`)** | 5 | 36 | 59.0 | 24.5 | 5 | 22 | 46.0 | 24.5 | -14 | -13 | 0 |
| **Sprint 3 (`S3`)** | 9 | 55 | 88.0 | 37.0 | 10 | 40 | 75.0 | 37.0 | -15 | -13 | 0 |
| **Total Backlog** | **20** | **132** | **211.0** | **90.0** | **21** | **88** | **173.0** | **90.0** | **-44** | **-38** | **0** |
