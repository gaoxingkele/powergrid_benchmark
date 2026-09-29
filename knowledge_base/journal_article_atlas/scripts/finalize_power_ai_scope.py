"""Merge complete, source-screened scope decisions without altering prior atlas data."""
import hashlib
import html
import json
import re
import fitz
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'calibration/2026-09-13_power_ai_scope'
DECISIONS = ['core_ai','computational_support','review_background','adjacent','out_of_scope','uncertain']
MDPI_CODES = {'Applied Sciences':'app','Energies':'en','Electronics':'electronics','Information':'info','Algorithms':'a','Mathematics':'math','Sensors':'s','Machines':'machines','Symmetry':'sym','Sustainability':'su','Processes':'pr','Remote Sensing':'rs','Future Internet':'fi','Atmosphere':'atmos'}

def front_identity(source):
    """Local DOI identity cross-check; not publisher/Crossmark verification."""
    with fitz.open(source['source_path']) as doc:
        first=doc[0].get_text()
    doi=(source.get('doi') or '').lower()
    compact=re.sub(r'\s+','',first).lower()
    same_doi=bool(doi and doi in compact)
    venue=source['venue']
    expected = bool(re.fullmatch('10\\.3390/'+MDPI_CODES[venue]+r'\d+',doi)) if venue in MDPI_CODES else doi.startswith('10.1109/access.')
    draft=bool(re.search(r'FOR PEER REVIEW|arXiv:',first,re.I))
    return {'doi_matches_front_page':same_doi,'doi_namespace_matches_venue':expected,'draft_marker':draft,
            'status':'local_identity_candidate' if same_doi and expected and not draft else 'requires_identity_review'}

def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def merge(manifest, batches, audit, overrides):
    expected = {r['paper_id']:r for r in manifest['articles']}
    reviews = {}
    for reviewer, rows in batches:
        for r in rows:
            pid = r['paper_id']
            if pid in reviews or pid not in expected:
                raise ValueError(f'duplicate or unexpected ID: {pid}')
            if r['decision'] not in DECISIONS or not r.get('rationale') or not r.get('evidence_pages'):
                raise ValueError(f'incomplete review: {pid}')
            reviews[pid] = dict(r, reviewer=reviewer)
    if set(reviews)!=set(expected):
        raise ValueError(f'missing reviews: {sorted(set(expected)-set(reviews))}')
    checks = {r['paper_id']:r for r in audit['records']}
    if set(checks)!=set(expected):
        raise ValueError('source audit ID mismatch')
    output = []
    for pid, source in expected.items():
        r = reviews[pid]
        check = checks[pid]
        pages = r['evidence_pages']
        if any(not isinstance(p,int) or p<1 or p>check.get('pages',0) for p in pages):
            raise ValueError(f'invalid source page: {pid}')
        row = dict(source)
        row.update(r)
        row['manifest_title'] = source['title']
        row['title'] = r.get('source_title') or source['title']
        row['manifest_venue'] = source['venue']
        row['identity_adjudication'] = overrides.get(pid)
        identity=source.get('local_identity_check',{})
        row['venue_profile_eligible'] = identity.get('status')=='local_identity_candidate'
        if pid in overrides:
            decision = overrides[pid]
            row['title'] = decision['source_title']
            row['venue_profile_eligible'] = decision['venue_profile_eligible']
        row['ai_role'] = r.get('ai_role','not_assessed')
        row['source_integrity_status'] = check['status']
        row['scope_status'] = 'source_screened' if check['status']=='source_integrity_pass' and r['decision']!='uncertain' else 'requires_review'
        row['core_scope_eligible'] = r['decision']=='core_ai' and row['scope_status']=='source_screened'
        row['journal_core_candidate'] = row['core_scope_eligible'] and row['venue_profile_eligible']
        row['full_semantic_calibration'] = False
        row['object_counts'] = check.get('candidate_counts')
        row['object_counts_status'] = 'automatic_candidate'
        row['retraction_status'] = 'not_assessed'
        row['difficulty_profile'] = None
        output.append(row)
    return output

def main():
    paths = [OUT/f'review_{name}.json' for name in ['core','energy','other']]
    batches=[]
    for p in paths:
        content=read(p)
        batches.append((p.stem,content['records'] if isinstance(content,dict) else content))
    manifest_path=ROOT/'outputs/corpus_manifest.json'
    audit=read(OUT/'source_audit.json')
    if audit['manifest_sha256']!=digest(manifest_path):
        raise ValueError('audit belongs to stale manifest')
    overrides={r['paper_id']:r for r in read(OUT/'identity_adjudications.json')['records']}
    manifest=read(manifest_path)
    for item in manifest['articles']:
        item['local_identity_check']=front_identity(item)
    rows=merge(manifest,batches,audit,overrides)
    (OUT/'scope_records.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
    counts=dict(Counter(r['decision'] for r in rows))
    journals=read(ROOT/'journal_profiles.json')['profiles']
    report=['# 电力 × AI：现有169篇全量范围核验','','范围通过不是全文质量通过。本表来自摘要及必要方法/数据页的助手复核；AI中心/辅助作用未检查时保留not_assessed。','','## 总体结果','',f'决策数量：`{counts}`。',f'文件完整性：`{audit["counts"]}`。','','## 逐刊覆盖','','“AI候选”仅指范围和文件通过，尚非完成全文校准的期刊样本。','','| 期刊 | 本地记录 | 核心AI | 计算支持 | 综述 | 相邻 | 排除 | 待核实 | 可进入该刊的AI候选 |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for j in journals:
        group=[r for r in rows if r['manifest_venue']==j]
        c=Counter(r['decision'] for r in group)
        report.append('| '+j+' | '+str(len(group))+' | '+' | '.join(str(c[d]) for d in DECISIONS)+' | '+str(sum(r['journal_core_candidate'] for r in group))+' |')
    report+=['','## 使用边界','','- 使用 `scope_records.json` 查询本轮；旧SQLite与旧自动总表保持历史版本，不代表本轮筛选。','- 169条均有决定，不代表169篇均在范围内，也不代表所有期刊已具备足量同类文章。','- 公式、图表计数仍为automatic_candidate；段落语义、统计适当性、实验真实性、代码可运行性、撤稿/更正状态尚未全量核验。','- 分层时继续区分负荷预测、风光预测、规划、调度、诊断、电力信息/NLP与安全；混合代理数据与AI辅助场景建模单列。','- 预印本或归属冲突文章不用于期刊版式画像。','- 未重算期刊平均水平/难度/录用概率；不以数量代替证据。','','## 身份修订的一手依据','']
    for r in overrides.values():
        report.append(f'- `{r["paper_id"]}`：{r["reason"]} [来源]({r["source_url"]})')
    report+=['','## 下一步全文校准','','对核心AI候选依次完成：对象编号与视觉校验→数据集/split/基线/消融设计→统计单位与区间→章节和段落逻辑→难度与证据质量分离评分。先完成同任务组，再发布小样本描述画像；不能将不同电力任务直接混算。']
    (OUT/'SCOPE_REPORT.md').write_text('\n'.join(report),encoding='utf8')
    detailed=['# 全部文章的范围决定','','保留排除记录以便复核；“页”指原PDF物理页。','','| ID | 期刊候选 | 原文/记录标题 | 决定 | 任务 | 方法 | 页 | 理由与边界 |','|---|---|---|---|---|---|---|---|']
    for r in rows:
        vals=[r['paper_id'],r['manifest_venue'],r['title'],r['decision'],r['task'],r['method_family'],str(r['evidence_pages']),r['rationale']+' '+r.get('scope_notes','')]
        detailed.append('| '+' | '.join(str(v).replace('|','/').replace('\n',' ') for v in vals)+' |')
    (OUT/'ALL_ARTICLES.md').write_text('\n'.join(detailed),encoding='utf8')
    core=[r for r in rows if r['core_scope_eligible']]
    (OUT/'core_ai_reading_list.json').write_text(json.dumps(core,ensure_ascii=False,indent=2),encoding='utf8')
    # A readable, local-only searchable table; values are HTML-escaped.
    trs=[]
    for r in rows:
        cells=[r['paper_id'],r['manifest_venue'],r['title'],r['decision'],r['task'],r['method_family'],r['rationale'],r.get('scope_notes','')]
        trs.append('<tr>'+''.join('<td>'+html.escape(str(c))+'</td>' for c in cells)+'</tr>')
    page='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>电力×AI范围核验</title><style>body{font:14px system-ui;margin:24px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:8px;text-align:left;vertical-align:top}th{background:#eaf0f7;position:sticky;top:0}input{padding:10px;width:70%}small{display:block;margin:12px 0}</style><h1>电力 × AI 全量范围核验</h1><p>现有169篇；范围复核不等于全文质量认证。数量/难度仍未正式校准。</p><input id="q" placeholder="筛选期刊、任务、算法或决定，例如 core_ai"><small id="n"></small><table><thead><tr>'''+''.join('<th>'+x+'</th>' for x in ['ID','期刊候选','标题','决定','任务','方法','理由','边界'])+'</tr></thead><tbody>'+''.join(trs)+'''</tbody></table><script>const q=document.getElementById('q'),rows=[...document.querySelectorAll('tbody tr')];function filter(){let n=0;for(const r of rows){let ok=r.textContent.toLowerCase().includes(q.value.toLowerCase());r.hidden=!ok;if(ok)n++}document.getElementById('n').textContent=n+' / '+rows.length+' 条'}q.addEventListener('input',filter);filter();</script></html>'''
    (OUT/'scope_browser.html').write_text(page,encoding='utf8')
    bound=[*paths,OUT/'identity_adjudications.json',OUT/'source_audit.json',OUT/'SCOPE_PROTOCOL.md',Path(__file__).resolve()]
    summary={'scope_records':len(rows),'decision_counts':counts,'core_scope_candidates':len(core),'journal_core_candidates':sum(r['journal_core_candidate'] for r in rows),'source_audit_counts':audit['counts'],'full_semantic_calibration_count':0,'missing_reviews':0,'duplicate_reviews':0,'invalid_evidence_pages':0,'external_llm_calls':0,'input_sha256':{str(p.relative_to(ROOT)):digest(p) for p in bound},'corpus_manifest_sha256':digest(manifest_path)}
    (OUT/'validation_report.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in summary.items() if k!='input_sha256'},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
