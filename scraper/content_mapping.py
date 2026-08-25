"""Competition <-> subject concept mapping (赛代学双向匹配).

Each entry links one competition concept (Conrad dimension/deliverable or BPA
format) to the subject topics that teach it. Subjects: ib-econ, al-econ,
ib-bus, al-bus. `comp` field: "conrad" | "bpa" | "both".
Source: 康莱德&BPA_经济商科知识点拟合表 + Conrad 写作手册 + OCP-9 大纲.
"""

SUBJECT_SHORT = {
    "ib-econ": "IB经济", "al-econ": "AL经济",
    "ib-bus": "IB商科", "al-bus": "AL商科", "igcse-bus": "IGCSE商科",
}

MAPPING = [
    # ---------- 康莱德 6 维评分 & Lean Canvas ----------
    {"id": "m-theme", "concept_zh": "主题契合 / SDG·ESG", "concept_en": "Theme & SDG/ESG",
     "comp": "conrad", "context": "康莱德 Theme 30%（权重最高）· Brief 全文需显式呼应",
     "matches": [
         {"subject": "ib-econ", "topic": "4.7", "why": "可持续发展的定义与增长-可持续权衡，直接构成 Theme 论证。"},
         {"subject": "ib-econ", "topic": "2.8", "why": "负外部性/公共池塘资源为环境类主题提供理论支撑。"},
         {"subject": "al-econ", "topic": "AE6.3", "why": "经济发展与可持续：A2 发展经济学的核心议题。"},
         {"subject": "ib-bus", "topic": "BB1.3", "why": "CSR 与三重底线：企业层面的 ESG 表达。"},
     ]},
    {"id": "m-tam", "concept_zh": "TAM/SAM/SOM 市场测算", "concept_en": "TAM / SAM / SOM",
     "comp": "conrad", "context": "Lean Canvas 市场格 · Innovation Brief Market 部分",
     "matches": [
         {"subject": "ib-econ", "topic": "2.5", "why": "弹性决定定价与量测：TAM 自上而下/自下而上测算的方法论基础。"},
         {"subject": "al-econ", "topic": "AE2.2", "why": "四种弹性的计算与判断，是市场容量估算的学科工具。"},
         {"subject": "ib-bus", "topic": "BB4.1", "why": "市场调研方法（一级/二级）提供数据来源与口径。"},
         {"subject": "al-bus", "topic": "AB3.1", "why": "市场细分与规模判断：STP 的 S（细分）。"},
     ]},
    {"id": "m-problem", "concept_zh": "Problem 量化与人群定位", "concept_en": "Problem & target users",
     "comp": "conrad", "context": "Lean Canvas Q1（≤40词：人群+量化+主题词）",
     "matches": [
         {"subject": "ib-econ", "topic": "2.1", "why": "需求的决定因素：谁在何种场景产生需求。"},
         {"subject": "al-econ", "topic": "AE2.1", "why": "需求曲线与 shift 因素＝人群行为的结构化表达。"},
         {"subject": "ib-bus", "topic": "BB4.1", "why": "市场调研的定量证据（样本/数据来源）支撑量化表述。"},
     ]},
    {"id": "m-pricing", "concept_zh": "定价策略", "concept_en": "Pricing strategy",
     "comp": "conrad", "context": "Lean Canvas 收入格 · Marketing 10%",
     "matches": [
         {"subject": "ib-econ", "topic": "2.5", "why": "PED 决定能否用低价换量（渗透）或高价撇脂。"},
         {"subject": "al-econ", "topic": "AE2.2", "why": "弹性与总收入检验是定价决策的学科依据。"},
         {"subject": "ib-bus", "topic": "BB4.4", "why": "撇脂/渗透/心理定价等策略工具箱。"},
         {"subject": "al-bus", "topic": "AB3.2", "why": "价格弹性与定价战略（A2）。"},
     ]},
    {"id": "m-diff", "concept_zh": "差异化与竞争优势", "concept_en": "Differentiation & unfair advantage",
     "comp": "conrad", "context": "Lean Canvas UVP/优势格 · Innovation 20%",
     "matches": [
         {"subject": "ib-econ", "topic": "2.11", "why": "垄断竞争的差异化与进入壁垒(HL)：优势可持续性的理论。"},
         {"subject": "al-econ", "topic": "AE4.4", "why": "寡头非价格竞争与可竞争市场：壁垒决定优势寿命。"},
         {"subject": "ib-bus", "topic": "BB4.3", "why": "USP 与品牌：差异化的商科实现。"},
         {"subject": "al-bus", "topic": "AB6.1", "why": "波特通用战略（差异化/聚焦）。"},
     ]},
    {"id": "m-cost", "concept_zh": "成本结构与规模经济", "concept_en": "Cost structure & economies of scale",
     "comp": "both", "context": "康莱德 Finances 10% · BPA 案例成本分析",
     "matches": [
         {"subject": "ib-econ", "topic": "2.2", "why": "供给/成本视角：产能与投入价格。"},
         {"subject": "al-econ", "topic": "AE4.1", "why": "AC/MC 与规模(不)经济：判断单位成本走势。"},
         {"subject": "ib-bus", "topic": "BB3.2", "why": "固定/可变成本结构直接进 Brief 财务表。"},
         {"subject": "al-bus", "topic": "AB4.1", "why": "规模经济五类与产能利用率。"},
     ]},
    {"id": "m-bep", "concept_zh": "盈亏平衡分析", "concept_en": "Break-even analysis",
     "comp": "both", "context": "康莱德 Practicality/Finances · BPA 客观题+案例",
     "matches": [
         {"subject": "ib-bus", "topic": "BB5.4", "why": "BEP=FC/(P−VC)、安全边际：可行性论证标配。"},
         {"subject": "al-bus", "topic": "AB5.1", "why": "AS 财务预测中的盈亏平衡。"},
         {"subject": "al-econ", "topic": "AE4.1", "why": "成本理论（固定/可变）是 BEP 的经济学基础。"},
     ]},
    {"id": "m-finstmt", "concept_zh": "三大财务报表", "concept_en": "Financial statements",
     "comp": "both", "context": "康莱德 Finances 10% · BPA 财务类客观题/WSAP",
     "matches": [
         {"subject": "ib-bus", "topic": "BB3.3", "why": "利润表与资产负债表的结构与勾稽。"},
         {"subject": "al-bus", "topic": "AB5.2", "why": "A2 报表解读与调整。"},
     ]},
    {"id": "m-appraisal", "concept_zh": "投资评估 NPV/IRR/ARR", "concept_en": "Investment appraisal",
     "comp": "both", "context": "康莱德融资策略 · BPA 案例决策建议",
     "matches": [
         {"subject": "ib-bus", "topic": "BB3.7", "why": "NPV/回收期(HL)：设备/扩张决策的量化依据。"},
         {"subject": "al-bus", "topic": "AB5.2", "why": "ARR/NPV 与折现思想。"},
     ]},
    {"id": "m-cash", "concept_zh": "现金流管理", "concept_en": "Cash flow management",
     "comp": "both", "context": "康莱德 burn rate / runway · BPA 案例",
     "matches": [
         {"subject": "ib-bus", "topic": "BB3.6", "why": "现金流预测：\"盈利也会死\"的关键概念。"},
         {"subject": "al-bus", "topic": "AB5.1", "why": "现金流预测与赤字对策(AS)。"},
     ]},
    {"id": "m-unit-econ", "concept_zh": "LTV/CAC 与单位经济", "concept_en": "LTV/CAC & unit economics",
     "comp": "conrad", "context": "Lean Canvas 指标格 · 评委追问高频",
     "matches": [
         {"subject": "ib-bus", "topic": "BB4.1", "why": "客户调研→留存→LTV 的数据链。"},
         {"subject": "ib-econ", "topic": "2.5", "why": "弹性与重复购买（YED/习惯形成）影响 LTV。"},
         {"subject": "al-bus", "topic": "AB3.2", "why": "品牌与留存策略（A2）。"},
     ]},
    {"id": "m-7p", "concept_zh": "STP 与营销组合 7P", "concept_en": "STP & marketing mix",
     "comp": "both", "context": "康莱德 Marketing 10% · BPA 营销案例/客观题",
     "matches": [
         {"subject": "ib-bus", "topic": "BB4.2", "why": "7P 整体一致性：Brief 市场部分的骨架。"},
         {"subject": "ib-bus", "topic": "BB4.3", "why": "细分-目标-定位与品牌落地。"},
         {"subject": "al-bus", "topic": "AB3.1", "why": "市场细分与 PLC 策略(AS)。"},
         {"subject": "al-econ", "topic": "AE2.2", "why": "YED/XED 支持细分市场的选择。"},
     ]},
    {"id": "m-promo", "concept_zh": "促销与 AIDA", "concept_en": "Promotion & AIDA",
     "comp": "conrad", "context": "康莱德 Marketing · Pitch 的获客叙事",
     "matches": [
         {"subject": "ib-bus", "topic": "BB4.5", "why": "推/拉策略与促销组合选择。"},
         {"subject": "al-bus", "topic": "AB3.2", "why": "整合营销传播(IMC)。"},
     ]},
    {"id": "m-channel", "concept_zh": "渠道与电商", "concept_en": "Place & e-commerce",
     "comp": "conrad", "context": "Lean Canvas 渠道格 · Marketing 10%",
     "matches": [
         {"subject": "ib-bus", "topic": "BB4.6", "why": "分销渠道长度与电商模式。"},
         {"subject": "al-bus", "topic": "AB3.1", "why": "渠道决策与零售业态。"},
     ]},
    {"id": "m-intl", "concept_zh": "国际市场与贸易", "concept_en": "International market & trade",
     "comp": "conrad", "context": "康莱德 Brief 的市场扩展叙事（全球站）",
     "matches": [
         {"subject": "ib-econ", "topic": "4.1", "why": "比较优势：为什么跨国分工。"},
         {"subject": "ib-econ", "topic": "4.2", "why": "关税/壁垒影响出海成本。"},
         {"subject": "ib-bus", "topic": "BB4.7", "why": "国际化营销与本土化(HL)。"},
         {"subject": "al-econ", "topic": "AE6.1", "why": "贸易收益与保护主义(AS/A2)。"},
     ]},
    {"id": "m-swot", "concept_zh": "SWOT / 五力 / PESTEL", "concept_en": "Strategic analysis tools",
     "comp": "bpa", "context": "BPA 案例分析标准框架 · 康莱德竞品格",
     "matches": [
         {"subject": "al-bus", "topic": "AB6.1", "why": "战略分析与选择(A2)的核心工具箱。"},
         {"subject": "ib-bus", "topic": "BB1.5", "why": "STEEPLE 外部环境扫描。"},
         {"subject": "ib-econ", "topic": "2.11", "why": "五力的经济学原型：市场力量与壁垒(HL)。"},
         {"subject": "comp", "topic": "CP2.2", "why": "BPA 案例三步答题法的诊断环节。"},
     ]},
    {"id": "m-ops", "concept_zh": "运营与精益生产", "concept_en": "Operations & lean",
     "comp": "conrad", "context": "康莱德 Practicality 20%（可行性/概念验证）",
     "matches": [
         {"subject": "ib-bus", "topic": "BB5.1", "why": "精益/JIT/Kaizen：证明\"造得出来\"。"},
         {"subject": "ib-bus", "topic": "BB5.2", "why": "生产方式与选址。"},
         {"subject": "al-bus", "topic": "AB4.2", "why": "精益与库存/供应链(A2)。"},
     ]},
    {"id": "m-team", "concept_zh": "团队与组织（叙事）", "concept_en": "Team & storytelling",
     "comp": "conrad", "context": "康莱德 Storytelling 20%（团队可信度）",
     "matches": [
         {"subject": "ib-bus", "topic": "BB2.2", "why": "激励理论解释团队分工与积极性。"},
         {"subject": "ib-bus", "topic": "BB2.3", "why": "领导风格与角色配置(HL)。"},
         {"subject": "al-bus", "topic": "AB2.2", "why": "组织结构与授权(A2)。"},
     ]},
    {"id": "m-change", "concept_zh": "变革与危机管理", "concept_en": "Change & crisis management",
     "comp": "bpa", "context": "BPA 案例\"企业转型\"母题",
     "matches": [
         {"subject": "al-bus", "topic": "AB6.2", "why": "Lewin 三步与变革阻力(A2)。"},
         {"subject": "ib-bus", "topic": "BB1.5", "why": "增长与组织演化。"},
     ]},
    {"id": "m-macro", "concept_zh": "宏观环境判断", "concept_en": "Macro environment reading",
     "comp": "bpa", "context": "BPA 客观题宏观部分 · 案例背景分析",
     "matches": [
         {"subject": "ib-econ", "topic": "3.2", "why": "AD/AS 判断经济周期位置。"},
         {"subject": "ib-econ", "topic": "3.5", "why": "利率环境影响企业融资决策。"},
         {"subject": "al-econ", "topic": "AE5.4", "why": "财政/货币政策与商业周期(AS)。"},
         {"subject": "al-bus", "topic": "AB1.3", "why": "PEST 的 E 维度。"},
     ]},
    {"id": "m-policy", "concept_zh": "政策评估（税/补贴/管制）", "concept_en": "Policy evaluation",
     "comp": "bpa", "context": "BPA 案例\"政府政策影响\"题型",
     "matches": [
         {"subject": "ib-econ", "topic": "2.7", "why": "间接税/补贴的归宿与效果。"},
         {"subject": "ib-econ", "topic": "2.8", "why": "外部性矫正政策的选择与评估。"},
         {"subject": "al-econ", "topic": "AE3.3", "why": "管制/碳交易/私有化评估(A2)。"},
     ]},
    {"id": "m-labor", "concept_zh": "劳动力与人力", "concept_en": "Labour & HR",
     "comp": "bpa", "context": "BPA HR 方向 WSAP · 案例人力成本",
     "matches": [
         {"subject": "ib-bus", "topic": "BB2.1", "why": "HRM 与流失率计算。"},
         {"subject": "al-econ", "topic": "AE4.7", "why": "劳动市场与工资决定(A2)。"},
         {"subject": "al-bus", "topic": "AB2.1", "why": "激励与契约(AS)。"},
     ]},
]

# IGCSE 0450 matches appended to the entries above (curated from 0450 syllabus)
_IGCSE_MATCHES = {
    "m-theme": [("IG6.2", "环境与伦理议题：Theme/ESG 的 IGCSE 对应内容。"),
                 ("IG6.1", "经济周期/汇率等外部议题支撑 Theme 的宏观叙事。")],
    "m-tam": [("IG3.2", "市场调研方法为 TAM/SAM/SOM 提供数据口径。")],
    "m-problem": [("IG3.1", "顾客需求与细分：Problem 的人群定位入门。"),
                   ("IG3.2", "调研（问卷/焦点小组）支撑问题的量化证据。")],
    "m-pricing": [("IG3.4", "定价策略（渗透/撇脂/成本加成）是 Marketing 维度的定价工具。")],
    "m-diff": [("IG3.3", "品牌/差异化/USP：不公平优势的 IGCSE 表达。")],
    "m-cost": [("IG4.1", "生产方式与生产率。"),
                ("IG4.2", "固定/可变成本结构直接进成本表。")],
    "m-bep": [("IG4.2", "盈亏平衡是 0450 必考计算，直接服务 Finances/Practicality。")],
    "m-finstmt": [("IG5.3", "利润表结构。"), ("IG5.4", "资产负债表。")],
    "m-appraisal": [("IG4.2", "盈亏平衡/安全边际提供最基础的投资可行性判断（0450 无 NPV）。")],
    "m-cash": [("IG5.2", "现金流预测与对策。")],
    "m-unit-econ": [("IG5.6", "报表使用者视角（银行/股东）呼应融资逻辑。")],
    "m-7p": [("IG3.1", "市场细分与顾客需求（STP 入门）。"), ("IG3.3", "产品与生命周期策略。")],
    "m-promo": [("IG3.5", "促销组合（线上广告/线下推广）与 AIDA 的入门对应。")],
    "m-channel": [("IG3.6", "分销渠道与电商：Lean Canvas 渠道格的学科基础。")],
    "m-intl": [("IG6.3", "全球化与跨国公司：出海叙事的 IGCSE 支撑。")],
    "m-ops": [("IG4.1", "精益/JIT/质量：Practicality 可行性论证的核心。")],
    "m-team": [("IG2.2", "激励理论支撑团队叙事。"),
                ("IG2.3", "组织结构与领导：团队分工的 IGCSE 表达。")],
    "m-change": [("IG2.3", "组织结构与授权：变革阻力的入门视角。")],
    "m-macro": [("IG6.1", "通胀/失业/汇率/利率：Pitch 宏观背景一段话的来源。")],
    "m-policy": [("IG3.7", "营销法律管制：政策环境影响的入门。")],
    "m-labor": [("IG2.1", "招聘/培训/裁员：人力成本与组织的基础。")],
}
for _e in MAPPING:
    for _tid, _why in _IGCSE_MATCHES.get(_e["id"], []):
        _e["matches"].append({"subject": "igcse-bus", "topic": _tid, "why": _why})

# 学科 → 竞赛 反向视角的补充说明（用于反向表表头提示）
REVERSE_NOTE = "反查用法：备赛学生按竞赛任务找到要用的学科知识点；学科学生按知识点找到竞赛练兵场。"
