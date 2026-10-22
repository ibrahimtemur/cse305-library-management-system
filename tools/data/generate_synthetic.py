# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Reproducible generator of 100% synthetic members, librarians, copies, loans, fines, and reservations for the LMS seed data (feature M6).
"""Generate synthetic operational seed data.

Everything produced here is fictional. No real person, ADU student, staff member, or
institutional identifier is used. The generator only reads ``books-openlibrary.json``
and is fully deterministic (fixed ``RANDOM_SEED``, fixed ``REFERENCE_DATE``, pinned Faker).

Business rules follow the project ASSUMPTIONs in ``docs/01-proposal/PROJECT_PROPOSAL.md``:
  ASSUMPTION-02 loan limits, -03 loan periods, -04 one renewal, -05 fines (5.00 TRY/day,
  cap 250.00 TRY), -06 borrowing block on overdue/unpaid fines/suspension, -07 FIFO holds,
  -09 one to four copies per title.

Usage (PowerShell):
    tools\\data\\.venv\\Scripts\\python.exe tools\\data\\generate_synthetic.py
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from faker import Faker

from lms_seed_common import (
    BOOKS_FILE,
    CURRENCY,
    LOAN_DAYS,
    MAX_ACTIVE_LOANS,
    RANDOM_SEED,
    REFERENCE_DATE,
    SEED_DIR,
    compute_fine,
    overdue_days,
    read_json,
    write_json,
)

STUDENT_COUNT = 44
STAFF_COUNT = 16
SUSPENDED_STUDENTS = 3
SUSPENDED_STAFF = 1
LIBRARIAN_COUNT = 3

DEPARTMENTS = [
    "Computer Engineering",
    "Electrical and Electronics Engineering",
    "Mechanical Engineering",
    "Mathematics",
    "Physics",
    "Chemistry",
    "History",
    "Philosophy",
    "Turkish Language and Literature",
    "Business Administration",
]

DUE_SOON_DAYS = 3  # An active loan is "due soon" when due within 0..3 days.
HISTORY_WINDOW_DAYS = 300
HISTORY_START = REFERENCE_DATE - timedelta(days=HISTORY_WINDOW_DAYS)

# Profile counts for non-suspended members (sum = 56).
PROFILE_COUNTS = {"OVERDUE": 12, "DUE_SOON": 9, "ONTIME": 13, "HISTORY": 22}
TERMINAL_UNPAID_ACTIVE_MEMBERS = 5  # HISTORY-profile members blocked by an unpaid fine.
TERMINAL_UNPAID_SUSPENDED = 2
QUEUE_TITLES = 9
READY_TITLES = 3
MAINTENANCE_COPIES = 15
LOST_COPIES = 8
COPY_COUNT_WEIGHTS = {1: 30, 2: 35, 3: 20, 4: 15}
FAR_FUTURE = date.max


def iso(value: date | None) -> str | None:
    return value.isoformat() if value else None


class CopyCalendar:
    """Tracks half-open loan intervals per copy so no copy is ever loaned twice at once."""

    def __init__(self) -> None:
        self._intervals: dict[str, list[tuple[date, date]]] = defaultdict(list)

    def is_free(self, barcode: str, start: date, end: date) -> bool:
        return all(not (start < b and s < end) for s, b in self._intervals[barcode])

    def book(self, barcode: str, start: date, end: date) -> None:
        self._intervals[barcode].append((start, end))


def sample_late_days(rng: random.Random) -> int:
    roll = rng.random()
    if roll < 0.60:
        return rng.randint(1, 14)
    if roll < 0.85:
        return rng.randint(15, 49)
    return rng.randint(50, 80)


def sample_overdue_active_days(rng: random.Random) -> int:
    roll = rng.random()
    if roll < 0.25:
        return rng.randint(1, 7)
    if roll < 0.65:
        return rng.randint(8, 30)
    if roll < 0.85:
        return rng.randint(31, 49)
    return rng.randint(50, 80)


def build_members(rng: random.Random, fake: Faker) -> list[dict[str, Any]]:
    members: list[dict[str, Any]] = []
    for kind, prefix, count, member_type in (
        ("STU", "SYN-STU", STUDENT_COUNT, "STUDENT"),
        ("STF", "SYN-STF", STAFF_COUNT, "ACADEMIC_STAFF"),
    ):
        for number in range(1, count + 1):
            member_id = f"{prefix}-{number:04d}"
            registered = (
                date(2023, 9, 1) + timedelta(days=rng.randint(0, 800))
                if member_type == "STUDENT"
                else date(2018, 9, 1) + timedelta(days=rng.randint(0, 2000))
            )
            members.append(
                {
                    "memberId": member_id,
                    "firstName": fake.first_name(),
                    "lastName": fake.last_name(),
                    "email": f"{member_id.lower()}@synthetic.lms.local",
                    "memberType": member_type,
                    "status": "ACTIVE",
                    "department": rng.choice(DEPARTMENTS),
                    "registeredOn": registered,
                }
            )
    students = [m for m in members if m["memberType"] == "STUDENT"]
    staff = [m for m in members if m["memberType"] == "ACADEMIC_STAFF"]
    for member in rng.sample(students, SUSPENDED_STUDENTS) + rng.sample(staff, SUSPENDED_STAFF):
        member["status"] = "SUSPENDED"
    return members


def build_librarians(fake: Faker) -> list[dict[str, Any]]:
    librarians = []
    for number in range(1, LIBRARIAN_COUNT + 1):
        username = f"syn-lib-{number:04d}"
        first, last = fake.first_name(), fake.last_name()
        librarians.append(
            {
                "username": username,
                "displayName": f"{first} {last}",
                "email": f"{username}@synthetic.lms.local",
                "role": "ROLE_LIBRARIAN",
            }
        )
    return librarians


def build_copies(rng: random.Random, books: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts, weights = list(COPY_COUNT_WEIGHTS), list(COPY_COUNT_WEIGHTS.values())
    copies = []
    number = 1001
    for book in books:
        for _ in range(rng.choices(counts, weights)[0]):
            copies.append({"barcode": f"LMS-COPY-{number}", "isbn13": book["isbn13"], "status": "AVAILABLE"})
            number += 1
    return copies


def assign_profiles(rng: random.Random, members: list[dict[str, Any]]) -> dict[str, str]:
    """Assign a circulation profile to every member (SUSPENDED members get 'SUSPENDED')."""
    profiles = {m["memberId"]: "SUSPENDED" for m in members if m["status"] == "SUSPENDED"}
    active = [m["memberId"] for m in members if m["status"] == "ACTIVE"]
    rng.shuffle(active)
    cursor = 0
    for profile, count in PROFILE_COUNTS.items():
        for member_id in active[cursor : cursor + count]:
            profiles[member_id] = profile
        cursor += count
    assert cursor == len(active), "profile counts must cover all active members"
    return profiles


def build_active_slots(
    rng: random.Random, members: dict[str, dict[str, Any]], profiles: dict[str, str]
) -> list[dict[str, Any]]:
    """Create the active-loan 'slots' (member, scenario, dates) before copies are attached."""
    slots: list[dict[str, Any]] = []
    forced_limit_done = {"STUDENT": False, "ACADEMIC_STAFF": False}
    for member_id in sorted(profiles):
        profile = profiles[member_id]
        if profile not in ("OVERDUE", "DUE_SOON", "ONTIME"):
            continue
        member_type = members[member_id]["memberType"]
        period = LOAN_DAYS[member_type]
        limit = MAX_ACTIVE_LOANS[member_type]
        if profile == "OVERDUE":
            first_k = sample_overdue_active_days(rng)
            ks = [first_k]
            if rng.random() < 0.3:
                ks.append(first_k + rng.randint(0, period))
            for k in ks:
                slots.append({"memberId": member_id, "scenario": "OVERDUE", "dueDate": REFERENCE_DATE - timedelta(days=k), "renewable": False})
            continue
        if profile == "DUE_SOON":
            count = rng.randint(1, min(2, limit))
        else:
            count = rng.randint(1, min(3, limit))
            if not forced_limit_done[member_type]:
                count, forced_limit_done[member_type] = limit, True  # at least one member exactly at the limit
        for _ in range(count):
            if profile == "DUE_SOON":
                days_left = rng.randint(0, DUE_SOON_DAYS)
            else:
                days_left = rng.randint(DUE_SOON_DAYS + 1, period - 1)
            slots.append(
                {
                    "memberId": member_id,
                    "scenario": profile,
                    "dueDate": REFERENCE_DATE + timedelta(days=days_left),
                    "renewable": rng.random() < 0.15,
                }
            )
    return slots


def finalize_slot_as_loan(rng: random.Random, slot: dict[str, Any], members: dict[str, dict[str, Any]], barcode: str, isbn13: str) -> dict[str, Any]:
    member_type = members[slot["memberId"]]["memberType"]
    period = LOAN_DAYS[member_type]
    due = slot["dueDate"]
    renewed = slot["renewable"] and slot["scenario"] != "OVERDUE"
    if renewed:
        checkout = due - timedelta(days=2 * period)
        renewed_on = checkout + timedelta(days=rng.randint(1, period))
    else:
        checkout = due - timedelta(days=period)
        renewed_on = None
    return {
        "memberId": slot["memberId"],
        "copyBarcode": barcode,
        "isbn13": isbn13,
        "checkoutDate": checkout,
        "dueDate": due,
        "returnDate": None,
        "renewalCount": 1 if renewed else 0,
        "renewedOn": renewed_on,
        "scenario": slot["scenario"],
    }


def make_returned_loan(
    rng: random.Random,
    member: dict[str, Any],
    checkout: date,
    limit: date,
    late_days: int | None,
    allow_renewal: bool,
) -> dict[str, Any] | None:
    """Build a returned loan starting at checkout; None if it cannot finish before limit."""
    period = LOAN_DAYS[member["memberType"]]
    renewed_on = None
    renewal_count = 0
    if late_days:
        due = checkout + timedelta(days=period)
        returned = due + timedelta(days=late_days)
    else:
        due = checkout + timedelta(days=period)
        if allow_renewal and rng.random() < 0.10:
            renewal_count = 1
            renewed_on = checkout + timedelta(days=rng.randint(1, period))
            due = checkout + timedelta(days=2 * period)
            returned = renewed_on + timedelta(days=rng.randint(0, (due - renewed_on).days))
            returned = max(returned, checkout + timedelta(days=1))
        else:
            returned = checkout + timedelta(days=rng.randint(1, period))
    if returned > limit or returned <= checkout:
        return None
    return {
        "memberId": member["memberId"],
        "checkoutDate": checkout,
        "dueDate": due,
        "returnDate": returned,
        "renewalCount": renewal_count,
        "renewedOn": renewed_on,
    }


def pick_free_copy(rng: random.Random, all_barcodes: list[str], cal: CopyCalendar, start: date, end: date) -> str | None:
    for _ in range(80):
        candidate = rng.choice(all_barcodes)
        if cal.is_free(candidate, start, end):
            return candidate
    return None


def build_circulation(
    rng: random.Random,
    members_list: list[dict[str, Any]],
    librarians: list[dict[str, Any]],
    copies: list[dict[str, Any]],
) -> dict[str, Any]:
    members = {m["memberId"]: m for m in members_list}
    copy_by_barcode = {c["barcode"]: c for c in copies}
    copies_by_isbn: dict[str, list[str]] = defaultdict(list)
    for copy in copies:
        copies_by_isbn[copy["isbn13"]].append(copy["barcode"])
    isbn_of = {c["barcode"]: c["isbn13"] for c in copies}
    all_barcodes = [c["barcode"] for c in copies]

    # --- special titles (hold queues) -------------------------------------------------
    small_titles = sorted(i for i, bcs in copies_by_isbn.items() if len(bcs) <= 2)
    rng.shuffle(small_titles)
    queue_titles = small_titles[:QUEUE_TITLES]
    ready_titles = small_titles[QUEUE_TITLES : QUEUE_TITLES + READY_TITLES]
    special_titles = set(queue_titles) | set(ready_titles)

    must_loan: list[str] = []
    reserved_copies: dict[str, str] = {}  # ready title -> RESERVED copy barcode
    for isbn in queue_titles:
        must_loan.extend(copies_by_isbn[isbn])
    for isbn in ready_titles:
        first, *others = copies_by_isbn[isbn]
        reserved_copies[isbn] = first
        must_loan.extend(others)

    ordinary = [c for c in all_barcodes if isbn_of[c] not in special_titles]
    shuffled_ordinary = ordinary[:]
    rng.shuffle(shuffled_ordinary)
    maintenance = set(shuffled_ordinary[:MAINTENANCE_COPIES])
    lost = set(shuffled_ordinary[MAINTENANCE_COPIES : MAINTENANCE_COPIES + LOST_COPIES])
    loanable_ordinary = shuffled_ordinary[MAINTENANCE_COPIES + LOST_COPIES :]

    # --- member profiles and active-loan slots -----------------------------------------
    profiles = assign_profiles(rng, members_list)
    slots = build_active_slots(rng, members, profiles)
    assert len(slots) >= len(must_loan), "not enough active-loan slots for the hold-queue titles"
    rng.shuffle(slots)

    active_copy_list = must_loan + loanable_ordinary[: len(slots) - len(must_loan)]
    held_isbns: dict[str, set[str]] = defaultdict(set)
    unassigned = list(range(len(slots)))
    active_loans: list[dict[str, Any]] = []
    cal = CopyCalendar()
    for barcode in active_copy_list:
        isbn = isbn_of[barcode]
        index = next(i for i in unassigned if isbn not in held_isbns[slots[i]["memberId"]])
        unassigned.remove(index)
        slot = slots[index]
        if barcode in must_loan:
            slot["renewable"] = False
        held_isbns[slot["memberId"]].add(isbn)
        loan = finalize_slot_as_loan(rng, slot, members, barcode, isbn)
        active_loans.append(loan)
        cal.book(barcode, loan["checkoutDate"], FAR_FUTURE)

    first_active_checkout: dict[str, date] = {}
    for loan in active_loans:
        current = first_active_checkout.get(loan["memberId"])
        if current is None or loan["checkoutDate"] < current:
            first_active_checkout[loan["memberId"]] = loan["checkoutDate"]

    # --- history -----------------------------------------------------------------------
    history_members = sorted(m for m, p in profiles.items() if p == "HISTORY")
    terminal_active = set(rng.sample(history_members, TERMINAL_UNPAID_ACTIVE_MEMBERS))
    suspended_ids = sorted(m for m, p in profiles.items() if p == "SUSPENDED")
    terminal_suspended = set(rng.sample(suspended_ids, TERMINAL_UNPAID_SUSPENDED))
    terminal_members = terminal_active | terminal_suspended

    history_loans: list[dict[str, Any]] = []
    fines: list[dict[str, Any]] = []
    blocked_until: dict[str, date] = defaultdict(lambda: HISTORY_START)
    history_counts = [0, 1, 2, 3, 4]
    history_weights = [15, 30, 30, 15, 10]

    def attach_loan_and_fine(loan: dict[str, Any], status: str | None) -> bool:
        copy = pick_free_copy(rng, all_barcodes, cal, loan["checkoutDate"], loan["returnDate"])
        if copy is None:
            return False
        cal.book(copy, loan["checkoutDate"], loan["returnDate"])
        loan["copyBarcode"], loan["isbn13"] = copy, isbn_of[copy]
        history_loans.append(loan)
        late = overdue_days(loan["dueDate"], loan["returnDate"])
        settled = loan["returnDate"]
        if late > 0:
            fine_status = status or ("PAID" if rng.random() < 0.7 else "WAIVED")
            settled_on = None if fine_status == "UNPAID" else min(loan["returnDate"] + timedelta(days=rng.randint(0, 14)), loan["limit"])
            fines.append(
                {
                    "memberId": loan["memberId"],
                    "loan": loan,
                    "overdueDays": late,
                    "amount": compute_fine(late),
                    "status": fine_status,
                    "assessedOn": loan["returnDate"],
                    "settledOn": settled_on,
                    "settledBy": None if settled_on is None else rng.choice(librarians)["username"],
                }
            )
            settled = settled_on or loan["returnDate"]
        blocked_until[loan["memberId"]] = max(blocked_until[loan["memberId"]], settled)
        return True

    for member_id in sorted(profiles):
        member = members[member_id]
        profile = profiles[member_id]
        if profile in ("OVERDUE", "DUE_SOON", "ONTIME"):
            limit = first_active_checkout[member_id] - timedelta(days=1)
        elif profile == "SUSPENDED":
            limit = REFERENCE_DATE - timedelta(days=20)
        else:
            limit = REFERENCE_DATE - timedelta(days=1)
        wanted = rng.choices(history_counts, history_weights)[0]
        terminal = member_id in terminal_members
        if terminal:
            wanted = max(wanted, 1)
        earlier_limit = limit
        if terminal:
            period = LOAN_DAYS[member["memberType"]]
            late = min(sample_late_days(rng), 60)
            returned = limit - timedelta(days=rng.randint(0, 20))
            checkout = returned - timedelta(days=late + period)
            final_loan = make_returned_loan(rng, member, checkout, limit, late, False)
            if final_loan is not None:
                final_loan["limit"] = limit
                if attach_loan_and_fine(final_loan, "UNPAID"):
                    earlier_limit = checkout - timedelta(days=1)
                    wanted -= 1
        cursor = HISTORY_START + timedelta(days=rng.randint(0, 120))
        for _ in range(wanted):
            late_days = sample_late_days(rng) if rng.random() < 0.25 else None
            loan = make_returned_loan(rng, member, cursor, earlier_limit, late_days, True)
            if loan is None:
                break
            loan["limit"] = earlier_limit
            if not attach_loan_and_fine(loan, None):
                break
            settled = blocked_until[member_id]
            cursor = max(loan["returnDate"], settled) + timedelta(days=rng.randint(3, 60))

    # --- fines for active overdue loans -----------------------------------------------
    for loan in active_loans:
        late = overdue_days(loan["dueDate"], REFERENCE_DATE)
        if late > 0:
            fines.append(
                {
                    "memberId": loan["memberId"],
                    "loan": loan,
                    "overdueDays": late,
                    "amount": compute_fine(late),
                    "status": "UNPAID",
                    "assessedOn": REFERENCE_DATE,
                    "settledOn": None,
                    "settledBy": None,
                }
            )

    # --- copy statuses -------------------------------------------------------------------
    for barcode in maintenance:
        copy_by_barcode[barcode]["status"] = "MAINTENANCE"
    for barcode in lost:
        copy_by_barcode[barcode]["status"] = "LOST"
    for barcode in reserved_copies.values():
        copy_by_barcode[barcode]["status"] = "RESERVED"
    for loan in active_loans:
        copy_by_barcode[loan["copyBarcode"]]["status"] = "LOANED"

    # --- reservations ----------------------------------------------------------------------
    eligible_for_holds = sorted(m for m, p in profiles.items() if p in ("DUE_SOON", "ONTIME", "HISTORY") and m not in terminal_members)
    active_by_isbn: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for loan in active_loans:
        active_by_isbn[loan["isbn13"]].append(loan)
    reservations: list[dict[str, Any]] = []
    holds_per_member: dict[str, int] = defaultdict(int)

    def build_queue(isbn: str, ready_copy: str | None) -> None:
        holders = {loan["memberId"] for loan in active_by_isbn[isbn]}
        pool = [m for m in eligible_for_holds if m not in holders and holds_per_member[m] < 2]
        size = rng.choice([1, 2, 2, 3])
        chosen = rng.sample(pool, size)
        lower = max((loan["checkoutDate"] for loan in active_by_isbn[isbn]), default=HISTORY_START)
        created = lower
        for position, member_id in enumerate(chosen, start=1):
            created = min(max(created + timedelta(days=rng.randint(0, 2)), blocked_until[member_id]), REFERENCE_DATE)
            reservations.append(
                {
                    "isbn13": isbn,
                    "memberId": member_id,
                    "queuePosition": position,
                    "status": "READY" if (ready_copy and position == 1) else "WAITING",
                    "createdOn": created,
                    "readyCopyBarcode": ready_copy if (ready_copy and position == 1) else None,
                }
            )
            holds_per_member[member_id] += 1

    for isbn in queue_titles:
        build_queue(isbn, None)
    for isbn in ready_titles:
        build_queue(isbn, reserved_copies[isbn])

    # --- finalize ids and registration dates ------------------------------------------------
    all_loans = active_loans + history_loans
    all_loans.sort(key=lambda l: (l["checkoutDate"], l["memberId"], l["copyBarcode"]))
    for number, loan in enumerate(all_loans, start=1):
        loan["loanId"] = f"LOAN-{number:04d}"

    earliest_checkout: dict[str, date] = {}
    for loan in all_loans:
        earliest_checkout.setdefault(loan["memberId"], loan["checkoutDate"])
    for member in members_list:
        first = earliest_checkout.get(member["memberId"])
        if first is not None and member["registeredOn"] >= first:
            member["registeredOn"] = first - timedelta(days=rng.randint(1, 60))

    fines.sort(key=lambda f: (f["assessedOn"], f["loan"]["loanId"]))
    for number, fine in enumerate(fines, start=1):
        fine["fineId"] = f"FINE-{number:04d}"

    reservations.sort(key=lambda r: (r["isbn13"], r["queuePosition"]))
    for number, reservation in enumerate(reservations, start=1):
        reservation["reservationId"] = f"RES-{number:04d}"

    return {"loans": all_loans, "fines": fines, "reservations": reservations}


def serialize(members: list[dict[str, Any]], librarians: list[dict[str, Any]], copies: list[dict[str, Any]], circulation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    members_out = [
        {
            "memberId": m["memberId"],
            "firstName": m["firstName"],
            "lastName": m["lastName"],
            "email": m["email"],
            "memberType": m["memberType"],
            "status": m["status"],
            "department": m["department"],
            "registeredOn": iso(m["registeredOn"]),
        }
        for m in members
    ]
    loans_out = [
        {
            "loanId": l["loanId"],
            "memberId": l["memberId"],
            "copyBarcode": l["copyBarcode"],
            "checkoutDate": iso(l["checkoutDate"]),
            "dueDate": iso(l["dueDate"]),
            "returnDate": iso(l["returnDate"]),
            "status": "ACTIVE" if l["returnDate"] is None else "RETURNED",
            "renewalCount": l["renewalCount"],
            "renewedOn": iso(l["renewedOn"]),
        }
        for l in circulation["loans"]
    ]
    fines_out = [
        {
            "fineId": f["fineId"],
            "loanId": f["loan"]["loanId"],
            "memberId": f["memberId"],
            "overdueDays": f["overdueDays"],
            "amount": f"{f['amount']:.2f}",
            "currency": CURRENCY,
            "status": f["status"],
            "assessedOn": iso(f["assessedOn"]),
            "settledOn": iso(f["settledOn"]),
            "settledBy": f["settledBy"],
        }
        for f in circulation["fines"]
    ]
    reservations_out = [
        {
            "reservationId": r["reservationId"],
            "isbn13": r["isbn13"],
            "memberId": r["memberId"],
            "queuePosition": r["queuePosition"],
            "status": r["status"],
            "createdOn": iso(r["createdOn"]),
            "readyCopyBarcode": r["readyCopyBarcode"],
        }
        for r in circulation["reservations"]
    ]
    return {
        "members.json": members_out,
        "librarians.json": librarians,
        "copies.json": copies,
        "loans.json": loans_out,
        "fines.json": fines_out,
        "reservations.json": reservations_out,
    }


def generate(books: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Generate all synthetic datasets (pure function of the book list)."""
    rng = random.Random(RANDOM_SEED)
    fake = Faker("tr_TR")
    fake.seed_instance(RANDOM_SEED)
    members = build_members(rng, fake)
    librarians = build_librarians(fake)
    copies = build_copies(rng, books)
    circulation = build_circulation(rng, members, librarians, copies)
    return serialize(members, librarians, copies, circulation)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic LMS seed data.")
    parser.add_argument("--books", type=Path, default=BOOKS_FILE, help="input books-openlibrary.json")
    parser.add_argument("--output-dir", type=Path, default=SEED_DIR, help="directory for the generated JSON files")
    args = parser.parse_args()

    if not args.books.exists():
        print(f"ERROR: {args.books} not found. Run fetch_books.py first.", file=sys.stderr)
        return 2
    datasets = generate(read_json(args.books))
    for name, rows in datasets.items():
        write_json(args.output_dir / name, rows)
        print(f"{name}: {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
