# TACT 三轴坐标分类法 / TACT Three-Axis Coordinate Check

给 AI 系统（大模型 / 智能体）的错误、失败与异常做定位的三轴坐标分类法。

**L 轴**（在哪一层犯）· **M 轴**（怎么错的）· **P 轴**（破坏了哪一面）

> **判据蓝本声明**：本仓库的判据与坐标尚未经人工标注者独立验证，属"带判据的分类假设"，正确性待社区 **ratify**（提交真实案例 + 结构校验）逐项确认。使用者引用坐标时请自行核验，勿当作已验证事实。

## 快速部署（在豆包工作模式里装这个技能）

**方式一：用打包好的安装包（推荐，30 秒）**

1. 下载 [`install/tact-skill-package-v1.2.1.zip`](install/tact-skill-package-v1.2.1.zip)（123KB，技能安装包）
2. 打开**豆包工作模式**（agent 模式，不是普通聊天窗口）
3. 把这个 zip 文件直接发给豆包，说"安装这个技能"——豆包会识别并完成安装
4. 安装成功后，在对话里描述一个 AI 事故/失败现象，**命令豆包用 TACT 技能分析这个事故**
5. 豆包会输出 L/M/P 三轴坐标 + 命中含义 + 验证路径 + 行业合规映射（OWASP / NIST / EU AI Act）

> 注意：必须在**豆包工作模式**下安装和使用；普通聊天窗口不支持技能安装与触发。

**方式二：开发者从仓库源码直接装**

仓库里 `tact-three-axis-check/` 和 `tact-ecosystem-interface/` 是技能源目录，结构与安装包一致，可直接复制到技能开发目录。

## 可运行测试（无需 LLM key，零依赖）

仓库 `engine/` 提供纯 Python 规则引擎，一键复现校准集命中率：

```bash
cd engine
python3 tact_run.py --calibration    # 跑 29 校准样例，输出三轴命中率报告
python3 tact_run.py --text "事故描述"  # 输入事故文本，输出坐标 + 合规映射
```

当前基线（规则版，无 LLM）：M 轴召回 95.7% · P 轴 86.4% · L 轴 78.6%。接 LLM 判定可进一步提升。

## 仓库结构

```
├── LICENSE                          # CC BY 4.0 开源许可
├── install/                         # 打包好的技能安装包（zip，解压即用）
├── engine/                         # 可运行规则引擎（python3，零依赖，复现命中率）
├── demo/                           # 零配置演示台（单 HTML，浏览器打开即用）
├── tact-three-axis-check/           # 主判据引擎（含中文 + en/ 英文版）
│   ├── SKILL.md                     # 过闸流程与判据（入口，先读这里）
│   ├── references/                  # 坐标底座 coordinate_data.json + 校准集 calibration_cases.json
│   ├── guard/                       # 受控文件完整性校验脚本（lock/unlock/watch/verify）
│   └── docs/                        # 卡帕一致性全历程汇总与分析
└── tact-ecosystem-interface/        # 生态接口资产包
    └── references/                  # 跨地图 / EU AI Act 义务 / 元标签 / Agentic 覆盖查缺
```

## 快速开始

1. 从 `tact-three-axis-check/SKILL.md` 开始，按过闸流程对错误现象做 L/M/P 定位。
2. 坐标定义以 `tact-three-axis-check/references/coordinate_data.json` 为准（TACT v2.7.8，117 子坐标）。
3. 涉及行业框架映射 / EU 义务 / Agentic 覆盖查缺，使用 `tact-ecosystem-interface/`。

## 校准与一致性

- 校准基线：`calibration_cases.json`（v1.2.1，29 例，含真实 agent 空转案例 CAL-29），运行校准模式计算三轴命中率作为诊断信号，**非通过/失败门槛**。
- 一致性历程：`docs/TACT-kappa全历程汇总与分析.md`（5 家国产模型、12 条 synthetic、Fleiss κ，最终 L κ 0.945 / 命中 98.2%）。
- 说明：卡帕验证目前依赖模型自评，**人工独立验证交由开源社区自发 ratify**。

## 参与贡献

欢迎提交真实案例（脱敏）以帮助 ratify 坐标，重点征集：
- Agentic 应用事故 / 异常记录（补强 ASI05 / ASI07 覆盖）
- 自发越界（M9 待 ratify）案例，累计 **2 条互不相干真实案例** 触发评审

详见各子目录的 CONTRIBUTING.md。

## 许可与联系方式

- 许可证：Creative Commons Attribution 4.0（CC BY 4.0），署名 **KLameng**。详见 `LICENSE`。
- 维护者：**KLameng** · 联系邮箱：**911712412@qq.com**（问题反馈 / 案例提交 / 合作）

---

*Copyright (c) 2026 KLameng <911712412@qq.com> · Released under CC BY 4.0.*
