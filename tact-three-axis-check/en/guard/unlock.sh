#!/usr/bin/env bash
# Unlock controlled files to writable (only for finalize-time editing)
# Usage: guard/unlock.sh
# Finalize flow: unlock → edit → verify & update MANIFEST → commit → lock
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
# Refuse unlock if another process is writing (write-lock convention)
if [ -f guard/LOCK ]; then
  echo "[LOCK] guard/LOCK exists (another process is writing); refusing to unlock. Confirm no conflict, then rm guard/LOCK and retry." >&2
  exit 1
fi
chmod 644 SKILL.md references/calibration_cases.json references/coordinate_data.json
echo "Controlled files unlocked to writable (644). After editing: update guard/MANIFEST.json → git commit → guard/lock.sh to re-lock."
