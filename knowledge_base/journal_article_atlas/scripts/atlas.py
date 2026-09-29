"""Local-only PDF inventory and candidate extraction. Never declares semantic verification."""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib
import html
import json
import math
import os
import re
import sqlite3
import statistics
import sys
import fitz
from definitions import ROOT, fields, STATUS

REPO = ROOT.parents[1]
OUT = ROOT/'outputs'
VENUES = {
 'applsci':'Applied Sciences','energies':'Energies','electronics':'Electronics',
 'information':'Information','algorithms':'Algorithms','mathematics':'Mathematics',
 'sensors':'Sensors','machines':'Machines','symmetry':'Symmetry','sustainability':'Sustainability',
 'processes':'Processes','remotesensing':'Remote Sensing','futureinternet':'Future Internet','atmosphere':'Atmosphere'
}
DOI_CODES = {'app':'Applied Sciences','en':'Energies','su':'Sustainability','s':'Sensors','math':'Mathematics','fi':'Future Internet','rs':'Remote Sensing','a':'Algorithms','info':'Information','sym':'Symmetry','atmos':'Atmosphere','pr':'Processes'}
POWER = re.compile(r'power|grid|electric|load.forecast|microgrid|energy|renewable|photovoltaic|wind.farm|battery|transmission|dispatch|voltage',re.I)
WORD = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*|\d+(?:\.\d+)?")
DOI = re.compile(r'10\.(?:3390/[a-z]+\d+|1109/ACCESS\.\d+\.\d+)',re.I)
CAPTION = re.compile(r'^(Figure|Fig\.|Table)\s+(\d+[a-z]?|[IVX]+)[.:\s]',re.I)
EQ = re.compile(r'^\((\d+[a-z]?)\)$')
HEADING = re.compile(r'^(\d{1,2}(?:\.\d+)*\.?|[IVX]+\.)\s+([A-Z][^\n]{2,100})$')
SIGNALS = {'bootstrap':r'bootstrap','confidence_interval':r'confidence interval',
 'hypothesis_test':r't.test|wilcoxon|mann.whitney|friedman|anova|p.value',
 'multiplicity':r'holm|bonferroni|false discovery', 'bayesian':r'bayesian|posterior',
 'ablation':r'ablation','sensitivity':r'sensitivity','uncertainty':r'uncertainty',
 'optimization':r'optimiza','graph':r'graph|GCN','deep_learning':r'neural|LSTM|transformer'}

def digest(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def percentile(xs,p):
    ys=sorted(xs); x=(len(ys)-1)*p; a=math.floor(x); b=math.ceil(x)
    return ys[a]+(ys[b]-ys[a])*(x-a)

def validate_observation(obs):
    definition = {r['field_id']:r for r in fields()}
    if obs['field_id'] not in definition: raise ValueError('unknown field')
    if obs['status'] not in STATUS: raise ValueError('unknown status')
    if obs['status'] not in STATUS[:2]:
        if obs['value'] is not None: raise ValueError('missing values must be null')
    elif obs['value'] is None or not obs['evidence']:
        raise ValueError('observed values require value and evidence')
    else:
        for ev in obs['evidence']:
            if not re.fullmatch(r'[a-fA-F0-9]{64}',ev.get('source_sha256','')) or not isinstance(ev.get('locator'),dict):
                raise ValueError('invalid source anchor')
        typ=definition[obs['field_id']]['type']; v=obs['value']
        expected={'integer':int,'number':(int,float),'string':str,'array':list,'object':dict}[typ]
        if not isinstance(v,expected) or (typ in ['integer','number'] and isinstance(v,bool)):
            raise ValueError('wrong field type')
    return True

def infer_venue(path, doi):
    if doi and '/ACCESS.' in doi.upper(): return 'IEEE Access'
    if doi and doi.lower().startswith('10.3390/'):
        code=re.search(r'/([a-z]+)',doi.lower())[1]
        if code in DOI_CODES: return DOI_CODES[code]
        if code in VENUES: return VENUES[code]
    for part in reversed(path.parts):
        normalized=re.sub(r'[^a-z]','',part.lower().removeprefix('mdpi-'))
        for k,v in VENUES.items():
            if normalized in {k,re.sub(r'[^a-z]','',v.lower())}: return v
        if normalized=='ieeeaccess': return 'IEEE Access'
    return None

def source_paths():
    roots=[Path('D:/aicoding/papers'),REPO/'papers/literature']
    excluded={'author_own_publications_5','.git','__pycache__','node_modules'}
    for root in roots:
        if not root.exists(): continue
        for folder,dirs,files_ in os.walk(root,followlinks=False):
            dirs[:]=[d for d in dirs if d not in excluded and not Path(folder,d).is_junction() and not Path(folder,d).is_symlink()]
            for name in sorted(files_):
                if name.lower().endswith('.pdf'): yield Path(folder,name)

def extract(path,sha):
    with fitz.open(path) as doc:
        if doc.is_encrypted: raise ValueError('encrypted PDF')
        first=doc[0].get_text() if len(doc) else ''
        match=DOI.search(first)
        doi=match[0] if match else None
        venue=infer_venue(path,doi)
        if not venue: return None
        title=(doc.metadata.get('title') or '').strip()
        title_origin='pdf_metadata'
        if len(title)<15 or title.lower() in {'untitled','manuscript'}:
            title=re.sub(r'^\d{4}_','',path.stem); title_origin='filename_fallback'
        pid='p_'+sha[:16]
        objects=[]; heads=[]; caps={'figure':{},'table':{}}; equations={}; blocks=[]; lines=[]
        for pn,page in enumerate(doc,1):
            for b in page.get_text('blocks',sort=True):
                if b[6]!=0: continue
                text=b[4].strip()
                if not text: continue
                bbox=[round(v,2) for v in b[:4]]
                record={'page':pn,'bbox':bbox,'text':text}
                blocks.append(record)
                for line in text.splitlines():
                    s=line.strip(); lines.append({'page':pn,'text':s,'bbox':bbox})
                    cap=CAPTION.match(s)
                    if cap:
                        kind='table' if cap[1].lower()=='table' else 'figure'
                        label=cap[2]
                        caps[kind].setdefault(label,[]).append({'page':pn,'bbox':bbox,'caption_candidate':s[:240]})
                    eq=EQ.fullmatch(s)
                    if eq: equations.setdefault(eq[1],[]).append({'page':pn,'bbox':bbox})
                    head=HEADING.match(s)
                    if head and len(WORD.findall(s))<=16:
                        level=1 if re.match('[IVX]',head[1]) else len(head[1].rstrip('.').split('.'))
                        heads.append({'label':head[1],'heading_candidate':head[2],'level':level,'page':pn,'bbox':bbox})
        text='\n'.join(r['text'] for r in lines)
        # Crop text using actual heading candidates, not a prose occurrence of "introduction".
        intro=[i for i,r in enumerate(lines) if re.match(r'^(?:1\.?|I\.)\s+Introduction\s*$',r['text'],re.I)]
        refs=[i for i,r in enumerate(lines) if re.match(r'^(?:(?:\d+\.?|[IVX]+\.)\s+)?References\s*$',r['text'],re.I)]
        body_lines=lines[intro[0]:refs[-1]] if intro and refs and refs[-1]>intro[0] else []
        body='\n'.join(r['text'] for r in body_lines)
        body_page_start=body_lines[0]['page'] if body_lines else None
        body_page_end=body_lines[-1]['page'] if body_lines else None
        prose=[]
        for b in blocks:
            s=' '.join(b['text'].split()); words=WORD.findall(s)
            if body_page_start and body_page_start<=b['page']<=body_page_end and len(words)>=25 and not CAPTION.match(s):
                # Proxy only: not a validated paragraph or body boundary.
                prose.append({'page':b['page'],'bbox':b['bbox'],'words':len(words),'text_preview':s[:180]})
        abstract=re.search(r'\bAbstract\s*[:—–-]?\s*(.+?)(?:\bKeywords\s*:|\bIndex Terms\s*[:—–-])',first,re.S|re.I)
        abstract_words=len(WORD.findall(abstract[1])) if abstract else None
        signal_source=body or text
        signals={key:bool(re.search(pattern,signal_source,re.I)) for key,pattern in SIGNALS.items()}
        lengths=[p['words'] for p in prose]
        metrics={'pages':len(doc),'numbered_equation_label_candidates':len(equations),
          'figure_label_candidates':len(caps['figure']),'table_label_candidates':len(caps['table']),
          'section_heading_candidates':len(heads),'l1_heading_candidates':sum(h['level']==1 for h in heads),
          'body_text_block_candidates':len(prose) if body else None,
          'mean_words_per_body_block_candidate':round(statistics.mean(lengths),2) if lengths else None,
          'body_word_candidates':len(WORD.findall(body)) if body else None,
          'abstract_word_candidates':abstract_words}
        # Preserve all labels/positions rather than pretending a maximum label is a count.
        for kind,collection in [('figure',caps['figure']),('table',caps['table']),('equation',equations)]:
            for label,spans in collection.items():
                objects.append({'entity_id':f'{pid}:{kind}:{label}','entity_type':kind,'status':'automatic_candidate','label':label,'evidence':spans})
        for kind,collection in [('section',heads),('paragraph',prose)]:
            for index,item in enumerate(collection,1):
                objects.append({'entity_id':f'{pid}:{kind}:{index}','entity_type':kind,'status':'automatic_candidate',**item})
        years=re.findall(r'\b(20(?:1\d|2\d))\b',first)
        record={'paper_id':pid,'title':title,'title_origin':title_origin,'authors':[],'year':None,
          'year_candidates':sorted(set(years)),'venue':venue,'doi':doi,'citation_count':None,
          'full_text_status':'unknown','local_pdf_status':'readable_rights_not_rechecked','code_url':None,
          'source_platforms':['local_pdf'],'fetched_at':'2026-09-13','source_path':str(path.resolve()),
          'source_sha256':sha,'duplicate_paths':[], 'relevance_candidate':'direct_keyword_match' if POWER.search(title) else 'uncertain',
          'article_type_candidate':'review' if re.search(r'\breview\b|\bsurvey\b',title,re.I) else 'unclassified',
          'measurement_status':'automatic_candidate','metrics':metrics,'signals_NOT_validated_methods':signals,
          'difficulty':None,'quality':None,'objects':objects,
          'read_integrity':'not_assessed; page anchors are parser candidates, not certified',
          'parser':str(fitz.version),'body_boundary_found':bool(body)}
        terms=Counter(w.lower() for w in WORD.findall(body) if len(w)>3 and not w.isnumeric())
        record['term_counts_body_candidate']=dict(terms.most_common(100))
        patterns=json.loads((ROOT/'dictionary/language_patterns.json').read_text(encoding='utf-8'))
        record['language_pattern_candidates']={}
        for pat in patterns['patterns']:
            hits=[{'page':r['page'],'bbox':r['bbox']} for r in body_lines if re.search(pat['cue_regex'],r['text'],re.I)]
            if hits: record['language_pattern_candidates'][pat['id']]={'line_cue_hits':len(hits),'locators':hits}
        return record

def summaries(rows):
    groups=defaultdict(list)
    for r in rows:
        key=(r['venue'],r['relevance_candidate'],r['article_type_candidate'])
        groups[key].append(r)
    result=[]
    for key,items in sorted(groups.items()):
        stats={}
        for name in items[0]['metrics']:
            vals=[r['metrics'][name] for r in items if r['metrics'][name] is not None]
            stats[name]={'n_total':len(items),'n_valid_candidates':len(vals),'n_verified':0,
              'missing':len(items)-len(vals),'mean':statistics.mean(vals) if vals else None,
              'median':statistics.median(vals) if vals else None,'sd':statistics.stdev(vals) if len(vals)>1 else None,
              'p25':percentile(vals,.25) if vals else None,'p75':percentile(vals,.75) if vals else None,
              'p10':percentile(vals,.1) if vals else None,'p90':percentile(vals,.9) if vals else None,
              'min':min(vals) if vals else None,'max':max(vals) if vals else None}
        result.append({'journal':key[0],'relevance_stratum':key[1],'article_type_stratum':key[2],
          'n':len(items),'sampling':'local_convenience; article type and relevance not adjudicated',
          'status':'EXPLORATORY_AUTOMATIC_NOT_JOURNAL_STANDARD','metrics':stats,
          'difficulty_profile':None,'quality_profile':None,'verified_profile':None})
    return result

def database(rows):
    con=sqlite3.connect(OUT/'atlas.sqlite'); con.execute('PRAGMA foreign_keys=ON')
    # Only generated atlas tables are rebuilt; never connects to a source-paper database.
    for table in ['observation','relation','entity','paper','field_definition','taxonomy_node','cohort_profile']:
        con.execute(f'DROP TABLE IF EXISTS {table}')
    con.executescript('''
CREATE TABLE paper(paper_id TEXT PRIMARY KEY, journal TEXT, title TEXT, doi TEXT, sha256 TEXT UNIQUE, source_path TEXT, status TEXT);
CREATE TABLE entity(entity_id TEXT PRIMARY KEY, paper_id TEXT REFERENCES paper(paper_id), entity_type TEXT, record_json TEXT);
CREATE TABLE field_definition(field_id TEXT PRIMARY KEY, definition_json TEXT);
CREATE TABLE observation(observation_id INTEGER PRIMARY KEY, entity_id TEXT REFERENCES entity(entity_id), field_id TEXT REFERENCES field_definition(field_id), value_json TEXT, status TEXT, evidence_json TEXT, method TEXT, annotator TEXT, version TEXT);
CREATE TABLE relation(relation_id TEXT PRIMARY KEY, source_entity TEXT REFERENCES entity(entity_id), target_entity TEXT REFERENCES entity(entity_id), relation_type TEXT, evidence_json TEXT, status TEXT);
CREATE TABLE taxonomy_node(taxonomy TEXT, path TEXT, PRIMARY KEY(taxonomy,path));
CREATE TABLE cohort_profile(cohort_id INTEGER PRIMARY KEY, profile_json TEXT);
''')
    for f in fields(): con.execute('INSERT INTO field_definition VALUES (?,?)',(f['field_id'],json.dumps(f,ensure_ascii=False)))
    from definitions import TAXONOMIES
    def walk(value,path):
        if isinstance(value,dict):
            for k,v in value.items(): yield from walk(v,path+[k])
        else:
            for item in value: yield '/'.join(path+[item])
    for tax,tree in TAXONOMIES.items():
        for path in walk(tree,[]): con.execute('INSERT INTO taxonomy_node VALUES (?,?)',(tax,path))
    mapping={'pages':'pages','equation_count_numbered':'numbered_equation_label_candidates','figure_count':'figure_label_candidates',
      'table_count':'table_label_candidates','section_count_all':'section_heading_candidates','section_count_l1':'l1_heading_candidates'}
    for r in rows:
        pid=r['paper_id']; con.execute('INSERT INTO paper VALUES (?,?,?,?,?,?,?)',(pid,r['venue'],r['title'],r['doi'],r['source_sha256'],r['source_path'],r['measurement_status']))
        con.execute('INSERT INTO entity VALUES (?,?,?,?)',(pid,pid,'paper',json.dumps({'paper_id':pid})))
        for obj in r['objects']: con.execute('INSERT INTO entity VALUES (?,?,?,?)',(obj['entity_id'],pid,obj['entity_type'],json.dumps(obj,ensure_ascii=False)))
        for f in fields():
            if f['entity']!='paper': continue
            name=f['field_id'].split('.')[1]
            value=r['metrics'].get(mapping.get(name,''))
            status='automatic_candidate' if name in mapping else 'not_assessed'
            ev=[{'source_sha256':r['source_sha256'],'locator':{'source_path':r['source_path'],'scope':'full_pdf_candidate_scan'},'note':'object-level candidate locations in entity records'}] if status=='automatic_candidate' else []
            obs={'entity_id':pid,'field_id':f['field_id'],'value':value,'status':status,'evidence':ev,'method':'pdf_label_heuristic_v0.1','annotator':None,'version':'0.1'}
            validate_observation(obs)
            con.execute('INSERT INTO observation(entity_id,field_id,value_json,status,evidence_json,method,annotator,version) VALUES (?,?,?,?,?,?,?,?)',
              (pid,f['field_id'],json.dumps(value),status,json.dumps(ev),'pdf_label_heuristic_v0.1',None,'0.1'))
    for profile in summaries(rows): con.execute('INSERT INTO cohort_profile(profile_json) VALUES (?)',(json.dumps(profile,ensure_ascii=False),))
    con.executescript('''
DROP VIEW IF EXISTS paper_comparison;
CREATE VIEW paper_comparison AS SELECT p.paper_id,p.journal,p.title,p.doi,
MAX(CASE WHEN o.field_id='paper.pages' THEN o.value_json END) AS pages_candidate,
MAX(CASE WHEN o.field_id='paper.equation_count_numbered' THEN o.value_json END) AS equations_candidate,
MAX(CASE WHEN o.field_id='paper.figure_count' THEN o.value_json END) AS figures_candidate,
MAX(CASE WHEN o.field_id='paper.table_count' THEN o.value_json END) AS tables_candidate,
p.status FROM paper p LEFT JOIN observation o ON p.paper_id=o.entity_id GROUP BY p.paper_id;
''')
    assert not con.execute('PRAGMA foreign_key_check').fetchall()
    con.commit(); con.close()

def main():
    OUT.mkdir(exist_ok=True)
    rows=[]; by_hash={}; by_doi={}; errors=[]; duplicate_versions=[]; scanned=0
    for p in sorted(source_paths()):
        scanned+=1
        try:
            sha=digest(p)
            if sha in by_hash:
                if by_hash[sha] is not None: by_hash[sha]['duplicate_paths'].append(str(p.resolve()))
                continue
            row=extract(p,sha)
            by_hash[sha]=row
            if row:
                key=(row['doi'] or '').lower()
                if key and key in by_doi:
                    duplicate_versions.append({'doi':key,'retained':by_doi[key]['source_path'],'alternative':row['source_path'],'sha256':sha,'status':'version_selection_needs_review'})
                else:
                    rows.append(row)
                    if key: by_doi[key]=row
        except Exception as exc: errors.append({'path':str(p),'error':str(exc)})
    rows.sort(key=lambda r:(r['venue'],r['title']))
    corpus_manifest={'version':'0.1','sampling':'local_convenience','selection_status':'candidate_pool_not_adjudicated',
      'source_roots':['D:/aicoding/papers',str(REPO/'papers/literature')],
      'articles':[{k:r[k] for k in ['paper_id','title','venue','doi','source_path','source_sha256','duplicate_paths','relevance_candidate','article_type_candidate']} for r in rows]}
    manifest_path=OUT/'corpus_manifest.json'
    manifest_path.write_text(json.dumps(corpus_manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'articles.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    profiles=summaries(rows)
    (OUT/'cohort_profiles.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2),encoding='utf-8')
    database(rows)
    heads=['期刊','题目','相关性候选','页数','公式标签候选','图标签候选','表标签候选','标题候选','正文块候选','平均块词数','摘要词候选','难度']
    table=[]
    for r in rows:
        m=r['metrics']; vals=[r['venue'],r['title'],r['relevance_candidate'],m['pages'],m['numbered_equation_label_candidates'],m['figure_label_candidates'],m['table_label_candidates'],m['section_heading_candidates'],m['body_text_block_candidates'],m['mean_words_per_body_block_candidate'],m['abstract_word_candidates'],'未评定']
        table.append('<tr>'+''.join('<td>'+html.escape(str(v) if v is not None else '解析缺失/未评估')+'</td>' for v in vals)+'</tr>')
    page='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>Journal Article Atlas</title>
<style>body{font:15px system-ui;margin:28px;color:#183047}h1{font-size:25px}.notice{padding:16px;background:#fff3cd}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd6de;padding:8px;text-align:left}th{position:sticky;top:0;background:#e4eef5}tr:nth-child(even){background:#f7fafc}input{padding:10px;margin:15px 0;width:400px}</style>
<h1>论文解构对照表 · 自动候选版</h1><div class="notice">不是期刊录用标准。公式/图表是标签候选，段落是PDF文字块代理；0 不能解释为人工确认不存在。难度、实验设计数、消融数与语义逻辑尚待核验。完整211字段与关系模式见字典和JSON/SQLite。</div>
<input id="filter" placeholder="筛选期刊 / 题目 / 相关性"><table><thead><tr>'''+''.join('<th>'+h+'</th>' for h in heads)+'</tr></thead><tbody>'+''.join(table)+'''</tbody></table><script>document.querySelector('#filter').oninput=e=>document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.innerText.toLowerCase().includes(e.target.value.toLowerCase()));</script></html>'''
    (OUT/'paper_comparison.html').write_text(page,encoding='utf-8')
    df=defaultdict(Counter)
    for r in rows:
        if r['relevance_candidate']=='direct_keyword_match': df[r['venue']].update(r['term_counts_body_candidate'].keys())
    lexical={v:{term:n for term,n in cnt.most_common(60) if n>=3} for v,cnt in df.items()}
    (OUT/'term_document_frequency_candidates.json').write_text(json.dumps({'status':'automatic_token_candidates_NOT_curated_terminology','journals':lexical},ensure_ascii=False,indent=2),encoding='utf-8')
    pattern_df=defaultdict(Counter)
    for r in rows:
        if r['relevance_candidate']=='direct_keyword_match': pattern_df[r['venue']].update(r['language_pattern_candidates'].keys())
    (OUT/'language_function_candidates.json').write_text(json.dumps({'status':'line_cue_document_frequency_NOT_verified_sentence_functions','journals':{k:dict(v) for k,v in pattern_df.items()}},ensure_ascii=False,indent=2),encoding='utf-8')
    report={'date':'2026-09-13','pdf_files_scanned':scanned,'selected_unique_article_candidates':len(rows),
      'journal_counts':dict(Counter(r['venue'] for r in rows)),
      'power_keyword_candidates':sum(r['relevance_candidate']=='direct_keyword_match' for r in rows),
      'errors':errors,'doi_version_collisions':duplicate_versions,'schema_fields':len(fields()),
      'semantic_annotations_verified':0,'difficulty_ratings_verified':0,'external_llm_calls':0,
      'parser':str(fitz.version),'sampling':'local convenience; metadata/rights/versions not fully reverified'}
    report['corpus_manifest_sha256']=digest(manifest_path)
    report['implementation_sha256']={p.name:digest(p) for p in [Path(__file__),ROOT/'scripts/definitions.py',ROOT/'dictionary/language_patterns.json']}
    (OUT/'run_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    md=['# 本轮实测与完成状态','',f"扫描 {scanned} 个本地 PDF 文件；保留 {len(rows)} 篇去重文章候选；标题命中电力/能源关键词 {report['power_keyword_candidates']} 篇。",'',
      f"字段定义 {len(fields())} 项。正式语义核验 0 篇，正式难度评分 0 篇；不要将候选值用于录用水平推断。",'',
      '| 期刊 | 候选数 |','|---|---|']
    md += [f'| {k} | {v} |' for k,v in sorted(report['journal_counts'].items())]
    md += ['',f'解析错误 {len(errors)} 项；同 DOI 不同文件 {len(duplicate_versions)} 组，保留待复核版本映射。', '',
      '已生成：字段字典、分类树、元模式、文章和对象候选 JSON、关系数据库、按期刊/相关性/类型的候选统计、可筛选 HTML、词项文档频率候选。',
      '未完成：逐段语义核验、真实公式/实验/消融计数校准、统计适当性和理论评分、跨章节人工逻辑图、双评一致性、正式样本画像。执行路径见 ../EXECUTION_PLAN.md。']
    (OUT/'RUN_REPORT.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['errors','doi_version_collisions']},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
