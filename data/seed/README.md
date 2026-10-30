<!--
  Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
  Student No(s)#: 231805033, 231805026
  General Comments: Directory index for the seed data files (real Open Library book metadata plus 100% synthetic operational data under confirmed ADU library rules).
-->
# Seed Data (`data/seed`)

Contains the generated seed v2 datasets: real book metadata from Open Library (`books-openlibrary.json`, 782 books including 3 `referenceOnly` reference works) and
100% synthetic members (`members.json`, 60 rows across `STUDENT`, `ACADEMIC_STAFF`, and `ADMINISTRATIVE_STAFF`), librarians (`librarians.json`, 3 rows), physical copies (`copies.json`, 1,706 rows), loans (`loans.json`, 164 rows), fines (`fines.json`, 47 rows), and reservations (`reservations.json`, 22 rows). Real personal data, credentials, and book prices are strictly prohibited.

Sources, regeneration commands, file formats, confirmed ADU library business rules (`docs/02-inception/BUSINESS_RULES.md`), and the Open Library CC0 license are documented in
[`../README.md`](../README.md). These JSON files are machine-generated; do not edit them by hand.
