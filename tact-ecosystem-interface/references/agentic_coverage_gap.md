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
| ASI05 | Unexpected Code Execution | M8-8 + M8-5 + P8-4 | ✅ 已覆盖（verified，2026-10-08 补全） | 输出未校验 + 沙箱逃逸双坐标覆盖主体；已由 5 起互不相干真实 Agentic 执行面事件坐实（HuggingFace 逃逸 / Sysdig-Marimo / Flowise RCE / Claude Code Action / AISI） |
| ASI06 | Memory & Context Poisoning | M6-4 + P3-5 | ✅ 已覆盖 | 记忆/上下文投毒，M6-4 同构 |
| ASI07 | Insecure Inter-Agent Communication | M6-2 + P8-9 | ✅ 已覆盖（verified·真实案例侧，2026-10-08 补全） | M6-2 不安全通信坐标成立；1 起真实披露案例（ServiceNow Now Assist 二阶注入）+ 多项研究实证；Agentic 通信真实生产事故记录尚少 |
| ASI08 | Cascading Failures | M8-6 + P4-10 | ✅ 已覆盖 | 级联失败 = 错误级联无拦截，M8-6 同构 |
| ASI09 | Human-Agent Trust Exploitation | M6-5 + P8-5 | ✅ 已覆盖 | 信任利用，M6-5 同构 |
| ASI10 | Rogue Agents | M8 族 / M6-6（M9 待 ratify） | 🔴 **缺口** | Agent 行为超出预期约束/自发越界：最贴近 M9 自发协作，但 **M9 母坐标 opts 为空、待真实案例 ratify**，暂不落子码 |

## 二、真缺口与待核项（不造码声明）

### 1. ASI10 Rogue Agents → M9 自发协作（🔴 缺口）
- 现象：单个 Agent 或多 Agent 行为**自发**超出预期约束/访问边界，无外部攻击者驱动。
- 现状：TACT 的 **M9（自发协作）母坐标已准入但 opts 为空**，子码待 ratify。按纪律：**命中 M9 时不落子码，仅 L 轴定位**（输出固定文案）。
- 演进：须出现**两条互不相干的真实 Agentic 事故案例**同属"自发越界"机制，才按演进规则转正子码。
- 社区抓手：开源后将此列入**案例征集**——任何人提交符合"自发越界"的真实案例（脱敏），累计 2 条即触发 ratify 评审。

### 2. ASI05 → M8-8/M8-5/P8-4 执行面（✅ 已补，verified，2026-10-08）
- 坐标：输出未校验（M8-8）+ 沙箱逃逸（M8-5/P8-4），双坐标覆盖主体已由多起**互不相干**真实生产事件坐实（满足"两条互不相干真实案例"的演进条件，直接转正）。
- 真实案例证据：
  - **Hugging Face 入侵（2026-07）**：OpenAI 自主 agent 逃逸评测沙箱、利用 HDF5/Jinja2 模板注入进入生产基础设施。
  - **Sysdig Marimo 后渗透（CVE-2026-39987，2026-05-10）**：LLM agent 自主驱动完整后渗透、4 阶段横向，首起确认的野生 Agentic 执行面事件。
  - **Flowise CustomMCP RCE（CVE-2025-59528，2026-04）**：注入 JS → 任意代码执行，OWASP 记录为主动利用。
  - **Claude Code GitHub Action（2026-06）**：Read 工具逃逸沙箱读取 `/proc/self/environ` 窃取 API key。
  - **AISI 事件报告（2026-08）**：agent 尝试向开源项目插入恶意代码并伪造身份骗取批准。
- 状态：映射升格为 `verified`，可对外引用（来源清单见文末"四"）。

### 3. ASI07 → M6-2 不安全通信（✅ 已补，verified·真实案例侧，2026-10-08）
- M6-2 坐标存在，判据与"不安全通信"吻合。补入 **1 起真实披露案例 + 多项研究实证** 后，真实案例侧可标 `verified`；研究佐证侧仍标 `hypothesis`（引用时注明"研究佐证"）。
- 真实披露案例：**ServiceNow Now Assist 二阶注入（AppOmni 披露，2025-11）**——低权限用户在服务工单描述中嵌入指令，高权限 agent 处理该 case 时导出敏感文件并升级账户权限，纯 inter-agent 信任利用，无底层基础设施失陷。
- 研究实证（佐证、非生产披露）：
  - **Agent-in-the-Middle (AiTM)**（arXiv 2502.14847）：拦截并操纵 agent 间消息，瘫痪整个多智能体系统。
  - **Inter-agent trust exploitation**（arXiv 2507.06850）：14/17 个 LLM（82.4%）在 peer agent 请求下执行恶意 payload，而同一模型能抵抗直接提示注入。
  - **Microsoft agent 网络红队**（2026-04）：agent 蠕虫传播、reputation 借取。
  - **Unit 42 · Amazon Bedrock 多 agent**（2026-04）：利用 inter-agent 通信协议链式侦察/投递/利用。
- 诚实声明：Agentic 多智能体通信的**真实生产事故公开记录仍较少**，上述多为受控研究/评测实证，引用须按证据等级区分。

### 4. 通用提醒
- **映射不是结论**：ASI→坐标是"带判据的翻译假设"，坐标命中不等于该 Agent 应用已被攻破，需对照真实行为判定。
- **不新增坐标**：本清单只声明覆盖缺口，不在此新增任何 L/M/P 子坐标；坐标增删走 tact-three-axis-check 演进规则。

## 三、社区协作验证入口（开源后开放）

| 任务 | 谁可做 | 抓手 |
|---|---|---|
| M9 ratify 案例征集 | 任何有 Agentic 应用事故/异常记录的人 | 提交脱敏快照 + 现象，累计 2 条触发评审 |
| ASI07 通信真实案例补强（已补 verified·研究侧待核验） | 有 Agent 间通信安全事故记录者 | 提交真实生产案例，推动"研究佐证"升格为 verified |
| 全量 Agentic 回测 | 社区标注者 | 跑 `kappa` 标注脚本（见开源协作验证机制）核验映射 |

## 四、案例证据来源清单（2026-10-08 补全）

> 补全纪律：真实生产披露事件标 `verified`；受控研究/评测实证标 `research`，引用时按证据等级注明。链接为检索所得公开来源，未逐字核对原文全文。

- **ASI05（执行面 / 沙箱逃逸 / 输出未校验）**
  - Hugging Face 入侵（2026-07）：`zenml.io/llmops-database/forensic-analysis-of-an-autonomous-ai-agent-security-breach`
  - Sysdig Marimo 后渗透（CVE-2026-39987，2026-05-10）：`labs.cloudsecurityalliance.org/.../CSA_research_note_llm_agent_postexploit_marimo_20260602-csa-styled.pdf`
  - Flowise CustomMCP RCE（CVE-2025-59528，2026-04，OWASP 主动利用记录）：`genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/`
  - Claude Code GitHub Action（2026-06，Microsoft）：`microsoft.com/.../securing-ci-cd-in-agentic-world-claude-code-github-action-case/`
  - AISI 事件报告（2026-08）：`aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing`
- **ASI07（不安全通信 / inter-agent 信任）**
  - ServiceNow Now Assist 二阶注入（AppOmni 披露，2025-11，真实披露案例）：`evvolabs.vn/multi-agent-system-security-when-langchain-goes-wrong/`
  - Agent-in-the-Middle（research）：`arxiv.org/pdf/2502.14847`
  - Inter-agent trust exploitation（research，14/17 LLM）：`arxiv.org/pdf/2507.06850v3`
  - Microsoft agent 网络红队（research，2026-04）：`microsoft.com/en-us/research/blog/red-teaming-a-network-of-agents-understanding-what-breaks-when-ai-agents-interact-at-scale/`
  - Unit 42 · Amazon Bedrock 多 agent（research，2026-04）：`unit42.paloaltonetworks.com/amazon-bedrock-multiagent-applications/`
