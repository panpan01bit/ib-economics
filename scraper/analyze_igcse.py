#!/usr/bin/env python3
"""Analyze the local IGCSE 0450 past-paper library.

Scans data/raw/igcse-0450/<year>/<session>/0450_<code>_<yy>_<type><variant>.pdf,
extracts question-paper text, tags each paper with syllabus topics (keyword
scoring), pairs qp with its mark scheme and the session's examiner report,
and writes data/kb/subjects/igcse-papers.json (+ heat merged by build_subjects).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import fitz  # PyMuPDF

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
RAW = PROJECT / "data" / "raw" / "igcse-0450"
KB = PROJECT / "data" / "kb" / "subjects"

SESSION_MAP = {"s": "May/June", "w": "Oct/Nov", "m": "March"}

# topic id -> scoring keywords (case-insensitive substrings)
KEYWORDS = {
    "IG1.1": ["business objective", "added value", "opportunity cost", "specialis", "division of labour",
              "survival", "market share", "scarcity"],
    "IG1.2": ["sole trader", "partnership", "limited liability", "private limited", "public limited",
              "franchise", "joint venture", "unlimited liability", "incorporat", "shareholder"],
    "IG1.3": ["merger", "takeover", "horizontal integration", "vertical integration", "conglomerate",
              "economies of scale", "external growth", "internal growth", "retention"],
    "IG1.4": ["stakeholder", "mixed economy", "public sector", "private sector", "privatis"],
    "IG1.5": ["communication", "information technolog", "email"],
    "IG2.1": ["recruit", "selection", "training", "part-time", "full-time", "redundan", "dismissal",
              "workforce", "job description", "person specification", "employment contract", "interview"],
    "IG2.2": ["motivat", "maslow", "herzberg", "taylor", "incentive", "job enrichment", "job rotation",
              "empower", "piece rate", "bonus"],
    "IG2.3": ["leadership", "autocratic", "democratic", "laissez", "management style", "organisational structure",
              "organizational structure", "span of control", "chain of command", "delayering", "matrix",
              "trade union", "collective bargaining", "centralis", "decentralis"],
    "IG3.1": ["mass market", "niche", "market orient", "product orient", "customer need", "consumer need",
              "market segment", "elasticity", "elastic"],
    "IG3.2": ["market research", "primary research", "secondary research", "quantitative", "qualitative",
              "survey", "questionnaire", "focus group", "sample"],
    "IG3.3": ["product life cycle", "extension strateg", "brand", "packaging", "product mix", "differentiat",
              "new product develop"],
    "IG3.4": ["pricing", "penetration", "skimming", "cost-plus", "cost plus", "competitive pricing",
              "promotional pricing", "psychological pricing", "price war", "loss leader"],
    "IG3.5": ["advertis", "promotion", "above-the-line", "above the line", "below-the-line", "below the line",
              "sales promotion", "sponsorship", "public relation", "social media", "brand aware"],
    "IG3.6": ["distribution", "channel", "retailer", "wholesaler", "e-commerce", "ecommerce", "online shopp",
              "website"],
    "IG3.7": ["marketing strateg", "legal control", "consumer protection", "misleading"],
    "IG4.1": ["production", "productivity", "lean", "just-in-time", "just in time", "quality control",
              "quality assurance", "stock", "inventory", "batch production", "flow production", "job production"],
    "IG4.2": ["break-even", "break even", "fixed cost", "variable cost", "contribution", "margin of safety",
              "total cost", "revenue"],
    "IG4.3": ["location", "relocat"],
    "IG5.1": ["source of finance", "overdraft", "loan", "share issue", "retained profit", "venture capital",
              "micro-finance", "microfinance", "crowdfund", "leasing", "trade credit", "debenture",
              "capital expenditure"],
    "IG5.2": ["cash flow", "cash-flow", "working capital", "net cash"],
    "IG5.3": ["income statement", "profit and loss", "gross profit", "net profit", "dividend"],
    "IG5.4": ["balance sheet", "current asset", "non-current asset", "current liabilit", "long-term liabilit",
              "net asset", "capital employ"],
    "IG5.5": ["ratio", "gross profit margin", "net profit margin", "return on capital", "current ratio",
              "acid test", "profitability", "liquidity ratio"],
    "IG5.6": ["use of account", "interested part"],
    "IG6.1": ["recession", "inflation", "unemployment", "exchange rate", "interest rate", "economic growth",
              "economic cycle", "deflation", "export", "import", "tariff", "taxation"],
    "IG6.2": ["environment", "ethical", "social responsibility", "sustainab", "pollut", "waste", "recycl"],
    "IG6.3": ["globalis", "multinational", "mnc", "international econom", "competitiven", "foreign firm",
              "transnational"],
}

THRESHOLD = 3  # min keyword hits to tag a topic


def kb_open(kb_root, filename, mode):
    """Open a file inside kb_root only: bare filename + resolved containment."""
    if "/" in filename or "\\" in filename or ".." in filename:
        raise ValueError(f"unsafe filename: {filename!r}")
    root = kb_root.resolve()
    out = (kb_root / filename).resolve()
    if out.parent != root:
        raise ValueError(f"path escapes kb dir: {out}")
    return open(out, mode, encoding="utf-8")


def pdf_text(path):
    try:
        doc = fitz.open(str(path))
        txt = "\n".join(page.get_text("text") for page in doc)
        doc.close()
        return txt
    except Exception as e:  # noqa: BLE001
        print(f"  ! pdf failed {path.name}: {e}", file=sys.stderr)
        return ""


def tag_paper(text):
    t = text.lower()
    tags = []
    for tid, kws in KEYWORDS.items():
        score = sum(t.count(k) for k in kws)
        if score >= THRESHOLD:
            tags.append({"id": tid, "score": score})
    tags.sort(key=lambda x: -x["score"])
    return tags[:6]


def main():
    if not RAW.exists():
        print("igcse papers not found under data/raw/igcse-0450", file=sys.stderr)
        sys.exit(1)
    KB.mkdir(parents=True, exist_ok=True)

    fname_re = re.compile(r"0450_([swm])(\d{2})_(qp|ms|er|gt|in)_?(\d{1,2})?\.pdf$", re.IGNORECASE)
    parsed = {}
    er_by_key = {}
    for f in sorted(RAW.rglob("*.pdf")):
        m = fname_re.search(f.name)
        if not m:
            continue
        s, yy, typ, variant = m.group(1).lower(), m.group(2), m.group(3).lower(), m.group(4) or ""
        year = 2000 + int(yy) if int(yy) < 50 else 1900 + int(yy)
        if typ == "er":
            er_by_key[(year, s)] = f
            continue
        if typ not in ("qp", "ms"):
            continue
        paper_no = 1 if variant.startswith("1") else (2 if variant.startswith("2") else None)
        d = parsed.setdefault((year, s, variant),
                              {"year": year, "session": SESSION_MAP[s],
                               "variant": variant or "1", "paper": paper_no or 1})
        d["qp" if typ == "qp" else "ms"] = f

    papers = []
    heat = Counter()
    for (_y, s, _v), d in sorted(parsed.items()):
        if "qp" not in d:
            continue
        text = pdf_text(d["qp"])
        tags = tag_paper(text)
        for t in tags:
            heat[t["id"]] += 1
        rel_qp = d["qp"].relative_to(PROJECT).as_posix()
        rel_ms = d["ms"].relative_to(PROJECT).as_posix() if "ms" in d else None
        er = er_by_key.get((d["year"], s))
        rel_er = er.relative_to(PROJECT).as_posix() if er else None
        papers.append({
            "year": d["year"], "session": d["session"], "variant": d["variant"],
            "paper": d["paper"], "chars": len(text),
            "qp": rel_qp, "ms": rel_ms, "er": rel_er,
            "topics": tags,
        })

    out = {
        "subject": "igcse-bus",
        "count": len(papers),
        "years": sorted({p["year"] for p in papers}),
        "topic_heat": [{"id": tid, "freq": n} for tid, n in heat.most_common()],
        "papers": papers,
    }
    with kb_open(KB, "igcse-papers.json", "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"papers parsed: {len(papers)} | years: {out['years'][0]}-{out['years'][-1]}")
    print("top heat:", out["topic_heat"][:8])


if __name__ == "__main__":
    main()
