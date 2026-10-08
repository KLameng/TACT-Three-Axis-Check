#!/usr/bin/env bash
# 解锁受控文件为可写（仅落库编辑时使用）
# 用法：guard/unlock.sh
# 落库流程：unlock → 编辑 → verify 更新 MANIFEST → commit → lock
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
# 若有其他进程正在写入，拒绝解锁（写锁约定）
if [ -f guard/LOCK ]; then
  echo "[LOCK] 存在 guard/LOCK（另一进程正在写），拒绝解锁。确认无冲突后 rm guard/LOCK 再试。" >&2
  exit 1
fi
chmod 644 SKILL.md references/calibration_cases.json references/coordinate_data.json
echo "受控文件已解锁为可写（644）。编辑完成后：更新 guard/MANIFEST.json → git commit → guard/lock.sh 重新锁定。"
