# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Fetches real book metadata from the Open Library search API (polite, cached, rate-limited) and writes data/seed/books-openlibrary.json.
"""Fetch and normalize book metadata from Open Library.

Politeness rules (see https://openlibrary.org/developers/api):
  * at least ``MIN_INTERVAL_SECONDS`` between network requests,
  * a descriptive User-Agent that names this course project and a contact e-mail
    read from the ``LMS_CONTACT_EMAIL`` environment variable (never stored in Git),
  * every raw response is cached in ``data/raw/openlibrary`` (gitignored),
  * a hard cap on the total number of network requests (no bulk crawling).

Usage (PowerShell):
    $env:LMS_CONTACT_EMAIL = "<your e-mail>"
    tools\\data\\.venv\\Scripts\\python.exe tools\\data\\fetch_books.py
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests

from lms_seed_common import (
    BOOKS_FILE,
    CATEGORIES,
    RAW_DIR,
    clean_isbn,
    is_reference_only_book,
    is_valid_isbn13,
    isbn10_to_isbn13,
    write_json,
)

SEARCH_URL = "https://openlibrary.org/search.json"
COVER_URL_TEMPLATE = "https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
CONTACT_ENV_VAR = "LMS_CONTACT_EMAIL"

MIN_INTERVAL_SECONDS = 1.2  # Open Library default limit is 1 request/second.
MAX_NETWORK_REQUESTS = 80  # Hard cap: never crawl in bulk.
PAGES_PER_QUERY = 2
PAGE_SIZE = 100
MAX_PER_QUERY = 30
MAX_BOOKS = 800
MIN_BOOKS = 500
MAX_RETRIES = 3
REQUEST_TIMEOUT_SECONDS = 30
MIN_PUBLISH_YEAR = 1450
MAX_PUBLISH_YEAR = 2026

SEARCH_FIELDS = ",".join(
    [
        "key",
        "title",
        "author_name",
        "first_publish_year",
        "subject",
        "cover_i",
        "number_of_pages_median",
        "editions",
        "editions.title",
        "editions.subtitle",
        "editions.isbn",
        "editions.publisher",
        "editions.cover_i",
    ]
)

# (slug, Solr query, language code, default category)
QUERIES: list[tuple[str, str, str, str]] = [
    ("computer-science", 'subject:"computer science"', "eng", "Computer Science"),
    ("software-engineering", 'subject:"software engineering"', "eng", "Software Engineering"),
    ("computer-programming", 'subject:"computer programming"', "eng", "Programming"),
    ("python", 'subject:"python (computer program language)"', "eng", "Programming"),
    ("java", 'subject:"java (computer program language)"', "eng", "Programming"),
    ("cpp", 'subject:"c++ (computer program language)"', "eng", "Programming"),
    ("databases", "subject:databases", "eng", "Databases"),
    ("sql", 'subject:"sql (computer program language)"', "eng", "Databases"),
    ("algorithms", "subject:algorithms", "eng", "Computer Science"),
    ("data-structures", 'subject:"data structures (computer science)"', "eng", "Computer Science"),
    ("operating-systems", 'subject:"operating systems (computers)"', "eng", "Computer Science"),
    ("computer-networks", 'subject:"computer networks"', "eng", "Computer Science"),
    ("artificial-intelligence", 'subject:"artificial intelligence"', "eng", "Computer Science"),
    ("engineering", "subject:engineering", "eng", "Engineering"),
    ("electrical-engineering", 'subject:"electrical engineering"', "eng", "Engineering"),
    ("mechanical-engineering", 'subject:"mechanical engineering"', "eng", "Engineering"),
    ("mathematics", "subject:mathematics", "eng", "Mathematics"),
    ("statistics", "subject:statistics", "eng", "Mathematics"),
    ("linear-algebra", 'subject:"linear algebra"', "eng", "Mathematics"),
    ("physics", "subject:physics", "eng", "Physics & Natural Sciences"),
    ("chemistry", "subject:chemistry", "eng", "Physics & Natural Sciences"),
    ("biology", "subject:biology", "eng", "Physics & Natural Sciences"),
    ("astronomy", "subject:astronomy", "eng", "Physics & Natural Sciences"),
    ("fiction", "subject:fiction", "eng", "Fiction"),
    ("science-fiction", 'subject:"science fiction"', "eng", "Fiction"),
    ("mystery", 'subject:"detective and mystery stories"', "eng", "Fiction"),
    ("history", "subject:history", "eng", "History"),
    ("world-war-ii", 'subject:"world war, 1939-1945"', "eng", "History"),
    ("turkey-history", 'subject:"turkey history"', "eng", "History"),
    ("philosophy", "subject:philosophy", "eng", "Philosophy & Social Sciences"),
    ("economics", "subject:economics", "eng", "Philosophy & Social Sciences"),
    ("psychology", "subject:psychology", "eng", "Philosophy & Social Sciences"),
    ("turkish-literature", 'subject:"turkish literature"', "tur", "Turkish Literature"),
    ("turkish-fiction", 'subject:"turkish fiction"', "tur", "Turkish Literature"),
]

# Categories whose subjects may be refined by keyword rules. Humanities queries
# keep their query default because their subject lists are too generic.
REFINABLE_CATEGORIES = {
    "Computer Science",
    "Software Engineering",
    "Programming",
    "Databases",
    "Engineering",
    "Mathematics",
    "Physics & Natural Sciences",
}

# Ordered keyword rules (first match wins) applied to lower-cased subject strings.
CATEGORY_RULES: list[tuple[tuple[str, ...], str]] = [
    (("software engineering", "software development", "agile", "software architecture"), "Software Engineering"),
    (("database", "sql", "data mining", "nosql"), "Databases"),
    (("programming", "python (computer", "java (computer", "c++", "javascript"), "Programming"),
    (
        (
            "algorithm",
            "data structure",
            "artificial intelligence",
            "machine learning",
            "operating system",
            "computer network",
            "computer science",
            "computer architecture",
        ),
        "Computer Science",
    ),
    (("linear algebra", "statistic", "calculus", "mathematic", "geometry", "probability"), "Mathematics"),
    (("physics", "chemistry", "biology", "astronomy", "quantum"), "Physics & Natural Sciences"),
    (("engineering",), "Engineering"),
]


def map_category(subjects: list[str], default_category: str) -> str:
    """Map Open Library subjects to one of the small fixed categories."""
    if default_category not in REFINABLE_CATEGORIES:
        return default_category
    lowered = [s.lower() for s in subjects]
    for keywords, category in CATEGORY_RULES:
        if any(keyword in subject for subject in lowered for keyword in keywords):
            return category
    return default_category


def pick_isbn13(isbn_values: list[str]) -> str | None:
    """Return the first valid ISBN-13 (or a converted valid ISBN-10) from a list."""
    cleaned = [clean_isbn(v) for v in isbn_values if isinstance(v, str)]
    for value in cleaned:
        if is_valid_isbn13(value):
            return value
    for value in cleaned:
        converted = isbn10_to_isbn13(value)
        if converted:
            return converted
    return None


def _first_str(values: Any) -> str | None:
    if isinstance(values, str):
        values = [values]
    if isinstance(values, list):
        for value in values:
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _capitalize_first(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


def normalize_doc(doc: dict[str, Any], default_category: str) -> tuple[dict[str, Any] | None, str]:
    """Normalize one Open Library search doc.

    Returns ``(record, "ok")`` or ``(None, reason)`` when the record is dropped.
    """
    title = _first_str(doc.get("title"))
    if not title:
        return None, "missing_title"

    authors = [a.strip() for a in doc.get("author_name") or [] if isinstance(a, str) and a.strip()]
    if not authors:
        return None, "missing_authors"

    year = doc.get("first_publish_year")
    if not isinstance(year, int) or not MIN_PUBLISH_YEAR <= year <= MAX_PUBLISH_YEAR:
        return None, "missing_or_invalid_year"

    pages = doc.get("number_of_pages_median")
    if not isinstance(pages, int) or pages <= 0:
        return None, "missing_pages"

    chosen: dict[str, Any] | None = None
    isbn13: str | None = None
    saw_edition = False
    for edition in (doc.get("editions") or {}).get("docs", []):
        saw_edition = True
        candidate = pick_isbn13(edition.get("isbn") or [])
        if candidate and _first_str(edition.get("publisher")):
            chosen, isbn13 = edition, candidate
            break
    if chosen is None or isbn13 is None:
        return None, "no_isbn13_or_publisher" if saw_edition else "no_edition"

    cover_id = chosen.get("cover_i")
    if not isinstance(cover_id, int):
        cover_id = doc.get("cover_i")
    if not isinstance(cover_id, int) or cover_id <= 0:
        return None, "missing_cover"

    subjects = []
    for raw in doc.get("subject") or []:
        if isinstance(raw, str) and 0 < len(raw.strip()) <= 60 and raw.strip() not in subjects:
            subjects.append(raw.strip())
    subtitle = _first_str(chosen.get("subtitle"))

    subtitle_norm = _capitalize_first(subtitle) if subtitle else None
    subjects_trimmed = subjects[:5]
    record = {
        "isbn13": isbn13,
        "title": title,
        "subtitle": subtitle_norm,
        "authors": authors[:5],
        "publisher": _first_str(chosen.get("publisher")),
        "firstPublishYear": year,
        "category": map_category(subjects, default_category),
        "subjects": subjects_trimmed,
        "pageCount": pages,
        "coverId": cover_id,
        "coverUrl": COVER_URL_TEMPLATE.format(cover_id=cover_id),
        "openLibraryWorkKey": doc.get("key"),
        "referenceOnly": is_reference_only_book(title, subtitle_norm, subjects_trimmed),
    }
    return record, "ok"


class PoliteClient:
    """HTTP client with caching, a minimum request interval, and a hard request cap."""

    def __init__(self, offline: bool, refresh: bool) -> None:
        self.offline = offline
        self.refresh = refresh
        self.network_requests = 0
        self._last_request_time: float | None = None
        self._session: requests.Session | None = None

    def _ensure_session(self) -> requests.Session:
        if self._session is None:
            email = os.environ.get(CONTACT_ENV_VAR, "").strip()
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                print(
                    f"ERROR: environment variable {CONTACT_ENV_VAR} is not set (or not an e-mail).\n"
                    "Open Library asks for a contact e-mail in the User-Agent. Set it for this PowerShell\n"
                    f'session only, e.g.:  $env:{CONTACT_ENV_VAR} = "<your e-mail>"\n'
                    "The e-mail is never written to the repository.",
                    file=sys.stderr,
                )
                raise SystemExit(2)
            session = requests.Session()
            session.headers["User-Agent"] = (
                "CSE305-ADU-LibraryManagementSystem/1.0 "
                f"(student course project, Adnan Menderes University; contact: {email})"
            )
            session.headers["Accept"] = "application/json"
            self._session = session
        return self._session

    def _wait_turn(self) -> None:
        if self._last_request_time is not None:
            remaining = MIN_INTERVAL_SECONDS - (time.monotonic() - self._last_request_time)
            if remaining > 0:
                time.sleep(remaining)

    def get_page(self, slug: str, query: str, language: str, page: int) -> dict[str, Any]:
        """Return one search results page, from cache when available."""
        cache_file = RAW_DIR / f"{slug}_p{page}.json"
        if cache_file.exists() and not self.refresh:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        if self.offline:
            raise SystemExit(f"ERROR: --offline given but cache file is missing: {cache_file}")

        params = {
            "q": f"{query} language:{language}",
            "fields": SEARCH_FIELDS,
            "limit": PAGE_SIZE,
            "page": page,
        }
        session = self._ensure_session()
        url = f"{SEARCH_URL}?{urlencode(params)}"
        for attempt in range(1, MAX_RETRIES + 1):
            if self.network_requests >= MAX_NETWORK_REQUESTS:
                raise SystemExit(f"ERROR: network request cap ({MAX_NETWORK_REQUESTS}) reached; stopping.")
            self._wait_turn()
            self.network_requests += 1
            self._last_request_time = time.monotonic()
            print(f"  GET {slug} page {page} (network request #{self.network_requests}, attempt {attempt})")
            try:
                response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            except requests.RequestException as exc:
                print(f"  request error: {exc}", file=sys.stderr)
                time.sleep(5 * attempt)
                continue
            if response.status_code == 200:
                RAW_DIR.mkdir(parents=True, exist_ok=True)
                cache_file.write_text(response.text, encoding="utf-8", newline="\n")
                return response.json()
            if response.status_code in (429, 500, 502, 503, 504):
                retry_after = response.headers.get("Retry-After", "")
                delay = int(retry_after) if retry_after.isdigit() else 5 * (2 ** (attempt - 1))
                print(f"  HTTP {response.status_code}; backing off {delay}s", file=sys.stderr)
                if response.status_code == 429 and attempt == MAX_RETRIES:
                    raise SystemExit("ERROR: repeatedly rate limited (HTTP 429); stopping. Try again later.")
                time.sleep(delay)
                continue
            raise SystemExit(f"ERROR: unexpected HTTP {response.status_code} for {url}")
        raise SystemExit(f"ERROR: giving up on {slug} page {page} after {MAX_RETRIES} attempts.")


def build_catalog(client: PoliteClient) -> tuple[list[dict[str, Any]], Counter]:
    """Run all queries and return the deduplicated, trimmed catalog and drop statistics."""
    stats: Counter = Counter()
    seen_isbn: set[str] = set()
    seen_work: set[str] = set()
    per_query: list[list[dict[str, Any]]] = []

    for slug, query, language, default_category in QUERIES:
        print(f"Query {slug}: {query} language:{language}")
        kept: list[dict[str, Any]] = []
        for page in range(1, PAGES_PER_QUERY + 1):
            payload = client.get_page(slug, query, language, page)
            docs = payload.get("docs", [])
            for doc in docs:
                record, reason = normalize_doc(doc, default_category)
                if record is None:
                    stats[f"dropped:{reason}"] += 1
                    continue
                work_key = record["openLibraryWorkKey"]
                if record["isbn13"] in seen_isbn or work_key in seen_work:
                    stats["dropped:duplicate"] += 1
                    continue
                seen_isbn.add(record["isbn13"])
                seen_work.add(work_key)
                kept.append(record)
            if len(kept) >= MAX_PER_QUERY or len(docs) < PAGE_SIZE:
                break
        per_query.append(kept)

    cap = MAX_PER_QUERY
    while sum(min(len(items), cap) for items in per_query) > MAX_BOOKS and cap > 1:
        cap -= 1
    catalog = [record for items in per_query for record in items[:cap]]
    stats["dropped:trimmed_to_cap"] = sum(len(items) for items in per_query) - len(catalog)
    catalog.sort(key=lambda r: r["isbn13"])
    return catalog, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch book metadata from Open Library into data/seed.")
    parser.add_argument("--refresh", action="store_true", help="ignore the raw cache and re-fetch from the network")
    parser.add_argument("--offline", action="store_true", help="use only the raw cache; never touch the network")
    args = parser.parse_args()

    client = PoliteClient(offline=args.offline, refresh=args.refresh)
    catalog, stats = build_catalog(client)

    write_json(BOOKS_FILE, catalog)
    print(f"\nNetwork requests made: {client.network_requests} (cap {MAX_NETWORK_REQUESTS})")
    print(f"Books written: {len(catalog)} -> {BOOKS_FILE}")
    for category in CATEGORIES:
        print(f"  {category}: {sum(1 for b in catalog if b['category'] == category)}")
    for key, value in sorted(stats.items()):
        print(f"  {key}: {value}")
    if not MIN_BOOKS <= len(catalog) <= MAX_BOOKS:
        print(f"WARNING: book count {len(catalog)} is outside the target {MIN_BOOKS}-{MAX_BOOKS}.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
