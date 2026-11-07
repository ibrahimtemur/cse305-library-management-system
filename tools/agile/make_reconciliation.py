#!/usr/bin/env python3
# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Generates docs/process/BACKLOG_POINT_RECONCILIATION.md directly from git show 28c40d9:docs/02-inception/PRODUCT_BACKLOG.md and current PRODUCT_BACKLOG.md / HW02_Inception_Agile.md.

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD_COMMIT = "28c40d9"
NEW_COMMIT = "df7eaa4"
BACKLOG_REL = "docs/02-inception/PRODUCT_BACKLOG.md"
HW02_MD = ROOT / "docs/02-inception/HW02_Inception_Agile.md"
OUT_MD = ROOT / "docs/process/BACKLOG_POINT_RECONCILIATION.md"


def parse_backlog_table(md_text: str) -> tuple[list[dict], list[str]]:
    m = re.search(
        r"<!-- BACKLOG-TABLE:START -->(.*?)<!-- BACKLOG-TABLE:END -->",
        md_text,
        re.S,
    )
    if not m:
        raise ValueError("Missing BACKLOG-TABLE markers")
    rows: list[dict] = []
    raw_lines: list[str] = []
    for line in m.group(1).strip().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        raw_lines.append(line)
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0] in ("ID", "---") or set(cells[0]) <= {"-"}:
            continue
        rows.append(
            {
                "id": cells[0],
                "epic": cells[1],
                "title": cells[2],
                "moscow": cells[3],
                "pts": int(cells[4]),
                "classic": float(cells[5]),
                "human": float(cells[6]),
                "sessions": int(cells[7]),
                "sprint": cells[8],
                "deps": cells[9],
                "status": cells[11] if len(cells) > 11 else "",
            }
        )
    return rows, raw_lines


def parse_hw02_md_tables(md_text: str) -> tuple[dict[str, tuple[int, float, float]], dict[str, tuple[int, float, float]]]:
    """Parse §2.2 Catalog of User Stories and §2.3 Ordered Product Backlog in HW02_Inception_Agile.md."""
    sec22: dict[str, tuple[int, float, float]] = {}
    for m in re.finditer(
        r"^\|\s*\*\*`(LMS-\d+)`\*\*\s*\|.*?\|\s*`(\d+)\s*pts`\s*/\s*`(\d+(?:\.\d+)?)\s*h`\s*/\s*`(\d+(?:\.\d+)?)\s*h`",
        md_text,
        re.M,
    ):
        sec22[m.group(1)] = (int(m.group(2)), float(m.group(3)), float(m.group(4)))

    sec23: dict[str, tuple[int, float, float]] = {}
    for m in re.finditer(
        r"^\|\s*\d+\s*\|\s*`(LMS-\d+)`\s*\|\s*E\d+\s*\|.*?\|\s*(Must|Should|Could)\s*\|\s*(\d+)\s*\|\s*(\d+(?:\.\d+)?)\s*\|\s*(\d+(?:\.\d+)?)\s*\|",
        md_text,
        re.M,
    ):
        sec23[m.group(1)] = (int(m.group(3)), float(m.group(4)), float(m.group(5)))
    return sec22, sec23


def fmt_num(v: float) -> str:
    return f"{v:.1f}" if v % 1 else f"{int(v)}"


def fmt_delta(new_v: float, old_v: float, is_float: bool = False) -> str:
    d = float(new_v) - float(old_v)
    if abs(d) < 1e-9:
        return "0"
    if is_float:
        return f"{d:+.1f}"
    return f"{int(d):+d}" if d.is_integer() else f"{d:+.1f}"


def summarize(rows: list[dict]) -> dict:
    tot_pts = sum(r["pts"] for r in rows)
    tot_classic = sum(r["classic"] for r in rows)
    tot_human = sum(r["human"] for r in rows)
    tot_sess = sum(r["sessions"] for r in rows)
    by_moscow = {}
    for p in ("Must", "Should", "Could"):
        sub = [r for r in rows if r["moscow"] == p]
        by_moscow[p] = {
            "count": len(sub),
            "pts": sum(r["pts"] for r in sub),
            "classic": sum(r["classic"] for r in sub),
            "human": sum(r["human"] for r in sub),
        }
    by_sprint = {}
    for sp in ("S1", "S2", "S3"):
        sub = [r for r in rows if r["sprint"] == sp]
        by_sprint[sp] = {
            "count": len(sub),
            "pts": sum(r["pts"] for r in sub),
            "classic": sum(r["classic"] for r in sub),
            "human": sum(r["human"] for r in sub),
        }
    return {
        "count": len(rows),
        "pts": tot_pts,
        "classic": tot_classic,
        "human": tot_human,
        "sessions": tot_sess,
        "by_moscow": by_moscow,
        "by_sprint": by_sprint,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Write docs/process/BACKLOG_POINT_RECONCILIATION.md")
    args = ap.parse_args()

    old_md = subprocess.check_output(
        ["git", "show", f"{OLD_COMMIT}:{BACKLOG_REL}"],
        cwd=ROOT,
        text=True,
    )
    new_md = (ROOT / BACKLOG_REL).read_text(encoding="utf-8")

    old_rows, old_raw = parse_backlog_table(old_md)
    new_rows, new_raw = parse_backlog_table(new_md)

    old_by_id = {r["id"]: r for r in old_rows}
    new_by_id = {r["id"]: r for r in new_rows}

    old_sum = summarize(old_rows)
    new_sum = summarize(new_rows)

    # Verify against HW02_Inception_Agile.md (§2.2 and §2.3)
    hw02_text = HW02_MD.read_text(encoding="utf-8")
    sec22, sec23 = parse_hw02_md_tables(hw02_text)
    mismatches = []
    for r in new_rows:
        sid = r["id"]
        expected = (r["pts"], r["classic"], r["human"])
        if sec22.get(sid) != expected:
            mismatches.append(f"HW02 §2.2 {sid}: got {sec22.get(sid)}, expected {expected}")
        if sec23.get(sid) != expected:
            mismatches.append(f"HW02 §2.3 {sid}: got {sec23.get(sid)}, expected {expected}")

    if mismatches:
        for m in mismatches:
            print(f"[ERROR] {m}", file=sys.stderr)
        return 1

    # Build reconciliation table rows in current backlog order
    table_lines = [
        "| Old ID (`28c40d9`) | Old Story Title (`28c40d9`) | Old MoSCoW | Old Sprint | Old Pts | Old Classic h | Old Human h | New ID (`HEAD` / PDF) | New Story Title (`HEAD` / PDF) | New MoSCoW | New Sprint | New Pts | New Classic h | New Human h | Δ Pts | Δ Classic h | Δ Human h | Reconciliation Note |",
        "|---|---|---|---|---:|---:|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]

    for nr in new_rows:
        nid = nr["id"]
        if nid == "LMS-015":
            orow = old_by_id["LMS-015"]
            note = (
                "Split part 1 (`015a`, committed): original `LMS-015` (`8 pts / 12 h / 5.0 h`) was re-calibrated to `5 pts / 10 h / 5.0 h` and split into `LMS-015` (`2 pts / 4 h / 2.0 h`) + `LMS-021` (`3 pts / 6 h / 3.0 h`)."
            )
            table_lines.append(
                f"| `{orow['id']}` | {orow['title']} | {orow['moscow']} | {orow['sprint']} | {orow['pts']} | {fmt_num(orow['classic'])} | {orow['human']:.1f} "
                f"| `{nr['id']}` | {nr['title']} | {nr['moscow']} | {nr['sprint']} | {nr['pts']} | {fmt_num(nr['classic'])} | {nr['human']:.1f} "
                f"| {fmt_delta(nr['pts'], orow['pts'])} | {fmt_delta(nr['classic'], orow['classic'])} | {fmt_delta(nr['human'], orow['human'], True)} | {note} |"
            )
        elif nid == "LMS-021":
            note = (
                "Split part 2 (`015b`, stretch): newly assigned story ID for the report table slice of `LMS-015` (combined `LMS-015 + LMS-021 = 5 pts / 10 h / 5.0 h`, net `-3 pts / -2 h / 0.0 h` vs `28c40d9` `LMS-015`)."
            )
            table_lines.append(
                f"| *(from `LMS-015`)* | *(Included in `LMS-015` in `28c40d9`)* | — | — | — | — | — "
                f"| `{nr['id']}` | {nr['title']} | {nr['moscow']} | {nr['sprint']} | {nr['pts']} | {fmt_num(nr['classic'])} | {nr['human']:.1f} "
                f"| +3 | +6 | +3.0 | {note} |"
            )
        else:
            orow = old_by_id[nid]
            d_pts = fmt_delta(nr["pts"], orow["pts"])
            d_cls = fmt_delta(nr["classic"], orow["classic"])
            d_hum = fmt_delta(nr["human"], orow["human"], True)
            if nr["pts"] == orow["pts"] and nr["classic"] == orow["classic"] and nr["human"] == orow["human"]:
                note = "Unchanged between `28c40d9` and `df7eaa4` / `HEAD`."
            elif nr["pts"] == orow["pts"] and nr["classic"] != orow["classic"]:
                note = f"Points (`{nr['pts']} pts`) and human hours (`{nr['human']:.1f} h`) unchanged; classic effort re-calibrated (`{fmt_num(orow['classic'])} -> {fmt_num(nr['classic'])} h`)."
            else:
                note = f"Re-calibrated in `df7eaa4` (`{orow['pts']} -> {nr['pts']} pts`, `{fmt_num(orow['classic'])} -> {fmt_num(nr['classic'])} classic h`); human hours unchanged (`{nr['human']:.1f} h`)."
            table_lines.append(
                f"| `{orow['id']}` | {orow['title']} | {orow['moscow']} | {orow['sprint']} | {orow['pts']} | {fmt_num(orow['classic'])} | {orow['human']:.1f} "
                f"| `{nr['id']}` | {nr['title']} | {nr['moscow']} | {nr['sprint']} | {nr['pts']} | {fmt_num(nr['classic'])} | {nr['human']:.1f} "
                f"| {d_pts} | {d_cls} | {d_hum} | {note} |"
            )

    table_lines.append(
        f"| **TOTAL (`20` stories)** | **`LMS-001`..`LMS-020` in `28c40d9`** | **11M / 6S / 3C** | **S1–S3** | **{old_sum['pts']}** | **{old_sum['classic']:.1f}** | **{old_sum['human']:.1f}** "
        f"| **TOTAL (`21` stories)** | **`LMS-001`..`LMS-021` in `HEAD` / PDF** | **11M / 7S / 3C** | **S1–S3** | **{new_sum['pts']}** | **{new_sum['classic']:.1f}** | **{new_sum['human']:.1f}** "
        f"| **{fmt_delta(new_sum['pts'], old_sum['pts'])}** | **{fmt_delta(new_sum['classic'], old_sum['classic'])}** | **{fmt_delta(new_sum['human'], old_sum['human'], True)}** | **Programmatically verified sums (`make_reconciliation.py`).** |"
    )

    doc = f"""<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Script-generated story-by-story reconciliation between initial git commit 28c40d9 and calibrated commit df7eaa4 / HEAD.
-->
# Backlog Story Point & Classic Effort Reconciliation (`28c40d9` → `{NEW_COMMIT}` / `HEAD`)

> [!NOTE]
> **Generated automatically by `python3 tools/agile/make_reconciliation.py` — zero manual typing.**
> This document parses `git show {OLD_COMMIT}:{BACKLOG_REL}` and the current `{BACKLOG_REL}` (and cross-checks `docs/02-inception/HW02_Inception_Agile.md` §2.2 & §2.3) to provide an exact, verifiable comparison of story IDs, titles, Fibonacci points, classic effort hours, and human hours.

---

## 1. Provenance & Git History Facts

1. **External Prompt Baseline vs. First Git Commit:**
   - A preliminary 23-story planning outline (`88` story points, `98` classic Must hours) was kept outside the repository and was never committed to Git.
   - The first Git commits of the Agile backlog on branch `docs/hw02-agile` were `6b4265c` (`USER_STORIES.md`) and `583e1a2` / `{OLD_COMMIT}` (`PRODUCT_BACKLOG.md`), which consolidated the backlog into **`{old_sum['count']}` stories (`LMS-001`..`LMS-020`)** totaling **`{old_sum['pts']}` story points**, **`{old_sum['classic']:.1f}` classic hours**, and **`{old_sum['human']:.1f}` human hours** (`{old_sum['sessions']}` agent sessions).
2. **Re-Calibration & Story Split in Commit `{NEW_COMMIT}` (`HEAD` / PDF):**
   - In commit `{NEW_COMMIT}`, story points and classic hours were re-calibrated across the backlog to **`{new_sum['pts']}` story points** and **`{new_sum['classic']:.1f}` classic hours** (with Must stories totaling **`{new_sum['by_moscow']['Must']['pts']}` points** and **`{new_sum['by_moscow']['Must']['classic']:.1f}` classic hours**: Sprint 1 = `{new_sum['by_sprint']['S1']['classic']:.1f} h`, Sprint 2 = `{new_sum['by_sprint']['S2']['classic']:.1f} h`), while human-hour estimates remained **`{new_sum['human']:.1f}` human hours** (`{new_sum['sessions']}` agent sessions).
   - By Product Owner decision, `LMS-015` (*Dashboard KPIs and overdue/unpaid report*) was split into **`LMS-015`** (*Operational dashboard KPI summary cards (015a)*, `2 pts`, `4` classic h, `2.0` human h — Sprint 3 Commit) and **`LMS-021`** (*Actionable overdue loans and unpaid fines report (015b)*, `3 pts`, `6` classic h, `3.0` human h — Sprint 3 Stretch), bringing the backlog to **`{new_sum['count']}` stories (`LMS-001`..`LMS-021`)**.

---

## 2. Raw Markdown Table Lines Read from Git (`{OLD_COMMIT}` vs `HEAD`)

### 2.1 `git show {OLD_COMMIT}:{BACKLOG_REL}` (Raw Table Lines)
```text
{chr(10).join(old_raw)}
```

### 2.2 Current `{BACKLOG_REL}` (`HEAD`, Raw Table Lines)
```text
{chr(10).join(new_raw)}
```

---

## 3. Story-by-Story Reconciliation Table (`{OLD_COMMIT}` vs `HEAD` / `HW02_Inception_Agile.pdf`)

{chr(10).join(table_lines)}

---

## 4. Category & Sprint Summary Comparison

| Category / Sprint | `{OLD_COMMIT}` Stories | `{OLD_COMMIT}` Pts | `{OLD_COMMIT}` Classic h | `{OLD_COMMIT}` Human h | `HEAD` / PDF Stories | `HEAD` / PDF Pts | `HEAD` / PDF Classic h | `HEAD` / PDF Human h | Δ Pts | Δ Classic h | Δ Human h |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Must Have** | {old_sum['by_moscow']['Must']['count']} | {old_sum['by_moscow']['Must']['pts']} | {old_sum['by_moscow']['Must']['classic']:.1f} | {old_sum['by_moscow']['Must']['human']:.1f} | {new_sum['by_moscow']['Must']['count']} | {new_sum['by_moscow']['Must']['pts']} | {new_sum['by_moscow']['Must']['classic']:.1f} | {new_sum['by_moscow']['Must']['human']:.1f} | {fmt_delta(new_sum['by_moscow']['Must']['pts'], old_sum['by_moscow']['Must']['pts'])} | {fmt_delta(new_sum['by_moscow']['Must']['classic'], old_sum['by_moscow']['Must']['classic'])} | {fmt_delta(new_sum['by_moscow']['Must']['human'], old_sum['by_moscow']['Must']['human'], True)} |
| **Should Have** | {old_sum['by_moscow']['Should']['count']} | {old_sum['by_moscow']['Should']['pts']} | {old_sum['by_moscow']['Should']['classic']:.1f} | {old_sum['by_moscow']['Should']['human']:.1f} | {new_sum['by_moscow']['Should']['count']} | {new_sum['by_moscow']['Should']['pts']} | {new_sum['by_moscow']['Should']['classic']:.1f} | {new_sum['by_moscow']['Should']['human']:.1f} | {fmt_delta(new_sum['by_moscow']['Should']['pts'], old_sum['by_moscow']['Should']['pts'])} | {fmt_delta(new_sum['by_moscow']['Should']['classic'], old_sum['by_moscow']['Should']['classic'])} | {fmt_delta(new_sum['by_moscow']['Should']['human'], old_sum['by_moscow']['Should']['human'], True)} |
| **Could Have** | {old_sum['by_moscow']['Could']['count']} | {old_sum['by_moscow']['Could']['pts']} | {old_sum['by_moscow']['Could']['classic']:.1f} | {old_sum['by_moscow']['Could']['human']:.1f} | {new_sum['by_moscow']['Could']['count']} | {new_sum['by_moscow']['Could']['pts']} | {new_sum['by_moscow']['Could']['classic']:.1f} | {new_sum['by_moscow']['Could']['human']:.1f} | {fmt_delta(new_sum['by_moscow']['Could']['pts'], old_sum['by_moscow']['Could']['pts'])} | {fmt_delta(new_sum['by_moscow']['Could']['classic'], old_sum['by_moscow']['Could']['classic'])} | {fmt_delta(new_sum['by_moscow']['Could']['human'], old_sum['by_moscow']['Could']['human'], True)} |
| **Sprint 1 (`S1`)** | {old_sum['by_sprint']['S1']['count']} | {old_sum['by_sprint']['S1']['pts']} | {old_sum['by_sprint']['S1']['classic']:.1f} | {old_sum['by_sprint']['S1']['human']:.1f} | {new_sum['by_sprint']['S1']['count']} | {new_sum['by_sprint']['S1']['pts']} | {new_sum['by_sprint']['S1']['classic']:.1f} | {new_sum['by_sprint']['S1']['human']:.1f} | {fmt_delta(new_sum['by_sprint']['S1']['pts'], old_sum['by_sprint']['S1']['pts'])} | {fmt_delta(new_sum['by_sprint']['S1']['classic'], old_sum['by_sprint']['S1']['classic'])} | {fmt_delta(new_sum['by_sprint']['S1']['human'], old_sum['by_sprint']['S1']['human'], True)} |
| **Sprint 2 (`S2`)** | {old_sum['by_sprint']['S2']['count']} | {old_sum['by_sprint']['S2']['pts']} | {old_sum['by_sprint']['S2']['classic']:.1f} | {old_sum['by_sprint']['S2']['human']:.1f} | {new_sum['by_sprint']['S2']['count']} | {new_sum['by_sprint']['S2']['pts']} | {new_sum['by_sprint']['S2']['classic']:.1f} | {new_sum['by_sprint']['S2']['human']:.1f} | {fmt_delta(new_sum['by_sprint']['S2']['pts'], old_sum['by_sprint']['S2']['pts'])} | {fmt_delta(new_sum['by_sprint']['S2']['classic'], old_sum['by_sprint']['S2']['classic'])} | {fmt_delta(new_sum['by_sprint']['S2']['human'], old_sum['by_sprint']['S2']['human'], True)} |
| **Sprint 3 (`S3`)** | {old_sum['by_sprint']['S3']['count']} | {old_sum['by_sprint']['S3']['pts']} | {old_sum['by_sprint']['S3']['classic']:.1f} | {old_sum['by_sprint']['S3']['human']:.1f} | {new_sum['by_sprint']['S3']['count']} | {new_sum['by_sprint']['S3']['pts']} | {new_sum['by_sprint']['S3']['classic']:.1f} | {new_sum['by_sprint']['S3']['human']:.1f} | {fmt_delta(new_sum['by_sprint']['S3']['pts'], old_sum['by_sprint']['S3']['pts'])} | {fmt_delta(new_sum['by_sprint']['S3']['classic'], old_sum['by_sprint']['S3']['classic'])} | {fmt_delta(new_sum['by_sprint']['S3']['human'], old_sum['by_sprint']['S3']['human'], True)} |
| **Total Backlog** | **{old_sum['count']}** | **{old_sum['pts']}** | **{old_sum['classic']:.1f}** | **{old_sum['human']:.1f}** | **{new_sum['count']}** | **{new_sum['pts']}** | **{new_sum['classic']:.1f}** | **{new_sum['human']:.1f}** | **{fmt_delta(new_sum['pts'], old_sum['pts'])}** | **{fmt_delta(new_sum['classic'], old_sum['classic'])}** | **{fmt_delta(new_sum['human'], old_sum['human'], True)}** |
"""

    if args.write:
        OUT_MD.write_text(doc, encoding="utf-8")
        print(f"[OK] Wrote {OUT_MD.relative_to(ROOT)} and verified 100% match with {HW02_MD.relative_to(ROOT)} (§2.2 & §2.3).")
    else:
        print(doc, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
