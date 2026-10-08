#!/usr/bin/env bash
# TACT toolkit controlled-file integrity verification
# Purpose: detect whether controlled files have been rolled back / tampered externally. Alert on rollback (exit 1).
# Usage: guard/verify.sh
# Dependency: MANIFEST.json (under guard/). After updating controlled files, you must regenerate MANIFEST.
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAN="$DIR/guard/MANIFEST.json"
FAIL=0

echo "== TACT controlled-file integrity verification =="
# Parse MANIFEST with python3 and compare sha256 per file (avoids fragile awk/json parsing)
python3 - "$DIR" "$MAN" <<'PY'
import sys, json, hashlib, os
root, man = sys.argv[1], sys.argv[2]
try:
    m = json.load(open(man, encoding='utf-8'))
except Exception as e:
    print("  [FATAL] MANIFEST.json could not be parsed:", e); sys.exit(2)
ok = True
for rel, meta in m['controlled_files'].items():
    path = os.path.join(root, rel)
    exp = meta['sha256']
    if not os.path.exists(path):
        print(f"  [FAIL] File missing: {rel} (expected {meta.get('version','?')})"); ok = False; continue
    cur = hashlib.sha256(open(path,'rb').read()).hexdigest()
    st = "OK " if cur==exp else "FAIL"
    if cur != exp: ok = False
    print(f"  [{st}] {rel}  expected {exp[:12]}…  actual {cur[:12]}…")
print("== Result:", "PASS (controlled files untouched)" if ok else "FAIL (files rolled back/tampered externally; recover via git tracing)", "==")
sys.exit(0 if ok else 1)
PY
exit $?
