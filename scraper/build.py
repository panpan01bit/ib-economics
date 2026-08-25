#!/usr/bin/env python3
"""Verify the generated site + knowledge base are complete and print next steps.

The static site in ../site is authored directly and reads data from ../data/kb
and ../data/{raw,text}; this script checks everything lines up.
"""
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
KB = PROJECT / "data" / "kb"
SITE = PROJECT / "site"

KB_FILES = ["syllabus.json", "topics.json", "glossary.json", "assessment.json",
            "textbooks.json", "papers.json", "ias.json", "guides.json",
            "graph.json", "stats.json", "search_docs.json"]
SITE_FILES = ["index.html", "css/style.css", "js/app.js", "assets/echarts.min.js"]


def main():
    missing = [f for f in KB_FILES if not (KB / f).exists()]
    msite = [f for f in SITE_FILES if not (SITE / f).exists()]
    ok = True
    if missing:
        ok = False
        print("缺少知识库文件（先运行 parse.py 与 analyze.py）：")
        for f in missing:
            print("  -", f)
    if msite:
        ok = False
        print("缺少站点文件：", msite)
    if not (KB / "pdf_meta.json").exists():
        ok = False
        print("缺少 pdf_meta.json —— 运行 parse.py 解析 PDF。")

    if ok:
        print("✅ 站点与知识库均已就绪。")
        print("\n启动本地网站：")
        print("  cd", PROJECT)
        print("  python3 -m http.server 8000")
        print("然后浏览器打开 http://localhost:8000/site/")
    else:
        print("\n完整流程：")
        print("  1) .venv/bin/python scraper/scrape.py enumerate")
        print("  2) .venv/bin/python scraper/scrape.py download")
        print("  3) .venv/bin/python scraper/parse.py")
        print("  4) .venv/bin/python scraper/analyze.py")
        print("  5) python3 -m http.server 8000  (在项目根目录)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
