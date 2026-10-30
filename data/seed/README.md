<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Directory index for the seed data files (real Open Library book metadata plus 100% synthetic operational data under confirmed ADU library rules).
-->
# Seed Data (`data/seed`)

Contains the generated seed v2 datasets: real book metadata from Open Library (`books-openlibrary.json`, 782 books including 3 `referenceOnly` reference works and 779 circulating books) and
100% synthetic members (`members.json`, 60 rows: 40 `STUDENT`, 10 `ACADEMIC_STAFF`, 10 `ADMINISTRATIVE_STAFF`; 55 `ACTIVE`, 5 `SUSPENDED`), librarians (`librarians.json`, 3 rows), physical copies (`copies.json`, 1,706 rows: 1,624 `AVAILABLE`, 59 `LOANED`, 15 `MAINTENANCE`, 5 `LOST`, 3 `RESERVED`), loans (`loans.json`, 164 rows: 59 `ACTIVE`, 100 `RETURNED`, 5 `LOST`), fines (`fines.json`, 47 rows: 26 `UNPAID`, 16 `PAID`, 5 `WAIVED`), and reservations (`reservations.json`, 22 rows across 12 titles: 19 `WAITING`, 3 `READY`). Real personal data, credentials, and book prices are strictly prohibited.

Sources, regeneration commands, file formats, confirmed ADU library business rules (`docs/02-inception/BUSINESS_RULES.md`), and the Open Library CC0 license are documented in
[`../README.md`](../README.md). These JSON files are machine-generated; do not edit them by hand.
