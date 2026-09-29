"""Render traceable paragraph records and honest semantic-field gaps."""
import hashlib
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'deconstruction/v1/papers'
IDS=['p_71fe4f1acd7e01c5','p_654ca5ab287c1e14','p_61e82cc0ce8ee029']
EXTRA_FIELDS={
 'topic_sentence':'Source span of the topic sentence, including absent/implicit status',
 'secondary_functions':'Multiple rhetorical roles without splitting real source paragraphs',
 'sentence_map':'Sentence boundaries, counts, lengths and source spans',
 'claim_ids':'Atomic claims made by this paragraph',
 'evidence_links':'Source-linked equations, figures, tables, experiments and citations',
 'argument_edges':'supports/qualifies/contradicts/depends_on edges, distinct from reading order',
 'assumptions':'Stated or reviewer-identified assumptions, separately attributed',
 'claim_strength':'Observed/associated/causal/generalized wording versus actual support',
 'terminology':'Terms and consistency links; document frequency and per1000words after token review',
 'language':'Tense, voice, hedging, transitions and function-based sentence patterns',
 'scope_boundary':'Domain, time, population and engineering limits',
 'reuse_guidance':'Reusable rhetorical action and evidence requirement, not copied prose',
 'review_lineage':'Source, map, label version and independent review status'
}

def main():
    outputs=[]
    for pid in IDS:
        coverage=json.loads((BASE/(pid+'.coverage_audit.json')).read_text(encoding='utf8'))
        measured=BASE/(pid+'.paragraphs.json')
        if not measured.exists():
            outputs.append({'paper_id':pid,'paragraphs':None,'status':'full_paragraph_map_missing',
                            'text_partition_complete':coverage['text_partition_complete'],
                            'unassigned_lines':coverage['counts'].get('unassigned',0)})
            continue
        d=json.loads(measured.read_text(encoding='utf8'))
        mapping=BASE/(pid+'.paragraph_map.json')
        if hashlib.sha256(mapping.read_bytes()).hexdigest()!=d['map_sha256']:
            raise ValueError('Stale measurements: '+pid)
        if coverage['map_sha256']!=d['map_sha256']:
            raise ValueError('Stale coverage: '+pid)
        records=[]
        for i,p in enumerate(d['paragraphs']):
            records.append({**p,
                'source_sha256':d['source_sha256'],
                'previous_in_reading_order':d['paragraphs'][i-1]['id'] if i else None,
                'next_in_reading_order':d['paragraphs'][i+1]['id'] if i+1<len(d['paragraphs']) else None,
                'body_word_share':p['words']/d['summary']['body_words'],
                'semantic_fields':{key:{'status':'not_assessed','value':None} for key in EXTRA_FIELDS},
                'audit_note':'Reading order and word share are deterministic metadata, not inferred argument links.'})
        outputs.append({'paper_id':pid,'source_sha256':d['source_sha256'],
                        'text_partition_complete':coverage['text_partition_complete'],
                        'semantic_distillation_complete':False,'summary':d['summary'],
                        'role_distribution':dict(Counter(p['role_primary'] for p in records)),
                        'paragraphs':records})
    result={'schema':'information_paragraph_meta/1','new_field_dictionary':EXTRA_FIELDS,
            'status':'partial_semantics_with_explicit_coverage_audit','papers':outputs}
    target=ROOT/'deconstruction/v1/INFORMATION_PARAGRAPH_META.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    lines=['# Information逐段映射与元解构台账','',
           '每行绑定原文位置；词数沿用已声明tokenizer。新增语义字段尚待逐项标注，见配套JSON字段字典。',
           '阅读顺序不代表论证关系；文本分区闭合不代表所有科学字段已完成。','']
    for paper in outputs:
        lines.extend(['## '+paper['paper_id'],''])
        if paper['paragraphs'] is None:
            lines.extend(['全文逐段映射缺失；当前未归类提取行：'+str(paper['unassigned_lines'])+'。原有10个示例不能作为全篇段落分母。',''])
            continue
        lines.extend(['| 段ID | 章节 | 原文页/块/行（行区间左闭右开） | 类型 | 主要作用 | 词数 | 功能概括 |',
                      '|---|---|---|---|---|---:|---|'])
        for p in paper['paragraphs']:
            loc='; '.join(f"{s['page']}/{s['block_index']}/{s['line_range_half_open']}" for s in p['spans'])
            lines.append(f"| {p['id']} | {p['section_id']} | {loc} | {p['kind']} | {p['role_primary']} | {p['words']} | {p['functional_paraphrase'].replace('|','/')} |")
        lines.append('')
    target.with_suffix('.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print('Exported',sum(len(x['paragraphs'] or []) for x in outputs),'paragraph units; third map remains incomplete')

if __name__=='__main__':
    main()
