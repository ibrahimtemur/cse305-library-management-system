# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Shared constants, ISBN helpers, reference-only detection, fine rules, and deterministic JSON I/O for the seed data pipeline (feature M6).
"""Shared helpers for the LMS seed data pipeline.

The loan, fine, renewal cooldown, hold pickup, and reference-only constants below
implement the confirmed Adnan Menderes University (ADU) library lending rules and
explicit project assumptions documented in ``docs/02-inception/BUSINESS_RULES.md``
(BR-001..BR-018) and ``docs/02-inception/DOMAIN_GLOSSARY.md``.
"""

from __future__ import annotations

import json
import re
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SEED_DIR = REPO_ROOT / "data" / "seed"
RAW_DIR = REPO_ROOT / "data" / "raw" / "openlibrary"
BOOKS_FILE = SEED_DIR / "books-openlibrary.json"

# Fixed reference date ("today") for every synthetic date in the seed data.
REFERENCE_DATE = date(2026, 10, 22)
# Fixed random seed for reproducible synthetic data.
RANDOM_SEED = 20261022

# BR-002 / BR-003 (CONFIRMED ADU rules): borrowing limits and 30-day loan period across all member types.
LOAN_DAYS = {
    "STUDENT": 30,
    "ACADEMIC_STAFF": 30,
    "ADMINISTRATIVE_STAFF": 30,
}
MAX_ACTIVE_LOANS = {
    "STUDENT": 3,
    "ACADEMIC_STAFF": 7,
    "ADMINISTRATIVE_STAFF": 3,
}

# BR-008 / BR-009 (CONFIRMED ADU tariff + ASSUMPTION-10): 0.25 TRY per overdue day, no cap.
FINE_PER_DAY = Decimal("0.25")
CURRENCY = "TRY"

# BR-006 / ASSUMPTION-12: 1-month (30-day) post-renewal re-borrowing cooldown on the same title.
RENEWAL_COOLDOWN_DAYS = 30
# BR-013 / ASSUMPTION-13: 3-day pickup hold window for READY reservations.
HOLD_PICKUP_DAYS = 3
# BR-015 / ASSUMPTION-12: 1-month (30-day) replacement window from lostReportedOn.
LOST_REPLACEMENT_DAYS = 30

# BR-014 / ASSUMPTION-14: strict word-boundary heuristic for non-circulating reference works
# (dictionaries, encyclopedias, catalogs and Turkish equivalents).
REFERENCE_KEYWORD_RE = re.compile(
    r"\b(dictionar(?:y|ies)|encyclopa?edia(?:s)?|catalog(?:ue)?s?|sözlük(?:ler)?|ansiklopedi(?:ler)?|katalog(?:lar)?)\b",
    re.IGNORECASE,
)

# Small fixed set of catalog categories (subject mapping targets).
CATEGORIES = (
    "Computer Science",
    "Software Engineering",
    "Programming",
    "Databases",
    "Mathematics",
    "Physics & Natural Sciences",
    "Engineering",
    "Fiction",
    "History",
    "Philosophy & Social Sciences",
    "Turkish Literature",
)


def isbn13_check_digit(first12: str) -> int:
    """Return the ISBN-13 check digit for the first 12 digits."""
    total = sum(int(ch) * (1 if i % 2 == 0 else 3) for i, ch in enumerate(first12))
    return (10 - total % 10) % 10


def is_valid_isbn13(value: str) -> bool:
    """Return True if value is exactly 13 digits with a correct checksum."""
    if not isinstance(value, str) or len(value) != 13 or not value.isdigit():
        return False
    return isbn13_check_digit(value[:12]) == int(value[12])


def is_valid_isbn10(value: str) -> bool:
    """Return True if value is a valid ISBN-10 (digits, optional trailing X)."""
    if not isinstance(value, str) or len(value) != 10:
        return False
    if not value[:9].isdigit() or not (value[9].isdigit() or value[9] in "xX"):
        return False
    total = sum((10 - i) * int(ch) for i, ch in enumerate(value[:9]))
    total += 10 if value[9] in "xX" else int(value[9])
    return total % 11 == 0


def isbn10_to_isbn13(value: str) -> str | None:
    """Convert a valid ISBN-10 to ISBN-13 (prefix 978); return None if invalid."""
    if not is_valid_isbn10(value):
        return None
    first12 = "978" + value[:9]
    return first12 + str(isbn13_check_digit(first12))


def clean_isbn(raw: str) -> str:
    """Remove hyphens and spaces from a raw ISBN string."""
    return raw.replace("-", "").replace(" ", "").strip()


def is_reference_only_book(
    title_or_book: str | dict[str, Any],
    subtitle: str | None = None,
    subjects: list[str] | tuple[str, ...] = (),
) -> bool:
    """Return True if the book is a non-circulating reference work (BR-014)."""
    if isinstance(title_or_book, dict):
        title = str(title_or_book.get("title") or "")
        subtitle = title_or_book.get("subtitle")
        subjects = title_or_book.get("subjects") or ()
    else:
        title = title_or_book
    texts = [title]
    if subtitle:
        texts.append(subtitle)
    texts.extend(s for s in subjects if isinstance(s, str))
    return any(REFERENCE_KEYWORD_RE.search(text) for text in texts)


def overdue_days(due: date, end: date) -> int:
    """Return whole calendar days past the due date (0 if not late)."""
    return max(0, (end - due).days)


def compute_fine(days: int) -> Decimal:
    """Return the uncapped fine for the given overdue days under BR-008 and BR-009 (0.25 TRY/day)."""
    if days <= 0:
        return Decimal("0.00")
    return FINE_PER_DAY * days


def write_json(path: Path, data: Any) -> None:
    """Write data as UTF-8 (no BOM), LF-terminated, 2-space-indented JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def read_json(path: Path) -> Any:
    """Read a UTF-8 JSON file."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)
