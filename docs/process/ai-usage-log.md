<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Audit log of all significant AI-assisted engineering tasks, outputs, and human review decisions.
-->
# AI Usage Log — CSE305 Library Management System

Every significant AI-assisted task in this project is logged below for academic transparency and traceability.

| Date | Person | Prompt Summary | Model / Tool | Output Produced | Human Review Notes |
|---|---|---|---|---|---|
| 2026-10-21 | Ibrahim Temur (231805033) | Task A/B/C bootstrap: inspect OS & toolchain, install Maven 3.9.16, check GitHub & Stitch MCP integrations, scaffold Spring Boot 3.5.16 project (`edu.adu.lms`) with passing test, create directory structure, `AGENTS.md`, process logs, `tools/set-author`, `tools/package`, initialize Git, and push `main` + `develop` to private GitHub repo. | Antigravity Agent (Claude Opus 4.6 planning / Gemini 3 Pro execution) | Installed Maven 3.9.16 + Wrapper; created `pom.xml`, `LibraryManagementApplication.java`, `LibraryManagementApplicationTests.java`, `AGENTS.md`, `README.md`, `.gitignore`, `.gitattributes`, `docs/**`, `tools/set-author.{ps1,cmd}`, `tools/package.{ps1,cmd}`; initialized Git (`db0acd1`) and pushed `main` and `develop` to `ibrahimtemur/cse305-library-management-system`. | Plan reviewed and approved by Ibrahim Temur prior to execution; verified `mvn test` and `.\mvnw.cmd test` pass, scripts work, and repository visibility is private. |
| 2026-10-21 | Ibrahim Temur (231805033) | Closing step of Sprint 0 bootstrap: finalize `docs/process/PROJECT_STATE.md` and `docs/process/ai-usage-log.md` with commit reference (`db0acd1`), verified status, next phase roadmap, and open questions; commit and push to `develop`. | Antigravity Agent (Gemini 3 Pro) | Updated `docs/process/PROJECT_STATE.md` and `docs/process/ai-usage-log.md`; committed and pushed to `origin/develop`. | Reviewed by Ibrahim Temur at the close of Session 01. |
