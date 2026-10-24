#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TACT 版本号单一真源渲染器

问题背景：guard/MANIFEST.json 里的 version 字段是权威的逻辑版本，但 README、
guard/README.md、docs 头部的版本串此前靠人工同步，连续三版出现漂移
（本脚本存在的理由就是消除这类漂移）。

本脚本做两件事：
  1) render —— 从 guard/MANIFEST.json 读取版本，渲染/更新各文档中的版本串
     （用标记区间替换，保证只动版本串、不动其他正文）
  2) check —— 只校验不修改，返回非零表示存在漂移（可作 CI 门禁）

版本串标记约定（首次需人工插入，之后由本脚本维护）：
  文档中形如 {{V:SKILL.md}} / {{V:references/calibration_cases.json}} /
  {{V:references/coordinate_data.json}} 的占位符会被替换为实际版本号。
  另支持 {{CASES:references/calibration_cases.json}} 渲染用例条数、
  {{SYN:…}} / {{REAL:…}} 渲染 synthetic / real 用例条数。

用法：
  python3 guard/sync_versions.py render   # 渲染更新
  python3 guard/sync_versions.py check    # 校验（漂移则 exit 1）
  python3 guard/sync_versions.py --help
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MANIFEST = os.path.join(HERE, 'MANIFEST.json')

# 参与渲染的文档（相对技能包根）
DOCS = [
    'README.md',
    'guard/README.md',
    'docs/TACT-kappa全历程汇总与分析.md',
    'SKILL.md',
]

# 校准集统计需要读取的路径
CALIB = os.path.join(ROOT, 'references', 'calibration_cases.json')


def load_manifest():
    with open(MANIFEST, 'r', encoding='utf-8') as f:
        return json.load(f)


def calib_stats():
    """返回 (总条数, synthetic 条数, real 条数)。文件缺失时返回 None。"""
    if not os.path.exists(CALIB):
        return None
    with open(CALIB, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cases = data.get('cases', [])
    syn = sum(1 for c in cases if c.get('status') == 'synthetic')
    real = sum(1 for c in cases if c.get('status') == 'real')
    return len(cases), syn, real


def build_tokens(man):
    """构造 占位符 -> 实际值 的替换表。"""
    cf = man['controlled_files']
    tokens = {}
    for rel, meta in cf.items():
        key = rel.replace('/', '|')
        tokens['{{V:%s}}' % rel] = meta['version']
        tokens['{{V:%s}}' % key] = meta['version']
    stats = calib_stats()
    if stats:
        total, syn, real = stats
        for rel in cf:
            if 'calibration' in rel:
                tokens['{{CASES:%s}}' % rel] = str(total)
                tokens['{{SYN:%s}}' % rel] = str(syn)
                tokens['{{REAL:%s}}' % rel] = str(real)
                tokens['{{CASES}}'] = str(total)
                tokens['{{SYN}}'] = str(syn)
                tokens['{{REAL}}'] = str(real)
    return tokens


def render_text(text, tokens):
    """替换占位符；未识别的 {{...}} 保持原样并记为遗留。"""
    leftovers = []

    def repl(m):
        key = m.group(0)
        if key in tokens:
            return tokens[key]
        leftovers.append(key)
        return key

    return re.sub(r'\{\{[A-Z]+:[^}]+\}\}|\{\{[A-Z]+\}\}', repl, text), leftovers


def cmd_render():
    man = load_manifest()
    tokens = build_tokens(man)
    all_leftovers = []
    for rel in DOCS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print('  [SKIP] %s（不存在）' % rel)
            continue
        with open(path, 'r', encoding='utf-8') as f:
            old = f.read()
        new, leftovers = render_text(old, tokens)
        if leftovers:
            all_leftovers.extend((rel, x) for x in leftovers)
        if new != old:
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(new)
            print('  [RENDER] %s' % rel)
        else:
            print('  [OK] %s（无需改动）' % rel)
    if all_leftovers:
        print('\n  [WARN] 未识别的占位符（未替换）：')
        for rel, x in all_leftovers:
            print('    %s: %s' % (rel, x))
        return 1
    return 0


def cmd_check():
    """校验：把已渲染的版本串与 MANIFEST 对比。"""
    man = load_manifest()
    tokens = build_tokens(man)
    problems = []
    for rel in DOCS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        # 文档中出现的受控文件版本号，必须与 MANIFEST 一致
        for crel, meta in man['controlled_files'].items():
            ver = meta['version']
            base = os.path.basename(crel)
            # 找出 "<base> ... vX.Y.Z" 形式的引用
            for m in re.finditer(re.escape(base) + r'[^\n]{0,80}?(v\d+\.\d+\.\d+)', text):
                found = m.group(1)
                if found != ver:
                    problems.append('%s: %s 处引用 %s，MANIFEST 为 %s'
                                    % (rel, base, found, ver))
    if problems:
        print('== 版本漂移检测：FAIL ==')
        for p in problems:
            print('  - ' + p)
        return 1
    print('== 版本漂移检测：PASS（文档版本串与 MANIFEST 一致）==')
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    cmd = args[0]
    if cmd == 'render':
        return cmd_render()
    if cmd == 'check':
        return cmd_check()
    print('未知命令: %s（可用: render / check）' % cmd)
    return 2


if __name__ == '__main__':
    sys.exit(main())
