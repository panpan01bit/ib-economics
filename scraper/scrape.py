#!/usr/bin/env python3
"""Scrape IB Economics resources from ibdocs.re (OpenList/AList REST API).

Usage:
    python3 scrape.py enumerate [--out data/kb/manifest.json]
    python3 scrape.py download  [--manifest data/kb/manifest.json] [--limit N]
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import requests

BASE = "https://ibdocs.re"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
RAW = PROJECT / "data" / "raw"
KB = PROJECT / "data" / "kb"

# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def new_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "application/json"})
    return s


def api_call(session, endpoint, payload, retries=5):
    """POST to the AList API with retry / exponential backoff."""
    url = BASE + endpoint
    for attempt in range(retries):
        try:
            r = session.post(url, json=payload, timeout=60)
            if r.status_code == 429 or r.status_code >= 500:
                wait = min(2 ** attempt * 2, 60)
                time.sleep(wait)
                continue
            r.raise_for_status()
            data = r.json()
            if data.get("code") != 200:
                raise RuntimeError(f"API error for {payload.get('path')}: {data}")
            return data
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            time.sleep(min(2 ** attempt * 2, 60))
    raise RuntimeError("unreachable")


def list_dir(session, path):
    data = api_call(session, "/api/fs/list",
                    {"path": path, "password": "", "page": 1, "per_page": 0, "refresh": False})
    return data["data"]["content"] or []


def get_raw_url(session, path):
    data = api_call(session, "/api/fs/get", {"path": path, "password": ""})
    return data["data"]["raw_url"]


# ---------------------------------------------------------------------------
# Recursive walk
# ---------------------------------------------------------------------------

def _walk(session, path, keep_dir, inside, depth, max_depth):
    """Shared recursive walker. `keep_dir(name, inside)` decides whether to
    descend into a directory. Yields (full_path, entry, inside_econ) for files;
    `inside_econ` is True when the file sits under an Economics-named folder."""
    if depth > max_depth:
        return
    try:
        entries = list_dir(session, path)
    except Exception as e:  # noqa: BLE001
        print(f"  ! walk failed {path}: {e}", file=sys.stderr)
        return
    for e in entries:
        full = f"{path}/{e['name']}".replace("//", "/")
        if e.get("is_dir"):
            now_inside = inside or ("economics" in e["name"].lower())
            if keep_dir(e["name"], now_inside):
                yield from _walk(session, full, keep_dir, now_inside, depth + 1, max_depth)
        else:
            yield full, e, inside


def walk_all(session, path, max_depth=8):
    """Descend into every directory (used for the Economics book folder)."""
    return _walk(session, path, keep_dir=lambda name, inside: True,
                 inside=True, depth=0, max_depth=max_depth)


_CONTAINER_KW = ("examination session", "session", "may", "november",
                 "subject guide", "subject report", "specimen", "guide",
                 "report", "first assessment", "first teaching",
                 "assessed student work", "internal assessment", "questionbank")


def is_container(name):
    n = name.lower()
    if "individual" in n or "group 3" in n or "group3" in n:
        return True
    if re.search(r"20\d{2}", n):
        return True
    return any(kw in n for kw in _CONTAINER_KW)


def walk_smart(session, path, max_depth=10):
    """Descend only into Economics/Group-3/container dirs; prune other subjects."""
    def keep_dir(name, inside):
        return inside or "economics" in name.lower() or is_container(name)
    return _walk(session, path, keep_dir=keep_dir, inside=False,
                 depth=0, max_depth=max_depth)


# ---------------------------------------------------------------------------
# Metadata parsing
# ---------------------------------------------------------------------------

PAPER_RE = re.compile(
    r"economics[_-]paper[_-](\d+)__?(?:TZ(\d+)_?)?(SL|HL)(?:_markscheme)?",
    re.IGNORECASE)


def parse_paper_name(name):
    """Return dict(paper, tz, level, markscheme) from a past-paper filename."""
    m = PAPER_RE.search(name)
    if not m:
        return {}
    return {
        "paper": int(m.group(1)),
        "tz": f"TZ{m.group(2)}" if m.group(2) else None,
        "level": m.group(3).upper(),
        "markscheme": "markscheme" in name.lower(),
    }


YEAR_RE = re.compile(r"(20\d{2})")


def year_from_path(path):
    m = YEAR_RE.search(path)
    return int(m.group(1)) if m else None


SESSION_RE = re.compile(r"/(May|November)\s+20\d{2}", re.IGNORECASE)

# non-English exam language versions (we keep English only)
_FOREIGN = re.compile(r"french|spanish|japanese|german|korean", re.IGNORECASE)


def is_english(name):
    return not _FOREIGN.search(name)


def session_from_path(path):
    m = SESSION_RE.search(path)
    if m:
        return "May" if m.group(1).lower() == "may" else "November"
    return None


def safe_local_name(name):
    name = name.replace("\x00", "")
    name = re.sub(r"[^\w.\-() ]+", "_", name, flags=re.UNICODE)
    return name.strip(" .")


# ---------------------------------------------------------------------------
# Category roots and filters
# ---------------------------------------------------------------------------

ROOTS = {
    "textbook": "/IB BOOKS/Group 3 - Individuals and Societies/Economics",
    "papers": "/IB PAST PAPERS - YEAR",
    "ia": "/IB ASSESSED STUDENT WORK/Group 3 - Individuals &amp; Societies",
    "guide": "/IB SUBJECT GUIDES",
    "specimen": "/IB SPECIMEN PAPERS",
    "report": "/IB SUBJECT REPORTS",
}

PDF_EXTS = (".pdf", ".epub", ".mobi", ".cbz")


def categorize(session):
    """Enumerate all Economics resources into a list of manifest dicts."""
    items = []

    # 1) Textbooks: everything under the Economics book folder (skip the
    #    redundant low-quality "ugly ebook" duplicate).
    p = ROOTS["textbook"]
    for full, e, _in in walk_all(session, p):
        if e.get("type") == 0 and e["name"].lower().endswith(PDF_EXTS) \
                and "ugly" not in e["name"].lower():
            publisher = full[len(p):].strip("/").split("/")[0]
            items.append(dict(
                category="textbook", remote_path=full, name=e["name"],
                size=e.get("size", 0), publisher=publisher,
                local_path=f"textbooks/{safe_local_name(publisher)}/{safe_local_name(e['name'])}",
            ))

    # 2) Past papers + markschemes (current syllabus: year >= 2022, English).
    p = ROOTS["papers"]
    for full, e, _in in walk_smart(session, p):
        name = e["name"]
        if e.get("type") != 0 or not name.lower().startswith("economics"):
            continue
        if not name.lower().endswith(".pdf") or not is_english(name):
            continue
        year = year_from_path(full)
        if year is None or year < 2022:
            continue
        meta = parse_paper_name(name)
        if not meta:
            continue
        session_name = session_from_path(full) or "Unknown"
        category = "markscheme" if meta["markscheme"] else "paper"
        items.append(dict(
            category=category, remote_path=full, name=name,
            size=e.get("size", 0), year=year, session=session_name,
            paper=meta["paper"], tz=meta["tz"], level=meta["level"],
            local_path=f"papers/{year}/{session_name}/{safe_local_name(name)}",
        ))

    # 3) IA examples.
    p = ROOTS["ia"]
    for full, e, inside in walk_smart(session, p):
        if e.get("type") == 0 and e["name"].lower().endswith(".pdf") \
                and (inside or "economics" in e["name"].lower()):
            rel = full[len(p):].strip("/")
            items.append(dict(
                category="ia", remote_path=full, name=e["name"],
                size=e.get("size", 0),
                local_path="ia/" + safe_local_name(rel),
            ))

    # 4) Subject guides / 5) specimen / 6) reports (English only).
    for cat, key in [("guide", "guide"), ("specimen", "specimen"),
                     ("report", "report")]:
        p = ROOTS[key]
        for full, e, inside in walk_smart(session, p):
            if e.get("type") == 0 and e["name"].lower().endswith(".pdf") \
                    and (inside or "economics" in e["name"].lower()) \
                    and is_english(e["name"]):
                rel = full[len(p):].strip("/")
                items.append(dict(
                    category=cat, remote_path=full, name=e["name"],
                    size=e.get("size", 0),
                    local_path=f"{cat}/" + safe_local_name(rel),
                ))

    return items


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def summarize(items):
    from collections import defaultdict
    agg = defaultdict(lambda: [0, 0])
    for it in items:
        agg[it["category"]][0] += 1
        agg[it["category"]][1] += it.get("size", 0)
    print("\n=== Enumeration summary ===")
    for cat in ("textbook", "paper", "markscheme", "ia", "guide",
                "specimen", "report"):
        c, s = agg[cat]
        if c:
            print(f"  {cat:14s} {c:5d} files  {human(s):>12s}")
    total = sum(it.get("size", 0) for it in items)
    print(f"  {'TOTAL':14s} {len(items):5d} files  {human(total):>12s}")


def cmd_enumerate(args):
    s = new_session()
    print("Enumerating ibdocs.re Economics resources ...")
    items = categorize(s)
    KB.mkdir(parents=True, exist_ok=True)
    out = args.out or str(KB / "manifest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Manifest written to {out} ({len(items)} items)")
    summarize(items)


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def cmd_download(args):
    manifest = args.manifest or str(KB / "manifest.json")
    with open(manifest, encoding="utf-8") as f:
        items = json.load(f)
    if args.categories:
        items = [it for it in items if it["category"] in args.categories]
    if args.limit:
        items = items[: args.limit]
    print(f"Downloading {len(items)} items ...")
    s = new_session()
    RAW.mkdir(parents=True, exist_ok=True)
    try:
        import tqdm  # type: ignore
    except ImportError:
        tqdm = None

    ok = skip = fail = 0
    it = tqdm.tqdm(items) if tqdm else items
    raw_root = RAW.resolve()
    for item in it:
        # local_path comes from the (possibly hand-edited) manifest: validate
        # segments and keep the resolved destination under data/raw/.
        rel = str(item["local_path"])
        if rel.startswith(("/", "\\")) or any(seg.startswith(".") for seg in rel.split("/")):
            print(f"\n  ! skipped unsafe local_path: {rel!r}", file=sys.stderr)
            fail += 1
            continue
        dest = (RAW / rel).resolve()
        if raw_root not in dest.parents:
            print(f"\n  ! local_path escapes data/raw/: {rel!r}", file=sys.stderr)
            fail += 1
            continue
        if dest.exists() and dest.stat().st_size == item.get("size", 0):
            skip += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            url = get_raw_url(s, item["remote_path"])
            r = s.get(url, stream=True, timeout=120)
            r.raise_for_status()
            with open(dest, "wb") as fh:
                for chunk in r.iter_content(1 << 20):
                    fh.write(chunk)
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"\n  ! failed {item['remote_path']}: {e}", file=sys.stderr)
            fail += 1
        time.sleep(args.sleep)
    print(f"\nDone. ok={ok} skipped={skip} failed={fail}")


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("enumerate", help="list all Economics resources")
    e.add_argument("--out")
    e.set_defaults(func=cmd_enumerate)

    d = sub.add_parser("download", help="download from manifest")
    d.add_argument("--manifest")
    d.add_argument("--categories", nargs="*",
                   choices=["textbook", "paper", "markscheme", "ia", "guide",
                            "specimen", "report"])
    d.add_argument("--limit", type=int)
    d.add_argument("--sleep", type=float, default=0.3)
    d.set_defaults(func=cmd_download)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
