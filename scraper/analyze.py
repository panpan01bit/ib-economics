#!/usr/bin/env python3
"""Build the knowledge base JSON from parsed PDFs + curated content.

Reads:  data/kb/pdf_meta.json  (from parse.py)
        scraper/content.py      (curated syllabus/glossary/assessment)
Writes: data/kb/{syllabus,topics,glossary,assessment,textbooks,papers,ias,
                guides,graph,stats,search_docs}.json
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import content  # noqa: E402

PROJECT = HERE.parent
KB = PROJECT / "data" / "kb"
TEXT = PROJECT / "data" / "text"

PAGE_SEP = "\x0c"

# generic single words that are too common to be discriminating
_GENERIC = {"demand", "supply", "price", "market", "economics", "economy",
            "good", "goods", "cost", "production", "consumption", "trade",
            "growth", "development", "income", "policy", "money", "tax"}


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def dump_json(obj, name):
    out = KB / name
    with open(out, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    return out


def build_topic_index():
    """Return (units, topics, topic_by_id, glossary_by_term)."""
    units = content.SYLLABUS
    topics = []
    topic_by_id = {}
    for u in units:
        for t in u["topics"]:
            t2 = dict(t)
            t2["unit_id"] = u["id"]
            t2["unit_title_en"] = u["title_en"]
            t2["unit_title_zh"] = u["title_zh"]
            topics.append(t2)
            topic_by_id[t["id"]] = t2
    glossary_by_term = {g["term_en"]: g for g in content.GLOSSARY}
    return units, topics, topic_by_id, glossary_by_term


def topic_keywords(topic, glossary_by_term):
    """Return dict keyword -> weight for a topic."""
    d = {}
    for w in re.findall(r"[a-z]+", topic["title_en"].lower()):
        if len(w) >= 3 and w not in _GENERIC:
            d[w] = max(d.get(w, 0), 2)
    for c in topic.get("key_concepts", []):
        g = glossary_by_term.get(c)
        if not g:
            continue
        term = g["term_en"].lower()
        if " " in term or term in _GENERIC:
            d[term] = max(d.get(term, 0), 4)
        else:
            d[term] = max(d.get(term, 0), 4)
        if g.get("term_zh"):
            d[g["term_zh"]] = max(d.get(g["term_zh"], 0), 2)
    # also match the HL extension lines' english/zh words lightly
    for line in topic.get("hl_extensions", [])[::2]:
        for w in re.findall(r"[a-z]+", line.lower()):
            if len(w) >= 4 and w not in _GENERIC:
                d.setdefault(w, 2)
    return d


def score_text(text, kw_map):
    t = text.lower()
    total = 0
    for kw, w in kw_map.items():
        if kw in t:
            total += w
    return total


def tag_text(text, topics, kw_maps, top=4):
    """Return list of {id, score} sorted desc, above a small threshold."""
    res = []
    for i, t in enumerate(topics):
        s = score_text(text, kw_maps[i])
        if s >= 6:
            res.append({"id": t["id"], "score": s})
    res.sort(key=lambda x: -x["score"])
    return res[:top]


def load_text(item):
    """Return extracted text for an item, or ''."""
    rel = item.get("text_rel")
    if not rel:
        return ""
    p = TEXT / rel
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="ignore")


def main():
    KB.mkdir(parents=True, exist_ok=True)
    meta_path = KB / "pdf_meta.json"
    if not meta_path.exists():
        print("pdf_meta.json not found — run parse.py first.", file=sys.stderr)
        sys.exit(1)
    meta = load_json(meta_path)

    units, topics, topic_by_id, glossary_by_term = build_topic_index()
    kw_maps = [topic_keywords(t, glossary_by_term) for t in topics]

    # ---- dump static content ----
    dump_json(units, "syllabus.json")
    dump_json(topics, "topics.json")
    import content_glossary_bus as _gdeep
    _tby = {tid: {"title": t.get("title_zh") or t.get("title") or tid,
                  "unit": t.get("unit_title_zh", "")} for tid, t in topic_by_id.items()}
    dump_json(_gdeep.enrich_ib_econ(_tby), "glossary.json")
    dump_json({"assessment": content.ASSESSMENT,
               "command_terms": content.COMMAND_TERMS}, "assessment.json")
    dump_json(content.ANSWER_GUIDE, "answer_guide.json")
    dump_json(content.TOPIC_EXAM_GUIDE, "topic_exam_guide.json")
    dump_json(content.RESOURCE_TYPE_LABEL, "resource_types.json")
    dump_json(content.DIAGRAMS, "diagrams.json")

    # ---- partition items by category ----
    by_cat = defaultdict(list)
    for it in meta:
        by_cat[it["category"]].append(it)

    # ---- textbooks: map TOC entries to topics ----
    textbooks = []
    for it in by_cat["textbook"]:
        chapters = []
        for ch in it.get("toc", []):
            title = ch.get("title", "")
            tags = tag_text(title, topics, kw_maps, top=2)
            chapters.append({
                "level": ch.get("level", 1), "title": title,
                "page": ch.get("page", 1), "topics": tags,
            })
        # Tag from TOC chapter titles + filename (scanned textbooks have no text).
        tag_src = it["name"] + " " + " ".join(ch["title"] for ch in chapters if ch["title"])
        tags = tag_text(tag_src, topics, kw_maps, top=6)
        textbooks.append({
            "name": it["name"], "publisher": it.get("publisher"),
            "local_path": it["local_path"], "pages": it.get("pages"),
            "size": it.get("size"), "text_rel": it.get("text_rel"),
            "cover": it.get("cover"),
            "resource_type": content.classify_textbook(it["name"]),
            "chapters": chapters, "topics": tags,
        })

    # ---- papers + markschemes ----
    papers = [it for it in by_cat["paper"]]

    def _mk_key(it):
        return (it.get("year"), it.get("session"), it.get("paper"),
                it.get("level"), it.get("tz"))

    marks = {_mk_key(it): it for it in by_cat["markscheme"]}

    papers_out = []
    for it in papers:
        text = load_text(it)
        tags = tag_text(text, topics, kw_maps, top=5)
        mk = marks.get(_mk_key(it))
        papers_out.append({
            "name": it["name"], "year": it.get("year"),
            "session": it.get("session"), "paper": it.get("paper"),
            "tz": it.get("tz"), "level": it.get("level"),
            "local_path": it["local_path"], "size": it.get("size"),
            "text_rel": it.get("text_rel"),
            "markscheme_path": mk["local_path"] if mk else None,
            "topics": tags,
        })

    # ---- IA ----
    ias_out = []
    for it in by_cat["ia"]:
        text = load_text(it)
        tags = tag_text(text, topics, kw_maps, top=4)
        n = it["name"].lower()
        if "comm" in n:
            kind = "comment"
        elif "example" in n or "portfolio" in n:
            kind = "work"
        else:
            kind = "compilation"
        ias_out.append({
            "name": it["name"], "local_path": it["local_path"],
            "size": it.get("size"), "text_rel": it.get("text_rel"),
            "topics": tags, "kind": kind,
        })

    # ---- guides / specimen / reports (reference docs) ----
    guides_out = []
    for cat in ("guide", "specimen", "report"):
        for it in by_cat[cat]:
            tags = []
            if cat == "report":
                tags = tag_text(load_text(it), topics, kw_maps, top=3)
            guides_out.append({
                "category": cat, "name": it["name"],
                "local_path": it["local_path"], "size": it.get("size"),
                "topics": tags,
            })

    dump_json(textbooks, "textbooks.json")
    dump_json(papers_out, "papers.json")
    dump_json(ias_out, "ias.json")
    dump_json(guides_out, "guides.json")

    # ---- graph ----
    nodes, edges = [], []
    unit_ids = set()
    for u in units:
        nodes.append({"id": f"unit:{u['id']}", "name": u["title_en"],
                      "name_zh": u["title_zh"], "type": "unit"})
        unit_ids.add(u["id"])
    for t in topics:
        nodes.append({"id": f"topic:{t['id']}", "name": t["title_en"],
                      "name_zh": t["title_zh"], "type": "topic",
                      "level": t["level"], "unit": t["unit_id"]})
        edges.append({"source": f"unit:{t['unit_id']}",
                      "target": f"topic:{t['id']}", "rel": "contains"})
        for c in t.get("key_concepts", []):
            if c in glossary_by_term:
                edges.append({"source": f"topic:{t['id']}",
                              "target": f"concept:{c}", "rel": "contains"})
    for g in content.GLOSSARY:
        nodes.append({"id": f"concept:{g['term_en']}", "name": g["term_en"],
                      "name_zh": g["term_zh"], "type": "concept",
                      "topic": g["topic"]})
    # link concepts to their home topic too (explicit)
    for g in content.GLOSSARY:
        edges.append({"source": f"concept:{g['term_en']}",
                      "target": f"topic:{g['topic']}", "rel": "in_topic"})
    for it in papers_out:
        pid = f"paper:{it['local_path']}"
        nodes.append({"id": pid, "name": it["name"], "type": "paper",
                      "level": it["level"], "year": it["year"],
                      "session": it["session"], "paper": it["paper"]})
        for t in it["topics"][:3]:
            edges.append({"source": f"topic:{t['id']}", "target": pid,
                          "rel": "tested_in"})
    for it in ias_out:
        iid = f"ia:{it['local_path']}"
        nodes.append({"id": iid, "name": it["name"], "type": "ia"})
        for t in it["topics"][:3]:
            edges.append({"source": f"topic:{t['id']}", "target": iid,
                          "rel": "illustrated_by"})
    for it in textbooks:
        tid = f"textbook:{it['local_path']}"
        nodes.append({"id": tid, "name": it["name"], "type": "textbook",
                      "publisher": it["publisher"]})
        for t in it["topics"][:4]:
            edges.append({"source": f"topic:{t['id']}", "target": tid,
                          "rel": "explained_in"})

    # cross-topic "related" edges + enriched links list
    topic_links = []
    for r in content.RELATED_TOPICS:
        a, b = r["a"], r["b"]
        if a in topic_by_id and b in topic_by_id:
            edges.append({"source": f"topic:{a}", "target": f"topic:{b}",
                          "rel": "related", "type": r["type"]})
            topic_links.append({
                "a": a, "b": b, "type": r["type"],
                "a_title_en": topic_by_id[a]["title_en"],
                "a_title_zh": topic_by_id[a]["title_zh"],
                "b_title_en": topic_by_id[b]["title_en"],
                "b_title_zh": topic_by_id[b]["title_zh"],
                "rel_en": r["rel_en"], "rel_zh": r["rel_zh"],
            })
    dump_json(topic_links, "topic_links.json")
    dump_json({"nodes": nodes, "edges": edges}, "graph.json")

    # ---- stats ----
    topic_freq = Counter()
    for p in papers_out:
        for t in p["topics"]:
            topic_freq[t["id"]] += 1
    paper_level = Counter(p["level"] for p in papers_out if p["level"])
    paper_year = Counter(p["year"] for p in papers_out if p["year"])
    paper_session = Counter(p["session"] for p in papers_out if p["session"])

    # command term frequency across paper texts
    cmd_freq = Counter()
    cmd_terms = [c["term_en"].lower() for c in content.COMMAND_TERMS]
    for p in papers_out:
        t = load_text(p).lower()
        for cmd in cmd_terms:
            if cmd in t:
                cmd_freq[cmd] += 1

    # topic "heat" (how often each topic appears in recent papers)
    freq = topic_freq
    freqs = sorted(((tid, freq.get(tid, 0)) for tid in topic_by_id), key=lambda x: -x[1])
    maxf = max((f for _, f in freqs), default=0)
    def heat_of(f):
        if maxf == 0:
            return "cold"
        r = f / maxf
        return "hot" if r >= 0.6 else ("cold" if r < 0.2 else "normal")
    topic_heat = [{"id": tid, "freq": f, "heat": heat_of(f)} for tid, f in freqs]

    stats = {
        "counts": {c: len(v) for c, v in by_cat.items()},
        "topic_freq": {k: v for k, v in topic_freq.most_common()},
        "paper_by_level": dict(paper_level),
        "paper_by_year": {str(k): v for k, v in sorted(paper_year.items())},
        "paper_by_session": dict(paper_session),
        "command_term_freq": {k: v for k, v in cmd_freq.most_common()},
        "topic_heat": topic_heat,
        "total_papers": len(papers_out),
        "total_ias": len(ias_out),
        "total_textbooks": len(textbooks),
    }
    dump_json(stats, "stats.json")

    # ---- search docs (for Lunr) ----
    docs = []
    for t in topics:
        concepts = ", ".join(t.get("key_concepts", []))
        docs.append({"id": f"topic:{t['id']}", "type": "topic",
                     "title": t["title_en"], "title_zh": t["title_zh"],
                     "level": t["level"], "unit": t["unit_title_en"],
                     "unit_zh": t["unit_title_zh"],
                     "body": t["desc_en"] + " " + t["desc_zh"] + " " + concepts,
                     "href": f"#/topic/{t['id']}"})
    for g in content.GLOSSARY:
        docs.append({"id": f"concept:{g['term_en']}", "type": "concept",
                     "title": g["term_en"], "title_zh": g["term_zh"],
                     "topic": g["topic"], "level": "both",
                     "body": g["def_en"] + " " + g["def_zh"],
                     "href": f"#/glossary/{quote(g['term_en'])}"})
    for p in papers_out:
        docs.append({"id": f"paper:{p['local_path']}", "type": "paper",
                     "title": p["name"], "title_zh": p["name"],
                     "level": p["level"], "year": p["year"],
                     "body": f"{p['year']} {p['session']} Paper {p['paper']} {p['level']}",
                     "href": f"#/papers/{p['year']}/{p['session']}"})
    for it in textbooks:
        docs.append({"id": f"textbook:{it['local_path']}", "type": "textbook",
                     "title": it["name"], "title_zh": it["name"],
                     "publisher": it["publisher"],
                     "body": f"{it['publisher']} textbook",
                     "href": f"#/textbooks"})
    dump_json(docs, "search_docs.json")

    print(f"topics={len(topics)} glossary={len(content.GLOSSARY)} "
          f"textbooks={len(textbooks)} papers={len(papers_out)} "
          f"ias={len(ias_out)} guides={len(guides_out)}")
    print(f"graph nodes={len(nodes)} edges={len(edges)}")
    print("Knowledge base written to", KB)


if __name__ == "__main__":
    main()
