/* 学习地图 Hub — 五科目统一外壳：IB经济 / AL经济 / IB商科 / AL商科 / 竞赛知识。
 * Generic views per subject: overview / tree / glossary / quiz (+ topic detail).
 * IB econ deep features (papers/textbooks/IA/diagrams/graph) stay in index.html. */
(function () {
  "use strict";

  const KB = "../data/kb/";
  let INDEX = [];          // subject index
  const CACHE = {};        // subject id -> data
  let cur = null;          // current subject data
  let curId = "ib-econ";
  let MAP = null;          // mapping.json
  const MAP_BY_TOPIC = {}; // "subject:topic" -> [entries]
  const charts = [];
  const state = { glossaryQ: "", quizMode: null, quiz: null, mapFilter: { subject: null, comp: null } };

  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const LEVEL_COLOR = { hl: "#f97316", sl: "#10b981", both: "#14b8a6", a2: "#8b5cf6", as: "#38bdf8",
    conrad: "#ef4444", bpa: "#f59e0b" };
  const LEVEL_LABEL = { hl: "HL", sl: "SL", both: "核心", a2: "A2", as: "AS", conrad: "康莱德", bpa: "BPA" };

  function levelBadge(level) {
    const color = LEVEL_COLOR[level] || LEVEL_COLOR.both;
    const label = (cur.level_names && cur.level_names[level]) || LEVEL_LABEL[level] || level || "";
    return `<span class="badge" style="background:${color}22;color:${color}">${esc(label)}</span>`;
  }

  function heatBadge(t) {
    if (t.freq == null) return "";
    if (t.heat === "hot") return `<span class="badge hl" title="真题高频考点">🔥 常考 · ${t.freq} 卷</span>`;
    if (t.heat === "cold") return `<span class="badge tag" title="真题低频考点">❄️ 冷门 · ${t.freq} 卷</span>`;
    return `<span class="badge both" title="真题中频考点">中频 · ${t.freq} 卷</span>`;
  }

  // ------------------------------------------------------------------ load
  async function loadSubject(id) {
    if (CACHE[id]) return CACHE[id];
    const r = await fetch(KB + "subjects/" + id + ".json");
    const d = await r.json();
    d.topicById = {};
    d.topics.forEach((t) => (d.topicById[t.id] = t));
    CACHE[id] = d;
    return d;
  }

  async function boot() {
    const r = await fetch(KB + "subjects/index.json");
    INDEX = await r.json();
    try {
      const mr = await fetch(KB + "subjects/mapping.json");
      MAP = await mr.json();
      (MAP.entries || []).forEach((e) => e.matches.forEach((m) => {
        const k = m.subject + ":" + m.topic;
        (MAP_BY_TOPIC[k] = MAP_BY_TOPIC[k] || []).push({ entry: e, why: m.why });
      }));
    } catch (e) { /* mapping optional */ }
    window.addEventListener("hashchange", route);
    window.addEventListener("resize", () => charts.forEach((c) => c.resize()));
    route();
  }

  // ------------------------------------------------------------------ nav & router
  const NAV = [
    ["overview", "🏠", "总览 Overview"],
    ["tree", "🌳", "知识树 Topics"],
    ["guide", "💡", "答题指南 Exam Guide"],
    ["diagrams", "📈", "图表解析 Diagrams"],
    ["glossary", "📖", "术语表 Glossary"],
    ["models", "🧰", "模型工具箱 Models"],
    ["examq", "🗂️", "常见考题 Exam Bank"],
    ["quiz", "🎯", "练习问答 Quiz"],
    ["papers", "📝", "真题库 Papers"],
    ["iaee", "✍️", "IA·EE·大题写作"],
    ["resources", "📚", "教学资料 Resources"],
    ["mapping", "🗺️", "赛代学地图 Mapping"],
    ["progression", "🧭", "IG→AL 衔接 Progression"],
  ];

  const VIEW_TITLE = {
    overview: ["总览", "考试结构与大纲速览"],
    tree: ["知识树", "单元 → 主题，点击展开详情"],
    guide: ["答题指南", "各主题考点 · 易错点 · 图表"],
    glossary: ["术语表", "英中对照 · 可搜索"],
    models: ["模型工具箱", "商业模型 · 结构 · IG/AL 考法 · 竞赛应用 · 本地课件指引"],
    examq: ["常见考题", "真题切片 · 官方答案要点 · 典型题解析"],
    quiz: ["练习问答", "选择题自测 · 即时解析"],
    papers: ["真题库", "题目 · 评分方案 · 考官报告 · 考点频次"],
    iaee: ["IA·EE·大题写作", "结构模板 · 评分标准 · 常见失分"],
    resources: ["教学资料", "教材章节映射 · 指定阅读 · 官方文件"],
    diagrams: ["图表解析", "模型图 · 点线面积 · 训练"],
    mapping: ["赛代学地图", "竞赛概念 ↔ 学科知识点 双向匹配"],
    progression: ["IG→AL 衔接地图", "IG 打底 → AL 升级 · 关联与新增模块"],
    fitting: ["赛代学拟合", "竞赛 × 学科知识点对照"],
  };

  async function route() {
    const hash = location.hash.replace(/^#\/?/, "") || "overview";
    const parts = hash.split("/");
    let v = parts[0], arg = parts[1];
    if (v === "s") { curId = parts[1]; v = parts[2] || "overview"; arg = parts[3]; }
    cur = await loadSubject(curId);
    renderTabs();
    renderNav(v);
    const [t, s] = VIEW_TITLE[v] || VIEW_TITLE.overview;
    $("#page-title").textContent = t;
    $("#page-sub").textContent = `${cur.name_zh} · ${s}`;
    $("#brand-title").textContent = cur.name_zh;
    $("#brand-sub").textContent = cur.name_en;
    const logo = $("#brand-logo");
    logo.style.background = `linear-gradient(135deg, ${cur.accent}, #38bdf8)`;
    const dl = $("#deep-link");
    if (curId === "ib-econ") {
      dl.href = "index.html#/overview"; dl.textContent = "→ 进入 IB 经济完整站（真题/教材/IA/图表/图谱）";
    } else if (curId === "comp") {
      dl.href = "index.html#/overview"; dl.textContent = "→ 查看 IB 经济知识点详情（赛代学对应）";
    } else {
      dl.href = "index.html#/overview"; dl.textContent = "→ 前往 IB 经济资源站";
    }
    renderView(v, arg);
  }

  function renderTabs() {
    $("#subj-tabs").innerHTML = INDEX.map((s) => `
      <span class="subj-tab ${s.id === curId ? "on" : ""}" data-id="${s.id}"
            style="${s.id === curId ? `background:${s.accent}` : ""}">
        <span class="dot" style="background:${s.id === curId ? "#fff" : s.accent}"></span>
        ${esc(s.name_zh)}
        <span style="font-size:11px;opacity:.75">${s.topics} 主题</span>
      </span>`).join("");
    document.querySelectorAll(".subj-tab").forEach((el) =>
      el.addEventListener("click", () => { location.hash = `#/s/${el.dataset.id}/overview`; }));
  }

  function renderNav(view) {
    const items = NAV.filter(([id]) => id !== "papers" || curId === "igcse-bus")
      .filter(([id]) => id !== "progression" || curId === "igcse-bus" || curId === "al-bus")
      .filter(([id]) => id !== "models" || (cur.models && cur.models.length));
    $("#nav").innerHTML = items.map(([id, ico, label]) => `
      <a href="#/s/${curId}/${id}" class="${view === id ? "active" : ""}">
        <span class="ico">${ico}</span>${label}</a>`).join("");
  }

  function renderView(v, arg) {
    const el = $("#view");
    el.innerHTML = "";
    charts.length = 0;
    switch (v) {
      case "tree": renderTree(el, arg); break;
      case "guide": renderGuide(el); break;
      case "glossary": renderGlossary(el, arg); break;
      case "models": renderModels(el, arg); break;
      case "examq": renderExamq(el, arg); break;
      case "quiz": renderQuiz(el); break;
      case "papers": renderPapers(el); break;
      case "iaee": renderIaee(el); break;
      case "resources": renderResources(el); break;
      case "diagrams": renderDiagramsView(el); break;
      case "mapping": renderMapping(el); break;
      case "progression": renderProgression(el); break;
      default: renderOverview(el);
    }
  }

  // ------------------------------------------------------------------ overview
  function renderOverview(el) {
    const a = cur.assessment || {};
    const comps = a.SL || a.HL || a.components || [];
    const hasSplit = !!(a.SL && a.HL);
    el.innerHTML = `
      <div class="hero" style="background:linear-gradient(135deg,${cur.accent},#38bdf8)">
        <h2>${esc(cur.name_zh)} · ${esc(cur.name_en)}</h2>
        <p>${cur.syllabus.length} 个单元 · ${cur.topics.length} 个主题 · ${cur.glossary.length} 个术语 · ${cur.quiz.length} 道自测题。
        ${curId === "ib-econ" ? "本页为知识速览；真题、教材、IA、图表训练、知识图谱等在左侧底部「完整站」入口。" : ""}</p>
      </div>
      <div class="grid cols-4">
        <div class="stat teal"><div class="num">${cur.syllabus.length}</div><div class="label">单元</div></div>
        <div class="stat sky"><div class="num">${cur.topics.length}</div><div class="label">主题</div></div>
        <div class="stat coral"><div class="num">${cur.glossary.length}</div><div class="label">术语</div></div>
        <div class="stat amber"><div class="num">${cur.quiz.length}</div><div class="label">自测题</div></div>
      </div>
      <div class="card pad" style="margin-top:16px">
        <h3>考试结构 ${a.note ? `<span class="muted" style="font-size:12px">（${esc(a.note)}）</span>` : ""}</h3>
        ${hasSplit ? ["SL", "HL"].map((lv) => `
          <h4 style="margin:12px 0 6px">${lv === "HL" ? "HL 高级别" : "SL 标准级别"}</h4>
          ${tableFor(a[lv])}`).join("") : tableFor(comps)}
      </div>
      <div class="card pad" style="margin-top:16px">
        <h3>单元概览</h3>
        <div class="grid cols-2">
          ${cur.syllabus.map((u) => `
            <div class="unit-card" style="cursor:pointer" onclick="location.hash='#/s/${curId}/tree'">
              <div style="display:flex;justify-content:space-between;align-items:baseline">
                <b>${esc(u.title_zh)}</b>
                <span class="badge unit">${u.topics.length} 主题</span>
              </div>
              <div class="muted" style="font-size:12.5px;margin-top:4px">${esc(u.title_en)}</div>
            </div>`).join("")}
        </div>
      </div>`;
  }

  function tableFor(comps) {
    if (!comps.length) return '<div class="empty">—</div>';
    return `<table>
      <thead><tr><th>部分</th><th>时长</th><th>权重</th></tr></thead><tbody>
      ${comps.map((c) => `
        <tr><td>${esc(c.name_zh)}${c.note_zh ? `<div class="muted" style="font-size:12px">${esc(c.note_zh)}</div>` : ""}</td>
        <td>${esc(c.time || "—")}</td><td>${c.weight != null ? c.weight + "%" : "—"}</td></tr>`).join("")}
      </tbody></table>`;
  }

  // ------------------------------------------------------------------ tree
  function renderTree(el, arg) {
    el.innerHTML = `
      <div class="two-col">
        <div class="card pad">
          <h3>知识树（点击主题查看详情）</h3>
          <div class="chart tall" id="topic-chart"></div>
        </div>
        <div id="topic-detail"></div>
      </div>`;
    const chart = echarts.init($("#topic-chart"));
    const data = {
      name: cur.name_zh,
      itemStyle: { color: cur.accent },
      children: cur.syllabus.map((u) => ({
        name: `${u.short_zh || u.title_zh} ${u.title_en}`,
        itemStyle: { color: "#8b5cf6" },
        children: u.topics.map((t) => ({
          name: `${t.id}  ${t.title_zh}`,
          itemStyle: { color: LEVEL_COLOR[t.level] || LEVEL_COLOR.both },
          _topicId: t.id,
        })),
      })),
    };
    chart.setOption({
      tooltip: { trigger: "item", formatter: (p) => {
        const t = p.data._topicId ? cur.topicById[p.data._topicId] : null;
        return t ? `<b>${esc(t.id)} ${esc(t.title_en)}</b><br>${esc(t.title_zh)}` : esc(p.name);
      } },
      series: [{
        type: "tree", data: [data], layout: "orthogonal", orient: "LR",
        top: "3%", left: "5%", bottom: "3%", right: "16%",
        roam: true, initialTreeDepth: -1, symbolSize: 9,
        label: { fontSize: 11, position: "left", align: "right" },
        leaves: { label: { position: "right", align: "left" } },
        lineStyle: { color: "#cbd5e1", width: 1.3 },
      }],
    });
    chart.on("click", (p) => {
      if (p.data && p.data._topicId) renderTopicDetail(p.data._topicId);
    });
    charts.push(chart);
    renderTopicDetail(arg ? decodeURIComponent(arg) : null);
  }

  function renderTopicDetail(id) {
    const box = $("#topic-detail");
    const t = id && cur.topicById[id];
    if (!t) { box.innerHTML = '<div class="detail-panel"><div class="empty">点击左侧主题节点查看详情</div></div>'; return; }
    const concepts = (t.key_concepts || []).map((c) => `<span class="concept-tag">${esc(c)}</span>`).join("");
    const tips = (t.exam_tips || []).map((x) => `<div class="tip-box">💡 ${esc(x)}</div>`).join("");
    const dias = (t.diagrams_list || []).map((x) => `<div class="tip-box" style="background:var(--brand-soft);color:#0f766e">📐 ${esc(x)}</div>`).join("");
    const terms = cur.glossary.filter((g) => g.topic === t.id)
      .map((g) => `<span class="concept-tag" title="${esc(g.def_zh)}">${esc(g.term_en)} · ${esc(g.term_zh)}</span>`).join("");
    const compHits = (MAP_BY_TOPIC[curId + ":" + t.id] || []);
    const compSection = compHits.length ? `
      <div class="sec-title">🏆 竞赛应用（以赛代学）</div>
      ${compHits.map(({ entry, why }) => `
        <div style="font-size:13px;margin:6px 0;padding:8px 10px;background:var(--coral-soft);border-radius:8px">
          <span class="badge" style="background:${COMP_COLOR[entry.comp]}22;color:${COMP_COLOR[entry.comp]}">${COMP_LABEL[entry.comp]}</span>
          <b>${esc(entry.concept_zh)}</b>
          <span class="muted" style="font-size:12px">${esc(entry.context)}</span>
          <div style="color:var(--ink-2);margin-top:3px">${esc(why)}</div>
        </div>`).join("")}
      <div class="muted" style="font-size:12px;margin-top:4px">↗ 完整匹配见「赛代学地图」</div>` : "";
    box.innerHTML = `
      <div class="detail-panel">
        <div style="margin-bottom:8px">
          <a href="#/s/${curId}/mapping" class="pill" style="background:var(--coral-soft);color:#be123c;text-decoration:none">🗺️ ← 返回赛代学地图</a>
          <a href="#/s/${curId}/tree" class="pill" style="background:var(--surface-2);color:var(--ink-2);text-decoration:none;margin-left:6px">🌳 知识树</a>
        </div>
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
          <h4 style="margin:0">${esc(t.id)} ${esc(t.title_en || t.title_zh)}</h4>${levelBadge(t.level)}${heatBadge(t)}
        </div>
        <div class="zh">${esc(t.title_zh)}</div>
        <p style="font-size:13.5px;line-height:1.6">${esc(t.desc_zh || t.desc_en || "")}</p>
        ${concepts ? `<div class="sec-title">核心概念</div><div>${concepts}</div>` : ""}
        ${terms ? `<div class="sec-title">本主题术语</div><div>${terms}</div>` : ""}
        ${dias ? `<div class="sec-title">核心图表（答什么）</div>${dias}` : ""}
        ${tips ? `<div class="sec-title">答题要点 / 易错点（怎么答）</div>${tips}` : ""}
        ${compSection}
      </div>`;
  }

  // ------------------------------------------------------------------ guide
  function renderGuide(el) {
    el.innerHTML = cur.syllabus.map((u) => `
      <div class="card pad" style="margin-bottom:16px">
        <h3>${esc(u.title_zh)} <span class="muted" style="font-size:13px">${esc(u.title_en)}</span></h3>
        ${u.topics.map((t) => `
          <div class="topic-row" data-t="${esc(t.id)}">
            <div style="flex:1;min-width:0">
              <b style="font-size:13.5px">${esc(t.id)} ${esc(t.title_zh)}</b>
              <span class="muted" style="font-size:12px;margin-left:6px">${esc(t.title_en || "")}</span>
              <div style="margin-left:2px">${levelBadge(t.level)}${heatBadge(t)}</div>
              ${(t.exam_tips || []).map((x) => `<div class="tip-box">💡 ${esc(x)}</div>`).join("")}
              ${(t.diagrams_list || []).map((x) => `<div class="tip-box" style="background:var(--brand-soft);color:#0f766e">📐 ${esc(x)}</div>`).join("")}
            </div>
          </div>`).join("")}
      </div>`).join("");
  }

  // ------------------------------------------------------------------ glossary
  const SUBJ_SHORT_HUB = { "ib-econ": "IB经济", "al-econ": "AL经济", "ib-bus": "IB商科", "al-bus": "AL商科", "igcse-bus": "IG商科", "comp": "竞赛" };
  const LINK_COLOR = { same: "#14b8a6", related: "#38bdf8", prereq: "#f59e0b", part: "#8b5cf6" };

  function subjOf(id) { return INDEX.find((s) => s.id === id); }

  function glossTermCard(g) {
    const links = (g.links || []).map((l) => {
      const s = subjOf(l.subj) || {};
      const color = s.accent || "#14b8a6";
      return `<a href="#/s/${l.subj}/glossary/${encodeURIComponent(l.term)}" class="badge"
                 style="background:${color}1e;color:${color};text-decoration:none"
                 title="同属概念簇：${esc(l.note || "")}">${esc(SUBJ_SHORT_HUB[l.subj] || s.name_zh || l.subj)} · ${esc(l.term)}</a>`;
    }).join(" ");
    const body = `
      <div style="color:var(--ink-2);font-size:13px">${esc(g.def_zh || g.def_en || "")}</div>
      ${g.def_en && g.def_zh ? `<div class="muted" style="font-size:12px;margin-top:2px">${esc(g.def_en)}</div>` : ""}
      ${g.more ? `<div style="margin-top:7px;font-size:13px;line-height:1.65;color:var(--ink)"><b style="color:#0d9488">📖 详解</b>　${esc(g.more)}</div>` : ""}
      ${g.example ? `<div style="margin-top:5px;font-size:12.5px;line-height:1.6;color:var(--ink-2)"><b style="color:#f59e0b">💡 例</b>　${esc(g.example)}</div>` : ""}
      ${g.part_of ? `<div style="margin-top:5px;font-size:12.5px"><b style="color:#8b5cf6">🧩 上位概念</b>　${esc(g.part_of)}</div>` : ""}
      ${g.prereq ? `<div style="margin-top:3px;font-size:12.5px"><b style="color:#d97706">🔑 先决条件</b>　${esc(g.prereq)}</div>` : ""}
      ${links ? `<div style="margin-top:7px;font-size:12.5px"><b style="color:#0ea5e9">🔗 同概念 · 跨科目</b>　${links}</div>` : ""}`;
    return `
      <div class="gloss-term" style="border-bottom:1px solid var(--line);padding:9px 2px">
        <div class="gloss-head" style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;cursor:pointer">
          <b>${esc(g.term_en)}</b><span class="muted">${esc(g.term_zh)}</span>
          ${g.topic ? `<span class="badge tag">${esc(g.topic)}</span>` : ""}
          ${g.cluster ? `<span class="badge" style="background:#8b5cf61a;color:#8b5cf6">${esc(g.cluster)}</span>` : ""}
          ${g.links ? `<span class="muted" style="font-size:11.5px;margin-left:auto">▾ ${g.links.length} 个跨科关联</span>` : ""}
        </div>
        <div class="gloss-body" style="display:none;margin-top:2px">${body}</div>
      </div>`;
  }

  function renderGlossary(el, arg) {
    if (arg) state.glossaryQ = decodeURIComponent(arg);
    el.innerHTML = `
      <div class="note" style="margin-bottom:10px">📖 术语深读：点击词条展开<b>详解与例子</b>；🔗 徽章直达其他科目中的<b>同一概念</b>（IB经济 ↔ AL经济 ↔ IB/AL/IG商科 ↔ 竞赛），
      🧩 指出它是什么更大框架的一部分，🔑 标明它是什么题型的<b>先决条件</b>。</div>
      <div style="display:flex;gap:10px;align-items:center;margin-bottom:10px">
        <input id="gq" style="flex:1;padding:10px 14px;border-radius:999px;border:1px solid var(--line);outline:none;font-size:14px"
               placeholder="筛选术语（中英/详解内容）…" value="${esc(state.glossaryQ)}">
        <button id="gexp" class="chip" style="border:1px solid var(--line);background:#fff;cursor:pointer">展开全部</button>
      </div>
      <div id="gloss-list"></div>`;
    $("#gq").addEventListener("input", (e) => { state.glossaryQ = e.target.value; renderGlossList(); });
    $("#gexp").addEventListener("click", () => {
      const bodies = document.querySelectorAll("#gloss-list .gloss-body");
      const anyClosed = [...bodies].some((b) => b.style.display === "none");
      bodies.forEach((b) => (b.style.display = anyClosed ? "block" : "none"));
      $("#gexp").textContent = anyClosed ? "收起全部" : "展开全部";
    });
    renderGlossList();
  }

  function renderGlossList() {
    const q = state.glossaryQ.trim().toLowerCase();
    const list = cur.glossary.filter((g) => !q ||
      g.term_en.toLowerCase().includes(q) || g.term_zh.includes(q) ||
      (g.def_zh || "").includes(q) || (g.more || "").includes(q) ||
      (g.example || "").includes(q) || (g.part_of || "").includes(q) ||
      (g.links || []).some((l) => l.term.toLowerCase().includes(q) || (SUBJ_SHORT_HUB[l.subj] || "").includes(q)));
    const groups = {};
    list.forEach((g) => {
      const t = cur.topicById[g.topic];
      const key = t ? t.unit_title_zh : "其他";
      (groups[key] = groups[key] || []).push(g);
    });
    $("#gloss-list").innerHTML = Object.entries(groups).map(([unit, arr]) => `
      <div class="card pad" style="margin-bottom:14px">
        <h3>${esc(unit)} <span class="muted" style="font-size:13px">${arr.length} 个术语</span></h3>
        ${arr.map(glossTermCard).join("")}
      </div>`).join("") || '<div class="empty">未找到匹配术语</div>';
    document.querySelectorAll("#gloss-list .gloss-head").forEach((h) =>
      h.addEventListener("click", () => {
        const b = h.parentElement.querySelector(".gloss-body");
        b.style.display = b.style.display === "none" ? "block" : "none";
      }));
  }

  // ------------------------------------------------------------------ models
  const CAT_ICON = {"环境与战略": "🧭", "营销": "📣", "财务决策": "💰", "组织与领导": "👥",
                    "运营与质量": "⚙️", "决策工具": "⚖️", "创业与商业模式": "🚀"};
  const CAT_COLOR = {"环境与战略": "#0ea5e9", "营销": "#ec4899", "财务决策": "#f59e0b",
                     "组织与领导": "#8b5cf6", "运营与质量": "#14b8a6", "决策工具": "#64748b",
                     "创业与商业模式": "#ef4444"};

  function modelTopicLinks(m) {
    return Object.entries(m.topics || {}).map(([sid, tids]) =>
      tids.map((tid) => {
        const s = subjOf(sid) || {};
        const color = s.accent || "#14b8a6";
        return `<a href="#/s/${sid}/tree/${encodeURIComponent(tid)}" class="badge"
                   style="background:${color}1e;color:${color};text-decoration:none">${esc(SUBJ_SHORT_HUB[sid] || s.name_zh || sid)} ${esc(tid)}</a>`;
      }).join(" ")).join(" ");
  }

  function modelCard(m, open) {
    const color = CAT_COLOR[m.cat] || "#14b8a6";
    const body = `
      <div style="font-size:13.5px;line-height:1.65;margin-top:2px">${esc(m.one)}</div>
      ${m.draw ? `<div style="margin-top:7px;font-size:12.5px;color:var(--ink-2)"><b style="color:${color}">📐 怎么画</b>　${esc(m.draw)}</div>` : ""}
      ${m.steps && m.steps.length ? `<div style="margin-top:6px;font-size:12.5px"><b style="color:${color}">🪜 使用步骤</b><ol style="margin:4px 0 0 18px;padding:0">${m.steps.map((s) => `<li style="margin:2px 0">${esc(s)}</li>`).join("")}</ol></div>` : ""}
      ${m.formula ? `<div style="margin-top:7px;font-family:ui-monospace,Menlo,monospace;font-size:12px;background:#0f172a0a;border:1px dashed ${color}55;border-radius:8px;padding:7px 10px">${esc(m.formula)}</div>` : ""}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px">
        <div style="font-size:12.5px;line-height:1.6"><b style="color:#10b981">✅ 优势</b><ul style="margin:3px 0 0 16px;padding:0">${(m.pros || []).map((x) => `<li style="margin:2px 0">${esc(x)}</li>`).join("")}</ul></div>
        <div style="font-size:12.5px;line-height:1.6"><b style="color:#ef4444">⚠️ 局限</b><ul style="margin:3px 0 0 16px;padding:0">${(m.cons || []).map((x) => `<li style="margin:2px 0">${esc(x)}</li>`).join("")}</ul></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr;gap:6px;margin-top:8px">
        ${m.ig ? `<div style="font-size:12.5px;line-height:1.6;border-left:3px solid #ec4899;padding-left:8px"><b>IG 考法</b>　${esc(m.ig)}</div>` : ""}
        ${m.al ? `<div style="font-size:12.5px;line-height:1.6;border-left:3px solid #f59e0b;padding-left:8px"><b>AL 深度</b>　${esc(m.al)}</div>` : ""}
        ${m.comp ? `<div style="font-size:12.5px;line-height:1.6;border-left:3px solid #ef4444;padding-left:8px"><b>竞赛应用</b>　${esc(m.comp)}</div>` : ""}
      </div>
      ${m.example ? `<div style="margin-top:7px;font-size:12.5px;color:var(--ink-2)"><b style="color:#f59e0b">💡 例</b>　${esc(m.example)}</div>` : ""}
      ${m.exam ? `<div style="margin-top:5px;font-size:12.5px"><b style="color:#8b5cf6">📝 真题问法</b>　${esc(m.exam)}</div>` : ""}
      ${Object.keys(m.topics || {}).length ? `<div style="margin-top:7px;font-size:12.5px"><b style="color:#0ea5e9">🔗 关联知识点</b>　${modelTopicLinks(m)}</div>` : ""}
      ${(m.res || []).length ? `<div style="margin-top:6px;font-size:12px;color:var(--ink-2)"><b>📁 本地课件</b>　${m.res.map((r) => `<span class="badge" style="background:#f1f5f9;color:#475569;font-weight:400">${esc(r)}</span>`).join(" ")}</div>` : ""}
    `;
    return `
      <div class="model-item" style="border-bottom:1px solid var(--line);padding:10px 2px" data-id="${esc(m.id)}">
        <div class="model-head" style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;cursor:pointer">
          <b>${esc(m.en)}</b><span class="muted">${esc(m.zh)}</span>
          <span class="badge" style="background:${color}1a;color:${color}">${esc((CAT_ICON[m.cat] || "") + " " + m.cat)}</span>
          <span class="muted" style="font-size:11.5px;margin-left:auto">▾</span>
        </div>
        <div class="model-body" style="display:${open ? "block" : "none"};margin-top:4px">${body}</div>
      </div>`;
  }

  function renderModels(el, arg) {
    const models = (cur.models || []).slice();
    if (!models.length) { el.innerHTML = '<div class="empty">本科目暂无模型工具箱</div>'; return; }
    if (arg) state.modelsQ = decodeURIComponent(arg);
    state.modelsQ = state.modelsQ || "";
    state.modelCat = state.modelCat || "";
    const cats = [...new Set(models.map((m) => m.cat))];
    el.innerHTML = `
      <div class="note" style="margin-bottom:10px">🧰 <b>模型工具箱</b>：本科目相关的 ${models.length} 个商业模型（全库 28 个）。
      每个模型含<b>怎么画/使用步骤/优势局限/IG 考法 vs AL 深度/竞赛应用/真题问法</b>；
      📁 标注了备课文件夹里对应的本地课件（思铺备课/ 下的相对路径）。点击卡片展开。</div>
      <div style="display:flex;gap:10px;align-items:center;margin-bottom:10px;flex-wrap:wrap">
        <input id="mq" style="flex:1;min-width:220px;padding:10px 14px;border-radius:999px;border:1px solid var(--line);outline:none;font-size:14px"
               placeholder="搜索模型（中英/内容）…" value="${esc(state.modelsQ)}">
        <span class="chip ${!state.modelCat ? "on" : ""}" data-cat="" style="cursor:pointer">全部</span>
        ${cats.map((c) => `<span class="chip ${state.modelCat === c ? "on" : ""}" data-cat="${esc(c)}" style="cursor:pointer">${esc((CAT_ICON[c] || "") + " " + c)}</span>`).join("")}
      </div>
      <div id="model-list"></div>`;
    $("#mq").addEventListener("input", (e) => { state.modelsQ = e.target.value; renderModelList(models); });
    el.querySelectorAll(".chip[data-cat]").forEach((c) =>
      c.addEventListener("click", () => {
        state.modelCat = c.dataset.cat || "";
        el.querySelectorAll(".chip[data-cat]").forEach((x) => x.classList.toggle("on", x === c));
        renderModelList(models);
      }));
    renderModelList(models);
  }

  function renderModelList(models) {
    const q = (state.modelsQ || "").trim().toLowerCase();
    const list = models.filter((m) =>
      (!state.modelCat || m.cat === state.modelCat) &&
      (!q || [m.en, m.zh, m.cat, m.one, m.ig, m.al, m.comp, m.exam, m.example]
        .some((x) => (x || "").toLowerCase().includes(q))));
    const groups = {};
    list.forEach((m) => ((groups[m.cat] = groups[m.cat] || []).push(m)));
    $("#model-list").innerHTML = Object.entries(groups).map(([cat, arr]) => `
      <div class="card pad" style="margin-bottom:14px">
        <h3>${esc((CAT_ICON[cat] || "") + " " + cat)} <span class="muted" style="font-size:13px">${arr.length} 个模型</span></h3>
        ${arr.map((m) => modelCard(m, false)).join("")}
      </div>`).join("") || '<div class="empty">未找到匹配模型</div>';
    document.querySelectorAll("#model-list .model-head").forEach((h) =>
      h.addEventListener("click", () => {
        const b = h.parentElement.querySelector(".model-body");
        b.style.display = b.style.display === "none" ? "block" : "none";
      }));
  }

  // ------------------------------------------------------------------ examq（常见考题）
  function examqTopicChip(tid, on) {
    const t = cur.topicById[tid];
    const label = tid + (t ? " " + t.title_zh.slice(0, 10) : "");
    return `<span class="chip ${on ? "on" : ""}" data-tid="${esc(tid)}" style="cursor:pointer">${esc(label)}</span>`;
  }

  function examqCard(q) {
    const t = cur.topicById[q.topic];
    const marks = q.marks ? `<span class="badge" style="background:#f59e0b22;color:#b45309">${q.marks} 分</span>` : "";
    const meta = q.tag ? `<span class="muted" style="font-size:12px">${esc(q.tag)}</span>` :
      `<span class="muted" style="font-size:12px">${q.year || ""} ${esc(q.session || "")}${q.level && q.level !== "Core/Ext" ? " · " + esc(q.level) : ""}${q.paper ? " · Paper " + q.paper : ""}${q.qno ? " · 第" + q.qno + "题(" + esc(q.part || "") + ")" : ""}</span>`;
    const link = (href, label, bg, fg) => href ?
      `<a href="${href}" target="_blank" class="pill" style="background:${bg};color:${fg}">${label}</a>` : "";
    const answer = q.answer ? `
      <div style="margin-top:8px;font-size:12.5px;line-height:1.65;color:var(--ink-2);border-left:3px solid #10b981;padding-left:8px">
        <b style="color:#059669">✔ 答题要点</b>　${esc(q.answer)}</div>` : "";
    const dup = q.dup > 1 ? `<span class="badge" style="background:#f1f5f9;color:#64748b" title="近年出现次数（按题目指纹）">近现 ${q.dup} 次</span>` : "";
    return `
      <div class="examq-item" style="border-bottom:1px solid var(--line);padding:10px 2px">
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:baseline">
          ${marks}<span class="badge" style="background:#14b8a622;color:#0f766e">${esc(q.topic)}</span>
          <a href="#/s/${curId}/tree/${encodeURIComponent(q.topic)}" class="badge"
             style="background:#8b5cf61a;color:#7c3aed;text-decoration:none"
             title="打开知识点卡片">${esc(t ? t.title_zh : "知识点卡 ↗")}</a>
          ${dup}${meta}
        </div>
        <div style="margin-top:6px;font-size:13.5px;line-height:1.6">${esc(q.q)}</div>
        ${q.aos ? `<div class="muted" style="margin-top:3px;font-size:12px">能力维度：${esc(q.aos)}</div>` : ""}
        ${answer}
        ${(q.qp_link || q.ms_link) ? `<div style="margin-top:7px;display:flex;gap:6px">
          ${link(q.qp_link, "📝 原题 PDF", "var(--brand-soft)", "#0f766e")}
          ${link(q.ms_link, "✔ 评分方案", "var(--amber-soft)", "#b45309")}</div>` : ""}
      </div>`;
  }

  function renderExamq(el, arg) {
    const ex = cur.examq || {};
    const hasReal = ex.topics && Object.keys(ex.topics).length;
    const hasCur = ex.curated && ex.curated.length;
    if (!(state.examqTab === "real" && hasReal) && !(state.examqTab === "curated" && hasCur)) {
      state.examqTab = hasReal ? "real" : (hasCur ? "curated" : null);
      state.examqTopic = "";
    }
    el.innerHTML = `
      <div class="note" style="margin-bottom:10px">🗂️ <b>常见考题</b>：从历年真题中切片的<b>真题原题</b>（配官方评分方案要点与原卷 PDF 直链）＋按官方卷型整理的<b>典型题解析</b>。
      每题挂接<b>知识点卡片</b>（点击紫色徽章跳转），按主题与分值筛选高频题。</div>
      <div id="examq-tabs" style="display:flex;gap:8px;margin-bottom:12px"></div>
      <div id="examq-topicbar" style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px"></div>
      <div id="examq-patterns" style="margin-bottom:12px"></div>
      <div id="examq-list"></div>`;
    renderExamqInner(ex);
  }

  function renderExamqInner(ex) {
    const tabs = [];
    if (ex.topics && Object.keys(ex.topics).length) tabs.push(["real", "🗂️ 真题切片" + (ex.count ? `（${ex.count} 条原始切片）` : "")]);
    if (ex.curated && ex.curated.length) tabs.push(["curated", "📋 典型题解析（官方卷型）"]);
    $("#examq-tabs").innerHTML = tabs.map(([k, label]) =>
      `<span class="chip ${state.examqTab === k ? "on" : ""}" data-tab="${k}" style="cursor:pointer">${esc(label)}</span>`).join(" ");
    $("#examq-tabs").querySelectorAll(".chip").forEach((c) =>
      c.addEventListener("click", () => { state.examqTab = c.dataset.tab; renderExamqInner(ex); }));

    const bar = $("#examq-topicbar"), pat = $("#examq-patterns");
    if (state.examqTab === "real") {
      const tids = Object.keys(ex.topics || {}).sort();
      bar.innerHTML = `<span class="chip ${!state.examqTopic ? "on" : ""}" data-tid="" style="cursor:pointer">全部主题</span>` +
        tids.map((tid) => examqTopicChip(tid, state.examqTopic === tid)).join("");
      bar.querySelectorAll(".chip").forEach((c) =>
        c.addEventListener("click", () => { state.examqTopic = c.dataset.tid || ""; renderExamqInner(ex); }));
      if (state.examqTopic && ex.patterns && ex.patterns[state.examqTopic]) {
        const items = Object.entries(ex.patterns[state.examqTopic]);
        pat.innerHTML = items.length ? `<div class="card pad" style="padding:10px 14px;font-size:12.5px">
          <b>该主题常见题型</b>　${items.map(([k, n]) => `<span class="badge" style="background:#0ea5e91a;color:#0369a1">${esc(k)} ×${n}</span>`).join(" ")}</div>` : "";
      } else pat.innerHTML = "";
      const list = Object.entries(ex.topics || {})
        .filter(([tid]) => !state.examqTopic || tid === state.examqTopic)
        .flatMap(([tid, arr]) => arr);
      list.sort((a, b) => (b.dup - a.dup) || (b.year - a.year) || (b.marks - a.marks));
      $("#examq-list").innerHTML = list.map(examqCard).join("") || '<div class="empty">暂无切片</div>';
    } else {
      bar.innerHTML = "";
      pat.innerHTML = ex.note ? `<div class="card pad" style="padding:10px 14px;font-size:12.5px;color:var(--ink-2)">${esc(ex.note)}</div>` : "";
      $("#examq-list").innerHTML = (ex.curated || []).map(examqCard).join("") || '<div class="empty">暂无</div>';
    }
  }

  // ------------------------------------------------------------------ quiz
  function renderQuiz(el) {
    el.innerHTML = `
      <div class="note" style="margin-bottom:14px">🎯 <b>练习问答</b>：共 ${cur.quiz.length} 题，随机出题、即时判分与解析。答题时先自己判断，再点选项核对。</div>
      <div class="card pad" id="quiz-box"></div>`;
    startQuiz();
  }

  function startQuiz() {
    const bank = cur.quiz.slice().sort(() => Math.random() - 0.5);
    let idx = 0, score = 0, answered = false;
    const box = $("#quiz-box");
    function next() {
      const q = bank[idx];
      if (!q) {
        const pct = score / bank.length;
        box.innerHTML = `<h3>🎉 完成</h3>
          <div style="font-size:30px;font-weight:800;color:${cur.accent}">${score} / ${bank.length}</div>
          <div class="muted" style="margin-top:6px">${pct >= 0.8 ? "掌握得很好！" : pct >= 0.5 ? "不错，再刷一轮巩固。" : "建议先看「答题指南」再来挑战。"}</div>
          <button class="pill" style="background:${cur.accent};color:#fff;border:none;cursor:pointer;margin-top:14px;padding:8px 18px" id="qz-retry">再来一轮</button>`;
        $("#qz-retry").onclick = startQuiz;
        return;
      }
      answered = false;
      box.innerHTML = `
        <div style="display:flex;justify-content:space-between;color:var(--ink-3);font-size:12.5px">
          <span>第 ${idx + 1} / ${bank.length} 题</span><span>得分 ${score}</span></div>
        <h3 style="margin:10px 0 14px">${esc(q.q)}</h3>
        <div style="display:grid;gap:9px">
          ${q.opts.map((o, i) => `<div class="quiz-opt" data-oi="${i}">${String.fromCharCode(65 + i)}. ${esc(o)}</div>`).join("")}
        </div>
        <div id="qz-fb" style="margin-top:14px"></div>`;
      box.querySelectorAll(".quiz-opt").forEach((btn) => btn.addEventListener("click", () => {
        if (answered) return;
        answered = true;
        const oi = Number(btn.dataset.oi);
        const ok = oi === q.a;
        if (ok) score++;
        box.querySelectorAll(".quiz-opt").forEach((b) => {
          const i = Number(b.dataset.oi);
          if (i === q.a) b.classList.add("correct");
          else if (i === oi) b.classList.add("wrong");
        });
        $("#qz-fb").innerHTML = `
          <div style="padding:12px 15px;border-radius:10px;background:${ok ? "var(--sl-soft)" : "var(--coral-soft)"}">
            <b>${ok ? "✅ 正确" : "❌ 错误"}</b> · ${esc(q.why)}
            ${q.topic ? `<div class="muted" style="font-size:12px;margin-top:3px">考点：${esc(q.topic)}${cur.topicById[q.topic] ? " · " + esc(cur.topicById[q.topic].title_zh) : ""}</div>` : ""}
          </div>
          <button class="pill" style="background:${cur.accent};color:#fff;border:none;cursor:pointer;margin-top:12px;padding:8px 18px" id="qz-next">${idx + 1 >= bank.length ? "查看结果" : "下一题"}</button>`;
        $("#qz-next").onclick = () => { idx++; next(); };
      }));
    }
    next();
  }

  // ------------------------------------------------------------------ papers (igcse real past papers)
  let PAPERS = null;
  async function loadPapers() {
    if (PAPERS !== null) return PAPERS;
    try {
      const r = await fetch(KB + "subjects/igcse-papers.json");
      PAPERS = await r.json();
    } catch (e) { PAPERS = null; }
    return PAPERS;
  }

  async function renderPapers(el) {
    el.innerHTML = '<div class="spin">加载真题库…</div>';
    const data = await loadPapers();
    if (!data || curId !== "igcse-bus") {
      el.innerHTML = '<div class="note">📝 本科目真题库建设中。IB 经济真题/评分方案在完整站。</div>' +
        '<div class="card pad" style="margin-top:12px"><a class="pill" style="background:var(--brand-soft);color:#0f766e" href="index.html#/papers">→ 前往 IB 经济真题库</a></div>';
      return;
    }
    const F = (state.paperFilter = state.paperFilter || {});
    const years = [...new Set(data.papers.map((p) => p.year))].sort((a, b) => b - a);
    const sessions = ["May/June", "Oct/Nov", "March"];
    el.innerHTML = `
      <div class="note" style="margin-bottom:14px">📝 <b>IGCSE 0450 真题库</b>：${data.count} 份（${data.years[0]}–${data.years[data.years.length - 1]}）。
      每行配齐 📝题目 · ✔评分方案 · 📋考官报告；主题标签为自动打标（关键词匹配），点标签跳转知识点。刷法：近 5 年全刷，早年按频次图挑。</div>
      <div class="card pad" style="margin-bottom:16px">
        <h3>考点频次（${data.count} 份真题统计）</h3>
        <div class="chart short" id="pp-heat"></div>
      </div>
      <div class="card pad">
        <div class="filters">
          <span class="chip ${!F.year ? "on" : ""}" data-k="year" data-v="">全部年份</span>
          ${years.map((y) => `<span class="chip ${F.year === y ? "on" : ""}" data-k="year" data-v="${y}">${y}</span>`).join("")}
        </div>
        <div class="filters">
          <span class="chip ${!F.session ? "on" : ""}" data-k="session" data-v="">全部考季</span>
          ${sessions.map((s) => `<span class="chip ${F.session === s ? "on" : ""}" data-k="session" data-v="${s}">${s}</span>`).join("")}
        </div>
        <div class="filters">
          <span class="chip ${!F.paper ? "on" : ""}" data-k="paper" data-v="">全部卷</span>
          <span class="chip ${F.paper === 1 ? "on" : ""}" data-k="paper" data-v="1">Paper 1</span>
          <span class="chip ${F.paper === 2 ? "on" : ""}" data-k="paper" data-v="2">Paper 2</span>
        </div>
        <div id="pp-list"></div>
      </div>`;
    // heat bar chart
    const heat = data.topic_heat || [];
    const chart = echarts.init($("#pp-heat"));
    chart.setOption({
      tooltip: { trigger: "axis" },
      grid: { left: 40, right: 16, top: 16, bottom: 60 },
      xAxis: { type: "category", data: heat.map((h) => h.id),
        axisLabel: { rotate: 45, fontSize: 9.5 } },
      yAxis: { type: "value", name: "出现卷数" },
      series: [{ type: "bar", data: heat.map((h) => h.freq),
        itemStyle: { color: "#ec4899", borderRadius: [4, 4, 0, 0] } }],
    });
    charts.push(chart);
    document.querySelectorAll(".filters .chip").forEach((c) =>
      c.addEventListener("click", () => {
        const k = c.dataset.k;
        const v = c.dataset.v;
        F[k] = v === "" ? null : (k === "paper" ? Number(v) : (k === "year" ? Number(v) : v));
        renderPapers(el);
      }));
    const list = data.papers.filter((p) =>
      (!F.year || p.year === F.year) && (!F.session || p.session === F.session) &&
      (!F.paper || p.paper === F.paper));
    const link = (rel) => rel ? "../" + rel.split("/").map(encodeURIComponent).join("/") : null;
    $("#pp-list").innerHTML = list.map((p) => `
      <div class="list-item">
        <div class="grow">
          <div class="t">${p.year} ${esc(p.session)} · Paper ${p.paper} <span class="muted" style="font-weight:400">(v${esc(p.variant)})</span></div>
          <div class="d">${(p.topics || []).map((t) =>
            `<a class="badge tag" style="margin:2px 4px 0 0;text-decoration:none" href="#/s/igcse-bus/tree/${encodeURIComponent(t.id)}">${esc(t.id)} ${esc(cur.topicById[t.id] ? cur.topicById[t.id].title_zh : "")}</a>`).join("")}</div>
        </div>
        <div style="display:flex;gap:6px;white-space:nowrap;flex-wrap:wrap;justify-content:flex-end">
          ${p.qp ? `<a href="${link(p.qp)}" target="_blank" class="pill" style="background:var(--brand-soft);color:#0f766e">📝 题目</a>` : ""}
          ${p.ms ? `<a href="${link(p.ms)}" target="_blank" class="pill" style="background:var(--amber-soft);color:#b45309">✔ 评分方案</a>` : ""}
          ${p.er ? `<a href="${link(p.er)}" target="_blank" class="pill" style="background:var(--violet-soft);color:#6d28d9">📋 考官报告</a>` : ""}
        </div>
      </div>`).join("") || '<div class="empty">无匹配真题</div>';
  }

  // ------------------------------------------------------------------ progression (IG -> AL)
  let PROG = null;
  async function loadProgression() {
    if (PROG !== null) return PROG;
    try {
      const r = await fetch(KB + "subjects/progression.json");
      PROG = await r.json();
    } catch (e) { PROG = null; }
    return PROG;
  }

  async function renderProgression(el) {
    el.innerHTML = '<div class="spin">加载衔接地图…</div>';
    const data = await loadProgression();
    if (!data) { el.innerHTML = '<div class="empty">progression.json 未加载</div>'; return; }
    await Promise.all([loadSubject("igcse-bus"), loadSubject("al-bus")]);
    const igTopic = (id) => CACHE["igcse-bus"] && CACHE["igcse-bus"].topicById[id];
    const alTopic = (id) => CACHE["al-bus"] && CACHE["al-bus"].topicById[id];
    el.innerHTML = `
      <div class="note" style="margin-bottom:14px">🧭 <b>IG→AL 商科衔接地图</b>：${esc(data.note)}</div>
      ${data.groups.map((g) => `
        <div class="card pad" style="margin-bottom:16px">
          <h3>${g.icon} ${esc(g.theme)} <span class="muted" style="font-size:13px">${g.rows.length} 组衔接</span></h3>
          ${g.rows.map((r) => `
            <div style="padding:10px 12px;margin:8px 0;background:var(--surface-2);border-radius:10px">
              <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
                <a class="pill" style="background:#fce7f3;color:#be185d;text-decoration:none" href="#/s/igcse-bus/tree/${encodeURIComponent(r.ig)}">IG ${esc(r.ig)}${igTopic(r.ig) ? " " + esc(igTopic(r.ig).title_zh) : ""}</a>
                <span style="color:var(--ink-3)">→</span>
                <a class="pill" style="background:var(--amber-soft);color:#b45309;text-decoration:none" href="#/s/al-bus/tree/${encodeURIComponent(r.al)}">AL ${esc(r.al)}${alTopic(r.al) ? " " + esc(alTopic(r.al).title_zh) : ""}</a>
              </div>
              <div style="font-size:13px;line-height:1.65;margin-top:6px">
                <span style="color:#9d174d"><b>IG 已学：</b>${esc(r.ig_zh)}</span><br>
                <span style="color:var(--ink)"><b>AL 升级：</b>${esc(r.up_zh)}</span>
              </div>
            </div>`).join("")}
        </div>`).join("")}
      <div class="card pad">
        <h3>🆕 AL 独有模块（IG 完全没有）</h3>
        ${data.al_only.map((a) => `
          <div style="font-size:13px;line-height:1.65;padding:9px 12px;margin:6px 0;background:var(--violet-soft);border-radius:8px">
            <b>${esc(a.title)}</b> ${a.topics.map((t) => `<a class="badge tag" style="text-decoration:none" href="#/s/al-bus/tree/${encodeURIComponent(t)}">${esc(t)}</a>`).join("")}
            <div style="color:var(--ink-2);margin-top:3px">${esc(a.desc)}</div>
          </div>`).join("")}
      </div>`;
  }

  // ------------------------------------------------------------------ IA / EE / essay
  function renderIaee(el) {
    const d = cur.iaee || {};
    if (!d.sections) { el.innerHTML = '<div class="empty">暂无内容</div>'; return; }
    el.innerHTML = `
      <div class="note" style="margin-bottom:14px">✍️ <b>${esc(d.title || "IA/EE 指南")}</b>：结构模板 + 评分标准 + 考官视角的高频失分点。写前过一遍，写后逐条自查。</div>
      ${d.sections.map((s) => `
        <div class="card pad" style="margin-bottom:16px">
          <h3>${esc(s.h)}</h3>
          ${s.items.map((it, i) => `
            <div style="font-size:13.5px;line-height:1.7;padding:8px 12px;margin:6px 0;
                        background:${i === s.items.length - 1 ? "var(--coral-soft)" : "var(--surface-2)"};
                        border-radius:8px;border-left:3px solid ${i === s.items.length - 1 ? "#ef4444" : cur.accent}">
              ${i === s.items.length - 1 ? "⚠️ " : "✅ "}${esc(it)}
            </div>`).join("")}
        </div>`).join("")}
      ${(d.links || []).length ? `<div class="card pad">
        <h3>配套资源</h3>
        ${d.links.map((l) => `<div style="margin:6px 0"><a href="${esc(l.href)}">🔗 ${esc(l.label)}</a></div>`).join("")}
      </div>` : ""}`;
  }

  // ------------------------------------------------------------------ resources
  function renderResources(el) {
    const d = cur.resources || {};
    if (!d.groups) { el.innerHTML = '<div class="empty">暂无内容</div>'; return; }
    el.innerHTML = `
      <div class="note" style="margin-bottom:14px">📚 <b>教学辅助资料</b>：教材章节→知识点的阅读地图、指定阅读与官方文件。按此顺序读，效率最高。</div>
      ${d.groups.map((g) => `
        <div class="card pad" style="margin-bottom:16px">
          <h3>${esc(g.h)}</h3>
          ${g.items.map((it) => `
            <div style="font-size:13.5px;line-height:1.7;padding:7px 12px;margin:5px 0;background:var(--surface-2);border-radius:8px">
              📖 ${esc(it)}
            </div>`).join("")}
          ${g.link ? `<div style="margin-top:8px"><a class="pill" style="background:var(--brand-soft);color:#0f766e;padding:7px 16px" href="${esc(g.link.href)}">${esc(g.link.label)}</a></div>` : ""}
        </div>`).join("")}`;
  }

  // ------------------------------------------------------------------ diagrams (shared with IB econ images)
  let DIAGRAM_META = null;
  async function loadDiagramMeta() {
    if (DIAGRAM_META) return DIAGRAM_META;
    try {
      const r = await fetch(KB + "diagrams.json");
      DIAGRAM_META = await r.json();
    } catch (e) { DIAGRAM_META = []; }
    return DIAGRAM_META;
  }

  async function renderDiagramsView(el) {
    el.innerHTML = '<div class="spin">加载图表…</div>';
    const meta = await loadDiagramMeta();
    const byId = {};
    meta.forEach((d) => (byId[d.id] = d));
    if (!cur.has_diagrams) {
      // ib-econ etc: deep-link to full site
      el.innerHTML = `
        <div class="note">📈 本科目图表解析与训练在 <b>IB 经济完整站</b>（28 张模型图 + 31 道图表训练题，点线面积逐项解析）。AL 经济可在本科目内直接查看。</div>
        <div class="card pad" style="margin-top:12px"><a class="pill" style="background:var(--brand-soft);color:#0f766e;padding:8px 18px" href="index.html#/diagrams">→ 打开图表解析与训练</a></div>`;
      return;
    }
    const rows = [];
    cur.topics.forEach((t) => (t.diagram_ids || []).forEach((did) => {
      if (byId[did]) rows.push({ t, d: byId[did] });
    }));
    el.innerHTML = `
      <div class="note" style="margin-bottom:14px">📈 ${esc(cur.name_zh)}所需的核心模型图（点移动 · 线移动 · 面积含义逐项解析），与考试画图要求一一对应。</div>
      <div class="grid cols-2">
        ${rows.map(({ t, d }) => `
          <div class="card pad" style="background:var(--surface-2)">
            <div style="display:flex;justify-content:space-between;align-items:baseline;gap:8px">
              <b style="font-size:14px">${esc(d.name_zh)}</b>
              <a href="#/s/${curId}/tree/${encodeURIComponent(t.id)}" class="badge tag">${esc(t.id)}</a>
            </div>
            <div class="muted" style="font-size:12px;margin:2px 0 6px">${esc(d.name_en)}</div>
            <img src="assets/diagrams/${d.id}.png" loading="lazy" style="width:100%;max-width:380px;border-radius:8px;background:#fff;border:1px solid var(--line)">
            <div style="font-size:13px;line-height:1.55;margin-top:6px">${esc(d.what)}</div>
            <div class="sec-title">线移动</div><div style="font-size:12.5px">${esc(d.lines)}</div>
            <div class="sec-title">点移动</div><div style="font-size:12.5px">${esc(d.points)}</div>
            <div class="sec-title">面积含义</div><div style="font-size:12.5px">${esc(d.areas)}</div>
          </div>`).join("")}
      </div>`;
  }

  // ------------------------------------------------------------------ mapping (赛代学地图)
  const COMP_LABEL = { conrad: "康莱德", bpa: "BPA", both: "康莱德+BPA" };
  const COMP_COLOR = { conrad: "#ef4444", bpa: "#f59e0b", both: "#8b5cf6" };
  const SUBJ_COLOR = { "ib-econ": "#14b8a6", "al-econ": "#0ea5a4", "ib-bus": "#6366f1", "al-bus": "#f59e0b", "comp": "#ef4444" };

  function renderMapping(el) {
    if (!MAP) { el.innerHTML = '<div class="empty">mapping.json 未加载</div>'; return; }
    const F = state.mapFilter;
    el.innerHTML = `
      <div class="note" style="margin-bottom:14px">🗺️ <b>赛代学地图</b>：左边是竞赛里的概念/交付物（康莱德 6 维评分与 Lean Canvas、BPA 题型），右边是对应的学科知识点。
      备赛时按竞赛任务 → 找学科知识点补强；复习学科时按知识点 → 找竞赛练兵场。点击图中节点可跳转详情。</div>
      <div class="card pad" style="margin-bottom:16px">
        <div class="filters" id="map-f-comp">
          <span class="chip ${!F.comp ? "on" : ""}" data-v="">全部竞赛</span>
          ${["conrad", "bpa", "both"].map((c) => `<span class="chip ${F.comp === c ? "on" : ""}" data-v="${c}">${COMP_LABEL[c]}</span>`).join("")}
        </div>
        <div class="filters" id="map-f-subj">
          <span class="chip ${!F.subject ? "on" : ""}" data-v="">全部学科</span>
          ${INDEX.filter((s) => s.id !== "comp").map((s) =>
            `<span class="chip ${F.subject === s.id ? "on" : ""}" data-v="${s.id}">${esc(s.name_zh)}</span>`).join("")}
        </div>
        <div class="chart tall" id="map-chart"></div>
      </div>
      <div class="card pad" style="margin-bottom:16px">
        <h3>正向表：竞赛概念 → 学科知识点</h3>
        <div id="map-table"></div>
      </div>
      <div class="card pad">
        <h3>反向表：${esc(cur.name_zh)}知识点 → 竞赛应用</h3>
        <div id="map-reverse"></div>
      </div>`;
    document.querySelectorAll("#map-f-comp .chip").forEach((c) =>
      c.addEventListener("click", () => { F.comp = c.dataset.v || null; renderMapping(el); }));
    document.querySelectorAll("#map-f-subj .chip").forEach((c) =>
      c.addEventListener("click", () => { F.subject = c.dataset.v || null; renderMapping(el); }));
    drawSankey();
    renderMapTable();
    renderMapReverse();
  }

  function mapEntriesFiltered() {
    const F = state.mapFilter;
    return (MAP.entries || []).filter((e) =>
      (!F.comp || e.comp === F.comp || e.comp === "both") &&
      (!F.subject || e.matches.some((m) => m.subject === F.subject)));
  }

  function drawSankey() {
    const dom = $("#map-chart");
    if (!dom) return;
    const entries = mapEntriesFiltered();
    const nodes = [], links = [], seen = new Set();
    const addNode = (name, color) => {
      if (seen.has(name)) return;
      seen.add(name); nodes.push({ name, itemStyle: { color } });
    };
    entries.forEach((e) => {
      addNode(e.concept_zh, COMP_COLOR[e.comp]);
      e.matches.forEach((m) => {
        if (state.mapFilter.subject && m.subject !== state.mapFilter.subject) return;
        const sdata = CACHE[m.subject];
        const t = sdata && sdata.topicById[m.topic];
        const tname = `${MAP.subject_short[m.subject] || m.subject}·${m.topic} ${(t ? t.title_zh : "").slice(0, 8)}`;
        addNode(tname, SUBJ_COLOR[m.subject] || "#94a3b8");
        links.push({ source: e.concept_zh, target: tname, value: 1,
                     lineStyle: { color: "gradient" } });
      });
    });
    const chart = echarts.init(dom);
    chart.setOption({
      tooltip: { trigger: "item", formatter: (p) => {
        if (p.dataType === "edge") return `${esc(p.data.source)} → ${esc(p.data.target)}`;
        return esc(p.name);
      } },
      series: [{
        type: "sankey", left: 10, right: 180, top: 10, bottom: 10,
        nodeWidth: 14, nodeGap: 8, data: nodes, links,
        emphasis: { focus: "adjacency" },
        label: { fontSize: 10.5, color: "#334155" },
        lineStyle: { color: "gradient", curveness: 0.5, opacity: 0.35 },
        levels: [{ depth: 0, label: { position: "right" } }, { depth: 1, label: { position: "right" } }],
      }],
    });
    chart.on("click", (p) => {
      if (p.dataType !== "node") return;
      const name = p.name;
      const e = (MAP.entries || []).find((x) => x.concept_zh === name);
      if (e) { // competition concept -> comp subject tree
        location.hash = "#/s/comp/tree"; return;
      }
      const m = name.match(/^(.+?)·(\S+)\s/);
      if (m) {
        const short = m[1], tid = m[2];
        const sid = Object.keys(MAP.subject_short).find((k) => MAP.subject_short[k] === short);
        if (sid) location.hash = `#/s/${sid}/tree/${encodeURIComponent(tid)}`;
      }
    });
    charts.push(chart);
  }

  function renderMapTable() {
    const box = $("#map-table");
    if (!box) return;
    const entries = mapEntriesFiltered();
    box.innerHTML = `<table>
      <thead><tr><th>竞赛概念</th><th>出处（评委关注）</th><th>对应学科知识点</th><th>匹配逻辑</th></tr></thead>
      <tbody>${entries.map((e) => `
        <tr>
          <td><span class="badge" style="background:${COMP_COLOR[e.comp]}22;color:${COMP_COLOR[e.comp]}">${COMP_LABEL[e.comp]}</span><br><b style="font-size:13px">${esc(e.concept_zh)}</b><div class="muted" style="font-size:11.5px">${esc(e.concept_en)}</div></td>
          <td style="font-size:12.5px">${esc(e.context)}</td>
          <td>${e.matches.filter((m) => !state.mapFilter.subject || m.subject === state.mapFilter.subject).map((m) => {
            const sd = CACHE[m.subject];
            const t = sd && sd.topicById[m.topic];
            return `<a class="badge tag" style="margin:2px" href="#/s/${m.subject}/tree/${encodeURIComponent(m.topic)}">${esc(MAP.subject_short[m.subject] || m.subject)} ${esc(m.topic)} ${esc(t ? t.title_zh : "")}</a>`;
          }).join("")}</td>
          <td style="font-size:12.5px">${e.matches.filter((m) => !state.mapFilter.subject || m.subject === state.mapFilter.subject).map((m) => `· ${esc(MAP.subject_short[m.subject])} ${esc(m.topic)}：${esc(m.why)}`).join("<br>")}</td>
        </tr>`).join("")}
      </tbody></table>`;
  }

  function renderMapReverse() {
    const box = $("#map-reverse");
    if (!box) return;
    const rows = cur.topics.map((t) => {
      const hits = MAP_BY_TOPIC[curId + ":" + t.id] || [];
      return { t, hits };
    }).filter((r) => r.hits.length);
    box.innerHTML = rows.length ? `<table>
      <thead><tr><th>知识点</th><th>竞赛应用（以赛代学）</th></tr></thead>
      <tbody>${rows.map(({ t, hits }) => `
        <tr>
          <td><a href="#/s/${curId}/tree/${encodeURIComponent(t.id)}"><b>${esc(t.id)} ${esc(t.title_zh)}</b></a></td>
          <td>${hits.map(({ entry, why }) =>
            `<div style="margin:3px 0"><span class="badge" style="background:${COMP_COLOR[entry.comp]}22;color:${COMP_COLOR[entry.comp]}">${COMP_LABEL[entry.comp]}</span> <b>${esc(entry.concept_zh)}</b> <span class="muted" style="font-size:12px">${esc(entry.context)}</span><div style="font-size:12.5px;color:var(--ink-2);margin:2px 0 0 4px">${esc(why)}</div></div>`).join("")}</td>
        </tr>`).join("")}
      </tbody></table>` : `<div class="empty">本科目暂无直接匹配的竞赛概念</div>`;
  }

  boot().catch((e) => {
    $("#view").innerHTML = `<div class="empty">加载失败：${esc(e.message)}<br>请在项目根目录运行 <code>python3 -m http.server 8000</code> 后访问。</div>`;
  });
})();
