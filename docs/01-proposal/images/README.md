<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Directory index and regeneration commands for rendered Mermaid diagrams in the HW01 proposal package.
-->
# HW01 Rendered Diagrams (`docs/01-proposal/images`)

Contains the Mermaid source files (`*.mmd`) and their pre-rendered vector (`*.svg`) and high-resolution raster (`*.png`) exports embedded in [`../HW01_Problem_Solution_DomainModel.md`](../HW01_Problem_Solution_DomainModel.md) so that diagrams display cleanly in Markdown viewers without native Mermaid rendering as well as in the exported PDF.

## Files in This Directory

| File | Description |
|---|---|
| `domain-model.mmd` | Mermaid `classDiagram` source for the Part 3 Conceptual Domain Model (`Book`, `BookCopy`, `Member`, `Librarian`, `Loan`, `Fine`, `Reservation`). |
| `domain-model.png` | High-resolution (`3x` scale, white background) PNG export of `domain-model.mmd`. |
| `domain-model.svg` | Vector SVG export of `domain-model.mmd`. |
| `architecture-overview.mmd` | Mermaid `flowchart TB` source for the Part 2 Five-Tier Layered Web Architecture Overview. |
| `architecture-overview.png` | High-resolution (`2x` scale, white background) PNG export of `architecture-overview.mmd`. |
| `architecture-overview.svg` | Vector SVG export of `architecture-overview.mmd`. |

> **File Header Note:** The `.mmd` source files carry the mandatory CSE305 authorship header using Mermaid `%%` comments. Binary/generated output files (`*.png`, `*.svg`, and `../HW01_Problem_Solution_DomainModel.pdf`) are machine-rendered outputs produced from these sources and documented here.

## Regeneration Commands (PowerShell from Repository Root)

```powershell
npx --yes @mermaid-js/mermaid-cli -i docs/01-proposal/images/domain-model.mmd -o docs/01-proposal/images/domain-model.png -b white -s 3
npx --yes @mermaid-js/mermaid-cli -i docs/01-proposal/images/domain-model.mmd -o docs/01-proposal/images/domain-model.svg -b white
npx --yes @mermaid-js/mermaid-cli -i docs/01-proposal/images/architecture-overview.mmd -o docs/01-proposal/images/architecture-overview.png -b white -s 2
npx --yes @mermaid-js/mermaid-cli -i docs/01-proposal/images/architecture-overview.mmd -o docs/01-proposal/images/architecture-overview.svg -b white
```
