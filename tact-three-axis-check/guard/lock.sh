#!/usr/bin/env bash
# 锁定受控文件为只读（版本锁的权限层）
# 用法：guard/lock.sh
# 锁定后受控文件不可被误写/低权限覆盖；verify.sh 仍可读运行。
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
chmod 444 SKILL.md references/calibration_cases.json references/coordinate_data.json
echo "受控文件已锁定为只读（444）。落库前用 guard/unlock.sh 解锁。"
