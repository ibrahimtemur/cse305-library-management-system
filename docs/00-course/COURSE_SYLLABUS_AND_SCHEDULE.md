<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Official CSE305 Software Engineering Lecture 0 organizational policies, weekly course schedule, 5-homework project schedule, textbooks, and ADUZEM submission rules.
-->
# CSE305 Software Engineering — Course Syllabus, Project Schedule & Policies

> **Source:** Adnan Menderes University (ADU), Faculty of Engineering — *CSE305 Software Engineering, Lecture 0: Organizational Issues*, prepared and presented by **Assoc. Prof. Dr. Fatih Soygazi** (`fatih.soygazi@adu.edu.tr`, Office: C 3-41).

---

## 1. Course Metadata

| Field | Value |
|---|---|
| **Course Code & Title** | `CSE305` — Software Engineering |
| **Semester** | Fall |
| **Weekly Hours** | Theory: `2` hrs/week, Practice: `2` hrs/week |
| **Credits** | ADU Credit: `3` / ECTS: `5` |
| **Course Type** | Programme Compulsory Course (Undergraduate / First Cycle) |
| **Language of Instruction** | English |
| **Recommended Prerequisite** | `CSE203` — Object Oriented Programming |
| **Course Instructor** | **Assoc. Prof. Dr. Fatih Soygazi** (`fatih.soygazi@adu.edu.tr`, Office `#C 3-41`) |
| **Office Hours** | Monday `15:00–17:00`, Tuesday `10:00–12:00` |

---

## 2. Main Objective & Learning Outcomes

- **Main Objective:** Acquisition of the basic principles of software engineering and the ability to apply them in a software development project.
- **Learning Outcomes:** Upon successful completion of this course, students will learn:
  1. Software engineering **methodologies** (Unified Process & Agile Scrum),
  2. **Modeling techniques** (Use Cases, Domain Models, Class & Sequence Diagrams),
  3. **Design and development practices** (GRASP & GoF Object-Oriented Design Patterns, Architectural & UI Design),
  4. **Testing** (Test-Driven Development, Automated Build, Version Control).

---

## 3. Textbooks & Reference Materials

### Required Course Materials
1. **Roger S. Pressman & Bruce R. Maxim**, *"Software Engineering: A Practitioner's Approach"*, 9th Edition, McGraw Hill, 2020.
2. **Craig Larman**, *"Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development"*, 3rd Edition, Addison-Wesley, 2004.
3. Official CSE305 Lecture Notes.

### Recommended Course Materials
1. **Ian Sommerville**, *"Software Engineering"*, 10th Edition, Pearson, 2016.
2. **Kenneth S. Rubin**, *"Essential Scrum: A Practical Guide to the Most Popular Agile Process"*, 1st Edition, Addison-Wesley, 2012.

---

## 4. Weekly Course Lecture Schedule

| Week | Lecture Topics | Preliminary Preparation / Readings |
|---|---|---|
| **1** | Introduction | — |
| **2** | Software & Software Engineering | Pressman Ch. 1–2 |
| **3** | Process Models; Object Oriented Analysis & Design | Pressman Ch. 3–4; Larman Ch. 1 |
| **4** | Unified Process (UP) Approach; Use Cases | Larman Ch. 2–3–4–5–6–7 |
| **5** | Agile Development; Scrum | Pressman Ch. 5 |
| **6** | Domain Models | Larman Ch. 9 |
| **7** | Understanding Requirements; Class Diagram, Sequence Diagram | Pressman Ch. 8–9–10–11; Larman Ch. 10–15–16 |
| **8** | **MIDTERM EXAM** | — |
| **9** | **MIDTERM EXAM** | — |
| **10** | Design Concepts; GRASP Design Patterns | Pressman Ch. 12; Larman Ch. 17–18 |
| **11** | UP/Agile Tools, Test Driven Development, Automated Build, Version Control | — |
| **12** | Architectural Design, Component-Level Design | Pressman Ch. 13–14 |
| **13** | User Interface Design, Pattern-Based Design | Pressman Ch. 15–16 |
| **14** | More Object Design with GoF Patterns | Larman |
| **15** | AI-based Software Development Lifecycle | — |
| **16** | **FINAL EXAM** | — |

---

## 5. Official Project & Assignment Schedule (5 Homework Submissions)

The course evaluation consists of **5 Project Assignments (total weight: 40%)** and **1 Final Examination / Final Project Evaluation (weight: 60%)**.

| Week | Date / Deadline | Homework Archive ID | Official Deliverable Topics (UP or Agile Scrum Track) | Status in This Repository |
|---|---|---|---|---|
| **Week 4** | **October 20** | *(Group & Topic Selection)* | **Project Group, Selected Project** (*Library Management System* — Ibrahim Temur `231805033`, Omer Faruk Kuş `231805026`) | **COMPLETED** |
| **Week 6** *(postponed from Week 5 / Oct 27 per instructor's 2026-10-27 announcement)* | **November 3** | **`cse305_hw01_231805033_231805026.zip`** | **HW01 — Problem Description, Solution Outline & Domain Model:**<br>- Consolidated submission document (`docs/01-proposal/HW01_Problem_Solution_DomainModel.md` & `.pdf`) containing **Part 1: Problem Description**, **Part 2: Solution Outline**, and **Part 3: Domain Model** (Larman conceptual class diagram, enumerations, seed traceability, and modelling decisions), backed by `docs/01-proposal/PROJECT_PROPOSAL.md` (`v1.2`) and `docs/01-proposal/SOLUTION_OUTLINE.md` (`v1.2`). | **COMPLETED (v1.2 Ready for Submission)** |
| **Week 7** | **November 10** | **`cse305_hw02_231805033_231805026.zip`** | **HW02 — Inception:**<br>- *Agile Scrum Track:* Themes, epics, user stories, tasks, sprint planning, product backlog, PSI (Potentially Shippable Increment), MVP definition.<br>- *UP / Supporting Artifacts:* Vision document, system context diagram, use cases, iteration plan, supplementary specification, glossary, business rules (`docs/02-inception/`). | **IN PROGRESS (Part 1 Completed; Part 2 Next)** |
| **Weeks 8–9** | **Nov 17 – Nov 28** | — | **MIDTERM EXAM WEEKS** *(Reduced team capacity window)* | Planned Buffer |
| **Week 11** | **December 8** | **`cse305_hw03_231805033_231805026.zip`** | **HW03 — Elaboration OR Sprint 1:**<br>- Working Sprint 1 increment + Use case diagram, system sequence diagram, class diagram, plan for Test-Driven Development (TDD) / version control (Git) / Maven usage (`docs/03-design/`, `docs/04-sprints/sprint-1/`, `src/`). | Planned |
| **Week 13** | **December 22** | **`cse305_hw04_231805033_231805026.zip`** | **HW04 — Construction OR Sprint 2:**<br>- Working Sprint 2 increment (Circulation engine, overdue/fine calculation, GoF & GRASP patterns, Stitch UI + Thymeleaf views, JUnit 5 tests) (`docs/04-sprints/sprint-2/`, `src/`). | Planned |
| **Week 15** | **January 5** | **`cse305_hw05_231805033_231805026.zip`** | **HW05 — Transition OR MVP:**<br>- Complete Minimum Viable Product (MVP) release, reservation queue, dashboard, full test suite, and sprint reviews/retrospectives (`docs/04-sprints/sprint-3/`, `src/`). | Planned |

---

## 6. Assessment Breakdown

| Assessment Activity | Number | Weight (%) |
|---|---|---|
| **Assignments (Project Milestones HW01–HW05)** | `5` | **40%** |
| **Final Examination / Final Project / Dissertation** | `1` | **60%** |
| **TOTAL** | — | **100%** |

---

## 7. Official Project Policy Rules (Mandatory Compliance)

1. **Team Size:** Assignments may be submitted as a group of up to three students (our group consists of 2 students: **Ibrahim Temur** `231805033` and **Omer Faruk Kuş** `231805026`).
2. **Mandatory Source File Header:** Every source file must start with:
   ```text
   /*
   Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
   Student No(s)#: 231805033, 231805026
   General Comments: <purpose of file>
   */
   ```
3. **Methodology & Patterns:** Projects must be implemented using Unified Process (UP) or Agile (Scrum) methodologies, and the use of Object-Oriented Design Patterns (GRASP & GoF) is strongly encouraged.
4. **ADUZEM Archive Naming Format:** Compressed project archives uploaded to the ADUZEM portal assignment folder must be named:
   ```text
   cse305_hwNN_231805033_231805026.zip
   ```
   (e.g., `cse305_hw01_231805033_231805026.zip` generated via `tools\package 01`).
5. **Individual ADUZEM Upload Requirement:** **Each student must upload the assignment archive from his/her own individual ADUZEM account** (both **Ibrahim Temur** and **Omer Faruk Kuş** must upload the exact same `.zip` package to their respective ADUZEM accounts before each deadline).
6. **Academic Honesty:** Cheating or plagiarism is strictly prohibited and subject to the university's disciplinary policies.
