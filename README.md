# IB / AL 经济与商科 · 学习地图 🗺️

一个**本地静态双语网站**（中文界面 + 英文术语），从 [ibdocs.re](https://ibdocs.re) 抓取 IB 经济学资源
并覆盖六个科目与竞赛知识，以现行大纲为基准，梳理知识树、知识图谱、术语深读、真题考频，
并以「赛代学」把竞赛（康莱德 / BPA）概念与学科知识点双向匹配。

> ⚠️ 仅供个人学习/备考使用。教科书、IB/CAIE 真题与官方资料的版权归原出版方与考试局所有，
> 本仓库**不包含**任何抓取的原始资料（见下文「数据与版权」）。

## 页面入口

项目根目录启动本地服务：

```bash
python3 -m http.server 8000
```

| 入口 | 地址 | 内容 |
|---|---|---|
| 六科目学习地图（主入口） | http://localhost:8000/site/hub.html | IB经济 / AL经济 / IB商科 / AL商科 / IGCSE商科 / 竞赛知识 |
| IB 经济完整站 | http://localhost:8000/site/index.html | 真题库 / 教材深链 / IA 示例 / 图表训练 / 知识图谱 |

> 由于浏览器跨域限制，需通过 HTTP 访问（不能用 `file://` 直接打开）。

## 功能亮点

- 🌳 **知识树** — 单元 → 主题交互式思维导图，HL/SL、AS/A2、康莱德/BPA 分色
- 🕸️ **知识图谱** — 概念 ↔ 主题 ↔ 真题 ↔ IA ↔ 教材 的关联网络（IB 经济）
- 📖 **术语深读（共 420 条）** — 每条术语含：详解（机制/易错点/考法）、例子、
  🧩 上位概念（它是什么框架的一部分）、🔑 先决条件（什么题型的前置）、
  🔗 跨科目同概念徽章（28 个概念簇，IB经济 ↔ AL经济 ↔ IB/AL/IG商科 ↔ 竞赛互跳）
- 📝 **真题库** — IB 经济 2022+ 真题（绑定 markscheme/考官报告）与 IGCSE 0450 二十余年真题，
  按主题打标并生成 🔥常考/❄️冷门 考频热力
- ✍️ **IA/EE 指南** — 各科 IA/EE 写作结构与高频失分点
- 📊 **图表训练** — 28 张程序化生成的经济模型图（点/线/面积解析 + 练习题）
- 🗺️ **赛代学地图** — 22 个竞赛概念 × 96 条学科知识点匹配（桑基图 + 双向表），
  学生备赛时可反查需要补强的学科知识点
- 🧭 **IG→AL 衔接地图** — 商科 24 组「IG 已学 → AL 升级」对照 + 4 个 AL 独有模块

## 目录结构

```
ib-economics/
  scraper/                  # Python 管线（Python 3.9+，依赖见 scraper/requirements.txt）
    scrape.py               #   枚举+下载（ibdocs.re AList API）
    parse.py                #   PDF → 分页文本 / 书签 / 封面
    analyze.py              #   IB 经济知识库（打标签/图谱/统计/搜索）
    analyze_igcse.py        #   IGCSE 0450 真题解析 → 主题考频
    content.py              #   人工整理：大纲/术语/考试结构/命令词/主题关联
    content_subjects.py     #   AL经济 / IB商科 / AL商科 / 竞赛 大纲与术语
    content_igcse.py        #   IGCSE 商科（0450）大纲/术语/题型指南
    content_deep.py         #   深化：扩充术语/测验/IA·EE 指南/资源地图
    content_mapping.py      #   赛代学：竞赛概念 ↔ 学科知识点
    content_progression.py  #   IG→AL 商科衔接地图
    content_glossary_*.py   #   术语深读（详解/例子/跨科概念簇）
    make_diagrams.py        #   生成 28 张模型图（matplotlib）
    build_subjects.py       #   组装六科目 JSON → data/kb/subjects/
    enrich_glossary_site.py #   生成 IB 经济主站增强版术语表
  site/
    index.html + js/app.js  # IB 经济完整站
    hub.html  + js/hub.js   # 六科目学习地图
    assets/diagrams/        # 自制经济模型图（matplotlib 生成）
  data/                     # （不入库）raw/ 原始 PDF、text/ 提取文本、kb/ 生成 JSON
```

## 数据与版权

`data/` 目录（原始 PDF、提取文本与生成的知识库 JSON）**不包含在本仓库**：
体积约 2.2 GB，且内容来自受版权保护的教材与考试局材料。本地按以下顺序运行管线即可再生：

```bash
python3 -m venv .venv
.venv/bin/pip install -r scraper/requirements.txt

cd scraper
.venv/bin/python scrape.py enumerate --out ../data/kb/manifest.json
.venv/bin/python scrape.py download --manifest ../data/kb/manifest.json
.venv/bin/python parse.py
.venv/bin/python analyze.py
.venv/bin/python analyze_igcse.py    # IGCSE 0450 真题另行放置于 data/ 对应目录
.venv/bin/python make_diagrams.py
.venv/bin/python build_subjects.py
.venv/bin/python enrich_glossary_site.py
```

IGCSE 真题原始文件夹路径约定见 `analyze_igcse.py` 顶部说明。

## 技术说明

- **抓取**：ibdocs.re 是 OpenList/AList 文件服务器，`POST /api/fs/list`（列目录）、
  `POST /api/fs/get`（取 `raw_url` 直链），无需登录/签名；下载为增量可续传。
- **解析**：PyMuPDF 提取分页文本（`\x0c` 分页）、目录书签与封面缩略图。
- **打标签**：基于主题标题 + 核心概念关键词的加权匹配，把真题/教材章节/IA 映射到大纲主题；
  标签为启发式，前端已标注。IGCSE 0450 按 27 个主题关键词打标（阈值 3，取 top-6）。
- **前端**：纯静态 HTML/CSS/JS + 本地 vendored ECharts，无构建步骤、无后端、无 CDN 依赖。

## 备注

- 真题主题标签为**自动生成**，可能存在少量偏差，仅供参考；教材章节页号来自 PDF 目录书签。
- 部分教材 PDF 为扫描版（无文本层），此时该教材仅提供页级跳转、不提供内联摘录。
- 教学内容（大纲结构、术语详解、答题指南、竞赛匹配、衔接地图）为原创整理；
  引用的考试材料版权归原机构所有。
