<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Permanent agent operating rules, workflow standards, and academic policies for the CSE305 Library Management System.
-->
# AGENTS.md — Permanent Repository Rules

## Project Identity
- **Course:** CSE305 Software Engineering — Adnan Menderes University (ADU), Department of Computer Engineering
- **Project:** Library Management System (standalone project, unrelated to any other repository)
- **Authors:**
  - **Ibrahim Temur** — Student No: `231805033`
  - **Omer Faruk Kuş** — Student No: `231805026`

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
- **AI Transparency:** Log every significant AI-assisted task in `docs/process/ai-usage-log.md` with date, active student name, prompt summary, model, output produced, and human review notes.
- **Synthetic Data Only:** Never use real personal data (names, national IDs, phone numbers, real student records). All member and loan seed/test data in `data/seed/` and tests must be completely synthetic.
- **Zero Secrets:** Never commit API keys, tokens, passwords, or credentials to the repository or print them in logs.

---

## 8. Execution Cadence & Homework Packaging
- **Plan → Execute → Record:**
  1. Before writing or modifying code, present a short plan in Turkish.
  2. Execute and verify with automated tests (`mvn test`).
  3. After finishing each work item, update `docs/process/PROJECT_STATE.md` and `docs/process/ai-usage-log.md`.
- **Submission Archive Naming:** Homework archives MUST be generated via `tools\package <NN>` and named:
  ```text
  cse305_hwNN_231805033_231805026.zip
  ```
  where `NN` is a two-digit number (`01`, `02`, ...), excluding `target/`, `.git/`, `.venv/`, `dist/`, `data/db/`, and IDE metadata.

---

## 9. Agent Working "Hats" (Roles)
When executing tasks, explicitly adopt and reason from the appropriate software engineering perspective:
1. **Product Owner:** Clarifies domain rules, user stories, acceptance criteria, and backlog priority.
2. **Architect:** Governs layered architecture, domain boundaries, database schema, and GoF/GRASP design patterns.
3. **Developer:** Implements clean, idiomatic Java 17 / Spring Boot 3 code adhering to TDD and SOLID principles.
4. **QA Engineer:** Designs unit, slice, and integration tests, boundary conditions, and negative test cases.
5. **Reviewer:** Audits code quality, header compliance, security, git authorship, and documentation completeness before commit.
