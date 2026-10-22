<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Permanent agent operating rules, workflow standards, and academic policies for the CSE305 Library Management System.
-->
# AGENTS.md — Permanent Repository Rules

## Project Identity
- **Course:** CSE305 Software Engineering — Adnan Menderes University (ADU), Department of Computer Engineering
- **Course Instructor:** Assoc. Prof. Dr. Fatih Soygazi (`fatih.soygazi@adu.edu.tr`, Office: C 3-41)
- **Official Syllabus & Schedule Reference:** Always consult [`docs/00-course/COURSE_SYLLABUS_AND_SCHEDULE.md`](docs/00-course/COURSE_SYLLABUS_AND_SCHEDULE.md) for official lecture topics, required textbooks (Pressman 9th Ed., Larman 3rd Ed., Rubin *Essential Scrum*), grading breakdown (`5 Assignments = 40%`, `Final = 60%`), and ADUZEM submission policies.
- **Project:** Library Management System (standalone project, unrelated to any other repository)
- **Authors & Scrum Roles:**
  - **Ibrahim Temur** — Student No: `231805033` (**Product Owner (PO)** & Developer / Architect / QA / Reviewer)
  - **Omer Faruk Kuş** — Student No: `231805026` (**Scrum Master (SM)** & Developer / Architect / QA / Reviewer)

---

## 1. Language Rule (Strict Separation)
- **Chat communication with the user:** ALWAYS reply ONLY in **Turkish**.
- **Repository content:** Every file created or updated in the repository — source code, identifiers, comments, Javadoc, Markdown documentation, commit messages, branch names, UI strings, and test names — MUST be written in **English**.

---

## 2. Mandatory File Header Rule
Every first-party source file and every Markdown document in this repository MUST begin with the following header using the file's native comment syntax:

```text
Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
Student No(s)#: 231805033, 231805026
General Comments: <one-line purpose of this file>
```

### Header Syntax Examples
- **Java (`*.java`):**
  ```java
  /*
   * Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
   * Student No(s)#: 231805033, 231805026
   * General Comments: <one-line purpose of this file>
   */
  ```
- **XML / HTML / Thymeleaf / Markdown (`*.xml`, `*.html`, `*.md`):**
  ```xml
  <!--
    Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
    Student No(s)#: 231805033, 231805026
    General Comments: <one-line purpose of this file>
  -->
  ```
- **Properties / PowerShell / Git Config (`*.properties`, `*.ps1`, `.gitignore`, `.gitattributes`):**
  ```properties
  # Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  # Student No(s)#: 231805033, 231805026
  # General Comments: <one-line purpose of this file>
  ```
- **Windows Batch (`*.cmd`, `*.bat`):**
  ```bat
  @rem Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  @rem Student No(s)#: 231805033, 231805026
  @rem General Comments: <one-line purpose of this file>
  ```

> **Third-Party Generated Files Exception:** Standard third-party tool bootstrap files (`mvnw`, `mvnw.cmd`, `.mvn/wrapper/maven-wrapper.properties`) keep their upstream Apache 2.0 license headers intact and are attributed in `README.md`.

> **Generated JSON Data Files Exception:** Machine-generated JSON data files under `data/seed/` (`*.json`) cannot hold comments and therefore carry **no** header. Authorship is documented in `data/README.md` (which has the mandatory header), and the generator scripts that produce them (`tools/data/*.py`) keep the mandatory header. This exception applies **only** to generated JSON data files; all code and documents still require the header.

---

## 3. Shared Computer Rule (Mandatory Start-of-Chat Check)
Both team members work on this **same computer**, taking turns under a shared Windows session and GitHub login:
1. **At the very start of every chat session**, the agent MUST ask the user in **Turkish** who is currently at the keyboard (**Ibrahim Temur** or **Omer Faruk Kuş**).
2. **Before making any Git commit**, run `tools\set-author ibrahim` or `tools\set-author omer` so that repository-local (`--local` scope only) `user.name` and `user.email` match the active student.
3. **Never modify `--global` Git identity.**
4. **Never commit under the wrong person.**
5. Record the active team member's full name in every new entry added to `docs/process/ai-usage-log.md` and `docs/process/PROJECT_STATE.md`.

---

## 4. Engineering Methodology & Design Patterns
- **Methodology:** Agile **Scrum** with iterative sprints documented under `docs/04-sprints/`.
- **Object-Oriented Design Patterns:** Apply **GoF** (Gang of Four) and **GRASP** principles wherever architecturally justified (never forced artificially) and document every pattern decision, structure, and rationale in `docs/03-design/`.
- **Test-Driven Development (TDD):** Write or update automated JUnit 5 tests before or alongside production code and verify with `mvn test` (`.\mvnw.cmd test`).

---

## 5. Git, Branching, and Release Discipline
- **Build Tool:** Apache Maven (`mvn test`, `mvn package`, or `./mvnw.cmd`).
- **Branching Model:**
  - `main`: stable, user-approved releases only.
  - `develop`: ongoing sprint integration branch.
  - `feature/<short-topic>`, `fix/<short-topic>`, `docs/<short-topic>`: short-lived working branches created from `develop`.
- **Commit Format:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`).
- **Push Policy:** Push to `origin` after every commit.
- **Protected Main Policy:** Merge into `main` **ONLY after explicit approval** from the user.

---

## 6. UI-First Design Workflow (Stitch MCP)
- All user interface screens MUST first be designed using the **Stitch MCP** server.
- Exported HTML prototypes and screenshots from Stitch MUST be saved under `docs/03-design/ui/` before implementing the corresponding Spring MVC + Thymeleaf templates.

---

## 7. Academic Integrity, Data Privacy, and Security
- **Originality:** Never copy code or prose from external student projects. Cite any external references, standards, or libraries used.
- **AI Transparency:** Log every significant AI-assisted task in `docs/process/ai-usage-log.md` with date, active student name, prompt summary, the model name (log the model name exactly as shown in the Antigravity model selector, as told by the user), output produced, and human review notes.
- **Synthetic Data Only:** Never use real personal data (names, national IDs, phone numbers, real student records). All member and loan seed/test data in `data/seed/` and tests must be completely synthetic.
- **Zero Secrets:** Never commit API keys, tokens, passwords, or credentials to the repository or print them in logs.

---

## 8. Execution Cadence & Homework Packaging
- **Plan → Execute → Record:**
  1. Before writing or modifying code, present a short plan in Turkish.
  2. Execute and verify with automated tests (`mvn test`).
  3. After finishing each work item, update `docs/process/PROJECT_STATE.md` and `docs/process/ai-usage-log.md`.
- **Submission Archive Naming & Official 5-Homework Schedule:** Homework archives MUST be generated via `tools\package <NN>` and named:
  ```text
  cse305_hwNN_231805033_231805026.zip
  ```
  where `NN` is a two-digit number (`01`..`05`), excluding `target/`, `.git/`, `.venv/`, `dist/`, `data/db/`, `data/raw/`, and IDE metadata:
  - **Week 4 (Oct 20):** Project Group & Selected Project (*Library Management System*)
  - **HW01 — Week 5 (Oct 27):** `cse305_hw01_231805033_231805026.zip` — Project Proposal & Solution Outline (`docs/01-proposal/`)
  - **HW02 — Week 7 (Nov 10):** `cse305_hw02_231805033_231805026.zip` — Inception: Vision, System Context, Use Cases, Glossary, Business Rules, Themes, Epics, User Stories, Tasks, Sprint Planning, Product Backlog, PSI, MVP (`docs/02-inception/`)
  - **Weeks 8–9 (Nov 17–28):** Midterm Exam Weeks (reduced capacity buffer)
  - **HW03 — Week 11 (Dec 8):** `cse305_hw03_231805033_231805026.zip` — Elaboration (Use case diagram, System sequence diagram, Class diagram, TDD/Git/Maven plan) & **Sprint 1** (`docs/03-design/`, `docs/04-sprints/sprint-1/`, `src/`)
  - **HW04 — Week 13 (Dec 22):** `cse305_hw04_231805033_231805026.zip` — Construction & **Sprint 2** (`docs/04-sprints/sprint-2/`, `src/`)
  - **HW05 — Week 15 (Jan 5):** `cse305_hw05_231805033_231805026.zip` — Transition & **MVP Final Release** (`docs/04-sprints/sprint-3/`, `src/`)
- **Individual ADUZEM Upload Rule:** Remind the user when packaging an assignment that **both team members (Ibrahim Temur and Omer Faruk Kuş) must upload the generated `.zip` file individually from their own personal ADUZEM accounts**.

---

## 9. Agent Working "Hats" (Roles)
When executing tasks, explicitly adopt and reason from the appropriate software engineering perspective:
1. **Product Owner:** Clarifies domain rules, user stories, acceptance criteria, and backlog priority.
2. **Architect:** Governs layered architecture, domain boundaries, database schema, and GoF/GRASP design patterns.
3. **Developer:** Implements clean, idiomatic Java 17 / Spring Boot 3 code adhering to TDD and SOLID principles.
4. **QA Engineer:** Designs unit, slice, and integration tests, boundary conditions, and negative test cases.
5. **Reviewer:** Audits code quality, header compliance, security, git authorship, and documentation completeness before commit.
