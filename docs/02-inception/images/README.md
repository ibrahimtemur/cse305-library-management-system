<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Directory index and regeneration commands for rendered Mermaid diagrams in the HW02 inception and Agile package.
-->
# HW02 Rendered Diagrams (`docs/02-inception/images`)

Contains the Mermaid source files (`*.mmd`) and their pre-rendered vector (`*.svg`) and high-resolution raster (`*.png`) exports embedded in [`../HW02_Inception_Agile.md`](../HW02_Inception_Agile.md) so that diagrams display cleanly in Markdown viewers and in the exported PDF (`../HW02_Inception_Agile.pdf` and root `HW02_Inception_Agile.pdf`).

## Files in This Directory

| File | Description |
|---|---|
| `system-context.mmd` / `.png` / `.svg` | System Context Diagram showing human actors (`ROLE_LIBRARIAN`, `ROLE_MEMBER`, `ROLE_GUEST`), the Spring Boot + H2 + Seed v2 system boundary, the offline Open Library data-preparation pipeline, and explicitly excluded external systems. |
| `use-case-diagram.mmd` / `.png` / `.svg` | Use Case Diagram mapping the three actor roles to `UC-01`..`UC-11`. |
| `themes-epics.mmd` / `.png` / `.svg` | Agile Scrum hierarchy mapping 4 Themes (`T1`..`T4`) to 9 Epics (`E1`..`E9`) across 21 stories (`88` story points, `90.0` human hours). |
| `sprint-roadmap.mmd` / `.png` / `.svg` | Three-Sprint Iteration Roadmap (Sprint 1 / HW03, Sprint 2 / HW04, Sprint 3 / HW05) showing net capacity, Must stories (`53.0 h`), the Sprint 3 commitment line (`17.5 h <= 17.8 h`), and stretch stories (`19.5 h`). |
| `trello-board.png` | Screenshot of the public Trello Sprint Board (`https://trello.com/b/34K6O3Y1/cse305-lms-sprint-board`) showing the 6-list workflow and story cards. |

> **File Header Note:** The `.mmd` source files carry the mandatory CSE305 authorship header using Mermaid `%%` comments. Binary/generated output files (`*.png`, `*.svg`, and `../HW02_Inception_Agile.pdf`) are machine-rendered outputs produced from these sources and documented here.

## Regeneration Commands (Linux VM or PowerShell from Repository Root)

```bash
for name in system-context use-case-diagram themes-epics sprint-roadmap; do
  npx --yes @mermaid-js/mermaid-cli -p tools/puppeteer-config.json -i "docs/02-inception/images/${name}.mmd" -o "docs/02-inception/images/${name}.png" -b white -s 2
  npx --yes @mermaid-js/mermaid-cli -p tools/puppeteer-config.json -i "docs/02-inception/images/${name}.mmd" -o "docs/02-inception/images/${name}.svg" -b white
done
```
