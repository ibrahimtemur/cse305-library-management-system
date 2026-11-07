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
STORIES_MD = ROOT / "docs/02-inception/USER_STORIES.md"
REQ_MD = ROOT / "docs/02-inception/REQUIREMENTS.md"
MUST_GAP_TRIGGER = 0.10   # PO rule: re-plan Sprint 2 if Must exceeds S1+S2 net by more than 10 percent

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


def parse_meta(path: Path) -> dict:
    """Read the **Meta:** line of every story in USER_STORIES.md."""
    meta, cur = {}, None
    for ln in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"### (LMS-\d{3}) ", ln)
        if m:
            cur = m.group(1)
        m = re.match(r"\*\*Meta:\*\* (E\d) \| (\w+) \| (\d+) pts \| ([\d.]+) h \(classic ([\d.]+)\) \| (\d+) agent sessions? \| (S\d) \| FR: (.*?) \| UC: (.*?) \| BR: (.*)$", ln)
        if m and cur:
            meta[cur] = {"epic": m[1], "moscow": m[2], "pts": int(m[3]), "human": float(m[4]), "classic": float(m[5]),
                         "sessions": int(m[6]), "sprint": m[7], "fr": m[8], "uc": m[9], "br": m[10]}
    return meta


def parse_requirements(path: Path) -> dict:
    reqs = {}
    for ln in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| \*\*`(FR-\d{3})`\*\* \| ([^|]+) \|.*\| ([^|]*) \| ([^|]*) \|\s*$", ln)
        if m:
            reqs[m[1]] = {"prio": m[2].strip(), "br": ", ".join(re.findall(r"BR-\d{3}", m[3])), "uc": ", ".join(re.findall(r"UC-\d{2}|System Startup", m[4]))}
    return reqs


def fr_coverage(meta: dict) -> dict:
    cov = {}
    for sid, m in meta.items():
        if m["fr"].startswith(("supports", "enabler")):
            continue
        for fr in re.findall(r"FR-\d{3}", m["fr"]):
            cov.setdefault(fr, []).append(sid)
    return cov


def fmt(x: float) -> str:
    return f"{x:.1f}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", type=Path, default=BACKLOG)
    ap.add_argument("--emit-trace", action="store_true")
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
    print("*Sign convention for `Planned - Net`: positive (`+`) = overrun / over net capacity (`over`); negative (`-`) = unused net capacity (`slack`).*")
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
        delta = planned - net
        label = "over" if delta > 0 else "slack"
        if sp == "S3":
            committed_s3 = sum(s["human"] for s in grp if "commit" in s["status"])
            c_delta = committed_s3 - net
            delta_str = f"{delta:+.1f} h (over; {c_delta:+.1f} h slack committed)"
        else:
            delta_str = f"{delta:+.1f} h ({label})"
        print(f"| {sp} ({a:%b %d}–{b:%b %d}) | {fmt(g)} | {fmt(CEREMONY_H[sp])} | {fmt(HW_DOC_H[sp])} | {fmt(buf)} | {fmt(net)} | {fmt(planned)} | "
              f"{fmt(part['Must'])} | {fmt(part['Should'])} | {fmt(part['Could'])} | {delta_str} |")

    must = sum(s["human"] for s in stories if s["moscow"] == "Must")
    must_s12 = sum(s["human"] for s in stories if s["moscow"] == "Must" and s["sprint"] in ("S1", "S2"))
    net12 = net_total["S1"] + net_total["S2"]
    print("\n## " + ("Must sığma kontrolü (Sprint 1 + Sprint 2)" if tr else "Must fit check (Sprint 1 + Sprint 2)"))
    print(f"- Must human hours: {fmt(must)} (in S1+S2: {fmt(must_s12)})")
    print(f"- S1+S2 net capacity: {fmt(net12)}")
    diff = must_s12 - net12
    pct = diff / net12 * 100
    if diff <= 0:
        print(f"- Result: FITS (Must - Net = {diff:+.1f} h)")
    elif diff / net12 <= MUST_GAP_TRIGGER:
        print(f"- Result: KNOWN GAP, ACCEPTED RISK (Must - Net = {diff:+.1f} h = {pct:.1f} percent of net; trigger is {MUST_GAP_TRIGGER*100:.0f} percent)")
    else:
        print(f"- Result: GAP ABOVE TRIGGER (Must - Net = {diff:+.1f} h = {pct:.1f} percent): re-plan Sprint 2 and ask the Product Owner")
        ok = False
    if any(s["moscow"] == "Must" and s["sprint"] == "S3" for s in stories):
        print("- ERROR: a Must story is planned in S3"); ok = False

    print("\n## Sprint 3 commitment line (Should stories in backlog order, cumulative human hours)")
    print(f"- Sprint 3 net capacity: {fmt(net_total['S3'])}")
    print("| Rank | Story | MoSCoW | Human h | Cumulative h | Line |")
    print("|---|---|---|---|---|---|")
    cum, rank = 0.0, 0
    for s in [x for x in stories if x["sprint"] == "S3"]:
        rank += 1
        cum += s["human"]
        line = "COMMIT" if (s["moscow"] == "Should" and cum <= net_total["S3"]) else "STRETCH"
        print(f"| {rank} | {s['id']} {s['title']} | {s['moscow']} | {fmt(s['human'])} | {fmt(cum)} | {line} |")

    print("\n## Story meta vs backlog (USER_STORIES.md)")
    meta = parse_meta(STORIES_MD)
    bad = []
    for s in stories:
        m = meta.get(s["id"])
        if not m:
            bad.append(f"{s['id']}: no Meta line"); continue
        for k_m, k_s in (("epic", "epic"), ("moscow", "moscow"), ("pts", "pts"), ("human", "human"), ("classic", "classic"), ("sessions", "sessions"), ("sprint", "sprint")):
            if m[k_m] != s[k_s]:
                bad.append(f"{s['id']}: {k_m} story={m[k_m]} backlog={s[k_s]}")
    for sid in meta:
        if sid not in by_id:
            bad.append(f"{sid}: in USER_STORIES.md but not in backlog")
    print("- Mismatches: " + ("none" if not bad else "; ".join(bad)))
    ok &= not bad

    print("\n## Task hours vs story hours (TASKS.md)")
    tt = ROOT / "docs/02-inception/TASKS.md"
    sums, ntasks = {}, 0
    for ln in tt.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| (T-\d{3}-\d+) \| (LMS-\d{3}) \| .* \| ([\d.]+) \|\s*\|\s*$", ln)
        if m:
            sums[m[2]] = sums.get(m[2], 0.0) + float(m[3]); ntasks += 1
    tbad = [f"{s['id']}: tasks {sums.get(s['id'], 0.0):.1f} vs story {s['human']:.1f}" for s in stories if abs(sums.get(s["id"], 0.0) - s["human"]) > 1e-9]
    print(f"- Tasks: {ntasks}; total task hours {sum(sums.values()):.1f}; mismatches: {'none' if not tbad else '; '.join(tbad)}")
    ok &= not tbad

    print("\n## FR coverage (every Must FR must be in Sprint 1 or Sprint 2)")
    reqs = parse_requirements(REQ_MD)
    cov = fr_coverage(meta)
    must_frs = [f for f, r in reqs.items() if r["prio"].startswith("Must")]
    miss = [f for f in must_frs if not any(by_id[x]["sprint"] in ("S1", "S2") for x in cov.get(f, []))]
    uncovered = [f for f in reqs if f not in cov]
    print(f"- FR in REQUIREMENTS.md: {len(reqs)}; Must FR: {len(must_frs)} ({must_frs[0]}..{must_frs[-1]})")
    print(f"- Must FR not covered in S1+S2: {miss or 'none'}")
    print(f"- Any FR without a story: {uncovered or 'none'}")
    ok &= not miss and not uncovered
    if args.emit_trace:
        print("\n## Traceability table (FR -> UC -> BR -> story)")
        print("| FR | MoSCoW | UC | BR | Story | Sprint |")
        print("|---|---|---|---|---|---|")
        for f, r in reqs.items():
            ids = cov.get(f, [])
            print(f"| {f} | {r['prio']} | {r['uc']} | {r['br']} | {', '.join(ids)} | {', '.join(sorted({by_id[i]['sprint'] for i in ids}))} |")

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

    print("\n## Seed v2 JSON breakdown check (data/seed/*.json vs docs)")
    import json
    from collections import Counter
    seed_dir = ROOT / "data/seed"
    books_j = json.loads((seed_dir / "books-openlibrary.json").read_text(encoding="utf-8"))
    copies_j = json.loads((seed_dir / "copies.json").read_text(encoding="utf-8"))
    members_j = json.loads((seed_dir / "members.json").read_text(encoding="utf-8"))
    libs_j = json.loads((seed_dir / "librarians.json").read_text(encoding="utf-8"))
    loans_j = json.loads((seed_dir / "loans.json").read_text(encoding="utf-8"))
    fines_j = json.loads((seed_dir / "fines.json").read_text(encoding="utf-8"))
    res_j = json.loads((seed_dir / "reservations.json").read_text(encoding="utf-8"))

    ref_cnt = Counter(bool(b.get("referenceOnly")) for b in books_j)
    cp_cnt = Counter(c.get("status") for c in copies_j)
    mt_cnt = Counter(m.get("memberType") for m in members_j)
    ms_cnt = Counter(m.get("status") for m in members_j)
    ln_cnt = Counter(l.get("status") for l in loans_j)
    fn_cnt = Counter(f.get("status") for f in fines_j)
    unpaid_try = sum(float(f.get("amount", 0)) for f in fines_j if f.get("status") == "UNPAID")
    rs_cnt = Counter(r.get("status") for r in res_j)

    print(f"- Books: {len(books_j)} (circulating={ref_cnt[False]}, referenceOnly={ref_cnt[True]})")
    print(f"- Copies: {len(copies_j)} (AVAILABLE={cp_cnt['AVAILABLE']}, LOANED={cp_cnt['LOANED']}, MAINTENANCE={cp_cnt['MAINTENANCE']}, LOST={cp_cnt['LOST']}, RESERVED={cp_cnt['RESERVED']})")
    print(f"- Members: {len(members_j)} (STUDENT={mt_cnt['STUDENT']}, ACADEMIC_STAFF={mt_cnt['ACADEMIC_STAFF']}, ADMINISTRATIVE_STAFF={mt_cnt['ADMINISTRATIVE_STAFF']}; ACTIVE={ms_cnt['ACTIVE']}, SUSPENDED={ms_cnt['SUSPENDED']})")
    print(f"- Librarians: {len(libs_j)}")
    print(f"- Loans: {len(loans_j)} (ACTIVE={ln_cnt['ACTIVE']}, RETURNED={ln_cnt['RETURNED']}, LOST={ln_cnt['LOST']})")
    print(f"- Fines: {len(fines_j)} (UNPAID={fn_cnt['UNPAID']} [{unpaid_try:.2f} TRY], PAID={fn_cnt['PAID']}, WAIVED={fn_cnt['WAIVED']})")
    print(f"- Reservations: {len(res_j)} (WAITING={rs_cnt['WAITING']}, READY={rs_cnt['READY']})")

    doc_files = [ROOT / "README.md", ROOT / "data/README.md", ROOT / "data/seed/README.md", ROOT / "docs/process/PROJECT_STATE.md"] + sorted((ROOT / "docs/02-inception").glob("*.md"))
    forbidden_patterns = [
        (r"\b29\b[^|\n]{0,25}referenceOnly|referenceOnly[^|\n]{0,25}\b29\b", "outdated 29 referenceOnly"),
        (r"\b1[,.]?472\b", "outdated 1,472 AVAILABLE copies"),
        (r"\b164\s+`?LOANED`?", "outdated 164 LOANED copies"),
        (r"\b8\s+`?RESERVED`?", "outdated 8 RESERVED copies"),
        (r"\b49\s+`?MAINTENANCE`?", "outdated 49 MAINTENANCE copies"),
        (r"\b13\s+`?LOST`?", "outdated 13 LOST copies/loans"),
        (r"\b42\s+`?STUDENT`?", "outdated 42 STUDENT members"),
        (r"\b12\s+`?ACADEMIC_STAFF`?", "outdated 12 ACADEMIC_STAFF members"),
        (r"\b6\s+`?ADMINISTRATIVE_STAFF`?", "outdated 6 ADMINISTRATIVE_STAFF members"),
        (r"\b56\s+`?ACTIVE`?", "outdated 56 ACTIVE members"),
        (r"\b4\s+`?SUSPENDED`?", "outdated 4 SUSPENDED members"),
        (r"\b58\s+`?ACTIVE`?", "outdated 58 ACTIVE loans"),
        (r"\b93\s+`?RETURNED`?", "outdated 93 RETURNED loans"),
        (r"\b18\s+`?UNPAID`?", "outdated 18 UNPAID fines"),
        (r"\b23\s+`?PAID`?", "outdated 23 PAID fines"),
        (r"\b6\s+`?WAIVED`?", "outdated 6 WAIVED fines"),
        (r"\b14\s+`?WAITING`?", "outdated 14 WAITING reservations"),
        (r"\b8\s+`?READY`?", "outdated 8 READY reservations"),
    ]
    seed_errors = []
    for df in doc_files:
        if not df.exists():
            continue
        txt = df.read_text(encoding="utf-8")
        for pat, desc in forbidden_patterns:
            if re.search(pat, txt):
                seed_errors.append(f"{df.relative_to(ROOT)}: found {desc}")
    for req_doc in (ROOT / "data/README.md", ROOT / "data/seed/README.md", ROOT / "docs/02-inception/REQUIREMENTS.md", ROOT / "docs/02-inception/USER_STORIES.md", ROOT / "docs/02-inception/HW02_Inception_Agile.md"):
        txt = req_doc.read_text(encoding="utf-8")
        for expected_tok in ("1,624", "59", "100", "26", "16", "19"):
            if expected_tok not in txt:
                seed_errors.append(f"{req_doc.relative_to(ROOT)}: missing verified seed breakdown token '{expected_tok}'")
    print("- Seed breakdown mismatches in docs: " + ("none" if not seed_errors else "; ".join(seed_errors)))
    ok &= not seed_errors

    print("\nOVERALL: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
