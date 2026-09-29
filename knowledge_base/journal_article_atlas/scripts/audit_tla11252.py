"""Conditional arithmetic check of printed metrics, not experiment reproduction."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'deconstruction/v1/papers/p_d564ed78dc6f82bd.json'


def implied_variance(r2, mse, rounding=0.0005):
    if mse < rounding or r2 + rounding >= 1:
        raise ValueError('Outside supported positive MSE and R2<1 domain')
    return {
        'point': mse / (1-r2),
        'rounding_interval': [(mse-rounding)/(1-r2+rounding),
                              (mse+rounding)/(1-r2-rounding)]
    }


def common_intersection(rows):
    intervals = [r['rounding_interval'] for r in rows]
    return max(i[0] for i in intervals) <= min(i[1] for i in intervals)


def audit(data):
    result = {
        'source_sha256': data['identity']['source_sha256'],
        'status': 'single_assistant_printed_arithmetic_pending_independent_review',
        'assumption': 'Same target vector, equal sample weights, pooled standard R2 and MSE; no per-household or per-period macro averaging.',
        'interpretation': 'Incompatibility under these assumptions needs aggregation/data clarification; does not establish fabrication or actual implementation error.',
        'rounding': 'Each printed three-decimal value allowed plus/minus 0.0005, inclusive conservative bounds.',
        'tables': {}
    }
    for table in data['tables']:
        if table['id'] not in ('2', '3'):
            continue
        rows = {name: implied_variance(values[0], values[2])
                for name, values in table['rows'].items()}
        result['tables'][table['id']] = {
            'physical_page': table['page'],
            'implied_target_variances': rows,
            'common_variance_possible_with_rounding': common_intersection(list(rows.values()))
        }
    return result


if __name__ == '__main__':
    data = json.loads(CASE.read_text(encoding='utf-8'))
    output = CASE.with_name(CASE.stem + '.numeric_audit.json')
    output.write_text(json.dumps(audit(data), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(output)
