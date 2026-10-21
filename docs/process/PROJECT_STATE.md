<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Living tracker for current project phase, completed tasks, upcoming work, architectural decisions, and open questions.
-->
# Project State — CSE305 Library Management System

- **Last Updated:** 2026-10-21
- **Active Team Member:** Ibrahim Temur (231805033)
- **Current Phase:** Sprint 0 — Environment & Repository Bootstrap (Foundation)

---

## 1. Done
- **[2026-10-21 | Ibrahim Temur]** Inspected local Windows 11 Pro environment: verified Oracle JDK 25, Git 2.55.0, Python 3.11.9 + pip 26.2.1, and GitHub CLI 2.102.0 (`ibrahimtemur`).
- **[2026-10-21 | Ibrahim Temur]** Installed Apache Maven 3.9.16 (verified via SHA-512 checksum) under `%LOCALAPPDATA%\Programs\apache-maven-3.9.16`, configured User `PATH` and `JAVA_HOME`, and generated the project Maven Wrapper (`mvnw`, `mvnw.cmd`).
- **[2026-10-21 | Ibrahim Temur]** Audited GitHub CLI/MCP authentication and documented all 16 Stitch MCP tools without invoking Stitch design generation.
- **[2026-10-21 | Ibrahim Temur]** Created Spring Boot 3.5.16 skeleton (`edu.adu.lms`, Java 17 bytecode target) with Web, Thymeleaf, Data JPA, H2 (file mode for runtime, in-memory for tests), Validation, and JUnit 5 test starter; verified `mvn test` passes.
- **[2026-10-21 | Ibrahim Temur]** Created standard repository directory layout (`docs/00-course`, `docs/01-proposal`, `docs/02-inception`, `docs/03-design`, `docs/03-design/ui`, `docs/04-sprints`, `docs/process`, `data/seed`, `tools`, `src`).
- **[2026-10-21 | Ibrahim Temur]** Authored `AGENTS.md`, `README.md`, `.gitignore`, `.gitattributes`, `tools/set-author` (`ibrahim` / `omer`), and `tools/package` (`cse305_hwNN_231805033_231805026.zip`).
- **[2026-10-21 | Ibrahim Temur]** Initialized Git repository, set local author to Ibrahim Temur, created private GitHub repository `ibrahimtemur/cse305-library-management-system`, and pushed both `main` and `develop` branches.

---

## 2. Next
1. Provide Omer Faruk Kuş's GitHub username (to invite him as a repository collaborator) and confirm whether `231805026@stu.adu.edu.tr` is linked to his GitHub account.
2. **Phase 01 — Proposal & Inception (`docs/01-proposal`, `docs/02-inception`):** Define problem statement, user personas (Librarian, Member, Administrator), functional/non-functional requirements, and initial Scrum Product Backlog.
3. **Phase 02 — Architecture & Stitch UI Design (`docs/03-design`, `docs/03-design/ui`):** Define domain model, GoF/GRASP pattern catalog, and Stitch UI screens before implementing features.

---

## 3. Architectural & Process Decisions
| ID | Date | Decided By | Decision | Rationale |
|---|---|---|---|---|
| DEC-01 | 2026-10-21 | Ibrahim Temur | Use Spring Boot 3.5.16 with `--release 17` on JDK 25 | Satisfies Java 17+ baseline while running cleanly on installed JDK 25 LTS; includes Maven Wrapper 3.9.16 for reproducible builds across machines. |
| DEC-02 | 2026-10-21 | Ibrahim Temur | H2 file-mode (`./data/db/lms`) in runtime, in-memory H2 in tests | Persists application data locally during demos while keeping automated JUnit tests fast, isolated, and deterministic. |
| DEC-03 | 2026-10-21 | Ibrahim Temur | Git workflow: `main` (approved releases) ← `develop` ← `feature/*` | Protects `main` while enabling continuous pushes and review gates. |
| DEC-04 | 2026-10-21 | Ibrahim Temur | Enforce repository-local Git identity via `tools/set-author` | Prevents accidental commits under the wrong student on the shared computer without altering global OS Git settings. |

---

## 4. Open Questions & Follow-ups
- **[OPEN-01]** What is Omer Faruk Kuş's GitHub username so we can send the repository collaborator invitation?
- **[OPEN-02]** Has Omer Faruk Kuş added `231805026@stu.adu.edu.tr` to his GitHub account emails (or does he prefer another GitHub-linked email in `tools/set-author.ps1`)?
- **[OPEN-03]** The workspace currently resides inside a OneDrive-synced folder (`OneDrive\Masaüstü\LibraryManagementSystem`). If file-locking issues occur with `.git` or H2 database files, consider relocating the workspace outside OneDrive (e.g., `C:\dev\LibraryManagementSystem`).
