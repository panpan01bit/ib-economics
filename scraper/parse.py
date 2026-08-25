#!/usr/bin/env python3
"""Parse downloaded PDFs -> page-delimited text + TOC bookmarks + metadata.

Resumable: files whose text already exists are reused (only TOC + page count are
re-read). Scanned textbooks/IA are slow & text-poor, so their text extraction is
capped (or skipped); chapter->topic mapping relies on TOC bookmarks instead.

Usage:
    python3 parse.py [--manifest data/kb/manifest.json] [--limit N]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
RAW = PROJECT / "data" / "raw"
TEXT = PROJECT / "data" / "text"
KB = PROJECT / "data" / "kb"
SITE = PROJECT / "site"

PAGE_SEP = "\x0c"  # form feed separates pages in extracted text

# Text-read cap per category. 0 = skip text entirely (scanned textbooks);
# positive = read at most N pages; None/absent = full text (papers, IA, ...).
MAX_PAGES_BY_CAT = {"textbook": 0}


def read_toc(doc):
    toc = []
    for lvl, title, pg in doc.get_toc():
        toc.append({"level": lvl, "title": title.strip(), "page": pg})
    return toc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(KB / "manifest.json"))
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    with open(args.manifest, encoding="utf-8") as f:
        items = json.load(f)
    if args.limit:
        items = items[: args.limit]

    TEXT.mkdir(parents=True, exist_ok=True)
    KB.mkdir(parents=True, exist_ok=True)

    meta = []
    done = reused = skip = fail = 0
    for it in items:
        src = (RAW / it["local_path"]).resolve()
        if RAW.resolve() not in src.parents:
            skip += 1
            continue
        if not src.exists() or src.suffix.lower() != ".pdf":
            skip += 1
            continue
        max_pages = MAX_PAGES_BY_CAT.get(it["category"], None)
        txt_rel = None
        txt_path = None
        if max_pages != 0:  # 0 = skip text entirely
            txt_rel = it["local_path"][: -len(src.suffix)] + ".txt"
            txt_path = (TEXT / txt_rel).resolve()
            text_root = TEXT.resolve()
            if text_root not in txt_path.parents:
                skip += 1
                continue
            txt_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            doc = fitz.open(str(src))
            n = doc.page_count
            toc = read_toc(doc)
            chars = 0
            cover = None
            # generate a small cover thumbnail for textbooks (professional look)
            if it["category"] == "textbook" and n > 0:
                cover_rel = ("assets/covers/" +
                             re.sub(r"[^\w\-]+", "_", it["name"])[:120] + ".png")
                cover_path = (SITE / cover_rel).resolve()
                if SITE.resolve() not in cover_path.parents:
                    cover_rel = None
                else:
                    cover_path.parent.mkdir(parents=True, exist_ok=True)
                if not cover_path.exists():
                    try:
                        pix = doc.load_page(0).get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
                        pix.save(str(cover_path))
                    except Exception:
                        cover_rel = None
                cover = cover_rel
            if txt_path and not txt_path.exists():
                pages_to_read = n if max_pages is None else min(max_pages, n)
                pages = [doc.load_page(i).get_text("text") for i in range(pages_to_read)]
                doc.close()
                with open(txt_path, "w", encoding="utf-8") as f:
                    for p in pages:
                        f.write(p)
                        f.write(PAGE_SEP)
                chars = sum(len(p) for p in pages)
                done += 1
            elif txt_path:
                doc.close()
                chars = txt_path.stat().st_size  # reuse existing
                reused += 1
            else:
                doc.close()
            m = dict(it)
            m.update({"pages": n, "chars": chars, "toc": toc, "text_rel": txt_rel,
                      "cover": cover,
                      "partial": max_pages is not None and max_pages > 0 and n > max_pages})
            meta.append(m)
        except Exception as e:  # noqa: BLE001
            print(f"  ! parse failed {src}: {e}", file=sys.stderr)
            fail += 1

    out = KB / "pdf_meta.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Parsed {done} fresh, reused {reused}, skipped {skip} (no-text/other), failed {fail}.")
    print(f"Metadata written to {out}")


if __name__ == "__main__":
    main()
