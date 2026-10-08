---
name: tact-ecosystem-interface
description: TACT 三轴坐标分类法的生态接口资产包：跨地图（TACT↔OWASP/NIST/ATLAS/EU AI Act/OWASP Agentic 2026 双向映射）、EU AI Act 义务映射、元标签分级层。当需要把 TACT 坐标翻译成行业框架条目、查 EU 法律义务条文、或给坐标补严重度/可检测性/镜像等元标签时使用。坐标体系以 tact-three-axis-check（117 坐标）为准。
cross_skill_refs:
  - references/coordinate_data.json
---

# TACT 生态接口（tact-ecosystem-interface）

## 定位

本 skill 不是独立分类引擎，是 tact-three-axis-check（过闸引擎）的**外部接口资产包**。坐标 code（如 M2-2、M6-6）以 tact-three-axis-check 的 `references/coordinate_data.json` 为准——注意该文件位于**兄弟技能目录 `tact-three-axis-check/references/coordinate_data.json`**，不在本技能自身的 `references` 下；判据与过闸流程也在主 skill，本 skill 不重复。

## 资产清单

| 文件 | 内容 | 何时读取 |
|---|---|---|
| `references/crosswalk_four_frameworks.json` | TACT↔五大框架双向映射（OWASP LLM / NIST / EU AI Act / ATLAS / OWASP Agentic 2026；正向 48 项 + 反向 32 项） | 命中坐标后需要行业名/框架引用时 |
| `references/eu_ai_act_obligations.json` | 坐标→EU AI Act 义务条文+落地动作（正向 14 项 + 反向自查 + 合规清单） | 涉欧盟高风险场景/合规自查时 |
| `references/tact_meta_tags.json` | 7 维元标签（严重度/可检测性/攻击面/镜像/状态/语义域/证据强度） | 需要分级、排序、镜像对照或给坐标补标注时 |
| `references/agentic_coverage_gap.md` | OWASP Agentic 2026 覆盖查缺清单（覆盖状态 + M9 待 ratify 缺口 + 社区协作入口） | 涉 Agent 应用风险映射/查缺、社区案例征集时 |

## 用法流程（过闸后）

1. **查跨地图**：命中坐标 → crosswalk 正向表找行业条目（行业→坐标）或反向表找框架引用（坐标→行业名）。对外引用前先看该条目的 `status` 字段：`verified` 可引用，`hypothesis` 必须标注"待验证"。**坐标查无 → 标注"暂无映射"，不强行对应**。
2. **查义务**：涉欧盟部署或医疗高风险场景 → 读 `eu_ai_act_obligations.json`：坐标→条文→落地动作；命中 `severity=S1` 的坐标自动进 Art. 73 严重事故上报流程（参见元标签）。
3. **补元标签**：`tact_meta_tags.json` 分 5 区——`schema`（7 维定义）/ `mirrors`（18 对镜像）/ `status_annotations`（预测格与预测族）/ `domain_symbol`（符号域 8 坐标）/ `examples`（仅 10 个高频坐标完整标注，**不是全量**）。给未标注坐标补元标签时按 schema 7 维填写；证据不足用 `evidence_strength=E0/E1` 并标记"待验证"，不得虚报案例数。**该坐标无完整标签 → 标注"元标签待补"，不默认缺省值**。

## 纪律（护栏）

- **版本绑定**：三张表绑定 TACT v2.7.8 与框架版本（OWASP Top 10 for LLM 2025 / NIST AI 600-1 / EU AI Act 2024/1689 / ATLAS 2026 / OWASP Agentic Applications 2026）。主数据升版后，映射必须重新核验再沿用；版本不匹配时禁止直接引用映射。
- **数据结构**：`crosswalk_four_frameworks.json` 的 `forward` 为按框架（OWASP/NIST/EU_AI_ACT/ATLAS/AGENTIC）分组的 dict，`reverse` 为扁平 list；同一文件内两种形状是既有设计，读取时按形状处理，勿假设同构。
- **核验状态**：每条映射带 `status` 字段：`verified`=有案例支撑（可引用）；`hypothesis`=待验证假设（引用时须标注"待验证"）；`verified_refused`=治理域正确拒绝（如 EU05/EU08/AT07，该条目在 TACT 无坐标，引用时声明"治理域"，不视为坐标命中）。hypothesis 与 verified_refused 均不视为已核验事实。
- **示例级标注**：`tact_meta_tags.json` 仅 10 个高频坐标完整标注，其余坐标元标签为 `null` 待补。使用前先查该坐标是否有完整元标签，不得默认全量已标。
- **不新增坐标**：本 skill 只提供接口与标注，不添加任何 L/M/P 子坐标；坐标增删走 tact-three-axis-check 的演进规则（两条互不相干真实案例 + 结构校验）。
- **映射不是结论**：跨地图映射是"带判据的翻译假设"，义务映射是"触发线索"——坐标命中不等于违反法律义务，需对照性能基准与条文原文判断。
