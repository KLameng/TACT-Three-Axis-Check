# TACT 工具包版本锁与权限防护（guard/）

本目录提供"版本锁 + 完整性检测 + 写锁约定"，用于防止受控文件被外部进程回滚/篡改（曾在 2026-10-01 发生过一次：v1.1.0 落库改动被外部回滚到 v1.0.3）。

## 受控文件
- `SKILL.md`（判据引导，v1.1.3）
- `references/calibration_cases.json`（校准集，v1.2.2）
- `references/coordinate_data.json`（坐标底座，v2.7.9；**坐标语义不随判据修订变**，但语义修订须升版并在 MANIFEST 登记新哈希）

## 四件工具
| 工具 | 作用 | 用法 |
|---|---|---|
| `verify.sh` | **完整性检测**：比对受控文件 SHA-256 与 MANIFEST 基线，回滚/篡改即报警（exit 1） | `guard/verify.sh` |
| `lock.sh` | 受控文件设为只读 444，防误写/低权限覆盖 | `guard/lock.sh` |
| `unlock.sh` | 受控文件恢复可写 644，**仅落库编辑时用**；若有 `LOCK` 文件则拒绝解锁 | `guard/unlock.sh` |
| `sync_versions.py` | **版本号单一真源**：从 MANIFEST 渲染各文档的版本串（render）/ 检测版本漂移（check） | `python3 guard/sync_versions.py render` |

`MANIFEST.json` 是 SHA-256 + version 基线，**受控文件更新后必须重新生成**（见下）。

> **平台说明**：`verify.sh` 与 `sync_versions.py` 跨平台可用（仅需 python3）。`lock.sh`/`unlock.sh` 依赖 `chmod 444/644`，**权限锁仅在类 Unix 环境有效**（Windows 上 chmod 基本无效，但 sha256 完整性检测层仍有效）。`watch.sh` 依赖 Linux 专有的 `inotifywait`；Windows/macOS 请用 `guard/README.md` 末节的手工溯源方式。

## 标准落库流程（写锁约定）
```bash
guard/unlock.sh        # 1. 解锁（无 LOCK 冲突）
# 2. 编辑受控文件
# 3. 更新 guard/MANIFEST.json（重新算 sha256；可用 git diff 辅助）
python3 guard/sync_versions.py render   # 4. 渲染各文档版本串（勿手工填版本号）
git add -A && git commit -m "描述本次变更"   # 5. 提交，留历史可溯源
guard/lock.sh          # 6. 重新锁定只读
guard/verify.sh        # 7. 复核 PASS
python3 guard/sync_versions.py check    # 8. 版本漂移检测 PASS
```

## 单写者治理
- 工具包目录**只允许主 agent 落库 + 用户手动**，其他进程只读。
- 若多进程并发编辑，先用 `touch guard/LOCK` 占锁，完成后 `rm guard/LOCK`；unlock.sh 见到 LOCK 会拒绝解锁，防止互相覆盖。
- 受控文件在**源码仓库**中纳入 git 版本控制（发布包不含 `.git` 目录）。在源码仓库中可用：
  - `git status` 立即发现改动
  - `git log` 溯源谁在何时改了什么
  - `git restore <file>` 一键恢复
  - `git diff` 看差异

## 回滚处置 SOP
1. `guard/verify.sh` → FAIL 定位被改文件
2. `git log --oneline` + `git diff` 看被改成了什么
3. `git restore <file>` 恢复到已知良好基线
4. `guard/verify.sh` → PASS 确认
5. 溯源源头（见 `guard/watch.sh` 与"溯源"小节），防止再次发生

## 溯源（排查回滚源头）
- 检查精确改动时间：`stat SKILL.md references/calibration_cases.json`
- 谁在占用/写入：`lsof +D .`
- 定时任务：`crontab -l`；`ls /etc/cron*`
- 实时抓写入者：`guard/watch.sh`（基于 inotifywait，挂上后任何对受控文件的写都会报 PID）

> 上面四条是 Linux 路径。Windows/macOS 对应做法：
> - 改动时间：资源管理器"修改日期"列，或 PowerShell `Get-Item SKILL.md | Select-Object LastWriteTime`
> - 占用进程：Windows `handle.exe SKILL.md`（Sysinternals）；macOS `lsof SKILL.md`
> - 定时任务：Windows `schtasks /query /fo list`；macOS `crontab -l`
> - 实时监控：Windows 用 Sysinternals `Procmon` 过滤路径；macOS `fswatch`（`fswatch -o .`）
