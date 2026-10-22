# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Unit tests for ISBN validation/conversion and ASSUMPTION-05 fine helpers (offline, no data files needed).
import sys
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lms_seed_common import (  # noqa: E402
    clean_isbn,
    compute_fine,
    is_valid_isbn10,
    is_valid_isbn13,
    isbn10_to_isbn13,
    overdue_days,
)


class IsbnTests(unittest.TestCase):
    def test_valid_isbn13_accepted(self):
        self.assertTrue(is_valid_isbn13("9780306406157"))
        self.assertTrue(is_valid_isbn13("9780201633610"))

    def test_invalid_isbn13_checksum_rejected(self):
        self.assertFalse(is_valid_isbn13("9780306406158"))

    def test_isbn13_wrong_length_or_characters_rejected(self):
        self.assertFalse(is_valid_isbn13("978030640615"))
        self.assertFalse(is_valid_isbn13("97803064061570"))
        self.assertFalse(is_valid_isbn13("978030640615X"))
        self.assertFalse(is_valid_isbn13(""))

    def test_valid_isbn10_accepted_including_x_check_digit(self):
        self.assertTrue(is_valid_isbn10("0306406152"))
        self.assertTrue(is_valid_isbn10("080442957X"))

    def test_invalid_isbn10_rejected(self):
        self.assertFalse(is_valid_isbn10("0306406153"))
        self.assertFalse(is_valid_isbn10("12345"))

    def test_isbn10_converts_to_isbn13(self):
        self.assertEqual(isbn10_to_isbn13("0306406152"), "9780306406157")
        self.assertEqual(isbn10_to_isbn13("0201633612"), "9780201633610")

    def test_invalid_isbn10_does_not_convert(self):
        self.assertIsNone(isbn10_to_isbn13("0306406153"))

    def test_clean_isbn_removes_hyphens_and_spaces(self):
        self.assertEqual(clean_isbn("978-0-306-40615-7"), "9780306406157")
        self.assertEqual(clean_isbn(" 0 306 40615 2 "), "0306406152")


class FineRuleTests(unittest.TestCase):
    """ASSUMPTION-05: 5.00 TRY per overdue day, capped at 250.00 TRY."""

    def test_zero_days_costs_nothing(self):
        self.assertEqual(compute_fine(0), Decimal("0.00"))

    def test_daily_rate(self):
        self.assertEqual(compute_fine(1), Decimal("5.00"))
        self.assertEqual(compute_fine(10), Decimal("50.00"))

    def test_cap_boundaries(self):
        self.assertEqual(compute_fine(49), Decimal("245.00"))
        self.assertEqual(compute_fine(50), Decimal("250.00"))
        self.assertEqual(compute_fine(51), Decimal("250.00"))
        self.assertEqual(compute_fine(400), Decimal("250.00"))

    def test_overdue_days(self):
        due = date(2026, 10, 1)
        self.assertEqual(overdue_days(due, date(2026, 9, 30)), 0)
        self.assertEqual(overdue_days(due, date(2026, 10, 1)), 0)
        self.assertEqual(overdue_days(due, date(2026, 10, 2)), 1)


if __name__ == "__main__":
    unittest.main()
