# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Validation tests for the committed seed data files (integrity, foreign keys, loan/fine rules, FIFO queues, privacy, reproducibility).
"""Validate data/seed/*.json against the project ASSUMPTIONs.

The business-rule constants are deliberately re-declared here (instead of imported from
the generator) so that a typo in the generator cannot silently pass its own tests.
"""
import json
import re
import sys
import tempfile
import unittest
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

TOOLS_DATA = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOLS_DATA.parents[1]
SEED = REPO_ROOT / "data" / "seed"
sys.path.insert(0, str(TOOLS_DATA))

# ASSUMPTION-02/03/05 (project assumptions, not official ADU regulations).
REFERENCE_DATE = date(2026, 10, 22)
LOAN_DAYS = {"STUDENT": 14, "ACADEMIC_STAFF": 30}
MAX_ACTIVE = {"STUDENT": 3, "ACADEMIC_STAFF": 5}
FINE_PER_DAY = Decimal("5.00")
FINE_CAP = Decimal("250.00")

CATEGORIES = {
    "Computer Science", "Software Engineering", "Programming", "Databases", "Mathematics",
    "Physics & Natural Sciences", "Engineering", "Fiction", "History",
    "Philosophy & Social Sciences", "Turkish Literature",
}
COPY_STATUSES = {"AVAILABLE", "LOANED", "RESERVED", "MAINTENANCE", "LOST"}
SYNTHETIC_DOMAIN = "synthetic.lms.local"

DATA = {}


def d(text):
    return date.fromisoformat(text) if text else None


def isbn13_ok(value):
    if not isinstance(value, str) or len(value) != 13 or not value.isdigit():
        return False
    total = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(value[:12]))
    return (10 - total % 10) % 10 == int(value[12])


def setUpModule():
    for name in ("books-openlibrary", "members", "librarians", "copies", "loans", "fines", "reservations"):
        with open(SEED / f"{name}.json", "r", encoding="utf-8") as handle:
            DATA[name] = json.load(handle)
    DATA["members_by_id"] = {m["memberId"]: m for m in DATA["members"]}
    DATA["copies_by_barcode"] = {c["barcode"]: c for c in DATA["copies"]}
    DATA["loans_by_id"] = {l["loanId"]: l for l in DATA["loans"]}
    DATA["books_by_isbn"] = {b["isbn13"]: b for b in DATA["books-openlibrary"]}
    DATA["copies_by_isbn"] = defaultdict(list)
    for c in DATA["copies"]:
        DATA["copies_by_isbn"][c["isbn13"]].append(c)
    DATA["loans_by_member"] = defaultdict(list)
    for l in DATA["loans"]:
        DATA["loans_by_member"][l["memberId"]].append(l)


def end_of(loan):
    """Date up to which the loan ran (return date, or the reference date if still active)."""
    return d(loan["returnDate"]) or REFERENCE_DATE


def active_at(loan, day):
    returned = d(loan["returnDate"])
    return d(loan["checkoutDate"]) <= day and (returned is None or returned > day)


class BookTests(unittest.TestCase):
    def test_row_count_is_within_target(self):
        self.assertTrue(500 <= len(DATA["books-openlibrary"]) <= 800, len(DATA["books-openlibrary"]))

    def test_isbn13_unique_and_checksum_valid(self):
        isbns = [b["isbn13"] for b in DATA["books-openlibrary"]]
        self.assertEqual(len(isbns), len(set(isbns)))
        for isbn in isbns:
            self.assertTrue(isbn13_ok(isbn), isbn)

    def test_open_library_work_keys_unique(self):
        keys = [b["openLibraryWorkKey"] for b in DATA["books-openlibrary"]]
        self.assertEqual(len(keys), len(set(keys)))

    def test_required_fields_present_and_complete(self):
        for b in DATA["books-openlibrary"]:
            with self.subTest(isbn=b["isbn13"]):
                self.assertTrue(b["title"].strip())
                self.assertTrue(b["publisher"].strip())
                self.assertTrue(b["authors"] and all(a.strip() for a in b["authors"]))
                self.assertIsInstance(b["pageCount"], int)
                self.assertGreater(b["pageCount"], 0)
                self.assertTrue(1450 <= b["firstPublishYear"] <= 2026)
                self.assertIn(b["category"], CATEGORIES)
                self.assertTrue(b["subtitle"] is None or b["subtitle"].strip())
                self.assertEqual(b["coverUrl"], f"https://covers.openlibrary.org/b/id/{b['coverId']}-M.jpg")

    def test_every_category_is_used(self):
        self.assertEqual({b["category"] for b in DATA["books-openlibrary"]}, CATEGORIES)


class MemberAndLibrarianTests(unittest.TestCase):
    def test_member_count_ids_and_emails(self):
        members = DATA["members"]
        self.assertTrue(55 <= len(members) <= 65)
        self.assertEqual(len({m["memberId"] for m in members}), len(members))
        self.assertEqual(len({m["email"] for m in members}), len(members))
        for m in members:
            kind = "STU" if m["memberType"] == "STUDENT" else "STF"
            self.assertRegex(m["memberId"], rf"^SYN-{kind}-\d{{4}}$")
            self.assertEqual(m["email"], f"{m['memberId'].lower()}@{SYNTHETIC_DOMAIN}")
            self.assertIn(m["memberType"], LOAN_DAYS)
            self.assertIn(m["status"], {"ACTIVE", "SUSPENDED"})
            self.assertTrue(m["firstName"].strip() and m["lastName"].strip())

    def test_both_member_types_and_a_few_suspended_members(self):
        types = {m["memberType"] for m in DATA["members"]}
        self.assertEqual(types, {"STUDENT", "ACADEMIC_STAFF"})
        suspended = [m for m in DATA["members"] if m["status"] == "SUSPENDED"]
        self.assertTrue(1 <= len(suspended) <= 8)

    def test_librarians(self):
        librarians = DATA["librarians"]
        self.assertEqual(len(librarians), 3)
        self.assertEqual(len({l["username"] for l in librarians}), 3)
        for l in librarians:
            self.assertEqual(l["role"], "ROLE_LIBRARIAN")
            self.assertTrue(l["displayName"].strip())
            self.assertEqual(set(l), {"username", "displayName", "email", "role"})

    def test_no_credentials_anywhere_in_seed_files(self):
        pattern = re.compile(r"pass(word|wd)|secret|token|credential|hash|apikey|api_key", re.IGNORECASE)

        def walk(node, path):
            if isinstance(node, dict):
                for key, value in node.items():
                    self.assertIsNone(pattern.search(key), f"credential-like key {key!r} in {path}")
                    walk(value, path)
            elif isinstance(node, list):
                for item in node:
                    walk(item, path)

        for name in ("books-openlibrary", "members", "librarians", "copies", "loans", "fines", "reservations"):
            walk(DATA[name], name)


class CopyTests(unittest.TestCase):
    def test_barcodes_unique_and_formatted(self):
        barcodes = [c["barcode"] for c in DATA["copies"]]
        self.assertEqual(len(barcodes), len(set(barcodes)))
        for b in barcodes:
            self.assertRegex(b, r"^LMS-COPY-\d{4,}$")
        self.assertEqual(barcodes[0], "LMS-COPY-1001")

    def test_one_to_four_copies_per_book(self):
        for isbn in DATA["books_by_isbn"]:
            self.assertTrue(1 <= len(DATA["copies_by_isbn"][isbn]) <= 4, isbn)

    def test_copies_reference_existing_books_and_valid_status(self):
        for c in DATA["copies"]:
            self.assertIn(c["isbn13"], DATA["books_by_isbn"])
            self.assertIn(c["status"], COPY_STATUSES)

    def test_every_status_is_represented(self):
        self.assertEqual({c["status"] for c in DATA["copies"]}, COPY_STATUSES)

    def test_loaned_status_matches_active_loans_exactly(self):
        loaned = {c["barcode"] for c in DATA["copies"] if c["status"] == "LOANED"}
        active = {l["copyBarcode"] for l in DATA["loans"] if l["status"] == "ACTIVE"}
        self.assertEqual(loaned, active)

    def test_reserved_copies_match_ready_reservations(self):
        reserved = {c["barcode"] for c in DATA["copies"] if c["status"] == "RESERVED"}
        ready = {r["readyCopyBarcode"] for r in DATA["reservations"] if r["status"] == "READY"}
        self.assertEqual(reserved, ready)


class LoanTests(unittest.TestCase):
    def test_row_count_and_unique_ids(self):
        self.assertTrue(120 <= len(DATA["loans"]) <= 200, len(DATA["loans"]))
        self.assertEqual(len(DATA["loans_by_id"]), len(DATA["loans"]))

    def test_foreign_keys_resolve(self):
        for l in DATA["loans"]:
            self.assertIn(l["memberId"], DATA["members_by_id"])
            self.assertIn(l["copyBarcode"], DATA["copies_by_barcode"])

    def test_dates_are_valid_and_ordered(self):
        for l in DATA["loans"]:
            with self.subTest(loan=l["loanId"]):
                checkout, due, returned = d(l["checkoutDate"]), d(l["dueDate"]), d(l["returnDate"])
                self.assertLessEqual(checkout, REFERENCE_DATE)
                self.assertGreater(due, checkout)
                if returned:
                    self.assertGreater(returned, checkout)
                    self.assertLessEqual(returned, REFERENCE_DATE)
                    self.assertEqual(l["status"], "RETURNED")
                else:
                    self.assertEqual(l["status"], "ACTIVE")

    def test_due_date_follows_loan_period_and_renewal_rules(self):
        for l in DATA["loans"]:
            with self.subTest(loan=l["loanId"]):
                period = LOAN_DAYS[DATA["members_by_id"][l["memberId"]]["memberType"]]
                checkout = d(l["checkoutDate"])
                self.assertIn(l["renewalCount"], (0, 1))
                self.assertEqual(d(l["dueDate"]), checkout + timedelta(days=period * (1 + l["renewalCount"])))
                if l["renewalCount"] == 0:
                    self.assertIsNone(l["renewedOn"])
                else:
                    renewed = d(l["renewedOn"])
                    self.assertGreater(renewed, checkout)
                    self.assertLessEqual(renewed, checkout + timedelta(days=period))  # renewed before it was overdue
                    self.assertLessEqual(renewed, REFERENCE_DATE)
                    if l["returnDate"]:
                        self.assertGreaterEqual(d(l["returnDate"]), renewed)

    def test_no_member_ever_exceeds_the_active_loan_limit(self):
        for member_id, loans in DATA["loans_by_member"].items():
            limit = MAX_ACTIVE[DATA["members_by_id"][member_id]["memberType"]]
            for loan in loans:
                day = d(loan["checkoutDate"])
                simultaneous = sum(1 for other in loans if active_at(other, day))
                self.assertLessEqual(simultaneous, limit, f"{member_id} on {day}")

    def test_current_active_loans_respect_the_limit_and_member_status(self):
        for member_id, loans in DATA["loans_by_member"].items():
            member = DATA["members_by_id"][member_id]
            active = [l for l in loans if l["status"] == "ACTIVE"]
            self.assertLessEqual(len(active), MAX_ACTIVE[member["memberType"]])
            if member["status"] == "SUSPENDED":
                self.assertEqual(active, [], f"suspended member {member_id} holds an active loan")

    def test_at_least_one_member_is_exactly_at_the_limit_per_type(self):
        for member_type, limit in MAX_ACTIVE.items():
            counts = [
                sum(1 for l in loans if l["status"] == "ACTIVE")
                for member_id, loans in DATA["loans_by_member"].items()
                if DATA["members_by_id"][member_id]["memberType"] == member_type
            ]
            self.assertIn(limit, counts, member_type)

    def test_no_copy_is_loaned_twice_at_the_same_time(self):
        by_copy = defaultdict(list)
        for l in DATA["loans"]:
            by_copy[l["copyBarcode"]].append(l)
        for barcode, loans in by_copy.items():
            loans.sort(key=lambda l: l["checkoutDate"])
            self.assertLessEqual(sum(1 for l in loans if l["status"] == "ACTIVE"), 1, barcode)
            for earlier, later in zip(loans, loans[1:]):
                self.assertIsNotNone(earlier["returnDate"], f"{barcode}: open loan followed by another loan")
                self.assertLessEqual(d(earlier["returnDate"]), d(later["checkoutDate"]), barcode)

    def test_no_member_holds_two_copies_of_the_same_title_at_once(self):
        for member_id, loans in DATA["loans_by_member"].items():
            seen = set()
            for l in loans:
                if l["status"] == "ACTIVE":
                    isbn = DATA["copies_by_barcode"][l["copyBarcode"]]["isbn13"]
                    self.assertNotIn(isbn, seen, member_id)
                    seen.add(isbn)

    def test_borrowing_block_rule_assumption_06_at_every_checkout(self):
        fines_by_member = defaultdict(list)
        for f in DATA["fines"]:
            fines_by_member[f["memberId"]].append(f)
        for member_id, loans in DATA["loans_by_member"].items():
            for loan in loans:
                day = d(loan["checkoutDate"])
                for other in loans:
                    if other is loan:
                        continue
                    overdue_then = d(other["dueDate"]) < day and active_at(other, day)
                    self.assertFalse(overdue_then, f"{member_id} borrowed on {day} while {other['loanId']} was overdue")
                for fine in fines_by_member[member_id]:
                    settled = d(fine["settledOn"])
                    unpaid_then = d(fine["assessedOn"]) <= day and (settled is None or settled > day)
                    self.assertFalse(unpaid_then, f"{member_id} borrowed on {day} with unpaid {fine['fineId']}")

    def test_scenario_coverage(self):
        active = [l for l in DATA["loans"] if l["status"] == "ACTIVE"]
        due_in = [(d(l["dueDate"]) - REFERENCE_DATE).days for l in active]
        self.assertGreaterEqual(sum(1 for x in due_in if x >= 4), 5, "on-time active loans")
        self.assertGreaterEqual(sum(1 for x in due_in if 0 <= x <= 3), 5, "due-soon loans")
        self.assertGreaterEqual(sum(1 for x in due_in if x < 0), 5, "overdue active loans")
        self.assertGreaterEqual(len([l for l in DATA["loans"] if l["status"] == "RETURNED"]), 50)
        self.assertTrue(any(l["renewalCount"] == 1 for l in DATA["loans"]))


class FineTests(unittest.TestCase):
    def test_foreign_keys_and_uniqueness(self):
        librarians = {l["username"] for l in DATA["librarians"]}
        self.assertEqual(len({f["fineId"] for f in DATA["fines"]}), len(DATA["fines"]))
        for f in DATA["fines"]:
            loan = DATA["loans_by_id"][f["loanId"]]
            self.assertEqual(loan["memberId"], f["memberId"])
            self.assertIn(f["memberId"], DATA["members_by_id"])
            if f["settledBy"] is not None:
                self.assertIn(f["settledBy"], librarians)
        self.assertEqual(len({f["loanId"] for f in DATA["fines"]}), len(DATA["fines"]), "one fine per loan")

    def test_every_late_loan_has_exactly_one_correct_fine_and_no_other_loan_has_one(self):
        fines_by_loan = {f["loanId"]: f for f in DATA["fines"]}
        for l in DATA["loans"]:
            with self.subTest(loan=l["loanId"]):
                late = max(0, (end_of(l) - d(l["dueDate"])).days)
                fine = fines_by_loan.get(l["loanId"])
                if late == 0:
                    self.assertIsNone(fine)
                    continue
                self.assertIsNotNone(fine)
                expected = min(FINE_CAP, FINE_PER_DAY * late)
                self.assertEqual(fine["overdueDays"], late)
                self.assertEqual(fine["amount"], f"{expected:.2f}")
                self.assertEqual(Decimal(fine["amount"]), expected)
                self.assertEqual(fine["currency"], "TRY")

    def test_fine_amounts_never_exceed_the_cap_and_cap_applies_from_50_days(self):
        for f in DATA["fines"]:
            self.assertLessEqual(Decimal(f["amount"]), FINE_CAP)
            self.assertGreater(Decimal(f["amount"]), 0)
            if f["overdueDays"] >= 50:
                self.assertEqual(Decimal(f["amount"]), FINE_CAP)
        self.assertTrue(any(f["overdueDays"] > 50 and f["amount"] == "250.00" for f in DATA["fines"]), "no capped example")
        self.assertTrue(any(Decimal(f["amount"]) < FINE_CAP for f in DATA["fines"]), "no uncapped example")

    def test_status_and_settlement_consistency(self):
        for f in DATA["fines"]:
            loan = DATA["loans_by_id"][f["loanId"]]
            self.assertIn(f["status"], {"PAID", "WAIVED", "UNPAID"})
            assessed = d(f["assessedOn"])
            if loan["status"] == "ACTIVE":
                self.assertEqual(f["status"], "UNPAID")
                self.assertEqual(assessed, REFERENCE_DATE)
            else:
                self.assertEqual(assessed, d(loan["returnDate"]))
            if f["status"] == "UNPAID":
                self.assertIsNone(f["settledOn"])
                self.assertIsNone(f["settledBy"])
            else:
                self.assertEqual(loan["status"], "RETURNED")
                self.assertIsNotNone(f["settledBy"])
                settled = d(f["settledOn"])
                self.assertGreaterEqual(settled, assessed)
                self.assertLessEqual(settled, REFERENCE_DATE)

    def test_all_three_statuses_are_present(self):
        self.assertEqual({f["status"] for f in DATA["fines"]}, {"PAID", "WAIVED", "UNPAID"})

    def test_members_with_overdue_or_unpaid_fines_hold_no_new_loans_after(self):
        blocked = {f["memberId"] for f in DATA["fines"] if f["status"] == "UNPAID"}
        self.assertTrue(blocked)
        for member_id in blocked:
            unpaid_assessed = min(d(f["assessedOn"]) for f in DATA["fines"] if f["memberId"] == member_id and f["status"] == "UNPAID")
            for loan in DATA["loans_by_member"][member_id]:
                self.assertLess(d(loan["checkoutDate"]), unpaid_assessed)


class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.queues = defaultdict(list)
        for r in DATA["reservations"]:
            self.queues[r["isbn13"]].append(r)
        for items in self.queues.values():
            items.sort(key=lambda r: r["queuePosition"])

    def test_foreign_keys_and_unique_ids(self):
        self.assertEqual(len({r["reservationId"] for r in DATA["reservations"]}), len(DATA["reservations"]))
        for r in DATA["reservations"]:
            self.assertIn(r["isbn13"], DATA["books_by_isbn"])
            self.assertIn(r["memberId"], DATA["members_by_id"])
            if r["readyCopyBarcode"] is not None:
                self.assertEqual(DATA["copies_by_barcode"][r["readyCopyBarcode"]]["isbn13"], r["isbn13"])

    def test_there_are_a_few_queues(self):
        self.assertTrue(8 <= len(self.queues) <= 20, len(self.queues))
        self.assertTrue(any(len(q) >= 2 for q in self.queues.values()))

    def test_fifo_positions_and_dates(self):
        for isbn, queue in self.queues.items():
            self.assertEqual([r["queuePosition"] for r in queue], list(range(1, len(queue) + 1)), isbn)
            dates = [d(r["createdOn"]) for r in queue]
            self.assertEqual(dates, sorted(dates), f"{isbn}: queue is not FIFO by creation date")
            for created in dates:
                self.assertLessEqual(created, REFERENCE_DATE)

    def test_no_member_twice_in_one_queue_and_not_holding_the_title(self):
        for isbn, queue in self.queues.items():
            members = [r["memberId"] for r in queue]
            self.assertEqual(len(members), len(set(members)), isbn)
            for r in queue:
                for loan in DATA["loans_by_member"][r["memberId"]]:
                    if loan["status"] == "ACTIVE":
                        self.assertNotEqual(DATA["copies_by_barcode"][loan["copyBarcode"]]["isbn13"], isbn)

    def test_queue_members_are_eligible_borrowers(self):
        overdue_members = {
            l["memberId"] for l in DATA["loans"] if l["status"] == "ACTIVE" and d(l["dueDate"]) < REFERENCE_DATE
        }
        unpaid_members = {f["memberId"] for f in DATA["fines"] if f["status"] == "UNPAID"}
        for r in DATA["reservations"]:
            self.assertEqual(DATA["members_by_id"][r["memberId"]]["status"], "ACTIVE")
            self.assertNotIn(r["memberId"], overdue_members)
            self.assertNotIn(r["memberId"], unpaid_members)

    def test_hold_queues_exist_only_when_no_copy_is_available(self):
        for isbn, queue in self.queues.items():
            statuses = {c["status"] for c in DATA["copies_by_isbn"][isbn]}
            self.assertTrue(statuses <= {"LOANED", "RESERVED"}, f"{isbn} has copies {statuses}")
            has_ready = any(r["status"] == "READY" for r in queue)
            if not has_ready:
                self.assertEqual(statuses, {"LOANED"}, f"{isbn}: waiting queue but not all copies LOANED")

    def test_waiting_queues_start_only_after_every_copy_was_loaned(self):
        active_by_isbn = defaultdict(list)
        for l in DATA["loans"]:
            if l["status"] == "ACTIVE":
                active_by_isbn[DATA["copies_by_barcode"][l["copyBarcode"]]["isbn13"]].append(l)
        for isbn, queue in self.queues.items():
            latest_checkout = max((d(l["checkoutDate"]) for l in active_by_isbn[isbn]), default=date.min)
            self.assertGreaterEqual(d(queue[0]["createdOn"]), latest_checkout, isbn)

    def test_ready_reservations_are_at_the_head_and_waiting_ones_have_no_copy(self):
        for isbn, queue in self.queues.items():
            for r in queue:
                if r["status"] == "READY":
                    self.assertEqual(r["queuePosition"], 1)
                    self.assertEqual(DATA["copies_by_barcode"][r["readyCopyBarcode"]]["status"], "RESERVED")
                else:
                    self.assertEqual(r["status"], "WAITING")
                    self.assertIsNone(r["readyCopyBarcode"])
        self.assertTrue(any(r["status"] == "READY" for r in DATA["reservations"]))
        self.assertTrue(any(r["status"] == "WAITING" for r in DATA["reservations"]))

    def test_titles_with_holds_have_no_renewed_active_loans(self):
        for l in DATA["loans"]:
            if l["status"] == "ACTIVE" and DATA["copies_by_barcode"][l["copyBarcode"]]["isbn13"] in self.queues:
                self.assertEqual(l["renewalCount"], 0, l["loanId"])


class PrivacyTests(unittest.TestCase):
    EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+")

    def test_only_synthetic_emails_in_seed_files_and_pipeline_sources(self):
        files = sorted(SEED.glob("*.json")) + sorted(TOOLS_DATA.glob("*.py")) + [REPO_ROOT / "data" / "README.md"]
        for path in files:
            text = path.read_text(encoding="utf-8")
            for match in self.EMAIL.findall(text):
                self.assertTrue(match.endswith("@" + SYNTHETIC_DOMAIN), f"non-synthetic e-mail {match!r} in {path.name}")

    def test_readme_declares_data_synthetic(self):
        text = (REPO_ROOT / "data" / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("synthetic", text)
        self.assertIn("not related to any real", text)


class ReproducibilityTests(unittest.TestCase):
    def test_generator_output_is_byte_identical_to_committed_files(self):
        import generate_synthetic
        from lms_seed_common import write_json

        books = DATA["books-openlibrary"]
        with tempfile.TemporaryDirectory() as tmp:
            for name, rows in generate_synthetic.generate(books).items():
                write_json(Path(tmp) / name, rows)
                expected = (SEED / name).read_bytes()
                self.assertEqual((Path(tmp) / name).read_bytes(), expected, f"{name} differs from a fresh run")

    def test_generator_is_deterministic_across_two_runs(self):
        import generate_synthetic

        books = DATA["books-openlibrary"]
        self.assertEqual(generate_synthetic.generate(books), generate_synthetic.generate(books))


if __name__ == "__main__":
    unittest.main()
