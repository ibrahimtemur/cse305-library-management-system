# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Generates leak-free, print-ready PDFs from Markdown with base64 embedded images, sanitized plain-text repo links, verified internal page anchors, and generic landscape sections across Linux and Windows.


import argparse
import base64
import glob
import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from typing import List, Optional, Tuple

from pypdf import PdfReader


PUBLIC_GITHUB_REPO_URL = "https://github.com/ibrahimtemur/cse305-library-management-system"
PUBLIC_TRELLO_BOARD_URL = "https://trello.com/b/34K6O3Y1/cse305-lms-sprint-board"
ALLOWED_EXTERNAL_URLS = {
    PUBLIC_GITHUB_REPO_URL,
    PUBLIC_TRELLO_BOARD_URL,
}

LEAK_PATTERNS = [
    "file://",
    "c:\\users",
    "c:/users",
    "users\\ibrah",
    "users/ibrah",
    "onedrive",
    "antigravity",
    ".gemini",
    "scratch",
]

KNOWN_CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_chrome() -> str:
    env_path = os.environ.get("CHROME_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path
    for cmd in ["chromium", "chromium-browser", "google-chrome", "chrome", "msedge"]:
        which_path = shutil.which(cmd)
        if which_path and os.path.isfile(which_path):
            return which_path
    pw_globs = [
        os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome"),
        os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-win/chrome.exe"),
    ]
    for pattern in pw_globs:
        matches = sorted(glob.glob(pattern), reverse=True)
        for m in matches:
            if os.path.isfile(m):
                return m
    for p in KNOWN_CHROME_PATHS:
        if os.path.isfile(p):
            return p
    raise RuntimeError(
        "Chrome or Chromium executable not found. Please install Chromium/Google Chrome "
        "or set the CHROME_PATH environment variable."
    )


def github_slugify(text: str) -> str:
    plain = re.sub(r"<[^>]+>", "", text).strip()
    plain = plain.replace("&amp;", "")
    plain = plain.replace(" — ", "--").replace(" – ", "--").replace("—", "-").replace("–", "-")
    plain = plain.lower()
    plain = re.sub(r"[^\w\s\-]", "", plain)
    plain = re.sub(r"\s+", "-", plain)
    return plain


def extract_header_metadata(md_text: str) -> Tuple[str, str]:
    general_comments = (
        "Single HW01 submission document consolidating the Problem Description, "
        "the Solution Outline, and the conceptual Domain Model of the CSE305 Library Management System."
    )
    m_comment = re.search(r"General Comments:\s*(.+)", md_text)
    if m_comment:
        general_comments = m_comment.group(1).strip()

    doc_title = "CSE305 HW01 — Problem Description, Solution Outline, and Domain Model (v1.2)"
    m_h1 = re.search(r"^#\s+(.+)$", md_text, flags=re.MULTILINE)
    if m_h1:
        doc_title = re.sub(r"[`*_]", "", m_h1.group(1)).strip()

    return general_comments, doc_title


def render_markdown_to_html(md_text: str) -> str:
    # Support generic landscape markers <!-- landscape:start --> ... <!-- landscape:end -->
    md_prepared = re.sub(
        r"<!--\s*landscape:start\s*-->",
        '<div class="dm-landscape-section">',
        md_text,
        flags=re.IGNORECASE,
    )
    md_prepared = re.sub(
        r"<!--\s*landscape:end\s*-->",
        "</div>",
        md_prepared,
        flags=re.IGNORECASE,
    )

    npx_cmd = "npx.cmd" if sys.platform == "win32" else "npx"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", encoding="utf-8", delete=False
    ) as tf_in, tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8", delete=False
    ) as tf_out:
        tf_in.write(md_prepared)
        temp_md_path = tf_in.name
        temp_html_path = tf_out.name
    try:
        proc = subprocess.run(
            [npx_cmd, "--yes", "marked@18.1.2", "--gfm", "-i", temp_md_path, "-o", temp_html_path],
            text=True,
            encoding="utf-8",
            capture_output=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"marked@18.1.2 failed with code {proc.returncode}:\n{proc.stderr}")
        return pathlib.Path(temp_html_path).read_text(encoding="utf-8")
    finally:
        for p in (temp_md_path, temp_html_path):
            if os.path.exists(p):
                os.remove(p)


def sanitize_links_and_structure(
    body_html: str,
    repo_root: pathlib.Path,
    doc_dir: pathlib.Path,
) -> Tuple[str, List[Tuple[str, str]]]:
    # 1. Transform GitHub alert blockquotes ([!NOTE], [!IMPORTANT], [!WARNING], [!TIP], [!CAUTION])
    alert_labels = {
        "NOTE": "Note",
        "IMPORTANT": "Important",
        "WARNING": "Warning",
        "TIP": "Tip",
        "CAUTION": "Caution",
    }
    for key, label in alert_labels.items():
        body_html = body_html.replace(
            f"<blockquote>\n<p>[!{key}]\n",
            f'<blockquote class="gh-note gh-{key.lower()}">\n<p><strong class="gh-note-title">{label}</strong><br>',
        )

    # 2. Inject explicit IDs into all headings so TOC anchors resolve reliably
    def add_heading_id(match: re.Match) -> str:
        level = match.group(1)
        attrs = match.group(2) or ""
        inner = match.group(3)
        slug = github_slugify(inner)
        if "id=" in attrs:
            return match.group(0)
        return f'<h{level}{attrs} id="{slug}">{inner}</h{level}>'

    body_html = re.sub(
        r"<h([1-6])([^>]*)>(.*?)</h\1>",
        add_heading_id,
        body_html,
        flags=re.DOTALL,
    )

    # Collect all available heading IDs
    available_ids = set(re.findall(r'<h[1-6][^>]*\sid=["\']([^"\']+)["\']', body_html))

    # 3. Process <a> tags
    toc_links: List[Tuple[str, str]] = []

    def replace_a_tag(match: re.Match) -> str:
        href = match.group("href").strip()
        content = match.group("content").strip()

        # Case A: Public GitHub repository link or Trello board link (allowed external links)
        if "github.com/ibrahimtemur/cse305-library-management-system" in href:
            return f'<a href="{PUBLIC_GITHUB_REPO_URL}"><code>{PUBLIC_GITHUB_REPO_URL}</code></a>'
        if "trello.com/b/34K6O3Y1" in href:
            return f'<a href="{PUBLIC_TRELLO_BOARD_URL}"><code>{PUBLIC_TRELLO_BOARD_URL}</code></a>'

        # Case B: Internal page anchor
        if href.startswith("#"):
            target_id = href[1:]
            if target_id in available_ids:
                plain_title = re.sub(r"<[^>]+>", "", content)
                toc_links.append((plain_title, target_id))
                return f'<a href="#{target_id}">{content}</a>'
            return content

        # Case C: Other external http/https links (e.g., Open Library, ADU rule citations) -> plain code text
        if href.startswith("http://") or href.startswith("https://"):
            return f"<code>{href}</code>"

        # Case D: Repository-relative file links (e.g., .md, .svg, .mmd, README)
        anchor_part = ""
        path_part = href
        if "#" in href:
            path_part, anchor_part = href.split("#", 1)
        target_path = (doc_dir / path_part).resolve() if path_part else doc_dir.resolve()
        try:
            repo_rel = target_path.relative_to(repo_root).as_posix()
        except ValueError:
            repo_rel = path_part or href

        extra_match = re.search(r"(?:</code>|\b)(\s*§\s*[\d\.]+.*)$", content)
        extra_text = extra_match.group(1) if extra_match else ""

        return f"<code>{repo_rel}</code>{extra_text}"

    a_pattern = re.compile(
        r'<a\s+[^>]*href=["\'](?P<href>[^"\']+)["\'][^>]*>(?P<content>.*?)</a>',
        re.DOTALL,
    )
    body_html = a_pattern.sub(replace_a_tag, body_html)

    # 4. Backward-compatible fallback: wrap HW01 §3.1 Class Diagram in landscape if no explicit marker exists
    if 'class="dm-landscape-section"' not in body_html:
        target_start = '<h2 id="31-class-diagram">3.1 Class Diagram</h2>'
        target_end = '<h2 id="32-enumerations">3.2 Enumerations</h2>'
        if target_start in body_html and target_end in body_html:
            body_html = body_html.replace(
                target_start,
                f'<div class="dm-landscape-section">\n{target_start}',
                1,
            )
            body_html = body_html.replace(
                target_end,
                f"</div>\n{target_end}",
                1,
            )
        else:
            body_html = re.sub(
                r'(<h2[^>]*>3\.1 Class Diagram</h2>)',
                r'<div class="dm-landscape-section">\n\1',
                body_html,
                count=1,
            )
            body_html = re.sub(
                r'(<h2[^>]*>3\.2 Enumerations</h2>)',
                r'</div>\n\1',
                body_html,
                count=1,
            )

    # 5. Inline local images as base64 Data URIs
    def replace_img_src(match: re.Match) -> str:
        src = match.group("src").strip()
        if src.startswith("data:") or src.startswith("http"):
            return match.group(0)
        img_file = (doc_dir / src).resolve()
        if not img_file.is_file():
            img_file = (repo_root / src).resolve()
        if not img_file.is_file():
            raise FileNotFoundError(f"Referenced image file does not exist: {src}")

        ext = img_file.suffix.lower().lstrip(".")
        mime = "image/svg+xml" if ext == "svg" else f"image/{ext}"
        b64 = base64.b64encode(img_file.read_bytes()).decode("ascii")
        return f'src="data:{mime};base64,{b64}"'

    img_pattern = re.compile(r'src=["\'](?P<src>[^"\']+)["\']')
    body_html = img_pattern.sub(replace_img_src, body_html)

    return body_html, toc_links


def build_full_html_document(body_html: str, general_comments: str, doc_title: str) -> str:
    header_banner = f"""<div class="cse305-header">
<div><strong>Name(s) Surname(s) :</strong> Ibrahim Temur, Omer Faruk Kuş</div>
<div><strong>Student No(s)# :</strong> 231805033, 231805026</div>
<div><strong>General Comments :</strong> {general_comments}</div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{doc_title}</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 14mm 14mm 14mm 14mm;
  }}
  @page dm-landscape {{
    size: A4 landscape;
    margin: 10mm 12mm 10mm 12mm;
  }}
  .dm-landscape-section {{
    page: dm-landscape;
    page-break-before: always;
    break-before: page;
    page-break-after: always;
    break-after: page;
  }}
  .dm-landscape-section img {{
    display: block;
    margin: 6px auto;
    max-width: 100%;
    max-height: 152mm;
    width: auto;
    height: auto;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  body {{
    font-family: "Segoe UI", "DejaVu Sans", "Liberation Sans", "Noto Sans", -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.42;
    color: #1f2328;
    margin: 0;
    padding: 0;
  }}
  .cse305-header {{
    font-family: Consolas, "DejaVu Sans Mono", "Liberation Mono", "Courier New", monospace;
    font-size: 8.5pt;
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-left: 4px solid #1f2328;
    border-radius: 4px;
    padding: 6px 10px;
    margin-bottom: 10px;
    line-height: 1.35;
  }}
  h1 {{
    font-size: 16pt;
    border-bottom: 2px solid #d0d7de;
    padding-bottom: 4px;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
    break-after: avoid;
  }}
  h1:first-of-type {{
    margin-top: 0;
  }}
  h2 {{
    font-size: 12.5pt;
    border-bottom: 1px solid #d8dee4;
    padding-bottom: 3px;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
    break-after: avoid;
  }}
  h3 {{
    font-size: 10.5pt;
    margin-top: 10px;
    margin-bottom: 4px;
    page-break-after: avoid;
    break-after: avoid;
  }}
  p, ul, ol {{
    margin-top: 4px;
    margin-bottom: 6px;
  }}
  li {{
    margin-bottom: 2px;
  }}
  blockquote.gh-note {{
    margin: 8px 0;
    padding: 8px 12px;
    border-left: 4px solid #0969da;
    background-color: #f6f8fa;
    border-radius: 0 4px 4px 0;
  }}
  blockquote.gh-warning {{
    border-left-color: #9a6700;
  }}
  blockquote.gh-important {{
    border-left-color: #8250df;
  }}
  .gh-note-title {{
    color: #0969da;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 6px;
    margin-bottom: 10px;
    font-size: 8.5pt;
  }}
  th, td {{
    border: 1px solid #d0d7de;
    padding: 4px 6px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background-color: #f6f8fa;
    font-weight: 600;
  }}
  tr {{
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  code {{
    font-family: Consolas, "DejaVu Sans Mono", "Liberation Mono", "Courier New", monospace;
    font-size: 8.3pt;
    background-color: #f6f8fa;
    padding: 1px 3px;
    border-radius: 3px;
  }}
  pre {{
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 4px;
    padding: 6px 8px;
    font-size: 8pt;
    overflow-x: auto;
  }}
  pre code {{
    background: none;
    padding: 0;
  }}
  img {{
    display: block;
    margin: 8px auto;
    max-width: 100%;
    max-height: 225mm;
    width: auto;
    height: auto;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  details {{
    margin: 4px 0 8px 0;
    font-size: 8.5pt;
    color: #57606a;
  }}
  hr {{
    border: 0;
    border-top: 1px solid #d0d7de;
    margin: 12px 0;
  }}
  a {{
    color: #0969da;
    text-decoration: none;
  }}
</style>
</head>
<body>
{header_banner}
{body_html}
</body>
</html>
"""


def validate_pdf_integrity_and_leaks(
    pdf_path: pathlib.Path,
    expected_pages: Optional[int] = None,
    max_pages: Optional[int] = None,
) -> Tuple[int, List[Tuple[str, str, int]]]:
    reader = PdfReader(str(pdf_path))
    page_count = len(reader.pages)
    if expected_pages is not None and page_count != expected_pages:
        raise ValueError(f"Expected {expected_pages} pages in PDF, but found {page_count}")
    if max_pages is not None and page_count > max_pages:
        raise ValueError(f"PDF page count {page_count} exceeds maximum allowed {max_pages} pages")

    # 1. Check metadata
    meta = reader.metadata or {}
    for key, value in meta.items():
        val_str = str(value)
        val_lower = val_str.lower()
        for pat in LEAK_PATTERNS:
            if pat.lower() in val_lower:
                raise RuntimeError(
                    f"Leak pattern '{pat}' detected in PDF metadata field '{key}': {val_str}"
                )

    # 2. Check extracted text on each page
    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        txt = page.extract_text() or ""
        txt_lower = txt.lower()
        for pat in LEAK_PATTERNS:
            if pat.lower() in txt_lower:
                raise RuntimeError(
                    f"Leak pattern '{pat}' detected in extracted text on Page {page_num}"
                )

    # 3. Check link annotations & resolve internal destinations and allowlisted external links
    resolved_links: List[Tuple[str, str, int]] = []
    named_dests = reader.named_destinations

    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        if "/Annots" in page:
            for annot_ref in page["/Annots"]:
                annot = annot_ref.get_object()
                if annot.get("/Subtype") == "/Link":
                    action = annot.get("/A")
                    if action and "/URI" in action:
                        uri = str(action["/URI"])
                        if uri not in ALLOWED_EXTERNAL_URLS:
                            raise RuntimeError(
                                f"Unexpected clickable /URI link found on Page {page_num}: {uri}. "
                                f"Only allowlisted external links ({ALLOWED_EXTERNAL_URLS}) are permitted as external links."
                            )
                        resolved_links.append(("EXTERNAL", uri, page_num))

                    dest = annot.get("/Dest")
                    if dest:
                        dest_key = str(dest)
                        dest_obj = named_dests.get(dest_key)
                        if dest_obj is None and dest_key.startswith("/"):
                            dest_obj = named_dests.get(dest_key[1:])
                        if dest_obj is None:
                            for k, v in named_dests.items():
                                if k.strip("/") == dest_key.strip("/"):
                                    dest_obj = v
                                    break

                        if dest_obj is not None:
                            target_page_idx = reader.get_destination_page_number(dest_obj)
                            target_page_num = target_page_idx + 1
                            resolved_links.append(("INTERNAL", dest_key.lstrip("/"), target_page_num))
                        else:
                            raise RuntimeError(
                                f"Internal anchor destination '{dest_key}' on Page {page_num} could not be resolved!"
                            )

    return page_count, resolved_links


def export_pdf(
    input_md: pathlib.Path,
    output_pdf: pathlib.Path,
    root_pdf: Optional[pathlib.Path] = None,
    expected_pages: Optional[int] = None,
    max_pages: Optional[int] = None,
) -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    chrome_path = find_chrome()

    if not input_md.is_file():
        raise FileNotFoundError(f"Input markdown file not found: {input_md}")

    md_text = input_md.read_text(encoding="utf-8")
    general_comments, doc_title = extract_header_metadata(md_text)
    body_html = render_markdown_to_html(md_text)
    body_html, toc_links = sanitize_links_and_structure(body_html, repo_root, input_md.parent)
    full_html = build_full_html_document(body_html, general_comments, doc_title)

    with tempfile.TemporaryDirectory() as td:
        temp_dir = pathlib.Path(td)
        temp_html = temp_dir / "print_doc.html"
        temp_pdf = temp_dir / "output.pdf"

        temp_html.write_text(full_html, encoding="utf-8")

        chrome_cmd = [
            chrome_path,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
        ]
        if sys.platform != "win32":
            chrome_cmd.extend(["--no-sandbox", "--disable-dev-shm-usage"])
        chrome_cmd.extend([f"--print-to-pdf={temp_pdf}", str(temp_html)])

        proc_chrome = subprocess.run(chrome_cmd, capture_output=True, text=True)
        if proc_chrome.returncode != 0:
            raise RuntimeError(
                f"Chromium headless PDF export failed ({proc_chrome.returncode}):\n{proc_chrome.stderr}"
            )

        page_count, resolved_links = validate_pdf_integrity_and_leaks(
            temp_pdf,
            expected_pages=expected_pages,
            max_pages=max_pages,
        )

        output_pdf.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(temp_pdf, output_pdf)

        if root_pdf:
            root_pdf.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(temp_pdf, root_pdf)

    hash_out = hashlib.sha256(output_pdf.read_bytes()).hexdigest()
    print(f"[OK] Browser: {chrome_path}")
    print(f"[OK] Generated {output_pdf} (pages: {page_count}, size: {output_pdf.stat().st_size} bytes)")
    print(f"     SHA-256: {hash_out}")

    if root_pdf:
        hash_root = hashlib.sha256(root_pdf.read_bytes()).hexdigest()
        print(f"[OK] Generated {root_pdf} (pages: {page_count}, size: {root_pdf.stat().st_size} bytes)")
        print(f"     SHA-256: {hash_root}")
        if hash_out != hash_root:
            raise ValueError("SHA-256 hashes of output PDFs do not match!")
        print("[OK] Identical SHA-256 hash verified across both PDF files.")

    print("[OK] Leak scan passed: 0 occurrences of forbidden patterns across metadata, page text, and annotations.")
    print(f"\n--- Document Link Annotations Audit ({len(resolved_links)} links) ---")
    print(f"{'Type':<10} | {'Destination / Target':<65} | {'Page'}")
    print("-" * 85)
    for link_type, target, target_page in resolved_links:
        print(f"{link_type:<10} | {target:<65} | Page {target_page}")


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Export CSE305 Markdown documents to PDF.")
    parser.add_argument(
        "--input",
        "-i",
        type=pathlib.Path,
        default=repo_root / "docs" / "01-proposal" / "HW01_Problem_Solution_DomainModel.md",
        help="Input markdown file.",
    )
    parser.add_argument(
        "--docs-output",
        "--output",
        "-o",
        dest="docs_output",
        type=pathlib.Path,
        default=repo_root / "docs" / "01-proposal" / "HW01_Problem_Solution_DomainModel.pdf",
        help="Output PDF file in docs/.",
    )
    parser.add_argument(
        "--root-output",
        type=str,
        default=None,
        help="Optional root-level copy of the output PDF.",
    )
    parser.add_argument(
        "--expected-pages",
        type=int,
        default=None,
        help="Optional exact expected page count.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional maximum allowed page count.",
    )

    args = parser.parse_args()
    default_hw01_input = repo_root / "docs" / "01-proposal" / "HW01_Problem_Solution_DomainModel.md"
    root_path: Optional[pathlib.Path] = None
    if args.root_output is not None and args.root_output.strip() != "":
        root_path = pathlib.Path(args.root_output)
    elif args.root_output is None and args.input.resolve() == default_hw01_input.resolve() and "--docs-output" not in sys.argv and "--output" not in sys.argv and "-o" not in sys.argv:
        root_path = repo_root / "HW01_Problem_Solution_DomainModel.pdf"

    export_pdf(
        input_md=args.input,
        output_pdf=args.docs_output,
        root_pdf=root_path,
        expected_pages=args.expected_pages,
        max_pages=args.max_pages,
    )


if __name__ == "__main__":
    main()
