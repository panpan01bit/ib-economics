# -*- coding: utf-8 -*-
"""术语深度内容（商科侧 + 跨科目桥梁）。
- ENRICH_BUS：IGCSE 商科 / IB 商科 / AL 商科 / 竞赛 的术语详解（more + example）。
- BRIDGES：跨科目概念簇。members=(subject_id, term_en) 互为"同概念"链接；
  whole=上位概念（这个概念是哪个更大框架的一部分）；
  prereq=先决条件（它是什么题/什么分析的前提）。
- all_glossaries()/enrich_subject()：供 build_subjects.py 与 analyze.py 调用。
"""

ENRICH_BUS = {
    # ------------------------------------------------------------------ IGCSE 商科
    "igcse-bus": {
        "Added value": {
            "more": "增值=产出价值−购入材料与服务的成本，衡量企业在链条中“创造”了多少财富。0450 论述题常把增值与目的、企业家职能、利润混为一谈：利润还要再扣人工、租金等其他成本，增值先于利润。提高增值的两条路：提高单位售价（品牌、质量）或降低购入成本（议价、工艺）。",
            "example": "面包店面粉黄油成本 8 元，面包卖 15 元，增值 7 元；再扣人工房租后剩 2 元才是利润。",
        },
        "Opportunity cost": {
            "more": "IG 阶段重点在“商业决策的机会成本”：资金、老板的时间、店面空间投向 A 就不能投向 B。d(c) 8 分题用它做评价的骨架——推荐方案时必须点明放弃了什么。与经济科的 opportunity cost 是同一个概念，AL/IB 经济会把它画成 PPC。",
            "example": "便利店把角落改成咖啡吧，机会成本是该角落原本货架的日用品销量。",
        },
        "Limited liability": {
            "more": "有限责任=股东最多损失投入的股本，个人财产不受公司债务牵连。这是公司（ltd/plc）相对独资合伙的核心优势，也是“风险换融资”的制度基础。IG 论述题常与“筹资渠道选择”结合：外部投资人只有有限责任保护才肯入股。",
            "example": "有限责任公司破产欠债 100 万，股东只损失认购股份的钱，房子车子安全。",
        },
        "Franchise": {
            "more": "特许经营=加盟商付费获得品牌、流程与供应链使用权。对加盟商：低失败率+现成客源 vs 付出加盟费/抽成、丧失经营自由；对品牌方：轻资产快速扩张+加盟商自担风险。评价题两边都要写，并给出“适合什么人”的条件判断。",
            "example": "麦当劳门店多为加盟：业主出资经营，总部收加盟费并强制执行统一标准。",
        },
        "Joint venture": {
            "more": "合资=两家以上企业共投资源、共担风险做一件事。优点：互补技术、分摊成本、进入受管制市场；缺点：文化冲突、利润分享、机密泄露。与 merger 的区别：合资只绑定一个项目/实体，不合并整体。",
            "example": "外资车企与本地厂商合资建厂，换取政策准入与渠道，本地伙伴获得技术。",
        },
        "Economies of scale": {
            "more": "规模经济=产量扩大使平均成本下降：采购议价、专业化分工、设备摊薄、融资便宜。在 IG 阶段要与“大企业病”（协调困难）对冲着写。它也是连接经济科的桥：AL 经济把它画成 LRAC 递减段，并推出自然垄断。",
            "example": "连锁咖啡集中烘焙采购生豆，单杯豆成本比独立小店低三成。",
        },
        "Stakeholder": {
            "more": "利益相关者=影响或被企业影响的群体：股东、员工、顾客、供应商、银行、政府、社区。IG 论述的万能框架之一：任何决策（涨价、裁员、迁厂）都要求“对不同 stakeholder 的冲突影响”分层讨论，再给出权衡结论。与竞赛里的 ESG/SDG 直接相关。",
            "example": "工厂自动化：股东省钱、部分员工失业、顾客享受降价、政府税收结构改变——同一决策四种结果。",
        },
        "Privatisation": {
            "more": "私有化=国有转民营，与 mixed economy（混合经济）概念配套。论点：效率激励、减财政负担 vs 私人垄断抬价、公共服务断供。IG 考试要求能用具体行业（水务、电力、公交）双边论述。",
            "example": "英国铁路“路网国有、运营私有”就是部分私有化的折中形态。",
        },
        "Maslow's hierarchy": {
            "more": "马斯洛五层：生理→安全→社交→尊重→自我实现，低层满足后高层才成为主导激励。商业应用：工资保底两层、团队与表彰供给中层、授权与成长满足顶层。批评：层次并非严格递进、个体差异大——评价时必须带上。",
            "example": "制造业先确保计件工资稳定（安全），再靠班组关系（社交）与月度之星（尊重）留人。",
        },
        "Herzberg two-factor": {
            "more": "双因素：保健因素（工资、条件、政策）不好会不满，好了也只“不满消失”并不激励；激励因素（成就、认可、责任、成长）才真正驱动绩效。管理含义：光涨薪有天花板，激励要靠工作本身。IG 论述常把它与马斯洛对比使用。",
            "example": "公司空调修好了抱怨消失但效率没升；真正的提升来自让员工主导一个新品项目。",
        },
        "Job enrichment": {
            "more": "工作丰富化=纵向加载责任与自主权（不只是横向加活，那是 job enlargement）。与 Herzberg 激励因素直接对应。风险：不是人人想要更多责任（能力/意愿差异），培训与薪酬要跟上。",
            "example": "客服专员获得“自行决定 200 元内赔付”的权限，处理速度与成就感同时上升。",
        },
        "Span of control": {
            "more": "管理幅度=一名上级直接管理的人数。宽幅度=扁平结构、沟通快但监督弱；窄幅度=层级多、控制紧但成本高且信息失真。影响因素：下属能力、任务复杂度、监督技术。IG 组织结构题的基本参数。",
            "example": "流水线标准化作业可以 1 管 20；研发团队 1 管 5 才顾得过来。",
        },
        "Delegation": {
            "more": "授权=把任务与相应权限下放，但最终责任仍在上级。作用：减负、培养接班人、提升响应速度（与授权型领导、empowerment 一脉）。失败原因常见于“只给活不给权”或上司不愿担最终责任。",
            "example": "店长把采购决定权交给副手并保留复核，自己腾出手开新店。",
        },
        "Trade union": {
            "more": "工会代表雇员集体谈判工资与条件。集体力量提高谈判地位（否则个体面对雇主议价弱），工具包括谈判、行动（罢工）与协商。IG 题要求双边：工资与保障提升 vs 成本上升、罢工双输、罢工资格的法律边界。",
            "example": "港口工会集体谈判使装卸时薪上调 8%，船公司转向自动化应对。",
        },
        "Niche market": {
            "more": "利基市场=大企业看不上、需求独特的小细分。优点：竞争少、专注溢价、贴近顾客；缺点：容量天花板、易被巨头顺手碾压、需求波动即生死。与 mass market 对比出题是 d 题常客。",
            "example": "专做左手吉他的小厂：市场规模有限但几乎没有直接竞争者，可维持高毛利。",
        },
        "Market orientation": {
            "more": "市场导向=先做调研按需求开发产品，与产品导向（先做出来再找买家）相对。优点：命中需求、退货少；缺点：调研成本、滞后于颠覆式创新（顾客说不出他们没见过的东西）。IG 常配 market research 一起考。",
            "example": "饮料公司调研发现低糖需求，抢先推无糖线；对手笃信“经典配方”错失窗口。",
        },
        "Primary research": {
            "more": "一手调研=自己直接收集：问卷、访谈、焦点小组、观察、试销。优：针对性强、最新；劣：贵、慢、样本偏差。与 secondary research（现成数据）互补搭配是标准答法。竞赛里的“客户访谈 100 人”就是 primary research 的实操。",
            "example": "开店前一周在商圈门口做 200 份口味问卷，决定菜单主推单品。",
        },
        "Product life cycle": {
            "more": "导入→成长→成熟→衰退四阶段：各阶段的营销/定价/现金特征不同（导入期亏钱铺渠道、成熟期利润主力、衰退期收割或转型）。策略含义是 extension strategy 与 Ansoff 的再投资决策。局限：长度不可预测、可被营销人为续命、部分产品周期极短。",
            "example": "功能手机在成熟期被智能手机直接送入衰退，NoKia 用品牌授权续命。",
        },
        "Extension strategy": {
            "more": "延长成熟期/推迟衰退：改包装、新口味、新渠道、降价渗透、找新细分。本质是“再投资换时间”，为下一代产品研发争取现金。评价：烧钱买时间是否值得，取决于后续产品线的衔接。",
            "example": "老款游戏机出轻薄版+降价 30%，为新一代主机上市前维持现金流。",
        },
        "Penetration pricing": {
            "more": "渗透定价=低价切入抢份额，适合需求弹性大、有规模经济、怕模仿的场景；导入期专用。风险：低价锚定品牌形象、提价难（消费者反弹）、被更大对手用更低价格反杀。与 skimming 是 d 题的常见对比组合。",
            "example": "新 streaming 平台首年月费 5 元抢用户，靠规模摊薄内容成本后再提价。",
        },
        "Price skimming": {
            "more": "撇脂定价=先高价收割最愿付的人，再逐步降价放量。前提：新品有独特价值、短期无竞争、不同收入层可分层。风险：高价吸引模仿者、早期买家在降价时感到被背刺（声誉）。科技产品经典。",
            "example": "旗舰手机发布价 9999，半年后降到 7999，两年后 4999 清库存。",
        },
        "Above-the-line": {
            "more": "线上推广=面向大众的付费广告（电视、户外、门户、信息流），广而告之建认知；对应 below-the-line 是定向促销（直邮、赞助、促销活动、社媒互动）。选择逻辑：预算、目标（认知 vs 转化）、受众媒体习惯。IG 考试要求按场景选组合而不是背定义。",
            "example": "新品上市先投电视与信息流广告铺认知，再用地推试饮做转化。",
        },
        "Below-the-line": {
            "more": "线下/定向推广：针对具体人群的促销、直邮、赞助、展销、口碑与社媒运营。优：精准可测、性价比高；劣：覆盖窄、制作管理耗时。与 above-the-line 组合成整合营销（IMC，AL 商科概念）。",
            "example": "母婴品牌只在月子所与妈妈社群做试用与讲座，转化率远高于大众广告。",
        },
        "Distribution channel": {
            "more": "分销渠道=产品到消费者手里的路径：直售→零售→批发→代理/经销商，加上电商与直播新链路。选择因素：单价、保鲜、市场覆盖、控制欲与成本。渠道变革（DTC、平台化）是当代案例题热点。",
            "example": "眼镜品牌从百货专柜转向 DTC 电商+体验店，砍掉中间加价后售价降三成。",
        },
        "Consumer protection": {
            "more": "消费者保护法界定商品安全、信息真实与退换责任。对企业是合规成本，也是建立信任的资产；对市场纠正信息不对称（连回经济科 asymmetric information）。IG 常考“违法代价+为什么守法反而有利”。",
            "example": "虚标续航被罚款+召回，短期省钱长期品牌崩塌——反面教材的标准写法。",
        },
        "Lean production": {
            "more": "精益生产=持续消除一切不增值的浪费（时间、库存、次品、多余动作），核心是“只做顾客愿意付钱的事”。工具箱：JIT、Kaizen、质量前置。评价：省成本提周转 vs 对供应链稳定性要求高、员工压力上升。",
            "example": "家具厂把工序重排并砍掉中转仓，交付周期从 4 周缩到 9 天。",
        },
        "JIT": {
            "more": "准时制=物料恰好按生产需要到达，库存近零。优点：库存成本与呆滞风险骤降、问题即时暴露；风险：供应链一断全线停摆（疫情期汽车芯片荒就是 JIT 脆弱性的大案例）。多数企业实际采用 JIT+安全库存的混合。",
            "example": "总装线按两小时节拍收零部件，供应商在 50 公里半径内循环送货。",
        },
        "Quality assurance": {
            "more": "质量保证=全流程每个人对质量负责、预防缺陷（过程导向）；区别于 quality control 事后检验挑次品（产品导向）。ISO 认证、TQM 都建立在 QA 思想上。d 题对比两者时，落点在“成本前置 vs 成本后置”。",
            "example": "流水线任何工人发现异常可拉停整线（安灯系统），缺陷不流入下道工序。",
        },
        "Break-even": {
            "more": "盈亏平衡点=贡献恰好盖住固定成本的产量：BEP=FC÷单位贡献。必须会画图（FC 线、TC 线、TR 线、BEP 交点、安全边际区）并算数字。用途：定价/成本决策、抗风险评估、新项目可行性初筛。假设刚性（价格、单位变动成本不变）是评价点。",
            "example": "固定成本 6 万、每杯咖啡贡献 12 元 → 5000 杯回本；月卖 7000 杯则有 2000 杯安全边际。",
        },
        "Margin of safety": {
            "more": "安全边际=实际（或预期）销量−盈亏平衡销量，可换算成百分比。它度量“生意离亏损有多远”，是银行与投资人最关心的稳健指标之一。固定成本占比越高，BEP 越高、安全边际越薄——运营杠杆视角。",
            "example": "月 BEP 5000 杯、预计 7000 杯，安全边际 28.6%：销量跌三成以内不亏。",
        },
        "Contribution": {
            "more": "贡献=售价−单位变动成本，先“贡献”去盖固定成本，盖完才是利润。它是 BEP 计算、特殊订单定价（只要价格>VC 短期可接）、产品线取舍的共同工具。注意与毛利区分：贡献不扣固定制造费。",
            "example": "售价 15、变动成本 8 → 每单位贡献 7 元；临时团购价 12 元仍贡献 4 元，短期可接。",
        },
        "Cash flow forecast": {
            "more": "现金流预测按月列“期初+流入−流出=期末”，用来提前发现资金缺口、安排透支或融资。考试要求会填表并解释某月为何转负（季节性备货、赊账周期错配）。核心观念：利润≠现金，赊销有利润没现金。",
            "example": "圣诞季前两个月大量进货，现金转负，靠透支额度桥接到节后回款。",
        },
        "Working capital": {
            "more": "营运资本=流动资产−流动负债，支撑日常周转的“血量”。过少→付款与断供风险；过多→资金躺在低收益资产上。管理与现金循环周期（进货→销售→回款）联动。比率题里配 current ratio / acid test 一起考。",
            "example": "超市压低存货天数、向供应商赊账，把现金循环变成负数——用别人的钱做生意。",
        },
        "ROCE": {
            "more": "资本回报率=营业利润÷所用资本（股本+长期负债），衡量“投入的长期钱赚了多少”。跨企业比较要同行业、警惕一次性损益与资产重估扭曲。与利率/融资成本对比可判断扩张是否创造价值。",
            "example": "ROCE 18% 而银行贷款利率 6% → 借债扩张理论上增厚股东回报（也要看风险）。",
        },
        "Recession": {
            "more": "衰退=实际 GDP 连续两季负增长（常用定义）。对企业：可选消费与耐用品需求暴跌（高 YED）、坏账与库存风险上升。应对：收缩可变成本、保现金、逆周期并购。连回经济科的 business cycle 与 AD 下降。",
            "example": "2009 年奢侈品与汽车销量两位数下滑，折扣零售与维修服务逆势增长。",
        },
        "Exchange rate": {
            "more": "IG 阶段抓两条链：本币贬值→进口原料变贵（成本↑）+出口以外币变便宜（竞争力↑）；升值相反。进口依赖型企业与出口型企业的损益方向相反，d 题要求分主体讨论。与经济科 exchange rate 同源，AL 会加汇率制度与马歇尔-勒纳。",
            "example": "日元贬值使丰田出口利润大增，同时日本进口能源成本飙升推高物价。",
        },
    },
    # ------------------------------------------------------------------ IB 商科
    "ib-bus": {
        "SMART objectives": {
            "more": "目标要 Specific/Measurable/Achievable/Relevant/Time-bound。作用：统一方向、绩效考核基准、激励与问责。评价：过度聚焦 SMART 目标诱发短视与指标博弈（“考核什么得到什么”）。给企业案例设目标并批判是 BM 论文常见任务。",
            "example": "“12 个月内将复购率从 20% 提升到 30%（按季度追踪）”远好于“提升客户忠诚度”。",
        },
        "Stakeholder": {
            "more": "IB BM 的 stakeholder 分析强调权力-利益矩阵（power/interest grid）选沟通策略，以及 HL 的冲突调和。任何战略题（增长、外包、合并）都用“对不同 stakeholder 的影响”展开 AO2/AO3。与康莱德的 ESG/SDG 评价维度直接相通。",
            "example": "裁员决策：股东与高管受益、员工与社区受损——用权力利益矩阵决定谁必须先沟通。",
        },
        "STEEPLE": {
            "more": "外部环境扫描框架：社会/技术/经济/环境/政治/法律/伦理。用途是机会与威胁（接 SWOT 的 OT 半边）。评价：维度全但易泛泛而谈，要与具体行业的关键驱动力挂钩才有分析价值。AL 商科叫 PEST（少环境伦理维度）。",
            "example": "教培企业做 STEEPLE：政策（监管收紧）与技术（AI 学习）两个维度权重最高。",
        },
        "Ansoff matrix": {
            "more": "增长四象限：市场渗透（老产品老市场，风险最低）→市场开发→产品开发→多元化（风险最高）。考法：给案例判断处于哪格、评估风险与资源匹配度。与风险管理、融资能力联动（多元化常需大额资金）。",
            "example": "元气森林先气泡水渗透（同款多渠道），再推电解质水（产品开发），风险逐级抬升。",
        },
        "Labour turnover": {
            "more": "员工流失率=期间离职人数÷平均员工数。高流失=招聘培训成本+知识流失+士气与服务质量下滑；过低也可能意味着僵化缺活力。诊断要分层（部门、年限、绩效），对策连回激励理论（Herzberg）与领导方式。",
            "example": "呼叫中心年流失 60%，替换成本占工资 40%——投资管理与职业路径后降到 25%。",
        },
        "Herzberg": {
            "more": "IB 版本同样双因素：保健（薪酬、政策、环境、关系）止不满，激励（成就、认可、责任、成长、进步）造满意。论文要求用案例把“涨薪天花板”讲透，并与 Maslow、Taylor、赋能等组合成激励工具箱。",
            "example": "远程办公政策解决的是保健因素；职级与项目Ownership才真正留优秀工程师。",
        },
        "Laissez-faire": {
            "more": "放任型领导给资源与自由、极少干预，适合自我驱动的高技能团队（研发、创意）；代价是方向涣散与绩效失控。与民主型、专制型组成风格谱系，判断“情境匹配”而非“哪种最好”才是 AO3 满分姿势（连领导情境理论）。",
            "example": "游戏工作室主创团队近乎自治，发行节点前才介入里程碑评审。",
        },
        "Depreciation": {
            "more": "在 IB 财务语境有两义：①固定资产折旧（成本按使用年限分摊，影响利润但不减现金）；②货币贬值（连经济科）。考试先辨义再作答。折旧方法（直线/余额递减）会改变各年利润与资产净值，是报表分析常考点。",
            "example": "百万设备直线折旧 5 年：每年利润减 20 万现金却没流出——EBITDA 与净利润差异的来源之一。",
        },
        "ROCE": {
            "more": "IB BM 要求会用、会比较、会挑毛病：跨年趋势、同业对标、一次性项目与租赁资本化的影响。作为“长期资金效率”指标，配合利润率与周转率拆解（杜邦思路）更完整。与 AL 商科同名指标完全一致。",
            "example": "两家利润率相同的企业，轻资产模式的 ROCE 显著更高——资本结构差异所致。",
        },
        "Current ratio": {
            "more": "流动比率=流动资产÷流动负债，经验区间 1.5–2。过低有断供风险，过高说明存货/应收淤积。必须与 acid test（剔除存货）连用——存货占比高时流动比率会高估流动性。 d 题给两张报表比较流动性是固定曲目。",
            "example": "流动比率 2.5 但全是压仓存货：剔除后 acid test 仅 0.6，实际风险很高。",
        },
        "Working capital": {
            "more": "IB 的营运资本管理扩展到现金循环周期：存货天数+应收天数−应付天数。缩短周期的抓手：精益库存、应收账期管理、供应商议价。HL 案例常把营运资本危机当作增长过快的并发症（增长吞噬现金）。",
            "example": "营收翻倍但账期 90 天：利润表漂亮、现金转负，需要融资桥接——growth eats cash。",
        },
        "NPV": {
            "more": "净现值=各期现金流按资本成本折现后加总减初始投资，>0 则创造价值。相比回收期它考虑全部现金流与货币时间价值，是 HL 投资评估首选；缺点是折现率假设敏感、远期数字可信度问题。与 AL 商科 ARR/回收期、竞赛的 LTV/CAC 同属估值家族。",
            "example": "机器 3 年现金流折现后合计 120 万>买价 100 万 → NPV=+20 万，可投。",
        },
        "Variance analysis": {
            "more": "差异分析=实际−预算，分有利/不利，再拆价差与量差。目的不是追责而是找原因、改流程（原料涨价、效率、销量结构）。评价：预算本身过时或博弈性松弛（budget slack）会让差异失真。HL 财务单元的核心工具。",
            "example": "原料成本超支 8%：拆出 5% 是采购价上涨（可谈判/换源）、3% 是损耗率（工艺问题）。",
        },
        "Marketing mix": {
            "more": "IB 用 4P（产品/价格/渠道/促销）扩展到 7P（+人员/流程/有形展示）适配服务业。考法是“一致性”：各 P 必须服务同一目标市场定位，互相打架的 mix 是典型扣分点。延伸概念：数字化 mix、整合营销（AL 的 IMC）。",
            "example": "高端定位配低价促销渠道会互相拆台——mix 一致性比单个 P 的“最优”更重要。",
        },
        "AIDA": {
            "more": "消费者反应漏斗：注意→兴趣→欲望→行动。用途：诊断营销漏斗断在哪一层（曝光高转化低=兴趣到欲望断层），据此选工具。评价：线性模型不适应社媒时代的循环与口碑路径，但作诊断骨架依然好用。",
            "example": "广告点击率高、下单率低：问题在 Desire 层，改详情页与社会证明而非加投放。",
        },
        "TQM": {
            "more": "全面质量管理=质量是全员全流程的责任，以顾客为中心、持续改进（Kaizen）、零缺陷文化。与事后 QC 相比把质量成本前移（预防成本<失败成本）。落地难点：文化变革、度量与授权。丰田体系是标准案例。",
            "example": "全员提案制度每年采纳上千条微改进，次品率与返工成本逐年下降。",
        },
        "Break-even point": {
            "more": "IB 版本要会算、会画、会用于决策情境（定价选择、外包 vs 自制、新增固定成本）。多产品 BE 用加权平均贡献算。评价假设：线性价格与成本、单一产品、产量=销量。与 IG/AL 同源，IB 更强调情境应用与敏感性。",
            "example": "自营客服月固定 10 万、单位 5 元；外包按 8 元/单无固定——月单量低于 3.3 万单外包更省。",
        },
        "Mission statement": {
            "more": "使命陈述回答“我们为谁创造什么价值、为何存在”，为战略提供长期方向与身份认同。评价：好使命可指导取舍（说“不”的依据），坏使命是墙上的空话（无法操作、无法证伪）。与愿景/价值观/目标层级串起来记。",
            "example": "“组织全世界的信息”让谷歌历史上多次拒绝与搜索无关的机会——使命的真用途。",
        },
        "Ethics": {
            "more": "商业伦理超出法律底线：诚信、公平、责任。IB 考“伦理与利润是否冲突”的双边论证（短期成本 vs 长期声誉、员工敬业、监管关系），以及 stakeholder 视角的伦理分析。与 CSR、可持续、康莱德 ESG 维度天然衔接。",
            "example": "主动召回成本 2 亿但保住品牌信任；同业隐瞒缺陷者被罚 10 亿+销量腰斩。",
        },
        "Horizontal integration": {
            "more": "横向整合=并购同行业同环节竞争者：消除竞争、规模经济、扩大份额；风险：垄断审查、文化冲突、协同不及预期。与纵向（上下游）、混合（跨行业）并列为并购三型，判断类型+评估协同是固定考法。",
            "example": "两家区域快递合并覆盖全国，干线装载率上升摊薄单位成本。",
        },
        "Vertical integration": {
            "more": "纵向整合并购上下游：控制供应质量/关键原料（后向）或渠道与客户触点（前向）。收益：交易成本内部化、议价力、保证供给；代价：资本重、灵活性差（上游被锁定）。平台时代更多用“生态”替代重资产整合。",
            "example": "电动车厂自建电池厂保证供应并压成本——后向纵向整合的当代样板。",
        },
        "Conglomerate": {
            "more": "混合并购跨行业组合，逻辑是分散风险（行业周期互补）与内部资本市场；代价是管理半径过大、不相关协同很弱（母公司折价）。评价时几乎一定要提到“多元化折扣”与专注派（核心竞争力）的反驳。",
            "example": "集团同时持有地产、传媒、保险：任一行业下行时集团整体波动更小。",
        },
        "Strategic alliance": {
            "more": "战略联盟=不并股权的合作（合资、联营、许可、特许）。动机：共享风险与技术、进入新市场、绕开外资限制；风险：知识泄露、依赖不对称、目标漂移。与并购对比：轻、快、可逆但控制力弱。",
            "example": "航司联盟共享代码与贵宾室，用合作网络对抗超级承运人而无须合并。",
        },
        "Outsourcing": {
            "more": "外包把非核心职能交给外部：聚焦核心、转固定成本为变动、借用专业能力；风险：质量失控、机密外流、依赖锁定（切换成本）。判断标准是“核心能力与否+交易成本”，一刀切外包与一律自营都是错的。",
            "example": "把 IT 运维外包省 30%，但核心数据平台自研自营——核心/非核心的边界划分。",
        },
        "Glocalization": {
            "more": "全球本土化=全球品牌框架+本地化执行（菜单、定价、内容）。解决标准化（规模经济、品牌一致）与本地响应（口味、法规、文化）的两难。国际营销题的核心张力就是 this。评价：过度本地稀释品牌，过度标准错失市场。",
            "example": "快餐巨头在印度用素食汉堡替代牛肉产品，品牌视觉全球统一。",
        },
        "Force field analysis": {
            "more": "力场分析：现状=驱动力与阻碍力的平衡，变革=增强驱动或削弱阻碍（通常更有效，因为阻力常源于恐惧而非反对目标）。与 Lewin 三阶段（AL 商科）配套使用，是变革管理题的结构化工具。",
            "example": "推行新系统：阻力多来自“怕学不会”，先培训与试点（削弱阻碍）比强推命令更有效。",
        },
        "Piece rate": {
            "more": "计件工资=按产出付酬，激励直接、计酬透明；适用标准化可计件的工作。代价：质量投机（求快求量）、设备损耗、团队协作瓦解、需求低谷时收入波动。现代变体是绩效奖金与佣金制。",
            "example": "采摘按公斤计酬高效，但精细装配若计件则次品率上升——需配质检对冲。",
        },
        "Profit sharing": {
            "more": "利润分享把部分利润分给员工，对齐利益、培养主人翁感；局限：个人努力与总利润关系模糊（搭便车）、周期性行业利润波动使激励失真。与持股计划（ESOP）一起构成财务性参与。",
            "example": "小企业拿出利润 10% 按贡献分红，次年主动节约成本的建议明显变多。",
        },
        "Empowerment": {
            "more": "授权赋能=给一线员工决策权与资源（连 Herzberg 激励因素与授权型领导）。收益：响应速度、创新、客户满意；条件：培训到位、容错文化、清晰的边界。失败常见于“口头授权、审批照旧”。",
            "example": "丽思卡尔顿员工可自主动用 2000 美元为客户救急，无须逐级审批。",
        },
        "Matrix structure": {
            "more": "矩阵结构=职能×项目双线汇报，跨部门协作与资源共享强；代价是双重上司的冲突、权责模糊、会议成本。适合多项目并行的工程/咨询组织。与扁平化、去层级对照出题。",
            "example": "工程师既属研发部（专业线）又属车型项目组（交付线），KPI 两条线各占一半。",
        },
        "Delayering": {
            "more": "去层级=削减中间管理层：加快决策、降低管理成本、扩大管理幅度；风险：监督真空、晋升通道变窄挫伤士气、剩余经理负荷激增。常与扁平结构、信息技术（监控替代人盯人）一起考。",
            "example": "层级从 7 层压到 4 层后，一线反馈直达高管，但中层岗位流失引发士气问题。",
        },
        "Chain of command": {
            "more": "指挥链=命令自上而下的正式路径，与 span of control 共同决定组织形状。长链条信息失真累积、短链条控制弱。矩阵与项目制会“绕开”正式指挥链，带来协调新问题。IG/IB/AL 三科共用此概念。",
            "example": "仓库爆仓信息逐级上报到总部用时 11 天，扁平化后 2 天即获追加预算。",
        },
        "Crowdfunding": {
            "more": "众筹=大众小额集资（预售型/股权型/捐赠型）。功能不止融资：预售验证需求、提前锁定种子用户、制造传播。风险：未达标尴尬、创意被抄、交付压力与预期管理。连竞赛 pitch deck 的 proof of concept。",
            "example": "智能手表项目众筹千万美元：融资本身完成了需求验证+首批订单。",
        },
        "Debenture": {
            "more": "公司债=长期借款凭证，固定利息、求偿优先于股东。优点：不稀释股权、利息可税前扣；风险：财务杠杆放大、条款（抵押/限制）约束经营。与其他长期融资来源对比（股票、长期贷款、租赁）是财务题基本盘。",
            "example": "发债 5 亿利率 5% 建厂，项目 ROCE 12%——杠杆放大股东回报的教科书情形。",
        },
        "Gearing": {
            "more": "资本 gearing=长期负债÷（负债+权益）（口径多样），衡量财务杠杆。高杠杆=扩张弹性和股东回报放大+利息与再融资风险放大。超过约 50% 通常视为偏高，但要结合现金流稳定性与行业惯例判断。",
            "example": "公用事业现金流稳，gearing 60% 可持续；初创软件同样杠杆则近乎赌命。",
        },
        "Market share": {
            "more": "市场份额=本企业销量（额）÷市场总量。意义：规模经济、议价力、渠道控制、心理地位；但份额≠利润（烧钱换份额的失败案例比比皆是）。与市场增长率组合成 BCG 矩阵（AL 商科）的战略含义。",
            "example": "网约车补贴大战份额暴涨但巨亏——份额是手段，价值创造才是目的。",
        },
        "Brand loyalty": {
            "more": "品牌忠诚=重复购买+价格容忍+主动推荐，是护城河的来源（转换成本+心智占位）。度量：复购率、NPS、价格弹性变化。建设路径长期（质量一致、情感叙事、会员体系），可被一次危机清零。",
            "example": "果粉每年换新并容忍溢价；品牌危机后同样的溢价立即失灵。",
        },
        "Cost-plus pricing": {
            "more": "成本加成定价=单位成本+固定利润率。简单、保本导向；致命缺陷：无视需求弹性与竞争价格，加成率是拍脑袋。适合合同定价/公共采购，竞争市场里几乎必然次优。与竞争导向、价值导向定价对比记忆。",
            "example": "工程师文化的公司按成本×1.4 定价，被按“顾客愿付”定价的对手抢占高端。",
        },
        "Capacity utilization": {
            "more": "产能利用率=实际产出÷满负荷产出。过低→固定成本摊薄不足、单位成本高；过高（>90%）→无弹性、维护不足、质量下滑。管理手段：调班、外包峰值、错峰定价。AL 商科同词同义。",
            "example": "酒店淡季利用率 45%：推长住套餐与企业协议价抬升基线需求。",
        },
    },
    # ------------------------------------------------------------------ AL 商科
    "al-bus": {
        "M&A": {
            "more": "并购=兼并（平等合并）+收购（控股买下）。评估框架：动因（协同、份额、能力补全）vs 风险（整合文化、出价过高、监管）。统计上多数并购毁损买方价值——“协同幻觉”是论述题的必写反方。",
            "example": "并购宣称节省 2 亿协同成本，整合两年实际只兑现 30%，商誉减值反噬报表。",
        },
        "PEST analysis": {
            "more": "PEST 扫描政治/经济/社会/技术宏观环境，输出机会与威胁供战略输入。AL 版常扩为 PESTLE（+法律环境）。关键在“影响路径”：政策→成本/需求→企业变量的链条要写具体，抄新闻不算分析。IB 商科的 STEEPLE 同源多两维。",
            "example": "碳关税政策→出口成本+8%→要么本地化生产要么涨价——影响路径完整的写法。",
        },
        "Span of control": {
            "more": "AL 版本同 IG：管理幅度决定层级与沟通质量。组织设计题的抓手：任务标准化程度高→宽幅度；创意与例外多→窄幅度。与 delayering/flat structure 联动考“扁平化的收益与极限”。",
            "example": "客服中心 1 管 15 顺畅；投行团队 1 管 4~5 是常态——工作性质决定幅度。",
        },
        "Market segmentation": {
            "more": "细分维度：地理、人口、心理、行为。好细分=可衡量、可触达、够大、可差异化（可行动）。细分→目标（targeting）→定位（positioning）三步构成 STP（竞赛科也用）。反例：为细分而细分导致 SKU 爆炸、渠道复杂。",
            "example": "运动品牌按“跑步习惯”而非年龄切分：竞速型/养生型/社交型，文案渠道完全不同。",
        },
        "IMC": {
            "more": "整合营销传播=所有触点（广告、公关、促销、直效、社媒、包装）传递同一信息。价值：认知累积、预算效率、品牌一致性；组织障碍：渠道分属不同团队与代理。数字时代 IMC 还要管 UGC 与舆情对信息的“污染”。",
            "example": "“怕上火”一句贯穿电视、包装、社媒与门店物料——教科书级 IMC。",
        },
        "Capacity utilisation": {
            "more": "同 IB 概念：利用率牵动单位成本与交付弹性。AL 考法更算术：给产能与销量算比率、做外包/扩产决策。注意瓶颈工序决定有效产能（TOC 思想可加分）。",
            "example": "产线利用率 78%，旺季缺口 12%：外包比新购设备（折旧+闲置风险）更优。",
        },
        "Porter's generic strategies": {
            "more": "三种通用战略：成本领先、差异化、聚焦（细分市场内的前两者）。夹在中间（stuck in the middle）绩效最差是核心论点。评价：战略可以演化（先聚焦后扩展）、数字化使“双元”成为可能，但考纲仍以经典框架为准。",
            "example": "廉价航空=聚焦+成本领先；独立设计师品牌=聚焦+差异化；两者都避开正面硬刚。",
        },
        "Core competences": {
            "more": "核心竞争力三判据：跨市场通用、对顾客价值贡献大、难模仿。战略应围绕能力而非产品定义（“我们做物流”vs“我们卖书”）。连 Prahalad/Hamel 经典：能力组合决定多元化边界与外包决策。",
            "example": "佳能的光学与精密制造能力依次复制到相机、复印机、打印机——能力驱动的多元化。",
        },
        "Lewin's change model": {
            "more": "解冻（制造紧迫感、瓦解旧习惯）→变革（新行为试点推广）→再冻结（制度固化防回弹）。考点：忽略第 1/3 步是变革失败主因——突变式强推跳过解冻、验收后不管导致回潮。与力场分析（IB 同有）配套。",
            "example": "新 ERP 上线：先停旧流程权限（解冻）→双轨并行（变革）→关闭旧系统（再冻结）。",
        },
        "Entrepreneur": {
            "more": "企业家=识别机会、组合资源、承担风险创造价值的人。特质论（冒险、成就需要）vs 行为论（机会-资源匹配的动作）是论述的两条线。连竞赛科：Lean Canvas 就是把企业家的机会识别流程模板化。",
            "example": "同一商圈别人看到奶茶红海，她看到“宠物友好+现制”空白——机会识别的差异。",
        },
        "Risk vs reward": {
            "more": "风险-回报权衡：高预期回报伴随高失败概率，企业家的核心技能是把风险“定价+分期+转移”。工具：小步试错（MVP）、保险、对冲、合伙分摊。论述题要区分经营风险与财务风险的叠加效应。",
            "example": "先以快闪店测选址（降风险），跑通再签长约重仓（获取回报）。",
        },
        "Incorporation": {
            "more": "法人化=注册为独立法人：有限责任、永续存在、股权可转让、融资渠道拓宽；代价：设立与合规成本、信息披露、所有权经营权分离的代理问题。独资→合伙→公司的选择题是 AL 开篇必考。",
            "example": "设计师工作室接政府大单需法人资质与投标保函——法人化的现实推力。",
        },
        "Internal growth": {
            "more": "内生增长=靠自身利润与能力扩张（开新店、新产品、新市场）。优点：稳、文化可控、风险分散推进；缺点：慢、受自有资金与人才瓶颈。与并购（external）对比的决策因素：时间窗口、标的有无、整合能力。",
            "example": "连锁每年自营新开 20 店稳步加密；为抢占异地市场则并购当地品牌一步到位。",
        },
        "Holding company": {
            "more": "控股公司通过持股控制多个子公司而不直接经营。功能：风险隔离（子公司独立法人）、税务架构、分板块上市融资；代价：多层结构的管理与披露成本、少数股东权益与关联交易争议。",
            "example": "集团总部只管资本与高管任命，各业务子公司独立负债与经营，互不担保。",
        },
        "B2B": {
            "more": "B2B 采购特征：买家少而专业、决策链长（多人/多_criteria）、金额大周期长、关系与定制权重高。营销含义：内容与解决方案销售、招投标、账期与供应链金融。与 B2C 的营销组合差异是常考对比。",
            "example": "卖工业泵的关键是总拥有成本核算与售后响应，而不是大众广告。",
        },
        "Management by objectives": {
            "more": "目标管理：上下级共同设定目标、以目标达成度考核。优点：对齐、可量化、参与感；缺点：短期导向、目标博弈、环境剧变时目标作废（需滚动修订）。德鲁克的思想源头，SMART 与 KPI 都由此演化。",
            "example": "市场部目标“年度线索量+30%”，团队自选渠道组合，季度复盘滚动调整。",
        },
        "On-the-job training": {
            "more": "在岗培训=真实工作情境中带教（师徒、轮岗、示范）。优：省钱、贴合实际、即学即用；劣：可能传递坏习惯、生产受干扰、教的人不会教。与 off-the-job（课堂/模拟）互补搭配是标准答法。",
            "example": "新柜员先跟老员工见习两周再独立上岗，差错率低于纯课堂培训。",
        },
        "Appraisal": {
            "more": "考评=定期评估表现与发展需求：绩效工资、晋升、培训计划、反馈面谈的依据。方法：特质评级（主观）→目标管理（MBO）→360°反馈。评价：指标设计不当+主管宽容/严苛偏差会毁掉公信力。",
            "example": "强制分布评级逼管理者“轮流背 C”，团队协作立刻恶化——设计缺陷案例。",
        },
        "Flat structure": {
            "more": "扁平结构=少层级宽幅度：沟通快、授权多、成本低；上限是管理者注意力和企业规模（人一多必然重新加层）。与 tall structure 对比，考“什么规模/业务适合什么形状”。",
            "example": "30 人软件公司全员一个层级直达 CEO；扩张到 300 人被迫引入中层。",
        },
        "Centralisation": {
            "more": "集权=决策集中于高层：战略一致、规模谈判力、风控强；代价是响应慢、一线能动性差、信息上传失真。分权反之。趋势是“战略集中+运营分散”的混合，数字化让总部既能集中数据又能授权一线。",
            "example": "连锁定价总部统一定框架，店长在±10% 内按商圈浮动——混合式设计。",
        },
        "Mass market": {
            "more": "大众市场：规模大、标准化、单位成本低、竞争激烈、品牌与渠道是关键成功因素；与 niche 互为反面。产品生命周期通常更长但易被颠覆（颠覆者从边缘细分切入）。d 题对比两者按“企业资源与竞争位势”下结论。",
            "example": "可乐是大众市场百年常青；精酿啤酒从利基切入逐步蚕食主流口味。",
        },
        "Product differentiation": {
            "more": "差异化=让顾客觉得你不同且值得溢价：功能、设计、品牌、服务、体验皆可为源。有效差异化的检验：顾客愿付溢价>差异成本，且竞品难以速仿。经济科的垄断竞争理论为其提供“为什么溢价可持续”的解释。",
            "example": "同配置笔记本，设计+生态+门店服务支撑 20% 溢价——差异化的货币化。",
        },
        "Sampling": {
            "more": "抽样：概率抽样（随机/系统/分层/整群）可推断总体，非概率（便利/判断/配额/滚雪球）便宜但偏差不可量化。样本量与置信度的权衡、无回答偏差是调研质量的暗坑。竞赛科的用户访谈也讲“样本不代表市场”。",
            "example": "分层抽样按地区×年龄配额，避免便利抽样“只访到商圈白领”的系统性偏差。",
        },
        "Boston matrix": {
            "more": "BCG 矩阵：市场增长率×相对份额四象限——明星/现金牛/问题/瘦狗。用法：现金牛供养明星与问题，瘦狗收割退出。批评：份额与增长非成败唯一维度、静态快照误导动态战略。与产品生命周期、Ansoff 连用。",
            "example": "主业现金牛输血新业务问题产品，两季验证失败即砍——组合管理的纪律。",
        },
        "Five forces": {
            "more": "五力：现有竞争、潜在进入、替代品、买方议价、供方议价，合力决定行业利润池。分析时写清“力从哪来+强度判断+对企业变量的影响”。局限：静态、忽略互补者与生态合作（第六力之争）。竞赛科同样列为核心工具。",
            "example": "分析航空业：进入壁垒低+替代（高铁）强+买方价格透明→行业利润薄如刀刃。",
        },
        "Force field analysis": {
            "more": "同 IB：驱动力 vs 阻碍力的现状平衡图，变革策略=加驱动/减阻碍，减阻碍通常性价比更高。AL 考试要求与 Lewin 三阶段互相映射（解冻≈减阻碍，再冻结≈固化新平衡）。",
            "example": "推行 гибкие 排班阻力是“老员工担心收入”，改保底工资后阻力消失。",
        },
        "Contingency plan": {
            "more": "应急预案=对高冲击情景预设触发条件与响应动作（供应链双源、现金压力线、公关口径）。风险管理闭环=识别→评估→应对（避免/转移/减轻/接受）→预案演练。没有触发条件的“预案”只是文档。",
            "example": "单一供应商占采购 70%：预案规定其断供 48h 内切换二供并启用安全库存。",
        },
        "Working capital cycle": {
            "more": "营运资本周期=存货天数+应收天数−应付天数，度量现金被占用的时间。每缩短一天都释放现金（=免息融资）。压缩手段：精益、赊账政策、供应链金融。数值题给三率（存货/应收/应付周转）算天数是固定题型。",
            "example": "周期从 90 天压到 60 天、日均销售 100 万→一次性释放现金 3000 万。",
        },
    },
    # ------------------------------------------------------------------ 竞赛（赛代学）
    "comp": {
        "Lean Canvas": {
            "more": "一页纸商业模式画布：问题-解决方案-独特价值主张-渠道-收入结构-成本结构-关键指标-门槛优势-客户细分。价值在于“强制回答最难的问题”（问题是否真实、门槛在哪），写完即自检商业逻辑闭环。与 BM 商业模式画布同源但更创业导向。",
            "example": "康莱德初赛材料先用 Lean Canvas 对齐团队认知，再展开成 pitch 的叙事骨架。",
        },
        "UVP": {
            "more": "独特价值主张=一句话说清“为谁、解决什么、凭什么是你”，必须具体可证伪（“高效省时”不算 UVP）。检验方法：拿掉你的品牌名，这句话还成立吗？成立=不合格（竞品也能说）。与商科的 product differentiation、定位理论直接同源。",
            "example": "“给考研党的、按遗忘曲线排期的单词本”优于“智能高效的学习工具”。",
        },
        "Unfair advantage": {
            "more": "门槛优势=别人拿钱买不走、短期学不会的东西：独家数据、社区网络效应、专利、领军人物信任。评委追问“大厂抄你怎么办”就是考这一格。没有就诚实写“暂无，通过 X 积累中”——比硬编一个更可信。",
            "example": "社区UGC菜谱库五年积累的独家内容与创作者关系，是后来者用钱堆不出的壁垒。",
        },
        "TAM/SAM/SOM": {
            "more": "市场规模的漏斗口径：TAM 全市场理论容量→SAM 可服务市场（地域/客群切分）→SOM 可获得市场（渠道与资源约束下）。常见错误是用行业报告数字当 SOM。自下而上测算（客单价×可触达客户数）比自上而下引用更被认可。",
            "example": "TAM 500 亿的行业，你的产品只服务一线城市学生（SAM 40 亿），三年渠道能力能拿到 2%（SOM 8000 万）。",
        },
        "MVP": {
            "more": "最小可行产品=用最小成本验证核心假设的版本，关键是“验证什么假设”先想清楚，MVP 不是烂版成品。可用 concierge/巫师测试等假 MVP 手法。连商科的 test marketing 与产品的概念测试。",
            "example": "想验证“愿为上门宠物美容付 3 倍价”：先人工接单+手动排期跑两周，不用先开发 App。",
        },
        "ERRC": {
            "more": "蓝海战略的消除-减少-增加-创造网格：消除行业理所当然因素、减少过度设计、增加低于行业标准处、创造全新因素。用于从红海拼杀转向价值创新，康莱德方案做差异化定位时的结构化工具。",
            "example": "廉价酒店消除大堂餐厅、减少面积，增加床位品质，创造自助入住——行业的成本结构被重写。",
        },
        "LTV": {
            "more": "客户终身价值=客户全生命周期贡献的利润（简化：客单毛利×购买频次×留存时长−获取与服务成本）。商业含义：LTV/CAC≥3 是健康线，决定“敢花多少钱获客”。与商科的顾客终身价值、NPV 折现思想同源。",
            "example": "订阅制咖啡月毛利 40 元、平均留存 18 个月→LTV 720 元，可承受 200 元获客成本。",
        },
        "CAC": {
            "more": "获客成本=营销销售总投入÷新增客户数，须含人力与工具的全口径。关键分析：分渠道 CAC（内容/投放/地推差异巨大）、与 LTV 配对看回收期。CAC 上涨而 LTV 不动是商业模式恶化的最早警报。",
            "example": "投放渠道 CAC 300 元、转介绍 30 元：把留存做好的边际收益远高于加预算。",
        },
        "Burn rate": {
            "more": "烧钱率=每月净现金流出，直接决定 runway（现金存量÷月烧钱）。分 gross/net burn：削减烧钱要区分可变（营销、活动）与刚性（工资、房租）部分。评委常问“钱能撑多久”考的就是这组数字的自洽。",
            "example": "账上 120 万、月净烧 15 万→runway 8 个月；下一轮融资必须在此前 3 个月启动。",
        },
        "STP": {
            "more": "细分-目标-定位三步法：先切分市场，再按吸引力与匹配度选择目标，最后在目标心智中占位。康莱德/BPA 的营销模块都用它把“卖给谁”讲清楚——与 AL 商科的 STP 完全同源，是赛代学的直通概念。",
            "example": "校园智能储物：细分出“考研自习人群”为目标，定位“离座不慌的安心存”。",
        },
        "SDG": {
            "more": "联合国 17 项可持续发展目标（2023 议程）是全球共同语言。康莱德评分含社会价值维度：方案对齐哪个 SDG、影响如何度量（受益人数、减排量）必须量化而非贴标签。与 IB 商科的 sustainability、经济科的发展经济学互通。",
            "example": "秸秆建材项目对齐 SDG12（负责任消费）+SDG13（气候行动），量化年减排吨数。",
        },
        "ESG": {
            "more": "环境-社会-治理三支柱的投资与企业评价框架。竞赛语境：评委用 ESG 视角审视你的方案外部性（连经济科的 externality）、劳工与治理结构。区分 ESG 评级（第三方打分）与 ESG 实践（企业动作）。",
            "example": "方案写明供应商劳工审计与董事会设 ESG 委员会——治理支柱落到可核查动作。",
        },
        "Five forces": {
            "more": "竞赛版五力与 AL 商科同源：用于论证“你所在的赛道利润池是否值得进、你的位置是否守得住”。写法要点：每条力给出强度判断+证据（哪怕是访谈与二手数据），最后落到对你的定价与渠道的含义。",
            "example": "校园二手教材平台：替代品（二手群）极强是最大威胁→对策是做成官方化验真服务。",
        },
        "Pitch Deck": {
            "more": "路演幻灯片的经典骨架：问题-方案-市场-商业模式-竞争-团队-财务-融资诉求。评审逻辑=每页回答评委的一个疑问，证据密度>美观度。常见死因：技术自嗨、市场数字引用不当、财务预测无假设。",
            "example": "10 页 deck 每页一个论点一句证据，比 30 页功能罗列的通过率高一个量级。",
        },
        "Problem-solution fit": {
            "more": "问题-解决方案契合=确认“问题真实、痛到愿意付钱、你的方案能缓解”，发生在大规模开发之前。验证工具：问题访谈（过去行为而非未来意愿）、假门测试。未过此关就烧钱开发是创业死亡之首。",
            "example": "访谈 30 人中 24 人上月为该问题花过钱或时间——用行为而非“我会用”证明 fit。",
        },
        "Product-market fit": {
            "more": "产品-市场契合=产品已满足市场需求的信号：留存曲线走平、口碑自传播、供不应求。判断标志（超预期增长、用户主动推荐）比主观感觉可靠。达到 PMF 前重学习迭代、达到后重扩张效率——节奏错配烧掉无数公司。",
            "example": "次月留存稳定在 45% 且 30% 新客来自老客推荐——PMF 信号，可以踩油门。",
        },
        "Pivot": {
            "more": "转向=基于验证证据的战略级调整（客群、渠道、问题或方案），不是随机换赛道。可辨识的 pivot 信号：访谈反复指向相邻问题、某渠道 CAC 异常低、某功能使用率一枝独秀。记录“假设-证据-调整”链条让 pivot 看起来是科学而非逃跑。",
            "example": "团队笔记 App 发现用户只用“打卡分享”功能→pivot 成学习打卡社区，增长重启。",
        },
        "Bootstrapping": {
            "more": "自举=不靠外部投资、用收入与极低成本运营，逼迫单位经济模型（LTV/CAC）先跑正。优点：股权完整、方向自主；代价：增长慢、抗风险弱。与融资路线是选择题而非优劣题——看赛道的赢家通吃程度。",
            "example": "设计工作室用企业定制单养自研 SaaS，两年后产品收入过半再考虑融资。",
        },
        "Valuation": {
            "more": "估值=公司在某时点的价值判定：早期常用可比法（同轮次同赛道）与 Berkus/记分卡，成熟期用 DCF（连 NPV 思想）。融资额÷出让比例的反推要自洽于里程碑与 runway。评委挑战的常是“估值依据”而非数字本身。",
            "example": "融 300 万出让 15%（投后 2000 万）：要能说明这笔钱恰好够把产品做到下一阶段的验证里程碑。",
        },
    },
}

# ---------------------------------------------------------------------- 跨科目桥梁
# members 中的 term_en 必须与各科 glossary 完全一致；whole=上位概念；
# prereq=先决条件说明（是什么的前置）。
BRIDGES = [
    {"id": "scarcity", "label": "稀缺与选择", "whole": "经济学的底层出发点：一切选择皆有机会成本",
     "prereq": "所有经济与商业决策论述的地基；PPC、成本、融资选择题都以它为前提",
     "members": [("ib-econ", "Scarcity"), ("ib-econ", "Opportunity cost"), ("ib-econ", "Factors of production"),
                 ("ib-econ", "Ceteris paribus"), ("ib-econ", "Economic goods"), ("ib-econ", "Free goods"),
                 ("al-econ", "Scarcity"), ("al-econ", "Opportunity cost"), ("al-econ", "Economic goods"),
                 ("al-econ", "Free goods"), ("al-econ", "Production possibility curve"),
                 ("al-econ", "Division of labour"), ("al-econ", "Ceteris paribus"),
                 ("igcse-bus", "Opportunity cost"), ("igcse-bus", "Division of labour")]},
    {"id": "supply-demand", "label": "供需与价格机制", "whole": "微观市场分析的核心框架（属于市场如何配置资源这一大问题）",
     "prereq": "价格管制、税收归宿、补贴、汇率与宏观 AD 分析的共同前提",
     "members": [("ib-econ", "Demand"), ("ib-econ", "Law of demand"), ("ib-econ", "Supply"), ("ib-econ", "Market equilibrium"),
                 ("ib-econ", "Price mechanism"), ("ib-econ", "Consumer surplus"), ("ib-econ", "Producer surplus"),
                 ("ib-econ", "Allocative efficiency"),
                 ("al-econ", "Movement along the curve"), ("al-econ", "Shift of the curve"),
                 ("al-econ", "Price mechanism"), ("al-econ", "Rationing function"), ("al-econ", "Signal function"),
                 ("al-econ", "Consumer surplus"), ("al-econ", "Producer surplus"), ("al-econ", "Allocative efficiency"),
                 ("al-econ", "Marginal utility"), ("al-econ", "Equi-marginal principle")]},
    {"id": "elasticity", "label": "弹性家族", "whole": "量化需求/供给对价格与收入变化的敏感度",
     "prereq": "税收归宿、企业定价策略、贬值改善贸易收支（马歇尔-勒纳）论证的先决条件",
     "members": [("ib-econ", "Price elasticity of demand"), ("ib-econ", "Income elasticity of demand"),
                 ("ib-econ", "Cross-price elasticity of demand"), ("ib-econ", "Price elasticity of supply"),
                 ("al-econ", "PED"), ("al-econ", "XED"), ("al-econ", "YED"), ("al-econ", "PES"),
                 ("al-econ", "Marshall-Lerner condition"),
                 ("al-bus", "Price elasticity (marketing)"), ("comp", "LTV"), ("comp", "CAC")]},
    {"id": "gov-intervention", "label": "政府直接干预", "whole": "市场失灵后的政策工具箱（属于政府与市场关系这一主题）",
     "prereq": "供需图+弹性是评价这些工具福利效果的前提",
     "members": [("ib-econ", "Indirect tax"), ("ib-econ", "Subsidy"), ("ib-econ", "Price ceiling"), ("ib-econ", "Price floor"),
                 ("al-econ", "Ad valorem tax"), ("al-econ", "Pigouvian tax"), ("al-econ", "Buffer stock scheme"),
                 ("al-econ", "Deadweight loss")]},
    {"id": "market-failure", "label": "外部性与市场失灵", "whole": "政府干预的微观依据",
     "prereq": "讨论任何环境/公共健康/规制政策题的出发点",
     "members": [("ib-econ", "Market failure"), ("ib-econ", "Externality"), ("ib-econ", "Negative externality of production"),
                 ("ib-econ", "Negative externality of consumption"), ("ib-econ", "Positive externality"),
                 ("ib-econ", "Merit goods"), ("ib-econ", "Demerit goods"), ("ib-econ", "Public goods"),
                 ("ib-econ", "Free-rider problem"), ("ib-econ", "Common pool resources"),
                 ("ib-econ", "Asymmetric information"), ("ib-econ", "Adverse selection"), ("ib-econ", "Moral hazard"),
                 ("al-econ", "Externality"), ("al-econ", "Public goods"), ("al-econ", "Merit good"), ("al-econ", "Demerit good"),
                 ("al-econ", "Information asymmetry"), ("al-econ", "Cap-and-trade"),
                 ("comp", "SDG"), ("comp", "ESG")]},
    {"id": "market-structure", "label": "市场结构与竞争", "whole": "产业组织分析：市场势力从哪来、效率代价多大",
     "prereq": "竞争政策、并购审查、定价策略题的框架",
     "members": [("ib-econ", "Market power"), ("ib-econ", "Monopoly"), ("ib-econ", "Oligopoly"), ("ib-econ", "Barriers to entry"),
                 ("al-econ", "Monopoly"), ("al-econ", "Natural monopoly"), ("al-econ", "Price discrimination"),
                 ("al-econ", "Concentration ratio"), ("al-econ", "Cartel"), ("al-econ", "Non-price competition"),
                 ("al-econ", "Limit pricing"), ("al-econ", "Nationalisation"),
                 ("al-bus", "Five forces"), ("al-bus", "Porter's generic strategies"), ("comp", "Five forces"),
                 ("al-bus", "Product differentiation"), ("comp", "Unfair advantage"), ("comp", "IP defensibility")]},
    {"id": "costs-econ", "label": "成本、产量与利润（经济科）", "whole": "企业理论与生产决策",
     "prereq": "成本结构理解是盈亏平衡（商科）与供给曲线推导的共同前提",
     "members": [("al-econ", "Fixed cost"), ("al-econ", "Variable cost"), ("al-econ", "Marginal product"),
                 ("al-econ", "Law of diminishing returns"), ("al-econ", "Economies of scale"), ("al-econ", "Diseconomies of scale"),
                 ("al-econ", "Total revenue"), ("al-econ", "Normal profit"), ("al-econ", "Abnormal profit"),
                 ("al-econ", "Shut-down point"), ("al-econ", "Productive efficiency"), ("al-econ", "Dynamic efficiency"),
                 ("igcse-bus", "Economies of scale"), ("ib-bus", "Capacity utilization"), ("al-bus", "Capacity utilisation")]},
    {"id": "labour-econ", "label": "劳动市场", "whole": "要素市场分析（HL/AL）",
     "prereq": "MRP 与派生需求是理解最低工资、工会与自动化影响的钥匙",
     "members": [("al-econ", "MRP"), ("al-econ", "Derived demand"), ("al-econ", "Monopsony"),
                 ("igcse-bus", "Trade union"), ("ib-bus", "Labour turnover")]},
    {"id": "macro-goals", "label": "宏观经济目标与波动", "whole": "宏观分析：总量、周期与政策目标",
     "prereq": "AD/AS 图是判断政策方向的前提；商科的 PEST/STEEPLE 经济维度直接引用这些指标",
     "members": [("ib-econ", "Gross Domestic Product"), ("ib-econ", "Gross National Income"), ("ib-econ", "Real vs nominal GDP"),
                 ("ib-econ", "Circular flow of income"), ("ib-econ", "Aggregate demand"), ("ib-econ", "Aggregate supply"),
                 ("ib-econ", "Business cycle"), ("ib-econ", "Short-run"), ("ib-econ", "Long-run"),
                 ("ib-econ", "Inflation"), ("ib-econ", "Deflation"), ("ib-econ", "Inflation rate"),
                 ("ib-econ", "Unemployment"), ("ib-econ", "Economic growth"), ("ib-econ", "Productive capacity"),
                 ("al-econ", "Aggregate demand"), ("al-econ", "Demand-pull inflation"), ("al-econ", "Cost-push inflation"),
                 ("al-econ", "Phillips curve"), ("al-econ", "Frictional unemployment"), ("al-econ", "Structural unemployment"),
                 ("al-econ", "Cyclical unemployment"), ("al-econ", "Multiplier"),
                 ("igcse-bus", "Recession"), ("igcse-bus", "Inflation")]},
    {"id": "macro-policy", "label": "宏观政策工具", "whole": "需求管理与供给侧管理",
     "prereq": "先会判别通胀/失业类型，才能选对政策组合",
     "members": [("ib-econ", "Monetary policy"), ("ib-econ", "Fiscal policy"), ("ib-econ", "Supply-side policy"),
                 ("ib-econ", "Interest rate"), ("ib-econ", "Central bank"), ("ib-econ", "Taxation"),
                 ("ib-econ", "Government spending"), ("ib-econ", "Budget deficit"),
                 ("al-econ", "Progressive tax"), ("al-econ", "Crowding out"), ("al-econ", "Quantitative easing"),
                 ("ib-econ", "Redistribution of income"), ("igcse-bus", "Privatisation"), ("igcse-bus", "Mixed economy")]},
    {"id": "inequality", "label": "分配与公平", "whole": "效率-公平权衡分析",
     "prereq": "基尼/洛伦兹读图是评价再分配政策的前提",
     "members": [("ib-econ", "Equity"), ("ib-econ", "Equality"), ("ib-econ", "Lorenz curve"),
                 ("ib-econ", "Gini coefficient"), ("ib-econ", "Income inequality"), ("ib-econ", "Poverty"),
                 ("ib-econ", "Poverty trap"), ("al-econ", "Gini coefficient")]},
    {"id": "trade", "label": "国际贸易与汇率", "whole": "开放经济分析",
     "prereq": "比较优势计算是贸易保护评价题的前提；汇率传导链是商科进出口损益分析的前提",
     "members": [("ib-econ", "Absolute advantage"), ("ib-econ", "Comparative advantage"), ("ib-econ", "Free trade"),
                 ("ib-econ", "Tariff"), ("ib-econ", "Quota"), ("ib-econ", "Trade protection"), ("ib-econ", "Infant industry"),
                 ("ib-econ", "Trade deficit"), ("ib-econ", "Trade surplus"), ("ib-econ", "Current account"),
                 ("ib-econ", "Balance of payments"), ("ib-econ", "Exchange rate"), ("ib-econ", "Appreciation"),
                 ("ib-econ", "Depreciation"),
                 ("al-econ", "Absolute advantage"), ("al-econ", "Comparative advantage"), ("al-econ", "Quota"),
                 ("al-econ", "Terms of trade"), ("al-econ", "Marshall-Lerner condition"), ("al-econ", "Fixed exchange rate"),
                 ("al-econ", "Revaluation"), ("al-econ", "Financial account"), ("al-econ", "Purchasing power parity"),
                 ("igcse-bus", "Exchange rate"), ("igcse-bus", "Globalisation"), ("igcse-bus", "Multinational"),
                 ("ib-bus", "Depreciation"), ("ib-bus", "Glocalization")]},
    {"id": "integration", "label": "区域经济一体化", "whole": "贸易制度的深度安排（ib-econ 专属层级）",
     "members": [("ib-econ", "Economic integration"), ("ib-econ", "Free trade area"), ("ib-econ", "Customs union"),
                 ("ib-econ", "Common market"), ("ib-econ", "Monetary union")]},
    {"id": "development", "label": "发展经济学", "whole": "增长之外：发展质量与可持续",
     "prereq": "区分 growth 与 development 是发展类论文的第一步",
     "members": [("ib-econ", "Sustainable development"), ("ib-econ", "Sustainability"), ("ib-econ", "Economic development"),
                 ("ib-econ", "Human Development Index"), ("ib-econ", "Foreign direct investment"),
                 ("ib-econ", "Official development assistance"), ("ib-econ", "Multinational corporation"),
                 ("al-econ", "HDI"), ("al-econ", "Microfinance"), ("al-econ", "Foreign aid"),
                 ("igcse-bus", "Sustainability"), ("comp", "SDG")]},
    {"id": "methodology", "label": "经济学方法论", "whole": "学科如何形成知识",
     "members": [("ib-econ", "Positive economics"), ("ib-econ", "Normative economics"), ("ib-econ", "Economic model"),
                 ("ib-econ", "Rational choice"), ("ib-econ", "Behavioural economics"),
                 ("al-econ", "Positive statement"), ("al-econ", "Normative statement")]},
    {"id": "business-entity", "label": "企业形态与成长", "whole": "商业组织与扩张路径",
     "prereq": "有限责任概念是理解公司融资（发股发债）的前提",
     "members": [("igcse-bus", "Limited liability"), ("igcse-bus", "Franchise"), ("igcse-bus", "Joint venture"),
                 ("igcse-bus", "Merger"), ("igcse-bus", "Takeover"),
                 ("ib-bus", "Limited liability"), ("ib-bus", "Added value"), ("ib-bus", "Horizontal integration"),
                 ("ib-bus", "Vertical integration"), ("ib-bus", "Conglomerate"), ("ib-bus", "Strategic alliance"),
                 ("ib-bus", "Outsourcing"),
                 ("al-bus", "Franchise"), ("al-bus", "M&A"), ("al-bus", "Takeover"), ("al-bus", "Holding company"),
                 ("al-bus", "Internal growth"), ("al-bus", "Incorporation"), ("al-bus", "Franchisee"),
                 ("al-bus", "Entrepreneur"), ("al-bus", "Risk vs reward"), ("al-bus", "Unlimited liability"),
                 ("igcse-bus", "Added value"),
                 ("comp", "Lean Canvas"), ("comp", "BMC"), ("comp", "Pivot"), ("comp", "Bootstrapping")]},
    {"id": "objectives", "label": "企业目标与治理", "whole": "为谁经营、追求什么",
     "members": [("ib-bus", "SMART objectives"), ("ib-bus", "Mission statement"), ("ib-bus", "Tactical objectives"),
                 ("ib-bus", "Private sector"), ("ib-bus", "Public sector"), ("ib-bus", "Non-profit"),
                 ("al-bus", "Survival objective"), ("al-bus", "Management by objectives")]},
    {"id": "stakeholders", "label": "利益相关者与外部环境", "whole": "企业与其影响网络",
     "prereq": "STEEPLE/PEST 扫描输出（OT）是 SWOT 的输入",
     "members": [("igcse-bus", "Stakeholder"), ("igcse-bus", "Pressure group"), ("igcse-bus", "Consumer protection"),
                 ("ib-bus", "Stakeholder"), ("ib-bus", "STEEPLE"), ("ib-bus", "Ethics"), ("ib-bus", "Sustainability"),
                 ("ib-bus", "Pressure group"), ("al-bus", "PEST analysis"), ("comp", "ESG")]},
    {"id": "marketing", "label": "营销组合与定价", "whole": "4P/7P 框架：把价值送达顾客",
     "prereq": "市场细分与调研结果（STP）是设计营销组合的先决输入",
     "members": [("igcse-bus", "Niche market"), ("igcse-bus", "Market orientation"), ("igcse-bus", "Product life cycle"),
                 ("igcse-bus", "Extension strategy"), ("igcse-bus", "Penetration pricing"), ("igcse-bus", "Price skimming"),
                 ("igcse-bus", "Above-the-line"), ("igcse-bus", "Below-the-line"), ("igcse-bus", "Distribution channel"),
                 ("igcse-bus", "E-commerce"),
                 ("ib-bus", "Marketing mix"), ("ib-bus", "Price skimming"), ("ib-bus", "Penetration pricing"),
                 ("ib-bus", "AIDA"), ("ib-bus", "Cost-plus pricing"), ("ib-bus", "Loss leader"),
                 ("ib-bus", "Promotional pricing"), ("ib-bus", "Above-the-line promotion"),
                 ("ib-bus", "Below-the-line promotion"), ("ib-bus", "Viral marketing"), ("ib-bus", "Distribution channel"),
                 ("ib-bus", "E-commerce"), ("ib-bus", "Extension strategy"), ("ib-bus", "Brand loyalty"),
                 ("ib-bus", "Niche market"), ("ib-bus", "Market share"),
                 ("al-bus", "IMC"), ("al-bus", "Extension strategy"), ("al-bus", "Competitive pricing"),
                 ("al-bus", "Sales promotion"), ("al-bus", "Public relations"), ("al-bus", "Direct marketing"),
                 ("al-bus", "Product differentiation"), ("al-bus", "Brand image"), ("al-bus", "Mass market"),
                 ("al-bus", "Market segmentation"), ("al-bus", "B2B"),
                 ("comp", "STP"), ("comp", "UVP")]},
    {"id": "market-research", "label": "市场调研与证据", "whole": "以证据支撑营销与产品决策",
     "prereq": "调研结果是 STP、UVP 与产品路线图的输入；竞赛的 problem-solution fit 靠它验证",
     "members": [("igcse-bus", "Primary research"), ("ib-bus", "Secondary research"), ("ib-bus", "Quantitative data"),
                 ("ib-bus", "Qualitative data"), ("al-bus", "Sampling"),
                 ("comp", "Verification"), ("comp", "Market insight"), ("comp", "TAM/SAM/SOM"),
                 ("comp", "Problem-solution fit"), ("comp", "Product-market fit"), ("comp", "Proof of concept"),
                 ("comp", "MVP"), ("comp", "Pivot")]},
    {"id": "hr-org", "label": "组织与人力资源", "whole": "组织行为学：结构、领导、激励",
     "prereq": "激励理论（Maslow/Herzberg）是设计薪酬与授权方案的前提",
     "members": [("igcse-bus", "Job description"), ("igcse-bus", "Redundancy"), ("igcse-bus", "Dismissal"),
                 ("igcse-bus", "Maslow's hierarchy"), ("igcse-bus", "Herzberg two-factor"), ("igcse-bus", "Job enrichment"),
                 ("igcse-bus", "Span of control"), ("igcse-bus", "Delegation"),
                 ("ib-bus", "Herzberg"), ("ib-bus", "Laissez-faire"), ("ib-bus", "Paternalistic"),
                 ("ib-bus", "Emotional intelligence"), ("ib-bus", "Piece rate"), ("ib-bus", "Profit sharing"),
                 ("ib-bus", "Job enrichment"), ("ib-bus", "Empowerment"), ("ib-bus", "Matrix structure"),
                 ("ib-bus", "Delayering"), ("ib-bus", "Chain of command"), ("ib-bus", "Conciliation"),
                 ("al-bus", "Span of control"), ("al-bus", "On-the-job training"), ("al-bus", "Appraisal"),
                 ("al-bus", "Dismissal"), ("al-bus", "Job rotation"), ("al-bus", "Flat structure"), ("al-bus", "Centralisation")]},
    {"id": "change", "label": "变革管理", "whole": "组织如何从现状迁移到目标状态",
     "members": [("ib-bus", "Force field analysis"), ("al-bus", "Force field analysis"), ("al-bus", "Lewin's change model"),
                 ("al-bus", "Contingency plan")]},
    {"id": "strategy", "label": "战略工具箱", "whole": "公司层与业务层战略分析",
     "prereq": "五力/PEST 的输出是 SWOT 与 Ansoff 决策的输入",
     "members": [("ib-bus", "Ansoff matrix"), ("al-bus", "PEST analysis"), ("al-bus", "Porter's generic strategies"),
                 ("al-bus", "Core competences"), ("al-bus", "Five forces"), ("al-bus", "Boston matrix"),
                 ("comp", "Five forces"), ("comp", "WSAP"), ("comp", "ERRC")]},
    {"id": "ops", "label": "运营与质量", "whole": "把投入转化为产出的方式",
     "prereq": "固定/变动成本区分是精益收益量化的前提",
     "members": [("igcse-bus", "Batch production"), ("igcse-bus", "Lean production"), ("igcse-bus", "JIT"),
                 ("igcse-bus", "Quality assurance"),
                 ("ib-bus", "Lean production"), ("ib-bus", "TQM"), ("ib-bus", "Kaizen"), ("ib-bus", "Productivity"),
                 ("ib-bus", "Quality control"), ("ib-bus", "Quality assurance"), ("ib-bus", "Just-in-case stock"),
                 ("al-bus", "Lean production"), ("al-bus", "JIT"), ("al-bus", "Job production"), ("al-bus", "Flow production"),
                 ("al-bus", "Buffer stock"), ("al-bus", "Lead time")]},
    {"id": "bep", "label": "盈亏平衡与本量利", "whole": "成本-产量-利润分析（CVP）",
     "prereq": "固定/变动成本与贡献的概念是 BEP 计算与画图的先决条件",
     "members": [("igcse-bus", "Break-even"), ("igcse-bus", "Margin of safety"), ("igcse-bus", "Contribution"),
                 ("ib-bus", "Break-even point"), ("ib-bus", "Margin of safety")]},
    {"id": "finance-stmt", "label": "财务报表与利润", "whole": "企业经营成果的货币刻画",
     "members": [("igcse-bus", "Gross profit"), ("igcse-bus", "Retained profit"), ("igcse-bus", "Net assets"),
                 ("igcse-bus", "Current asset"), ("igcse-bus", "Working capital"),
                 ("ib-bus", "Gross profit"), ("ib-bus", "Net profit"), ("ib-bus", "Retained profit"),
                 ("ib-bus", "Working capital"), ("al-bus", "Gross profit margin")]},
    {"id": "ratios", "label": "财务比率分析", "whole": "盈利性/流动性/效率的三维体检",
     "prereq": "报表结构理解是比率计算与解读的前提",
     "members": [("igcse-bus", "ROCE"), ("igcse-bus", "Acid test"),
                 ("ib-bus", "ROCE"), ("ib-bus", "Current ratio"), ("ib-bus", "Acid test ratio"), ("ib-bus", "Gearing"),
                 ("ib-bus", "Stock turnover"), ("ib-bus", "Debtor days"), ("ib-bus", "Variance analysis"),
                 ("al-bus", "ROCE"), ("al-bus", "ARR"), ("al-bus", "Creditor days")]},
    {"id": "cash-funding", "label": "现金流与融资", "whole": "企业的血液与输血渠道",
     "prereq": "现金流预测的质量决定投资评估（ARR/NPV）结论的可信度；利润≠现金是第一道认知坎",
     "members": [("igcse-bus", "Cash flow forecast"), ("igcse-bus", "Overdraft"), ("igcse-bus", "Trade credit"),
                 ("igcse-bus", "Venture capital"), ("igcse-bus", "Micro-finance"), ("igcse-bus", "Working capital"),
                 ("ib-bus", "Overdraft"), ("ib-bus", "Trade credit"), ("ib-bus", "Venture capital"),
                 ("ib-bus", "Crowdfunding"), ("ib-bus", "Debenture"), ("ib-bus", "Retained profit"),
                 ("al-bus", "Hire purchase"), ("al-bus", "Business angel"), ("al-bus", "Working capital cycle"),
                 ("comp", "Burn rate"), ("comp", "Runway"), ("comp", "Bootstrapping")]},
    {"id": "investment", "label": "投资评估与估值", "whole": "跨期现金流的价值判断",
     "prereq": "现金流预测与货币时间价值概念是 NPV/ARR/LTV 的共同前提",
     "members": [("ib-bus", "NPV"), ("al-bus", "ARR"), ("comp", "NPV"), ("comp", "LTV"), ("comp", "CAC"),
                 ("comp", "Valuation"), ("comp", "Revenue projections"), ("comp", "Budget reasonableness"),
                 ("comp", "Investor appeal")]},
    {"id": "comp-pitch", "label": "竞赛交付物", "whole": "康莱德/BPA 的表达层：把分析讲成故事",
     "members": [("comp", "Lean Canvas"), ("comp", "UVP"), ("comp", "TAM/SAM/SOM"), ("comp", "Pitch Deck"),
                 ("comp", "Elevator pitch"), ("comp", "Narrative structure"), ("comp", "Market insight"),
                 ("comp", "Entry & adoption"), ("comp", "Engagement channels"), ("comp", "Investor appeal")]},
]

# 竞赛科里无 ENRICH 之外还需要的补充说明（表述层概念多为方法词）
_LINK_TYPE_LABEL = {"same": "同概念", "related": "相关", "prereq": "前置", "part": "上位"}


def _econ_enrich():
    from content_glossary_econ import ENRICH_ECON
    return ENRICH_ECON


def all_enrich():
    """合并两份手写详解，返回 {subject_id: {term_en: {...}}}。"""
    out = {}
    for sid, d in _econ_enrich().items():
        out.setdefault(sid, {}).update(d)
    for sid, d in ENRICH_BUS.items():
        out.setdefault(sid, {}).update(d)
    return out


def all_glossaries():
    """{sid: [terms]} — 六个科目的完整术语表（基础+扩充），供桥梁计算与装配复用。"""
    import content
    import content_subjects
    import content_deep
    import content_igcse
    g = {"ib-econ": content.GLOSSARY, "igcse-bus": content_igcse.IGCSE_BUS["glossary"]}
    for s in content_subjects.SUBJECTS:
        g[s["id"]] = s["glossary"] + content_deep.GLOSSARY_EXTRA.get(s["id"], [])
    return g


def enrich_ib_econ(topic_by_id):
    """Convenience wrapper for analyze.py: ib-econ glossary with full enrichment."""
    gloss = all_glossaries()
    links, meta, _invalid = build_bridges(gloss)
    ctx = {"topic_by_id": topic_by_id, "bridge_links": links, "bridge_meta": meta}
    return enrich_subject_terms("ib-econ", gloss["ib-econ"], ctx)


def build_bridges(glossaries):
    """按 glossaries（{sid:[terms]}）解析 BRIDGES，返回：
    links   : {sid: {term_en: [ {"type","subj","term","note"} ]}}  跨科同概念链接
    meta    : {sid: {term_en: {"part_of","prereq","cluster"}}}
    invalid : [(sid, term_en)] 引用了不存在术语的成员
    """
    have = {sid: {t["term_en"] for t in terms} for sid, terms in glossaries.items()}
    links, meta, invalid = {}, {}, []
    for b in BRIDGES:
        valid = [(s, t) for (s, t) in b["members"] if s in have and t in have[s]]
        for (s, t) in b["members"]:
            if (s, t) not in valid:
                invalid.append((s, t))
        for (s, t) in valid:
            # 大簇不做全连接网格：每个术语只链到"其他科目"的最多 3 个代表词
            arr = links.setdefault(s, {}).setdefault(t, [])
            by_subj = {}
            for (s2, t2) in valid:
                if s2 != s:
                    by_subj.setdefault(s2, []).append(t2)
            for s2, names in by_subj.items():
                for t2 in names[:3]:
                    arr.append({"type": "same", "subj": s2, "term": t2, "note": b["label"]})
            meta.setdefault(s, {}).setdefault(t, {})
            meta[s][t].setdefault("part_of", b.get("whole"))
            if b.get("prereq"):
                prev = meta[s][t].get("prereq")
                meta[s][t]["prereq"] = b["prereq"] if not prev else prev + "；" + b["prereq"]
            meta[s][t].setdefault("cluster", b["label"])
    return links, meta, invalid


def enrich_subject_terms(sid, terms, ctx=None):
    """给一科 glossary 注入 more/example/links/part_of/prereq。
    ctx = {"topic_by_id": {tid: {"title": str, "unit": str}},
           "related": {tid: [tid...]}, "mapping": {tid: [concept_zh...]}, "freq": {tid: int}}
    无手写 more 的术语用 ctx 组装结构性保底解释。
    """
    ctx = ctx or {}
    enrich = all_enrich().get(sid, {})
    glossaries = {sid: terms}  # 单科时桥梁信息在调用方先算好再传入更高效
    # 期望调用方传入 bridge_links/bridge_meta
    bl = ctx.get("bridge_links", {}).get(sid, {})
    bm = ctx.get("bridge_meta", {}).get(sid, {})
    tby = {g["term_en"]: g for g in terms}
    out = []
    for g in terms:
        t2 = dict(g)
        e = enrich.get(g["term_en"], {})
        more, example = e.get("more"), e.get("example")
        if not more:
            bits = []
            tip = ctx.get("topic_by_id", {}).get(g.get("topic"))
            if tip:
                bits.append(f"属于「{tip['unit']} · {tip['title']}」的核心概念。")
            rel = ctx.get("related", {}).get(g.get("topic")) or []
            if rel:
                names = []
                for r in rel[:3]:
                    rt = ctx.get("topic_by_id", {}).get(r)
                    if rt:
                        names.append(rt["title"])
                if names:
                    bits.append(f"常与 {'、'.join(names)} 联动出题。")
            mp = ctx.get("mapping", {}).get(g.get("topic")) or []
            if mp:
                bits.append(f"竞赛应用（以赛代学）：{ '、'.join(mp[:3]) }。")
            fq = ctx.get("freq", {}).get(g.get("topic"))
            if fq:
                bits.append(f"真题考频：{fq} 卷。")
            if bm.get(g["term_en"], {}).get("part_of"):
                bits.append(f"它是「{bm[g['term_en']]['part_of']}」这一更大概念的一部分。")
            if bm.get(g["term_en"], {}).get("prereq"):
                bits.append(f"先决条件：{bm[g['term_en']]['prereq']}。")
            if bits:
                more = "".join(bits)
        if more:
            t2["more"] = more
        if example:
            t2["example"] = example
        if bl.get(g["term_en"]):
            t2["links"] = bl[g["term_en"]]
        if bm.get(g["term_en"], {}).get("part_of"):
            t2["part_of"] = bm[g["term_en"]]["part_of"]
        if bm.get(g["term_en"], {}).get("prereq"):
            t2["prereq"] = bm[g["term_en"]]["prereq"]
        if bm.get(g["term_en"], {}).get("cluster"):
            t2["cluster"] = bm[g["term_en"]]["cluster"]
        out.append(t2)
    return out
