# -*- coding: utf-8 -*-
"""Regenerate data/kb/glossary.json for the IB econ full site (index.html)
with the same deep enrichment used by the hub subjects (详解/例/上位/前置/跨科链接)。
Standalone so we don't need to re-run the full analyze pipeline.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import content
import content_subjects
import content_deep
import content_igcse
import content_mapping
import content_glossary_bus as gdeep

KB = Path(__file__).parent.parent / "data" / "kb"


def all_glossaries():
    g = {"ib-econ": content.GLOSSARY, "igcse-bus": content_igcse.IGCSE_BUS["glossary"]}
    for s in content_subjects.SUBJECTS:
        g[s["id"]] = s["glossary"] + content_deep.GLOSSARY_EXTRA.get(s["id"], [])
    return g


def main():
    gloss = all_glossaries()
    links, meta, invalid = gdeep.build_bridges(gloss)
    if invalid:
        print("WARN bridge members not found:", invalid)

    units, topics, _, _ = (None, None, None, None)
    import analyze  # reuse its topic index builder
    units, topics, topic_by_id, _ = analyze.build_topic_index()

    related = {}
    for r in getattr(content, "RELATED_TOPICS", []):
        related.setdefault(r["a"], []).append(r["b"])
        related.setdefault(r["b"], []).append(r["a"])
    mapping_hits = {}
    for e in content_mapping.MAPPING:
        for m in e.get("matches", []):
            if m.get("subject") == "ib-econ":
                mapping_hits.setdefault(m["topic"], []).append(e["concept_zh"])

    tby = {t["id"]: {"title": t.get("title_zh") or t["id"], "unit": t.get("unit_title_zh", "")}
           for t in topics}
    ctx = {"topic_by_id": tby, "related": related, "mapping": mapping_hits,
           "freq": {}, "bridge_links": links, "bridge_meta": meta}
    out = gdeep.enrich_subject_terms("ib-econ", content.GLOSSARY, ctx)
    KB.mkdir(parents=True, exist_ok=True)
    with open(KB / "glossary.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    more = sum(1 for t in out if t.get("more"))
    lk = sum(1 for t in out if t.get("links"))
    print(f"glossary.json rewritten: {len(out)} terms | more {more} | links {lk}")


if __name__ == "__main__":
    main()
