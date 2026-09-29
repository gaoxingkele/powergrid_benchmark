"""Descriptive finite differences from the published eight-condition table.

No raw observations, standard errors, significance tests or causal identification
are inferred from one aggregate number per condition.
"""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'deconstruction/v1/papers/p_82d41dafd52827e4.json'


def factorial_contrasts(configs, rows, factors, metrics):
    k = len(factors)
    expected = set(itertools.product((0, 1), repeat=k))
    if set(configs) != set(rows):
        raise ValueError('Configuration and metric identities must match')
    assignments = [tuple(x) for x in configs.values()]
    if len(set(assignments)) != len(assignments) or set(assignments) != expected:
        raise ValueError('Requires every binary cell exactly once')
    if any(len(values) != len(metrics) for values in rows.values()):
        raise ValueError('Metric width mismatch')
    cells = {tuple(configs[name]): (name, values) for name, values in rows.items()}
    conditional = []
    for axis, factor in enumerate(factors):
        for cell in sorted(expected):
            if cell[axis] != 0:
                continue
            other = list(cell)
            other[axis] = 1
            off_name, off = cells[cell]
            on_name, on = cells[tuple(other)]
            conditional.append({
                'factor': factor,
                'fixed': {factors[j]: cell[j] for j in range(k) if j != axis},
                'off': off_name, 'on': on_name,
                'on_minus_off': {m: round(b-a, 9) for m, a, b in zip(metrics, off, on)}
            })
    marginal = []
    for order in range(1, k+1):
        for axes in itertools.combinations(range(k), order):
            values = {}
            for j, metric in enumerate(metrics):
                total = sum(
                    (-1)**sum(1-cell[a] for a in axes)*cells[cell][1][j]
                    for cell in expected)
                values[metric] = round(total / 2**(k-order), 9)
            marginal.append({'factors': [factors[a] for a in axes],
                             'order': order, 'finite_difference': values})
    return {'conditional_effects': conditional, 'averaged_finite_differences': marginal}


def make_report():
    data = json.loads(CASE.read_text(encoding='utf-8'))
    table = next(t for t in data['tables'] if t['id'] == '5')
    experiment = next(e for e in data['experiments'] if e['id'] == 'E1')
    source = (CASE.parent / data['identity']['source_path']).resolve()
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual != data['identity']['source_sha256']:
        raise ValueError('Source PDF hash mismatch')
    return {
        'paper_id': data['paper_id'], 'doi': data['identity']['doi'],
        'source_sha256': actual, 'source_locator': {'physical_page': 19, 'table': '5'},
        'status': 'reviewer_descriptive_recalculation_pending_independent_review',
        'metrics': table['columns'],
        'units': {'RMSE': 'source-reported kW, physical scale unverified',
                  'MAE': 'source-reported kW, physical scale unverified',
                  'MAPE': 'percentage points', 'EVS': 'dimensionless', 'runtime_s': 'seconds'},
        'convention': 'On minus off; pair interactions are difference-in-differences averaged over the third factor. Three-way term is the difference of pair interactions. These are not regression coefficients under +/-1 coding.',
        'limitations': ['One printed aggregate per cell; no uncertainty can be estimated.',
                       'Rounding retained; no replication or actual implementation equivalence established.',
                       'Descriptive reviewer calculation, not author-reported factorial inference.',
                       'Metric definitions, data leakage boundaries and runtime scope remain unresolved in source case.'],
        **factorial_contrasts(experiment['config_map'], table['rows'],
                              experiment['factors'], table['columns'])
    }


if __name__ == '__main__':
    report = make_report()
    target = CASE.with_name(CASE.stem + '.factorial_audit.json')
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report['averaged_finite_differences'], ensure_ascii=False, indent=2))
