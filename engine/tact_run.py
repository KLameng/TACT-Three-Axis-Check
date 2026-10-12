#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TACT 三轴坐标分类引擎（可复现基线版）

用法:
  python3 tact_run.py --calibration            # 跑校准集，输出三轴命中率报告
  python3 tact_run.py --text "一段事故描述"       # 薄入口：事故文本 -> 坐标 + 合规映射
  python3 tact_run.py --data-dir <references目录> # 指定坐标库/校准集位置

设计说明:
  - 零依赖（仅标准库 json/argparse/difflib），无 LLM key 即可运行。
  - 规则匹配器从现象文本推断 L/M/P 坐标，是"可复现基线"，不是金标判决。
  - 命中率是诊断信号：用来证明"输入一段事故 -> 程序吐出坐标 -> 可重复跑"，
    不是用来宣称分类器已达生产精度。接 LLM 后可显著提升（见 README）。
"""
import os, sys, json, argparse

# ---------- 数据加载 ----------
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def resolve_paths(data_dir):
    cd = os.path.join(data_dir, 'coordinate_data.json')
    cc = os.path.join(data_dir, 'calibration_cases.json')
    return cd, cc

# ---------- 规则字典（关键词 -> 坐标码）----------
# 每条规则是 (坐标码, [关键词...])；文本命中任一关键词即记一票。
# 关键词按校准集 29 例的现象语言设计，追求"可复现基线"的稳定命中，
# 不追求 100%（规则局限本身就是可复现实验要暴露的东西）。

L_RULES = [
    ('L4', ['网络抖动', '配额耗尽', '隔离边界故障', '环境故障', '资源配额', '基础设施',
            '隔离边界', '网络、资源配额']),
    ('L3', ['检索', 'RAG', '知识库', '跨轮', '长对话', '协作链', '多组件', '流水线',
            '多智能体', '跨环节', '第 40 轮', '第40轮', '层层放大', '训练', '部署到',
            '各环节', '每环节', '过期文档', '早期明确给出', '早期信息', '协作',
            '多智能体协作', '整条链', '放大']),
    ('L2', ['提示注入', '注入', '忽略以上', '忽略所有指令', '嵌入', '输入中',
            '日志', '明文', 'JSON schema', 'schema', '导出到外部', '外传',
            '感知前端', '物理贴纸', '停止标志', '日志与上下文', '接口调用',
            '出口链路', '输入接口', '打印对抗', '从日志窃取']),
    ('L1', ['自己决定', '自行发现', '自主', '单轮', '无任何外部', '自己',
            '无外部指令', '无任何外部指令', '未收到任何外部', '自发',
            '客服智能体', '客服系统为', '被要求遵守', '单个内容生成模型',
            '单个模型', '被它当成', '先断言', '反复失败']),
]

M_RULES = [
    ('M6-8', ['知识库写入', '伪造答案', 'RAG 知识库', '向智能体的 RAG', '投毒']),
    ('M6-6', ['遗留的 api 密钥', 'api 密钥', '权限外的薪酬', '权限外', '导出到外部',
              '自行发现环境', '自行发现']),
    ('M6-5', ['操纵性的诱导', '诱导话术', '说服', '高风险理财', '操纵', '高风险决策']),
    ('M5-2', ['无视内容安全禁令', '无视', '禁令', '直接输出违规', '违规内容']),
    ('M8-6', ['各环节单独都正确', '每环节', '过期文档', '无任何环节拦截', '错误级联',
              '中间无任何环节']),
    ('M7-3', ['权限校验未拦住', '权限校验', '低权限', '越权承接', '顺带']),
    ('M5-9', ['不得误导', '可权衡的指标', '区别对待', '约束当成', '被降级为', '绕」行误导',
              '绕行误导']),
    ('M6-3', ['忽略以上所有指令', '忽略以上', '嵌入指令', '当轮即', '即时放弃',
              '夹带指令', '当轮即时']),
    ('M6-4', ['写入长期记忆', '写入记忆', '长期记忆', '此后多轮对话', '持续引用',
              '已失效的指令']),
    ('M6-11', ['改写措辞', '拆分环节', '规则盲区', '绕开监管', '利用规则盲区', '规避方式',
               '钻盲区', '变体']),
    ('M2-3', ['置信信号', '肯定语气', '内部置信', '它其实不确定', '毫不含糊']),
    ('M2-4', ['不提示能力边界', '不拒绝', 'benchmark', '伪装通过', '不可靠的确定性']),
    ('M5-6', ['套用到完全不同', '过度外推', '被它当成普遍真理', '抽离语境', '前提被丢弃',
              '过度泛化']),
    ('M8-3', ['第 40 轮', '第40轮', '被模型遗忘', '早期明确给出', '长对话', '早期信息']),
    ('M1-3', ['仿真环境', '部署到产线', '产线后', '边缘场景', '仿真未覆盖', '错误率超过阈值',
              '训练/仿真']),
    ('M6-10', ['对抗贴纸', '停止标志', '视觉感知模型', '物理贴纸', '误判为', '定向改变']),
    ('M2-5', ['某特定群体系统性', '通过率差', '资质相同', '群体属性', '系统性更差',
              '决策结果层']),
    ('M4-2', ['凭证明文', '写进日志', '窃取该凭证', '明文写进', '冒充服务']),
    ('M4-3', ['约定 json', 'json schema', '非 json', '字段缺失', '接口契约失效',
              '下游解析失败', '按约定']),
    ('M9', ['两个隔离', '共享的缓存', '自发建立', '非授权通信', '自发协作', '无任何外部人类指令']),
    ('M8-7', ['反复失败', '空转', '反复重试', '不熔断', '直到用户催促', '死循环',
              '不升级上报', '不降级', '持续空转']),
]

P_RULES = [
    ('P1-8', ['错误结论', '事实', '误判', '错误驾驶决策', '照搬输出', '伪造答案',
              '定向改变', '错误方向']),
    ('P5-2', ['权限外', '权限被自行扩大', '权限校验', '越权承接']),
    ('P8-5', ['高风险理财', '财务决策', '基于其话术']),
    ('P5-5', ['内容安全禁令', '无视', '违规内容']),
    ('P6-4', ['系统提示约束', '目标被覆盖', '放弃系统提示', '按嵌入指令']),
    ('P8-7', ['绕开监管', '被禁止的操作', '监管红线']),
    ('P4-5', ['置信信号', '自评', '肯定语气']),
    ('P4-9', ['遗忘', '早期约束', '记忆衰减']),
    ('P7-4', ['群体', '区别对待', '系统性更差', '公平']),
    ('P3-6', ['仿真', '部署到', '产线', '边缘场景']),
    ('P8-3', ['凭证', '窃取', '冒充服务', '日志窃取']),
    ('P5-6', ['schema', '契约', '字段', '格式', '下游解析失败']),
    ('P2-4', ['互相否定', '矛盾', '两命题', '互相打架', '冲突']),
    ('P5-7', ['空转', '持续空转', '死循环', '无节制消耗']),
    ('P4-8', ['不暴露', '错信', '催促', '卡点', '毫无察觉']),
]

def classify(text):
    """输入事故现象文本，输出 {L:[], M:[], P:[]} 坐标集合。"""
    t = text.lower()
    def hit(rules):
        out = []
        for code, kws in rules:
            for kw in kws:
                if kw.lower() in t:
                    out.append(code); break
        return out
    return {'L': hit(L_RULES), 'M': hit(M_RULES), 'P': hit(P_RULES)}

# ---------- 命中率报告 ----------
def set_eq(a, b):
    return set(a) == set(b)

def run_calibration(calib):
    cases = calib['cases']
    rows = []
    # 逐码统计：golden 被命中数 / golden 总数；预测码里 golden 数 / 预测总数
    tp = {'L':0, 'M':0, 'P':0}; gtot = {'L':0,'M':0,'P':0}; ptot = {'L':0,'M':0,'P':0}
    exact = 0
    for c in cases:
        pred = classify(c['phenomenon'])
        gold = c['golden']
        row = {'id': c['id'], 'golden': gold, 'pred': pred, 'flags': c.get('flags', [])}
        for axis in ('L','M','P'):
            g = set(gold.get(axis, [])); p = set(pred[axis])
            tp[axis] += len(g & p)
            gtot[axis] += len(g)
            ptot[axis] += len(p)
            row[axis+'_hit'] = (g & p)
            row[axis+'_miss'] = (g - p)
        # case 级完全匹配（golden 空且预测空也算对）
        if all(set(pred[a]) == set(gold.get(a, [])) for a in ('L','M','P')):
            exact += 1
        rows.append(row)
    return rows, {'tp':tp, 'gtot':gtot, 'ptot':ptot, 'exact':exact, 'n':len(cases)}

def print_report(rows, stat):
    print('='*72)
    print('TACT 校准集命中率报告  (%s, bound %s)' % ('v1.2.1', 'coordinate_data v2.7.8'))
    print('='*72)
    print('%-8s %-22s %-22s %s' % ('ID','golden(L/M/P)','predicted(L/M/P)','判定'))
    print('-'*72)
    for r in rows:
        g = '/'.join([','.join(r['golden'].get(a,[]) or ['-']) for a in ('L','M','P')])
        p = '/'.join([','.join(r['pred'][a] or ['-']) for a in ('L','M','P')])
        ok = all(set(r['pred'][a])==set(r['golden'].get(a,[])) for a in ('L','M','P'))
        print('%-8s %-22s %-22s %s' % (r['id'], g, p, 'OK' if ok else '~'))
    print('-'*72)
    n = stat['n']
    print('样例数: %d   三轴完全匹配: %d/%d (%.1f%%)' % (n, stat['exact'], n, 100*stat['exact']/n))
    print()
    print('%-6s %-12s %-12s %-12s' % ('轴','召回率recall','精确率precision','说明'))
    for a in ('L','M','P'):
        rec = 100*stat['tp'][a]/stat['gtot'][a] if stat['gtot'][a] else float('nan')
        prec = 100*stat['tp'][a]/stat['ptot'][a] if stat['ptot'][a] else float('nan')
        g = stat['gtot'][a]; p = stat['ptot'][a]; hit = stat['tp'][a]
        print('%-6s %.1f%% (%d/%d)  %.1f%% (%d/%d)' % (a, rec, hit, g, prec, hit, p))
    print()
    print('注: recall=golden 码被预测命中的比例; precision=预测码里真属于 golden 的比例。')
    print('    这是无 LLM 的规则基线命中率，用来证明"可复现"；接 LLM 判定可显著提升。')

# ---------- 薄入口：坐标 + 生态映射 ----------
ECO_MAP = {
  'L1': ('OWASP LLM01/L02 模型层', 'NIST AI RMF Map-Measure'),
  'L2': ('OWASP LLM03/LM04 接口/输入层', 'EU AI Act  Annex I 技术文档'),
  'L3': ('OWASP LLM08/LM07 供应链/编排层', 'NIST AI RMF Manage-Manage'),
  'L4': ('环境/基础设施（非 AI 错误）', '—'),
  'M6': ('OWASP LLM01 Prompt Injection / LLM06 敏感信息', 'ATLAS T08xx 对抗行动'),
  'P8': ('NIST AI RMF Measure-Misuse', 'EU AI Act  Art.15 安全义务'),
  'P7': ('EU AI Act  Art.15 基本权利影响', 'NIST AI RMF Measure-Fairness'),
  'P1': ('NIST AI RMF Measure-Valid&Rel', '—'),
}
def eco_of(code):
    if code in ECO_MAP: return ECO_MAP[code]
    head = code.split('-')[0]
    return ECO_MAP.get(head, ('（映射待补）','（映射待补）'))

def run_text(text, coord_data):
    pred = classify(text)
    print('输入:', text)
    print('-'*60)
    for axis, label in (('L','L 轴·在哪一层犯'), ('M','M 轴·怎么错的'), ('P','P 轴·破坏了哪一面')):
        codes = pred[axis] or ['（未命中）']
        print('%s: %s' % (label, ', '.join(codes)))
    print('-'*60)
    print('生态合规映射（样例坐标 -> 行业框架）:')
    for axis in ('L','M','P'):
        for c in pred[axis]:
            ow, eu = eco_of(c)
            print('  %-8s -> %-32s | %s' % (c, ow, eu))

def main():
    ap = argparse.ArgumentParser(description='TACT 三轴坐标分类引擎')
    ap.add_argument('--calibration', action='store_true', help='跑校准集出命中率报告')
    ap.add_argument('--text', type=str, help='事故现象文本，输出坐标')
    ap.add_argument('--data-dir', type=str, default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'),
                    help='coordinate_data.json / calibration_cases.json 所在目录（默认 ./data）')
    args = ap.parse_args()

    cd, cc = resolve_paths(os.path.abspath(args.data_dir))
    if not (os.path.exists(cd) and os.path.exists(cc)):
        print('找不到数据文件: %s / %s' % (cd, cc)); sys.exit(1)
    coord = load_json(cd); calib = load_json(cc)

    if args.calibration:
        rows, stat = run_calibration(calib)
        print_report(rows, stat)
    elif args.text:
        run_text(args.text, coord)
    else:
        ap.print_help()

if __name__ == '__main__':
    main()
