#!/usr/bin/env python3
"""Render a Grail Message Foundation document (report or guideline) to PDF
with the branded header and footer repeated on every page.

The header/footer are drawn with Chromium's native templates so the page body
can never overlap them. Google Fonts are fetched and embedded locally before
rendering so the PDF is reproducible offline.

Usage:
    python3 render-pdf.py <input.html> <output.pdf> [--ref REF] [--kind KIND]

    --ref   document reference shown in header/footer (default RPT-2026-GMN-001)
    --kind  document type shown in the header (default "Report & Proposal")

Requires: playwright (pip install playwright) and a Chromium install.
"""
import argparse
import base64
import os
import pathlib
import re
import shutil
import urllib.request

GF_CSS_URL = ("https://fonts.googleapis.com/css2"
              "?family=Bebas+Neue&family=Inter:wght@400;500;600;700&display=swap")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36"
LINK1 = '<link rel="preconnect" href="https://fonts.googleapis.com">'
LINK2 = f'<link href="{GF_CSS_URL.replace("&", "&amp;")}" rel="stylesheet">'
LINK2_RAW = f'<link href="{GF_CSS_URL}" rel="stylesheet">'


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req) as r:
        return r.read()


def embedded_fonts_css() -> str:
    css = fetch(GF_CSS_URL).decode()

    def embed(m):
        data = base64.b64encode(fetch(m.group(1))).decode()
        return f"url(data:font/woff2;base64,{data})"

    return re.sub(r"url\((https://[^)]+)\)", embed, css)


def bebas_face(css: str) -> str:
    m = re.search(r"@font-face\s*{[^}]*Bebas[^}]*}", css)
    return m.group(0) if m else ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=pathlib.Path)
    ap.add_argument("out", type=pathlib.Path)
    ap.add_argument("--ref", default="RPT-2026-GMN-001")
    ap.add_argument("--kind", default="Report & Proposal")
    args = ap.parse_args()

    html = args.src.read_text()
    css = embedded_fonts_css()
    for link in (LINK1, LINK2, LINK2_RAW):
        html = html.replace(link, "")
    html = html.replace("</head>", f"<style>{css}</style></head>")

    kind = args.kind.replace("&", "&amp;")
    header = f"""
    <style>{bebas_face(css)}</style>
    <div style="width:100%;font-family:Arial,sans-serif;font-size:8.5px;color:#4A4F5C;">
      <div style="margin:4mm 48px 0;padding-bottom:6px;border-bottom:1px solid #D1CBC6;
                  display:flex;justify-content:space-between;align-items:flex-end;">
        <span style="font-family:'Bebas Neue','Arial Narrow',Arial,sans-serif;
                     letter-spacing:3px;color:#1C4636;font-size:10px;">GRAIL MESSAGE FOUNDATION</span>
        <span>{kind} &middot; {args.ref}</span>
      </div>
    </div>"""

    footer = f"""
    <style>{bebas_face(css)}</style>
    <div style="width:100%;margin:0 0 4mm;padding:8px 48px 0;border-top:1px solid #D1CBC6;
                font-family:Arial,sans-serif;font-size:8.5px;color:#4A4F5C;
                display:flex;justify-content:space-between;align-items:center;">
      <span>Grail Message Foundation &middot; Halls of Worship, Nigeria</span>
      <span style="font-family:'Bebas Neue','Arial Narrow',Arial,sans-serif;
                   letter-spacing:3px;color:#1C4636;font-size:10px;">GRAIL MESSAGE FOUNDATION</span>
      <span>{args.ref}</span>
    </div>"""

    from playwright.sync_api import sync_playwright

    # temp file lives beside the source so relative links (style.css) resolve
    tmp = args.src.with_name(f".render-tmp-{args.src.name}")
    tmp.write_text(html)
    try:
        with sync_playwright() as p:
            exe = (os.environ.get("CHROMIUM_PATH") or shutil.which("chromium")
                   or "/opt/pw-browsers/chromium")
            browser = p.chromium.launch(executable_path=exe)
            page = browser.new_page()
            page.goto(f"file://{tmp.resolve()}")
            page.pdf(
                path=str(args.out),
                format="A4",
                display_header_footer=True,
                header_template=header,
                footer_template=footer,
                margin={"top": "17mm", "bottom": "20mm", "left": "0", "right": "0"},
                print_background=True,
            )
            browser.close()
    finally:
        tmp.unlink(missing_ok=True)
    print(f"written: {args.out} ({args.out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
