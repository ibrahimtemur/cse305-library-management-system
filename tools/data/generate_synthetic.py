# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Reproducible generator of 100% synthetic members, librarians, copies, loans, fines, and reservations for the LMS seed data (feature M6).
"""Generate synthetic operational seed data (seed v2 — confirmed ADU rules).

Everything produced here is fictional. No real person, ADU student, staff member, or
institutional identifier is used. The generator only reads ``books-openlibrary.json``
and is fully deterministic (fixed ``RANDOM_SEED``, fixed ``REFERENCE_DATE``, pinned Faker).

Business rules follow ``docs/02-inception/BUSINESS_RULES.md`` (BR-001..BR-018) and field/enum
names follow ``docs/02-inception/DOMAIN_GLOSSARY.md``:
  * BR-002 borrowing quotas: ACADEMIC_STAFF = 7, ADMINISTRATIVE_STAFF = 3, STUDENT = 3
  * BR-003 loan duration: 30 calendar days for all three member types
  * BR-004 / BR-005 renewals: at most 1 renewal (+30 days), never when overdue or reserved
  * BR-006 post-renewal cooldown: 30 calendar days after returnDate before the same member
    may borrow the same title again (does not block reservations)
  * BR-007..BR-010 overdue fines: 0.25 TRY/day with no cap
  * BR-011 borrowing block on overdue active loan, unpaid fine, or SUSPENDED status
  * BR-012 / BR-013 FIFO title holds & 3-day pickup window (readyOn, holdUntil) for READY holds
  * BR-014 non-circulating reference works (referenceOnly = true) are never loaned or reserved
  * BR-015 / BR-017 LOST copies correspond to status="LOST" loans (returnDate=null) with
    lostReportedOn within the active 30-day replacement window and fine frozen on lostReportedOn

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
    HOLD_PICKUP_DAYS,
    LOAN_DAYS,
    LOST_REPLACEMENT_DAYS,
    MAX_ACTIVE_LOANS,
    RANDOM_SEED,
    REFERENCE_DATE,
    RENEWAL_COOLDOWN_DAYS,
    SEED_DIR,
    compute_fine,
    is_reference_only_book,
    overdue_days,
    read_json,
    write_json,
)

STUDENT_COUNT = 40
ACADEMIC_STAFF_COUNT = 10
ADMINISTRATIVE_STAFF_COUNT = 10
LIBRARIAN_COUNT = 3

# Raw generation counts used to preserve exact Faker/RNG alignment for persona identities and copies.
_RAW_STUDENT_DRAWS = 44
_RAW_STAFF_DRAWS = 16
_SUSPENDED_RAW_STUDENTS = 3
_SUSPENDED_RAW_STAFF = 1

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

# Profile counts for non-suspended active members (sum = 55).
PROFILE_COUNTS = {"OVERDUE": 12, "DUE_SOON": 9, "ONTIME": 13, "HISTORY": 21}
TERMINAL_UNPAID_ACTIVE_MEMBERS = 4  # HISTORY-profile members blocked by an unpaid fine on a RETURNED loan.
TERMINAL_UNPAID_SUSPENDED = 2
LOST_COPIES = 5  # LOST copies with status="LOST" loans and lostReportedOn within 30 days of REFERENCE_DATE.
MAINTENANCE_COPIES = 15
QUEUE_TITLES = 9
READY_TITLES = 3
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


class CooldownTracker:
    """Tracks 30-day post-renewal re-borrowing cooldowns per (memberId, isbn13) (BR-006)."""

    def __init__(self) -> None:
        self._renewed_returns: dict[tuple[str, str], list[date]] = defaultdict(list)

    def record_return(self, member_id: str, isbn13: str, return_date: date, renewal_count: int) -> None:
        if renewal_count >= 1:
            self._renewed_returns[(member_id, isbn13)].append(return_date)

    def can_checkout(self, member_id: str, isbn13: str, checkout_date: date) -> bool:
        for ret in self._renewed_returns.get((member_id, isbn13), ()):
            if ret <= checkout_date < ret + timedelta(days=RENEWAL_COOLDOWN_DAYS):
                return False
        return True


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
    """Build 40 STUDENT, 10 ACADEMIC_STAFF, and 10 ADMINISTRATIVE_STAFF members.

    Preserves the exact RNG and Faker call sequence of the 60-member draw so that
    persona records (SYN-STU-0001..0040, SYN-STF-0001..0010, syn-lib-0001..0003)
    and copy barcodes remain stable.
    """
    raw_draws: list[dict[str, Any]] = []
    for i in range(_RAW_STUDENT_DRAWS + _RAW_STAFF_DRAWS):
        is_raw_stu = i < _RAW_STUDENT_DRAWS
        registered = (
            date(2023, 9, 1) + timedelta(days=rng.randint(0, 800))
            if is_raw_stu
            else date(2018, 9, 1) + timedelta(days=rng.randint(0, 2000))
        )
        raw_draws.append(
            {
                "firstName": fake.first_name(),
                "lastName": fake.last_name(),
                "status": "ACTIVE",
                "department": rng.choice(DEPARTMENTS),
                "registeredOn": registered,
            }
        )
    for item in rng.sample(raw_draws[:_RAW_STUDENT_DRAWS], _SUSPENDED_RAW_STUDENTS) + rng.sample(
        raw_draws[_RAW_STUDENT_DRAWS:], _SUSPENDED_RAW_STAFF
    ):
        item["status"] = "SUSPENDED"
    # Ensure ACADEMIC_STAFF also has 1 SUSPENDED member (index 53 -> SYN-STF-0010).
    raw_draws[53]["status"] = "SUSPENDED"

    stu_draws = raw_draws[:STUDENT_COUNT]  # indices 0..39 -> SYN-STU-0001..0040
    stf_draws = raw_draws[44 : 44 + ACADEMIC_STAFF_COUNT]  # indices 44..53 -> SYN-STF-0001..0010
    # Remaining 10 draws (indices 40..43 and 54..59) -> SYN-ADM-0001..0010, with index 42 first (Business Administration).
    adm_indices = [42, 40, 41, 43, 54, 55, 56, 57, 58, 59]
    adm_draws = [raw_draws[idx] for idx in adm_indices]

    members: list[dict[str, Any]] = []
    for prefix, member_type, group in (
        ("SYN-STU", "STUDENT", stu_draws),
        ("SYN-STF", "ACADEMIC_STAFF", stf_draws),
        ("SYN-ADM", "ADMINISTRATIVE_STAFF", adm_draws),
    ):
        for number, base in enumerate(group, start=1):
            member_id = f"{prefix}-{number:04d}"
            members.append(
                {
                    "memberId": member_id,
                    "firstName": base["firstName"],
                    "lastName": base["lastName"],
                    "email": f"{member_id.lower()}@synthetic.lms.local",
                    "memberType": member_type,
                    "status": base["status"],
                    "department": base["department"],
                    "registeredOn": base["registeredOn"],
                }
            )
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
    assert cursor == len(active), f"profile counts ({cursor}) must cover all active members ({len(active)})"

    # Pin key persona profiles so documented persona scenarios remain consistent:
    # SYN-STU-0001 (Tutkucan Ergül) -> OVERDUE active loan
    # Ensure documented hold-queue members are never placed in OVERDUE.
    hold_pinned_members = {
        "SYN-STF-0002",
        "SYN-STU-0034",
        "SYN-STU-0027",
        "SYN-STU-0032",
        "SYN-STU-0012",
        "SYN-STU-0014",
        "SYN-STF-0003",
        "SYN-STU-0016",
        "SYN-STU-0003",
        "SYN-STU-0024",
    }
    member_by_id = {m["memberId"]: m for m in members}
    if profiles.get("SYN-STU-0001") != "OVERDUE":
        swap_id = next(mid for mid, p in profiles.items() if p == "OVERDUE" and mid != "SYN-STU-0001")
        profiles[swap_id], profiles["SYN-STU-0001"] = profiles["SYN-STU-0001"], "OVERDUE"

    for hmid in sorted(hold_pinned_members):
        if profiles.get(hmid) == "OVERDUE":
            swap_id = next(
                mid
                for mid in active
                if profiles[mid] in ("HISTORY", "DUE_SOON") and mid not in hold_pinned_members and mid != "SYN-STU-0001"
            )
            profiles[hmid], profiles[swap_id] = profiles[swap_id], "OVERDUE"

    for mtype in ("STUDENT", "ACADEMIC_STAFF", "ADMINISTRATIVE_STAFF"):
        if not any(profiles[mid] == "ONTIME" and member_by_id[mid]["memberType"] == mtype for mid in active):
            candidate = next(mid for mid in active if member_by_id[mid]["memberType"] == mtype and profiles[mid] == "HISTORY")
            swap_ontime = next(
                mid
                for mid in active
                if profiles[mid] == "ONTIME"
                and sum(1 for other in active if profiles[other] == "ONTIME" and member_by_id[other]["memberType"] == member_by_id[mid]["memberType"]) > 1
            )
            profiles[candidate], profiles[swap_ontime] = "ONTIME", "HISTORY"
    return profiles


def build_active_slots(
    rng: random.Random, members: dict[str, dict[str, Any]], profiles: dict[str, str]
) -> list[dict[str, Any]]:
    """Create the active-loan 'slots' (member, scenario, dates) before copies are attached."""
    slots: list[dict[str, Any]] = []
    forced_limit_done = {"STUDENT": False, "ACADEMIC_STAFF": False, "ADMINISTRATIVE_STAFF": False}
    for member_id in sorted(profiles):
        profile = profiles[member_id]
        if profile not in ("OVERDUE", "DUE_SOON", "ONTIME"):
            continue
        member_type = members[member_id]["memberType"]
        period = LOAN_DAYS[member_type]
        limit = MAX_ACTIVE_LOANS[member_type]
        if profile == "OVERDUE":
            first_k = 53 if member_id == "SYN-STU-0001" else sample_overdue_active_days(rng)
            ks = [first_k]
            if member_id != "SYN-STU-0001" and rng.random() < 0.3:
                ks.append(first_k + rng.randint(1, period))
            for k in ks:
                slots.append(
                    {
                        "memberId": member_id,
                        "scenario": "OVERDUE",
                        "dueDate": REFERENCE_DATE - timedelta(days=k),
                        "renewable": False,
                    }
                )
            continue
        if profile == "DUE_SOON":
            count = rng.randint(1, min(2, limit))
        else:
            count = rng.randint(1, min(3, limit))
            if not forced_limit_done[member_type]:
                count, forced_limit_done[member_type] = limit, True  # at least one member per type at exact limit
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


def finalize_slot_as_loan(
    rng: random.Random, slot: dict[str, Any], members: dict[str, dict[str, Any]], barcode: str, isbn13: str
) -> dict[str, Any]:
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
        "lostReportedOn": None,
        "status": "ACTIVE",
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
    force_renewal: bool = False,
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
        if allow_renewal and (force_renewal or rng.random() < 0.12):
            renewal_count = 1
            renewed_on = checkout + timedelta(days=rng.randint(1, period))
            due = checkout + timedelta(days=2 * period)
            returned = renewed_on + timedelta(days=rng.randint(1, (due - renewed_on).days))
        else:
            returned = checkout + timedelta(days=rng.randint(1, period))
    if returned > limit or returned <= checkout:
        return None
    return {
        "memberId": member["memberId"],
        "checkoutDate": checkout,
        "dueDate": due,
        "returnDate": returned,
        "lostReportedOn": None,
        "status": "RETURNED",
        "renewalCount": renewal_count,
        "renewedOn": renewed_on,
    }


def pick_free_copy(
    rng: random.Random,
    candidate_barcodes: list[str],
    isbn_of: dict[str, str],
    cal: CopyCalendar,
    cooldowns: CooldownTracker,
    member_id: str,
    start: date,
    end: date,
) -> str | None:
    for _ in range(100):
        candidate = rng.choice(candidate_barcodes)
        isbn = isbn_of[candidate]
        if cal.is_free(candidate, start, end) and cooldowns.can_checkout(member_id, isbn, start):
            return candidate
    return None


def build_circulation(
    rng: random.Random,
    books: list[dict[str, Any]],
    members_list: list[dict[str, Any]],
    librarians: list[dict[str, Any]],
    copies: list[dict[str, Any]],
) -> dict[str, Any]:
    members = {m["memberId"]: m for m in members_list}
    copy_by_barcode = {c["barcode"]: c for c in copies}
    reference_isbns = {b["isbn13"] for b in books if b.get("referenceOnly")}

    copies_by_isbn: dict[str, list[str]] = defaultdict(list)
    for copy in copies:
        if copy["isbn13"] not in reference_isbns:
            copies_by_isbn[copy["isbn13"]].append(copy["barcode"])
    isbn_of = {c["barcode"]: c["isbn13"] for c in copies}
    circulating_barcodes = [c["barcode"] for c in copies if c["isbn13"] not in reference_isbns]

    # --- special titles (hold queues on non-reference books) ---------------------------
    small_titles = sorted(i for i, bcs in copies_by_isbn.items() if len(bcs) <= 2)
    rng.shuffle(small_titles)

    # Keep documented hold-queue ISBNs in queue_titles / ready_titles for persona stability.
    pinned_queues: dict[str, list[str]] = {
        "9780130960160": ["SYN-STF-0002", "SYN-STU-0034"],
        "9780132128810": ["SYN-STU-0027"],
        "9780321573513": ["SYN-STU-0032", "SYN-STU-0012", "SYN-STU-0014"],
        "9780345309884": ["SYN-STF-0003", "SYN-STU-0016"],
        "9780345451323": ["SYN-STU-0003", "SYN-STU-0024"],
    }
    pinned_queue = ["9780130960160", "9780132128810", "9780321573513", "9780345309884"]
    pinned_ready = ["9780345451323"]
    remaining_small = [i for i in small_titles if i > "9780345451323" and i not in pinned_queue and i not in pinned_ready]
    queue_titles = sorted(pinned_queue + remaining_small[: QUEUE_TITLES - len(pinned_queue)])
    ready_pool = [i for i in remaining_small[QUEUE_TITLES - len(pinned_queue) :] if len(copies_by_isbn[i]) == 2]
    ready_titles = sorted(pinned_ready + ready_pool[: READY_TITLES - len(pinned_ready)])
    special_titles = set(queue_titles) | set(ready_titles)

    must_loan: list[str] = []
    reserved_copies: dict[str, str] = {}  # ready title -> RESERVED copy barcode
    for isbn in queue_titles:
        must_loan.extend(copies_by_isbn[isbn])
    for isbn in ready_titles:
        first, *others = copies_by_isbn[isbn]
        reserved_copies[isbn] = first
        must_loan.extend(others)

    ordinary = [c for c in circulating_barcodes if isbn_of[c] not in special_titles]
    shuffled_ordinary = ordinary[:]
    rng.shuffle(shuffled_ordinary)
    # Keep LMS-COPY-2119 in loanable_ordinary so SYN-STU-0001's documented active overdue loan uses it.
    if "LMS-COPY-2119" in shuffled_ordinary[: MAINTENANCE_COPIES + LOST_COPIES]:
        idx_2119 = shuffled_ordinary.index("LMS-COPY-2119")
        shuffled_ordinary[idx_2119], shuffled_ordinary[MAINTENANCE_COPIES + LOST_COPIES + 5] = (
            shuffled_ordinary[MAINTENANCE_COPIES + LOST_COPIES + 5],
            shuffled_ordinary[idx_2119],
        )
    maintenance = set(shuffled_ordinary[:MAINTENANCE_COPIES])
    lost_barcodes = shuffled_ordinary[MAINTENANCE_COPIES : MAINTENANCE_COPIES + LOST_COPIES]
    lost = set(lost_barcodes)
    loanable_ordinary = shuffled_ordinary[MAINTENANCE_COPIES + LOST_COPIES :]

    # --- member profiles and active-loan slots -----------------------------------------
    profiles = assign_profiles(rng, members_list)
    slots = build_active_slots(rng, members, profiles)
    assert len(slots) >= len(must_loan), "not enough active-loan slots for the hold-queue titles"
    rng.shuffle(slots)

    # Pin LMS-COPY-2119 to SYN-STU-0001's overdue active slot for persona/use-case stability.
    stu1_slot_idx = next(i for i, s in enumerate(slots) if s["memberId"] == "SYN-STU-0001")
    slots[0], slots[stu1_slot_idx] = slots[stu1_slot_idx], slots[0]
    if "LMS-COPY-2119" in loanable_ordinary:
        loanable_ordinary.remove("LMS-COPY-2119")
    active_copy_list = ["LMS-COPY-2119"] + must_loan + loanable_ordinary[: len(slots) - 1 - len(must_loan)]

    held_isbns: dict[str, set[str]] = defaultdict(set)
    unassigned = list(range(len(slots)))
    active_loans: list[dict[str, Any]] = []
    cal = CopyCalendar()
    cooldowns = CooldownTracker()

    for barcode in active_copy_list:
        isbn = isbn_of[barcode]
        disallowed_holders = set(pinned_queues.get(isbn, ()))
        index = next(
            i
            for i in unassigned
            if isbn not in held_isbns[slots[i]["memberId"]] and slots[i]["memberId"] not in disallowed_holders
        )
        unassigned.remove(index)
        slot = slots[index]
        if barcode in must_loan or isbn in special_titles:
            slot["renewable"] = False
        held_isbns[slot["memberId"]].add(isbn)
        loan = finalize_slot_as_loan(rng, slot, members, barcode, isbn)
        active_loans.append(loan)
        cal.book(barcode, loan["checkoutDate"], FAR_FUTURE)

    # Reserve calendar intervals for LOST and RESERVED copies so history loans do not collide after loss/hold.
    for barcode in reserved_copies.values():
        cal.book(barcode, REFERENCE_DATE - timedelta(days=10), FAR_FUTURE)

    first_active_checkout: dict[str, date] = {}
    for loan in active_loans:
        current = first_active_checkout.get(loan["memberId"])
        if current is None or loan["checkoutDate"] < current:
            first_active_checkout[loan["memberId"]] = loan["checkoutDate"]

    # --- LOST copy loans (status="LOST", returnDate=null, lostReportedOn within last 30 days) ---
    history_members = sorted(m for m, p in profiles.items() if p == "HISTORY")
    suspended_ids = sorted(m for m, p in profiles.items() if p == "SUSPENDED")

    # Select 5 dedicated members for LOST loans (from HISTORY/SUSPENDED) so their active replacement
    # window and frozen fine on lostReportedOn block any subsequent checkouts cleanly.
    protected_members = {
        "SYN-STU-0003",
        "SYN-STU-0012",
        "SYN-STU-0014",
        "SYN-STU-0016",
        "SYN-STU-0024",
        "SYN-STU-0026",
        "SYN-STU-0027",
        "SYN-STU-0032",
        "SYN-STU-0034",
        "SYN-STU-0038",
        "SYN-STU-0040",
        "SYN-STF-0001",
        "SYN-STF-0002",
        "SYN-STF-0003",
    }
    lost_member_pool = [m for m in history_members if m not in protected_members]
    lost_holders = lost_member_pool[:LOST_COPIES]

    remaining_history = [m for m in history_members if m not in lost_holders and m not in protected_members]
    pinned_unpaid_suspended = ["SYN-STU-0025"] if "SYN-STU-0025" in suspended_ids else []
    other_suspended = [m for m in suspended_ids if m not in pinned_unpaid_suspended]
    terminal_active = set(rng.sample(remaining_history, TERMINAL_UNPAID_ACTIVE_MEMBERS))
    terminal_suspended = set(pinned_unpaid_suspended + rng.sample(other_suspended, TERMINAL_UNPAID_SUSPENDED - len(pinned_unpaid_suspended)))
    terminal_members = terminal_active | terminal_suspended

    history_loans: list[dict[str, Any]] = []
    lost_loans: list[dict[str, Any]] = []
    fines: list[dict[str, Any]] = []
    blocked_until: dict[str, date] = defaultdict(lambda: HISTORY_START)

    # Create the 5 LOST loans with REFERENCE_DATE - 30 < lostReportedOn <= REFERENCE_DATE and lostReportedOn > dueDate.
    lost_checkout_cap: dict[str, date] = {}
    for idx, (barcode, member_id) in enumerate(zip(lost_barcodes, lost_holders)):
        period = LOAN_DAYS[members[member_id]["memberType"]]
        days_since_reported = rng.randint(2, LOST_REPLACEMENT_DAYS - 2)  # 2..28 days ago (< 30 days)
        lost_reported_on = REFERENCE_DATE - timedelta(days=days_since_reported)
        overdue_at_report = rng.randint(4, 18)
        due_date = lost_reported_on - timedelta(days=overdue_at_report)
        checkout_date = due_date - timedelta(days=period)
        cal.book(barcode, checkout_date, FAR_FUTURE)
        lost_loan = {
            "memberId": member_id,
            "copyBarcode": barcode,
            "isbn13": isbn_of[barcode],
            "checkoutDate": checkout_date,
            "dueDate": due_date,
            "returnDate": None,
            "lostReportedOn": lost_reported_on,
            "status": "LOST",
            "renewalCount": 0,
            "renewedOn": None,
        }
        lost_loans.append(lost_loan)
        fines.append(
            {
                "memberId": member_id,
                "loan": lost_loan,
                "overdueDays": overdue_at_report,
                "amount": compute_fine(overdue_at_report),
                "status": "UNPAID",
                "assessedOn": lost_reported_on,
                "settledOn": None,
                "settledBy": None,
            }
        )
        lost_checkout_cap[member_id] = checkout_date - timedelta(days=1)
        blocked_until[member_id] = FAR_FUTURE

    # --- historical RETURNED loans -----------------------------------------------------
    history_Only_barcodes = [c for c in circulating_barcodes if c not in lost and isbn_of[c] not in special_titles]
    history_counts = [0, 1, 2, 3, 4]
    history_weights = [15, 30, 30, 15, 10]

    def attach_loan_and_fine(
        loan: dict[str, Any],
        status: str | None,
        forced_barcode: str | None = None,
        forced_librarian: str | None = None,
    ) -> bool:
        if forced_barcode is not None:
            if not (
                cal.is_free(forced_barcode, loan["checkoutDate"], loan["returnDate"])
                and cooldowns.can_checkout(loan["memberId"], isbn_of[forced_barcode], loan["checkoutDate"])
            ):
                return False
            copy = forced_barcode
        else:
            copy = pick_free_copy(
                rng,
                history_Only_barcodes,
                isbn_of,
                cal,
                cooldowns,
                loan["memberId"],
                loan["checkoutDate"],
                loan["returnDate"],
            )
        if copy is None:
            return False
        cal.book(copy, loan["checkoutDate"], loan["returnDate"])
        loan["copyBarcode"], loan["isbn13"] = copy, isbn_of[copy]
        cooldowns.record_return(loan["memberId"], loan["isbn13"], loan["returnDate"], loan["renewalCount"])
        history_loans.append(loan)
        late = overdue_days(loan["dueDate"], loan["returnDate"])
        settled = loan["returnDate"]
        if late > 0:
            fine_status = status or ("PAID" if rng.random() < 0.7 else "WAIVED")
            settled_on = (
                None
                if fine_status == "UNPAID"
                else min(loan["returnDate"] + timedelta(days=rng.randint(0, 14)), loan["limit"])
            )
            settled_by = (
                None
                if settled_on is None
                else (forced_librarian or rng.choice(librarians)["username"])
            )
            fines.append(
                {
                    "memberId": loan["memberId"],
                    "loan": loan,
                    "overdueDays": late,
                    "amount": compute_fine(late),
                    "status": fine_status,
                    "assessedOn": loan["returnDate"],
                    "settledOn": settled_on,
                    "settledBy": settled_by,
                }
            )
            settled = settled_on or FAR_FUTURE
        blocked_until[loan["memberId"]] = max(blocked_until[loan["memberId"]], settled)
        return True

    # Pin LOAN-0001 (SYN-STU-0026 on LMS-COPY-1758, checkout 2025-12-28) for glossary/use-case stability.
    loan1 = {
        "memberId": "SYN-STU-0026",
        "checkoutDate": date(2025, 12, 28),
        "dueDate": date(2026, 1, 27),
        "returnDate": date(2025, 12, 30),
        "lostReportedOn": None,
        "status": "RETURNED",
        "renewalCount": 0,
        "renewedOn": None,
        "limit": date(2026, 8, 1),
    }
    attach_loan_and_fine(loan1, None, forced_barcode="LMS-COPY-1758")

    # Pin an explicit post-renewal re-borrowing pair after the >= 30-day cooldown (BR-006):
    # SYN-STF-0001 borrows & renews a book, returns it, waits >= 30 days, and borrows another copy of the same title.
    cooldown_demo_barcode = next(
        b for b in history_Only_barcodes if b != "LMS-COPY-1758" and cal.is_free(b, date(2026, 1, 5), date(2026, 6, 1))
    )
    rc_loan_1 = {
        "memberId": "SYN-STF-0001",
        "checkoutDate": date(2026, 1, 10),
        "dueDate": date(2026, 3, 11),
        "returnDate": date(2026, 2, 20),
        "lostReportedOn": None,
        "status": "RETURNED",
        "renewalCount": 1,
        "renewedOn": date(2026, 2, 5),
        "limit": date(2026, 8, 1),
    }
    attach_loan_and_fine(rc_loan_1, None, forced_barcode=cooldown_demo_barcode)
    rc_loan_2 = {
        "memberId": "SYN-STF-0001",
        "checkoutDate": date(2026, 3, 25),  # 33 days after 2026-02-20 (>= 30 days cooldown)
        "dueDate": date(2026, 4, 24),
        "returnDate": date(2026, 4, 15),
        "lostReportedOn": None,
        "status": "RETURNED",
        "renewalCount": 0,
        "renewedOn": None,
        "limit": date(2026, 8, 1),
    }
    attach_loan_and_fine(rc_loan_2, None, forced_barcode=cooldown_demo_barcode)

    for member_id in sorted(profiles):
        member = members[member_id]
        profile = profiles[member_id]
        if member_id in lost_checkout_cap:
            limit = lost_checkout_cap[member_id]
        elif profile in ("OVERDUE", "DUE_SOON", "ONTIME"):
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
            if checkout > blocked_until[member_id]:
                final_loan = make_returned_loan(rng, member, checkout, limit, late, False)
                if final_loan is not None:
                    final_loan["limit"] = limit
                    if attach_loan_and_fine(final_loan, "UNPAID"):
                        earlier_limit = checkout - timedelta(days=1)
                        wanted -= 1

        cursor = max(
            HISTORY_START + timedelta(days=rng.randint(0, 90)),
            blocked_until[member_id] + timedelta(days=5) if blocked_until[member_id] < FAR_FUTURE else FAR_FUTURE,
        )
        for _ in range(wanted):
            if cursor >= earlier_limit:
                break
            late_days = sample_late_days(rng) if rng.random() < 0.25 else None
            loan = make_returned_loan(rng, member, cursor, earlier_limit, late_days, True)
            if loan is None:
                break
            loan["limit"] = earlier_limit
            if not attach_loan_and_fine(loan, None):
                break
            settled = blocked_until[member_id]
            if settled >= FAR_FUTURE:
                break
            cursor = max(loan["returnDate"], settled) + timedelta(days=rng.randint(5, 45))

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
    eligible_for_holds = sorted(
        m
        for m, p in profiles.items()
        if p in ("DUE_SOON", "ONTIME", "HISTORY") and m not in terminal_members and m not in lost_checkout_cap
    )
    active_by_isbn: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for loan in active_loans:
        active_by_isbn[loan["isbn13"]].append(loan)
    reservations: list[dict[str, Any]] = []
    holds_per_member: dict[str, int] = defaultdict(int)

    def build_queue(isbn: str, ready_copy: str | None) -> None:
        holders = {loan["memberId"] for loan in active_by_isbn[isbn]}
        pool = [m for m in eligible_for_holds if m not in holders and holds_per_member[m] < 2]
        if isbn in pinned_queues and all(m in pool for m in pinned_queues[isbn]):
            chosen = pinned_queues[isbn]
        else:
            size = rng.choice([1, 2, 2, 3])
            chosen = rng.sample(pool, size)
        lower = max((loan["checkoutDate"] for loan in active_by_isbn[isbn]), default=REFERENCE_DATE - timedelta(days=7))
        created = max(lower, date(2026, 10, 12) if isbn in ("9780130960160", "9780345309884") else REFERENCE_DATE - timedelta(days=10))
        for position, member_id in enumerate(chosen, start=1):
            member_unblocked = blocked_until[member_id] if blocked_until[member_id] < FAR_FUTURE else HISTORY_START
            if isbn == "9780130960160":
                created = max(date(2026, 10, 12) if position == 1 else date(2026, 10, 13), member_unblocked, lower)
            else:
                created = min(max(created + timedelta(days=rng.randint(0, 2)), member_unblocked, lower), REFERENCE_DATE)
            is_ready = bool(ready_copy and position == 1)
            if is_ready:
                ready_on = max(created, REFERENCE_DATE - timedelta(days=rng.randint(0, 2)))
                hold_until = ready_on + timedelta(days=HOLD_PICKUP_DAYS)
            else:
                ready_on = None
                hold_until = None
            reservations.append(
                {
                    "isbn13": isbn,
                    "memberId": member_id,
                    "queuePosition": position,
                    "status": "READY" if is_ready else "WAITING",
                    "createdOn": created,
                    "readyCopyBarcode": ready_copy if is_ready else None,
                    "readyOn": ready_on,
                    "holdUntil": hold_until,
                }
            )
            holds_per_member[member_id] += 1

    for isbn in queue_titles:
        build_queue(isbn, None)
    for isbn in ready_titles:
        build_queue(isbn, reserved_copies[isbn])

    # --- finalize ids and registration dates ------------------------------------------------
    all_loans = active_loans + lost_loans + history_loans
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


def serialize(
    members: list[dict[str, Any]],
    librarians: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    circulation: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
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
            "lostReportedOn": iso(l["lostReportedOn"]),
            "status": l["status"],
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
            "readyOn": iso(r["readyOn"]),
            "holdUntil": iso(r["holdUntil"]),
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
    normalized_books = [{**b, "referenceOnly": is_reference_only_book(b)} for b in books]
    members = build_members(rng, fake)
    librarians = build_librarians(fake)
    copies = build_copies(rng, normalized_books)
    circulation = build_circulation(rng, normalized_books, members, librarians, copies)
    return serialize(members, librarians, copies, circulation)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic LMS seed data.")
    parser.add_argument("--books", type=Path, default=BOOKS_FILE, help="input books-openlibrary.json")
    parser.add_argument("--output-dir", type=Path, default=SEED_DIR, help="directory for the generated JSON files")
    args = parser.parse_args()

    if not args.books.exists():
        print(f"ERROR: {args.books} not found. Run fetch_books.py first.", file=sys.stderr)
        return 2
    books = read_json(args.books)
    for b in books:
        b["referenceOnly"] = is_reference_only_book(b)
    if args.books.resolve() == (args.output_dir / "books-openlibrary.json").resolve():
        write_json(args.books, books)
    datasets = generate(books)
    for name, rows in datasets.items():
        write_json(args.output_dir / name, rows)
        print(f"{name}: {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
