/* IB Economics 学习地图 — single-page app (no build step, no backend). */
(function () {
  "use strict";

  const KB = "../data/kb/";
  const D = {};
  const charts = [];
  const state = { selectedTopic: null, glossaryQ: "", paperFilter: {} };

  const $ = (sel) => document.querySelector(sel);
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const assetUrl = (rel) => "../data/" + String(rel).split("/").map(encodeURIComponent).join("/");
  const pdfUrl = (rel, page) => assetUrl("raw/" + rel) + (page ? "#page=" + page : "");

  const LEVEL_COLOR = { hl: "#f97316", both: "#14b8a6", sl: "#10b981" };
  const TYPE_COLOR = {
    unit: "#8b5cf6", topic: "#14b8a6", concept: "#38bdf8",
    paper: "#0ea5a4", ia: "#f59e0b", textbook: "#6366f1",
  };

  function levelBadge(level) {
    if (level === "hl") return '<span class="badge hl">HL 专属</span>';
    if (level === "sl") return '<span class="badge sl">SL</span>';
    return '<span class="badge both">SL + HL</span>';
  }

  function heatBadge(id) {
    const h = D.heatById && D.heatById[id];
    if (!h) return "";
    const n = h.freq || 0;
    if (h.heat === "hot") return `<span class="badge hl" title="近年真题高频出现">🔥 常考 · ${n} 次</span>`;
    if (h.heat === "cold") return `<span class="badge tag" title="近年真题较少出现">❄️ 冷门 · ${n} 次</span>`;
    return `<span class="badge both" title="近年真题频率中等">中频 · ${n} 次</span>`;
  }

  const REL_TYPE_LABEL = { micro: "微观内", macro: "宏观内", global: "全球内",
    macro2micro: "宏观→微观", micro2macro: "微观→宏观", cross: "跨单元" };

  function resourceBadge(rt) {
    const label = (D.resource_types || {})[rt];
    if (!label) return "";
    const zh = esc(label.zh);
    if (rt === "study_guide") return `<span class="badge hl" title="对教材中较复杂内容与易错难点的详解">🎯 ${zh}</span>`;
    if (rt === "textbook") return `<span class="badge both">📘 ${zh}</span>`;
    if (rt === "workbook") return `<span class="badge sl">📝 ${zh}</span>`;
    if (rt === "answers") return `<span class="badge tag">✔ ${zh}</span>`;
    return `<span class="badge tag">${zh}</span>`;
  }

  // ------------------------------------------------------------------ load
  async function load() {
    const names = ["syllabus", "topics", "glossary", "assessment", "papers",
      "ias", "textbooks", "guides", "graph", "stats", "search_docs", "topic_links",
      "topic_exam_guide", "answer_guide", "resource_types", "diagrams"];
    await Promise.all(names.map(async (n) => {
      const r = await fetch(KB + n + ".json");
      D[n] = await r.json();
    }));
    D.topicById = {}; D.topics.forEach((t) => (D.topicById[t.id] = t));
    D.unitById = {}; D.syllabus.forEach((u) => (D.unitById[u.id] = u));
    D.glossaryByTerm = {}; D.glossary.forEach((g) => (D.glossaryByTerm[g.term_en] = g));
    D.heatById = {}; (D.stats.topic_heat || []).forEach((h) => (D.heatById[h.id] = h));
    D.reportsByTopic = {};
    (D.guides || []).forEach((g) => {
      if (g.category === "report" && g.topics) g.topics.forEach((t) => {
        (D.reportsByTopic[t.id] = D.reportsByTopic[t.id] || []).push(g);
      });
    });
    D.relatedByTopic = {};
    (D.topic_links || []).forEach((l) => {
      (D.relatedByTopic[l.a] = D.relatedByTopic[l.a] || []).push({ other: l.b, type: l.type, rel_en: l.rel_en, rel_zh: l.rel_zh, title_en: l.b_title_en, title_zh: l.b_title_zh, tid: l.b });
      (D.relatedByTopic[l.b] = D.relatedByTopic[l.b] || []).push({ other: l.a, type: l.type, rel_en: l.rel_en, rel_zh: l.rel_zh, title_en: l.a_title_en, title_zh: l.a_title_zh, tid: l.a });
    });
    window.addEventListener("hashchange", route);
    window.addEventListener("resize", () => charts.forEach((c) => c.resize()));
    route();
  }

  // ------------------------------------------------------------------ router
  const VIEW_TITLE = {
    overview: ["总览 Overview", "考试结构与大纲速览"],
    tree: ["知识树 Knowledge Tree", "单元 → 主题，点击节点查看详情"],
    topic: ["知识树 Knowledge Tree", "主题详情与关联知识点"],
    graph: ["知识图谱 Graph", "概念 · 主题 · 真题 · IA · 教材的关联网络"],
    hlsl: ["HL vs SL 对照", "逐主题区分 HL 与 SL 内容"],
    glossary: ["术语表 Glossary", "英中对照 · 点击查看定义与关联主题"],
    papers: ["真题库 Past Papers", "现行大纲（2022 起）真题与评分方案"],
    ia: ["IA 示例库", "内部评估（评论组合）官方示例"],
    textbooks: ["教材原文 Textbooks", "主流教材章节 → 主题 → 原文页"],
    diagrams: ["图表解析与训练 Diagrams", "点 · 线 · 面积的解析与自测训练"],
    charts: ["数据分析 Charts", "出题频率 · 命令词 · 分布统计"],
  };

  function route() {
    const hash = location.hash.replace(/^#\/?/, "") || "overview";
    const parts = hash.split("/");
    const view = parts[0];
    const [title, sub] = VIEW_TITLE[view] || ["IB Economics", ""];
    $("#page-title").textContent = title;
    $("#page-sub").textContent = sub;
    const navView = view === "topic" ? "tree" : view;
    document.querySelectorAll("#nav a").forEach((a) =>
      a.classList.toggle("active", a.dataset.view === navView));
    render(view, parts.slice(1));
  }

  function render(view, args) {
    const el = $("#view");
    el.innerHTML = "";
    switch (view) {
      case "overview": renderOverview(el); break;
      case "tree": renderTree(el, args); break;
      case "topic": renderTree(el, args); break;
      case "graph": renderGraph(el); break;
      case "hlsl": renderHlSl(el); break;
      case "glossary": renderGlossary(el, args); break;
      case "papers": renderPapers(el, args); break;
      case "ia": renderIa(el); break;
      case "textbooks": renderTextbooks(el); break;
      case "diagrams": renderDiagrams(el); break;
      case "charts": renderCharts(el); break;
      default: renderOverview(el);
    }
  }

  // ------------------------------------------------------------------ overview
  function renderOverview(el) {
    const s = D.stats || {};
    const counts = s.counts || {};
    el.innerHTML = `
      <div class="hero">
        <h2>IB Economics 学习地图 🗺️</h2>
        <p>以现行大纲（2022 首考 / 2024 更新）为基准，梳理知识树与知识图谱，区分 <b>HL / SL</b>，
        并深度链接到教材原文、真题、评分方案与 IA 示例。左侧导航开始探索，或直接用右上角搜索。</p>
      </div>
      <div class="grid cols-4">
        <div class="stat teal"><div class="num">${counts.textbook || 0}</div><div class="label">教材 PDF</div></div>
        <div class="stat sky"><div class="num">${counts.paper || 0}</div><div class="label">真题卷</div></div>
        <div class="stat coral"><div class="num">${counts.markscheme || 0}</div><div class="label">评分方案</div></div>
        <div class="stat amber"><div class="num">${counts.ia || 0}</div><div class="label">IA 示例</div></div>
      </div>
      <div class="grid cols-2" style="margin-top:16px">
        <div class="card pad">
          <h3>考试结构（SL vs HL）</h3>
          <div id="ov-assess"></div>
        </div>
        <div class="card pad">
          <h3>各卷权重</h3>
          <div class="chart short" id="ov-weight"></div>
        </div>
      </div>
      <div class="card pad" style="margin-top:16px">
        <h3>大纲单元</h3>
        <div class="grid cols-4" id="ov-units"></div>
      </div>`;
    renderAssessmentTable($("#ov-assess"));
    renderWeightChart($("#ov-weight"));
    $("#ov-units").innerHTML = D.syllabus.map((u) => `
      <div class="card pad" style="cursor:pointer" onclick="location.hash='#/tree'">
        <div style="display:flex;justify-content:space-between;align-items:baseline">
          <b>${esc(u.short_zh)}</b><span class="badge unit">${u.topics.length} 主题</span>
        </div>
        <div class="muted" style="font-size:13px;margin-top:6px">${esc(u.title_en)}</div>
        <div style="font-size:12px;color:var(--ink-3);margin-top:4px">HL 专属 ${u.topics.filter(t=>t.level==='hl').length} 个</div>
      </div>`).join("");
  }

  function renderAssessmentTable(container) {
    const rows = ["SL", "HL"].map((lv) => {
      const a = D.assessment.assessment[lv];
      const comps = a.components.map((c) => `
        <tr>
          <td>${esc(c.name_zh)}<div class="muted" style="font-size:12px">${esc(c.name_en)}</div></td>
          <td>${esc(c.time || "—")}</td><td>${c.marks}</td><td>${c.weight}%</td>
        </tr>`).join("");
      return `<h4 style="margin:14px 0 6px">${esc(a.name_zh)} <span class="badge ${lv==='HL'?'hl':'sl'}">${lv}</span></h4>
        <table><thead><tr><th>部分</th><th>时长</th><th>分数</th><th>权重</th></tr></thead><tbody>${comps}</tbody></table>`;
    }).join("");
    container.innerHTML = rows;
  }

  function renderWeightChart(dom) {
    const chart = echarts.init(dom);
    const mk = (lv) => D.assessment.assessment[lv].components.map((c) => ({
      name: c.name_zh, value: c.weight,
    }));
    chart.setOption({
      tooltip: { trigger: "item" },
      legend: { bottom: 0 },
      series: [
        { name: "SL", type: "pie", radius: ["28%", "52%"], center: ["28%", "48%"],
          data: mk("SL"), label: { fontSize: 10 },
          color: ["#14b8a6", "#38bdf8", "#94a3b8"] },
        { name: "HL", type: "pie", radius: ["28%", "52%"], center: ["72%", "48%"],
          data: mk("HL"), label: { fontSize: 10 },
          color: ["#fb7185", "#38bdf8", "#f59e0b", "#94a3b8"] },
      ],
    });
    charts.push(chart);
  }

  // ------------------------------------------------------------------ tree
  function renderTree(el, args) {
    if (args && args[0]) state.selectedTopic = decodeURIComponent(args[0]);
    el.innerHTML = `
      <div class="two-col">
        <div class="card pad">
          <h3>知识树（点击节点查看详情）</h3>
          <div class="chart tall" id="tree-chart"></div>
        </div>
        <div id="topic-detail"></div>
      </div>`;
    const chart = echarts.init($("#tree-chart"));
    const data = {
      name: "IB Economics",
      children: D.syllabus.map((u) => ({
        name: u.short_zh + " " + u.title_en,
        itemStyle: { color: "#8b5cf6" },
        children: u.topics.map((t) => ({
          name: t.id + "  " + t.title_zh,
          itemStyle: { color: LEVEL_COLOR[t.level] },
          symbolSize: 11,
          _topicId: t.id,
        })),
      })),
    };
    chart.setOption({
      tooltip: { trigger: "item", formatter: (p) => {
        const t = p.data._topicId ? D.topicById[p.data._topicId] : null;
        return t ? `<b>${esc(t.id)} ${esc(t.title_en)}</b><br>${esc(t.title_zh)}<br>${esc(t.level === "hl" ? "HL 专属" : "SL + HL")}` : esc(p.name);
      } },
      series: [{
        type: "tree", data: [data], layout: "orthogonal", orient: "LR",
        top: "4%", left: "4%", bottom: "4%", right: "14%",
        symbol: "circle", symbolSize: 10,
        roam: true, expandAndCollapse: true, initialTreeDepth: -1,
        label: { fontSize: 11, position: "left", verticalAlign: "middle", align: "right" },
        leaves: { label: { position: "right", align: "left" } },
        lineStyle: { color: "#cbd5e1", width: 1.4 },
        emphasis: { focus: "descendant" },
      }],
    });
    chart.on("click", (p) => {
      if (p.data && p.data._topicId) { state.selectedTopic = p.data._topicId; renderTopicDetail(); }
    });
    charts.push(chart);
    renderTopicDetail();
  }

  function topicLinks(id) {
    const books = [], papers = [], ias = [];
    (D.textbooks || []).forEach((b) => (b.chapters || []).forEach((ch) => {
      if ((ch.topics || []).some((t) => t.id === id))
        books.push({ name: b.name, publisher: b.publisher, path: b.local_path, page: ch.page, title: ch.title, text_rel: b.text_rel });
    }));
    (D.papers || []).forEach((p) => {
      if ((p.topics || []).some((t) => t.id === id)) papers.push(p);
    });
    (D.ias || []).forEach((i) => {
      if ((i.topics || []).some((t) => t.id === id)) ias.push(i);
    });
    return { books, papers, ias };
  }

  function renderTopicDetail() {
    const box = $("#topic-detail");
    const id = state.selectedTopic;
    const t = id && D.topicById[id];
    if (!t) { box.innerHTML = '<div class="detail-panel"><div class="empty">点击左侧主题节点查看详情</div></div>'; return; }
    const links = topicLinks(id);
    const concepts = (t.key_concepts || []).map((c) =>
      `<span class="concept-tag" onclick="location.hash='#/glossary/${encodeURIComponent(c)}'">${esc(c)}</span>`).join("");
    const related = (D.relatedByTopic[id] || []).map((r) => `
      <div style="font-size:13px;margin:6px 0;padding:8px 10px;background:var(--surface-2);border-radius:8px">
        <span class="pill" style="background:var(--violet-soft);color:#6d28d9">${REL_TYPE_LABEL[r.type] || esc(r.type)}</span>
        <a href="#/topic/${encodeURIComponent(r.tid)}"><b>${esc(r.tid)} ${esc(r.title_en)}</b></a>
        <span class="muted">${esc(r.title_zh)}</span>
        <div style="color:var(--ink-2);margin-top:3px">${esc(r.rel_zh)}</div>
      </div>`).join("");
    const relatedSection = related
      ? `<div class="sec-title">关联知识点（经济学是一个整体）</div>${related}` : "";

    const guide = (D.topic_exam_guide || {})[id];
    const guideSection = guide ? `
      <div class="sec-title">答题指南 · 答什么 / 怎么答</div>
      <div class="card pad" style="background:var(--sky-soft);margin:4px 0">
        ${(guide.diagrams && guide.diagrams.length) ? `<div style="font-size:13px;margin-bottom:6px"><b>📐 核心图表（答什么）</b>${guide.diagrams.map((d) => `<div style="margin:2px 0 2px 10px">· ${esc(d)}</div>`).join("")}</div>` : ""}
        <div style="font-size:13px"><b>💡 答题要点 / 易错点（怎么答）</b>${guide.tips.map((t) => `<div style="margin:2px 0 2px 10px">· ${esc(t)}</div>`).join("")}</div>
        <details style="font-size:12.5px;margin-top:8px;color:var(--ink-2)">
          <summary style="cursor:pointer">📐 命令词 / AO 答题方法速查</summary>
          ${(D.answer_guide || []).map((a) => `<div style="margin:6px 0"><b>${esc(a.name_zh)}</b>：${esc(a.how_zh)}</div>`).join("")}
        </details>
      </div>` : "";

    const reports = (D.reportsByTopic[id] || []).slice(0, 3);
    const reportSection = reports.length ? `
      <div class="sec-title">官方考官报告依据（评分逻辑）</div>
      <div style="font-size:13px">${reports.map((r) => `<a class="pdf-link" href="${pdfUrl(r.local_path)}" target="_blank">📋 ${esc(r.name)}</a>`).join("<br>")}</div>` : "";
    const ext = (t.hl_extensions || []).length
      ? `<div class="sec-title">HL 拓展</div>` + t.hl_extensions.map((x, i) =>
          `<p style="font-size:13px;color:#c2410c">${i % 2 === 0 ? "· " + esc(x) : "  <span style='color:var(--ink-2)'>" + esc(x) + "</span>"}</p>`).join("")
      : "";
    const bookList = links.books.length
      ? `<div class="sec-title">教材原文（${links.books.length}）</div>` + links.books.slice(0, 8).map((b, i) =>
          `<div style="font-size:13px;margin:6px 0">
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
              <a class="pdf-link" href="${pdfUrl(b.path, b.page)}" target="_blank">📖 ${esc(b.name)}</a>
              ${b.text_rel ? `<span class="pill" style="background:var(--sky-soft);color:#0369a1;cursor:pointer" data-excerpt="${i}">📄 原文摘录</span>` : ""}
            </div>
            <div style="color:var(--ink-3)">${esc(b.title || "")} · p.${b.page}</div>
            <div class="excerpt" id="excerpt-${i}" style="display:none"></div>
          </div>`).join("")
      : "";
    const paperList = links.papers.length
      ? `<div class="sec-title">相关真题（${links.papers.length}）</div>` + links.papers.slice(0, 6).map((p) =>
          `<div style="font-size:13px;margin:4px 0"><a href="${pdfUrl(p.local_path)}" target="_blank">📝 ${esc(p.year)} ${esc(p.session)} · Paper ${p.paper} ${esc(p.tz||"")} ${esc(p.level||"")}</a></div>`).join("")
      : "";
    const iaList = links.ias.length
      ? `<div class="sec-title">相关 IA（${links.ias.length}）</div>` + links.ias.slice(0, 4).map((i) =>
          `<div style="font-size:13px;margin:4px 0"><a href="${pdfUrl(i.local_path)}" target="_blank">✍️ ${esc(i.name)}</a></div>`).join("")
      : "";

    box.innerHTML = `
      <div class="detail-panel">
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
          <h4 style="margin:0">${esc(t.id)} ${esc(t.title_en)}</h4>${levelBadge(t.level)}${heatBadge(id)}
        </div>
        <div class="zh">${esc(t.title_zh)}</div>
        <p>${esc(t.desc_en)}</p>
        <p style="color:var(--ink-2)">${esc(t.desc_zh)}</p>
        ${relatedSection}
        ${guideSection}${reportSection}
        ${ext}
        <div class="sec-title">核心概念</div><div>${concepts || '<span class="empty" style="padding:0">—</span>'}</div>
        ${bookList}${paperList}${iaList}
      </div>`;
    box.querySelectorAll("[data-excerpt]").forEach((btn) =>
      btn.addEventListener("click", () => {
        const i = Number(btn.dataset.excerpt);
        const b = links.books[i];
        const c = box.querySelector(`#excerpt-${i}`);
        if (!c) return;
        if (c.style.display !== "none") { c.style.display = "none"; return; }
        c.style.display = "block"; c.textContent = "加载中…";
        showExcerpt(c, b);
      }));
  }

  function showExcerpt(container, book) {
    if (!book.text_rel) { container.textContent = "（无文本层，请直接打开 PDF）"; return; }
    fetch(assetUrl("text/" + book.text_rel))
      .then((r) => r.text())
      .then((txt) => {
        const pages = txt.split("\x0c");
        const p = book.page ? (pages[book.page - 1] || "") : pages.join("\n");
        container.textContent = p.trim().slice(0, 1500) || "（本页无文本层）";
      })
      .catch(() => { container.textContent = "加载原文失败。"; });
  }

  // ------------------------------------------------------------------ graph
  function renderGraph(el) {
    const types = ["unit", "topic", "concept", "paper", "ia", "textbook"];
    const labels = { unit: "单元", topic: "主题", concept: "概念", paper: "真题", ia: "IA", textbook: "教材" };
    const defOn = { unit: true, topic: true, concept: true, paper: false, ia: false, textbook: false };
    el.innerHTML = `
      <div class="card pad">
        <h3>知识图谱</h3>
        <div class="filters" id="graph-filters">
          ${types.map((t) => `<span class="chip ${defOn[t] ? "on" : ""}" data-t="${t}">${labels[t]}</span>`).join("")}
        </div>
        <div class="chart tall" id="graph-chart"></div>
      </div>`;
    const sel = { ...defOn };
    let chart = null;
    function draw() {
      const nodes = D.graph.nodes.filter((n) => sel[n.type]);
      const ids = new Set(nodes.map((n) => n.id));
      const edges = D.graph.edges.filter((e) => ids.has(e.source) && ids.has(e.target));
      const data = nodes.map((n) => {
        const o = {
          id: n.id, name: n.name,
          category: types.indexOf(n.type), // numeric category index (0-5)
          symbolSize: n.type === "unit" ? 46 : n.type === "topic" ? 32 : n.type === "concept" ? 16 : 20,
          itemStyle: { color: TYPE_COLOR[n.type] },
        };
        if (n.type === "topic" && n.level === "hl") o.itemStyle = { color: "#f97316" };
        return o;
      });
      if (!chart) { chart = echarts.init($("#graph-chart")); charts.push(chart); }
      chart.setOption({
        tooltip: { formatter: (p) => {
          const n = p.data;
          const full = D.graph.nodes.find((x) => x.id === n.id) || {};
          return `<b>${esc(full.name || n.name)}</b>${full.name_zh ? "<br>" + esc(full.name_zh) : ""}<br><span class="muted">${esc(labels[full.type] || full.type || "")}</span>`;
        } },
        legend: [{ data: types.map((t) => ({ name: labels[t] })), bottom: 0 }],
        series: [{
          type: "graph", layout: "force", data, links: edges.map((e) => ({ source: e.source, target: e.target })),
          categories: types.map((t) => ({ name: labels[t], itemStyle: { color: TYPE_COLOR[t] } })),
          roam: true, draggable: true,
          force: { repulsion: 160, edgeLength: 70, gravity: 0.1, friction: 0.6, layoutAnimation: false },
          label: { show: true, fontSize: 9, color: "#475569", position: "right" },
          edgeSymbol: ["none", "arrow"], edgeSymbolSize: 6,
          lineStyle: { color: "#cbd5e1", width: 0.8, curveness: 0.05 },
          emphasis: { focus: "adjacency", lineStyle: { width: 2 } },
        }],
      }, true);
    }
    $("#graph-filters").addEventListener("click", (e) => {
      const chip = e.target.closest(".chip"); if (!chip) return;
      const t = chip.dataset.t; sel[t] = !sel[t]; chip.classList.toggle("on", sel[t]); draw();
    });
    draw();
  }

  // ------------------------------------------------------------------ hlsl
  function renderHlSl(el) {
    const units = D.syllabus.map((u) => `
      <div class="card pad" style="margin-bottom:16px">
        <h3 style="display:flex;justify-content:space-between;align-items:center">
          <span>${esc(u.title_zh)} <span class="muted" style="font-size:13px">${esc(u.title_en)}</span></span>
          <span class="badge unit">${u.topics.filter(t=>t.level==='hl').length} HL 专属</span>
        </h3>
        <table><thead><tr><th>主题</th><th>层级</th><th>HL 拓展要点</th></tr></thead><tbody>
        ${u.topics.map((t) => `
          <tr ${t.level === "hl" ? 'style="background:var(--hl-soft)"' : ""}>
            <td><a href="#/topic/${encodeURIComponent(t.id)}">${esc(t.id)} ${esc(t.title_en)}</a>
              <div class="muted" style="font-size:12px">${esc(t.title_zh)}</div></td>
            <td>${levelBadge(t.level)}</td>
            <td style="font-size:13px">${(t.hl_extensions || []).filter((_, i) => i % 2 === 0).map((x) => "· " + esc(x)).join("<br>") || (t.level === "hl" ? "整主题仅 HL" : "—")}</td>
          </tr>`).join("")}
        </tbody></table>
      </div>`).join("");
    el.innerHTML = `
      <div class="note" style="margin-bottom:16px">💡 <b>HL 与 SL 的区别</b>：HL 增加三个微观专属主题（2.10 信息不对称、2.11 市场力量、2.12 市场与公平），并有额外的评估/拓展内容（下表「HL 拓展要点」），且需参加 <b>Paper 3 政策题</b>。SL 与 HL 共享大部分核心内容与 IA 形式。</div>
      ${units}`;
  }

  // ------------------------------------------------------------------ glossary
  function renderGlossary(el, args) {
    const q = (args && args[0]) ? decodeURIComponent(args[0]) : state.glossaryQ;
    const open = (args && args[0]) ? decodeURIComponent(args[0]) : null;
    el.innerHTML = `
      <div class="search" style="margin:0 0 14px;position:relative">
        <span class="mag" style="position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--ink-3)">🔍</span>
        <input id="gq" style="width:100%" placeholder="筛选术语（中英）…" value="${esc(q)}">
      </div>
      <div id="gloss-list"></div>`;
    $("#gq").addEventListener("input", (e) => {
      state.glossaryQ = e.target.value; renderGlossList(e.target.value, open);
    });
    renderGlossList(q, open);
  }

  function renderGlossList(q, openTerm) {
    const ql = (q || "").trim().toLowerCase();
    const list = D.glossary.filter((g) => !ql ||
      g.term_en.toLowerCase().includes(ql) || g.term_zh.includes(ql) ||
      g.def_en.toLowerCase().includes(ql) || g.def_zh.includes(ql) ||
      (g.more || "").includes(ql) || (g.example || "").includes(ql) ||
      (g.part_of || "").includes(ql) || (g.links || []).some((l) => l.term.toLowerCase().includes(ql)));
    const SUBJ_SHORT = { "ib-econ": "IB经济", "al-econ": "AL经济", "ib-bus": "IB商科", "al-bus": "AL商科", "igcse-bus": "IG商科", "comp": "竞赛" };
    const groups = {};
    list.forEach((g) => {
      const t = D.topicById[g.topic];
      const key = t ? `${t.unit_title_zh}` : "其他";
      (groups[key] = groups[key] || []).push(g);
    });
    $("#gloss-list").innerHTML = Object.entries(groups).map(([unit, arr]) => `
      <div class="card pad" style="margin-bottom:14px">
        <h3>${esc(unit)} <span class="muted" style="font-size:13px">${arr.length} 个术语</span></h3>
        ${arr.map((g) => `
          <div class="gloss-item" style="border-bottom:1px solid var(--line);padding:10px 2px" data-term="${esc(g.term_en)}">
            <div style="display:flex;align-items:baseline;gap:8px;cursor:pointer" class="gloss-head">
              <b>${esc(g.term_en)}</b><span class="muted" style="font-size:13px">${esc(g.term_zh)}</span>
              <a href="#/topic/${encodeURIComponent(g.topic)}" class="badge tag" style="margin-left:auto">${esc(g.topic)}</a>
              ${g.cluster ? `<span class="badge" style="background:#8b5cf61a;color:#8b5cf6">${esc(g.cluster)}</span>` : ""}
            </div>
            <div class="gloss-body" style="display:${openTerm === g.term_en ? "block" : "none"};margin-top:8px;color:var(--ink-2);font-size:13.5px;line-height:1.6">
              <div>🇬🇧 ${esc(g.def_en)}</div>
              <div style="margin-top:4px">🇨🇳 ${esc(g.def_zh)}</div>
              ${g.more ? `<div style="margin-top:8px;color:var(--ink)"><b style="color:#0d9488">📖 详解</b>　${esc(g.more)}</div>` : ""}
              ${g.example ? `<div style="margin-top:5px"><b style="color:#f59e0b">💡 例</b>　${esc(g.example)}</div>` : ""}
              ${g.part_of ? `<div style="margin-top:5px"><b style="color:#8b5cf6">🧩 上位概念</b>　${esc(g.part_of)}</div>` : ""}
              ${g.prereq ? `<div style="margin-top:3px"><b style="color:#d97706">🔑 先决条件</b>　${esc(g.prereq)}</div>` : ""}
              ${(g.links || []).length ? `<div style="margin-top:7px"><b style="color:#0ea5e9">🔗 同概念 · 跨科目</b>　${g.links.map((l) =>
                `<a href="hub.html#/s/${l.subj}/glossary/${encodeURIComponent(l.term)}" class="badge"
                    style="background:#0ea5e91e;color:#0284c7;text-decoration:none"
                    title="${esc(l.note || "")}">${esc(SUBJ_SHORT[l.subj] || l.subj)} · ${esc(l.term)}</a>`).join(" ")}</div>` : ""}
            </div>
          </div>`).join("")}
      </div>`).join("") || '<div class="empty">未找到匹配术语</div>';
    document.querySelectorAll(".gloss-head").forEach((h) =>
      h.addEventListener("click", () => {
        const body = h.parentElement.querySelector(".gloss-body");
        body.style.display = body.style.display === "none" ? "block" : "none";
      }));
  }

  // ------------------------------------------------------------------ papers
  function renderPapers(el, args) {
    const F = state.paperFilter;
    if (args && args[0]) { F.year = args[0]; F.session = args[1] || null; }
    const years = [...new Set(D.papers.map((p) => p.year))].sort();
    const sessions = ["May", "November"];
    const levels = ["SL", "HL"];
    const paperNos = [1, 2, 3];
    el.innerHTML = `
      <div class="card pad" style="margin-bottom:16px">
        <h3>各主题出题频次</h3>
        <div class="chart short" id="pp-freq"></div>
      </div>
      <div class="card pad">
        <h3>真题列表</h3>
        <div class="filters">
          <span class="chip ${!F.year ? "on" : ""}" data-k="year" data-v="">全部年份</span>
          ${years.map((y) => `<span class="chip ${F.year == y ? "on" : ""}" data-k="year" data-v="${y}">${y}</span>`).join("")}
        </div>
        <div class="filters">
          <span class="chip ${!F.session ? "on" : ""}" data-k="session" data-v="">全部考季</span>
          ${sessions.map((s) => `<span class="chip ${F.session === s ? "on" : ""}" data-k="session" data-v="${s}">${s}</span>`).join("")}
        </div>
        <div class="filters">
          <span class="chip ${!F.level ? "on" : ""}" data-k="level" data-v="">全部级别</span>
          ${levels.map((l) => `<span class="chip ${F.level === l ? "on" : ""}" data-k="level" data-v="${l}">${l}</span>`).join("")}
        </div>
        <div class="filters">
          <span class="chip ${!F.paper ? "on" : ""}" data-k="paper" data-v="">全部卷号</span>
          ${paperNos.map((p) => `<span class="chip ${F.paper == p ? "on" : ""}" data-k="paper" data-v="${p}">Paper ${p}</span>`).join("")}
        </div>
        <div id="pp-list"></div>
      </div>`;
    renderFreqChart($("#pp-freq"));
    document.querySelectorAll(".filters .chip").forEach((c) =>
      c.addEventListener("click", () => {
        const k = c.dataset.k, v = c.dataset.v;
        F[k] = v === "" ? null : (k === "paper" ? Number(v) : v);
        renderPapers(el, null);
      }));
    const list = D.papers.filter((p) =>
      (!F.year || p.year == F.year) && (!F.session || p.session === F.session) &&
      (!F.level || p.level === F.level) && (!F.paper || p.paper === F.paper));
    $("#pp-list").innerHTML = list.map((p) => `
      <div class="list-item">
        <div class="grow">
          <div class="t">${esc(p.year)} ${esc(p.session)} · Paper ${p.paper} ${esc(p.tz || "")} · <span class="badge ${p.level === "HL" ? "hl" : "sl"}">${esc(p.level)}</span></div>
          <div class="d">${(p.topics || []).map((t) => `<span class="badge tag" style="margin:2px 4px 0 0">${esc(t.id)} ${esc(D.topicById[t.id]?.title_zh || "")}</span>`).join("")}</div>
        </div>
        <div style="display:flex;gap:8px;white-space:nowrap">
          <a href="${pdfUrl(p.local_path)}" target="_blank" class="pill" style="background:var(--brand-soft);color:#0f766e">📝 题目</a>
          ${p.markscheme_path ? `<a href="${pdfUrl(p.markscheme_path)}" target="_blank" class="pill" style="background:var(--amber-soft);color:#b45309">✔ 评分方案</a>` : ""}
        </div>
      </div>`).join("") || '<div class="empty">无匹配真题</div>';
  }

  function renderFreqChart(dom) {
    const freq = D.stats.topic_freq || {};
    const data = Object.entries(freq).map(([id, v]) => ({ name: id, value: v })).sort((a, b) => b.value - a.value);
    const chart = echarts.init(dom);
    chart.setOption({
      tooltip: { trigger: "axis" },
      grid: { left: 40, right: 16, top: 16, bottom: 30 },
      xAxis: { type: "category", data: data.map((d) => d.name), axisLabel: { rotate: 45, fontSize: 10 } },
      yAxis: { type: "value", name: "被标记次数" },
      series: [{ type: "bar", data: data.map((d) => d.value),
        itemStyle: { color: "#14b8a6", borderRadius: [4, 4, 0, 0] } }],
    });
    charts.push(chart);
  }

  // ------------------------------------------------------------------ ia
  function renderIa(el) {
    const sections = [
      { key: "work", title: "📝 学生作业原文", sub: "IBO 官方评估的学生评论原文（含基于真实新闻的三篇评论）", color: "var(--brand-soft)", accent: "#0f766e" },
      { key: "comment", title: "🖋 考官评分评语", sub: "对应的评分细则与考官批注，配合「原文」对照学习", color: "var(--amber-soft)", accent: "#b45309" },
      { key: "compilation", title: "📚 合集文件", sub: "IBO 评估学生作业的完整合集", color: "var(--violet-soft)", accent: "#6d28d9" },
    ];
    el.innerHTML = `
      <div class="note" style="margin-bottom:16px">✍️ <b>IA（内部评估）</b>：3 篇基于真实新闻的评论（每篇约 800 词），分别取材于微观、宏观与全球经济。「学生作业原文」与「考官评分评语」已分开列出，可对照学习。</div>
      ${sections.map((s, si) => {
        const list = D.ias.filter((i) => i.kind === s.key);
        return `<div class="card pad" style="margin-bottom:16px">
          <h3 style="color:${s.accent}">${s.title} <span class="muted" style="font-size:13px">${list.length} 个</span></h3>
          <div class="muted" style="font-size:12.5px;margin-bottom:6px">${s.sub}</div>
          ${list.map((i, ii) => {
            const id = `ia-ex-${si}-${ii}`;
            return `<div class="list-item" style="align-items:flex-start">
              <div class="grow">
                <div class="t">${esc(i.name)}</div>
                <div class="d">${(i.topics || []).map((t) => `<span class="badge tag" style="margin:2px 4px 0 0">${esc(t.id)} ${esc(D.topicById[t.id]?.title_zh || "")}</span>`).join("") || "（自动标记）"}</div>
                ${i.text_rel ? `<div class="excerpt" id="${id}" style="display:none;margin-top:8px"></div>` : ""}
              </div>
              <div style="display:flex;gap:6px;white-space:nowrap;flex-direction:column;align-items:flex-end">
                ${i.text_rel ? `<span class="pill" style="background:var(--sky-soft);color:#0369a1;cursor:pointer" data-iaex="${id}" data-rel="${esc(i.text_rel)}">📄 原文</span>` : ""}
                <a href="${pdfUrl(i.local_path)}" target="_blank" class="pill" style="background:${s.color};color:${s.accent}">PDF</a>
              </div>
            </div>`;
          }).join("") || '<div class="empty" style="padding:12px">暂无</div>'}
        </div>`;
      }).join("")}`;
    document.querySelectorAll("[data-iaex]").forEach((btn) =>
      btn.addEventListener("click", () => {
        const c = document.getElementById(btn.dataset.iaex);
        if (!c) return;
        if (c.style.display !== "none") { c.style.display = "none"; return; }
        c.style.display = "block"; c.textContent = "加载中…";
        showExcerpt(c, { text_rel: btn.dataset.rel });
      }));
  }

  // ------------------------------------------------------------------ textbooks
  function renderTextbooks(el) {
    const byPub = {};
    (D.textbooks || []).forEach((b) => {
      const p = b.publisher || "其他";
      (byPub[p] = byPub[p] || []).push(b);
    });
    el.innerHTML = `
      <div class="note" style="margin-bottom:16px">📚 教材按类型标注：<span class="badge both">📘 主教材</span> <span class="badge hl">🎯 学习指南 · 难点详解</span> <span class="badge sl">📝 练习册</span> <span class="badge tag">✔ 答案</span>。「学习指南」对教材中较复杂、易错的内容做详解，建议配合主教材对照使用。</div>
      ` + Object.entries(byPub).map(([pub, books]) => `
      <div class="card pad" style="margin-bottom:16px">
        <h3>${esc(pub)} <span class="muted" style="font-size:13px">${books.length} 本</span></h3>
        <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px">
        ${books.map((b) => `
          <div class="card pad" style="background:var(--surface-2)">
            <div style="display:flex;gap:14px;align-items:flex-start">
              ${b.cover ? `<img src="${esc(b.cover)}" alt="封面" loading="lazy" style="width:96px;height:auto;border-radius:6px;box-shadow:var(--shadow-sm);flex:0 0 auto">`
                : `<div style="width:96px;aspect-ratio:3/4;flex:0 0 auto;display:grid;place-items:center;background:var(--surface);border-radius:6px;color:var(--ink-3);font-size:11px">无封面</div>`}
              <div style="flex:1;min-width:0">
                <div style="font-weight:600;font-size:13.5px;line-height:1.4">${esc(b.name)}</div>
                <div style="margin:4px 0">${resourceBadge(b.resource_type)}</div>
                <div style="margin-top:6px"><a href="${pdfUrl(b.local_path, 1)}" target="_blank" class="pill" style="background:var(--brand-soft);color:#0f766e">打开教材（${b.pages || "?"} 页）</a></div>
                ${(b.chapters || []).length ? `<div class="sec-title" style="margin-top:10px">章节 → 主题</div>
                  <div>${b.chapters.slice(0, 18).map((ch) => `
                    <div style="font-size:12px;padding:3px 0;border-bottom:1px dashed var(--line)">
                      <a class="pdf-link" href="${pdfUrl(b.local_path, ch.page)}" target="_blank">${esc(ch.title)}</a> <span class="muted">p.${ch.page}</span>
                      ${(ch.topics || []).map((t) => `<span class="badge tag">${esc(t.id)}</span>`).join("")}
                    </div>`).join("")}</div>` : ""}
              </div>
            </div>
          </div>`).join("")}
        </div>
      </div>`).join("");
  }

  // ------------------------------------------------------------------ diagrams
  function renderDiagrams(el) {
    el.innerHTML = `
      <div class="note" style="margin-bottom:14px">📈 图表是 IB 经济学得分的关键：<b>画图、标点、说线、算面积</b>。「图表解析」系统梳理点移动、线移动与面积含义；「图表训练」做自测题即时检验。</div>
      <div class="filters" id="dg-tabs" style="margin:0 0 14px">
        <span class="chip on" data-tab="learn">📖 图表解析</span>
        <span class="chip" data-tab="quiz">🎯 图表训练（自测）</span>
      </div>
      <div id="dg-body"></div>`;

    function showLearn() {
      const groups = {};
      D.diagrams.forEach((d) => {
        const t = D.topicById[d.topic];
        const unit = t ? t.unit_title_zh : "其他";
        (groups[unit] = groups[unit] || []).push(d);
      });
      $("#dg-body").innerHTML = Object.entries(groups).map(([unit, arr]) => `
        <div class="card pad" style="margin-bottom:16px">
          <h3>${esc(unit)} <span class="muted" style="font-size:13px">${arr.length} 个图表</span></h3>
          <div class="grid cols-2">
          ${arr.map((d) => `
            <div class="card pad" style="background:var(--surface-2)">
              <div style="display:flex;justify-content:space-between;align-items:baseline;gap:8px">
                <b style="font-size:14px">${esc(d.name_zh)}</b>
                <a href="#/topic/${encodeURIComponent(d.topic)}" class="badge tag">${esc(d.topic)}</a>
              </div>
              <div class="muted" style="font-size:12.5px;margin:3px 0 6px">${esc(d.name_en)}</div>
              <img src="assets/diagrams/${d.id}.png" alt="${esc(d.name_zh)}" loading="lazy" style="width:100%;max-width:400px;border-radius:8px;margin:4px 0 8px;background:#fff;border:1px solid var(--line)">
              <div style="font-size:13px;line-height:1.6">${esc(d.what)}</div>
              <div class="sec-title">线移动</div><div style="font-size:13px;line-height:1.5">${esc(d.lines)}</div>
              <div class="sec-title">点移动</div><div style="font-size:13px;line-height:1.5">${esc(d.points)}</div>
              <div class="sec-title">面积含义</div><div style="font-size:13px;line-height:1.5">${esc(d.areas)}</div>
            </div>`).join("")}
          </div>
        </div>`).join("");
    }

    function showQuiz() {
      const bank = [];
      D.diagrams.forEach((d) => (d.practice || []).forEach((p) => bank.push({ ...p, diagram: d })));
      const qs = bank.slice().sort(() => Math.random() - 0.5);
      let idx = 0, score = 0, answered = false;
      function renderQ() {
        const q = qs[idx];
        if (!q) {
          $("#dg-body").innerHTML = `<div class="card pad"><h3>🎉 训练完成</h3><div style="font-size:26px;font-weight:800;color:var(--brand)">${score} / ${qs.length}</div>
            <div class="muted" style="margin-top:6px">${score >= qs.length * 0.8 ? "掌握得很好！" : score >= qs.length * 0.5 ? "继续巩固图表要点。" : "建议回到「图表解析」再复习一遍。"}</div>
            <button class="pill" style="background:var(--brand);color:#fff;border:none;cursor:pointer;margin-top:14px" id="dg-restart">再来一轮</button></div>`;
          $("#dg-restart").onclick = () => { idx = 0; score = 0; renderQ(); };
          return;
        }
        answered = false;
        $("#dg-body").innerHTML = `
          <div class="card pad">
            <div style="display:flex;justify-content:space-between;color:var(--ink-3);font-size:12.5px">
              <span>第 ${idx + 1} / ${qs.length} 题</span><span>得分 ${score}</span>
            </div>
            <h3 style="margin:10px 0 14px">${esc(q.q)}</h3>
            <div style="display:grid;gap:8px">
              ${q.opts.map((o, oi) => `<div data-oi="${oi}" style="background:var(--surface-2);border:1px solid var(--line);padding:11px 14px;cursor:pointer;font-size:14px;border-radius:10px;transition:all .12s">${String.fromCharCode(65 + oi)}. ${esc(o)}</div>`).join("")}
            </div>
            <div id="dg-feedback" style="margin-top:14px"></div>
          </div>`;
        $("#dg-body").querySelectorAll("[data-oi]").forEach((btn) => btn.addEventListener("click", () => {
          if (answered) return;
          answered = true;
          const oi = Number(btn.dataset.oi);
          const qq = qs[idx];
          const correct = oi === qq.a;
          if (correct) score++;
          $("#dg-body").querySelectorAll("[data-oi]").forEach((b) => {
            const i = Number(b.dataset.oi);
            if (i === qq.a) b.style.background = "var(--sl-soft)";
            else if (i === oi) b.style.background = "var(--coral-soft)";
          });
          $("#dg-feedback").innerHTML = `
            <div style="padding:10px 14px;border-radius:8px;background:${correct ? "var(--sl-soft)" : "var(--coral-soft)"}">
              <b>${correct ? "✅ 正确" : "❌ 错误"}</b> · ${esc(qq.why)}
              <div class="muted" style="font-size:12px;margin-top:3px">图表：${esc(qq.diagram.name_zh)}（${esc(qq.diagram.topic)}）</div>
            </div>
            <button class="pill" style="background:var(--brand);color:#fff;border:none;cursor:pointer;margin-top:12px" id="dg-next">${idx + 1 >= qs.length ? "查看结果" : "下一题"}</button>`;
          $("#dg-next").onclick = () => { idx++; renderQ(); };
        }));
      }
      renderQ();
    }

    function setTab(t) {
      document.querySelectorAll("#dg-tabs .chip").forEach((c) => c.classList.toggle("on", c.dataset.tab === t));
      if (t === "learn") showLearn(); else showQuiz();
    }
    document.querySelectorAll("#dg-tabs .chip").forEach((c) => c.addEventListener("click", () => setTab(c.dataset.tab)));
    showLearn();
  }

  // ------------------------------------------------------------------ charts
  function renderCharts(el) {
    const heat = (D.stats.topic_heat || []).slice().sort((a, b) => b.freq - a.freq);
    const hot = heat.filter((h) => h.heat === "hot");
    const cold = heat.filter((h) => h.heat === "cold");
    const heatItem = (h) => {
      const t = D.topicById[h.id]; if (!t) return "";
      return `<div style="font-size:13px;padding:4px 0;border-bottom:1px dashed var(--line)"><a href="#/topic/${esc(h.id)}"><b>${esc(h.id)}</b> ${esc(t.title_zh)}</a> <span class="muted">· ${h.freq} 次</span></div>`;
    };
    el.innerHTML = `
      <div class="card pad" style="margin-bottom:16px">
        <h3>主题热度 — 近年真题「常考 vs 冷门」</h3>
        <div class="chart tall" id="c-heat"></div>
        <div class="grid cols-2" style="margin-top:14px">
          <div class="card pad" style="background:var(--hl-soft)">
            <h3 style="color:#c2410c;margin-top:0">🔥 常考主题（高频）</h3>
            ${hot.map(heatItem).join("") || '<div class="muted">暂无</div>'}
          </div>
          <div class="card pad" style="background:var(--surface-2)">
            <h3 style="margin-top:0">❄️ 冷门主题（低频）</h3>
            ${cold.map(heatItem).join("") || '<div class="muted">暂无</div>'}
          </div>
        </div>
      </div>
      <div class="grid cols-2">
        <div class="card pad"><h3>真题年份分布</h3><div class="chart" id="c-year"></div></div>
        <div class="card pad"><h3>真题级别 / 考季</h3><div class="chart" id="c-level"></div></div>
        <div class="card pad"><h3>命令词出现频率（真题）</h3><div class="chart" id="c-cmd"></div></div>
        <div class="card pad"><h3>大纲结构</h3><div class="chart" id="c-struct"></div></div>
      </div>`;
    // topic heat bar chart
    mkBar($("#c-heat"), heat.map((h) => h.id), heat.map((h) => h.freq), "#fb7185");
    // year distribution
    const y = D.stats.paper_by_year || {};
    const yk = Object.keys(y).sort();
    mkBar($("#c-year"), yk, yk.map((k) => y[k]), "#38bdf8");
    // level / session pie
    const lv = D.stats.paper_by_level || {}, ss = D.stats.paper_by_session || {};
    mkPie($("#c-level"), [
      { name: "SL", value: lv.SL || 0 }, { name: "HL", value: lv.HL || 0 },
      { name: "May", value: ss.May || 0 }, { name: "November", value: ss.November || 0 },
    ], ["#10b981", "#f97316", "#0ea5a4", "#8b5cf6"]);
    // command terms
    const c = D.stats.command_term_freq || {};
    const ck = Object.keys(c);
    mkBar($("#c-cmd"), ck, ck.map((k) => c[k]), "#fb7185");
    // structure: topics per unit
    mkBar($("#c-struct"), D.syllabus.map((u) => u.short_zh),
      D.syllabus.map((u) => u.topics.length), "#14b8a6");
  }

  function mkBar(dom, cats, vals, color) {
    const chart = echarts.init(dom);
    chart.setOption({
      tooltip: { trigger: "axis" },
      grid: { left: 40, right: 16, top: 16, bottom: 50 },
      xAxis: { type: "category", data: cats, axisLabel: { rotate: 40, fontSize: 10 } },
      yAxis: { type: "value" },
      series: [{ type: "bar", data: vals, itemStyle: { color, borderRadius: [4, 4, 0, 0] } }],
    });
    charts.push(chart);
  }
  function mkPie(dom, data, colors) {
    const chart = echarts.init(dom);
    chart.setOption({
      tooltip: { trigger: "item" }, legend: { bottom: 0 },
      series: [{ type: "pie", radius: ["30%", "60%"], data, color: colors, label: { fontSize: 11 } }],
    });
    charts.push(chart);
  }

  // ------------------------------------------------------------------ search
  function bindSearch() {
    const input = $("#search-input"), box = $("#search-results");
    input.addEventListener("input", () => {
      const q = input.value.trim().toLowerCase();
      if (!q) { box.style.display = "none"; return; }
      const hits = D.search_docs.filter((d) =>
        (d.title || "").toLowerCase().includes(q) || (d.title_zh || "").includes(q) ||
        (d.body || "").toLowerCase().includes(q)).slice(0, 24);
      const typeName = { topic: "主题", concept: "术语", paper: "真题", textbook: "教材" };
      box.innerHTML = hits.map((h) => `
        <div class="hit" onclick="location.hash='${esc(h.href.replace(/^#/, "#"))}'">
          <div><span class="badge tag">${typeName[h.type] || h.type}</span><span class="t">${esc(h.title)}</span> ${h.title_zh && h.title_zh !== h.title ? `<span class="muted">${esc(h.title_zh)}</span>` : ""}</div>
          <div class="d">${esc((h.body || "").slice(0, 80))}</div>
        </div>`).join("") || '<div class="empty" style="padding:16px">无结果</div>';
      box.style.display = "block";
    });
    document.addEventListener("click", (e) => {
      if (!e.target.closest(".search")) box.style.display = "none";
    });
  }

  // ------------------------------------------------------------------ boot
  load().catch((e) => {
    $("#view").innerHTML = `<div class="empty">加载数据失败：${esc(e.message)}<br><br>请确认已在项目根目录运行<br><code>python3 -m http.server 8000</code><br>并已完成抓取、解析与分析（见 README）。</div>`;
  });
  bindSearch();
})();
