# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Parses the product backlog table and computes totals, sprint capacity, Must-fit check, and dependency proof for the HW02 agile documents.
"""Validate the product backlog and print the numbers used in the HW02 documents.

Usage: python3 tools/agile/validate_backlog.py [--md PATH] [--lang en|tr]
Every number in the agile documents must come from this script's output.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKLOG = ROOT / "docs/02-inception/PRODUCT_BACKLOG.md"

# ---- Planning assumptions (PO-confirmed 2026-11-07; recalibrate after Sprint 1) ----
SPRINTS = {
    "S1": (date(2026, 11, 11), date(2026, 12, 8)),
    "S2": (date(2026, 12, 9), date(2026, 12, 22)),
    "S3": (date(2026, 12, 23), date(2027, 1, 5)),
}
MIDTERM = (date(2026, 11, 17), date(2026, 11, 28))
HOURS_PER_PERSON_WEEK = {"normal": 8.0, "midterm": 3.0}
PEOPLE = 2
CEREMONY_H = {"S1": 4.0, "S2": 4.0, "S3": 4.0}   # team total (2 people x 2 h)
HW_DOC_H = {"S1": 8.0, "S2": 4.0, "S3": 7.0}     # HW03 / HW04 / HW05 human review + delivery
BUFFER = 0.10


def gross_capacity(start: date, end: date) -> float:
    """Team hours: per-person weekly hours prorated per calendar day."""
    total, day = 0.0, start
    while day <= end:
        rate = HOURS_PER_PERSON_WEEK["midterm" if MIDTERM[0] <= day <= MIDTERM[1] else "normal"]
        total += rate / 7.0
        day += timedelta(days=1)
    return total * PEOPLE


def parse_backlog(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    block = re.search(r"<!-- BACKLOG-TABLE:START -->(.*?)<!-- BACKLOG-TABLE:END -->", text, re.S).group(1)
    rows = [ln for ln in block.strip().splitlines() if ln.startswith("| LMS-")]
    stories = []
    for ln in rows:
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        stories.append({
            "id": c[0], "epic": c[1], "title": c[2], "moscow": c[3], "pts": int(c[4]),
            "classic": float(c[5]), "human": float(c[6]), "sessions": int(c[7]), "sprint": c[8],
            "deps": [] if c[9] in ("—", "-", "") else [d.strip() for d in c[9].split(",")],
            "owner": c[10], "status": c[11],
        })
    return stories


def fmt(x: float) -> str:
    return f"{x:.1f}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", type=Path, default=BACKLOG)
    ap.add_argument("--lang", choices=("en", "tr"), default="en")
    args = ap.parse_args()
    tr = args.lang == "tr"
    stories = parse_backlog(args.md)
    by_id = {s["id"]: s for s in stories}
    ok = True

    print(f"## Totals ({len(stories)} stories)")
    print(f"- Story points: {sum(s['pts'] for s in stories)}")
    print(f"- Human hours: {fmt(sum(s['human'] for s in stories))} (classic effort {fmt(sum(s['classic'] for s in stories))})")
    print(f"- Agent sessions: {sum(s['sessions'] for s in stories)}")
    for m in ("Must", "Should", "Could"):
        g = [s for s in stories if s["moscow"] == m]
        print(f"- {m}: {len(g)} stories, {sum(s['pts'] for s in g)} pts, {fmt(sum(s['human'] for s in g))} h")

    print("\n## " + ("Sprint kapasitesi (saat = insan emeği)" if tr else "Sprint capacity (hours = human effort)"))
    hdr = ["Sprint", "Gross", "Ceremonies", "HW docs", "Buffer", "Net for stories", "Planned", "Must", "Should", "Could", "Planned - Net"]
    if tr:
        hdr = ["Sprint", "Brüt", "Seremoni", "HW belge", "Tampon", "Hikâye net", "Planlanan", "Must", "Should", "Could", "Planlanan - Net"]
    print("| " + " | ".join(hdr) + " |")
    print("|" + "---|" * len(hdr))
    net_total = {}
    for sp, (a, b) in SPRINTS.items():
        g = gross_capacity(a, b)
        buf = g * BUFFER
        net = g - CEREMONY_H[sp] - HW_DOC_H[sp] - buf
        net_total[sp] = net
        grp = [s for s in stories if s["sprint"] == sp]
        part = {m: sum(s["human"] for s in grp if s["moscow"] == m) for m in ("Must", "Should", "Could")}
        planned = sum(part.values())
        print(f"| {sp} ({a:%b %d}–{b:%b %d}) | {fmt(g)} | {fmt(CEREMONY_H[sp])} | {fmt(HW_DOC_H[sp])} | {fmt(buf)} | {fmt(net)} | {fmt(planned)} | "
              f"{fmt(part['Must'])} | {fmt(part['Should'])} | {fmt(part['Could'])} | {planned - net:+.1f} |")

    must = sum(s["human"] for s in stories if s["moscow"] == "Must")
    must_s12 = sum(s["human"] for s in stories if s["moscow"] == "Must" and s["sprint"] in ("S1", "S2"))
    net12 = net_total["S1"] + net_total["S2"]
    print("\n## " + ("Must sığma kontrolü (Sprint 1 + Sprint 2)" if tr else "Must fit check (Sprint 1 + Sprint 2)"))
    print(f"- Must human hours: {fmt(must)} (in S1+S2: {fmt(must_s12)})")
    print(f"- S1+S2 net capacity: {fmt(net12)}")
    diff = must - net12
    verdict = "FITS" if diff <= 0 else "DOES NOT FIT"
    print(f"- Result: {verdict} (Must - Net = {diff:+.1f} h)")
    if diff > 0:
        ok = False
    if any(s["moscow"] == "Must" and s["sprint"] == "S3" for s in stories):
        print("- ERROR: a Must story is planned in S3"); ok = False

    print("\n## " + ("Bağımlılık kanıtı" if tr else "Dependency proof (no story depends on a later sprint)"))
    print("| Story | Sprint | Depends on | Dependency sprint | OK |")
    print("|---|---|---|---|---|")
    rank = {"S1": 1, "S2": 2, "S3": 3}
    for s in sorted(stories, key=lambda x: x["id"]):
        for d in s["deps"] or ["—"]:
            if d == "—":
                print(f"| {s['id']} | {s['sprint']} | — | — | yes |"); continue
            if d not in by_id:
                print(f"| {s['id']} | {s['sprint']} | {d} | MISSING | NO |"); ok = False; continue
            good = rank[by_id[d]["sprint"]] <= rank[s["sprint"]]
            ok &= good
            print(f"| {s['id']} | {s['sprint']} | {d} | {by_id[d]['sprint']} | {'yes' if good else 'NO'} |")
    print("\nOVERALL: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
