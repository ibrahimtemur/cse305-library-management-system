<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Root project documentation covering overview, team, tech stack, build instructions, workflow, and academic disclosures.
-->
# CSE305 — Library Management System

A standalone web-based **Library Management System** developed for **CSE305 Software Engineering** at **Adnan Menderes University (ADU)**, Department of Computer Engineering, following **Agile Scrum**, **Test-Driven Development (TDD)**, **GoF/GRASP Object-Oriented Design Patterns**, and an **agentic software engineering workflow**.

- **GitHub Repository:** [`https://github.com/ibrahimtemur/cse305-library-management-system`](https://github.com/ibrahimtemur/cse305-library-management-system) *(Private academic repository; collaborator access available to the course instructor upon request)*
- **Course Instructor:** Assoc. Prof. Dr. Fatih Soygazi (`fatih.soygazi@adu.edu.tr`)

---

## Team Members

| Name Surname | Student Number | Role |
|---|---|---|
| **Ibrahim Temur** | `231805033` | **Product Owner (PO)** & Full-Stack Developer / Architect / QA / Reviewer |
| **Omer Faruk Kuş** | `231805026` | **Scrum Master (SM)** & Full-Stack Developer / Architect / QA / Reviewer |

---

## HW01 Submission Deliverables (`v1.2` — Due: Tuesday, November 3, 2026)

For immediate inspection when opening the submission archive (`cse305_hw01_231805033_231805026.zip`), the consolidated three-part **HW01** document (**Part 1: Problem Description**, **Part 2: Solution Outline**, and **Part 3: Domain Model**) is placed both at the repository root and under [`docs/01-proposal/`](docs/01-proposal/README.md):

- **[`HW01_Problem_Solution_DomainModel.pdf`](HW01_Problem_Solution_DomainModel.pdf)** *(Root-level print-ready PDF with rendered diagrams)*
- **[`docs/01-proposal/HW01_Problem_Solution_DomainModel.md`](docs/01-proposal/HW01_Problem_Solution_DomainModel.md)** & **[`docs/01-proposal/HW01_Problem_Solution_DomainModel.pdf`](docs/01-proposal/HW01_Problem_Solution_DomainModel.pdf)** *(Consolidated Markdown source & PDF)*
- **[`docs/01-proposal/PROJECT_PROPOSAL.md`](docs/01-proposal/PROJECT_PROPOSAL.md)** (`v1.2`) — Detailed Problem Description, Stakeholders, Scope, MoSCoW Features, Confirmed ADU Rules & `ASSUMPTION-01`..`17`, Scrum Timeline, and Risk Matrix
- **[`docs/01-proposal/SOLUTION_OUTLINE.md`](docs/01-proposal/SOLUTION_OUTLINE.md)** (`v1.2`) — Detailed 5-Tier Layered Architecture, Technology Stack, Stitch MCP UI-First Workflow, `Seed v2` Data Strategy, and GoF/GRASP Design Patterns
- **[`docs/01-proposal/images/domain-model.png`](docs/01-proposal/images/domain-model.png)** / **[`.svg`](docs/01-proposal/images/domain-model.svg)** / **[`.mmd`](docs/01-proposal/images/domain-model.mmd)** — Larman (Ch. 9) Conceptual Domain Model Class Diagram

---

## Technology Stack

- **Language:** Java 17 (compiled with `--release 17`, compatible with JDK 17–25)
- **Framework:** Spring Boot 3.5.16 (`spring-boot-starter-web`, `spring-boot-starter-thymeleaf`, `spring-boot-starter-data-jpa`, `spring-boot-starter-validation`)
- **Database:** H2 Database (persistent file mode at `./data/db/lms` for runtime; isolated in-memory mode for automated tests)
- **Testing:** JUnit 5 (`spring-boot-starter-test`)
- **Build Tool:** Apache Maven 3.9.16 (includes Maven Wrapper `mvnw` / `mvnw.cmd`)
- **UI Design Pipeline:** Stitch MCP prototypes exported to `docs/03-design/ui/` prior to Thymeleaf implementation

---

## Repository Structure

```text
LibraryManagementSystem/
├── HW01_Problem_Solution_DomainModel.pdf # Root-level consolidated HW01 submission PDF (v1.2)
├── AGENTS.md                        # Permanent AI agent & engineering governance rules
├── README.md                        # Project overview and usage instructions
├── pom.xml                          # Maven build configuration
├── mvnw / mvnw.cmd                  # Maven Wrapper scripts
├── docs/
│   ├── 00-course/                   # Course guidelines and assignment rubrics
│   ├── 01-proposal/                 # HW01 Problem Description, Solution Outline & Domain Model (v1.2)
│   ├── 02-inception/                # Requirements, personas, use cases, product backlog
│   ├── 03-design/                   # Architecture, UML diagrams, GoF/GRASP documentation
│   │   └── ui/                      # Stitch UI screen designs and exports
│   ├── 04-sprints/                  # Sprint planning, review, and retrospective artifacts
│   └── process/
│       ├── PROJECT_STATE.md         # Current phase, completed work, decisions, next steps
│       └── ai-usage-log.md          # Complete audit log of AI-assisted tasks
├── data/
│   └── seed/                        # Reproducible Open Library + synthetic seed v2 datasets
├── tools/
│   ├── data/                        # Reproducible seed data pipeline scripts & 80 unit tests
│   ├── set-author.ps1 / .cmd        # Sets repository-local Git author (ibrahim | omer)
│   └── package.ps1 / .cmd           # Builds homework zip: cse305_hwNN_231805033_231805026.zip
└── src/
    ├── main/
    │   ├── java/edu/adu/lms/        # Application source code
    │   └── resources/               # Templates, static assets, application.properties
    └── test/
        ├── java/edu/adu/lms/        # Automated JUnit 5 test suite
        └── resources/               # Test-specific configuration
```

---

## Getting Started

### 1. Select Active Author (Shared Computer Rule)
Because both team members work on the same workstation in turns, always set the local Git author before committing:

```powershell
# If Ibrahim Temur is working:
tools\set-author ibrahim

# If Omer Faruk Kuş is working:
tools\set-author omer
```

### 2. Run Automated Tests
```powershell
mvn test
# or without a system Maven installation:
.\mvnw.cmd test
```

### 3. Run the Application Locally
```powershell
mvn spring-boot:run
```
- Application URL: `http://localhost:8080`
- H2 Console (local dev): `http://localhost:8080/h2-console` (`JDBC URL`: `jdbc:h2:file:./data/db/lms;AUTO_SERVER=TRUE`, user: `sa`, password: empty)

### 4. Package a Homework Submission Archive
```powershell
tools\package 01
```
Produces `dist\cse305_hw01_231805033_231805026.zip` with `target/`, `.git/`, `.venv/`, `dist/`, `data/db/`, and IDE files excluded.

---

## Academic Integrity & Third-Party Notices

- All AI-assisted tasks are logged with human review notes in [`docs/process/ai-usage-log.md`](docs/process/ai-usage-log.md).
- All seed and test datasets are strictly synthetic.
- `mvnw`, `mvnw.cmd`, and `.mvn/wrapper/maven-wrapper.properties` are generated by the Apache Maven Wrapper Plugin under the Apache License, Version 2.0.
