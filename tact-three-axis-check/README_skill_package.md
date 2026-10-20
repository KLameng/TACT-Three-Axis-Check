# TACT 技能包说明

本技能包（`tact-skill-package-v1.2.1.zip`）是**运行核心版**，仅包含安装和运行所需的最小文件。

## 技能包内包含

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 过闸流程与判据（入口） |
| `references/coordinate_data.json` | 坐标底座（117 坐标 / 580 条 pairs） |
| `references/calibration_cases.json` | 校准基线（29 例） |
| `references/verification-chain.md` | 证据链四要素规范 |
| `references/novice_verification_gate.md` | novice 复现率质量门 |
| `references/coordinate_data.en.json` | 英文版坐标底座 |
| `guard/` | 文件完整性校验脚本 |

## 主仓库里还有（未随技能包提供）

| 文件 | 作用 | 获取方式 |
|---|---|---|
| `docs/TACT-kappa全历程汇总与分析.md` | κ 一致性检验全历程 | GitHub/Gitee 主仓库 |
| `SELF_FAILURES.md` | TACT 自我失败记录 | GitHub/Gitee 主仓库 |
| `engine/` | 可运行 Python 规则引擎 | GitHub/Gitee 主仓库 |
| `demo/` | 零配置 HTML 演示台 | GitHub/Gitee 主仓库 |
| `install/` | 安装包打包脚本 | GitHub/Gitee 主仓库 |

## 获取完整仓库

- GitHub：https://github.com/KLameng/TACT-Three-Axis-Check
- Gitee：https://gitee.com/heavenly-single-mark/tact-three-axis-check

---

*Copyright (c) 2026 KLameng <911712412@qq.com> · Released under Apache-2.0.*
