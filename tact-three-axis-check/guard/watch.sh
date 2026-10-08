#!/usr/bin/env bash
# TACT 工具包目录写入监控（溯源用）
# 用途：实时抓"谁在写受控文件"，锁定回滚源头。
# 用法：guard/watch.sh [秒数]   （默认监控 120 秒，Ctrl-C 结束）
# 依赖：inotifywait（若未安装，用 lsof/ps 手动溯源，见 guard/README.md）
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DUR="${1:-120}"
if ! command -v inotifywait >/dev/null 2>&1; then
  echo "[!] 未安装 inotifywait。可用替代："
  echo "    watch -n1 'lsof +D $DIR'"
  echo "    ps aux | grep -iE 'tact|restore|backup'"
  exit 1
fi
echo "监控 $DIR 下受控文件写入 ${DUR}s（任何写操作会打印时间与 PID；Ctrl-C 提前结束）..."
inotifywait -m -r --timefmt '%H:%M:%S' --format '[%T] %w%f %e (pid=%p cmd=%c)' \
  -e modify,close_write,create,move,delete "$DIR" --timeout "$DUR" 2>/dev/null \
  | grep -vE '\.git/' \
  || echo "（${DUR}s 内无受控文件写入）"
