# Agentic 覆盖查缺清单（OWASP Agentic Applications 2026 ↔ TACT 坐标库）

> 绑定：TACT v2.7.8 · OWASP Top 10 for Agentic Applications 2026
> 目的：记录"OWASP Agentic 2026 十项风险"在 TACT 坐标库中的映射覆盖情况，区分【已覆盖 / 部分覆盖 / 缺口】；缺口如实声明，**不造码、不走捷径**，按坐标库演进规则（两条互不相干真实案例 → ratify）处理。
> 对应跨地图：`references/crosswalk_four_frameworks.json` 的 `forward.AGENTIC`（正向 10 项）+ `reverse`（坐标→AGENTIC）。

## 一、覆盖对照总表

| OWASP Agentic 2026 | 风险名（英） | TACT 映射坐标 | 覆盖状态 | 说明 |
|---|---|---|---|---|
| ASI01 | Agent Goal Hijack | M6-3 + M5-8 + P6-4 | ✅ 已覆盖 | 目标劫持 = 提示注入核心表现，M6-3 判据同构 |
| ASI02 | Tool Misuse and Exploitation | M6-6 / M7-3 + P5-2 | ✅ 已覆盖 | 工具/能力越界调用，映射自主越权与越权承接 |
| ASI03 | Identity & Privilege Abuse | M7-3 + P5-2 / M6-6 | ✅ 已覆盖 | 身份/权限滥用，M7-3 越权承接判据吻合 |
| ASI04 | Agentic Supply Chain Vulnerabilities | M6-1 + P8-8 | ✅ 已覆盖 | 供应链植入，M6-1 同构 |
| ASI05 | Unexpected Code Execution | M8-8 + M8-5 + P8-4 | 🟡 部分覆盖（hypothesis） | 输出未校验 + 沙箱逃逸双坐标覆盖主体；Agentic 特有执行面案例待补 |
| ASI06 | Memory & Context Poisoning | M6-4 + P3-5 | ✅ 已覆盖 | 记忆/上下文投毒，M6-4 同构 |
| ASI07 | Insecure Inter-Agent Communication | M6-2 + P8-9 | 🟡 部分覆盖（hypothesis） | M6-2 不安全通信坐标存在，但**判据缺 Agentic 真实案例佐证** |
| ASI08 | Cascading Failures | M8-6 + P4-10 | ✅ 已覆盖 | 级联失败 = 错误级联无拦截，M8-6 同构 |
| ASI09 | Human-Agent Trust Exploitation | M6-5 + P8-5 | ✅ 已覆盖 | 信任利用，M6-5 同构 |
| ASI10 | Rogue Agents | M8 族 / M6-6（M9 待 ratify） | 🔴 **缺口** | Agent 行为超出预期约束/自发越界：最贴近 M9 自发协作，但 **M9 母坐标 opts 为空、待真实案例 ratify**，暂不落子码 |

## 二、真缺口与待核项（不造码声明）

### 1. ASI10 Rogue Agents → M9 自发协作（🔴 缺口）
- 现象：单个 Agent 或多 Agent 行为**自发**超出预期约束/访问边界，无外部攻击者驱动。
- 现状：TACT 的 **M9（自发协作）母坐标已准入但 opts 为空**，子码待 ratify。按纪律：**命中 M9 时不落子码，仅 L 轴定位**（输出固定文案）。
- 演进：须出现**两条互不相干的真实 Agentic 事故案例**同属"自发越界"机制，才按演进规则转正子码。
- 社区抓手：开源后将此列入**案例征集**——任何人提交符合"自发越界"的真实案例（脱敏），累计 2 条即触发 ratify 评审。

### 2. ASI07 → M6-2 不安全通信（🟡 判据待补）
- M6-2 坐标存在，判据与"不安全通信"吻合，但现有判据的案例支撑多为传统信道，**缺 Agentic 多智能体通信场景的真实案例**。
- 处理：映射标 `hypothesis`，引用时标注"待验证"；不因映射存在而虚报为已核验。

### 3. 通用提醒
- **映射不是结论**：ASI→坐标是"带判据的翻译假设"，坐标命中不等于该 Agent 应用已被攻破，需对照真实行为判定。
- **不新增坐标**：本清单只声明覆盖缺口，不在此新增任何 L/M/P 子坐标；坐标增删走 tact-three-axis-check 演进规则。

## 三、社区协作验证入口（开源后开放）

| 任务 | 谁可做 | 抓手 |
|---|---|---|
| M9 ratify 案例征集 | 任何有 Agentic 应用事故/异常记录的人 | 提交脱敏快照 + 现象，累计 2 条触发评审 |
| ASI07 判据补强 | 有 Agent 间通信安全事故记录者 | 提交真实案例佐证 M6-2 判据在 Agentic 域成立 |
| 全量 Agentic 回测 | 社区标注者 | 跑 `kappa` 标注脚本（见开源协作验证机制）核验映射 |
