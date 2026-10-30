# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Offline unit tests for Open Library record normalization, referenceOnly tagging, category mapping, and politeness rules in fetch_books.py.
import contextlib
import io
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fetch_books  # noqa: E402
from lms_seed_common import is_valid_isbn13  # noqa: E402


def make_doc(**overrides):
    doc = {
        "key": "/works/OL1W",
        "title": "Database Design for Mere Mortals",
        "author_name": ["Michael J. Hernandez"],
        "first_publish_year": 1996,
        "number_of_pages_median": 611,
        "cover_i": 135738,
        "subject": ["Database design", "Relational databases"],
        "editions": {
            "docs": [
                {
                    "subtitle": "a hands-on guide to relational database design",
                    "isbn": ["0201752840", "9780201752847"],
                    "publisher": ["Addison-Wesley"],
                    "cover_i": 15105950,
                }
            ]
        },
    }
    doc.update(overrides)
    return doc


class NormalizeDocTests(unittest.TestCase):
    def test_complete_record_is_normalized(self):
        record, reason = fetch_books.normalize_doc(make_doc(), "Databases")
        self.assertEqual(reason, "ok")
        self.assertEqual(record["isbn13"], "9780201752847")
        self.assertEqual(record["subtitle"], "A hands-on guide to relational database design")
        self.assertEqual(record["publisher"], "Addison-Wesley")
        self.assertEqual(record["coverId"], 15105950)
        self.assertEqual(record["coverUrl"], "https://covers.openlibrary.org/b/id/15105950-M.jpg")
        self.assertEqual(record["pageCount"], 611)
        self.assertEqual(record["category"], "Databases")
        self.assertIs(record["referenceOnly"], False)

    def test_reference_only_flag_set_for_dictionaries_and_encyclopedias_only(self):
        enc_doc = make_doc(title="Encyclopedia of Computer Science and Technology", subject=["Computer science"])
        enc_record, _ = fetch_books.normalize_doc(enc_doc, "Computer Science")
        self.assertIs(enc_record["referenceOnly"], True)

        complete_ref_doc = make_doc(title="C, The Complete Reference", subject=["C (Computer program language)"])
        complete_ref_record, _ = fetch_books.normalize_doc(complete_ref_doc, "Programming")
        self.assertIs(complete_ref_record["referenceOnly"], False)

    def test_isbn10_only_edition_is_converted_to_valid_isbn13(self):
        doc = make_doc()
        doc["editions"]["docs"][0]["isbn"] = ["0201752840"]
        record, _ = fetch_books.normalize_doc(doc, "Databases")
        self.assertIsNotNone(record)
        self.assertTrue(is_valid_isbn13(record["isbn13"]))
        self.assertEqual(record["isbn13"], "9780201752847")

    def test_invalid_isbns_drop_the_record(self):
        doc = make_doc()
        doc["editions"]["docs"][0]["isbn"] = ["0201752841", "9780201752846"]
        record, reason = fetch_books.normalize_doc(doc, "Databases")
        self.assertIsNone(record)
        self.assertEqual(reason, "no_isbn13_or_publisher")

    def test_missing_subtitle_is_null(self):
        doc = make_doc()
        del doc["editions"]["docs"][0]["subtitle"]
        record, _ = fetch_books.normalize_doc(doc, "Databases")
        self.assertIsNone(record["subtitle"])

    def test_incomplete_records_are_dropped(self):
        cases = {
            "missing_title": {"title": None},
            "missing_authors": {"author_name": []},
            "missing_or_invalid_year": {"first_publish_year": None},
            "missing_pages": {"number_of_pages_median": None},
            "missing_cover": {"cover_i": None},
            "no_edition": {"editions": {"docs": []}},
        }
        for expected_reason, override in cases.items():
            with self.subTest(reason=expected_reason):
                doc = make_doc(**override)
                if expected_reason == "missing_cover":
                    del doc["editions"]["docs"][0]["cover_i"]
                record, reason = fetch_books.normalize_doc(doc, "Databases")
                self.assertIsNone(record)
                self.assertEqual(reason, expected_reason)

    def test_missing_publisher_drops_record(self):
        doc = make_doc()
        del doc["editions"]["docs"][0]["publisher"]
        record, reason = fetch_books.normalize_doc(doc, "Databases")
        self.assertIsNone(record)
        self.assertEqual(reason, "no_isbn13_or_publisher")


class CategoryMappingTests(unittest.TestCase):
    def test_technical_subject_refines_default(self):
        self.assertEqual(
            fetch_books.map_category(["Python (Computer program language)"], "Computer Science"),
            "Programming",
        )

    def test_humanities_default_is_kept(self):
        self.assertEqual(fetch_books.map_category(["Psychology", "Physics"], "Fiction"), "Fiction")

    def test_unmatched_subjects_use_default(self):
        self.assertEqual(fetch_books.map_category(["Gardening"], "Engineering"), "Engineering")

    def test_all_query_defaults_are_known_categories(self):
        from lms_seed_common import CATEGORIES

        for _, _, _, category in fetch_books.QUERIES:
            self.assertIn(category, CATEGORIES)


class PolitenessTests(unittest.TestCase):
    def test_query_count_is_about_thirty(self):
        self.assertGreaterEqual(len(fetch_books.QUERIES), 30)
        self.assertEqual(len({q[0] for q in fetch_books.QUERIES}), len(fetch_books.QUERIES))

    def test_request_budget_is_bounded(self):
        self.assertGreaterEqual(fetch_books.MIN_INTERVAL_SECONDS, 1.0)
        self.assertLessEqual(len(fetch_books.QUERIES) * fetch_books.PAGES_PER_QUERY, fetch_books.MAX_NETWORK_REQUESTS)

    def test_missing_contact_email_stops_the_client(self):
        client = fetch_books.PoliteClient(offline=False, refresh=False)
        with mock.patch.dict(os.environ, {}, clear=True), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                client._ensure_session()
        self.assertEqual(ctx.exception.code, 2)

    def test_user_agent_names_project_and_uses_env_email(self):
        client = fetch_books.PoliteClient(offline=False, refresh=False)
        with mock.patch.dict(os.environ, {fetch_books.CONTACT_ENV_VAR: "someone@example.org"}):
            session = client._ensure_session()
        agent = session.headers["User-Agent"]
        self.assertIn("CSE305", agent)
        self.assertIn("LibraryManagementSystem", agent)
        self.assertIn("someone@example.org", agent)

    def test_no_email_literal_in_source(self):
        source = Path(fetch_books.__file__).read_text(encoding="utf-8")
        self.assertNotIn("@gmail", source)


if __name__ == "__main__":
    unittest.main()
