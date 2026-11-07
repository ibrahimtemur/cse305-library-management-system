# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Cross-platform counterpart of tools/package.ps1; zips the repository into dist/cse305_hwNN_231805033_231805026.zip with the same exclusion rules.
"""Package the repository (or another source tree) as a submission archive.

Usage:
    python3 tools/package.py 02
    python3 tools/package.py 01 --source /tmp/tree --output-dir /tmp/out
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
import zipfile
from pathlib import Path

EXCLUDED_TOP_DIRS = {"target", ".git", ".venv", "venv", "dist", ".idea", ".vscode", ".settings", "node_modules", "__pycache__"}
EXCLUDED_ANY_SEGMENT = {"__pycache__", "node_modules", ".venv", "venv", ".pytest_cache", ".idea", ".vscode", ".settings", ".git"}
EXCLUDED_FILE_PATTERNS = [
    "*.iml", "*.ipr", "*.iws", "*.mv.db", "*.trace.db", "*.lock.db", "*.log", "*.zip",
    "*.pyc", "*.pyo", ".classpath", ".project", ".DS_Store", "Thumbs.db", "Desktop.ini",
]
EXCLUDED_EXACT = {".mvn/timing.properties", ".mvn/wrapper/maven-wrapper.jar"}
EXCLUDED_PREFIXES = ("data/db/", "data/raw/")


def normalize_number(value: str) -> str:
    if re.fullmatch(r"\d", value):
        return "0" + value
    if re.fullmatch(r"\d{2}", value):
        return value
    raise SystemExit(f"Invalid homework number '{value}'. Use a two-digit number such as 01 or 02.")


def is_excluded(rel: str) -> bool:
    segments = rel.split("/")
    if segments[0] in EXCLUDED_TOP_DIRS:
        return True
    if any(s in EXCLUDED_ANY_SEGMENT for s in segments[:-1]):
        return True
    if rel in EXCLUDED_EXACT or rel.startswith(EXCLUDED_PREFIXES):
        return True
    name = segments[-1]
    return any(fnmatch.fnmatch(name, p) for p in EXCLUDED_FILE_PATTERNS)


def collect(source: Path) -> list[str]:
    files = []
    for path in sorted(source.rglob("*")):
        if path.is_file() and not path.is_symlink():
            rel = path.relative_to(source).as_posix()
            if not is_excluded(rel):
                files.append(rel)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("homework", nargs="?", default="01")
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--list", action="store_true", help="print the included file list")
    args = parser.parse_args()

    nn = normalize_number(args.homework)
    source = args.source.resolve()
    out_dir = (args.output_dir or source / "dist").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"cse305_hw{nn}_231805033_231805026.zip"
    zip_path.unlink(missing_ok=True)

    files = collect(source)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in files:
            info = zipfile.ZipInfo.from_file(source / rel, rel)  # '/' separators; names stored as UTF-8
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(source / rel, "rb") as fh:
                zf.writestr(info, fh.read())
    if args.list:
        print("\n".join(files))
    print(f"Created submission archive: {zip_path} ({len(files)} files included)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
