#!/usr/bin/env python3
"""Build per-subject knowledge bases (including IB Economics) -> data/kb/subjects/.

Output: subjects.json (index) + <id>.json per subject with unified shape:
  {id, name_zh, name_en, accent, level_names, syllabus, topics, glossary,
   assessment, quiz, extra:{...subject-specific}}
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import content  # IB econ
import content_subjects  # AL econ / IB bus / AL bus / comp
import content_mapping  # competition <-> subject concept mapping
import content_deep  # expanded glossaries/quiz, IA/EE guides, resources, diagram map
import content_igcse  # IGCSE Business Studies 0450
import content_progression  # IG -> AL progression map
import content_glossary_bus as gdeep  # glossary deep explanations + cross-subject bridges

PROJECT = HERE.parent
KB = PROJECT / "data" / "kb" / "subjects"

PAGE_SEP = "\x0c"


def ib_econ_subject():
    """Wrap the existing IB economics curated content into the unified shape."""
    topics = []
    for u in content.SYLLABUS:
        for t in u["topics"]:
            t2 = dict(t)
            t2["unit_id"] = u["id"]
            t2["unit_title_zh"] = u["title_zh"]
            guide = content.TOPIC_EXAM_GUIDE.get(t["id"], {})
            t2["exam_tips"] = guide.get("tips", [])
            t2["diagrams_list"] = guide.get("diagrams", [])
            topics.append(t2)
    glossary = [{**g, "def_en": g.get("def_en", "")} for g in content.GLOSSARY]
    quiz = []
    for d in content.DIAGRAMS:
        for p in d.get("practice", []):
            quiz.append({**p, "diagram": d["name_zh"], "topic": d["topic"]})
    return {
        "id": "ib-econ", "name_zh": "IB 经济学", "name_en": "IB Economics",
        "accent": "#14b8a6",
        "level_names": {"hl": "HL", "sl": "SL", "both": "SL + HL"},
        "syllabus": content.SYLLABUS, "topics": topics,
        "glossary": glossary,
        "assessment": {
            "note": "现行大纲（2022 首考 / 2024 更新）",
            "SL": [{"id": c["id"], "name_zh": c["name_zh"], "time": c["time"], "weight": c["weight"]}
                   for c in content.ASSESSMENT["SL"]["components"]],
            "HL": [{"id": c["id"], "name_zh": c["name_zh"], "time": c["time"], "weight": c["weight"]}
                   for c in content.ASSESSMENT["HL"]["components"]],
        },
        "quiz": quiz,
        "iaee": content_deep.IAEE.get("ib-econ", {}),
        "resources": content_deep.RESOURCES.get("ib-econ", {}),
        "has_diagrams": False,  # diagrams live in the full site (index.html)
        "extra": {"has_papers": True, "has_diagrams": True},
    }


def norm_subject(s):
    """Normalize a content_subjects entry into the unified shape."""
    topics = []
    dmap = content_deep.DIAGRAM_MAP if s["id"] == "al-econ" else {}
    for u in s["syllabus"]:
        for t in u["topics"]:
            t2 = {k: v for k, v in t.items() if k != "exam_zh"}
            t2["unit_id"] = u["id"]
            t2["unit_title_zh"] = u["title_zh"]
            if t2["id"] in dmap:
                t2["diagram_ids"] = dmap[t2["id"]]
            topics.append(t2)
    glossary = s["glossary"] + content_deep.GLOSSARY_EXTRA.get(s["id"], [])
    quiz = s["quiz"] + content_deep.QUIZ_EXTRA.get(s["id"], [])
    return {
        "id": s["id"], "name_zh": s["name_zh"], "name_en": s["name_en"],
        "accent": s["accent"], "level_names": s["level_names"],
        "syllabus": s["syllabus"], "topics": topics,
        "glossary": glossary, "assessment": s["assessment"],
        "quiz": quiz,
        "iaee": content_deep.IAEE.get(s["id"], {}),
        "resources": content_deep.RESOURCES.get(s["id"], {}),
        "has_diagrams": s["id"] == "al-econ",
        "extra": {"has_papers": False, "has_diagrams": s["id"] == "al-econ"},
    }


def igcse_subject():
    """IGCSE Business (0450): content + real past-paper heat."""
    s = content_igcse.IGCSE_BUS
    topics = []
    for u in s["syllabus"]:
        for t in u["topics"]:
            t2 = dict(t)
            t2["unit_id"] = u["id"]
            t2["unit_title_zh"] = u["title_zh"]
            topics.append(t2)
    sub = {
        "id": s["id"], "name_zh": s["name_zh"], "name_en": s["name_en"],
        "accent": s["accent"], "level_names": s["level_names"],
        "syllabus": s["syllabus"], "topics": topics,
        "glossary": s["glossary"], "assessment": s["assessment"],
        "quiz": s["quiz"],
        "iaee": content_igcse.IAEE_IG,
        "resources": content_igcse.RESOURCES_IG,
        "has_diagrams": False,
        "topic_heat": [], "paper_count": 0, "paper_years": "",
        "extra": {"has_papers": True, "has_diagrams": False},
    }
    papers_file = KB / "igcse-papers.json"
    if papers_file.exists():
        with open(papers_file, encoding="utf-8") as f:
            pdata = json.load(f)
        heat_map = {h["id"]: h["freq"] for h in pdata.get("topic_heat", [])}
        for t in sub["topics"]:
            if t["id"] in heat_map:
                t["freq"] = heat_map[t["id"]]
        maxf = max(heat_map.values(), default=0)
        for t in sub["topics"]:
            f = t.get("freq", 0)
            t["heat"] = "hot" if maxf and f / maxf >= 0.6 else ("cold" if maxf == 0 or f / maxf < 0.2 else "normal")
        sub["topic_heat"] = pdata.get("topic_heat", [])
        sub["paper_count"] = pdata.get("count", 0)
        ys = pdata.get("years", [])
        sub["paper_years"] = f"{ys[0]}–{ys[-1]}" if ys else ""
    return sub


def safe_id(sid):
    """Subject ids are local content keys; still validate strictly so a bad
    id can never turn into a path traversal (e.g. '../../x')."""
    import re
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,30}", sid or ""):
        raise ValueError(f"unsafe subject id: {sid!r}")
    return sid


def kb_open(kb_root, filename, mode):
    """Open a file inside kb_root only. The resolved path must stay within
    kb_root (blocks any ../ traversal) and the name must be a bare filename."""
    if "/" in filename or "\\" in filename or ".." in filename:
        raise ValueError(f"unsafe filename: {filename!r}")
    root = kb_root.resolve()
    out = (kb_root / filename).resolve()
    if out.parent != root:
        raise ValueError(f"path escapes kb dir: {out}")
    return open(out, mode, encoding="utf-8")


def glossary_ctx(s, bridge_links, bridge_meta):
    """Assemble the structural context used to enrich s's glossary terms."""
    tby = {t["id"]: {"title": t.get("title_zh") or t.get("title") or t["id"],
                     "unit": t.get("unit_title_zh", "")} for t in s["topics"]}
    related = {}
    for r in getattr(content, "RELATED_TOPICS", []):
        a, b = r["a"], r["b"]
        related.setdefault(a, []).append(b)
        related.setdefault(b, []).append(a)
    mapping_hits = {}
    for e in content_mapping.MAPPING:
        for m in e.get("matches", []):
            if m.get("subject") == s["id"]:
                mapping_hits.setdefault(m["topic"], []).append(e["concept_zh"])
    freq = {t["id"]: t["freq"] for t in s["topics"] if t.get("freq") is not None}
    return {"topic_by_id": tby, "related": related, "mapping": mapping_hits,
            "freq": freq, "bridge_links": bridge_links, "bridge_meta": bridge_meta}


def main():
    KB.mkdir(parents=True, exist_ok=True)
    subs = [ib_econ_subject()] + [norm_subject(s) for s in content_subjects.SUBJECTS]
    subs = [{**s, "id": safe_id(s["id"])} for s in subs]
    ig = igcse_subject()
    # keep comp last; insert igcse before it
    comp_idx = next((i for i, s in enumerate(subs) if s["id"] == "comp"), len(subs))
    subs.insert(comp_idx, ig)
    # glossary deep pass: curated explanations + cross-subject bridges + fallback
    bridge_links, bridge_meta, invalid = gdeep.build_bridges({s["id"]: s["glossary"] for s in subs})
    if invalid:
        print(f"  WARN bridge members not found: {invalid}")
    for s in subs:
        s["glossary"] = gdeep.enrich_subject_terms(s["id"], s["glossary"], glossary_ctx(s, bridge_links, bridge_meta))
    index = [{"id": s["id"], "name_zh": s["name_zh"], "name_en": s["name_en"],
              "accent": s["accent"],
              "units": len(s["syllabus"]), "topics": len(s["topics"]),
              "glossary": len(s["glossary"]), "quiz": len(s["quiz"])}
             for s in subs]
    with kb_open(KB, "index.json", "w") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    mapping = {"subject_short": content_mapping.SUBJECT_SHORT,
               "note": content_mapping.REVERSE_NOTE,
               "entries": content_mapping.MAPPING}
    with kb_open(KB, "mapping.json", "w") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=1)
    with kb_open(KB, "progression.json", "w") as f:
        json.dump(content_progression.PROGRESSION, f, ensure_ascii=False, indent=1)
    for s in subs:
        with kb_open(KB, s["id"] + ".json", "w") as f:
            json.dump(s, f, ensure_ascii=False)
        print(f"  {s['id']:8s} {s['name_zh']}: {len(s['syllabus'])}u {len(s['topics'])}t "
              f"{len(s['glossary'])}g {len(s['quiz'])}q")
    print("subjects index + 5 subject files written to", KB)


if __name__ == "__main__":
    main()
