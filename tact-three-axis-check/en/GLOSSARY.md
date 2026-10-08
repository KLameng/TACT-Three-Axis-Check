# TACT 三轴坐标分类法 · 中英对照词表（English Glossary）

> 本文件是全包英文化的统一基准。翻译 SKILL.md / README / coordinate_data / calibration / docs / CONTRIBUTING 时，**所有中文术语一律套用本表英文**，保证跨文件引用（速查、镜像表、分流声明、维护记录）不断裂。
> 坐标码（L1 / M6-8 / P1-8 等）语言中立，跨语言不变，不在翻译之列。

## 1. 坐标体系

| 中文 | English | 备注 |
|---|---|---|
| 封闭坐标空间 | closed coordinate space | 288 格 |
| 三维坐标 / 三维坐标定位 | three-axis coordinate | |
| 母坐标（机制族） | parent coordinate (mechanism family) | M/P 轴上层闸 |
| 子坐标（子类型） | child coordinate (subtype) | |
| 坐标码 | coordinate code | 如 M6-8，不译 |
| 落码 / 落坐标 | assign / land a coordinate | |
| 命中 / 判命中 | hit / confirmed hit | |
| 预测格 | prediction slot | 仅 1 例真实案例 |
| 不占 M/P 码 | carries no M/P code | |

## 2. 三轴

| 中文 | English |
|---|---|
| L 轴（在哪） | L-axis (where) |
| M 轴（怎么） | M-axis (how) |
| P 轴（破坏了哪一面） | P-axis (which facet is broken) |

**L 层名**：L1 模型内部 = Internal to Model · L2 输入输出接口 = Input/Output Interface · L3 推理协作链 = Reasoning-Collaboration Chain · L4 系统环境 = System Environment

**M 族名**：
- M1 信息不足 = Insufficient Information
- M2 信息失真 = Information Corruption
- M3 推理失效 = Reasoning Failure
- M4 输出失真 = Output Corruption
- M5 目标偏移 = Goal Drift
- M6 外部对抗 = External Adversarial Action
- M7 规则-职责-权限体系失配 = Rule/Role/Authority Mismatch
- M8 系统涌现 = System Emergence
- M9 自发协作 = Spontaneous Collaboration

**P 档名**：
- P1 事实失真 = Factual Distortion
- P2 逻辑断裂 = Logical Break
- P3 完整性缺失 = Completeness Loss
- P4 一致性破坏 = Consistency Breakdown
- P5 合规越界 = Compliance Overstep
- P6 目标偏离 = Goal Deviation
- P7 公平失衡 = Fairness Imbalance
- P8 安全威胁 = Safety Threat

## 3. 核心机制 / 执行流程

| 中文 | English |
|---|---|
| 三步匹配法 | Three-Step Matching Method |
| 前置排除闸 | Pre-Exclusion Gate |
| 过闸 | gate evaluation (pass through the gate) |
| 母坐标闸 / 子坐标闸 | parent-coordinate gate / child-coordinate gate |
| 硬分流判据 | hard-split criterion |
| 一票否决级判据 | veto-level criterion |
| 锋利判据 | sharp criterion (decisive) |
| 反向约束 | reverse constraint |
| 反向锚点 | reverse anchor (counter-anchor) |
| 防腐锚点 | anti-overfitting anchor |
| 反问验证 / 反问 | counter-check |
| 反问留痕 | counter-check trail |
| 双挂（列出） | dual-listing (list on both axes) |
| 镜像（对） | mirror (pair) |
| 跨轴分流声明 | cross-axis split declaration |

## 4. 排除闸与护栏

| 中文 | English |
|---|---|
| 治理域 | governance domain |
| 环境/基础设施故障（越界声明） | environmental/infrastructure failure (out-of-scope) |
| 越界声明 | out-of-scope declaration |
| 评测风险信号 | evaluation risk signal |
| 防误伤护栏 | over-exclusion guardrail |
| 疑罪从宽入闸 | default-to-inclusion when in doubt |
| 仅 L 层描述 | describe at the L layer only |

## 5. 维护 / 验证

| 中文 | English |
|---|---|
| 落库 | finalize / land into the package |
| 校准集 | calibration set |
| 金标 golden | golden (standard) |
| 回归模式 | regression mode |
| 命中率 | hit rate (agreement with golden) |
| kappa 检验 | kappa test (Fleiss κ) |
| 含空码 / 有码 | with-empty-code / non-empty-code |
| 标注者 | annotator |
| 离群 | outlier |
| 平台期 | plateau |
| ratify | ratify |
| 回灌 | back-fill (feed back) |
| 转正 | graduate to formal status |
| 演进规则 | evolution rule |
| 版本锁 | version lock |
| 受控文件 | controlled files |
| 维护记录 / changelog | changelog entry |

## 6. 跨引用坐标名（SKILL.md 速查/镜像/分流处引用，翻译必须一致）

| 码 | 中文 | English |
|---|---|---|
| M1-3 / P3-6 | 环境迁移失配 | Environment-Transfer Mismatch |
| M2-3 / P4-5 | 自我评估失准 | Self-Assessment Miscalibration |
| M2-4 | 能力虚报 | Capability Overclaiming |
| M2-5 | 算法歧视 | Algorithmic Discrimination |
| M3-1 | 推导跳跃 | Inference Jump |
| M4-2 / P8-3 | 凭证泄露 | Credential Leakage |
| M4-3 / P5-6 | 规约违约 | Contract Violation |
| M5-2 / P5-5 | 任务规范不遵守 | Task-Spec Non-Compliance |
| M5-5 | 目标漂移（奖励黑客与自主利益） | Goal Drift (Reward Hacking & Self-Interest) |
| M5-6 | 语境漂移（适用范围漂移） | Context Drift (Scope Drift) |
| M5-8 | 自生成驻留指令 | Self-Generated Persistent Instruction |
| M5-9 / P7-4 | 约束-目标反转 | Constraint-Goal Inversion |
| M6-3 / P6-4 | 提示注入（目标劫持） | Prompt Injection (Goal Hijacking) |
| M6-4 | 记忆投毒（上下文投毒） | Memory Poisoning (Context Poisoning) |
| M6-5 / P8-5 | 人-智能体信任利用 | Human-Agent Trust Exploitation |
| M6-6 | 自主越权访问 | Autonomous Privilege Escalation |
| M6-7 | 训练投毒 | Training Poisoning |
| M6-8 | 检索库投毒 | Retrieval-DB Poisoning |
| M6-10 | 特征扰动（对抗样本） | Feature Perturbation (Adversarial Examples) |
| M6-11 / P8-7 | 监管规避行为 | Regulatory Evasion |
| M7-3 / P5-2 | 越权承接 | Unauthorized Task Assumption |
| M8-3 / P4-9 | 记忆衰减 | Memory Decay |
| M8-6 | 错误级联无拦截 | Unchecked Error Cascade |
| P1-8 | 事实冲突 | Factual Conflict |
| P2-4 | 推理自相矛盾 | Self-Contradictory Reasoning |
| P8-4 | 沙箱逃逸 | Sandbox Escape |
| P8-8 | 供应链漏洞 | Supply-Chain Vulnerability |
| P8-9 | 不安全通信 | Insecure Communication |

> 镜像同名保留：M4-2≙P8-3、M5-9≙P7-4、M6-3≙P6-4、M2-3≙P4-5、M8-3≙P4-9、M7-3≙P5-2、M4-3≙P5-6、M6-5≙P8-5、M6-11≙P8-7 等镜像对，同名同译，与中文版一致。
> coordinate_data 中其余子坐标名（本表未列的 ~80 个）按上述命名风格统一翻译，并遵循镜像同名规则。
