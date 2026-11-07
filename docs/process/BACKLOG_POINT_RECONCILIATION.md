<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Git-verified story-by-story reconciliation note comparing the initial 20-story backlog draft in commits 6b4265c/28c40d9 (132 pts, 211.0 classic h) against the calibrated 21-story backlog in commit df7eaa4 (88 pts, 173.0 classic h, 90.0 human h).
-->
# Product Backlog Point & Effort Reconciliation Note (`6b4265c` / `28c40d9` -> `df7eaa4`)

- **Date:** 2026-11-07
- **Source Commits in Git History:**
  - **Initial 20-Story Backlog Commits (`Claude Sonnet 5.5 Medium`):** `6b4265c` (*"docs(inception): draft product backlog and add backlog validator"*), `583e1a2` (*"docs(inception): add user stories LMS-001..LMS-020 with acceptance criteria"*), and `28c40d9` (*"docs(inception): complete product backlog with totals, commitment line, and FR traceability; extend validator"*).
  - **Calibrated 21-Story Backlog Commit (`Gemini 4 Argon (High)`):** `df7eaa4` (*"docs(inception): apply PO-approved S3 commitment line, split LMS-015/LMS-021, and reconcile 88-point baseline"*).
- **Important Fact on the Earlier 23-Story Reference:** The 23-story (`88` story points, `98` Must classic hours) preliminary list originated in the external planning prompt (`ROADMAP_AND_PROMPTS.md`) at the start of the session and **was never committed to the Git repository**. The very first commit of [`docs/02-inception/PRODUCT_BACKLOG.md`](../02-inception/PRODUCT_BACKLOG.md) in Git (`6b4265c`) already contained `20` stories (`LMS-001`..`LMS-020`) where `Claude Sonnet 5.5 Medium` had inflated 16 stories by one Fibonacci step (raising total points to `132` and classic hours to `211.0`). Therefore, the authoritative Git reconciliation below compares `git show 28c40d9:docs/02-inception/PRODUCT_BACKLOG.md` (`20` stories, `132 pts`, `211.0` classic h, `90.0` human h) directly against [`docs/02-inception/PRODUCT_BACKLOG.md`](../02-inception/PRODUCT_BACKLOG.md) (`21` stories, `88 pts`, `173.0` classic h, `90.0` human h), matching [`HW02_Inception_Agile.pdf`](../02-inception/HW02_Inception_Agile.pdf) 100%.

---

## 1. Story-by-Story Comparison (`git show 28c40d9:docs/02-inception/PRODUCT_BACKLOG.md` vs `df7eaa4` / `HEAD`)

| Old ID (`28c40d9`) | Epic | MoSCoW | Sprint | Old Pts (`28c40d9`) | Old Classic h (`28c40d9`) | Old Human h (`28c40d9`) | New ID (`df7eaa4`) | New Story Title (`PRODUCT_BACKLOG.md` & PDF) | New Pts | New Classic h | New Human h | Agent Sess. | Reason for Change |
|---|---|---|---|---:|---:|---:|---|---|---:|---:|---:|---:|---|
| `LMS-001` | E1 | Must | S1 | 5 | 8 | 3.5 | `LMS-001` | Domain model and persistence skeleton | **3** | **6** | **3.5** | 2 | Reverted unapproved Fibonacci inflation (`5 -> 3 pts`, `8 -> 6` classic h); human hours (`3.5 h`) unchanged. |
| `LMS-002` | E1 | Must | S1 | 8 | 13 | 5.0 | `LMS-002` | Seed loader with date shifting | **5** | **10** | **5.0** | 3 | Reverted unapproved Fibonacci inflation (`8 -> 5 pts`, `13 -> 10` classic h); human hours (`5.0 h`) unchanged. |
| `LMS-003` | E2 | Must | S1 | 8 | 13 | 5.0 | `LMS-003` | Login/logout with BCrypt demo passwords and RBAC | **5** | **10** | **5.0** | 3 | Reverted unapproved Fibonacci inflation (`8 -> 5 pts`, `13 -> 10` classic h); human hours (`5.0 h`) unchanged. |
| `LMS-004` | E3 | Must | S1 | 5 | 8 | 3.5 | `LMS-004` | Catalog search and book detail | **3** | **6** | **3.5** | 2 | Reverted unapproved Fibonacci inflation (`5 -> 3 pts`, `8 -> 6` classic h); human hours (`3.5 h`) unchanged. |
| `LMS-005` | E3 | Must | S1 | 13 | 18 | 7.5 | `LMS-005` | Book CRUD, copy registration and copy lifecycle | **8** | **16** | **7.5** | 3 | Reverted unapproved Fibonacci inflation (`13 -> 8 pts`, `18 -> 16` classic h); PO-approved `7.5` human h safety value preserved. |
| `LMS-008` | E8 | Must | S1 | 2 | 4 | 4.0 | `LMS-008` | Design spike: compensation tracking and reservation terminal states | **2** | **4** | **4.0** | 1 | Unchanged (`2 pts`, `4` classic h, `4.0` human h timeboxed spike). |
| **Sprint 1 Must Subtotal** | — | **Must** | **S1** | **41** | **64** | **28.5** | **6 stories** | — | **26** | **52** | **28.5** | **14** | **S1 points calibrated `41 -> 26 pts`, classic `64 -> 52 h`, human `28.5 h` unchanged.** |
| `LMS-006` | E4 | Must | S2 | 5 | 8 | 3.5 | `LMS-006` | Member registration, profile update and suspension | **3** | **6** | **3.5** | 2 | Reverted unapproved Fibonacci inflation (`5 -> 3 pts`, `8 -> 6` classic h); human hours (`3.5 h`) unchanged. |
| `LMS-007` | E5 | Must | S2 | 13 | 22 | 9.0 | `LMS-007` | Checkout with eligibility, cooldown and referenceOnly enforcement | **8** | **18** | **9.0** | 4 | Reverted unapproved Fibonacci inflation (`13 -> 8 pts`, `22 -> 18` classic h); PO-approved `9.0` human h safety value preserved. |
| `LMS-009` | E7 | Must | S2 | 5 | 8 | 3.5 | `LMS-009` | Overdue detection and uncapped fine calculation | **3** | **6** | **3.5** | 2 | Reverted unapproved Fibonacci inflation (`5 -> 3 pts`, `8 -> 6` classic h); human hours (`3.5 h`) unchanged. |
| `LMS-010` | E5 | Must | S2 | 5 | 8 | 3.5 | `LMS-010` | Return of a copy (copy to AVAILABLE only) | **3** | **6** | **3.5** | 2 | Reverted unapproved Fibonacci inflation (`5 -> 3 pts`, `8 -> 6` classic h); human hours (`3.5 h`) unchanged. |
| `LMS-013` | E2 | Must | S2 | 8 | 13 | 5.0 | `LMS-013` | Member self-service portal and librarian member inspection | **5** | **10** | **5.0** | 3 | Reverted unapproved Fibonacci inflation (`8 -> 5 pts`, `13 -> 10` classic h); human hours (`5.0 h`) unchanged. |
| **Sprint 2 Must Subtotal** | — | **Must** | **S2** | **36** | **59** | **24.5** | **5 stories** | — | **22** | **46** | **24.5** | **13** | **S2 points calibrated `36 -> 22 pts`, classic `59 -> 46 h`, human `24.5 h` unchanged.** |
| **All Must Subtotal (S1+S2)** | — | **Must** | **S1+S2** | **77** | **123** | **53.0** | **11 stories** | — | **48** | **98** | **53.0** | **27** | **Matches baseline `48` Must pts, `98.0` Must classic h, `53.0` Must human h.** |
| `LMS-017` | E6 | Should | S3 | 13 | 21 | 8.5 | `LMS-017` | Reservation, FIFO queue, hold promotion and in-app notification | **8** | **16** | **8.5** | 4 | Reverted unapproved Fibonacci inflation (`13 -> 8 pts`, `21 -> 16` classic h); human hours (`8.5 h`, **Commit #1**) unchanged. |
| `LMS-011` | E7 | Should | S3 | 5 | 8 | 3.5 | `LMS-011` | Fine payment and waiver | **3** | **7** | **3.5** | 2 | Reverted unapproved Fibonacci inflation (`5 -> 3 pts`, `8 -> 7` classic h); human hours (`3.5 h`, **Commit #2**) unchanged. |
| `LMS-012` | E6 | Should | S3 | 5 | 8 | 3.5 | `LMS-012` | Reservation cancellation and hold expiry | **3** | **7** | **3.5** | 2 | Reverted unapproved Fibonacci inflation (`5 -> 3 pts`, `8 -> 7` classic h); promoted to **Commit #3** (`3.5 h`). |
| `LMS-015` *(before split)* | E9 | Should | S3 | 8 | 12 | 5.0 | `LMS-015` + `LMS-021` | `LMS-015`: Operational dashboard KPI summary cards (`015a`, **Commit #4**)<br>`LMS-021`: Actionable overdue loans and unpaid fines report (`015b`, *Stretch*) | **2 + 3 = 5** | **4 + 6 = 10** | **2.0 + 3.0 = 5.0** | **1 + 1 = 2** | Reverted inflation (`8 -> 5 pts`, `12 -> 10` classic h) and split per PO decision into `LMS-015` (`2 pts`, `4` classic h, `2.0` human h, **Commit #4**) + `LMS-021` (`3 pts`, `6` classic h, `3.0` human h, *Stretch*). |
| `LMS-014` | E5 | Should | S3 | 5 | 8 | 3.5 | `LMS-014` | Loan renewal with reserved guard | **5** | **8** | **3.5** | 2 | Unchanged (`5 pts`, `8` classic h, `3.5` human h, *Stretch*). |
| `LMS-016` | E8 | Should | S3 | 8 | 13 | 5.5 | `LMS-016` | Lost-copy process with runtime appraised value | **8** | **12** | **5.5** | 3 | Points (`8 pts`) and human hours (`5.5 h`, *Stretch*) unchanged; classic effort aligned `13 -> 12 h`. |
| **Should Subtotal (S3)** | — | **Should** | **S3** | **44** | **70** | **29.5** | **7 stories** | **`4` Committed (`16 pts / 34 classic h / 17.5 human h`) + `3` Stretch (`16 pts / 26 classic h / 12.0 human h`)** | **32** | **60** | **29.5** | **15** | **Should points calibrated `44 -> 32 pts`, classic `70 -> 60 h`, human `29.5 h` unchanged.** |
| `LMS-018` | E3 | Could | S3 | 3 | 5 | 2.0 | `LMS-018` | Public guest catalog portal | **2** | **4** | **2.0** | 1 | Reverted unapproved Fibonacci inflation (`3 -> 2 pts`, `5 -> 4` classic h); human hours (`2.0 h`, *Stretch*) unchanged. |
| `LMS-019` | E9 | Could | S3 | 3 | 5 | 2.0 | `LMS-019` | CSV export of overdue and inventory reports | **3** | **5** | **2.0** | 1 | Unchanged (`3 pts`, `5` classic h, `2.0` human h, *Stretch*; depends on `LMS-021`). |
| `LMS-020` | E3 | Could | S3 | 5 | 8 | 3.5 | `LMS-020` | Open Library ISBN lookup helper | **3** | **6** | **3.5** | 2 | Reverted unapproved Fibonacci inflation (`5 -> 3 pts`, `8 -> 6` classic h); human hours (`3.5 h`, *Stretch*) unchanged. |
| **Could Subtotal (S3)** | — | **Could** | **S3** | **11** | **18** | **7.5** | **3 stories** | — | **8** | **15** | **7.5** | **4** | **Could points calibrated `11 -> 8 pts`, classic `18 -> 15 h`, human `7.5 h` unchanged.** |
| **GRAND TOTAL** | **E1–E9** | **All** | **S1–S3** | **132** | **211** | **90.0** | **21 stories** | **`15` Committed MVP (`64 pts / 132 classic h / 70.5 human h`) + `6` Stretch (`24 pts / 41 classic h / 19.5 human h`)** | **88** | **173** | **90.0** | **46** | **Exact match across `PRODUCT_BACKLOG.md`, `USER_STORIES.md`, `SPRINT_PLAN.md`, `THEMES_EPICS.md`, `TASKS.md`, `PSI_AND_MVP.md`, and `HW02_Inception_Agile.pdf`.** |

---

## 2. Verification Command

```bash
git show 28c40d9:docs/02-inception/PRODUCT_BACKLOG.md
python3 tools/agile/validate_backlog.py
```
