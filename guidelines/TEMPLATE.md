# Document Template — Structure & Corrections
**Grail Message Foundation — Halls of Worship, Nigeria**

This is the single source of truth for how every Foundation document (reports,
guidelines, standards) is structured and styled. Start new documents from
[`_TEMPLATE.html`](_TEMPLATE.html); this file explains the structure and
records every correction made to the template so far.

---

## 1. Files that make the template

| File | Role |
|---|---|
| [`_TEMPLATE.html`](_TEMPLATE.html) | Blank skeleton with `{{TOKENS}}` and one example of every content block. Copy this to start. |
| [`style.css`](style.css) | All shared design (colours, fonts, masthead, meta card, tables, header/footer). **Never** put design rules in a document — only in here. |
| [`../reports/render-pdf.py`](../reports/render-pdf.py) | Renders any document to PDF, drawing the repeating header/footer and embedding fonts. |

## 2. How to make a new document

```
cp guidelines/_TEMPLATE.html guidelines/GMF-XX-001-my-document.html
# replace every {{TOKEN}}, delete unused content blocks
python3 reports/render-pdf.py \
    guidelines/GMF-XX-001-my-document.html \
    guidelines/GMF-XX-001-my-document.pdf \
    --ref GMF-XX-001 --kind "Guideline Document"
```

`--kind` is the label in the page header (e.g. `Guideline Document`,
`Report & Proposal`). `--ref` is the document reference shown in the header and
footer. Both default to the leadership report's values if omitted.

## 3. Fixed structure (in order)

1. **Masthead** — green band, `GRAIL MESSAGE FOUNDATION` wordmark (Bebas Neue),
   rust rule beneath, contact block top-right. Identical on every document.
2. **Kicker** — small rust uppercase label above the title.
3. **Title** — Bebas Neue, one or two lines.
4. **Meta card** — six cream cells. The **last cell is always `Prepared By`**.
   - Reports: Report Reference · Date · Classification · Prepared By · Department · (empty)
   - Guidelines: Document No. · Version · Date · Applies To · Status · Prepared By
5. **Content blocks** — any mix of the blocks in §4, sections numbered in the
   `<h2>` text (`01.`, `02.`, …).
6. **Revision History** — table, every document.
7. **Authorisation** — **`Prepared By` only.**
8. **Footer** — screen footer in the page; the print footer on every page is
   drawn by `render-pdf.py`.

## 4. Content blocks (CSS classes)

| Block | Class | Use for |
|---|---|---|
| Prose | `p.body` | ordinary paragraphs |
| Findings panel | `.finding` + `.num` | goals, findings, numbered highlights (cream panel, rust numerals) |
| Sequence | `.seq` + `.n` | ordered steps / phases (rust numerals, no panel) |
| Data table | `table.cost` | parameters, costs, schedules (green header). Modifier rows: `tr.sub`, `tr.total` |
| Table title | `h3.tbl-title` | rust caption above a table |
| Bullets | `ul.recs` / `ol.recs` | lists |
| Note box | `.note` | key rule / caveat (rust left border) |
| Code / tree | `pre.tree` | folder structures, naming schemes |

## 5. Brand tokens (defined in `style.css`)

| Token | Value | Use |
|---|---|---|
| `--green` | `#1C4636` | masthead, table headers, wordmark |
| `--rust` | `#B85C38` | accent rule, kickers, numerals |
| `--cream` | `#F5EFE8` | meta card, panels, table cells |
| `--sage` | `#AECFC0` | subtotal rows, masthead tag |
| Display font | **Bebas Neue** | wordmark, titles |
| Body font | **Inter** | everything else |

Fonts are fetched from Google Fonts and **embedded into the PDF** by the render
script, so output is self-contained and reproducible offline.

## 6. Record of corrections made to the template

These are the corrections applied over the course of development, newest first.
Any future change to the template's look or structure is added here.

| # | Correction | Where it lives now |
|---|---|---|
| 1 | Based the house style on the Osogbo project report (RPT-2026-OSG-001). | whole template |
| 2 | **Removed `Reviewed By` and `Approved By`** — authorisation and meta card carry **`Prepared By` only**. | `_TEMPLATE.html` meta card + authorisation |
| 3 | **Renamed the organisation** from *Grail Movement (Nigeria)* to **Grail Message Foundation** (new legal form) — masthead, contact block, header, footer and body. | masthead, `style.css` usage, `render-pdf.py` |
| 4 | **Repeating footer on every page** (was last page only) — drawn in the print bottom margin via Chromium's footer template. | `render-pdf.py` footer, `@page` margins |
| 5 | **Repeating header on every page** — wordmark left, `{{kind}} · {{ref}}` right, hairline rule; margins synced so it never overlaps body text. | `render-pdf.py` header, `style.css` `@page` |
| 6 | **Document codes changed `GMN-` → `GMF-`** across all documents, the project-code scheme, template codes and file names. | all documents + filenames |
| 7 | **Report reference `RPT-2026-GMN-001` → `RPT-2026-GMF-001`.** | report + `render-pdf.py` default |
| 8 | **`render-pdf.py` generalised** with `--ref` and `--kind` so each document carries its own reference/type in the header and footer; temp render file placed beside the source so `style.css` resolves. | `render-pdf.py` |
| 9 | **Shared stylesheet extracted** to `style.css` so no document holds its own design rules. | `style.css` |
| 10 | Trimmed Osogbo-specific cost references out of reused prose (report only, not structural). | report body |

## 7. Rules to keep the template consistent

- Do **not** add design rules inside a document — extend `style.css` instead.
- Keep the masthead, meta-card layout, header/footer and authorisation exactly
  as in `_TEMPLATE.html`; vary only the content blocks.
- `Prepared By` is the only signatory unless leadership directs otherwise.
- Keep `--ref` equal to the document's reference and repeat it in the screen
  footer's last span.
- Every document ends with **Revision History** then **Authorisation**.
