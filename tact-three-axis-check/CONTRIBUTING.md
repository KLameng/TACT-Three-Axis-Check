# 贡献指南 / Contributing

感谢你想为 TACT 做贡献。本项目目前处于早期阶段，我们欢迎以下类型的贡献：

## 1. 提交真实案例（最重要）

TACT 的坐标判据目前主要基于 synthetic（人工构造）样例，**真实事故案例是最缺的资源**。

**如何提交：**
- 通过 GitHub Issues 提交（脱敏后的事故描述）
- 或发邮件到 911712412@qq.com

**提交内容：**
- 事故现象（发生了什么）
- 你的判断（你觉得属于什么坐标）
- 验证路径（你是怎么确认的）

## 2. 坐标 ratify 流程

当某个机制累计 **2 条互不相干的真实案例** 后，触发坐标评审：
- 评审该机制是否应该成为正式子坐标
- 评审通过后，coordinate_data.json 升版
- 校准集同步扩充

## 3. 不建议的贡献

- **不要自行造码**：不建议自己发明新坐标编号。坐标体系有严格的演进规则，需要真实案例支撑。
- **不要修改 golden**：校准集的 golden 坐标是基线，不要随意改动。
- **不要补镜像**：不为了"对称好看"补镜像坐标。

## 4. 反馈渠道

- GitHub Issues：https://github.com/KLameng/TACT-Three-Axis-Check/issues
- Gitee Issues：https://gitee.com/heavenly-single-mark/tact-three-axis-check/issues
- 邮箱：911712412@qq.com

---

*Copyright (c) 2026 KLameng <911712412@qq.com> · Released under CC BY 4.0.*
