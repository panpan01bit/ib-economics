# -*- coding: utf-8 -*-
"""常见考题切片器：从本地真题+评分方案中切出题目与官方答案要点。
输出 data/kb/subjects/examq-ib-econ.json 与 examq-igcse-bus.json。

IB 经济：解析 data/text/papers/**（parse.py 产物），评分方案按 _markscheme 同名配对。
IGCSE 0450：用 fitz 现场抽取 qp/ms 文本（analyze_igcse 的 papers 清单与主题关键词）。

每条切片：{topic, q, marks, part, verb, year, session, level, paper, variant,
          qp_link, ms_link, answer}
answer 为评分方案该小题的要点（截断），q 为题干原文。
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

PROJECT = HERE.parent
KB = PROJECT / "data" / "kb"

VERBS = ["Define", "State", "Identify", "Calculate", "Outline", "Explain", "Describe",
         "Analyse", "Analyze", "Discuss", "Evaluate", "Examine", "Do you think",
         "Justify", "Recommend", "Consider", "Distinguish", "Comment"]


def verb_of(text):
    for v in VERBS:
        if text.lower().startswith(v.lower()):
            return "Do you think" if v == "Do you think" else ("Analyse" if v == "Analyze" else v)
    m = re.match(r"[^\w']*(\w+)", text)
    return m.group(1) if m else ""


def clean(text):
    """Collapse whitespace, drop boilerplate & answer-dot lines."""
    lines = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        # IGCSE answer lines: long dot runs / underscores
        if re.fullmatch(r"[.\s_·]{8,}", s):
            continue
        lines.append(s)
    t = " ".join(lines)
    t = re.sub(r"[.]{4,}", " ", t)   # inline answer-dot runs (Way 1: ......)
    t = re.sub(r"[_]{4,}", " ", t)
    t = re.sub(r"[\x00-\x08\x0b-\x1f]", "", t)  # PDF control chars
    t = re.sub(r"Turn over\s*[\d_]*0450[\d_.]*\s*©?\s*UCLES\s*\d{4}\s*(\*\d+\*)?", " ", t)
    t = re.sub(r"© UCLES \d{4}", " ", t)
    t = re.sub(r"© CIE \d{4}", " ", t)
    t = re.sub(r"\[\s*Turn over", " ", t)
    t = re.sub(r"[\d_]*0450[\d_.]*", " ", t)
    t = re.sub(r"\*+\d+\*+", " ", t)
    # front matter (old papers)
    t = re.sub(r"This document consists of \d+ printed pages( and \d+ blank pages)?\.?", " ", t)
    t = re.sub(r"SP\s*\([A-Z/]+\)\s*\S+\d+", " ", t)
    t = re.sub(r"CAMBRIDGE INTERNATIONAL EXAMINATIONS\s*", " ", t)
    t = re.sub(r"Cambridge International Examinations\s*", " ", t)
    t = re.sub(r"International General Certificate of Secondary Education\s*", " ", t)
    t = re.sub(r"BUSINESS STUDIES\s*/\d{2}\s*Paper\s*\d\s*[A-Za-z/]+\s*\d{4}\s*\d+\s*hours?\s*\d*\s*minutes?", " ", t)
    t = re.sub(r"Candidates answer on the Question Paper\.\s*No Additional Materials are required\.?", " ", t)
    t = re.sub(r"Read all the questions carefully before you start answering them\.?", " ", t)
    t = re.sub(r"\s+", " ", t)
    t = t.replace("– 2 –", " ").replace("– 3 –", " ").replace("– 4 –", " ")
    return t


def norm_question(q):
    """Key for grouping near-identical questions."""
    s = q.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\b(this|that|the|a|an|of|for|to|in|and|or)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()[:80]


# --------------------------------------------------------------------------- IB econ

PART_RE = re.compile(r"\((?P<part>[a-z])\)\s*(?P<q>.{15,700}?)\[(?P<marks>\d{1,2})\]")

def parse_ib_file(txt_path):
    """Return [(part, question, marks)] from an IB econ question-paper text."""
    t = clean(txt_path.read_text(encoding="utf-8"))
    # cut at "markscheme"-style endings or blank-page markers already cleaned
    out = []
    for m in PART_RE.finditer(t):
        q = m.group("q").strip()
        # skip fragments that are clearly boilerplate / instructions
        if re.search(r"maximum mark|answer one|examination paper|not write|cache|permission", q, re.I):
            continue
        if re.search(r"command term|real-world example", q, re.I) and len(q) < 40:
            continue
        out.append((m.group("part"), q, int(m.group("marks"))))
    return out


def parse_ib_ms(txt_path):
    """{part: answer guidance} from an IB econ markscheme text."""
    t = txt_path.read_text(encoding="utf-8")
    t = re.sub(r"\s+", " ", t)
    # parts look like "(a) <question> [10] Answers may include: ... "
    blocks = {}
    for m in PART_RE.finditer(t):
        part, q, marks = m.group("part"), m.group("q"), m.group("marks")
        start = m.end()
        nxt = PART_RE.search(t, start)
        body = t[start:nxt.start() if nxt else len(t)]
        body = re.sub(r"Assessment Criteria.*$", "", body, flags=re.S)
        body = re.sub(r"A maximum of \[\d+\].*$", "", body, flags=re.S)
        # keep the "Answers may include:" substance
        i = body.find("Answers may include")
        seg = body[i: i + 600] if i != -1 else body[:300]
        seg = seg.replace("Answers may include:", "要点").strip()
        if len(seg) > 40:
            blocks[part] = seg
    return blocks


def ib_econ_stats():
    """(topic keyword scorer, topics) reused from analyze.py."""
    import analyze
    units, topics, topic_by_id, glossary_by_term = analyze.build_topic_index()
    kw_maps = [(t, analyze.topic_keywords(t, glossary_by_term)) for t in topics]
    return kw_maps


def score_topics(text, kw_maps):
    tl = " " + text.lower() + " "
    scored = []
    for t, kws in kw_maps:
        s = sum(w for kw, w in kws.items() if kw.lower() in tl)
        if s:
            scored.append((s, t["id"]))
    scored.sort(reverse=True)
    return scored


def extract_ib_econ():
    text_dir = PROJECT / "data" / "text" / "papers"
    if not text_dir.exists():
        print("no IB paper texts; skip")
        return None
    kw_maps = ib_econ_stats()
    records = []
    for txt in sorted(text_dir.rglob("*.txt")):
        name = txt.name
        if name.endswith("_markscheme.txt"):
            continue
        m = re.match(r"Economics_paper_(\d)__(SL|HL)(_.*)?\.txt", name)
        if not m:
            continue
        paper_no, level = int(m.group(1)), m.group(2)
        year = int(txt.parent.parent.name)
        session = txt.parent.name  # May / November
        ms_txt = txt.with_name(name.replace(".txt", "_markscheme.txt"))
        ms_map = parse_ib_ms(ms_txt) if ms_txt.exists() else {}
        rel = lambda p: "../data/" + str(p.relative_to(PROJECT / "data")).replace("\\", "/")
        qp_link = rel(PROJECT / "data" / "raw" / "papers" / str(year) / session / name.replace(".txt", ".pdf"))
        ms_link = ("../" + str(ms_txt.relative_to(PROJECT / "data")).replace("\\", "/").replace("text/", "raw/")
                   if ms_txt.exists() else None)
        for part, q, marks in parse_ib_file(txt):
            tops = score_topics(q, kw_maps)
            topic = tops[0][1] if tops else None
            if not topic or marks < 2:
                continue
            records.append({
                "topic": topic, "q": q, "marks": marks, "part": part,
                "verb": verb_of(q), "year": year,
                "session": "May" if session == "May" else "Nov",
                "level": level, "paper": paper_no,
                "qp_link": qp_link, "ms_link": ms_link,
                "answer": ms_map.get(part, ""),
            })
    print(f"IB econ slices: {len(records)}")
    return records


# --------------------------------------------------------------------------- IGCSE 0450

QPART_RE = re.compile(
    r"(?P<q>[^[\[\]]{15,500}?)\s*\((?P<part>[a-d])\)(?P<sub>\s*\((?:i{1,3}|iv)\))?"
    r"(?P<mid>[^\[\]]{0,60}?)\[(?P<marks>\d{1,2})\]")

# IGCSE: anchor = part label followed within 80 chars by [N]; question text is the
# segment between the previous mark anchor and this label (layout-tolerant).
# 2020+ papers have FIVE parts per question: (a)2 (b)2 (c)4 (d)4 (e)8.
IG_ANCHOR_RE = re.compile(
    r"\((?P<part>[a-f])\)(?P<sub>\s*\((?:i{1,3}|iv)\))?(?P<mid>[^\[\]]{0,80}?)\[(?P<marks>\d{1,2})\]")

MS_KEY_RE = re.compile(r"(?<![\d(])的就是")


def extract_igcse():
    import fitz
    import analyze_igcse as A

    papers_meta = json.loads((KB / "subjects" / "igcse-papers.json").read_text(encoding="utf-8"))
    records = []
    for p in papers_meta["papers"]:
        qp_path = PROJECT / p["qp"] if not str(p["qp"]).startswith("/") else Path(p["qp"])
        if not qp_path.exists():
            continue
        try:
            doc = fitz.open(str(qp_path))
            t = clean("\n".join(doc[i].get_text() for i in range(doc.page_count)))
            doc.close()
        except Exception:
            continue
        # paper-level topics as fallback
        pt = [x["id"] for x in (p.get("topics") or [])]
        ms_map = []
        if p.get("ms"):
            ms_path = PROJECT / p["ms"]
            if ms_path.exists():
                try:
                    doc = fitz.open(str(ms_path))
                    ms_map = parse_igcse_ms("\n".join(doc[i].get_text() for i in range(doc.page_count)))
                    doc.close()
                except Exception:
                    ms_map = []
        anchors = list(IG_ANCHOR_RE.finditer(t))
        prev_end = 0
        qno, prev_letter = 1, None
        for m in anchors:
            q = t[prev_end: m.start()].strip()
            prev_end = m.end()
            q = re.sub(r"^\s*\d{1,2}\s+", "", q)  # leading question number
            q = re.sub(r"\s+", " ", q)
            letter = m.group("part")
            if prev_letter and ord(letter) < ord(prev_letter):
                qno += 1
            prev_letter = letter
            if re.search(r"^(name|name of|do not|award|accept|ignore|total)\b", q, re.I):
                continue
            if len(q) < 15 or re.fullmatch(r"[\d\s$%.,()-]+", q):
                continue
            part = letter + (re.sub(r"\s+", "", m.group("sub") or ""))
            marks = int(m.group("marks"))
            # per-part topic scoring with analyze_igcse.KEYWORDS
            tl = " " + q.lower() + " "
            scored = []
            for tid, kws in A.KEYWORDS.items():
                s = sum(1 for kw in kws if kw.lower() in tl)
                if s >= 2:
                    scored.append((s, tid))
            scored.sort(reverse=True)
            topic = scored[0][1] if scored else (pt[0] if pt else None)
            if not topic:
                continue
            rel = lambda fp: "../" + str(fp.relative_to(PROJECT)).replace("\\", "/")
            records.append({
                "topic": topic, "q": q, "marks": marks, "part": part,
                "verb": verb_of(q), "year": p["year"], "session": p["session"],
                "level": "Core/Ext", "paper": p["paper"], "variant": p.get("variant"),
                "qp_link": rel(qp_path),
                "ms_link": (rel(ms_path) if p.get("ms") else None),
                "answer": best_ms_answer(q, ms_map, qno=qno, part=part),
                "qno": qno,
            })
    print(f"IGCSE slices: {len(records)}")
    return records


def parse_igcse_ms(ms_text):
    """{(qno, part): guidance} from '1(a)'-style markscheme keys."""
    t = clean(ms_text)
    t = re.sub(r"Page \d+ of \d+", " ", t)
    t = re.sub(r"Question\s+Answer\s+Marks\s+Notes", " ", t)
    t = re.sub(r"Cambridge IGCSE –? ?Mark Scheme( PUBLISHED)?", " ", t)
    t = re.sub(r"PUBLISHED", " ", t)
    t = re.sub(r"(October/November|May/June|March)\s*\d{4}", " ", t)
    t = re.sub(r"0450/\d{1,2}", " ", t)
    t = re.sub(r"\s+", " ", t)
    key_re = re.compile(r"(?P<no>\d{1,2}) ?\((?P<part>[a-f])\)(?P<sub> ?\((?:i{1,3}|iv)\))?")
    keys = []
    for m in key_re.finditer(t):
        if re.search(r"\[\d{1,2}\]", t[m.end(): m.end() + 1400]):
            keys.append(m)
    out = {}
    for i, m in enumerate(keys):
        end = keys[i + 1].start() if i + 1 < len(keys) else len(t)
        seg = t[m.end(): end].strip()
        if len(seg) < 60:
            continue
        no = int(m.group("no"))
        part = m.group("part") + (re.sub(r"\s+", "", m.group("sub") or ""))
        seg = seg[:460]
        key_full = (no, part)
        key_bare = (no, m.group("part"))
        if key_full not in out:
            out[key_full] = seg
        if key_bare not in out:
            out[key_bare] = seg
    return out


def best_ms_answer(q, segs, qno=None, part=None):
    if qno is not None and part is not None and isinstance(segs, dict):
        hit = segs.get((qno, part)) or segs.get((qno, part[0]))
        if hit:
            return hit
    if not segs:
        return ""
    import difflib
    probe = norm_question(q)[:70]
    best, best_r = "", 0.0
    items = segs.values() if isinstance(segs, dict) else segs
    for s in items:
        sq = s["q"] if isinstance(s, dict) else s
        r = difflib.SequenceMatcher(None, probe, norm_question(sq)[:70]).ratio()
        if r > best_r:
            best_r, best = r, (s["text"] if isinstance(s, dict) else s)
    return best if best_r > 0.5 else ""


# --------------------------------------------------------------------------- 聚合

def aggregate(records):
    """per-topic 常见题型 patterns + dedup/cap selection."""
    by_topic = defaultdict(list)
    for r in records:
        by_topic[r["topic"]].append(r)
    patterns = {}
    picked = {}
    for topic, items in by_topic.items():
        pc = defaultdict(int)
        for r in items:
            pc[f"{r['verb']}[{r['marks']}分]"] += 1
        patterns[topic] = dict(sorted(pc.items(), key=lambda kv: -kv[1])[:8])
        # dedupe by normalized prefix, prefer recent & answered
        seen = {}
        for r in sorted(items, key=lambda x: (-x["year"], -x["marks"])):
            k = norm_question(r["q"])[:60]
            if k in seen:
                seen[k]["dup"] += 1
                continue
            seen[k] = r
            r["dup"] = 1
        sel = list(seen.values())
        # cap per topic: keep mark-variety, recent first
        sel.sort(key=lambda x: (-x["year"], -x["marks"]))
        picked[topic] = sel[:14]
    return patterns, picked


def main():
    out = {}
    ib = extract_ib_econ()
    if ib is not None:
        patterns, picked = aggregate(ib)
        data = {"subject": "ib-econ",
                "note": "切片自 2022+ 现行大纲真题（qp+markscheme 配对）；answer 为官方评分方案要点摘录。",
                "patterns": patterns,
                "topics": {t: sorted(v, key=lambda x: (-x["year"], -x["marks"])) for t, v in picked.items()},
                "count": len(ib)}
        with (KB / "subjects" / "examq-ib-econ.json").open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"  topics: {len(picked)} | sample:", json.dumps(list(picked.values())[0][0], ensure_ascii=False)[:220])

    ig = extract_igcse()
    if ig is not None:
        patterns, picked = aggregate(ig)
        data = {"subject": "igcse-bus",
                "note": "切片自 2002-2025 共 239 卷 0450 真题（qp+ms 配对）；answer 为官方评分方案要点摘录。",
                "patterns": patterns,
                "topics": {t: sorted(v, key=lambda x: (-x["year"], -x["marks"])) for t, v in picked.items()},
                "count": len(ig)}
        with (KB / "subjects" / "examq-igcse-bus.json").open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"  topics: {len(picked)} | total slices: {len(ig)}")


if __name__ == "__main__":
    main()
