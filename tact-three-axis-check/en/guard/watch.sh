#!/usr/bin/env bash
# TACT toolkit directory write monitor (for attribution/tracing)
# Purpose: catch in real time who is writing controlled files; pin down the source of a rollback.
# Usage: guard/watch.sh [seconds]   (default 120s, end with Ctrl-C)
# Dependency: inotifywait (if not installed, trace manually with lsof/ps; see guard/README.md)
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DUR="${1:-120}"
if ! command -v inotifywait >/dev/null 2>&1; then
  echo "[!] inotifywait not installed. Alternatives:"
  echo "    watch -n1 'lsof +D $DIR'"
  echo "    ps aux | grep -iE 'tact|restore|backup'"
  exit 1
fi
echo "Monitoring writes to controlled files under $DIR for ${DUR}s (each write prints time & PID; Ctrl-C to stop early)..."
inotifywait -m -r --timefmt '%H:%M:%S' --format '[%T] %w%f %e (pid=%p cmd=%c)' \
  -e modify,close_write,create,move,delete "$DIR" --timeout "$DUR" 2>/dev/null \
  | grep -vE '\.git/' \
  || echo "(No writes to controlled files within ${DUR}s)"
