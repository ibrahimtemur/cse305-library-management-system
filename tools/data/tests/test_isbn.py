# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Unit tests for ISBN validation/conversion, reference-only detection (BR-014), and confirmed ADU fine helpers (BR-008/BR-009).
import sys
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lms_seed_common import (  # noqa: E402
    clean_isbn,
    compute_fine,
    is_reference_only_book,
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
    """BR-008 & BR-009 (ASSUMPTION-10): 0.25 TRY per overdue day, with no maximum cap."""

    def test_zero_days_costs_nothing(self):
        self.assertEqual(compute_fine(0), Decimal("0.00"))

    def test_daily_rate_of_25_kurus(self):
        self.assertEqual(compute_fine(1), Decimal("0.25"))
        self.assertEqual(compute_fine(4), Decimal("1.00"))
        self.assertEqual(compute_fine(10), Decimal("2.50"))
        self.assertEqual(compute_fine(53), Decimal("13.25"))

    def test_no_upper_cap(self):
        self.assertEqual(compute_fine(50), Decimal("12.50"))
        self.assertEqual(compute_fine(100), Decimal("25.00"))
        self.assertEqual(compute_fine(1000), Decimal("250.00"))
        self.assertEqual(compute_fine(1200), Decimal("300.00"))

    def test_overdue_days(self):
        due = date(2026, 10, 1)
        self.assertEqual(overdue_days(due, date(2026, 9, 30)), 0)
        self.assertEqual(overdue_days(due, date(2026, 10, 1)), 0)
        self.assertEqual(overdue_days(due, date(2026, 10, 2)), 1)


class ReferenceOnlyRuleTests(unittest.TestCase):
    """BR-014: strict word-boundary detection for dictionaries, encyclopedias, and catalogs."""

    def test_matches_dictionary_encyclopedia_and_catalog_keywords(self):
        self.assertTrue(is_reference_only_book("Dictionary of mechanical engineering", None, ["Mechanical engineering"]))
        self.assertTrue(is_reference_only_book("Encyclopedia of Computer Science and Technology", None, ["Computer science"]))
        self.assertTrue(is_reference_only_book("World War II", None, ["World War, 1939-1945", "Encyclopedias"]))
        self.assertTrue(is_reference_only_book("National Union Catalog", None, []))
        self.assertTrue(is_reference_only_book("Türkçe Sözlük", None, []))

    def test_rejects_complete_reference_and_substring_false_positives(self):
        self.assertFalse(is_reference_only_book("C, The Complete Reference", None, ["C (Computer program language)"]))
        self.assertFalse(is_reference_only_book("Java", "The Complete Reference, Thirteenth Edition", ["Java"]))
        self.assertFalse(is_reference_only_book("Mechanical engineering reference manual for the PE exam", None, ["Handbooks, manuals"]))
        self.assertFalse(is_reference_only_book("Unravel me", None, ["Dictatorship", "Fiction"]))


if __name__ == "__main__":
    unittest.main()
