#!/usr/bin/env python3
"""Render the report HTML to PDF with the Grail Movement footer repeated at
the base of every page.

The footer is drawn with Chromium's native footer template so the page body
can never overlap it. Google Fonts are fetched and embedded locally before
rendering so the PDF is reproducible offline.

Usage:  python3 render-pdf.py <report.html> <output.pdf>
Requires: playwright (pip install playwright) and a Chromium install.
"""
import base64
import pathlib
import re
import subprocess
import sys
import tempfile
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
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    html = src.read_text()
    css = embedded_fonts_css()
    for link in (LINK1, LINK2, LINK2_RAW):
        html = html.replace(link, "")
    html = html.replace("</head>", f"<style>{css}</style></head>")

    header = f"""
    <style>{bebas_face(css)}</style>
    <div style="width:100%;font-family:Arial,sans-serif;font-size:8.5px;color:#4A4F5C;">
      <div style="margin:4mm 48px 0;padding-bottom:6px;border-bottom:1px solid #D1CBC6;
                  display:flex;justify-content:space-between;align-items:flex-end;">
        <span style="font-family:'Bebas Neue','Arial Narrow',Arial,sans-serif;
                     letter-spacing:3px;color:#1C4636;font-size:10px;">GRAIL MOVEMENT</span>
        <span>Report &amp; Proposal &middot; RPT-2026-GMN-001</span>
      </div>
    </div>"""

    footer = f"""
    <style>{bebas_face(css)}</style>
    <div style="width:100%;margin:0 0 4mm;padding:8px 48px 0;border-top:1px solid #D1CBC6;
                font-family:Arial,sans-serif;font-size:8.5px;color:#4A4F5C;
                display:flex;justify-content:space-between;align-items:center;">
      <span>Grail Movement &middot; Halls of Worship, Nigeria</span>
      <span style="font-family:'Bebas Neue','Arial Narrow',Arial,sans-serif;
                   letter-spacing:3px;color:#1C4636;font-size:10px;">GRAIL MOVEMENT</span>
      <span>RPT-2026-GMN-001</span>
    </div>"""

    from playwright.sync_api import sync_playwright

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        page_path = f.name

    with sync_playwright() as p:
        import os, shutil
        exe = os.environ.get("CHROMIUM_PATH") or shutil.which("chromium") or "/opt/pw-browsers/chromium"
        browser = p.chromium.launch(executable_path=exe)
        page = browser.new_page()
        page.goto(f"file://{page_path}")
        page.pdf(
            path=str(out),
            format="A4",
            display_header_footer=True,
            header_template=header,
            footer_template=footer,
            margin={"top": "17mm", "bottom": "20mm", "left": "0", "right": "0"},
            print_background=True,
        )
        browser.close()
    print(f"written: {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
