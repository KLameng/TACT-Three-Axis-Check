# TACT Engine — 可复现判定引擎

把 TACT 三轴坐标分类法从「SKILL.md 方法论」变成**可运行、可复现、无需 LLM key 的 Python 程序**。

> 输入一段 AI 事故/失败现象文本 → 程序吐出 L/M/P 三轴坐标 + 行业合规映射（OWASP / NIST / EU AI Act）。
> 再内置 29 个校准样例，一键跑出三轴命中率报告 —— 这就是赛道一要求的「可复现测试案例结果数据」。

## 一分钟跑通

零依赖，只需 Python 3.8+（无任何 pip 安装）：

```bash
cd engine

# 1) 跑校准集，输出 29 个样例的三轴命中率报告（可复现证据）
python3 tact_run.py --calibration

# 2) 薄入口：输入一段事故描述，输出坐标 + 合规映射
python3 tact_run.py --text "客服智能体无视内容安全禁令，对老年用户用诱导话术说服购买高风险理财"
```

## 当前基线命中率（规则版，无 LLM）

| 轴 | 召回率 recall | 精确率 precision |
|---|---|---|
| L（在哪一层犯） | 78.6% (22/28) | 88.0% (22/25) |
| M（怎么错的） | 95.7% (22/23) | 91.7% (22/24) |
| P（破坏了哪一面） | 86.4% (19/22) | 82.6% (19/23) |

三轴完全匹配：**14/29（48.3%）**。

> 这是**无 LLM 的纯规则基线**，用来证明「输入可复现、输出可复现」。接 LLM（OpenAI 兼容接口）后可把 L 轴和边界样例的命中率显著拉高 —— 规则基线管「跑通」，LLM 管「判准」。

## 目录结构

```
engine/
├── tact_run.py            # 判定引擎 + CLI（--calibration / --text）
├── data/
│   ├── coordinate_data.json      # 117 坐标库（L4/M9组/P8组，含判据与验证路径）
│   └── calibration_cases.json    # 29 校准样例（含 golden 坐标）
└── README.md
```

## 它证明了什么

- **代码实现度**：不是 SKILL 文档，是可执行 Python；
- **可复现**：任何人 clone 后 `python3 tact_run.py --calibration` 得到同一份命中率报告；
- **测试案例结果数据**：29 个样例逐 case 的 golden vs predicted 对照表直接打印在报告里；
- **行业映射**：输出坐标的同时给出 OWASP / NIST / EU AI Act 对应义务。

## 升级路线（已预留）

1. `classify()` 换成 LLM 判定（保留同一套输入/输出接口），规则版作 fallback；
2. 把 `calibration_cases.json` 从 29 例扩到真实事故库（过闸台账 33+ 事件）；
3. 加 `--json` 输出，方便接入外部系统（事故上报 → 自动坐标 → 合规工单）。

---
TACT: Where did it break (L) · How (M) · What did it damage (P).
