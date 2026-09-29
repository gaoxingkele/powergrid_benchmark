"""Publish targeted source-screening records, parser discrepancies and journal coverage."""
import json,re,hashlib
from pathlib import Path
from collections import defaultdict,Counter
import fitz
from atlas import validate_observation

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'calibration/2026-09-13_round1'

def corrected_labels(pdf):
    objects=[]
    with fitz.open(pdf) as doc:
        for page_n,page in enumerate(doc,1):
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    text=''.join(s['text'] for s in line['spans']).strip()
                    match=re.match(r'^(Figure|Fig\.|Table)\s*(\d+|[IVX]+)\s*\.',text,re.I)
                    if match:
                        objects.append({'type':'table' if match[1].lower()=='table' else 'figure','label':match[2],
                           'page':page_n,'bbox':line['bbox'],'caption_candidate':text[:200]})
                    # Keep equation numbering from short standalone math-label lines;
                    # this avoids dependence on the right edge of a two-column page.
                    match=re.fullmatch(r'\((\d+[a-z]?)\)',text)
                    if match:objects.append({'type':'equation','label':match[1],'page':page_n,'bbox':line['bbox']})
    return objects

def main():
    records=json.loads((OUT/'pilot_records.json').read_text(encoding='utf8'))
    reviews=json.loads((OUT/'source_reviews.json').read_text(encoding='utf8'))['records']
    corpus=json.loads((ROOT/'outputs/corpus_manifest.json').read_text(encoding='utf8'))
    cohorts=defaultdict(list); observations=[]; discrepancies=[]
    for r in records:
        rev=reviews[r['paper_id']]; r['task']=rev['task'];r['subtype']=rev['subtype']
        r['cohort']=r['journal']+'|'+r['task']+'|empirical_method'
        r['semantic_review_status']='targeted_source_screened_NOT_full_annotation'
        r['review']=rev
        objects=corrected_labels(r['source_path']); r['v2_objects']=objects
        metrics={key:len(set(o['label'] for o in objects if o['type']==kind)) for key,kind in
           [('figure_label_candidates','figure'),('table_label_candidates','table'),('numbered_equation_label_candidates','equation')]}
        r['v2_metrics']=metrics
        for name,value in metrics.items():
            if value!=r['v0_metrics'][name] or value!=r['v1_metrics'][name]:
                discrepancies.append({'paper_id':r['paper_id'],'metric':name,'v0':r['v0_metrics'][name],'v1':r['v1_metrics'][name],'v2':value,'status':'parser_disagreement_NOT_gold_error','reason':'strict caption punctuation, case-insensitive labels, span-line equation recovery; source visual audit still required'})
        for field,value in [('paper.topic',rev['task']),('paper.relevance','direct'),('paper.pages',r['v0_metrics']['pages'])]:
            if rev['task']=='traffic_proxy_plus_electric_load' and field=='paper.relevance':value='adjacent'
            obs={'entity_id':r['paper_id'],'field_id':field,'value':value,'status':'verified',
              'evidence':[{'source_sha256':r['source_sha256'],'locator':{'physical_page':1,'section':'Abstract' if field!='paper.pages' else 'whole_pdf_page_tree','read_integrity':r['read_integrity']}}],
              'method':'single_assistant_targeted_source_review' if field!='paper.pages' else 'three_page_count_signals_agree',
              'annotator':'current_assistant','version':'2026-09-13_round1'}
            validate_observation(obs); observations.append(obs)
        cohorts[r['cohort']].append(r)
    (OUT/'reviewed_records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/'source_screened_observations.json').write_text(json.dumps(observations,ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/'parser_disagreements.json').write_text(json.dumps(discrepancies,ensure_ascii=False,indent=2),encoding='utf8')
    profiles=[]
    md=['# 同期刊 × 同任务校准对照（第一轮）','','这是14篇的来源筛选与提取器校准，不是完整论文难度评定。n<10 按本库协议只展示个案，不给期刊平均值。公式/图表的v2仍是候选；双解析器一致也不等于人工金标准。','','| 期刊 / 任务 | 已核对任务的篇数 | 子类型 | 状态 |','|---|---|---|---|']
    for key,group in sorted(cohorts.items()):
        profiles.append({'cohort':key,'source_screened_n':len(group),'full_annotation_n':0,'independent_human_n':0,'paper_ids':[r['paper_id'] for r in group],'status':'CASE_SERIES_ONLY','difficulty_profile':None,'journal_mean':None})
        md.append(f"| {key} | {len(group)} | {', '.join(sorted(set(r['subtype'] for r in group)))} | CASE_SERIES_ONLY |")
    md+=['','## 逐篇数量对照','','页数经页树检查；其他列为严格图题/行级公式标签候选，不是最终人工计数。','','| 论文ID | 期刊 | 页数 | 公式候选 | 图候选 | 表候选 |','|---|---|---|---|---|---|']
    for r in records:
        m=r['v2_metrics'];md.append(f"| {r['paper_id']} | {r['journal']} | {r['v0_metrics']['pages']} | {m['numbered_equation_label_candidates']} | {m['figure_label_candidates']} | {m['table_label_candidates']} |")
    md+=['','## 每篇框架与证据使用方式','']
    for r in records:
        v=r['review']; md += [f"### {r['title']}",'',f"ID `{r['paper_id']}`；原件 `{r['source_path']}`；定位页 {v['evidence_pages']}。",'',f"- 框架：{v['framework']}",f"- 实验分类：{v['experiment_note']}",f"- 不可照搬之处：{v['risk']}",'']
    (OUT/'COHORT_COMPARISON.md').write_text('\n'.join(md),encoding='utf8')
    (OUT/'cohort_profiles.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2),encoding='utf8')
    allprofiles=json.loads((ROOT/'journal_profiles.json').read_text(encoding='utf8'))['profiles']
    counts=Counter(r['venue'] for r in corpus['articles']); selected=Counter(r['journal'] for r in records)
    table=['# 全部期刊覆盖与缺口','','未选中的期刊不是已完成校准，也不据此断言该刊没有相关论文。本轮未重新联网补采。','','| 期刊 | 本地候选 | 本轮来源复核 | 处理 |','|---|---|---|---|']
    for journal in allprofiles:
        n=selected[journal]
        note='已形成同任务个案组，逐篇完整标注与独立复核待完成' if n>=3 else ('仅1篇相关样本，不能形成期刊平均值' if n else '未形成电力同任务组；需从摘要复核候选并补采，禁止跨领域凑数')
        table.append(f'| {journal} | {counts[journal]} | {n} | {note} |')
    table+=['','Algorithms/Information/Future Internet/Machines 等有可迁移方法文献，但本地目录中的方法借鉴文章不能替代同任务电力文章。Atmosphere、Remote Sensing、Symmetry 中现有样本主要来自其他任务，本轮保留为未校准。Mathematics、Sustainability、Processes 尚无本轮清单样本。','','新增样本需使用任务限定检索并核对摘要、数据与实验，而非仅命中 energy / power；例如 potential energy surface 不属于电力系统研究。']
    (OUT/'JOURNAL_COVERAGE.md').write_text('\n'.join(table),encoding='utf8')
    summary={'source_screened_papers':len(records),'journals_with_reviewed_samples':len(selected),'cohorts':len(cohorts),'verified_scope_and_page_observations':len(observations),'parser_discrepancies':len(discrepancies),'full_annotation_papers':0,'human_calibration_complete':False,'external_llm_calls':0,'source_manifest_sha256':hashlib.sha256((ROOT/'outputs/corpus_manifest.json').read_bytes()).hexdigest()}
    (OUT/'round_manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
