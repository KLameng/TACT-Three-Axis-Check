#!/usr/bin/env bash
# TACT 工具包受控文件完整性校验
# 用途：检测受控文件是否被外部回滚/篡改。回滚即报警（exit 1）。
# 用法：guard/verify.sh
# 依赖：MANIFEST.json（guard 目录下）。更新受控文件后必须重新生成 MANIFEST。
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAN="$DIR/guard/MANIFEST.json"
FAIL=0

echo "== TACT 受控文件完整性校验 =="
# 用 python3 解析 MANIFEST，逐文件比对 sha256（避免 awk/json 解析脆弱）
python3 - "$DIR" "$MAN" <<'PY'
import sys, json, hashlib, os
root, man = sys.argv[1], sys.argv[2]
try:
    m = json.load(open(man, encoding='utf-8'))
except Exception as e:
    print("  [FATAL] MANIFEST.json 无法解析:", e); sys.exit(2)
ok = True
for rel, meta in m['controlled_files'].items():
    path = os.path.join(root, rel)
    exp = meta['sha256']
    if not os.path.exists(path):
        print(f"  [FAIL] 文件缺失: {rel} (应为 {meta.get('version','?')})"); ok = False; continue
    cur = hashlib.sha256(open(path,'rb').read()).hexdigest()
    st = "OK " if cur==exp else "FAIL"
    if cur != exp: ok = False
    print(f"  [{st}] {rel}  期望 {exp[:12]}…  实际 {cur[:12]}…")
print("== 结果:", "PASS（受控文件未被动过）" if ok else "FAIL（有文件被外部回滚/篡改，请用 git 溯源恢复）", "==")
sys.exit(0 if ok else 1)
PY
exit $?
