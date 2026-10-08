#!/usr/bin/env bash
# Lock controlled files to read-only (permission layer of the version lock)
# Usage: guard/lock.sh
# After locking, controlled files cannot be accidentally written / overwritten by lower privileges; verify.sh still runs read-only.
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
chmod 444 SKILL.md references/calibration_cases.json references/coordinate_data.json
echo "Controlled files locked to read-only (444). Use guard/unlock.sh to unlock before finalizing."
